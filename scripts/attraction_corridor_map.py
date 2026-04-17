#!/usr/bin/env python3
"""Priority 2: Two-parameter corridor map for attraction.

Replace "mean_degree >= 3" with a 2D corridor:
  x-axis: mean_out_degree (connectivity)
  y-axis: field_gradient (spatial resolution)

Sweep (connect_radius, y_range) to span the parameter space.
For each point, measure attraction rate and plot the corridor.

PStack experiment: attraction-corridor-map
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag


def compute_field_on_dag(positions, adj, mass_indices, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    mass_set = set(mass_indices)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        new_field = [0.0] * n
        for i in range(n):
            if i in mass_set:
                new_field[i] = 1.0
                continue
            nbs = undirected.get(i, set())
            if nbs:
                new_field[i] = sum(field[j] for j in nbs) / len(nbs)
        field = new_field
    return field


def measure_point(n_layers, npl, y_range, radius, n_seeds=4):
    """Measure mean_degree, field_gradient, and attraction rate for one config."""
    k_band = [3.0, 5.0, 7.0]
    degrees = []
    gradients = []
    attract_count = 0
    total = 0

    for seed in range(n_seeds):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=npl,
            y_range=y_range, connect_radius=radius,
            rng_seed=seed * 17 + 3,
        )

        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 4:
            continue

        n = len(positions)
        edges = sum(len(v) for v in adj.values())
        mean_out = edges / n if n > 0 else 0
        degrees.append(mean_out)

        src = by_layer[layers[0]]
        det = by_layer[layers[-1]]
        mid = len(layers) // 2
        mid_idx = by_layer[layers[mid]]

        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)
        mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 0.5]
        if len(mass_idx) < 2:
            continue

        mass_cy = sum(positions[i][1] for i in mass_idx) / len(mass_idx)
        field = compute_field_on_dag(positions, adj, mass_idx)

        # Field gradient at detector
        above = [field[i] for i in det if positions[i][1] > center_y]
        below = [field[i] for i in det if positions[i][1] < center_y]
        if above and below:
            grad = sum(above) / len(above) - sum(below) / len(below)
            gradients.append(grad)

        # k-averaged attraction
        free_f = [0.0] * n
        k_shifts = []
        for k in k_band:
            # Propagate
            in_deg = [0] * n
            for i, nbs in adj.items():
                for j in nbs:
                    in_deg[j] += 1
            from collections import deque
            q = deque(i for i in range(n) if in_deg[i] == 0)
            order = []
            while q:
                i = q.popleft()
                order.append(i)
                for j in adj.get(i, []):
                    in_deg[j] -= 1
                    if in_deg[j] == 0:
                        q.append(j)

            for use_field in [free_f, field]:
                amps = [0.0 + 0.0j] * n
                for s in src:
                    amps[s] = 1.0 / len(src)
                for i in order:
                    if abs(amps[i]) < 1e-30:
                        continue
                    for j in adj.get(i, []):
                        x1, y1 = positions[i]
                        x2, y2 = positions[j]
                        L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                        if L < 1e-10:
                            continue
                        lf = 0.5 * (use_field[i] + use_field[j])
                        dl = L * (1 + lf)
                        ret = math.sqrt(max(dl * dl - L * L, 0))
                        act = dl - ret
                        ea = cmath.exp(1j * k * act) / (L ** 1.0)
                        amps[j] += amps[i] * ea

                probs = {d: abs(amps[d]) ** 2 for d in det}
                total_p = sum(probs.values())
                if total_p > 0:
                    cy = sum(positions[d][1] * p for d, p in probs.items()) / total_p
                else:
                    cy = 0
                if use_field is free_f:
                    free_cy = cy
                else:
                    k_shifts.append(cy - free_cy)

        if k_shifts:
            avg = sum(k_shifts) / len(k_shifts)
            total += 1
            toward = mass_cy - center_y
            if (toward > 0 and avg > 0.05):
                attract_count += 1

    mean_deg = sum(degrees) / len(degrees) if degrees else 0
    mean_grad = sum(gradients) / len(gradients) if gradients else 0
    rate = attract_count / total if total > 0 else 0
    return mean_deg, mean_grad, rate, total


def main() -> None:
    n_layers = 12
    npl = 20

    print("=" * 80)
    print("ATTRACTION CORRIDOR MAP")
    print("  2-parameter: mean_degree × field_gradient → attraction rate")
    print("=" * 80)
    print()

    # Sweep over (radius, y_range) grid
    radii = [1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    y_ranges = [3.0, 5.0, 8.0, 10.0, 15.0, 20.0, 30.0]

    print(f"  {'radius':>6s}  {'y_range':>7s}  {'deg':>5s}  {'grad':>6s}  {'attract':>7s}  {'zone':>12s}")
    print(f"  {'-' * 52}")

    data = []
    for radius in radii:
        for yr in y_ranges:
            deg, grad, rate, n = measure_point(n_layers, npl, yr, radius, n_seeds=4)
            if n == 0:
                continue

            # Classify zone
            if rate >= 0.75:
                zone = "CORRIDOR"
            elif rate >= 0.25:
                zone = "marginal"
            elif deg < 2.5:
                zone = "too sparse"
            elif grad < 0.05:
                zone = "too compact"
            else:
                zone = "mixed"

            pct = f"{int(rate * 100)}%"
            print(f"  {radius:6.1f}  {yr:7.1f}  {deg:5.1f}  {grad:+6.3f}  {pct:>7s}  {zone:>12s}")
            data.append((deg, grad, rate, zone))

    # ================================================================
    # CORRIDOR BOUNDARIES
    # ================================================================
    print()
    print("=" * 80)
    print("CORRIDOR BOUNDARIES")
    print("=" * 80)
    print()

    corridor = [d for d in data if d[2] >= 0.75]
    marginal = [d for d in data if 0.25 <= d[2] < 0.75]
    fail = [d for d in data if d[2] < 0.25]

    if corridor:
        deg_min = min(d[0] for d in corridor)
        deg_max = max(d[0] for d in corridor)
        grad_min = min(d[1] for d in corridor)
        grad_max = max(d[1] for d in corridor)
        print(f"  CORRIDOR (≥75% attract):")
        print(f"    degree: [{deg_min:.1f}, {deg_max:.1f}]")
        print(f"    gradient: [{grad_min:.3f}, {grad_max:.3f}]")
        print()

    # Simple classifier: degree >= D AND gradient >= G
    best_d = 0
    best_g = 0
    best_score = 0
    for d_thresh in [x * 0.5 for x in range(1, 20)]:
        for g_thresh in [x * 0.02 for x in range(1, 30)]:
            tp = sum(1 for d in data if d[0] >= d_thresh and d[1] >= g_thresh and d[2] >= 0.75)
            fp = sum(1 for d in data if d[0] >= d_thresh and d[1] >= g_thresh and d[2] < 0.25)
            fn = sum(1 for d in data if not (d[0] >= d_thresh and d[1] >= g_thresh) and d[2] >= 0.75)
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
            if f1 > best_score:
                best_score = f1
                best_d = d_thresh
                best_g = g_thresh

    print(f"  Best 2-parameter classifier:")
    print(f"    degree >= {best_d:.1f} AND gradient >= {best_g:.2f}")
    print(f"    F1 score: {best_score:.3f}")
    print()

    # Apply classifier
    print(f"  {'deg':>5s}  {'grad':>6s}  {'rate':>5s}  {'pred':>6s}  {'correct':>7s}")
    print(f"  {'-' * 34}")
    correct = 0
    for deg, grad, rate, zone in data:
        pred = "YES" if deg >= best_d and grad >= best_g else "no"
        actual = "YES" if rate >= 0.75 else "no"
        ok = pred == actual
        if ok:
            correct += 1
        print(f"  {deg:5.1f}  {grad:+6.3f}  {rate:5.0%}  {pred:>6s}  {'✓' if ok else '✗':>7s}")

    accuracy = correct / len(data) if data else 0
    print(f"\n  Accuracy: {accuracy:.0%} ({correct}/{len(data)})")

    # ================================================================
    # FINAL SUMMARY TABLE
    # ================================================================
    print()
    print("=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print()
    print("| propagator          | status      | gravity | interf | decoh | scaling |")
    print("|---------------------|-------------|---------|--------|-------|---------|")
    print("| 1/delay^p           | REJECT      | repel   | yes    | yes   | n/a     |")
    print("| (1+field)^p boost   | REJECT      | attract | broken | n/a   | blow-up |")
    print("| 1/L^p (bare)        | PROVISIONAL | attract | yes    | weak  | flat    |")
    print("| 1/L^p k-averaged    | BEST KEEP   | 11/12   | 12/12  | 5/12  | flat    |")
    print()
    print(f"Attraction corridor: degree >= {best_d:.1f} AND field_gradient >= {best_g:.2f}")
    print(f"  Too sparse: degree < {best_d:.1f} (insufficient paths)")
    print(f"  Too compact: gradient < {best_g:.2f} (field saturated)")
    print()
    print("Mechanism: mass field creates asymmetric action → phase gradient")
    print("→ constructive interference on mass-side → probability shifts toward mass")
    print()
    print("Open issue: shift doesn't fall off with distance (flat scaling)")
    print("→ may indicate the corrected propagator needs further refinement")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
