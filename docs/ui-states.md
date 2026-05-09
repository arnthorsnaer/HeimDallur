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

HEIMDALLUR  20:21:06

INTERNET  ✓ Online  38ms
  IP 3/3  ·  DNS 3/3  ·  HTTP 3/3
  ↓ 429 Mbps  ·  ping 21 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  2ms
  ✓ Online  2ms  WiFi Garage
  ✓ Online  4ms  WiFi Living Room
  ✓ Online  5ms  WiFi Upper Floor
  ✓ Online  1ms  WiFi Basement
  LAN  LAN Studio
  LAN  LAN Home Theater
  LAN  LAN Router

All monitored devices OK

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 20:21:06 UTC  |  **Interval:** 30s

## Summary

✅ All systems healthy — 33 / 33 devices online

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 20 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 25 ms |
| Google (8.8.8.8) | ✅ healthy | 28 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 17 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 5 ms |
| Google (google.com) | ✅ Online | 15 ms |
| Quad9 (quad9.net) | ✅ Online | 5 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 62 ms | 69 ms |
| Google | ✅ Online | 63 ms | 82 ms |
| Microsoft | ✅ Online | 53 ms | 69 ms |

**Speed test:** ↓ 373 Mbps  |  ping 19 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 18%  |  **Memory:** 43%  |  **Uptime:** 3d

### Groups

#### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 2 ms  |  **Clients:** 5

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 1 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 5 ms |

#### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 5 ms  |  **Clients:** 8

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 2 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 5 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 3 ms |

#### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 1 ms  |  **Clients:** 6

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 1 ms |

#### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 1 ms  |  **Clients:** 11

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 2 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 2 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 1 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 3 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 2 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 5 ms |

#### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 3 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 1 ms |

#### LAN Home Theater

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 1 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 1 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 5 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 2 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 5 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 3 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 3 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 1 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 1 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 2 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 2 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 1 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 3 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 2 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 5 ms |

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

HEIMDALLUR  20:21:06

INTERNET  ✗ Offline  138ms
  IP 0/3  ·  DNS 3/3  ·  HTTP 3/3
  ↓ 270 Mbps  ·  ping 18 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  1ms
  ✓ Online  5ms  WiFi Garage
  ✓ Online  4ms  WiFi Living Room
  ✓ Online  3ms  WiFi Upper Floor
  ✓ Online  4ms  WiFi Basement
  LAN  LAN Studio
  LAN  LAN Home Theater
  LAN  LAN Router

PROBLEMS
  ✗  Internet offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 20:21:06 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- Internet offline — full network unreachable

---

## Internet

**Status:** ❌ UNREACHABLE  |  **Latency (ONT):** 171 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ❌ unreachable | 143 ms |
| Google (8.8.8.8) | ❌ unreachable | 155 ms |
| Quad9 (9.9.9.9) | ❌ unreachable | 164 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 65 ms |
| Google (google.com) | ✅ Online | 121 ms |
| Quad9 (quad9.net) | ✅ Online | 121 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 285 ms | 351 ms |
| Google | ✅ Online | 274 ms | 309 ms |
| Microsoft | ✅ Online | 312 ms | 372 ms |

**Speed test:** ↓ 430 Mbps  |  ping 31 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 3 ms
**CPU:** 7%  |  **Memory:** 29%  |  **Uptime:** 3d

### Groups

#### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 2 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 5 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 2 ms |

#### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 2 ms  |  **Clients:** 9

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 1 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 4 ms |

#### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 5 ms  |  **Clients:** 5

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 4 ms |

#### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 2 ms  |  **Clients:** 9

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 3 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 4 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 3 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 5 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 4 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 5 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 2 ms |

#### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 1 ms |

#### LAN Home Theater

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 4 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 5 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 2 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 1 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 4 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 1 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 4 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 3 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 4 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 3 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 5 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 4 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 5 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 2 ms |

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

HEIMDALLUR  20:21:06

INTERNET  ✗ Offline  timeout
  IP 0/3  ·  DNS 0/3  ·  HTTP 0/3
  ↓ 222 Mbps  ·  ping 21 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  2ms
  ✓ Online  4ms  WiFi Garage
  ✓ Online  2ms  WiFi Living Room
  ✓ Online  4ms  WiFi Upper Floor
  ✓ Online  4ms  WiFi Basement
  LAN  LAN Studio
  LAN  LAN Home Theater
  LAN  LAN Router

PROBLEMS
  ✗  Internet offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 20:21:06 UTC  |  **Interval:** 30s

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

