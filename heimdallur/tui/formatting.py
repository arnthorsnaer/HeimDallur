from __future__ import annotations

from heimdallur.core.topology import InternetQuality, ProbeStatus, SpeedResult
from heimdallur.tui.theme import UI_DIM, S_ERR, S_OK, S_UNK, S_WARN

# ── Formatting helpers ────────────────────────────────────────────────────
def _sc(status: ProbeStatus | None) -> str:
    if status is None: return S_UNK
    return {ProbeStatus.HEALTHY: S_OK, ProbeStatus.DEGRADED: S_WARN,
            ProbeStatus.UNREACHABLE: S_ERR, ProbeStatus.UNKNOWN: S_UNK}[status]

def _status_word(status: ProbeStatus | None) -> str:
    if status is None: return "—"
    return {ProbeStatus.HEALTHY: "Online", ProbeStatus.DEGRADED: "Degraded",
            ProbeStatus.UNREACHABLE: "Offline", ProbeStatus.UNKNOWN: "—"}[status]

def _ms(v: float | None) -> str:
    return f"{v:.0f}ms" if v is not None else "—"

def _fmt_uptime(seconds: float) -> str:
    h, r = divmod(int(seconds), 3600)
    m, s = divmod(r, 60)
    if h >= 24:
        d, h = divmod(h, 24)
        return f"{d}d {h}h {m:02d}m"
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    if m:
        return f"{m}m {s:02d}s"
    return f"{s}s"

def _issue_color(issue: str) -> str:
    low = issue.lower()
    if any(k in low for k in ("offline", "unreachable", "no ip connectivity", "outage")):
        return S_ERR
    return S_WARN

def _rolling_avg(data: list[float], n: int = 10) -> float | None:
    if not data:
        return None
    window = data[-n:]
    return sum(window) / len(window)


def _jitter(data: list[float]) -> float | None:
    if len(data) < 2:
        return None
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return variance ** 0.5


def _p95(data: list[float]) -> float | None:
    if not data:
        return None
    s = sorted(data)
    idx = max(0, int(len(s) * 0.95) - 1)
    return s[idx]


def _speed_summary(speed: "SpeedResult | None") -> str:
    if speed and speed.ok:
        dl_c = S_OK if speed.download_mbps >= 50 else (S_WARN if speed.download_mbps >= 10 else S_ERR)
        return f"  [{UI_DIM}]·  SPEED ↓[/] [{dl_c}]{speed.download_mbps:.0f} Mbps[/]"
    return f"  [{UI_DIM}]·  SPEED —[/]"


def _loss_pct(loss_flags: list[float]) -> float:
    if not loss_flags:
        return 0.0
    return sum(loss_flags) / len(loss_flags) * 100.0


def _internet_diagnosis(iq: "InternetQuality") -> tuple[str, str]:
    """Return (color, message) summarising what the IQ data means."""
    ip_ok    = sum(1 for r in iq.raw_ip if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED))
    ip_tot   = len(iq.raw_ip)
    dns_ok   = sum(1 for r in iq.dns  if r.success)
    dns_tot  = len(iq.dns)
    http_ok  = sum(1 for r in iq.http if r.success)
    http_tot = len(iq.http)

    if ip_tot > 0 and ip_ok == 0:
        return S_ERR,  "No IP connectivity — likely ISP outage"
    if ip_ok == ip_tot and dns_tot > 0 and dns_ok == 0:
        return S_WARN, "All DNS failing — ISP resolver issue — try manual DNS (8.8.8.8)"
    if 0 < ip_ok < ip_tot:
        return S_WARN, "Some IP paths degraded — routing or congestion issue"
    if 0 < dns_ok < dns_tot:
        return S_WARN, "Some DNS resolvers failing — upstream issue, not your line"
    if http_tot > 0 and http_ok == 0 and ip_ok == ip_tot and dns_ok == dns_tot:
        return S_WARN, "All HTTP failing with healthy IP/DNS — possible firewall issue"
    if 0 < http_ok < http_tot:
        return S_WARN, "Some HTTP checks failing — likely destination issue, not your connection"
    return S_OK, "All paths healthy — no action needed"


def _latency_qualifier(avg_ms: float) -> tuple[str, str]:
    if avg_ms < 50:  return S_OK,   "excellent"
    if avg_ms < 100: return S_WARN, "elevated"
    return S_ERR, "degraded"


def _iq_derived_status(iq: InternetQuality) -> ProbeStatus:
    """Derive overall internet status from all three check categories."""
    ok = (
        sum(1 for r in iq.raw_ip if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED))
        + sum(1 for r in iq.dns  if r.success)
        + sum(1 for r in iq.http if r.success)
    )
    total = len(iq.raw_ip) + len(iq.dns) + len(iq.http)
    if total == 0:
        return ProbeStatus.UNKNOWN
    degraded_ip = sum(1 for r in iq.raw_ip if r.status == ProbeStatus.DEGRADED)
    ratio = ok / total
    if ratio == 1.0 and degraded_ip == 0:
        return ProbeStatus.HEALTHY
    if ratio >= 4 / 9:
        return ProbeStatus.DEGRADED
    return ProbeStatus.UNREACHABLE


def _check_counts(iq: InternetQuality) -> tuple[int, int, int, int, int, int]:
    """Return (ip_ok, ip_total, dns_ok, dns_total, http_ok, http_total)."""
    ip_ok   = sum(1 for r in iq.raw_ip if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED))
    dns_ok  = sum(1 for r in iq.dns    if r.success)
    http_ok = sum(1 for r in iq.http   if r.success)
    return ip_ok, len(iq.raw_ip), dns_ok, len(iq.dns), http_ok, len(iq.http)


def _count_label(ok: int, total: int) -> str:
    c = S_OK if ok == total else (S_WARN if ok > 0 else S_ERR)
    return f"[{c}]{ok}/{total}[/]"



