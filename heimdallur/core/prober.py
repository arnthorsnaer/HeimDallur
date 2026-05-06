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

        gateway_results: dict[str, ProbeResult] = {}
        device_results: dict[str, ProbeResult] = {}

        if router.status == ProbeStatus.UNREACHABLE:
            for g in self._config.groups:
                if g.gateway_ip:
                    gateway_results[g.gateway_ip] = ProbeResult(
                        ip=g.gateway_ip, status=ProbeStatus.UNKNOWN,
                        response_ms=None, cause="router_offline",
                    )
            for d in self._config.devices:
                device_results[d.ip] = ProbeResult(
                    ip=d.ip, status=ProbeStatus.UNKNOWN,
                    response_ms=None, cause="router_offline",
                )
        else:
            # Probe unique gateway IPs concurrently
            gw_ips = list({g.gateway_ip for g in self._config.groups if g.gateway_ip})
            gw_results = await asyncio.gather(*[probe_ip(ip) for ip in gw_ips])
            gateway_results = dict(zip(gw_ips, gw_results))

            # Map group_id → gateway accessible?
            grp_up: dict[str, bool] = {}
            for g in self._config.groups:
                if g.gateway_ip:
                    r = gateway_results.get(g.gateway_ip)
                    grp_up[g.id] = r is None or r.status != ProbeStatus.UNREACHABLE
                else:
                    grp_up[g.id] = True  # unprobed gateway → always up (cascades from router only)

            # Probe devices, skip those whose group gateway is down
            pending: list[tuple[str, asyncio.Task]] = []
            for d in self._config.devices:
                if not grp_up.get(d.group_id, True):
                    device_results[d.ip] = ProbeResult(
                        ip=d.ip, status=ProbeStatus.UNKNOWN,
                        response_ms=None, cause="gateway_offline",
                    )
                else:
                    pending.append((d.ip, asyncio.create_task(probe_ip(d.ip))))

            if pending:
                probe_res = await asyncio.gather(*[t for _, t in pending])
                for (ip, _), r in zip(pending, probe_res):
                    device_results[ip] = r

        return NetworkState(
            timestamp=ts,
            ont_result=ont,
            router_result=router,
            gateway_results=gateway_results,
            device_results=device_results,
        )
