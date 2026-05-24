# UI States

All snapshots are generated from mock data via `scripts/capture_all.py` and committed to `docs/snapshots/`. The Web UI, status output, and markdown report samples for each base network state are injected automatically by the same script.

---

## Status screen

The main view, always visible. Three panels stack vertically: Internet, Home Network, and a collapsible status banner at the top. Each panel shows a bold online/offline indicator with a live duration ticker and a rolling-average summary line. Click a panel or press the shortcut key to expand it for sparklines and detail.

---

### All healthy

Everything reachable — internet, router, access points, and all devices. The status banner is collapsed since there is nothing to report.

| ![Status — all healthy](snapshots/01-status-healthy.png) |
|:---:|

<!-- generated:all_healthy:start -->
<details>
<summary>Web UI (<code>make web</code>)</summary>

| ![Web UI — All healthy](snapshots/web-01-status-healthy.png) |
|:---:|

</details>

<details>
<summary>Status output (<code>--mode status</code>)</summary>

```text

HEIMDALLUR  2026-05-24 16:00:32 UTC

INTERNET  ✓ Online  32ms  excellent
  IP 3/3  ·  DNS 3/3  ·  HTTP 3/3
  All paths healthy
  ↓ 237 Mbps  ·  ping 18 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  2ms
  ✓ Online  2ms  WiFi Garage
  ✓ Online  2ms  WiFi Main Floor
  ✓ Online  1ms  WiFi Upper Floor
  ✓ Online  2ms  WiFi Lower Floor
  LAN  LAN Office
  LAN  LAN Media
  LAN  LAN Router

All monitored devices OK

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-24 16:00:32 UTC  |  **Interval:** 30s

## Summary

✅ All systems healthy — 33 / 33 devices online

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 22 ms avg (excellent)  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 13 ms |
| Google (8.8.8.8) | ✅ healthy | 24 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 20 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 9 ms |
| Google (google.com) | ✅ Online | 14 ms |
| Quad9 (quad9.net) | ✅ Online | 17 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 71 ms | 87 ms |
| Google | ✅ Online | 66 ms | 88 ms |
| Microsoft | ✅ Online | 47 ms | 63 ms |

**Speed test:** ↓ 419 Mbps  |  ping 14 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 7%  |  **Memory:** 45%  |  **Uptime:** 3d

### Groups

#### WiFi Garage

**Gateway `192.0.2.25`:** ✅ 5 ms

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Garage Door Controller | `192.0.2.100` | ✅ healthy | 2 ms |
| Garage Light | `192.0.2.101` | ✅ healthy | 3 ms |
| Utility Meter | `192.0.2.102` | ✅ healthy | 4 ms |
| Workbench Plug | `192.0.2.103` | ✅ healthy | 3 ms |

#### WiFi Main Floor

**Gateway `192.0.2.21`:** ✅ 1 ms

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Entry Light | `192.0.2.110` | ✅ healthy | 3 ms |
| Kitchen Ceiling Light | `192.0.2.111` | ✅ healthy | 4 ms |
| Kitchen Counter Light | `192.0.2.112` | ✅ healthy | 3 ms |
| Dining Room Light | `192.0.2.113` | ✅ healthy | 3 ms |
| Living Room Light 1 | `192.0.2.114` | ✅ healthy | 3 ms |
| Living Room Light 2 | `192.0.2.115` | ✅ healthy | 3 ms |
| Living Room Light 3 | `192.0.2.116` | ✅ healthy | 4 ms |
| Hallway Light | `192.0.2.117` | ✅ healthy | 1 ms |
| Porch Light | `192.0.2.118` | ✅ healthy | 5 ms |
| Plant Light | `192.0.2.119` | ✅ healthy | 4 ms |
| Coffee Maker | `192.0.2.120` | ✅ healthy | 1 ms |

#### WiFi Upper Floor

**Gateway `192.0.2.22`:** ✅ 3 ms

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bathroom LED | `192.0.2.130` | ✅ healthy | 4 ms |
| Thermostat | `192.0.2.131` | ✅ healthy | 1 ms |

#### WiFi Lower Floor

**Gateway `192.0.2.23`:** ✅ 3 ms

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bedroom Light 1 | `192.0.2.140` | ✅ healthy | 2 ms |
| Bedroom Light 2 | `192.0.2.141` | ✅ healthy | 1 ms |
| Lower Bathroom Light | `192.0.2.142` | ✅ healthy | 3 ms |
| Media Room Light | `192.0.2.143` | ✅ healthy | 3 ms |
| Laundry Fan | `192.0.2.144` | ✅ healthy | 3 ms |
| Laundry Room Light | `192.0.2.145` | ✅ healthy | 3 ms |
| Storage Room Light | `192.0.2.146` | ✅ healthy | 3 ms |
| Patio Light | `192.0.2.147` | ✅ healthy | 2 ms |
| Patio Outlet | `192.0.2.148` | ✅ healthy | 2 ms |

#### LAN Office

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Office Workstation | `192.0.2.132` | ✅ healthy | 1 ms |
| Automation Server | `192.0.2.64` | ✅ healthy | 2 ms |

#### LAN Media

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Network Controller | `192.0.2.151` | ✅ healthy | 2 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Garage Door Controller | `192.0.2.100` | WiFi Garage | ✅ healthy | 2 ms |
| Garage Light | `192.0.2.101` | WiFi Garage | ✅ healthy | 3 ms |
| Utility Meter | `192.0.2.102` | WiFi Garage | ✅ healthy | 4 ms |
| Workbench Plug | `192.0.2.103` | WiFi Garage | ✅ healthy | 3 ms |
| Entry Light | `192.0.2.110` | WiFi Main Floor | ✅ healthy | 3 ms |
| Kitchen Ceiling Light | `192.0.2.111` | WiFi Main Floor | ✅ healthy | 4 ms |
| Kitchen Counter Light | `192.0.2.112` | WiFi Main Floor | ✅ healthy | 3 ms |
| Dining Room Light | `192.0.2.113` | WiFi Main Floor | ✅ healthy | 3 ms |
| Living Room Light 1 | `192.0.2.114` | WiFi Main Floor | ✅ healthy | 3 ms |
| Living Room Light 2 | `192.0.2.115` | WiFi Main Floor | ✅ healthy | 3 ms |
| Living Room Light 3 | `192.0.2.116` | WiFi Main Floor | ✅ healthy | 4 ms |
| Hallway Light | `192.0.2.117` | WiFi Main Floor | ✅ healthy | 1 ms |
| Porch Light | `192.0.2.118` | WiFi Main Floor | ✅ healthy | 5 ms |
| Plant Light | `192.0.2.119` | WiFi Main Floor | ✅ healthy | 4 ms |
| Coffee Maker | `192.0.2.120` | WiFi Main Floor | ✅ healthy | 1 ms |
| Bathroom LED | `192.0.2.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Thermostat | `192.0.2.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Office Workstation | `192.0.2.132` | LAN Office | ✅ healthy | 1 ms |
| Automation Server | `192.0.2.64` | LAN Office | ✅ healthy | 2 ms |
| Network Controller | `192.0.2.151` | LAN Router | ✅ healthy | 2 ms |
| Bedroom Light 1 | `192.0.2.140` | WiFi Lower Floor | ✅ healthy | 2 ms |
| Bedroom Light 2 | `192.0.2.141` | WiFi Lower Floor | ✅ healthy | 1 ms |
| Lower Bathroom Light | `192.0.2.142` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Media Room Light | `192.0.2.143` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Laundry Fan | `192.0.2.144` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Laundry Room Light | `192.0.2.145` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Storage Room Light | `192.0.2.146` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Patio Light | `192.0.2.147` | WiFi Lower Floor | ✅ healthy | 2 ms |
| Patio Outlet | `192.0.2.148` | WiFi Lower Floor | ✅ healthy | 2 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>
<!-- generated:all_healthy:end -->

---

### Email notifications configured

Same healthy state, but with a Gmail incident-report address configured. The footer shows the admin email address in place of the default "no email configured" placeholder.

| ![Status — email notifications configured](snapshots/01b-status-email-configured.png) |
|:---:|

---

### Internet degraded

Latency is elevated and packet loss is intermittent, but connectivity is maintained. The Internet panel changes colour and the rolling-average summary reflects the degraded quality; the status banner expands to name the fault.

| ![Status — internet degraded](snapshots/02-status-internet-degraded.png) |
|:---:|

<!-- generated:internet_degraded:start -->
<details>
<summary>Web UI (<code>make web</code>)</summary>

| ![Web UI — Internet degraded](snapshots/web-02-status-internet-degraded.png) |
|:---:|

</details>

<details>
<summary>Status output (<code>--mode status</code>)</summary>

```text

