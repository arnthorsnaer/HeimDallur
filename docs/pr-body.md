<details>
<summary><strong>TUI Screenshots</strong></summary>

<details>
<summary>All healthy</summary>

![All healthy](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/01-status-healthy.png)

</details>

<details>
<summary>Internet degraded</summary>

![Internet degraded](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/02-status-internet-degraded.png)

</details>

<details>
<summary>Internet offline</summary>

![Internet offline](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/03-status-internet-offline.png)

</details>

<details>
<summary>Router offline</summary>

![Router offline](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/04-status-router-offline.png)

</details>

<details>
<summary>AP offline (Basement)</summary>

![AP offline (Basement)](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/05-status-gateway-offline.png)

</details>

<details>
<summary>Multiple issues</summary>

![Multiple issues](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/06-status-multiple-issues.png)

</details>

</details>

---

<details>
<summary><strong>Web UI Screenshots (<code>make web</code>)</strong></summary>

<details>
<summary>Web UI — all healthy</summary>

![Web UI — all healthy](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/web-01-status-healthy.png)

</details>

<details>
<summary>Web UI — internet degraded</summary>

![Web UI — internet degraded](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/web-02-status-internet-degraded.png)

</details>

<details>
<summary>Web UI — internet offline</summary>

![Web UI — internet offline](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/web-03-status-internet-offline.png)

</details>

<details>
<summary>Web UI — router offline</summary>

![Web UI — router offline](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/web-04-status-router-offline.png)

</details>

<details>
<summary>Web UI — AP offline (Basement)</summary>

![Web UI — AP offline (Basement)](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/web-05-status-gateway-offline.png)

</details>

<details>
<summary>Web UI — multiple issues</summary>

