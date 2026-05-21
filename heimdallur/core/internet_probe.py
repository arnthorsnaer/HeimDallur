from __future__ import annotations
import asyncio
import socket
import ssl
import time
from typing import Optional

import httpx

from heimdallur.core.prober import _ping, _classify
from heimdallur.core.topology import (
    DnsResult, HttpResult, InternetQuality, ProbeStatus, RawIpResult,
)

# ── Probe targets ──────────────────────────────────────────────
IP_TARGETS: list[tuple[str, str]] = [
    ("1.1.1.1", "Cloudflare"),
    ("8.8.8.8", "Google"),
    ("9.9.9.9", "Quad9"),
]

DNS_TARGETS: list[tuple[str, str]] = [
    ("cloudflare.com", "Cloudflare"),
    ("google.com",     "Google"),
    ("quad9.net",      "Quad9"),
]

HTTP_TARGETS: list[tuple[str, str, str, int]] = [
    # (url, label, short_path, expected_status)
    ("https://www.cloudflare.com/cdn-cgi/trace",       "Cloudflare", "/cdn-cgi/trace", 200),
    ("https://www.google.com/generate_204",             "Google",     "/generate_204",  204),
    ("http://www.msftconnecttest.com/connecttest.txt",  "Microsoft",  "/connecttest",   200),
]

_HTTP_TIMEOUT = 10.0
_CONNECT_TIMEOUT = 5.0


async def _probe_raw_ip(target: str, label: str) -> RawIpResult:
    ok, ms = await _ping(target)
    return RawIpResult(
        target=target,
        label=label,
        status=_classify(ms if ok else None),
        rtt_ms=ms if ok else None,
    )


async def _probe_dns(hostname: str, label: str) -> DnsResult:
    loop = asyncio.get_running_loop()
    t0 = time.monotonic()
    try:
        infos = await asyncio.wait_for(
            loop.getaddrinfo(hostname, None, type=socket.SOCK_STREAM),
            timeout=5.0,
        )
        lookup_ms = (time.monotonic() - t0) * 1000
        resolved_ip: Optional[str] = infos[0][4][0] if infos else None
        return DnsResult(
            hostname=hostname, label=label,
            success=True, lookup_ms=lookup_ms, resolved_ip=resolved_ip,
        )
    except Exception:
        lookup_ms = (time.monotonic() - t0) * 1000
        return DnsResult(
            hostname=hostname, label=label,
            success=False, lookup_ms=lookup_ms, resolved_ip=None,
        )


async def _measure_tcp_tls(host: str, port: int) -> tuple[Optional[float], Optional[float]]:
    """Return (tcp_ms, tls_handshake_ms) by upgrading an existing TCP connection to TLS."""
    loop = asyncio.get_running_loop()

    # TCP connect only
    t_tcp = time.monotonic()
    try:
        transport, _ = await asyncio.wait_for(
            loop.create_connection(asyncio.Protocol, host=host, port=port),
            timeout=_CONNECT_TIMEOUT,
        )
    except Exception:
        return None, None
    tcp_ms = (time.monotonic() - t_tcp) * 1000

    # Upgrade the same TCP connection to TLS — no second TCP handshake
    ctx = ssl.create_default_context()
    t_tls = time.monotonic()
    try:
        tls_transport = await asyncio.wait_for(
            loop.start_tls(transport, asyncio.Protocol(), ctx, server_hostname=host),
            timeout=_CONNECT_TIMEOUT,
        )
        tls_ms = (time.monotonic() - t_tls) * 1000
        tls_transport.close()
    except Exception:
        transport.close()
        return tcp_ms, None

    return tcp_ms, tls_ms


async def _measure_tcp(host: str, port: int) -> Optional[float]:
    loop = asyncio.get_running_loop()
    t_tcp = time.monotonic()
    try:
        transport, _ = await asyncio.wait_for(
            loop.create_connection(asyncio.Protocol, host=host, port=port),
            timeout=_CONNECT_TIMEOUT,
        )
    except Exception:
        return None
    tcp_ms = (time.monotonic() - t_tcp) * 1000
    transport.close()
    return tcp_ms


async def _probe_http(url: str, label: str, short_path: str, expected_status: int) -> HttpResult:
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    if parsed.scheme == "https":
        tcp_ms, tls_ms = await _measure_tcp_tls(host, port)
    else:
        tcp_ms, tls_ms = await _measure_tcp(host, port), None

    t0 = time.monotonic()
    ttfb_ms: Optional[float] = None
    total_ms: Optional[float] = None
    status_code: Optional[int] = None
    success = False

    try:
        async with httpx.AsyncClient(
            timeout=_HTTP_TIMEOUT,
            follow_redirects=False,
            verify=True,
        ) as client:
            async with client.stream("GET", url) as resp:
                ttfb_ms = (time.monotonic() - t0) * 1000
                status_code = resp.status_code
                async for _ in resp.aiter_bytes():
                    pass
                total_ms = (time.monotonic() - t0) * 1000
                success = status_code == expected_status
    except Exception:
        total_ms = (time.monotonic() - t0) * 1000

    return HttpResult(
        url=url, label=label, short_path=short_path,
        success=success,
        status_code=status_code,
        tcp_ms=tcp_ms,
        tls_ms=tls_ms,
        ttfb_ms=ttfb_ms,
        total_ms=total_ms,
    )


class InternetProber:
    async def probe_all(self) -> InternetQuality:
        ts = time.time()

        ip_coros  = [_probe_raw_ip(t, l)              for t, l       in IP_TARGETS]
        dns_coros = [_probe_dns(h, l)                  for h, l       in DNS_TARGETS]
        http_coros = [_probe_http(u, l, p, s)          for u, l, p, s in HTTP_TARGETS]

        ip_results, dns_results, http_results = await asyncio.gather(
            asyncio.gather(*ip_coros),
            asyncio.gather(*dns_coros),
            asyncio.gather(*http_coros),
        )

        return InternetQuality(
            timestamp=ts,
            raw_ip=list(ip_results),
            dns=list(dns_results),
            http=list(http_results),
        )
