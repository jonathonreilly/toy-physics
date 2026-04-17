#!/usr/bin/env python3
"""Node-placement emergence: can WHERE nodes appear create topological barriers?

All previous emergence tests modified CONNECTION rules.
CLT defeats those because amplitude still reaches all nodes.

The modular DAG works because nodes DON'T EXIST in the gap.
Can a placement rule create this absence dynamically?

RULE: Post-barrier, place nodes where slit-distinguishability is HIGH.
Near y=0, both slits contribute equally → low distinguishability.
Near |y|>>0, one slit dominates → high distinguishability.
This directly avoids the center, creating an emergent gap.

Distinguishability at position y:
  D(y) = |f_upper(y) - f_lower(y)| / (f_upper(y) + f_lower(y))
  where f_slit(y) = amplitude density from that slit at height y.

Placement probability: P(y) ~ D(y)^alpha
  alpha=0: uniform (baseline)
  alpha>0: avoid center, place at edges

This is physically meaningful: the geometry grows where measurement
information exists. Space itself encodes which-path information
through its structure.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
N_YBINS = 8
LAM = 10.0


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


def _propagate_quick(positions, adj, n, src_set, blocked=None):
    """Quick propagation returning |amp|^2 per node."""
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src_set:
        amps[s] = 1.0 / max(1, len(src_set))
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * 5.0 * L) * w / L
            amps[j] += amps[i] * ea
    return [abs(a) ** 2 for a in amps]


def _slit_distinguishability_profile(positions, adj, n, src, slit_upper, slit_lower,
                                      barrier_blocked, y_range, n_bins=20):
    """Compute slit distinguishability D(y) as a function of y.

    Returns list of (y_center, D_value) for n_bins y-bins.
    D(y) = |f_upper(y) - f_lower(y)| / (f_upper(y) + f_lower(y) + eps)
    where f_slit(y) = sum of |amp|^2 at nodes near y from that slit.
    """
    blocked_lower = barrier_blocked | set(slit_lower)
    blocked_upper = barrier_blocked | set(slit_upper)

    amp_upper = _propagate_quick(positions, adj, n, src, blocked_lower)
    amp_lower = _propagate_quick(positions, adj, n, src, blocked_upper)

    bw = 2 * y_range / n_bins
    profile = []
    for b in range(n_bins):
        y_lo = -y_range + b * bw
        y_hi = y_lo + bw
        y_center = (y_lo + y_hi) / 2

        fu = sum(amp_upper[i] for i in range(n)
                 if y_lo <= positions[i][1] < y_hi)
        fl = sum(amp_lower[i] for i in range(n)
                 if y_lo <= positions[i][1] < y_hi)
        total = fu + fl
        if total > 1e-30:
            D = abs(fu - fl) / total
        else:
            D = 0.0
        profile.append((y_center, D))

    return profile


def generate_placement_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    alpha: float = 2.0,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """DAG with distinguishability-weighted node placement.

    Pre-barrier: uniform placement.
    Post-barrier: P(y) ~ D(y)^alpha where D is slit distinguishability.
    Nodes avoid the y-center where both slits contribute equally.
    """
    rng = __import__("random").Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    barrier_layer = n_layers // 3
    slit_upper = []
    slit_lower = []
    barrier_blocked = set()

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
        elif layer <= barrier_layer:
            # Pre-barrier: uniform placement
            for _ in range(nodes_per_layer):
                y = rng.uniform(-y_range, y_range)
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)

            # At barrier: identify slits
            if layer == barrier_layer:
                all_ys = [yy for _, yy in positions]
                cy = sum(all_ys) / len(all_ys)
                for idx in layer_nodes:
                    y = positions[idx][1]
                    if y > cy + 3:
                        slit_upper.append(idx)
                    elif y < cy - 3:
                        slit_lower.append(idx)
                    else:
                        barrier_blocked.add(idx)
                slit_upper = slit_upper[:3]
                slit_lower = slit_lower[:3]
        else:
            # Post-barrier: distinguishability-weighted placement
            n = len(positions)

            if alpha > 0 and slit_upper and slit_lower:
                # Compute distinguishability profile
                profile = _slit_distinguishability_profile(
                    positions, adj, n,
                    layer_indices[0], slit_upper, slit_lower,
                    barrier_blocked, y_range,
                )

                # Build CDF for rejection sampling
                weights = [(yc, max(d, 0.01) ** alpha) for yc, d in profile]
                total_w = sum(w for _, w in weights)

                for _ in range(nodes_per_layer):
                    # Rejection sampling: sample y proportional to D(y)^alpha
                    for _ in range(50):  # max attempts
                        y_cand = rng.uniform(-y_range, y_range)
                        # Find D at this y
                        bw = 2 * y_range / len(profile)
                        b = int((y_cand + y_range) / bw)
                        b = max(0, min(len(profile) - 1, b))
                        _, d_val = profile[b]
                        p_accept = max(d_val, 0.01) ** alpha / (1.0 ** alpha)
                        # Normalize
                        max_d = max(d for _, d in profile)
                        if max_d > 0:
                            p_accept = (max(d_val, 0.01) / max(max_d, 0.01)) ** alpha
                        else:
                            p_accept = 1.0

                        if rng.random() < p_accept:
                            break
                    else:
                        y_cand = rng.uniform(-y_range, y_range)

                    y = y_cand
                    idx = len(positions)
                    positions.append((x, y))
                    layer_nodes.append(idx)

                    for prev_layer in layer_indices[max(0, layer - 2):]:
                        for prev_idx in prev_layer:
                            if prev_idx in barrier_blocked:
                                continue
                            px, py = positions[prev_idx]
                            dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)
            else:
                # Fallback: uniform
                for _ in range(nodes_per_layer):
                    y = rng.uniform(-y_range, y_range)
                    idx = len(positions)
                    positions.append((x, y))
                    layer_nodes.append(idx)
                    for prev_layer in layer_indices[max(0, layer - 2):]:
                        for prev_idx in prev_layer:
                            if prev_idx in barrier_blocked:
                                continue
                            px, py = positions[prev_idx]
                            dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    # Arrival
    n = len(positions)
    arrival = [float("inf")] * n
    for i in range(n):
        if positions[i][0] == 0.0:
            arrival[i] = 0.0
    order = sorted(range(n), key=lambda i: (positions[i][0], i))
    for i in order:
        if not math.isfinite(arrival[i]):
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            cand = arrival[i] + dist
            if cand < arrival[j]:
                arrival[j] = cand

    return positions, dict(adj), arrival


# ─── Shared test machinery ─────────────────────────────────────────

def compute_field(positions, mass_nodes, strength=0.1):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += strength / r
    return field


def propagate_full(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
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
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def bin_amplitudes(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity_triple(amps_a, amps_b, D, det_list):
    def _pur(Dv):
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                    + Dv * amps_a[d1].conjugate() * amps_b[d2]
                    + Dv * amps_b[d1].conjugate() * amps_a[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real
    return _pur(D), _pur(1.0), _pur(0.0)


def run_joint(positions, adj, k_band, n_layers):
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None
    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
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
    stop = min(len(layers), start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])
    field_m = compute_field(positions, mass_nodes, 0.1)
    field_f = [0.0] * len(positions)
    gd, pmv, dv = [], [], []
    for k in k_band:
        am = propagate_full(positions, adj, field_m, src, k, blocked)
        af = propagate_full(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            gd.append(ym - yf)
        aa = propagate_full(positions, adj, field_m, src, k, blocked | set(sb))
        ab = propagate_full(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes(aa, positions, mid)
        bb = bin_amplitudes(ab, positions, mid)
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D = math.exp(-LAM ** 2 * Sn)
        pc, pcoh, pmin = cl_purity_triple(aa, ab, D, det_list)
        if not math.isnan(pc):
            pmv.append(pmin)
            dv.append(pcoh - pc)
    if not gd or not pmv:
        return None
    return {"grav": sum(gd)/len(gd), "pm": sum(pmv)/len(pmv), "dec": sum(dv)/len(dv)}


def measure_gap(positions, n_layers):
    """Measure effective gap in post-barrier node placement."""
    barrier_layer = n_layers // 3
    post_ys = [y for x, y in positions if x > barrier_layer]
    if not post_ys:
        return 0.0
    # Sort and find largest gap between consecutive y values
    post_ys.sort()
    max_gap = 0.0
    for i in range(1, len(post_ys)):
        gap = post_ys[i] - post_ys[i-1]
        if gap > max_gap:
            max_gap = gap
    return max_gap


def main():
    from scripts.generative_causal_dag_interference import generate_causal_dag

    print("=" * 78)
    print("NODE-PLACEMENT EMERGENCE: Distinguishability-Weighted Growth")
    print("  Nodes placed where slit distinguishability is HIGH")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7], 16 seeds")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 16

    families = [
        ("Uniform (baseline)", generate_causal_dag, {}),
        ("Placement alpha=1", generate_placement_dag, {"alpha": 1.0}),
        ("Placement alpha=2", generate_placement_dag, {"alpha": 2.0}),
        ("Placement alpha=4", generate_placement_dag, {"alpha": 4.0}),
        ("Placement alpha=8", generate_placement_dag, {"alpha": 8.0}),
    ]

    for name, gen, kwargs in families:
        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'grav_d':>8s}  {'pur_min':>8s}  {'decoh':>8s}  "
              f"{'eff_gap':>7s}  {'n_ok':>4s}")
        print(f"  {'-' * 48}")

        for nl in [12, 18, 25, 40]:
            t0 = time.time()
            grav_all, pm_all, dec_all, gap_all = [], [], [], []

            for seed in range(n_seeds):
                positions, adj, _ = gen(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 7 + 3, **kwargs,
                )

                eg = measure_gap(positions, nl)
                gap_all.append(eg)

                r = run_joint(positions, adj, k_band, nl)
                if r:
                    grav_all.append(r["grav"])
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])

            dt = time.time() - t0

            if grav_all:
                ag = sum(grav_all) / len(grav_all)
                apm = sum(pm_all) / len(pm_all)
                adec = sum(dec_all) / len(dec_all)
                agap = sum(gap_all) / len(gap_all)
                print(f"  {nl:4d}  {ag:+8.3f}  {apm:8.4f}  {adec:+8.4f}  "
                      f"{agap:7.2f}  {len(grav_all):4d}  ({dt:.0f}s)")
            else:
                print(f"  {nl:4d}  FAIL")

        print()

    print("eff_gap = largest y-gap between consecutive post-barrier nodes")
    print("EMERGENT = pur_min < 0.95 AND eff_gap > 2.0 at N=40")
    print("(eff_gap > 2.0 would show nodes actually avoiding the center)")


if __name__ == "__main__":
    main()