HEIMDALLUR  2026-05-24 16:00:32 UTC

INTERNET  ✗ Offline  170ms  degraded
  IP 0/3  ·  DNS 3/3  ·  HTTP 3/3
  No IP connectivity — likely ISP outage
  ↓ 382 Mbps  ·  ping 14 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  3ms
  ✓ Online  3ms  WiFi Garage
  ✓ Online  2ms  WiFi Main Floor
  ✓ Online  1ms  WiFi Upper Floor
  ✓ Online  3ms  WiFi Lower Floor
  LAN  LAN Office
  LAN  LAN Media
  LAN  LAN Router

PROBLEMS
  ✗  Internet offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-24 16:00:32 UTC  |  **Interval:** 30s

## Summary

✅ All systems healthy — 33 / 33 devices online

---

## Internet

**Status:** ⚠️ DEGRADED  |  **Latency (ONT):** 87 ms avg (elevated)  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ❌ unreachable | 160 ms |
| Google (8.8.8.8) | ❌ unreachable | 100 ms |
| Quad9 (9.9.9.9) | ❌ unreachable | 131 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 127 ms |
| Google (google.com) | ✅ Online | 70 ms |
| Quad9 (quad9.net) | ✅ Online | 134 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 291 ms | 362 ms |
| Google | ✅ Online | 347 ms | 384 ms |
| Microsoft | ✅ Online | 253 ms | 323 ms |

**Speed test:** ↓ 218 Mbps  |  ping 18 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 22%  |  **Memory:** 41%  |  **Uptime:** 3d

### Groups

#### WiFi Garage

**Gateway `192.0.2.25`:** ✅ 5 ms

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Garage Door Controller | `192.0.2.100` | ✅ healthy | 3 ms |
| Garage Light | `192.0.2.101` | ✅ healthy | 3 ms |
| Utility Meter | `192.0.2.102` | ✅ healthy | 1 ms |
| Workbench Plug | `192.0.2.103` | ✅ healthy | 1 ms |

#### WiFi Main Floor

**Gateway `192.0.2.21`:** ✅ 2 ms

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Entry Light | `192.0.2.110` | ✅ healthy | 4 ms |
| Kitchen Ceiling Light | `192.0.2.111` | ✅ healthy | 3 ms |
| Kitchen Counter Light | `192.0.2.112` | ✅ healthy | 3 ms |
| Dining Room Light | `192.0.2.113` | ✅ healthy | 5 ms |
| Living Room Light 1 | `192.0.2.114` | ✅ healthy | 5 ms |
| Living Room Light 2 | `192.0.2.115` | ✅ healthy | 3 ms |
| Living Room Light 3 | `192.0.2.116` | ✅ healthy | 2 ms |
| Hallway Light | `192.0.2.117` | ✅ healthy | 3 ms |
| Porch Light | `192.0.2.118` | ✅ healthy | 4 ms |
| Plant Light | `192.0.2.119` | ✅ healthy | 3 ms |
| Coffee Maker | `192.0.2.120` | ✅ healthy | 4 ms |

#### WiFi Upper Floor

**Gateway `192.0.2.22`:** ✅ 2 ms

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bathroom LED | `192.0.2.130` | ✅ healthy | 2 ms |
| Thermostat | `192.0.2.131` | ✅ healthy | 2 ms |

#### WiFi Lower Floor

**Gateway `192.0.2.23`:** ✅ 4 ms

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bedroom Light 1 | `192.0.2.140` | ✅ healthy | 3 ms |
| Bedroom Light 2 | `192.0.2.141` | ✅ healthy | 5 ms |
| Lower Bathroom Light | `192.0.2.142` | ✅ healthy | 2 ms |
| Media Room Light | `192.0.2.143` | ✅ healthy | 4 ms |
| Laundry Fan | `192.0.2.144` | ✅ healthy | 1 ms |
| Laundry Room Light | `192.0.2.145` | ✅ healthy | 2 ms |
| Storage Room Light | `192.0.2.146` | ✅ healthy | 4 ms |
| Patio Light | `192.0.2.147` | ✅ healthy | 3 ms |
| Patio Outlet | `192.0.2.148` | ✅ healthy | 4 ms |

