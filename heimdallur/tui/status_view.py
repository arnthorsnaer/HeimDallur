from __future__ import annotations
import time

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Label, Sparkline

from heimdallur.core.topology import (
    Device, Group, NetworkConfig, NetworkState, ProbeStatus,
    GatewayEnrichment, SpeedResult,
    InternetQuality, HttpResult,
)

from heimdallur.tui.theme import (
    UI_FG, UI_DIM, UI_BG, UI_BG2, UI_BDR,
    S_OK, S_WARN, S_ERR, S_UNK,
    SPARK_OK_HI, SPARK_OK_LO, SPARK_ERR,
)
from heimdallur.tui.formatting import (
    _sc, _status_word, _ms, _fmt_uptime, _issue_color,
    _rolling_avg, _jitter, _p95, _speed_summary, _loss_pct,
    _internet_diagnosis, _latency_qualifier, _iq_derived_status,
    _check_counts, _count_label,
)
from heimdallur.tui.chrome import FooterBar, HeaderBar, NavButton, SectionToggle


# ── Internet panel ─────────────────────────────────────────────
class InternetPanel(Widget):
    DEFAULT_CSS = f"""
    InternetPanel {{
        width: 1fr;
        height: auto;
        background: {UI_BG2};
        border: solid {UI_BDR};
        padding: 0 1;
    }}
    #inet-header       {{ height: 1; layout: horizontal; }}
    #inet-summary      {{ width: 1fr; height: 1; }}
    #inet-hint         {{ width: 9; height: 1; content-align: right middle; color: {UI_DIM}; }}
    #inet-detail       {{ height: auto; display: none; padding-top: 1; }}
    #inet-diagnosis    {{ height: 1; }}
    #inet-ip-hdr-row   {{ height: 1; layout: horizontal; }}
    #inet-dns-hdr-row  {{ height: 1; layout: horizontal; }}
    #inet-http-hdr-row {{ height: 1; layout: horizontal; }}
    #inet-ip-hdr       {{ width: auto; margin-right: 2; color: {UI_DIM}; text-style: bold; }}
    #inet-ip-compact   {{ width: 1fr; height: 1; }}
    #inet-ip-rows      {{ height: auto; }}
    #inet-dns-hdr      {{ width: auto; margin-right: 2; color: {UI_DIM}; text-style: bold; }}
    #inet-dns-compact  {{ width: 1fr; height: 1; }}
    #inet-dns-rows     {{ height: auto; }}
    #inet-http-hdr     {{ width: auto; margin-right: 2; color: {UI_DIM}; text-style: bold; }}
    #inet-http-compact {{ width: 1fr; height: 1; }}
    #inet-http-rows    {{ height: auto; }}
    #inet-speed-hdr    {{ height: 1; color: {UI_DIM}; text-style: bold; margin-top: 1; }}
    #inet-spark-hdr    {{ height: 1; color: {UI_DIM}; text-style: bold; margin-top: 1; }}
    #inet-speed-row    {{ height: 1; }}
    InternetPanel Sparkline {{ height: 3; }}
    """

    def __init__(self) -> None:
        super().__init__()
        self._status_since: float = 0.0
        self._status_word: str = "—"
        self._status_color: str = S_UNK
        self._prev_status: ProbeStatus | None = None
        self._expanded: bool = False
        self._ip_expanded: bool = False
        self._dns_expanded: bool = False
        self._http_expanded: bool = False
        self._last_detail_args: tuple | None = None

    def compose(self) -> ComposeResult:
        with Horizontal(id="inet-header"):
            yield Label("", id="inet-summary")
            yield Label("", id="inet-hint")
        with Vertical(id="inet-detail"):
            yield Label("", id="inet-diagnosis")
            with Horizontal(id="inet-ip-hdr-row"):
                yield Label("", id="inet-ip-hdr")
                yield Label("", id="inet-ip-compact")
                yield SectionToggle("ip")
            yield Label("", id="inet-ip-rows")
            with Horizontal(id="inet-dns-hdr-row"):
                yield Label("", id="inet-dns-hdr")
                yield Label("", id="inet-dns-compact")
                yield SectionToggle("dns")
            yield Label("", id="inet-dns-rows")
            with Horizontal(id="inet-http-hdr-row"):
                yield Label("", id="inet-http-hdr")
                yield Label("", id="inet-http-compact")
                yield SectionToggle("http")
            yield Label("", id="inet-http-rows")
            yield Label("SPEED TEST", id="inet-speed-hdr")
            yield Label("", id="inet-speed-row")
            yield Sparkline([], min_color=SPARK_OK_LO, max_color=SPARK_OK_HI, id="inet-speed-spark")
            yield Label("", id="inet-spark-hdr")
            yield Sparkline([], min_color=SPARK_OK_LO, max_color=SPARK_OK_HI, id="inet-lat-spark")

    def on_mount(self) -> None:
        self.border_title = "INTERNET"
        self.set_interval(1, self._tick)
        self._refresh_hint()

    def on_click(self) -> None:
        self._toggle()

    def _toggle(self) -> None:
        self._expanded = not self._expanded
        if not self._expanded:
            self._ip_expanded = self._dns_expanded = self._http_expanded = False
        self.query_one("#inet-detail", Vertical).display = self._expanded
        self._refresh_hint()

    def _refresh_hint(self) -> None:
        arrow = "▴" if self._expanded else "▾"
        self.query_one("#inet-hint", Label).update(
            f"[{UI_FG}]I[/][{UI_DIM}] {arrow}[/]"
        )

    def _tick(self) -> None:
        if not self._status_since:
            return
        elapsed = time.time() - self._status_since
        c = self._status_color
        sw = self._status_word
        self.border_title = (
            f"[bold {c}]INTERNET · {sw.upper()}[/]"
            f" [{UI_DIM}]({_fmt_uptime(elapsed)})[/]"
        )

    def on_section_toggle_toggled(self, msg: SectionToggle.Toggled) -> None:
        if msg.section == "ip":
            self._ip_expanded = not self._ip_expanded
        elif msg.section == "dns":
            self._dns_expanded = not self._dns_expanded
        elif msg.section == "http":
            self._http_expanded = not self._http_expanded
        if self._last_detail_args is not None:
            self._render_detail(*self._last_detail_args)

    def update(self, state: NetworkState, config: NetworkConfig,
               ont_lat: list[float], ont_loss: list[float],
               speed: SpeedResult | None,
               iq: InternetQuality | None,
               snapshot) -> None:

        if iq is not None:
            derived = _iq_derived_status(iq)
        else:
            ont = state.ont_result
            derived = ont.status if ont else ProbeStatus.UNKNOWN

        c  = _sc(derived)
        sw = _status_word(derived)

        # Duration tracks binary connectivity (online vs offline), not quality.
        # HEALTHY and DEGRADED both count as "online" — the timer only resets
        # when crossing the UNREACHABLE boundary in either direction.
        offline      = derived        == ProbeStatus.UNREACHABLE
        was_offline  = self._prev_status == ProbeStatus.UNREACHABLE
        conn_changed = (self._prev_status is None) or (offline != was_offline)

        if conn_changed:
            self._status_since = time.time()
            self._status_word  = "Offline" if offline else "Online"
            self._status_color = S_ERR if offline else S_OK
        self._prev_status = derived

        self.styles.border = ("solid", c)
        elapsed = time.time() - self._status_since if self._status_since else 0.0
        self.border_title = (
            f"[bold {c}]INTERNET · {sw.upper()}[/]"
            f" [{UI_DIM}]({_fmt_uptime(elapsed)})[/]"
        )

        # ── Collapsed summary line ──────────────────────────────
        if iq is not None:
            ip_ok, ip_tot, dns_ok, dns_tot, http_ok, http_tot = _check_counts(iq)
            avg_rtt = _rolling_avg(
                [r.rtt_ms for r in iq.raw_ip if r.rtt_ms is not None]
            )
            rtt_str = (f"  [{UI_DIM}]·  LATENCY[/] [{c}]{avg_rtt:.0f}ms[/]"
                       if avg_rtt is not None else "")
            spd_str = _speed_summary(speed)
            self.query_one("#inet-summary", Label).update(
                f"[{UI_DIM}]IP[/] {_count_label(ip_ok, ip_tot)}"
                f"   [{UI_DIM}]DNS[/] {_count_label(dns_ok, dns_tot)}"
                f"   [{UI_DIM}]HTTP[/] {_count_label(http_ok, http_tot)}"
                + spd_str + rtt_str
            )
        else:
            avg_lat = _rolling_avg(ont_lat)
            lat_str = (f"  [{UI_DIM}]·  LATENCY[/] [{c}]{avg_lat:.1f}ms[/]"
                       if avg_lat is not None else "")
            if speed and speed.ok:
                dl_c = S_OK if speed.download_mbps >= 50 else (S_WARN if speed.download_mbps >= 10 else S_ERR)
                spd_lead = f"[{UI_DIM}]SPEED ↓[/] [{dl_c}]{speed.download_mbps:.0f} Mbps[/]"
            else:
                spd_lead = f"[{UI_DIM}]SPEED —[/]"
            self.query_one("#inet-summary", Label).update(spd_lead + lat_str)

        if iq is None:
            return

        self._last_detail_args = (iq, speed, ont_lat, snapshot)
        self._render_detail(iq, speed, ont_lat, snapshot)

    def _render_detail(self, iq: InternetQuality, speed: SpeedResult | None,
                       ont_lat: list[float], snapshot) -> None:
        # ── Diagnosis banner ────────────────────────────────────
        diag_c, diag_msg = _internet_diagnosis(iq)
        diag_icon = "✓" if diag_c == S_OK else ("⚠" if diag_c == S_WARN else "✗")
        self.query_one("#inet-diagnosis", Label).update(
            f"[{diag_c}]{diag_icon} {diag_msg}[/]"
        )

        ip_ok, ip_tot, dns_ok, dns_tot, http_ok, http_tot = _check_counts(iq)

        # ── IP section ───────────────────────────────────────────
        self.query_one("#inet-ip-hdr", Label).update(
            f"[{UI_DIM}]IP[/] {_count_label(ip_ok, ip_tot)}"
        )
        compact_lbl = self.query_one("#inet-ip-compact", Label)
        rows_lbl    = self.query_one("#inet-ip-rows",    Label)

        if self._ip_expanded:
            compact_lbl.display = False
            rows: list[str] = []
            for r in iq.raw_ip:
                rc   = _sc(r.status)
                icon = "●" if r.status == ProbeStatus.HEALTHY else ("~" if r.status == ProbeStatus.DEGRADED else "✗")
                rtt_s  = f"[{rc}]{r.rtt_ms:.0f}ms[/]" if r.rtt_ms is not None else f"[{S_ERR}]timeout[/]"
                hist   = snapshot.inet_ip_lat.get(r.target, [])
                loss_h = snapshot.inet_ip_loss.get(r.target, [])
                j  = _jitter(hist);  p  = _p95(hist);  lp = _loss_pct(loss_h)
                j_s  = f"[{UI_DIM}]±{j:.1f}ms[/]"   if j  is not None else f"[{UI_DIM}]±—[/]"
                p_s  = f"[{UI_DIM}]P95 {p:.0f}ms[/]" if p  is not None else f"[{UI_DIM}]P95 —[/]"
                lp_s = f"[{S_ERR}]{lp:.0f}% loss[/]" if lp > 0 else f"[{UI_DIM}]0% loss[/]"
                rows.append(
                    f"[{rc}]{icon}[/] [{UI_FG}]{r.target:<9}[/] [{UI_DIM}]{r.label:<11}[/]"
                    f" {rtt_s:<18} {j_s:<20} {lp_s:<18} {p_s}"
                )
            rows_lbl.update("\n".join(rows))
            rows_lbl.display = True
        else:
            ok_ip  = [r for r in iq.raw_ip if r.status in (ProbeStatus.HEALTHY, ProbeStatus.UNKNOWN)]
            bad_ip = [r for r in iq.raw_ip if r.status in (ProbeStatus.DEGRADED, ProbeStatus.UNREACHABLE)]
            if ok_ip:
                compact_lbl.update("  ".join(
                    f"[{S_OK}]●[/] [{UI_FG}]{r.target}[/]" for r in ok_ip
                ))
                compact_lbl.display = True
            else:
                compact_lbl.display = False
            if bad_ip:
                detail_rows: list[str] = []
                for r in bad_ip:
                    rc   = _sc(r.status)
                    icon = "~" if r.status == ProbeStatus.DEGRADED else "✗"
                    rtt_s  = f"[{rc}]{r.rtt_ms:.0f}ms[/]" if r.rtt_ms is not None else f"[{S_ERR}]timeout[/]"
                    loss_h = snapshot.inet_ip_loss.get(r.target, [])
                    lp     = _loss_pct(loss_h)
                    lp_s   = f"  [{S_ERR}]{lp:.0f}% loss[/]" if lp > 0 else ""
                    detail_rows.append(
                        f"[{rc}]{icon}[/] [{UI_FG}]{r.target:<9}[/] [{UI_DIM}]{r.label:<11}[/]"
                        f" {rtt_s}{lp_s}"
                    )
                rows_lbl.update("\n".join(detail_rows))
                rows_lbl.display = True
            else:
                rows_lbl.display = False

        # ── DNS section ──────────────────────────────────────────
        self.query_one("#inet-dns-hdr", Label).update(
            f"[{UI_DIM}]DNS[/] {_count_label(dns_ok, dns_tot)}"
        )
        dns_compact = self.query_one("#inet-dns-compact", Label)
        dns_rows    = self.query_one("#inet-dns-rows",    Label)

        if self._dns_expanded:
            dns_compact.display = False
            rows = []
            for r in iq.dns:
                rc     = S_OK if r.success else S_ERR
                icon   = "●" if r.success else "✗"
                hist   = snapshot.inet_dns_lat.get(r.hostname, [])
                loss_h = snapshot.inet_dns_loss.get(r.hostname, [])
                avg_ms = _rolling_avg(hist)
                lp     = _loss_pct(loss_h)
                if r.success:
                    ms_s  = f"[{rc}]{r.lookup_ms:.0f}ms[/]" if r.lookup_ms is not None else "—"
                    avg_s = f"[{UI_DIM}]avg {avg_ms:.0f}ms[/]" if avg_ms is not None else ""
                    lp_s  = f"[{S_ERR}]{lp:.0f}% fail[/]" if lp > 0 else f"[{UI_DIM}]0% fail[/]"
                    rows.append(
                        f"[{rc}]{icon}[/] [{UI_FG}]{r.hostname:<18}[/] {ms_s:<12} {avg_s:<18} {lp_s}"
                    )
                else:
                    fail_s = f"[{S_ERR}]{lp:.0f}% fail[/]" if lp > 0 else f"[{S_ERR}]FAILED[/]"
                    rows.append(
                        f"[{rc}]{icon}[/] [{UI_FG}]{r.hostname:<18}[/] [{S_ERR}]lookup failed[/]"
                        f"{'':32} {fail_s}"
                    )
            dns_rows.update("\n".join(rows))
            dns_rows.display = True
        else:
            ok_dns  = [r for r in iq.dns if r.success]
            bad_dns = [r for r in iq.dns if not r.success]
            if ok_dns:
                dns_compact.update("  ".join(
                    f"[{S_OK}]●[/] [{UI_FG}]{r.hostname}[/]" for r in ok_dns
                ))
                dns_compact.display = True
            else:
                dns_compact.display = False
            if bad_dns:
                detail_rows = []
                for r in bad_dns:
                    loss_h = snapshot.inet_dns_loss.get(r.hostname, [])
                    lp     = _loss_pct(loss_h)
                    fail_s = f"[{S_ERR}]{lp:.0f}% fail[/]" if lp > 0 else f"[{S_ERR}]FAILED[/]"
                    detail_rows.append(
                        f"[{S_ERR}]✗[/] [{UI_FG}]{r.hostname:<18}[/]"
                        f" [{S_ERR}]lookup failed[/]  {fail_s}"
                    )
                dns_rows.update("\n".join(detail_rows))
                dns_rows.display = True
            else:
                dns_rows.display = False

        # ── HTTP section ─────────────────────────────────────────
        self.query_one("#inet-http-hdr", Label).update(
            f"[{UI_DIM}]HTTP[/] {_count_label(http_ok, http_tot)}"
        )
        http_compact = self.query_one("#inet-http-compact", Label)
        http_rows    = self.query_one("#inet-http-rows",    Label)

        def _http_row(r: HttpResult) -> str:
            rc   = S_OK if r.success else S_ERR
            icon = "●" if r.success else "✗"
            sc_s = f"[{rc}]{r.status_code}[/]" if r.status_code is not None else f"[{S_ERR}]err[/]"
            tot_s = f"[{UI_FG}]{r.total_ms:.0f}ms[/]" if r.total_ms is not None else f"[{UI_DIM}]—[/]"
            return (
                f"[{rc}]{icon}[/] [{UI_FG}]{r.label:<11}[/]"
                f" [{UI_DIM}]{r.short_path:<18}[/] {sc_s:<10} {tot_s}"
            )

        if self._http_expanded:
            http_compact.display = False
            http_rows.update("\n".join(_http_row(r) for r in iq.http))
            http_rows.display = True
        else:
            ok_http  = [r for r in iq.http if r.success]
            bad_http = [r for r in iq.http if not r.success]
            if ok_http:
                http_compact.update("  ".join(
                    f"[{S_OK}]●[/] [{UI_FG}]{r.label}[/]" for r in ok_http
                ))
                http_compact.display = True
            else:
                http_compact.display = False
            if bad_http:
                http_rows.update("\n".join(_http_row(r) for r in bad_http))
                http_rows.display = True
            else:
                http_rows.display = False

        # ── Latency sparkline ────────────────────────────────────
        primary_hist  = snapshot.inet_ip_lat.get("1.1.1.1", ont_lat)
        avg_rtt_spark = _rolling_avg(primary_hist) if primary_hist else None
        if avg_rtt_spark is not None:
            q_c, q_s = _latency_qualifier(avg_rtt_spark)
            self.query_one("#inet-spark-hdr", Label).update(
                f"[{UI_DIM}]LATENCY  1.1.1.1  avg {avg_rtt_spark:.0f}ms[/]"
                f"  [{q_c}]{q_s}[/]"
            )
        else:
            self.query_one("#inet-spark-hdr", Label).update(
                f"[{UI_DIM}]LATENCY  1.1.1.1  avg —[/]"
            )
        if primary_hist:
            self.query_one("#inet-lat-spark", Sparkline).data = primary_hist

        # ── Speed section ────────────────────────────────────────
        dl_hist = snapshot.dl_hist
        avg_dl  = _rolling_avg(dl_hist) if dl_hist else None

        if speed and speed.ok:
            age_s  = _fmt_uptime(time.time() - speed.timestamp)
            dl_c   = S_OK if speed.download_mbps >= 50 else (S_WARN if speed.download_mbps >= 10 else S_ERR)
            ping_c = S_OK if speed.ping_ms <= 30        else (S_WARN if speed.ping_ms <= 80        else S_ERR)
            avg_part = (
                f"  [{UI_DIM}]·  avg ~{avg_dl:.0f} Mbps[/]" if avg_dl is not None else ""
            )
            self.query_one("#inet-speed-row", Label).update(
                f"[{UI_DIM}]↓[/] [{dl_c}]{speed.download_mbps:.0f} Mbps[/]"
                f"  [{UI_DIM}]·  ping[/] [{ping_c}]{speed.ping_ms:.0f}ms[/]"
                + avg_part
                + f"  [{UI_DIM}]·  tested {age_s} ago[/]"
            )
        else:
            self.query_one("#inet-speed-row", Label).update(
                f"[{UI_DIM}]Pending — runs every 5 min[/]"
            )
        if dl_hist:
            self.query_one("#inet-speed-spark", Sparkline).data = dl_hist


