#!/usr/bin/env python3
"""Weak coupling regime: does small-k gravity have distance falloff?

At large k (≥1.5), the beam undergoes complete polarity flip (shift≈±28).
This is saturated — no distance dependence possible.

At small k (<0.5), the shift is proportional to k and much smaller.
In this LINEAR regime, the distance scaling should be physical.

Test: sweep impact parameter at k=0.1, 0.2, 0.3, 0.5 on 60x61 grid.
Look for 1/b falloff in the linear regime.

PStack experiment: weak-coupling-distance
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
                   detector_xs, screen_ys):
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
            atten = 1.0 / (L ** atten_power) if L > 0 else 1.0
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
    postulates = RulePostulates(phase_per_action=0.3, attenuation_power=1.0)
    free_field = {n: 0.0 for n in nodes}

    mass_x = 30
    detector_xs = [35, 40, 45, 50]

    print("=" * 80)
    print("WEAK COUPLING DISTANCE SCALING")
    print(f"  Grid: {width}x{2*height+1}, source=(0,0), mass at x={mass_x}")
    print("  1/L^p attenuation (geometry only)")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: Verify linear regime
    # ================================================================
    print("TEST 1: Identify linear regime (shift vs k)")
    print(f"  Mass at (30, y=6..8), impact b=6")
    print()

    mn = frozenset((mass_x, y) for y in range(5, 9))
    mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
    mf = derive_node_field(nodes, mr)

    print(f"  {'k':>6s}  {'avg_shift':>10s}  {'shift/k':>8s}  {'regime':>8s}")
    print(f"  {'-' * 38}")

    prev_ratio = None
    for k in [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]:
        free_r = propagate_geom(nodes, source, free_field, k, 1.0, detector_xs, screen_ys)
        mass_r = propagate_geom(nodes, source, mf, k, 1.0, detector_xs, screen_ys)
        shifts = [centroid_y(mass_r[dx]) - centroid_y(free_r[dx]) for dx in detector_xs]
        avg = sum(shifts) / len(shifts)
        ratio = avg / k if k > 0 else 0

        regime = "LINEAR" if prev_ratio and abs(ratio - prev_ratio) / (abs(prev_ratio) + 1e-10) < 0.2 else "?"
        if abs(avg) > height * 0.8:
            regime = "SATURATED"
        prev_ratio = ratio

        print(f"  {k:6.2f}  {avg:+10.3f}  {ratio:+8.2f}  {regime:>8s}")

    # ================================================================
    # TEST 2: Distance scaling in linear regime
    # ================================================================
    print()
    print("TEST 2: Distance scaling at small k (linear regime)")
    print()

    for k in [0.1, 0.2, 0.3, 0.5]:
        print(f"  k = {k}:")
        print(f"    {'b':>4s}  {'shift':>10s}  {'shift×b':>9s}  {'shift×b²':>9s}")
        print(f"    {'-' * 36}")

        free_r = propagate_geom(nodes, source, free_field, k, 1.0, detector_xs, screen_ys)
        ref_cys = {dx: centroid_y(free_r[dx]) for dx in detector_xs}

        bs = [3, 4, 5, 6, 8, 10, 12, 15, 18, 20, 25]
        data = []

        for b in bs:
            mn = frozenset((mass_x, y) for y in range(b - 1, b + 2))
            mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
            mf = derive_node_field(nodes, mr)
            mass_r = propagate_geom(nodes, source, mf, k, 1.0, detector_xs, screen_ys)
            shifts = [centroid_y(mass_r[dx]) - ref_cys[dx] for dx in detector_xs]
            avg = sum(shifts) / len(shifts)
            data.append((b, avg))
            print(f"    {b:4d}  {avg:+10.4f}  {avg*b:+9.2f}  {avg*b*b:+9.1f}")

        # Fit power law
        valid = [(b, s) for b, s in data if s > 0.001]
        if len(valid) > 3:
            log_b = [math.log(b) for b, _ in valid]
            log_s = [math.log(s) for _, s in valid]
            n = len(valid)
            mb = sum(log_b) / n
            ms = sum(log_s) / n
            num = sum((lb - mb) * (ls - ms) for lb, ls in zip(log_b, log_s))
            den = sum((lb - mb) ** 2 for lb in log_b)
            slope = num / den if den > 0 else 0
            print(f"    → shift ~ b^({slope:.3f})")
            if abs(slope + 1) < 0.3:
                print(f"    → Consistent with 1/b falloff!")
            elif abs(slope) < 0.2:
                print(f"    → Flat (no falloff)")
            else:
                print(f"    → Power law with exponent {slope:.2f}")
        print()

    # ================================================================
    # TEST 3: Deflection angle at fixed k
    # ================================================================
    print("TEST 3: Deflection angle θ = shift / lever_arm")
    print(f"  k=0.2, lever_arm = det_x - mass_x")
    print()

    k = 0.2
    print(f"  {'b':>4s}  {'shift':>10s}  {'angle':>10s}  {'angle×b':>10s}")
    print(f"  {'-' * 40}")

    free_r = propagate_geom(nodes, source, free_field, k, 1.0, detector_xs, screen_ys)
    ref_cys = {dx: centroid_y(free_r[dx]) for dx in detector_xs}

    for b in [3, 5, 8, 10, 12, 15, 20, 25]:
        mn = frozenset((mass_x, y) for y in range(b - 1, b + 2))
        mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
        mf = derive_node_field(nodes, mr)
        mass_r = propagate_geom(nodes, source, mf, k, 1.0, detector_xs, screen_ys)

        # Average deflection angle across detectors
        angles = []
        for dx in detector_xs:
            shift = centroid_y(mass_r[dx]) - ref_cys[dx]
            lever = dx - mass_x
            angles.append(shift / lever if lever > 0 else 0)

        avg_angle = sum(angles) / len(angles)
        avg_shift = sum(centroid_y(mass_r[dx]) - ref_cys[dx] for dx in detector_xs) / len(detector_xs)
        print(f"  {b:4d}  {avg_shift:+10.4f}  {avg_angle:+10.5f}  {avg_angle*b:+10.4f}")

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("LINEAR REGIME (k < ~0.5): shift is proportional to k.")
    print("If shift ~ 1/b in this regime: genuine gravitational deflection.")
    print("If still flat: the phase effect is non-perturbative even at small k.")
    print()
    print("The key observable is the DEFLECTION ANGLE θ = shift/lever_arm.")
    print("If θ ~ 1/b: this is the 2D analog of gravitational lensing.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
