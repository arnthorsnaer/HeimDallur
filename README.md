# Heimdallur

> **Pre-alpha — under active development. Not production ready.**

A terminal-based network health monitor designed to run on a Raspberry Pi with an attached display, positioned physically next to your ONT and router.

Heimdallur gives you a persistent, at-a-glance view of your entire home network — ideal for households with many smart home devices where quickly understanding the current state of the network matters.

![Heimdallur status screen — all healthy](docs/screenshots/01-status-healthy.png)

## What it does

- **Internet health** — IP, DNS, and HTTP reachability checks against multiple targets; latency trending and speed test results (Cloudflare)
- **Home network panel** — router latency, memory usage, and uptime; device groups (WI-FI access points and LAN segments) with per-AP signal strength and online/offline counts
- **Status panel** — single-line summary that expands to list every active fault
- **History screen** — 24h uptime bars per network segment
- **Device list** — full device inventory with live latency and status per device

Faults cascade correctly: if an access point goes offline, its downstream devices are shown as affected rather than individually failed, keeping the signal-to-noise ratio low.

![Heimdallur status screen — multiple issues detected](docs/screenshots/06-status-multiple-issues.png)

## Intended use

Mount or place a Raspberry Pi with a small display next to your ONT or router. Heimdallur runs as a systemd service and displays continuously. When something feels off — the internet is slow, a group of smart lights stops responding, a gateway goes unreachable — the monitor tells you immediately without having to open a phone app or log into a router UI.

## Stack

- Python 3.12
- [Textual](https://github.com/Textualize/textual) — TUI framework
- [aiosqlite](https://github.com/omnilib/aiosqlite) — async SQLite for history
- [httpx](https://github.com/encode/httpx) — speed tests
- [uv](https://github.com/astral-sh/uv) — package management

## Running locally (mock mode)

```bash
# Install dependencies
make install

# Run with simulated network data (no real pings)
make mock

# Run with hot reload during development
make dev
```

## Configuration

All devices and groups are defined in `heimdallur/config/devices.toml`. Edit this file to match your network topology — groups, access points, and devices.

## Deploying to a Raspberry Pi

```bash
make deploy   # rsyncs to pi@heimdallur.local and restarts the systemd service
make logs     # tail the service log
```

---

## Running in production

### Keeping the application up to date

Heimdallur ships a systemd timer that checks the public GitHub repo for updates once an hour and applies them automatically. Install it once after the initial deploy:

```bash
# On the Pi
sudo cp /opt/heimdallur/scripts/heimdallur-update.service /etc/systemd/system/
sudo cp /opt/heimdallur/scripts/heimdallur-update.timer   /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now heimdallur-update.timer
```

When a new commit lands on `main` the timer will:
1. `git pull --ff-only`
2. `uv sync --no-dev`
3. `systemctl restart heimdallur`

All activity is logged to the systemd journal under the `heimdallur-update` identifier:

```bash
journalctl -t heimdallur-update -f
```

To trigger an immediate update without waiting for the timer:

```bash
sudo systemctl start heimdallur-update
```

The footer shows the running version as `v0.3.0+20260507.d40c034` — date and git hash — so you can identify the exact commit at a glance and match it against the GitHub commit list without running any commands.

---

### Updating device configuration

All devices and groups are defined in `heimdallur/config/devices.toml`. On a live Pi you can edit this file directly (or copy a new version over SSH) and then restart the service:

```bash
# Validate before applying
python /opt/heimdallur/scripts/validate-config.py /path/to/new-devices.toml

# Apply
cp /path/to/new-devices.toml /opt/heimdallur/heimdallur/config/devices.toml
sudo systemctl restart heimdallur
```

The validator (`scripts/validate-config.py`) checks TOML syntax, required fields, IP address validity, duplicate IPs, and that every device references a defined group. It exits 0 on success, 1 on any error, so it is safe to use in automated workflows.

---

### Agent / automation access

Heimdallur writes a markdown snapshot of its full current state to:

```
~/.local/share/heimdallur/status.md
```

This file is rewritten after every 30-second probe cycle. An agent with SSH access can read the current network state instantly without running a fresh probe:

```bash
ssh pi@heimdallur.local "cat ~/.local/share/heimdallur/status.md"
```

To force a fresh probe and get the result directly:

```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && uv run python -m heimdallur --mode report"
```

See [`SKILL.md`](SKILL.md) for the full agent skill reference — status queries, config updates, service management, and the complete file reference.

---

## Status

Pre-alpha. Core monitoring loop, TUI, mock mode, and local history storage are working. Production hardening, real router stats integration, and a proper history screen are in progress.
