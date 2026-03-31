#!/usr/bin/env python3
"""Field-coupled CA v2: mass placed along glider's path.

v1 placed the mass far from the glider (x=40 vs glider at x=10).
The field was negligible at the glider's location. v2 places the
mass at (25, 0) — directly in the glider's path neighborhood.
The glider travels from (10,10) toward (+x,-y) and passes near
(25,0) around step 60.

Also tests a subtler coupling: field biases the CA by adding a
fractional effective neighbor in the field gradient direction,
rather than shifting the total count.

PStack experiment: field-coupled-ca-v2
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


def evolve_gradient_coupled(
    nodes, active, base_survive, base_birth, lookup, field,
    coupling, steps,
):
    """CA where the field gradient biases birth direction.

    Instead of shifting effective count (v1), the field gradient
    determines a preferred direction. Birth probability in the
    gradient direction is enhanced; birth against the gradient
    is suppressed.

    Implemented: a node in the birth zone gets born if count is
    in base_birth OR if count == max(base_birth)-1 AND the node
    is "downhill" in the field (toward higher field = toward mass).
    """
    history = []
    for _ in range(steps):
        history.append(frozenset(active))

        counts: dict[tuple[int, int], int] = defaultdict(int)
        for node in active:
            for nb in lookup[node]:
                counts[nb] += 1

        new_active = set()
        candidates = set(active)
        for node in active:
            candidates.update(lookup[node])

        for node in candidates:
            c = counts.get(node, 0)

            if node in active:
                if c in base_survive:
                    new_active.add(node)
            else:
                if c in base_birth:
                    new_active.add(node)
                elif coupling > 0:
                    # Enhanced birth: if count is one below the birth
                    # threshold AND this node has higher field than
                    # the average of its active neighbors
                    threshold_minus_1 = frozenset(b - 1 for b in base_birth if b > 0)
                    if c in threshold_minus_1:
                        my_field = field.get(node, 0.0)
                        active_nbs = [nb for nb in lookup[node] if nb in active]
                        if active_nbs:
                            avg_nb_field = sum(field.get(nb, 0) for nb in active_nbs) / len(active_nbs)
                            if my_field > avg_nb_field + coupling * 0.01:
                                new_active.add(node)

        active = new_active

    return history


def centroid(state):
    if not state:
        return (0.0, 0.0)
    return (sum(x for x, _ in state) / len(state),
            sum(y for _, y in state) / len(state))


def main() -> None:
    width = 60
    height = 25
    steps = 80
    nodes = build_rectangular_nodes(width=width, height=height)
    lookup = build_graph_neighbor_lookup(nodes)

    survive = frozenset({2, 3})
    birth = frozenset({3})
    glider = frozenset([(10, 10), (11, 10), (12, 10), (12, 11), (11, 12)])

    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    print("=" * 80)
    print("FIELD-COUPLED CA v2: Gradient coupling, mass near glider path")
    print("=" * 80)
    print()

    # Control
    zero_field = {n: 0.0 for n in nodes}
    control = evolve_gradient_coupled(
        nodes, set(glider), survive, birth, lookup, zero_field, 0.0, steps
    )
    ctrl_c = [centroid(s) for s in control]
    print(f"CONTROL: ({ctrl_c[0][0]:.1f},{ctrl_c[0][1]:.1f}) → "
          f"({ctrl_c[-1][0]:.1f},{ctrl_c[-1][1]:.1f}), size={len(control[-1])}")

    # Mass configurations along the glider's path
    # Glider moves from (10,10) toward (30,-10) approximately
    # Place masses at different offsets from this path

    mass_configs = [
        ("mass at (20, 5) — path side", frozenset((20, y) for y in range(3, 8))),
        ("mass at (20, -5) — opposite side", frozenset((20, y) for y in range(-7, -2))),
        ("mass at (20, 0) — below path", frozenset((20, y) for y in range(-2, 3))),
        ("mass at (15, 5) — near, path side", frozenset((15, y) for y in range(3, 8))),
        ("mass at (25, 0) — far, below path", frozenset((25, y) for y in range(-2, 3))),
    ]

    for coupling in [0.0, 1.0, 5.0, 10.0]:
        print(f"\n  Coupling = {coupling}:")
        print(f"  {'mass':>30s}  {'final_x':>8s}  {'final_y':>8s}  {'size':>6s}  "
              f"{'dy_from_ctrl':>12s}  {'toward?':>7s}")
        print(f"  {'-' * 76}")

        for label, mass_nodes in mass_configs:
            rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
            field = derive_node_field(nodes, rule)

            history = evolve_gradient_coupled(
                nodes, set(glider), survive, birth, lookup,
                field, coupling, steps,
            )
            c_final = centroid(history[-1])
            size = len(history[-1])

            if size > 0:
                dy = c_final[1] - ctrl_c[-1][1]
                # Is the mass above or below the control path endpoint?
                mass_cy = sum(y for _, y in mass_nodes) / len(mass_nodes)
                toward = "YES" if (mass_cy > ctrl_c[-1][1] and dy > 0.5) or \
                                  (mass_cy < ctrl_c[-1][1] and dy < -0.5) else "NO"
                print(f"  {label:>30s}  {c_final[0]:8.1f}  {c_final[1]:8.1f}  {size:6d}  "
                      f"{dy:+12.1f}  {toward:>7s}")
            else:
                print(f"  {label:>30s}  {'DEAD':>8s}  {'':>8s}  {0:6d}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
