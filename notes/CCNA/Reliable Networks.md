---
title: "Networking – Reliable Networks"
tags: ["networking", "core", "reliability"]
source: ["ITN_Module_1.pptx.pdf"]
created: "2025-10-29"
summary: "Covers the four fundamental characteristics of a reliable network: fault tolerance, scalability, QoS, and security."
---
> [!Abstract]
> Reliability ensures networks remain functional, expandable, and secure while meeting user performance expectations.

## Key Ideas
- Fault tolerance through redundancy.
- Scalability via standard protocols.
- QoS manages traffic priorities.
- Security protects data and devices.

## Definitions
- **Fault Tolerance:** Network’s ability to recover from failure.
- **Scalability:** Expansion without loss of performance.
- **QoS (Quality of Service):** Traffic prioritization method.
- **Security:** Protection of confidentiality, integrity, and availability.

## Explanation
Reliable networks use redundant links and routers to ensure uptime.  
QoS allocates bandwidth based on traffic type, giving priority to voice/video.  
Scalability and security underpin sustainable network design.

### Configuration Example
```plaintext
Router(config)# access-list 10 permit 192.168.1.0 0.0.0.255
Router(config)# class-map match-any VOICE
Router(config)# policy-map PRIORITY
Router(config-pmap)# class VOICE
Router(config-pmap-c)# priority 1000