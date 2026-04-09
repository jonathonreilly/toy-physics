#!/usr/bin/env python3
"""Test: does replacing the nonlinear field solver with a standard linear
Poisson solver restore gravitational superposition?

BACKGROUND:
  frontier_two_body_gravity.py found 223% superposition error. The root
  cause is derive_node_field's nonlinear source term:
    new = support + (1 - support) * avg_neighbor
  The (1-support) factor couples the two fields, making them sub-additive.

  A standard linear Poisson solver uses:
    new = source + avg_neighbor
  which IS linear: field(A+B) = field(A) + field(B) exactly.

THIS EXPERIMENT:
  1. Implement a linear Poisson solver
  2. Re-run the two-body superposition test with both solvers
  3. Check if gravity still works with the linear solver
  4. Compare field linearity directly: |field(A+B) - field(A) - field(B)|

HYPOTHESIS: Linear Poisson restores superposition while preserving gravity.
FALSIFICATION: If gravity vanishes with the linear solver, the nonlinearity
  is load-bearing.
"""

from __future__ import annotations
import cmath
import math
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    derive_persistence_support,
    infer_arrival_times_from_source,
    build_causal_dag,
    local_edge_properties,
    graph_neighbors,
    boundary_nodes,
)


def linear_poisson_field(
    nodes: set[tuple[int, int]],
    persistent_nodes: frozenset[tuple[int, int]],
    tolerance: float = 1e-8,
    max_iterations: int = 400,
) -> dict[tuple[int, int], float]:
    """Standard linear Poisson solver: field = source + Laplacian average.

    Unlike derive_node_field, this uses:
      new = source + avg_neighbor  (no (1-support) coupling)
    which guarantees field(A+B) = field(A) + field(B).
    """
    support = derive_persistence_support(nodes, persistent_nodes)
    field = dict(support)
    bounds = boundary_nodes(nodes)

    for _ in range(max_iterations):
        updated = {}
        max_change = 0.0
        for node in nodes:
            if node in bounds:
                new_value = 0.0
            else:
                neighbors = graph_neighbors(node, nodes)
                avg = sum(field[n] for n in neighbors) / len(neighbors)
                # LINEAR: source + average (no coupling)
                new_value = support[node] + avg
            updated[node] = new_value
            max_change = max(max_change, abs(new_value - field[node]))
        field = updated
        if max_change < tolerance:
            break
    return field


def propagate(nodes, source, dag, rule, node_field, width):
    """Simple propagation through DAG, returns detector amplitudes."""
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    order = sorted(arrival_times, key=arrival_times.get)

    states = defaultdict(complex)
    states[source] = 1.0 + 0j

    detector = {}
    for node in order:
        amp = states.get(node, 0j)
        if abs(amp) < 1e-30:
            continue
        if node[0] == width:
            detector[node[1]] = detector.get(node[1], 0j) + amp
            continue
        for neighbor in dag.get(node, []):
            _, _, link_amp = local_edge_properties(node, neighbor, rule, node_field)
            states[neighbor] += amp * link_amp

    return detector


def centroid(detector):
    total_p = sum(abs(a)**2 for a in detector.values())
    if total_p < 1e-30:
        return 0.0, total_p
    c = sum(y * abs(a)**2 for y, a in detector.items()) / total_p
    return c, total_p


def run_superposition_test(field_fn, label):
    """Run the two-body superposition test with a given field solver."""
    width = 24
    height = 10
    nodes = build_rectangular_nodes(width, height)
    source = (0, 0)

    # Mass clusters — ASYMMETRIC placement to avoid cancellation
    # Both on same side so delta(A+B) != 0
    mass_a_center = (12, 4)
    mass_b_center = (18, 4)

    def make_cluster(cx, cy, radius=1):
        cluster = set()
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if abs(dx) + abs(dy) <= radius:
                    n = (cx + dx, cy + dy)
                    if n in nodes:
                        cluster.add(n)
        return frozenset(cluster)

    cluster_a = make_cluster(*mass_a_center)
    cluster_b = make_cluster(*mass_b_center)
    cluster_ab = cluster_a | cluster_b

    postulates = RulePostulates(
        phase_per_action=4.0,
        attenuation_power=1.0,
    )

    # Compute fields
    field_none = {n: 0.0 for n in nodes}
    field_a = field_fn(nodes, cluster_a)
    field_b = field_fn(nodes, cluster_b)
    field_ab = field_fn(nodes, cluster_ab)

    # Check field linearity
    max_lin_err = 0.0
    max_field_val = 0.0
    for n in nodes:
        fa = field_a.get(n, 0.0)
        fb = field_b.get(n, 0.0)
        fab = field_ab.get(n, 0.0)
        err = abs(fab - fa - fb)
        max_lin_err = max(max_lin_err, err)
        max_field_val = max(max_field_val, abs(fab))

    rel_lin_err = max_lin_err / max_field_val if max_field_val > 1e-30 else 0.0

    print(f"\n  [{label}] Field linearity:")
    print(f"    max |f(A+B) - f(A) - f(B)| = {max_lin_err:.6e}")
    print(f"    max |f(A+B)|                = {max_field_val:.6e}")
    print(f"    relative linearity error    = {rel_lin_err:.4f} ({100*rel_lin_err:.1f}%)")

    # Propagate for each configuration
    rule = derive_local_rule(frozenset(), postulates)

    configs = [
        ("no mass", field_none),
        ("mass A", field_a),
        ("mass B", field_b),
        ("A + B", field_ab),
    ]

    centroids = {}
    for name, field in configs:
        # Need to rebuild DAG with each field (arrival times depend on field)
        arrival = infer_arrival_times_from_source(nodes, source, rule)
        dag = build_causal_dag(nodes, arrival)
        det = propagate(nodes, source, dag, rule, field, width)
        c, p = centroid(det)
        centroids[name] = c
        print(f"    {name:>10}: centroid = {c:+.6f}, det_prob = {p:.4e}")

    baseline = centroids["no mass"]
    delta_a = centroids["mass A"] - baseline
    delta_b = centroids["mass B"] - baseline
    delta_ab = centroids["A + B"] - baseline
    delta_sum = delta_a + delta_b

    print(f"\n    delta_A     = {delta_a:+.6f}")
    print(f"    delta_B     = {delta_b:+.6f}")
    print(f"    delta_A+B   = {delta_ab:+.6f}")
    print(f"    delta_A + delta_B = {delta_sum:+.6f}")

    if abs(delta_ab) > 1e-10:
        sup_err = abs(delta_ab - delta_sum) / abs(delta_ab) * 100
        print(f"    Superposition error: {sup_err:.1f}%")
    else:
        sup_err = 0.0
        print(f"    delta_AB ~ 0 (no gravity signal)")

    return {
        "field_linearity": rel_lin_err,
        "delta_a": delta_a,
        "delta_b": delta_b,
        "delta_ab": delta_ab,
        "delta_sum": delta_sum,
        "superposition_error": sup_err,
    }


