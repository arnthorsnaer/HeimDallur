"""Render current network state as a self-contained markdown document.

The file at _DEFAULT_REPORT is rewritten after every probe cycle by the TUI app
so that agents/scripts can read it instantly without running a fresh probe.
"""
from __future__ import annotations

import asyncio
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from heimdallur.tui.app import EnrichedState, HistorySnapshot
    from heimdallur.core.topology import NetworkConfig

_DEFAULT_REPORT = Path.home() / ".local" / "share" / "heimdallur" / "status.md"

_STATUS_ICON = {
    "healthy":     "✅",
    "degraded":    "⚠️",
    "unreachable": "❌",
    "unknown":     "❓",
}


def _icon(status_value: str | None) -> str:
    return _STATUS_ICON.get(status_value or "unknown", "❓")


def _ms(v: float | None) -> str:
    if v is None:
        return "—"
    return f"{v:.0f} ms"


def _avg_ms(history: list[float]) -> str:
    if not history:
        return "—"
    return f"{mean(history):.0f} ms"


def _pct(history: list[float]) -> str:
    if not history:
        return "—"
    return f"{mean(history) * 100:.0f}%"


def _loss_pct(history: list[float]) -> str:
    if not history:
        return "0%"
    pct = mean(history) * 100
    return f"{pct:.0f}%"


def _ago(ts: float) -> str:
    secs = int(time.time() - ts)
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    h = secs // 3600
    m = (secs % 3600) // 60
    return f"{h}h {m}m ago" if m else f"{h}h ago"


