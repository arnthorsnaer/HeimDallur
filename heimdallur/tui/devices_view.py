from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Label

from heimdallur.core.topology import (
    Device, Group, NetworkConfig, NetworkState, ProbeStatus,
)

UI_FG  = "#c9d1d9"
UI_DIM = "#6e7681"
UI_BG  = "#0d1117"
UI_BG2 = "#161b22"
UI_BDR = "#30363d"

S_OK   = "#3fb950"
S_WARN = "#d29922"
S_ERR  = "#f85149"
S_UNK  = "#6e7681"


def _sc(status: ProbeStatus | None) -> str:
    if status is None:
        return S_UNK
    return {
        ProbeStatus.HEALTHY:     S_OK,
        ProbeStatus.DEGRADED:    S_WARN,
        ProbeStatus.UNREACHABLE: S_ERR,
        ProbeStatus.UNKNOWN:     S_UNK,
    }[status]


def _ms(v: float | None) -> str:
    return f"{v:.0f}ms" if v is not None else "—"


# ── Section header  e.g. "WI-FI  3/4" ──────────────────────────
class SectionHeader(Widget):
    DEFAULT_CSS = f"""
    SectionHeader {{
        height: 1;
        layout: horizontal;
        margin-top: 1;
    }}
    .sec-lbl {{ width: 8; color: {UI_DIM}; text-style: bold; }}
    .sec-cnt {{ width: auto; }}
    """

    def __init__(self, label: str, sid: str) -> None:
        super().__init__(id=f"sechdr-{sid}")
        self._sid = sid
        self._label = label

    def compose(self) -> ComposeResult:
        yield Label(self._label, classes="sec-lbl")
        yield Label("", id=f"seccnt-{self._sid}", classes="sec-cnt")

    def update(self, ok: int, total: int) -> None:
        c = S_OK if ok == total else (S_WARN if ok > 0 else S_ERR)
        self.query_one(f"#seccnt-{self._sid}", Label).update(
            f"[{c}]{ok}[/][{UI_DIM}]/{total}[/]"
        )


# ── Group header row  e.g. "●  Living Room  -58dBm ▂▄▆█  11/11" ─
class GroupHeaderRow(Widget):
    DEFAULT_CSS = f"""
    GroupHeaderRow {{
        height: 1;
        layout: horizontal;
        padding-left: 2;
        margin-top: 1;
    }}
    .ghdr-icon {{ width: 2; }}
    .ghdr-name {{ width: 1fr; color: {UI_FG}; text-style: bold; }}
    .ghdr-cnt  {{ width: 5; content-align: right middle; }}
    """

    def __init__(self, group: Group) -> None:
        super().__init__(id=f"ghdr-{group.id}")
        self._group = group

    def _strip_name(self) -> str:
        name = self._group.name
        for prefix in ("WiFi ", "LAN "):
            if name.startswith(prefix):
                return name[len(prefix):]
        return name

    def compose(self) -> ComposeResult:
        gid = self._group.id
        yield Label("", id=f"ghdr-icon-{gid}", classes="ghdr-icon")
        yield Label(self._strip_name(), classes="ghdr-name")
        yield Label("", id=f"ghdr-cnt-{gid}",  classes="ghdr-cnt")

    def update(self, state: NetworkState, devices: list[Device]) -> None:
        g = self._group
        gid = g.id
        has_gw = bool(g.gateway_ip)
        gw_result = state.gateway_results.get(g.gateway_ip) if has_gw else None
        gw_offline = gw_result is not None and gw_result.status == ProbeStatus.UNREACHABLE

        if gw_offline:
            c, icon = S_ERR, "✗"
        else:
            dev_results = [state.device_results.get(d.ip) for d in devices]
            known = [r for r in dev_results if r is not None]
            if not known:
                c, icon = UI_DIM, "○"
            else:
                n_ok  = sum(1 for r in known if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED))
                n_err = sum(1 for r in known if r.status == ProbeStatus.UNREACHABLE)
                if n_ok == len(known):
                    c, icon = S_OK, "●"
                elif n_err == len(known):
                    c, icon = S_ERR, "✗"
                else:
                    c, icon = S_WARN, "~"

        self.query_one(f"#ghdr-icon-{gid}", Label).update(f"[{c}]{icon}[/]")

        total = len(devices) + (1 if has_gw else 0)
        online = 0
        if has_gw and gw_result and gw_result.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED):
            online += 1
        for d in devices:
            r = state.device_results.get(d.ip)
            if r and r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED):
                online += 1
        count_c = S_OK if online == total else (S_WARN if online > 0 else S_ERR)
        self.query_one(f"#ghdr-cnt-{gid}", Label).update(
            f"[{count_c}]{online}[/][{UI_DIM}]/{total}[/]"
        )


