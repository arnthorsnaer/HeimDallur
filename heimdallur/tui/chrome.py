from __future__ import annotations

import time
from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label, Static

from heimdallur.core.topology import NetworkConfig, NetworkState
from heimdallur.version import __version__
from heimdallur.tui.formatting import _fmt_uptime
from heimdallur.tui.theme import UI_BDR, UI_BG2, UI_DIM, UI_FG, S_ERR, S_OK

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
    #hdr-left    {{ width: 1fr; content-align: left middle; color: {UI_FG}; text-style: bold; }}
    #hdr-version {{ width: 1fr; content-align: center middle; color: #52596b; }}
    #hdr-right   {{ width: 1fr; content-align: right middle; color: {UI_DIM}; }}
    """

    def __init__(self, start_time: float) -> None:
        super().__init__()
        self._start_time = start_time

    def compose(self) -> ComposeResult:
        yield Label("HEIMDALLUR  Network Health Monitor", id="hdr-left")
        yield Label(f"v{__version__}", id="hdr-version")
        yield Label("", id="hdr-right")

    def on_mount(self) -> None:
        self.set_interval(1, self._tick)
        self._tick()

    def _tick(self) -> None:
        self.query_one("#hdr-right", Label).update(
            f"UP {_fmt_uptime(time.time() - self._start_time)}"
            f"   {datetime.now().strftime('%H:%M:%S')}"
        )


# ── Section toggle ─────────────────────────────────────────────
class SectionToggle(Static):
    """Tiny ≡ tap target that expands/collapses one detail sub-section."""

    class Toggled(Message):
        def __init__(self, section: str) -> None:
            super().__init__()
            self.section = section

    DEFAULT_CSS = f"""
    SectionToggle {{
        width: 2; height: 1;
        color: {UI_DIM};
    }}
    SectionToggle:hover {{ color: {UI_FG}; }}
    """

    def __init__(self, section: str) -> None:
        super().__init__("≡")
        self._section = section

    def on_click(self, event) -> None:
        event.stop()
        self.post_message(SectionToggle.Toggled(self._section))



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
    #ftr-email   {{ width: 1fr; content-align: center middle; }}
    #ftr-nav     {{ width: 1fr; layout: horizontal; align: right middle; }}
    FooterBar NavButton {{ margin-left: 1; }}
    """

    def __init__(self, config: NetworkConfig) -> None:
        super().__init__()
        self._config = config

    def compose(self) -> ComposeResult:
        yield Label("", id="ftr-summary")
        yield Label("", id="ftr-email")
        with Horizontal(id="ftr-nav"):
            yield NavButton("H", "History", "history")
            yield NavButton("D", "Devices", "devices")
            yield NavButton("Q", "Quit",    "quit")

    def on_mount(self) -> None:
        gm  = self._config.gmail_notification
        rcpt = self._config.contacts.home_network_admin_email
        enabled = bool(gm.sender_email and gm.app_password and rcpt)
        if enabled:
            self.query_one("#ftr-email", Label).update(
                f"[{UI_DIM}]✉[/] [{UI_FG}]{rcpt}[/]"
            )
        else:
            self.query_one("#ftr-email", Label).update(
                f"[{UI_DIM}]✉  no email configured[/]"
            )

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



