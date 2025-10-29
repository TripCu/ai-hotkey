---
title: "Networking – Network Layer Characteristics"
tags: ["networking", "network-layer", "ip", "ipv4", "ipv6", "osi-layer3", "module8"]
source: ["ITN_Module_8.pptx.pdf"]
created: "2025-10-29"
summary: "Explains how the network layer enables communication using IP, its core functions, and its characteristics such as connectionless and best-effort delivery."
---

> [!Abstract]
> The Network Layer (Layer 3) provides logical addressing and path determination, enabling data to move between networks using IP packets.

## Key Ideas
- Responsible for **addressing, encapsulation, routing, and de-encapsulation**.  
- IP is the main Layer 3 protocol: **IPv4** and **IPv6**.  
- Packets are created and handled at this layer for delivery between end devices.  
- Provides **best-effort**, **connectionless**, and **media-independent** delivery.

## Core Functions
1. **Addressing** – Assigns logical IP addresses for identification and routing.  
2. **Encapsulation** – Packages transport-layer segments into IP packets.  
3. **Routing** – Determines the best path for data across interconnected networks.  
4. **De-encapsulation** – Extracts transport-layer data at the destination.

## IP Characteristics
- **Connectionless:** IP does not establish a session before sending data.  
- **Best Effort:** IP doesn’t guarantee delivery or acknowledgment.  
- **Media Independent:** Can operate across copper, fiber, or wireless media.

## MTU and Fragmentation
- **MTU (Maximum Transmission Unit):** Largest packet size that can traverse a link.  
- If packet > MTU → **IPv4 fragments** it; **IPv6** drops and relies on sender to adjust.  
- Fragmentation introduces latency and overhead.

## Common Mistakes
- Believing IP handles retransmissions (it does not).  
- Confusing physical and logical addressing.  
- Ignoring MTU differences between links.

## Quick Checks
- What are the four primary network layer operations?  
- How does IPv4 handle packets larger than the MTU?  

## Connections
- Builds on: [[Purpose of the Data Link Layer]]  
- Leads to: [[IPv4 Packet Structure and Header Fields]]  
- Related: [[Networking – IP Addressing and Subnetting]]