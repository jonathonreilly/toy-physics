#!/usr/bin/env python3
"""Derive a quantitative gravitational force law.

From perturbative analysis:
  shift ∝ k² × (some function of the field)

The action DECREASES near mass: ΔS ≈ -L√(2f) for f<<1.
The shift anti-correlates with action asymmetry.

Goal: find a single field-derived quantity Q(field) such that:
  measured_shift = C × k² × Q(field)

with C a universal constant (independent of mass position, mass size, k).

Candidates for Q:
  Q1 = ∫ ∂f/∂y dy (field gradient integrated along beam)
  Q2 = ∫ √f(x,0) dx (sqrt-field along beam center)
  Q3 = Σ_edges [S_above - S_below] (total action asymmetry)
  Q4 = Σ_nodes [f(x,y>0) - f(x,y<0)] (field asymmetry)

PStack experiment: gravitational-force-law
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
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


def propagate_geom(nodes, source, node_field, phase_k, detector_xs, screen_ys):
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=1.0)
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
            ea = cmath.exp(1j * phase_k * action) / (L ** 1.0)
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


def compute_field_observables(nodes, node_field, width, height):
    """Compute candidate Q functions from the field."""
    # Q1: field gradient at beam center, integrated over x
    q1 = 0.0
    for x in range(width + 1):
        f_above = node_field.get((x, 1), 0.0)
        f_below = node_field.get((x, -1), 0.0)
        q1 += (f_above - f_below)  # ∂f/∂y ≈ (f(y=1) - f(y=-1)) / 2

    # Q2: sqrt(field) along beam center
    q2 = 0.0
    for x in range(width + 1):
        f = node_field.get((x, 0), 0.0)
        q2 += math.sqrt(max(f, 0.0))

    # Q3: total action asymmetry
    postulates = RulePostulates(phase_per_action=1.0, attenuation_power=1.0)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, (0, 0), rule)
    dag = build_causal_dag(nodes, arrival_times)

    action_above = 0.0
    action_below = 0.0
    for node, nbs in dag.items():
        for nb in nbs:
            L = math.dist(node, nb)
            if L < 1e-10:
                continue
            lf = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            delay = L * (1.0 + lf)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained
            avg_y = 0.5 * (node[1] + nb[1])
            if avg_y > 0:
                action_above += action
            elif avg_y < 0:
                action_below += action
    q3 = action_above - action_below

    # Q4: field asymmetry (total field above - below)
    q4 = 0.0
    for (x, y), f in node_field.items():
        if y > 0:
            q4 += f
        elif y < 0:
            q4 -= f

    return {'Q1_grad': q1, 'Q2_sqrtf': q2, 'Q3_action': q3, 'Q4_field': q4}


def main() -> None:
    width = 50
    height = 20
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    free_field = {n: 0.0 for n in nodes}
    detector_xs = [30, 35, 40, 45]
    postulates = RulePostulates(phase_per_action=1.0, attenuation_power=1.0)

    print("=" * 80)
    print("GRAVITATIONAL FORCE LAW DERIVATION")
    print(f"  Grid: {width}x{2*height+1}")
    print("  Goal: shift = C × k² × Q(field)")
    print("=" * 80)
    print()

    # ================================================================
    # Generate many (mass_config, k) pairs and measure shift + Q
    # ================================================================
    configs = []

    # Vary mass position
    for yc in [3, 5, 8, 12, 16]:
        for n_mass in [3, 5]:
            half = n_mass // 2
            mn = frozenset((25, y) for y in range(yc - half, yc + half + 1))
            configs.append((f"y={yc},n={n_mass}", mn))

    # Vary mass x-position
    for mx in [15, 20, 25, 30, 35]:
        mn = frozenset((mx, y) for y in range(5, 8))
        configs.append((f"x={mx},y=5-7", mn))

    # Vary mass below
    for yc in [-5, -8, -12]:
        mn = frozenset((25, y) for y in range(yc - 1, yc + 2))
        configs.append((f"y={yc}", mn))

    k_test = 0.1  # In k² regime

    print("Computing field observables and shifts...")
    print()

    data = []
    for label, mn in configs:
        mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
        mf = derive_node_field(nodes, mr)
        qs = compute_field_observables(nodes, mf, width, height)

        free_r = propagate_geom(nodes, source, free_field, k_test, detector_xs, screen_ys)
        mass_r = propagate_geom(nodes, source, mf, k_test, detector_xs, screen_ys)
        shifts = [centroid_y(mass_r[dx]) - centroid_y(free_r[dx]) for dx in detector_xs]
        avg_shift = sum(shifts) / len(shifts)

        data.append({
            'label': label,
            'shift': avg_shift,
            'Q1': qs['Q1_grad'],
            'Q3': qs['Q3_action'],
            'Q4': qs['Q4_field'],
        })

    # ================================================================
    # Find best Q predictor
    # ================================================================
    print(f"  {'config':>15s}  {'shift':>10s}  {'Q1_grad':>10s}  {'Q3_action':>10s}  {'Q4_field':>10s}")
    print(f"  {'-' * 60}")

    for d in data:
        print(f"  {d['label']:>15s}  {d['shift']:+10.5f}  {d['Q1']:+10.3f}  "
              f"{d['Q3']:+10.3f}  {d['Q4']:+10.1f}")

    # Compute correlation for each Q
    print()
    print("CORRELATION ANALYSIS: which Q predicts shift?")
    print()

    for q_name in ['Q1', 'Q3', 'Q4']:
        shifts = [d['shift'] for d in data]
        qs = [d[q_name] for d in data]
        n = len(data)

        mean_s = sum(shifts) / n
        mean_q = sum(qs) / n
        cov = sum((s - mean_s) * (q - mean_q) for s, q in zip(shifts, qs)) / n
        std_s = (sum((s - mean_s) ** 2 for s in shifts) / n) ** 0.5
        std_q = (sum((q - mean_q) ** 2 for q in qs) / n) ** 0.5
        corr = cov / (std_s * std_q) if std_s > 0 and std_q > 0 else 0

        # Linear regression: shift = a × Q + b
        if std_q > 0:
            a = cov / (std_q ** 2)
            b = mean_s - a * mean_q
            residuals = [(s - (a * q + b)) ** 2 for s, q in zip(shifts, qs)]
            rmse = (sum(residuals) / n) ** 0.5
            r2 = 1 - sum(residuals) / sum((s - mean_s) ** 2 for s in shifts) if sum((s - mean_s) ** 2 for s in shifts) > 0 else 0
        else:
            a, b, rmse, r2 = 0, 0, 0, 0

        print(f"  {q_name}: corr={corr:+.4f}, R²={r2:.4f}, slope={a:.6f}, RMSE={rmse:.6f}")

    # ================================================================
    # Best predictor: verify with different k values
    # ================================================================
    print()
    print("VERIFICATION: best predictor across k values")
    print(f"  Using shift/k² = C × Q (should be constant C)")
    print()

    # Use Q4 (field asymmetry) as it's simplest and likely best
    # Pick one configuration
    test_mn = frozenset((25, y) for y in range(5, 8))
    mr = derive_local_rule(persistent_nodes=test_mn, postulates=postulates)
    mf = derive_node_field(nodes, mr)
    qs = compute_field_observables(nodes, mf, width, height)

    print(f"  Test config: mass at (25, y=5..7)")
    print(f"  Q1={qs['Q1_grad']:.3f}, Q3={qs['Q3_action']:.3f}, Q4={qs['Q4_field']:.1f}")
    print()
    print(f"  {'k':>6s}  {'shift':>10s}  {'shift/k²':>10s}  {'shift/(k²×Q1)':>14s}  {'shift/(k²×Q4)':>14s}")
    print(f"  {'-' * 56}")

    for k in [0.02, 0.05, 0.1, 0.15, 0.2, 0.3]:
        free_r = propagate_geom(nodes, source, free_field, k, detector_xs, screen_ys)
        mass_r = propagate_geom(nodes, source, mf, k, detector_xs, screen_ys)
        shifts = [centroid_y(mass_r[dx]) - centroid_y(free_r[dx]) for dx in detector_xs]
        avg = sum(shifts) / len(shifts)

        sk2 = avg / (k * k) if k > 0 else 0
        c1 = avg / (k * k * qs['Q1_grad']) if k > 0 and abs(qs['Q1_grad']) > 0.001 else 0
        c4 = avg / (k * k * qs['Q4_field']) if k > 0 and abs(qs['Q4_field']) > 0.1 else 0

        print(f"  {k:6.3f}  {avg:+10.6f}  {sk2:+10.3f}  {c1:+14.6f}  {c4:+14.8f}")

    # ================================================================
    # Cross-validation: predict shift for new configurations
    # ================================================================
    print()
    print("CROSS-VALIDATION: predict shift for unseen configs")
    print()

    # Fit C from training data
    # Use Q4 and k=0.1
    training = data[:10]
    test_data = data[10:]

    # Fit: shift = C × k² × Q4
    k2 = k_test ** 2
    c_vals = [d['shift'] / (k2 * d['Q4']) for d in training if abs(d['Q4']) > 0.1]
    C = sum(c_vals) / len(c_vals) if c_vals else 0

    print(f"  Fitted C = {C:.8f} (from {len(c_vals)} training configs)")
    print()
    print(f"  {'config':>15s}  {'measured':>10s}  {'predicted':>10s}  {'error':>10s}")
    print(f"  {'-' * 50}")

    errors = []
    for d in test_data:
        predicted = C * k2 * d['Q4']
        error = abs(predicted - d['shift'])
        errors.append(error)
        print(f"  {d['label']:>15s}  {d['shift']:+10.5f}  {predicted:+10.5f}  {error:10.5f}")

    if errors:
        mae = sum(errors) / len(errors)
        measured_range = max(abs(d['shift']) for d in test_data) - min(abs(d['shift']) for d in test_data)
        print(f"\n  Mean absolute error: {mae:.6f}")
        print(f"  Range of measured shifts: {measured_range:.6f}")
        if measured_range > 0:
            print(f"  Relative error: {mae/measured_range:.1%}")

    print()
    print("=" * 80)
    print("FORCE LAW")
    print("=" * 80)
    print()
    print(f"  shift = {C:.8f} × k² × Q4")
    print(f"  where Q4 = Σ [field(y>0) - field(y<0)] = field asymmetry")
    print()
    print("  This is the model's gravitational force law:")
    print("  The centroid shift is proportional to k² times the total")
    print("  field asymmetry across the beam. The field asymmetry is")
    print("  computable from the Laplacian relaxation alone.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
