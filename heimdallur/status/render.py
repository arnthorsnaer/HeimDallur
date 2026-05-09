from __future__ import annotations
import asyncio
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box
from heimdallur.config.loader import load_config
from heimdallur.core.topology import ProbeStatus

GREEN = "green"
AMBER = "yellow"
RED   = "red"
GRAY  = "dim"


def _status_str(status: ProbeStatus | None, response_ms: float | None) -> str:
    if status is None:
        return f"[{GRAY}]unknown[/]"
    ms = f"{response_ms:.0f}ms" if response_ms is not None else "timeout"
    colors = {
        ProbeStatus.HEALTHY: GREEN,
        ProbeStatus.DEGRADED: AMBER,
        ProbeStatus.UNREACHABLE: RED,
        ProbeStatus.UNKNOWN: GRAY,
    }
    icons = {
        ProbeStatus.HEALTHY: "✓",
        ProbeStatus.DEGRADED: "~",
        ProbeStatus.UNREACHABLE: "✗",
        ProbeStatus.UNKNOWN: "·",
    }
    c = colors[status]
    i = icons[status]
    return f"[{c}]{i}  {ms}[/]"


async def render_status(console: "Console | None" = None) -> None:
    config = load_config()

    if os.getenv("NETWATCH_MOCK"):
        from pathlib import Path
        from heimdallur.mock.network import MockProber
        scenario = os.getenv("NETWATCH_MOCK_SCENARIO")
        prober = MockProber(config, scenario_path=Path(scenario) if scenario else None)
    else:
        from heimdallur.core.prober import Prober
        prober = Prober(config)

    if console is None:
        console = Console()
    console.print(f"\n[bold]HEIMDALLUR[/]  {datetime.now().strftime('%H:%M:%S')}\n")

    state = await prober.probe_all()

    t = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    t.add_column(style="dim", width=12)
    t.add_column()
    t.add_row("INTERNET", _status_str(state.ont_result.status if state.ont_result else None,
                                      state.ont_result.response_ms if state.ont_result else None))
    t.add_row("ROUTER",   _status_str(state.router_result.status if state.router_result else None,
                                      state.router_result.response_ms if state.router_result else None))
    console.print(t)

    console.print("[dim]Access Points[/]")
    for group in config.groups:
        if group.gateway_ip:
            r = state.gateway_results.get(group.gateway_ip)
            console.print(f"  {_status_str(r.status if r else None, r.response_ms if r else None)}  {group.name}")

    problems = state.problems(config)
    if problems:
        console.print("\n[bold yellow]PROBLEMS[/]")
        for p in problems:
            console.print(f"  [red]✗[/]  {p}")
    else:
        console.print("\n[green]All monitored devices OK[/]")

    total, ok, bad = state.summary(config)
    console.print(f"\n[dim]{total} monitored  ·  {ok} OK  ·  {bad} down[/]\n")
