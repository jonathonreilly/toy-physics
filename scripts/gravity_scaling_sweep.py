#!/usr/bin/env python3
"""Test whether the gravity decay rate α decreases on larger grids.

In the 2D continuum limit, the Laplace Green's function ∝ -ln(r)/2π.
On a finite grid of size L, the effective decay is approximately
exponential with α ∝ π/L. So α should decrease as 1/L.

If confirmed: the model's gravity becomes longer-range on larger
networks, approaching continuum-like behavior at scale.

Also tests the self-maintenance rule viability boundary by checking
which persistent-node configurations produce nonzero support.

PStack experiments: gravity-scaling, self-maintenance-viability
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
    derive_persistence_support,
)


def measure_decay_rate(
    width: int, height: int, mass_x: int, mass_center_y: int, n_mass_nodes: int,
) -> tuple[float, list[tuple[int, float]]]:
    """Measure the field decay rate along +x from a mass cluster.
    Returns (estimated alpha, [(distance, field_value), ...])."""
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    ys = list(range(mass_center_y - (n_mass_nodes - 1) // 2,
                    mass_center_y + n_mass_nodes // 2 + 1))[:n_mass_nodes]
    pnodes = frozenset((mass_x, y) for y in ys)
    rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
    nodes = build_rectangular_nodes(width=width, height=height)
    field = derive_node_field(nodes, rule)

    # Measure along +x from mass center at y = mass_center_y - 3 (off-axis to avoid source)
    measure_y = 0  # measure at y=0 which is below mass for all configs
    data = []
    for step in range(1, width):
        x = mass_x + step
        if x > width:
            break
        f = field.get((x, measure_y), 0.0)
        if f > 0:
            data.append((step, f))

    # Fit alpha from mid-range data (avoid near-field and boundary)
    if len(data) >= 4:
        # Use the middle third of points
        start = len(data) // 4
        end = 3 * len(data) // 4
        mid_data = data[start:end]
        if len(mid_data) >= 2:
            # Linear fit of ln(field) vs distance
            n = len(mid_data)
            sum_r = sum(r for r, _ in mid_data)
            sum_lnf = sum(math.log(f) for _, f in mid_data)
            sum_r2 = sum(r * r for r, _ in mid_data)
            sum_r_lnf = sum(r * math.log(f) for r, f in mid_data)
            denom = n * sum_r2 - sum_r * sum_r
            if denom != 0:
                alpha = -(n * sum_r_lnf - sum_r * sum_lnf) / denom
                return alpha, data

    return 0.0, data


def main() -> None:
    print("=" * 72)
    print("GRAVITY SCALING SWEEP: decay rate vs grid size")
    print("=" * 72)
    print()

    # =========================================================
    # SWEEP 1: Vary grid size, measure decay rate
    # =========================================================
    print("SWEEP 1: Alpha vs grid size (5 mass nodes at grid center)")
    print()

    configs = [
        (20, 8),
        (30, 12),
        (40, 16),
        (60, 24),
        (80, 32),
        (100, 40),
    ]

    print(f"{'width':>6s}  {'height':>6s}  {'L_eff':>6s}  {'alpha':>10s}  {'pi/L':>10s}  "
          f"{'alpha*L':>10s}  {'field_at_5':>10s}  {'field_at_10':>10s}")
    print("-" * 78)

    for w, h in configs:
        mass_x = w // 2
        mass_y = h // 2
        alpha, data = measure_decay_rate(w, h, mass_x, mass_y, 5)
        L_eff = min(w, 2 * h)  # effective size (height limits vertical extent)
        pi_over_L = math.pi / L_eff

        f_at_5 = next((f for r, f in data if r == 5), 0.0)
        f_at_10 = next((f for r, f in data if r == 10), 0.0)

        print(f"{w:6d}  {h:6d}  {L_eff:6d}  {alpha:10.6f}  {pi_over_L:10.6f}  "
              f"{alpha * L_eff:10.4f}  {f_at_5:10.6f}  {f_at_10:10.6f}")

    # =========================================================
    # SWEEP 2: Full radial profile at each grid size
    # =========================================================
    print()
    print("=" * 72)
    print("SWEEP 2: Radial field profiles at selected grid sizes")
    print("=" * 72)

    for w, h in [(20, 8), (40, 16), (80, 32)]:
        mass_x = w // 2
        mass_y = h // 2
        alpha, data = measure_decay_rate(w, h, mass_x, mass_y, 5)

        print(f"\n  Grid {w}x{2*h}, alpha={alpha:.6f}:")
        print(f"  {'r':>4s}  {'field':>12s}  {'ln(field)':>10s}  {'ratio':>8s}")
        print(f"  {'-' * 40}")
        prev_f = None
        for r, f in data[:20]:
            lnf = math.log(f)
            ratio = f / prev_f if prev_f else 0.0
            print(f"  {r:4d}  {f:12.8f}  {lnf:10.4f}  {ratio:8.4f}")
            prev_f = f

    # =========================================================
    # SWEEP 3: Self-maintenance viability — which configs give nonzero support?
    # =========================================================
    print()
    print("=" * 72)
    print("SWEEP 3: Self-maintenance viability boundary")
    print("=" * 72)
    print()
    print("Which persistent-node configurations produce nonzero support?")
    print("Support = fraction of neighbors that are also persistent.")
    print()

    w, h = 20, 10
    nodes = build_rectangular_nodes(width=w, height=h)

    # Test various configurations
    test_configs = [
        ("1 isolated node", frozenset([(10, 0)])),
        ("2 adjacent (horizontal)", frozenset([(10, 0), (11, 0)])),
        ("2 adjacent (vertical)", frozenset([(10, 0), (10, 1)])),
        ("2 adjacent (diagonal)", frozenset([(10, 0), (11, 1)])),
        ("2 separated by 1", frozenset([(10, 0), (12, 0)])),
        ("2 separated by 2", frozenset([(10, 0), (13, 0)])),
        ("3 line (horizontal)", frozenset([(10, 0), (11, 0), (12, 0)])),
        ("3 line (vertical)", frozenset([(10, 0), (10, 1), (10, 2)])),
        ("3 L-shape", frozenset([(10, 0), (11, 0), (10, 1)])),
        ("3 triangle", frozenset([(10, 0), (11, 0), (11, 1)])),
        ("4 square", frozenset([(10, 0), (11, 0), (10, 1), (11, 1)])),
        ("4 line", frozenset([(10, 0), (11, 0), (12, 0), (13, 0)])),
        ("5 cross", frozenset([(10, 0), (11, 0), (9, 0), (10, 1), (10, -1)])),
        ("5 line", frozenset([(10, 0), (11, 0), (12, 0), (13, 0), (14, 0)])),
        ("1 at corner", frozenset([(0, -h)])),
        ("2 at corner", frozenset([(0, -h), (1, -h)])),
        ("1 at edge", frozenset([(0, 0)])),
        ("2 at edge", frozenset([(0, 0), (1, 0)])),
    ]

    print(f"{'config':>25s}  {'max_support':>12s}  {'total_support':>14s}  {'nonzero':>8s}")
    print("-" * 65)

    for label, pnodes in test_configs:
        support = derive_persistence_support(nodes, pnodes)
        max_s = max(support.values())
        total_s = sum(support.values())
        nonzero = sum(1 for v in support.values() if v > 0)
        print(f"{label:>25s}  {max_s:12.6f}  {total_s:14.6f}  {nonzero:8d}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
