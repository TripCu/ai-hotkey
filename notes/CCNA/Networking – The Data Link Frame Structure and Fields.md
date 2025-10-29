---
title: "Networking – The Data Link Frame: Structure and Fields"
tags: ["networking", "data-link-frame", "frame-fields", "layer2-address", "crc", "module6"]
source: ["ITN_Module_6.pptx.pdf"]
created: "2025-10-29"
summary: "Describes the composition of a data link frame, its fields, and how addressing and error detection are used for local delivery."
---

> [!Abstract]
> The data link frame defines how packets are encapsulated for transmission. Each frame includes addressing, control, and error detection fields to ensure data integrity.

## Key Ideas
- Each frame contains **header**, **data (payload)**, and **trailer**.  
- Frame structure varies by protocol (Ethernet, Wi-Fi, PPP, HDLC, etc.).  
- Frame addresses are used **only within the local network segment**.  

## Frame Fields
| Field | Description |
|:------|:-------------|
| Frame Start/Stop | Marks beginning and end of frame. |
| Addressing | Source and destination MAC addresses. |
| Type | Identifies the encapsulated Layer 3 protocol (IPv4/IPv6). |
| Control | Flow control and priority information. |
| Data | Encapsulated payload (Layer 3 packet). |
| Error Detection | Ensures data integrity, typically via **Cyclic Redundancy Check (CRC)**. |

## Explanation
When data is sent over a network:
1. The Layer 3 packet is encapsulated into a frame.  
2. The frame’s header includes source and destination MAC addresses.  
3. The trailer carries the CRC for error detection.  
4. At each hop, routers or switches remove and replace the frame header and trailer before forwarding.  

LAN and WAN technologies define their own frame formats:  
- **Ethernet (802.3)** for LANs.  
- **PPP/HDLC** for WAN links.  
- **802.11** for wireless LANs.

## Common Mistakes
- Assuming Layer 2 addresses remain constant across the internet (they only apply locally).  
- Forgetting that each hop uses a new frame with new source/destination MACs.  

## Quick Checks
- What is contained in the trailer of a frame?  
- Why do MAC addresses change at each hop?  

## Connections
- Builds on: [[Topologies and Media Access Control Methods]]  
- Leads to: [[LAN and WAN Frame Protocols]]  
- Related: [[Networking – Encapsulation and Access]]