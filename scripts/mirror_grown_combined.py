#!/usr/bin/env python3
"""Mirror symmetry on grown geometric DAGs.

Codex found: Z₂ mirror on imposed 3D graphs gives 27% decoherence
+ 7.2 SE gravity (S4 mirror architecture).

Our finding: grown 4D graphs close the axiom chain with 7.5%
decoherence + 2.5 SE gravity.

Can we get the best of both? Grow a geometric DAG with Z₂ mirror
symmetry in the y-coordinate:
  - For each node at (x, y, z1, ..., zd), also create its mirror
    at (x, -y, z1, ..., zd) with mirrored edges.
  - This is axiom-compatible: "the growth rule respects a symmetry"
    is a weaker assumption than "the geometry is imposed."

Tests d_growth=2 (3D with mirror, like Codex's best) and d_growth=3
(4D with mirror).
"""

from __future__ import annotations
import math
import cmath
import random as rng_mod
from collections import defaultdict, deque

BETA = 0.8


def grow_mirror_dag(n_layers=20, npl=25, d_growth=2,
                     connect_radius=3.5, spread=1.2, rng_seed=42):
    """Grow geometric DAG with Z₂ y-mirror symmetry.

    For each new node at position (x, y, z...), also create its
    mirror at (x, -y, z...). Edges respect the mirror: if i→j
    exists, mirror(i)→mirror(j) also exists.
    """
    rng = rng_mod.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}  # node → its mirror

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            # Source at origin (its own mirror)
            positions.append(tuple([x] + [0.0] * d_growth))
            layer_nodes.append(0)
            mirror_map[0] = 0
        else:
            prev = []
            for pl in layer_indices[max(0, layer - 2):]:
                prev.extend(pl)

            # Create npl//2 nodes, each with a mirror
            for _ in range(npl // 2):
                parent_idx = rng.choice(prev)
                pp = positions[parent_idx]

                # New position: parent + offset
                y_offset = rng.gauss(0, spread)
                extra = [rng.gauss(0, spread) for _ in range(d_growth - 1)]

                # Original node
                pos_orig = tuple([x, pp[1] + y_offset] + [pp[2 + d] + extra[d] for d in range(d_growth - 1)])
                idx_orig = len(positions)
                positions.append(pos_orig)
                layer_nodes.append(idx_orig)

                # Mirror node (flip y)
                pos_mirror = tuple([x, -(pp[1] + y_offset)] + [pp[2 + d] + extra[d] for d in range(d_growth - 1)])
                idx_mirror = len(positions)
                positions.append(pos_mirror)
                layer_nodes.append(idx_mirror)

                mirror_map[idx_orig] = idx_mirror
                mirror_map[idx_mirror] = idx_orig

                # Connect both to nearby prev nodes
                for prev_idx in prev:
                    ppos = positions[prev_idx]
                    # Original
                    dist_o = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos_orig, ppos)))
                    if dist_o <= connect_radius:
                        adj[prev_idx].append(idx_orig)
                        # Mirror edge
                        if prev_idx in mirror_map:
                            adj[mirror_map[prev_idx]].append(idx_mirror)
                    # Mirror
                    dist_m = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos_mirror, ppos)))
                    if dist_m <= connect_radius:
                        adj[prev_idx].append(idx_mirror)
                        if prev_idx in mirror_map:
                            adj[mirror_map[prev_idx]].append(idx_orig)

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


def run_mirror_test(nl, d_growth, seed):
    positions, adj = grow_mirror_dag(nl, 30, d_growth, 3.5, 1.2, seed)
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
    }


def main():
    import time

    print("=" * 70)
    print("MIRROR + GROWN: Z₂ symmetry on geometric DAGs")
    print("  Combining Codex's mirror insight with our grown-graph axiom chain")
    print("=" * 70)
    print()

    n_seeds = 16

    for d_growth in [2, 3]:
        print(f"  [d_growth={d_growth} ({d_growth+1}D), Z₂ y-mirror]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'grav':>8s}  "
              f"{'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 44}")

        for nl in [18, 25, 30, 40]:
            t0 = time.time()
            pm_all, gd_all = [], []
            for seed_i in range(n_seeds):
                r = run_mirror_test(nl, d_growth, seed_i * 7 + 3)
                if r:
                    pm_all.append(r["pm"])
                    gd_all.append(r["grav"])
            dt = time.time() - t0
            if pm_all:
                n_ok = len(pm_all)
                apm = sum(pm_all) / n_ok
                agd = sum(gd_all) / n_ok
                se = (sum((g - agd) ** 2 for g in gd_all) / n_ok) ** 0.5 / math.sqrt(n_ok) if n_ok > 1 else 0
                ratio = agd / se if se > 0 else 0
                print(f"  {nl:4d}  {apm:8.4f}  {1-apm:7.4f}  {agd:+8.3f}  "
                      f"{n_ok:4d}  {dt:4.0f}s  ({ratio:+.1f}SE)")
            else:
                print(f"  {nl:4d}  FAIL")
            import sys
            sys.stdout.flush()
        print()

    print("Compare:")
    print("  Codex S4 mirror (imposed 3D): 27% decoh, 7.2 SE gravity")
    print("  Our grown 4D (no mirror):     7.5% decoh, 2.5 SE gravity")
    print("  Combined mirror+grown:        ??? (above)")


if __name__ == "__main__":
    main()
