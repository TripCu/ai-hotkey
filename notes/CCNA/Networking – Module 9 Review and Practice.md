---
title: "Networking – Module 9 Review and Practice"
tags: ["networking", "review", "quiz", "practice", "module9"]
source: ["ITN_Module_9.pptx.pdf"]
created: "2025-10-29"
summary: "Consolidates the concepts of MAC vs IP addressing, ARP for IPv4, and Neighbor Discovery for IPv6."
---

> [!Abstract]
> This summary ties together IPv4 and IPv6 address resolution, ensuring understanding of when and how each protocol uses MAC and IP information to complete communication.

## Summary Points
- MAC addresses deliver frames **locally**; IP addresses route packets **logically**.  
- IPv4 uses **ARP** for address resolution; IPv6 uses **ICMPv6 ND**.  
- Local traffic → destination MAC of host.  
- Remote traffic → MAC of default gateway.  
- ARP tables cache mappings; ND maintains neighbor caches.  
- Entries time out and refresh dynamically.  

### Key Commands
| Platform | Command | Function |
|:----------|:----------|:----------|
| Cisco | `show ip arp` | Displays ARP table |
| Windows | `arp -a` | Displays local ARP cache |
| Cisco/IPv6 | `show ipv6 neighbors` | Displays ND cache |

### Practice Objectives
- Identify which MAC is used for local vs remote destinations.  
- Interpret ARP/ND table entries.  
- Recognize potential ARP security threats.

## Common Mistakes
- Misunderstanding that routers forward ARP or ND messages (they don’t).  
- Assuming IPv6 still relies on ARP.  

## Connections
- Builds on: [[IPv6 Neighbor Discovery Protocol (ND)]]  
- Related: [[Networking – Network Layer Characteristics]]  
- Leads to: [[Networking – Transport Layer Fundamentals (Module 10)]]