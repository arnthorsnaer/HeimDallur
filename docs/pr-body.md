<details>
<summary><strong>Screenshots</strong></summary>

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

</details>

---

<details>
<summary><strong>Status Output (<code>--mode status</code>)</strong></summary>

<details>
<summary>All healthy</summary>

```text

HEIMDALLUR  11:55:47

                              
   INTERNET         ✓  48ms   
   ROUTER           ✓  1ms    
                              
Access Points
  ✓  3ms  WiFi Garage
  ✓  3ms  WiFi Living Room
  ✓  3ms  WiFi Upper Floor
  ✓  1ms  WiFi Basement

All monitored devices OK

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Internet degraded</summary>

```text

HEIMDALLUR  11:55:47

                               
   INTERNET         ✗  123ms   
   ROUTER           ✓  1ms     
                               
Access Points
  ✓  4ms  WiFi Garage
  ✓  3ms  WiFi Living Room
  ✓  2ms  WiFi Upper Floor
  ✓  3ms  WiFi Basement

PROBLEMS
  ✗  WAN offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Internet offline</summary>

```text

HEIMDALLUR  11:55:47

                                 
   INTERNET         ✗  timeout   
   ROUTER           ✓  3ms       
                                 
Access Points
  ✓  3ms  WiFi Garage
  ✓  1ms  WiFi Living Room
  ✓  4ms  WiFi Upper Floor
  ✓  3ms  WiFi Basement

PROBLEMS
  ✗  WAN offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Router offline</summary>

```text

HEIMDALLUR  11:55:48

                                 
   INTERNET         ✓  46ms      
   ROUTER           ✗  timeout   
                                 
Access Points
  ✓  2ms  WiFi Garage
  ✓  3ms  WiFi Living Room
  ✓  2ms  WiFi Upper Floor
  ✓  2ms  WiFi Basement

PROBLEMS
  ✗  Router offline — home network affected

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>AP offline (Basement)</summary>

```text

HEIMDALLUR  11:55:48

                              
   INTERNET         ✓  19ms   
   ROUTER           ✓  1ms    
                              
Access Points
  ✓  1ms  WiFi Garage
  ✓  5ms  WiFi Living Room
  ✓  1ms  WiFi Upper Floor
  ✗  timeout  WiFi Basement

PROBLEMS
  ✗  WiFi Basement WiFi access point offline — 9 devices affected

33 monitored  ·  32 OK  ·  1 down
```

</details>

<details>
<summary>Multiple issues</summary>

```text

HEIMDALLUR  11:55:48

                              
   INTERNET         ✓  24ms   
   ROUTER           ✓  2ms    
                              
Access Points
  ~  75ms  WiFi Garage
  ✓  1ms  WiFi Living Room
  ✓  3ms  WiFi Upper Floor
  ✗  timeout  WiFi Basement

PROBLEMS
  ✗  WiFi Basement WiFi access point offline — 9 devices affected

33 monitored  ·  32 OK  ·  1 down
```

</details>

</details>

---

<details>
<summary><strong>Markdown Report (<code>--mode report</code>)</strong></summary>

<details>
<summary>All healthy</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:55:47 UTC  |  **Interval:** 30s

## Summary

✅ All systems healthy — 33 / 33 devices online

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 25 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 26 ms |
| Google (8.8.8.8) | ✅ healthy | 20 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 21 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 14 ms |
| Google (google.com) | ✅ ok | 12 ms |
| Quad9 (quad9.net) | ✅ ok | 15 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 59 ms | 76 ms |
| Google | ✅ ok | 49 ms | 59 ms |
| Microsoft | ✅ ok | 53 ms | 65 ms |

**Speed test:** ↓ 217 Mbps  |  ping 15 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 17%  |  **Memory:** 40%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 4 ms  |  **Clients:** 3

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 4 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 2 ms  |  **Clients:** 9

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 2 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 1 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 1 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 5 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 1 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 4

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 1 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 3 ms  |  **Clients:** 9

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 1 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 3 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 3 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 4 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 1 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 1 ms |

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
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 4 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 1 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 5 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 1 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 1 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 3 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 1 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 3 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 3 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 4 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 1 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Internet degraded</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:55:47 UTC  |  **Interval:** 30s

## Summary

✅ All systems healthy — 33 / 33 devices online

---

## Internet

**Status:** ⚠️ DEGRADED  |  **Latency (ONT):** 93 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ❌ unreachable | 152 ms |
| Google (8.8.8.8) | ❌ unreachable | 136 ms |
| Quad9 (9.9.9.9) | ❌ unreachable | 112 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 69 ms |
| Google (google.com) | ✅ ok | 93 ms |
| Quad9 (quad9.net) | ✅ ok | 130 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 341 ms | 412 ms |
| Google | ✅ ok | 262 ms | 335 ms |
| Microsoft | ✅ ok | 248 ms | 326 ms |

