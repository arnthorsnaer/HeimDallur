#!/usr/bin/env python3
"""Generate screenshots for every meaningful UI state of Heimdallur.

Runs all captures in a single process, one asyncio event loop per capture,
so there is no subprocess overhead and no SQLite lock contention.

Usage:
    python scripts/capture_all.py [--output-dir DIR] [--png | --svg]
"""
from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

_REPO  = Path(__file__).parent.parent
_SCEN  = _REPO / "heimdallur" / "mock" / "scenarios"

COLUMNS      = 120
ROWS         = 38
TINY_COLUMNS = 66
TINY_ROWS    = 20
SETTLE  = 5.0   # seconds — long enough for probe + speed-test mock to fire
NAV     = 0.6   # seconds — pause after navigation keypresses

# ── All captures ───────────────────────────────────────────────
CAPTURES: list[dict] = [
    # Status screen variants
    {"slug": "01-status-healthy",           "title": "Status — all healthy",
     "scenario": "all_healthy.toml"},
    {"slug": "01b-status-email-configured", "title": "Status — email notifications configured",
     "scenario": "all_healthy.toml",
     "env": {"NETWATCH_DEMO_EMAIL": "addi@example.com"}},
    {"slug": "02-status-internet-degraded", "title": "Status — internet degraded",
     "scenario": "internet_degraded.toml"},
    {"slug": "03-status-internet-offline",  "title": "Status — internet offline",
     "scenario": "internet_offline.toml"},
    {"slug": "04-status-router-offline",    "title": "Status — router offline (devices cascade to unknown)",
     "scenario": "router_offline.toml"},
    {"slug": "05-status-gateway-offline",   "title": "Status — AP offline (Basement, 9 devices suppressed)",
     "scenario": "gateway_offline.toml"},
    {"slug": "06-status-multiple-issues",   "title": "Status — multiple issues (AP + degraded + flapping)",
     "scenario": "multiple_issues.toml"},
    # Expanded panels
    {"slug": "07-inet-panel-expanded",      "title": "Internet panel expanded — all healthy",
     "scenario": "all_healthy.toml",  "keys": ["i"]},
    {"slug": "07b-inet-panel-partial",      "title": "Internet panel expanded — partial failure",
     "scenario": "internet_partial.toml", "keys": ["i"]},
    {"slug": "07c-inet-panel-offline",      "title": "Internet panel expanded — offline",
     "scenario": "internet_offline.toml", "keys": ["i"]},
    {"slug": "06b-status-panel-expanded",   "title": "Status banner expanded — multiple issues",
     "scenario": "multiple_issues.toml", "keys": ["s"]},
    {"slug": "08-net-panel-expanded",        "title": "Home network panel expanded",
     "scenario": "all_healthy.toml",  "keys": ["n"]},
    {"slug": "08b-net-panel-gateway-offline", "title": "Home network panel expanded — AP offline",
     "scenario": "gateway_offline.toml", "keys": ["n"]},
    # Other screens
    {"slug": "09-history-screen",           "title": "History screen",
     "scenario": "multiple_issues.toml", "keys": ["h"]},
    {"slug": "10-devices-screen",           "title": "Devices screen",
     "scenario": "gateway_offline.toml", "keys": ["d"]},
]

TINY_CAPTURES: list[dict] = [
    # STATUS panel — various scenarios
    {"slug": "t01-status-healthy",         "title": "Tiny — all healthy",
     "scenario": "all_healthy.toml"},
    {"slug": "t02-status-degraded",        "title": "Tiny — internet degraded",
     "scenario": "internet_degraded.toml"},
    {"slug": "t03-status-multiple-issues", "title": "Tiny — multiple issues",
     "scenario": "multiple_issues.toml"},
    # INTERNET panel (navigate with right arrow — only works when no active errors)
    {"slug": "t04-internet",               "title": "Tiny — internet panel",
     "scenario": "all_healthy.toml",       "keys": ["right"]},
    # HOME panel
    {"slug": "t05-home",                   "title": "Tiny — home panel",
     "scenario": "all_healthy.toml",       "keys": ["right", "right"]},
]


