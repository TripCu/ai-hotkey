---
title: "Networking – Network Components"
tags: ["networking", "core", "components"]
source: ["ITN_Module_1.pptx.pdf"]
created: "2025-10-29"
summary: "Identifies hosts, servers, clients, intermediary devices, and media used to build a functional network."
---
> [!Abstract]
> Every network consists of end devices, intermediary devices, and transmission media that enable data exchange.

## Key Ideas
- Hosts act as senders or receivers of data.
- Intermediary devices connect and manage data paths.
- Network media carry signals between devices.

## Definitions
- **Host:** Any device that sends or receives data across a network.
- **Server:** Provides information or services to clients.
- **Client:** Requests and uses services from a server.
- **Peer-to-Peer (P2P):** Network where devices can act as both client and server.
- **Intermediary Device:** Connects end devices (e.g., routers, switches).
- **Media:** Physical or wireless pathways that carry data.

## Explanation
Networks operate through cooperation among hosts and intermediary devices.  
Servers store resources; clients request them.  
P2P networks allow direct sharing without a dedicated server—useful for small setups but limited in scalability and security.  
Intermediaries manage traffic and optimize delivery using protocols and routing tables.

### Configuration Example
```plaintext
Switch> enable
Switch# show interfaces
Router(config)# interface g0/0
Router(config-if)# description Connection to Switch1
Router(config-if)# no shutdown