# ── Home Network panel ─────────────────────────────────────────
class HomeNetworkPanel(Widget):
    DEFAULT_CSS = f"""
    HomeNetworkPanel {{
        width: 1fr;
        height: 1fr;
        background: {UI_BG2};
        border: solid {UI_BDR};
        padding: 0 1;
    }}
    #hn-groups     {{ height: 1fr; layout: horizontal; }}
    #hn-wifi-col   {{ width: 1fr; margin-right: 4; }}
    #hn-lan-col    {{ width: 1fr; }}
    #hn-wifi-hdr   {{ height: 1; color: {UI_DIM}; text-style: bold; }}
    #hn-lan-hdr    {{ height: 1; color: {UI_DIM}; text-style: bold; }}
    """

    def __init__(self, config: NetworkConfig) -> None:
        super().__init__()
        self._config = config
        self._status_since: float = 0.0
        self._status_word: str = "—"
        self._status_color: str = S_UNK
        self._prev_composite: ProbeStatus | None = None
        self._wifi_groups = [g for g in config.groups if g.type == "wifi"]
        self._lan_groups  = [g for g in config.groups if g.type == "lan"]

    def compose(self) -> ComposeResult:
        with Horizontal(id="hn-groups"):
            with VerticalScroll(id="hn-wifi-col"):
                yield Label("", id="hn-wifi-hdr")
                for group in self._wifi_groups:
                    devices = self._config.devices_in_group(group.id)
                    yield GroupRow(group, devices)
            with VerticalScroll(id="hn-lan-col"):
                yield Label("", id="hn-lan-hdr")
                for group in self._lan_groups:
                    devices = self._config.devices_in_group(group.id)
                    yield GroupRow(group, devices)

    def on_mount(self) -> None:
        self.border_title = "HOME NETWORK"
        self.set_interval(1, self._tick)

    def _tick(self) -> None:
        if not self._status_since:
            return
        elapsed = time.time() - self._status_since
        c = self._status_color
        sw = self._status_word
        self.border_title = (
            f"[bold {c}]HOME NETWORK · {sw.upper()}[/]"
            f" [{UI_DIM}]({_fmt_uptime(elapsed)})[/]"
        )

    def _composite_status(self, state: NetworkState) -> ProbeStatus:
        """Derive home network status from all gateway + device probes combined.
        Any device responding means the network is not fully offline."""
        all_results = list(state.gateway_results.values()) + list(state.device_results.values())
        if not all_results:
            return ProbeStatus.UNKNOWN
        responding   = any(r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED) for r in all_results)
        unreachable  = any(r.status == ProbeStatus.UNREACHABLE for r in all_results)
        if responding:
            return ProbeStatus.HEALTHY if not unreachable else ProbeStatus.DEGRADED
        return ProbeStatus.UNREACHABLE

    def update(self, state: NetworkState, config: NetworkConfig,
               gw_enrichment: dict[str, GatewayEnrichment]) -> None:
        composite = self._composite_status(state)
        sw = {
            ProbeStatus.HEALTHY:     "Online",
            ProbeStatus.DEGRADED:    "Partially Online",
            ProbeStatus.UNREACHABLE: "Offline",
            ProbeStatus.UNKNOWN:     "—",
        }[composite]
        c = _sc(composite)

        if composite != self._prev_composite:
            self._prev_composite = composite
            self._status_since = time.time()
            self._status_word = sw
            self._status_color = c

        self.styles.border = ("solid", c)
        elapsed = time.time() - self._status_since if self._status_since else 0.0
        self.border_title = (
            f"[bold {c}]HOME NETWORK · {sw.upper()}[/]"
            f" [{UI_DIM}]({_fmt_uptime(elapsed)})[/]"
        )

        # Count healthy groups per type
        def _groups_ok(groups: list) -> int:
            return sum(
                1 for g in groups
                if not g.gateway_ip or (
                    (r := state.gateway_results.get(g.gateway_ip)) is None
                    or r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED)
                )
            )

        wifi_ok = _groups_ok(self._wifi_groups)
        lan_ok  = _groups_ok(self._lan_groups)

        wifi_c = S_OK if wifi_ok == len(self._wifi_groups) else (S_WARN if wifi_ok > 0 else S_ERR)
        lan_c  = S_OK if lan_ok  == len(self._lan_groups)  else (S_WARN if lan_ok  > 0 else S_ERR)

        self.query_one("#hn-wifi-hdr", Label).update(
            f"[{UI_DIM}]WI-FI[/] [{wifi_c}]{wifi_ok}/{len(self._wifi_groups)}[/]"
        )
        self.query_one("#hn-lan-hdr", Label).update(
            f"[{UI_DIM}]LAN[/] [{lan_c}]{lan_ok}/{len(self._lan_groups)}[/]"
        )

        for group in self._config.groups:
            enr = gw_enrichment.get(group.gateway_ip) if group.gateway_ip else None
            self.query_one(f"#grp-{group.id}", GroupRow).update(state, enr)


