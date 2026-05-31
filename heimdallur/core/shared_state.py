from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from heimdallur.core.topology import (
    DnsResult,
    GatewayEnrichment,
    HttpResult,
    InternetQuality,
    NetworkState,
    ProbeResult,
    ProbeStatus,
    RawIpResult,
    RouterStats,
    SpeedResult,
)
from heimdallur.tui.app import EnrichedState, HistorySnapshot


def state_path() -> Path:
    if path := os.getenv("HEIMDALLUR_STATE_FILE"):
        return Path(path).expanduser()
    return Path.home() / ".local" / "share" / "heimdallur" / "live-state.json"


def _probe_result_to_dict(result: ProbeResult | None) -> dict[str, Any] | None:
    if result is None:
        return None
    data = asdict(result)
    data["status"] = result.status.value
    return data


def _probe_result_from_dict(data: dict[str, Any] | None) -> ProbeResult | None:
    if data is None:
        return None
    return ProbeResult(
        ip=data["ip"],
        status=ProbeStatus(data["status"]),
        response_ms=data.get("response_ms"),
        timestamp=data.get("timestamp", 0.0),
        cause=data.get("cause"),
    )


def _network_state_to_dict(state: NetworkState) -> dict[str, Any]:
    return {
        "timestamp": state.timestamp,
        "ont_result": _probe_result_to_dict(state.ont_result),
        "router_result": _probe_result_to_dict(state.router_result),
        "gateway_results": {ip: _probe_result_to_dict(r) for ip, r in state.gateway_results.items()},
        "device_results": {ip: _probe_result_to_dict(r) for ip, r in state.device_results.items()},
    }


def _network_state_from_dict(data: dict[str, Any]) -> NetworkState:
    return NetworkState(
        timestamp=data["timestamp"],
        ont_result=_probe_result_from_dict(data.get("ont_result")),
        router_result=_probe_result_from_dict(data.get("router_result")),
        gateway_results={ip: r for ip, value in data.get("gateway_results", {}).items() if (r := _probe_result_from_dict(value))},
        device_results={ip: r for ip, value in data.get("device_results", {}).items() if (r := _probe_result_from_dict(value))},
    )


def _internet_quality_to_dict(iq: InternetQuality | None) -> dict[str, Any] | None:
    if iq is None:
        return None
    return {
        "timestamp": iq.timestamp,
        "raw_ip": [dict(asdict(r), status=r.status.value) for r in iq.raw_ip],
        "dns": [asdict(r) for r in iq.dns],
        "http": [asdict(r) for r in iq.http],
    }


def _internet_quality_from_dict(data: dict[str, Any] | None) -> InternetQuality | None:
    if data is None:
        return None
    return InternetQuality(
        timestamp=data["timestamp"],
        raw_ip=[RawIpResult(status=ProbeStatus(item["status"]), **{k: v for k, v in item.items() if k != "status"}) for item in data.get("raw_ip", [])],
        dns=[DnsResult(**item) for item in data.get("dns", [])],
        http=[HttpResult(**item) for item in data.get("http", [])],
    )


def write_live_state(enriched: EnrichedState, snapshot: HistorySnapshot, path: Path | None = None) -> None:
    target = path or state_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "enriched": {
            "network": _network_state_to_dict(enriched.network),
            "router_stats": asdict(enriched.router_stats) if enriched.router_stats else None,
            "gw_enrichment": {ip: asdict(enr) for ip, enr in enriched.gw_enrichment.items()},
            "speed_result": asdict(enriched.speed_result) if enriched.speed_result else None,
            "internet_quality": _internet_quality_to_dict(enriched.internet_quality),
            "doctor_checks": enriched.doctor_checks,
        },
        "snapshot": asdict(snapshot),
    }
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(fd, "w") as tmp:
            json.dump(payload, tmp)
        os.replace(tmp_name, target)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def read_live_state(path: Path | None = None) -> tuple[EnrichedState, HistorySnapshot]:
    target = path or state_path()
    with target.open() as f:
        payload = json.load(f)
    enriched_data = payload["enriched"]
    enriched = EnrichedState(
        network=_network_state_from_dict(enriched_data["network"]),
        router_stats=RouterStats(**enriched_data["router_stats"]) if enriched_data.get("router_stats") else None,
        gw_enrichment={ip: GatewayEnrichment(**value) for ip, value in enriched_data.get("gw_enrichment", {}).items()},
        speed_result=SpeedResult(**enriched_data["speed_result"]) if enriched_data.get("speed_result") else None,
        internet_quality=_internet_quality_from_dict(enriched_data.get("internet_quality")),
        doctor_checks=enriched_data.get("doctor_checks", []),
    )
    snapshot = HistorySnapshot(**payload["snapshot"])
    return enriched, snapshot
