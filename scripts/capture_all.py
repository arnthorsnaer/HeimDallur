#!/usr/bin/env python3
"""Generate screenshots for every meaningful UI state of Heimdallur.

Runs scripts/screenshot.py once per scenario (via subprocess so each
capture gets a clean process state).  Outputs to docs/screenshots/.

Usage:
    python scripts/capture_all.py [--output-dir DIR] [--png | --svg]

Produces one image per entry in CAPTURES, named by slug.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

_REPO   = Path(__file__).parent.parent
_SCRIPT = _REPO / "scripts" / "screenshot.py"
_SCEN   = _REPO / "heimdallur" / "mock" / "scenarios"

# ── All captures ───────────────────────────────────────────────
# Each entry renders one screenshot.  Fields:
#   slug     unique filename stem (determines sort order in PR gallery)
#   title    human-readable caption shown in PR description
#   scenario scenario TOML filename (relative to heimdallur/mock/scenarios/)
#   keys     optional list of Textual key names pressed after settling
CAPTURES: list[dict] = [
    # ── Status screen variants ─────────────────────────────────
    {
        "slug":     "01-status-healthy",
        "title":    "Status screen — all healthy",
        "scenario": "all_healthy.toml",
    },
    {
        "slug":     "02-status-internet-degraded",
        "title":    "Status screen — internet degraded (high latency)",
        "scenario": "internet_degraded.toml",
    },
    {
        "slug":     "03-status-internet-offline",
        "title":    "Status screen — internet offline",
        "scenario": "internet_offline.toml",
    },
    {
        "slug":     "04-status-router-offline",
        "title":    "Status screen — router offline (all devices cascade to unknown)",
        "scenario": "router_offline.toml",
    },
    {
        "slug":     "05-status-gateway-offline",
        "title":    "Status screen — AP offline (Basement, 9 devices suppressed)",
        "scenario": "gateway_offline.toml",
    },
    {
        "slug":     "06-status-multiple-issues",
        "title":    "Status screen — multiple issues (AP down + degraded + flapping device)",
        "scenario": "multiple_issues.toml",
    },
    # ── Expanded panels ────────────────────────────────────────
    {
        "slug":     "07-inet-panel-expanded",
        "title":    "Internet panel expanded (latency sparkline + speed-test detail)",
        "scenario": "all_healthy.toml",
        "keys":     ["i"],
    },
    {
        "slug":     "08-rtr-panel-expanded",
        "title":    "Router panel expanded (CPU sparkline + memory / uptime)",
        "scenario": "all_healthy.toml",
        "keys":     ["r"],
    },
    # ── Other screens ──────────────────────────────────────────
    {
        "slug":     "09-history-screen",
        "title":    "History screen (24 h uptime bars)",
        "scenario": "multiple_issues.toml",
        "keys":     ["h"],
    },
    {
        "slug":     "10-devices-screen",
        "title":    "Devices screen (per-device latency + status)",
        "scenario": "gateway_offline.toml",
        "keys":     ["d"],
    },
]


def run_capture(capture: dict, out_dir: Path, ext: str) -> Path:
    slug     = capture["slug"]
    scenario = str(_SCEN / capture["scenario"])
    keys     = ",".join(capture.get("keys", []))
    outfile  = out_dir / f"{slug}.{ext}"

    cmd = [sys.executable, str(_SCRIPT), str(outfile),
           "--scenario", scenario]
    if keys:
        cmd += ["--keys", keys]

    print(f"\n[{slug}]  {capture['title']}")
    t0 = time.monotonic()
    result = subprocess.run(cmd, cwd=str(_REPO))
    elapsed = time.monotonic() - t0

    if result.returncode != 0:
        print(f"  FAILED (exit {result.returncode})")
        sys.exit(result.returncode)

    print(f"  done in {elapsed:.1f}s")
    return outfile


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", default="docs/screenshots",
                        help="Destination directory (default: docs/screenshots)")
    fmt = parser.add_mutually_exclusive_group()
    fmt.add_argument("--png", dest="ext", action="store_const", const="png",
                     help="Output PNG via rsvg-convert (default)")
    fmt.add_argument("--svg", dest="ext", action="store_const", const="svg",
                     help="Output raw SVG (no rsvg-convert needed)")
    parser.set_defaults(ext="png")
    args = parser.parse_args()

    out_dir = (_REPO / args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(CAPTURES)} screenshots → {out_dir}")
    t_start = time.monotonic()

    files: list[tuple[dict, Path]] = []
    for capture in CAPTURES:
        path = run_capture(capture, out_dir, args.ext)
        files.append((capture, path))

    elapsed = time.monotonic() - t_start
    print(f"\nDone — {len(files)} screenshots in {elapsed:.0f}s")
    for cap, path in files:
        print(f"  {path.name}  —  {cap['title']}")


if __name__ == "__main__":
    main()
