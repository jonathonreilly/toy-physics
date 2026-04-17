#!/usr/bin/env python3
"""No-barrier lattice distance-law check on the ordered 2D lattice.

This is the canonical follow-up to the sign-changing barrier-lattice probe.
It uses the same regular lattice transport, but removes the barrier entirely
and launches an unfocused beam from the source at y=0. The quantity of
interest is the detector-centroid shift induced by a mass row at y=b.

The retained question is narrow:
  does the ordered lattice keep a clean magnitude falloff in |delta| vs b,
  and does the k=0 control stay exactly zero?
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.lattice_mirror_distance import compute_field_at_b, generate_lattice_mirror, propagate

K = 5.0
B_VALUES = [3, 5, 7, 10, 13, 16, 19]


def centroid_y(amps, positions, det_list):
    total = 0.0
    weighted = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * positions[d][1]
    return weighted / total if total > 1e-30 else math.nan


def fit_power_law(points):
    usable = [(b, v) for b, v in points if b > 0 and v > 0 and not math.isnan(v)]
    if len(usable) < 3:
        return None
    xs = [math.log(b) for b, _ in usable]
    ys = [math.log(v) for _, v in usable]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 1e-12 or syy <= 1e-12:
        return None
    alpha = sxy / sxx
    coeff = math.exp(my - alpha * mx)
    r2 = (sxy * sxy) / (sxx * syy)
    return coeff, alpha, r2


def main():
    n_layers = 40
    half_width = 20
    positions, adj, _, node_map = generate_lattice_mirror(n_layers, half_width, 42)
    layers = sorted({round(p[0]) for p in positions})
    src = [node_map[(layers[0], 0)]]
    det_list = [
        node_map[(layers[-1], y)]
        for y in range(-half_width, half_width + 1)
        if (layers[-1], y) in node_map
    ]
    grav_layer = layers[2 * len(layers) // 3]
    field_zero = [0.0] * len(positions)
    blocked = set()

    print("=" * 78)
    print("NO-BARRIER LATTICE DISTANCE LAW")
    print("  ordered 2D lattice, source at y=0, no barrier, mass row at y=b")
    print(f"  N={n_layers}, half_width={half_width}, k={K}")
    print("=" * 78)
    print()

    rows = []
    for b in B_VALUES:
        field_m, _ = compute_field_at_b(positions, node_map, grav_layer, b, n_mass=1)
        am = propagate(positions, adj, field_m, src, K, blocked)
        af = propagate(positions, adj, field_zero, src, K, blocked)
        delta = centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list)
        rows.append((b, delta))

    print(f"{'b':>4s}  {'delta':>10s}  {'|delta|':>10s}")
    print("-" * 30)
    for b, delta in rows:
        print(f"{b:4d}  {delta:+10.4f}  {abs(delta):10.4f}")

    print()
    k0_field, _ = compute_field_at_b(positions, node_map, grav_layer, 7, n_mass=1)
    am0 = propagate(positions, adj, k0_field, src, 0.0, blocked)
    af0 = propagate(positions, adj, field_zero, src, 0.0, blocked)
    delta0 = centroid_y(am0, positions, det_list) - centroid_y(af0, positions, det_list)
    print(f"k=0 control: {delta0:+.6e}")
    print()

    tail = [(b, abs(delta)) for b, delta in rows if b >= 7]
    fit = fit_power_law(tail)
    if fit:
        coeff, alpha, r2 = fit
        print("Far-field |delta| fit on b >= 7:")
        print(f"  |delta| ~= {coeff:.4f} * b^({alpha:.3f})")
        print(f"  R^2 = {r2:.4f}")
    else:
        print("Far-field fit unavailable")


if __name__ == "__main__":
    main()
