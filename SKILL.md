---
name: heimdallur
description: >
  Operating Heimdallur — a home network health monitor designed to run as a
  systemd service on a Raspberry Pi. Use this skill when you need to install
  Heimdallur on a device, configure automatic updates, add or modify monitored
  devices and groups, query current network status, or troubleshoot a running
  instance. Assumes SSH access to the target machine.
allowed-tools: Bash Read
---

## Overview

Heimdallur monitors a home network and displays a live terminal dashboard.
It probes all configured devices every 30 seconds and writes a markdown
snapshot of the full network state to `~/.local/share/heimdallur/status.md`
after each cycle — the primary way for agents to read current status.

The application usually lives at `/opt/heimdallur/` on the target host and is
commonly supervised by systemd. Configuration is a single TOML file.

Keep deployment-specific details — hostnames, usernames, passwords, private
network topology, service overrides, and display preferences — outside this
public skill. Store those in private, gitignored operator notes.

### Display + web runtime model

For low overhead, run only one probing instance:

- primary display: `python -m heimdallur --mode tui`
- web UI: `python scripts/web_serve.py --host <host-or-ip> --port <port>`

By default the web server starts Heimdallur in viewer mode:

```bash
python -m heimdallur --mode view
```

Viewer mode reads the shared live-state file written by the primary TUI and
does not run its own probes or speed tests. Use `--standalone` only if the web
process should run a second independent prober.

Default shared state path:

```text
~/.local/share/heimdallur/live-state.json
```

Override with `HEIMDALLUR_STATE_FILE` when needed.

---

## 0. Requirements

**On the Raspberry Pi:**

