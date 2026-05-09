#!/usr/bin/env python3
"""Generate screenshots and text outputs for every meaningful state of Heimdallur.

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

COLUMNS = 66
ROWS    = 20
SETTLE  = 5.0   # seconds — long enough for probe + speed-test mock to fire
NAV     = 0.6   # seconds — pause after navigation keypresses

# ── TUI screenshot captures ─────────────────────────────────────
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

# ── Base network-state scenarios for status/report output ────────
# One entry per distinct network state — no UI-specific keys or screens.
TEXT_SCENARIOS: list[dict] = [
    {"slug": "01-status-healthy",           "title": "All healthy",
     "scenario": "all_healthy.toml"},
    {"slug": "02-status-internet-degraded", "title": "Internet degraded",
     "scenario": "internet_degraded.toml"},
    {"slug": "03-status-internet-offline",  "title": "Internet offline",
     "scenario": "internet_offline.toml"},
    {"slug": "04-status-router-offline",    "title": "Router offline",
     "scenario": "router_offline.toml"},
    {"slug": "05-status-gateway-offline",   "title": "AP offline (Basement)",
     "scenario": "gateway_offline.toml"},
    {"slug": "06-status-multiple-issues",   "title": "Multiple issues",
     "scenario": "multiple_issues.toml"},
]


# ── TUI screenshot capture ───────────────────────────────────────

async def _capture_svg(scenario_path: Path, keys: list[str], svg_path: Path,
                       extra_env: dict[str, str] | None = None) -> None:
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
    app = _app_mod.HeimdallurApp()

    async with app.run_test(size=(COLUMNS, ROWS)) as pilot:
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


# ── Status text capture (`--mode status`) ───────────────────────

async def _capture_status_text(scenario_path: Path,
                                extra_env: dict[str, str] | None = None) -> str:
    import importlib
    from rich.console import Console as RichConsole

    os.environ["NETWATCH_MOCK"] = "1"
    os.environ["NETWATCH_MOCK_SCENARIO"] = str(scenario_path)
    if extra_env:
        os.environ.update(extra_env)

    console = RichConsole(record=True, no_color=True, width=72)

    import heimdallur.status.render as _render_mod
    importlib.reload(_render_mod)
    await _render_mod.render_status(console=console)

    text = console.export_text()

    if extra_env:
        for k in extra_env:
            os.environ.pop(k, None)

    return text


# ── Markdown report capture (`--mode report`) ────────────────────

async def _capture_report_md(scenario_path: Path,
                              extra_env: dict[str, str] | None = None) -> str:
    import importlib

    os.environ["NETWATCH_MOCK"] = "1"
    os.environ["NETWATCH_MOCK_SCENARIO"] = str(scenario_path)
    if extra_env:
        os.environ.update(extra_env)

    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
        tmp_path = Path(f.name)

    import heimdallur.core.report as _report_mod
    importlib.reload(_report_mod)
    content = await _report_mod.run_report(output_path=tmp_path)

    try:
        tmp_path.unlink(missing_ok=True)
    except OSError:
        pass

    if extra_env:
        for k in extra_env:
            os.environ.pop(k, None)

    return content


# ── Output-formats doc generation ────────────────────────────────

def _write_output_formats_doc(
    out_dir: Path,
    text_results: list[tuple[str, str, str]],   # (slug, title, text)
    report_results: list[tuple[str, str, str]],  # (slug, title, md)
    img_ext: str,
) -> Path:
    lines: list[str] = [
        "# Heimdallur Output Formats",
        "",
        "> Auto-generated by `scripts/capture_all.py` — do not edit manually.",
        "",
        "Heimdallur has three output modes:",
        "",
        "| Mode | Command | Description |",
        "|------|---------|-------------|",
        "| `tui` | `heimdallur` | Interactive Textual dashboard (default) |",
        "| `status` | `heimdallur --mode status` | Single-pass Rich console output |",
        "| `report` | `heimdallur --mode report` | Markdown snapshot written to `~/.local/share/heimdallur/status.md` |",
        "",
        "All outputs below are generated from mock data via the scenario files in",
        "`heimdallur/mock/scenarios/`.",
        "",
        "---",
        "",
    ]

    # ── TUI Screenshots ──────────────────────────────────────────
    lines += [
        "## TUI Screenshots (`--mode tui`)",
        "",
        "The interactive dashboard. Press `i` / `n` to expand panels,",
        "`h` for history, `d` for devices, `q` to quit.",
        "",
    ]
    for slug, title, _ in text_results:
        img_path = f"screenshots/{slug}.{img_ext}"
        lines += [
            f"### {title}",
            "",
            f"| ![{title}]({img_path}) |",
            "|:---:|",
            "",
        ]

    lines += ["---", ""]

    # ── Status text ──────────────────────────────────────────────
    lines += [
        "## Status Output (`--mode status`)",
        "",
        "Single-pass Rich console render — no TUI, no file written. Useful for",
        "scripts, cron jobs, or a quick terminal check.",
        "",
        "```",
        "NETWATCH_MOCK=1 heimdallur --mode status",
        "```",
        "",
    ]
    for slug, title, text in text_results:
        lines += [
            f"### {title}",
            "",
            "```text",
            text.rstrip(),
            "```",
            "",
        ]

    lines += ["---", ""]

    # ── Markdown reports ─────────────────────────────────────────
    lines += [
        "## Markdown Report (`--mode report`)",
        "",
        "Self-contained markdown snapshot. Written to",
        "`~/.local/share/heimdallur/status.md` and printed to stdout.",
        "The TUI also rewrites this file after every probe cycle.",
        "",
        "```",
        "NETWATCH_MOCK=1 heimdallur --mode report",
        "```",
        "",
    ]
    for slug, title, md in report_results:
        lines += [
            f"<details>",
            f"<summary><strong>{title}</strong></summary>",
            "",
            md.strip(),
            "",
            "</details>",
            "",
        ]

    doc_path = out_dir.parent / "output-formats.md"
    doc_path.write_text("\n".join(lines), encoding="utf-8")
    return doc_path


def _write_pr_body(
    out_dir: Path,
    text_results: list[tuple[str, str, str]],   # (slug, title, text)
    report_results: list[tuple[str, str, str]],  # (slug, title, md)
    img_ext: str,
) -> Path:
    """Generate docs/pr-body.md — a ready-to-paste GitHub PR description.

    Three top-level collapsed sections (screenshots / status / markdown report),
    each containing per-scenario collapsed sub-sections.
    """
    def _scenario_block(items: list[str]) -> list[str]:
        return items

    lines: list[str] = []

    # ── Screenshots ──────────────────────────────────────────────
    lines += ["<details>", "<summary><strong>Screenshots</strong></summary>", ""]
    for slug, title, _ in text_results:
        img_path = f"docs/screenshots/{slug}.{img_ext}"
        lines += [
            "<details>",
            f"<summary>{title}</summary>",
            "",
            f"![{title}]({img_path})",
            "",
            "</details>",
            "",
        ]
    lines += ["</details>", "", "---", ""]

    # ── Status output ────────────────────────────────────────────
    lines += ["<details>", "<summary><strong>Status Output (<code>--mode status</code>)</strong></summary>", ""]
    for slug, title, text in text_results:
        lines += [
            "<details>",
            f"<summary>{title}</summary>",
            "",
            "```text",
            text.rstrip(),
            "```",
            "",
            "</details>",
            "",
        ]
    lines += ["</details>", "", "---", ""]

    # ── Markdown report ──────────────────────────────────────────
    lines += ["<details>", "<summary><strong>Markdown Report (<code>--mode report</code>)</strong></summary>", ""]
    for slug, title, md in report_results:
        lines += [
            "<details>",
            f"<summary>{title}</summary>",
            "",
            md.strip(),
            "",
            "</details>",
            "",
        ]
    lines += ["</details>", ""]

    pr_body_path = out_dir.parent / "pr-body.md"
    pr_body_path.write_text("\n".join(lines), encoding="utf-8")
    return pr_body_path


# ── Main ─────────────────────────────────────────────────────────

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

    # ── TUI screenshots ──────────────────────────────────────────
    print(f"Generating {len(CAPTURES)} TUI screenshots → {out_dir}\n")
    t_start = time.monotonic()

    for cap in CAPTURES:
        slug      = cap["slug"]
        scenario  = _SCEN / cap["scenario"]
        keys      = cap.get("keys", [])
        extra_env = cap.get("env")
        svg_path  = out_dir / f"{slug}.svg"
        out_path  = out_dir / f"{slug}.{args.ext}"

        print(f"[{slug}]")
        t0 = time.monotonic()
        asyncio.run(_capture_svg(scenario, keys, svg_path, extra_env))
        print(f"  SVG done ({time.monotonic()-t0:.1f}s)")

        if args.ext == "png":
            _svg_to_png(svg_path, out_path)
            svg_path.unlink()
            print(f"  PNG saved → {out_path.name}")
        else:
            print(f"  SVG saved → {out_path.name}")

    # ── Status text and markdown reports ────────────────────────
    print(f"\nGenerating {len(TEXT_SCENARIOS)} status + report outputs\n")

    text_results:   list[tuple[str, str, str]] = []
    report_results: list[tuple[str, str, str]] = []

    for scen in TEXT_SCENARIOS:
        slug     = scen["slug"]
        title    = scen["title"]
        scenario = _SCEN / scen["scenario"]

        print(f"[{slug}] status …", end=" ", flush=True)
        t0 = time.monotonic()
        text = asyncio.run(_capture_status_text(scenario))
        print(f"done ({time.monotonic()-t0:.1f}s)")
        text_results.append((slug, title, text))

        print(f"[{slug}] report …", end=" ", flush=True)
        t0 = time.monotonic()
        md = asyncio.run(_capture_report_md(scenario))
        print(f"done ({time.monotonic()-t0:.1f}s)")
        report_results.append((slug, title, md))

    # ── Output-formats doc + PR body ────────────────────────────
    doc_path = _write_output_formats_doc(out_dir, text_results, report_results, args.ext)
    pr_path  = _write_pr_body(out_dir, text_results, report_results, args.ext)
    print(f"\nOutput-formats doc → {doc_path.relative_to(_REPO)}")
    print(f"PR body            → {pr_path.relative_to(_REPO)}")

    elapsed = time.monotonic() - t_start
    print(f"\nDone — {len(CAPTURES)} screenshots + {len(TEXT_SCENARIOS)} status/report pairs"
          f" in {elapsed:.0f}s")


if __name__ == "__main__":
    main()
