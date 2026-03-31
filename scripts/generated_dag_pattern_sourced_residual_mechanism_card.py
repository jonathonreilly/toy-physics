#!/usr/bin/env python3
"""Render the retained mover-lane residual mechanism card.

This is the compact architecture artifact after the wide / self:sparse-25
crosswalk. It is intentionally small and declarative: the goal is to preserve
the retained mechanism map, not to reopen search.
"""

from __future__ import annotations


def main() -> None:
    print("=" * 80)
    print("GENERATED DAG PATTERN-SOURCED RESIDUAL MECHANISM CARD")
    print("=" * 80)
    print()
    print("Base mover substrate")
    print("  coherent mover substrate: neighbor_radius = 2.5")
    print("  retained static coupling: 3.0")
    print("  retained source footprint: last3_union")
    print("  effect: pattern-sourced steering is viable and toward-source on average")
    print()
    print("Over-broad source footprint failure")
    print("  failure trigger: replacing last3_union with last6_union")
    print("  generic effect: sign can flip from toward-source to away-shift / retiming")
    print("  shared abstract language: forward-packet retiming")
    print()
    print("Retained residual branches")
    print("  branch A: wide-rule low-added-packet-field")
    print("    mechanism: added last4-6 support exists but does not project enough extra field onto the tracked packet")
    print("    retained hint: extra_field_mean_on_packet <= 0.0010")
    print("  branch B: self:sparse-25 forward-corridor collapse")
    print("    mechanism: added last4-6 support stops contributing forward corridor support and forward-side balance")
    print("    retained hints: extra_support_corridor_share <= 0.0000, extra_support_forward_share <= 0.1429, extra_packet_side_gap <= 0.0000")
    print()
    print("What did not retain")
    print("  no universal late-support scalar closes both residual branches cleanly")
    print("  pooled forward-family rules exist, but they stay weaker than the branch-local stories")
    print()
    print("Current architecture")
    print("  one shared family: forward-packet retiming")
    print("  two residual mechanisms: wide low packet-field, self:sparse corridor collapse")
    print()
    print("Next step")
    print("  use this card as the retained map before any further local threshold shaving")


if __name__ == "__main__":
    main()
