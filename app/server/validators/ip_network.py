"""
Utilities for validating subnetting answers.

The validator is intentionally permissive: it scans text for CIDR-like
substrings, parses them with :mod:`ipaddress`, and reports structured
details that the backend can include alongside LLM output.
"""

from __future__ import annotations

import ipaddress
import re
from typing import Dict, List, Union

CIDR_PATTERN = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}/\d{1,2}\b")

IPv4Network = ipaddress.IPv4Network
IPv6Network = ipaddress.IPv6Network
IPAddress = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
IPNetwork = Union[IPv4Network, IPv6Network]


def parse_network(token: str) -> IPNetwork:
    """Parse a CIDR, tolerating host addresses (strict=False)."""
    network = ipaddress.ip_network(token, strict=False)
    return network


def first_host(network: IPNetwork) -> IPAddress:
    """Return the first usable host. Falls back to network address if none."""
    if network.num_addresses <= 2:
        return network.network_address
    return network.network_address + 1


def last_host(network: IPNetwork) -> IPAddress:
    """Return the last usable host. Falls back to broadcast/network as needed."""
    if network.num_addresses <= 2:
        return network.broadcast_address
    return network.broadcast_address - 1


def network_summary(network: IPNetwork) -> Dict[str, str]:
    """Compute a summary of network details for reporting."""
    summary = {
        "cidr": str(network.with_prefixlen),
        "network": str(network.network_address),
        "prefix_length": str(network.prefixlen),
        "first_host": str(first_host(network)),
        "last_host": str(last_host(network)),
    }
    if isinstance(network, IPv4Network):
        summary["broadcast"] = str(network.broadcast_address)
    return summary


def validate_answer(text: str) -> Dict[str, object]:
    """
    Inspect the provided text (typically an Answer: line) for CIDR networks.

    Returns a structure describing the parsed networks, along with any notes or
    errors. No exceptions are raised; callers receive ``ok=False`` if parsing fails.
    """
    matches = CIDR_PATTERN.findall(text or "")
    if not matches:
        return {"ok": False, "reason": "No CIDR networks detected in answer."}

    summaries: List[Dict[str, str]] = []
    for token in matches:
        try:
            network = parse_network(token)
            summaries.append(network_summary(network))
        except ValueError as exc:
            return {"ok": False, "reason": f"Invalid CIDR '{token}': {exc}"}

    return {"ok": True, "networks": summaries}
