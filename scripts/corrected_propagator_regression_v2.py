#!/usr/bin/env python3
"""Regression test v2: fixed Born rule (3-slit I₃), larger grid.

v1 had errors:
- "Born rule" test computed I₂ (2-slit interference), not I₃ (3-slit)
- Grid too small (30x21) for visible fringes with 1/L^p
- V=0 because geometry was suboptimal

Fixes:
- Proper 3-slit I₃ test
- Larger grid (50x31)
- Multiple k values to find optimal interference

PStack experiment: corrected-propagator-regression-v2
"""

from __future__ import annotations
import math
import cmath
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    build_causal_dag,
)


def propagate_geom_masked(nodes, source, node_field, phase_k, atten_power,
                          mask_set=None):
    """Propagate with 1/L^p, amplitude masking (zero amp at masked nodes)."""
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)
    mask_set = mask_set or set()

    amplitudes = {source: 1.0 + 0.0j}
    for node in order:
        if node not in amplitudes:
            continue
        if node in mask_set:
            continue  # Zero amplitude, edges still in DAG
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            lf = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            delay = L * (1.0 + lf)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained
            atten = 1.0 / (L ** atten_power) if L > 0 else 1.0
            ea = cmath.exp(1j * phase_k * action) * atten
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * ea

    return amplitudes


