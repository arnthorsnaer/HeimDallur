# Heimdallur

> **Pre-alpha — under active development. Not production ready.**

A terminal-based network health monitor designed to run on a Raspberry Pi with an attached display, positioned physically next to your ONT and router.

Heimdallur gives you a persistent, at-a-glance view of your entire home network — ideal for households with many smart home devices where quickly understanding the current state of the network matters.

![Heimdallur status screen — all healthy](docs/snapshots/01-status-healthy.png)

## What it does

- **Internet health** — IP, DNS, and HTTP reachability checks against multiple targets; latency trending and speed test results (Cloudflare)
- **Home network panel** — router latency, memory usage, and uptime; device groups (WI-FI access points and LAN segments) with per-AP signal strength and online/offline counts
- **Status panel** — single-line summary that expands to list every active fault
- **Incident reports** — emails the home network admin when internet or home network connectivity is restored after an outage; sent via Gmail with a 16-character app password
- **History screen** — 24h uptime bars per network segment
- **Device list** — full device inventory with live latency and status per device

Faults cascade correctly: if an access point goes offline, its downstream devices are shown as affected rather than individually failed, keeping the signal-to-noise ratio low.

![Heimdallur status screen — multiple issues detected](docs/snapshots/06-status-multiple-issues.png)

## Intended use

Mount or place a Raspberry Pi with a small display next to your ONT or router. Heimdallur runs as a systemd service and displays continuously. When something feels off — the internet is slow, a group of smart lights stops responding, a gateway goes unreachable — the monitor tells you immediately without having to open a phone app or log into a router UI.

## Stack

