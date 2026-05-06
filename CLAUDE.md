# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
make install       # uv sync — install all dependencies
make mock          # run TUI in mock mode (no real network, no Pi needed)
make dev           # mock mode with hot reload via watchfiles
make status-render # single-pass rich status output (no TUI, useful for quick checks)

make deploy        # rsync to pi@heimdallur.local + restart systemd service
make logs          # tail systemd journal on the Pi
```

There are no automated tests. Validate changes by running `make mock` and visually confirming the TUI behaves correctly.

## After any TUI change — regenerate screenshots

The PR description and `docs/screenshots/` are kept in sync manually. After changing anything in `heimdallur/tui/` or `heimdallur/mock/`, regenerate all screenshots and commit them:

```bash
PYTHONPATH=. python scripts/capture_all.py --output-dir docs/screenshots
git add docs/screenshots/
```

`capture_all.py` runs 10 scenarios (all-healthy, internet degraded/offline, router offline, AP offline, multiple issues, both panels expanded, history screen, devices screen). Each capture takes ~6 s; the full run takes ~60 s. It requires Python 3.12 and either `rsvg-convert` (librsvg2-bin) or `cairosvg` (`pip install cairosvg`) for PNG conversion.

## Architecture

### Data flow

```
HeimdallurApp (tui/app.py)
  ├── _probe_loop()   every 30 s  →  Prober / MockProber  →  NetworkState
  ├── _speed_loop()   every 300 s →  run_speed_test()     →  SpeedResult
  └── ProbeComplete message
        └── StatusScreen.update_state()
              ├── InternetPanel.update()
              ├── RouterPanel.update()
              ├── GroupsPanel.update() × N
              └── FooterBar.update()
```

`HeimdallurApp` maintains rolling history buffers (deque, maxlen=40) for latency, loss, CPU, memory, and download speed. These are passed as plain `list[float]` snapshots to each panel on every update — panels do not hold their own history except `RouterPanel`, which accumulates its own internal latency list (up to 20 readings) since only the current `response_ms` is passed in per cycle.

### Mock mode

Set `NETWATCH_MOCK=1` to use `MockProber` instead of real pings. Set `NETWATCH_MOCK_SCENARIO` to a TOML file path to inject specific failures:

```
heimdallur/mock/scenarios/
  all_healthy.toml
  internet_degraded.toml   # ont = "slow"
  internet_offline.toml    # ont = "down"
  router_offline.toml      # router = "down" — cascades to all devices
  gateway_offline.toml     # one AP down — downstream devices suppressed
  multiple_issues.toml     # AP + degraded + intermittent device
```

Failure modes per IP or alias (`"ont"`, `"router"`): `"down"` | `"slow"` | `"intermittent"`.

`NETWATCH_SCREENSHOT_DB` sets a custom SQLite path, used by the screenshot scripts to avoid lock contention between sequential runs.

### Fault cascade logic

Offline states cascade: router offline → all gateways and devices shown as `UNKNOWN` (not individually failed). Gateway offline → its downstream devices shown as `UNKNOWN`. This keeps signal-to-noise low — only the root cause is highlighted. Implemented in `MockProber.probe_all()` and reflected in `NetworkState.problems()`.

### Key files

| File | Purpose |
|---|---|
| `heimdallur/config/devices.toml` | Network topology — groups, APs, devices. Edit to match your network. |
| `heimdallur/core/topology.py` | All data models: `ProbeResult`, `NetworkState`, `RouterStats`, `SpeedResult`, `NetworkConfig` |
| `heimdallur/tui/status_view.py` | All status-screen widgets. Colour palette and semantic status colours defined at the top. |
| `heimdallur/tui/app.py` | App entry point, probe/speed loops, history accumulation |
| `heimdallur/mock/network.py` | `MockProber` and `MockNetwork` — fake probe results, router stats, speed tests |
| `scripts/capture_all.py` | Generates all 10 UI-state screenshots using `asyncio.run()` per capture |
| `scripts/screenshot.py` | Single-capture helper — `--scenario PATH`, `--keys KEY,...` |

### TUI panels

`InternetPanel` and `RouterPanel` both follow the same pattern:
- Collapsed (default): bold `● ONLINE` / `✗ OFFLINE`, live duration ticker (`set_interval(1, _tick)`), rolling-average summary line
- Expanded: click panel or press `i` / `r` — reveals sparkline + detail labels; border subtitle shows `▾ / ▴`
- State transition timestamp tracked in `_status_since`; `_prev_status` compared on each `update()` call to detect changes

`StatusPanel` (the top banner) has the same expand/collapse pattern, toggled by `Space`.

### Screens

Three Textual `Screen` subclasses pushed onto the screen stack:
- `StatusScreen` — main view, always at the base of the stack
- `HistoryScreen` — pushed by `h`; currently uses mock bar data, not live DB
- `DevicesScreen` — pushed by `d`; updated via `ProbeComplete` messages even while not visible

### Storage

`Store` (core/store.py) writes probe events and speed tests to SQLite at `~/.local/share/heimdallur/events.db`. The `HistoryScreen` does not yet read from this DB — it renders mock bars. Connecting history to real data is a known gap.
