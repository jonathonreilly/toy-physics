#!/usr/bin/env python3
"""5D dense pilot on the retained local modular family.

This is a bounded follow-up to the 5D connectivity diagnostic.
The question is whether a denser but still local 5D regime can produce
a statistically meaningful positive mass-law signal, or whether 5D
remains connectivity-limited even after densification.

The pilot intentionally stays small:
  - one modular gap lane (gap=5)
  - a few denser local graph settings
  - the same paired mass-law measurement as the diagnostic

PStack experiment: five-d-dense-pilot
"""

from __future__ import annotations

import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8
K_BAND = [3.0, 5.0]
N_SEEDS = 4
N_LAYERS = 12
GAP = 5.0
MASS_COUNTS = [1, 2, 4, 6, 8, 12]


def generate_5d_modular_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = 50,
    spatial_range: float = 6.0,
    connect_radius: float = 5.5,
    rng_seed: int = 42,
    gap: float = GAP,
    crosslink_prob: float = 0.02,
):
    """Generate a 5D modular DAG with four transverse dimensions.

    The y-coordinate is channelized post-barrier, while the remaining
    transverse coordinates stay uniform. This keeps the pilot local.
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
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

                for prev_layer in layer_indices[max(0, layer - 2):]:
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


def compute_field(positions, adj, mass_idx, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    mass_set = set(mass_idx)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0] * n
        for i in range(n):
            if i in mass_set:
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
            L = math.sqrt(sum((a - b) ** 2 for a, b in zip(pi, pj)))
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            amps[j] += amps[i] * (cmath.exp(1j * k * act) * w / L)
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


def fit_alpha(rows):
    positive = [(n, s) for n, s, _, _ in rows if n > 0 and s > 0]
    if len(positive) < 3:
        return None
    xs = [math.log(n) for n, _ in positive]
    ys = [math.log(s) for _, s in positive]
    n_pts = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n_pts * sxx - sx * sx
    if abs(denom) < 1e-10:
        return None
    return (n_pts * sxy - sx * sy) / denom


def measure_config(nodes_per_layer, connect_radius, spatial_range, gap=GAP, n_seeds=N_SEEDS):
    per_mass = {target: [] for target in MASS_COUNTS}
    valid_seeds = 0
    out_degrees = []
    reach_fracs = []
    candidate_counts = []
    max_t_seen = 0.0

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

        if reach_frac <= 0.05 or len(candidates) < 4:
            continue

        valid_seeds += 1
        free_f = [0.0] * len(positions)

        for target_n in MASS_COUNTS:
            mass_nodes = candidates[:target_n]
            if len(mass_nodes) < target_n:
                continue

            field = compute_field(positions, adj, mass_nodes)
            shifts = []
            for k in K_BAND:
                amps_m = propagate(positions, adj, field, src, k)
                amps_f = propagate(positions, adj, free_f, src, k)
                shifts.append(
                    centroid_y(amps_m, positions, det_list)
                    - centroid_y(amps_f, positions, det_list)
                )
            if shifts:
                per_mass[target_n].append(sum(shifts) / len(shifts))

    summaries = []
    for target_n, vals in per_mass.items():
        if not vals:
            continue
        avg = sum(vals) / len(vals)
        se = math.sqrt(sum((v - avg) ** 2 for v in vals) / len(vals)) / math.sqrt(len(vals))
        t = avg / se if se > 1e-10 else 0.0
        summaries.append((target_n, avg, se, t))
        max_t_seen = max(max_t_seen, t)

    alpha = fit_alpha(summaries)
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
        "max_t": max_t_seen,
        "mass_summaries": summaries,
    }


def verdict(row):
    if row["alpha"] is not None and row["alpha"] > 0.2 and row["max_t"] > 2.0 and row["valid_rate"] > 0.5:
        return "POSITIVE"
    if row["alpha"] is not None and row["alpha"] > 0.2:
        return "WEAK POS"
    if row["valid_rate"] < 0.5 and row["avg_reach"] < 0.2:
        return "SPARSE"
    if row["valid_rate"] >= 0.5 and row["max_t"] > 1.5:
        return "MARGINAL"
    return "NO SIGNAL"


def main():
    print("=" * 78)
    print("5D DENSE PILOT")
    print("  4 spatial dims + 1 causal dim")
    print("  Goal: bounded densification probe, not a heroic search")
    print("=" * 78)
    print()
    print(f"  seeds/config: {N_SEEDS}")
    print(f"  layers: {N_LAYERS}")
    print(f"  gap: {GAP}")
    print(f"  mass counts: {MASS_COUNTS}")
    print(f"  k-band: {K_BAND}")
    print()

    configs = [
        (60, 6.0, 6.0),
        (80, 6.5, 5.5),
        (100, 6.5, 5.0),
    ]

    rows = []
    for nodes_per_layer, connect_radius, spatial_range in configs:
        rows.append(measure_config(nodes_per_layer, connect_radius, spatial_range))

    print("CONFIG SWEEP")
    print(
        f"  {'nodes':>5s}  {'rad':>4s}  {'range':>5s}  {'valid':>5s}  "
        f"{'out_deg':>7s}  {'reach':>7s}  {'cand':>5s}  {'alpha':>7s}  "
        f"{'max_t':>5s}  verdict"
    )
    print(f"  {'-' * 86}")

    best_alpha_row = None
    best_valid_row = None
    for row in rows:
        alpha_str = "NA" if row["alpha"] is None else f"{row['alpha']:.3f}"
        v = verdict(row)
        print(
            f"  {row['nodes_per_layer']:5d}  {row['connect_radius']:4.1f}  {row['spatial_range']:5.1f}  "
            f"{row['valid_rate']:5.2f}  {row['avg_out']:7.3f}  {row['avg_reach']:7.3f}  "
            f"{row['avg_candidates']:5.1f}  {alpha_str:>7s}  {row['max_t']:5.2f}  {v}"
        )
        if row["alpha"] is not None and (best_alpha_row is None or row["alpha"] > best_alpha_row["alpha"]):
            best_alpha_row = row
        if best_valid_row is None or row["valid_rate"] > best_valid_row["valid_rate"]:
            best_valid_row = row

    print()
    print("VERDICT")
    if best_alpha_row and best_alpha_row["alpha"] is not None and best_alpha_row["alpha"] > 0.2:
        if best_alpha_row["max_t"] > 2.0:
            print("  A measurable positive mass-law signal appears in the dense 5D pilot.")
        else:
            print("  A weak positive mass-law slope appears in the dense 5D pilot, but t-stats remain sub-significant.")
        print(
            f"  Best alpha = {best_alpha_row['alpha']:.3f} at "
            f"nodes={best_alpha_row['nodes_per_layer']}, rad={best_alpha_row['connect_radius']}, "
            f"range={best_alpha_row['spatial_range']}"
        )
    else:
        print(
            "  No stable positive mass-law signal emerged in this dense pilot."
            "  The 5D result still looks connectivity-limited."
        )

    if best_valid_row is not None:
        print(
            f"  Highest valid-setup rate = {best_valid_row['valid_rate']:.2f} at "
            f"nodes={best_valid_row['nodes_per_layer']}, rad={best_valid_row['connect_radius']}, "
            f"range={best_valid_row['spatial_range']}"
        )
    print("=" * 78)


if __name__ == "__main__":
    main()
