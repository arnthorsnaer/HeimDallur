"""Tiny Monitor Mode — full-screen TUI optimised for 66×20 on an 800×480 display.

Three panels cycle automatically every 10 seconds:
  STATUS    — overview of all systems; locks here when faults are active
  INTERNET  — WAN quality, IP/DNS/HTTP checks, speed test
  HOME NET  — router stats + all gateway groups

Manual navigation: ← / → (or H / L keys).
"""
from __future__ import annotations

import time
from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Label, Static

from heimdallur.core.topology import (
    NetworkConfig, ProbeStatus,
)
from heimdallur.tui.status_view import (
    _check_counts, _fmt_uptime, _internet_diagnosis,
    _iq_derived_status, _issue_color, _ms, _rolling_avg, _sc,
    _status_word,
)

# ── Palette (matches status_view) ──────────────────────────────
UI_FG  = "#c9d1d9"
UI_DIM = "#6e7681"
UI_BG  = "#0d1117"
UI_BG2 = "#161b22"
UI_BDR = "#30363d"
S_OK   = "#3fb950"
S_WARN = "#d29922"
S_ERR  = "#f85149"
S_UNK  = "#6e7681"

CYCLE_SECONDS = 10
_PANELS       = ["status", "internet", "home"]
_PANEL_LABELS = ["STATUS", "INTERNET", "HOME"]


# ── Helpers ────────────────────────────────────────────────────

def _dot(status: ProbeStatus | None) -> str:
    if status is None:            return f"[{S_UNK}]○[/]"
    if status == ProbeStatus.HEALTHY:     return f"[{S_OK}]●[/]"
    if status == ProbeStatus.DEGRADED:    return f"[{S_WARN}]~[/]"
    if status == ProbeStatus.UNREACHABLE: return f"[{S_ERR}]✗[/]"
    return f"[{S_UNK}]○[/]"


def _online_count(group, state, config) -> tuple[int, int]:
    devices = config.devices_in_group(group.id)
    gw_online = 1 if (group.gateway_ip and
                      state.gateway_results.get(group.gateway_ip) and
                      state.gateway_results[group.gateway_ip].status == ProbeStatus.HEALTHY) else 0
    dev_online = sum(
        1 for d in devices
        if state.device_results.get(d.ip) and
        state.device_results[d.ip].status == ProbeStatus.HEALTHY
    )
    total = len(devices) + (1 if group.gateway_ip else 0)
    return (dev_online + gw_online), total


# ── Panel content renderers ────────────────────────────────────

def _render_status(enriched, snapshot, config: NetworkConfig) -> str:
    state  = enriched.network
    iq     = enriched.internet_quality
    issues = state.problems(config)

    if iq:
        diag_c, diag_msg = _internet_diagnosis(iq)
        if diag_c in (S_WARN, S_ERR):
            issues = [diag_msg] + issues

    lines: list[str] = []

    if issues:
        sev = S_ERR if any(
            k in i.lower() for i in issues
            for k in ("offline", "outage", "no ip")
        ) else S_WARN
        lines.append(f"[{sev}]✗  {len(issues)} issue{'s' if len(issues)!=1 else ''} detected[/]")
        lines.append("")
        for issue in issues:
            c = _issue_color(issue)
            sym = "✗" if c == S_ERR else "⚠"
            lines.append(f"  [{c}]{sym}  {issue}[/]")
        return "\n".join(lines)

    lines.append(f"[{S_OK}]●  All systems healthy[/]")
    lines.append("")

    # WAN
    ont    = state.ont_result
    ont_ms = _rolling_avg(snapshot.ont_lat) if snapshot.ont_lat else (ont.response_ms if ont else None)
    ont_st = ont.status if ont else None
    lines.append(
        f"  {_dot(ont_st)} [{UI_FG}]WAN     [/]"
        f"[{_sc(ont_st)}]{_status_word(ont_st):<10}[/]"
        f"[{UI_DIM}]{_ms(ont_ms):>8}[/]"
    )

    # Router
    rtr    = state.router_result
    rtr_st = rtr.status if rtr else None
    rs     = enriched.router_stats
    rtr_extra = ""
    if rs:
        cpu_c = S_OK if rs.cpu_pct < 50 else (S_WARN if rs.cpu_pct < 80 else S_ERR)
        mem_c = S_OK if rs.memory_pct < 70 else (S_WARN if rs.memory_pct < 90 else S_ERR)
        rtr_extra = (
            f"  [{cpu_c}]CPU {rs.cpu_pct:.0f}%[/]"
            f"[{UI_DIM}]  [/][{mem_c}]Mem {rs.memory_pct:.0f}%[/]"
        )
    lines.append(
        f"  {_dot(rtr_st)} [{UI_FG}]Router  [/]"
        f"[{_sc(rtr_st)}]{_status_word(rtr_st):<10}[/]"
        f"[{UI_DIM}]{_ms(rtr.response_ms if rtr else None):>8}[/]"
        f"{rtr_extra}"
    )

    wifi_groups = [g for g in config.groups if g.type == "wifi"]
    lan_groups  = [g for g in config.groups if g.type == "lan"]

    for section_label, groups in (("WI-FI", wifi_groups), ("LAN", lan_groups)):
        if not groups:
            continue
        lines.append("")
        lines.append(f"  [{UI_DIM}]{section_label}[/]")
        for g in groups:
            gw_r    = state.gateway_results.get(g.gateway_ip) if g.gateway_ip else None
            on, tot = _online_count(g, state, config)
            c_cnt   = S_OK if on == tot else (S_WARN if on > 0 else S_ERR)
            name    = g.name.removeprefix("WiFi ").removeprefix("LAN ")
            lat     = gw_r.response_ms if gw_r else None
            lines.append(
                f"  {_dot(gw_r.status if gw_r else None)}"
                f" [{UI_FG}]{name:<16}[/]"
                f"[{UI_DIM}]{_ms(lat):>7}[/]"
                f"   [{c_cnt}]{on}/{tot}[/]"
            )

    return "\n".join(lines)


