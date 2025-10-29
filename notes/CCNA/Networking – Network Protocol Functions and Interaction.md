---
title: "Networking – Network Protocol Functions and Interaction"
tags: ["networking", "protocol-functions", "module3"]
source: ["ITN_Module_3.pptx.pdf"]
created: "2025-10-29"
summary: "Covers how different network protocols work together to support reliable data transfer and services."
---

> [!Abstract]
> Network protocols define structure, purpose, and interdependence among layers, ensuring reliable communication between devices.

## Key Ideas
- Protocols can exist in **hardware**, **software**, or both.  
- Each protocol has specific functions like addressing, sequencing, and reliability.  
- Communication requires multiple cooperating protocols (e.g., HTTP, TCP, IP, Ethernet).  

## Definitions
- **Addressing:** Identifies sender and receiver.  
- **Reliability:** Guarantees delivery and retransmission if errors occur.  
- **Sequencing:** Orders data segments for reassembly.  
- **Error Detection:** Ensures integrity via checksums.  
- **Service Discovery:** Detects devices/services automatically (e.g., mDNS, SSDP).  

## Explanation
Each protocol contributes a layer of function:  
- **HTTP** defines web content rules.  
- **TCP** guarantees data delivery and manages sessions.  
- **IP** determines addressing and pathfinding.  
- **Ethernet** transmits frames locally over LAN.  

Together, they form a *protocol stack* — a layered system where each level provides services to the one above.

## Common Mistakes
- Thinking one protocol handles everything.  
- Misidentifying the role of TCP vs IP (TCP = transport, IP = addressing).  

## Quick Checks
- What layer handles reliable delivery?  
- How do multiple protocols interact during a web request?  

## Connections
- Builds on: [[Communication Rules & Protocol Basics]]  
- Leads to: [[Protocol Suites and Standards]]  
- Related: [[Data Encapsulation and PDUs]]