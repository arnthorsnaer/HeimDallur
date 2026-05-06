#!/usr/bin/env python3
"""Generate a UI screenshot of Heimdallur running in mock mode.

Usage:
    python scripts/screenshot.py [output]

Output defaults to docs/screenshot.png.  If the path ends in .svg only
the SVG is written; any other extension triggers SVG→PNG conversion via
rsvg-convert (package: librsvg2-bin).

The script sets NETWATCH_MOCK=1, starts the app headlessly via Textual's
pilot API, waits long enough for the probe loop and speed-test mock to
fire at least once, then exports the rendered screen.
"""
from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path

# ── tunables ────────────────────────────────────────────────────
COLUMNS = 120
ROWS = 38
# Speed-test mock waits 3 s before first result; 5 s guarantees both
# the probe loop and the speed loop have fired at least once.
SETTLE_SECONDS = 5.0


async def _capture(svg_path: Path) -> None:
    os.environ.setdefault("NETWATCH_MOCK", "1")

    from heimdallur.tui.app import HeimdallurApp

    app = HeimdallurApp()
    async with app.run_test(size=(COLUMNS, ROWS)) as pilot:
        await pilot.pause(SETTLE_SECONDS)
        svg = app.export_screenshot()

    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg, encoding="utf-8")
    print(f"SVG saved  → {svg_path}")


def _svg_to_png(svg_path: Path, png_path: Path) -> None:
    try:
        subprocess.run(
            [
                "rsvg-convert",
                "--dpi-x=144",
                "--dpi-y=144",
                "-o", str(png_path),
                str(svg_path),
            ],
            check=True,
        )
        print(f"PNG saved  → {png_path}")
    except FileNotFoundError:
        sys.exit(
            "rsvg-convert not found.\n"
            "  Ubuntu/Debian: sudo apt-get install librsvg2-bin\n"
            "  macOS:         brew install librsvg"
        )


def main() -> None:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/screenshot.png")
    want_png = output.suffix.lower() != ".svg"
    svg_path = output.with_suffix(".svg") if want_png else output

    asyncio.run(_capture(svg_path))

    if want_png:
        _svg_to_png(svg_path, output)
        svg_path.unlink()  # keep repo clean — only the PNG is committed


if __name__ == "__main__":
    main()
