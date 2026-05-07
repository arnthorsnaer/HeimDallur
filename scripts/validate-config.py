#!/usr/bin/env python3
"""Validate heimdallur/config/network.toml before applying it to production.

Usage:
    python scripts/validate-config.py                          # validates the default config
    python scripts/validate-config.py /path/to/network.toml   # validates a given file

Exits 0 on success, 1 on any error. All output goes to stdout so agents can capture it.
"""
import ipaddress
import sys
import tomllib
from pathlib import Path

_DEFAULT = Path(__file__).parent.parent / "heimdallur" / "config" / "network.toml"
_REQUIRED_GROUP_TYPES = {"wifi", "lan"}
_REQUIRED_DEVICE_TYPES = {"generic", "light", "sensor", "smart_plug", "smart_switch", "server", "ap"}

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def _valid_ip(s: str) -> bool:
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def validate(path: Path) -> bool:
    if not path.exists():
        err(f"File not found: {path}")
        return False

    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        err(f"TOML parse error: {e}")
        return False

    # [network]
    net = data.get("network")
    if not isinstance(net, dict):
        err("Missing [network] section")
    else:
        for key in ("ont_check_host", "router_ip"):
            if key not in net:
                err(f"[network] missing required key: {key}")
            elif not _valid_ip(str(net[key])):
                err(f"[network].{key} is not a valid IP address: {net[key]!r}")
        for key in ("probe_interval_seconds", "speed_test_interval_seconds"):
            if key in net and not isinstance(net[key], int):
                err(f"[network].{key} must be an integer, got {type(net[key]).__name__}")

    # [[groups]]
    groups = data.get("groups", [])
    if not isinstance(groups, list):
        err("'groups' must be an array")
        groups = []

    group_ids: set[str] = set()
    for i, g in enumerate(groups):
        prefix = f"groups[{i}]"
        if not isinstance(g, dict):
            err(f"{prefix}: must be a table")
            continue
        for key in ("id", "name", "type"):
            if key not in g:
                err(f"{prefix}: missing required key '{key}'")
        gid = g.get("id", f"<unnamed-{i}>")
        if gid in group_ids:
            err(f"{prefix}: duplicate group id {gid!r}")
        group_ids.add(gid)
        gtype = g.get("type", "")
        if gtype not in _REQUIRED_GROUP_TYPES:
            err(f"{prefix} ({gid!r}): type must be one of {sorted(_REQUIRED_GROUP_TYPES)}, got {gtype!r}")
        gw = g.get("gateway_ip", "")
        if gw and not _valid_ip(str(gw)):
            err(f"{prefix} ({gid!r}): gateway_ip is not a valid IP address: {gw!r}")

    # [[devices]]
    devices = data.get("devices", [])
    if not isinstance(devices, list):
        err("'devices' must be an array")
        devices = []

    seen_ips: set[str] = set()
    for i, d in enumerate(devices):
        prefix = f"devices[{i}]"
        if not isinstance(d, dict):
            err(f"{prefix}: must be a table")
            continue
        for key in ("name", "ip", "group"):
            if key not in d:
                err(f"{prefix}: missing required key '{key}'")
        ip = d.get("ip", "")
        if ip:
            if not _valid_ip(str(ip)):
                err(f"{prefix} ({d.get('name', '?')!r}): ip is not a valid IP address: {ip!r}")
            elif ip in seen_ips:
                err(f"{prefix} ({d.get('name', '?')!r}): duplicate IP {ip!r}")
            seen_ips.add(ip)
        grp = d.get("group", "")
        if grp and grp not in group_ids:
            err(f"{prefix} ({d.get('name', '?')!r}): group {grp!r} is not defined in [[groups]]")
        dtype = d.get("type", "generic")
        if dtype not in _REQUIRED_DEVICE_TYPES:
            warn(f"{prefix} ({d.get('name', '?')!r}): unknown device type {dtype!r} (will be treated as generic)")

    return len(errors) == 0


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else _DEFAULT
    print(f"Validating: {path}")

    ok = validate(path)

    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")

    if ok:
        print(f"  OK    Config is valid ({len(data_summary(path))} groups, loaded successfully)")
    else:
        print(f"\n{len(errors)} error(s) found. Config NOT applied.")

    sys.exit(0 if ok else 1)


def data_summary(path: Path) -> list:
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return data.get("groups", [])


if __name__ == "__main__":
    main()
