#!/usr/bin/env python3
"""Backreaction cross-family transfer: does the b trend survive beyond modular?

The stability map shows 20/20 stable on modular gap=3. Now test:
  - Hierarchical leak=0.20 (nondegenerate channel structure)
  - Hierarchical leak=0.50
  - Uniform (no channels)

Use depth_weight=0.5 (pilot value, best M/b balance).

PStack experiment: backreaction-cross-family
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.edge_flux_architecture_pilot import (
    _normalize_edge_field,
    propagate_edge_field,
    _paired_seed_delta_edge,
    _mean,
    _se,
    K_BAND,
)
from scripts.source_projected_field_pilot import (
    CONNECT_RADIUS,
    FIXED_MASS_B,
    MASS_COUNT_FIXED,
    MASS_COUNTS,
    MASS_LAYER_OFFSET,
    N_LAYERS,
    NODES_PER_LAYER,
    N_SEEDS,
    TARGET_BS,
    XYZ_RANGE,
    _select_fixed_mass_nodes,
)
from scripts.source_projected_cross_family_pilot import (
    generate_3d_hierarchical_dag,
    generate_3d_modular_dag,
)
from scripts.local_continuation_backreaction_pilot import (
    CONTINUATION_ALIGN_FLOOR,
)
from scripts.backreaction_stability_map import (
    make_backreaction_fn,
    _fit_power_law,
)


DEPTH_WEIGHT = 0.5
STRENGTH = 0.08
EPS = 0.5


def gen_uniform(*, rng_seed, npl=NODES_PER_LAYER, r=CONNECT_RADIUS):
    import random
    rng = random.Random(rng_seed)
    positions = []; adj = defaultdict(list); layers = []
    for layer in range(N_LAYERS):
        x = float(layer); nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0)); nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-XYZ_RANGE, XYZ_RANGE)
                z = rng.uniform(-XYZ_RANGE, XYZ_RANGE)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r: adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def measure_family(label, gen_fn, n_seeds=16, **gen_kwargs):
    edge_fn = make_backreaction_fn(STRENGTH, EPS, DEPTH_WEIGHT)
    by_b = {b: [] for b in TARGET_BS}
    by_m = {m: [] for m in MASS_COUNTS}

    for seed in range(n_seeds):
        positions, adj, layer_indices = gen_fn(rng_seed=seed*17+3, **gen_kwargs)
        if len(layer_indices) < 7:
            continue
        by_layer = defaultdict(list)
        for idx, (x, *_) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers_sorted = sorted(by_layer)
        src = by_layer[layers_sorted[0]]
        det_list = list(by_layer[layers_sorted[-1]])
        if not det_list:
            continue
        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        grav_layer = layers_sorted[min(MASS_LAYER_OFFSET, len(layers_sorted)-1)]

        for b in TARGET_BS:
            mass = _select_fixed_mass_nodes(by_layer[grav_layer], positions, center_y+b, MASS_COUNT_FIXED)
            if not mass:
                continue
            delta = _paired_seed_delta_edge(positions, adj, src, det_list, mass, edge_fn)
            if delta is not None:
                by_b[b].append(delta)

        max_m = max(MASS_COUNTS)
        ranked = _select_fixed_mass_nodes(by_layer[grav_layer], positions, center_y+FIXED_MASS_B, max_m)
        if len(ranked) < max_m:
            continue
        for m in MASS_COUNTS:
            delta = _paired_seed_delta_edge(positions, adj, src, det_list, ranked[:m], edge_fn)
            if delta is not None:
                by_m[m].append(delta)

    b_xs = [b for b in TARGET_BS if by_b[b] and _mean(by_b[b]) > 0]
    b_ys = [_mean(by_b[b]) for b in b_xs]
    b_fit = _fit_power_law(b_xs, b_ys)
    b_alpha = b_fit[0] if b_fit else None

    m_xs = [float(m) for m in MASS_COUNTS if by_m[m] and _mean(by_m[m]) > 0]
    m_ys = [_mean(by_m[m]) for m in MASS_COUNTS if by_m[m] and _mean(by_m[m]) > 0]
    m_fit = _fit_power_law(m_xs, m_ys)
    m_alpha = m_fit[0] if m_fit else None

    max_t = 0
    for b in TARGET_BS:
        vals = by_b[b]
        if vals:
            avg = _mean(vals); se = _se(vals)
            if se and math.isfinite(se) and se > 1e-12:
                max_t = max(max_t, abs(avg/se))

    return b_alpha, m_alpha, max_t


def main():
    print("=" * 70)
    print("BACKREACTION CROSS-FAMILY TRANSFER")
    print(f"  depth_weight={DEPTH_WEIGHT}, strength={STRENGTH}, eps={EPS}")
    print("=" * 70)
    print()

    families = [
        ("Modular gap=3", generate_3d_modular_dag, {"gap": 3.0}),
        ("Hierarchical leak=0.20", generate_3d_hierarchical_dag, {"gap": 3.0, "channel_leak": 0.20}),
        ("Hierarchical leak=0.50", generate_3d_hierarchical_dag, {"gap": 3.0, "channel_leak": 0.50}),
        ("Uniform", gen_uniform, {}),
    ]

    print(f"  {'family':>30s}  {'b_alpha':>8s}  {'M_alpha':>8s}  {'max_t':>6s}  verdict")
    print(f"  {'-'*65}")

    for name, gen_fn, kwargs in families:
        b_a, m_a, mt = measure_family(name, gen_fn, n_seeds=16, **kwargs)
        if b_a is not None and m_a is not None:
            good = b_a < -0.1 and m_a > 0.1
            v = "TRANSFERS" if good else "partial" if (b_a < -0.1 or m_a > 0.1) else "fails"
            print(f"  {name:>30s}  {b_a:+8.3f}  {m_a:+8.3f}  {mt:6.2f}  {v}")
        else:
            b_s = f"{b_a:+8.3f}" if b_a is not None else "FAIL"
            m_s = f"{m_a:+8.3f}" if m_a is not None else "FAIL"
            print(f"  {name:>30s}  {b_s:>8s}  {m_s:>8s}  {mt:6.2f}")

    print()
    print("=" * 70)
    print("KEY: TRANSFERS = b<-0.1 AND M>0.1 on the new family")
    print("=" * 70)


if __name__ == "__main__":
    main()