async def _capture_svg(scenario_path: Path, keys: list[str], svg_path: Path,
                       extra_env: dict[str, str] | None = None,
                       size: tuple[int, int] = (COLUMNS, ROWS),
                       app_class: str = "HeimdallurApp") -> None:
    # Use a fresh temp DB per capture to avoid lock contention.
    import importlib
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        tmp_db = f.name

    os.environ["NETWATCH_MOCK"] = "1"
    os.environ["NETWATCH_MOCK_SCENARIO"] = str(scenario_path)
    os.environ["NETWATCH_SCREENSHOT_DB"] = tmp_db
    if extra_env:
        os.environ.update(extra_env)

    # Re-import the app module fresh each time so env vars are re-read.
    import heimdallur.tui.app as _app_mod
    importlib.reload(_app_mod)
    app = getattr(_app_mod, app_class)()

    async with app.run_test(size=size) as pilot:
        await pilot.pause(SETTLE)
        for key in keys:
            await pilot.press(key)
        if keys:
            await pilot.pause(NAV)
        svg = app.export_screenshot()

    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(svg, encoding="utf-8")

    try:
        Path(tmp_db).unlink(missing_ok=True)
    except OSError:
        pass
    if extra_env:
        for k in extra_env:
            os.environ.pop(k, None)


def _svg_to_png(svg_path: Path, png_path: Path) -> None:
    try:
        subprocess.run(
            ["rsvg-convert", "--dpi-x=144", "--dpi-y=144",
             "-o", str(png_path), str(svg_path)],
            check=True, capture_output=True,
        )
        return
    except FileNotFoundError:
        pass
    try:
        import cairosvg
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), scale=2)
    except ImportError:
        sys.exit(
            "No SVG→PNG converter found.\n"
            "  Ubuntu/Debian: sudo apt-get install librsvg2-bin\n"
            "  macOS:         brew install librsvg\n"
            "  Any platform:  pip install cairosvg"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", default="docs/screenshots")
    fmt = parser.add_mutually_exclusive_group()
    fmt.add_argument("--png", dest="ext", action="store_const", const="png")
    fmt.add_argument("--svg", dest="ext", action="store_const", const="svg")
    parser.set_defaults(ext="png")
    args = parser.parse_args()

    out_dir = (_REPO / args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(CAPTURES) + len(TINY_CAPTURES)
    print(f"Generating {total} screenshots ({len(CAPTURES)} normal + {len(TINY_CAPTURES)} tiny) → {out_dir}\n")
    t_start = time.monotonic()

    def _run_capture(cap: dict, subdir: str = "",
                     size: tuple[int, int] = (COLUMNS, ROWS),
                     app_class: str = "HeimdallurApp") -> None:
        slug      = cap["slug"]
        scenario  = _SCEN / cap["scenario"]
        keys      = cap.get("keys", [])
        extra_env = cap.get("env")
        dest      = out_dir / subdir if subdir else out_dir
        svg_path  = dest / f"{slug}.svg"
        out_path  = dest / f"{slug}.{args.ext}"

        print(f"[{slug}]")
        t0 = time.monotonic()
        asyncio.run(_capture_svg(scenario, keys, svg_path, extra_env, size, app_class))
        print(f"  SVG done ({time.monotonic()-t0:.1f}s)")

        if args.ext == "png":
            _svg_to_png(svg_path, out_path)
            svg_path.unlink()
            print(f"  PNG saved → {('tiny/' if subdir else '') + out_path.name}")
        else:
            print(f"  SVG saved → {('tiny/' if subdir else '') + out_path.name}")

    print("── Normal mode (120×38) ──────────────────────")
    for cap in CAPTURES:
        _run_capture(cap)

    print("\n── Tiny mode (66×20) ─────────────────────────")
    (out_dir / "tiny").mkdir(parents=True, exist_ok=True)
    for cap in TINY_CAPTURES:
        _run_capture(cap, subdir="tiny",
                     size=(TINY_COLUMNS, TINY_ROWS),
                     app_class="TinyApp")

    elapsed = time.monotonic() - t_start
    print(f"\nDone — {total} screenshots in {elapsed:.0f}s")


if __name__ == "__main__":
    main()