# ── Device row ───────────────────────────────────────────────────
class DeviceRow(Widget):
    DEFAULT_CSS = f"""
    DeviceRow {{
        height: 1;
        layout: horizontal;
        padding-left: 4;
    }}
    .dev-icon {{ width: 2; }}
    .dev-name {{ width: 1fr; color: {UI_FG}; }}
    .dev-ip   {{ width: 18; color: {UI_DIM}; }}
    .dev-lat  {{ width: 8; }}
    """

    def __init__(self, device: Device) -> None:
        super().__init__(id=f"devrow-{device.ip.replace('.', '-')}")
        self._device = device

    def compose(self) -> ComposeResult:
        d = self._device
        ipk = d.ip.replace(".", "-")
        yield Label("", id=f"devicon-{ipk}", classes="dev-icon")
        yield Label(d.name, classes="dev-name")
        yield Label(d.ip, classes="dev-ip")
        yield Label("", id=f"devlat-{ipk}", classes="dev-lat")

    def update(self, result, suppressed: bool = False) -> None:
        ipk = self._device.ip.replace(".", "-")
        icon_lbl = self.query_one(f"#devicon-{ipk}", Label)
        lat_lbl  = self.query_one(f"#devlat-{ipk}", Label)
        if suppressed:
            icon_lbl.update(f"[{UI_DIM}]○[/]")
            lat_lbl.update(f"[{UI_DIM}]—[/]")
            return
        if result is None:
            icon_lbl.update(f"[{S_UNK}]○[/]")
            lat_lbl.update(f"[{S_UNK}]—[/]")
            return
        c = _sc(result.status)
        icon = {
            ProbeStatus.HEALTHY:     "●",
            ProbeStatus.DEGRADED:    "~",
            ProbeStatus.UNREACHABLE: "✗",
            ProbeStatus.UNKNOWN:     "○",
        }[result.status]
        icon_lbl.update(f"[{c}]{icon}[/]")
        lat_lbl.update(f"[{UI_DIM}]{_ms(result.response_ms)}[/]")


# ── Group block (header row + device rows) ───────────────────────
class GroupBlock(Widget):
    DEFAULT_CSS = """
    GroupBlock { height: auto; }
    """

    def __init__(self, group: Group, devices: list[Device]) -> None:
        super().__init__(id=f"grpblk-{group.id}")
        self._group = group
        self._devices = devices

    def compose(self) -> ComposeResult:
        yield GroupHeaderRow(self._group)
        for dev in self._devices:
            yield DeviceRow(dev)

    def update(self, state: NetworkState) -> None:
        self.query_one(GroupHeaderRow).update(state, self._devices)

        g = self._group
        gw_result = state.gateway_results.get(g.gateway_ip) if g.gateway_ip else None
        gw_offline = gw_result is not None and gw_result.status == ProbeStatus.UNREACHABLE

        for dev in self._devices:
            result = state.device_results.get(dev.ip)
            self.query_one(f"#devrow-{dev.ip.replace('.', '-')}", DeviceRow).update(
                result, suppressed=gw_offline
            )


# ── Devices screen ───────────────────────────────────────────────
class DevicesScreen(Screen):
    CSS = f"""
    DevicesScreen {{
        background: {UI_BG};
        color: {UI_FG};
        layout: vertical;
    }}
    #dev-header {{
        height: 2;
        background: {UI_BG2};
        border-bottom: solid {UI_BDR};
        layout: horizontal;
        padding: 0 2;
    }}
    #dev-title  {{ width: 1fr; content-align: left middle; color: {UI_FG}; text-style: bold; }}
    #dev-hint   {{ width: auto; content-align: right middle; color: {UI_DIM}; }}
    #dev-scroll {{ height: 1fr; padding: 0 2 1 2; }}
    #dev-footer {{
        height: 1;
        background: {UI_BG2};
        border-top: solid {UI_BDR};
        content-align: center middle;
        color: {UI_DIM};
        dock: bottom;
    }}
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("s", "go_back", "Status"),
        ("q", "app.quit", "Quit"),
    ]

    def __init__(self, config: NetworkConfig) -> None:
        super().__init__()
        self._config = config
        self._wifi_groups = [g for g in config.groups if g.type == "wifi"]
        self._lan_groups  = [g for g in config.groups if g.type == "lan"]

    def compose(self) -> ComposeResult:
        with Widget(id="dev-header"):
            yield Label("DEVICES", id="dev-title")
            yield Label("[Esc] back", id="dev-hint")
        with VerticalScroll(id="dev-scroll"):
            if self._wifi_groups:
                yield SectionHeader("WI-FI", "wifi")
                for group in self._wifi_groups:
                    devices = self._config.devices_in_group(group.id)
                    yield GroupBlock(group, devices)
            if self._lan_groups:
                yield SectionHeader("LAN", "lan")
                for group in self._lan_groups:
                    devices = self._config.devices_in_group(group.id)
                    yield GroupBlock(group, devices)
        yield Label("[Esc/S] Status   [Q] Quit", id="dev-footer")

    def on_mount(self) -> None:
        enriched = getattr(self.app, "_last_enriched", None)
        if enriched is not None:
            self.update_state(enriched.network)

    def update_state(self, state: NetworkState) -> None:

        def _grp_has_any_online(group: Group) -> bool:
            gw_result = state.gateway_results.get(group.gateway_ip) if group.gateway_ip else None
            if gw_result and gw_result.status == ProbeStatus.UNREACHABLE:
                return False
            devices = self._config.devices_in_group(group.id)
            return any(
                (r := state.device_results.get(d.ip)) is not None
                and r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED)
                for d in devices
            )

        def _grp_all_online(group: Group) -> bool:
            gw_result = state.gateway_results.get(group.gateway_ip) if group.gateway_ip else None
            if gw_result and gw_result.status == ProbeStatus.UNREACHABLE:
                return False
            devices = self._config.devices_in_group(group.id)
            results = [state.device_results.get(d.ip) for d in devices]
            known = [r for r in results if r is not None]
            if not known:
                return True
            return all(r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED) for r in known)

        if self._wifi_groups:
            wifi_ok = sum(1 for g in self._wifi_groups if _grp_all_online(g))
            self.query_one("#sechdr-wifi", SectionHeader).update(wifi_ok, len(self._wifi_groups))
        if self._lan_groups:
            lan_ok = sum(1 for g in self._lan_groups if _grp_all_online(g))
            self.query_one("#sechdr-lan", SectionHeader).update(lan_ok, len(self._lan_groups))

        for group in self._config.groups:
            self.query_one(f"#grpblk-{group.id}", GroupBlock).update(state)

    def action_go_back(self) -> None:
        self.app.pop_screen()
