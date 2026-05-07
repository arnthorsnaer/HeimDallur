from __future__ import annotations

import subprocess
from datetime import date
from importlib.metadata import version, PackageNotFoundError

try:
    _base = version("heimdallur")
except PackageNotFoundError:
    _base = "0.0.0"

try:
    _sha = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()
except Exception:
    _sha = "abc1234"

_date = date.today().strftime("%Y%m%d")

__version__ = f"{_base}+{_date}.{_sha}"
