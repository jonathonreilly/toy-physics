#!/usr/bin/env python3
"""Bounded action-power scaling sweep on one fixed 3D ordered-lattice family.

This harness is intentionally narrow. It freezes the strongest safe read we
currently have about action-power scaling:

  - 3D ordered dense lattice
  - h = 0.5, W = 10, L = 12
  - valley-style 1/L^2 propagator with h^2 measure
  - field f = s/r
  - action family S = L (1 - f^p)

What it is for:
  - verifying the bounded claim F~M ~= p on the fixed family
  - measuring how the post-peak distance tail steepens with p

What it is not:
  - a universal theorem over all graph families
  - a proof that the tail law is exact or architecture-independent
"""

from __future__ import annotations

import math

from action_universality_probe import Lattice3D, detector, measure_action


H = 0.5
PHYS_W = 10
PHYS_L = 12
POWERS = [0.5, 0.75, 1.0, 1.5, 2.0]


def fmt(x: float, places: int = 2) -> str:
    if math.isnan(x):
        return "nan"
    return f"{x:.{places}f}"


def main() -> None:
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = detector(lat)

    print("=" * 92)
    print("ACTION-POWER SCALING SWEEP")
    print("  Fixed 3D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, max_d={lat.max_d}")
    print("  Kernel: 1/L^2 with h^2 measure")
    print("  Field: s/r")
    print("  Action family: S = L (1 - f^p)")
    print("  Goal: bound the action-power universality-class claim on one family")
    print("=" * 92)
    print()
    print(
        f"{'p':>5} {'Born':>10} {'grav(z=3)':>12} {'TOWARD':>8} "
        f"{'F~M':>8} {'tail':>14} {'-(2p-1)':>10}"
    )
    print("-" * 92)

    rows = []
    for power in POWERS:
        mode = f"power:{power}"
        row = measure_action(lat, det, mode)
        rows.append((power, row))
        tail = "n/a"
        if not math.isnan(row.tail_slope):
            peak = f"z>={row.peak_z}" if row.peak_z is not None else "tail"
            tail = f"{peak}:{row.tail_slope:+.2f}"
        pred = -(2 * power - 1)
        print(
            f"{power:>5.2f} "
            f"{row.born:>10.2e} "
            f"{row.gravity_z3:>+12.6f} "
            f"{f'{row.toward_count}/7':>8s} "
            f"{fmt(row.fm_alpha):>8s} "
            f"{tail:>14s} "
            f"{pred:>10.2f}"
        )

    print()
    print("SAFE READ")
    print("  - On this fixed family, F~M tracks p closely across the tested powers.")
    print("  - Tail slopes steepen with p, but only the p >= 1 rows line up loosely with -(2p-1).")
    print("  - The strongest retained claim here is the mass-scaling universality class.")
    print("  - The distance-tail rule is still a bounded empirical pattern on one family.")


if __name__ == "__main__":
    main()
