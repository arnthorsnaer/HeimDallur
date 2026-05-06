#!/usr/bin/env python3
"""Generate comparison screenshots at different terminal sizes to simulate larger fonts.

For an 800x480 Pi display, reducing cols/rows makes each character cell
proportionally bigger, simulating a larger terminal font.

Usage:
    uv run python scripts/experiment_font_size.py
"""
from __future__ import annotations
import asyncio
import importlib
import os
import sys
import tempfile
from pathlib import Path

_REPO = Path(__file__).parent.parent
sys.path.insert(0, str(_REPO))

SCENARIO = _REPO / "heimdallur/mock/scenarios/all_healthy.toml"
OUT_DIR  = _REPO / "docs/screenshots"

# (cols, rows, label)
SIZES = [
    (120, 38, "font-baseline-120x38"),
    (100, 30, "font-medium-100x30"),
    (80,  24, "font-large-80x24"),
]

SETTLE = 5.0


async def capture(cols: int, rows: int, slug: str) -> None:
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        os.environ["NETWATCH_SCREENSHOT_DB"] = f.name

    import heimdallur.tui.app as mod
    importlib.reload(mod)
    app = mod.HeimdallurApp()

    async with app.run_test(size=(cols, rows)) as pilot:
        await pilot.pause(SETTLE)
        svg = app.export_screenshot()

    svg_path = OUT_DIR / f"exp-{slug}.svg"
    png_path = OUT_DIR / f"exp-{slug}.png"
    svg_path.write_text(svg)

    import cairosvg
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=2)
    svg_path.unlink()
    print(f"  saved: {png_path.name}")


def main() -> None:
    os.environ["NETWATCH_MOCK"] = "1"
    os.environ["NETWATCH_MOCK_SCENARIO"] = str(SCENARIO)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for cols, rows, slug in SIZES:
        print(f"Capturing {cols}x{rows} ({slug})...")
        asyncio.run(capture(cols, rows, slug))

    print("\nDone — check docs/screenshots/exp-*.png")


if __name__ == "__main__":
    main()
