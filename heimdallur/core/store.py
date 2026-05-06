from __future__ import annotations
import time
from pathlib import Path
import aiosqlite
from heimdallur.core.topology import NetworkConfig, NetworkState, SpeedResult

_DEFAULT_DB = Path.home() / ".local" / "share" / "heimdallur" / "events.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS probe_events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   REAL    NOT NULL,
    target_ip   TEXT    NOT NULL,
    target_name TEXT,
    status      TEXT    NOT NULL,
    response_ms REAL,
    cause       TEXT
);
CREATE TABLE IF NOT EXISTS speed_tests (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp     REAL NOT NULL,
    download_mbps REAL,
    ping_ms       REAL,
    ok            INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_probe_ts  ON probe_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_probe_ip  ON probe_events(target_ip, timestamp);
CREATE INDEX IF NOT EXISTS idx_speed_ts  ON speed_tests(timestamp);
"""


class Store:
    def __init__(self, db_path: Path = _DEFAULT_DB):
        self._path = db_path
        self._db: aiosqlite.Connection | None = None

    async def open(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._db = await aiosqlite.connect(self._path)
        await self._db.executescript(_SCHEMA)
        await self._db.commit()

    async def close(self) -> None:
        if self._db:
            await self._db.close()

    async def record_state(self, state: NetworkState, config: NetworkConfig) -> None:
        assert self._db
        rows: list[tuple] = []
        ts = state.timestamp
        if state.ont_result:
            r = state.ont_result
            rows.append((ts, r.ip, "Internet", r.status.value, r.response_ms, r.cause))
        if state.router_result:
            r = state.router_result
            rows.append((ts, r.ip, "Router", r.status.value, r.response_ms, r.cause))
        for group in config.groups:
            if group.gateway_ip:
                r = state.gateway_results.get(group.gateway_ip)
                if r:
                    rows.append((ts, group.gateway_ip, group.gateway_name or group.name, r.status.value, r.response_ms, r.cause))
        for d in config.devices:
            r = state.device_results.get(d.ip)
            if r:
                rows.append((ts, d.ip, d.name, r.status.value, r.response_ms, r.cause))
        await self._db.executemany(
            "INSERT INTO probe_events(timestamp,target_ip,target_name,status,response_ms,cause)"
            " VALUES(?,?,?,?,?,?)",
            rows,
        )
        await self._db.commit()

    async def record_speed_test(self, result: SpeedResult) -> None:
        assert self._db
        await self._db.execute(
            "INSERT INTO speed_tests(timestamp,download_mbps,ping_ms,ok) VALUES(?,?,?,?)",
            (result.timestamp, result.download_mbps, result.ping_ms, int(result.ok)),
        )
        await self._db.commit()

    async def get_recent_speed_tests(self, limit: int = 40) -> list[SpeedResult]:
        assert self._db
        cur = await self._db.execute(
            "SELECT timestamp,download_mbps,ping_ms,ok FROM speed_tests ORDER BY timestamp DESC LIMIT ?",
            (limit,),
        )
        rows = await cur.fetchall()
        return [SpeedResult(r[0], r[1], r[2], bool(r[3])) for r in reversed(rows)]

    async def get_hourly_buckets(self, target_ip: str, hours: int = 24) -> list[tuple]:
        assert self._db
        since = time.time() - hours * 3600
        cur = await self._db.execute(
            """
            SELECT CAST((timestamp - :s) / 3600 AS INTEGER) AS bucket, status, COUNT(*) AS cnt
            FROM probe_events
            WHERE target_ip = :ip AND timestamp >= :s
            GROUP BY bucket, status ORDER BY bucket
            """,
            {"s": since, "ip": target_ip},
        )
        return await cur.fetchall()

    async def purge_old(self, retain_days: int = 30) -> None:
        assert self._db
        cutoff = time.time() - retain_days * 86400
        await self._db.execute("DELETE FROM probe_events WHERE timestamp < ?", (cutoff,))
        await self._db.commit()
