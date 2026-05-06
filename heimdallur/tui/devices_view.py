from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
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
        ProbeStatus.HEALTHY: S_OK,
        ProbeStatus.DEGRADED: S_WARN,
        ProbeStatus.UNREACHABLE: S_ERR,
        ProbeStatus.UNKNOWN: S_UNK,
    }[status]


def _status_word(status: ProbeStatus | None) -> str:
    if status is None:
        return "—"
    return {
        ProbeStatus.HEALTHY: "Online",
        ProbeStatus.DEGRADED: "Degraded",
        ProbeStatus.UNREACHABLE: "OFFLINE",
        ProbeStatus.UNKNOWN: "—",
    }[status]


def _ms(v: float | None) -> str:
    return f"{v:.0f}ms" if v is not None else "—"


class DeviceRow(Widget):
    DEFAULT_CSS = f"""
    DeviceRow {{
        height: 1;
        layout: horizontal;
    }}
    .dev-name  {{ width: 30; color: {UI_FG}; }}
    .dev-ip    {{ width: 18; color: {UI_DIM}; }}
    .dev-lat   {{ width: 10; color: {UI_DIM}; }}
    .dev-stat  {{ width: 12; }}
    """

    def __init__(self, device: Device) -> None:
        super().__init__(id=f"devrow-{device.ip.replace('.', '-')}")
        self._device = device

    def compose(self) -> ComposeResult:
        d = self._device
        yield Label(d.name, classes="dev-name")
        yield Label(d.ip, classes="dev-ip")
        yield Label("", id=f"devlat-{d.ip.replace('.', '-')}", classes="dev-lat")
        yield Label("", id=f"devst-{d.ip.replace('.', '-')}",  classes="dev-stat")

    def update(self, result) -> None:
        ip_key = self._device.ip.replace(".", "-")
        if result is None:
            self.query_one(f"#devlat-{ip_key}", Label).update(f"[{S_UNK}]—[/]")
            self.query_one(f"#devst-{ip_key}",  Label).update(f"[{S_UNK}]—[/]")
            return
        c = _sc(result.status)
        self.query_one(f"#devlat-{ip_key}", Label).update(
            f"[{UI_DIM}]{_ms(result.response_ms)}[/]"
        )
        self.query_one(f"#devst-{ip_key}", Label).update(
            f"[{c}]{_status_word(result.status)}[/]"
        )


class GroupBlock(Widget):
    DEFAULT_CSS = f"""
    GroupBlock {{
        height: auto;
        margin-bottom: 1;
    }}
    .grp-heading {{
        height: 1;
        background: {UI_BDR};
        color: {UI_FG};
        text-style: bold;
        padding: 0 1;
    }}
    """

    def __init__(self, group: Group, devices: list[Device]) -> None:
        super().__init__(id=f"grpblk-{group.id}")
        self._group = group
        self._devices = devices

    def compose(self) -> ComposeResult:
        g = self._group
        name = g.name
        for prefix in ("WiFi ", "LAN "):
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        type_tag = "WiFi" if g.type == "wifi" else "LAN"
        gw_tag = f"  [{UI_DIM}]{g.gateway_ip}[/]" if g.gateway_ip else ""
        yield Label(
            f"[{UI_DIM}]{type_tag}[/]  [{UI_FG}]{name}[/]{gw_tag}",
            id=f"grphead-{g.id}",
            classes="grp-heading",
        )
        for dev in self._devices:
            yield DeviceRow(dev)

    def update(self, state: NetworkState) -> None:
        for dev in self._devices:
            result = state.device_results.get(dev.ip)
            self.query_one(f"#devrow-{dev.ip.replace('.', '-')}", DeviceRow).update(result)


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
    #dev-col-hdr {{
        height: 1;
        layout: horizontal;
        padding: 0 2;
        background: {UI_BG2};
        color: {UI_DIM};
    }}
    #dev-scroll {{ height: 1fr; padding: 1 2; }}
    #dev-footer {{
        height: 1;
        background: {UI_BG2};
        border-top: solid {UI_BDR};
        content-align: center middle;
        color: {UI_DIM};
        dock: bottom;
    }}
    .col-name   {{ width: 30; }}
    .col-ip     {{ width: 18; }}
    .col-lat    {{ width: 10; }}
    .col-stat   {{ width: 12; }}
    """

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("s", "go_back", "Status"),
        ("q", "app.quit", "Quit"),
    ]

    def __init__(self, config: NetworkConfig) -> None:
        super().__init__()
        self._config = config

    def compose(self) -> ComposeResult:
        with Widget(id="dev-header"):
            yield Label("DEVICES", id="dev-title")
            yield Label("[Esc] back", id="dev-hint")
        with Widget(id="dev-col-hdr"):
            yield Label("Name", classes="col-name")
            yield Label("IP", classes="col-ip")
            yield Label("Latency", classes="col-lat")
            yield Label("Status", classes="col-stat")
        with VerticalScroll(id="dev-scroll"):
            for group in self._config.groups:
                devices = self._config.devices_in_group(group.id)
                yield GroupBlock(group, devices)
        yield Label("[Esc/S] Status   [Q] Quit", id="dev-footer")

    def update_state(self, state: NetworkState) -> None:
        for group in self._config.groups:
            self.query_one(f"#grpblk-{group.id}", GroupBlock).update(state)

    def action_go_back(self) -> None:
        self.app.pop_screen()