- Raspberry Pi OS (Bookworm or later) or any Debian-based Linux
- Python 3.12+: `python3 --version`
- [uv](https://github.com/astral-sh/uv) package manager:
  `curl -LsSf https://astral.sh/uv/install.sh | sh`
- git: `sudo apt install -y git`
- Network access to the public repo: `https://github.com/arnthorsnaer/HeimDallur`

**Verify prerequisites:**

```bash
ssh pi@heimdallur.local "python3 --version && uv --version && git --version"
```

All three must return version strings before proceeding.

---

## 1. Installing on the Device

```bash
# Clone the repo
ssh pi@heimdallur.local "sudo git clone https://github.com/arnthorsnaer/HeimDallur /opt/heimdallur"

# Install Python dependencies
ssh pi@heimdallur.local "cd /opt/heimdallur && uv sync --no-dev"

# Install the systemd service unit
ssh pi@heimdallur.local "sudo cp /opt/heimdallur/scripts/heimdallur.service /etc/systemd/system/"
ssh pi@heimdallur.local "sudo systemctl daemon-reload && sudo systemctl enable --now heimdallur"

# Verify it started
ssh pi@heimdallur.local "systemctl is-active heimdallur"
```

Expected output of the last command: `active`

**Note:** The service file at `scripts/heimdallur.service` runs the TUI on the
Pi's attached display. If the file does not exist yet, create it — see the
Troubleshooting section for a minimal unit template.

---

## 2. Setting Up Automatic Updates

The auto-update mechanism is a systemd timer that checks `origin/main` once
per hour and applies updates if the local commit is behind.

```bash
# Install the timer and its companion service unit
ssh pi@heimdallur.local "sudo cp /opt/heimdallur/scripts/heimdallur-update.service /etc/systemd/system/"
ssh pi@heimdallur.local "sudo cp /opt/heimdallur/scripts/heimdallur-update.timer   /etc/systemd/system/"
ssh pi@heimdallur.local "sudo systemctl daemon-reload && sudo systemctl enable --now heimdallur-update.timer"

# Confirm the timer is active
ssh pi@heimdallur.local "systemctl list-timers heimdallur-update.timer"
```

**What happens on each run** (`scripts/auto-update.sh`):
1. `git fetch origin main`
2. Compare local HEAD to remote — exit early if already up to date
3. `git pull --ff-only origin main`
4. `uv sync --no-dev`
5. `systemctl restart heimdallur`
6. Log everything via `logger -t heimdallur-update`

**Trigger an immediate update:**
```bash
ssh pi@heimdallur.local "sudo systemctl start heimdallur-update"
```

**Read the update log:**
```bash
ssh pi@heimdallur.local "journalctl -t heimdallur-update -n 30 --no-pager"
```

**Check currently running commit:**
```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && git log -1 --oneline"
```

---

## 3. Setting / Updating Device Configuration

All monitored devices and network groups are defined in the user config:

```
~/.config/heimdallur/network.toml
```

Set `HEIMDALLUR_CONFIG=/path/to/network.toml` to use an explicit path. If no
user config exists, Heimdallur falls back to the tracked demo config at
`/opt/heimdallur/heimdallur/config/default-network.toml`.

### Schema

```toml
[network]
ont_check_host              = "8.8.8.8"        # WAN reachability target (IP, not hostname)
router_ip                   = "192.168.1.1"     # Router LAN IP
probe_interval_seconds      = 30
speed_test_interval_seconds = 300

[[groups]]
id            = "wifi-main"     # Unique ID — referenced by devices[].group
name          = "WiFi Living Room"
type          = "wifi"          # "wifi" | "lan"
gateway_ip    = "192.168.1.44"  # AP or managed switch IP; "" = no probed gateway
gateway_name  = "Main AP"       # Display label
gateway_model = "U6 Pro"        # Optional model string
channel       = 36              # WiFi channel (wifi groups only)
band          = "5GHz"          # Band label (wifi groups only)

[[devices]]
name  = "Smart TV"
ip    = "192.168.1.120"
group = "wifi-main"             # Must match a groups[].id exactly
type  = "generic"               # generic | light | sensor | smart_plug | smart_switch | server | ap
```

**Cascade rules:**
- `gateway_ip = ""` — group has no probed gateway; devices only go UNKNOWN if the router goes down
- If a gateway goes offline, its downstream devices are shown as UNKNOWN (not individually failed)
- Router offline → every gateway and device shown as UNKNOWN

### Safe update procedure

**Step 1 — Read current config:**
```bash
ssh pi@heimdallur.local "cat ~/.config/heimdallur/network.toml"
```

**Step 2 — Write new config to a temp file and dry-run the safe apply helper:**
```bash
scp network.toml pi@heimdallur.local:/tmp/devices-new.toml
ssh pi@heimdallur.local "cd /opt/heimdallur && python scripts/apply-config.py /tmp/devices-new.toml --dry-run"
```

The helper validates TOML syntax, required fields, valid IPs, duplicate IPs,
and that every `devices[].group` references a defined `groups[].id`. It also
shows a unified diff against the current production config.

**Step 3 — Apply, restart, and verify:**
```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && python scripts/apply-config.py /tmp/devices-new.toml --yes --restart-command 'sudo systemctl restart heimdallur' --verify"
```

Use restart commands appropriate for the deployment. The helper backs up the
current config before replacing it and prints a rollback command.

**Step 4 — Confirm status:**
```bash
ssh pi@heimdallur.local "cat ~/.local/share/heimdallur/status.md"
```

---

## 3a. Configuring Incident Report Emails

Heimdallur emails the home network admin when an outage ends (internet or home
network going offline then back online). Emails are sent on recovery — not
during the outage — so a full internet outage will still produce a report once
connectivity is restored.

### Configure in `~/.config/heimdallur/network.toml`

Add or update these sections:

```toml
[notifications]
enabled = true

[contacts]
home_network_admin_email = "you@example.com"   # recipient
```

Set Gmail credentials through the service environment:

```bash
export HEIMDALLUR_GMAIL_SENDER_EMAIL="heimdallur.alerts@gmail.com"
export HEIMDALLUR_GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

Notifications are sent only when `[notifications].enabled` is true and both
Gmail environment variables plus `home_network_admin_email` are present. To
disable notifications, set `enabled = false` without changing any environment
variables.

**Step 1 — Create a Gmail app password:**
Google Account → Security → 2-Step Verification → App passwords.
Generate one named "Heimdallur" and copy the 16-character code.

**Step 2 — Edit and dry-run:**
```bash
ssh pi@heimdallur.local "cat ~/.config/heimdallur/network.toml"
# Edit locally, then:
scp network.toml pi@heimdallur.local:/tmp/network-new.toml
ssh pi@heimdallur.local "cd /opt/heimdallur && python scripts/apply-config.py /tmp/network-new.toml --dry-run"
```

**Step 3 — Apply:**
```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && python scripts/apply-config.py /tmp/network-new.toml --yes --restart-command 'sudo systemctl restart heimdallur' --verify"
```

**Step 4 — Verify:**
The footer indicator confirms the state — `✉ you@example.com` means notifications
are active; `✉  notifications off` means disabled in config; `✉  no email
configured` means enabled but one or more email settings are missing.

To test without waiting for a real outage, temporarily set
`HEIMDALLUR_GMAIL_APP_PASSWORD` to a valid value and bounce the service — the
notifier fires on the OFFLINE→ONLINE transition, so toggling the ONT or router
off/on in mock mode is not required; simply disconnecting and reconnecting your
broadband will trigger it.

---

## 4. Getting Network Status

### Fast read — snapshot file (preferred)

The running service writes a fresh markdown snapshot after every probe cycle
(default: every 30 seconds):

```bash
ssh pi@heimdallur.local "cat ~/.local/share/heimdallur/status.md"
```

The file contains:
- **Summary** — all healthy, or a list of active faults with cascade context
- **Internet** — ONT latency/loss, IP reachability (3 targets), DNS, HTTP checks, speed test
- **Router** — latency, CPU %, memory %, uptime
- **Groups** — per-gateway status, client count, signal strength, per-device table
- **All Devices** — flat table of every monitored device with status and latency

The `Probed:` timestamp at the top of the file shows when data was collected.
If the file is older than 60 seconds, the service may not be running — check
with `systemctl is-active heimdallur`.

### Fresh probe — force a new cycle

When you need guaranteed-fresh data (e.g., immediately after a config change):

```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && uv run python -m heimdallur --mode report"
```

This runs a full probe, overwrites `status.md`, and prints the markdown to
stdout. Takes 5–15 seconds.

### Parse a specific field

```bash
# Just the summary line
ssh pi@heimdallur.local "grep -A5 '## Summary' ~/.local/share/heimdallur/status.md | head -6"

# List of active problems only
ssh pi@heimdallur.local "awk '/## Summary/{found=1} found && /^- /{print} found && /^---/{exit}' ~/.local/share/heimdallur/status.md"
```

---

## 5. Troubleshooting

### Run deployment doctor first

Use the read-only doctor script for a quick production health check:

```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && python scripts/pi-doctor.py --app-dir /opt/heimdallur"
```

It checks config validity, mock mode, status freshness, primary/web processes,
systemd units, git state, network routes, web listener, and display basics.
Warnings and failures include a `Next:` section with suggested commands.

### Service not running

```bash
ssh pi@heimdallur.local "systemctl status heimdallur"
ssh pi@heimdallur.local "journalctl -u heimdallur -n 50 --no-pager"
```

Common causes:
- Python or uv not on PATH for the service user → check `ExecStart` in the unit file
- Network TOML syntax error → run `validate-config.py` and fix before restarting
- Display not available (headless Pi) → the TUI requires a terminal; use `--mode status` instead for headless use

### status.md not being updated

```bash
ssh pi@heimdallur.local "stat ~/.local/share/heimdallur/status.md"
```

If the file is missing or stale, the service is not completing probe cycles.
Check logs for probe errors, then try:
```bash
ssh pi@heimdallur.local "sudo systemctl restart heimdallur && sleep 35 && cat ~/.local/share/heimdallur/status.md"
```

### Auto-update not working

```bash
ssh pi@heimdallur.local "systemctl list-timers heimdallur-update.timer"
ssh pi@heimdallur.local "journalctl -t heimdallur-update -n 20 --no-pager"
```

If the timer is not listed, re-run the install steps in section 2.
If the update script errors, the most common cause is git credential or
network access — verify the Pi can reach GitHub:
```bash
ssh pi@heimdallur.local "curl -s https://api.github.com/repos/arnthorsnaer/HeimDallur/commits/main | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d[\"sha\"][:7], d[\"commit\"][\"message\"].splitlines()[0])'"
```

### Minimal systemd service unit template

If `scripts/heimdallur.service` is missing from an older install, create it:

```ini
[Unit]
Description=Heimdallur network monitor
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/heimdallur
ExecStart=/home/pi/.local/bin/uv run python -m heimdallur --mode tui
Restart=on-failure
RestartSec=10
Environment=TERM=xterm-256color

[Install]
WantedBy=multi-user.target
```

Write to `/etc/systemd/system/heimdallur.service`, then:
```bash
ssh pi@heimdallur.local "sudo systemctl daemon-reload && sudo systemctl enable --now heimdallur"
```

### Reset to a known-good state

```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && sudo git fetch origin main && sudo git reset --hard origin/main && uv sync --no-dev && sudo systemctl restart heimdallur"
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Read network status | `ssh pi@heimdallur.local "cat ~/.local/share/heimdallur/status.md"` |
| Force fresh probe | `ssh pi@heimdallur.local "cd /opt/heimdallur && uv run python -m heimdallur --mode report"` |
| Dry-run config apply | `ssh pi@heimdallur.local "cd /opt/heimdallur && python scripts/apply-config.py /tmp/devices-new.toml --dry-run"` |
| Apply config + restart | `ssh pi@heimdallur.local "cd /opt/heimdallur && python scripts/apply-config.py /tmp/devices-new.toml --yes --restart-command 'sudo systemctl restart heimdallur' --verify"` |
| Trigger immediate update | `ssh pi@heimdallur.local "sudo systemctl start heimdallur-update"` |
| Check running version | `ssh pi@heimdallur.local "cd /opt/heimdallur && git log -1 --oneline"` |
| View service logs | `ssh pi@heimdallur.local "journalctl -u heimdallur -n 50 --no-pager"` |
| Restart service | `ssh pi@heimdallur.local "sudo systemctl restart heimdallur"` |
