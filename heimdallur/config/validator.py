from __future__ import annotations

import ipaddress
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_REQUIRED_GROUP_TYPES = {"wifi", "lan"}
_REQUIRED_DEVICE_TYPES = {"generic", "light", "sensor", "smart_plug", "smart_switch", "server", "ap"}


@dataclass
class ValidationResult:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    group_count: int = 0
    device_count: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def _valid_ip(value: Any) -> bool:
    try:
        ipaddress.ip_address(str(value))
        return True
    except ValueError:
        return False


def validate_config(path: Path) -> ValidationResult:
    result = ValidationResult(path=path)

    if not path.exists():
        result.errors.append(f"File not found: {path}")
        return result

    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        result.errors.append(f"TOML parse error: {exc}")
        return result
    except OSError as exc:
        result.errors.append(f"Could not read file: {exc}")
        return result

    net = data.get("network")
    if not isinstance(net, dict):
        result.errors.append("Missing [network] section")
    else:
        for key in ("ont_check_host", "router_ip"):
            if key not in net:
                result.errors.append(f"[network] missing required key: {key}")
            elif not _valid_ip(net[key]):
                result.errors.append(f"[network].{key} is not a valid IP address: {net[key]!r}")
        for key in ("probe_interval_seconds", "speed_test_interval_seconds"):
            if key in net and not isinstance(net[key], int):
                result.errors.append(f"[network].{key} must be an integer, got {type(net[key]).__name__}")

    groups = data.get("groups", [])
    if not isinstance(groups, list):
        result.errors.append("'groups' must be an array")
        groups = []
    result.group_count = len(groups)

    group_ids: set[str] = set()
    for i, group in enumerate(groups):
        prefix = f"groups[{i}]"
        if not isinstance(group, dict):
            result.errors.append(f"{prefix}: must be a table")
            continue
        for key in ("id", "name", "type"):
            if key not in group:
                result.errors.append(f"{prefix}: missing required key '{key}'")
        gid = group.get("id")
        if isinstance(gid, str):
            if gid in group_ids:
                result.errors.append(f"{prefix}: duplicate group id {gid!r}")
            group_ids.add(gid)
        gtype = group.get("type", "")
        if gtype not in _REQUIRED_GROUP_TYPES:
            result.errors.append(
                f"{prefix} ({gid or '?'}): type must be one of {sorted(_REQUIRED_GROUP_TYPES)}, got {gtype!r}"
            )
        gateway_ip = group.get("gateway_ip", "")
        if gateway_ip and not _valid_ip(gateway_ip):
            result.errors.append(f"{prefix} ({gid or '?'}): gateway_ip is not a valid IP address: {gateway_ip!r}")

    devices = data.get("devices", [])
    if not isinstance(devices, list):
        result.errors.append("'devices' must be an array")
        devices = []
    result.device_count = len(devices)

    seen_ips: set[str] = set()
    for i, device in enumerate(devices):
        prefix = f"devices[{i}]"
        if not isinstance(device, dict):
            result.errors.append(f"{prefix}: must be a table")
            continue
        for key in ("name", "ip", "group"):
            if key not in device:
                result.errors.append(f"{prefix}: missing required key '{key}'")
        ip = device.get("ip", "")
        if ip:
            if not _valid_ip(ip):
                result.errors.append(f"{prefix} ({device.get('name', '?')!r}): ip is not a valid IP address: {ip!r}")
            elif ip in seen_ips:
                result.errors.append(f"{prefix} ({device.get('name', '?')!r}): duplicate IP {ip!r}")
            seen_ips.add(ip)
        group_id = device.get("group", "")
        if group_id and group_id not in group_ids:
            result.errors.append(f"{prefix} ({device.get('name', '?')!r}): group {group_id!r} is not defined in [[groups]]")
        device_type = device.get("type", "generic")
        if device_type not in _REQUIRED_DEVICE_TYPES:
            result.warnings.append(
                f"{prefix} ({device.get('name', '?')!r}): unknown device type {device_type!r} (will be treated as generic)"
            )

    return result


def format_validation_result(result: ValidationResult) -> str:
    lines = [f"Validating: {result.path}"]
    for warning in result.warnings:
        lines.append(f"  WARN  {warning}")
    for error in result.errors:
        lines.append(f"  ERROR {error}")
    if result.ok:
        lines.append(f"  OK    Config is valid ({result.group_count} groups, {result.device_count} devices)")
    else:
        lines.append(f"")
        lines.append(f"{len(result.errors)} error(s) found. Config NOT applied.")
    return "\n".join(lines)
