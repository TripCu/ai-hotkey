---
title: "Networking – Switch Forwarding Methods and Port Settings"
tags: ["networking", "switching", "forwarding-methods", "duplex", "auto-mdix", "module7"]
source: ["ITN_Module_7.pptx.pdf"]
created: "2025-10-29"
summary: "Describes switch forwarding techniques, buffering, duplex modes, and Auto-MDIX operation."
---

> [!Abstract]
> Modern switches use specialized forwarding algorithms and memory strategies to achieve efficient, low-latency data delivery.

## Frame Forwarding Methods
- **Store-and-Forward:** Reads entire frame, checks CRC for errors before forwarding.  
  - Pros: error checking, QoS support.  
  - Cons: higher latency.  
- **Cut-Through:** Begins forwarding after destination MAC read.  
  - **Fast-Forward:** minimal latency, may forward bad frames.  
  - **Fragment-Free:** checks first 64 bytes to catch collisions.  

## Memory Buffering
| Type | Description |
|------|--------------|
| **Port-based** | Each port has its own queue. Frames wait until previous ones are sent. |
| **Shared Memory** | Frames stored in a common pool accessible by all ports. Better for asymmetric traffic. |

## Duplex and Speed Settings
- **Full-duplex:** Send and receive simultaneously (no collisions).  
- **Half-duplex:** One direction at a time (legacy).  
- **Auto-negotiation:** Automatically chooses best speed and duplex.  
- **Duplex mismatch:** Common cause of performance issues — occurs when one side is full, other half.  
- **Best practice:** Enable autonegotiation or manually set both ends to full-duplex.

## Auto-MDIX
- Detects cable type (straight-through vs crossover) and adjusts automatically.  
- Enabled by default on Cisco IOS 12.2(18)SE and later.  
- Can be manually set with: `mdix auto`.

## Explanation
Cut-through reduces latency but risks error propagation.  
Store-and-forward verifies CRC integrity and is preferred for QoS and VoIP.  
Shared memory improves switch efficiency under asymmetric loads.  
Matching duplex/speed settings prevents collisions and slowdowns.

## Common Mistakes
- Manually forcing inconsistent duplex settings.  
- Assuming cut-through always better regardless of errors.  

## Quick Checks
- How does fragment-free switching differ from fast-forward?  
- What problem does Auto-MDIX solve?  

## Connections
- Builds on: [[Switch MAC Address Tables and Frame Forwarding]]  
- Related: [[Networking – Data Link Layer]]  
- Leads to: [[Networking – Ethernet Troubleshooting and Practice]]