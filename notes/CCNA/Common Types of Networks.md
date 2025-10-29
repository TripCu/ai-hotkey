---
title: "Networking – Common Types of Networks"
tags: ["networking", "core", "network-types"]
source: ["ITN_Module_1.pptx.pdf"]
created: "2025-10-29"
summary: "Compares LANs, WANs, intranets, extranets, and network scales from SOHO to world-wide networks."
---

> [!Abstract]
> Networks vary in size, scope, and management—from small home setups to the global internet.

## Key Ideas
- LANs connect devices in limited areas.
- WANs interconnect LANs across regions.
- Intranets and extranets provide internal and partner access.

## Definitions
- **LAN (Local Area Network):** Small geographic coverage, single admin.
- **WAN (Wide Area Network):** Connects multiple LANs across distances.
- **Intranet:** Private internal network.
- **Extranet:** Restricted external access to internal resources.

## Explanation
LANs provide high-speed connectivity for local users; WANs bridge these LANs globally.  
ISPs and organizations use fiber, wireless, and copper media.  
Intranets serve internal communication; extranets extend access to trusted external users.

### Configuration Example
```plaintext
Router(config)# interface g0/0
Router(config-if)# ip address 10.0.0.1 255.255.255.0
Router(config)# interface s0/0/0
Router(config-if)# ip address 172.16.0.1 255.255.255.252
Router(config-if)# clock rate 64000