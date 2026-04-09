#!/usr/bin/env python3
"""Channel-count-preserving prune guard on the dense same-graph control.

The path-cancellation audit found that the gravity flip tracks an effective
detector channel count metric (`eff_ch`) much better than the coarse reach /
core proxies. This script tests a guard that preserves that channel count.

Guard policy
------------
For each pruning step we compute the tentative pruned graph and its
`eff_ch`. We accept the step only if:

  - `eff_ch` stays above an absolute floor, and
  - `eff_ch` does not drop by more than a bounded fraction from the
    current graph's channel count.

This is narrower than the earlier reach/core guards: the protected quantity
is the detector-channel support itself.

PStack experiment: dense-prune-channel-count-guard
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
    _barrier_slices,
    _joint_summary,
    _layer_map,
    _prune_graph,
    _score_candidates,
    _select_mass_nodes,
)
from scripts.three_d_joint_test import (  # type: ignore  # noqa: E402
    compute_field_3d,
    generate_3d_dag,
    propagate_3d,
)


Q_LIST = (0.03, 0.05, 0.10)
EFF_DROP_FRAC = 0.15
MIN_EFF_CH = 2.5


def _env_int_list(name: str, default: tuple[int, ...]) -> tuple[int, ...]:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    vals = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        vals.append(int(item))
    return tuple(vals) if vals else default


def _env_float_list(name: str, default: tuple[float, ...]) -> tuple[float, ...]:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    vals = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        vals.append(float(item))
    return tuple(vals) if vals else default


N_LAYERS_SWEEP = _env_int_list("DENSE_GUARD_LAYERS", N_LAYERS_LIST)
Q_SWEEP = _env_float_list("DENSE_GUARD_QS", Q_LIST)


@dataclass(frozen=True)
class Summary:
    q: float
    mode: str
    pur_base: float
    pur_pruned: float
    grav_base: float
    grav_pruned: float
    eff_base: float
    eff_pruned: float
    removed_total: int
    flip_count: int

    @property
    def pur_delta(self) -> float:
        return self.pur_pruned - self.pur_base

    @property
    def grav_delta(self) -> float:
        return self.grav_pruned - self.grav_base

    @property
    def eff_delta(self) -> float:
        return self.eff_pruned - self.eff_base


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


def _channel_eff(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    mass_nodes: list[int],
    det_nodes: list[int],
    blocked: set[int],
) -> float:
    """Average effective detector-channel count from the path-cancellation audit."""
    center_y = statistics.fmean(y for _, y, _ in positions)
    field_mass = compute_field_3d(positions, mass_nodes)
    field_flat = [0.0] * len(positions)

    eff_vals: list[float] = []
    for k in K_BAND:
        amps_mass = propagate_3d(positions, adj, field_mass, src, k, blocked)
        amps_flat = propagate_3d(positions, adj, field_flat, src, k, blocked)

        signed: list[float] = []
        for d in det_nodes:
            pm = abs(amps_mass[d]) ** 2
            pf = abs(amps_flat[d]) ** 2
            dy = positions[d][1] - center_y
            signed.append((pm - pf) * dy)

        weights = [abs(v) for v in signed]
        wsum = sum(weights)
        if wsum <= 1e-30:
            eff_vals.append(0.0)
            continue

        probs = [w / wsum for w in weights]
        entropy = -sum(p * math.log(p) for p in probs if p > 1e-30)
        eff_vals.append(math.exp(entropy))

    return statistics.fmean(eff_vals) if eff_vals else 0.0


def _guard_floor(current_eff: float) -> float:
    return max(MIN_EFF_CH, current_eff * (1.0 - EFF_DROP_FRAC))


def _guarded_prune_graph(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    q: float,
    n_iters: int,
    mass_nodes: list[int],
    det_nodes: list[int],
) -> tuple[dict[int, list[int]], int]:
    """Prune the bottom-q distinguishability nodes without dropping eff_ch too far."""
    current_adj = {i: list(nbs) for i, nbs in adj.items()}
    total_removed = 0

    def _apply_remove_set(remove_set: set[int]) -> dict[int, list[int]]:
        tentative_adj: dict[int, list[int]] = {}
        for i, nbs in current_adj.items():
            if i in remove_set:
                continue
            kept = [j for j in nbs if j not in remove_set]
            tentative_adj[i] = kept
        return tentative_adj

    for _ in range(n_iters):
        by_layer, layers = _layer_map(positions)
        blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
            positions, by_layer, layers
        )
        if not slit_upper or not slit_lower:
            break

        candidate_scores = _score_candidates(
            positions,
            current_adj,
            by_layer[layers[0]],
            blocked_barrier,
            slit_upper,
            slit_lower,
            by_layer,
            layers,
        )
        if not candidate_scores:
            break

        n_target = int(len(candidate_scores) * q)
        if n_target <= 0:
            break

        current_eff = _channel_eff(
            positions,
            current_adj,
            by_layer[layers[0]],
            mass_nodes,
            det_nodes,
            blocked_barrier,
        )
        floor = _guard_floor(current_eff)

        low = 0
        high = n_target
        accepted_adj: dict[int, list[int]] | None = None
        accepted_removed = 0

        # Binary search on the number of removable low-D nodes. eff_ch is
        # typically monotone enough in the prune count for this to be a good
        # bounded guard and much cheaper than scanning every intermediate count.
        while low <= high:
            n_remove = (low + high) // 2
            if n_remove <= 0:
                low = 1
                continue

            remove_set = {node for node, _ in candidate_scores[:n_remove]}
            tentative_adj = _apply_remove_set(remove_set)
            tentative_eff = _channel_eff(
                positions,
                tentative_adj,
                by_layer[layers[0]],
                mass_nodes,
                det_nodes,
                blocked_barrier,
            )
            if tentative_eff >= floor:
                accepted_adj = tentative_adj
                accepted_removed = len(remove_set)
                low = n_remove + 1
            else:
                high = n_remove - 1

        if accepted_adj is None:
            break

        current_adj = accepted_adj
        total_removed += accepted_removed

    return current_adj, total_removed


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
    guarded_adj, guarded_removed = _guarded_prune_graph(positions, adj, q, PRUNE_ITERS, mass_nodes, det_nodes)

    pur_base, grav_base, _ = _joint_summary(positions, adj, mass_nodes, n_layers)
    pur_pruned, grav_pruned, _ = _joint_summary(positions, guarded_adj, mass_nodes, n_layers)
    if any(math.isnan(v) for v in (pur_base, grav_base, pur_pruned, grav_pruned)):
        return None

    blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
        positions, by_layer, layers
    )
    if not slit_upper or not slit_lower:
        return None
    eff_base = _channel_eff(positions, adj, list(by_layer[layers[0]]), mass_nodes, det_nodes, blocked_barrier)
    eff_pruned = _channel_eff(
        positions,
        guarded_adj,
        list(by_layer[layers[0]]),
        mass_nodes,
        det_nodes,
        blocked_barrier,
    )

    flip_count = 1 if grav_base > 0 and grav_pruned < 0 else 0
    return Summary(
        q=q,
        mode="guarded",
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        eff_base=eff_base,
        eff_pruned=eff_pruned,
        removed_total=guarded_removed,
        flip_count=flip_count,
    )


def _plain_seed_summary(n_layers: int, seed: int, q: float) -> Summary | None:
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

    blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
        positions, by_layer, layers
    )
    if not slit_upper or not slit_lower:
        return None
    eff_base = _channel_eff(positions, adj, list(by_layer[layers[0]]), mass_nodes, det_nodes, blocked_barrier)
    eff_pruned = _channel_eff(
        positions,
        pruned_adj,
        list(by_layer[layers[0]]),
        mass_nodes,
        det_nodes,
        blocked_barrier,
    )

    flip_count = 1 if grav_base > 0 and grav_pruned < 0 else 0
    return Summary(
        q=q,
        mode="plain",
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        eff_base=eff_base,
        eff_pruned=eff_pruned,
        removed_total=removed_total,
        flip_count=flip_count,
    )


def _print_rows(rows: list[Summary], n_layers: int, q: float, mode: str) -> None:
    if not rows:
        print(f"{n_layers:4d}  {mode:>8s}  {q:4.2f}  {'0':>5s}  {'NA':>8s}  {'NA':>8s}")
        return

    pur_base = statistics.fmean(r.pur_base for r in rows)
    pur_pruned = statistics.fmean(r.pur_pruned for r in rows)
    grav_base = statistics.fmean(r.grav_base for r in rows)
    grav_pruned = statistics.fmean(r.grav_pruned for r in rows)
    eff_base = statistics.fmean(r.eff_base for r in rows)
    eff_pruned = statistics.fmean(r.eff_pruned for r in rows)
    removed = statistics.fmean(r.removed_total for r in rows)
    flips = sum(r.flip_count for r in rows)

    pur_deltas = [r.pur_delta for r in rows]
    grav_deltas = [r.grav_delta for r in rows]
    eff_deltas = [r.eff_delta for r in rows]

    pur_mean, pur_se, pur_t = _mean_se_t(pur_deltas)
    grav_mean, grav_se, grav_t = _mean_se_t(grav_deltas)
    corr_eff = _pearson(grav_deltas, eff_deltas)

    print(
        f"{n_layers:4d}  {mode:>8s}  {q:4.2f}  {len(rows):5d}  "
        f"{pur_base:8.4f}  {pur_pruned:8.4f}  {pur_mean:+8.4f}  "
        f"{grav_base:+8.4f}  {grav_pruned:+8.4f}  {grav_mean:+8.4f}  "
        f"{pur_se:7.4f}  {grav_se:7.4f}  {eff_base:7.3f}  {eff_pruned:7.3f}  "
        f"{removed:7.1f}  {flips:5d}  {corr_eff:+6.3f}"
    )


def main() -> None:
    print("=" * 118)
    print("DENSE + PRUNE CHANNEL-COUNT GUARD")
    print("  Same dense 3D same-graph setup; guard protects eff_ch instead of coarse reach/core")
    print("=" * 118)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_SWEEP}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  k-band: {K_BAND}")
    print(f"  guard floor: max({MIN_EFF_CH:.2f}, eff_ch * (1 - {EFF_DROP_FRAC:.2f}))")
    print()
    print(
        f"{'N':>4s}  {'mode':>8s}  {'q':>4s}  {'valid':>5s}  "
        f"{'pur_b':>8s}  {'pur_p':>8s}  {'d_pur':>8s}  "
        f"{'grav_b':>8s}  {'grav_p':>8s}  {'d_grav':>8s}  "
        f"{'pur_SE':>7s}  {'grav_SE':>7s}  {'eff_b':>7s}  {'eff_p':>7s}  "
        f"{'removed':>7s}  {'flip':>5s}  {'corr_eff':>8s}"
    )
    print("-" * 118)

    for n_layers in N_LAYERS_SWEEP:
        for q in Q_SWEEP:
            plain_rows: list[Summary] = []
            guard_rows: list[Summary] = []
            for seed in range(N_SEEDS):
                plain = _plain_seed_summary(n_layers, seed, q)
                guard = _seed_summary(n_layers, seed, q)
                if plain is not None:
                    plain_rows.append(plain)
                if guard is not None:
                    guard_rows.append(guard)

            _print_rows(plain_rows, n_layers, q, "plain")
            _print_rows(guard_rows, n_layers, q, "guarded")
            print()

    print("=" * 118)
    print("KEY")
    print("  guarded = channel-count floor enforced on eff_ch")
    print("  corr_eff = corr(delta_grav, delta_eff_ch) within each row")
    print("  The guard is only meaningful if it lowers flips without killing pur_cl gains")
    print("=" * 118)


if __name__ == "__main__":
    main()
