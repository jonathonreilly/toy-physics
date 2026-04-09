#!/usr/bin/env python3
"""Two-body gravitational deflection: superposition, force balance, three-body.

Places TWO mass sources on the lattice and tests:
1. Superposition: delta(A+B) == delta(A) + delta(B)?
2. Force balance: equal masses -> centroid at y=0; unequal -> shifts?
3. Three-body: central mass changes deflection pattern?

Uses the 2D causal-DAG path-sum infrastructure from toy_event_physics.

Hypothesis: gravitational deflection is superposable to within 10%.
Falsification: superposition error > 20% implies nonlinear gravitational
interaction in the phase-valley mechanism.

PStack experiment: two-body-gravity
"""

from __future__ import annotations
import cmath
import math
import sys
import os
from collections import defaultdict
from typing import DefaultDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_with_field,
    build_causal_dag,
    local_edge_properties,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_mass_cluster(cx: int, cy: int) -> frozenset[tuple[int, int]]:
    """5-node cross pattern centered at (cx, cy)."""
    return frozenset({(cx, cy), (cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)})


def make_large_mass_cluster(cx: int, cy: int) -> frozenset[tuple[int, int]]:
    """13-node diamond pattern — heavier mass."""
    core = make_mass_cluster(cx, cy)
    ring = frozenset({
        (cx + 2, cy), (cx - 2, cy), (cx, cy + 2), (cx, cy - 2),
        (cx + 1, cy + 1), (cx + 1, cy - 1), (cx - 1, cy + 1), (cx - 1, cy - 1),
    })
    return core | ring


def propagate_and_measure(
    nodes: set[tuple[int, int]],
    persistent_nodes: frozenset[tuple[int, int]],
    source: tuple[int, int],
    detector_x: int,
    postulates: RulePostulates,
) -> dict[int, float]:
    """Propagate amplitude from source through the DAG, return detector distribution.

    Returns {y: probability} at x = detector_x.
    """
    rule = derive_local_rule(persistent_nodes=persistent_nodes, postulates=postulates)
    node_field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_with_field(nodes, source, rule, node_field)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    # State: (current_node, heading) -> complex amplitude
    states: DefaultDict[tuple[tuple[int, int], tuple[int, int]], complex] = defaultdict(complex)
    states[(source, (1, 0))] = 1.0 + 0.0j

    boundary_amplitudes: DefaultDict[int, complex] = defaultdict(complex)

    for node in order:
        matching = [
            (state, amp) for state, amp in list(states.items()) if state[0] == node
        ]
        if not matching:
            continue

        if node[0] == detector_x:
            for state, amp in matching:
                boundary_amplitudes[node[1]] += amp
                del states[state]
            continue

        for (current_node, heading), amplitude in matching:
            del states[(current_node, heading)]
            for neighbor in dag.get(node, []):
                dx = neighbor[0] - node[0]
                dy = neighbor[1] - node[1]
                next_heading = (dx, dy)
                _delay, _action_inc, link_amplitude = local_edge_properties(
                    node, neighbor, rule, node_field,
                )
                states[(neighbor, next_heading)] += amplitude * link_amplitude

    # Convert amplitudes to probabilities
    distribution: dict[int, float] = {}
    for y, amp in boundary_amplitudes.items():
        distribution[y] = abs(amp) ** 2

    return distribution


def centroid(distribution: dict[int, float]) -> float:
    """Probability-weighted centroid of detector distribution."""
    total = sum(distribution.values())
    if total == 0.0:
        return 0.0
    return sum(y * p for y, p in distribution.items()) / total


