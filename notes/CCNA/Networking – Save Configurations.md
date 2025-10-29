---
title: "Networking – Save Configurations"
tags: ["networking", "ios-config", "startup-config", "module2"]
source: ["ITN_Module_2.pptx.pdf"]
created: "2025-10-29"
summary: "Explains running-config vs startup-config, saving and restoring configurations."
---

> [!Abstract]
> Describes how to store, backup, and restore Cisco device configurations.

## Key Ideas
- Two config files: **running-config** (RAM) and **startup-config** (NVRAM).  
- Save with `copy running-config startup-config`.  
- Restore with `reload` or `erase startup-config`.  
- Logs can be captured using PuTTY or Tera Term.  

## Definitions
- **NVRAM:** Non-volatile storage for startup config.  
- **RAM:** Volatile working memory.  
- **Reload:** Reboots the device.  
- **Erase Startup-Config:** Clears saved settings.  

## Explanation
The running configuration is active and volatile. To persist changes:  