**Speed test:** ↓ 261 Mbps  |  ping 24 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 17%  |  **Memory:** 37%  |  **Uptime:** 3d

### Groups

#### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 1 ms  |  **Clients:** 3

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 1 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 2 ms |

#### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 2 ms  |  **Clients:** 8

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 3 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 5 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 4 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 5 ms |

#### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 5 ms  |  **Clients:** 5

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 4 ms |

#### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 3 ms  |  **Clients:** 9

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 4 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 4 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 1 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 5 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 3 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 3 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 1 ms |

#### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 5 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 4 ms |

#### LAN Home Theater

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 4 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 1 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 2 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 4 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 5 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 5 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 4 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 4 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 4 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 1 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 5 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 3 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 3 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 1 ms |

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

HEIMDALLUR  20:21:06

INTERNET  ✓ Online  22ms
  IP 3/3  ·  DNS 3/3  ·  HTTP 3/3
  ↓ 269 Mbps  ·  ping 12 ms  (0s ago)

HOME NETWORK
  ROUTER  ✗ Offline  timeout
  ✓ Online  4ms  WiFi Garage
  ✓ Online  4ms  WiFi Living Room
  ✓ Online  2ms  WiFi Upper Floor
  ✓ Online  5ms  WiFi Basement
  LAN  LAN Studio
  LAN  LAN Home Theater
  LAN  LAN Router

PROBLEMS
  ✗  Router offline — home network affected

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 20:21:06 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- Router offline — home network affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 38 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 20 ms |
| Google (8.8.8.8) | ✅ healthy | 29 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 22 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 8 ms |
| Google (google.com) | ✅ Online | 12 ms |
| Quad9 (quad9.net) | ✅ Online | 5 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 53 ms | 73 ms |
| Google | ✅ Online | 58 ms | 69 ms |
| Microsoft | ✅ Online | 43 ms | 54 ms |

**Speed test:** ↓ 363 Mbps  |  ping 25 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ❌ UNREACHABLE  |  **Latency:** —
**CPU:** 13%  |  **Memory:** 51%  |  **Uptime:** 3d

### Groups

#### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 2 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 1 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 4 ms |

#### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 3 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 1 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 3 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 2 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 1 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 4 ms |

#### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 3 ms  |  **Clients:** 4

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 1 ms |

#### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 3 ms  |  **Clients:** 10

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 1 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 3 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 3 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 1 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 3 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 2 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 4 ms |

#### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 4 ms |

#### LAN Home Theater

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 5 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 1 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 4 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 1 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 1 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 4 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 4 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 5 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 1 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 3 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 3 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 1 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 3 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 2 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 4 ms |

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

HEIMDALLUR  20:21:06

INTERNET  ✓ Online  40ms
  IP 3/3  ·  DNS 3/3  ·  HTTP 3/3
  ↓ 273 Mbps  ·  ping 34 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  3ms
  ✓ Online  3ms  WiFi Garage
  ✓ Online  4ms  WiFi Living Room
  ✓ Online  3ms  WiFi Upper Floor
  ✗ Offline  timeout  WiFi Basement
  LAN  LAN Studio
  LAN  LAN Home Theater
  LAN  LAN Router

PROBLEMS
  ✗  WiFi Basement WiFi access point offline — 9 devices affected

33 monitored  ·  32 OK  ·  1 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 20:21:06 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 32 / 33 devices online

- WiFi Basement WiFi access point offline — 9 devices affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 29 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 24 ms |
| Google (8.8.8.8) | ✅ healthy | 23 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 22 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 2 ms |
| Google (google.com) | ✅ Online | 14 ms |
| Quad9 (quad9.net) | ✅ Online | 6 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 72 ms | 78 ms |
| Google | ✅ Online | 70 ms | 94 ms |
| Microsoft | ✅ Online | 53 ms | 59 ms |

**Speed test:** ↓ 258 Mbps  |  ping 31 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 4%  |  **Memory:** 52%  |  **Uptime:** 3d

### Groups

#### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 4 ms  |  **Clients:** 3

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 2 ms |

#### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 1 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 2 ms |

#### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 6

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 4 ms |

#### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ❌ —  |  **Clients:** 8

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ❓ unknown (gateway down) | — |
| Svefnherbergi ljós 2 | `192.168.1.141` | ❓ unknown (gateway down) | — |
| Baðherbergi ljós | `192.168.1.142` | ❓ unknown (gateway down) | — |
| Kvikmyndaherbergi | `192.168.1.143` | ❓ unknown (gateway down) | — |
| Þvottavél blásari | `192.168.1.144` | ❓ unknown (gateway down) | — |
| Þvottaherbergi ljós | `192.168.1.145` | ❓ unknown (gateway down) | — |
| Geymsla ljós | `192.168.1.146` | ❓ unknown (gateway down) | — |
| Garðljós | `192.168.1.214` | ❓ unknown (gateway down) | — |
| Garðtenglar | `192.168.1.148` | ❓ unknown (gateway down) | — |

#### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 3 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 2 ms |

#### LAN Home Theater

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 2 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 2 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 2 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 3 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 2 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 2 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ❓ unknown | — |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ❓ unknown | — |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ❓ unknown | — |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ❓ unknown | — |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ❓ unknown | — |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ❓ unknown | — |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ❓ unknown | — |
| Garðljós | `192.168.1.214` | WiFi Basement | ❓ unknown | — |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ❓ unknown | — |

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

HEIMDALLUR  20:21:06

INTERNET  ✓ Online  40ms
  IP 3/3  ·  DNS 3/3  ·  HTTP 3/3
  ↓ 300 Mbps  ·  ping 21 ms  (0s ago)

HOME NETWORK
  ROUTER  ✓ Online  1ms
  ✗ Offline  106ms  WiFi Garage
  ✓ Online  2ms  WiFi Living Room
  ✓ Online  3ms  WiFi Upper Floor
  ✗ Offline  timeout  WiFi Basement
  LAN  LAN Studio
  LAN  LAN Home Theater
  LAN  LAN Router

PROBLEMS
  ✗  WiFi Garage WiFi access point offline — 4 devices affected
  ✗  WiFi Basement WiFi access point offline — 9 devices affected
  ✗  Kaffivél unreachable

33 monitored  ·  30 OK  ·  3 down
```

</details>

<details>
<summary>Markdown report (<code>--mode report</code>)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 20:21:06 UTC  |  **Interval:** 30s

## Summary

⚠️  2 issue(s) detected — 31 / 33 devices online

- WiFi Garage WiFi access point offline — 4 devices affected
- WiFi Basement WiFi access point offline — 9 devices affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 38 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 22 ms |
| Google (8.8.8.8) | ✅ healthy | 27 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 15 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ Online | 15 ms |
| Google (google.com) | ✅ Online | 15 ms |
| Quad9 (quad9.net) | ✅ Online | 6 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ Online | 54 ms | 59 ms |
| Google | ✅ Online | 61 ms | 79 ms |
| Microsoft | ✅ Online | 64 ms | 87 ms |

**Speed test:** ↓ 382 Mbps  |  ping 30 ms  *(0s ago)*

---

## Home Network

### Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 8%  |  **Memory:** 36%  |  **Uptime:** 3d

### Groups

#### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ❌ 130 ms  |  **Clients:** 2

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ❓ unknown (gateway down) | — |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ❓ unknown (gateway down) | — |
| Bílskúrshurð | `192.168.1.102` | ❓ unknown (gateway down) | — |
| Bílskúrsljós | `192.168.1.103` | ❓ unknown (gateway down) | — |

#### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 4 ms  |  **Clients:** 8

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 3 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 2 ms |

#### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 5

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 3 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 4 ms |

#### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ❌ —  |  **Clients:** 9

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ❓ unknown (gateway down) | — |
| Svefnherbergi ljós 2 | `192.168.1.141` | ❓ unknown (gateway down) | — |
| Baðherbergi ljós | `192.168.1.142` | ❓ unknown (gateway down) | — |
| Kvikmyndaherbergi | `192.168.1.143` | ❓ unknown (gateway down) | — |
| Þvottavél blásari | `192.168.1.144` | ❓ unknown (gateway down) | — |
| Þvottaherbergi ljós | `192.168.1.145` | ❓ unknown (gateway down) | — |
| Geymsla ljós | `192.168.1.146` | ❓ unknown (gateway down) | — |
| Garðljós | `192.168.1.214` | ❓ unknown (gateway down) | — |
| Garðtenglar | `192.168.1.148` | ❓ unknown (gateway down) | — |

#### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 5 ms |

#### LAN Home Theater

**Devices:** 0 / 0 online

#### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 1 ms |


---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ❓ unknown | — |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ❓ unknown | — |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ❓ unknown | — |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ❓ unknown | — |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 2 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 5 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 1 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ❓ unknown | — |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ❓ unknown | — |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ❓ unknown | — |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ❓ unknown | — |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ❓ unknown | — |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ❓ unknown | — |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ❓ unknown | — |
| Garðljós | `192.168.1.214` | WiFi Basement | ❓ unknown | — |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ❓ unknown | — |

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
