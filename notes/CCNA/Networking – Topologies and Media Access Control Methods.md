---
title: "Networking – Topologies and Media Access Control Methods"
tags: ["networking", "topologies", "wan", "lan", "csma-cd", "csma-ca", "duplex", "module6"]
source: ["ITN_Module_6.pptx.pdf"]
created: "2025-10-29"
summary: "Compares physical and logical topologies, explains LAN/WAN structures, duplex communication, and media access control methods."
---

> [!Abstract]
> The topology of a network defines its structure—physically and logically—while media access control governs how devices share communication channels.

## Key Ideas
- **Physical topology:** How devices and cables are physically arranged.  
- **Logical topology:** How data moves between devices virtually.  
- **Common WAN topologies:** Point-to-point, hub-and-spoke, mesh.  
- **Common LAN topologies:** Star, extended star, bus, ring.  
- **Access control:** Determines who transmits data and when.  

## Definitions
- **Half-Duplex:** Devices take turns transmitting; cannot send and receive simultaneously.  
- **Full-Duplex:** Devices can send and receive simultaneously.  
- **CSMA/CD:** Collision detection for Ethernet (half-duplex).  
- **CSMA/CA:** Collision avoidance for Wi-Fi (half-duplex).  
- **Controlled Access:** Each node has a specific turn (used in legacy networks like Token Ring).

## Explanation
**Physical vs Logical Topologies:**  
- Physical shows cable layout (e.g., switches, routers, links).  
- Logical defines how signals flow (e.g., IP addressing, virtual paths).

**WAN Examples:**  
- **Point-to-Point:** Simple link between two nodes.  
- **Hub-and-Spoke:** Central site connects multiple branches.  
- **Mesh:** High reliability; each node connects to all others.

**LAN Examples:**  
- **Star:** Central switch connects all nodes (modern Ethernet).  
- **Bus/Ring:** Used in older networks.

**Access Control Methods:**
- **Contention-Based:** Devices compete for medium (CSMA/CD, CSMA/CA).  
- **Controlled:** Sequential access (Token Ring).

## Common Mistakes
- Mixing up physical and logical topologies.  
- Using half-duplex on switches (modern networks use full-duplex).  

## Quick Checks
- What is the difference between physical and logical topology?  
- When is CSMA/CA preferred over CSMA/CD?  

## Connections
- Builds on: [[Purpose of the Data Link Layer]]  
- Leads to: [[The Data Link Frame – Structure and Fields]]  
- Related: [[Networking – Physical Layer]]