---
title: "Networking – MAC and IP Address Roles"
tags: ["networking", "mac", "ip", "layer2", "layer3", "addressing", "module9"]
source: ["ITN_Module_9.pptx.pdf"]
created: "2025-10-29"
summary: "Explains the relationship between MAC and IP addresses and how they enable local and remote communication."
---

> [!Abstract]
> Devices use two address types: **MAC addresses** for local delivery at Layer 2 and **IP addresses** for logical delivery at Layer 3. Understanding how they interact is crucial to grasping how networks forward data between devices.

## Key Ideas
- **MAC (Media Access Control)** address: physical identifier burned into a device’s NIC.  
- **IP address:** logical identifier assigned to enable end-to-end communication across networks.  
- Communication type determines which MAC address is used: destination device (local) or default gateway (remote).

## Local vs Remote Delivery
| Scenario | MAC Destination | IP Destination | Description |
|:----------|:----------------|:---------------|:-------------|
| **Local Network** | Destination device’s MAC | Destination device’s IP | Devices communicate directly. |
| **Remote Network** | Default gateway’s MAC | Destination device’s IP | Frame sent to router, which forwards it onward. |

### Local Network Communication
- If the destination IP is on the same subnet, the sender encapsulates the packet using the **destination’s MAC**.  
- Data never leaves the local broadcast domain.

### Remote Network Communication
- If the destination IP is on another network, the sender encapsulates the frame using the **default gateway’s MAC**.  
- The router de-encapsulates, re-encapsulates, and forwards it toward the destination.

## Common Mistakes
- Thinking MAC addresses are used across the internet (they’re local only).  
- Forgetting that routers change Layer 2 headers at each hop.  

## Quick Checks
- When does a device use its default gateway’s MAC address?  
- How are Layer 2 and Layer 3 addresses related?

## Connections
- Builds on: [[Networking – Host Routing Decisions and Default Gateways]]  
- Leads to: [[Address Resolution Protocol (ARP) Overview]]  
- Related: [[IPv6 Neighbor Discovery Protocol]]