def main():
    print("=" * 70)
    print("LINEAR POISSON vs NONLINEAR: SUPERPOSITION TEST")
    print("=" * 70)
    print()
    print("Does replacing the nonlinear field solver with a standard")
    print("linear Poisson solver restore gravitational superposition?")
    print()

    # Nonlinear solver (current default)
    def nonlinear_field(nodes, persistent):
        rule = derive_local_rule(persistent, RulePostulates(
            phase_per_action=4.0, attenuation_power=1.0))
        return derive_node_field(nodes, rule)

    print("--- NONLINEAR SOLVER (current: support + (1-support)*avg) ---")
    r_nonlin = run_superposition_test(nonlinear_field, "nonlinear")

    print("\n\n--- LINEAR SOLVER (proposed: support + avg) ---")
    r_linear = run_superposition_test(linear_poisson_field, "linear")

    # Summary
    print(f"\n\n{'='*70}")
    print("COMPARISON")
    print(f"{'='*70}")
    print(f"  {'':>20} | {'Nonlinear':>15} | {'Linear':>15}")
    print(f"  {'-'*55}")
    print(f"  {'Field linearity':>20} | {r_nonlin['field_linearity']*100:>14.1f}% | {r_linear['field_linearity']*100:>14.1f}%")
    print(f"  {'delta(A)':>20} | {r_nonlin['delta_a']:>+15.6f} | {r_linear['delta_a']:>+15.6f}")
    print(f"  {'delta(B)':>20} | {r_nonlin['delta_b']:>+15.6f} | {r_linear['delta_b']:>+15.6f}")
    print(f"  {'delta(A+B)':>20} | {r_nonlin['delta_ab']:>+15.6f} | {r_linear['delta_ab']:>+15.6f}")
    print(f"  {'delta(A)+delta(B)':>20} | {r_nonlin['delta_sum']:>+15.6f} | {r_linear['delta_sum']:>+15.6f}")
    print(f"  {'Superposition err':>20} | {r_nonlin['superposition_error']:>14.1f}% | {r_linear['superposition_error']:>14.1f}%")

    # Verdict
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    lin_has_gravity = abs(r_linear['delta_ab']) > 1e-6
    lin_is_linear = r_linear['field_linearity'] < 0.01
    lin_sup_ok = r_linear['superposition_error'] < 20

    if lin_has_gravity and lin_is_linear and lin_sup_ok:
        print(f"\n  Linear Poisson RESTORES superposition while PRESERVING gravity.")
        print(f"  The nonlinear source term was an unnecessary coupling —")
        print(f"  a standard linear Poisson solver produces the same gravity")
        print(f"  mechanism with correct superposition.")
        print(f"\n  RECOMMENDATION: Replace derive_node_field's source term")
        print(f"  with the linear version for future work.")
    elif lin_has_gravity and not lin_sup_ok:
        print(f"\n  Linear Poisson has gravity but superposition still fails.")
        print(f"  The nonlinearity in the field is not the only source of")
        print(f"  superposition violation.")
    elif not lin_has_gravity:
        print(f"\n  Linear Poisson KILLS gravity.")
        print(f"  The nonlinear (1-support) coupling is LOAD-BEARING —")
        print(f"  removing it destroys the gravitational mechanism.")
        print(f"  The superposition failure is a fundamental property of")
        print(f"  gravity in this model, not a fixable bug.")
    else:
        print(f"\n  Inconclusive — check the numbers above.")


if __name__ == "__main__":
    main()
