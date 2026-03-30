#!/usr/bin/env python3
"""Compare the model's delay field to the discrete Laplace Green's function.

The delay field is computed by derive_node_field() via iterative
relaxation: field[node] = support[node] + (1-support[node]) * avg(neighbors).
On a finite grid with zero boundary conditions, this converges to
the discrete Green's function of the Laplacian.

This script computes the field directly, measures it along various
cross-sections, and compares to the theoretical 2D discrete Green's
function behavior (logarithmic falloff in the interior, with
finite-size corrections at boundaries).

PStack experiment: gravity-field-theory
"""

from __future__ import annotations
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
)


def main() -> None:
    width = 40
    height = 16
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    print("=" * 72)
    print("GRAVITY FIELD THEORY COMPARISON")
    print("=" * 72)
    print(f"width={width}, height={height}")
    print()

    # =========================================================
    # SINGLE SOURCE: 5 persistent nodes at center
    # =========================================================
    pnodes = frozenset((20, y) for y in [3, 4, 5, 6, 7])
    rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
    nodes = build_rectangular_nodes(width=width, height=height)
    field = derive_node_field(nodes, rule)

    print("=" * 72)
    print("FIELD MAP: 5 persistent nodes at x=20, y=3..7")
    print("=" * 72)
    print()

    # Cross-section along x at y=0 (below the mass)
    print("Cross-section: y=0 (below mass at y=5)")
    print(f"{'x':>4s}  {'field':>12s}  {'ln(field)':>10s}  bar")
    print("-" * 50)
    for x in range(0, width + 1, 2):
        f = field.get((x, 0), 0.0)
        lnf = math.log(f) if f > 0 else float("-inf")
        bar = "#" * int(f * 200)
        print(f"{x:4d}  {f:12.8f}  {lnf:10.4f}  {bar}")

    # Cross-section along y at x=20 (through the mass)
    print()
    print("Cross-section: x=20 (through mass)")
    print(f"{'y':>4s}  {'field':>12s}  {'dist_to_mass':>12s}  bar")
    print("-" * 55)
    mass_center_y = 5.0
    for y in range(-height, height + 1):
        f = field.get((20, y), 0.0)
        dist = abs(y - mass_center_y)
        bar = "#" * int(f * 100)
        marker = " <-- mass" if 3 <= y <= 7 else ""
        print(f"{y:4d}  {f:12.8f}  {dist:12.1f}  {bar}{marker}")

    # Cross-section along y at x=10 (10 units from mass)
    print()
    print("Cross-section: x=10 (10 units from mass x-position)")
    print(f"{'y':>4s}  {'field':>12s}  {'dist_to_mass':>12s}  bar")
    print("-" * 55)
    for y in range(-height, height + 1):
        f = field.get((10, y), 0.0)
        dist = math.sqrt((10 - 20) ** 2 + (y - mass_center_y) ** 2)
        bar = "#" * int(f * 300)
        print(f"{y:4d}  {f:12.8f}  {dist:12.2f}  {bar}")

    # =========================================================
    # RADIAL FALLOFF from mass center
    # =========================================================
    print()
    print("=" * 72)
    print("RADIAL FALLOFF from mass center (20, 5)")
    print("=" * 72)
    print()

    # Sample field at various distances along several directions
    directions = [
        ("right (+x)", (1, 0)),
        ("left (-x)", (-1, 0)),
        ("up (+y)", (0, 1)),
        ("down (-y)", (0, -1)),
        ("diagonal (+x,+y)", (1, 1)),
        ("diagonal (+x,-y)", (1, -1)),
    ]

    for dir_label, (dx, dy) in directions:
        print(f"Direction: {dir_label}")
        print(f"{'dist':>6s}  {'field':>12s}  {'ln(field)':>10s}  {'field*dist':>12s}  {'field*dist^2':>12s}")
        print("-" * 60)
        for step in range(1, 16):
            x = 20 + dx * step
            y = 5 + dy * step  # mass center
            if (x, y) not in field:
                break
            f = field[(x, y)]
            if f <= 0:
                continue
            d = math.sqrt(dx * dx + dy * dy) * step
            lnf = math.log(f)
            print(f"{d:6.2f}  {f:12.8f}  {lnf:10.4f}  {f * d:12.6f}  {f * d * d:12.6f}")
        print()

    # =========================================================
    # FUNCTIONAL FORM TEST: is field ~ 1/r, ln(r), or 1/r^2?
    # =========================================================
    print("=" * 72)
    print("FUNCTIONAL FORM TEST")
    print("=" * 72)
    print()
    print("In 2D, the discrete Laplace Green's function ∝ -ln(r)/2π for large r.")
    print("On a finite grid with zero BCs, it deviates near boundaries.")
    print()

    # Use the +x direction (most data points before hitting boundary)
    print("Test along +x direction from mass center:")
    print(f"{'r':>6s}  {'field':>12s}  {'-ln(r)/2π':>12s}  {'ratio':>10s}  {'field/(-lnr)':>12s}")
    print("-" * 60)
    data_x = []
    for step in range(1, 20):
        x = 20 + step
        y = 5
        if (x, y) not in field:
            break
        f = field[(x, y)]
        r = float(step)
        if f > 0 and r > 0:
            theory = -math.log(r) / (2 * math.pi) if r > 1 else 0.5
            ratio = f / theory if theory > 0 else float("inf")
            f_over_lnr = f / (-math.log(r)) if r > 1 else float("nan")
            data_x.append((r, f, theory, ratio))
            print(f"{r:6.1f}  {f:12.8f}  {theory:12.8f}  {ratio:10.4f}  "
                  f"{f_over_lnr:12.8f}" if r > 1 else
                  f"{r:6.1f}  {f:12.8f}  {'N/A':>12s}  {'N/A':>10s}  {'N/A':>12s}")

    # Successive ratio test on +x direction
    print()
    print("Successive ratio test (field[r+1] / field[r]) along +x:")
    prev_f = None
    for step in range(1, 20):
        x = 20 + step
        if (x, 5) not in field:
            break
        f = field[(x, 5)]
        if prev_f is not None and prev_f > 0:
            print(f"  r={step}: {f/prev_f:.6f}")
        prev_f = f

    print()
    print("COMPARISON COMPLETE")


if __name__ == "__main__":
    main()