def _uptime_str(seconds: float) -> str:
    d = int(seconds // 86400)
    h = int((seconds % 86400) // 3600)
    m = int((seconds % 3600) // 60)
    parts = []
    if d:
        parts.append(f"{d}d")
    if h:
        parts.append(f"{h}h")
    if m or not parts:
        parts.append(f"{m}m")
    return " ".join(parts)


def render_markdown(
    enriched: "EnrichedState",
    snapshot: "HistorySnapshot",
    config: "NetworkConfig",
) -> str:
    from heimdallur.core.internet_probe import IP_TARGETS, DNS_TARGETS, HTTP_TARGETS
    from heimdallur.core.topology import ProbeStatus

    state = enriched.network
    lines: list[str] = []

    probed_at = datetime.fromtimestamp(state.timestamp, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines += [
        "# Heimdallur Network Status",
        "",
        f"**Probed:** {probed_at}  |  **Interval:** {config.probe_interval_seconds}s",
        "",
    ]

    # ── Summary ──────────────────────────────────────────────────────────
    problems = state.problems(config)
    total, ok, bad = state.summary(config)
    lines.append("## Summary")
    lines.append("")
    if not problems:
        lines.append(f"✅ All systems healthy — {ok} / {total} devices online")
    else:
        lines.append(f"⚠️  {len(problems)} issue(s) detected — {ok} / {total} devices online")
        lines.append("")
        for p in problems:
            lines.append(f"- {p}")
    lines += ["", "---", ""]

    # ── Internet ─────────────────────────────────────────────────────────
    lines.append("## Internet")
    lines.append("")
    ont = state.ont_result
    if ont:
        icon = _icon(ont.status.value)
        avg = _avg_ms(snapshot.ont_lat)
        loss = _loss_pct(snapshot.ont_loss)
        lines.append(f"**Status:** {icon} {ont.status.value.upper()}  |  **Latency (ONT):** {avg} avg  |  **Loss:** {loss}")
    else:
        lines.append("**Status:** ❓ unknown")
    lines.append("")

    if enriched.internet_quality:
        iq = enriched.internet_quality

        if iq.raw_ip:
            lines.append("### IP Reachability")
            lines.append("")
            lines.append("| Target | Status | Latency |")
            lines.append("|--------|--------|---------|")
            for r in iq.raw_ip:
                icon = _icon(r.status.value)
                lat_avg = _avg_ms(snapshot.inet_ip_lat.get(r.target, []))
                lines.append(f"| {r.label} ({r.target}) | {icon} {r.status.value} | {lat_avg} |")
            lines.append("")

        if iq.dns:
            lines.append("### DNS")
            lines.append("")
            lines.append("| Resolver | Status | Lookup |")
            lines.append("|----------|--------|--------|")
            for r in iq.dns:
                icon = "✅" if r.success else "❌"
                lat_avg = _avg_ms(snapshot.inet_dns_lat.get(r.hostname, []))
                lines.append(f"| {r.label} ({r.hostname}) | {icon} {'ok' if r.success else 'fail'} | {lat_avg} |")
            lines.append("")

        if iq.http:
            lines.append("### HTTP")
            lines.append("")
            lines.append("| Endpoint | Status | TTFB | Total |")
            lines.append("|----------|--------|------|-------|")
            for r in iq.http:
                icon = "✅" if r.success else "❌"
                ttfb = _avg_ms(snapshot.inet_http_ttfb.get(r.url, []))
                total_t = _avg_ms(snapshot.inet_http_total.get(r.url, []))
                lines.append(f"| {r.label} | {icon} {'ok' if r.success else 'fail'} | {ttfb} | {total_t} |")
            lines.append("")

    spd = enriched.speed_result
    if spd and spd.ok:
        lines.append(f"**Speed test:** ↓ {spd.download_mbps:.0f} Mbps  |  ping {spd.ping_ms:.0f} ms  *({_ago(spd.timestamp)})*")
    else:
        lines.append("**Speed test:** not yet run")
    lines += ["", "---", ""]

    # ── Router ───────────────────────────────────────────────────────────
    lines.append("## Router")
    lines.append("")
    rtr = state.router_result
    if rtr:
        icon = _icon(rtr.status.value)
        lat = _ms(rtr.response_ms)
        lines.append(f"**Status:** {icon} {rtr.status.value.upper()}  |  **Latency:** {lat}")
    if enriched.router_stats:
        rs = enriched.router_stats
        lines.append(
            f"**CPU:** {rs.cpu_pct:.0f}%  |  **Memory:** {rs.memory_pct:.0f}%  |  "
            f"**Uptime:** {_uptime_str(rs.uptime_seconds)}"
        )
    lines += ["", "---", ""]

    # ── Groups ───────────────────────────────────────────────────────────
    lines.append("## Groups")
    lines.append("")
    for group in config.groups:
        band_info = ""
        if group.type == "wifi":
            parts = []
            if group.band:
                parts.append(group.band)
            if group.channel:
                parts.append(f"ch {group.channel}")
            if parts:
                band_info = "  |  " + "  ".join(parts)

        lines.append(f"### {group.name}{band_info}")
        lines.append("")

        if group.gateway_ip:
            gw_r = state.gateway_results.get(group.gateway_ip)
            gw_icon = _icon(gw_r.status.value if gw_r else "unknown")
            gw_lat = _ms(gw_r.response_ms if gw_r else None)
            enr = enriched.gw_enrichment.get(group.gateway_ip)
            enr_parts = [f"**Gateway `{group.gateway_ip}`:** {gw_icon} {gw_lat}"]
            if enr:
                if enr.client_count is not None:
                    enr_parts.append(f"**Clients:** {enr.client_count}")
                if enr.signal_dbm is not None:
                    enr_parts.append(f"**Signal:** {enr.signal_dbm} dBm")
            lines.append("  |  ".join(enr_parts))
            lines.append("")

        devices = config.devices_in_group(group.id)
        gw_up = state.gateway_up(group)
        online = sum(
            1 for d in devices
            if (r := state.device_results.get(d.ip)) and r.status.value in ("healthy", "degraded")
        )
        lines.append(f"**Devices:** {online} / {len(devices)} online")
        lines.append("")

        if devices:
            lines.append("| Device | IP | Status | Latency |")
            lines.append("|--------|----|--------|---------|")
            for d in devices:
                r = state.device_results.get(d.ip)
                if not gw_up:
                    row_icon = "❓"
                    row_status = "unknown (gateway down)"
                    row_lat = "—"
                else:
                    row_icon = _icon(r.status.value if r else "unknown")
                    row_status = r.status.value if r else "unknown"
                    row_lat = _ms(r.response_ms if r else None)
                lines.append(f"| {d.name} | `{d.ip}` | {row_icon} {row_status} | {row_lat} |")
            lines.append("")

    lines += ["---", ""]

    # ── All devices flat table ────────────────────────────────────────────
    lines.append("## All Devices")
    lines.append("")
    lines.append("| Device | IP | Group | Status | Latency |")
    lines.append("|--------|----|-------|--------|---------|")
    grp_by_id = config.group_by_id()
    for d in config.devices:
        r = state.device_results.get(d.ip)
        grp = grp_by_id.get(d.group_id)
        gw_up = state.gateway_up(grp) if grp else True
        if not gw_up:
            row_icon, row_status, row_lat = "❓", "unknown", "—"
        else:
            row_icon = _icon(r.status.value if r else "unknown")
            row_status = r.status.value if r else "unknown"
            row_lat = _ms(r.response_ms if r else None)
        grp_name = grp.name if grp else d.group_id
        lines.append(f"| {d.name} | `{d.ip}` | {grp_name} | {row_icon} {row_status} | {row_lat} |")

    lines += [
        "",
        "---",
        "",
        f"*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*",
        "",
    ]

    return "\n".join(lines)


def write_report(content: str, path: Path = _DEFAULT_REPORT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


async def run_report(output_path: Path = _DEFAULT_REPORT) -> str:
    """Run a single probe cycle, render markdown, write to file, and return content."""
    from heimdallur.config.loader import load_config
    from heimdallur.tui.app import EnrichedState, HistorySnapshot

    config = load_config()

    if os.getenv("NETWATCH_MOCK"):
        from heimdallur.mock.network import MockProber
        prober = MockProber(config)
        state = await prober.probe_all()
        iq = prober.mock_internet_quality()
        router_stats = prober.mock_router_stats()
        gw_enrichment = {}
        for g in config.groups:
            enr = prober.mock_gateway_enrichment(g)
            if g.gateway_ip:
                gw_enrichment[g.gateway_ip] = enr
        speed = prober.mock_speed_result()
    else:
        from heimdallur.core.prober import Prober
        from heimdallur.core.internet_probe import InternetProber
        prober = Prober(config)
        inet_prober = InternetProber()
        state, iq = await asyncio.gather(prober.probe_all(), inet_prober.probe_all())
        router_stats = None
        gw_enrichment = {}
        speed = None

    from heimdallur.core.internet_probe import IP_TARGETS, DNS_TARGETS, HTTP_TARGETS
    from collections import deque

    # Build a minimal one-shot snapshot (no rolling history)
    def _single(ip: str, result) -> list[float]:
        if result and result.response_ms is not None:
            return [result.response_ms]
        return []

    ont_ip = state.ont_result.ip if state.ont_result else config.ont_check_host

    snapshot = HistorySnapshot(
        ont_lat=_single(ont_ip, state.ont_result),
        ont_loss=[0.0 if (state.ont_result and state.ont_result.response_ms is not None) else 1.0],
        rtr_cpu=[router_stats.cpu_pct] if router_stats else [],
        rtr_mem=[router_stats.memory_pct] if router_stats else [],
        gw_lat={
            g.gateway_ip: _single(g.gateway_ip, state.gateway_results.get(g.gateway_ip))
            for g in config.groups if g.gateway_ip
        },
        gw_loss={
            g.gateway_ip: [0.0 if (r := state.gateway_results.get(g.gateway_ip)) and r.response_ms else 1.0]
            for g in config.groups if g.gateway_ip
        },
        dl_hist=[speed.download_mbps] if speed and speed.ok else [],
        inet_ip_lat={t: [r.rtt_ms] if (r := next((x for x in (iq.raw_ip if iq else []) if x.target == t), None)) and r.rtt_ms else [] for t, _ in IP_TARGETS},
        inet_ip_loss={t: [0.0 if (r := next((x for x in (iq.raw_ip if iq else []) if x.target == t), None)) and r.rtt_ms else 1.0] for t, _ in IP_TARGETS},
        inet_dns_lat={h: [r.lookup_ms] if (r := next((x for x in (iq.dns if iq else []) if x.hostname == h), None)) and r.lookup_ms else [] for h, _ in DNS_TARGETS},
        inet_dns_loss={h: [0.0 if (r := next((x for x in (iq.dns if iq else []) if x.hostname == h), None)) and r.success else 1.0] for h, _ in DNS_TARGETS},
        inet_http_ttfb={u: [r.ttfb_ms] if (r := next((x for x in (iq.http if iq else []) if x.url == u), None)) and r.ttfb_ms else [] for u, _, _, _ in HTTP_TARGETS},
        inet_http_total={u: [r.total_ms] if (r := next((x for x in (iq.http if iq else []) if x.url == u), None)) and r.total_ms else [] for u, _, _, _ in HTTP_TARGETS},
        inet_http_loss={u: [0.0 if (r := next((x for x in (iq.http if iq else []) if x.url == u), None)) and r.success else 1.0] for u, _, _, _ in HTTP_TARGETS},
    )

    enriched = EnrichedState(
        network=state,
        router_stats=router_stats,
        gw_enrichment=gw_enrichment,
        speed_result=speed,
        internet_quality=iq,
    )

    content = render_markdown(enriched, snapshot, config)
    write_report(content, output_path)
    return content
