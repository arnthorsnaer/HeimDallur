#!/usr/bin/env python3
"""Check a Heimdallur deployment and print actionable diagnostics.

This script is read-only: it reports problems and suggested next steps, but does
not modify the system.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from shutil import which

from heimdallur.config.loader import resolve_config_path
from heimdallur.config.validator import validate_config
from heimdallur.version import __version__

OK = "ok"
WARN = "warn"
FAIL = "fail"


@dataclass
class Check:
    name: str
    status: str
    summary: str
    why: str = ""
    next_steps: list[str] = field(default_factory=list)


class Doctor:
    def __init__(self, *, app_dir: Path, status_path: Path, state_path: Path, db_path: Path, max_age: int | None) -> None:
        self.app_dir = app_dir
        self.status_path = status_path
        self.state_path = state_path
        self.db_path = db_path
        self.max_age = max_age
        self.checks: list[Check] = []
        self.probe_interval = 30

    def add(self, check: Check) -> None:
        self.checks.append(check)

    def run(self, *, print_report: bool = True) -> int:
        self.check_version()
        self.check_config()
        self.check_runtime_env()
        self.check_status_files()
        self.check_db()
        self.check_processes()
        self.check_systemd()
        self.check_git()
        self.check_network()
        self.check_display_optional()
        if print_report:
            self.print_report()
        return 1 if any(c.status == FAIL for c in self.checks) else 0

    def check_version(self) -> None:
        self.add(Check("version", OK, __version__))

    def check_config(self) -> None:
        path = resolve_config_path()
        result = validate_config(path)
        if result.ok:
            self.probe_interval = _load_probe_interval(path) or self.probe_interval
            self.add(Check("config", OK, f"{path} ({result.group_count} groups, {result.device_count} devices)"))
        else:
            self.add(Check(
                "config",
                FAIL,
                f"invalid: {path}",
                why="Heimdallur may not start, and status output may be stale or missing.",
                next_steps=[f"python -m heimdallur --mode validate-config {path}"],
            ))

    def check_runtime_env(self) -> None:
        if os.getenv("NETWATCH_MOCK"):
            self.add(Check(
                "mock mode",
                WARN,
                "NETWATCH_MOCK is set in this process",
                why="Production should normally probe the real network, not mock data.",
                next_steps=["Check the service environment or tty startup file for NETWATCH_MOCK."],
            ))
        else:
            self.add(Check("mock mode", OK, "off"))

    def check_status_files(self) -> None:
        max_age = self.max_age if self.max_age is not None else max(60, self.probe_interval * 2)
        for name, path in (("status.md", self.status_path), ("live-state.json", self.state_path)):
            if not path.exists():
                self.add(Check(
                    name,
                    FAIL,
                    f"missing: {path}",
                    why=f"Agents and web viewers rely on {name} for current Heimdallur state.",
                    next_steps=[
                        'pgrep -af "python.*heimdallur|web_serve.py"',
                        "Check the primary TUI/prober process or service logs.",
                    ],
                ))
                continue
            age = int(time.time() - path.stat().st_mtime)
            status = OK if age <= max_age else WARN
            self.add(Check(
                name,
                status,
                f"{age}s old at {path}",
                why="Stale status can make agents or the web UI report old information." if status == WARN else "",
                next_steps=["Restart or inspect the primary TUI/prober if this file stops updating." ] if status == WARN else [],
            ))

    def check_db(self) -> None:
        if not self.db_path.exists():
            self.add(Check(
                "events db",
                WARN,
                f"missing: {self.db_path}",
                why="History and future diagnostics rely on SQLite probe events.",
                next_steps=["Confirm the primary TUI/prober has completed at least one probe cycle."],
            ))
            return
        try:
            with sqlite3.connect(self.db_path) as db:
                db.execute("select count(*) from probe_events").fetchone()
            self.add(Check("events db", OK, str(self.db_path)))
        except Exception as exc:
            self.add(Check(
                "events db",
                FAIL,
                f"unreadable: {exc}",
                why="Heimdallur may be unable to record history.",
                next_steps=[f"Check permissions and integrity for {self.db_path}"],
            ))

    def check_processes(self) -> None:
        procs = _cmd(["pgrep", "-af", "python.*heimdallur|web_serve.py"]).stdout.strip().splitlines()
        primary = [p for p in procs if "-m heimdallur --mode tui" in p]
        web = [p for p in procs if "web_serve.py" in p]
        standalone = [p for p in procs if "--standalone" in p]

        if primary:
            self.add(Check("primary monitor", OK, primary[0]))
        else:
            self.add(Check(
                "primary monitor",
                FAIL,
                "not found",
                why="The primary TUI/prober writes status.md and live-state.json.",
                next_steps=["Start/restart the Heimdallur display process or service."],
            ))

        if web:
            status = WARN if standalone else OK
            self.add(Check(
                "web UI process",
                status,
                web[0] + (" (standalone)" if standalone else ""),
                why="Standalone web UI runs a second prober instead of reading shared state." if standalone else "",
                next_steps=["Remove --standalone unless a second independent prober is intended."] if standalone else [],
            ))
        else:
            self.add(Check(
                "web UI process",
                WARN,
                "not found",
                why="The browser UI and /status.md endpoint will not be available.",
                next_steps=["Start heimdallur-web.service or run scripts/web_serve.py."],
            ))

    def check_systemd(self) -> None:
        if which("systemctl") is None:
            self.add(Check("systemd", WARN, "systemctl not found"))
            return
        for unit, required in (("heimdallur-web.service", False), ("heimdallur-update.timer", False)):
            enabled = _cmd(["systemctl", "is-enabled", unit]).stdout.strip()
            active = _cmd(["systemctl", "is-active", unit]).stdout.strip()
            if active == "active":
                self.add(Check(unit, OK, f"active, enabled={enabled or 'unknown'}"))
            else:
                self.add(Check(
                    unit,
                    FAIL if required else WARN,
                    f"{active or 'not installed'}, enabled={enabled or 'unknown'}",
                    why="This unit is commonly used in production deployments.",
                    next_steps=[f"systemctl status {unit} --no-pager -l"],
                ))

    def check_git(self) -> None:
        if not (self.app_dir / ".git").exists():
            self.add(Check("git", WARN, f"not a git checkout: {self.app_dir}"))
            return
        branch = _git(self.app_dir, "branch", "--show-current")
        commit = _git(self.app_dir, "log", "-1", "--oneline")
        dirty = _git(self.app_dir, "status", "--short")
        status = OK if branch == "main" and not dirty else WARN
        summary = f"{branch or '?'} · {commit or '?'}" + (" · dirty" if dirty else "")
        self.add(Check(
            "git checkout",
            status,
            summary,
            why="Auto-update expects a clean checkout on the deployment branch." if status == WARN else "",
            next_steps=["cd /opt/heimdallur && git status --short && git branch --show-current"] if status == WARN else [],
        ))
        bad_git_files = _root_owned_git_files(self.app_dir)
        if bad_git_files:
            self.add(Check(
                "git permissions",
                FAIL,
                f"{len(bad_git_files)} .git file(s) not owned by current user",
                why="Root-owned git metadata can break fetch/pull during auto-update.",
                next_steps=[f"sudo chown -R $(whoami):$(id -gn) {self.app_dir / '.git'}"],
            ))
        else:
            self.add(Check("git permissions", OK, ".git ownership looks usable"))

    def check_network(self) -> None:
        route = _cmd(["ip", "route", "get", "1.1.1.1"]).stdout.strip()
        if route:
            self.add(Check("default route", OK, route.splitlines()[0]))
        else:
            self.add(Check(
                "default route",
                FAIL,
                "missing",
                why="Internet checks cannot run without a default route.",
                next_steps=["ip route", "nmcli dev status"],
            ))

        defaults = _cmd(["ip", "route", "show", "default"]).stdout.strip().splitlines()
        if len(defaults) > 1:
            self.add(Check(
                "multiple default routes",
                WARN,
                f"{len(defaults)} default routes configured",
                why="Heimdallur may fail over to Wi-Fi or another interface without that being obvious.",
                next_steps=["ip route show default", "Disable unwanted fallback interfaces if production should be wired-only."],
            ))
        else:
            self.add(Check("multiple default routes", OK, "no fallback default route"))

        wlan = _cmd(["ip", "-br", "addr", "show", "dev", "wlan0"]).stdout.strip()
        if wlan and " UP " in f" {wlan} ":
            self.add(Check(
                "wifi interface",
                WARN,
                wlan,
                why="If Wi-Fi remains active, the monitor may keep working when Ethernet fails.",
                next_steps=["nmcli con mod <wifi-connection> connection.autoconnect no", "nmcli con down <wifi-connection>"],
            ))
        elif wlan:
            self.add(Check("wifi interface", OK, wlan))

        listeners = _cmd(["ss", "-tulpn"]).stdout
        if ":80 " in listeners or ":8080 " in listeners:
            self.add(Check("web listener", OK, _first_listener_line(listeners)))
        else:
            self.add(Check(
                "web listener",
                WARN,
                "no :80 or :8080 listener found",
                why="The browser UI and /status.md endpoint may be unavailable.",
                next_steps=["systemctl status heimdallur-web.service --no-pager -l", "ss -tulpn | grep -E ':(80|8080) '"],
            ))

    def check_display_optional(self) -> None:
        tty1 = Path("/dev/tty1")
        self.add(Check("tty1", OK if tty1.exists() else WARN, "present" if tty1.exists() else "missing"))
        setup = Path("/etc/default/console-setup")
        self.add(Check("console font", OK if setup.exists() else WARN, str(setup) if setup.exists() else "not configured"))
        cmdline = Path("/boot/firmware/cmdline.txt")
        if cmdline.exists() and "consoleblank=" in cmdline.read_text(errors="ignore"):
            self.add(Check("console blanking", OK, "configured"))
        else:
            self.add(Check("console blanking", WARN, "not configured", why="Always-on displays may use more power and heat without blanking."))

    def to_dict(self) -> dict:
        failures = sum(1 for c in self.checks if c.status == FAIL)
        warnings = sum(1 for c in self.checks if c.status == WARN)
        return {
            "failures": failures,
            "warnings": warnings,
            "checks": [asdict(check) for check in self.checks],
        }

    def print_json(self) -> None:
        print(json.dumps(self.to_dict(), ensure_ascii=False))

    def print_report(self) -> None:
        print("HEIMDALLUR DOCTOR")
        print()
        for check in self.checks:
            icon = {OK: "✓", WARN: "⚠", FAIL: "✗"}[check.status]
            print(f"{icon} {check.name}: {check.summary}")
            if check.why:
                print(f"  Why: {check.why}")
            if check.next_steps:
                print("  Next:")
                for step in check.next_steps:
                    print(f"    {step}")
        print()
        failures = sum(1 for c in self.checks if c.status == FAIL)
        warnings = sum(1 for c in self.checks if c.status == WARN)
        print(f"Summary: {failures} failure(s), {warnings} warning(s)")


def _cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(args, text=True, capture_output=True, timeout=5)
    except Exception as exc:
        return subprocess.CompletedProcess(args, 1, "", str(exc))


def _git(app_dir: Path, *args: str) -> str:
    return _cmd(["git", "-C", str(app_dir), *args]).stdout.strip()


def _root_owned_git_files(app_dir: Path) -> list[Path]:
    git_dir = app_dir / ".git"
    if not git_dir.exists() or os.name != "posix":
        return []
    uid = os.getuid()
    bad: list[Path] = []
    for path in git_dir.rglob("*"):
        try:
            if path.stat().st_uid != uid:
                bad.append(path)
                if len(bad) >= 10:
                    break
        except OSError:
            continue
    return bad


def _first_listener_line(listeners: str) -> str:
    for line in listeners.splitlines():
        if ":80 " in line or ":8080 " in line:
            return line.strip()
    return "listener found"


def _load_probe_interval(path: Path) -> int | None:
    try:
        import tomllib
        with path.open("rb") as f:
            data = tomllib.load(f)
        return int(data.get("network", {}).get("probe_interval_seconds", 30))
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-dir", type=Path, default=Path.cwd())
    parser.add_argument("--status-path", type=Path, default=Path.home() / ".local" / "share" / "heimdallur" / "status.md")
    parser.add_argument("--state-path", type=Path, default=Path.home() / ".local" / "share" / "heimdallur" / "live-state.json")
    parser.add_argument("--db-path", type=Path, default=Path.home() / ".local" / "share" / "heimdallur" / "events.db")
    parser.add_argument("--max-age", type=int, default=None, help="freshness threshold in seconds; default is max(60, 2x probe interval)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()

    doctor = Doctor(
        app_dir=args.app_dir.expanduser().resolve(),
        status_path=args.status_path.expanduser(),
        state_path=args.state_path.expanduser(),
        db_path=args.db_path.expanduser(),
        max_age=args.max_age,
    )
    exit_code = doctor.run(print_report=not args.json)
    if args.json:
        doctor.print_json()
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
