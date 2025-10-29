---
title: "Networking – Data Encapsulation, De-encapsulation & Access"
tags: ["networking", "encapsulation", "pdu", "data-access", "addressing", "module3"]
source: ["ITN_Module_3.pptx.pdf"]
created: "2025-10-29"
summary: "Explains how data moves through the network stack using encapsulation and how MAC and IP addresses guide delivery."
---

> [!Abstract]
> Data encapsulation and addressing define how information is packaged, transmitted, and received across networks.

## Key Ideas
- Encapsulation wraps data with headers at each layer.  
- Each layer produces a **Protocol Data Unit (PDU)**:  
  - Application → Data  
  - Transport → Segment  
  - Network → Packet  
  - Data Link → Frame  
  - Physical → Bits  
- De-encapsulation unwraps data in reverse.  
- Layer 2 (MAC) = local delivery, Layer 3 (IP) = global delivery.  

## Definitions
- **Encapsulation:** Wrapping data with control info.  
- **De-encapsulation:** Removing headers as data ascends layers.  
- **MAC Address:** Hardware address for local segment.  
- **IP Address:** Logical address for global delivery.  
- **Default Gateway:** Router that forwards traffic to remote networks.  

## Explanation
When data leaves an application:
1. Transport adds port and sequence info.  
2. Network adds source/destination IPs.  
3. Data Link adds MAC addresses.  
4. Physical converts bits to signals.

During travel, each hop changes MAC addresses but keeps the same IPs.

**Wireshark** can capture frames at each layer for analysis.

## Common Mistakes
- Assuming IP addresses change hop-to-hop.  
- Forgetting to configure the default gateway, isolating the host.  

## Quick Checks
- What’s the order of PDUs in encapsulation?  
- Why does Layer 2 addressing change per hop?  

## Connections
- Builds on: [[Reference Models (OSI and TCP/IP)]]  
- Leads to: [[Networking – Connectivity and Troubleshooting (Next Module)]]  
- Related: [[Configure IP Addressing]]