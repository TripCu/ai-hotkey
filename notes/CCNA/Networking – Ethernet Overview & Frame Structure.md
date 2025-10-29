---
title: "Networking – Ethernet Overview & Frame Structure"
tags: ["networking", "ethernet", "frame-structure", "ieee-802.3", "module7"]
source: ["ITN_Module_7.pptx.pdf"]
created: "2025-10-29"
summary: "Explains Ethernet operation across OSI Layers 1–2, including encapsulation, MAC/LLC sublayers, and frame composition."
---

> [!Abstract]
> Ethernet functions at both the **Data Link** and **Physical** layers, defining how bits are framed, addressed, and transmitted across media. Its reliability and scalability make it the most widespread LAN technology.

## Key Ideas
- Governed by **IEEE 802.2 (LLC)** and **IEEE 802.3 (MAC)** standards.  
- Operates across Layers 1 and 2 of the OSI model.  
- Provides consistent **encapsulation**, **addressing**, and **error detection**.  
- Supports half-duplex (legacy) and full-duplex (modern switch-based) modes.

## Data Link Sublayers
- **LLC (Logical Link Control)** – Identifies the Layer 3 protocol (IPv4, IPv6, etc.).  
- **MAC (Media Access Control)** – Performs encapsulation, addressing, and media access.

## Frame Encapsulation
1. **Frame structure** – Defines header, payload, trailer.  
2. **Addressing** – Source / destination MACs deliver the frame locally.  
3. **Error detection** – Frame Check Sequence (FCS) validates integrity.

### Frame Size
- **Minimum:** 64 bytes **Maximum:** 1518 bytes (preamble excluded).  
- < 64 B → “runt frame”; > 1518 B → “jumbo frame”.  
- Invalid-size frames are dropped.

## Explanation
Legacy Ethernet (bus / hub) relied on **CSMA/CD** to avoid collisions.  
Modern switched Ethernet runs **full-duplex**, eliminating contention and improving throughput.

## Common Mistakes
- Confusing **Layer 1 bit transmission** with **Layer 2 frame handling**.  
- Forgetting that invalid-length frames are discarded automatically.

## Quick Checks
- What OSI layers does Ethernet span?  
- Minimum and maximum Ethernet frame sizes?

## Connections
- Builds on: [[Purpose of the Data Link Layer]]  
- Leads to: [[Ethernet MAC Addresses and Address Types]]  
- Related: [[Networking – Physical Layer Standards and Signaling]]