from __future__ import annotations
import asyncio
import random
import time
import tomllib
from pathlib import Path
from heimdallur.core.topology import (
    NetworkConfig, NetworkState, ProbeResult, ProbeStatus,
    Group, RouterStats, GatewayEnrichment, SpeedResult,
    InternetQuality, RawIpResult, DnsResult, HttpResult,
)
from heimdallur.core.internet_probe import IP_TARGETS, DNS_TARGETS, HTTP_TARGETS

_SCENARIO_PATH = Path(__file__).parent / "scenario.toml"

_GW_BASES: dict[str, dict] = {
    "192.0.2.25": {"clients": 3},
    "192.0.2.21": {"clients": 8},
    "192.0.2.22": {"clients": 5},
    "192.0.2.23": {"clients": 9},
}


class MockNetwork:
    def __init__(self, scenario_path: Path | None = None):
        path = scenario_path or _SCENARIO_PATH
        if path.exists():
            with open(path, "rb") as f:
                data = tomllib.load(f)
            self._failures: dict[str, str] = data.get("failures", {})
            # [inet] section: per-target overrides for internet quality probes.
            # Keys: IP address, hostname, or "<label>_http" for HTTP targets.
            self._inet_failures: dict[str, str] = data.get("inet", {})
        else:
            self._failures = {}
            self._inet_failures = {}
        self._intermittent: dict[str, bool] = {}
        self._start_time = time.time()

    def _mode(self, ip: str, alias: str | None = None) -> str | None:
        return self._failures.get(ip) or (self._failures.get(alias) if alias else None)

    def _inet_mode(self, key: str) -> str | None:
        """Per-target [inet] override, falling back to global ont mode."""
        return self._inet_failures.get(key) or self._failures.get("ont")

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
            base = _GW_BASES.get(group.gateway_ip, {"clients": 3})
            return GatewayEnrichment(
                gateway_ip=group.gateway_ip,
                client_count=max(0, base["clients"] + random.randint(-1, 2)),
            )
        return GatewayEnrichment(gateway_ip=group.gateway_ip, client_count=None)

    def mock_speed_result(self) -> SpeedResult:
        return SpeedResult(
            timestamp=time.time(),
            download_mbps=random.uniform(180.0, 480.0),
            ping_ms=random.uniform(8.0, 35.0),
            ok=True,
        )

    def mock_internet_quality(self) -> InternetQuality:
        ts = time.time()

        def _raw_ip(target: str, label: str) -> RawIpResult:
            mode = self._inet_mode(target)
            if mode == "down":
                return RawIpResult(target=target, label=label,
                                   status=ProbeStatus.UNREACHABLE, rtt_ms=None)
            if mode == "slow":
                ms = random.uniform(90.0, 200.0)
                return RawIpResult(target=target, label=label,
                                   status=ProbeStatus.DEGRADED if ms < 100 else ProbeStatus.UNREACHABLE,
                                   rtt_ms=ms)
            if mode == "intermittent" and random.random() < 0.35:
                return RawIpResult(target=target, label=label,
                                   status=ProbeStatus.UNREACHABLE, rtt_ms=None)
            bases = {"1.1.1.1": (12.0, 28.0), "8.8.8.8": (15.0, 35.0), "9.9.9.9": (11.0, 26.0)}
            lo, hi = bases.get(target, (18.0, 45.0))
            ms = random.uniform(lo, hi)
            return RawIpResult(target=target, label=label,
                               status=ProbeStatus.HEALTHY, rtt_ms=ms)

        _DNS_IPS = {
            "cloudflare.com": "104.16.133.229",
            "google.com":     "142.251.1.100",
            "quad9.net":      "9.9.9.9",
        }

        def _dns(hostname: str, label: str) -> DnsResult:
            mode = self._inet_mode(hostname)
            if mode == "down":
                return DnsResult(hostname=hostname, label=label,
                                 success=False, lookup_ms=None, resolved_ip=None)
            if mode == "slow":
                ms = random.uniform(60.0, 140.0)
                return DnsResult(hostname=hostname, label=label,
                                 success=True, lookup_ms=ms,
                                 resolved_ip=_DNS_IPS.get(hostname, "1.2.3.4"))
            if mode == "intermittent" and random.random() < 0.25:
                return DnsResult(hostname=hostname, label=label,
                                 success=False, lookup_ms=None, resolved_ip=None)
            ms = random.uniform(2.0, 18.0)
            return DnsResult(hostname=hostname, label=label,
                             success=True, lookup_ms=ms,
                             resolved_ip=_DNS_IPS.get(hostname, "1.2.3.4"))

        def _http(url: str, label: str, short_path: str, expected: int) -> HttpResult:
            # HTTP targets keyed by "<label>_http" (lowercase), e.g. "microsoft_http"
            http_key = label.lower().replace(" ", "_") + "_http"
            mode = self._inet_mode(http_key)
            if mode == "down":
                return HttpResult(url=url, label=label, short_path=short_path,
                                  success=False, status_code=None,
                                  tcp_ms=None, tls_ms=None, ttfb_ms=None, total_ms=None)
            if mode == "slow":
                tcp  = random.uniform(80.0, 160.0)
                tls  = random.uniform(60.0, 120.0)
                ttfb = tcp + tls + random.uniform(50.0, 150.0)
                total = ttfb + random.uniform(20.0, 80.0)
                return HttpResult(url=url, label=label, short_path=short_path,
                                  success=True, status_code=expected,
                                  tcp_ms=tcp, tls_ms=tls, ttfb_ms=ttfb, total_ms=total)
            if mode == "intermittent" and random.random() < 0.20:
                return HttpResult(url=url, label=label, short_path=short_path,
                                  success=False, status_code=None,
                                  tcp_ms=None, tls_ms=None, ttfb_ms=None, total_ms=None)
            tcp  = random.uniform(8.0, 22.0)
            tls  = random.uniform(12.0, 30.0)
            ttfb = tcp + tls + random.uniform(10.0, 40.0)
            total = ttfb + random.uniform(5.0, 25.0)
            return HttpResult(url=url, label=label, short_path=short_path,
                              success=True, status_code=expected,
                              tcp_ms=tcp, tls_ms=tls, ttfb_ms=ttfb, total_ms=total)

        return InternetQuality(
            timestamp=ts,
            raw_ip=[_raw_ip(t, l)        for t, l       in IP_TARGETS],
            dns=   [_dns(h, l)           for h, l       in DNS_TARGETS],
            http=  [_http(u, l, p, s)    for u, l, p, s in HTTP_TARGETS],
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

    def mock_internet_quality(self) -> InternetQuality:
        return self._net.mock_internet_quality()

    async def probe_all(self) -> NetworkState:
        ts = time.time()
        ont, router = await asyncio.gather(
            self._net.probe_ip(self._config.ont_check_host, alias="ont"),
            self._net.probe_ip(self._config.router_ip, alias="router"),
        )

        gateway_results: dict[str, ProbeResult] = {}
        device_results: dict[str, ProbeResult] = {}

        # Probe all gateways and devices in parallel — no cascade suppression.
        gw_ips = list({g.gateway_ip for g in self._config.groups if g.gateway_ip})
        all_tasks = [self._net.probe_ip(ip) for ip in gw_ips] + \
                    [self._net.probe_ip(d.ip) for d in self._config.devices]

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
