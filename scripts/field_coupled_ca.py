#!/usr/bin/env python3
"""Field-coupled CA: birth/survival depends on local delay field.

The current model has two uncoupled layers:
  CA rule (pattern evolution) ← does NOT see the field
  Field (delay/gravity)       ← IS sourced by the CA pattern

This prototype couples them: the CA rule's effective birth/survival
thresholds shift based on the local field value. In a high-field
region (near a mass), nodes need fewer neighbors to survive and
more neighbors to be born (or vice versa).

If this coupling produces gravitational deflection of moving
patterns, the model's two dynamics layers become ONE.

PStack experiment: field-coupled-ca
"""

from __future__ import annotations
import math
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    build_rectangular_nodes,
    build_graph_neighbor_lookup,
    RulePostulates,
    derive_local_rule,
    derive_node_field,
)


def evolve_field_coupled(
    nodes: set[tuple[int, int]],
    active: set[tuple[int, int]],
    base_survive: frozenset[int],
    base_birth: frozenset[int],
    neighbor_lookup: dict,
    field: dict[tuple[int, int], float],
    coupling_strength: float,
    steps: int,
) -> list[frozenset[tuple[int, int]]]:
    """CA evolution where the field modifies effective thresholds.

    At each node, the effective neighbor count is:
      effective_count = actual_count + coupling_strength * field[node]

    So in high-field regions (near a mass), nodes "feel" more neighbors
    than they actually have → easier to survive, easier to be born
    (shifted toward higher effective counts).

    The field attracts patterns by making survival easier in the
    field's direction.
    """
    history = []
    for _ in range(steps):
        history.append(frozenset(active))

        # Count neighbors
        counts: dict[tuple[int, int], int] = defaultdict(int)
        for node in active:
            for nb in neighbor_lookup[node]:
                counts[nb] += 1

        new_active = set()
        candidates = set(active)
        for node in active:
            candidates.update(neighbor_lookup[node])

        for node in candidates:
            actual_count = counts.get(node, 0)
            f = field.get(node, 0.0)
            effective_count = actual_count + coupling_strength * f

            # Round to nearest int for threshold comparison
            eff_int = round(effective_count)

            if node in active and eff_int in base_survive:
                new_active.add(node)
            elif node not in active and eff_int in base_birth:
                new_active.add(node)

        active = new_active

    return history


def centroid(state):
    if not state:
        return (0.0, 0.0)
    return (sum(x for x, _ in state) / len(state),
            sum(y for _, y in state) / len(state))


def main() -> None:
    width = 80
    height = 30
    steps = 80
    nodes = build_rectangular_nodes(width=width, height=height)
    lookup = build_graph_neighbor_lookup(nodes)

    survive = frozenset({2, 3})
    birth = frozenset({3})

    # Glider seed (translates on uncoupled Life)
    glider = frozenset([(10, 10), (11, 10), (12, 10), (12, 11), (11, 12)])

    # Stationary mass (2x2 block, stable under Life)
    mass_block = frozenset([(40, 0), (41, 0), (40, 1), (41, 1)])

    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    print("=" * 80)
    print("FIELD-COUPLED CA: Gravity affects pattern evolution")
    print("=" * 80)
    print()

    # =========================================================
    # CONTROL: Uncoupled glider (coupling=0)
    # =========================================================
    print("CONTROL: Uncoupled glider (coupling=0, no mass)")
    zero_field = {n: 0.0 for n in nodes}
    control = evolve_field_coupled(
        nodes, set(glider), survive, birth, lookup,
        zero_field, coupling_strength=0.0, steps=steps,
    )
    control_centroids = [centroid(s) for s in control]
    print(f"  Step 0: ({control_centroids[0][0]:.1f}, {control_centroids[0][1]:.1f}), size={len(control[0])}")
    print(f"  Step 80: ({control_centroids[-1][0]:.1f}, {control_centroids[-1][1]:.1f}), size={len(control[-1])}")
    print()

    # =========================================================
    # TEST: Sweep coupling strength with a mass
    # =========================================================
    # Build field from a LARGE persistent mass
    mass_nodes = frozenset((40, y) for y in range(-5, 6))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)

    print("SWEEP: coupling_strength with mass at x=40, y=[-5,5]")
    print(f"  Glider starts at (10,10), normally moves toward (+x,-y)")
    print()

    print(f"{'coupling':>9s}  {'final_x':>8s}  {'final_y':>8s}  {'final_size':>10s}  "
          f"{'dx_from_ctrl':>12s}  {'dy_from_ctrl':>12s}  {'deflection':>10s}")
    print("-" * 76)

    for coupling in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, -1.0, -2.0]:
        history = evolve_field_coupled(
            nodes, set(glider), survive, birth, lookup,
            mass_field, coupling_strength=coupling, steps=steps,
        )
        centroids = [centroid(s) for s in history]
        sizes = [len(s) for s in history]

        if sizes[-1] > 0:
            fx, fy = centroids[-1]
            cx, cy = control_centroids[-1]
            dx = fx - cx
            dy = fy - cy
            defl = math.sqrt(dx**2 + dy**2)

            print(f"{coupling:9.1f}  {fx:8.1f}  {fy:8.1f}  {sizes[-1]:10d}  "
                  f"{dx:+12.1f}  {dy:+12.1f}  {defl:10.2f}")
        else:
            print(f"{coupling:9.1f}  {'DEAD':>8s}  {'':>8s}  {0:10d}")

    # =========================================================
    # TEST 2: Does coupling produce deflection TOWARD the mass?
    # =========================================================
    print()
    print("=" * 80)
    print("TEST 2: Direction of deflection")
    print("  Mass at (40, y_mass). Glider at (10, 10).")
    print("  Does the glider bend TOWARD the mass?")
    print("=" * 80)
    print()

    coupling = 2.0
    print(f"  Coupling = {coupling}")
    print(f"  {'mass_y':>7s}  {'final_x':>8s}  {'final_y':>8s}  {'dy_from_ctrl':>12s}  {'toward_mass?':>12s}")
    print(f"  {'-' * 52}")

    _, ctrl_cy = control_centroids[-1]

    for mass_y_center in [-10, -5, 0, 5, 10, 15, 20]:
        m_nodes = frozenset((40, y) for y in range(mass_y_center - 3, mass_y_center + 4))
        m_rule = derive_local_rule(persistent_nodes=m_nodes, postulates=postulates)
        m_field = derive_node_field(nodes, m_rule)

        history = evolve_field_coupled(
            nodes, set(glider), survive, birth, lookup,
            m_field, coupling_strength=coupling, steps=steps,
        )
        centroids = [centroid(s) for s in history]
        if len(history[-1]) > 0:
            fx, fy = centroids[-1]
            dy = fy - ctrl_cy
            toward = "YES" if (mass_y_center > ctrl_cy and dy > 0.5) or \
                              (mass_y_center < ctrl_cy and dy < -0.5) else "NO"
            print(f"  {mass_y_center:7d}  {fx:8.1f}  {fy:8.1f}  {dy:+12.1f}  {toward:>12s}")
        else:
            print(f"  {mass_y_center:7d}  {'DEAD':>8s}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
