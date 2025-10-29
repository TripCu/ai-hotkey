---
title: "Networking – Router Routing Tables and Forwarding Methods"
tags: ["networking", "routing", "static", "dynamic", "directly-connected", "default-route", "module8"]
source: ["ITN_Module_8.pptx.pdf"]
created: "2025-10-29"
summary: "Explains how routers use routing tables to make forwarding decisions and the difference between directly connected, remote, and default routes."
---

> [!Abstract]
> Routers forward packets based on the best match found in the routing table. Routes may be directly connected, statically configured, or learned dynamically.

## Key Ideas
- Routers maintain routing tables for path selection and forwarding.  
- Table entries contain **destination network**, **next hop**, and **outgoing interface**.  
- Three route types:
  1. **Directly Connected:** Automatically added when an interface is up.  
  2. **Remote:** Learned via static configuration or dynamic routing protocols.  
  3. **Default:** Used when no specific match exists (the “last resort”).

## Route Learning
| Method | Description | Example |
|:------|:-------------|:-------------|
| **Static** | Manually configured; doesn’t change automatically. | `ip route 10.0.0.0 255.255.255.0 192.168.1.1` |
| **Dynamic** | Learned via routing protocols (OSPF, EIGRP, etc.). | Automatically adapts to topology changes. |

### Routing Table Symbols
| Symbol | Meaning |
|:-------|:---------|
| L | Local address |
| C | Connected network |
| S | Static route |
| D | EIGRP learned |
| O | OSPF learned |
| S\* | Static default route |

### Decision Process
1. Router examines destination IP.  
2. Finds the **longest prefix match** in the table.  
3. Forwards packet out the matching interface or next hop.  

## Common Mistakes
- Assuming routers forward broadcasts (they don’t).  
- Forgetting static routes need manual updates.  

## Quick Checks
- What is the difference between directly connected and remote routes?  
- What does “longest prefix match” mean?  

## Connections
- Builds on: [[Host Routing Decisions and Default Gateways]]  
- Related: [[Network Layer Characteristics]]  
- Leads to: [[Routing Protocols Overview and Practice]]