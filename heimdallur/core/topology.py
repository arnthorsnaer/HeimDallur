from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class ProbeStatus(Enum):
    HEALTHY     = "healthy"
    DEGRADED    = "degraded"
    UNREACHABLE = "unreachable"
    UNKNOWN     = "unknown"


@dataclass
class ProbeResult:
    ip: str
    status: ProbeStatus
    response_ms: Optional[float]
    timestamp: float = field(default_factory=time.time)
    cause: Optional[str] = None


@dataclass
class Group:
    """A device group with an optional probed gateway (AP or managed switch)."""
    id: str
    name: str
    type: str           # "wifi" | "lan"
    gateway_ip: str     # empty string = no probed gateway (unmanaged switch / direct router)
    gateway_name: str = ""
    gateway_model: str = ""
    channel: int = 0
    band: str = ""


@dataclass
class Device:
    name: str
    ip: str
    group_id: str
    device_type: str = "generic"


@dataclass
class RouterStats:
    cpu_pct: float
    memory_pct: float
    uptime_seconds: float


@dataclass
class GatewayEnrichment:
    gateway_ip: str
    client_count: Optional[int]  # WiFi only


@dataclass
class SpeedResult:
    timestamp: float
    download_mbps: float
    ping_ms: float
    ok: bool


@dataclass
class RawIpResult:
    """Single ICMP probe to a well-known public IP."""
    target: str
    label: str
    status: ProbeStatus
    rtt_ms: Optional[float]


@dataclass
class DnsResult:
    """DNS lookup result for a well-known hostname."""
    hostname: str
    label: str
    success: bool
    lookup_ms: Optional[float]
    resolved_ip: Optional[str]


@dataclass
class HttpResult:
    """HTTP/HTTPS request quality metrics for a stable public endpoint."""
    url: str
    label: str
    short_path: str
    success: bool
    status_code: Optional[int]
    tcp_ms: Optional[float]
    tls_ms: Optional[float]
    ttfb_ms: Optional[float]
    total_ms: Optional[float]


@dataclass
class InternetQuality:
    """Aggregated result of a full multi-target internet quality probe run."""
    timestamp: float
    raw_ip: list[RawIpResult]
    dns: list[DnsResult]
    http: list[HttpResult]


@dataclass
class Contacts:
    network_admin: str = "network admin"
    home_network_admin_email: str = ""
    isp_name: str = "ISP"


@dataclass
class GmailNotificationConfig:
    sender_email: str = ""
    app_password: str = ""


@dataclass
class NetworkConfig:
    ont_check_host: str
    router_ip: str
    probe_interval_seconds: int
    speed_test_interval_seconds: int
    groups: list[Group]
    devices: list[Device]
    contacts: Contacts = field(default_factory=Contacts)
    gmail_notification: GmailNotificationConfig = field(default_factory=GmailNotificationConfig)

    def group_by_id(self) -> dict[str, Group]:
        return {g.id: g for g in self.groups}

    def devices_in_group(self, group_id: str) -> list[Device]:
        return [d for d in self.devices if d.group_id == group_id]


@dataclass
class NetworkState:
    timestamp: float
    ont_result: Optional[ProbeResult]
    router_result: Optional[ProbeResult]
    gateway_results: dict[str, ProbeResult]   # gateway_ip -> result (only probed gateways)
    device_results: dict[str, ProbeResult]

    def gateway_up(self, group: Group) -> bool:
        """True if the group's gateway is reachable (or has no gateway to probe)."""
        if not group.gateway_ip:
            return True
        r = self.gateway_results.get(group.gateway_ip)
        return r is None or r.status != ProbeStatus.UNREACHABLE

    def problems(self, config: NetworkConfig) -> list[str]:
        issues = []
        if self.ont_result and self.ont_result.status == ProbeStatus.UNREACHABLE:
            issues.append("Internet offline — full network unreachable")
            return issues
        if self.router_result and self.router_result.status == ProbeStatus.UNREACHABLE:
            issues.append("Router offline — home network affected")
            return issues

        # Report access point / switch failures.
        # Track their group IDs so we don't double-report the devices behind them.
        offline_group_ids: set[str] = set()
        for group in config.groups:
            if group.gateway_ip:
                r = self.gateway_results.get(group.gateway_ip)
                if r and r.status == ProbeStatus.UNREACHABLE:
                    n = len(config.devices_in_group(group.id))
                    label = "WiFi access point" if group.type == "wifi" else "switch"
                    issues.append(f"{group.name} {label} offline — {n} devices affected")
                    offline_group_ids.add(group.id)

        for device in config.devices:
            if device.group_id in offline_group_ids:
                continue  # access point explains this; don't double-report
            r = self.device_results.get(device.ip)
            if r and r.status == ProbeStatus.UNREACHABLE:
                issues.append(f"{device.name} unreachable")
        return issues

    def summary(self, config: NetworkConfig) -> tuple[int, int, int]:
        probed_gw = {g.gateway_ip for g in config.groups if g.gateway_ip}
        total = len(probed_gw) + len(config.devices)
        ok = bad = 0
        for ip in probed_gw:
            r = self.gateway_results.get(ip)
            if r:
                if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED):
                    ok += 1
                elif r.status == ProbeStatus.UNREACHABLE:
                    bad += 1
        for d in config.devices:
            r = self.device_results.get(d.ip)
            if r:
                if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED):
                    ok += 1
                elif r.status == ProbeStatus.UNREACHABLE:
                    bad += 1
        return total, ok, bad
