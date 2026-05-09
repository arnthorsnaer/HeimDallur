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

# Chromium headless shell bundled with the system playwright installation.
_CHROMIUM = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"

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

# Web screenshots mirror the 6 base scenarios (one browser capture each).
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


# ── Web (browser) screenshot capture ────────────────────────────

_WEB_SETTLE   = 8.0   # seconds — wait for server + app to render in browser
_WEB_PORT_BASE = 18080  # start port; incremented per capture to avoid conflicts

def _capture_web_screenshot(
    scenario_path: Path,
    png_path: Path,
    port: int,
    extra_env: dict[str, str] | None = None,
) -> None:
    """Start textual-serve for the given scenario, take a browser screenshot, stop."""
    env = os.environ.copy()
    env["NETWATCH_MOCK"] = "1"
    env["NETWATCH_MOCK_SCENARIO"] = str(scenario_path)
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

        from playwright.sync_api import sync_playwright
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
    web_slugs: list[tuple[str, str]],            # (slug, title) captured web screenshots
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

    # ── Web UI Screenshots ────────────────────────────────────────
    if web_slugs:
        lines += [
            "## Web UI (`make web`)",
            "",
            "The same TUI served in a browser via textual-serve + xterm.js.",
            "Open `http://heimdallur.local:8080` from any device on the local network.",
            "",
        ]
        for slug, title in web_slugs:
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
    web_slugs: list[tuple[str, str]],            # (slug, title) captured web screenshots
    img_ext: str,
    github_repo: str | None = None,
    branch: str | None = None,
) -> Path:
    """Generate docs/pr-body.md — a ready-to-paste GitHub PR description.

    Four top-level collapsed sections (TUI screenshots / web UI screenshots /
    status / markdown report), each containing per-scenario collapsed sub-sections.

    When github_repo and branch are provided, screenshot URLs are absolute
    raw.githubusercontent.com links so images render in the PR description.
    """
    def _img_url(slug: str) -> str:
        rel = f"docs/screenshots/{slug}.{img_ext}"
        if github_repo and branch:
            return f"https://raw.githubusercontent.com/{github_repo}/{branch}/{rel}"
        return rel

    lines: list[str] = []

    # ── TUI Screenshots ──────────────────────────────────────────
    lines += ["<details>", "<summary><strong>TUI Screenshots</strong></summary>", ""]
    for slug, title, _ in text_results:
        lines += [
            "<details>",
            f"<summary>{title}</summary>",
            "",
            f"![{title}]({_img_url(slug)})",
            "",
            "</details>",
            "",
        ]
    lines += ["</details>", "", "---", ""]

    # ── Web UI Screenshots ────────────────────────────────────────
    if web_slugs:
        lines += ["<details>", "<summary><strong>Web UI Screenshots (<code>make web</code>)</strong></summary>", ""]
        for slug, title in web_slugs:
            lines += [
                "<details>",
                f"<summary>{title}</summary>",
                "",
                f"![{title}]({_img_url(slug)})",
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
    parser.add_argument(
        "--github-repo", default="arnthorsnaer/HeimDallur",
        help="owner/repo slug — used for absolute image URLs in pr-body.md",
    )
    parser.add_argument(
        "--scenarios",
        help=(
            "Comma-separated scenario names to capture (default: all). "
            f"Available: {', '.join(_ALL_SCENARIO_NAMES)}"
        ),
    )
    parser.add_argument(
        "--pr-only", action="store_true",
        help="Skip TUI screenshot generation; only regenerate status/report text and pr-body.md",
    )
    parser.add_argument(
        "--no-web", action="store_true",
        help="Skip web (browser) screenshot generation",
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

    # Detect current git branch for absolute image URLs in the PR body.
    try:
        import subprocess as _sp
        _branch = _sp.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=_REPO, text=True, stderr=_sp.DEVNULL,
        ).strip()
    except Exception:
        _branch = None

    out_dir = (_REPO / args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    t_start = time.monotonic()

    # ── TUI screenshots ──────────────────────────────────────────
    if not args.pr_only:
        print(f"Generating {len(active_caps)} TUI screenshots → {out_dir}\n")

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
        print("Skipping TUI screenshots (--pr-only)\n")

    # ── Web (browser) screenshots ────────────────────────────────
    web_slugs: list[tuple[str, str]] = []
    do_web = not args.no_web and args.ext == "png"
    if do_web and active_web:
        print(f"\nGenerating {len(active_web)} web (browser) screenshots\n")
        for idx, scen in enumerate(active_web):
            slug     = scen["slug"]
            title    = scen["title"]
            scenario = _SCEN / scen["scenario"]
            port     = _WEB_PORT_BASE + idx
            png_path = out_dir / f"{slug}.png"

            print(f"[{slug}] starting server on port {port} …", end=" ", flush=True)
            t0 = time.monotonic()
            _capture_web_screenshot(scenario, png_path, port)
            print(f"done ({time.monotonic()-t0:.1f}s) → {png_path.name}")
            web_slugs.append((slug, title))
    elif args.no_web:
        print("\nSkipping web screenshots (--no-web)\n")
        # Still include web entries in docs if the PNGs already exist.
        for scen in active_web:
            slug = scen["slug"]
            if (out_dir / f"{slug}.png").exists():
                web_slugs.append((slug, scen["title"]))
    else:
        # SVG mode — skip browser capture (not supported).
        print("\nSkipping web screenshots (SVG mode not supported for browser captures)\n")

    # ── Status text and markdown reports ────────────────────────
    print(f"\nGenerating {len(active_text)} status + report outputs\n")

    text_results:   list[tuple[str, str, str]] = []
    report_results: list[tuple[str, str, str]] = []

    for scen in active_text:
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
    doc_path = _write_output_formats_doc(out_dir, text_results, report_results, web_slugs, args.ext)
    pr_path  = _write_pr_body(
        out_dir, text_results, report_results, web_slugs, args.ext,
        github_repo=args.github_repo, branch=_branch,
    )
    print(f"\nOutput-formats doc → {doc_path.relative_to(_REPO)}")
    print(f"PR body            → {pr_path.relative_to(_REPO)}")

    elapsed = time.monotonic() - t_start
    print(f"\nDone — {len(active_caps)} TUI screenshots + {len(web_slugs)} web screenshots"
          f" + {len(active_text)} status/report pairs in {elapsed:.0f}s")


if __name__ == "__main__":
    main()
