#!/usr/bin/env python3
"""Born rule check on LN+|y| combined propagator.

The LN+|y| combination gives N_half=85k — but does it preserve Born?
Layer norm is a nonlinear operation (amplitude-dependent rescaling).
The other thread found LN preserves Born at machine precision on 2D,
but we need to verify on 3D with |y|-removal.

Test: three-slit Sorkin identity |I_3|/P on LN+|y| graphs.
  I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C
  Born-compliant: |I_3|/P = 0 (machine precision)
  Born-violated: |I_3|/P >> 0

Also: compare linear vs LN vs LN+|y| Born compliance.

Note: Sorkin test on random DAGs gives I_3/P ~ O(1) without
chokepoint barriers (known from the other thread). So we test on
graphs where the barrier IS a chokepoint (no skip-layer edges
bypassing barrier). Use layer-2 connectivity only (no layer-to-layer+2).
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
XYZ_RANGE = 12.0
CONNECT_RADIUS = 4.0
NPL = 50
N_SEEDS = 16
K_BAND = [3.0, 5.0, 7.0]


def generate_3d_dag_chokepoint(n_layers, npl, xyz_range, connect_radius, rng_seed):
    """Generate 3D DAG with strict chokepoint barrier (no skip-layer edges across barrier)."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for _ in range(npl):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                # Connect to previous layer only (not layer-2)
                # This ensures barrier is a true chokepoint
                if layer_indices:
                    prev = layer_indices[-1]
                    for prev_idx in prev:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)
    return positions, dict(adj), barrier_layer


def propagate_3d_variant(positions, adj, field, src, k, blocked, use_ln=False):
    """Propagate with optional layer normalization."""
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if abs(amps[i]) < 1e-30 or i in blocked:
                continue
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1, z1 = positions[i]
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                ea = cmath.exp(1j * k * act) * w / L
                amps[j] += amps[i] * ea

        if use_ln and li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm

    return amps


def apply_y_removal(positions, adj, barrier_layer, y_thresh, protected):
    removed = set()
    for idx, (x, y, z) in enumerate(positions):
        if x <= barrier_layer or idx in protected:
            continue
        if abs(y) < y_thresh:
            removed.add(idx)
    new_adj = {}
    for i, nbs in adj.items():
        if i in removed:
            continue
        new_nbs = [j for j in nbs if j not in removed]
        if new_nbs:
            new_adj[i] = new_nbs
    return new_adj, removed


def sorkin_test(positions, adj, src, k, barrier_nodes, slit_a, slit_b, slit_c,
                det_list, use_ln, field):
    """Three-slit Sorkin test. Returns |I_3|/P."""
    all_slits = set(slit_a + slit_b + slit_c)
    other_barrier = set(barrier_nodes) - all_slits

    def prop(open_set):
        bl = other_barrier | (all_slits - open_set)
        return propagate_3d_variant(positions, adj, field, src, k, bl, use_ln)

    a_abc = prop(set(slit_a + slit_b + slit_c))
    a_ab = prop(set(slit_a + slit_b))
    a_ac = prop(set(slit_a + slit_c))
    a_bc = prop(set(slit_b + slit_c))
    a_a = prop(set(slit_a))
    a_b = prop(set(slit_b))
    a_c = prop(set(slit_c))

    I3 = 0.0
    P_abc = 0.0
    for d in det_list:
        p_abc = abs(a_abc[d]) ** 2
        p_ab = abs(a_ab[d]) ** 2
        p_ac = abs(a_ac[d]) ** 2
        p_bc = abs(a_bc[d]) ** 2
        p_a = abs(a_a[d]) ** 2
        p_b = abs(a_b[d]) ** 2
        p_c = abs(a_c[d]) ** 2
        I3 += abs(p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c)
        P_abc += p_abc

    return I3 / P_abc if P_abc > 1e-30 else math.nan


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 90)
    print("BORN RULE CHECK: LN + |y|-REMOVAL ON CHOKEPOINT 3D DAGs")
    print(f"  NPL={NPL}, {N_SEEDS} seeds, chokepoint barrier (layer-1 only)")
    print("=" * 90)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("linear", False, False),
        ("linear+|y|", False, True),
        ("LN", True, False),
        ("LN+|y|", True, True),
    ]

    for nl in [15, 25, 40]:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'mode':>12s}  {'|I3|/P':>12s}  {'max':>10s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 50}")

        for label, use_ln, use_yrem in configs:
            t0 = time.time()
            i3p_all = []

            for seed in seeds:
                pos, adj, bl = generate_3d_dag_chokepoint(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)

                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(pos):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7:
                    continue

                src = by_layer[layers[0]]
                det_list = list(by_layer[layers[-1]])
                if not det_list:
                    continue

                cy = sum(pos[i][1] for i in range(n)) / n
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]

                # Find three well-separated slits
                upper = sorted([i for i in bi if pos[i][1] > cy + 2], key=lambda i: pos[i][1])
                lower = sorted([i for i in bi if pos[i][1] < cy - 2], key=lambda i: -pos[i][1])
                middle = sorted([i for i in bi if abs(pos[i][1] - cy) <= 2],
                                key=lambda i: abs(pos[i][1] - cy))

                if not upper or not lower or not middle:
                    continue

                slit_a = [upper[0]]
                slit_b = [lower[0]]
                slit_c = [middle[0]]

                protected = set(src) | set(det_list) | set(slit_a + slit_b + slit_c)

                if use_yrem:
                    adj, _ = apply_y_removal(pos, adj, bl, 2.0, protected)

                field = [0.0] * n  # flat field for Born test

                for k in K_BAND:
                    val = sorkin_test(pos, adj, src, k, bi, slit_a, slit_b, slit_c,
                                     det_list, use_ln, field)
                    if not math.isnan(val):
                        i3p_all.append(val)

            dt = time.time() - t0
            if i3p_all:
                mi, sei = _mean_se(i3p_all)
                mx = max(i3p_all)
                status = "PASS" if mx < 0.01 else ("MARGINAL" if mx < 0.1 else "FAIL")
                print(f"  {label:>12s}  {mi:12.2e}±{sei:.1e}  {mx:10.2e}  {len(i3p_all):3d}  {dt:4.0f}s  {status}")
            else:
                print(f"  {label:>12s}  NO DATA  {dt:4.0f}s")

        print()

    print("BORN COMPLIANCE:")
    print("  |I3|/P < 1e-10: machine precision (PASS)")
    print("  |I3|/P < 0.01: Born-compliant (PASS)")
    print("  |I3|/P < 0.1: marginal")
    print("  |I3|/P >= 0.1: Born violated (FAIL)")
    print()
    print("NOTE: chokepoint barrier (layer-1 only connectivity) ensures")
    print("all paths pass through the barrier. Without this, I3/P~1 on")
    print("random DAGs due to bypass paths, not Born violation.")


if __name__ == "__main__":
    main()
