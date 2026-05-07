from __future__ import annotations
import asyncio
import os
import time
from collections import defaultdict, deque
from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.message import Message
from textual import work

from heimdallur.config.loader import load_config
from heimdallur.core.store import Store
from heimdallur.core.topology import (
    NetworkConfig, NetworkState, Group,
    RouterStats, GatewayEnrichment, SpeedResult, InternetQuality,
)

_HIST = 40


@dataclass
class EnrichedState:
    network: NetworkState
    router_stats: RouterStats | None
    gw_enrichment: dict[str, GatewayEnrichment]   # gateway_ip -> enrichment
    speed_result: SpeedResult | None
    internet_quality: InternetQuality | None


@dataclass
class HistorySnapshot:
    ont_lat:  list[float]
    ont_loss: list[float]
    rtr_cpu:  list[float]
    rtr_mem:  list[float]
    gw_lat:   dict[str, list[float]]   # gateway_ip -> latency history
    gw_loss:  dict[str, list[float]]
    dl_hist:  list[float]
    # Per-target internet quality histories
    inet_ip_lat:     dict[str, list[float]]   # target IP -> rtt history
    inet_ip_loss:    dict[str, list[float]]   # target IP -> loss flags (0/1)
    inet_dns_lat:    dict[str, list[float]]   # hostname  -> lookup time history
    inet_dns_loss:   dict[str, list[float]]   # hostname  -> failure flags (0/1)
    inet_http_ttfb:  dict[str, list[float]]   # url       -> TTFB history
    inet_http_total: dict[str, list[float]]   # url       -> total time history
    inet_http_loss:  dict[str, list[float]]   # url       -> failure flags (0/1)


class ProbeComplete(Message):
    def __init__(self, enriched: EnrichedState, snapshot: HistorySnapshot) -> None:
        super().__init__()
        self.enriched = enriched
        self.snapshot = snapshot


