#!/usr/bin/env python3
"""Diagnose why 2D gives AWAY gravity while 3D gives TOWARD with valley-linear.

THE MYSTERY:
  - 2D toy_event_physics + derive_node_field + VL => AWAY
  - 3D ordered lattice + analytic 1/r^2 field + VL => TOWARD
  Both use S = L*(1-f). Why does the sign flip?

POSSIBLE CAUSES:
  1. The nonlinear (1-support) coupling in derive_node_field
  2. The 2D logarithmic field profile (vs 3D Coulomb 1/r)
  3. The 2D path topology (fewer paths, different interference)
  4. The field including causal-direction dependence in 2D
  5. The attenuation mode (delay vs geometry)

TESTS:
  A. Analytic 1/r field in 2D (full spacetime radius)
  B. Analytic spatial-only field in 2D (|y - y_mass| only)
  C. Linear Laplacian field (linear Poisson solver)
  D. derive_node_field (nonlinear solver, the original)
  E. Vary field strength (1e-6 to 1e-2)

HYPOTHESIS: AWAY comes from derive_node_field's nonlinear coupling,
  not from the 2D geometry.
FALSIFICATION: If ALL field types give AWAY in 2D, the 2D path
  topology is the cause.
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

# Match the 2D VL scripts
K = 4.0
P = 1  # kernel power for 2D


# ── Field solvers ──────────────────────────────────────────────

def analytic_full_radius_field(nodes, mass_pos, strength):
    """Analytic 1/r field using FULL spacetime distance (x AND y).

    This is what the 2D version of the 3D script's approach would be
    if we naively include the causal direction in the radius.
    """
    mx, my = mass_pos
    field = {}
    for n in nodes:
        r = math.sqrt((n[0] - mx) ** 2 + (n[1] - my) ** 2) + 0.1
        field[n] = strength / r
    return field


def analytic_spatial_only_field(nodes, mass_pos, strength):
    """Analytic spatial-only field: f = strength / |y - y_mass|.

    This matches what the 3D scripts actually do -- the field depends
    ONLY on spatial separation, not on causal (x) separation.
    Every layer sees the same potential.
    """
    _mx, my = mass_pos
    field = {}
    for n in nodes:
        r = abs(n[1] - my) + 0.1
        field[n] = strength / r
    return field


def analytic_2d_coulomb_field(nodes, mass_pos, strength):
    """Analytic 2D Coulomb: f = strength * log(r_spatial).

    In 2D, the Green's function is logarithmic, not 1/r.
    Use -log(r) so field is positive near the source and decays.
    """
    _mx, my = mass_pos
    field = {}
    for n in nodes:
        r = abs(n[1] - my) + 0.1
        field[n] = strength * max(0, -math.log(r / 10.0))
    return field


def linear_poisson_field(nodes, persistent_nodes, tolerance=1e-8, max_iter=400):
    """Standard linear Poisson: source + avg_neighbor (no (1-support))."""
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


def nonlinear_field(nodes, persistent_nodes):
    """Original derive_node_field (nonlinear: support + (1-support)*avg)."""
    rule = derive_local_rule(persistent_nodes, RulePostulates(
        phase_per_action=K, attenuation_power=P))
    return derive_node_field(nodes, rule)


# ── Propagation ────────────────────────────────────────────────

def propagate_vl(nodes, source, node_field, width, k=K, p=P):
    """Valley-linear propagation: S = L*(1-f), 1/L^p kernel.

    Uses a flat-space DAG (no field in arrival times) to isolate
    the action effect from the DAG-ordering effect.
    """
    # Build DAG from FLAT space (no field influence on causal order)
    flat_field = {n: 0.0 for n in nodes}
    rule = derive_local_rule(frozenset(), RulePostulates(
        phase_per_action=k, attenuation_power=p))
    from toy_event_physics import infer_arrival_times_with_field
    arrival = infer_arrival_times_with_field(nodes, source, rule, flat_field)
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
            act = L * (1.0 - f)
            edge_amp = cmath.exp(1j * k * act) / (L ** p)
            states[neighbor] += amp * edge_amp

    return detector


def centroid(det):
    total = sum(abs(a) ** 2 for a in det.values())
    if total < 1e-30:
        return 0.0, total
    return sum(y * abs(a) ** 2 for y, a in det.items()) / total, total


# ── Test harness ───────────────────────────────────────────────

def make_cluster(cx, cy, nodes, radius=1):
    cluster = set()
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if abs(dx) + abs(dy) <= radius:
                n = (cx + dx, cy + dy)
                if n in nodes:
                    cluster.add(n)
    return frozenset(cluster)


def run_single_test(label, node_field_with_mass, node_field_flat, nodes, source, width):
    """Run one gravity test and return delta and direction."""
    det_flat = propagate_vl(nodes, source, node_field_flat, width)
    det_mass = propagate_vl(nodes, source, node_field_with_mass, width)

    c_flat, p_flat = centroid(det_flat)
    c_mass, p_mass = centroid(det_mass)
    delta = c_mass - c_flat

    # Mass is at +y, so positive delta = TOWARD
    direction = "TOWARD" if delta > 0 else "AWAY"
    return delta, direction, c_flat, c_mass, p_flat, p_mass


def field_stats(field, nodes):
    """Return min, max, mean of field values."""
    vals = [field[n] for n in nodes]
    return min(vals), max(vals), sum(vals) / len(vals)


def main():
    print("=" * 72)
    print("2D GRAVITY SIGN DIAGNOSIS")
    print("Why does 2D give AWAY while 3D gives TOWARD with valley-linear?")
    print("=" * 72)

    width = 20
    height = 8
    nodes = build_rectangular_nodes(width, height)
    source = (0, 0)
    mass_pos = (10, 4)  # mass at +y side

    flat_field = {n: 0.0 for n in nodes}
    cluster = make_cluster(mass_pos[0], mass_pos[1], nodes)

    # Default strength for Tests A-D
    strength = 1e-4

    # ── Test A: Analytic 1/r field (full spacetime radius) ──
    print(f"\n{'─' * 72}")
    print("Test A: Analytic 1/r field (full spacetime radius, like naive 2D)")
    field_a = analytic_full_radius_field(nodes, mass_pos, strength)
    fmin, fmax, fmean = field_stats(field_a, nodes)
    print(f"  Field range: [{fmin:.2e}, {fmax:.2e}], mean={fmean:.2e}")
    delta, direction, c0, cm, p0, pm = run_single_test(
        "A", field_a, flat_field, nodes, source, width)
    print(f"  Flat centroid:  {c0:+.6f}  (prob={p0:.3e})")
    print(f"  Mass centroid:  {cm:+.6f}  (prob={pm:.3e})")
    print(f"  Delta:          {delta:+.6f}  => {direction}")

    # ── Test B: Analytic spatial-only field (3D convention) ──
    print(f"\n{'─' * 72}")
    print("Test B: Analytic spatial-only field (|y - y_mass|, matches 3D convention)")
    field_b = analytic_spatial_only_field(nodes, mass_pos, strength)
    fmin, fmax, fmean = field_stats(field_b, nodes)
    print(f"  Field range: [{fmin:.2e}, {fmax:.2e}], mean={fmean:.2e}")
    delta, direction, c0, cm, p0, pm = run_single_test(
        "B", field_b, flat_field, nodes, source, width)
    print(f"  Flat centroid:  {c0:+.6f}  (prob={p0:.3e})")
    print(f"  Mass centroid:  {cm:+.6f}  (prob={pm:.3e})")
    print(f"  Delta:          {delta:+.6f}  => {direction}")

    # ── Test B2: Spatial-only with stronger field ──
    print(f"\n{'─' * 72}")
    print("Test B2: Spatial-only field with stronger coupling (1e-3)")
    field_b2 = analytic_spatial_only_field(nodes, mass_pos, 1e-3)
    fmin, fmax, fmean = field_stats(field_b2, nodes)
    print(f"  Field range: [{fmin:.2e}, {fmax:.2e}], mean={fmean:.2e}")
    delta, direction, c0, cm, p0, pm = run_single_test(
        "B2", field_b2, flat_field, nodes, source, width)
    print(f"  Flat centroid:  {c0:+.6f}  (prob={p0:.3e})")
    print(f"  Mass centroid:  {cm:+.6f}  (prob={pm:.3e})")
    print(f"  Delta:          {delta:+.6f}  => {direction}")

    # ── Test C: Linear Poisson solver ──
    print(f"\n{'─' * 72}")
    print("Test C: Linear Poisson solver (source + avg, no (1-support))")
    field_c = linear_poisson_field(nodes, cluster)
    fmin, fmax, fmean = field_stats(field_c, nodes)
    print(f"  Field range: [{fmin:.2e}, {fmax:.2e}], mean={fmean:.2e}")
    delta, direction, c0, cm, p0, pm = run_single_test(
        "C", field_c, flat_field, nodes, source, width)
    print(f"  Flat centroid:  {c0:+.6f}  (prob={p0:.3e})")
    print(f"  Mass centroid:  {cm:+.6f}  (prob={pm:.3e})")
    print(f"  Delta:          {delta:+.6f}  => {direction}")

    # ── Test D: Nonlinear derive_node_field (original) ──
    print(f"\n{'─' * 72}")
    print("Test D: derive_node_field (nonlinear: support + (1-support)*avg)")
    field_d = nonlinear_field(nodes, cluster)
    fmin, fmax, fmean = field_stats(field_d, nodes)
    print(f"  Field range: [{fmin:.2e}, {fmax:.2e}], mean={fmean:.2e}")
    delta, direction, c0, cm, p0, pm = run_single_test(
        "D", field_d, flat_field, nodes, source, width)
    print(f"  Flat centroid:  {c0:+.6f}  (prob={p0:.3e})")
    print(f"  Mass centroid:  {cm:+.6f}  (prob={pm:.3e})")
    print(f"  Delta:          {delta:+.6f}  => {direction}")

    # ── Test E: Vary field strength (spatial-only) ──
    print(f"\n{'─' * 72}")
    print("Test E: Spatial-only field at varying strengths")
    print(f"  {'strength':>12} | {'delta':>12} | {'direction':>9} | field_max")
    print(f"  {'-' * 55}")
    for s in [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 5e-2, 1e-1]:
        field_e = analytic_spatial_only_field(nodes, mass_pos, s)
        delta, direction, _, _, _, _ = run_single_test(
            f"E_{s}", field_e, flat_field, nodes, source, width)
        _, fmax_e, _ = field_stats(field_e, nodes)
        print(f"  {s:>12.1e} | {delta:>+12.6f} | {direction:>9} | {fmax_e:.3e}")

    # ── Test F: Check if DAG ordering matters ──
    # The 2D scripts use field-dependent arrival times for the DAG,
    # while our tests above use flat-space DAG. Let's also try with
    # field-dependent DAG.
    print(f"\n{'─' * 72}")
    print("Test F: Field-dependent DAG (arrival times include field)")
    print("  (This is what the original 2D VL script does)")

    from toy_event_physics import infer_arrival_times_with_field

    def propagate_vl_field_dag(nodes, source, node_field, width, k=K, p=P):
        """VL propagation with field-dependent DAG ordering."""
        rule = derive_local_rule(frozenset(), RulePostulates(
            phase_per_action=k, attenuation_power=p))
        arrival = infer_arrival_times_with_field(nodes, source, rule, node_field)
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
                act = L * (1.0 - f)
                edge_amp = cmath.exp(1j * k * act) / (L ** p)
                states[neighbor] += amp * edge_amp

        return detector

    # Re-run spatial-only with field-dependent DAG
    for label, fld in [("spatial s=1e-4", analytic_spatial_only_field(nodes, mass_pos, 1e-4)),
                       ("spatial s=1e-3", analytic_spatial_only_field(nodes, mass_pos, 1e-3)),
                       ("nonlinear",     nonlinear_field(nodes, cluster))]:
        det_flat_fdag = propagate_vl_field_dag(nodes, source, flat_field, width)
        det_mass_fdag = propagate_vl_field_dag(nodes, source, fld, width)
        c0, p0 = centroid(det_flat_fdag)
        cm, pm = centroid(det_mass_fdag)
        delta = cm - c0
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  {label:>20}: delta={delta:+.6f} => {direction}")

    # ── Test G: Attenuation mode (geometry vs delay) ──
    print(f"\n{'─' * 72}")
    print("Test G: Attenuation 1/L^p (geometry) vs 1/delay^p")
    print("  The 3D scripts use 1/L^p. The 2D default uses 1/delay^p.")
    print("  In flat space, delay = L*(1+f), so 1/delay^p differs from 1/L^p.")

    def propagate_vl_delay_atten(nodes, source, node_field, width, k=K, p=P):
        """VL with 1/delay^p attenuation (2D default behavior)."""
        flat = {n: 0.0 for n in nodes}
        rule = derive_local_rule(frozenset(), RulePostulates(
            phase_per_action=k, attenuation_power=p))
        from toy_event_physics import infer_arrival_times_with_field
        arrival = infer_arrival_times_with_field(nodes, source, rule, flat)
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
                act = L * (1.0 - f)
                delay = L * (1.0 + f)
                # Attenuation by delay instead of L
                edge_amp = cmath.exp(1j * k * act) / (delay ** p)
                states[neighbor] += amp * edge_amp

        return detector

    for label, fld in [("spatial s=1e-4", analytic_spatial_only_field(nodes, mass_pos, 1e-4)),
                       ("spatial s=1e-3", analytic_spatial_only_field(nodes, mass_pos, 1e-3)),
                       ("nonlinear",     nonlinear_field(nodes, cluster))]:
        det_flat_d = propagate_vl_delay_atten(nodes, source, flat_field, width)
        det_mass_d = propagate_vl_delay_atten(nodes, source, fld, width)
        c0, _ = centroid(det_flat_d)
        cm, _ = centroid(det_mass_d)
        delta = cm - c0
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  1/delay^p  {label:>20}: delta={delta:+.6f} => {direction}")

        det_flat_g = propagate_vl(nodes, source, flat_field, width)
        det_mass_g = propagate_vl(nodes, source, fld, width)
        c0, _ = centroid(det_flat_g)
        cm, _ = centroid(det_mass_g)
        delta = cm - c0
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  1/L^p      {label:>20}: delta={delta:+.6f} => {direction}")

    # ── Test H: Mass on opposite side (sanity check) ──
    print(f"\n{'─' * 72}")
    print("Test H: Mass at (10, -4) instead of (10, +4) — sign should flip")
    mass_neg = (10, -4)
    field_neg = analytic_spatial_only_field(nodes, mass_neg, 1e-3)
    delta_neg, dir_neg, _, _, _, _ = run_single_test(
        "H_neg", field_neg, flat_field, nodes, source, width)
    field_pos = analytic_spatial_only_field(nodes, mass_pos, 1e-3)
    delta_pos, dir_pos, _, _, _, _ = run_single_test(
        "H_pos", field_pos, flat_field, nodes, source, width)
    print(f"  Mass at y=+4: delta={delta_pos:+.6f} => {dir_pos} (should be TOWARD +4)")
    print(f"  Mass at y=-4: delta={delta_neg:+.6f} => {dir_neg} (should be TOWARD -4)")
    if delta_pos > 0 and delta_neg < 0:
        print("  CONSISTENT: both deflect TOWARD the mass.")
    elif delta_pos < 0 and delta_neg > 0:
        print("  CONSISTENT repulsion: both deflect AWAY from mass.")
    else:
        print("  INCONSISTENT: deflections don't have opposite signs!")

    # ── Summary ────────────────────────────────────────────────
    print(f"\n{'=' * 72}")
    print("SUMMARY TABLE")
    print(f"{'=' * 72}")
    print(f"  {'Test':>4} | {'Field type':<30} | {'delta':>12} | {'direction':>9}")
    print(f"  {'-' * 65}")

    # Re-run everything compactly for the table
    tests = [
        ("A", "Analytic 1/r (full radius)", analytic_full_radius_field(nodes, mass_pos, 1e-4)),
        ("B", "Analytic spatial-only 1/|y|", analytic_spatial_only_field(nodes, mass_pos, 1e-4)),
        ("B2", "Spatial-only (stronger)", analytic_spatial_only_field(nodes, mass_pos, 1e-3)),
        ("C", "Linear Poisson solver", linear_poisson_field(nodes, cluster)),
        ("D", "Nonlinear derive_node_field", nonlinear_field(nodes, cluster)),
    ]
    for tid, desc, fld in tests:
        delta, direction, _, _, _, _ = run_single_test(tid, fld, flat_field, nodes, source, width)
        print(f"  {tid:>4} | {desc:<30} | {delta:>+12.6f} | {direction:>9}")

    print(f"\n{'=' * 72}")
    print("DIAGNOSIS")
    print(f"{'=' * 72}")

    # Collect results for diagnosis
    results = {}
    for tid, desc, fld in tests:
        delta, direction, _, _, _, _ = run_single_test(tid, fld, flat_field, nodes, source, width)
        results[tid] = (delta, direction)

    all_away = all(d[1] == "AWAY" for d in results.values())
    all_toward = all(d[1] == "TOWARD" for d in results.values())
    mixed = not all_away and not all_toward

    if all_toward:
        print("\n  ALL tests give TOWARD in 2D.")
        print("  => The AWAY result in original 2D was due to a specific")
        print("     feature of derive_node_field or the propagation setup,")
        print("     not the 2D geometry itself.")
    elif all_away:
        print("\n  ALL tests give AWAY in 2D.")
        print("  => The 2D path topology is the cause.")
        print("  => The sign flip between 2D and 3D is FUNDAMENTAL,")
        print("     not an artifact of the field solver.")
    elif mixed:
        print("\n  MIXED results — some TOWARD, some AWAY.")
        toward_tests = [t for t, (d, dr) in results.items() if dr == "TOWARD"]
        away_tests = [t for t, (d, dr) in results.items() if dr == "AWAY"]
        print(f"  TOWARD: {toward_tests}")
        print(f"  AWAY:   {away_tests}")
        print("  => The sign depends on the field type/solver, not just geometry.")
        print("  => Comparing TOWARD vs AWAY tests will identify the cause.")

    print()


if __name__ == "__main__":
    main()
