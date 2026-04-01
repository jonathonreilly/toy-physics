#!/usr/bin/env python3
"""Per-seed correlation between gravity and decoherence.

The model produces both gravity and decoherence from the same propagator
on the same graphs. But do they CO-VARY across seeds? Three possibilities:

  1. POSITIVE correlation: graphs that give strong gravity also give
     strong decoherence → shared structural cause
  2. NEGATIVE correlation: gravity and decoherence compete for the
     same graph features → structural tradeoff
  3. NO correlation: independent mechanisms that happen to coexist

This tests across many seeds on 3D modular DAGs, measuring both
gravity (centroid shift) and decoherence (1 - pur_cl) per seed.

PStack experiment: gravity-decoherence-correlation
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8
LAM = 10.0


def generate_3d_modular_dag(n_layers=18, nodes_per_layer=30, yz_range=10.0,
                            connect_radius=3.5, rng_seed=42, gap=3.0,
                            crosslink_prob=0.02):
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
            layer_nodes.append(len(positions)-1)
        else:
            for ni in range(nodes_per_layer):
                z = rng.uniform(-yz_range, yz_range)
                if gap > 0 and layer > barrier_layer:
                    y = rng.uniform(gap/2, yz_range) if ni < nodes_per_layer//2 else rng.uniform(-yz_range, -gap/2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if gap > 0 and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch and dist <= connect_radius:
                                adj[prev_idx].append(idx)
                            elif not same_ch and dist <= 2*connect_radius and rng.random() < crosslink_prob:
                                adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


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
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
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


def measure_both(seed, nl=25, gap=3.0):
    """Measure gravity and decoherence on the same graph instance."""
    k_band = [3.0, 5.0, 7.0]

    positions, adj, layer_indices = generate_3d_modular_dag(
        n_layers=nl, nodes_per_layer=30, yz_range=10.0,
        connect_radius=3.5, rng_seed=seed*13+5, gap=gap)

    n = len(positions)
    n_actual = len(layer_indices)
    bl_idx = n_actual // 3
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    if not det_list or n_actual < 7:
        return None

    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys) / len(all_ys)

    # Barrier/slits for decoherence
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b:
        return None
    blocked = set(barrier) - set(slit_a + slit_b)
    blocked_a = blocked | set(slit_b)
    blocked_b = blocked | set(slit_a)

    # Mass for field
    bath_mass = []
    for li in range(bl_idx+1, min(n_actual, bl_idx+3)):
        for i in layer_indices[li]:
            if abs(positions[i][1] - cy) <= 3:
                bath_mass.append(i)
    grav_idx = 2 * n_actual // 3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1][:8]
    all_mass = list(set(bath_mass) | set(grav_mass))
    field = compute_field(positions, adj, all_mass) if all_mass else [0.0]*n
    free_field = [0.0] * n

    mid_nodes = [i for li in range(bl_idx+1, n_actual-1)
                 for i in layer_indices[li]
                 if i not in blocked and i not in set(det_list)]
    if len(mid_nodes) < 4:
        return None

    grav_shifts = []
    pur_cls = []

    for k in k_band:
        # Gravity
        am = propagate(positions, adj, field, src, k)
        af = propagate(positions, adj, free_field, src, k)
        grav_shifts.append(centroid_y(am, positions, det_list) -
                           centroid_y(af, positions, det_list))

        # Decoherence
        aa = propagate(positions, adj, field, src, k, blocked_a)
        ab = propagate(positions, adj, field, src, k, blocked_b)
        Sn = cl_contrast(aa, ab, mid_nodes, positions)
        D = math.exp(-LAM**2 * Sn)
        pur = cl_purity(aa, ab, D, det_list)
        if not math.isnan(pur):
            pur_cls.append(pur)

    if grav_shifts and pur_cls:
        grav = sum(grav_shifts) / len(grav_shifts)
        decoh = 1 - sum(pur_cls) / len(pur_cls)  # higher = more decoherence
        return grav, decoh
    return None


def pearson_r(xs, ys):
    n = len(xs)
    if n < 3:
        return 0, 0
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    sxx = sum((x-mx)**2 for x in xs)
    syy = sum((y-my)**2 for y in ys)
    if sxx < 1e-30 or syy < 1e-30:
        return 0, 0
    r = sxy / math.sqrt(sxx * syy)
    # t-statistic
    if abs(r) > 0.999:
        t = 999
    else:
        t = r * math.sqrt((n-2) / (1 - r*r))
    return r, t


def main():
    print("=" * 70)
    print("GRAVITY-DECOHERENCE CORRELATION")
    print("  Per-seed: do strong-gravity seeds also show strong decoherence?")
    print("=" * 70)
    print()

    for gap in [0.0, 3.0, 5.0]:
        for nl in [20, 30, 40]:
            label = f"gap={gap}, N={nl}"
            gravs = []
            decohs = []

            for seed in range(48):
                result = measure_both(seed, nl=nl, gap=gap)
                if result:
                    g, d = result
                    gravs.append(g)
                    decohs.append(d)

            if len(gravs) < 10:
                print(f"  [{label}] — insufficient data ({len(gravs)} seeds)")
                continue

            r, t = pearson_r(gravs, decohs)
            n_ok = len(gravs)
            mg = sum(gravs) / n_ok
            md = sum(decohs) / n_ok

            if abs(t) > 2.5:
                verdict = "STRONG" if r > 0 else "STRONG NEGATIVE"
            elif abs(t) > 1.5:
                verdict = "MODERATE" if r > 0 else "MODERATE NEGATIVE"
            else:
                verdict = "INDEPENDENT"

            print(f"  [{label}] n={n_ok}")
            print(f"    <gravity>    = {mg:+.4f}")
            print(f"    <decoherence>= {md:+.4f}")
            print(f"    Pearson r    = {r:+.3f} (t={t:+.2f})")
            print(f"    → {verdict}")
            print()

    print("=" * 70)
    print("INTERPRETATION:")
    print("  r > 0, significant: shared structural cause (co-dependent)")
    print("  r < 0, significant: structural tradeoff (competitive)")
    print("  r ≈ 0: independent mechanisms (coexistence, not coupling)")
    print("=" * 70)


if __name__ == "__main__":
    main()
