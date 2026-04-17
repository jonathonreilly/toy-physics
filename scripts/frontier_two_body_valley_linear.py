#!/usr/bin/env python3
"""Two-body gravity + linear Poisson: valley-linear action on 2D lattice.

FIXES from review:
  - frontier_two_body_gravity.py used default spent_delay action (wrong lane)
  - This script uses valley-linear S = L*(1-f) explicitly
  - Tests both nonlinear and linear Poisson field solvers
  - Asymmetric mass placement for real superposition test

NOTE: The 2D toy_event_physics.py does not have a valley-linear
action_mode. This script computes amplitudes directly using
act = L * (1 - f), matching the retained 3D lattice scripts.
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
    graph_neighbors,
    boundary_nodes,
)

K = 4.0
P = 1  # kernel power for 2D


def linear_poisson_field(nodes, persistent_nodes, tolerance=1e-8, max_iter=400):
    """Standard linear Poisson: source + avg_neighbor."""
    support = derive_persistence_support(nodes, persistent_nodes)
    field = dict(support)
    bounds = boundary_nodes(nodes)
    for _ in range(max_iter):
        updated = {}
        max_change = 0.0
        for node in nodes:
            if node in bounds:
                nv = 0.0
            else:
                nbrs = graph_neighbors(node, nodes)
                avg = sum(field[n] for n in nbrs) / len(nbrs)
                nv = support[node] + avg
            updated[node] = nv
            max_change = max(max_change, abs(nv - field[node]))
        field = updated
        if max_change < tolerance:
            break
    return field


def propagate_valley_linear(nodes, source, node_field, width, k=K, p=P):
    """Propagate with EXPLICIT valley-linear action S = L*(1-f).

    Does NOT use local_edge_properties or action_mode. Computes
    amplitude per edge directly to match the 3D lattice scripts.
    """
    # Build arrival times and DAG using a dummy rule (for ordering only)
    rule = derive_local_rule(frozenset(), RulePostulates(
        phase_per_action=k, attenuation_power=p))
    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)

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
            L = math.dist(node, neighbor)
            f = 0.5 * (node_field.get(node, 0.0) + node_field.get(neighbor, 0.0))
            # VALLEY-LINEAR action
            act = L * (1.0 - f)
            edge_amp = cmath.exp(1j * k * act) / (L ** p)
            states[neighbor] += amp * edge_amp

    return detector


def centroid(det):
    total = sum(abs(a)**2 for a in det.values())
    if total < 1e-30:
        return 0.0, total
    return sum(y * abs(a)**2 for y, a in det.items()) / total, total


def make_cluster(cx, cy, nodes, radius=1):
    cluster = set()
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if abs(dx) + abs(dy) <= radius:
                n = (cx + dx, cy + dy)
                if n in nodes:
                    cluster.add(n)
    return frozenset(cluster)


def run_test(field_fn, solver_name):
    """Run superposition + gravity test with given field solver."""
    width = 24
    height = 10
    nodes = build_rectangular_nodes(width, height)
    source = (0, 0)

    # Asymmetric: both masses on +y side at different x
    cluster_a = make_cluster(12, 4, nodes)
    cluster_b = make_cluster(18, 4, nodes)
    cluster_ab = cluster_a | cluster_b

    field_none = {n: 0.0 for n in nodes}
    field_a = field_fn(nodes, cluster_a)
    field_b = field_fn(nodes, cluster_b)
    field_ab = field_fn(nodes, cluster_ab)

    # Field linearity check
    max_err = max(abs(field_ab.get(n, 0) - field_a.get(n, 0) - field_b.get(n, 0)) for n in nodes)
    max_fab = max(abs(field_ab.get(n, 0)) for n in nodes)
    lin_err = max_err / max_fab if max_fab > 1e-30 else 0

    print(f"\n  [{solver_name}] Field linearity error: {lin_err*100:.1f}%")

    # Propagate each config
    configs = [
        ("no mass", field_none),
        ("mass A", field_a),
        ("mass B", field_b),
        ("A + B", field_ab),
    ]

    results = {}
    for name, fld in configs:
        det = propagate_valley_linear(nodes, source, fld, width)
        c, prob = centroid(det)
        results[name] = (c, prob)
        dir_label = ""
        if name != "no mass":
            d = c - results["no mass"][0]
            dir_label = f" (delta={d:+.4f}, {'TOWARD' if d > 0 else 'AWAY'} +y mass)"
        print(f"    {name:>10}: centroid={c:+.6f}, prob={prob:.3e}{dir_label}")

    base = results["no mass"][0]
    da = results["mass A"][0] - base
    db = results["mass B"][0] - base
    dab = results["A + B"][0] - base
    dsum = da + db

    print(f"\n    delta(A)         = {da:+.6f}")
    print(f"    delta(B)         = {db:+.6f}")
    print(f"    delta(A+B)       = {dab:+.6f}")
    print(f"    delta(A)+delta(B)= {dsum:+.6f}")

    sup_err = abs(dab - dsum) / abs(dab) * 100 if abs(dab) > 1e-10 else 0
    print(f"    Superposition error: {sup_err:.1f}%")

    grav_works = abs(dab) > 1e-6
    grav_toward = dab > 0  # mass is at +y, so TOWARD means positive delta

    return {
        "field_lin": lin_err,
        "da": da, "db": db, "dab": dab, "dsum": dsum,
        "sup_err": sup_err,
        "grav_works": grav_works,
        "grav_toward": grav_toward,
    }


def main():
    print("=" * 70)
    print("TWO-BODY GRAVITY: VALLEY-LINEAR ACTION + LINEAR POISSON")
    print("=" * 70)
    print()
    print("Action: S = L*(1-f) (valley-linear, explicit — not action_mode)")
    print("Masses at (12,+4) and (18,+4) — asymmetric, both on +y side")
    print()

    # Nonlinear solver
    def nonlin(nodes, pn):
        rule = derive_local_rule(pn, RulePostulates(phase_per_action=K, attenuation_power=P))
        return derive_node_field(nodes, rule)

    print("--- NONLINEAR field solver ---")
    r_nl = run_test(nonlin, "nonlinear")

    print("\n--- LINEAR field solver ---")
    r_li = run_test(linear_poisson_field, "linear")

    # Comparison
    print(f"\n{'='*70}")
    print("COMPARISON (valley-linear action)")
    print(f"{'='*70}")
    print(f"  {'':>22} | {'Nonlinear':>12} | {'Linear':>12}")
    print(f"  {'-'*50}")
    print(f"  {'Field linearity':>22} | {r_nl['field_lin']*100:>11.1f}% | {r_li['field_lin']*100:>11.1f}%")
    print(f"  {'delta(A)':>22} | {r_nl['da']:>+12.4f} | {r_li['da']:>+12.4f}")
    print(f"  {'delta(B)':>22} | {r_nl['db']:>+12.4f} | {r_li['db']:>+12.4f}")
    print(f"  {'delta(A+B)':>22} | {r_nl['dab']:>+12.4f} | {r_li['dab']:>+12.4f}")
    print(f"  {'delta(A)+delta(B)':>22} | {r_nl['dsum']:>+12.4f} | {r_li['dsum']:>+12.4f}")
    print(f"  {'Superposition err':>22} | {r_nl['sup_err']:>11.1f}% | {r_li['sup_err']:>11.1f}%")
    print(f"  {'Gravity works':>22} | {'YES' if r_nl['grav_works'] else 'NO':>12} | {'YES' if r_li['grav_works'] else 'NO':>12}")
    print(f"  {'Direction':>22} | {'TOWARD' if r_nl['grav_toward'] else 'AWAY':>12} | {'TOWARD' if r_li['grav_toward'] else 'AWAY':>12}")

    # Verdict
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")

    if r_li['grav_works'] and r_li['sup_err'] < 20:
        print(f"\n  Linear Poisson + valley-linear: gravity works with {r_li['sup_err']:.1f}% superposition error.")
        if r_nl['sup_err'] > 50:
            print(f"  Nonlinear solver: {r_nl['sup_err']:.1f}% error — substantially worse.")
            print(f"  The linear solver restores superposition on the retained VL action.")
    elif r_li['grav_works'] and r_li['sup_err'] >= 20:
        print(f"\n  Linear Poisson has gravity but superposition still fails ({r_li['sup_err']:.1f}%).")
        print(f"  The nonlinearity is not the sole cause of superposition failure.")
    elif not r_li['grav_works']:
        print(f"\n  Linear Poisson kills gravity on the valley-linear action.")
        print(f"  The field nonlinearity may be load-bearing for VL gravity.")
    print()


if __name__ == "__main__":
    main()