#### LAN Office

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Office Workstation | `192.0.2.132` | ✅ healthy | 3 ms |
| Automation Server | `192.0.2.64` | ✅ healthy | 3 ms |

#### LAN Media

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Network Controller | `192.0.2.151` | ✅ healthy | 2 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Garage Door Controller | `192.0.2.100` | WiFi Garage | ✅ healthy | 3 ms |
| Garage Light | `192.0.2.101` | WiFi Garage | ✅ healthy | 3 ms |
| Utility Meter | `192.0.2.102` | WiFi Garage | ✅ healthy | 1 ms |
| Workbench Plug | `192.0.2.103` | WiFi Garage | ✅ healthy | 1 ms |
| Entry Light | `192.0.2.110` | WiFi Main Floor | ✅ healthy | 4 ms |
| Kitchen Ceiling Light | `192.0.2.111` | WiFi Main Floor | ✅ healthy | 3 ms |
| Kitchen Counter Light | `192.0.2.112` | WiFi Main Floor | ✅ healthy | 3 ms |
| Dining Room Light | `192.0.2.113` | WiFi Main Floor | ✅ healthy | 5 ms |
| Living Room Light 1 | `192.0.2.114` | WiFi Main Floor | ✅ healthy | 5 ms |
| Living Room Light 2 | `192.0.2.115` | WiFi Main Floor | ✅ healthy | 3 ms |
| Living Room Light 3 | `192.0.2.116` | WiFi Main Floor | ✅ healthy | 2 ms |
| Hallway Light | `192.0.2.117` | WiFi Main Floor | ✅ healthy | 3 ms |
| Porch Light | `192.0.2.118` | WiFi Main Floor | ✅ healthy | 4 ms |
| Plant Light | `192.0.2.119` | WiFi Main Floor | ✅ healthy | 3 ms |
| Coffee Maker | `192.0.2.120` | WiFi Main Floor | ✅ healthy | 4 ms |
| Bathroom LED | `192.0.2.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Thermostat | `192.0.2.131` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Office Workstation | `192.0.2.132` | LAN Office | ✅ healthy | 3 ms |
| Automation Server | `192.0.2.64` | LAN Office | ✅ healthy | 3 ms |
| Network Controller | `192.0.2.151` | LAN Router | ✅ healthy | 2 ms |
| Bedroom Light 1 | `192.0.2.140` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Bedroom Light 2 | `192.0.2.141` | WiFi Lower Floor | ✅ healthy | 5 ms |
| Lower Bathroom Light | `192.0.2.142` | WiFi Lower Floor | ✅ healthy | 2 ms |
| Media Room Light | `192.0.2.143` | WiFi Lower Floor | ✅ healthy | 4 ms |
| Laundry Fan | `192.0.2.144` | WiFi Lower Floor | ✅ healthy | 1 ms |
| Laundry Room Light | `192.0.2.145` | WiFi Lower Floor | ✅ healthy | 2 ms |
| Storage Room Light | `192.0.2.146` | WiFi Lower Floor | ✅ healthy | 4 ms |
| Patio Light | `192.0.2.147` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Patio Outlet | `192.0.2.148` | WiFi Lower Floor | ✅ healthy | 4 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>
<!-- generated:internet_degraded:end -->

---

### Internet offline

Complete loss of internet connectivity — IP, DNS, and HTTP checks all failing. The Internet panel shows `✗ OFFLINE` and the status banner surfaces the diagnosis.

| ![Status — internet offline](snapshots/03-status-internet-offline.png) |
|:---:|

<!-- generated:internet_offline:start -->
<details>
<summary>Web UI (<code>make web</code>)</summary>

| ![Web UI — Internet offline](snapshots/web-03-status-internet-offline.png) |
|:---:|

</details>

<details>
<summary>Status output (<code>--mode status</code>)</summary>

```text

HEIMDALLUR  2026-05-24 16:00:32 UTC

INTERNET  ✗ Offline  timeout
  IP 0/3  ·  DNS 0/3  ·  HTTP 0/3
  No IP connectivity — likely ISP outage
  ↓ 207 Mbps  ·  ping 31 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  1ms
  ✓ Online  3ms  WiFi Garage
  ✓ Online  4ms  WiFi Main Floor
  ✓ Online  3ms  WiFi Upper Floor
  ✓ Online  1ms  WiFi Lower Floor
  LAN  LAN Office
  LAN  LAN Media
  LAN  LAN Router

PROBLEMS
  ✗  Internet offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-24 16:00:32 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- Internet offline — full network unreachable

---

## Internet

**Status:** ❌ UNREACHABLE  |  **Latency (ONT):** — avg  |  **Loss:** 100%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ❌ unreachable | — |
| Google (8.8.8.8) | ❌ unreachable | — |
| Quad9 (9.9.9.9) | ❌ unreachable | — |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ❌ Offline | — |
| Google (google.com) | ❌ Offline | — |
| Quad9 (quad9.net) | ❌ Offline | — |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ❌ Offline | — | — |
| Google | ❌ Offline | — | — |
| Microsoft | ❌ Offline | — | — |

**Speed test:** ↓ 421 Mbps  |  ping 31 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 15%  |  **Memory:** 38%  |  **Uptime:** 3d

### Groups

#### WiFi Garage

**Gateway `192.0.2.25`:** ✅ 2 ms

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Garage Door Controller | `192.0.2.100` | ✅ healthy | 1 ms |
| Garage Light | `192.0.2.101` | ✅ healthy | 2 ms |
| Utility Meter | `192.0.2.102` | ✅ healthy | 3 ms |
| Workbench Plug | `192.0.2.103` | ✅ healthy | 1 ms |

#### WiFi Main Floor