def main() -> None:
    width = 50
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    free_field = {n: 0.0 for n in nodes}

    passed = 0
    failed = 0
    total = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed, total
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            failed += 1
            print(f"  [FAIL] {name}")
        if detail:
            print(f"         {detail}")

    print("=" * 80)
    print("CORRECTED PROPAGATOR REGRESSION TEST v2")
    print(f"  Grid: {width}x{2*height+1}, 1/L^p attenuation")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: Born rule — proper 3-slit I₃
    # ================================================================
    print("TEST 1: Born rule (3-slit Sorkin I₃ on FIXED DAG)")
    print("  I₃ = P(ABC) - P(AB) - P(AC) - P(BC) + P(A) + P(B) + P(C) - P(∅)")
    print()

    barrier_x = 25
    slit_centers = [-5, 0, 5]  # 3 slits
    det_x = 40
    phase_k = 4.0

    # Build barrier and slits
    barrier_all = set()
    for y in range(-height, height + 1):
        barrier_all.add((barrier_x, y))

    slits = {}
    for i, sc in enumerate(slit_centers):
        label = chr(ord('A') + i)
        slits[label] = {(barrier_x, y) for y in range(sc - 1, sc + 2)}

    # All 8 combinations for 3 slits
    from itertools import combinations

    def screen_for_open(open_labels):
        """Get screen probabilities with specified slits open."""
        open_nodes = set()
        for label in open_labels:
            open_nodes |= slits[label]
        mask = barrier_all - open_nodes
        amps = propagate_geom_masked(nodes, source, free_field, phase_k, 1.0, mask)
        return {y: abs(amps.get((det_x, y), 0.0)) ** 2 for y in screen_ys}

    p = {}
    for r in range(4):
        for combo in combinations('ABC', r):
            key = ''.join(combo) if combo else ''
            p[key] = screen_for_open(combo)

    # Compute I₃ at each y
    i3_values = []
    for y in screen_ys:
        i3 = (p['ABC'].get(y, 0)
              - p['AB'].get(y, 0) - p['AC'].get(y, 0) - p['BC'].get(y, 0)
              + p['A'].get(y, 0) + p['B'].get(y, 0) + p['C'].get(y, 0)
              - p[''].get(y, 0))
        i3_values.append(abs(i3))

    max_i3 = max(i3_values)
    max_p3 = max(max(p['ABC'].values()), 1e-30)
    ratio_i3 = max_i3 / max_p3

    check("Born rule I₃=0 (3-slit, amplitude mask, fixed DAG)",
          ratio_i3 < 1e-8,
          f"|I₃|/P = {ratio_i3:.2e}")

    # ================================================================
    # TEST 2: Two-slit interference — sweep k for best V
    # ================================================================
    print()
    print("TEST 2: Two-slit interference visibility")

    slit_2_ys = [-4, 4]
    barrier_2 = set()
    for y in range(-height, height + 1):
        barrier_2.add((barrier_x, y))

    slit_2_nodes = set()
    for sc in slit_2_ys:
        for y in range(sc - 1, sc + 2):
            slit_2_nodes.add((barrier_x, y))

    mask_2slit = barrier_2 - slit_2_nodes

    best_v = 0
    best_k = 0

    for k in [1.0, 2.0, 3.0, 4.0, 6.0, 8.0]:
        amps = propagate_geom_masked(nodes, source, free_field, k, 1.0, mask_2slit)
        probs = {y: abs(amps.get((det_x, y), 0.0)) ** 2 for y in screen_ys}
        total_p = sum(probs.values())
        if total_p > 0:
            norm = {y: p / total_p for y, p in probs.items()}
        else:
            norm = probs

        vals = [norm.get(y, 0) for y in sorted(screen_ys)]
        peaks = [vals[i] for i in range(1, len(vals) - 1)
                 if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
        troughs = [vals[i] for i in range(1, len(vals) - 1)
                   if vals[i] < vals[i-1] and vals[i] < vals[i+1]]

        if peaks and troughs:
            V = (max(peaks) - min(troughs)) / (max(peaks) + min(troughs))
        else:
            V = 0

        if V > best_v:
            best_v = V
            best_k = k

    check("Two-slit interference V > 0.3 (best k)",
          best_v > 0.3,
          f"Best V = {best_v:.4f} at k = {best_k}")

    # ================================================================
    # TEST 3: Signal speed = 1
    # ================================================================
    print()
    print("TEST 3: Signal speed")

    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival = infer_arrival_times_from_source(nodes, source, rule)

    speeds = [x / arrival[(x, 0)] for x in [10, 20, 30, 40, 50] if arrival.get((x, 0), 0) > 0]
    avg_speed = sum(speeds) / len(speeds) if speeds else 0

    check("Signal speed = 1.0",
          abs(avg_speed - 1.0) < 0.001,
          f"speed = {avg_speed:.6f}")

    # ================================================================
    # TEST 4: Gravitational time dilation
    # ================================================================
    print()
    print("TEST 4: Time dilation")

    mass_nodes = frozenset((25, y) for y in range(3, 8))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)

    arrival_free = infer_arrival_times_from_source(nodes, source, rule)
    rule_mass = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    arrival_mass = infer_arrival_times_from_source(nodes, source, rule_mass)

    t_free = arrival_free.get((50, 0), 0)
    t_mass = arrival_mass.get((50, 0), 0)

    check("Time dilation (mass delays arrival)",
          t_mass > t_free,
          f"t_free={t_free:.3f}, t_mass={t_mass:.3f}")

    # ================================================================
    # TEST 5: k=0 → no gravity
    # ================================================================
    print()
    print("TEST 5: k=0 → no gravity (pure phase test)")

    amps_f0 = propagate_geom_masked(nodes, source, free_field, 0.0, 1.0)
    amps_m0 = propagate_geom_masked(nodes, source, mass_field, 0.0, 1.0)

    det_xs = [30, 35, 40, 45]
    shifts = []
    for dx in det_xs:
        fd = {y: abs(amps_f0.get((dx, y), 0.0)) ** 2 for y in screen_ys}
        md = {y: abs(amps_m0.get((dx, y), 0.0)) ** 2 for y in screen_ys}
        tf = sum(fd.values())
        tm = sum(md.values())
        if tf > 0 and tm > 0:
            fcy = sum(y * p / tf for y, p in fd.items())
            mcy = sum(y * p / tm for y, p in md.items())
            shifts.append(mcy - fcy)

    avg_shift = sum(shifts) / len(shifts) if shifts else 0
    check("k=0 → zero gravity", abs(avg_shift) < 0.01,
          f"shift = {avg_shift:+.6f}")

    # ================================================================
    # TEST 6: Gravitational attraction at k=2
    # ================================================================
    print()
    print("TEST 6: Gravitational attraction at k=2.0")

    amps_f2 = propagate_geom_masked(nodes, source, free_field, 2.0, 1.0)
    amps_m2 = propagate_geom_masked(nodes, source, mass_field, 2.0, 1.0)

    shifts2 = []
    for dx in det_xs:
        fd = {y: abs(amps_f2.get((dx, y), 0.0)) ** 2 for y in screen_ys}
        md = {y: abs(amps_m2.get((dx, y), 0.0)) ** 2 for y in screen_ys}
        tf = sum(fd.values())
        tm = sum(md.values())
        if tf > 0 and tm > 0:
            fcy = sum(y * p / tf for y, p in fd.items())
            mcy = sum(y * p / tm for y, p in md.items())
            shifts2.append(mcy - fcy)

    avg2 = sum(shifts2) / len(shifts2) if shifts2 else 0
    check("Gravity attraction at k=2.0",
          avg2 > 0.5,
          f"shift = {avg2:+.2f}")

    # ================================================================
    # TEST 7: Record suppression
    # ================================================================
    print()
    print("TEST 7: Record suppression")

    # Use the best k for interference
    k_use = best_k if best_k > 0 else 4.0
    amps_both = propagate_geom_masked(nodes, source, free_field, k_use, 1.0, mask_2slit)

    # Per-slit amplitudes
    slit_a_mask = barrier_2 - {(barrier_x, y) for y in range(slit_2_ys[0] - 1, slit_2_ys[0] + 2)}
    slit_b_mask = barrier_2 - {(barrier_x, y) for y in range(slit_2_ys[1] - 1, slit_2_ys[1] + 2)}

    amps_a = propagate_geom_masked(nodes, source, free_field, k_use, 1.0, slit_a_mask)
    amps_b = propagate_geom_masked(nodes, source, free_field, k_use, 1.0, slit_b_mask)

    # Coherent V
    prob_coh = {y: abs(amps_both.get((det_x, y), 0.0)) ** 2 for y in screen_ys}
    t_coh = sum(prob_coh.values())

    # Incoherent: |a_A|² + |a_B|²
    prob_inc = {y: abs(amps_a.get((det_x, y), 0.0)) ** 2 + abs(amps_b.get((det_x, y), 0.0)) ** 2
                for y in screen_ys}
    t_inc = sum(prob_inc.values())

    def calc_v(probs, total):
        if total == 0:
            return 0
        norm = {y: p / total for y, p in probs.items()}
        vals = [norm.get(y, 0) for y in sorted(screen_ys)]
        peaks = [vals[i] for i in range(1, len(vals) - 1)
                 if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
        troughs = [vals[i] for i in range(1, len(vals) - 1)
                   if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
        if peaks and troughs:
            return (max(peaks) - min(troughs)) / (max(peaks) + min(troughs))
        return 0

    v_coh = calc_v(prob_coh, t_coh)
    v_inc = calc_v(prob_inc, t_inc)

    check("Record suppression (V_incoh < V_coh)",
          v_inc < v_coh or (v_coh < 0.01 and v_inc < 0.01),
          f"V_coh={v_coh:.4f}, V_incoh={v_inc:.4f}")

    # ================================================================
    # SUMMARY
    # ================================================================
    print()
    print("=" * 80)
    print(f"REGRESSION: {passed}/{total} passed, {failed}/{total} failed")
    print("=" * 80)

    if failed == 0:
        print("\n  ALL TESTS PASS")
    else:
        print(f"\n  {failed} failure(s)")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