![Web UI — multiple issues](https://raw.githubusercontent.com/arnthorsnaer/HeimDallur/claude/implement-web-ui-docs-TEErC/docs/screenshots/web-06-status-multiple-issues.png)

</details>

</details>

---

<details>
<summary><strong>Status Output (<code>--mode status</code>)</strong></summary>

<details>
<summary>All healthy</summary>

```text

HEIMDALLUR  14:16:02

                              
   INTERNET         ✓  49ms   
   ROUTER           ✓  1ms    
                              
Access Points
  ✓  2ms  WiFi Garage
  ✓  3ms  WiFi Living Room
  ✓  1ms  WiFi Upper Floor
  ✓  2ms  WiFi Basement

All monitored devices OK

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Internet degraded</summary>

```text

HEIMDALLUR  14:16:02

                               
   INTERNET         ✗  164ms   
   ROUTER           ✓  1ms     
                               
Access Points
  ✓  1ms  WiFi Garage
  ✓  2ms  WiFi Living Room
  ✓  4ms  WiFi Upper Floor
  ✓  3ms  WiFi Basement

PROBLEMS
  ✗  WAN offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Internet offline</summary>

```text

HEIMDALLUR  14:16:02

                                 
   INTERNET         ✗  timeout   
   ROUTER           ✓  2ms       
                                 
Access Points
  ✓  3ms  WiFi Garage
  ✓  4ms  WiFi Living Room
  ✓  1ms  WiFi Upper Floor
  ✓  2ms  WiFi Basement

PROBLEMS
  ✗  WAN offline — full network unreachable

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>Router offline</summary>

```text

HEIMDALLUR  14:16:02

                                 
   INTERNET         ✓  26ms      
   ROUTER           ✗  timeout   
                                 
Access Points
  ✓  5ms  WiFi Garage
  ✓  3ms  WiFi Living Room
  ✓  2ms  WiFi Upper Floor
  ✓  5ms  WiFi Basement

PROBLEMS
  ✗  Router offline — home network affected

33 monitored  ·  33 OK  ·  0 down
```

</details>

<details>
<summary>AP offline (Basement)</summary>

```text

HEIMDALLUR  14:16:02

                              
   INTERNET         ✓  47ms   
   ROUTER           ✓  1ms    
                              
Access Points
  ✓  4ms  WiFi Garage
  ✓  3ms  WiFi Living Room
  ✓  2ms  WiFi Upper Floor
  ✗  timeout  WiFi Basement

PROBLEMS
  ✗  WiFi Basement WiFi access point offline — 9 devices affected

33 monitored  ·  32 OK  ·  1 down
```

</details>

<details>
<summary>Multiple issues</summary>

```text

HEIMDALLUR  14:16:02

                              
   INTERNET         ✓  38ms   
   ROUTER           ✓  1ms    
                              
Access Points
  ✗  110ms  WiFi Garage
  ✓  4ms  WiFi Living Room
  ✓  2ms  WiFi Upper Floor
  ✗  timeout  WiFi Basement

PROBLEMS
  ✗  WiFi Garage WiFi access point offline — 4 devices affected
  ✗  WiFi Basement WiFi access point offline — 9 devices affected

33 monitored  ·  31 OK  ·  2 down
```

</details>

</details>

---

<details>
<summary><strong>Markdown Report (<code>--mode report</code>)</strong></summary>

<details>
<summary>All healthy</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 14:16:02 UTC  |  **Interval:** 30s

## Summary

✅ All systems healthy — 33 / 33 devices online

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 54 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 24 ms |
| Google (8.8.8.8) | ✅ healthy | 22 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 19 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 14 ms |
| Google (google.com) | ✅ ok | 13 ms |
| Quad9 (quad9.net) | ✅ ok | 4 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 68 ms | 90 ms |
| Google | ✅ ok | 35 ms | 54 ms |
| Microsoft | ✅ ok | 60 ms | 67 ms |

**Speed test:** ↓ 191 Mbps  |  ping 28 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 3 ms
**CPU:** 7%  |  **Memory:** 42%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 4 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 1 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 4 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 4 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 3 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 5 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 5 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 1 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 4 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 4 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 3 ms  |  **Clients:** 4

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 2 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 4 ms  |  **Clients:** 11

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 4 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 3 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 1 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 4 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 3 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 3 ms |

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
| Unifi Controller | `192.168.1.151` | ✅ healthy | 5 ms |

---

## All Devices

| Device | IP | Group | Status | Latency |
|--------|----|-------|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 1 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 4 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 5 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 3 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 1 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 4 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 4 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 1 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 4 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 5 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 4 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 3 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 1 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 4 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 3 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 3 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Internet degraded</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 14:16:02 UTC  |  **Interval:** 30s

## Summary

✅ All systems healthy — 33 / 33 devices online

---

## Internet

**Status:** ⚠️ DEGRADED  |  **Latency (ONT):** 77 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ❌ unreachable | 115 ms |
| Google (8.8.8.8) | ❌ unreachable | 152 ms |
| Quad9 (9.9.9.9) | ❌ unreachable | 181 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 74 ms |
| Google (google.com) | ✅ ok | 120 ms |
| Quad9 (quad9.net) | ✅ ok | 88 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 356 ms | 390 ms |
| Google | ✅ ok | 335 ms | 372 ms |
| Microsoft | ✅ ok | 263 ms | 336 ms |

**Speed test:** ↓ 407 Mbps  |  ping 11 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 1 ms
**CPU:** 12%  |  **Memory:** 29%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 4 ms  |  **Clients:** 3

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 2 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 1 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 5 ms  |  **Clients:** 9

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 5 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 5 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 4 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 7

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 1 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 2 ms  |  **Clients:** 10

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 5 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 3 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 2 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 1 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 2 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 4 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 3 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 3 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 1 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 5 ms |

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
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 1 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 5 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 5 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 4 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 1 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 1 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 5 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 2 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 5 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 3 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 2 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 1 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 4 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 2 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 4 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 3 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 3 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Internet offline</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 14:16:02 UTC  |  **Interval:** 30s

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

**Speed test:** ↓ 220 Mbps  |  ping 18 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 10%  |  **Memory:** 52%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 2 ms  |  **Clients:** 3

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 2 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 5 ms  |  **Clients:** 9

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 2 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 2 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 4 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 2 ms  |  **Clients:** 7

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 4 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 1 ms  |  **Clients:** 8

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 4 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 2 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 1 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 3 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 2 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 3 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 1 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 5 ms |

### LAN Studio

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 3 ms |
| Home Assistant | `192.168.1.64` | ✅ healthy | 1 ms |

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
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 4 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 2 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 3 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 2 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 3 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 4 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 3 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 1 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 4 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 4 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 2 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 1 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 3 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 2 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 3 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 1 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 5 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>Router offline</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 14:16:02 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 33 / 33 devices online

- Router offline — home network affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 38 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 25 ms |
| Google (8.8.8.8) | ✅ healthy | 16 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 21 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 8 ms |
| Google (google.com) | ✅ ok | 2 ms |
| Quad9 (quad9.net) | ✅ ok | 4 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 53 ms | 64 ms |
| Google | ✅ ok | 63 ms | 73 ms |
| Microsoft | ✅ ok | 56 ms | 70 ms |

**Speed test:** ↓ 215 Mbps  |  ping 20 ms  *(0s ago)*

---

## Router

**Status:** ❌ UNREACHABLE  |  **Latency:** —
**CPU:** 5%  |  **Memory:** 34%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 1 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 2 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 3 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 1 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 2 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 5 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 3 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 2 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 1 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 1 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 4 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 4 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 2 ms  |  **Clients:** 4

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 3 ms |

### WiFi Basement  |  2.4GHz  ch 6

**Gateway `192.168.1.45`:** ✅ 3 ms  |  **Clients:** 11

**Devices:** 9 / 9 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Svefnherbergi ljós 1 | `192.168.1.140` | ✅ healthy | 5 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | ✅ healthy | 1 ms |
| Þvottavél blásari | `192.168.1.144` | ✅ healthy | 2 ms |
| Þvottaherbergi ljós | `192.168.1.145` | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | ✅ healthy | 2 ms |
| Garðljós | `192.168.1.214` | ✅ healthy | 1 ms |
| Garðtenglar | `192.168.1.148` | ✅ healthy | 5 ms |

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
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ✅ healthy | 2 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ✅ healthy | 3 ms |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ✅ healthy | 1 ms |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 2 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 4 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 3 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 1 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 1 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 4 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 4 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 1 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 4 ms |
| Unifi Controller | `192.168.1.151` | LAN Router | ✅ healthy | 3 ms |
| Svefnherbergi ljós 1 | `192.168.1.140` | WiFi Basement | ✅ healthy | 5 ms |
| Svefnherbergi ljós 2 | `192.168.1.141` | WiFi Basement | ✅ healthy | 2 ms |
| Baðherbergi ljós | `192.168.1.142` | WiFi Basement | ✅ healthy | 1 ms |
| Kvikmyndaherbergi | `192.168.1.143` | WiFi Basement | ✅ healthy | 1 ms |
| Þvottavél blásari | `192.168.1.144` | WiFi Basement | ✅ healthy | 2 ms |
| Þvottaherbergi ljós | `192.168.1.145` | WiFi Basement | ✅ healthy | 3 ms |
| Geymsla ljós | `192.168.1.146` | WiFi Basement | ✅ healthy | 2 ms |
| Garðljós | `192.168.1.214` | WiFi Basement | ✅ healthy | 1 ms |
| Garðtenglar | `192.168.1.148` | WiFi Basement | ✅ healthy | 5 ms |

---

*Generated by Heimdallur · DB: `~/.local/share/heimdallur/events.db`*

</details>

<details>
<summary>AP offline (Basement)</summary>

# Heimdallur Network Status

**Probed:** 2026-05-09 14:16:02 UTC  |  **Interval:** 30s

## Summary

⚠️  1 issue(s) detected — 32 / 33 devices online

- WiFi Basement WiFi access point offline — 9 devices affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 34 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 24 ms |
| Google (8.8.8.8) | ✅ healthy | 16 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 14 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 9 ms |
| Google (google.com) | ✅ ok | 6 ms |
| Quad9 (quad9.net) | ✅ ok | 15 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 59 ms | 73 ms |
| Google | ✅ ok | 53 ms | 68 ms |
| Microsoft | ✅ ok | 68 ms | 81 ms |

**Speed test:** ↓ 423 Mbps  |  ping 34 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 11%  |  **Memory:** 30%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ✅ 3 ms  |  **Clients:** 5

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ✅ healthy | 3 ms |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ✅ healthy | 4 ms |
| Bílskúrshurð | `192.168.1.102` | ✅ healthy | 2 ms |
| Bílskúrsljós | `192.168.1.103` | ✅ healthy | 4 ms |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 4 ms  |  **Clients:** 7

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 2 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 5 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 5 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 3 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 7

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 4 ms |
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
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ✅ healthy | 4 ms |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 1 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 2 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 5 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 4 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 4 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 3 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 3 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 2 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 1 ms |
| Home Assistant | `192.168.1.64` | LAN Studio | ✅ healthy | 3 ms |
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

**Probed:** 2026-05-09 14:16:02 UTC  |  **Interval:** 30s

## Summary

⚠️  2 issue(s) detected — 31 / 33 devices online

- WiFi Garage WiFi access point offline — 4 devices affected
- WiFi Basement WiFi access point offline — 9 devices affected

---

## Internet

**Status:** ✅ HEALTHY  |  **Latency (ONT):** 30 ms avg  |  **Loss:** 0%

### IP Reachability

| Target | Status | Latency |
|--------|--------|---------|
| Cloudflare (1.1.1.1) | ✅ healthy | 18 ms |
| Google (8.8.8.8) | ✅ healthy | 18 ms |
| Quad9 (9.9.9.9) | ✅ healthy | 24 ms |

### DNS

| Resolver | Status | Lookup |
|----------|--------|--------|
| Cloudflare (cloudflare.com) | ✅ ok | 17 ms |
| Google (google.com) | ✅ ok | 9 ms |
| Quad9 (quad9.net) | ✅ ok | 4 ms |

### HTTP

| Endpoint | Status | TTFB | Total |
|----------|--------|------|-------|
| Cloudflare | ✅ ok | 59 ms | 80 ms |
| Google | ✅ ok | 68 ms | 74 ms |
| Microsoft | ✅ ok | 68 ms | 76 ms |

**Speed test:** ↓ 326 Mbps  |  ping 28 ms  *(0s ago)*

---

## Router

**Status:** ✅ HEALTHY  |  **Latency:** 2 ms
**CPU:** 11%  |  **Memory:** 50%  |  **Uptime:** 3d

---

## Groups

### WiFi Garage  |  2.4GHz  ch 11

**Gateway `192.168.1.95`:** ❌ 129 ms  |  **Clients:** 4

**Devices:** 4 / 4 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | ❓ unknown (gateway down) | — |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | ❓ unknown (gateway down) | — |
| Bílskúrshurð | `192.168.1.102` | ❓ unknown (gateway down) | — |
| Bílskúrsljós | `192.168.1.103` | ❓ unknown (gateway down) | — |

### WiFi Living Room  |  5GHz  ch 36

**Gateway `192.168.1.44`:** ✅ 1 ms  |  **Clients:** 10

**Devices:** 11 / 11 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Inngangur ljós | `192.168.1.110` | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | ✅ healthy | 5 ms |

### WiFi Upper Floor  |  5GHz  ch 44

**Gateway `192.168.1.43`:** ✅ 4 ms  |  **Clients:** 5

**Devices:** 2 / 2 online

| Device | IP | Status | Latency |
|--------|----|--------|---------|
| Baðherbergi LED | `192.168.1.130` | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | ✅ healthy | 3 ms |

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
| Stúdíóbúnaður | `192.168.1.132` | ✅ healthy | 1 ms |
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
| Rafmagnsmaelir 1-fasa | `192.168.1.100` | WiFi Garage | ❓ unknown | — |
| Rafmagnsmaelir 3-fasa | `192.168.1.101` | WiFi Garage | ❓ unknown | — |
| Bílskúrshurð | `192.168.1.102` | WiFi Garage | ❓ unknown | — |
| Bílskúrsljós | `192.168.1.103` | WiFi Garage | ❓ unknown | — |
| Inngangur ljós | `192.168.1.110` | WiFi Living Room | ✅ healthy | 4 ms |
| Gestasnyrtingur ljós | `192.168.1.111` | WiFi Living Room | ✅ healthy | 3 ms |
| Eldhús efri ljós | `192.168.1.112` | WiFi Living Room | ✅ healthy | 5 ms |
| Eldhús neðri ljós | `192.168.1.113` | WiFi Living Room | ✅ healthy | 1 ms |
| Stofa ljós 1 | `192.168.1.114` | WiFi Living Room | ✅ healthy | 2 ms |
| Stofa ljós 2 | `192.168.1.115` | WiFi Living Room | ✅ healthy | 4 ms |
| Stofa ljós 3 | `192.168.1.116` | WiFi Living Room | ✅ healthy | 3 ms |
| Kjallaragang ljós | `192.168.1.117` | WiFi Living Room | ✅ healthy | 2 ms |
| Útiljós framhlið | `192.168.1.118` | WiFi Living Room | ✅ healthy | 2 ms |
| Plöntuljós | `192.168.1.119` | WiFi Living Room | ✅ healthy | 2 ms |
| Kaffivél | `192.168.1.219` | WiFi Living Room | ✅ healthy | 5 ms |
| Baðherbergi LED | `192.168.1.130` | WiFi Upper Floor | ✅ healthy | 4 ms |
| Gólfahitun | `192.168.1.131` | WiFi Upper Floor | ✅ healthy | 3 ms |
| Stúdíóbúnaður | `192.168.1.132` | LAN Studio | ✅ healthy | 1 ms |
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

</details>
