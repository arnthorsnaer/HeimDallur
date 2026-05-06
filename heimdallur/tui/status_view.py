from __future__ import annotations
import time

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Label, Sparkline, Static

from heimdallur.core.topology import (
    Device, Group, NetworkConfig, NetworkState, ProbeStatus,
    GatewayEnrichment, RouterStats, SpeedResult,
)

# ── Colour palette ─────────────────────────────────────────────
# UI chrome uses neutral off-white so semantic green/red pop clearly
UI_FG   = "#c9d1d9"   # off-white — labels, chrome, borders
UI_DIM  = "#6e7681"   # dimmed — secondary text, units, IPs
UI_BG   = "#0d1117"   # near-black background
UI_BG2  = "#161b22"   # slightly lighter — panel backgrounds
UI_BDR  = "#30363d"   # border colour

# Semantic colours — reserved for status meaning only
S_OK    = "#3fb950"   # green  — healthy / online
S_WARN  = "#d29922"   # amber  — degraded / warning
S_ERR   = "#f85149"   # red    — unreachable / error
S_UNK   = "#6e7681"   # gray   — unknown / no data

SPARK_OK_HI = "#3fb950"
SPARK_OK_LO = "#0d3018"
SPARK_ERR   = "#f85149"


# ── Helpers ────────────────────────────────────────────────────
def _sc(status: ProbeStatus | None) -> str:
    if status is None: return S_UNK
    return {ProbeStatus.HEALTHY: S_OK, ProbeStatus.DEGRADED: S_WARN,
            ProbeStatus.UNREACHABLE: S_ERR, ProbeStatus.UNKNOWN: S_UNK}[status]

def _status_word(status: ProbeStatus | None) -> str:
    if status is None: return "—"
    return {ProbeStatus.HEALTHY: "Online", ProbeStatus.DEGRADED: "Degraded",
            ProbeStatus.UNREACHABLE: "OFFLINE", ProbeStatus.UNKNOWN: "—"}[status]

def _ms(v: float | None) -> str:
    return f"{v:.0f}ms" if v is not None else "—"

def _signal_bars(dbm: int) -> str:
    filled = 4 if dbm >= -55 else 3 if dbm >= -67 else 2 if dbm >= -80 else 1
    return "".join(
        f"[{S_OK}]{b}[/]" if i < filled else f"[{UI_BDR}]{b}[/]"
        for i, b in enumerate("▂▄▆█")
    )

def _fmt_uptime(seconds: float) -> str:
    h, r = divmod(int(seconds), 3600)
    m, s = divmod(r, 60)
    if h >= 24:
        d, h = divmod(h, 24)
        return f"{d}d {h}h {m:02d}m"
    return f"{h}h {m:02d}m {s:02d}s"

def _issue_color(issue: str) -> str:
    low = issue.lower()
    if "offline" in low or "unreachable" in low:
        return S_ERR
    return S_WARN


# ── Nav button (touch + keyboard) ──────────────────────────────
class NavButton(Static):
    class Pressed(Message):
        def __init__(self, action: str) -> None:
            super().__init__()
            self.action = action

    DEFAULT_CSS = f"""
    NavButton {{
        width: auto; height: 1; padding: 0 2;
        background: {UI_BDR};
        color: {UI_DIM};
    }}
    NavButton:hover {{ background: #444c56; color: {UI_FG}; }}
    """

    def __init__(self, key: str, label: str, action: str) -> None:
        super().__init__(f"[bold {UI_FG}]{key}[/] {label}")
        self._action = action

    def on_click(self) -> None:
        self.post_message(NavButton.Pressed(self._action))


# ── Header ─────────────────────────────────────────────────────
class HeaderBar(Widget):
    DEFAULT_CSS = f"""
    HeaderBar {{
        dock: top; height: 2;
        background: {UI_BG2};
        border-bottom: solid {UI_BDR};
        layout: horizontal; padding: 0 2;
    }}
    #hdr-left  {{ width: 1fr; content-align: left middle; color: {UI_FG}; text-style: bold; }}
    #hdr-right {{ width: auto; content-align: right middle; color: {UI_DIM}; }}
    """

    def __init__(self, start_time: float) -> None:
        super().__init__()
        self._start_time = start_time

    def compose(self) -> ComposeResult:
        yield Label("HEIMDALLUR  Network Health Monitor", id="hdr-left")
        yield Label("", id="hdr-right")

    def on_mount(self) -> None:
        self.set_interval(1, self._tick)
        self._tick()

    def _tick(self) -> None:
        from datetime import datetime
        self.query_one("#hdr-right", Label).update(
            f"v0.1.0   UP {_fmt_uptime(time.time() - self._start_time)}"
            f"   {datetime.now().strftime('%H:%M:%S')}"
        )


