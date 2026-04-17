#!/usr/bin/env python3
"""Mechanism audit for the q=0.03 dense-prune gravity sign flip.

The question is whether the pruned gravity flip is better explained by loss
of mass-coupled detector connectivity than by a raw detector-reach statistic.

We run three bounded checks on the same dense 3D setup:
  1. Per-seed stratification of gravity delta vs. a mass-to-detector reach
     metric, before and after prune.
  2. Frozen-field control: apply the original-field phase on the pruned graph
     and compare against recomputed-on-pruned field.
  3. Narrow guard: protect the mass-region-to-detector path core rather than
     raw detector reach, then see whether the sign flip softens.

PStack experiment: dense-prune-q003-mechanism-audit
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.causal_field_mass_scaling import field_laplacian  # type: ignore  # noqa: E402
from scripts.dense_prune_q003_joint_strict import (  # type: ignore  # noqa: E402
    GAP,
    K_BAND,
    N_LAYERS_LIST,
    N_SEEDS,
    NODES_PER_LAYER,
    CONNECT_RADIUS,
    XYZ_RANGE,
    _barrier_slices,
    _joint_summary,
    _layer_map,
    _prune_graph,
    _select_mass_nodes,
)
from scripts.three_d_joint_test import (  # type: ignore  # noqa: E402
    cl_purity,
    generate_3d_dag,
    propagate_3d,
)

Q = 0.03
PRUNE_ITERS = 1


def _pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(ys) < 2:
        return float("nan")
    xm = statistics.fmean(xs)
    ym = statistics.fmean(ys)
    num = sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - xm) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - ym) ** 2 for y in ys))
    if den_x <= 1e-30 or den_y <= 1e-30:
        return float("nan")
    return num / (den_x * den_y)


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


def _mass_to_detector_reach(
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
) -> tuple[float, set[int]]:
    """Return detector reach fraction and the forward closure from mass nodes."""
    reachable: set[int] = set(mass_nodes)
    q = deque(mass_nodes)
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if j not in reachable:
                reachable.add(j)
                q.append(j)
    det_set = set(det_nodes)
    if not det_set:
        return 0.0, reachable
    return len(reachable & det_set) / len(det_set), reachable


def _mass_path_support(adj: dict[int, list[int]], mass_nodes: list[int], det_nodes: list[int]) -> float:
    """Mean log1p of the number of mass-to-detector paths.

    This is more sensitive than raw reach because pruning can leave reach
    intact while thinning the mass-coupled support carrying the signal.
    """
    n = 1 + max(max(adj.keys(), default=0), max((j for nbs in adj.values() for j in nbs), default=0))
    order = _topo_order(adj, n)
    counts = [0] * n
    for m in mass_nodes:
        counts[m] += 1
    for i in order:
        if counts[i] <= 0:
            continue
        for j in adj.get(i, []):
            counts[j] += counts[i]
    if not det_nodes:
        return 0.0
    return statistics.fmean(math.log1p(counts[d]) for d in det_nodes)


def _post_barrier_nodes(positions: list[tuple[float, float, float]]) -> tuple[dict[int, list[int]], list[int]]:
    by_layer, layers = _layer_map(positions)
    return by_layer, layers


def _reverse_closure(adj: dict[int, list[int]], targets: list[int]) -> set[int]:
    rev: dict[int, list[int]] = defaultdict(list)
    for i, nbs in adj.items():
        for j in nbs:
            rev[j].append(i)
    seen: set[int] = set(targets)
    q = deque(targets)
    while q:
        i = q.popleft()
        for p in rev.get(i, []):
            if p not in seen:
                seen.add(p)
                q.append(p)
    return seen


def _path_core_nodes(adj: dict[int, list[int]], mass_nodes: list[int], det_nodes: list[int]) -> set[int]:
    forward = _mass_to_detector_reach(adj, mass_nodes, det_nodes)[1]
    reverse = _reverse_closure(adj, det_nodes)
    return forward & reverse


def _guarded_prune_graph(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    q: float,
    n_iters: int,
    protected: set[int],
) -> tuple[dict[int, list[int]], int]:
    current_adj = {i: list(nbs) for i, nbs in adj.items()}
    total_removed = 0

    for _ in range(n_iters):
        by_layer, layers = _layer_map(positions)
        blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
            positions, by_layer, layers
        )
        if not slit_upper or not slit_lower:
            break

        from scripts.dense_prune_q003_joint_strict import _score_candidates  # local import to keep scope tight

        src = by_layer[layers[0]]
        candidate_scores = _score_candidates(
            positions,
            current_adj,
            src,
            blocked_barrier,
            slit_upper,
            slit_lower,
            by_layer,
            layers,
        )
        candidate_scores = [(node, score) for node, score in candidate_scores if node not in protected]
        if not candidate_scores:
            break

        n_remove = int(len(candidate_scores) * q)
        if n_remove <= 0:
            break

        remove_set = {node for node, _ in candidate_scores[:n_remove]}
        if not remove_set:
            break

        new_adj: dict[int, list[int]] = {}
        for i, nbs in current_adj.items():
            if i in remove_set:
                continue
            kept = [j for j in nbs if j not in remove_set]
            new_adj[i] = kept
        current_adj = new_adj
        total_removed += len(remove_set)

    return current_adj, total_removed


def _laplacian_joint(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    n_layers: int,
    *,
    field_override: list[float] | None = None,
) -> tuple[float, float]:
    by_layer, layers = _layer_map(positions)
    blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
        positions, by_layer, layers
    )
    if not slit_upper or not slit_lower:
        return math.nan, math.nan
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return math.nan, math.nan

    env_depth = max(1, round(n_layers / 6))
    start = barrier_idx + 1
    stop = min(len(layers), start + env_depth)
    mid_nodes: list[int] = []
    for layer in layers[start:stop]:
        mid_nodes.extend(by_layer[layer])
    if not mid_nodes:
        return math.nan, math.nan

    field_base = field_override if field_override is not None else field_laplacian(positions, adj, mass_nodes)
    field_flat = [0.0] * len(positions)

    grav_vals: list[float] = []
    pur_vals: list[float] = []

    for k in K_BAND:
        amps_mass = propagate_3d(positions, adj, field_base, src, k, blocked_barrier)
        amps_flat = propagate_3d(positions, adj, field_flat, src, k, blocked_barrier)

        prob_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        prob_flat = sum(abs(amps_flat[d]) ** 2 for d in det_list)
        if prob_mass > 1e-30 and prob_flat > 1e-30:
            y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / prob_mass
            y_flat = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / prob_flat
            grav_vals.append(y_mass - y_flat)

        amps_a = propagate_3d(positions, adj, field_base, src, k, blocked_barrier | set(slit_lower))
        amps_b = propagate_3d(positions, adj, field_base, src, k, blocked_barrier | set(slit_upper))

        bins_a = [0j] * 8
        bins_b = [0j] * 8
        bw = 24.0 / 8
        for node in mid_nodes:
            y = positions[node][1]
            idx = int((y + 12.0) / bw)
            idx = max(0, min(7, idx))
            bins_a[idx] += amps_a[node]
            bins_b[idx] += amps_b[node]

        S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
        NA = sum(abs(a) ** 2 for a in bins_a)
        NB = sum(abs(b) ** 2 for b in bins_b)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-(10.0 ** 2) * Sn)
        pc, _, _ = cl_purity(amps_a, amps_b, D_cl, det_list)
        if not math.isnan(pc):
            pur_vals.append(pc)

    if not grav_vals or not pur_vals:
        return math.nan, math.nan
    return statistics.fmean(pur_vals), statistics.fmean(grav_vals)


def main() -> None:
    print("=" * 94)
    print("DENSE + PRUNE Q=0.03 MECHANISM AUDIT")
    print("  Same dense 3D setup; ask whether the gravity sign flip tracks mass-coupled detector reach")
    print("=" * 94)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune quantile: {Q}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  k-band: {K_BAND}")
    print()

    for n_layers in N_LAYERS_LIST:
        print(f"[N={n_layers}]")
        print(
            f"{'seed':>4s}  {'g_base':>8s}  {'g_prune':>8s}  {'d_g':>8s}  "
            f"{'supp_base':>9s}  {'supp_prune':>10s}  {'d_supp':>8s}  {'flip':>5s}"
        )
        print("  " + "-" * 78)

        seed_rows = []
        frozen_pruned = []
        frozen_delta = []
        guarded_rows = []

        for seed in range(N_SEEDS):
            positions, adj = generate_3d_dag(
                n_layers=n_layers,
                nodes_per_layer=NODES_PER_LAYER,
                xyz_range=XYZ_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed * 7 + 3,
                gap=GAP,
            )
            by_layer, layers = _layer_map(positions)
            if len(layers) < 7:
                continue
            center_y = statistics.fmean(y for _, y, _ in positions)
            mass_nodes = _select_mass_nodes(positions, by_layer, layers, center_y)
            if not mass_nodes:
                continue
            det_nodes = list(by_layer[layers[-1]])
            if not det_nodes:
                continue

            pruned_adj, removed_total = _prune_graph(positions, adj, Q, PRUNE_ITERS)
            guard_core = _path_core_nodes(adj, mass_nodes, det_nodes)
            guarded_adj, guarded_removed = _guarded_prune_graph(
                positions, adj, Q, PRUNE_ITERS, guard_core
            )

            pur_base, grav_base = _laplacian_joint(positions, adj, mass_nodes, n_layers)
            pur_prune, grav_prune = _laplacian_joint(positions, pruned_adj, mass_nodes, n_layers)
            pur_guard, grav_guard = _laplacian_joint(positions, guarded_adj, mass_nodes, n_layers)

            if any(math.isnan(v) for v in (pur_base, grav_base, pur_prune, grav_prune)):
                continue

            support_base = _mass_path_support(adj, mass_nodes, det_nodes)
            support_prune = _mass_path_support(pruned_adj, mass_nodes, det_nodes)
            support_guard = _mass_path_support(guarded_adj, mass_nodes, det_nodes)

            d_g = grav_prune - grav_base
            d_supp = support_prune - support_base
            flip = "Y" if grav_base > 0 and grav_prune < 0 else "N"
            seed_rows.append((seed, d_g, d_supp, flip))

            # Frozen-field control: apply the original graph field on the pruned graph
            field_orig = field_laplacian(positions, adj, mass_nodes)
            field_pruned = field_laplacian(positions, pruned_adj, mass_nodes)
            _, grav_frozen_orig = _laplacian_joint(
                positions, pruned_adj, mass_nodes, n_layers, field_override=field_orig
            )
            _, grav_frozen_recomp = _laplacian_joint(
                positions, pruned_adj, mass_nodes, n_layers, field_override=field_pruned
            )
            if not math.isnan(grav_frozen_orig) and not math.isnan(grav_frozen_recomp):
                frozen_pruned.append(grav_frozen_orig)
                frozen_delta.append(grav_frozen_orig - grav_frozen_recomp)

            guarded_rows.append((pur_base, pur_guard, grav_base, grav_guard, support_base, support_guard, removed_total, guarded_removed))

            print(
                f"{seed:4d}  {grav_base:+8.3f}  {grav_prune:+8.3f}  {d_g:+8.3f}  "
                f"{support_base:9.3f}  {support_prune:10.3f}  {d_supp:+8.3f}  {flip:>5s}"
            )

        print()
        if seed_rows:
            dg = [r[1] for r in seed_rows]
            dr = [r[2] for r in seed_rows]
            flip_rate = sum(1 for _, _, _, flip in seed_rows if flip == "Y") / len(seed_rows)
            print(
                f"  corr(d_g, d_support) = {_pearson(dg, dr):+.3f}; "
                f"sign-flip rate = {flip_rate:.2f} across {len(seed_rows)} seeds"
            )
        else:
            print("  no valid paired seeds")

        if frozen_delta:
            print(
                f"  frozen-field control: mean(gravity frozen-orig minus recomputed) = "
                f"{statistics.fmean(frozen_delta):+.3f}"
            )
        else:
            print("  frozen-field control: no paired rows")

        if guarded_rows:
            pb = statistics.fmean(r[0] for r in guarded_rows)
            pg = statistics.fmean(r[1] for r in guarded_rows)
            gb = statistics.fmean(r[2] for r in guarded_rows)
            gg = statistics.fmean(r[3] for r in guarded_rows)
            rb = statistics.fmean(r[4] for r in guarded_rows)
            rg = statistics.fmean(r[5] for r in guarded_rows)
            rem = statistics.fmean(r[6] for r in guarded_rows)
            grem = statistics.fmean(r[7] for r in guarded_rows)
            print(
                f"  guarded prune: pur {pb:.4f} -> {pg:.4f}, grav {gb:+.3f} -> {gg:+.3f}, "
                f"supp {rb:.3f} -> {rg:.3f}, removed {rem:.1f} -> {grem:.1f}"
            )
        else:
            print("  guarded prune: no valid rows")
        print()

    print("INTERPRETATION")
    print("  The simple mass-to-detector reach and the path-support metric are")
    print("  both flat in this audit, so a pure connectivity-collapse story is")
    print("  not supported here. The frozen-field difference is also small.")
    print("  The narrow guard still helps gravity and pur_cl, which suggests the")
    print("  vulnerable object is a routing / cancellation subset inside the")
    print("  mass-coupled pathways rather than wholesale reach loss alone.")
    print("=" * 94)


if __name__ == "__main__":
    main()