**Gateway `192.0.2.21`:** ✅ 2 ms

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Entry Light | `192.0.2.110` | ✅ healthy | 5 ms |
| Kitchen Ceiling Light | `192.0.2.111` | ✅ healthy | 5 ms |
| Kitchen Counter Light | `192.0.2.112` | ✅ healthy | 2 ms |
| Dining Room Light | `192.0.2.113` | ✅ healthy | 3 ms |
| Living Room Light 1 | `192.0.2.114` | ✅ healthy | 1 ms |
| Living Room Light 2 | `192.0.2.115` | ✅ healthy | 3 ms |
| Living Room Light 3 | `192.0.2.116` | ✅ healthy | 4 ms |
| Hallway Light | `192.0.2.117` | ✅ healthy | 3 ms |
| Porch Light | `192.0.2.118` | ✅ healthy | 2 ms |
| Plant Light | `192.0.2.119` | ✅ healthy | 4 ms |
| Coffee Maker | `192.0.2.120` | ✅ healthy | 4 ms |

#### WiFi Upper Floor

**Gateway `192.0.2.22`:** ✅ 3 ms

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bathroom LED | `192.0.2.130` | ✅ healthy | 2 ms |
| Thermostat | `192.0.2.131` | ✅ healthy | 3 ms |

#### WiFi Lower Floor

**Gateway `192.0.2.23`:** ✅ 5 ms

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bedroom Light 1 | `192.0.2.140` | ✅ healthy | 3 ms |
| Bedroom Light 2 | `192.0.2.141` | ✅ healthy | 5 ms |
| Lower Bathroom Light | `192.0.2.142` | ✅ healthy | 2 ms |
| Media Room Light | `192.0.2.143` | ✅ healthy | 3 ms |
| Laundry Fan | `192.0.2.144` | ✅ healthy | 4 ms |
| Laundry Room Light | `192.0.2.145` | ✅ healthy | 4 ms |
| Storage Room Light | `192.0.2.146` | ✅ healthy | 4 ms |
| Patio Light | `192.0.2.147` | ✅ healthy | 2 ms |
| Patio Outlet | `192.0.2.148` | ✅ healthy | 3 ms |

#### LAN Office

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Office Workstation | `192.0.2.132` | ✅ healthy | 4 ms |
| Automation Server | `192.0.2.64` | ✅ healthy | 2 ms |

#### LAN Media

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Network Controller | `192.0.2.151` | ✅ healthy | 3 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Garage Door Controller | `192.0.2.100` | WiFi Garage | ✅ healthy | 1 ms |
| Garage Light | `192.0.2.101` | WiFi Garage | ✅ healthy | 2 ms |
| Utility Meter | `192.0.2.102` | WiFi Garage | ✅ healthy | 3 ms |
| Workbench Plug | `192.0.2.103` | WiFi Garage | ✅ healthy | 1 ms |
| Entry Light | `192.0.2.110` | WiFi Main Floor | ✅ healthy | 5 ms |
| Kitchen Ceiling Light | `192.0.2.111` | WiFi Main Floor | ✅ healthy | 5 ms |
| Kitchen Counter Light | `192.0.2.112` | WiFi Main Floor | ✅ healthy | 2 ms |
| Dining Room Light | `192.0.2.113` | WiFi Main Floor | ✅ healthy | 3 ms |
| Living Room Light 1 | `192.0.2.114` | WiFi Main Floor | ✅ healthy | 1 ms |
| Living Room Light 2 | `192.0.2.115` | WiFi Main Floor | ✅ healthy | 3 ms |
| Living Room Light 3 | `192.0.2.116` | WiFi Main Floor | ✅ healthy | 4 ms |
| Hallway Light | `192.0.2.117` | WiFi Main Floor | ✅ healthy | 3 ms |
| Porch Light | `192.0.2.118` | WiFi Main Floor | ✅ healthy | 2 ms |
| Plant Light | `192.0.2.119` | WiFi Main Floor | ✅ healthy | 4 ms |
| Coffee Maker | `192.0.2.120` | WiFi Main Floor | ✅ healthy | 4 ms |
| Bathroom LED | `192.0.2.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Thermostat | `192.0.2.131` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Office Workstation | `192.0.2.132` | LAN Office | ✅ healthy | 4 ms |
| Automation Server | `192.0.2.64` | LAN Office | ✅ healthy | 2 ms |
| Network Controller | `192.0.2.151` | LAN Router | ✅ healthy | 3 ms |
| Bedroom Light 1 | `192.0.2.140` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Bedroom Light 2 | `192.0.2.141` | WiFi Lower Floor | ✅ healthy | 5 ms |
| Lower Bathroom Light | `192.0.2.142` | WiFi Lower Floor | ✅ healthy | 2 ms |
| Media Room Light | `192.0.2.143` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Laundry Fan | `192.0.2.144` | WiFi Lower Floor | ✅ healthy | 4 ms |
| Laundry Room Light | `192.0.2.145` | WiFi Lower Floor | ✅ healthy | 4 ms |
| Storage Room Light | `192.0.2.146` | WiFi Lower Floor | ✅ healthy | 4 ms |
| Patio Light | `192.0.2.147` | WiFi Lower Floor | ✅ healthy | 2 ms |
| Patio Outlet | `192.0.2.148` | WiFi Lower Floor | ✅ healthy | 3 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>
<!-- generated:internet_offline:end -->

---

### Router offline

The router is unreachable. Because all downstream devices depend on the router, every access point and device is shown as `UNKNOWN` rather than individually failed — fault cascade keeps the signal-to-noise ratio low and points to the root cause.

| ![Status — router offline](snapshots/04-status-router-offline.png) |
|:---:|

<!-- generated:router_offline:start -->
<details>
<summary>Web UI (<code>make web</code>)</summary>

| ![Web UI — Router offline](snapshots/web-04-status-router-offline.png) |
|:---:|

</details>

<details>
<summary>Status output (<code>--mode status</code>)</summary>

```text

HEIMDALLUR  2026-05-24 16:00:32 UTC

INTERNET  ✓ Online  36ms  excellent
  IP 3/3  ·  DNS 3/3  ·  HTTP 3/3
  All paths healthy
  ↓ 406 Mbps  ·  ping 25 ms  (0s ago)

HOME NETWORK
  ROUTER  ✗ Offline  timeout
  ✓ Online  3ms  WiFi Garage
  ✓ Online  4ms  WiFi Main Floor
  ✓ Online  4ms  WiFi Upper Floor
  ✓ Online  4ms  WiFi Lower Floor
  LAN  LAN Office
  LAN  LAN Media
  LAN  LAN Router

