#!/usr/bin/env python3
"""Analytical derivation: why is gravitational deflection threshold-like?

The centroid shift depends on the ASYMMETRY of the probability
distribution, not just the total action deficit. Even if ΔS varies
with b, the shift can be b-independent if the probability distribution
shape is determined by the DIRECTION of the gradient, not its magnitude.

Key insight: in the path-sum, the centroid shift is determined by
the RELATIVE phase between paths above and below the beam center.
If the field gradient points in a fixed direction (toward mass),
the phase difference between adjacent y-positions is:
  Δφ(y) = k × [S(y+1) - S(y)] ≈ k × ∂S/∂y

The centroid shift is maximized when Δφ ≈ π (destructive interference
on one side). Once the gradient is strong enough for Δφ > π, the
shift SATURATES — it can't exceed the beam width.

This predicts:
- At weak coupling (small k or small field): shift ∝ k² × gradient
- At strong coupling: shift saturates at ±height (beam width limit)
- The transition happens at k × ∂S/∂y ≈ π

Test: verify the saturation point numerically.

PStack experiment: threshold-deflection-theory
"""

from __future__ import annotations
import math
import cmath
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
    local_edge_properties,
)


def propagate_and_measure(nodes, source, field, k, det_x, screen_ys):
    post = RulePostulates(phase_per_action=k, attenuation_power=1.0,
                          attenuation_mode="geometry")
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=post)
    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)

    amps = {source: 1.0+0.0j}
    for node in order:
        if node not in amps:
            continue
        a = amps[node]
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            lf = 0.5*(field.get(node, 0.0)+field.get(nb, 0.0))
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret
            ea = cmath.exp(1j*k*act)/(L**1.0)
            if nb not in amps:
                amps[nb] = 0.0+0.0j
            amps[nb] += a*ea

    probs = {}
    total = 0
    for y in screen_ys:
        p = abs(amps.get((det_x, y), 0.0))**2
        probs[y] = p
        total += p
    if total > 0:
        probs = {y: p/total for y, p in probs.items()}

    centroid = sum(y*p for y, p in probs.items())
    return centroid, probs


def main():
    width = 60
    height = 25
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height+1))
    det_x = 50

    mass_nodes = frozenset((30, y) for y in range(4, 9))
    post = RulePostulates(phase_per_action=1.0, attenuation_power=1.0,
                          attenuation_mode="geometry")
    rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=post)
    mass_field = derive_node_field(nodes, rule)
    free_field = {n: 0.0 for n in nodes}

    print("=" * 70)
    print("WHY IS DEFLECTION THRESHOLD-LIKE?")
    print("=" * 70)
    print()

    # TEST 1: Shift vs k — find the saturation point
    print("TEST 1: Shift vs k (find saturation)")
    print()

    print(f"  {'k':>6s}  {'shift':>10s}  {'shift/k²':>10s}  {'regime':>12s}")
    print(f"  {'-' * 42}")

    prev_shift = 0
    for k in [0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]:
        cy_free, _ = propagate_and_measure(nodes, source, free_field, k, det_x, screen_ys)
        cy_mass, _ = propagate_and_measure(nodes, source, mass_field, k, det_x, screen_ys)
        shift = cy_mass - cy_free
        sk2 = shift/(k*k) if k > 0 else 0

        if abs(shift) < 1.0:
            regime = "linear"
        elif abs(shift) < height * 0.8:
            regime = "nonlinear"
        else:
            regime = "SATURATED"

        print(f"  {k:6.3f}  {shift:+10.3f}  {sk2:+10.2f}  {regime:>12s}")
        prev_shift = shift

    # TEST 2: Phase gradient at mass region
    print()
    print("TEST 2: Phase gradient ∂(kS)/∂y at mass region (x=30)")
    print(f"  S = action per edge, k × S = phase per edge")
    print()

    print(f"  {'y':>4s}  {'f(30,y)':>10s}  {'S(y→y+1)':>10s}  {'dS':>10s}")
    print(f"  {'-' * 38}")

    for y in range(-5, 15):
        f1 = mass_field.get((30, y), 0.0)
        f2 = mass_field.get((30, y+1), 0.0)
        f_avg = 0.5*(f1+f2)
        L = 1.0  # vertical hop
        delay = L*(1+f_avg)
        retained = math.sqrt(max(delay**2-L**2, 0))
        S = delay - retained

        # Compare with free space
        S_free = 1.0  # at f=0, S=L=1
        dS = S - S_free

        print(f"  {y:4d}  {f1:10.6f}  {S:10.5f}  {dS:+10.5f}")

    # TEST 3: Critical k where shift saturates
    print()
    print("TEST 3: Saturation analysis")
    print()

    # The phase difference between y=0 and y=1 paths through mass at x=30
    f0 = mass_field.get((30, 0), 0.0)
    f1 = mass_field.get((30, 1), 0.0)
    S0 = 1.0*(1+f0) - math.sqrt(max((1+f0)**2-1, 0))
    S1 = 1.0*(1+f1) - math.sqrt(max((1+f1)**2-1, 0))
    dS = S1 - S0

    print(f"  Phase gradient at beam center:")
    print(f"    f(30,0) = {f0:.6f}")
    print(f"    f(30,1) = {f1:.6f}")
    print(f"    S(y=0→1) = {S0:.6f}")
    print(f"    S(y=1→2) = {S1:.6f}")
    print(f"    ΔS = {dS:+.6f}")
    print()

    k_crit = math.pi / abs(dS) if abs(dS) > 0 else float('inf')
    print(f"  Critical k (where k×ΔS = π): {k_crit:.2f}")
    print(f"  At k < {k_crit:.1f}: shift ∝ k² (linear regime)")
    print(f"  At k > {k_crit:.1f}: shift saturates (beam flips to one side)")
    print()

    # Count how many edges the beam traverses through the field
    n_field_edges = sum(1 for x in range(width) if mass_field.get((x, 0), 0) > 0.001)
    total_dS = sum(
        (1+mass_field.get((x, 0), 0)) - math.sqrt(max((1+mass_field.get((x, 0), 0))**2-1, 0)) - 1.0
        for x in range(width)
    )

    print(f"  Edges with nonzero field at y=0: {n_field_edges}")
    print(f"  Total action deficit at y=0: {total_dS:+.4f}")
    print(f"  Total phase at k=1: {abs(total_dS):.4f} rad")
    print(f"  At k={k_crit:.1f}: total phase = {k_crit*abs(total_dS):.1f} rad")
    print()
    print("CONCLUSION:")
    print(f"  The shift saturates when k × (action gradient per step) ≈ π.")
    print(f"  Below this: shift ∝ k² × gradient (perturbative, could scale).")
    print(f"  Above this: shift = ±height (beam width limit, b-independent).")
    print(f"  The 'threshold' behavior is just SATURATION at moderate k.")
    print(f"  To get 1/b scaling: stay in the PERTURBATIVE regime (small k).")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
