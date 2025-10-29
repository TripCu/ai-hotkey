---
title: "Networking – LAN and WAN Frame Protocols"
tags: ["networking", "ethernet", "wan", "ppp", "hdlc", "frame-relay", "layer2-protocols", "module6"]
source: ["ITN_Module_6.pptx.pdf"]
created: "2025-10-29"
summary: "Compares common LAN and WAN Layer 2 protocols and how they provide media access and data framing for different network topologies."
---

> [!Abstract]
> Different Layer 2 protocols define unique framing and access control methods based on network type and topology. Understanding their roles is key to diagnosing communication issues.

## Key Ideas
- Data Link protocols vary by network type (LAN/WAN).  
- Each performs **framing**, **error detection**, and **media access control**.  
- Examples include **Ethernet**, **802.11**, **PPP**, **HDLC**, and **Frame Relay**.

## Protocols
- **Ethernet (IEEE 802.3):**  
  - Most common LAN protocol.  
  - Uses MAC addressing and CSMA/CD (now full-duplex with switches).  

- **802.11 (Wi-Fi):**  
  - Wireless LAN standard.  
  - Uses CSMA/CA to prevent collisions.  

- **PPP (Point-to-Point Protocol):**  
  - Connects two nodes directly.  
  - Handles authentication (PAP/CHAP) and error detection.  

- **HDLC (High-Level Data Link Control):**  
  - Synchronous serial WAN protocol.  
  - Encapsulates Layer 3 packets with minimal overhead.  

- **Frame Relay:**  
  - Legacy packet-switched WAN protocol.  
  - Uses virtual circuits instead of dedicated physical links.  

## Explanation
Each protocol adapts the generic frame concept to its environment:
- LAN protocols manage multiple access and local broadcast domains.  
- WAN protocols focus on point-to-point or virtual connections.  
The Data Link Layer’s flexibility enables uniform communication across vastly different physical infrastructures.

## Common Mistakes
- Assuming all Layer 2 frames look alike—formats differ significantly.  
- Using Ethernet terminology (e.g., MAC) to describe WAN technologies like PPP.  

## Quick Checks
- What are two WAN protocols that encapsulate Layer 3 data?  
- Which Layer 2 protocol uses CSMA/CA?  

## Connections
- Builds on: [[The Data Link Frame – Structure and Fields]]  
- Related: [[Topologies and Media Access Control Methods]]  
- Leads to: [[Networking – Module Practice and Quiz Notes]]