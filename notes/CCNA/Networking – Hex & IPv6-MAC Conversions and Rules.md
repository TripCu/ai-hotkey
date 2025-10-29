---
title: "Networking – Hex & IPv6/MAC Conversions and Rules"
tags: ["networking", "hexadecimal", "ipv6", "mac", "conversions", "module5"]
source: ["ITN_Module_5.pptx.pdf"]
created: "2025-10-29"
summary: "Demonstrates hexadecimal↔binary conversion and how hex simplifies IPv6 and MAC notation."
---

> [!Abstract]
> Hexadecimal condenses long binary strings into short, human-readable groups. IPv6 and MAC addresses use hex to represent binary data compactly and accurately.

## Key Ideas
- 1 hex digit = 4 binary bits (nibble).  
- IPv6 = 128 bits = 8 hextets (16 bits each).  
- MAC addresses = 48 bits = 12 hex digits.  

## Decimal → Hex
1. Convert decimal → binary.  
2. Group bits into 4s.  
3. Replace each nibble with its hex equivalent.  

Example: 168 = 10101000₂ → 1010 1000 → A8₁₆.

## Hex → Decimal
1. Convert each hex digit → 4-bit binary.  
2. Combine and compute decimal value.  
Example: D2₁₆ = 11010010₂ = 210₁₀.

## IPv6 Structure
Eight groups of four hex digits (e.g., 2001:0DB8:0000:0000:0000:FF00:0042:8329).  
Each hextet = 16 bits; groups can omit leading zeros or use `::` once for zero compression.

## Common Mistakes
- Omitting required zeros within a hextet.  
- Confusing decimal “A” with hex A (10).  

## Quick Checks
- Convert 0x7F to decimal.  
- Convert 255 to hex.  
- How many hex digits make up one IPv6 address?  

## Connections
- Builds on: [[Binary & IPv4 – Conversions and Practice]]  
- Leads to: [[Hex & Binary Speed Drills – Tables and Patterns]]