def total_probability(distribution: dict[int, float]) -> float:
    return sum(distribution.values())


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def main() -> None:
    width = 24
    height = 10
    source = (0, 0)
    detector_x = width
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    nodes = build_rectangular_nodes(width=width, height=height)

    print("=" * 76)
    print("FRONTIER: TWO-BODY GRAVITATIONAL DEFLECTION")
    print("=" * 76)
    print()
    print(f"Lattice: {width+1} x {2*height+1} rectangular DAG")
    print(f"Source: {source}")
    print(f"Detector: x = {detector_x}")
    print(f"Postulates: phase_per_action=4.0, attenuation_power=1.0")
    print(f"            action_mode=spent_delay, field_mode=relaxed")
    print()

    # ==================================================================
    # PART 1: SUPERPOSITION TEST
    # ==================================================================
    # Break symmetry: place masses on the SAME side so deflections add
    # rather than cancel. A at (16, +3) and B at (12, +5).
    print("=" * 76)
    print("PART 1: SUPERPOSITION TEST")
    print("=" * 76)
    print()

    mass_a_center = (16, 3)
    mass_b_center = (12, 5)
    mass_a = make_mass_cluster(*mass_a_center)
    mass_b = make_mass_cluster(*mass_b_center)
    mass_both = mass_a | mass_b

    print(f"Mass A: 5-node cross at {mass_a_center}")
    print(f"Mass B: 5-node cross at {mass_b_center}")
    print(f"(Both on +y side to break cancellation symmetry)")
    print()

    configs = {
        "No mass":     frozenset(),
        "Mass A only": mass_a,
        "Mass B only": mass_b,
        "Both A+B":    mass_both,
    }

    results: dict[str, dict[int, float]] = {}
    centroids: dict[str, float] = {}

    for name, persistent in configs.items():
        dist = propagate_and_measure(nodes, persistent, source, detector_x, postulates)
        results[name] = dist
        centroids[name] = centroid(dist)

    baseline = centroids["No mass"]
    deltas = {name: centroids[name] - baseline for name in configs}

    print(f"{'Config':<16} | {'Centroid':>10} | {'Delta':>10} | {'Total P':>10}")
    print("-" * 56)
    for name in configs:
        c = centroids[name]
        d = deltas[name]
        tp = total_probability(results[name])
        print(f"{name:<16} | {c:>10.5f} | {d:>10.5f} | {tp:>10.5f}")

    sum_individual = deltas["Mass A only"] + deltas["Mass B only"]
    combined = deltas["Both A+B"]
    print()
    print(f"delta(A) + delta(B) = {sum_individual:.6f}")
    print(f"delta(A+B)          = {combined:.6f}")

    if abs(combined) > 1e-12:
        error = abs(combined - sum_individual) / abs(combined)
        print(f"Superposition error = |delta_AB - (delta_A + delta_B)| / |delta_AB| = {error:.4f} ({error*100:.1f}%)")
    elif abs(sum_individual) > 1e-12:
        print(f"Superposition error: combined delta ~ 0 but sum != 0 — ill-conditioned")
    else:
        print(f"Superposition error: both deltas ~ 0 — no deflection detected")

    # Also test superposition with the SYMMETRIC config for comparison
    print()
    print("--- Symmetric check (A at +3, B at -3) ---")
    mass_a_sym = make_mass_cluster(16, 3)
    mass_b_sym = make_mass_cluster(16, -3)
    dist_a_sym = propagate_and_measure(nodes, mass_a_sym, source, detector_x, postulates)
    dist_b_sym = propagate_and_measure(nodes, mass_b_sym, source, detector_x, postulates)
    dist_both_sym = propagate_and_measure(nodes, mass_a_sym | mass_b_sym, source, detector_x, postulates)
    ca = centroid(dist_a_sym) - baseline
    cb = centroid(dist_b_sym) - baseline
    cab = centroid(dist_both_sym) - baseline
    print(f"delta(A@+3) = {ca:+.5f}, delta(B@-3) = {cb:+.5f}")
    print(f"Sum = {ca+cb:+.5f}, Combined = {cab:+.5f}")
    print(f"Perfect cancellation by symmetry: {abs(ca + cb) < 1e-10}")

    # Also test field-level superposition
    print()
    print("--- Field-level superposition check ---")
    rule_a = derive_local_rule(persistent_nodes=mass_a, postulates=postulates)
    rule_b = derive_local_rule(persistent_nodes=mass_b, postulates=postulates)
    rule_both = derive_local_rule(persistent_nodes=mass_both, postulates=postulates)
    rule_none = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)

    field_a = derive_node_field(nodes, rule_a)
    field_b = derive_node_field(nodes, rule_b)
    field_both = derive_node_field(nodes, rule_both)

    field_sum = {n: field_a[n] + field_b[n] for n in nodes}

    max_field_diff = 0.0
    max_field_both = 0.0
    for n in nodes:
        diff = abs(field_both[n] - field_sum[n])
        if diff > max_field_diff:
            max_field_diff = diff
        if abs(field_both[n]) > max_field_both:
            max_field_both = abs(field_both[n])

    if max_field_both > 0:
        field_error = max_field_diff / max_field_both
        print(f"Max |field(A+B) - field(A) - field(B)| = {max_field_diff:.6f}")
        print(f"Max |field(A+B)|                       = {max_field_both:.6f}")
        print(f"Field superposition error (rel)        = {field_error:.4f} ({field_error*100:.1f}%)")
    else:
        print("No field detected — mass may be outside lattice or too small")

    # ==================================================================
    # PART 2: FORCE BALANCE
    # ==================================================================
    print()
    print("=" * 76)
    print("PART 2: FORCE BALANCE — EQUAL AND UNEQUAL MASSES")
    print("=" * 76)
    print()

    mass_upper = make_mass_cluster(12, 4)
    mass_lower = make_mass_cluster(12, -4)
    mass_upper_large = make_large_mass_cluster(12, 4)

    balance_configs = {
        "No mass":              frozenset(),
        "Upper only (5-node)":  mass_upper,
        "Lower only (5-node)":  mass_lower,
        "Equal (5+5)":          mass_upper | mass_lower,
        "Unequal (13+5)":       mass_upper_large | mass_lower,
    }

    print(f"Upper mass at (12, +4), Lower mass at (12, -4)")
    print(f"Equal: both 5-node crosses")
    print(f"Unequal: upper = 13-node diamond, lower = 5-node cross")
    print()
    print(f"{'Config':<24} | {'Centroid':>10} | {'Delta':>10}")
    print("-" * 52)

    balance_centroids: dict[str, float] = {}
    for name, persistent in balance_configs.items():
        dist = propagate_and_measure(nodes, persistent, source, detector_x, postulates)
        balance_centroids[name] = centroid(dist)

    bl_baseline = balance_centroids["No mass"]
    for name in balance_configs:
        c = balance_centroids[name]
        d = c - bl_baseline
        print(f"{name:<24} | {c:>10.5f} | {d:>10.5f}")

    print()
    equal_delta = balance_centroids["Equal (5+5)"] - bl_baseline
    unequal_delta = balance_centroids["Unequal (13+5)"] - bl_baseline
    upper_delta = balance_centroids["Upper only (5-node)"] - bl_baseline
    lower_delta = balance_centroids["Lower only (5-node)"] - bl_baseline

    print(f"Equal-mass centroid delta:   {equal_delta:+.6f}")
    print(f"  (expect ~0 by symmetry)")
    print(f"Unequal-mass centroid delta: {unequal_delta:+.6f}")
    print(f"  (expect shift toward upper/heavier mass)")
    print(f"Upper-only delta:            {upper_delta:+.6f}")
    print(f"Lower-only delta:            {lower_delta:+.6f}")

    # Check symmetry for equal masses
    if abs(upper_delta + lower_delta) < 1e-10:
        print(f"\nSymmetry: delta(upper) = -delta(lower) — EXACT")
    else:
        asym = abs(upper_delta + lower_delta) / max(abs(upper_delta), abs(lower_delta), 1e-12)
        print(f"\nSymmetry check: |delta(upper) + delta(lower)| / max = {asym:.6f}")

    # ==================================================================
    # PART 3: THREE-BODY
    # ==================================================================
    print()
    print("=" * 76)
    print("PART 3: THREE-BODY — EFFECT OF CENTRAL MASS")
    print("=" * 76)
    print()

    mass_top = make_mass_cluster(12, 4)
    mass_bottom = make_mass_cluster(12, -4)
    mass_center = make_mass_cluster(12, 0)

    three_configs = {
        "No mass":                frozenset(),
        "Top + Bottom":           mass_top | mass_bottom,
        "Top + Bottom + Center":  mass_top | mass_bottom | mass_center,
        "Center only":            mass_center,
    }

    print(f"Masses at (12, +4), (12, -4), (12, 0)")
    print()
    print(f"{'Config':<26} | {'Centroid':>10} | {'Delta':>10}")
    print("-" * 54)

    three_centroids: dict[str, float] = {}
    for name, persistent in three_configs.items():
        dist = propagate_and_measure(nodes, persistent, source, detector_x, postulates)
        three_centroids[name] = centroid(dist)

    t_baseline = three_centroids["No mass"]
    for name in three_configs:
        c = three_centroids[name]
        d = c - t_baseline
        print(f"{name:<26} | {c:>10.5f} | {d:>10.5f}")

    two_body_delta = three_centroids["Top + Bottom"] - t_baseline
    three_body_delta = three_centroids["Top + Bottom + Center"] - t_baseline
    center_only_delta = three_centroids["Center only"] - t_baseline

    print()
    print(f"Two-body delta (top+bottom):  {two_body_delta:+.6f}")
    print(f"Three-body delta (+center):   {three_body_delta:+.6f}")
    print(f"Center-only delta:            {center_only_delta:+.6f}")
    print(f"Three-body excess over two:   {three_body_delta - two_body_delta:+.6f}")

    # ==================================================================
    # PART 4: DETECTOR DISTRIBUTIONS — detailed view
    # ==================================================================
    print()
    print("=" * 76)
    print("PART 4: DETECTOR DISTRIBUTIONS (PART 1 CONFIGS)")
    print("=" * 76)
    print()

    all_ys = sorted(set().union(*(results[name].keys() for name in results)))
    print(f"{'y':>4} | {'No mass':>10} | {'Mass A':>10} | {'Mass B':>10} | {'Both':>10}")
    print("-" * 56)
    for y in all_ys:
        vals = [results[name].get(y, 0.0) for name in configs]
        # Normalize each column
        totals = [total_probability(results[name]) for name in configs]
        normed = [v / t if t > 0 else 0 for v, t in zip(vals, totals)]
        print(f"{y:>4} | {normed[0]:>10.6f} | {normed[1]:>10.6f} | {normed[2]:>10.6f} | {normed[3]:>10.6f}")

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print()
    print("=" * 76)
    print("SUMMARY")
    print("=" * 76)
    print()

    # Part 1 verdict
    if abs(combined) > 1e-12:
        error_pct = abs(combined - sum_individual) / abs(combined) * 100
    else:
        error_pct = float("nan")

    print(f"1. SUPERPOSITION: delta(A+B) vs delta(A)+delta(B)")
    if error_pct == error_pct:  # not NaN
        if error_pct <= 10:
            print(f"   PASS — error = {error_pct:.1f}% (< 10% threshold)")
            print(f"   Hypothesis SUPPORTED: deflection is superposable")
        elif error_pct <= 20:
            print(f"   MARGINAL — error = {error_pct:.1f}% (10-20% range)")
            print(f"   Weak superposition — field nonlinearity detectable")
        else:
            print(f"   FAIL — error = {error_pct:.1f}% (> 20% threshold)")
            print(f"   Hypothesis FALSIFIED: nonlinear gravitational interaction")
    else:
        print(f"   INCONCLUSIVE — no measurable deflection")

    print()
    print(f"2. FORCE BALANCE:")
    print(f"   Equal masses: centroid delta = {equal_delta:+.6f} (expect ~0)")
    print(f"   Upper-only deflects beam to y={balance_centroids['Upper only (5-node)']:.1f}")
    print(f"   Lower-only deflects beam to y={balance_centroids['Lower only (5-node)']:.1f}")
    sign_upper = "toward" if upper_delta * 4 > 0 else "away from"
    print(f"   Single mass deflects beam {sign_upper} itself (sign={'+' if upper_delta > 0 else '-'})")
    if abs(equal_delta) < 0.01:
        print(f"   PASS — equal masses balance to < 0.01")
    else:
        print(f"   NOTE — equal-mass residual = {abs(equal_delta):.6f}")

    print(f"   Unequal-mass centroid: {unequal_delta:+.6f}")
    # Determine if deflection favors heavier mass
    # Upper mass is at +4. If beam deflects negative, single mass deflects AWAY (repulsion).
    # For unequal, the net should shift toward the stronger deflector.
    if abs(unequal_delta) > 0.1:
        print(f"   Net asymmetry detected — heavier mass has stronger effect")
    else:
        print(f"   Masses nearly balanced despite size asymmetry")

    print()
    print(f"3. THREE-BODY:")
    print(f"   Central mass effect: {three_body_delta - two_body_delta:+.6f}")
    if abs(center_only_delta) < 0.01:
        print(f"   Central mass alone gives negligible deflection (symmetric)")
    else:
        print(f"   Central mass alone: delta = {center_only_delta:+.6f}")


if __name__ == "__main__":
    main()
