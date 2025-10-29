---
title: "Networking – IOS Navigation"
tags: ["networking", "ios-navigation", "cli-modes", "module2"]
source: ["ITN_Module_2.pptx.pdf"]
created: "2025-10-29"
summary: "Covers Cisco IOS command modes and how to move between them."
---

> [!Abstract]
> Understanding IOS modes and prompts is essential for configuring and troubleshooting Cisco devices.

## Key Ideas
- IOS CLI has hierarchical command modes with unique prompts.  
- `enable` → Privileged EXEC; `configure terminal` → Global Config.  
- Sub-modes like **Line** and **Interface Configuration** control specific components.  
- Use `exit`, `end`, or `Ctrl + Z` to move between modes.

## Definitions
- **User EXEC Mode:** Basic monitoring commands ( `>` ).  
- **Privileged EXEC Mode:** Full access ( `#` ).  
- **Global Config Mode:** System-wide settings.  
- **Line Config Mode:** Console or VTY line settings.  
- **Interface Config Mode:** Per-port or interface settings.  

## Explanation
Network administrators navigate IOS modes to configure devices:  
- Start in User EXEC (`Switch>`).  
- Use `enable` to enter Privileged EXEC (`Switch#`).  
- `configure terminal` opens Global Config (`Switch(config)#`).  
- `line console 0` or `interface Fa0/1` enters submodes.  
- `exit` steps back one level; `end` or `Ctrl + Z` returns to Privileged EXEC.  

## Common Mistakes
- Forgetting to save configurations before exiting.  
- Typing commands in the wrong mode.  
- Confusing `exit` and `end`.  

## Quick Checks
- What prompt indicates Privileged EXEC mode?  
- How do you return to Global Config from Line Config?  

## Connections
- Builds on: [[Cisco IOS Access]]  
- Related: [[The Command Structure]]  
- Leads to: [[Basic Device Configuration]]