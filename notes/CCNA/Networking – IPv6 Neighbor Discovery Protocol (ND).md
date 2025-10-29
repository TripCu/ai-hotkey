---
title: "Networking – IPv6 Neighbor Discovery Protocol (ND)"
tags: ["networking", "ipv6", "neighbor-discovery", "icmpv6", "ns", "na", "rs", "ra", "module9"]
source: ["ITN_Module_9.pptx.pdf"]
created: "2025-10-29"
summary: "Explains how IPv6 uses ICMPv6 Neighbor Discovery (ND) to replace ARP, manage address resolution, and enable router discovery."
---

> [!Abstract]
> IPv6 replaces ARP with the **Neighbor Discovery Protocol (ND)**, using ICMPv6 messages to resolve MAC addresses, discover routers, and maintain efficient network operation.

## Key Ideas
- ND provides:
  - **Address resolution** (replaces ARP).  
  - **Router discovery** for default gateways.  
  - **Redirection** for optimal path selection.  
- Uses ICMPv6 message types instead of broadcasts, relying on **multicast**.

## ND Message Types
| Message | Purpose |
|:---------|:---------|
| **Neighbor Solicitation (NS)** | Requests MAC of a known IPv6 address. |
| **Neighbor Advertisement (NA)** | Reply providing the MAC address. |
| **Router Solicitation (RS)** | Host requests router info. |
| **Router Advertisement (RA)** | Router provides prefix and gateway info. |
| **Redirect** | Router informs of a better next-hop path. |

### ND and Multicast
- IPv6 uses multicast instead of broadcast to minimize network load.  
- Example multicast addresses:
  - `FF02::1` – All nodes.  
  - `FF02::2` – All routers.  

### Comparison: ARP vs ND
| Feature | ARP (IPv4) | ND (IPv6) |
|:----------|:-------------|:-------------|
| Protocol | ARP | ICMPv6 |
| Addressing | Broadcast | Multicast |
| Security | Vulnerable to spoofing | Supports Secure Neighbor Discovery (SEND) |
| Router Discovery | Separate (via DHCP or manual) | Built-in (RS/RA) |

## Common Mistakes
- Assuming ND uses broadcast (it does not).  
- Confusing NS/NA messages with ARP request/reply (they serve the same purpose but differ in protocol).  

## Quick Checks
- What ICMPv6 messages replace ARP in IPv6?  
- Why is multicast preferred over broadcast in IPv6?  

## Connections
- Builds on: [[ARP Issues and Security Considerations]]  
- Leads to: [[Networking – Module 9 Review and Practice]]  
- Related: [[Networking – IPv6 Packet Structure and Improvements]]