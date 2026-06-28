#!/usr/bin/env python3
"""Safely apply a Heimdallur network config.

Run this on the target host after copying a candidate TOML there.

Examples:
    python scripts/apply-config.py /tmp/network.toml --dry-run
    python scripts/apply-config.py /tmp/network.toml --yes \
        --restart-command 'sudo systemctl restart getty@tty1.service' \
        --restart-command 'sudo systemctl restart heimdallur-web.service' \
        --verify
"""
from __future__ import annotations

import argparse
import difflib
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from heimdallur.config.loader import default_config_path, user_config_path
from heimdallur.config.validator import format_validation_result, validate_config

_DEFAULT_BACKUP_DIR = Path.home() / ".local" / "share" / "heimdallur" / "config-backups"
_DEFAULT_STATUS_PATH = Path.home() / ".local" / "share" / "heimdallur" / "status.md"


def _read_lines(path: Path) -> list[str]:
    try:
        return path.read_text().splitlines()
    except FileNotFoundError:
        return []


def _print_diff(current: Path, candidate: Path) -> None:
    current_lines = _read_lines(current)
    candidate_lines = _read_lines(candidate)
    if current_lines == candidate_lines:
        print("No config changes detected.")
        return

    print("Config diff:")
    print("\n".join(difflib.unified_diff(
        current_lines,
        candidate_lines,
        fromfile=str(current),
        tofile=str(candidate),
        lineterm="",
    )))


def _backup_current(dest: Path, backup_dir: Path) -> Path | None:
    if not dest.exists():
        print(f"No existing config at {dest}; no backup created.")
        return None

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"{dest.name}.{stamp}.bak"
    shutil.copy2(dest, backup)
    print(f"Backup created: {backup}")
    return backup


def _run_command(command: str) -> None:
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)


def _verify_status_fresh(status_path: Path, started_at: float, timeout: int) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            mtime = status_path.stat().st_mtime
        except FileNotFoundError:
            time.sleep(2)
            continue
        if mtime >= started_at:
            age = max(0, int(time.time() - mtime))
            print(f"Verified fresh status: {status_path} ({age}s old)")
            return True
        time.sleep(2)

    print(f"ERROR: {status_path} did not update within {timeout}s", file=sys.stderr)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="candidate network TOML to apply")
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help=f"destination config path (default: {user_config_path()})",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=_DEFAULT_BACKUP_DIR,
        help=f"backup directory (default: {_DEFAULT_BACKUP_DIR})",
    )
    parser.add_argument("--dry-run", action="store_true", help="validate and diff only; do not apply")
    parser.add_argument("--yes", action="store_true", help="required to apply changes")
    parser.add_argument(
        "--restart-command",
        action="append",
        default=[],
        help="command to run after applying; may be supplied multiple times",
    )
    parser.add_argument("--verify", action="store_true", help="wait for status.md to be freshly written")
    parser.add_argument(
        "--status-path",
        type=Path,
        default=_DEFAULT_STATUS_PATH,
        help=f"status file to verify (default: {_DEFAULT_STATUS_PATH})",
    )
    parser.add_argument("--verify-timeout", type=int, default=75, help="seconds to wait for fresh status")
    args = parser.parse_args()

    candidate = args.candidate.expanduser().resolve()
    dest_was_explicit = args.dest is not None
    dest = (args.dest.expanduser() if dest_was_explicit else user_config_path()).resolve()
    default_dest = default_config_path().resolve()

    if dest == default_dest and not dest_was_explicit:
        print(
            f"ERROR: refusing to apply config to packaged demo config: {default_dest}",
            file=sys.stderr,
        )
        print("Pass --dest explicitly only if you really intend to target that file.", file=sys.stderr)
        raise SystemExit(2)

    print(f"Candidate:   {candidate}")
    print(f"Destination: {dest}")
    print()

    result = validate_config(candidate)
    print(format_validation_result(result))
    if not result.ok:
        raise SystemExit(1)

    print()
    _print_diff(dest, candidate)

    if args.dry_run:
        print("\nDry run complete. No files changed.")
        return

    if not args.yes:
        print("\nRefusing to apply without --yes. Re-run with --yes after reviewing the diff.", file=sys.stderr)
        raise SystemExit(2)

    started_at = time.time()
    backup = _backup_current(dest, args.backup_dir.expanduser())
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(candidate, dest)
    if dest == user_config_path().resolve():
        dest.parent.chmod(0o700)
        dest.chmod(0o600)
    print(f"Applied config: {candidate} -> {dest}")

    try:
        for command in args.restart_command:
            _run_command(command)
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: restart command failed with exit code {exc.returncode}", file=sys.stderr)
        if backup:
            print(f"Rollback: cp {backup} {dest}", file=sys.stderr)
        raise SystemExit(exc.returncode)

    if args.verify:
        if not _verify_status_fresh(args.status_path.expanduser(), started_at, args.verify_timeout):
            if backup:
                print(f"Rollback: cp {backup} {dest}", file=sys.stderr)
            raise SystemExit(1)

    if backup:
        print(f"Rollback: cp {backup} {dest}")
    print("Config apply complete.")


if __name__ == "__main__":
    main()
