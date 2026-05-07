"""Incident report emails — sent when internet or home network recovers from an outage."""
from __future__ import annotations

import smtplib
import time
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from heimdallur.core.topology import NetworkConfig, NetworkState, ProbeStatus


def _internet_offline(state: NetworkState) -> bool:
    return (
        state.ont_result is not None
        and state.ont_result.status == ProbeStatus.UNREACHABLE
    )


def _home_offline(state: NetworkState) -> bool:
    """Mirrors HomeNetworkPanel._composite_status logic."""
    if state.router_result and state.router_result.status == ProbeStatus.UNREACHABLE:
        return True
    gw = list(state.gateway_results.values())
    return bool(gw) and all(r.status == ProbeStatus.UNREACHABLE for r in gw)


def _fmt_duration(seconds: float) -> str:
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}m {s}s"
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"


@dataclass
class _OutageTracker:
    name: str
    _offline: Optional[bool] = None
    _since: Optional[float] = None

    def update(self, is_offline: bool) -> Optional[float]:
        """Return outage duration (seconds) if recovery was just detected, else None."""
        if self._offline is None:
            self._offline = is_offline
            if is_offline:
                self._since = time.time()
            return None

        if not self._offline and is_offline:
            self._offline = True
            self._since = time.time()
            return None

        if self._offline and not is_offline:
            duration = time.time() - (self._since or time.time())
            self._offline = False
            self._since = None
            return duration

        return None


class IncidentNotifier:
    """Tracks per-subsystem outages and sends a Gmail incident report on recovery."""

    def __init__(self, config: NetworkConfig) -> None:
        self._config = config
        self._inet = _OutageTracker("Internet")
        self._home = _OutageTracker("Home Network")

    def check(self, state: NetworkState) -> None:
        """Call after each probe cycle. Fires emails synchronously in a thread pool."""
        inet_duration = self._inet.update(_internet_offline(state))
        home_duration = self._home.update(_home_offline(state))

        if inet_duration is not None:
            self._send("Internet", inet_duration)
        if home_duration is not None:
            self._send("Home Network", home_duration)

    def _send(self, subsystem: str, duration: float) -> None:
        cfg = self._config.gmail_notification
        if not cfg.sender_email or not cfg.app_password:
            return
        recipient = self._config.contacts.network_admin_email
        if not recipient:
            return

        dur_str = _fmt_duration(duration)
        admin = self._config.contacts.network_admin

        subject = f"[Heimdallur] {subsystem} outage resolved — duration {dur_str}"

        body = (
            f"Hi {admin},\n\n"
            f"The {subsystem} outage has been resolved.\n\n"
            f"  Affected:  {subsystem}\n"
            f"  Duration:  {dur_str}\n"
            f"  Resolved:  {time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n\n"
            f"All systems are back online.\n\n"
            f"— Heimdallur"
        )

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = cfg.sender_email
        msg["To"] = recipient
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(cfg.sender_email, cfg.app_password)
                smtp.sendmail(cfg.sender_email, recipient, msg.as_string())
        except Exception:
            pass
