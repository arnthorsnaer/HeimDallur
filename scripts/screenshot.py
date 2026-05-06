#!/usr/bin/env python3
"""Generate a single UI screenshot of Heimdallur running in mock mode.

Usage:
    python scripts/screenshot.py OUTPUT [--scenario TOML] [--keys KEY,...]

    OUTPUT          destination file (.svg keeps SVG; anything else triggers
                    SVG→PNG via rsvg-convert / librsvg2-bin)
    --scenario PATH path to a scenario TOML file (default: all_healthy.toml)
    --keys KEY,...   comma-separated Textual key names to press after settling
                    (e.g. "i" to expand the internet panel, "h" for history)

Environment:
    NETWATCH_MOCK=1            always set by this script
    NETWATCH_MOCK_SCENARIO     path forwarded to MockProber (set via --scenario)
"""
from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
from pathlib import Path

COLUMNS = 120
ROWS    = 38

# Speed-test mock waits 3 s before first result; 5 s guarantees both
# the probe loop and speed loop have fired at least once.
SETTLE_SECONDS = 5.0
# Short pause after navigation keypresses to let the new screen render.
NAV_PAUSE = 0.6

_SCENARIOS_DIR = Path(__file__).parent.parent / "heimdallur" / "mock" / "scenarios"
_DEFAULT_SCENARIO = _SCENARIOS_DIR / "all_healthy.toml"


async def _capture(svg_path: Path, keys: list[str]) -> None:
    from heimdallur.tui.app import HeimdallurApp

    app = HeimdallurApp()
    async with app.run_test(size=(COLUMNS, ROWS)) as pilot:
        await pilot.pause(SETTLE_SECONDS)
        for key in keys:
            await pilot.press(key)
        if keys:
            await pilot.pause(NAV_PAUSE)
        svg = app.export_screenshot()

    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg, encoding="utf-8")
    print(f"  SVG → {svg_path.name}")


def _svg_to_png(svg_path: Path, png_path: Path) -> None:
    try:
        subprocess.run(
            ["rsvg-convert", "--dpi-x=144", "--dpi-y=144",
             "-o", str(png_path), str(svg_path)],
            check=True, capture_output=True,
        )
        print(f"  PNG → {png_path.name}")
    except FileNotFoundError:
        sys.exit(
            "rsvg-convert not found.\n"
            "  Ubuntu/Debian: sudo apt-get install librsvg2-bin\n"
            "  macOS:         brew install librsvg"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("output", nargs="?",
                        default="docs/screenshot.png",
                        help="Output file path (default: docs/screenshot.png)")
    parser.add_argument("--scenario", default=str(_DEFAULT_SCENARIO),
                        help="Path to scenario TOML (default: all_healthy.toml)")
    parser.add_argument("--keys", default="",
                        help="Comma-separated key names to press after settling")
    args = parser.parse_args()

    output   = Path(args.output)
    want_png = output.suffix.lower() != ".svg"
    svg_path = output.with_suffix(".svg") if want_png else output
    keys     = [k for k in args.keys.split(",") if k]

    os.environ["NETWATCH_MOCK"] = "1"
    os.environ["NETWATCH_MOCK_SCENARIO"] = args.scenario

    asyncio.run(_capture(svg_path, keys))

    if want_png:
        _svg_to_png(svg_path, output)
        svg_path.unlink()


if __name__ == "__main__":
    main()
