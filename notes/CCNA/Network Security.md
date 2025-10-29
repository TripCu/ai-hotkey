---

title: "Networking – Network Security"

tags: ["networking", "security", "core"]

source: ["ITN_Module_1.pptx.pdf"]

created: "2025-10-29"

summary: "Outlines common network threats, attack vectors, and layered defenses for home and enterprise networks."

---
> [!Abstract]

> Security protects networks from internal and external threats while maintaining availability and performance.

  

## Key Ideas

- Security must balance protection and usability.

- Threats include malware, DoS, interception, and insider attacks.

- Layered defense uses antivirus, firewalls, ACLs, IPS, and VPNs.

  

## Definitions

- **Confidentiality:** Prevent unauthorized access.

- **Integrity:** Ensure data is unchanged.

- **Availability:** Guarantee reliable access for authorized users.

- **Firewall:** Device or software controlling network traffic.

  

## Explanation

Security operates on multiple layers:  

Endpoints (antivirus), perimeter (firewalls, ACLs), and network core (IPS/VPN).  

Home users focus on software protection; enterprises use dedicated systems.

  

### Configuration Example

```plaintext

Router(config)# access-list 101 deny tcp any any eq 23

Router(config)# access-list 101 permit ip any any

Router(config)# interface g0/0

Router(config-if)# ip access-group 101 in