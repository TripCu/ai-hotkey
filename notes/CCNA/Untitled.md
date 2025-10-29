---

```markdown
---
title: "Networking – Router Interface Configuration and Verification"
tags: ["networking", "router", "interfaces", "ipv4", "ipv6", "verification", "module10"]
source: ["ITN_Module_10.pptx.pdf"]
created: "2025-10-29"
summary: "Explains how to assign IP addresses, enable interfaces, and verify interface status on Cisco routers."
---

> [!Abstract]
> Router interfaces must be configured and enabled before data can flow. Proper labeling and verification prevent connectivity errors.

## Configuration Commands
```bash
Router(config)# interface gigabitEthernet 0/0/0
Router(config-if)# description Link to LAN
Router(config-if)# ip address 192.168.10.1 255.255.255.0
Router(config-if)# ipv6 address 2001:db8:acad:10::1/64
Router(config-if)# no shutdown