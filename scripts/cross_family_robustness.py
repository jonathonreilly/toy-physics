#!/usr/bin/env python3
"""Cross-family robustness: do gravity + decoherence survive beyond modular DAGs?

Gate E: "reduce the sense that the architecture only works on one family."
All current claims use modular gap-controlled DAGs. This tests three
structurally distinct 3D families:

  1. MODULAR (baseline): two y-channels with gap, sparse crosslinks
  2. HIERARCHICAL: upper/lower channel with leak parameter, no hard gap
  3. PREFERENTIAL: hub-based connectivity, no explicit channels

If gravity + decoherence work on 2+ families: robust architectural feature.
If only modular: family-specific artifact.

Uses FIXED mass geometry across b (lesson from causal field confound).

PStack experiment: cross-family-robustness
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8
LAM = 10.0
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 16


# ─── 3D Family generators ───

def generate_3d_modular(n_layers=20, npl=30, yz_range=10.0, r=3.5,
                        rng_seed=42, gap=3.0, xlink=0.02):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layers = []
    bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            nodes.append(len(positions)-1)
        else:
            for ni in range(npl):
                z = rng.uniform(-yz_range, yz_range)
                if gap > 0 and layer > bl:
                    y = rng.uniform(gap/2, yz_range) if ni < npl//2 else rng.uniform(-yz_range, -gap/2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if gap > 0 and layer > bl and round(positions[pi][0]) > bl:
                            if positions[idx][1]*positions[pi][1] > 0 and d <= r:
                                adj[pi].append(idx)
                            elif d <= 2*r and rng.random() < xlink:
                                adj[pi].append(idx)
                        elif d <= r:
                            adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def generate_3d_hierarchical(n_layers=20, npl=30, yz_range=10.0, r=3.5,
                              rng_seed=42, leak=0.05):
    """Hierarchical: post-barrier, same-sign y gets full radius, cross-sign gets r*leak."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layers = []
    bl = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if layer > bl and round(positions[pi][0]) > bl:
                            same = positions[idx][1]*positions[pi][1] > 0
                            threshold = r if same else r*leak
                        else:
                            threshold = r
                        if d <= threshold:
                            adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def generate_3d_preferential(n_layers=20, npl=30, yz_range=10.0, r=3.5,
                              rng_seed=42, hub_boost=3.0):
    """Preferential attachment: high-degree parents attract more connections."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    out_deg = defaultdict(int)
    layers = []
    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                candidates = []
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r:
                            w = 1.0 + hub_boost * out_deg[pi]
                            candidates.append((pi, w))
                if candidates:
                    max_w = max(c[1] for c in candidates)
                    for pi, w in candidates:
                        if rng.random() < w / max_w:
                            adj[pi].append(idx)
                            out_deg[pi] += 1
        layers.append(nodes)
    return positions, dict(adj), layers


def generate_3d_uniform(n_layers=20, npl=30, yz_range=10.0, r=3.5, rng_seed=42):
    """Uniform random (no channels, no hubs)."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layers = []
    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r:
                            adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


# ─── Physics ───