# ── Group row ──────────────────────────────────────────────────
class GroupRow(Widget):
    DEFAULT_CSS = f"""
    GroupRow {{
        height: 1;
        layout: horizontal;
    }}
    .grp-icon  {{ width: 2; }}
    .grp-name  {{ width: 1fr; color: {UI_FG}; }}
    .grp-count {{ width: 5; content-align: right middle; }}
    """

    def __init__(self, group: Group, devices: list[Device]) -> None:
        super().__init__(id=f"grp-{group.id}")
        self._group = group
        self._devices = devices

    def compose(self) -> ComposeResult:
        gid = self._group.id
        # Strip leading "WiFi " / "LAN " — panel title already says it
        name = self._group.name
        for prefix in ("WiFi ", "LAN "):
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        yield Label("", id=f"grp-icon-{gid}",  classes="grp-icon")
        yield Label(name, classes="grp-name")
        yield Label("", id=f"grp-count-{gid}", classes="grp-count")

    def update(self, state: NetworkState, enrichment: GatewayEnrichment | None) -> None:
        g = self._group
        gid = g.id
        has_gw = bool(g.gateway_ip)

        gw_result = state.gateway_results.get(g.gateway_ip) if has_gw else None
        gw_offline = gw_result is not None and gw_result.status == ProbeStatus.UNREACHABLE

        if gw_offline:
            # Gateway explicitly unreachable — authoritative failure signal
            c, icon = S_ERR, "✗"
        else:
            # Derive indicator from device aggregate for both WiFi and LAN groups
            dev_results = [state.device_results.get(d.ip) for d in self._devices]
            known = [r for r in dev_results if r is not None]
            if not known:
                c, icon = UI_DIM, "○"
            else:
                n_ok  = sum(1 for r in known if r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED))
                n_err = sum(1 for r in known if r.status == ProbeStatus.UNREACHABLE)
                if n_ok == len(known):
                    c, icon = S_OK, "●"
                elif n_err == len(known):
                    c, icon = S_ERR, "✗"
                else:
                    c, icon = S_WARN, "~"

        self.query_one(f"#grp-icon-{gid}", Label).update(f"[{c}]{icon}[/]")

        # Online / total  (gateway counts as one device)
        total = len(self._devices) + (1 if has_gw else 0)
        online = 0
        if has_gw and gw_result and gw_result.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED):
            online += 1
        for d in self._devices:
            r = state.device_results.get(d.ip)
            if r and r.status in (ProbeStatus.HEALTHY, ProbeStatus.DEGRADED):
                online += 1

        count_c = S_OK if online == total else (S_WARN if online > 0 else S_ERR)
        self.query_one(f"#grp-count-{gid}", Label).update(
            f"[{count_c}]{online}/{total}[/]"
        )



