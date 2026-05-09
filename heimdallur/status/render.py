from __future__ import annotations
import asyncio
import os
import time
from datetime import datetime
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
    c = colors[status]
    i = icons[status]
    return f"[{c}]{i}  {ms}[/]"


def _check_counts(ok: int, total: int) -> str:
    c = GREEN if ok == total else (AMBER if ok > 0 else RED)
    return f"[{c}]{ok}/{total}[/]"


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

    console.print(f"\n[bold]HEIMDALLUR[/]  {datetime.now().strftime('%H:%M:%S')}\n")

    # ── Internet ─────────────────────────────────────────────────────────
    ont = state.ont_result
    console.print(f"[bold]INTERNET[/]  {_status_str(ont.status if ont else None, ont.response_ms if ont else None)}")

    if iq:
        ip_ok   = sum(1 for r in iq.raw_ip if r.status == ProbeStatus.HEALTHY)
        dns_ok  = sum(1 for r in iq.dns    if r.success)
        http_ok = sum(1 for r in iq.http   if r.success)
        checks = (
            f"IP {_check_counts(ip_ok, len(iq.raw_ip))}"
            f"  ·  DNS {_check_counts(dns_ok, len(iq.dns))}"
            f"  ·  HTTP {_check_counts(http_ok, len(iq.http))}"
        )
        console.print(f"  {checks}")

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

    problems = state.problems(config)
    if problems:
        console.print("\n[bold yellow]PROBLEMS[/]")
        for p in problems:
            console.print(f"  [red]✗[/]  {p}")
    else:
        console.print("\n[green]All monitored devices OK[/]")

    total, ok, bad = state.summary(config)
    console.print(f"\n[{GRAY}]{total} monitored  ·  {ok} OK  ·  {bad} down[/]\n")
