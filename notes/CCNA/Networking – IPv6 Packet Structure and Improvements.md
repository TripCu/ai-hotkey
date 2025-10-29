---
title: "Networking – IPv6 Packet Structure and Improvements"
tags: ["networking", "ipv6", "header", "flow-label", "next-header", "module8"]
source: ["ITN_Module_8.pptx.pdf"]
created: "2025-10-29"
summary: "Compares IPv4 and IPv6 headers, explains IPv6 improvements, and describes major header fields and extension headers."
---

> [!Abstract]
> IPv6 replaces IPv4 with a simplified header, vastly larger address space, and modern design eliminating NAT and fragmentation overhead.

## Key Ideas
- **128-bit addressing** → virtually unlimited global addresses.  
- **Simplified header (fixed 40 bytes)** improves processing speed.  
- **Extension headers** handle optional info such as fragmentation, security, and QoS.  

## IPv6 vs IPv4 Improvements
- No NAT: Restores **end-to-end connectivity**.  
- Fewer fields: Removed checksum and fragmentation for simplicity.  
- Streamlined routing for higher efficiency.  
- Better QoS and flow identification using **Traffic Class** and **Flow Label**.

## Major IPv6 Header Fields
| Field | Description |
|:------|:-------------|
| **Version** | Identifies IPv6 (0110). |
| **Traffic Class** | QoS field; similar to DSCP. |
| **Flow Label** | Marks packets of the same flow for priority handling. |
| **Payload Length** | Size of encapsulated data (in bytes). |
| **Next Header** | Indicates next-layer protocol or extension header. |
| **Hop Limit** | Replaces IPv4 TTL. |
| **Source Address** | 128-bit source. |
| **Destination Address** | 128-bit destination. |

## Extension Headers (EH)
- Used for optional data like fragmentation, authentication, and routing options.  
- Routers **do not fragment** IPv6 packets; source must adjust MTU.

## Common Mistakes
- Assuming IPv6 packets can be fragmented by routers.  
- Thinking IPv6 headers are smaller; they are **simpler but fixed-length**.  

## Quick Checks
- What field replaced IPv4’s TTL?  
- Why was the checksum removed in IPv6?  

## Connections
- Builds on: [[IPv4 Packet Structure and Header Fields]]  
- Leads to: [[Host Routing Decisions and Default Gateways]]