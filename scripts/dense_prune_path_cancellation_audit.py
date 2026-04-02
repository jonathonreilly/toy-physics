#!/usr/bin/env python3
"""Path-resolved cancellation audit for the dense-prune gravity fragility.

The coarse reach/core audits and the weighted-flow proxy both stayed too flat
to explain why pruning sometimes flips the gravity signal while leaving the
decoherence gain intact.

This script asks a narrower question:
  - do detector-channel cancellation and skew metrics move with the gravity
    delta better than raw reach/core or weighted-flow proxies do?

We keep the exact same dense 3D same-graph setup used by the strict dense-
prune joint and mechanism scripts. For each seed and prune setting we measure:
  - baseline vs pruned gravity and pur_cl
  - coarse mass reach/core support
  - path-resolved detector-channel cancellation
  - detector-channel skew
  - effective detector channel count from the absolute delta-probability mass

The target is not a rescue claim. The target is to find whether any
path-resolved cancellation diagnostic tracks the gravity delta materially
better than the earlier weighted-flow audit.

PStack experiment: dense-prune-path-cancellation-audit
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
    PRUNE_ITERS,
    PRUNE_Q,
    _barrier_slices,
    _joint_summary,
    _layer_map,
    _prune_graph,
    _select_mass_nodes,
)
from scripts.dense_prune_q003_mechanism_audit import (  # type: ignore  # noqa: E402
    _mass_path_support,
    _mass_to_detector_reach,
    _path_core_nodes,
)
from scripts.causal_field_mass_scaling import field_laplacian  # type: ignore  # noqa: E402
from scripts.three_d_joint_test import (  # type: ignore  # noqa: E402
    cl_purity,
    generate_3d_dag,
    propagate_3d,
)


Q_LIST = (0.03, 0.10)


@dataclass(frozen=True)
class SeedRow:
    grav_base: float
    grav_pruned: float
    pur_base: float
    pur_pruned: float
    reach_base: float
    reach_pruned: float
    core_base: float
    core_pruned: float
    cancel_base: float
    cancel_pruned: float
    skew_base: float
    skew_pruned: float
    channel_eff_base: float
    channel_eff_pruned: float
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
    def cancel_delta(self) -> float:
        return self.cancel_pruned - self.cancel_base

    @property
    def skew_delta(self) -> float:
        return self.skew_pruned - self.skew_base

    @property
    def channel_eff_delta(self) -> float:
        return self.channel_eff_pruned - self.channel_eff_base


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


def _mean_se_t(vals: list[float]) -> tuple[float, float, float]:
    mean = statistics.fmean(vals)
    if len(vals) > 1:
        se = statistics.stdev(vals) / math.sqrt(len(vals))
    else:
        se = 0.0
    t = mean / se if se > 1e-30 else math.nan
    return mean, se, t


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


def _path_metrics(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
) -> tuple[float, float]:
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


def _channel_metrics(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    mass_nodes: list[int],
    det_nodes: list[int],
    blocked: set[int],
) -> tuple[float, float, float]:
    """Average detector-channel cancellation, skew, and effective channel count."""
    by_layer, layers = _layer_map(positions)
    center_y = statistics.fmean(y for _, y, _ in positions)
    field_mass = field_laplacian(positions, adj, mass_nodes)
    field_flat = [0.0] * len(positions)

    cancel_vals: list[float] = []
    skew_vals: list[float] = []
    eff_vals: list[float] = []

    for k in K_BAND:
        amps_mass = propagate_3d(positions, adj, field_mass, src, k, blocked)
        amps_flat = propagate_3d(positions, adj, field_flat, src, k, blocked)

        delta = []
        for d in det_nodes:
            pm = abs(amps_mass[d]) ** 2
            pf = abs(amps_flat[d]) ** 2
            delta.append((pm - pf, positions[d][1] - center_y))

        signed = [dp * dy for dp, dy in delta]
        if not signed:
            continue
        net = sum(signed)
        abs_net = sum(abs(v) for v in signed)
        if abs_net <= 1e-30:
            cancel_vals.append(0.0)
        else:
            cancel_vals.append(1.0 - min(1.0, abs(net) / abs_net))

        upper = sum(dp for dp, dy in delta if dy >= 0)
        lower = sum(dp for dp, dy in delta if dy < 0)
        denom = abs(upper) + abs(lower)
        skew_vals.append((upper - lower) / denom if denom > 1e-30 else 0.0)

        weights = [abs(v) for v in signed]
        wsum = sum(weights)
        if wsum > 1e-30:
            probs = [w / wsum for w in weights]
            entropy = -sum(p * math.log(p) for p in probs if p > 1e-30)
            eff_vals.append(math.exp(entropy))
        else:
            eff_vals.append(0.0)

    if not cancel_vals:
        return 0.0, 0.0, 0.0
    return statistics.fmean(cancel_vals), statistics.fmean(skew_vals), statistics.fmean(eff_vals)


def _seed_summary(n_layers: int, seed: int, q: float) -> SeedRow | None:
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
    src = list(by_layer[layers[0]])

    pruned_adj, removed_total = _prune_graph(positions, adj, q, PRUNE_ITERS)

    pur_base, grav_base, _ = _joint_summary(positions, adj, mass_nodes, n_layers)
    pur_pruned, grav_pruned, _ = _joint_summary(positions, pruned_adj, mass_nodes, n_layers)
    if any(math.isnan(v) for v in (pur_base, grav_base, pur_pruned, grav_pruned)):
        return None

    core_base, reach_base = _path_metrics(positions, adj, mass_nodes, det_nodes)
    core_pruned, reach_pruned = _path_metrics(positions, pruned_adj, mass_nodes, det_nodes)

    blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
        positions, by_layer, layers
    )
    if not slit_upper or not slit_lower:
        return None

    cancel_base, skew_base, eff_base = _channel_metrics(
        positions, adj, src, mass_nodes, det_nodes, blocked_barrier
    )
    cancel_pruned, skew_pruned, eff_pruned = _channel_metrics(
        positions, pruned_adj, src, mass_nodes, det_nodes, blocked_barrier
    )
    flip_count = 1 if grav_base > 0 and grav_pruned < 0 else 0

    return SeedRow(
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        reach_base=reach_base,
        reach_pruned=reach_pruned,
        core_base=core_base,
        core_pruned=core_pruned,
        cancel_base=cancel_base,
        cancel_pruned=cancel_pruned,
        skew_base=skew_base,
        skew_pruned=skew_pruned,
        channel_eff_base=eff_base,
        channel_eff_pruned=eff_pruned,
        removed_total=removed_total,
        flip_count=flip_count,
    )


def _print_table(rows: list[SeedRow], n_layers: int, q: float) -> None:
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
    cancel_base = statistics.fmean(r.cancel_base for r in rows)
    cancel_pruned = statistics.fmean(r.cancel_pruned for r in rows)
    skew_base = statistics.fmean(r.skew_base for r in rows)
    skew_pruned = statistics.fmean(r.skew_pruned for r in rows)
    eff_base = statistics.fmean(r.channel_eff_base for r in rows)
    eff_pruned = statistics.fmean(r.channel_eff_pruned for r in rows)
    removed = statistics.fmean(r.removed_total for r in rows)
    flips = sum(r.flip_count for r in rows)

    grav_deltas = [r.grav_delta for r in rows]
    reach_deltas = [r.reach_delta for r in rows]
    core_deltas = [r.core_delta for r in rows]
    cancel_deltas = [r.cancel_delta for r in rows]
    skew_deltas = [r.skew_delta for r in rows]
    eff_deltas = [r.channel_eff_delta for r in rows]
    pur_deltas = [r.pur_delta for r in rows]

    pur_mean, pur_se, pur_t = _mean_se_t(pur_deltas)
    grav_mean, grav_se, grav_t = _mean_se_t(grav_deltas)

    corr_reach = _pearson(grav_deltas, reach_deltas)
    corr_core = _pearson(grav_deltas, core_deltas)
    corr_cancel = _pearson(grav_deltas, cancel_deltas)
    corr_skew = _pearson(grav_deltas, skew_deltas)
    corr_eff = _pearson(grav_deltas, eff_deltas)

    print(
        f"{n_layers:4d}  {q:4.2f}  {len(rows):5d}  "
        f"{pur_base:8.4f}  {pur_pruned:8.4f}  {pur_mean:+8.4f}  "
        f"{grav_base:+8.4f}  {grav_pruned:+8.4f}  {grav_mean:+8.4f}  "
        f"{pur_se:7.4f}  {grav_se:7.4f}  {removed:7.1f}  {flips:5d}"
    )

    print(
        f"      reach/core      = {reach_base:.4f} -> {reach_pruned:.4f} | "
        f"{core_base:.4f} -> {core_pruned:.4f}"
    )
    print(
        f"      cancellation    = {cancel_base:.4f} -> {cancel_pruned:.4f} | "
        f"skew {skew_base:+.4f} -> {skew_pruned:+.4f} | "
        f"eff_ch {eff_base:.3f} -> {eff_pruned:.3f}"
    )
    print(
        f"      corr(delta_grav, d_reach)={corr_reach:+.3f}, "
        f"corr(..., d_core)={corr_core:+.3f}, "
        f"corr(..., d_cancel)={corr_cancel:+.3f}, "
        f"corr(..., d_skew)={corr_skew:+.3f}, "
        f"corr(..., d_eff)={corr_eff:+.3f}"
    )
    print(
        f"      pur_t={pur_t:+.2f}, grav_t={grav_t:+.2f}, "
        f"flip_rate={flips}/{len(rows)}"
    )


def main() -> None:
    print("=" * 100)
    print("DENSE + PRUNE PATH CANCELLATION AUDIT")
    print("  Same dense 3D same-graph setup; compare coarse reach/core vs path-resolved cancellation")
    print("=" * 100)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune iterations: {PRUNE_ITERS}")
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
            rows: list[SeedRow] = []
            for seed in range(N_SEEDS):
                row = _seed_summary(n_layers, seed, q)
                if row is not None:
                    rows.append(row)
            _print_table(rows, n_layers, q)

            if rows:
                grav_deltas = [r.grav_delta for r in rows]
                cancel_deltas = [r.cancel_delta for r in rows]
                skew_deltas = [r.skew_delta for r in rows]
                eff_deltas = [r.channel_eff_delta for r in rows]
                corr_cancel = abs(_pearson(grav_deltas, cancel_deltas))
                corr_skew = abs(_pearson(grav_deltas, skew_deltas))
                corr_eff = abs(_pearson(grav_deltas, eff_deltas))
                score = max(corr_cancel, corr_skew, corr_eff)
                candidate = (score, n_layers, q, corr_cancel, corr_skew, corr_eff, rows)
                if strongest is None or candidate[0] > strongest[0]:
                    strongest = candidate
            print()

    print("=" * 100)
    if strongest is None:
        print("NO STABLE ROWS")
        print("  The path-cancellation audit did not produce valid paired rows.")
    else:
        score, n_layers, q, corr_cancel, corr_skew, corr_eff, rows = strongest
        print("STRONGEST DIAGNOSTIC")
        print(
            f"  N={n_layers}, q={q:.2f}: strongest abs(corr)={score:.3f} "
            f"(cancel={corr_cancel:.3f}, skew={corr_skew:.3f}, eff={corr_eff:.3f})"
        )
        if corr_cancel >= corr_skew and corr_cancel >= corr_eff:
            print("  cancellation tracks the gravity delta best in this audit.")
        elif corr_skew >= corr_eff:
            print("  detector-channel skew tracks the gravity delta best in this audit.")
        else:
            print("  effective detector-channel count tracks the gravity delta best in this audit.")
        print("  This is a diagnostic only; it does not solve the gravity fragility.")
    print("=" * 100)


if __name__ == "__main__":
    main()
