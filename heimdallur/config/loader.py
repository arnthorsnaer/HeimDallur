import tomllib
from pathlib import Path
from heimdallur.core.topology import Device, Group, NetworkConfig

_DEFAULT_PATH = Path(__file__).parent / "devices.toml"


def load_config(path: Path | None = None) -> NetworkConfig:
    config_path = path or _DEFAULT_PATH
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    net = data["network"]
    groups = [
        Group(
            id=g["id"],
            name=g["name"],
            type=g["type"],
            gateway_ip=g.get("gateway_ip", ""),
            gateway_name=g.get("gateway_name", ""),
            gateway_model=g.get("gateway_model", ""),
            channel=g.get("channel", 0),
            band=g.get("band", ""),
        )
        for g in data.get("groups", [])
    ]
    devices = [
        Device(
            name=d["name"],
            ip=d["ip"],
            group_id=d["group"],
            device_type=d.get("type", "generic"),
        )
        for d in data.get("devices", [])
    ]
    return NetworkConfig(
        ont_check_host=net["ont_check_host"],
        router_ip=net["router_ip"],
        probe_interval_seconds=net.get("probe_interval_seconds", 30),
        speed_test_interval_seconds=net.get("speed_test_interval_seconds", 300),
        groups=groups,
        devices=devices,
    )
