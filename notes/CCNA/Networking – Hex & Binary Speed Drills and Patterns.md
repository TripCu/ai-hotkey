---
title: "Networking – Hex & Binary Speed Drills and Patterns"
tags: ["networking", "hexadecimal", "binary", "reference", "practice", "module5"]
source: ["ITN_Module_5.pptx.pdf"]
created: "2025-10-29"
summary: "Quick-reference tables and mental-math shortcuts for converting binary, decimal, and hex."
---

> [!Abstract]
> Memorizing nibble-to-hex mappings and octet weights allows near-instant conversion—crucial for subnetting and address decoding.

## Nibble ↔ Hex Table
| Binary | Hex | Binary | Hex | Binary | Hex | Binary | Hex |
|:------:|:--:|:------:|:--:|:------:|:--:|:------:|:--:|
|0000|0|0100|4|1000|8|1100|C|
|0001|1|0101|5|1001|9|1101|D|
|0010|2|0110|6|1010|A|1110|E|
|0011|3|0111|7|1011|B|1111|F|

## Common Octet Weights and Sums
128, 64, 32, 16, 8, 4, 2, 1  
Typical subnet masks:
- 192 = 128+64  
- 224 = 128+64+32  
- 240 = 128+64+32+16  
- 248 = 128+64+32+16+8  
- 252 = 128+64+32+16+8+4  
- 254 = 128+64+32+16+8+4+2  
- 255 = all ones  

## Rapid Practice
- Convert 0b11110000 → decimal and hex.  
- Convert 210₁₀ → binary and hex.  
- Convert 10101100₂ → decimal.  

## Tips
- Group binary in fours to read hex instantly.  
- For decimal → binary, subtract the largest fitting weight downward.  
- Recognize repeating mask patterns for subnet work.

## Connections
- Builds on: [[Hex & IPv6/MAC – Conversions and Rules]]  
- Related: [[Binary & IPv4 – Conversions and Practice]]
