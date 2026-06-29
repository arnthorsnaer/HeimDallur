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

## Deploying to a Raspberry Pi

```bash
make deploy   # rsyncs to pi@heimdallur.local and restarts the systemd service
make logs     # tail the service log
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
