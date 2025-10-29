---
title: "Networking – Communication Rules & Protocol Basics"
tags: ["networking", "protocols", "communication", "module3"]
source: ["ITN_Module_3.pptx.pdf"]
created: "2025-10-29"
summary: "Explains the core rules and principles that enable network communication, including encoding, timing, and delivery."
---

> [!Abstract]
> Every communication follows rules. In networking, these rules — called *protocols* — govern how devices encode, send, and receive data reliably.

## Key Ideas
- Communication needs a **sender**, **receiver**, and **channel**.  
- **Protocols** define *how* devices talk and what structure messages must follow.  
- Rules include encoding, formatting, timing, and delivery.  
- The network must handle collisions, timeouts, and flow control.  

## Definitions
- **Protocol:** Set of rules governing communication.  
- **Encoding:** Converting information into transmittable form (bits, light, or sound).  
- **Flow Control:** Manages rate and timing of data transmission.  
- **Access Method:** Defines who can transmit and when (CSMA/CD, token passing).  
- **Unicast:** One-to-one delivery.  
- **Multicast:** One-to-many delivery.  
- **Broadcast:** One-to-all delivery (IPv4 only).  

## Explanation
Successful communication depends on **shared conventions**:  
- Both sides must agree on message structure (headers, size).  
- Messages must be correctly *encoded* and *decoded*.  
- Devices must respect *timing* (speed, retries, and collisions).  
- Delivery type changes how traffic behaves on a LAN.

For example, a router uses unicast for specific destinations, while ARP requests broadcast.

## Common Mistakes
- Ignoring timing or flow control when troubleshooting.  
- Confusing encoding (signal conversion) with encryption (data security).  
- Assuming IPv6 supports broadcast—it does not.  

## Quick Checks
- What are the three components of communication?  
- How does flow control prevent data loss?  

## Connections
- Builds on: [[The IT Professional]]  
- Related: [[Network Protocol Functions and Interaction]]  
- Leads to: [[Protocol Suites and Standards]]