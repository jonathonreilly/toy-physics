#!/usr/bin/env python3
"""Diagnostic companion for the continuum close path.

This script does not try to prove a new physics result. It estimates why the
current h-sweep is expensive and why the current open-boundary observable is
not the right one to carry the continuum claim by itself.

Use it to answer:
  - how fast does the effective 3D work grow as h shrinks?
  - how much extra work does h = 0.0625 impose relative to h = 0.125?
  - why is brute-force continuation the wrong first move on the present
    observable?

This is intentionally conservative: it is a diagnostic, not a claim.
"""

from __future__ import annotations

REF_H = 0.125
REF_NODES = 2_267_569  # retained 3D h=0.125 run from CONTINUUM_LIMIT_NOTE.md
H_VALUES = [0.25, 0.125, 0.0625]


def node_ratio(h: float) -> float:
    return (REF_H / h) ** 3


def work_proxy(h: float) -> float:
    # Conservative proxy: 3D node count times a refinement-depth factor.
    # The exact propagation cost depends on the runner, but this captures the
    # practical trend: smaller h means more nodes and more layers.
    return node_ratio(h) * (REF_H / h)


def main() -> None:
    print("CONTINUUM CLOSE PATH DIAGNOSTIC")
    print("=" * 72)
    print(f"Reference h: {REF_H}")
    print(f"Retained h=0.125 node count: {REF_NODES:,}")
    print()
    print(f"{'h':>8} {'node x ref':>12} {'est nodes':>14} {'work x ref':>12}")
    print("-" * 52)

    for h in H_VALUES:
        n_ratio = node_ratio(h)
        est_nodes = round(REF_NODES * n_ratio)
        print(
            f"{h:8.4f} {n_ratio:12.2f} {est_nodes:14,d} {work_proxy(h):12.2f}"
        )

    print()
    print("Interpretation:")
    print("- node count grows ~h^-3")
    print("- the conservative work proxy grows ~h^-4")
    print("- h=0.0625 is roughly 8x the nodes and 16x the work proxy of h=0.125")
    print("- the open-boundary observable already underflows by h=0.125")
    print("- so h=0.0625 is mainly a stress test unless the observable is changed")
    print()
    print("Recommended next step:")
    print("  per-node T normalization or equivalent boundary correction")
    print("  + weak-field deflection / source-mass response")
    print("  + Richardson ladder on h = 0.25, 0.125, 0.0625")


if __name__ == "__main__":
    main()