PROBLEMS
  ✗  Router offline — home network affected

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-24 16:00:32 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- Router offline — home network affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 21 ms avg (excellent)  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 23 ms |
| Google (8.8.8.8) | ✅ healthy | 19 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 16 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 7 ms |
| Google (google.com) | ✅ Online | 16 ms |
| Quad9 (quad9.net) | ✅ Online | 16 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 43 ms | 68 ms |
| Google | ✅ Online | 56 ms | 70 ms |
| Microsoft | ✅ Online | 59 ms | 73 ms |

**Speed test:** ↓ 273 Mbps  |  ping 22 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ❌ UNREACHABLE  |  **Latency:** —
**CPU:** 10%  |  **Memory:** 43%  |  **Uptime:** 3d

### Groups

#### WiFi Garage

**Gateway `192.0.2.25`:** ✅ 1 ms

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Garage Door Controller | `192.0.2.100` | ✅ healthy | 4 ms |
| Garage Light | `192.0.2.101` | ✅ healthy | 2 ms |
| Utility Meter | `192.0.2.102` | ✅ healthy | 3 ms |
| Workbench Plug | `192.0.2.103` | ✅ healthy | 4 ms |

#### WiFi Main Floor

**Gateway `192.0.2.21`:** ✅ 4 ms

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Entry Light | `192.0.2.110` | ✅ healthy | 5 ms |
| Kitchen Ceiling Light | `192.0.2.111` | ✅ healthy | 5 ms |
| Kitchen Counter Light | `192.0.2.112` | ✅ healthy | 2 ms |
| Dining Room Light | `192.0.2.113` | ✅ healthy | 4 ms |
| Living Room Light 1 | `192.0.2.114` | ✅ healthy | 4 ms |
| Living Room Light 2 | `192.0.2.115` | ✅ healthy | 2 ms |
| Living Room Light 3 | `192.0.2.116` | ✅ healthy | 4 ms |
| Hallway Light | `192.0.2.117` | ✅ healthy | 2 ms |
| Porch Light | `192.0.2.118` | ✅ healthy | 3 ms |
| Plant Light | `192.0.2.119` | ✅ healthy | 3 ms |
| Coffee Maker | `192.0.2.120` | ✅ healthy | 2 ms |

#### WiFi Upper Floor

**Gateway `192.0.2.22`:** ✅ 1 ms

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bathroom LED | `192.0.2.130` | ✅ healthy | 3 ms |
| Thermostat | `192.0.2.131` | ✅ healthy | 1 ms |

#### WiFi Lower Floor

**Gateway `192.0.2.23`:** ✅ 2 ms

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bedroom Light 1 | `192.0.2.140` | ✅ healthy | 4 ms |
| Bedroom Light 2 | `192.0.2.141` | ✅ healthy | 4 ms |
| Lower Bathroom Light | `192.0.2.142` | ✅ healthy | 2 ms |
| Media Room Light | `192.0.2.143` | ✅ healthy | 3 ms |
| Laundry Fan | `192.0.2.144` | ✅ healthy | 5 ms |
| Laundry Room Light | `192.0.2.145` | ✅ healthy | 4 ms |
| Storage Room Light | `192.0.2.146` | ✅ healthy | 5 ms |
| Patio Light | `192.0.2.147` | ✅ healthy | 5 ms |
| Patio Outlet | `192.0.2.148` | ✅ healthy | 2 ms |

#### LAN Office

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Office Workstation | `192.0.2.132` | ✅ healthy | 5 ms |
| Automation Server | `192.0.2.64` | ✅ healthy | 5 ms |

#### LAN Media

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Network Controller | `192.0.2.151` | ✅ healthy | 3 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Garage Door Controller | `192.0.2.100` | WiFi Garage | ✅ healthy | 4 ms |
| Garage Light | `192.0.2.101` | WiFi Garage | ✅ healthy | 2 ms |
| Utility Meter | `192.0.2.102` | WiFi Garage | ✅ healthy | 3 ms |
| Workbench Plug | `192.0.2.103` | WiFi Garage | ✅ healthy | 4 ms |
| Entry Light | `192.0.2.110` | WiFi Main Floor | ✅ healthy | 5 ms |
| Kitchen Ceiling Light | `192.0.2.111` | WiFi Main Floor | ✅ healthy | 5 ms |
| Kitchen Counter Light | `192.0.2.112` | WiFi Main Floor | ✅ healthy | 2 ms |
| Dining Room Light | `192.0.2.113` | WiFi Main Floor | ✅ healthy | 4 ms |
| Living Room Light 1 | `192.0.2.114` | WiFi Main Floor | ✅ healthy | 4 ms |
| Living Room Light 2 | `192.0.2.115` | WiFi Main Floor | ✅ healthy | 2 ms |
| Living Room Light 3 | `192.0.2.116` | WiFi Main Floor | ✅ healthy | 4 ms |
| Hallway Light | `192.0.2.117` | WiFi Main Floor | ✅ healthy | 2 ms |
| Porch Light | `192.0.2.118` | WiFi Main Floor | ✅ healthy | 3 ms |
| Plant Light | `192.0.2.119` | WiFi Main Floor | ✅ healthy | 3 ms |
| Coffee Maker | `192.0.2.120` | WiFi Main Floor | ✅ healthy | 2 ms |
| Bathroom LED | `192.0.2.130` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Thermostat | `192.0.2.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Office Workstation | `192.0.2.132` | LAN Office | ✅ healthy | 5 ms |
| Automation Server | `192.0.2.64` | LAN Office | ✅ healthy | 5 ms |
| Network Controller | `192.0.2.151` | LAN Router | ✅ healthy | 3 ms |
| Bedroom Light 1 | `192.0.2.140` | WiFi Lower Floor | ✅ healthy | 4 ms |
| Bedroom Light 2 | `192.0.2.141` | WiFi Lower Floor | ✅ healthy | 4 ms |
| Lower Bathroom Light | `192.0.2.142` | WiFi Lower Floor | ✅ healthy | 2 ms |
| Media Room Light | `192.0.2.143` | WiFi Lower Floor | ✅ healthy | 3 ms |
| Laundry Fan | `192.0.2.144` | WiFi Lower Floor | ✅ healthy | 5 ms |
| Laundry Room Light | `192.0.2.145` | WiFi Lower Floor | ✅ healthy | 4 ms |
| Storage Room Light | `192.0.2.146` | WiFi Lower Floor | ✅ healthy | 5 ms |
| Patio Light | `192.0.2.147` | WiFi Lower Floor | ✅ healthy | 5 ms |
| Patio Outlet | `192.0.2.148` | WiFi Lower Floor | ✅ healthy | 2 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>
<!-- generated:router_offline:end -->

---

### AP offline

One access point (Basement) is down. Its nine downstream devices are suppressed to `UNKNOWN`, while all other groups remain unaffected. Only the root-cause AP is highlighted.

| ![Status — AP offline](snapshots/05-status-gateway-offline.png) |
|:---:|

<!-- generated:gateway_offline:start -->
<details>
<summary>Web UI (<code>make web</code>)</summary>

| ![Web UI — AP offline (Basement)](snapshots/web-05-status-gateway-offline.png) |
|:---:|

</details>

<details>
<summary>Status output (<code>--mode status</code>)</summary>

```text

