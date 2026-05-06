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
            ProbeStatus.UNREACHABLE: "Offline", ProbeStatus.UNKNOWN: "—"}[status]

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
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    if m:
        return f"{m}m {s:02d}s"
    return f"{s}s"

def _issue_color(issue: str) -> str:
    low = issue.lower()
    if "offline" in low or "unreachable" in low:
        return S_ERR
    return S_WARN

def _rolling_avg(data: list[float], n: int = 10) -> float | None:
    if not data:
        return None
    window = data[-n:]
    return sum(window) / len(window)


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
        super().__init__(f"[bold {UI_FG}]{key}[/]{label[1:]}")
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
        width: 1fr;
        height: auto;
        background: {UI_BG2};
        border: solid {UI_BDR};
        padding: 0 1;
    }}
    #inet-duration   {{ height: 1; }}
    #inet-summary    {{ height: 1; }}
    #inet-detail     {{ height: auto; display: none; padding-top: 1; }}
    #inet-lat-hdr    {{ height: 1; color: {UI_DIM}; }}
    InternetPanel Sparkline {{ height: 3; }}
    #inet-speed-full {{ height: 1; margin-top: 1; }}
    """

    def __init__(self) -> None:
        super().__init__()
        self._expanded = False
        self._status_since: float = 0.0
        self._status_word: str = "—"
        self._status_color: str = S_UNK
        self._prev_status: ProbeStatus | None = None

    def compose(self) -> ComposeResult:
        yield Label("", id="inet-duration")
        yield Label("", id="inet-summary")
        with Vertical(id="inet-detail"):
            yield Label("", id="inet-lat-hdr")
            yield Sparkline([], min_color=SPARK_OK_LO, max_color=SPARK_OK_HI, id="inet-lat-spark")
            yield Label("", id="inet-speed-full")

    def on_mount(self) -> None:
        self.border_title = "INTERNET"
        self.border_subtitle = f"[{UI_DIM}]i ▾[/]"
        self.set_interval(1, self._tick)

    def toggle(self) -> None:
        self._expanded = not self._expanded
        self.query_one("#inet-detail").display = self._expanded
        arrow = "▴" if self._expanded else "▾"
        self.border_subtitle = f"[{UI_DIM}]i {arrow}[/]"

    def on_click(self) -> None:
        self.toggle()

    def _tick(self) -> None:
        if not self._status_since:
            return
        elapsed = time.time() - self._status_since
        self.query_one("#inet-duration", Label).update(
            f"[{self._status_color}]{self._status_word}[/]"
            f" [{UI_DIM}]for {_fmt_uptime(elapsed)}[/]"
        )

    def update(self, state: NetworkState, config: NetworkConfig,
               ont_lat: list[float], ont_loss: list[float],
               speed: SpeedResult | None) -> None:
        ont = state.ont_result
        if not ont:
            return
        c = _sc(ont.status)
        sw = _status_word(ont.status)

        if ont.status != self._prev_status:
            self._prev_status = ont.status
            self._status_since = time.time()
            self._status_word = sw
            self._status_color = c

        self.styles.border = ("solid", c)
        self.border_title = f"[bold {c}]INTERNET · {sw.upper()}[/]"

        if self._status_since:
            elapsed = time.time() - self._status_since
            self.query_one("#inet-duration", Label).update(
                f"[{c}]{sw}[/] [{UI_DIM}]for {_fmt_uptime(elapsed)}[/]"
            )

        avg_lat = _rolling_avg(ont_lat)
        avg_str = (
            f"[{UI_DIM}]Avg[/] [{c}]{avg_lat:.1f}ms[/]"
            if avg_lat is not None else f"[{S_UNK}]Avg —[/]"
        )
        if speed and speed.ok:
            spd_str = (
                f"  [{UI_DIM}]·  ↓[/] [{S_OK}]{speed.download_mbps:.0f}[/]"
                f"[{UI_DIM}] Mbps[/]"
            )
        else:
            spd_str = f"  [{UI_DIM}]·  speed pending[/]"
        self.query_one("#inet-summary", Label).update(avg_str + spd_str)

        cur_lat_str = f"{ont_lat[-1]:.1f}ms" if ont_lat else "—"
        avg_lat_str = f"{avg_lat:.1f}ms" if avg_lat is not None else "—"
        self.query_one("#inet-lat-hdr", Label).update(
            f"[{UI_DIM}]Latency  current [/][{c}]{cur_lat_str}[/]"
            f"[{UI_DIM}]  ·  avg {avg_lat_str}[/]"
        )
        if ont_lat:
            self.query_one("#inet-lat-spark", Sparkline).data = ont_lat

        if speed and speed.ok:
            self.query_one("#inet-speed-full", Label).update(
                f"[{UI_DIM}]↓[/] [{S_OK}]{speed.download_mbps:.0f} Mbps[/]"
                f"  [{UI_DIM}]ping {speed.ping_ms:.0f}ms  ·  probe {config.ont_check_host}[/]"
            )
        else:
            self.query_one("#inet-speed-full", Label).update(
                f"[{UI_DIM}]Speed test pending  ·  probe {config.ont_check_host}[/]"
            )


# ── Router panel ───────────────────────────────────────────────
class RouterPanel(Widget):
    DEFAULT_CSS = f"""
    RouterPanel {{
        width: 1fr;
        height: auto;
        background: {UI_BG2};
        border: solid {UI_BDR};
        padding: 0 1;
    }}
    #rtr-duration   {{ height: 1; }}
    #rtr-summary    {{ height: 1; }}
    #rtr-detail     {{ height: auto; display: none; padding-top: 1; }}
    #rtr-cpu-hdr    {{ height: 1; color: {UI_DIM}; }}
    RouterPanel Sparkline {{ height: 3; }}
    #rtr-stats-full {{ height: 1; margin-top: 1; }}
    """

    def __init__(self) -> None:
        super().__init__()
        self._expanded = False
        self._status_since: float = 0.0
        self._status_word: str = "—"
        self._status_color: str = S_UNK
        self._prev_status: ProbeStatus | None = None
        self._lat_hist: list[float] = []

    def compose(self) -> ComposeResult:
        yield Label("", id="rtr-duration")
        yield Label("", id="rtr-summary")
        with Vertical(id="rtr-detail"):
            yield Label("", id="rtr-cpu-hdr")
            yield Sparkline([], min_color=SPARK_OK_LO, max_color=SPARK_OK_HI, id="rtr-cpu-spark")
            yield Label("", id="rtr-stats-full")

    def on_mount(self) -> None:
        self.border_title = "ROUTER"
        self.border_subtitle = f"[{UI_DIM}]r ▾[/]"
        self.set_interval(1, self._tick)

    def toggle(self) -> None:
        self._expanded = not self._expanded
        self.query_one("#rtr-detail").display = self._expanded
        arrow = "▴" if self._expanded else "▾"
        self.border_subtitle = f"[{UI_DIM}]r {arrow}[/]"

    def on_click(self) -> None:
        self.toggle()

    def _tick(self) -> None:
        if not self._status_since:
            return
        elapsed = time.time() - self._status_since
        self.query_one("#rtr-duration", Label).update(
            f"[{self._status_color}]{self._status_word}[/]"
            f" [{UI_DIM}]for {_fmt_uptime(elapsed)}[/]"
        )

    def update(self, state: NetworkState, config: NetworkConfig,
               rtr_cpu: list[float], rtr_mem: list[float],
               stats: RouterStats | None) -> None:
        rtr = state.router_result
        if not rtr:
            return
        c = _sc(rtr.status)
        sw = _status_word(rtr.status)

        if rtr.status != self._prev_status:
            self._prev_status = rtr.status
            self._status_since = time.time()
            self._status_word = sw
            self._status_color = c

        self.styles.border = ("solid", c)
        self.border_title = f"[bold {c}]ROUTER · {sw.upper()}[/]"

        if self._status_since:
            elapsed = time.time() - self._status_since
            self.query_one("#rtr-duration", Label).update(
                f"[{c}]{sw}[/] [{UI_DIM}]for {_fmt_uptime(elapsed)}[/]"
            )

        if rtr.response_ms is not None:
            self._lat_hist.append(rtr.response_ms)
            if len(self._lat_hist) > 20:
                self._lat_hist = self._lat_hist[-20:]

        avg_lat = _rolling_avg(self._lat_hist)
        avg_cpu = _rolling_avg(rtr_cpu)

        lat_str = (
            f"[{UI_DIM}]Avg latency[/] [{c}]{avg_lat:.1f}ms[/]"
            if avg_lat is not None else f"[{S_UNK}]Avg latency —[/]"
        )
        if avg_cpu is not None:
            cpu_c = S_OK if avg_cpu < 50 else (S_WARN if avg_cpu < 80 else S_ERR)
            cpu_str = f"  [{UI_DIM}]·  CPU avg[/] [{cpu_c}]{avg_cpu:.0f}%[/]"
        else:
            cpu_str = ""
        self.query_one("#rtr-summary", Label).update(lat_str + cpu_str)

        cur_cpu_str = f"{rtr_cpu[-1]:.0f}%" if rtr_cpu else "—"
        avg_cpu_str = f"{avg_cpu:.0f}%" if avg_cpu is not None else "—"
        cpu_c2 = S_OK if (avg_cpu or 0) < 50 else (S_WARN if (avg_cpu or 0) < 80 else S_ERR)
        self.query_one("#rtr-cpu-hdr", Label).update(
            f"[{UI_DIM}]CPU  current [/][{cpu_c2}]{cur_cpu_str}[/]"
            f"[{UI_DIM}]  ·  avg {avg_cpu_str}[/]"
        )
        if rtr_cpu:
            self.query_one("#rtr-cpu-spark", Sparkline).data = rtr_cpu

        if stats:
            mem_c = S_OK if stats.memory_pct < 60 else (S_WARN if stats.memory_pct < 85 else S_ERR)
            self.query_one("#rtr-stats-full", Label).update(
                f"[{UI_DIM}]LAN {config.router_ip}  ·  Mem [/]"
                f"[{mem_c}]{stats.memory_pct:.0f}%[/]"
                f"  [{UI_DIM}]·  Up {_fmt_uptime(stats.uptime_seconds)}[/]"
            )
        else:
            self.query_one("#rtr-stats-full", Label).update(
                f"[{UI_DIM}]LAN {config.router_ip}[/]"
            )


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
    #inet-rtr-row {{ height: auto; layout: horizontal; margin-bottom: 1; }}
    InternetPanel {{ margin-right: 1; }}
    #groups-row   {{ height: 1fr; layout: horizontal; }}
    #panel-wifi   {{ margin-right: 1; }}
    """

    BINDINGS = [
        ("h",     "switch_to_history",  "History"),
        ("d",     "switch_to_devices",  "Devices"),
        ("space", "toggle_status",      "Toggle Status"),
        ("i",     "toggle_internet",    "Toggle Internet"),
        ("r",     "toggle_router",      "Toggle Router"),
        ("q",     "app.quit",           "Quit"),
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

    def action_toggle_internet(self) -> None:
        self.query_one(InternetPanel).toggle()

    def action_toggle_router(self) -> None:
        self.query_one(RouterPanel).toggle()

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
