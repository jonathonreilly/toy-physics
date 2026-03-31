#!/usr/bin/env python3
"""Distance scaling on large grid — avoid finite-size saturation.

Previous test showed flat shift because beam saturated at ±25 boundary.
Fix: use 100x100 grid with mass at large x, measure at fixed detector
offset. Keep impact parameter small relative to grid half-height (50).

Also measure deflection ANGLE (shift/distance) rather than raw shift,
which should show 1/b falloff if present.

PStack experiment: distance-scaling-large-grid
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
    width = 80
    height = 40
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    phase_k = 2.0
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=1.0)
    free_field = {n: 0.0 for n in nodes}

    # Detector well past mass
    mass_x = 40
    detector_xs = [50, 55, 60]

    print("=" * 80)
    print("DISTANCE SCALING — LARGE GRID (80x81)")
    print(f"  Mass at x={mass_x}, detectors at {detector_xs}")
    print(f"  k={phase_k}, grid half-height={height}")
    print("=" * 80)
    print()

    print("Building free propagation...")
    free_result = propagate_geom(nodes, source, free_field, phase_k, 1.0,
                                  detector_xs, screen_ys)
    free_cys = {dx: centroid_y(free_result[dx]) for dx in detector_xs}
    print(f"  Free centroids: {', '.join(f'@{dx}={free_cys[dx]:.2f}' for dx in detector_xs)}")
    print()

    # Impact parameter sweep — keep b < height/2 to avoid saturation
    print(f"  {'b':>4s}  {'shift@50':>9s}  {'shift@55':>9s}  {'shift@60':>9s}  "
          f"{'avg_shift':>10s}  {'defl_angle':>10s}  {'shift×b':>8s}")
    print(f"  {'-' * 66}")

    distances = []
    shifts_list = []
    angles_list = []

    for b in [3, 4, 5, 6, 8, 10, 12, 15, 18, 20, 25, 30, 35]:
        mn = frozenset((mass_x, y) for y in range(b - 1, b + 2))
        mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
        mf = derive_node_field(nodes, mr)

        mass_result = propagate_geom(nodes, source, mf, phase_k, 1.0,
                                      detector_xs, screen_ys)

        shifts = []
        for dx in detector_xs:
            mcy = centroid_y(mass_result[dx])
            shifts.append(mcy - free_cys[dx])

        avg = sum(shifts) / len(shifts)
        # Deflection angle ≈ shift / (det_x - mass_x)
        angle = avg / (55 - mass_x) if avg != 0 else 0
        sb = avg * b

        distances.append(b)
        shifts_list.append(avg)
        angles_list.append(angle)

        print(f"  {b:4d}  {shifts[0]:+9.2f}  {shifts[1]:+9.2f}  {shifts[2]:+9.2f}  "
              f"{avg:+10.3f}  {angle:+10.4f}  {sb:+8.1f}")

    # Power law fits
    import math as m
    valid = [(d, s) for d, s in zip(distances, shifts_list) if s > 0.5]
    if len(valid) > 3:
        log_d = [m.log(d) for d, _ in valid]
        log_s = [m.log(s) for _, s in valid]
        n = len(valid)
        mean_ld = sum(log_d) / n
        mean_ls = sum(log_s) / n
        num = sum((ld - mean_ld) * (ls - mean_ls) for ld, ls in zip(log_d, log_s))
        den = sum((ld - mean_ld) ** 2 for ld in log_d)
        alpha = num / den if den > 0 else 0
        print(f"\n  Shift power law: shift ~ b^({alpha:.3f})")
        print(f"  (Newtonian 2D: alpha=-1, GR lensing 2D: alpha=-1)")

    valid_a = [(d, abs(a)) for d, a in zip(distances, angles_list) if abs(a) > 0.001]
    if len(valid_a) > 3:
        log_d = [m.log(d) for d, _ in valid_a]
        log_a = [m.log(a) for _, a in valid_a]
        n = len(valid_a)
        mean_ld = sum(log_d) / n
        mean_la = sum(log_a) / n
        num = sum((ld - mean_ld) * (la - mean_la) for ld, la in zip(log_d, log_a))
        den = sum((ld - mean_ld) ** 2 for ld in log_d)
        alpha_a = num / den if den > 0 else 0
        print(f"  Angle power law: angle ~ b^({alpha_a:.3f})")
        print(f"  (Newtonian 2D: alpha=-1, GR lensing: alpha=-1)")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
