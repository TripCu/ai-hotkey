---
title: "Networking – Ethernet MAC Addresses and Address Types"
tags: ["networking", "mac-address", "hexadecimal", "oui", "unicast", "broadcast", "multicast", "module7"]
source: ["ITN_Module_7.pptx.pdf"]
created: "2025-10-29"
summary: "Describes the structure and role of MAC addresses in unicast, broadcast, and multicast communication."
---

> [!Abstract]
> MAC addresses uniquely identify devices at the Data Link layer, enabling Ethernet to deliver frames accurately within a LAN.

## Key Ideas
- **48-bit (6-byte)** hardware address written as **12 hex digits**.  
- First 24 bits = **OUI** (organizationally unique identifier); last 24 bits = vendor assignment.  
- Each device’s NIC is burned-in with a unique MAC.  
- Represented as `AA:BB:CC:DD:EE:FF` or `AA-BB-CC-DD-EE-FF`.

## Address Types
- **Unicast:** One-to-one communication (most traffic).  
- **Broadcast:** All devices (`FF-FF-FF-FF-FF-FF`); never forwarded by routers.  
- **Multicast:** Group delivery (`01-00-5E` for IPv4, `33-33` for IPv6).

## Explanation
When a device transmits:
1. Ethernet header includes **source MAC** and **destination MAC**.  
2. NIC compares destination MAC to its own address.  
   - If match → accept frame.  
   - If broadcast or joined multicast → accept.  
   - Otherwise → discard.  
3. MACs ensure delivery only within the local broadcast domain.

### ARP and ND
- **ARP (IPv4)** maps IP → MAC.  
- **ND (IPv6)** performs similar function.  

## Common Mistakes
- Confusing IP with MAC addresses.  
- Thinking broadcast frames cross routers (they don’t).  
- Using duplicate MACs in virtual environments.

## Quick Checks
- How many bits in a MAC address?  
- Which hexadecimal prefixes denote IPv4 / IPv6 multicast?

## Connections
- Builds on: [[Networking – Ethernet Overview & Frame Structure]]  
- Leads to: [[Switch MAC Address Tables and Frame Forwarding]]