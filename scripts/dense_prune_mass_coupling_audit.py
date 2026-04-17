#!/usr/bin/env python3
"""Mass-coupling audit for the q=0.03 dense-prune gravity sign flip.

The hypothesis under test is narrow:
pruning may flip the gravity read not because it merely lowers detector reach,
but because it removes the mass-coupled channels that actually carry phase
perturbations from the mass neighborhood to the detector.

We use the same dense 3D same-graph setup as the q=0.03 joint controls and
measure, per seed:
  1. baseline vs pruned gravity/purity on the same graph instance
  2. mass-conditioned detector reach and path-support before/after prune
  3. a mass-source detector-amplitude proxy before/after prune
  4. a frozen-field control on the pruned graph to separate field distortion
     from graph-connectivity loss

PStack experiment: dense-prune-mass-coupling-audit
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict, deque
from dataclasses import dataclass

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
    PRUNE_ITERS,
    PRUNE_Q,
    _barrier_slices,
    _layer_map,
    _prune_graph,
    _select_mass_nodes,
)
from scripts.three_d_joint_test import (  # type: ignore  # noqa: E402
    cl_purity,
    generate_3d_dag,
    propagate_3d,
)


@dataclass(frozen=True)
class SeedAudit:
    pur_base: float
    pur_pruned: float
    grav_base: float
    grav_pruned: float
    grav_pruned_frozen: float
    reach_base: float
    reach_pruned: float
    support_base: float
    support_pruned: float
    launch_base: float
    launch_pruned: float
    removed_total: int

    @property
    def grav_delta(self) -> float:
        return self.grav_pruned - self.grav_base

    @property
    def reach_delta(self) -> float:
        return self.reach_pruned - self.reach_base

    @property
    def support_delta(self) -> float:
        return self.support_pruned - self.support_base

    @property
    def launch_delta(self) -> float:
        return self.launch_pruned - self.launch_base


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
            if 0 <= j < n:
                in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            if 0 <= j < n:
                in_deg[j] -= 1
                if in_deg[j] == 0:
                    q.append(j)
    return order


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


def _mass_to_detector_reach(
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
) -> tuple[float, set[int]]:
    """Fraction of detectors reachable from the mass neighborhood."""
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


def _mass_path_support(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
) -> float:
    """Mean log1p path count from mass nodes to detector nodes.

    This is a lightweight support proxy: if pruning keeps detector reach but
    thins the mass-coupled channels, this value should drop.
    """
    n = len(positions)
    order = _topo_order(adj, n)
    counts = [0] * n
    for m in mass_nodes:
        counts[m] += 1
    for i in order:
        if counts[i] <= 0:
            continue
        for j in adj.get(i, []):
            if 0 <= j < n:
                counts[j] += counts[i]
    if not det_nodes:
        return 0.0
    return statistics.fmean(math.log1p(counts[d]) for d in det_nodes)


def _mass_launch_detector_prob(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
    blocked: set[int],
) -> float:
    """Average detector probability when the mass neighborhood is the source.

    This is a connectivity proxy, not a field-coupling proxy: the field is flat
    so any change comes from the graph geometry itself.
    """
    field_flat = [0.0] * len(positions)
    vals: list[float] = []
    for k in K_BAND:
        amps = propagate_3d(positions, adj, field_flat, mass_nodes, k, blocked)
        vals.append(sum(abs(amps[d]) ** 2 for d in det_nodes))
    prob = statistics.fmean(vals) if vals else float("nan")
    return math.log10(max(prob, 1e-300)) if not math.isnan(prob) else float("nan")


def _laplacian_joint(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    n_layers: int,
    *,
    field_override: list[float] | None = None,
) -> tuple[float, float]:
    """Return (pur_cl, gravity shift) on the same graph instance."""
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

    field_mass = field_override if field_override is not None else field_laplacian(positions, adj, mass_nodes)
    field_flat = [0.0] * len(positions)

    grav_vals: list[float] = []
    pur_vals: list[float] = []

    for k in K_BAND:
        amps_mass = propagate_3d(positions, adj, field_mass, src, k, blocked_barrier)
        amps_flat = propagate_3d(positions, adj, field_flat, src, k, blocked_barrier)

        prob_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        prob_flat = sum(abs(amps_flat[d]) ** 2 for d in det_list)
        if prob_mass > 1e-30 and prob_flat > 1e-30:
            y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / prob_mass
            y_flat = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / prob_flat
            grav_vals.append(y_mass - y_flat)

        amps_a = propagate_3d(positions, adj, field_mass, src, k, blocked_barrier | set(slit_lower))
        amps_b = propagate_3d(positions, adj, field_mass, src, k, blocked_barrier | set(slit_upper))

        bins_a = [0j] * 8
        bins_b = [0j] * 8
        bw = 24.0 / 8
        for node in mid_nodes:
            y = positions[node][1]
            idx = int((y + 12.0) / bw)
            idx = max(0, min(7, idx))
            bins_a[idx] += amps_a[node]
            bins_b[idx] += amps_b[node]

        s_val = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
        na = sum(abs(a) ** 2 for a in bins_a)
        nb = sum(abs(b) ** 2 for b in bins_b)
        sn = s_val / (na + nb) if (na + nb) > 0 else 0.0
        d_cl = math.exp(-(10.0**2) * sn)
        pc, _, _ = cl_purity(amps_a, amps_b, d_cl, det_list)
        if not math.isnan(pc):
            pur_vals.append(pc)

    if not grav_vals or not pur_vals:
        return math.nan, math.nan
    return statistics.fmean(pur_vals), statistics.fmean(grav_vals)


def _seed_audit(n_layers: int, seed: int) -> SeedAudit | None:
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
        return None

    center_y = statistics.fmean(y for _, y, _ in positions)
    mass_nodes = _select_mass_nodes(positions, by_layer, layers, center_y)
    if not mass_nodes:
        return None
    det_nodes = list(by_layer[layers[-1]])
    if not det_nodes:
        return None

    pruned_adj, removed_total = _prune_graph(positions, adj, PRUNE_Q, PRUNE_ITERS)

    pur_base, grav_base = _laplacian_joint(positions, adj, mass_nodes, n_layers)
    pur_pruned, grav_pruned = _laplacian_joint(positions, pruned_adj, mass_nodes, n_layers)
    if any(math.isnan(v) for v in (pur_base, grav_base, pur_pruned, grav_pruned)):
        return None

    field_base = field_laplacian(positions, adj, mass_nodes)
    field_pruned = field_laplacian(positions, pruned_adj, mass_nodes)
    _, grav_pruned_frozen = _laplacian_joint(
        positions, pruned_adj, mass_nodes, n_layers, field_override=field_base
    )
    if math.isnan(grav_pruned_frozen):
        return None

    reach_base, _ = _mass_to_detector_reach(adj, mass_nodes, det_nodes)
    reach_pruned, _ = _mass_to_detector_reach(pruned_adj, mass_nodes, det_nodes)
    support_base = _mass_path_support(positions, adj, mass_nodes, det_nodes)
    support_pruned = _mass_path_support(positions, pruned_adj, mass_nodes, det_nodes)
    launch_base = _mass_launch_detector_prob(
        positions, adj, mass_nodes, det_nodes, blocked=set()
    )
    launch_pruned = _mass_launch_detector_prob(
        positions, pruned_adj, mass_nodes, det_nodes, blocked=set()
    )

    return SeedAudit(
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        grav_pruned_frozen=grav_pruned_frozen,
        reach_base=reach_base,
        reach_pruned=reach_pruned,
        support_base=support_base,
        support_pruned=support_pruned,
        launch_base=launch_base,
        launch_pruned=launch_pruned,
        removed_total=removed_total,
    )


def main() -> None:
    print("=" * 100)
    print("DENSE + PRUNE MASS-COUPLING AUDIT")
    print("  Same dense 3D same-graph setup; test whether gravity flips track loss of")
    print("  mass-coupled detector support rather than detector reach alone.")
    print("=" * 100)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  gap: {GAP}")
    print(f"  prune quantile: {PRUNE_Q}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  k-band: {K_BAND}")
    print()

    for n_layers in N_LAYERS_LIST:
        print(f"[N={n_layers}]")
        print(
            f"{'seed':>4s}  {'g_base':>8s}  {'g_prune':>8s}  {'d_g':>8s}  "
            f"{'reach_b':>8s}  {'reach_p':>8s}  {'d_r':>8s}  "
            f"{'supp_b':>8s}  {'supp_p':>8s}  {'d_s':>8s}  "
            f"{'logL_b':>9s}  {'logL_p':>9s}  {'d_l':>8s}  {'flip':>5s}"
        )
        print("  " + "-" * 118)

        rows: list[SeedAudit] = []
        for seed in range(N_SEEDS):
            row = _seed_audit(n_layers, seed)
            if row is None:
                continue
            rows.append(row)
            flip = "Y" if row.grav_base > 0 and row.grav_pruned < 0 else "N"
            print(
                f"{seed:4d}  {row.grav_base:+8.3f}  {row.grav_pruned:+8.3f}  {row.grav_delta:+8.3f}  "
                f"{row.reach_base:8.3f}  {row.reach_pruned:8.3f}  {row.reach_delta:+8.3f}  "
                f"{row.support_base:8.3f}  {row.support_pruned:8.3f}  {row.support_delta:+8.3f}  "
                f"{row.launch_base:9.3f}  {row.launch_pruned:9.3f}  {row.launch_delta:+8.3f}  {flip:>5s}"
            )

        print()
        if not rows:
            print("  no valid paired seeds")
            print()
            continue

        grav_deltas = [r.grav_delta for r in rows]
        reach_deltas = [r.reach_delta for r in rows]
        support_deltas = [r.support_delta for r in rows]
        launch_deltas = [r.launch_delta for r in rows]
        frozen_gaps = [r.grav_pruned_frozen - r.grav_pruned for r in rows]
        flip_rate = sum(1 for r in rows if r.grav_base > 0 and r.grav_pruned < 0) / len(rows)

        print(
            f"  corr(d_g, d_reach)   = {_pearson(grav_deltas, reach_deltas):+.3f}"
        )
        print(
            f"  corr(d_g, d_support) = {_pearson(grav_deltas, support_deltas):+.3f}"
        )
        print(
            f"  corr(d_g, d_launch)  = {_pearson(grav_deltas, launch_deltas):+.3f}"
        )
        print(
            f"  mean frozen-minus-recomputed gravity on pruned graph = "
            f"{statistics.fmean(frozen_gaps):+.4f}"
        )
        print(f"  sign-flip rate = {flip_rate:.2f} across {len(rows)} paired seeds")
        print(
            f"  mean pur_cl base/pruned = "
            f"{statistics.fmean(r.pur_base for r in rows):.4f} / "
            f"{statistics.fmean(r.pur_pruned for r in rows):.4f}"
        )
        print(
            f"  mean gravity base/pruned = "
            f"{statistics.fmean(r.grav_base for r in rows):+.4f} / "
            f"{statistics.fmean(r.grav_pruned for r in rows):+.4f}"
        )
        print(
            f"  mean reach base/pruned = "
            f"{statistics.fmean(r.reach_base for r in rows):.4f} / "
            f"{statistics.fmean(r.reach_pruned for r in rows):.4f}"
        )
        print(
            f"  mean support base/pruned = "
            f"{statistics.fmean(r.support_base for r in rows):.4f} / "
            f"{statistics.fmean(r.support_pruned for r in rows):.4f}"
        )
        print(
            f"  mean launch log10-prob base/pruned = "
            f"{statistics.fmean(r.launch_base for r in rows):.4f} / "
            f"{statistics.fmean(r.launch_pruned for r in rows):.4f}"
        )
        print(
            f"  mean removed nodes = {statistics.fmean(r.removed_total for r in rows):.1f}"
        )
        print()

    print("INTERPRETATION")
    print(
        "  If gravity deltas correlate more tightly with the mass-coupled support "
        "proxies than with the frozen-field control gap, the sign flip is best "
        "explained by loss of mass-to-detector connectivity."
    )
    print(
        "  If the frozen-field control dominates, then pruning changes the field "
        "itself enough to matter. Keep the conclusion narrow either way."
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