def _render_internet(enriched, snapshot) -> str:
    state = enriched.network
    iq    = enriched.internet_quality
    sr    = enriched.speed_result

    lines: list[str] = []

    if iq:
        iq_st = _iq_derived_status(iq)
        diag_c, diag_msg = _internet_diagnosis(iq)
        ip_ok, ip_tot, dns_ok, dns_tot, http_ok, http_tot = _check_counts(iq)

        lines.append(
            f"[{UI_DIM}]INTERNET[/]"
            f"                    "
            f"[{_sc(iq_st)}]{_status_word(iq_st)}[/]"
        )
        lines.append("")

        def _row(label: str, ok: int, tot: int, lat_list: list[float]) -> str:
            c  = S_OK if ok == tot else (S_WARN if ok > 0 else S_ERR)
            avg = _rolling_avg(lat_list) if lat_list else None
            return (
                f"  [{UI_DIM}]{label:<20}[/]"
                f"[{c}]{ok}/{tot}[/]"
                f"[{UI_DIM}]{'':>5}{_ms(avg):>9} avg[/]"
            )

        lines.append(_row("IP reachability", ip_ok, ip_tot,
                          [v for vals in snapshot.inet_ip_lat.values() for v in vals] if snapshot.inet_ip_lat else []))
        lines.append(_row("DNS resolution",  dns_ok, dns_tot,
                          [v for vals in snapshot.inet_dns_lat.values() for v in vals] if snapshot.inet_dns_lat else []))
        lines.append(_row("HTTP/HTTPS",      http_ok, http_tot,
                          [v for vals in snapshot.inet_http_ttfb.values() for v in vals] if snapshot.inet_http_ttfb else []))
        lines.append("")
        lines.append(f"  [{diag_c}]{diag_msg}[/]")
    else:
        ont    = state.ont_result
        ont_st = ont.status if ont else None
        ont_ms = _rolling_avg(snapshot.ont_lat) if snapshot.ont_lat else None
        lines.append(
            f"[{UI_DIM}]INTERNET[/]"
            f"                    "
            f"[{_sc(ont_st)}]{_status_word(ont_st)}[/]"
        )
        lines.append("")
        lines.append(f"  [{UI_DIM}]WAN latency    {_ms(ont_ms):>8} avg[/]")

    lines.append("")
    if sr and sr.ok:
        age = time.time() - sr.timestamp
        age_str = f"{int(age//60)}min ago" if age < 3600 else f"{int(age//3600)}h ago"
        dl_c = S_OK if sr.download_mbps >= 50 else (S_WARN if sr.download_mbps >= 10 else S_ERR)
        lines.append(
            f"  [{UI_DIM}]Speed test[/]"
            f"   [{dl_c}]↓ {sr.download_mbps:.0f} Mbps[/]"
            f"[{UI_DIM}]   ping {sr.ping_ms:.0f}ms   {age_str}[/]"
        )
    else:
        lines.append(f"  [{UI_DIM}]Speed test   —[/]")

    return "\n".join(lines)


