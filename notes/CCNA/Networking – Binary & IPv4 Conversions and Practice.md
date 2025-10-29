---
title: "Networking – Binary & IPv4 Conversions and Practice"
tags: ["networking", "binary", "ipv4", "octet", "conversions", "module5"]
source: ["ITN_Module_5.pptx.pdf"]
created: "2025-10-29"
summary: "Step-by-step binary↔decimal conversion for IPv4 addressing and subnet calculations."
---

> [!Abstract]
> IPv4 addresses are 32 bits split into four octets. Converting between binary and decimal forms is essential for subnetting and troubleshooting.

## Key Ideas
- Each octet contains 8 bits.  
- Each bit has a weight: 128, 64, 32, 16, 8, 4, 2, 1.  
- Converting octets accurately is critical for understanding IP addressing.

## Binary → Decimal
Multiply each bit by its weight and sum the results.  
Example: 11000000₂ = 128 + 64 = 192.  

Full IP Example:  
11000000.10101000.00001011.00001010₂ = 192.168.11.10.

## Decimal → Binary
Subtract the largest weight that fits until zero remains.  
Example: 168₁₀ →  
128 ✓ (1) → remainder 40; 64 ✗; 32 ✓ (1) → remainder 8; 16 ✗; 8 ✓ (1); remainder 0.  
Result = 10101000₂.

## Common Mistakes
- Forgetting to pad octets to 8 bits.  
- Misordering bit weights.  

## Quick Checks
- Convert 00001010₂ to decimal.  
- Convert 11₁₀ to 8-bit binary.  

## Connections
- Builds on: [[Networking – Number Systems Overview & Positional Notation]]  
- Leads to: [[Hex & IPv6/MAC – Conversions and Rules]]