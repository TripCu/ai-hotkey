---
title: "Networking – Number Systems Overview & Positional Notation"
tags: ["networking", "number-systems", "binary", "decimal", "hex", "positional-notation", "module5"]
source: ["ITN_Module_5.pptx.pdf"]
created: "2025-10-29"
summary: "Introduces why networks use binary, how positional notation works, and where decimal and hex fit in."
---
---
title: "Networking – Number Systems Overview & Positional Notation"
tags: ["networking", "number-systems", "binary", "decimal", "hexadecimal", "module5"]
source: ["ITN_Module_5.pptx.pdf"]
created: "2025-10-29"
summary: "Introduces why networking uses binary, how positional notation works, and how decimal and hexadecimal relate."
---

> [!Abstract]
> Networking relies on multiple numbering systems—binary for machine processing, decimal for human readability, and hexadecimal for compact notation. Understanding positional notation allows quick conversions between them.

## Key Ideas
- Computers and networking devices operate using **binary** (base 2).  
- Humans communicate in **decimal** (base 10).  
- IPv6 and MAC addresses use **hexadecimal** (base 16).  
- **Positional notation** determines a digit’s value by its base and position.

## Definitions
- **Radix (Base):** Number of unique digits in a system.  
- **Bit:** Smallest data unit (0 or 1).  
- **Octet:** 8 bits; used in IPv4.  
- **Nibble:** 4 bits; maps to one hexadecimal digit.  
- **Hextet:** 16 bits; used in IPv6 addressing.

## Explanation
In positional notation, each digit’s value = digit × (base raised to its position).

Examples:  
- Decimal 1234 = 1×10³ + 2×10² + 3×10¹ + 4×10⁰ = 1234  
- Binary 11000000 = 1×2⁷ + 1×2⁶ = 192  

Binary counts double each time you move left, while hexadecimal counts in groups of four bits (0000–1111 = 0–F).

## Common Mistakes
- Ignoring leading zeros in binary.  
- Mixing up digit values with positional weights.  

## Quick Checks
- Why is 1000₂ equal to 8₁₀?  
- How many values can one hexadecimal digit represent?  

## Connections
- Leads to: [[Binary & IPv4 – Conversions and Practice]]  
- Related: [[Hex & IPv6/MAC – Conversions and Rules]]