HEIMDALLUR  2026-05-24 16:00:32 UTC

INTERNET  ✓ Online  33ms  excellent
  IP 3/3  ·  DNS 3/3  ·  HTTP 3/3
  All paths healthy
  ↓ 181 Mbps  ·  ping 18 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  1ms
  ✓ Online  2ms  WiFi Garage
  ✓ Online  2ms  WiFi Main Floor
  ✓ Online  2ms  WiFi Upper Floor
  ✗ Offline  timeout  WiFi Lower Floor
  LAN  LAN Office
  LAN  LAN Media
  LAN  LAN Router

PROBLEMS
  ✗  WiFi Lower Floor WiFi access point offline — 9 devices affected

33 monitored  ·  32 OK  ·  1 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-24 16:00:32 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 32 / 33 devices online

- WiFi Lower Floor WiFi access point offline — 9 devices affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 49 ms avg (excellent)  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 23 ms |
| Google (8.8.8.8) | ✅ healthy | 30 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 20 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 10 ms |
| Google (google.com) | ✅ Online | 5 ms |
| Quad9 (quad9.net) | ✅ Online | 4 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 48 ms | 62 ms |
| Google | ✅ Online | 77 ms | 97 ms |
| Microsoft | ✅ Online | 48 ms | 56 ms |

**Speed test:** ↓ 187 Mbps  |  ping 20 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 6%  |  **Memory:** 49%  |  **Uptime:** 3d

### Groups

#### WiFi Garage

**Gateway `192.0.2.25`:** ✅ 3 ms

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Garage Door Controller | `192.0.2.100` | ✅ healthy | 3 ms |
| Garage Light | `192.0.2.101` | ✅ healthy | 3 ms |
| Utility Meter | `192.0.2.102` | ✅ healthy | 1 ms |
| Workbench Plug | `192.0.2.103` | ✅ healthy | 1 ms |

#### WiFi Main Floor

**Gateway `192.0.2.21`:** ✅ 1 ms

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Entry Light | `192.0.2.110` | ✅ healthy | 3 ms |
| Kitchen Ceiling Light | `192.0.2.111` | ✅ healthy | 3 ms |
| Kitchen Counter Light | `192.0.2.112` | ✅ healthy | 2 ms |
| Dining Room Light | `192.0.2.113` | ✅ healthy | 2 ms |
| Living Room Light 1 | `192.0.2.114` | ✅ healthy | 3 ms |
| Living Room Light 2 | `192.0.2.115` | ✅ healthy | 1 ms |
| Living Room Light 3 | `192.0.2.116` | ✅ healthy | 1 ms |
| Hallway Light | `192.0.2.117` | ✅ healthy | 4 ms |
| Porch Light | `192.0.2.118` | ✅ healthy | 2 ms |
| Plant Light | `192.0.2.119` | ✅ healthy | 4 ms |
| Coffee Maker | `192.0.2.120` | ✅ healthy | 5 ms |

#### WiFi Upper Floor

**Gateway `192.0.2.22`:** ✅ 2 ms

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bathroom LED | `192.0.2.130` | ✅ healthy | 4 ms |
| Thermostat | `192.0.2.131` | ✅ healthy | 3 ms |

#### WiFi Lower Floor

**Gateway `192.0.2.23`:** ❌ —

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bedroom Light 1 | `192.0.2.140` | ❓ unknown (gateway down) | — |
| Bedroom Light 2 | `192.0.2.141` | ❓ unknown (gateway down) | — |
| Lower Bathroom Light | `192.0.2.142` | ❓ unknown (gateway down) | — |
| Media Room Light | `192.0.2.143` | ❓ unknown (gateway down) | — |
| Laundry Fan | `192.0.2.144` | ❓ unknown (gateway down) | — |
| Laundry Room Light | `192.0.2.145` | ❓ unknown (gateway down) | — |
| Storage Room Light | `192.0.2.146` | ❓ unknown (gateway down) | — |
| Patio Light | `192.0.2.147` | ❓ unknown (gateway down) | — |
| Patio Outlet | `192.0.2.148` | ❓ unknown (gateway down) | — |

#### LAN Office

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Office Workstation | `192.0.2.132` | ✅ healthy | 2 ms |
| Automation Server | `192.0.2.64` | ✅ healthy | 1 ms |