def compute_field(positions, adj, mass_ids, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_ids)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0] * n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def propagate(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
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
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        pi = positions[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pj = positions[j]
            dx = pj[0] - pi[0]
            L = math.sqrt(sum((a-b)**2 for a, b in zip(pi, pj)))
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx/L, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d])**2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0
    y_min, y_max = min(ys)-0.01, max(ys)+0.01
    bw = (y_max - y_min) / N_YBINS
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid_nodes:
        b = max(0, min(N_YBINS-1, int((positions[m][1] - y_min) / bw)))
        ba[b] += amps_a[m]
        bb[b] += amps_b[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    d = sum(abs(a)**2 for a in ba) + sum(abs(b)**2 for b in bb)
    return S / d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (amps_a[d1]*amps_a[d2].conjugate() +
                             amps_b[d1]*amps_b[d2].conjugate() +
                             D * amps_a[d1]*amps_b[d2].conjugate() +
                             D * amps_b[d1]*amps_a[d2].conjugate())
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def test_family(name, gen_fn, n_layers_list, **gen_kwargs):
    """Test gravity + decoherence on a graph family."""
    print(f"  [{name}]")
    print(f"  {'N':>4s}  {'grav_d':>8s}  {'grav_t':>7s}  {'pur_cl':>8s}  "
          f"{'decoh':>8s}  {'n':>3s}")
    print(f"  {'-'*46}")

    for nl in n_layers_list:
        grav_seeds = []
        pur_list = []

        for seed in range(N_SEEDS):
            positions, adj, layer_indices = gen_fn(
                n_layers=nl, npl=30, yz_range=10.0, r=3.5,
                rng_seed=seed*13+5, **gen_kwargs)

            n = len(positions)
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list or len(layer_indices) < 7:
                continue

            all_ys = [positions[i][1] for i in range(n)]
            cy = sum(all_ys) / len(all_ys)
            bl_idx = len(layer_indices) // 3

            # Gravity
            grav_idx = 2 * len(layer_indices) // 3
            mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1][:8]
            if mass:
                field = compute_field(positions, adj, mass)
                free_f = [0.0] * n
                deltas = []
                for k in K_BAND:
                    am = propagate(positions, adj, field, src, k)
                    af = propagate(positions, adj, free_f, src, k)
                    deltas.append(centroid_y(am, positions, det_list) -
                                  centroid_y(af, positions, det_list))
                if deltas:
                    grav_seeds.append(sum(deltas)/len(deltas))

            # Decoherence
            barrier = layer_indices[bl_idx]
            slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
            slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
            if not slit_a or not slit_b:
                continue
            blocked = set(barrier) - set(slit_a + slit_b)
            blocked_a = blocked | set(slit_b)
            blocked_b = blocked | set(slit_a)

            bath_mass = []
            for li in range(bl_idx+1, min(len(layer_indices), bl_idx+3)):
                for i in layer_indices[li]:
                    if abs(positions[i][1] - cy) <= 3:
                        bath_mass.append(i)
            grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1]
            all_mass = list(set(bath_mass) | set(grav_mass))
            field_d = compute_field(positions, adj, all_mass) if all_mass else [0.0]*n

            mid_nodes = [i for li in range(bl_idx+1, len(layer_indices)-1)
                         for i in layer_indices[li]
                         if i not in blocked and i not in set(det_list)]
            if len(mid_nodes) < 4:
                continue

            for k in K_BAND:
                aa = propagate(positions, adj, field_d, src, k, blocked_a)
                ab = propagate(positions, adj, field_d, src, k, blocked_b)
                Sn = cl_contrast(aa, ab, mid_nodes, positions)
                D = math.exp(-LAM**2 * Sn)
                pur = cl_purity(aa, ab, D, det_list)
                if not math.isnan(pur):
                    pur_list.append(pur)

        if grav_seeds and pur_list:
            ng = len(grav_seeds)
            gd = sum(grav_seeds) / ng
            gse = (sum((d-gd)**2 for d in grav_seeds) / ng)**0.5 / ng**0.5
            gt = gd / gse if gse > 1e-10 else 0
            mp = sum(pur_list) / len(pur_list)
            gv = "GRAV" if gd > 0 and gt > 2 else "weak" if gd > 0 else "flat"
            dv = "DECOH" if mp < 0.97 else "weak"
            print(f"  {nl:4d}  {gd:+8.4f}  {gt:+7.2f}  {mp:8.4f}  "
                  f"{1-mp:+8.4f}  {ng:3d}  {gv} {dv}")
        else:
            print(f"  {nl:4d}  FAIL")

    print()


def main():
    print("=" * 74)
    print("CROSS-FAMILY ROBUSTNESS: Gate E")
    print("  Do gravity + decoherence work beyond modular DAGs?")
    print("=" * 74)
    print()

    n_layers = [15, 20, 25, 30]

    families = [
        ("3D Modular gap=3 (baseline)", generate_3d_modular, {"gap": 3.0}),
        ("3D Hierarchical leak=0.05", generate_3d_hierarchical, {"leak": 0.05}),
        ("3D Hierarchical leak=0.10", generate_3d_hierarchical, {"leak": 0.10}),
        ("3D Preferential hub=3", generate_3d_preferential, {"hub_boost": 3.0}),
        ("3D Uniform (no structure)", generate_3d_uniform, {}),
    ]

    for name, gen_fn, kwargs in families:
        test_family(name, gen_fn, n_layers, **kwargs)

    print("=" * 74)
    print("INTERPRETATION:")
    print("  GRAV + DECOH on 2+ families: robust architectural feature")
    print("  Only modular: family-specific artifact")
    print("  Hierarchical better than uniform: channel structure helps")
    print("=" * 74)


if __name__ == "__main__":
    main()
