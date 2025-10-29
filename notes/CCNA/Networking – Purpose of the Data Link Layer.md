---
title: "Networking – Purpose of the Data Link Layer"
tags: ["networking", "data-link-layer", "osi-layer2", "llc", "mac", "module6"]
source: ["ITN_Module_6.pptx.pdf"]
created: "2025-10-29"
summary: "Explains the purpose and sublayers of the Data Link Layer and how it enables communication between network devices."
---

> [!Abstract]
> The Data Link Layer (Layer 2) connects network software to physical media, ensuring reliable frame delivery between nodes through encapsulation, media access control, and error detection.

## Key Ideas
- Provides reliable communication between **Network Interface Cards (NICs)**.  
- Encapsulates **Layer 3 packets** into **Layer 2 frames** for transmission.  
- Defines **LLC (Logical Link Control)** and **MAC (Media Access Control)** sublayers.  
- Detects and rejects corrupted frames.  

## Definitions
- **Data Link Layer:** Responsible for node-to-node communication and frame transmission.  
- **LLC (Logical Link Control):** Manages communication between higher network software and hardware.  
- **MAC (Media Access Control):** Controls access to physical media and frame encapsulation.  
- **Frame:** Encapsulated packet with header and trailer for transmission.

## Explanation
When data moves from the Network Layer, the Data Link Layer takes over, preparing it for physical transmission.  
It performs three essential tasks:
1. **Encapsulation** – Wraps packets in frames, including control and addressing information.  
2. **Access Control** – Determines when devices can transmit on shared media.  
3. **Error Detection** – Uses checks (like CRC) to identify corrupted frames.  

Every router or switch performing Layer 2 forwarding must:
1. Accept the frame.  
2. Remove the header/trailer (de-encapsulation).  
3. Encapsulate the packet into a new frame.  
4. Forward the frame to the next hop.

## Common Mistakes
- Confusing **Layer 2 addresses (MAC)** with **Layer 3 addresses (IP)**.  
- Forgetting that each hop re-encapsulates the packet into a new frame.  

## Quick Checks
- What are the two sublayers of the Data Link Layer?  
- How does the MAC sublayer differ from LLC?  

## Connections
- Builds on: [[Networking – Reference Models (OSI and TCP/IP)]]  
- Leads to: [[Topologies and Media Access Control Methods]]  
- Related: [[Networking – Physical Layer Standards and Signaling]]