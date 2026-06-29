#!/usr/bin/env python3
"""Generate snapshots and text outputs for every meaningful state of Heimdallur.

Runs all captures in a single process, one asyncio event loop per capture,
so there is no subprocess overhead and no SQLite lock contention.

Usage:
    python scripts/capture_all.py [--output-dir DIR] [--png | --svg]
"""
from __future__ import annotations

import argparse
import asyncio
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

_REPO  = Path(__file__).parent.parent
_SCEN  = _REPO / "heimdallur" / "mock" / "scenarios"
_DEFAULT_CONFIG = _REPO / "heimdallur" / "config" / "default-network.toml"

COLUMNS = 66
ROWS    = 20
SETTLE  = 5.0   # seconds — long enough for probe + speed-test mock to fire
NAV     = 0.6   # seconds — pause after navigation keypresses

# Chromium headless shell bundled with the system playwright installation.
_CHROMIUM = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

# ── TUI snapshot captures ───────────────────────────────────────
CAPTURES: list[dict] = [
    # Status screen variants
    {"slug": "01-status-healthy",           "title": "Status — all healthy",
     "scenario": "all_healthy.toml"},
    {"slug": "01b-status-email-configured", "title": "Status — email notifications configured",
     "scenario": "all_healthy.toml",
     "env": {"HEIMDALLUR_DEMO_EMAIL": "network-admin@example.com"}},
    {"slug": "02-status-internet-degraded", "title": "Status — internet degraded",
     "scenario": "internet_degraded.toml"},
    {"slug": "03-status-internet-offline",  "title": "Status — internet offline",
     "scenario": "internet_offline.toml"},
    {"slug": "04-status-router-offline",    "title": "Status — router offline (devices cascade to unknown)",
     "scenario": "router_offline.toml"},
    {"slug": "05-status-gateway-offline",   "title": "Status — AP offline (lower floor, 9 devices suppressed)",
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
# The "name" key is the short identifier used with --scenarios.
TEXT_SCENARIOS: list[dict] = [
    {"slug": "01-status-healthy",           "title": "All healthy",
     "name": "all_healthy",       "scenario": "all_healthy.toml"},
    {"slug": "02-status-internet-degraded", "title": "Internet degraded",
     "name": "internet_degraded", "scenario": "internet_degraded.toml"},
    {"slug": "03-status-internet-offline",  "title": "Internet offline",
     "name": "internet_offline",  "scenario": "internet_offline.toml"},
    {"slug": "04-status-router-offline",    "title": "Router offline",
     "name": "router_offline",    "scenario": "router_offline.toml"},
    {"slug": "05-status-gateway-offline",   "title": "AP offline (Basement)",
     "name": "gateway_offline",   "scenario": "gateway_offline.toml"},
    {"slug": "06-status-multiple-issues",   "title": "Multiple issues",
     "name": "multiple_issues",   "scenario": "multiple_issues.toml"},
]

_ALL_SCENARIO_NAMES = [s["name"] for s in TEXT_SCENARIOS]

# Web snapshots mirror the 6 base scenarios (one browser capture each).
WEB_SCENARIOS: list[dict] = [
    {"slug": "web-01-status-healthy",           "title": "Web UI — all healthy",
     "name": "all_healthy",       "scenario": "all_healthy.toml"},
    {"slug": "web-02-status-internet-degraded", "title": "Web UI — internet degraded",
     "name": "internet_degraded", "scenario": "internet_degraded.toml"},
    {"slug": "web-03-status-internet-offline",  "title": "Web UI — internet offline",
     "name": "internet_offline",  "scenario": "internet_offline.toml"},
    {"slug": "web-04-status-router-offline",    "title": "Web UI — router offline",
     "name": "router_offline",    "scenario": "router_offline.toml"},
    {"slug": "web-05-status-gateway-offline",   "title": "Web UI — AP offline (Basement)",
     "name": "gateway_offline",   "scenario": "gateway_offline.toml"},
    {"slug": "web-06-status-multiple-issues",   "title": "Web UI — multiple issues",
     "name": "multiple_issues",   "scenario": "multiple_issues.toml"},
]


# ── TUI snapshot capture ────────────────────────────────────────

async def _capture_svg(scenario_path: Path, keys: list[str], svg_path: Path,
                       extra_env: dict[str, str] | None = None) -> None:
    # Use a fresh temp DB per capture to avoid lock contention.
    import importlib
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        tmp_db = f.name

    os.environ["HEIMDALLUR_MOCK"] = "1"
    os.environ["HEIMDALLUR_MOCK_SCENARIO"] = str(scenario_path)
    os.environ["HEIMDALLUR_SNAPSHOT_DB"] = tmp_db
    os.environ["HEIMDALLUR_CONFIG"] = str(_DEFAULT_CONFIG)
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


# ── Web (browser) snapshot capture ──────────────────────────────

_WEB_SETTLE   = 8.0   # seconds — wait for server + app to render in browser
_WEB_PORT_BASE = 18080  # start port; incremented per capture to avoid conflicts

def _capture_web_snapshot(
    scenario_path: Path,
    png_path: Path,
    port: int,
    extra_env: dict[str, str] | None = None,
) -> None:
    """Start textual-serve for the given scenario, take a browser snapshot, stop."""
    env = os.environ.copy()
    env["HEIMDALLUR_MOCK"] = "1"
    env["HEIMDALLUR_MOCK_SCENARIO"] = str(scenario_path)
    env["HEIMDALLUR_CONFIG"] = str(_DEFAULT_CONFIG)
    if extra_env:
        env.update(extra_env)

    # Inline server-start script — inherits the full env above.
    server_script = (
        "import sys; sys.path.insert(0, {repo!r}); "
        "from textual_serve.server import Server; "
        "Server('python -m heimdallur --mode tui', host='127.0.0.1', port={port}).serve()"
    ).format(repo=str(_REPO), port=port)

    proc = subprocess.Popen(
        [sys.executable, "-c", server_script],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        # Give the aiohttp server time to bind and the app subprocess time to start.
        time.sleep(_WEB_SETTLE)

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise RuntimeError(
                "playwright is not installed — run: pip install playwright"
            )
        if not Path(_CHROMIUM).exists():
            raise RuntimeError(
                f"Chromium not found at {_CHROMIUM}\n"
                "Run: playwright install chromium"
            )
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=_CHROMIUM)
            try:
                # 1200×750 gives a generous viewport; the xterm.js terminal
                # fills the page width and the TUI content sits at the top.
                page = browser.new_page(viewport={"width": 1200, "height": 750})
                page.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle")
                # Extra pause: xterm.js needs a moment to render the first frame.
                page.wait_for_timeout(3000)
                png_path.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(png_path), full_page=False)
            finally:
                browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ── Status text capture (`--mode status`) ───────────────────────

async def _capture_status_text(scenario_path: Path,
                                extra_env: dict[str, str] | None = None) -> str:
    import importlib
    from rich.console import Console as RichConsole

    os.environ["HEIMDALLUR_MOCK"] = "1"
    os.environ["HEIMDALLUR_MOCK_SCENARIO"] = str(scenario_path)
    os.environ["HEIMDALLUR_CONFIG"] = str(_DEFAULT_CONFIG)
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
    os.environ.pop("HEIMDALLUR_CONFIG", None)

    return text


# ── Markdown report capture (`--mode report`) ────────────────────

async def _capture_report_md(scenario_path: Path,
                              extra_env: dict[str, str] | None = None) -> str:
    import importlib

    os.environ["HEIMDALLUR_MOCK"] = "1"
    os.environ["HEIMDALLUR_MOCK_SCENARIO"] = str(scenario_path)
    os.environ["HEIMDALLUR_CONFIG"] = str(_DEFAULT_CONFIG)
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
    os.environ.pop("HEIMDALLUR_CONFIG", None)

    return content


# ── Shared helpers for per-state collapsed sections ──────────────

# (slug, title, name, text/md)
TextResult = tuple[str, str, str, str]
# (slug, title, name)
WebSlug = tuple[str, str, str]


def _state_sections(
    slug: str,
    title: str,
    name: str,
    text: str,
    report: str,
    web_by_name: dict[str, str],  # name → web slug
    img_url_fn,                   # callable(slug) → URL string
    img_tag_fn,                   # callable(alt, url) → markdown image string
) -> list[str]:
    """Return the collapsed detail sections for one network state."""
    lines: list[str] = []

    if name in web_by_name:
        web_slug = web_by_name[name]
        web_url  = img_url_fn(web_slug)
        lines += [
            "<details>",
            "<summary>Web UI (<code>make web</code>)</summary>",
            "",
            img_tag_fn(f"Web UI — {title}", web_url),
            "",
            "</details>",
            "",
        ]

    lines += [
        "<details>",
        "<summary>Status output (<code>--mode status</code>)</summary>",
        "",
        "```text",
        text.rstrip(),
        "```",
        "",
        "</details>",
        "",
        "<details>",
        "<summary>Markdown report (<code>--mode report</code>)</summary>",
        "",
        report.strip(),
        "",
        "</details>",
        "",
    ]

    return lines


# ── Output-formats doc generation ────────────────────────────────

def _write_output_formats_doc(
    out_dir: Path,
    text_results: list[TextResult],
    report_results: list[TextResult],
    web_slugs: list[WebSlug],
    img_ext: str,
) -> Path:
    lines: list[str] = [
        "# Heimdallur Output Formats",
        "",
        "> Auto-generated by `scripts/capture_all.py` — do not edit manually.",
        "",
        "Heimdallur has four output modes:",
        "",
        "| Mode | Command | Description |",
        "|------|---------|-------------|",
        "| `tui` | `heimdallur` | Interactive Textual dashboard (default) |",
        "| `web` | `make web` | Same TUI served in a browser via xterm.js |",
        "| `status` | `heimdallur --mode status` | Single-pass Rich console output |",
        "| `report` | `heimdallur --mode report` | Markdown snapshot written to `~/.local/share/heimdallur/status.md` |",
        "",
        "All outputs below are generated from mock data via the scenario files in",
        "`heimdallur/mock/scenarios/`.",
        "",
        "---",
        "",
    ]

    report_by_name = {name: md for _, _, name, md in report_results}

    def _img(alt: str, slug: str) -> str:
        return f"![{alt}](snapshots/{slug}.{img_ext})"

    # ── TUI section ──────────────────────────────────────────────────
    lines += ["## TUI (`heimdallur`)", ""]
    rows_of_3 = [text_results[i:i+3] for i in range(0, len(text_results), 3)]
    for row in rows_of_3:
        img_cells = " | ".join(_img(title, slug) for slug, title, _, __ in row)
        cap_cells = " | ".join(title for _, title, __, ___ in row)
        lines += [
            f"| {img_cells} |",
            "|" + "|".join(":---:" for _ in row) + "|",
            f"| {cap_cells} |",
            "",
        ]
    lines += ["---", ""]

    # ── Web UI section ────────────────────────────────────────────────
    if web_slugs:
        lines += ["## Web UI (`make web`)", ""]
        web_rows = [web_slugs[i:i+3] for i in range(0, len(web_slugs), 3)]
        for row in web_rows:
            img_cells = " | ".join(_img(title, slug) for slug, title, _ in row)
            cap_cells = " | ".join(title.replace("Web UI — ", "") for _, title, __ in row)
            lines += [
                f"| {img_cells} |",
                "|" + "|".join(":---:" for _ in row) + "|",
                f"| {cap_cells} |",
                "",
            ]
        lines += ["---", ""]

    # ── Status section ────────────────────────────────────────────────
    lines += ["## Status output (`--mode status`)", ""]
    for slug, title, name, text in text_results:
        lines += [
            f"### {title}",
            "",
            "```text",
            text.rstrip(),
            "```",
            "",
        ]
    lines += ["---", ""]

    # ── Report section ────────────────────────────────────────────────
    lines += ["## Markdown report (`--mode report`)", ""]
    for _, title, name, __ in text_results:
        report = report_by_name.get(name, "")
        lines += [
            f"### {title}",
            "",
            report.strip(),
            "",
        ]

    doc_path = out_dir.parent / "output-formats.md"
    doc_path.write_text("\n".join(lines), encoding="utf-8")
    return doc_path


# ── ui-states.md marker injection ───────────────────────────────

def _update_ui_states_doc(
    out_dir: Path,
    text_results: list[TextResult],
    report_results: list[TextResult],
    web_slugs: list[WebSlug],
    img_ext: str,
) -> None:
    """Inject generated collapsed sections into docs/ui-states.md.

    Finds <!-- generated:NAME:start --> … <!-- generated:NAME:end --> marker
    pairs and replaces the content between them with current Web UI / status /
    report sections for each base scenario.
    """
    ui_states_path = out_dir.parent / "ui-states.md"
    if not ui_states_path.exists():
        return

    content = ui_states_path.read_text(encoding="utf-8")

    web_by_name    = {name: slug for slug, _, name in web_slugs}
    report_by_name = {name: md   for _, _, name, md in report_results}

    def _rel_url(slug: str) -> str:
        return f"snapshots/{slug}.{img_ext}"

    def _img_tag(alt: str, url: str) -> str:
        return f"| ![{alt}]({url}) |\n|:---:|"

    for slug, title, name, text in text_results:
        start_marker = f"<!-- generated:{name}:start -->"
        end_marker   = f"<!-- generated:{name}:end -->"

        generated = _state_sections(
            slug, title, name, text, report_by_name.get(name, ""),
            web_by_name, _rel_url, _img_tag,
        )
        replacement = (
            start_marker + "\n"
            + "\n".join(generated)
            + end_marker
        )

        pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
        if re.search(pattern, content, flags=re.DOTALL):
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    ui_states_path.write_text(content, encoding="utf-8")


# ── Main ─────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", default="docs/snapshots")
    parser.add_argument(
        "--scenarios",
        help=(
            "Comma-separated scenario names to capture (default: all). "
            f"Available: {', '.join(_ALL_SCENARIO_NAMES)}"
        ),
    )
    parser.add_argument(
        "--pr-only", action="store_true",
        help="Skip TUI snapshot generation; only regenerate status/report text and docs",
    )
    parser.add_argument(
        "--no-web", action="store_true",
        help="Skip web (browser) snapshot generation",
    )
    fmt = parser.add_mutually_exclusive_group()
    fmt.add_argument("--png", dest="ext", action="store_const", const="png")
    fmt.add_argument("--svg", dest="ext", action="store_const", const="svg")
    parser.set_defaults(ext="png")
    args = parser.parse_args()

    # ── Scenario filter ──────────────────────────────────────────
    if args.scenarios:
        selected = {s.strip() for s in args.scenarios.split(",")}
        unknown  = selected - set(_ALL_SCENARIO_NAMES)
        if unknown:
            sys.exit(f"Unknown scenario(s): {', '.join(sorted(unknown))}\n"
                     f"Available: {', '.join(_ALL_SCENARIO_NAMES)}")
    else:
        selected = set(_ALL_SCENARIO_NAMES)

    active_text = [s for s in TEXT_SCENARIOS if s["name"] in selected]
    active_web  = [s for s in WEB_SCENARIOS  if s["name"] in selected]
    # For TUI captures, include entries whose scenario file matches the selection.
    active_caps = [c for c in CAPTURES if Path(c["scenario"]).stem in selected]

    out_dir = (_REPO / args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    t_start = time.monotonic()

    # ── TUI snapshots ────────────────────────────────────────────
    if not args.pr_only:
        print(f"Generating {len(active_caps)} TUI snapshots → {out_dir}\n")

        for cap in active_caps:
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
    else:
        print("Skipping TUI snapshots (--pr-only)\n")

    # ── Web (browser) snapshots ──────────────────────────────────
    web_slugs: list[WebSlug] = []
    do_web = not args.no_web and args.ext == "png"
    if do_web and active_web:
        print(f"\nGenerating {len(active_web)} web (browser) snapshots\n")
        for idx, scen in enumerate(active_web):
            slug     = scen["slug"]
            title    = scen["title"]
            name     = scen["name"]
            scenario = _SCEN / scen["scenario"]
            port     = _WEB_PORT_BASE + idx
            png_path = out_dir / f"{slug}.png"

            print(f"[{slug}] starting server on port {port} …", end=" ", flush=True)
            t0 = time.monotonic()
            try:
                _capture_web_snapshot(scenario, png_path, port)
                print(f"done ({time.monotonic()-t0:.1f}s) → {png_path.name}")
                web_slugs.append((slug, title, name))
            except RuntimeError as exc:
                print(f"SKIPPED — {exc}")
                break  # same dependency missing for all; no point retrying
    elif args.no_web:
        print("\nSkipping web snapshots (--no-web)\n")
        # Still include web entries in docs if the PNGs already exist.
        for scen in active_web:
            slug = scen["slug"]
            if (out_dir / f"{slug}.png").exists():
                web_slugs.append((slug, scen["title"], scen["name"]))
    else:
        # SVG mode — skip browser capture (not supported).
        print("\nSkipping web snapshots (SVG mode not supported for browser captures)\n")

    # ── Status text and markdown reports ────────────────────────
    print(f"\nGenerating {len(active_text)} status + report outputs\n")

    text_results:   list[TextResult] = []
    report_results: list[TextResult] = []

    for scen in active_text:
        slug     = scen["slug"]
        title    = scen["title"]
        name     = scen["name"]
        scenario = _SCEN / scen["scenario"]

        print(f"[{slug}] status …", end=" ", flush=True)
        t0 = time.monotonic()
        text = asyncio.run(_capture_status_text(scenario))
        print(f"done ({time.monotonic()-t0:.1f}s)")
        text_results.append((slug, title, name, text))

        print(f"[{slug}] report …", end=" ", flush=True)
        t0 = time.monotonic()
        md = asyncio.run(_capture_report_md(scenario))
        print(f"done ({time.monotonic()-t0:.1f}s)")
        report_results.append((slug, title, name, md))

    # ── Write docs ───────────────────────────────────────────────
    doc_path = _write_output_formats_doc(out_dir, text_results, report_results, web_slugs, args.ext)
    _update_ui_states_doc(out_dir, text_results, report_results, web_slugs, args.ext)

    print(f"\nOutput-formats doc → {doc_path.relative_to(_REPO)}")
    print(f"UI states updated  → docs/ui-states.md")

    elapsed = time.monotonic() - t_start
    print(f"\nDone — {len(active_caps)} TUI snapshots + {len(web_slugs)} web snapshots"
          f" + {len(active_text)} status/report pairs in {elapsed:.0f}s")


if __name__ == "__main__":
    main()