def _render_home(enriched, config: NetworkConfig) -> str:
    state = enriched.network
    rs    = enriched.router_stats
    rtr   = state.router_result

    lines: list[str] = []

    # Router row
    rtr_st = rtr.status if rtr else None
    router_ip = config.router_ip if hasattr(config, "router_ip") else ""
    if rs:
        cpu_c = S_OK if rs.cpu_pct < 50 else (S_WARN if rs.cpu_pct < 80 else S_ERR)
        mem_c = S_OK if rs.memory_pct < 70 else (S_WARN if rs.memory_pct < 90 else S_ERR)
        up    = _fmt_uptime(rs.uptime_seconds)
        lines.append(
            f"  {_dot(rtr_st)} [{UI_FG}]Router   {router_ip}[/]"
            f"[{UI_DIM}]  {_ms(rtr.response_ms if rtr else None):>6}[/]"
            f"  [{cpu_c}]CPU {rs.cpu_pct:.0f}%[/]"
            f"  [{mem_c}]Mem {rs.memory_pct:.0f}%[/]"
            f"[{UI_DIM}]  {up}[/]"
        )
    else:
        lines.append(
            f"  {_dot(rtr_st)} [{UI_FG}]Router   {router_ip}[/]"
            f"[{UI_DIM}]  {_ms(rtr.response_ms if rtr else None):>6}[/]"
        )

    wifi_groups = [g for g in config.groups if g.type == "wifi"]
    lan_groups  = [g for g in config.groups if g.type == "lan"]

    for section_label, groups in (("WI-FI", wifi_groups), ("LAN", lan_groups)):
        if not groups:
            continue
        lines.append("")
        lines.append(f"  [{UI_DIM}]{section_label}[/]")
        for g in groups:
            gw_r    = state.gateway_results.get(g.gateway_ip) if g.gateway_ip else None
            on, tot = _online_count(g, state, config)
            c_cnt   = S_OK if on == tot else (S_WARN if on > 0 else S_ERR)
            name    = g.name.removeprefix("WiFi ").removeprefix("LAN ")
            gw_ip   = f" {g.gateway_ip}" if g.gateway_ip else ""
            lines.append(
                f"  {_dot(gw_r.status if gw_r else None)}"
                f" [{UI_FG}]{name:<16}[/]"
                f"[{UI_DIM}]{gw_ip:<16}{_ms(gw_r.response_ms if gw_r else None):>7}[/]"
                f"   [{c_cnt}]{on}/{tot}[/]"
            )

    return "\n".join(lines)


# ── Widgets ────────────────────────────────────────────────────

class _TinyHeader(Widget):
    DEFAULT_CSS = f"""
    _TinyHeader {{
        height: 2;
        background: {UI_BG2};
        border-bottom: solid {UI_BDR};
        layout: horizontal;
        padding: 0 1;
    }}
    #th-title   {{ width: 1fr; content-align: left middle; color: {UI_FG}; text-style: bold; }}
    #th-version {{ width: auto; content-align: center middle; color: {UI_DIM}; }}
    #th-clock   {{ width: auto; content-align: right middle; color: {UI_DIM}; padding-left: 2; }}
    """

    def compose(self) -> ComposeResult:
        try:
            from heimdallur.version import version_string
            ver = version_string()
        except Exception:
            ver = ""
        yield Label("HEIMDALLUR", id="th-title")
        yield Label(ver, id="th-version")
        yield Label("", id="th-clock")

    def on_mount(self) -> None:
        self.set_interval(1, self._tick)

    def _tick(self) -> None:
        self.query_one("#th-clock", Label).update(datetime.now().strftime("%H:%M:%S"))


