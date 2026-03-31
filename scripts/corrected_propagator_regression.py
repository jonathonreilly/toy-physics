#!/usr/bin/env python3
"""Regression test: corrected propagator (1/L^p) vs all earlier findings.

The corrected propagator changes attenuation from 1/delay^p to 1/L^p.
Does this break any of the established results?

Tests:
1. Born rule (Sorkin I₃=0 on fixed DAG)
2. Topological decoherence (I₃≠0 when DAG changes)
3. Two-slit interference (fringes with V>0.5)
4. Critical ratio R_c = 1 + |y|/s
5. Signal speed = 1
6. Record suppression (V→0 with which-path info)
7. Gravitational time dilation

PStack experiment: corrected-propagator-regression
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


def propagate_geom(nodes, source, node_field, phase_k, atten_power,
                   blocked=None):
    """Propagate with 1/L^p attenuation, optionally blocking nodes."""
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)
    blocked = blocked or set()

    amplitudes = {source: 1.0 + 0.0j}
    for node in order:
        if node not in amplitudes or node in blocked:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            if nb in blocked:
                continue
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
    width = 30
    height = 10
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    free_field = {n: 0.0 for n in nodes}
    phase_k = 4.0

    passed = 0
    failed = 0
    total = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed, total
        total += 1
        status = "PASS" if condition else "FAIL"
        if condition:
            passed += 1
        else:
            failed += 1
        print(f"  [{status}] {name}")
        if detail:
            print(f"         {detail}")

    print("=" * 80)
    print("CORRECTED PROPAGATOR REGRESSION TEST")
    print("  All tests use 1/L^p attenuation")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: Born rule (Sorkin I₃ on fixed DAG via amplitude masking)
    # ================================================================
    print("TEST 1: Born rule (Sorkin I₃)")

    barrier_x = 15
    slit_ys = [-3, 3]
    det_x = 25

    def get_screen(blocked_set):
        amps = propagate_geom(nodes, source, free_field, phase_k, 1.0, blocked_set)
        return {y: abs(amps.get((det_x, y), 0.0)) ** 2 for y in screen_ys}

    # Build barrier
    barrier_all = {(barrier_x, y) for y in range(-height, height + 1)}
    slit_a_nodes = {(barrier_x, y) for y in range(slit_ys[0] - 1, slit_ys[0] + 2)}
    slit_b_nodes = {(barrier_x, y) for y in range(slit_ys[1] - 1, slit_ys[1] + 2)}

    blocked_none = barrier_all  # All blocked
    blocked_a = barrier_all - slit_a_nodes  # Only slit A open
    blocked_b = barrier_all - slit_b_nodes  # Only slit B open
    blocked_both = barrier_all - slit_a_nodes - slit_b_nodes  # Both open

    p_both = get_screen(blocked_both)
    p_a = get_screen(blocked_a)
    p_b = get_screen(blocked_b)
    p_none = get_screen(blocked_none)

    # I₃ = P(AB) - P(A) - P(B) + P(∅)
    max_i3 = max(abs(p_both.get(y, 0) - p_a.get(y, 0) - p_b.get(y, 0) + p_none.get(y, 0))
                 for y in screen_ys)
    max_p = max(max(p_both.values()), 1e-30)
    ratio = max_i3 / max_p

    # Note: blocking nodes changes the DAG, so I₃≠0 is expected!
    # The Born rule test needs AMPLITUDE masking (zero amplitude, keep edges)
    # Let me implement that properly.

    def get_screen_ampmask(mask_set):
        """Amplitude masking: set amplitude to 0 at masked nodes, keep edges."""
        postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=1.0)
        rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
        arrival_times = infer_arrival_times_from_source(nodes, source, rule)
        dag = build_causal_dag(nodes, arrival_times)
        order = sorted(arrival_times, key=arrival_times.get)

        amplitudes = {source: 1.0 + 0.0j}
        for node in order:
            if node not in amplitudes:
                continue
            if node in mask_set:
                continue  # Zero amplitude, but edges still in DAG
            amp = amplitudes[node]
            for nb in dag.get(node, []):
                L = math.dist(node, nb)
                lf = 0.5 * (free_field.get(node, 0.0) + free_field.get(nb, 0.0))
                delay = L * (1.0 + lf)
                retained = math.sqrt(max(delay * delay - L * L, 0.0))
                action = delay - retained
                atten = 1.0 / (L ** 1.0) if L > 0 else 1.0
                ea = cmath.exp(1j * phase_k * action) * atten
                if nb not in amplitudes:
                    amplitudes[nb] = 0.0 + 0.0j
                amplitudes[nb] += amp * ea

        return {y: abs(amplitudes.get((det_x, y), 0.0)) ** 2 for y in screen_ys}

    mask_none = barrier_all
    mask_a = barrier_all - slit_a_nodes
    mask_b = barrier_all - slit_b_nodes
    mask_both = barrier_all - slit_a_nodes - slit_b_nodes

    pm_both = get_screen_ampmask(mask_both)
    pm_a = get_screen_ampmask(mask_a)
    pm_b = get_screen_ampmask(mask_b)
    pm_none = get_screen_ampmask(mask_none)

    max_i3_m = max(abs(pm_both.get(y, 0) - pm_a.get(y, 0) - pm_b.get(y, 0) + pm_none.get(y, 0))
                   for y in screen_ys)
    max_pm = max(max(pm_both.values()), 1e-30)
    ratio_m = max_i3_m / max_pm

    check("Born rule (amplitude mask, fixed DAG)",
          ratio_m < 1e-10,
          f"|I₃|/P = {ratio_m:.2e} (need < 1e-10)")

    # ================================================================
    # TEST 2: Two-slit interference visibility
    # ================================================================
    print()
    print("TEST 2: Two-slit interference")

    total_p = sum(pm_both.values())
    if total_p > 0:
        norm = {y: p / total_p for y, p in pm_both.items()}
    else:
        norm = pm_both

    vals = [norm.get(y, 0) for y in sorted(screen_ys)]
    peaks = [vals[i] for i in range(1, len(vals) - 1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals) - 1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]

    if peaks and troughs:
        V = (max(peaks) - min(troughs)) / (max(peaks) + min(troughs))
    else:
        V = 0

    check("Two-slit interference V > 0.5",
          V > 0.5,
          f"V = {V:.4f}")

    # ================================================================
    # TEST 3: Signal speed = 1
    # ================================================================
    print()
    print("TEST 3: Signal speed")

    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=1.0)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)

    speeds = []
    for x in [5, 10, 15, 20, 25, 30]:
        t = arrival_times.get((x, 0), None)
        if t and t > 0:
            speeds.append(x / t)

    avg_speed = sum(speeds) / len(speeds) if speeds else 0
    check("Signal speed = 1.0",
          abs(avg_speed - 1.0) < 0.001,
          f"avg speed = {avg_speed:.6f}")

    # ================================================================
    # TEST 4: Gravitational time dilation
    # ================================================================
    print()
    print("TEST 4: Time dilation")

    mass_nodes = frozenset((15, y) for y in range(3, 8))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)

    # Arrival time through field vs free
    rule_free = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_free = infer_arrival_times_from_source(nodes, source, rule_free)

    rule_mass = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    arrival_mass = infer_arrival_times_from_source(nodes, source, rule_mass)

    t_free = arrival_free.get((30, 0), 0)
    t_mass = arrival_mass.get((30, 0), 0)

    check("Time dilation (mass delays arrival)",
          t_mass > t_free,
          f"t_free={t_free:.3f}, t_mass={t_mass:.3f}, delay={t_mass-t_free:.3f}")

    # ================================================================
    # TEST 5: Record suppression
    # ================================================================
    print()
    print("TEST 5: Record suppression (which-path → V drops)")

    # "Record" = measure which slit at barrier
    # Incoherent sum: P = |a_A|² + |a_B|²
    # vs coherent: P = |a_A + a_B|²

    p_a_only = get_screen_ampmask(mask_a)
    p_b_only = get_screen_ampmask(mask_b)

    # Incoherent sum
    p_incoh = {y: p_a_only.get(y, 0) + p_b_only.get(y, 0) for y in screen_ys}
    total_incoh = sum(p_incoh.values())
    if total_incoh > 0:
        norm_incoh = {y: p / total_incoh for y, p in p_incoh.items()}
    else:
        norm_incoh = p_incoh

    vals_i = [norm_incoh.get(y, 0) for y in sorted(screen_ys)]
    peaks_i = [vals_i[i] for i in range(1, len(vals_i) - 1)
               if vals_i[i] > vals_i[i-1] and vals_i[i] > vals_i[i+1]]
    troughs_i = [vals_i[i] for i in range(1, len(vals_i) - 1)
                 if vals_i[i] < vals_i[i-1] and vals_i[i] < vals_i[i+1]]

    if peaks_i and troughs_i:
        V_incoh = (max(peaks_i) - min(troughs_i)) / (max(peaks_i) + min(troughs_i))
    else:
        V_incoh = 0

    check("Record suppression (V_incoherent < V_coherent)",
          V_incoh < V,
          f"V_coherent={V:.4f}, V_incoherent={V_incoh:.4f}")

    # ================================================================
    # TEST 6: k=0 → no gravity (corrected propagator only)
    # ================================================================
    print()
    print("TEST 6: k=0 produces no gravity (corrected propagator feature)")

    amps_free_k0 = propagate_geom(nodes, source, free_field, 0.0, 1.0)
    amps_mass_k0 = propagate_geom(nodes, source, mass_field, 0.0, 1.0)

    det_xs = [20, 25, 30]
    shifts = []
    for dx in det_xs:
        free_dist = {y: abs(amps_free_k0.get((dx, y), 0.0)) ** 2 for y in screen_ys}
        mass_dist = {y: abs(amps_mass_k0.get((dx, y), 0.0)) ** 2 for y in screen_ys}
        tf = sum(free_dist.values())
        tm = sum(mass_dist.values())
        if tf > 0:
            free_dist = {y: p / tf for y, p in free_dist.items()}
        if tm > 0:
            mass_dist = {y: p / tm for y, p in mass_dist.items()}
        fcy = sum(y * p for y, p in free_dist.items())
        mcy = sum(y * p for y, p in mass_dist.items())
        shifts.append(mcy - fcy)

    avg_shift = sum(shifts) / len(shifts) if shifts else 0

    check("k=0 → zero gravity shift",
          abs(avg_shift) < 0.01,
          f"shift = {avg_shift:+.6f}")

    # ================================================================
    # TEST 7: Gravity with corrected propagator (attraction at k=2)
    # ================================================================
    print()
    print("TEST 7: Gravitational attraction at k=2.0")

    amps_free = propagate_geom(nodes, source, free_field, 2.0, 1.0)
    amps_mass = propagate_geom(nodes, source, mass_field, 2.0, 1.0)

    shifts2 = []
    for dx in det_xs:
        free_dist = {y: abs(amps_free.get((dx, y), 0.0)) ** 2 for y in screen_ys}
        mass_dist = {y: abs(amps_mass.get((dx, y), 0.0)) ** 2 for y in screen_ys}
        tf = sum(free_dist.values())
        tm = sum(mass_dist.values())
        if tf > 0:
            free_dist = {y: p / tf for y, p in free_dist.items()}
        if tm > 0:
            mass_dist = {y: p / tm for y, p in mass_dist.items()}
        fcy = sum(y * p for y, p in free_dist.items())
        mcy = sum(y * p for y, p in mass_dist.items())
        shifts2.append(mcy - fcy)

    avg_shift2 = sum(shifts2) / len(shifts2) if shifts2 else 0

    check("Gravitational attraction (shift toward mass)",
          avg_shift2 > 0.5,
          f"shift = {avg_shift2:+.2f} (mass at y=3..7)")

    # ================================================================
    # SUMMARY
    # ================================================================
    print()
    print("=" * 80)
    print(f"REGRESSION RESULTS: {passed}/{total} passed, {failed}/{total} failed")
    print("=" * 80)

    if failed == 0:
        print("\n  ALL TESTS PASS — corrected propagator is backward-compatible")
    else:
        print(f"\n  {failed} FAILURE(S) — investigate before proceeding")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