class HeimdallurApp(App):
    CSS = """Screen { background: #0d1117; }"""

    def __init__(self) -> None:
        super().__init__()
        self._config: NetworkConfig = load_config()
        from pathlib import Path as _Path
        _db = os.getenv("NETWATCH_SCREENSHOT_DB")
        self._store = Store(_Path(_db)) if _db else Store()
        self._start_time = time.time()

        if os.getenv("NETWATCH_MOCK"):
            from heimdallur.mock.network import MockProber
            from pathlib import Path as _Path
            _scenario = os.getenv("NETWATCH_MOCK_SCENARIO")
            self._prober = MockProber(
                self._config,
                scenario_path=_Path(_scenario) if _scenario else None,
            )
        else:
            from heimdallur.core.prober import Prober
            self._prober = Prober(self._config)

        from heimdallur.core.internet_probe import InternetProber
        self._inet_prober = InternetProber()

        # Rolling history — init loss with zeros so sparkline starts green not red
        self._lat:  dict[str, deque] = defaultdict(lambda: deque(maxlen=_HIST))
        self._loss: dict[str, deque] = defaultdict(lambda: deque([0.0, 0.0], maxlen=_HIST))
        self._cpu:  deque = deque([0.0, 0.0], maxlen=_HIST)
        self._mem:  deque = deque([0.0, 0.0], maxlen=_HIST)
        self._dl:   deque = deque(maxlen=_HIST)
        # Internet quality per-target rolling history
        self._inet_ip_lat:     dict[str, deque] = defaultdict(lambda: deque(maxlen=_HIST))
        self._inet_ip_loss:    dict[str, deque] = defaultdict(lambda: deque([0.0, 0.0], maxlen=_HIST))
        self._inet_dns_lat:    dict[str, deque] = defaultdict(lambda: deque(maxlen=_HIST))
        self._inet_dns_loss:   dict[str, deque] = defaultdict(lambda: deque([0.0, 0.0], maxlen=_HIST))
        self._inet_http_ttfb:  dict[str, deque] = defaultdict(lambda: deque(maxlen=_HIST))
        self._inet_http_total: dict[str, deque] = defaultdict(lambda: deque(maxlen=_HIST))
        self._inet_http_loss:  dict[str, deque] = defaultdict(lambda: deque([0.0, 0.0], maxlen=_HIST))
        self._speed_result: SpeedResult | None = None
        self._last_enriched: EnrichedState | None = None

    def compose(self) -> ComposeResult:
        return iter([])

    async def on_mount(self) -> None:
        from heimdallur.tui.status_view import StatusScreen
        from heimdallur.mock.network import MockProber
        await self._store.open()
        await self.push_screen(StatusScreen(self._config, self._start_time))
        if isinstance(self._prober, MockProber):
            self._seed_mock_history()
        self._probe_loop()
        self._speed_loop()

    def _seed_mock_history(self) -> None:
        import random
        from heimdallur.core.internet_probe import IP_TARGETS, DNS_TARGETS, HTTP_TARGETS

        def _walk(start: float, lo: float, hi: float, step: float) -> list[float]:
            v, out = start, []
            for _ in range(_HIST):
                v = max(lo, min(hi, v + random.uniform(-step, step)))
                out.append(v)
            return out

        ont_ip = self._config.ont_check_host
        rtr_ip = self._config.router_ip

        for v in _walk(28.0, 12.0, 65.0, 7.0):
            self._lat[ont_ip].append(v)
            self._loss[ont_ip].append(0.0)
        for v in _walk(1.5, 0.4, 5.0, 0.6):
            self._lat[rtr_ip].append(v)
            self._loss[rtr_ip].append(0.0)
        for v in _walk(12.0, 3.0, 32.0, 4.0):
            self._cpu.append(v)
        for v in _walk(38.0, 24.0, 58.0, 3.0):
            self._mem.append(v)

        # Seed a realistic speed result so screenshots show real data immediately
        for v in _walk(310.0, 180.0, 480.0, 40.0):
            self._dl.append(v)
        self._speed_result = SpeedResult(
            timestamp=time.time() - random.uniform(60.0, 240.0),
            download_mbps=_walk(310.0, 280.0, 380.0, 20.0)[-1],
            ping_ms=_walk(14.0, 8.0, 35.0, 4.0)[-1],
            ok=True,
        )

        bases_ip = {"1.1.1.1": (12.0, 28.0, 4.0), "8.8.8.8": (15.0, 35.0, 5.0), "9.9.9.9": (11.0, 26.0, 4.0)}
        for target, _ in IP_TARGETS:
            lo, hi, step = bases_ip.get(target, (18.0, 45.0, 6.0))
            for v in _walk((lo + hi) / 2, lo, hi, step):
                self._inet_ip_lat[target].append(v)
                self._inet_ip_loss[target].append(0.0)
        for hostname, _ in DNS_TARGETS:
            for v in _walk(8.0, 2.0, 20.0, 3.0):
                self._inet_dns_lat[hostname].append(v)
                self._inet_dns_loss[hostname].append(0.0)
        for url, _, _, _ in HTTP_TARGETS:
            for v in _walk(45.0, 20.0, 90.0, 10.0):
                self._inet_http_ttfb[url].append(v)
                self._inet_http_total[url].append(v + random.uniform(5.0, 20.0))
                self._inet_http_loss[url].append(0.0)

    async def on_unmount(self) -> None:
        await self._store.close()

    def _accumulate(self, state: NetworkState, enriched: EnrichedState) -> HistorySnapshot:
        def _upd(ip: str, r) -> None:
            if r is None:
                return
            if r.response_ms is not None:
                self._lat[ip].append(r.response_ms)
                self._loss[ip].append(0.0)
            else:
                self._loss[ip].append(1.0)

        if state.ont_result:
            _upd(state.ont_result.ip, state.ont_result)
        if state.router_result:
            _upd(state.router_result.ip, state.router_result)
        for ip, r in state.gateway_results.items():
            _upd(ip, r)

        if enriched.router_stats:
            self._cpu.append(enriched.router_stats.cpu_pct)
            self._mem.append(enriched.router_stats.memory_pct)
        if enriched.speed_result and enriched.speed_result.ok:
            self._dl.append(enriched.speed_result.download_mbps)

        if enriched.internet_quality:
            iq = enriched.internet_quality
            for r in iq.raw_ip:
                if r.rtt_ms is not None:
                    self._inet_ip_lat[r.target].append(r.rtt_ms)
                    self._inet_ip_loss[r.target].append(0.0)
                else:
                    self._inet_ip_loss[r.target].append(1.0)
            for r in iq.dns:
                if r.success and r.lookup_ms is not None:
                    self._inet_dns_lat[r.hostname].append(r.lookup_ms)
                    self._inet_dns_loss[r.hostname].append(0.0)
                else:
                    self._inet_dns_loss[r.hostname].append(1.0)
            for r in iq.http:
                if r.success and r.ttfb_ms is not None:
                    self._inet_http_ttfb[r.url].append(r.ttfb_ms)
                    self._inet_http_loss[r.url].append(0.0)
                else:
                    self._inet_http_loss[r.url].append(1.0)
                if r.total_ms is not None:
                    self._inet_http_total[r.url].append(r.total_ms)

        ont_ip = state.ont_result.ip if state.ont_result else self._config.ont_check_host
        gw_ips = [g.gateway_ip for g in self._config.groups if g.gateway_ip]

        from heimdallur.core.internet_probe import IP_TARGETS, DNS_TARGETS, HTTP_TARGETS
        return HistorySnapshot(
            ont_lat=list(self._lat.get(ont_ip, [])),
            ont_loss=list(self._loss.get(ont_ip, [])),
            rtr_cpu=list(self._cpu),
            rtr_mem=list(self._mem),
            gw_lat={ip: list(self._lat.get(ip, [])) for ip in gw_ips},
            gw_loss={ip: list(self._loss.get(ip, [])) for ip in gw_ips},
            dl_hist=list(self._dl),
            inet_ip_lat={t: list(self._inet_ip_lat.get(t, [])) for t, _ in IP_TARGETS},
            inet_ip_loss={t: list(self._inet_ip_loss.get(t, [])) for t, _ in IP_TARGETS},
            inet_dns_lat={h: list(self._inet_dns_lat.get(h, [])) for h, _ in DNS_TARGETS},
            inet_dns_loss={h: list(self._inet_dns_loss.get(h, [])) for h, _ in DNS_TARGETS},
            inet_http_ttfb={u: list(self._inet_http_ttfb.get(u, [])) for u, _, _, _ in HTTP_TARGETS},
            inet_http_total={u: list(self._inet_http_total.get(u, [])) for u, _, _, _ in HTTP_TARGETS},
            inet_http_loss={u: list(self._inet_http_loss.get(u, [])) for u, _, _, _ in HTTP_TARGETS},
        )

    @work(exclusive=True, group="probe")
    async def _probe_loop(self) -> None:
        while True:
            from heimdallur.mock.network import MockProber

            if isinstance(self._prober, MockProber):
                state = await self._prober.probe_all()
                iq = self._prober.mock_internet_quality()
            else:
                state, iq = await asyncio.gather(
                    self._prober.probe_all(),
                    self._inet_prober.probe_all(),
                )

            await self._store.record_state(state, self._config)

            router_stats: RouterStats | None = None
            gw_enrichment: dict[str, GatewayEnrichment] = {}

            if isinstance(self._prober, MockProber):
                router_stats = self._prober.mock_router_stats()
                for g in self._config.groups:
                    enr = self._prober.mock_gateway_enrichment(g)
                    if g.gateway_ip:
                        gw_enrichment[g.gateway_ip] = enr

            enriched = EnrichedState(
                network=state,
                router_stats=router_stats,
                gw_enrichment=gw_enrichment,
                speed_result=self._speed_result,
                internet_quality=iq,
            )
            snapshot = self._accumulate(state, enriched)
            self.post_message(ProbeComplete(enriched, snapshot))
            await asyncio.sleep(self._config.probe_interval_seconds)

    @work(exclusive=True, group="speedtest")
    async def _speed_loop(self) -> None:
        await asyncio.sleep(3)
        while True:
            from heimdallur.mock.network import MockProber
            if isinstance(self._prober, MockProber):
                result = self._prober.mock_speed_result()
            else:
                from heimdallur.core.speed import run_speed_test
                result = await run_speed_test()
            self._speed_result = result
            await self._store.record_speed_test(result)
            await asyncio.sleep(self._config.speed_test_interval_seconds)

    def on_probe_complete(self, message: ProbeComplete) -> None:
        from heimdallur.tui.status_view import StatusScreen
        from heimdallur.tui.devices_view import DevicesScreen
        self._last_enriched = message.enriched
        if isinstance(self.screen, StatusScreen):
            self.screen.update_state(message.enriched, message.snapshot)
        elif isinstance(self.screen, DevicesScreen):
            self.screen.update_state(message.enriched.network, message.enriched.gw_enrichment)