class _TinyFooter(Widget):
    DEFAULT_CSS = f"""
    _TinyFooter {{
        dock: bottom;
        height: 2;
        background: {UI_BG2};
        border-top: solid {UI_BDR};
        layout: horizontal;
        padding: 0 1;
        align: left middle;
    }}
    #tf-nav   {{ width: 1fr; content-align: left middle; color: {UI_DIM}; }}
    #tf-timer {{ width: auto; content-align: right middle; color: {UI_DIM}; }}
    #tf-quit  {{ width: auto; padding-left: 2; color: {UI_DIM}; }}
    """

    def compose(self) -> ComposeResult:
        yield Label("", id="tf-nav")
        yield Label("", id="tf-timer")
        yield Label(f"[{UI_DIM}][Q] Quit[/]", id="tf-quit")

    def set_nav(self, idx: int, has_errors: bool) -> None:
        prev_i = (idx - 1) % len(_PANEL_LABELS)
        next_i = (idx + 1) % len(_PANEL_LABELS)
        self.query_one("#tf-nav", Label).update(
            f"[{UI_DIM}]◀ {_PANEL_LABELS[prev_i]}[/]"
            f"   [{UI_FG}]{_PANEL_LABELS[idx]}[/]"
            f"   [{UI_DIM}]{_PANEL_LABELS[next_i]} ▶[/]"
        )

    def set_timer(self, secs: int, has_errors: bool) -> None:
        if has_errors:
            self.query_one("#tf-timer", Label).update(f"[{S_ERR}]● errors[/]")
        else:
            self.query_one("#tf-timer", Label).update(f"[{UI_DIM}]auto {secs}s[/]")


# ── Main screen ────────────────────────────────────────────────

class TinyScreen(Screen):
    CSS = f"""
    TinyScreen {{
        background: {UI_BG};
        color: {UI_FG};
        layout: vertical;
    }}
    .tiny-panel {{
        height: 1fr;
        padding: 1 2;
    }}
    """

    BINDINGS = [
        ("right", "next_panel", "Next"),
        ("left",  "prev_panel", "Prev"),
        ("l",     "next_panel", ""),
        ("h",     "prev_panel", ""),
        ("space", "next_panel", ""),
        ("q",     "app.quit",   "Quit"),
    ]

    def __init__(self, config: NetworkConfig, start_time: float) -> None:
        super().__init__()
        self._config     = config
        self._start_time = start_time
        self._panel_idx  = 0
        self._countdown  = CYCLE_SECONDS
        self._has_errors = False
        self._enriched   = None
        self._snapshot   = None

    def compose(self) -> ComposeResult:
        yield _TinyHeader()
        yield Static("Waiting for first probe…", id="tiny-panel-status",  classes="tiny-panel")
        yield Static("",                         id="tiny-panel-internet", classes="tiny-panel")
        yield Static("",                         id="tiny-panel-home",     classes="tiny-panel")
        yield _TinyFooter()

    def on_mount(self) -> None:
        self._show(0)
        self.set_interval(1, self._tick)

    def _tick(self) -> None:
        if self._has_errors:
            self.query_one(_TinyFooter).set_timer(0, True)
            return
        self._countdown -= 1
        self.query_one(_TinyFooter).set_timer(self._countdown, False)
        if self._countdown <= 0:
            self._panel_idx = (self._panel_idx + 1) % len(_PANELS)
            self._show(self._panel_idx)

    def _show(self, idx: int) -> None:
        ids = ["tiny-panel-status", "tiny-panel-internet", "tiny-panel-home"]
        for i, pid in enumerate(ids):
            self.query_one(f"#{pid}").display = (i == idx)
        self._countdown = CYCLE_SECONDS
        self.query_one(_TinyFooter).set_nav(idx, self._has_errors)

    def action_next_panel(self) -> None:
        if not self._has_errors:
            self._panel_idx = (self._panel_idx + 1) % len(_PANELS)
            self._show(self._panel_idx)

    def action_prev_panel(self) -> None:
        if not self._has_errors:
            self._panel_idx = (self._panel_idx - 1) % len(_PANELS)
            self._show(self._panel_idx)

    def update_state(self, enriched, snapshot) -> None:
        self._enriched  = enriched
        self._snapshot  = snapshot

        state  = enriched.network
        iq     = enriched.internet_quality
        issues = state.problems(self._config)
        if iq:
            diag_c, _ = _internet_diagnosis(iq)
            if diag_c in (S_WARN, S_ERR):
                issues = ["internet_issue"] + issues

        prev_errors     = self._has_errors
        self._has_errors = bool(issues)

        if self._has_errors and self._panel_idx != 0:
            self._panel_idx = 0
            self._show(0)
        elif prev_errors and not self._has_errors:
            # Errors just cleared — resume cycling from status
            self._panel_idx = 0
            self._show(0)

        self.query_one("#tiny-panel-status",  Static).update(
            _render_status(enriched, snapshot, self._config)
        )
        self.query_one("#tiny-panel-internet", Static).update(
            _render_internet(enriched, snapshot)
        )
        self.query_one("#tiny-panel-home",    Static).update(
            _render_home(enriched, self._config)
        )