# ── Internet panel ─────────────────────────────────────────────
class InternetPanel(Widget):
    DEFAULT_CSS = f"""
    InternetPanel {{
        width: 1fr; height: 6;
        background: {UI_BG2};
        border: solid {UI_BDR};
        border-title-color: {UI_FG};
        border-title-style: bold;
        padding: 0 1;
        layout: horizontal;
    }}
    #inet-left  {{ width: 22; content-align: left top; }}
    #inet-right {{ width: 1fr; content-align: left top; }}
    InternetPanel .lbl {{ color: {UI_DIM}; height: 1; }}
    InternetPanel .val {{ height: 1; }}
    InternetPanel Sparkline {{ height: 2; margin-top: 1; }}
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="inet-left"):
            yield Label("", id="inet-status", classes="val")
            yield Label("", id="inet-ext",    classes="lbl")
            yield Label("", id="inet-speed",  classes="val")
        with Vertical(id="inet-right"):
            yield Label("", id="inet-lat-lbl", classes="lbl")
            yield Sparkline([], min_color=SPARK_OK_LO, max_color=SPARK_OK_HI, id="inet-lat-spark")

    def on_mount(self) -> None:
        self.border_title = "INTERNET"

    def update(self, state: NetworkState, config: NetworkConfig,
               ont_lat: list[float], ont_loss: list[float],
               speed: SpeedResult | None) -> None:
        ont = state.ont_result
        if not ont:
            return
        c = _sc(ont.status)
        self.query_one("#inet-status", Label).update(
            f"[{UI_DIM}]Status:[/]  [{c}]{_status_word(ont.status)}[/]"
        )
        self.query_one("#inet-ext", Label).update(f"[{UI_DIM}]Probe: {config.ont_check_host}[/]")
        if speed and speed.ok:
            self.query_one("#inet-speed", Label).update(
                f"[{S_OK}]{speed.download_mbps:.0f}[/][{UI_DIM}] Mbps[/]"
                f"  [{UI_DIM}]ping {speed.ping_ms:.0f}ms[/]"
            )
        else:
            self.query_one("#inet-speed", Label).update(f"[{UI_DIM}]Speed test pending…[/]")
        cur = f"[{c}]{ont_lat[-1]:.1f}ms[/]" if ont_lat else f"[{S_UNK}]—[/]"
        self.query_one("#inet-lat-lbl", Label).update(f"[{UI_DIM}]Latency[/]  {cur}")
        if ont_lat:
            self.query_one("#inet-lat-spark", Sparkline).data = ont_lat


# ── Router panel ───────────────────────────────────────────────
class RouterPanel(Widget):
    DEFAULT_CSS = f"""
    RouterPanel {{
        width: 1fr; height: 6;
        background: {UI_BG2};
        border: solid {UI_BDR};
        border-title-color: {UI_FG};
        border-title-style: bold;
        padding: 0 1;
        layout: horizontal;
    }}
    #rtr-left  {{ width: 22; content-align: left top; }}
    #rtr-right {{ width: 1fr; content-align: left top; }}
    RouterPanel .lbl {{ color: {UI_DIM}; height: 1; }}
    RouterPanel .val {{ height: 1; }}
    RouterPanel Sparkline {{ height: 2; margin-top: 1; }}
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="rtr-left"):
            yield Label("", id="rtr-status",  classes="val")
            yield Label("", id="rtr-lan",     classes="lbl")
            yield Label("", id="rtr-uptime",  classes="lbl")
        with Vertical(id="rtr-right"):
            yield Label("", id="rtr-cpu-lbl", classes="lbl")
            yield Sparkline([], min_color=SPARK_OK_LO, max_color=SPARK_OK_HI, id="rtr-cpu-spark")

    def on_mount(self) -> None:
        self.border_title = "ROUTER"

    def update(self, state: NetworkState, config: NetworkConfig,
               rtr_cpu: list[float], rtr_mem: list[float],
               stats: RouterStats | None) -> None:
        rtr = state.router_result
        if not rtr:
            return
        c = _sc(rtr.status)
        self.query_one("#rtr-status", Label).update(
            f"[{UI_DIM}]Status:[/]  [{c}]{_status_word(rtr.status)}[/]"
        )
        self.query_one("#rtr-lan", Label).update(f"[{UI_DIM}]LAN: {config.router_ip}[/]")
        if stats:
            self.query_one("#rtr-uptime", Label).update(
                f"[{UI_DIM}]Up:  {_fmt_uptime(stats.uptime_seconds)}[/]"
            )
            cpu_c = S_OK if stats.cpu_pct < 50 else (S_WARN if stats.cpu_pct < 80 else S_ERR)
            self.query_one("#rtr-cpu-lbl", Label).update(
                f"[{UI_DIM}]CPU[/]  [{cpu_c}]{stats.cpu_pct:.0f}%[/]"
            )
        if rtr_cpu:
            self.query_one("#rtr-cpu-spark", Sparkline).data = rtr_cpu