- Python 3.12
- [Textual](https://github.com/Textualize/textual) — TUI framework
- [textual-serve](https://github.com/Textualize/textual-serve) — serve TUI in browser via xterm.js
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

# Serve in the browser (mock mode) — opens at http://localhost:8080
make web-mock
```

## Web UI

Heimdallur can be served in any browser on the local network via
[textual-serve](https://github.com/Textualize/textual-serve), which renders
the full interactive TUI as an xterm.js terminal in the browser. No code
changes are needed — the same app runs both on the Pi display and in the
browser.

```bash
# Private by default — serves on 127.0.0.1:8080
make web          # production viewer mode
make web-mock     # mock mode  (no real pings)
```

Open `http://127.0.0.1:8080` on the same machine. To expose the browser UI to
other devices, pass an explicit host, for example:

```bash
uv run python scripts/web_serve.py --host heimdallur.local --port 8080
```

The web UI and `/status.md` endpoint can reveal device names, IP addresses, and
network health. Only expose them on trusted networks, preferably behind a
reverse proxy with authentication.

All keyboard shortcuts (`i`, `r`, `n`, `h`, `d`, `q`) work in the browser.

> **Note:** textual-serve renders a terminal in the browser, not a native
> web page. It works well on desktop browsers; mobile support is limited.

## Configuration

The tracked demo topology lives in `heimdallur/config/default-network.toml`.
Keep that package-owned file read-only. For a real local network, copy it to
the user config path and edit that file instead:

```bash
mkdir -p ~/.config/heimdallur
cp heimdallur/config/default-network.toml ~/.config/heimdallur/network.toml
python scripts/validate-config.py ~/.config/heimdallur/network.toml
```

Normal Heimdallur runs use `~/.config/heimdallur/network.toml` automatically
when it exists. Set `HEIMDALLUR_CONFIG=/path/to/network.toml` to use an
explicit config path. Screenshot generation always forces
`default-network.toml` so docs and release images keep using the demo dataset.

## Notifications

When an outage ends — internet or home network going from offline back to online — Heimdallur can automatically email an incident report to the home network admin. Enable notifications and add the recipient to your network TOML:

```toml
[notifications]
enabled = true

[contacts]
home_network_admin_email = "you@example.com"   # who receives the report
```

Set Gmail credentials through the environment instead of storing them in TOML:

```bash
export HEIMDALLUR_GMAIL_SENDER_EMAIL="heimdallur.alerts@gmail.com"
export HEIMDALLUR_GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

Notifications are sent only when `[notifications].enabled` is true and both
Gmail environment variables plus `home_network_admin_email` are present. To
disable notifications, set `enabled = false` without changing any environment
variables.

To generate a Gmail app password: **Google Account → Security → 2-Step Verification → App passwords**.

The footer shows whether notifications are active — `✉ you@example.com` when active, `✉  notifications off` when disabled, or `✉  no email configured` when enabled but missing required email settings. Emails fire on recovery, not during the outage, so a full internet outage will still trigger a report once connectivity is restored.

![Heimdallur — email notifications configured](docs/snapshots/01b-status-email-configured.png)

## Environment variables

Public runtime environment variables use the `HEIMDALLUR_` prefix:

| Variable | Purpose |
|---|---|
| `HEIMDALLUR_CONFIG` | Explicit network TOML path |
| `HEIMDALLUR_STATE_FILE` | Shared live-state JSON path |
| `HEIMDALLUR_STATUS_FILE` | Markdown status file path for web/status tooling |
| `HEIMDALLUR_GMAIL_SENDER_EMAIL` | Gmail sender address for notifications |
| `HEIMDALLUR_GMAIL_APP_PASSWORD` | Gmail app password for notifications |
| `HEIMDALLUR_MOCK` | Use mock probes instead of real network probes |
| `HEIMDALLUR_MOCK_SCENARIO` | Mock scenario TOML path |
| `HEIMDALLUR_SNAPSHOT_DB` | SQLite DB path used by snapshot tooling |
| `HEIMDALLUR_DEMO_EMAIL` | Demo recipient used by snapshot tooling |
| `HEIMDALLUR_DEMO_SENDER_EMAIL` | Demo sender used by snapshot tooling |

## Deploying to a Raspberry Pi

A minimal appliance install is:

```bash
sudo git clone https://github.com/arnthorsnaer/HeimDallur /opt/heimdallur
sudo chown -R "$USER:$(id -gn)" /opt/heimdallur
cd /opt/heimdallur
uv sync --no-dev
mkdir -p ~/.config/heimdallur
cp heimdallur/config/default-network.toml ~/.config/heimdallur/network.toml
python scripts/validate-config.py ~/.config/heimdallur/network.toml
```

Install the main TUI service after editing `scripts/heimdallur.service` if your
runtime user is not `pi` or `uv` is installed somewhere other than
`/home/pi/.local/bin/uv`:

```bash
sudo cp /opt/heimdallur/scripts/heimdallur.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now heimdallur
systemctl status heimdallur --no-pager -l
```

The bundled unit renders Heimdallur on `/dev/tty1`. For browser access, run
`scripts/web_serve.py` separately or install a deployment-specific web service.

The current Makefile also contains maintainer-oriented Pi helpers. Defaults are
safe to override from the command line or environment:

```bash
make pi-status      # show commit, version, doctor output
make pi-update      # trigger heimdallur-update.service now
make pi-sync-config # sync one config file, then restart configured services
make pi-web-status  # show web service/listener status
make deploy         # rsync code, sync deps, then restart configured services
make logs           # tail the main service log
```

Common overrides:

```bash
make pi-status PI_USER=pi PI_HOST=heimdallur.local PI_APP_DIR=/opt/heimdallur
make pi-sync-config PI_CONFIG_SRC=~/.config/heimdallur/network.toml
make deploy PI_RESTART_DISPLAY='sudo systemctl restart heimdallur' PI_RESTART_WEB=
```

### Console font size

Heimdallur is designed to fill an 800×480 display (e.g. HyperPixel 4") using a large terminal font so the status is legible from across the room. The right font depends on your display resolution:

| Display | Target size | Font |
|---|---|---|
| 800×480 | ~66×20 | Terminus 12×24 |
| 1024×600 | ~80×24 | Terminus 12×24 |
| 1280×800 | ~100×30 | Terminus 12×24 |

To set the console font on the Pi, edit `/etc/default/console-setup`:

```
FONTFACE="Terminus"
FONTSIZE="12x24"
```

Then apply without rebooting:

```bash
sudo setupcon
```

To verify the terminal dimensions after the font change:

```bash
stty -F /dev/tty1 size   # prints rows cols, e.g. "20 66"
```

The `terminus-font` package must be installed (`sudo apt install terminus-font`).

---

## Running in production

### Keeping the application up to date

Heimdallur ships a systemd timer that checks the configured update channel once an hour and applies updates automatically. The default channel is tagged releases:

```toml
[updates]
channel = "release"  # "off" | "release" | "edge"
```

Use `release` for normal appliance installs. Use `edge` only for lab units that
should follow `origin/main`; use `off` to disable automatic updates without
disabling the systemd timer.

Install the timer once after the initial deploy:

```bash
# On the Pi
sudo cp /opt/heimdallur/scripts/heimdallur-update.service /etc/systemd/system/
sudo cp /opt/heimdallur/scripts/heimdallur-update.timer   /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now heimdallur-update.timer
```

On the `release` channel, when a new `vX.Y.Z` release tag is published, the timer will:
1. fetch tags from GitHub;
2. choose the latest matching release tag;
3. check out that tag in a clean detached checkout;
4. verify `pyproject.toml` matches the tag version;
5. run `uv sync --no-dev --frozen`;
6. restart `heimdallur`.

On the `edge` channel, the timer fetches `origin/main`, fast-forwards the local
`main` branch, syncs dependencies, and restarts `heimdallur`.

Before changing anything, the script runs `scripts/pi-doctor.py` as a pre-update
health check. If the current deployment is already unhealthy, the update aborts
without changing the checkout unless `UPDATE_FORCE=1` is set. After any update,
the script runs the health check again. If the post-update check fails, it rolls
the checkout back to the previous commit, syncs dependencies again, restarts the
service, and reports failure for operator follow-up.

Set `TARGET_TAG=vX.Y.Z` in the update service environment to pin a specific
release while using the `release` channel. Set `HEALTH_CHECK_CMD` to override
the default doctor check, `UPDATE_HEALTH_CHECK=0` to disable health checks, or
`UPDATE_FORCE=1` to bypass a failing pre-update check.

All activity is logged to the systemd journal under the `heimdallur-update` identifier:

```bash
journalctl -t heimdallur-update -f
```

To trigger an immediate update without waiting for the timer:

```bash
sudo systemctl start heimdallur-update
```

To check a deployment without changing anything, run the doctor script from the
Heimdallur checkout:

```bash
python scripts/pi-doctor.py --app-dir /opt/heimdallur
```

It checks config validity, status freshness, processes/services, git state,
network routes, web listener, and display basics. Warnings and failures include
suggested next commands for humans or agents.

The footer shows the running version as `v0.5.0+20260513.d40c034` — date and git hash — so you can identify the exact commit at a glance and match it against the GitHub commit list without running any commands.

---

### Publishing a release

Releases are created from `main` after the version bump has already been
reviewed and merged. The usual flow is:

1. Open a PR that updates `pyproject.toml` to the next version.
2. Merge that PR to `main`.
3. Check out the updated `main` locally.
4. Run `scripts/create-release.sh`.

By default, the script reads the version from `pyproject.toml`, creates an
annotated `vX.Y.Z` tag at `HEAD`, pushes the tag to `origin`, and creates a
GitHub Release using generated release notes.

Prerequisites:

- Run from the repository root on a clean `main` checkout.
- Install and authenticate the GitHub CLI with release permissions:
  `gh auth login`.

Prepare the local checkout:

```bash
git switch main
git pull --ff-only
```

Preview the actions without changing tags or releases:

```bash
DRY_RUN=1 scripts/create-release.sh
```

Create the tag and GitHub release:

```bash
scripts/create-release.sh
```

You can also pass a version explicitly:

```bash
scripts/create-release.sh 0.6.0
```

Set `NOTES_FILE=path/to/notes.md` to provide hand-written release notes instead
of GitHub-generated notes. Set `REMOTE=<name>` if tags should be pushed
somewhere other than `origin`.

---

### Updating device configuration

All devices and groups are defined in the network TOML. On a live Pi, copy a
candidate config to a temporary path and use the safe apply helper from the
Heimdallur checkout:

```bash
# Validate and show the diff without changing production
python /opt/heimdallur/scripts/apply-config.py /tmp/new-network.toml --dry-run

# Apply after reviewing the diff; restart commands depend on your deployment
python /opt/heimdallur/scripts/apply-config.py /tmp/new-network.toml --yes \
  --restart-command 'sudo systemctl restart heimdallur' \
  --verify
```

The helper validates the candidate, shows a unified diff, backs up the current
config, applies only with `--yes`, runs any restart commands you provide, and can
verify that `status.md` is freshly rewritten. It prints a rollback command after
applying.

For validation only, use:

```bash
python /opt/heimdallur/scripts/validate-config.py /path/to/new-network.toml
# or
python -m heimdallur --mode validate-config /path/to/new-network.toml
```

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
