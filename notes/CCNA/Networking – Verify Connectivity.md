---
title: "Networking – Verify Connectivity"
tags: ["networking", "ping", "troubleshooting", "module2"]
source: ["ITN_Module_2.pptx.pdf"]
created: "2025-10-29"
summary: "Tests interface and end-to-end connectivity using ping and show commands."
---

> [!Abstract]
> Validating connectivity ensures that device interfaces and network paths function properly.

## Key Ideas
- Use `no shutdown` to activate interfaces.  
- Test connections with `ping`.  
- Verify interface status with `show ip interface brief`.  

## Definitions
- **Ping:** ICMP test for reachability.  
- **Interface Assignment:** Binding an IP to a port.  

## Explanation
After configuration:  
1. Enable interfaces (`no shutdown`).  
2. Ping between devices to verify communication.  
3. Use `show ip int brief` to confirm interface status.  

## Common Mistakes
- Forgetting to enable interfaces.  
- Pinging before IP setup.  
- Ignoring failed ping causes (DNS, cable, IP mismatch).  

## Quick Checks
- What does `ping` test?  
- Which command shows interface status?  

## Connections
- Builds on: [[Configure IP Addressing]]  
- Leads to: [[Basic Switch and End Device Configuration Practice]]