# ── Group row ──────────────────────────────────────────────────
class GroupRow(Widget):
    DEFAULT_CSS = f"""
    GroupRow {{
        height: 1;
        layout: horizontal;
    }}
    .grp-icon  {{ width: 2; }}
    .grp-name  {{ width: 1fr; color: {UI_FG}; }}
    .grp-sig   {{ width: 13; content-align: right middle; color: {UI_DIM}; }}
    .grp-count {{ width: 5; content-align: right middle; }}
    """

    def __init__(self, group: Group, devices: list[Device]) -> None:
        super().__init__(id=f"grp-{group.id}")
        self._group = group
        self._devices = devices

    def compose(self) -> ComposeResult:
        gid = self._group.id
        # Strip leading "WiFi " / "LAN " — panel title already says it
        name = self._group.name
        for prefix in ("WiFi ", "LAN "):
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        yield Label("", id=f"grp-icon-{gid}",  classes="grp-icon")
        yield Label(name, classes="grp-name")
        yield Label("", id=f"grp-sig-{gid}",   classes="grp-sig")
        yield Label("", id=f"grp-count-{gid}", classes="grp-count")

    def update(self, state: NetworkState, enrichment: GatewayEnrichment | None) -> None:
        g = self._group
        gid = g.id
        has_gw = bool(g.gateway_ip)

        gw_result = state.gateway_results.get(g.gateway_ip) if has_gw else None
        gw_offline = gw_result is not None and gw_result.status == ProbeStatus.UNREACHABLE

        if gw_offline:
            c, icon = S_ERR, "✗"
        elif gw_result and gw_result.status == ProbeStatus.DEGRADED:
            c, icon = S_WARN, "~"
        elif has_gw:
            c, icon = S_OK, "●"
        else:
            c, icon = UI_DIM, "○"

        self.query_one(f"#grp-icon-{gid}", Label).update(f"[{c}]{icon}[/]")

        # Signal / latency for gateway
        if enrichment and enrichment.signal_dbm is not None:
            bars = _signal_bars(enrichment.signal_dbm)
            self.query_one(f"#grp-sig-{gid}", Label).update(
                f"[{UI_DIM}]{enrichment.signal_dbm}dBm[/] {bars}"
            )
        elif has_gw and gw_result:
            self.query_one(f"#grp-sig-{gid}", Label).update(
                f"[{_sc(gw_result.status)}]{_ms(gw_result.response_ms)}[/]"
            )
        else:
            self.query_one(f"#grp-sig-{gid}", Label).update("")

        # Online / total  (gateway counts as one device)
        total = len(self._devices) + (1 if has_gw else 0)
        online = 0
        if has_gw and gw_result and gw_result.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED):
            online += 1
        for d in self._devices:
            r = state.device_results.get(d.ip)
            if r and r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED):
                online += 1

        count_c = S_OK if online == total else (S_WARN if online > 0 else S_ERR)
        self.query_one(f"#grp-count-{gid}", Label).update(
            f"[{count_c}]{online}[/][{UI_DIM}]/{total}[/]"
        )


