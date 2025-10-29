---
title: "Networking – Reference Models (OSI and TCP/IP)"
tags: ["networking", "osi-model", "tcpip-model", "layers", "module3"]
source: ["ITN_Module_3.pptx.pdf"]
created: "2025-10-29"
summary: "Explains the OSI and TCP/IP layered models used to standardize communication and troubleshoot network problems."
---

> [!Abstract]
> Layered models simplify complex network design, allowing modular development, troubleshooting, and standardization.

## Key Ideas
- OSI has 7 layers; TCP/IP has 4.  
- Each layer provides services to the one above.  
- Models help isolate and troubleshoot network issues.  

## Definitions
**OSI Model Layers:**  
1. Physical – transmission of bits  
2. Data Link – frames and MAC addressing  
3. Network – IP addressing and routing  
4. Transport – segmentation and reassembly  
5. Session – maintains connections  
6. Presentation – data format and encryption  
7. Application – end-user interaction  

**TCP/IP Layers:**  
1. Network Access  
2. Internet  
3. Transport  
4. Application  

## Explanation
Layered models:
- Promote vendor interoperability.  
- Allow modular upgrades.  
- Provide a shared vocabulary for diagnosing issues.  

**Troubleshooting Example:**  
If a ping fails, check Layers 1–3 (Physical, Data Link, Network).  
If the ping works but login fails, check Layers 5–7 (Session, Presentation, Application).  

## Common Mistakes
- Assuming OSI and TCP/IP layers map one-to-one.  
- Forgetting OSI has Presentation and Session layers not explicitly present in TCP/IP.  

## Quick Checks
- What is the main purpose of a layered model?  
- Which OSI layer corresponds to IP?  

## Connections
- Builds on: [[Protocol Suites and Standards]]  
- Related: [[Data Encapsulation and PDUs]]  
- Leads to: [[Data Access and Addressing]]