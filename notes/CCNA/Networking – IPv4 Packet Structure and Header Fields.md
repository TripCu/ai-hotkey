---
title: "Networking – IPv4 Packet Structure and Header Fields"
tags: ["networking", "ipv4", "packet-header", "ttl", "checksum", "module8"]
source: ["ITN_Module_8.pptx.pdf"]
created: "2025-10-29"
summary: "Describes the structure of the IPv4 header, its fields, and their purpose in routing and delivery."
---

> [!Abstract]
> IPv4 provides logical addressing and routing. Its header contains fields that guide packets through the network and ensure minimal control overhead.

## Key Ideas
- IPv4 is a **32-bit addressing protocol** used for routing between networks.  
- The **header** provides control and addressing information to Layer 3 devices.  
- The **payload** carries the upper-layer data (segment).  

## Major IPv4 Header Fields
| Field | Description |
|:------|:-------------|
| **Version** | Identifies IPv4 (binary 0100). |
| **Differentiated Services (DS/ToS)** | Used for QoS prioritization. |
| **Header Checksum** | Detects errors in the header. |
| **Time to Live (TTL)** | Limits lifespan; decrements per router hop. |
| **Protocol** | Indicates next-layer protocol (TCP, UDP, ICMP, etc.). |
| **Source Address** | 32-bit IP of sender. |
| **Destination Address** | 32-bit IP of receiver. |

## Explanation
Each router examines and updates the header as packets move across the network.  
- TTL prevents endless looping.  
- Checksum ensures header integrity.  
- IP addresses ensure end-to-end delivery logic.

## Example
A ping from `192.168.1.5` to `8.8.8.8` passes through routers that decrement TTL and recalculate checksum at every hop.

## Common Mistakes
- Thinking the IPv4 header detects errors in payload (only header).  
- Forgetting routers always replace Layer 2 headers, not Layer 3.  

## Quick Checks
- Which field prevents routing loops?  
- What does the Protocol field identify?

## Connections
- Builds on: [[Network Layer Characteristics]]  
- Leads to: [[IPv6 Packet Structure and Improvements]]