# ── Groups panel (wifi or lan) ─────────────────────────────────
class GroupsPanel(Widget):
    DEFAULT_CSS = f"""
    GroupsPanel {{
        width: 1fr;
        height: 1fr;
        background: {UI_BG2};
        border: solid {UI_BDR};
        border-title-color: {UI_FG};
        border-title-style: bold;
        padding: 0 1;
    }}
    GroupsPanel VerticalScroll {{ height: 1fr; }}
    """

    def __init__(self, title: str, groups: list[Group], config: NetworkConfig) -> None:
        safe = title.lower().replace(" ", "").replace("-", "")
        super().__init__(id=f"panel-{safe}")
        self._title = title
        self._groups = groups
        self._config = config

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            for group in self._groups:
                devices = self._config.devices_in_group(group.id)
                yield GroupRow(group, devices)

    def on_mount(self) -> None:
        self.border_title = self._title

    def update(self, state: NetworkState, gw_enrichment: dict[str, GatewayEnrichment]) -> None:
        for group in self._groups:
            enr = gw_enrichment.get(group.gateway_ip) if group.gateway_ip else None
            self.query_one(f"#grp-{group.id}", GroupRow).update(state, enr)


# ── Footer ─────────────────────────────────────────────────────
class FooterBar(Widget):
    DEFAULT_CSS = f"""
    FooterBar {{
        dock: bottom; height: 2;
        background: {UI_BG2};
        border-top: solid {UI_BDR};
        layout: horizontal; padding: 0 1;
        align: left middle;
    }}
    #ftr-summary {{ width: 1fr; color: {UI_DIM}; content-align: left middle; }}
    FooterBar NavButton {{ margin-left: 1; }}
    """

    def compose(self) -> ComposeResult:
        yield Label("", id="ftr-summary")
        yield NavButton("H", "History", "history")
        yield NavButton("D", "Devices", "devices")
        yield NavButton("Q", "Quit",    "quit")

    def update(self, state: NetworkState, config: NetworkConfig) -> None:
        total, ok, bad = state.summary(config)
        unknown = total - ok - bad
        age = int(time.time() - state.timestamp)
        parts: list[str] = [f"[{S_OK}]{ok} OK[/]"]
        if bad:
            parts.append(f"[{S_ERR}]{bad} down[/]")
        if unknown:
            parts.append(f"[{UI_DIM}]{unknown} unknown[/]")
        self.query_one("#ftr-summary", Label).update(
            "  ·  ".join(parts) + f"  [{UI_DIM}]— {age}s ago[/]"
        )


# ── Status panel ───────────────────────────────────────────────
class StatusPanel(Widget):
    DEFAULT_CSS = f"""
    StatusPanel {{
        height: auto;
        background: {UI_BG2};
        border: solid {UI_BDR};
        border-title-color: {UI_FG};
        border-title-style: bold;
        padding: 0 1;
    }}
    #st-row    {{ height: 1; layout: horizontal; }}
    #st-icon   {{ width: 2; }}
    #st-msg    {{ width: 1fr; }}
    #st-hint   {{ width: 9; content-align: right middle; color: {UI_DIM}; }}
    #st-detail {{ height: auto; display: none; padding: 1 0 0 1; color: {UI_DIM}; }}
    """

    def __init__(self) -> None:
        super().__init__()
        self._expanded = False

    def compose(self) -> ComposeResult:
        with Horizontal(id="st-row"):
            yield Label("", id="st-icon")
            yield Label("", id="st-msg")
            yield Label("", id="st-hint")
        yield Label("", id="st-detail")

    def on_mount(self) -> None:
        self.border_title = "STATUS"
        self._refresh_hint()

    def toggle(self) -> None:
        self._expanded = not self._expanded
        self.query_one("#st-detail", Label).display = self._expanded
        self._refresh_hint()

    def _refresh_hint(self) -> None:
        arrow = "▴" if self._expanded else "▾"
        self.query_one("#st-hint", Label).update(f"[{UI_DIM}][Spc] {arrow}[/]")

    def update(self, state: NetworkState, config: NetworkConfig) -> None:
        issues = state.problems(config)

        ont_down = state.ont_result and state.ont_result.status == ProbeStatus.UNREACHABLE
        rtr_down = state.router_result and state.router_result.status == ProbeStatus.UNREACHABLE

        if ont_down or rtr_down:
            c, icon = S_ERR, "✗"
            summary = issues[0] if issues else "Critical failure"
        elif issues:
            c, icon = S_WARN, "⚠"
            gw  = sum(1 for i in issues if "gateway offline" in i)
            dev = sum(1 for i in issues if "gateway offline" not in i)
            parts = []
            if gw:  parts.append(f"{gw} gateway{'s' if gw > 1 else ''} offline")
            if dev: parts.append(f"{dev} device{'s' if dev > 1 else ''} unreachable")
            summary = " · ".join(parts) if parts else issues[0]
        else:
            c, icon = S_OK, "●"
            summary = "All systems operational"

        self.query_one("#st-icon", Label).update(f"[{c}]{icon}[/]")
        self.query_one("#st-msg",  Label).update(f"[{c}]{summary}[/]")

        if issues:
            lines = [f"[{_issue_color(i)}]{i}[/]" for i in issues]
        else:
            lines = [f"[{UI_DIM}]No issues detected[/]"]
        self.query_one("#st-detail", Label).update("\n".join(lines))


