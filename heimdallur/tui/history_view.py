from __future__ import annotations
from datetime import datetime, timedelta
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Label, Static
from heimdallur.core.topology import NetworkConfig, NetworkState, ProbeStatus

GREEN = "#3fb950"
AMBER = "#d29922"
RED   = "#f85149"
GRAY  = "#8b949e"
DIM   = "#30363d"
FG    = "#c9d1d9"
BG    = "#0d1117"
BG2   = "#161b22"

# Block characters for uptime bars
_FULL  = "█"
_MED   = "▓"
_LIGHT = "░"

# 24-bucket mock history keyed by label
_MOCK_BARS: dict[str, list[str]] = {}


def _status_bar_char(status: str) -> tuple[str, str]:
    """Return (color, char) for a status string."""
    if status == "healthy":
        return GREEN, _FULL
    if status == "degraded":
        return AMBER, _MED
    return RED, _LIGHT


def _render_bar(buckets: list[str], width: int = 24) -> str:
    """Render a Rich-markup uptime bar — 2 chars per bucket so axis labels align."""
    padded = (buckets + [" "] * width)[:width]
    parts = []
    for s in padded:
        c, ch = _status_bar_char(s)
        parts.append(f"[{c}]{ch}{ch}[/]")   # 2 chars per hour bucket
    return "".join(parts)


def _mock_history(label: str, num_buckets: int = 24, down_range: tuple[int, int] | None = None) -> list[str]:
    result = ["healthy"] * num_buckets
    if down_range:
        for i in range(down_range[0], min(down_range[1], num_buckets)):
            result[i] = "unreachable"
    return result


class HistoryScreen(Screen):
    CSS = f"""
    HistoryScreen {{
        background: {BG};
        color: {FG};
        layout: vertical;
    }}
    #hist-header {{
        height: 3;
        background: {BG2};
        layout: horizontal;
        padding: 0 2;
        content-align: center middle;
        border-bottom: solid {DIM};
    }}
    #hist-title {{
        width: 1fr;
        content-align: left middle;
        text-style: bold;
    }}
    #hist-time {{
        width: auto;
        color: {GRAY};
    }}
    #hist-body {{
        padding: 1 2;
        height: 1fr;
    }}
    #hist-axis-row {{
        margin-bottom: 1;
    }}
    .hist-time-axis {{
        color: {GRAY};
        width: 1fr;
    }}
    .hist-row {{
        height: 1;
        layout: horizontal;
    }}
    .hist-row-label {{
        width: 10;
        color: {GRAY};
    }}
    .hist-row-bar {{
        width: 1fr;
    }}
    #hist-note {{
        margin-top: 2;
        color: {GRAY};
    }}
    #hist-footer {{
        height: 2;
        background: {BG2};
        content-align: center middle;
        color: {GRAY};
        border-top: solid {DIM};
        dock: bottom;
    }}
    """

    BINDINGS = [("tab", "go_back", "Status"), ("escape", "go_back", "Back"), ("q", "app.quit", "Quit")]

    def __init__(self, config: NetworkConfig, state: NetworkState | None) -> None:
        super().__init__()
        self._config = config
        self._state = state

    def compose(self) -> ComposeResult:
        with Horizontal(id="hist-header"):
            yield Label("HISTORY  —  Last 24h", id="hist-title")
            yield Label(datetime.now().strftime("%H:%M"), id="hist-time")

        with Vertical(id="hist-body"):
            with Horizontal(classes="hist-row", id="hist-axis-row"):
                yield Label("", classes="hist-row-label")
                yield Label("00    03    06    09    12    15    18    21    24",
                            classes="hist-time-axis")

            rows = [
                ("WAN",    _mock_history("wan")),
                ("ROUTER", _mock_history("router")),
                ("Garage", _mock_history("garage-ap")),
                ("Main",   _mock_history("main-ap")),
                ("Upper",  _mock_history("upper-ap")),
                ("Lower",  _mock_history("lower-ap", down_range=(8, 10))),
            ]
            for label, buckets in rows:
                with Horizontal(classes="hist-row"):
                    yield Label(label, classes="hist-row-label")
                    yield Label(_render_bar(buckets), classes="hist-row-bar")

            yield Static(
                f"\n  [{AMBER}]08:00–10:00[/]  [{RED}]Lower AP offline (2h)[/]\n"
                f"  [{GRAY}]9 devices unreachable[/]",
                id="hist-note",
            )

        yield Label("[Tab] back to status", id="hist-footer")

    def action_go_back(self) -> None:
        self.app.pop_screen()