**Speed test:** ↓ 237 Mbps  |  ping 21 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 21%  |  **Memory:** 28%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 2 ms  |  **Clients:** 2

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 4 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 5 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 2 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 5 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 5 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 5 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 5 ms  |  **Clients:** 7

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 5 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 2 ms  |  **Clients:** 10

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 2 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 3 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 5 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 4 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 1 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 4 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 5 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 3 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 2 ms |

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
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 5 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 5 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 5 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 5 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 2 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 5 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 2 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 3 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 5 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 1 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 4 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 5 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 3 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Internet offline</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:55:47 UTC  |  **Interval:** 30s

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

**Speed test:** ↓ 286 Mbps  |  ping 23 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 3 ms
**CPU:** 21%  |  **Memory:** 49%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 3 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 2 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 2 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 2 ms  |  **Clients:** 7

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 5 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 5 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 2 ms  |  **Clients:** 4

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 3 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 2 ms  |  **Clients:** 9

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 2 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 4 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 5 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 5 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 1 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 2 ms |
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
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 2 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 2 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 5 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 5 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 2 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 3 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 2 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 2 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 4 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 5 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 5 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 4 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 1 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Router offline</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:55:48 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- Router offline — home network affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 28 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 15 ms |
| Google (8.8.8.8) | ✅ healthy | 29 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 18 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 13 ms |
| Google (google.com) | ✅ ok | 5 ms |
| Quad9 (quad9.net) | ✅ ok | 10 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 70 ms | 91 ms |
| Google | ✅ ok | 70 ms | 81 ms |
| Microsoft | ✅ ok | 41 ms | 57 ms |

**Speed test:** ↓ 462 Mbps  |  ping 23 ms  *(0s ago)*

---

## Router

**Status:** ❌ UNREACHABLE  |  **Latency:** —
**CPU:** 9%  |  **Memory:** 48%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 4 ms  |  **Clients:** 2

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 5 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 4 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 5 ms  |  **Clients:** 9

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 1 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 3 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 4 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 4 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 3 ms  |  **Clients:** 4

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 1 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 4 ms  |  **Clients:** 9

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 4 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 4 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 5 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 5 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 5 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 2 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 3 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 5 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 1 ms |

### LAN Home Theater

**Devices:** 0 / 0 online

### LAN Router

**Devices:** 1 / 1 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Unifi Controller | `192.168.1.151` | ✅ healthy | 1 ms |

---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 5 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 4 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 2 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 1 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 4 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 4 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 4 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 1 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 1 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 4 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 4 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 5 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 5 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 5 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 2 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 3 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 5 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>AP offline (Basement)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 11:55:48 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 32 / 33 devices online

- WiFi Basement WiFi access point offline — 9 devices affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 34 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 13 ms |
| Google (8.8.8.8) | ✅ healthy | 34 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 20 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 6 ms |
| Google (google.com) | ✅ ok | 4 ms |
| Quad9 (quad9.net) | ✅ ok | 2 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 60 ms | 67 ms |
| Google | ✅ ok | 62 ms | 74 ms |
| Microsoft | ✅ ok | 65 ms | 88 ms |

**Speed test:** ↓ 349 Mbps  |  ping 30 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 5%  |  **Memory:** 46%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 2 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 1 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 4 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 3 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 2 ms  |  **Clients:** 9

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 2 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 3 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 5 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 5 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 5 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 1 ms  |  **Clients:** 5

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 2 ms |

### WiFi Basement  |  2.4GHz  ch 6

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

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 1 ms |
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
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 1 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 3 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 5 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 1 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 5 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 1 ms |
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

**Probed:** 2026-05-09 11:55:48 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 32 / 33 devices online

- WiFi Basement WiFi access point offline — 9 devices affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 39 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 16 ms |
| Google (8.8.8.8) | ✅ healthy | 18 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 25 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 9 ms |
| Google (google.com) | ✅ ok | 12 ms |
| Quad9 (quad9.net) | ✅ ok | 14 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 58 ms | 74 ms |
| Google | ✅ ok | 74 ms | 80 ms |
| Microsoft | ✅ ok | 54 ms | 74 ms |

**Speed test:** ↓ 320 Mbps  |  ping 16 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 15%  |  **Memory:** 34%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ⚠️ 93 ms  |  **Clients:** 3

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 1 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 4 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 2 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 4 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 3 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 1 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 2 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 7

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 1 ms |

### WiFi Basement  |  2.4GHz  ch 6

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

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 1 ms |
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
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 1 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 2 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 1 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 2 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 1 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 4 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 3 ms |
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

</details>
