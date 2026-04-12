#!/usr/bin/env python3
"""Local continuation backreaction stability map.

The pilot gave b alpha=-0.430, M alpha=0.525 at the default parameters.
This sweep checks whether that point is stable or a one-off.

Sweep:
  - CONTINUATION_DEPTH_WEIGHT in (0.1, 0.3, 0.5, 0.7, 1.0)
  - GREEN_STRENGTH in (0.04, 0.08, 0.12, 0.20)
  - GREEN_EPS fixed at 0.5 (not swept)

For each combo: measure b alpha and M alpha on 16 seeds.
A stable region means b alpha stays negative and M alpha stays positive
across a range of parameters.

PStack experiment: backreaction-stability-map
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict
from functools import partial

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.edge_flux_architecture_pilot import (
    _normalize_edge_field,
    propagate_edge_field,
    _paired_seed_delta_edge,
    _mean,
    _se,
    BETA,
    K_BAND,
)


def _fit_power_law(xs_in, ys_in):
    pairs = [(x, y) for x, y in zip(xs_in, ys_in) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(x) for x, _ in pairs]
    ys = [math.log(y) for _, y in pairs]
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxy = sum(x*y for x, y in zip(xs, ys))
    sxx = sum(x*x for x in xs)
    denom = n*sxx - sx*sx
    if abs(denom) < 1e-12:
        return None
    slope = (n*sxy - sx*sy) / denom
    intercept = (sy - slope*sx) / n
    ss_tot = sum((y - sy/n)**2 for y in ys)
    ss_res = sum((y - (slope*x + intercept))**2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return slope, math.exp(intercept), r2
from scripts.source_projected_field_pilot import (
    CONNECT_RADIUS,
    FIXED_MASS_B,
    GAP,
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
from scripts.source_resolved_green_pilot import (
    generate_3d_modular_dag,
)
from scripts.local_continuation_backreaction_pilot import (
    _local_continuation_signature,
    CONTINUATION_ALIGN_FLOOR,
)


def make_backreaction_fn(strength, eps, depth_weight):
    """Create a backreaction edge field function with given parameters."""

    def edge_field_fn(positions, adj, mass_nodes):
        sx, sy, sz = positions[0]
        edge_field = {}
        # Cache signatures with custom depth_weight
        sigs = {}
        for j in range(len(positions)):
            outs = adj.get(j, [])
            if not outs:
                sigs[j] = (1.0, (0.0, 0.0, 0.0), 0.0)
                continue
            x0, y0, z0 = positions[j]
            vectors = []
            two_hop = 0.0
            for ch in outs:
                two_hop += len(adj.get(ch, []))
                dx = positions[ch][0] - x0
                dy = positions[ch][1] - y0
                dz = positions[ch][2] - z0
                L = math.sqrt(dx*dx + dy*dy + dz*dz)
                if L > 1e-12:
                    vectors.append((dx/L, dy/L, dz/L))
            if vectors:
                mx_ = sum(v[0] for v in vectors)/len(vectors)
                my_ = sum(v[1] for v in vectors)/len(vectors)
                mz_ = sum(v[2] for v in vectors)/len(vectors)
                coherence = math.sqrt(mx_*mx_ + my_*my_ + mz_*mz_)
                mean_dir = (mx_/coherence, my_/coherence, mz_/coherence) if coherence > 1e-12 else (0,0,0)
            else:
                coherence = 0.0
                mean_dir = (0,0,0)
            capacity = 1.0 + len(outs) + depth_weight * two_hop
            sigs[j] = (capacity, mean_dir, coherence)

        for i, outs in adj.items():
            x1, y1, z1 = positions[i]
            for j in outs:
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2-x1, y2-y1, z2-z1
                L = math.sqrt(dx*dx + dy*dy + dz*dz)
                if L < 1e-12:
                    continue
                ex, ey, ez = dx/L, dy/L, dz/L
                mid_x, mid_y, mid_z = 0.5*(x1+x2), 0.5*(y1+y2), 0.5*(z1+z2)
                cap, cont_dir, coherence = sigs[j]
                if cap <= 1e-12 or coherence <= 1e-12:
                    continue
                continuity_align = max(0.0, ex*cont_dir[0] + ey*cont_dir[1] + ez*cont_dir[2])
                if continuity_align <= 0.0:
                    continue
                v_x, v_y, v_z = mid_x-sx, mid_y-sy, mid_z-sz
                v_norm = math.sqrt(v_x*v_x + v_y*v_y + v_z*v_z)
                if v_norm < 1e-12:
                    continue
                response = 0.0
                for m in mass_nodes:
                    mx, my, mz = positions[m]
                    u_x, u_y, u_z = mx-sx, my-sy, mz-sz
                    u_norm = math.sqrt(u_x*u_x + u_y*u_y + u_z*u_z)
                    if u_norm < 1e-12:
                        continue
                    source_align = (u_x*v_x + u_y*v_y + u_z*v_z) / (u_norm*v_norm)
                    if source_align <= 0:
                        continue
                    r = math.sqrt((mid_x-mx)**2 + (mid_y-my)**2 + (mid_z-mz)**2)
                    if r < 1e-12:
                        continue
                    response += (
                        strength * source_align * continuity_align
                        * max(coherence, CONTINUATION_ALIGN_FLOOR)
                        / (cap * (r + eps))
                    )
                edge_field[(i, j)] = response
        return _normalize_edge_field(edge_field)

    return edge_field_fn


def quick_measure(edge_field_fn, n_seeds=16):
    """Measure b alpha and M alpha for a given backreaction function."""
    by_b = {b: [] for b in TARGET_BS}
    by_m = {m: [] for m in MASS_COUNTS}

    for seed in range(n_seeds):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS, nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE, connect_radius=CONNECT_RADIUS,
            rng_seed=seed*17+3, gap=GAP)
        if len(layer_indices) < 7:
            continue
        by_layer = defaultdict(list)
        for idx, (x, *_) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer)
        src = by_layer[layers[0]]
        det_list = list(by_layer[layers[-1]])
        if not det_list:
            continue
        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        grav_layer = layers[MASS_LAYER_OFFSET] if MASS_LAYER_OFFSET < len(layers) else layers[len(layers)//2]

        # b-sweep (fixed mass count)
        for b in TARGET_BS:
            mass = _select_fixed_mass_nodes(by_layer[grav_layer], positions, center_y+b, MASS_COUNT_FIXED)
            if not mass:
                continue
            delta = _paired_seed_delta_edge(positions, adj, src, det_list, mass, edge_field_fn)
            if delta is not None:
                by_b[b].append(delta)

        # M-sweep (fixed b)
        max_m = max(MASS_COUNTS)
        ranked = _select_fixed_mass_nodes(by_layer[grav_layer], positions, center_y+FIXED_MASS_B, max_m)
        if len(ranked) < max_m:
            continue
        for m in MASS_COUNTS:
            subset = ranked[:m]
            delta = _paired_seed_delta_edge(positions, adj, src, det_list, subset, edge_field_fn)
            if delta is not None:
                by_m[m].append(delta)

    # Fit b alpha
    b_xs = [b for b in TARGET_BS if by_b[b] and _mean(by_b[b]) > 0]
    b_ys = [_mean(by_b[b]) for b in b_xs]
    b_fit = _fit_power_law(b_xs, b_ys) if len(b_xs) >= 3 else None
    b_alpha = b_fit[0] if b_fit else None

    # Fit M alpha
    m_xs = [float(m) for m in MASS_COUNTS if by_m[m] and _mean(by_m[m]) > 0]
    m_ys = [_mean(by_m[m]) for m in MASS_COUNTS if by_m[m] and _mean(by_m[m]) > 0]
    m_fit = _fit_power_law(m_xs, m_ys) if len(m_xs) >= 3 else None
    m_alpha = m_fit[0] if m_fit else None

    # Max t across b points
    max_t = 0
    for b in TARGET_BS:
        vals = by_b[b]
        if vals:
            avg = _mean(vals)
            se = _se(vals)
            if se and math.isfinite(se) and se > 1e-12:
                max_t = max(max_t, abs(avg/se))

    return b_alpha, m_alpha, max_t


def main():
    print("=" * 74)
    print("BACKREACTION STABILITY MAP")
    print("  Sweep continuation_depth_weight × green_strength")
    print("  16 seeds per point, retained 3D modular gap=3")
    print("=" * 74)
    print()

    depth_weights = [0.1, 0.3, 0.5, 0.7, 1.0]
    strengths = [0.04, 0.08, 0.12, 0.20]
    eps = 0.5

    print(f"  {'dw':>4s}  {'str':>5s}  {'b_alpha':>8s}  {'M_alpha':>8s}  {'max_t':>6s}  verdict")
    print(f"  {'-'*48}")

    stable_count = 0
    for dw in depth_weights:
        for st in strengths:
            fn = make_backreaction_fn(st, eps, dw)
            b_a, m_a, mt = quick_measure(fn, n_seeds=16)

            if b_a is not None and m_a is not None:
                good_b = b_a < -0.1
                good_m = m_a > 0.1
                if good_b and good_m:
                    v = "STABLE"
                    stable_count += 1
                elif good_b:
                    v = "b only"
                elif good_m:
                    v = "M only"
                else:
                    v = "fail"
                print(f"  {dw:4.1f}  {st:5.2f}  {b_a:+8.3f}  {m_a:+8.3f}  {mt:6.2f}  {v}")
            else:
                print(f"  {dw:4.1f}  {st:5.2f}  {'FAIL':>8s}  {'FAIL':>8s}  {mt:6.2f}")

    print()
    print(f"  Stable points (b<-0.1 AND M>0.1): {stable_count}/{len(depth_weights)*len(strengths)}")
    print()
    print("=" * 74)
    print("KEY: if stable_count > 5: the backreaction is a robust regime")
    print("     if stable_count <= 2: it's a narrow parameter corner")
    print("=" * 74)


if __name__ == "__main__":
    main()
