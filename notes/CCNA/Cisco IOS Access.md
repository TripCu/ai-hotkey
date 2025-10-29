---
title: "Networking – Cisco IOS Access"
tags: ["networking", "switching", "ios"]
source: ["ITN_Module_2.pptx.pdf"]
created: "2025-10-29"
summary: "Explains Cisco IOS access methods, interfaces, and terminal emulation programs used to manage network devices."
---
> [!Abstract]
> Cisco IOS is the operating system used on routers and switches. This topic explains how to access IOS using local and remote methods.

## Key Ideas
- Network devices run the Cisco IOS operating system.
- Access can be through Console, SSH, or Telnet.
- SSH is preferred for secure remote management.

## Definitions
- **Shell:** Interface that allows users to request services from the OS.
- **Kernel:** Core that manages hardware and system processes.
- **Console:** Physical management port used for local setup.
- **SSH:** Encrypted remote CLI connection.
- **Telnet:** Unencrypted remote CLI session.

## Explanation
Network devices are managed through IOS via the Command-Line Interface.  
Local access uses a **console cable**, while remote management uses **SSH** or **Telnet**.  
Terminal emulation programs like **PuTTY** and **Tera Term** connect to these interfaces.

### Configuration Example
```plaintext
Switch> enable
Switch# configure terminal
Switch(config)# line console 0
Switch(config-line)# password cisco
Switch(config-line)# login
Switch(config-line)# exit