# ── Status screen ──────────────────────────────────────────────
class StatusScreen(Screen):
    CSS = f"""
    StatusScreen  {{ background: {UI_BG}; color: {UI_FG}; layout: vertical; }}
    #body         {{ height: 1fr; padding: 0 1; layout: vertical; }}
    StatusPanel   {{ margin-bottom: 1; }}
    #inet-rtr-row {{ height: 6; layout: horizontal; margin-bottom: 1; }}
    InternetPanel {{ margin-right: 1; }}
    #groups-row   {{ height: 1fr; layout: horizontal; }}
    #panel-wifi   {{ margin-right: 1; }}
    """

    BINDINGS = [
        ("h",     "switch_to_history", "History"),
        ("d",     "switch_to_devices", "Devices"),
        ("space", "toggle_status",     "Toggle Status"),
        ("q",     "app.quit",          "Quit"),
    ]

    def __init__(self, config: NetworkConfig, start_time: float) -> None:
        super().__init__()
        self._config = config
        self._start_time = start_time

    def compose(self) -> ComposeResult:
        wifi_groups = [g for g in self._config.groups if g.type == "wifi"]
        lan_groups  = [g for g in self._config.groups if g.type == "lan"]
        yield HeaderBar(self._start_time)
        with Vertical(id="body"):
            yield StatusPanel()
            with Horizontal(id="inet-rtr-row"):
                yield InternetPanel()
                yield RouterPanel()
            with Horizontal(id="groups-row"):
                yield GroupsPanel("WI-FI", wifi_groups, self._config)
                yield GroupsPanel("LAN",   lan_groups,  self._config)
        yield FooterBar()

    def update_state(self, enriched, snapshot) -> None:
        s = enriched.network
        c = self._config
        self.query_one(StatusPanel).update(s, c)
        self.query_one(InternetPanel).update(s, c, snapshot.ont_lat, snapshot.ont_loss, enriched.speed_result)
        self.query_one(RouterPanel).update(s, c, snapshot.rtr_cpu, snapshot.rtr_mem, enriched.router_stats)
        for panel in self.query(GroupsPanel):
            panel.update(s, enriched.gw_enrichment)
        self.query_one(FooterBar).update(s, c)

    def action_toggle_status(self) -> None:
        self.query_one(StatusPanel).toggle()

    def on_nav_button_pressed(self, msg: NavButton.Pressed) -> None:
        if msg.action == "history":
            self.action_switch_to_history()
        elif msg.action == "devices":
            self.action_switch_to_devices()
        elif msg.action == "quit":
            self.app.exit()

    def action_switch_to_history(self) -> None:
        from heimdallur.tui.history_view import HistoryScreen
        self.app.push_screen(HistoryScreen(self._config, None))

    def action_switch_to_devices(self) -> None:
        from heimdallur.tui.devices_view import DevicesScreen
        self.app.push_screen(DevicesScreen(self._config))
