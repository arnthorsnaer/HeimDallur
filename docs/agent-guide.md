# Heimdallur — Agent Guide

This document is a skill reference for AI agents operating on a machine running Heimdallur. It covers reading network status, updating device configuration, and managing the application itself.

---

## What is Heimdallur?

Heimdallur is a terminal-based home network health monitor running as a **systemd service** on a Raspberry Pi. It probes all devices on the local network every 30 seconds and displays a live TUI dashboard. It also writes a markdown status snapshot after every probe so agents can read the current state instantly.

---

## Reading the Current Network Status

The service writes a fresh markdown snapshot to:

```
~/.local/share/heimdallur/status.md
```

Read it over SSH without waiting:

```bash
ssh pi@heimdallur.local "cat ~/.local/share/heimdallur/status.md"
```

The file contains:

- **Summary** — all-healthy or a list of active faults with cascade context
- **Internet** — ONT latency/loss, IP reachability, DNS, HTTP checks, speed test
- **Router** — latency, CPU, memory, uptime
- **Groups** — per-AP gateway status, client count, signal strength, per-device table
- **All Devices** — flat table of every monitored device

The file is rewritten every 30 seconds (the probe interval). The `Probed:` timestamp at the top of the file tells you when the data was last collected.

### Forcing a fresh probe

If you need a guaranteed-fresh read (e.g., immediately after a config change), run:

```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && uv run python -m heimdallur --mode report"
```

This runs a single full probe cycle, overwrites `status.md`, and prints the markdown to stdout. Takes ~5–10 seconds.

---

## Checking Service Health

```bash
# Is the service running?
ssh pi@heimdallur.local "systemctl is-active heimdallur"

# Recent logs
ssh pi@heimdallur.local "journalctl -u heimdallur -n 50 --no-pager"

# Full status
ssh pi@heimdallur.local "systemctl status heimdallur"
```

---

## Updating Device Configuration

Device groups and IPs are defined in:

```
/opt/heimdallur/heimdallur/config/devices.toml
```

### Schema

```toml
[network]
ont_check_host              = "8.8.8.8"        # WAN reachability check target
router_ip                   = "192.168.1.1"
probe_interval_seconds      = 30
speed_test_interval_seconds = 300

[[groups]]
id            = "wifi-main"           # unique identifier (used by devices)
name          = "WiFi Living Room"    # display name
type          = "wifi"                # "wifi" | "lan"
gateway_ip    = "192.168.1.44"        # AP/switch IP to probe; "" = no probed gateway
gateway_name  = "Main AP"
gateway_model = "U6 Pro"
channel       = 36
band          = "5GHz"

[[devices]]
name  = "Smart TV"
ip    = "192.168.1.120"
group = "wifi-main"                   # must match a group id
type  = "generic"                     # generic | light | sensor | smart_plug | smart_switch | server | ap
```

**Rules:**
- Every `devices[].group` must reference a defined `groups[].id`
- Every IP must be unique and valid
- `gateway_ip = ""` means the group has no probed gateway (devices still appear, cascade only on router failure)

### Safe update procedure

1. **Read** the current config to understand existing groups and IPs:
   ```bash
   ssh pi@heimdallur.local "cat /opt/heimdallur/heimdallur/config/devices.toml"
   ```

2. **Write** the updated config to a temp file and validate it:
   ```bash
   scp devices.toml pi@heimdallur.local:/tmp/devices-new.toml
   ssh pi@heimdallur.local "cd /opt/heimdallur && python scripts/validate-config.py /tmp/devices-new.toml"
   ```
   The validator exits 0 on success, 1 on any error.

3. **Apply** the config if validation passed:
   ```bash
   ssh pi@heimdallur.local "cp /tmp/devices-new.toml /opt/heimdallur/heimdallur/config/devices.toml && sudo systemctl restart heimdallur"
   ```

4. **Verify** the service restarted cleanly:
   ```bash
   ssh pi@heimdallur.local "systemctl is-active heimdallur && cat ~/.local/share/heimdallur/status.md"
   ```
   Wait ~35 seconds after restart for the first probe to complete and the status file to be refreshed.

---

## Triggering an Application Update

The application auto-updates hourly via a systemd timer. To trigger an immediate update:

```bash
ssh pi@heimdallur.local "sudo systemctl start heimdallur-update"
```

Check the result:

```bash
ssh pi@heimdallur.local "journalctl -u heimdallur-update -n 20 --no-pager"
```

To check the currently running version:

```bash
ssh pi@heimdallur.local "cd /opt/heimdallur && git log -1 --oneline"
```

---

## Service Management

```bash
# Restart the monitor
ssh pi@heimdallur.local "sudo systemctl restart heimdallur"

# Stop / start
ssh pi@heimdallur.local "sudo systemctl stop heimdallur"
ssh pi@heimdallur.local "sudo systemctl start heimdallur"

# View all Heimdallur-related units
ssh pi@heimdallur.local "systemctl list-units 'heimdallur*'"
```

---

## File Reference

| Path | Purpose |
|------|---------|
| `/opt/heimdallur/` | Application root |
| `/opt/heimdallur/heimdallur/config/devices.toml` | Network topology — edit to add/remove devices and groups |
| `~/.local/share/heimdallur/status.md` | Live markdown snapshot, rewritten every 30s |
| `~/.local/share/heimdallur/events.db` | SQLite probe history (30-day retention) |
| `/opt/heimdallur/scripts/validate-config.py` | Config validator — run before applying changes |
| `/opt/heimdallur/scripts/auto-update.sh` | Update script run by the systemd timer |
