from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Label, Static

from heimdallur.config.validator import ValidationResult
from heimdallur.tui.theme import UI_BG, UI_BG2, UI_BDR, UI_DIM, UI_FG, S_ERR, S_WARN


class ConfigErrorScreen(Screen):
    CSS = f"""
    ConfigErrorScreen {{
        background: {UI_BG};
        color: {UI_FG};
        layout: vertical;
    }}
    #error-body {{
        height: 1fr;
        margin: 1 2;
        padding: 1 2;
        background: {UI_BG2};
        border: solid {S_ERR};
    }}
    #error-title {{
        height: 1;
        text-style: bold;
        color: {S_ERR};
    }}
    #error-path {{
        height: auto;
        margin-top: 1;
        color: {UI_DIM};
    }}
    #error-list {{
        height: auto;
        margin-top: 1;
        color: {S_ERR};
    }}
    #error-actions {{
        height: auto;
        margin-top: 1;
        color: {UI_FG};
    }}
    #error-footer {{
        height: 1;
        background: {UI_BG2};
        color: {UI_DIM};
        content-align: center middle;
        border-top: solid {UI_BDR};
    }}
    """

    BINDINGS = [("q", "app.quit", "Quit")]

    def __init__(self, result: ValidationResult) -> None:
        super().__init__()
        self._result = result

    def compose(self) -> ComposeResult:
        with Vertical(id="error-body"):
            yield Label("✗ CONFIG ERROR", id="error-title")
            yield Static(f"File: {self._result.path}", id="error-path", markup=False)

            lines: list[str] = []
            for error in self._result.errors:
                lines.append(f"• {error}")
            for warning in self._result.warnings:
                lines.append(f"• Warning: {warning}")
            yield Static("\n".join(lines), id="error-list", markup=False)

            yield Static(
                _suggested_actions(self._result.path),
                id="error-actions",
            )
        yield Label("Fix the config, then restart Heimdallur · [q] quit", id="error-footer")


def _suggested_actions(path: Path) -> str:
    return (
        f"Suggested action:\n"
        f"1. Edit the config file shown above.\n"
        f"2. Validate it:\n"
        f"   python scripts/validate-config.py {path}\n"
        f"3. Restart Heimdallur."
    )


class ConfigErrorApp(App):
    CSS = f"Screen {{ background: {UI_BG}; }}"

    def __init__(self, result: ValidationResult) -> None:
        super().__init__()
        self._result = result

    def compose(self) -> ComposeResult:
        return iter(())

    async def on_mount(self) -> None:
        await self.push_screen(ConfigErrorScreen(self._result))
