from __future__ import annotations
import asyncio
import sys
import time
from heimdallur.core.topology import (
    NetworkConfig, NetworkState, ProbeResult, ProbeStatus,
)

_HEALTHY_MS  = 10
_DEGRADED_MS = 100


async def _ping(ip: str, timeout: float = 2.0) -> tuple[bool, float | None]:
    cmd = (
        ["ping", "-c", "1", "-W", "2000", ip]
        if sys.platform == "darwin"
        else ["ping", "-c", "1", "-W", "2", ip]
    )
    start = time.monotonic()
    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await asyncio.wait_for(proc.wait(), timeout=timeout + 0.5)
        elapsed = (time.monotonic() - start) * 1000
        return proc.returncode == 0, elapsed if proc.returncode == 0 else None
    except (asyncio.TimeoutError, OSError):
        if proc:
            try: proc.kill()
            except ProcessLookupError: pass
        return False, None


def _classify(ms: float | None) -> ProbeStatus:
    if ms is None: return ProbeStatus.UNREACHABLE
    if ms < _HEALTHY_MS: return ProbeStatus.HEALTHY
    if ms < _DEGRADED_MS: return ProbeStatus.DEGRADED
    return ProbeStatus.UNREACHABLE


async def probe_ip(ip: str) -> ProbeResult:
    ok, ms = await _ping(ip)
    return ProbeResult(ip=ip, status=_classify(ms if ok else None), response_ms=ms if ok else None)


class Prober:
    def __init__(self, config: NetworkConfig):
        self._config = config

    async def probe_all(self) -> NetworkState:
        ts = time.time()
        ont, router = await asyncio.gather(
            probe_ip(self._config.ont_check_host),
            probe_ip(self._config.router_ip),
        )

        # Probe all gateways and devices in parallel — no cascade suppression.
        # Every device is probed every cycle regardless of its group's gateway status.
        gw_ips = list({g.gateway_ip for g in self._config.groups if g.gateway_ip})
        all_tasks = [probe_ip(ip) for ip in gw_ips] + [probe_ip(d.ip) for d in self._config.devices]

        if all_tasks:
            all_results = await asyncio.gather(*all_tasks)
            gateway_results = dict(zip(gw_ips, all_results[:len(gw_ips)]))
            device_results  = {d.ip: r for d, r in zip(self._config.devices, all_results[len(gw_ips):])}
        else:
            gateway_results = {}
            device_results  = {}

        return NetworkState(
            timestamp=ts,
            ont_result=ont,
            router_result=router,
            gateway_results=gateway_results,
            device_results=device_results,
        )
