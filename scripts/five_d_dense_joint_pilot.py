#!/usr/bin/env python3
"""5D dense joint pilot on the retained modular corner.

This is a conservative follow-up to the dense 5D robustness work.
The question is not whether 5D has a magic corner, but whether the
same dense modular window that supports the mass-law signal also
supports a gravity read plus a decoherence/Born sanity read.

The pilot stays narrow:
  - dense modular 5D neighborhood around the retained corner
  - same retained graph family as the mass-law pilot
  - mass-law sweep across a small target set
  - one fixed-mass gravity/decoherence/Born sanity read per seed
  - same graph instances for all measurements in a seed

The claim discipline is deliberately conservative:
  - report the gravity signal and the mass-law exponent
  - report CL-bath purity / decoherence from a fixed-mass read
  - report same-family Born sanity using a chokepoint-pruned view
  - do not promote any result beyond the narrow tested window

PStack experiment: five-d-dense-joint-pilot
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
import sys
from collections import defaultdict, deque

ROOT = sys.path[0]
if ROOT and ROOT not in sys.path:
    sys.path.insert(0, ROOT)

BETA = 0.8
LAM = 10.0
K_BAND = (3.0, 5.0)
BORN_K = 5.0
N_SEEDS = 4
N_LAYERS = 12
GAP = 5.0
MASS_COUNTS = (1, 2, 4, 8)
MASS_COUNT_FIXED = 8
N_YBINS = 6

# Neighborhood around the previously retained dense 5D corner.
CONFIGS = [
    ("low-center", 90, 6.50, 5.0),
    ("center-low", 100, 6.25, 5.0),
    ("center", 100, 6.50, 5.0),
    ("center-high", 100, 6.75, 5.0),
    ("top-center", 110, 6.50, 5.0),
]


def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else math.nan


def _se(vals: list[float]) -> float:
    if len(vals) < 2:
        return math.nan
    return statistics.stdev(vals) / math.sqrt(len(vals))


def _fit_power_law(xs_in: list[float], ys_in: list[float]) -> tuple[float, float, float] | None:
    pairs = [(x, y) for x, y in zip(xs_in, ys_in) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(x) for x, _ in pairs]
    ys = [math.log(y) for _, y in pairs]
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return slope, math.exp(intercept), r2


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def generate_5d_modular_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = 100,
    spatial_range: float = 5.0,
    connect_radius: float = 6.5,
    rng_seed: int = 42,
    gap: float = GAP,
    crosslink_prob: float = 0.02,
):
    """Generate the retained 5D modular DAG family."""
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            positions.append((x, 0.0, 0.0, 0.0, 0.0))
            layer_nodes.append(0)
        else:
            for node_i in range(nodes_per_layer):
                coords = [x]
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, spatial_range)
                    else:
                        y = rng.uniform(-spatial_range, -gap / 2)
                else:
                    y = rng.uniform(-spatial_range, spatial_range)
                coords.append(y)
                for _ in range(3):
                    coords.append(rng.uniform(-spatial_range, spatial_range))

                idx = len(positions)
                positions.append(tuple(coords))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2) :]:
                    for prev_idx in prev_layer:
                        px, py, pz, pw, pv = positions[prev_idx]
                        dx = x - px
                        dy = y - py
                        dz = coords[2] - pz
                        dw = coords[3] - pw
                        dv = coords[4] - pv
                        dist = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw + dv * dv)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_channel = (y * py > 0)
                            if same_channel:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
                                    adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def compute_field(positions, adj, mass_idx, iterations: int = 50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)

    mass_set = set(mass_idx)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        next_field = [0.0] * n
        for i in range(n):
            if i in mass_set:
                next_field[i] = 1.0
            elif undirected.get(i):
                next_field[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = next_field
    return field


def propagate(positions, adj, field, src, k, blocked=None, order=None):
    n = len(positions)
    blocked = blocked or set()
    if order is None:
        order = _topo_order(adj, n)
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
            L = math.sqrt(sum((a - b) ** 2 for a, b in zip(pi, pj)))
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            weight = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            amps[j] += amps[i] * (cmath.exp(1j * k * act) * weight / L)
    return amps


def centroid_y(amps, positions, det_list):
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def reachable_fraction(adj, src, det_list):
    seen = set(src)
    q = deque(src)
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if j not in seen:
                seen.add(j)
                q.append(j)
    if not det_list:
        return 0.0
    return sum(1 for d in det_list if d in seen) / len(det_list)


def _layer_map(layer_indices: list[list[int]]) -> dict[int, int]:
    out: dict[int, int] = {}
    for li, nodes in enumerate(layer_indices):
        for idx in nodes:
            out[idx] = li
    return out


def _prune_bypass_edges(
    adj: dict[int, list[int]],
    layer_indices: list[list[int]],
    barrier_layer: int,
) -> dict[int, list[int]]:
    """Remove edges that jump across the barrier layer."""
    by_idx = _layer_map(layer_indices)
    pruned: dict[int, list[int]] = defaultdict(list)
    for i, nbs in adj.items():
        li = by_idx.get(i, -1)
        for j in nbs:
            lj = by_idx.get(j, -1)
            if li < barrier_layer and lj > barrier_layer:
                continue
            pruned[i].append(j)
    return dict(pruned)


def _slit_partition(
    positions: list[tuple[float, float, float, float, float]],
    layer_indices: list[list[int]],
):
    n_layers = len(layer_indices)
    if n_layers < 6:
        return None

    barrier_layer = n_layers // 3
    barrier = list(layer_indices[barrier_layer])
    if len(barrier) < 15:
        return None

    barrier_sorted = sorted(barrier, key=lambda i: positions[i][1])
    slit_c = barrier_sorted[:5]
    slit_b = barrier_sorted[len(barrier_sorted) // 2 - 2 : len(barrier_sorted) // 2 + 3]
    slit_a = barrier_sorted[-5:]

    all_slits = slit_a + slit_b + slit_c
    blocked = set(barrier) - set(all_slits)
    src = list(layer_indices[0])
    det_list = list(layer_indices[-1])
    if not src or not det_list:
        return None
    return barrier_layer, barrier, src, blocked, det_list, slit_a, slit_b, slit_c


def _cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0, 0.0
    y_min, y_max = min(ys) - 0.01, max(ys) + 0.01
    bw = (y_max - y_min) / N_YBINS
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid_nodes:
        b = max(0, min(N_YBINS - 1, int((positions[m][1] - y_min) / bw)))
        ba[b] += amps_a[m]
        bb[b] += amps_b[m]
    S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    d = sum(abs(a) ** 2 for a in ba) + sum(abs(b) ** 2 for b in bb)
    return S, S / d if d > 0 else 0.0


def _cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            aa = amps_a[d1] * amps_a[d2].conjugate()
            bb = amps_b[d1] * amps_b[d2].conjugate()
            ab = amps_a[d1] * amps_b[d2].conjugate()
            ba = amps_b[d1] * amps_a[d2].conjugate()
            rho[(d1, d2)] = aa + bb + D * ab + D * ba
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def _born_sanity(
    positions,
    adj,
    layer_indices,
    field,
    src,
    det_list,
    k: float = BORN_K,
    order: list[int] | None = None,
):
    partition = _slit_partition(positions, layer_indices)
    if partition is None:
        return None
    barrier_layer, barrier, src, blocked, det_list, slit_a, slit_b, slit_c = partition
    born_adj = _prune_bypass_edges(adj, layer_indices, barrier_layer)
    born_order = order if order is not None else _topo_order(born_adj, len(positions))
    all_slits = set(slit_a) | set(slit_b) | set(slit_c)

    def prob(open_set: set[int]) -> tuple[float, list[complex]]:
        closed = all_slits - open_set
        amps = propagate(positions, born_adj, field, src, k, blocked | closed, born_order)
        return sum(abs(amps[d]) ** 2 for d in det_list), amps

    p_abc, amps_abc = prob(all_slits)
    p_ab, amps_ab = prob(set(slit_a) | set(slit_b))
    p_ac, amps_ac = prob(set(slit_a) | set(slit_c))
    p_bc, amps_bc = prob(set(slit_b) | set(slit_c))
    p_a, amps_a = prob(set(slit_a))
    p_b, amps_b = prob(set(slit_b))
    p_c, amps_c = prob(set(slit_c))

    max_lin = 0.0
    for d in det_list:
        ref = max(abs(amps_ab[d]), abs(amps_a[d] + amps_b[d]))
        if ref > 1e-30:
            max_lin = max(max_lin, abs(amps_ab[d] - (amps_a[d] + amps_b[d])) / ref)

    i3 = p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c
    ratio = abs(i3) / p_abc if p_abc > 1e-30 else math.nan
    return max_lin, i3, ratio


def measure_joint_config(nodes_per_layer, connect_radius, spatial_range, gap=GAP, n_seeds=N_SEEDS):
    per_mass = {target: [] for target in MASS_COUNTS}
    valid_seeds = 0
    out_degrees = []
    reach_fracs = []
    candidate_counts = []
    mass_count_fixed = MASS_COUNT_FIXED

    gravity_shifts = []
    pur_cl_vals = []
    pur_min_vals = []
    s_norm_vals = []
    born_lin_vals = []
    born_i3_vals = []
    born_ratio_vals = []

    for seed in range(n_seeds):
        positions, adj, layer_indices = generate_5d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=nodes_per_layer,
            spatial_range=spatial_range,
            connect_radius=connect_radius,
            rng_seed=seed * 17 + 3,
            gap=gap,
        )

        node_count = len(positions)
        edge_count = sum(len(v) for v in adj.values())
        out_degrees.append(edge_count / node_count if node_count else 0.0)
        order = _topo_order(adj, len(positions))

        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        reach_frac = reachable_fraction(adj, src, det_list)
        reach_fracs.append(reach_frac)

        all_ys = [positions[i][1] for i in range(len(positions))]
        cy = sum(all_ys) / len(all_ys)
        mid = len(layer_indices) // 2
        candidates = sorted(
            [i for i in layer_indices[mid] if positions[i][1] > cy + 1],
            key=lambda i: -positions[i][1],
        )
        candidate_counts.append(len(candidates))

        if reach_frac <= 0.05 or len(candidates) < max(MASS_COUNTS):
            continue

        partition = _slit_partition(positions, layer_indices)
        if partition is None:
            continue
        barrier_layer, barrier, _src, blocked, _det, slit_a, slit_b, slit_c = partition
        mid_nodes = [
            i
            for li in range(barrier_layer + 1, len(layer_indices) - 1)
            for i in layer_indices[li]
            if i not in blocked and i not in set(det_list)
        ]
        if len(mid_nodes) < 4:
            continue

        valid_seeds += 1
        free_f = [0.0] * len(positions)

        seed_gravity = []
        seed_pur = []
        seed_pmin = []
        seed_snorm = []
        seed_lin = []
        seed_i3 = []
        seed_ratio = []

        # Mass-law sweep on the retained window.
        for target_n in MASS_COUNTS:
            mass_nodes = candidates[:target_n]
            if len(mass_nodes) < target_n:
                continue

            field = compute_field(positions, adj, mass_nodes)
            shifts = []
            for k in K_BAND:
                amps_m = propagate(positions, adj, field, src, k, order=order)
                amps_f = propagate(positions, adj, free_f, src, k, order=order)
                shifts.append(centroid_y(amps_m, positions, det_list) - centroid_y(amps_f, positions, det_list))
            if shifts:
                per_mass[target_n].append(sum(shifts) / len(shifts))

        # Fixed-mass sanity read on the same graph instance.
        mass_nodes = candidates[:mass_count_fixed]
        if len(mass_nodes) >= mass_count_fixed:
            field = compute_field(positions, adj, mass_nodes)
            for k in K_BAND:
                amps_a = propagate(positions, adj, field, src, k, blocked | set(slit_b), order=order)
                amps_b = propagate(positions, adj, field, src, k, blocked | set(slit_a), order=order)
                S, s_norm = _cl_contrast(amps_a, amps_b, mid_nodes, positions)
                D = math.exp(-(LAM ** 2) * s_norm)
                pur_cl = _cl_purity(amps_a, amps_b, D, det_list)
                pur_min = _cl_purity(amps_a, amps_b, 0.0, det_list)
                born = _born_sanity(positions, adj, layer_indices, field, src, det_list, k=BORN_K, order=order)
                if born is not None:
                    born_lin, born_i3, born_ratio = born
                    seed_lin.append(born_lin)
                    seed_i3.append(born_i3)
                    seed_ratio.append(born_ratio)
                if not math.isnan(pur_cl):
                    seed_pur.append(pur_cl)
                    seed_pmin.append(pur_min)
                    seed_snorm.append(s_norm)

            if seed_pur:
                gravity_shifts.append(
                    _mean(
                        [
                            centroid_y(propagate(positions, adj, field, src, k, order=order), positions, det_list)
                            - centroid_y(propagate(positions, adj, free_f, src, k, order=order), positions, det_list)
                            for k in K_BAND
                        ]
                    )
                )
                pur_cl_vals.append(_mean(seed_pur))
                pur_min_vals.append(_mean(seed_pmin))
                s_norm_vals.append(_mean(seed_snorm))
                if seed_lin:
                    born_lin_vals.append(_mean(seed_lin))
                    born_i3_vals.append(_mean(seed_i3))
                    born_ratio_vals.append(_mean(seed_ratio))

    summaries = []
    for target_n, vals in per_mass.items():
        if not vals:
            continue
        avg = sum(vals) / len(vals)
        se = math.sqrt(sum((v - avg) ** 2 for v in vals) / len(vals)) / math.sqrt(len(vals))
        t = avg / se if se > 1e-10 else 0.0
        summaries.append((target_n, avg, se, t))

    alpha = None
    fit = _fit_power_law([n for n, _avg, _se, _t in summaries], [avg for _n, avg, _se, _t in summaries])
    if fit is not None:
        alpha = fit[0]

    valid_rate = valid_seeds / n_seeds if n_seeds else 0.0
    avg_out = sum(out_degrees) / len(out_degrees) if out_degrees else 0.0
    avg_reach = sum(reach_fracs) / len(reach_fracs) if reach_fracs else 0.0
    avg_candidates = sum(candidate_counts) / len(candidate_counts) if candidate_counts else 0.0

    return {
        "nodes_per_layer": nodes_per_layer,
        "connect_radius": connect_radius,
        "spatial_range": spatial_range,
        "gap": gap,
        "valid_rate": valid_rate,
        "avg_out": avg_out,
        "avg_reach": avg_reach,
        "avg_candidates": avg_candidates,
        "alpha": alpha,
        "mass_summaries": summaries,
        "grav_shift": _mean(gravity_shifts) if gravity_shifts else math.nan,
        "pur_cl": _mean(pur_cl_vals) if pur_cl_vals else math.nan,
        "pur_min": _mean(pur_min_vals) if pur_min_vals else math.nan,
        "s_norm": _mean(s_norm_vals) if s_norm_vals else math.nan,
        "born_lin": _mean(born_lin_vals) if born_lin_vals else math.nan,
        "born_i3": _mean(born_i3_vals) if born_i3_vals else math.nan,
        "born_ratio": _mean(born_ratio_vals) if born_ratio_vals else math.nan,
    }


def _fmt(v: float | None) -> str:
    if v is None or not math.isfinite(v):
        return "NA"
    return f"{v:.3f}"


def _positive_support_count(row) -> int:
    return sum(1 for _n, avg, _se, t in row["mass_summaries"] if avg > 0 and t > 1.5)


def _stable_score(row):
    alpha = row["alpha"] if row["alpha"] is not None else 0.0
    return (
        _positive_support_count(row),
        row["valid_rate"],
        row["pur_cl"] if math.isfinite(row["pur_cl"]) else 0.0,
        -abs(alpha - 0.6),
        row["born_ratio"] if math.isfinite(row["born_ratio"]) else 1.0,
        row["grav_shift"] if math.isfinite(row["grav_shift"]) else 0.0,
    )


def main() -> None:
    print("=" * 90)
    print("5D DENSE JOINT PILOT")
    print("  4 spatial dims + 1 causal dim")
    print("  Goal: same dense 5D corner, gravity plus decoherence/Born sanity read")
    print("=" * 90)
    print()
    print(f"  seeds/config: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  fixed mass count for sanity read: {MASS_COUNT_FIXED}")
    print(f"  mass counts: {MASS_COUNTS}")
    print(f"  k-band: {K_BAND}")
    print(f"  Born k: {BORN_K}")
    print("  neighborhood: the retained dense window around nodes=100, rad=6.5, range=5.0")
    print()

    rows = []
    for label, nodes_per_layer, connect_radius, spatial_range in CONFIGS:
        row = measure_joint_config(
            nodes_per_layer=nodes_per_layer,
            connect_radius=connect_radius,
            spatial_range=spatial_range,
            gap=GAP,
            n_seeds=N_SEEDS,
        )
        row["label"] = label
        rows.append(row)

    print("CONFIG SWEEP")
    print(
        f"  {'label':>12s}  {'nodes':>5s}  {'rad':>4s}  {'range':>5s}  {'valid':>5s}  "
        f"{'out_deg':>7s}  {'reach':>7s}  {'cand':>5s}  {'alpha':>7s}  {'grav':>7s}  "
        f"{'pur_cl':>8s}  {'born':>8s}  verdict"
    )
    print(f"  {'-' * 120}")

    for row in rows:
        if row["alpha"] is not None and row["alpha"] > 0.2 and row["grav_shift"] > 0 and row["pur_cl"] < 0.96 and row["born_ratio"] < 1e-8:
            verdict = "JOINT PASS"
        elif row["grav_shift"] > 0 and row["pur_cl"] < 0.96:
            verdict = "GRAV+DECOH"
        elif row["grav_shift"] > 0:
            verdict = "GRAV ONLY"
        else:
            verdict = "MARGINAL"

        print(
            f"  {row['label']:>12s}  {row['nodes_per_layer']:5d}  {row['connect_radius']:4.2f}  "
            f"{row['spatial_range']:5.2f}  {row['valid_rate']:5.2f}  {row['avg_out']:7.3f}  "
            f"{row['avg_reach']:7.3f}  {row['avg_candidates']:5.1f}  {_fmt(row['alpha']):>7s}  "
            f"{_fmt(row['grav_shift']):>7s}  {_fmt(row['pur_cl']):>8s}  {_fmt(row['born_ratio']):>8s}  "
            f"{verdict}"
        )

    print()
    print("MASS-LAW DETAIL")
    for row in rows:
        print(
            f"  {row['label']}: alpha={_fmt(row['alpha'])}, valid={row['valid_rate']:.2f}, "
            f"grav={_fmt(row['grav_shift'])}, pur_cl={_fmt(row['pur_cl'])}, born_ratio={_fmt(row['born_ratio'])}"
        )
        for target_n, avg, se, t in row["mass_summaries"]:
            print(f"    n={target_n:2d}, shift={avg:+.4f}, SE={se:.4f}, t={t:+.2f}")

    print()
    ranked = sorted(rows, key=_stable_score, reverse=True)
    print("RANKING")
    for idx, row in enumerate(ranked, start=1):
        print(
            f"  {idx:>2d}. {row['label']:>12s} | alpha={_fmt(row['alpha']):>7s} | "
            f"grav={_fmt(row['grav_shift']):>7s} | pur_cl={_fmt(row['pur_cl']):>8s} | "
            f"born={_fmt(row['born_ratio']):>8s} | support={_positive_support_count(row):d}"
        )

    best = ranked[0] if ranked else None
    print()
    print("VERDICT")
    if best is None:
        print("  No usable dense 5D row emerged.")
    else:
        print(
            f"  Best joint row = {best['label']} at nodes={best['nodes_per_layer']}, "
            f"rad={best['connect_radius']}, range={best['spatial_range']}."
        )
        print(
            f"  Gravity shift={_fmt(best['grav_shift'])}, alpha={_fmt(best['alpha'])}, "
            f"pur_cl={_fmt(best['pur_cl'])}, born_ratio={_fmt(best['born_ratio'])}."
        )
        if best["grav_shift"] > 0 and best["pur_cl"] < 0.96:
            print("  Conservative headline: the dense 5D corner supports gravity plus a decoherence sanity read.")
        elif best["grav_shift"] > 0:
            print("  Conservative headline: the dense 5D corner supports gravity, but the decoherence/Born read is only partial.")
        else:
            print("  Conservative headline: the dense 5D corner remains connectivity-limited for the joint read.")
    print("=" * 90)


if __name__ == "__main__":
    main()