def _notify_admin(config: NetworkConfig, *, urgent: bool = False) -> str:
    action = "call" if urgent else "let"
    suffix = "" if urgent else " know"
    return f"{action} {config.contacts.network_admin}{suffix}"


def _refresh_or_notify(config: NetworkConfig) -> str:
    return f"refresh browser or {_notify_admin(config)}"


def _fmt_age_brief(seconds: float) -> str:
    seconds_i = max(0, int(seconds))
    if seconds_i < 60:
        return f"{seconds_i}s"
    minutes = seconds_i // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    return f"{hours}h"


# ── Status panel ───────────────────────────────────────────────
class StatusPanel(Widget):
    DEFAULT_CSS = f"""
    StatusPanel {{
        height: auto;
        background: {UI_BG2};
        border: solid {UI_BDR};
        border-title-color: {UI_FG};
        border-title-style: bold;
        padding: 0 1;
    }}
    #st-row    {{ height: 1; layout: horizontal; }}
    #st-icon   {{ width: 2; }}
    #st-msg    {{ width: 1fr; }}
    #st-hint   {{ width: 9; content-align: right middle; color: {UI_DIM}; }}
    #st-detail {{ height: auto; display: none; padding: 1 0 0 1; color: {UI_DIM}; }}
    """

    def __init__(self) -> None:
        super().__init__()
        self._expanded = False

    def compose(self) -> ComposeResult:
        with Horizontal(id="st-row"):
            yield Label("", id="st-icon")
            yield Label("", id="st-msg")
            yield Label("", id="st-hint")
        yield Label("", id="st-detail")

    def on_mount(self) -> None:
        self.border_title = "STATUS"
        self._refresh_hint()

    def on_click(self) -> None:
        self.toggle()

    def toggle(self) -> None:
        self._expanded = not self._expanded
        self.query_one("#st-detail", Label).display = self._expanded
        self._refresh_hint()

    def _refresh_hint(self) -> None:
        arrow = "▴" if self._expanded else "▾"
        self.query_one("#st-hint", Label).update(
            f"[{UI_FG}]S[/][{UI_DIM}] {arrow}[/]"
        )

    def update_viewer_warning(self, config: NetworkConfig, reason: str,
                              age_seconds: float | None = None) -> None:
        action = _refresh_or_notify(config)
        if reason == "missing":
            c, icon = S_ERR, "✗"
            summary = f"Monitor is not sending updates · {action}"
            detail = (
                "Try refreshing the browser. If this message stays, the main "
                "Heimdallur monitor may not be running. The information below may be old."
            )
        elif reason == "unreadable":
            c, icon = S_ERR, "✗"
            summary = f"Monitor updates cannot be read · {action}"
            detail = (
                "Try refreshing the browser. If this message stays, the web view "
                "cannot read updates from the main monitor. The information below may be old."
            )
        else:
            c, icon = S_WARN, "⚠"
            age = _fmt_age_brief(age_seconds or 0.0)
            summary = f"Monitor has not updated in {age} · {action}"
            detail = (
                "Try refreshing the browser. If this message stays, the main "
                "Heimdallur monitor has not sent a recent update. The information below may be old."
            )

        self.query_one("#st-icon", Label).update(f"[{c}]{icon}[/]")
        self.query_one("#st-msg", Label).update(f"[{c}]{summary}[/]")
        self.query_one("#st-detail", Label).update(f"[{c}]{detail}[/]")

    def update(self, state: NetworkState, config: NetworkConfig,
               iq: "InternetQuality | None" = None,
               doctor_checks: list[dict] | None = None) -> None:
        issues = state.problems(config)
        doctor_checks = doctor_checks or []
        doctor_failures = [c for c in doctor_checks if c.get("status") == "fail"]
        doctor_warnings = [c for c in doctor_checks if c.get("status") == "warn"]
        admin = config.contacts.network_admin
        isp   = config.contacts.isp_name
        iq_issue: str | None = None

        # Surface internet quality issues only when basic connectivity is up
        ont_up = not (state.ont_result    and state.ont_result.status    == ProbeStatus.UNREACHABLE)
        rtr_up = not (state.router_result and state.router_result.status == ProbeStatus.UNREACHABLE)
        if iq is not None and ont_up and rtr_up:
            diag_c, diag_msg = _internet_diagnosis(iq)
            if diag_c != S_OK:
                iq_issue = diag_msg
                issues   = [diag_msg] + issues

        ont_down = state.ont_result    and state.ont_result.status    == ProbeStatus.UNREACHABLE
        rtr_down = state.router_result and state.router_result.status == ProbeStatus.UNREACHABLE

        contact_hint: str | None = None
        if ont_down:
            c, icon = S_ERR, "✗"
            summary = f"Internet is down · {_notify_admin(config, urgent=True)}"
            contact_hint = f"→ {admin} will contact {isp} if the outage is on their end"
        elif rtr_down:
            c, icon = S_ERR, "✗"
            summary = f"Home network down · {_notify_admin(config, urgent=True)}"
        elif issues:
            c, icon = S_WARN, "⚠"
            net_issues = [i for i in issues if i != iq_issue]
            ap  = sum(1 for i in net_issues if "access point offline" in i or "switch offline" in i)
            dev = sum(1 for i in net_issues if "unreachable" in i)
            parts = []
            if iq_issue:                        parts.append(iq_issue)
            if ap:  parts.append(f"{ap} access point{'s' if ap > 1 else ''} offline")
            if dev: parts.append(f"{dev} device{'s' if dev > 1 else ''} unreachable")
            summary = (" · ".join(parts) if parts else issues[0]) + f" · {_notify_admin(config)}"
        elif doctor_failures:
            c, icon = S_ERR, "✗"
            summary = f"Monitor has {len(doctor_failures)} system failure{'s' if len(doctor_failures) > 1 else ''} · {_notify_admin(config, urgent=True)}"
        elif doctor_warnings:
            c, icon = S_WARN, "⚠"
            summary = f"Monitor has {len(doctor_warnings)} system warning{'s' if len(doctor_warnings) > 1 else ''} · {_notify_admin(config)}"
        else:
            c, icon = S_OK, "●"
            summary = "All systems operational"

        self.query_one("#st-icon", Label).update(f"[{c}]{icon}[/]")
        self.query_one("#st-msg",  Label).update(f"[{c}]{summary}[/]")

        if issues:
            lines = [f"[{_issue_color(i)}]{i}[/]" for i in issues]
            if contact_hint:
                lines.append(f"[{UI_DIM}]{contact_hint}[/]")
        else:
            lines = [f"[{UI_DIM}]No network issues detected[/]"]

        if doctor_checks:
            lines.append(f"[{UI_DIM}]Deployment doctor:[/]")
            for check in doctor_checks:
                dc = S_ERR if check.get("status") == "fail" else S_WARN
                lines.append(f"[{dc}]{check.get('name', 'check')}: {check.get('summary', '')}[/]")
                if check.get("why"):
                    lines.append(f"[{UI_DIM}]  Why: {check['why']}[/]")
                steps = check.get("next_steps") or []
                if steps:
                    lines.append(f"[{UI_DIM}]  Next: {steps[0]}[/]")
        self.query_one("#st-detail", Label).update("\n".join(lines))


