#!/usr/bin/env python3
"""Structured mirror growth: lattice-like placement + Z₂ + geometric edges.

The gap between grown (7.5%) and imposed S4 (27%) is caused by:
1. Grown graphs at high density → CLT dominates (random positions)
2. S4 uses structured node placement that prevents CLT

Solution: grow each layer by placing nodes on a GRID within each
y-half-plane, then connect by radius. This gives:
- Geometric locality (axiom-compliant edges)
- Structural node placement (prevents CLT at high density)
- Exact Z₂ mirror symmetry (every node has a y-flipped partner)

The growth rule is still local: each layer's grid is offset from
the previous layer's grid by a small random shift (continuation).
"""

from __future__ import annotations
import math
import cmath
import random as rng_mod
from collections import defaultdict, deque

BETA = 0.8


def grow_structured_mirror(n_layers=20, npl_half=15, d_growth=2,
                            grid_spacing=1.5, connect_radius=3.5,
                            layer_jitter=0.3, rng_seed=42):
    """Grow a Z₂-symmetric DAG with structured node placement.

    Each layer has 2*npl_half nodes: npl_half in upper half (y>0),
    npl_half mirrored in lower half (y<0).

    Within each half, nodes are placed on a grid in the transverse
    dimensions, jittered slightly from layer to layer.

    d_growth=2: grid in (y, z) → 3D graph
    d_growth=3: grid in (y, z, w) → 4D graph
    """
    rng = rng_mod.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}

    # Grid size per transverse dimension (excluding y which is split)
    # For d_growth=2: z grid has npl_half points
    # For d_growth=3: (z, w) grid has sqrt(npl_half) × sqrt(npl_half) points
    n_extra = d_growth - 1  # dimensions besides y
    if n_extra == 0:
        grid_per_dim = npl_half
    elif n_extra == 1:
        grid_per_dim = npl_half
    else:
        grid_per_dim = max(2, int(npl_half ** (1.0 / n_extra)))

    # Cumulative grid offset (random walk across layers)
    grid_offset = [0.0] * d_growth

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            pos = tuple([x] + [0.0] * d_growth)
            positions.append(pos)
            layer_nodes.append(0)
            mirror_map[0] = 0
        else:
            # Update grid offset (small random shift = continuation)
            for d in range(d_growth):
                grid_offset[d] += rng.gauss(0, layer_jitter)

            # Generate grid positions in the extra dimensions
            if n_extra == 0:
                extra_positions = [[]]
            elif n_extra == 1:
                extra_positions = [[i * grid_spacing + grid_offset[1]]
                                   for i in range(grid_per_dim)]
            else:
                extra_positions = []
                for i in range(grid_per_dim):
                    for j in range(grid_per_dim):
                        ep = [i * grid_spacing + grid_offset[1]]
                        if n_extra > 1:
                            ep.append(j * grid_spacing + grid_offset[2] if d_growth > 2 else 0.0)
                        extra_positions.append(ep)

            # For each grid position, create upper and lower (mirror) nodes
            count = 0
            for ep in extra_positions:
                if count >= npl_half:
                    break
                # Upper node: y = grid_offset[0] + some positive offset
                y_upper = abs(grid_offset[0]) + (count + 1) * grid_spacing * 0.5
                pos_upper = tuple([x, y_upper] + ep[:n_extra])
                idx_upper = len(positions)
                positions.append(pos_upper)
                layer_nodes.append(idx_upper)

                # Mirror node: y flipped
                pos_lower = tuple([x, -y_upper] + ep[:n_extra])
                idx_lower = len(positions)
                positions.append(pos_lower)
                layer_nodes.append(idx_lower)

                mirror_map[idx_upper] = idx_lower
                mirror_map[idx_lower] = idx_upper
                count += 1

            # Connect to previous layers by radius
            prev_nodes = []
            for pl in layer_indices[max(0, layer - 2):]:
                prev_nodes.extend(pl)

            for idx in layer_nodes:
                pos_i = positions[idx]
                for prev_idx in prev_nodes:
                    pos_p = positions[prev_idx]
                    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos_i, pos_p)))
                    if dist <= connect_radius:
                        adj[prev_idx].append(idx)

            # Enforce exact mirror edges
            for idx in layer_nodes:
                if idx not in mirror_map:
                    continue
                midx = mirror_map[idx]
                for prev_idx in list(adj.keys()):
                    if idx in adj.get(prev_idx, []):
                        if prev_idx in mirror_map:
                            mprev = mirror_map[prev_idx]
                            if midx not in adj.get(mprev, []):
                                adj[mprev].append(midx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj)


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


