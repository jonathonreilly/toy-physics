#!/usr/bin/env python3
"""Symmetry spectrum diagnostic for mirror families.

This script asks a narrow question:

Does the two-slit detector response retain a genuinely two-dimensional
singular spectrum, or does it collapse toward rank-1?

We compare four matched families:
  - random 2-layer-lookback baseline
  - original mirror family
  - random chokepoint baseline
  - mirror chokepoint family

The diagnostic is the 2-column detector response matrix
    R = [psi_A(detectors), psi_B(detectors)]
after normalizing each branch response to unit norm.  Because the matrix
has only two columns, the singular values are analytic:

    s1 = sqrt(1 + |<u, v>|)
    s2 = sqrt(1 - |<u, v>|)

where u and v are the normalized detector-response vectors.

This is intentionally narrow and review-safe.  The mirror family may remain
exploratory unless the chokepoint Born check is also clean.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BETA = 0.8
K = 5.0
LAM = 10.0


def mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def _topo_order(adj, n):
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def generate_random_dag(n_layers, npl, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
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
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3


def generate_mirror_dag(n_layers, npl_half, xyz_range, connect_radius, rng_seed, p_cross=0.0):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
            mirror_map[idx] = idx
        else:
            upper_nodes = []
            lower_nodes = []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx_up = len(positions)
                positions.append((x, y, z))
                upper_nodes.append(idx_up)
                idx_lo = len(positions)
                positions.append((x, -y, z))
                lower_nodes.append(idx_lo)
                mirror_map[idx_up] = idx_lo
                mirror_map[idx_lo] = idx_up

            layer_nodes = upper_nodes + lower_nodes
            for prev_layer in layer_indices[max(0, layer - 2):]:
                for prev_idx in prev_layer:
                    px, py, pz = positions[prev_idx]
                    for curr_idx in upper_nodes:
                        cx, cy_val, cz = positions[curr_idx]
                        dist = math.sqrt((cx - px) ** 2 + (cy_val - py) ** 2 + (cz - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(curr_idx)
                            adj[mirror_map[prev_idx]].append(mirror_map[curr_idx])
                    if p_cross > 0:
                        for curr_idx in upper_nodes:
                            m_curr = mirror_map[curr_idx]
                            cx, cy_val, cz = positions[m_curr]
                            dist = math.sqrt((cx - px) ** 2 + (cy_val - py) ** 2 + (cz - pz) ** 2)
                            if dist <= connect_radius and rng.random() < p_cross:
                                adj[prev_idx].append(m_curr)
                                adj[mirror_map[prev_idx]].append(curr_idx)

        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3, mirror_map


def generate_random_chokepoint_dag(n_layers, npl_total, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for _ in range(npl_total):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                prev_layer = layer_indices[-1]
                for prev_idx in prev_layer:
                    px, py, pz = positions[prev_idx]
                    dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                    if dist <= connect_radius:
                        adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3


def generate_mirror_chokepoint_dag(n_layers, npl_half, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
            mirror_map[idx] = idx
        else:
            upper_nodes = []
            lower_nodes = []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx_up = len(positions)
                positions.append((x, y, z))
                upper_nodes.append(idx_up)
                idx_lo = len(positions)
                positions.append((x, -y, z))
                lower_nodes.append(idx_lo)
                mirror_map[idx_up] = idx_lo
                mirror_map[idx_lo] = idx_up

            layer_nodes = upper_nodes + lower_nodes
            if layer_indices:
                prev = layer_indices[-1]
                for prev_idx in prev:
                    px, py, pz = positions[prev_idx]
                    for curr_idx in upper_nodes:
                        cx, cy_val, cz = positions[curr_idx]
                        dist = math.sqrt((cx - px) ** 2 + (cy_val - py) ** 2 + (cz - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(curr_idx)
                            adj[mirror_map[prev_idx]].append(mirror_map[curr_idx])
        layer_indices.append(layer_nodes)

    return positions, dict(adj), n_layers // 3, mirror_map


def propagate_3d(positions, adj, field, src, k, blocked):
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
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
            ea = complex(math.cos(k * act), math.sin(k * act)) * w / L
            amps[j] += amps[i] * ea
    return amps


def compute_field_3d(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2 + (iz - mz) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def bin_amplitudes_3d(amps, positions, nodes):
    bins = [0j] * 8
    bw = 24.0 / 8
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(7, b))
        bins[b] += amps[m]
    return bins


def normalize(vec):
    norm2 = sum(abs(v) ** 2 for v in vec)
    if norm2 < 1e-30:
        return None, 0.0
    norm = math.sqrt(norm2)
    return [v / norm for v in vec], norm


def two_column_spectrum(a, b):
    ua, _ = normalize(a)
    ub, _ = normalize(b)
    if ua is None or ub is None:
        return None
    overlap = abs(sum(x.conjugate() * y for x, y in zip(ua, ub)))
    overlap = max(0.0, min(1.0, overlap))
    s1 = math.sqrt(1.0 + overlap)
    s2 = math.sqrt(max(0.0, 1.0 - overlap))
    eff_rank = (s1 + s2) ** 2 / max(1e-30, s1 * s1 + s2 * s2)
    return {
        "s1": s1,
        "s2": s2,
        "ratio": s2 / s1 if s1 > 1e-30 else math.nan,
        "overlap": overlap,
        "eff_rank": eff_rank,
    }


def sorkin_born_test(positions, adj, src, k, barrier_nodes, slit_a, slit_b, slit_c, det_list, field):
    all_slits = set(slit_a + slit_b + slit_c)
    other = set(barrier_nodes) - all_slits
    combos = {
        "abc": set(slit_a + slit_b + slit_c),
        "ab": set(slit_a + slit_b),
        "ac": set(slit_a + slit_c),
        "bc": set(slit_b + slit_c),
        "a": set(slit_a),
        "b": set(slit_b),
        "c": set(slit_c),
    }
    i3 = 0.0
    p_abc = 0.0
    for key, open_set in combos.items():
        blocked = other | (all_slits - open_set)
        amps = propagate_3d(positions, adj, field, src, k, blocked)
        for d in det_list:
            p = abs(amps[d]) ** 2
            if key == "abc":
                p_abc += p
                i3 += p
            elif key in ("ab", "ac", "bc"):
                i3 -= p
            else:
                i3 += p
    return abs(i3) / p_abc if p_abc > 1e-30 else math.nan


def measure_family_case(positions, adj, n_layers, k, family_kind):
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    n = len(positions)
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    upper = [i for i in bi if positions[i][1] > cy + 2]
    lower = [i for i in bi if positions[i][1] < cy - 2]
    middle = [i for i in bi if abs(positions[i][1] - cy) <= 2]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None

    blocked = set(bi) - set(sa + sb)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])

    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * n

    psi_a = propagate_3d(positions, adj, field_m, src, k, blocked | set(sb))
    psi_b = propagate_3d(positions, adj, field_m, src, k, blocked | set(sa))

    pa = {d: abs(psi_a[d]) ** 2 for d in det_list}
    pb = {d: abs(psi_b[d]) ** 2 for d in det_list}
    na_amp = sum(pa.values())
    nb_amp = sum(pb.values())
    if na_amp < 1e-30 or nb_amp < 1e-30:
        return None
    dtv = 0.5 * sum(abs(pa[d] / na_amp - pb[d] / nb_amp) for d in det_list)

    ba = bin_amplitudes_3d(psi_a, positions, mid)
    bb = bin_amplitudes_3d(psi_b, positions, mid)
    s_norm = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    na = sum(abs(a) ** 2 for a in ba)
    nb = sum(abs(b) ** 2 for b in bb)
    sn = s_norm / (na + nb) if (na + nb) > 0 else 0.0
    d_cl = math.exp(-LAM * LAM * sn)

    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                psi_a[d1].conjugate() * psi_a[d2]
                + psi_b[d1].conjugate() * psi_b[d2]
                + d_cl * psi_a[d1].conjugate() * psi_b[d2]
                + d_cl * psi_b[d1].conjugate() * psi_a[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr < 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    pur_cl = sum(abs(v) ** 2 for v in rho.values()).real

    spec = two_column_spectrum([psi_a[d] for d in det_list], [psi_b[d] for d in det_list])
    if spec is None:
        return None

    born = sorkin_born_test(
        positions,
        adj,
        src,
        k,
        bi,
        [upper[0]] if upper else [],
        [lower[0]] if lower else [],
        [middle[0]] if middle else [],
        det_list,
        field_f,
    ) if family_kind == "chokepoint" else math.nan

    return {
        "dtv": dtv,
        "pur_cl": pur_cl,
        "born": born,
        "ratio": spec["ratio"],
        "eff_rank": spec["eff_rank"],
        "overlap": spec["overlap"],
    }


def run_family(family_kind, n_layers_list, seeds, npl_half, xyz_range, connect_radius):
    rows = []
    for nl in n_layers_list:
        dtv_vals, pur_vals, born_vals, ratio_vals, eff_vals = [], [], [], [], []
        for seed in seeds:
            if family_kind == "mirror":
                pos, adj, _bl, _ = generate_mirror_dag(nl, npl_half, xyz_range, connect_radius, seed, p_cross=0.0)
            elif family_kind == "mirror_chokepoint":
                pos, adj, _bl, _ = generate_mirror_chokepoint_dag(nl, npl_half, xyz_range, connect_radius, seed)
            elif family_kind == "random_2layer":
                pos, adj, _bl = generate_random_dag(nl, 2 * npl_half, xyz_range, connect_radius, seed)
            elif family_kind == "random_chokepoint":
                pos, adj, _bl = generate_random_chokepoint_dag(nl, 2 * npl_half, xyz_range, connect_radius, seed)
            else:
                raise ValueError(f"unknown family_kind={family_kind}")
            r = measure_family_case(pos, adj, nl, K, "chokepoint" if "chokepoint" in family_kind else "mirror")
            if not r:
                continue
            dtv_vals.append(r["dtv"])
            pur_vals.append(r["pur_cl"])
            born_vals.append(r["born"])
            ratio_vals.append(r["ratio"])
            eff_vals.append(r["eff_rank"])
        rows.append(
            {
                "N": nl,
                "dtv": mean_se(dtv_vals),
                "pur": mean_se(pur_vals),
                "born": mean_se(born_vals),
                "ratio": mean_se(ratio_vals),
                "eff": mean_se(eff_vals),
                "count": len(dtv_vals),
            }
        )
    return rows


def fmt_pair(pair, signed=False):
    mean, se = pair
    if math.isnan(mean):
        return "FAIL"
    if signed:
        return f"{mean:+.3f}±{se:.3f}"
    return f"{mean:.3f}±{se:.3f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[40, 60, 80, 100])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--npl-half", type=int, default=25)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    npl_total = 2 * args.npl_half

    print("=" * 118)
    print("SYMMETRY SPECTRUM DIAGNOSTIC")
    print("  detector-response singular spectrum for mirror families vs matched random baselines")
    print(
        f"  k={K}, seeds={args.n_seeds}, mirror half={args.npl_half} (total {npl_total}), "
        f"xyz_range={args.xyz_range}, r={args.connect_radius}"
    )
    print("=" * 118)
    print()
    print(
        f"  {'N':>4s}  {'family':>18s}  {'dTV':>10s}  {'pur_cl':>10s}  {'Born':>10s}  "
        f"{'s2/s1':>8s}  {'eff_rank':>8s}  {'ok':>3s}"
    )
    print(f"  {'-' * 92}")

    families = [
        ("random-2layer", "random_2layer"),
        ("mirror-2layer", "mirror"),
        ("random-chokepoint", "random_chokepoint"),
        ("mirror-chokepoint", "mirror_chokepoint"),
    ]

    family_rows = {
        label: run_family(kind, args.n_layers, seeds, args.npl_half, args.xyz_range, args.connect_radius)
        for label, kind in families
    }

    for idx, nl in enumerate(args.n_layers):
        for label, _ in families:
            row = family_rows[label][idx]
            print(
                f"  {row['N']:4d}  {label:>18s}  {fmt_pair(row['dtv']):>10s}  "
                f"{fmt_pair(row['pur']):>10s}  {fmt_pair(row['born']):>10s}  "
                f"{fmt_pair(row['ratio']):>8s}  {fmt_pair(row['eff']):>8s}  {row['count']:3d}"
            )
        print()

    print("READOUT:")
    print("  Near-rank-2 support would show s2/s1 staying high in the mirror families")
    print("  relative to the matched random baseline, especially at larger N")
    print("  Born safety is only strict on the chokepoint family")


if __name__ == "__main__":
    main()
