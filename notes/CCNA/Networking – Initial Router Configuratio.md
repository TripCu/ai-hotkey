---
title: "Networking – Initial Router Configuration"
tags: ["networking", "router", "ios", "cli", "basic-configuration", "security", "module10"]
source: ["ITN_Module_10.pptx.pdf"]
created: "2025-10-29"
summary: "Outlines essential steps to configure Cisco routers with secure access, banners, and saved settings."
---

> [!Abstract]
> Every new Cisco router requires an initial configuration to secure access, set identification, and enable connectivity. These steps are the foundation for all subsequent network setup.

## Key Ideas
- Establishes secure access through passwords and encrypted authentication.  
- Identifies the device using a hostname and banner message.  
- Ensures configuration persistence by saving to NVRAM.  
- Promotes consistent documentation and accountability.

## Configuration Commands
```bash
Router(config)# hostname R1
Router(config)# enable secret <password>
Router(config)# line console 0
Router(config-line)# password <password>
Router(config-line)# login
Router(config)# line vty 0 4
Router(config-line)# password <password>
Router(config-line)# login
Router(config-line)# transport input ssh telnet
Router(config)# service password-encryption
Router(config)# banner motd # Unauthorized Access Prohibited #
Router# copy running-config startup-config