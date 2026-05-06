from __future__ import annotations
import time
import httpx
from heimdallur.core.topology import SpeedResult

_DL_URL  = "https://speed.cloudflare.com/__down?bytes=5000000"   # 5 MB
_PING_URL = "https://1.1.1.1"


async def run_speed_test(timeout: float = 20.0) -> SpeedResult:
    ts = time.time()
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            # Ping
            t0 = time.monotonic()
            await client.head(_PING_URL)
            ping_ms = (time.monotonic() - t0) * 1000

            # Download
            t1 = time.monotonic()
            r = await client.get(_DL_URL)
            elapsed = time.monotonic() - t1
            download_mbps = (len(r.content) * 8) / elapsed / 1_000_000

        return SpeedResult(timestamp=ts, download_mbps=download_mbps, ping_ms=ping_ms, ok=True)
    except Exception:
        return SpeedResult(timestamp=ts, download_mbps=0.0, ping_ms=0.0, ok=False)
