from __future__ import annotations
import asyncio
import os
import time
from datetime import datetime, timezone
from rich.console import Console
from heimdallur.config.loader import load_config
from heimdallur.core.topology import ProbeStatus

GREEN = "green"
AMBER = "yellow"
RED   = "red"
GRAY  = "dim"


def _status_str(status: ProbeStatus | None, response_ms: float | None) -> str:
    if status is None:
        return f"[{GRAY}]unknown[/]"
    ms = f"{response_ms:.0f}ms" if response_ms is not None else "timeout"
    colors = {
        ProbeStatus.HEALTHY:     GREEN,
        ProbeStatus.DEGRADED:    AMBER,
        ProbeStatus.UNREACHABLE: RED,
        ProbeStatus.UNKNOWN:     GRAY,
    }
    icons = {
        ProbeStatus.HEALTHY:     "✓",
        ProbeStatus.DEGRADED:    "~",
        ProbeStatus.UNREACHABLE: "✗",
        ProbeStatus.UNKNOWN:     "·",
    }
    labels = {
        ProbeStatus.HEALTHY:     "Online",
        ProbeStatus.DEGRADED:    "Degraded",
        ProbeStatus.UNREACHABLE: "Offline",
        ProbeStatus.UNKNOWN:     "Unknown",
    }
    c = colors[status]
    i = icons[status]
    lbl = labels[status]
    return f"[{c}]{i} {lbl}  {ms}[/]"


def _check_counts(ok: int, total: int) -> str:
    c = GREEN if ok == total else (AMBER if ok > 0 else RED)
    return f"[{c}]{ok}/{total}[/]"


def _internet_diagnosis(iq) -> tuple[str, str]:
    ip_ok   = sum(1 for r in iq.raw_ip if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED))
    ip_tot  = len(iq.raw_ip)
    dns_ok  = sum(1 for r in iq.dns  if r.success)
    dns_tot = len(iq.dns)
    http_ok  = sum(1 for r in iq.http if r.success)
    http_tot = len(iq.http)

    if ip_tot > 0 and ip_ok == 0:
        return RED,   "No IP connectivity — likely ISP outage"
    if ip_ok == ip_tot and dns_tot > 0 and dns_ok == 0:
        return AMBER, "All DNS failing — ISP resolver issue — try manual DNS (8.8.8.8)"
    if 0 < ip_ok < ip_tot:
        return AMBER, "Some IP paths degraded — routing or congestion issue"
    if 0 < dns_ok < dns_tot:
        return AMBER, "Some DNS resolvers failing — upstream issue, not your line"
    if http_tot > 0 and http_ok == 0 and ip_ok == ip_tot and dns_ok == dns_tot:
        return AMBER, "All HTTP failing with healthy IP/DNS — possible firewall issue"
    if 0 < http_ok < http_tot:
        return AMBER, "Some HTTP checks failing — likely destination issue, not your connection"
    return GREEN, "All paths healthy"


def _latency_qualifier(avg_ms: float) -> tuple[str, str]:
    if avg_ms < 50:  return GREEN, "excellent"
    if avg_ms < 100: return AMBER, "elevated"
    return RED, "degraded"


def _speed_age(ts: float) -> str:
    secs = int(time.time() - ts)
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    return f"{secs // 3600}h ago"


async def render_status(console: "Console | None" = None) -> None:
    config = load_config()

    if os.getenv("NETWATCH_MOCK"):
        from pathlib import Path
        from heimdallur.mock.network import MockProber
        scenario = os.getenv("NETWATCH_MOCK_SCENARIO")
        prober = MockProber(config, scenario_path=Path(scenario) if scenario else None)
        state = await prober.probe_all()
        iq = prober.mock_internet_quality()
        speed = prober.mock_speed_result()
    else:
        from heimdallur.core.prober import Prober
        from heimdallur.core.internet_probe import InternetProber
        prober = Prober(config)
        inet_prober = InternetProber()
        state, iq = await asyncio.gather(prober.probe_all(), inet_prober.probe_all())
        speed = None

    if console is None:
        console = Console()

    probe_dt = datetime.fromtimestamp(state.timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    console.print(f"\n[bold]HEIMDALLUR[/]  {probe_dt}\n")

    # ── Internet ─────────────────────────────────────────────────────────
    ont = state.ont_result
    ont_str = _status_str(ont.status if ont else None, ont.response_ms if ont else None)
    qualifier = ""
    if ont and ont.response_ms is not None:
        q_c, q_s = _latency_qualifier(ont.response_ms)
        qualifier = f"  [{q_c}]{q_s}[/]"
    console.print(f"[bold]INTERNET[/]  {ont_str}{qualifier}")

    if iq:
        ip_ok   = sum(1 for r in iq.raw_ip if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED))
        dns_ok  = sum(1 for r in iq.dns    if r.success)
        http_ok = sum(1 for r in iq.http   if r.success)
        checks = (
            f"IP {_check_counts(ip_ok, len(iq.raw_ip))}"
            f"  ·  DNS {_check_counts(dns_ok, len(iq.dns))}"
            f"  ·  HTTP {_check_counts(http_ok, len(iq.http))}"
        )
        console.print(f"  {checks}")
        diag_c, diag_msg = _internet_diagnosis(iq)
        console.print(f"  [{diag_c}]{diag_msg}[/]")

    if speed and speed.ok:
        console.print(f"  [{GRAY}]↓ {speed.download_mbps:.0f} Mbps  ·  ping {speed.ping_ms:.0f} ms  ({_speed_age(speed.timestamp)})[/]")

    console.print("")

    # ── Home Network ─────────────────────────────────────────────────────
    rtr = state.router_result
    console.print(f"[bold]HOME NETWORK[/]")
    console.print(f"  ROUTER  {_status_str(rtr.status if rtr else None, rtr.response_ms if rtr else None)}")

    for group in config.groups:
        if group.gateway_ip:
            r = state.gateway_results.get(group.gateway_ip)
            console.print(f"  {_status_str(r.status if r else None, r.response_ms if r else None)}  {group.name}")
        else:
            console.print(f"  [{GRAY}]LAN[/]  {group.name}")

    problems = state.problems(config)
    if problems:
        console.print("\n[bold yellow]PROBLEMS[/]")
        for p in problems:
            console.print(f"  [red]✗[/]  {p}")
    else:
        console.print("\n[green]All monitored devices OK[/]")

    total, ok, bad = state.summary(config)
    console.print(f"\n[{GRAY}]{total} monitored  ·  {ok} OK  ·  {bad} down[/]\n")
