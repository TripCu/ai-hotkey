---
title: "Networking – Host Routing Decisions and Default Gateways"
tags: ["networking", "host-routing", "default-gateway", "routing-table", "module8"]
source: ["ITN_Module_8.pptx.pdf"]
created: "2025-10-29"
summary: "Describes how hosts use routing tables and default gateways to determine whether destinations are local or remote."
---

> [!Abstract]
> Hosts decide where to send packets based on local routing tables, determining if destinations are local or remote using subnet and gateway logic.

## Key Ideas
- Hosts maintain their own **routing tables** with interfaces and gateway info.  
- Use IP + subnet mask (IPv4) or prefix (IPv6) to determine locality.  
- Forward unknown networks to the **Default Gateway (DGW)**.

## Local vs Remote Delivery
| Type | Description | Example |
|:------|:-------------|:-------------|
| **Local** | Same network; delivered directly. | 192.168.1.10 → 192.168.1.20 |
| **Remote** | Different network; sent to DGW. | 192.168.1.10 → 10.0.0.5 |
| **Loopback** | Sent to self for testing. | 127.0.0.1 or ::1 |

### Default Gateway (DGW)
- Must share the same network as the host.  
- Routes traffic outside local network.  
- Configured manually or via DHCP (IPv4), or learned from Router Advertisement (IPv6).  
- If incorrect or missing, host cannot reach remote networks.

### Displaying Routing Tables
- **Windows:** `route print` or `netstat -r`  
- **Sections:**  
  - Interface List  
  - IPv4 Routing Table  
  - IPv6 Routing Table

## Common Mistakes
- Forgetting to configure a gateway on Layer 2 switches.  
- Using incorrect subnet masks leading to wrong route decisions.  

## Quick Checks
- What is the purpose of a default gateway?  
- How does IPv6 learn gateway information automatically?

## Connections
- Builds on: [[IPv6 Packet Structure and Improvements]]  
- Leads to: [[Router Routing Tables and Forwarding Methods]]