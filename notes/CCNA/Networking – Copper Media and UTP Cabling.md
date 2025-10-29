---
title: "Networking – Copper Media and UTP Cabling"
tags: ["networking", "cabling", "utp", "stp", "coaxial", "module4"]
source: ["ITN_Module_4.pptx.pdf"]
created: "2025-10-29"
summary: "Explains the characteristics, standards, and applications of copper cabling including UTP, STP, and coaxial media."
---

> [!Abstract]
> Copper cabling dominates LAN environments due to its cost-effectiveness, but is limited by interference and attenuation.

## Key Ideas
- **Three types**: UTP, STP, and Coaxial.  
- UTP (Unshielded Twisted Pair) is most common in Ethernet.  
- EMI, RFI, and Crosstalk degrade signal quality.  
- Cable categories (Cat5e, Cat6) define bandwidth capability.  

## Definitions
- **UTP (Unshielded Twisted Pair):** Copper pairs twisted to reduce interference.  
- **STP (Shielded Twisted Pair):** Adds foil/braid for EMI protection.  
- **Coaxial Cable:** Central conductor shielded by metal braid and insulation.  
- **Attenuation:** Signal weakening over distance.  
- **Crosstalk:** Interference from adjacent wire pairs.  

## Explanation
Copper media transmits via **electrical signals**, making it sensitive to noise and distance.  
UTP minimizes interference through **pair twisting** and **cancellation**, not shielding.  
STP improves protection but increases cost and complexity.  
Coaxial cables provide strong shielding but are heavier and less flexible.  

### UTP Standards
Governed by **TIA/EIA-568**, defining:
- Cable types and lengths (≤100m typical)  
- Connector standard (**RJ-45**)  
- Pinout conventions (T568A/B)  

**Straight-through**: same standard both ends (PC → Switch).  
**Crossover**: mixed ends (Switch ↔ Switch, legacy).  
**Rollover**: console access (PC serial → Router/Switch).  

## Common Mistakes
- Mixing standards (one end A, one end B).  
- Exceeding max cable lengths.  
- Poor terminations causing reflection or loss.  

## Quick Checks
- How does UTP reduce EMI?  
- What is the difference between straight-through and crossover cables?  

## Connections
- Builds on: [[Physical Layer Standards and Signaling]]  
- Leads to: [[Fiber-Optic Cabling and its Advantages]]  
- Related: [[Wireless Media and Connectivity]]