#### LAN Media

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Network Controller | `192.0.2.151` | ✅ healthy | 3 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Garage Door Controller | `192.0.2.100` | WiFi Garage | ✅ healthy | 3 ms |
| Garage Light | `192.0.2.101` | WiFi Garage | ✅ healthy | 3 ms |
| Utility Meter | `192.0.2.102` | WiFi Garage | ✅ healthy | 1 ms |
| Workbench Plug | `192.0.2.103` | WiFi Garage | ✅ healthy | 1 ms |
| Entry Light | `192.0.2.110` | WiFi Main Floor | ✅ healthy | 3 ms |
| Kitchen Ceiling Light | `192.0.2.111` | WiFi Main Floor | ✅ healthy | 3 ms |
| Kitchen Counter Light | `192.0.2.112` | WiFi Main Floor | ✅ healthy | 2 ms |
| Dining Room Light | `192.0.2.113` | WiFi Main Floor | ✅ healthy | 2 ms |
| Living Room Light 1 | `192.0.2.114` | WiFi Main Floor | ✅ healthy | 3 ms |
| Living Room Light 2 | `192.0.2.115` | WiFi Main Floor | ✅ healthy | 1 ms |
| Living Room Light 3 | `192.0.2.116` | WiFi Main Floor | ✅ healthy | 1 ms |
| Hallway Light | `192.0.2.117` | WiFi Main Floor | ✅ healthy | 4 ms |
| Porch Light | `192.0.2.118` | WiFi Main Floor | ✅ healthy | 2 ms |
| Plant Light | `192.0.2.119` | WiFi Main Floor | ✅ healthy | 4 ms |
| Coffee Maker | `192.0.2.120` | WiFi Main Floor | ✅ healthy | 5 ms |
| Bathroom LED | `192.0.2.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Thermostat | `192.0.2.131` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Office Workstation | `192.0.2.132` | LAN Office | ✅ healthy | 2 ms |
| Automation Server | `192.0.2.64` | LAN Office | ✅ healthy | 1 ms |
| Network Controller | `192.0.2.151` | LAN Router | ✅ healthy | 3 ms |
| Bedroom Light 1 | `192.0.2.140` | WiFi Lower Floor | ❓ unknown | — |
| Bedroom Light 2 | `192.0.2.141` | WiFi Lower Floor | ❓ unknown | — |
| Lower Bathroom Light | `192.0.2.142` | WiFi Lower Floor | ❓ unknown | — |
| Media Room Light | `192.0.2.143` | WiFi Lower Floor | ❓ unknown | — |
| Laundry Fan | `192.0.2.144` | WiFi Lower Floor | ❓ unknown | — |
| Laundry Room Light | `192.0.2.145` | WiFi Lower Floor | ❓ unknown | — |
| Storage Room Light | `192.0.2.146` | WiFi Lower Floor | ❓ unknown | — |
| Patio Light | `192.0.2.147` | WiFi Lower Floor | ❓ unknown | — |
| Patio Outlet | `192.0.2.148` | WiFi Lower Floor | ❓ unknown | — |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>
<!-- generated:gateway_offline:end -->

---

### Multiple issues

A compound failure: an access point is offline, internet connectivity is degraded, and one device is flapping intermittently. The status banner lists every active fault; each affected panel reflects its own state independently.

| ![Status — multiple issues](snapshots/06-status-multiple-issues.png) |
|:---:|

<!-- generated:multiple_issues:start -->
<details>
<summary>Web UI (<code>make web</code>)</summary>

| ![Web UI — Multiple issues](snapshots/web-06-status-multiple-issues.png) |
|:---:|

</details>

<details>
<summary>Status output (<code>--mode status</code>)</summary>

```text

HEIMDALLUR  2026-05-24 16:00:32 UTC

INTERNET  ✓ Online  36ms  excellent
  IP 3/3  ·  DNS 3/3  ·  HTTP 3/3
  All paths healthy
  ↓ 334 Mbps  ·  ping 20 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  1ms
  ✗ Offline  164ms  WiFi Garage
  ✓ Online  4ms  WiFi Main Floor
  ✓ Online  4ms  WiFi Upper Floor
  ✗ Offline  timeout  WiFi Lower Floor
  LAN  LAN Office
  LAN  LAN Media
  LAN  LAN Router

PROBLEMS
  ✗  WiFi Garage WiFi access point offline — 4 devices affected
  ✗  WiFi Lower Floor WiFi access point offline — 9 devices affected

33 monitored  ·  31 OK  ·  2 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-24 16:00:32 UTC  |  **Interval:** 30s

## Summary

⚠️  3 issue(s) detected — 30 / 33 devices online

- WiFi Garage WiFi access point offline — 4 devices affected
- WiFi Lower Floor WiFi access point offline — 9 devices affected
- Coffee Maker unreachable

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 32 ms avg (excellent)  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 26 ms |
| Google (8.8.8.8) | ✅ healthy | 16 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 21 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 16 ms |
| Google (google.com) | ✅ Online | 7 ms |
| Quad9 (quad9.net) | ✅ Online | 9 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 50 ms | 58 ms |
| Google | ✅ Online | 63 ms | 72 ms |
| Microsoft | ✅ Online | 54 ms | 77 ms |

**Speed test:** ↓ 404 Mbps  |  ping 16 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 14%  |  **Memory:** 41%  |  **Uptime:** 3d

### Groups

#### WiFi Garage

**Gateway `192.0.2.25`:** ❌ 108 ms

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Garage Door Controller | `192.0.2.100` | ❓ unknown (gateway down) | — |
| Garage Light | `192.0.2.101` | ❓ unknown (gateway down) | — |
| Utility Meter | `192.0.2.102` | ❓ unknown (gateway down) | — |
| Workbench Plug | `192.0.2.103` | ❓ unknown (gateway down) | — |

#### WiFi Main Floor

**Gateway `192.0.2.21`:** ✅ 3 ms

**Devices:** 10 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Entry Light | `192.0.2.110` | ✅ healthy | 1 ms |
| Kitchen Ceiling Light | `192.0.2.111` | ✅ healthy | 2 ms |
| Kitchen Counter Light | `192.0.2.112` | ✅ healthy | 3 ms |
| Dining Room Light | `192.0.2.113` | ✅ healthy | 5 ms |
| Living Room Light 1 | `192.0.2.114` | ✅ healthy | 4 ms |
| Living Room Light 2 | `192.0.2.115` | ✅ healthy | 4 ms |
| Living Room Light 3 | `192.0.2.116` | ✅ healthy | 1 ms |
| Hallway Light | `192.0.2.117` | ✅ healthy | 1 ms |
| Porch Light | `192.0.2.118` | ✅ healthy | 2 ms |
| Plant Light | `192.0.2.119` | ✅ healthy | 3 ms |
| Coffee Maker | `192.0.2.120` | ❌ unreachable | — |

#### WiFi Upper Floor

**Gateway `192.0.2.22`:** ✅ 5 ms

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bathroom LED | `192.0.2.130` | ✅ healthy | 2 ms |
| Thermostat | `192.0.2.131` | ✅ healthy | 4 ms |

#### WiFi Lower Floor

**Gateway `192.0.2.23`:** ❌ —

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Bedroom Light 1 | `192.0.2.140` | ❓ unknown (gateway down) | — |
| Bedroom Light 2 | `192.0.2.141` | ❓ unknown (gateway down) | — |
| Lower Bathroom Light | `192.0.2.142` | ❓ unknown (gateway down) | — |
| Media Room Light | `192.0.2.143` | ❓ unknown (gateway down) | — |
| Laundry Fan | `192.0.2.144` | ❓ unknown (gateway down) | — |
| Laundry Room Light | `192.0.2.145` | ❓ unknown (gateway down) | — |
| Storage Room Light | `192.0.2.146` | ❓ unknown (gateway down) | — |
| Patio Light | `192.0.2.147` | ❓ unknown (gateway down) | — |
| Patio Outlet | `192.0.2.148` | ❓ unknown (gateway down) | — |

