#!/usr/bin/env python3
"""Test whether the (1-support) damping in derive_node_field causes
the gravity range plateau.

Hypothesis: The field relaxation rule
  field[n] = support[n] + (1-support[n]) * avg(neighbors)
is a screened Poisson equation. The screening mass m² ~ support
gives finite range ~1/m. Removing the damping (pure Laplacian)
should eliminate the plateau and recover α ~ π/L.

This script implements BOTH the original (damped) and an undamped
(pure Laplacian) field relaxation, then compares decay rates.

PStack experiment: gravity-damping-hypothesis
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
    derive_persistence_support,
    boundary_nodes,
    graph_neighbors,
)


def derive_undamped_field(
    nodes: set[tuple[int, int]],
    persistent_nodes: frozenset[tuple[int, int]],
    tolerance: float = 1e-8,
    max_iterations: int = 800,
) -> dict[tuple[int, int], float]:
    """Pure Laplacian relaxation: no (1-support) damping.

    At persistent nodes: field = 1.0 (Dirichlet BC, source)
    At boundary nodes: field = 0.0 (Dirichlet BC)
    At interior nodes: field = avg(neighbors) (Laplace equation)
    """
    support = derive_persistence_support(nodes, persistent_nodes)
    active = persistent_nodes & nodes

    field = {node: 0.0 for node in nodes}
    for node in active:
        field[node] = 1.0  # Fixed source

    boundaries = boundary_nodes(nodes)

    for _ in range(max_iterations):
        updated: dict[tuple[int, int], float] = {}
        max_change = 0.0
        for node in nodes:
            if node in boundaries:
                new_value = 0.0
            elif node in active:
                new_value = 1.0  # Pinned at source
            else:
                neighbors = graph_neighbors(node, nodes)
                new_value = sum(field[nb] for nb in neighbors) / len(neighbors)
            updated[node] = new_value
            max_change = max(max_change, abs(new_value - field[node]))
        field = updated
        if max_change < tolerance:
            break
    return field


def derive_damped_field(
    nodes: set[tuple[int, int]],
    persistent_nodes: frozenset[tuple[int, int]],
    tolerance: float = 1e-8,
    max_iterations: int = 800,
) -> dict[tuple[int, int], float]:
    """Original damped relaxation from derive_node_field."""
    support = derive_persistence_support(nodes, persistent_nodes)

    field = dict(support)
    boundaries = boundary_nodes(nodes)

    for _ in range(max_iterations):
        updated: dict[tuple[int, int], float] = {}
        max_change = 0.0
        for node in nodes:
            if node in boundaries:
                new_value = 0.0
            else:
                neighbors = graph_neighbors(node, nodes)
                avg_nb = sum(field[nb] for nb in neighbors) / len(neighbors)
                new_value = support[node] + (1.0 - support[node]) * avg_nb
            updated[node] = new_value
            max_change = max(max_change, abs(new_value - field[node]))
        field = updated
        if max_change < tolerance:
            break
    return field


def measure_alpha(field: dict, mass_x: int, measure_y: int, width: int) -> float:
    """Fit exponential decay rate from mid-range field values."""
    data = []
    for step in range(1, width):
        x = mass_x + step
        if (x, measure_y) in field and field[(x, measure_y)] > 1e-15:
            data.append((step, field[(x, measure_y)]))
    if len(data) < 4:
        return 0.0
    start = len(data) // 4
    end = 3 * len(data) // 4
    mid = data[start:end]
    if len(mid) < 2:
        return 0.0
    n = len(mid)
    sr = sum(r for r, _ in mid)
    slnf = sum(math.log(f) for _, f in mid)
    sr2 = sum(r*r for r, _ in mid)
    srlnf = sum(r * math.log(f) for r, f in mid)
    denom = n * sr2 - sr * sr
    if denom == 0:
        return 0.0
    return -(n * srlnf - sr * slnf) / denom


def main() -> None:
    print("=" * 72)
    print("GRAVITY DAMPING HYPOTHESIS TEST")
    print("=" * 72)
    print()
    print("Does the (1-support) damping cause the α plateau?")
    print("Compare: original (damped) vs pure Laplacian (undamped)")
    print()

    configs = [
        (20, 8),
        (30, 12),
        (40, 16),
        (60, 24),
        (80, 32),
        (100, 40),
        (140, 56),
    ]

    n_mass = 5

    print(f"{'width':>6s}  {'height':>6s}  {'L':>4s}  "
          f"{'α_damped':>10s}  {'α_undamped':>12s}  "
          f"{'αL_damped':>10s}  {'αL_undamped':>12s}  "
          f"{'π/L':>8s}")
    print("-" * 82)

    for w, h in configs:
        mass_x = w // 2
        mass_y = h // 2
        ys = list(range(mass_y - 2, mass_y + 3))
        pnodes = frozenset((mass_x, y) for y in ys)
        nodes = build_rectangular_nodes(width=w, height=h)
        L = min(w, 2 * h)

        damped = derive_damped_field(nodes, pnodes)
        undamped = derive_undamped_field(nodes, pnodes)

        alpha_d = measure_alpha(damped, mass_x, 0, w)
        alpha_u = measure_alpha(undamped, mass_x, 0, w)

        pi_L = math.pi / L

        print(f"{w:6d}  {h:6d}  {L:4d}  "
              f"{alpha_d:10.6f}  {alpha_u:12.6f}  "
              f"{alpha_d * L:10.4f}  {alpha_u * L:12.4f}  "
              f"{pi_L:8.6f}")

    # Detailed radial comparison at one grid size
    print()
    print("=" * 72)
    print("RADIAL COMPARISON at width=60, height=24")
    print("=" * 72)
    print()

    w, h = 60, 24
    mass_x = w // 2
    mass_y = h // 2
    ys = list(range(mass_y - 2, mass_y + 3))
    pnodes = frozenset((mass_x, y) for y in ys)
    nodes = build_rectangular_nodes(width=w, height=h)

    damped = derive_damped_field(nodes, pnodes)
    undamped = derive_undamped_field(nodes, pnodes)

    print(f"  {'r':>4s}  {'damped':>12s}  {'undamped':>12s}  {'ratio':>10s}  {'ln_d':>10s}  {'ln_u':>10s}")
    print(f"  {'-' * 62}")

    for step in range(1, 30):
        x = mass_x + step
        fd = damped.get((x, 0), 0.0)
        fu = undamped.get((x, 0), 0.0)
        if fd > 0 and fu > 0:
            print(f"  {step:4d}  {fd:12.8f}  {fu:12.8f}  {fu/fd:10.4f}  "
                  f"{math.log(fd):10.4f}  {math.log(fu):10.4f}")

    print()
    print("If αL_undamped ≈ π: pure Laplacian recovers continuum scaling.")
    print("If αL_damped plateaus while αL_undamped grows linearly: damping IS the cause.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
