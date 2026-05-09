## Screenshots

<details>
<summary>All healthy</summary>

![All healthy](docs/screenshots/01-status-healthy.png)

</details>

<details>
<summary>Internet degraded</summary>

![Internet degraded](docs/screenshots/02-status-internet-degraded.png)

</details>

<details>
<summary>Internet offline</summary>

![Internet offline](docs/screenshots/03-status-internet-offline.png)

</details>

<details>
<summary>Router offline</summary>

![Router offline](docs/screenshots/04-status-router-offline.png)

</details>

<details>
<summary>AP offline (Basement)</summary>

![AP offline (Basement)](docs/screenshots/05-status-gateway-offline.png)

</details>

<details>
<summary>Multiple issues</summary>

![Multiple issues](docs/screenshots/06-status-multiple-issues.png)

</details>

---

## Status Output (`--mode status`)

<details>
<summary>All healthy</summary>

```text

HEIMDALLUR  11:54:19

                              
   INTERNET         ✓  54ms   
   ROUTER           ✓  2ms    
                              
Access Points
  ✓  2ms  WiFi Garage
  ✓  2ms  WiFi Living Room
  ✓  1ms  WiFi Upper Floor
  ✓  3ms  WiFi Basement

All monitored devices OK

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Internet degraded</summary>

```text

HEIMDALLUR  11:54:19

                               
   INTERNET         ✗  113ms   
   ROUTER           ✓  2ms     
                               
Access Points
  ✓  3ms  WiFi Garage
  ✓  2ms  WiFi Living Room
  ✓  3ms  WiFi Upper Floor
  ✓  5ms  WiFi Basement

PROBLEMS
  ✗  WAN offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Internet offline</summary>

```text

HEIMDALLUR  11:54:19

                                 
   INTERNET         ✗  timeout   
   ROUTER           ✓  1ms       
                                 
Access Points
  ✓  1ms  WiFi Garage
  ✓  3ms  WiFi Living Room
  ✓  3ms  WiFi Upper Floor
  ✓  5ms  WiFi Basement

PROBLEMS
  ✗  WAN offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Router offline</summary>

```text

HEIMDALLUR  11:54:19

                                 
   INTERNET         ✓  42ms      
   ROUTER           ✗  timeout   
                                 
Access Points
  ✓  3ms  WiFi Garage
  ✓  5ms  WiFi Living Room
  ✓  3ms  WiFi Upper Floor
  ✓  4ms  WiFi Basement

PROBLEMS
  ✗  Router offline — home network affected

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>AP offline (Basement)</summary>

```text

HEIMDALLUR  11:54:19

                              
   INTERNET         ✓  51ms   
   ROUTER           ✓  2ms    
                              
Access Points
  ✓  3ms  WiFi Garage
  ✓  3ms  WiFi Living Room
  ✓  4ms  WiFi Upper Floor
  ✗  timeout  WiFi Basement

PROBLEMS
  ✗  WiFi Basement WiFi access point offline — 9 devices affected

33 monitored  ·  32 OK  ·  1 down
```

</details>

<details>
<summary>Multiple issues</summary>

```text

HEIMDALLUR  11:54:19

                              
   INTERNET         ✓  28ms   
   ROUTER           ✓  2ms    
                              
Access Points
  ✗  102ms  WiFi Garage
  ✓  2ms  WiFi Living Room
  ✓  2ms  WiFi Upper Floor
  ✗  timeout  WiFi Basement

PROBLEMS
  ✗  WiFi Garage WiFi access point offline — 4 devices affected
  ✗  WiFi Basement WiFi access point offline — 9 devices affected
  ✗  Kaffivél unreachable

33 monitored  ·  30 OK  ·  3 down
```

</details>

---

## Markdown Report (`--mode report`)

<details>
<summary>All healthy</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:54:19 UTC  |  **Interval:** 30s

## Summary

✅ All systems healthy — 33 / 33 devices online

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 46 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 18 ms |
| Google (8.8.8.8) | ✅ healthy | 25 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 24 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 17 ms |
| Google (google.com) | ✅ ok | 14 ms |
| Quad9 (quad9.net) | ✅ ok | 8 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 55 ms | 62 ms |
| Google | ✅ ok | 71 ms | 82 ms |
| Microsoft | ✅ ok | 41 ms | 61 ms |

**Speed test:** ↓ 431 Mbps  |  ping 18 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 3 ms
**CPU:** 7%  |  **Memory:** 37%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 2 ms  |  **Clients:** 2

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 3 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 3 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 3 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 1 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 3 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 7

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 2 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 2 ms  |  **Clients:** 11

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 1 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 2 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 2 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 4 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 3 ms |

### LAN Home Theater

**Devices:** 0 / 0 online

### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 2 ms |

---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 3 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 1 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 3 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 3 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 2 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 1 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 2 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 2 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 4 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Internet degraded</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:54:19 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- WAN offline — full network unreachable

---

## Internet

**Status:** ❌ UNREACHABLE  |  **Latency (ONT):** 158 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ❌ unreachable | 164 ms |
| Google (8.8.8.8) | ❌ unreachable | 180 ms |
| Quad9 (9.9.9.9) | ❌ unreachable | 151 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 133 ms |
| Google (google.com) | ✅ ok | 137 ms |
| Quad9 (quad9.net) | ✅ ok | 120 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 335 ms | 390 ms |
| Google | ✅ ok | 347 ms | 378 ms |
| Microsoft | ✅ ok | 336 ms | 375 ms |

