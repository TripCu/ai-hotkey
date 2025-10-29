---
title: "Networking – Basic Device Configuration"
tags: ["networking", "switch-setup", "security", "module2"]
source: ["ITN_Module_2.pptx.pdf"]
created: "2025-10-29"
summary: "Covers naming devices, securing access, encrypting passwords, and configuring banners."
---

> [!Abstract]
> Teaches initial switch configuration: hostname, passwords, and security standards.

## Key Ideas
- Devices need unique hostnames for identification.  
- Secure access using console, VTY, and enable passwords.  
- Use `service password-encryption` to hide passwords.  
- Add a legal login banner (`banner motd`).  

## Definitions
- **Hostname:** Unique device identifier.  
- **Enable Secret:** Encrypted Privileged EXEC password.  
- **VTY Lines:** Virtual terminals for Telnet/SSH access.  
- **MOTD Banner:** Login warning message.  

## Explanation
Configuration sequence:  
1. `hostname Switch1`  
2. `line console 0` → `password x` → `login`  
3. `enable secret strongpass`  
4. `line vty 0 15` → `password x` → `login`  
5. `service password-encryption`  
6. `banner motd # Unauthorized Access Prohibited #`  

These steps ensure basic security before network operation.

## Common Mistakes
- Using weak passwords (e.g., “cisco”).  
- Forgetting to apply `login`.  
- Skipping encryption or banner setup.  

## Quick Checks
- Which command encrypts all plaintext passwords?  
- Why configure a banner MOTD?  

## Connections
- Builds on: [[The Command Structure]]  
- Related: [[Save Configurations]]  
- Leads to: [[Ports and Addresses]]