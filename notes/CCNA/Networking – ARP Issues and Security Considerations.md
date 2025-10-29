---
title: "Networking – ARP Issues and Security Considerations"
tags: ["networking", "arp", "spoofing", "security", "broadcast", "module9"]
source: ["ITN_Module_9.pptx.pdf"]
created: "2025-10-29"
summary: "Discusses ARP broadcasts, performance impact, and security vulnerabilities such as spoofing and poisoning."
---

> [!Abstract]
> While ARP is essential for IPv4 communication, its broadcast nature can affect performance and be exploited by attackers, requiring network protection mechanisms.

## Key Ideas
- ARP broadcasts are processed by all devices on a LAN.  
- Excessive ARP traffic can create **broadcast storms** on large networks.  
- ARP lacks authentication → vulnerable to **spoofing/poisoning** attacks.  

## ARP Spoofing (Poisoning)
- Attacker sends fake ARP replies, associating their MAC with another device’s IP (often the default gateway).  
- Redirects or intercepts traffic → **Man-in-the-Middle (MitM)** attacks.  
- Can be used to capture credentials or disrupt communication.  

### Mitigation Techniques
- **Dynamic ARP Inspection (DAI):** Validates ARP packets against known IP–MAC bindings.  
- **Port Security:** Limits MACs on a port.  
- **Static ARP Entries:** Manual mappings for critical devices.  
- **VLAN Segmentation:** Reduces broadcast domains.

## Performance Concerns
- Each ARP broadcast interrupts all devices on the network.  
- Overuse in dense networks can cause temporary slowdowns.  

## Common Mistakes
- Ignoring ARP security risks on “trusted” LANs.  
- Assuming ARP is needed for IPv6 (it’s replaced by ND).  

## Quick Checks
- What vulnerability allows ARP spoofing?  
- Which feature prevents ARP table poisoning on switches?  

## Connections
- Builds on: [[Address Resolution Protocol (ARP) Overview]]  
- Leads to: [[IPv6 Neighbor Discovery Protocol]]  
- Related: [[Network Security Fundamentals]]