**Speed test:** ↓ 304 Mbps  |  ping 24 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 6%  |  **Memory:** 30%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 4 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 3 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 1 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 2 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 2 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 5 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 5 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 5 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 7

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 2 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 4 ms  |  **Clients:** 8

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 2 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 4 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 5 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 2 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 5 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 5 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 2 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 4 ms |

### LAN Home Theater

**Devices:** 0 / 0 online

### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 5 ms |

---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 1 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 2 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 5 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 5 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 4 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 5 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 2 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 4 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 5 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 5 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 5 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 2 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Internet offline</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:54:19 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- WAN offline — full network unreachable

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
| Cloudflare (cloudflare.com) | ❌ fail | — |
| Google (google.com) | ❌ fail | — |
| Quad9 (quad9.net) | ❌ fail | — |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ❌ fail | — | — |
| Google | ❌ fail | — | — |
| Microsoft | ❌ fail | — | — |

**Speed test:** ↓ 293 Mbps  |  ping 29 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 9%  |  **Memory:** 49%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 5 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 5 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 4 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 4 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 5 ms  |  **Clients:** 8

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 3 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 2 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 4 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 3 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 5 ms  |  **Clients:** 5

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 3 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 3 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 1 ms  |  **Clients:** 11

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 1 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 1 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 5 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 4 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 2 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 1 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 2 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 3 ms |

### LAN Home Theater

**Devices:** 0 / 0 online

### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 2 ms |

---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 5 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 4 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 2 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 4 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 3 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 3 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 2 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 1 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 1 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 5 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 4 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 2 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 1 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 2 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Router offline</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:54:19 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- Router offline — home network affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 50 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 16 ms |
| Google (8.8.8.8) | ✅ healthy | 22 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 11 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 6 ms |
| Google (google.com) | ✅ ok | 3 ms |
| Quad9 (quad9.net) | ✅ ok | 13 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 76 ms | 88 ms |
| Google | ✅ ok | 66 ms | 87 ms |
| Microsoft | ✅ ok | 53 ms | 66 ms |

**Speed test:** ↓ 421 Mbps  |  ping 22 ms  *(0s ago)*

---

## Router

**Status:** ❌ UNREACHABLE  |  **Latency:** —
**CPU:** 21%  |  **Memory:** 28%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 4 ms  |  **Clients:** 2

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 1 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 1 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 1 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 3 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 1 ms  |  **Clients:** 7

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 2 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 1 ms  |  **Clients:** 5

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 3 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 1 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 5 ms  |  **Clients:** 11

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 3 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 4 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 2 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 4 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 1 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 4 ms |

### LAN Home Theater

**Devices:** 0 / 0 online

### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 3 ms |

---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 1 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 1 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 1 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 3 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 2 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 4 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 3 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 3 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 4 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 2 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 4 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 1 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>AP offline (Basement)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:54:19 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 32 / 33 devices online

- WiFi Basement WiFi access point offline — 9 devices affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 43 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 28 ms |
| Google (8.8.8.8) | ✅ healthy | 22 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 18 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 5 ms |
| Google (google.com) | ✅ ok | 11 ms |
| Quad9 (quad9.net) | ✅ ok | 11 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 66 ms | 82 ms |
| Google | ✅ ok | 51 ms | 67 ms |
| Microsoft | ✅ ok | 60 ms | 76 ms |

**Speed test:** ↓ 423 Mbps  |  ping 32 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 20%  |  **Memory:** 46%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 4 ms  |  **Clients:** 3

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 5 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 3 ms  |  **Clients:** 9

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 1 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 3 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 1 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 5 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 1 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 4 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 1 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 4

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 5 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 4 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ❌ —  |  **Clients:** 10

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

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 3 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 2 ms |

### LAN Home Theater

**Devices:** 0 / 0 online

### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 2 ms |

---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 5 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 1 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 5 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 1 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 4 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 1 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 5 ms |
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

<details>
<summary>Multiple issues</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:54:19 UTC  |  **Interval:** 30s

## Summary

⚠️  2 issue(s) detected — 31 / 33 devices online

- WiFi Basement WiFi access point offline — 9 devices affected
- Kaffivél unreachable

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 41 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 13 ms |
| Google (8.8.8.8) | ✅ healthy | 27 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 20 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 16 ms |
| Google (google.com) | ✅ ok | 8 ms |
| Quad9 (quad9.net) | ✅ ok | 3 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 47 ms | 67 ms |
| Google | ✅ ok | 42 ms | 66 ms |
| Microsoft | ✅ ok | 62 ms | 85 ms |

**Speed test:** ↓ 216 Mbps  |  ping 19 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 10%  |  **Memory:** 29%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ⚠️ 78 ms  |  **Clients:** 3

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 2 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 3 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 4 ms  |  **Clients:** 10

**Devices:** 10 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 5 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 4 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 4 ms |
| Kaffivél | `192.168.1.219` | ❌ unreachable | — |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 1 ms  |  **Clients:** 7

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 1 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ❌ —  |  **Clients:** 11

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

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 5 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 4 ms |

### LAN Home Theater

**Devices:** 0 / 0 online

### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 4 ms |

---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 2 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 3 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 5 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 4 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 4 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ❌ unreachable | — |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 5 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 4 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 4 ms |
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