# ── Status screen ──────────────────────────────────────────────
class StatusScreen(Screen):
    CSS = f"""
    StatusScreen  {{ background: {UI_BG}; color: {UI_FG}; layout: vertical; }}
    #body         {{ height: 1fr; padding: 0 1; layout: vertical; }}
    StatusPanel   {{ margin-bottom: 1; }}
    InternetPanel {{ margin-bottom: 1; }}
    """

    BINDINGS = [
        ("h",     "switch_to_history",  "History"),
        ("d",     "switch_to_devices",  "Devices"),
        ("s",     "toggle_status",      "Toggle Status"),
        ("i",     "toggle_internet",    "Toggle Internet"),
        ("q",     "app.quit",           "Quit"),
    ]

    def __init__(self, config: NetworkConfig, start_time: float) -> None:
        super().__init__()
        self._config = config
        self._start_time = start_time

    def compose(self) -> ComposeResult:
        yield HeaderBar(self._start_time)
        with Vertical(id="body"):
            yield StatusPanel()
            yield InternetPanel()
            yield HomeNetworkPanel(self._config)
        yield FooterBar(self._config)

    def update_state(self, enriched, snapshot) -> None:
        s = enriched.network
        c = self._config
        self.query_one(StatusPanel).update(s, c, enriched.internet_quality, enriched.doctor_checks)
        self.query_one(InternetPanel).update(
            s, c, snapshot.ont_lat, snapshot.ont_loss,
            enriched.speed_result, enriched.internet_quality, snapshot,
        )
        self.query_one(HomeNetworkPanel).update(s, c, enriched.gw_enrichment)
        self.query_one(FooterBar).update(s, c)

    def update_viewer_warning(self, reason: str, age_seconds: float | None = None) -> None:
        self.query_one(StatusPanel).update_viewer_warning(self._config, reason, age_seconds)

    def action_toggle_status(self) -> None:
        self.query_one(StatusPanel).toggle()

    def action_toggle_internet(self) -> None:
        self.query_one(InternetPanel)._toggle()

    def on_nav_button_pressed(self, msg: NavButton.Pressed) -> None:
        if msg.action == "history":
            self.action_switch_to_history()
        elif msg.action == "devices":
            self.action_switch_to_devices()
        elif msg.action == "quit":
            self.app.exit()

    def action_switch_to_history(self) -> None:
        from heimdallur.tui.history_view import HistoryScreen
        self.app.push_screen(HistoryScreen(self._config, None))

    def action_switch_to_devices(self) -> None:
        from heimdallur.tui.devices_view import DevicesScreen
        self.app.push_screen(DevicesScreen(self._config))
