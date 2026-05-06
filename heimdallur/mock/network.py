from __future__ import annotations
import asyncio
import random
import time
import tomllib
from pathlib import Path
from heimdallur.core.topology import (
    NetworkConfig, NetworkState, ProbeResult, ProbeStatus,
    Group, RouterStats, GatewayEnrichment, SpeedResult,
)

_SCENARIO_PATH = Path(__file__).parent / "scenario.toml"

_GW_BASES: dict[str, dict] = {
    "192.168.1.95": {"dbm": -52, "clients": 3},
    "192.168.1.44": {"dbm": -44, "clients": 8},
    "192.168.1.43": {"dbm": -47, "clients": 5},
    "192.168.1.45": {"dbm": -58, "clients": 9},
}


class MockNetwork:
    def __init__(self, scenario_path: Path | None = None):
        path = scenario_path or _SCENARIO_PATH
        if path.exists():
            with open(path, "rb") as f:
                data = tomllib.load(f)
            self._failures: dict[str, str] = data.get("failures", {})
        else:
            self._failures = {}
        self._intermittent: dict[str, bool] = {}
        self._start_time = time.time()

    def _mode(self, ip: str, alias: str | None = None) -> str | None:
        return self._failures.get(ip) or (self._failures.get(alias) if alias else None)

    async def probe_ip(self, ip: str, alias: str | None = None) -> ProbeResult:
        await asyncio.sleep(random.uniform(0.001, 0.004))
        mode = self._mode(ip, alias)
        if mode == "down":
            return ProbeResult(ip=ip, status=ProbeStatus.UNREACHABLE, response_ms=None)
        if mode == "intermittent":
            state = self._intermittent.get(ip, True)
            if random.random() < 0.35:
                state = not state
            self._intermittent[ip] = state
            if not state:
                return ProbeResult(ip=ip, status=ProbeStatus.UNREACHABLE, response_ms=None)
            return ProbeResult(ip=ip, status=ProbeStatus.HEALTHY, response_ms=random.uniform(1.0, 6.0))
        if mode == "slow":
            ms = random.uniform(75.0, 180.0)
            return ProbeResult(ip=ip, status=ProbeStatus.DEGRADED if ms < 100 else ProbeStatus.UNREACHABLE, response_ms=ms)
        ms = (
            random.uniform(18.0, 55.0) if alias in ("ont",)
            else random.uniform(0.5, 3.0) if alias == "router"
            else random.uniform(0.8, 5.0)
        )
        return ProbeResult(ip=ip, status=ProbeStatus.HEALTHY, response_ms=ms)

    def mock_router_stats(self) -> RouterStats:
        return RouterStats(
            cpu_pct=random.uniform(4.0, 22.0),
            memory_pct=random.uniform(28.0, 52.0),
            uptime_seconds=time.time() - self._start_time + 3600 * 72,
        )

    def mock_gateway_enrichment(self, group: Group) -> GatewayEnrichment:
        if group.type == "wifi" and group.gateway_ip:
            base = _GW_BASES.get(group.gateway_ip, {"dbm": -65, "clients": 3})
            return GatewayEnrichment(
                gateway_ip=group.gateway_ip,
                signal_dbm=base["dbm"] + random.randint(-3, 3),
                client_count=max(0, base["clients"] + random.randint(-1, 2)),
            )
        return GatewayEnrichment(gateway_ip=group.gateway_ip, signal_dbm=None, client_count=None)

    def mock_speed_result(self) -> SpeedResult:
        return SpeedResult(
            timestamp=time.time(),
            download_mbps=random.uniform(180.0, 480.0),
            ping_ms=random.uniform(8.0, 35.0),
            ok=True,
        )


class MockProber:
    def __init__(self, config: NetworkConfig, scenario_path: Path | None = None):
        self._config = config
        self._net = MockNetwork(scenario_path)

    def mock_router_stats(self) -> RouterStats:
        return self._net.mock_router_stats()

    def mock_gateway_enrichment(self, group: Group) -> GatewayEnrichment:
        return self._net.mock_gateway_enrichment(group)

    def mock_speed_result(self) -> SpeedResult:
        return self._net.mock_speed_result()

    async def probe_all(self) -> NetworkState:
        ts = time.time()
        ont, router = await asyncio.gather(
            self._net.probe_ip(self._config.ont_check_host, alias="ont"),
            self._net.probe_ip(self._config.router_ip, alias="router"),
        )

        gateway_results: dict[str, ProbeResult] = {}
        device_results: dict[str, ProbeResult] = {}

        if router.status == ProbeStatus.UNREACHABLE:
            for g in self._config.groups:
                if g.gateway_ip:
                    gateway_results[g.gateway_ip] = ProbeResult(
                        ip=g.gateway_ip, status=ProbeStatus.UNKNOWN, response_ms=None, cause="router_offline"
                    )
            for d in self._config.devices:
                device_results[d.ip] = ProbeResult(
                    ip=d.ip, status=ProbeStatus.UNKNOWN, response_ms=None, cause="router_offline"
                )
        else:
            gw_ips = list({g.gateway_ip for g in self._config.groups if g.gateway_ip})
            gw_res = await asyncio.gather(*[self._net.probe_ip(ip) for ip in gw_ips])
            gateway_results = dict(zip(gw_ips, gw_res))

            grp_up: dict[str, bool] = {}
            for g in self._config.groups:
                if g.gateway_ip:
                    r = gateway_results.get(g.gateway_ip)
                    grp_up[g.id] = r is None or r.status != ProbeStatus.UNREACHABLE
                else:
                    grp_up[g.id] = True

            pending: list[tuple[str, asyncio.Task]] = []
            for d in self._config.devices:
                if not grp_up.get(d.group_id, True):
                    device_results[d.ip] = ProbeResult(
                        ip=d.ip, status=ProbeStatus.UNKNOWN, response_ms=None, cause="gateway_offline"
                    )
                else:
                    pending.append((d.ip, asyncio.create_task(self._net.probe_ip(d.ip))))

            if pending:
                res = await asyncio.gather(*[t for _, t in pending])
                for (ip, _), r in zip(pending, res):
                    device_results[ip] = r

        return NetworkState(
            timestamp=ts,
            ont_result=ont,
            router_result=router,
            gateway_results=gateway_results,
            device_results=device_results,
        )
