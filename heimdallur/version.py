from __future__ import annotations

import subprocess
from importlib.metadata import version, PackageNotFoundError

try:
    _base = version("heimdallur")
except PackageNotFoundError:
    _base = "0.0.0"

def _git_output(*args: str, fallback: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return fallback


_sha = _git_output("rev-parse", "--short", "HEAD", fallback="abc1234")
_commit_date = _git_output(
    "show", "-s", "--format=%cd", "--date=format:%Y%m%d", "HEAD",
    fallback="00000000",
)

__version__ = f"{_base}+{_commit_date}.{_sha}"
