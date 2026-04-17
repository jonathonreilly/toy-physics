#!/usr/bin/env python3
"""Mixed attenuation: interpolate between 1/L^p and 1/delay^p.

The problem:
- 1/delay^p: attraction impossible (attenuation dominates → repulsion)
- 1/L^p: attraction works but flat distance scaling (no falloff)

Hypothesis: the truth is in between. A mixed attenuation
  1/(L * (1 + α*field))^p
with small α retains enough field-dependent attenuation for distance
falloff while keeping phase-based attraction dominant.

At α=0: pure geometry (1/L^p) — attraction, flat scaling
At α=1: standard (1/delay^p) — repulsion
At α between: potentially attraction WITH distance falloff

Also test: does the k=0 gravity disappear as α→0? At which α does
phase-based attraction first dominate attenuation-based repulsion?

PStack experiment: mixed-attenuation-distance
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


def propagate_mixed(nodes, source, node_field, phase_k, atten_power, alpha,
                    detector_xs, screen_ys):
    """Propagate with mixed attenuation: 1/(L*(1+α*field))^p."""
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    amplitudes = {source: 1.0 + 0.0j}
    for node in order:
        if node not in amplitudes:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            lf = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            delay = L * (1.0 + lf)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained

            # Mixed attenuation
            mixed_denom = L * (1.0 + alpha * lf)
            atten = 1.0 / (mixed_denom ** atten_power) if mixed_denom > 0 else 1.0
            ea = cmath.exp(1j * phase_k * action) * atten
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * ea

    result = {}
    for dx in detector_xs:
        dist = {}
        total = 0
        for y in screen_ys:
            p = abs(amplitudes.get((dx, y), 0.0)) ** 2
            dist[y] = p
            total += p
        if total > 0:
            dist = {y: p / total for y, p in dist.items()}
        result[dx] = dist
    return result


def centroid_y(distribution):
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    return sum(y * p for y, p in distribution.items()) / total


def main() -> None:
    width = 60
    height = 30
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    postulates = RulePostulates(phase_per_action=2.0, attenuation_power=1.0)
    free_field = {n: 0.0 for n in nodes}

    mass_nodes = frozenset((30, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)

    detector_xs = [35, 40, 45, 50]

    print("=" * 80)
    print("MIXED ATTENUATION: 1/(L*(1+α*field))^p")
    print("  Interpolate between geometry (α=0) and standard (α=1)")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: α sweep — where does attraction first appear?
    # ================================================================
    print("TEST 1: α sweep at k=2.0 (attraction regime for α=0)")
    print(f"  Mass at x=30, y=4..8. Grid {width}x{2*height+1}")
    print()

    print(f"  {'alpha':>6s}  {'avg_shift':>10s}  {'dir':>8s}  {'k=0_shift':>10s}")
    print(f"  {'-' * 40}")

    for alpha in [0.0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 0.7, 1.0]:
        free_r = propagate_mixed(nodes, source, free_field, 2.0, 1.0, alpha,
                                  detector_xs, screen_ys)
        mass_r = propagate_mixed(nodes, source, mass_field, 2.0, 1.0, alpha,
                                  detector_xs, screen_ys)
        shifts = [centroid_y(mass_r[dx]) - centroid_y(free_r[dx]) for dx in detector_xs]
        avg = sum(shifts) / len(shifts)
        d = "ATTRACT" if avg > 0.5 else "REPEL" if avg < -0.5 else "~0"

        # k=0 test: does attenuation alone cause gravity?
        free_k0 = propagate_mixed(nodes, source, free_field, 0.0, 1.0, alpha,
                                   detector_xs, screen_ys)
        mass_k0 = propagate_mixed(nodes, source, mass_field, 0.0, 1.0, alpha,
                                   detector_xs, screen_ys)
        k0_shifts = [centroid_y(mass_k0[dx]) - centroid_y(free_k0[dx]) for dx in detector_xs]
        k0_avg = sum(k0_shifts) / len(k0_shifts)

        print(f"  {alpha:6.2f}  {avg:+10.2f}  {d:>8s}  {k0_avg:+10.2f}")

    # ================================================================
    # TEST 2: Distance scaling at promising α values
    # ================================================================
    print()
    print("TEST 2: Distance scaling at various α")
    print(f"  k=2.0, mass = 3-node column at x=30")
    print()

    for alpha in [0.0, 0.05, 0.1, 0.2, 0.5]:
        print(f"  α = {alpha}:")
        print(f"    {'b':>4s}  {'avg_shift':>10s}  {'shift×b':>9s}")
        print(f"    {'-' * 28}")

        free_r_ref = propagate_mixed(nodes, source, free_field, 2.0, 1.0, alpha,
                                      detector_xs, screen_ys)
        ref_cys = {dx: centroid_y(free_r_ref[dx]) for dx in detector_xs}

        bs = [3, 5, 8, 10, 15, 20, 25]
        shifts_for_fit = []

        for b in bs:
            mn = frozenset((30, y) for y in range(b - 1, b + 2))
            mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
            mf = derive_node_field(nodes, mr)
            mass_r = propagate_mixed(nodes, source, mf, 2.0, 1.0, alpha,
                                      detector_xs, screen_ys)
            shifts = [centroid_y(mass_r[dx]) - ref_cys[dx] for dx in detector_xs]
            avg = sum(shifts) / len(shifts)
            shifts_for_fit.append((b, avg))
            print(f"    {b:4d}  {avg:+10.3f}  {avg * b:+9.1f}")

        # Power law fit
        valid = [(b, s) for b, s in shifts_for_fit if s > 0.3]
        if len(valid) > 2:
            log_b = [math.log(b) for b, _ in valid]
            log_s = [math.log(s) for _, s in valid]
            n = len(valid)
            mb = sum(log_b) / n
            ms = sum(log_s) / n
            num = sum((lb - mb) * (ls - ms) for lb, ls in zip(log_b, log_s))
            den = sum((lb - mb) ** 2 for lb in log_b)
            slope = num / den if den > 0 else 0
            print(f"    Power law: shift ~ b^({slope:.3f})")
        elif valid:
            print(f"    Too few attractive points for fit")
        else:
            print(f"    No attraction")
        print()

    # ================================================================
    # TEST 3: k-averaged mixed attenuation on larger grid
    # ================================================================
    print("TEST 3: k-averaged (k=1..3) distance scaling")
    print()

    for alpha in [0.0, 0.05, 0.1]:
        print(f"  α = {alpha}, k-averaged [1.0, 1.5, 2.0, 2.5, 3.0]:")
        k_band = [1.0, 1.5, 2.0, 2.5, 3.0]

        print(f"    {'b':>4s}  {'avg_shift':>10s}")
        print(f"    {'-' * 18}")

        for b in [3, 5, 8, 12, 18, 25]:
            mn = frozenset((30, y) for y in range(b - 1, b + 2))
            mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
            mf = derive_node_field(nodes, mr)

            all_shifts = []
            for k in k_band:
                free_r = propagate_mixed(nodes, source, free_field, k, 1.0, alpha,
                                          detector_xs, screen_ys)
                mass_r = propagate_mixed(nodes, source, mf, k, 1.0, alpha,
                                          detector_xs, screen_ys)
                shifts = [centroid_y(mass_r[dx]) - centroid_y(free_r[dx]) for dx in detector_xs]
                all_shifts.extend(shifts)

            avg = sum(all_shifts) / len(all_shifts)
            print(f"    {b:4d}  {avg:+10.3f}")
        print()

    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("If small α (0.05-0.1) gives attraction WITH distance falloff:")
    print("  → The correct propagator is 1/(L*(1+α*f))^p with small α")
    print("  → α represents the fraction of field that affects spreading")
    print("  → Physically: most of the metric is compensated (like √(-g)),")
    print("    but a small residual field-dependent spreading remains")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
