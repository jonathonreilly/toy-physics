#!/usr/bin/env python3
"""Weighted-flow audit for the dense-prune gravity fragility.

The coarse reach/core audits answered one question: pruning does not appear to
cause the gravity sign flip by simply collapsing detector reach.

This script asks the next narrower question:
  - does the flip line up better with weighted mass-coupled flow, or with
    cancellation inside the surviving detector-side paths?

We keep the exact same dense 3D same-graph setup used by the strict dense-prune
joint and mechanism scripts. For each seed and prune setting we compare:
  - gravity shift baseline vs pruned
  - coarse mass-to-detector reach and path-core support
  - weighted mass-flow to detectors
  - detector-side flow balance / cancellation
  - flow centroid on the detector layer

The target is not a rescue claim. The target is to see which weighted diagnostic
tracks the gravity fragility better than the coarse reach proxy did.

PStack experiment: dense-prune-weighted-flow-audit
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
from scripts.dense_prune_q003_mechanism_audit import (  # type: ignore  # noqa: E402
    _mass_to_detector_reach,
    _path_core_nodes,
)
from scripts.three_d_joint_test import generate_3d_dag  # type: ignore  # noqa: E402


Q_LIST = (0.03, 0.10)
PRUNE_ITERS = 1
FIXED_MASS_COUNT = 8
FIXED_B_OFFSET = 3.0


@dataclass(frozen=True)
class Summary:
    q: float
    n_layers: int
    grav_base: float
    grav_pruned: float
    pur_base: float
    pur_pruned: float
    reach_base: float
    reach_pruned: float
    core_base: float
    core_pruned: float
    flow_base: float
    flow_pruned: float
    balance_base: float
    balance_pruned: float
    centroid_base: float
    centroid_pruned: float
    removed_total: int
    flip_count: int

    @property
    def grav_delta(self) -> float:
        return self.grav_pruned - self.grav_base

    @property
    def pur_delta(self) -> float:
        return self.pur_pruned - self.pur_base

    @property
    def reach_delta(self) -> float:
        return self.reach_pruned - self.reach_base

    @property
    def core_delta(self) -> float:
        return self.core_pruned - self.core_base

    @property
    def flow_delta(self) -> float:
        return self.flow_pruned - self.flow_base

    @property
    def balance_delta(self) -> float:
        return self.balance_pruned - self.balance_base

    @property
    def centroid_delta(self) -> float:
        return self.centroid_pruned - self.centroid_base


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _mean_se_t(vals: list[float]) -> tuple[float, float, float]:
    mean = statistics.fmean(vals)
    if len(vals) > 1:
        se = statistics.stdev(vals) / math.sqrt(len(vals))
    else:
        se = 0.0
    t = mean / se if se > 1e-30 else math.nan
    return mean, se, t


def _pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(ys) < 2:
        return math.nan
    xm = statistics.fmean(xs)
    ym = statistics.fmean(ys)
    num = sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - xm) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - ym) ** 2 for y in ys))
    if den_x <= 1e-30 or den_y <= 1e-30:
        return math.nan
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


def _flow_profile(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
) -> tuple[float, float, float, float]:
    """Propagate unit mass flow through the DAG and summarize detector support.

    The flow is a simple out-degree-split provenance model:
    each mass node starts with unit flow and divides its flow equally among
    outgoing edges. This gives a weighted mass-coupled support profile that can
    change even when raw reach stays flat.
    """
    n = len(positions)
    order = _topo_order(adj, n)
    flow = [0.0] * n
    if mass_nodes:
        share = 1.0 / len(mass_nodes)
        for m in mass_nodes:
            flow[m] += share

    for i in order:
        out = adj.get(i, [])
        if not out or flow[i] <= 1e-30:
            continue
        share = flow[i] / len(out)
        for j in out:
            flow[j] += share

    det_set = set(det_nodes)
    det_flows = [flow[d] for d in det_nodes if d in det_set]
    total = sum(det_flows)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0, 0.0

    center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
    upper = sum(flow[d] for d in det_nodes if positions[d][1] >= center_y)
    lower = sum(flow[d] for d in det_nodes if positions[d][1] < center_y)
    centroid = sum(flow[d] * positions[d][1] for d in det_nodes) / total
    balance = (upper - lower) / (upper + lower) if (upper + lower) > 1e-30 else 0.0
    return total, balance, centroid, upper + lower


def _path_metrics(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
) -> tuple[float, float]:
    """Return the coarse core-support proxy and detector reach fraction."""
    by_layer, layers = _layer_map(positions)
    post_nodes = [
        i
        for layer in layers[len(layers) // 3 + 1 : -1]
        for i in by_layer[layer]
    ]
    if not post_nodes:
        return 0.0, 0.0

    core_nodes = _path_core_nodes(adj, mass_nodes, det_nodes)
    reach_frac, _ = _mass_to_detector_reach(adj, mass_nodes, det_nodes)
    core_frac = len(core_nodes) / len(post_nodes)
    return core_frac, reach_frac


def _seed_summary(n_layers: int, seed: int, q: float) -> Summary | None:
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

    pruned_adj, removed_total = _prune_graph(positions, adj, q, PRUNE_ITERS)

    pur_base, grav_base, _ = _joint_summary(positions, adj, mass_nodes, n_layers)
    pur_pruned, grav_pruned, _ = _joint_summary(positions, pruned_adj, mass_nodes, n_layers)
    if any(math.isnan(v) for v in (pur_base, grav_base, pur_pruned, grav_pruned)):
        return None

    core_base, reach_base = _path_metrics(positions, adj, mass_nodes, det_nodes)
    core_pruned, reach_pruned = _path_metrics(positions, pruned_adj, mass_nodes, det_nodes)
    flow_base, balance_base, centroid_base, _ = _flow_profile(positions, adj, mass_nodes, det_nodes)
    flow_pruned, balance_pruned, centroid_pruned, _ = _flow_profile(positions, pruned_adj, mass_nodes, det_nodes)
    flip_count = 1 if grav_base > 0 and grav_pruned < 0 else 0

    return Summary(
        q=q,
        n_layers=n_layers,
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        reach_base=reach_base,
        reach_pruned=reach_pruned,
        core_base=core_base,
        core_pruned=core_pruned,
        flow_base=flow_base,
        flow_pruned=flow_pruned,
        balance_base=balance_base,
        balance_pruned=balance_pruned,
        centroid_base=centroid_base,
        centroid_pruned=centroid_pruned,
        removed_total=removed_total,
        flip_count=flip_count,
    )


def _print_table(rows: list[Summary], n_layers: int, q: float) -> None:
    if not rows:
        print(f"{n_layers:4d}  {q:4.2f}  {'0':>5s}  {'NA':>8s}  {'NA':>8s}  {'NA':>8s}")
        return

    grav_base = statistics.fmean(r.grav_base for r in rows)
    grav_pruned = statistics.fmean(r.grav_pruned for r in rows)
    pur_base = statistics.fmean(r.pur_base for r in rows)
    pur_pruned = statistics.fmean(r.pur_pruned for r in rows)
    reach_base = statistics.fmean(r.reach_base for r in rows)
    reach_pruned = statistics.fmean(r.reach_pruned for r in rows)
    core_base = statistics.fmean(r.core_base for r in rows)
    core_pruned = statistics.fmean(r.core_pruned for r in rows)
    flow_base = statistics.fmean(r.flow_base for r in rows)
    flow_pruned = statistics.fmean(r.flow_pruned for r in rows)
    bal_base = statistics.fmean(r.balance_base for r in rows)
    bal_pruned = statistics.fmean(r.balance_pruned for r in rows)
    cen_base = statistics.fmean(r.centroid_base for r in rows)
    cen_pruned = statistics.fmean(r.centroid_pruned for r in rows)
    removed = statistics.fmean(r.removed_total for r in rows)
    flips = sum(r.flip_count for r in rows)

    grav_deltas = [r.grav_delta for r in rows]
    reach_deltas = [r.reach_delta for r in rows]
    core_deltas = [r.core_delta for r in rows]
    flow_deltas = [r.flow_delta for r in rows]
    bal_deltas = [r.balance_delta for r in rows]
    cen_deltas = [r.centroid_delta for r in rows]
    pur_deltas = [r.pur_delta for r in rows]

    pur_mean, pur_se, pur_t = _mean_se_t(pur_deltas)
    grav_mean, grav_se, grav_t = _mean_se_t(grav_deltas)

    corr_reach = _pearson(grav_deltas, reach_deltas)
    corr_core = _pearson(grav_deltas, core_deltas)
    corr_flow = _pearson(grav_deltas, flow_deltas)
    corr_bal = _pearson(grav_deltas, bal_deltas)
    corr_cen = _pearson(grav_deltas, cen_deltas)

    print(
        f"{n_layers:4d}  {q:4.2f}  {len(rows):5d}  "
        f"{pur_base:8.4f}  {pur_pruned:8.4f}  {pur_mean:+8.4f}  "
        f"{grav_base:+8.4f}  {grav_pruned:+8.4f}  {grav_mean:+8.4f}  "
        f"{pur_se:7.4f}  {grav_se:7.4f}  {removed:7.1f}  {flips:5d}"
    )

    print(
        f"      coarse reach/core   = {reach_base:.4f} -> {reach_pruned:.4f} | "
        f"{core_base:.4f} -> {core_pruned:.4f}"
    )
    print(
        f"      weighted flow       = {flow_base:.4f} -> {flow_pruned:.4f} | "
        f"balance {bal_base:+.4f} -> {bal_pruned:+.4f} | "
        f"centroid {cen_base:+.4f} -> {cen_pruned:+.4f}"
    )
    print(
        f"      corr(delta_grav, d_reach)={corr_reach:+.3f}, "
        f"corr(..., d_core)={corr_core:+.3f}, "
        f"corr(..., d_flow)={corr_flow:+.3f}, "
        f"corr(..., d_balance)={corr_bal:+.3f}, "
        f"corr(..., d_centroid)={corr_cen:+.3f}"
    )
    print(
        f"      pur_t={pur_t:+.2f}, grav_t={grav_t:+.2f}, "
        f"flip_rate={flips}/{len(rows)}"
    )


def main() -> None:
    print("=" * 100)
    print("DENSE + PRUNE WEIGHTED FLOW AUDIT")
    print("  Same dense 3D same-graph setup; compare coarse reach vs weighted mass-coupled flow")
    print("=" * 100)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  fixed mass count: {FIXED_MASS_COUNT}")
    print(f"  fixed b offset: {FIXED_B_OFFSET}")
    print(f"  k-band: {K_BAND}")
    print()
    print(
        f"{'N':>4s}  {'q':>4s}  {'valid':>5s}  {'pur_b':>8s}  {'pur_p':>8s}  "
        f"{'d_pur':>8s}  {'grav_b':>8s}  {'grav_p':>8s}  {'d_grav':>8s}  "
        f"{'pur_SE':>7s}  {'grav_SE':>7s}  {'removed':>7s}  {'flip':>5s}"
    )
    print("-" * 100)

    strongest = None
    for n_layers in N_LAYERS_LIST:
        for q in Q_LIST:
            rows: list[Summary] = []
            for seed in range(N_SEEDS):
                row = _seed_summary(n_layers, seed, q)
                if row is not None:
                    rows.append(row)
            _print_table(rows, n_layers, q)

            if rows:
                grav_deltas = [r.grav_delta for r in rows]
                flow_deltas = [r.flow_delta for r in rows]
                bal_deltas = [r.balance_delta for r in rows]
                cen_deltas = [r.centroid_delta for r in rows]
                corr_flow = abs(_pearson(grav_deltas, flow_deltas))
                corr_bal = abs(_pearson(grav_deltas, bal_deltas))
                corr_cen = abs(_pearson(grav_deltas, cen_deltas))
                score = max(corr_flow, corr_bal, corr_cen)
                candidate = (score, n_layers, q, corr_flow, corr_bal, corr_cen, rows)
                if strongest is None or candidate[0] > strongest[0]:
                    strongest = candidate
            print()

    print("=" * 100)
    if strongest is None:
        print("NO STABLE ROWS")
        print("  The weighted-flow audit did not produce valid paired rows.")
    else:
        score, n_layers, q, corr_flow, corr_bal, corr_cen, rows = strongest
        print("STRONGEST DIAGNOSTIC")
        print(
            f"  N={n_layers}, q={q:.2f}: strongest abs(corr)={score:.3f} "
            f"(flow={corr_flow:.3f}, balance={corr_bal:.3f}, centroid={corr_cen:.3f})"
        )
        if corr_bal >= corr_flow and corr_bal >= corr_cen:
            print("  balance/cancellation tracks the gravity delta best in this audit.")
        elif corr_flow >= corr_cen:
            print("  weighted detector flow tracks the gravity delta best in this audit.")
        else:
            print("  detector centroid tracks the gravity delta best in this audit.")
        print("  This is a diagnostic only; it does not solve the gravity fragility.")
    print("=" * 100)


if __name__ == "__main__":
    main()
