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
    RouterStats, GatewayEnrichment, SpeedResult,
)

_HIST = 40


@dataclass
class EnrichedState:
    network: NetworkState
    router_stats: RouterStats | None
    gw_enrichment: dict[str, GatewayEnrichment]   # gateway_ip -> enrichment
    speed_result: SpeedResult | None


@dataclass
class HistorySnapshot:
    ont_lat:  list[float]
    ont_loss: list[float]
    rtr_cpu:  list[float]
    rtr_mem:  list[float]
    gw_lat:   dict[str, list[float]]   # gateway_ip -> latency history
    gw_loss:  dict[str, list[float]]
    dl_hist:  list[float]


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

        # Rolling history — init loss with zeros so sparkline starts green not red
        self._lat:  dict[str, deque] = defaultdict(lambda: deque(maxlen=_HIST))
        self._loss: dict[str, deque] = defaultdict(lambda: deque([0.0, 0.0], maxlen=_HIST))
        self._cpu:  deque = deque([0.0, 0.0], maxlen=_HIST)
        self._mem:  deque = deque([0.0, 0.0], maxlen=_HIST)
        self._dl:   deque = deque(maxlen=_HIST)
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

        ont_ip = state.ont_result.ip if state.ont_result else self._config.ont_check_host
        gw_ips = [g.gateway_ip for g in self._config.groups if g.gateway_ip]
        return HistorySnapshot(
            ont_lat=list(self._lat.get(ont_ip, [])),
            ont_loss=list(self._loss.get(ont_ip, [])),
            rtr_cpu=list(self._cpu),
            rtr_mem=list(self._mem),
            gw_lat={ip: list(self._lat.get(ip, [])) for ip in gw_ips},
            gw_loss={ip: list(self._loss.get(ip, [])) for ip in gw_ips},
            dl_hist=list(self._dl),
        )

    @work(exclusive=True, group="probe")
    async def _probe_loop(self) -> None:
        while True:
            state = await self._prober.probe_all()
            await self._store.record_state(state, self._config)

            router_stats: RouterStats | None = None
            gw_enrichment: dict[str, GatewayEnrichment] = {}

            from heimdallur.mock.network import MockProber
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