def propagate_ln(positions, adj, field, src, k, damping=None):
    n = len(positions)
    damping = damping or [1.0] * n
    by_layer = defaultdict(list)
    for idx in range(n):
        by_layer[round(positions[idx][0])].append(idx)
    layers = sorted(by_layer.keys())
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if abs(amps[i]) < 1e-30:
                continue
            amps[i] *= damping[i]
            if abs(amps[i]) < 1e-30:
                continue
            for j in adj.get(i, []):
                ip, jp = positions[i], positions[j]
                dsq = sum((a - b) ** 2 for a, b in zip(ip, jp))
                L = math.sqrt(dsq)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                dx = jp[0] - ip[0]
                trans = math.sqrt(dsq - dx * dx)
                theta = math.atan2(trans, max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                ea = cmath.exp(1j * k * act) * w / L
                amps[j] += amps[i] * ea
        if li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm
    return amps


def compute_field(positions, mass_nodes, strength=0.5):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mp = positions[m]
        for i in range(n):
            ip = positions[i]
            r = math.sqrt(sum((a - b) ** 2 for a, b in zip(ip, mp))) + 0.1
            field[i] += strength / r
    return field


def run_full_test(nl, npl_half, d_growth, seed):
    positions, adj = grow_structured_mirror(
        nl, npl_half, d_growth, grid_spacing=1.5,
        connect_radius=3.5 + 0.5 * d_growth, layer_jitter=0.3, rng_seed=seed)
    n = len(positions)
    flat = [0.0] * n

    by_layer = defaultdict(list)
    for idx in range(n):
        by_layer[round(positions[idx][0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    # Emergent barrier
    amps_b = propagate_ln(positions, adj, flat, src, 5.0)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    if len(bi) < 6:
        return None
    ba = sorted([(i, abs(amps_b[i]) ** 2) for i in bi], key=lambda x: -x[1])
    ns = max(2, len(ba) // 4)
    slits = set(i for i, _ in ba[:ns])
    damping = [1.0] * n
    for i in bi:
        damping[i] = 1.0 if i in slits else 0.0

    cy = sum(positions[i][1] for i in slits) / len(slits) if slits else 0
    sa = [i for i in slits if positions[i][1] > cy]
    sb = [i for i in slits if positions[i][1] <= cy]
    if not sa or not sb:
        return None

    # Emergent mass
    amps_m = propagate_ln(positions, adj, flat, src, 5.0, damping)
    mid_start = len(layers) // 2
    mid_end = min(len(layers) - 1, mid_start + 4)
    mid_upper = [i for layer in layers[mid_start:mid_end]
                 for i in by_layer[layer] if positions[i][1] > cy]
    if len(mid_upper) < 2:
        return None
    ranked = sorted([(i, abs(amps_m[i]) ** 2) for i in mid_upper], key=lambda x: -x[1])
    mass = [i for i, _ in ranked[:max(2, len(ranked) // 5)]]
    field = compute_field(positions, mass, 0.5)

    pm_vals, gd_vals = [], []
    for k in [3.0, 5.0, 7.0]:
        da = list(damping)
        db = list(damping)
        for i in sb:
            da[i] = 0.0
        for i in sa:
            db[i] = 0.0
        aa = propagate_ln(positions, adj, field, src, k, da)
        ab = propagate_ln(positions, adj, field, src, k, db)
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (aa[d1].conjugate() * aa[d2]
                                  + ab[d1].conjugate() * ab[d2])
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr > 1e-30:
            for key in rho:
                rho[key] /= tr
            pm_vals.append(sum(abs(v) ** 2 for v in rho.values()).real)
        am = propagate_ln(positions, adj, field, src, k, damping)
        af = propagate_ln(positions, adj, flat, src, k, damping)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            gd_vals.append(ym - yf)

    if not pm_vals:
        return None
    return {
        "pm": sum(pm_vals) / len(pm_vals),
        "grav": sum(gd_vals) / len(gd_vals) if gd_vals else 0.0,
        "n_nodes": n,
    }


def main():
    import time

    print("=" * 70)
    print("STRUCTURED MIRROR GROWTH")
    print("  Grid placement + Z₂ + geometric edges + layer norm")
    print("  Axiom-compliant growth with Codex-level structure")
    print("=" * 70)
    print()

    n_seeds = 16

    for npl_half, d_growth in [(15, 2), (20, 2), (30, 2), (40, 2), (15, 3)]:
        label = f"npl_half={npl_half}, d={d_growth} ({d_growth+1}D)"
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'grav':>8s}  "
              f"{'nodes':>6s}  {'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 52}")

        for nl in [25, 30, 40]:
            t0 = time.time()
            pm_all, gd_all, nn_all = [], [], []
            for seed_i in range(n_seeds):
                r = run_full_test(nl, npl_half, d_growth, seed_i * 7 + 3)
                if r:
                    pm_all.append(r["pm"])
                    gd_all.append(r["grav"])
                    nn_all.append(r["n_nodes"])
            dt = time.time() - t0
            if pm_all:
                n_ok = len(pm_all)
                apm = sum(pm_all) / n_ok
                agd = sum(gd_all) / n_ok
                ann = sum(nn_all) / n_ok
                se = (sum((g - agd) ** 2 for g in gd_all) / n_ok) ** 0.5 / math.sqrt(n_ok) if n_ok > 1 else 0
                ratio = agd / se if se > 0 else 0
                print(f"  {nl:4d}  {apm:8.4f}  {1-apm:7.4f}  {agd:+8.3f}  "
                      f"{ann:6.0f}  {n_ok:4d}  {dt:4.0f}s  ({ratio:+.1f}SE)")
            else:
                print(f"  {nl:4d}  FAIL")
            import sys
            sys.stdout.flush()
        print()

    print("Target: match Codex S4 (27% decoh, 7.2 SE gravity) on grown graphs")


if __name__ == "__main__":
    main()