#### LAN Office

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Office Workstation | `192.0.2.132` | ✅ healthy | 3 ms |
| Automation Server | `192.0.2.64` | ✅ healthy | 2 ms |

#### LAN Media

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Network Controller | `192.0.2.151` | ✅ healthy | 2 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Garage Door Controller | `192.0.2.100` | WiFi Garage | ❓ unknown | — |
| Garage Light | `192.0.2.101` | WiFi Garage | ❓ unknown | — |
| Utility Meter | `192.0.2.102` | WiFi Garage | ❓ unknown | — |
| Workbench Plug | `192.0.2.103` | WiFi Garage | ❓ unknown | — |
| Entry Light | `192.0.2.110` | WiFi Main Floor | ✅ healthy | 1 ms |
| Kitchen Ceiling Light | `192.0.2.111` | WiFi Main Floor | ✅ healthy | 2 ms |
| Kitchen Counter Light | `192.0.2.112` | WiFi Main Floor | ✅ healthy | 3 ms |
| Dining Room Light | `192.0.2.113` | WiFi Main Floor | ✅ healthy | 5 ms |
| Living Room Light 1 | `192.0.2.114` | WiFi Main Floor | ✅ healthy | 4 ms |
| Living Room Light 2 | `192.0.2.115` | WiFi Main Floor | ✅ healthy | 4 ms |
| Living Room Light 3 | `192.0.2.116` | WiFi Main Floor | ✅ healthy | 1 ms |
| Hallway Light | `192.0.2.117` | WiFi Main Floor | ✅ healthy | 1 ms |
| Porch Light | `192.0.2.118` | WiFi Main Floor | ✅ healthy | 2 ms |
| Plant Light | `192.0.2.119` | WiFi Main Floor | ✅ healthy | 3 ms |
| Coffee Maker | `192.0.2.120` | WiFi Main Floor | ❌ unreachable | — |
| Bathroom LED | `192.0.2.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Thermostat | `192.0.2.131` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Office Workstation | `192.0.2.132` | LAN Office | ✅ healthy | 3 ms |
| Automation Server | `192.0.2.64` | LAN Office | ✅ healthy | 2 ms |
| Network Controller | `192.0.2.151` | LAN Router | ✅ healthy | 2 ms |
| Bedroom Light 1 | `192.0.2.140` | WiFi Lower Floor | ❓ unknown | — |
| Bedroom Light 2 | `192.0.2.141` | WiFi Lower Floor | ❓ unknown | — |
| Lower Bathroom Light | `192.0.2.142` | WiFi Lower Floor | ❓ unknown | — |
| Media Room Light | `192.0.2.143` | WiFi Lower Floor | ❓ unknown | — |
| Laundry Fan | `192.0.2.144` | WiFi Lower Floor | ❓ unknown | — |
| Laundry Room Light | `192.0.2.145` | WiFi Lower Floor | ❓ unknown | — |
| Storage Room Light | `192.0.2.146` | WiFi Lower Floor | ❓ unknown | — |
| Patio Light | `192.0.2.147` | WiFi Lower Floor | ❓ unknown | — |
| Patio Outlet | `192.0.2.148` | WiFi Lower Floor | ❓ unknown | — |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>
<!-- generated:multiple_issues:end -->

---

### Status banner expanded

Press `s` to expand the top status banner into a full fault list. Each active problem is listed on its own line with a severity icon, giving a complete incident summary without leaving the main screen.

| ![Status banner expanded — multiple issues](snapshots/06b-status-panel-expanded.png) |
|:---:|

---

## Expanded panel views

Click any panel or press `i` (Internet) / `n` (Home Network) to expand it. The panel border subtitle changes from `▾` to `▴` and the detail view replaces the summary line.

---

### Internet panel — all healthy

The expanded Internet panel shows a latency sparkline, per-check results (IP reachability, DNS, HTTP) grouped by target, and the latest speed test reading with a historical average. Healthy targets are shown compactly; only degraded or failing targets get a detail row.

| ![Internet panel expanded — all healthy](snapshots/07-inet-panel-expanded.png) |
|:---:|

---

### Internet panel — partial failure

The same expanded view under a partial failure: one DNS resolver is failing while others pass, surfacing a plain-language diagnosis at the top of the panel ("All DNS failing — ISP resolver issue — try manual DNS").

| ![Internet panel expanded — partial failure](snapshots/07b-inet-panel-partial.png) |
|:---:|

---

### Internet panel — offline

The expanded Internet panel when internet connectivity is fully lost. All check rows show failing status and the diagnosis banner at the top states the conclusion plainly so no further interpretation is needed.

| ![Internet panel expanded — offline](snapshots/07c-inet-panel-offline.png) |
|:---:|

---

### Home network panel

The expanded Home Network panel shows router latency, memory usage, uptime, and per-group device counts. Each access point group lists its downstream devices with individual latency and online/offline status.

| ![Home network panel expanded](snapshots/08-net-panel-expanded.png) |
|:---:|

---

### Home network panel — AP offline

The same panel with an access point down. The affected group is highlighted; its downstream devices are listed as `UNKNOWN` rather than individually failed, confirming that the cascade suppression is working correctly.

| ![Home network panel expanded — AP offline](snapshots/08b-net-panel-gateway-offline.png) |
|:---:|

---

## Other screens

Press `h` for the history screen or `d` for the device list. Both screens are pushed onto the screen stack; press `q` or `Escape` to return to the status screen.

---

### History screen

24-hour uptime bars per network segment, updated on each probe cycle. Each bar represents a 30-minute window; colour indicates healthy / degraded / offline.

| ![History screen](snapshots/09-history-screen.png) |
|:---:|

---

### Devices screen

Full device inventory with live latency and status per device, grouped by access point. Devices whose gateway is offline are shown as `UNKNOWN` rather than individually failed, consistent with the cascade logic on the status screen.

| ![Devices screen](snapshots/10-devices-screen.png) |
|:---:|
