---
title: "Networking – Switch MAC Address Tables and Frame Forwarding"
tags: ["networking", "switching", "cam-table", "mac-learning", "forwarding", "module7"]
source: ["ITN_Module_7.pptx.pdf"]
created: "2025-10-29"
summary: "Explains how switches build and use MAC address tables to learn devices and make forwarding decisions."
---

> [!Abstract]
> Ethernet switches make intelligent forwarding decisions by dynamically learning source MAC addresses and associating them with specific ports.

## Key Ideas
- Switches operate at **Layer 2**, forwarding based solely on MAC addresses.  
- Each switch maintains a **MAC address table** (CAM table).  
- Entries = { MAC, port, timestamp }.  

## Learning Process
1. **Learn source MAC:**  
   - When a frame arrives, record { source MAC → incoming port }.  
2. **Update timer:** refresh entry (default ≈ 5 min).  
3. **Relearn if MAC appears on new port:** update mapping.  

## Forwarding Process
- **Unicast known:** send out specific port.  
- **Unicast unknown:** flood to all ports except incoming.  
- **Broadcast / Multicast:** flood all ports except incoming.  
- Each hop re-encapsulates the frame with new source / destination MACs.

## Explanation
Unlike hubs that repeat bits, switches analyze each frame header.  
This reduces collisions and increases bandwidth per device.  
Frames with errors or invalid lengths are dropped.  

### Example Scenario
- Host A → Host B on same switch: forwarded only to B’s port.  
- Host A → Host C unknown to switch: frame flooded; when C replies, switch learns MAC.

## Common Mistakes
- Assuming switches forward broadcasts to other networks.  
- Forgetting MAC tables are temporary and dynamic.  

## Quick Checks
- What happens if the destination MAC is unknown?  
- How long does a MAC entry usually remain in the table?

## Connections
- Builds on: [[Ethernet MAC Addresses and Address Types]]  
- Leads to: [[Switch Forwarding Methods and Port Settings]]  
- Related: [[Networking – Data Link Frame Structure and Fields]]