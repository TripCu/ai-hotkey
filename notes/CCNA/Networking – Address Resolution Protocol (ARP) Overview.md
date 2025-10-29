---
title: "Networking – Address Resolution Protocol (ARP) Overview"
tags: ["networking", "arp", "ipv4", "layer2", "layer3", "address-resolution", "module9"]
source: ["ITN_Module_9.pptx.pdf"]
created: "2025-10-29"
summary: "Describes how ARP maps IPv4 addresses to MAC addresses and maintains local address tables for communication."
---

> [!Abstract]
> ARP enables IPv4 devices to discover the MAC address of another device when only its IP address is known, allowing successful frame encapsulation for delivery within a LAN.

## Key Ideas
- ARP operates between **Layer 2 and Layer 3**.  
- Performs two main functions:
  1. **Resolve IPv4 → MAC** mappings.  
  2. **Maintain an ARP table** of known address pairs.  
- Required for **local delivery** of IPv4 packets.

## ARP Operation
1. Host checks its **ARP table** for a matching IP.  
2. If found → use stored MAC.  
3. If not found → broadcast an **ARP Request**:
   - "Who has IP 192.168.1.10? Tell 192.168.1.5."  
4. The matching host responds with an **ARP Reply** (unicast).  
5. Sender caches the mapping in its ARP table.

## ARP Table Examples
- **Cisco Router:** `show ip arp`  
- **Windows PC:** `arp -a`  