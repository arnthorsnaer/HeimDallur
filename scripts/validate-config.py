#!/usr/bin/env python3
"""Validate a Heimdallur network TOML before applying it to production.

Usage:
    python scripts/validate-config.py                          # validates the default config
    python scripts/validate-config.py /path/to/network.toml   # validates a given file

Exits 0 on success, 1 on any error. All output goes to stdout so agents can capture it.
"""
from pathlib import Path
import sys

from heimdallur.config.validator import format_validation_result, validate_config

_DEFAULT = Path(__file__).parent.parent / "heimdallur" / "config" / "default-network.toml"


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else _DEFAULT
    result = validate_config(path)
    print(format_validation_result(result))
    sys.exit(0 if result.ok else 1)


if __name__ == "__main__":
    main()
