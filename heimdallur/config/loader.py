import tomllib
import os
from pathlib import Path
from heimdallur.core.topology import Contacts, Device, GmailNotificationConfig, Group, NetworkConfig

_CONFIG_DIR = Path(__file__).parent
_DEFAULT_PATH = _CONFIG_DIR / "default-network.toml"
_XDG_CONFIG_HOME = Path(os.getenv("XDG_CONFIG_HOME", str(Path.home() / ".config"))).expanduser()
_USER_PATH = _XDG_CONFIG_HOME / "heimdallur" / "network.toml"


def user_config_path() -> Path:
    """Return the default writable user configuration path."""
    return _USER_PATH


def default_config_path() -> Path:
    """Return the packaged demo/default configuration path."""
    return _DEFAULT_PATH


def resolve_config_path(path: Path | None = None) -> Path:
    if path is not None:
        return path
    if env_path := os.getenv("HEIMDALLUR_CONFIG"):
        return Path(env_path).expanduser()
    if _USER_PATH.exists():
        return _USER_PATH
    return _DEFAULT_PATH


def load_config(path: Path | None = None) -> NetworkConfig:
    config_path = resolve_config_path(path)
    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    ct = data.get("contacts", {})
    contacts = Contacts(
        network_admin=ct.get("network_admin", "network admin"),
        home_network_admin_email=ct.get("home_network_admin_email", ""),
        isp_name=ct.get("isp_name", "ISP"),
    )

    notifications = data.get("notifications", {})
    gmail_notification = GmailNotificationConfig(
        enabled=bool(notifications.get("enabled", False)),
        sender_email=os.getenv("HEIMDALLUR_GMAIL_SENDER_EMAIL", ""),
        app_password=os.getenv("HEIMDALLUR_GMAIL_APP_PASSWORD", ""),
    )
    net = data["network"]
    groups = [
        Group(
            id=g["id"],
            name=g["name"],
            type=g["type"],
            gateway_ip=g.get("gateway_ip", ""),
            gateway_name=g.get("gateway_name", ""),
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
        contacts=contacts,
        gmail_notification=gmail_notification,
    )
