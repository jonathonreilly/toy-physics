#!/usr/bin/env python3
"""Companion controls for the channel-count-guarded dense-prune lane.

This script starts from the guarded dense 3D pruning lane and asks a stricter
question than the old reach/core checks:

  1. On the same dense 3D seed-generated graphs, does plain adaptive pruning
     or channel-count-guarded pruning do better on gravity + pur_cl?
  2. On those same graphs, does the guarded lane preserve a strict visibility
     style control as well?
  3. On a matched 3D chokepoint companion family, do the usual Born/linearity
     checks remain clean?

The goal is not to prove a full gravity law. The goal is to see whether the
channel-count-guarded dense-prune lane can be promoted beyond a narrow
gravity+pur_cl fix into a broader but still careful companion-controlled claim.

PStack experiment: channel-count-guard-companion-controls
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
    CONNECT_RADIUS,
    GAP,
    K_BAND,
    N_LAYERS_LIST,
    N_SEEDS,
    NODES_PER_LAYER,
    PRUNE_ITERS,
    XYZ_RANGE,
    _barrier_slices,
    _layer_map,
    _select_mass_nodes,
    _score_candidates,
)
from scripts.channel_count_guarded_prune import (  # type: ignore  # noqa: E402
    channel_guarded_prune,
)
from scripts.mass_path_guarded_prune import (  # type: ignore  # noqa: E402
    cl_purity,
    compute_field,
    gravity_signal,
    propagate,
)
from scripts.three_d_born_rule_chokepoint import (  # type: ignore  # noqa: E402
    generate_3d_dag_chokepoint,
    linearity_check,
    sorkin_test,
)
from scripts.three_d_joint_test import generate_3d_dag  # type: ignore  # noqa: E402

Q_LIST = (0.03, 0.05, 0.10)
N_BORN_SEEDS = 8
N_BINS = 12
Y_MIN = -12.0
Y_MAX = 12.0
SMOOTH_RADIUS = 1
FIXED_MASS_COUNT = 8
FIXED_B_OFFSET = 3.0


@dataclass(frozen=True)
class GuardSummary:
    q: float
    mode: str
    pur_base: float
    pur_pruned: float
    grav_base: float
    grav_pruned: float
    vis_base: float
    vis_pruned: float
    removed_total: int
    flip_count: int

    @property
    def pur_delta(self) -> float:
        return self.pur_pruned - self.pur_base

    @property
    def grav_delta(self) -> float:
        return self.grav_pruned - self.grav_base

    @property
    def vis_delta(self) -> float:
        return self.vis_pruned - self.vis_base


def _mean_se_t(vals: list[float]) -> tuple[float, float, float]:
    mean = statistics.fmean(vals)
    if len(vals) > 1:
        se = statistics.stdev(vals) / math.sqrt(len(vals))
    else:
        se = 0.0
    t = mean / se if se > 1e-30 else math.nan
    return mean, se, t


def _select_mass_nodes(
    positions: list[tuple[float, float, float]],
    by_layer: dict[int, list[int]],
    layers: list[int],
) -> list[int] | None:
    center_y = statistics.fmean(y for _, y, _ in positions)
    grav_idx = 2 * len(layers) // 3
    mass_nodes = sorted(
        [i for i in by_layer[layers[grav_idx]] if positions[i][1] > center_y + 2.0],
        key=lambda i: abs(positions[i][1] - (center_y + 3.0)),
    )[:FIXED_MASS_COUNT]
    return mass_nodes if len(mass_nodes) == FIXED_MASS_COUNT else None


def _all_mass_nodes(
    positions: list[tuple[float, float, float]],
    by_layer: dict[int, list[int]],
    layers: list[int],
) -> list[int]:
    center_y = statistics.fmean(y for _, y, _ in positions)
    bl_idx = len(layers) // 3
    grav_idx = 2 * len(layers) // 3

    bath_mass: list[int] = []
    for li in range(bl_idx + 1, min(len(layers), bl_idx + 3)):
        for i in by_layer[layers[li]]:
            if abs(positions[i][1] - center_y) <= 3.0:
                bath_mass.append(i)

    grav_mass_d = [i for i in by_layer[layers[grav_idx]] if positions[i][1] > center_y + 1.0]
    return sorted(set(bath_mass) | set(grav_mass_d))


def _binned_profile(
    probs: dict[int, float],
    positions: list[tuple[float, float, float]],
    det_list: list[int],
    *,
    y_min: float = Y_MIN,
    y_max: float = Y_MAX,
    n_bins: int = N_BINS,
) -> list[float]:
    bw = (y_max - y_min) / n_bins
    bins = [0.0] * n_bins
    for d in det_list:
        y = positions[d][1]
        b = int((y - y_min) / bw)
        b = max(0, min(n_bins - 1, b))
        bins[b] += probs.get(d, 0.0)
    return bins


def _smooth(profile: list[float], radius: int = SMOOTH_RADIUS) -> list[float]:
    if radius <= 0 or len(profile) < 3:
        return profile[:]
    out = []
    for i in range(len(profile)):
        lo = max(0, i - radius)
        hi = min(len(profile), i + radius + 1)
        window = profile[lo:hi]
        out.append(sum(window) / len(window))
    return out


def _profile_visibility(profile: list[float]) -> float:
    smooth = _smooth(profile)
    if len(smooth) < 3:
        return 0.0
    peaks = [
        smooth[i]
        for i in range(1, len(smooth) - 1)
        if smooth[i] > smooth[i - 1] and smooth[i] > smooth[i + 1]
    ]
    troughs = [
        smooth[i]
        for i in range(1, len(smooth) - 1)
        if smooth[i] < smooth[i - 1] and smooth[i] < smooth[i + 1]
    ]
    if not peaks or not troughs:
        return 0.0
    top = max(peaks)
    bottom = min(troughs)
    return (top - bottom) / (top + bottom) if top + bottom > 1e-30 else 0.0


def _strict_visibility_metrics(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    all_mass: list[int],
) -> tuple[float, float, float] | None:
    by_layer = defaultdict(list)
    for idx, (x, _y, _z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = statistics.fmean(y for _, y, _ in positions)
    bl_idx = len(layers) // 3
    barrier = by_layer[layers[bl_idx]]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:3]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:3]
    if not slit_a or not slit_b:
        return None
    blocked = set(barrier) - set(slit_a + slit_b)

    env_depth = max(1, round(len(layers) / 6))
    start = bl_idx + 1
    stop = min(len(layers), start + env_depth)
    mid = [i for layer in layers[start:stop] for i in by_layer[layer]]
    if not mid:
        return None

    field_mass = compute_field(positions, adj, all_mass) if all_mass else [0.0] * len(positions)

    v_coh_vals: list[float] = []
    v_single_vals: list[float] = []
    vis_gain_vals: list[float] = []

    for k in K_BAND:
        amps_both = propagate(positions, adj, field_mass, src, k, blocked)
        amps_a = propagate(positions, adj, field_mass, src, k, blocked | set(slit_b))
        amps_b = propagate(positions, adj, field_mass, src, k, blocked | set(slit_a))

        probs_both = {d: abs(amps_both[d]) ** 2 for d in det_list}
        probs_a = {d: abs(amps_a[d]) ** 2 for d in det_list}
        probs_b = {d: abs(amps_b[d]) ** 2 for d in det_list}
        tot_both = sum(probs_both.values())
        tot_a = sum(probs_a.values())
        tot_b = sum(probs_b.values())
        if tot_both > 1e-30:
            probs_both = {d: p / tot_both for d, p in probs_both.items()}
        if tot_a > 1e-30:
            probs_a = {d: p / tot_a for d, p in probs_a.items()}
        if tot_b > 1e-30:
            probs_b = {d: p / tot_b for d, p in probs_b.items()}

        probs_single_avg = {
            d: 0.5 * probs_a.get(d, 0.0) + 0.5 * probs_b.get(d, 0.0)
            for d in det_list
        }

        prof_both = _binned_profile(probs_both, positions, det_list)
        prof_single = _binned_profile(probs_single_avg, positions, det_list)
        v_coh = _profile_visibility(prof_both)
        v_single = _profile_visibility(prof_single)
        v_coh_vals.append(v_coh)
        v_single_vals.append(v_single)
        vis_gain_vals.append(v_coh - v_single)

    if not v_coh_vals:
        return None
    return (
        statistics.fmean(v_coh_vals),
        statistics.fmean(v_single_vals),
        statistics.fmean(vis_gain_vals),
    )


def _grav_pur_vis_metrics(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    all_mass: list[int],
    n_layers: int,
) -> tuple[float, float, float] | None:
    by_layer = defaultdict(list)
    for idx, (x, _y, _z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    center_y = statistics.fmean(y for _, y, _ in positions)
    bl_idx = len(layers) // 3
    barrier = by_layer[layers[bl_idx]]
    slit_a = [i for i in barrier if positions[i][1] > center_y + 3][:3]
    slit_b = [i for i in barrier if positions[i][1] < center_y - 3][:3]
    if not slit_a or not slit_b:
        return None
    blocked = set(barrier) - set(slit_a + slit_b)

    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers), start + env_depth)
    mid_nodes = [i for layer in layers[start:stop] for i in by_layer[layer]]
    if not mid_nodes:
        return None

    field_mass = compute_field(positions, adj, all_mass) if all_mass else [0.0] * len(positions)
    field_flat = [0.0] * len(positions)

    grav_vals: list[float] = []
    pur_vals: list[float] = []
    vis_vals: list[float] = []

    vis_metrics = _strict_visibility_metrics(positions, adj, all_mass)
    if vis_metrics is None:
        return None
    _vis_coh, _vis_single, vis_gain = vis_metrics

    for k in K_BAND:
        amps_mass = propagate(positions, adj, field_mass, src, k, blocked)
        amps_flat = propagate(positions, adj, field_flat, src, k, blocked)

        prob_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        prob_flat = sum(abs(amps_flat[d]) ** 2 for d in det_list)
        if prob_mass > 1e-30 and prob_flat > 1e-30:
            y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / prob_mass
            y_flat = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / prob_flat
            grav_vals.append(y_mass - y_flat)

        amps_a = propagate(positions, adj, field_mass, src, k, blocked | set(slit_b))
        amps_b = propagate(positions, adj, field_mass, src, k, blocked | set(slit_a))

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
        D = math.exp(-(10.0 ** 2) * Sn)
        pur = cl_purity(amps_a, amps_b, D, det_list)
        if not math.isnan(pur):
            pur_vals.append(pur)

    if not grav_vals or not pur_vals:
        return None

    return statistics.fmean(pur_vals), statistics.fmean(grav_vals), vis_gain


def _plain_adaptive_prune(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    q: float,
    max_iter: int,
) -> tuple[dict[int, list[int]], int]:
    current_adj = {i: list(nbs) for i, nbs in adj.items()}
    total_removed = 0

    for _ in range(max_iter):
        by_layer, layers = _layer_map(positions)
        blocked_barrier, slit_upper, slit_lower, _barrier_idx, _barrier_layer, _detector_layer = _barrier_slices(
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

        n_remove = int(len(candidate_scores) * q)
        if n_remove <= 0:
            break

        remove_set = {node for node, _score in candidate_scores[:n_remove]}
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


def _guarded_prune(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    q: float,
    max_iter: int,
) -> tuple[dict[int, list[int]], int]:
    by_layer, layers = _layer_map(positions)
    if len(layers) < 7:
        return adj, 0

    layer_list = [by_layer[layer] for layer in layers]
    mass_nodes = _select_mass_nodes(positions, by_layer, layers)
    if not mass_nodes:
        return adj, 0

    src = by_layer[layers[0]]
    det_nodes = list(by_layer[layers[-1]])
    blocked_base, _slit_upper, _slit_lower, _barrier_idx, _barrier_layer, _detector_layer = _barrier_slices(
        positions, by_layer, layers
    )
    pruned_adj, removed_total = channel_guarded_prune(
        positions,
        adj,
        layer_list,
        mass_nodes,
        src,
        det_nodes,
        blocked_base,
        quantile=q,
        max_iter=max_iter,
        min_eff_ratio=0.80,
    )
    return pruned_adj, removed_total


def _same_graph_seed_summary(
    n_layers: int,
    seed: int,
    q: float,
    guarded: bool,
) -> GuardSummary | None:
    positions, adj = generate_3d_dag(
        n_layers=n_layers,
        nodes_per_layer=NODES_PER_LAYER,
        xyz_range=XYZ_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=seed * 7 + 3,
        gap=GAP,
    )
    by_layer = defaultdict(list)
    for idx, (x, _y, _z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    if len(layers) < 7:
        return None

    mass_nodes = _select_mass_nodes(positions, by_layer, layers)
    if not mass_nodes:
        return None
    all_mass = _all_mass_nodes(positions, by_layer, layers)

    if guarded:
        pruned_adj, removed_total = _guarded_prune(positions, adj, q, PRUNE_ITERS)
        mode = "guarded"
    else:
        pruned_adj, removed_total = _plain_adaptive_prune(positions, adj, q, PRUNE_ITERS)
        mode = "plain"

    base_metrics = _grav_pur_vis_metrics(positions, adj, mass_nodes, all_mass, n_layers)
    prune_metrics = _grav_pur_vis_metrics(positions, pruned_adj, mass_nodes, all_mass, n_layers)
    if base_metrics is None or prune_metrics is None:
        return None

    pur_base, grav_base, vis_base = base_metrics
    pur_pruned, grav_pruned, vis_pruned = prune_metrics
    flip_count = 1 if grav_base > 0 and grav_pruned < 0 else 0

    if any(math.isnan(v) for v in (pur_base, grav_base, vis_base, pur_pruned, grav_pruned, vis_pruned)):
        return None

    return GuardSummary(
        q=q,
        mode=mode,
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        vis_base=vis_base,
        vis_pruned=vis_pruned,
        removed_total=removed_total,
        flip_count=flip_count,
    )


def _born_companion_seed_summary(seed: int) -> tuple[float, float] | None:
    positions, adj, layer_indices = generate_3d_dag_chokepoint(
        n_layers=12,
        nodes_per_layer=25,
        yz_range=10.0,
        connect_radius=3.5,
        rng_seed=seed * 13 + 5,
    )

    lin_rel = linearity_check(positions, adj, layer_indices, k=5.0)
    if lin_rel is None or math.isnan(lin_rel):
        return None

    i3_ratios: list[float] = []
    for k in (3.0, 5.0):
        result = sorkin_test(positions, adj, layer_indices, k)
        if result is None:
            continue
        i3, p = result
        if p > 1e-30:
            i3_ratios.append(abs(i3) / p)

    if not i3_ratios:
        return None

    return lin_rel, max(i3_ratios)


def _born_companion_summary() -> list[tuple[int, float, float, str]]:
    rows: list[tuple[int, float, float, str]] = []
    for seed in range(N_BORN_SEEDS):
        result = _born_companion_seed_summary(seed)
        if result is None:
            rows.append((seed, math.nan, math.nan, "SKIP"))
            continue
        lin_rel, i3_ratio = result
        verdict = "PASS" if lin_rel < 1e-10 and i3_ratio < 1e-10 else "WEAK" if lin_rel < 1e-6 else "FAIL"
        rows.append((seed, lin_rel, i3_ratio, verdict))
    return rows


def main() -> None:
    print("=" * 104)
    print("CHANNEL-COUNT-GUARD COMPANION CONTROLS")
    print("  Dense 3D same-graph plain adaptive vs channel-count guarded pruning")
    print("  Companion controls: strict visibility on the same dense graphs")
    print("  Companion Born/linearity on a matched 3D chokepoint family")
    print("=" * 104)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  gap: {GAP}")
    print(f"  q sweep: {Q_LIST}")
    print(f"  companion Born seeds: {N_BORN_SEEDS}")
    print()

    print("[1] SAME-GRAPH DENSE 3D: plain adaptive vs channel-count guarded")
    print(
        f"{'N':>4s}  {'q':>5s}  {'mode':>8s}  {'valid':>5s}  "
        f"{'pur_b':>8s}  {'pur_p':>8s}  {'d_pur':>8s}  "
        f"{'grav_b':>8s}  {'grav_p':>8s}  {'d_grav':>8s}  "
        f"{'vis_b':>8s}  {'vis_p':>8s}  {'d_vis':>8s}  "
        f"{'flips':>5s}  {'removed':>8s}"
    )
    print("-" * 126)

    for n_layers in N_LAYERS_LIST:
        for q in Q_LIST:
            for guarded in (False, True):
                rows: list[GuardSummary] = []
                for seed in range(N_SEEDS):
                    row = _same_graph_seed_summary(n_layers, seed, q, guarded)
                    if row is not None:
                        rows.append(row)
                if not rows:
                    print(
                        f"{n_layers:4d}  {q:5.2f}  {'guarded' if guarded else 'plain':>8s}  "
                        f"{0:5d}  {'NA':>8s}  {'NA':>8s}  {'NA':>8s}  "
                        f"{'NA':>8s}  {'NA':>8s}  {'NA':>8s}  "
                        f"{'NA':>8s}  {'NA':>8s}  {'NA':>8s}  {'NA':>5s}  {'NA':>8s}"
                    )
                    continue

                pur_base_vals = [r.pur_base for r in rows]
                pur_pruned_vals = [r.pur_pruned for r in rows]
                grav_base_vals = [r.grav_base for r in rows]
                grav_pruned_vals = [r.grav_pruned for r in rows]
                vis_base_vals = [r.vis_base for r in rows]
                vis_pruned_vals = [r.vis_pruned for r in rows]
                pur_deltas = [r.pur_delta for r in rows]
                grav_deltas = [r.grav_delta for r in rows]
                vis_deltas = [r.vis_delta for r in rows]
                flip_count = sum(r.flip_count for r in rows)
                removed_mean = statistics.fmean(r.removed_total for r in rows)

                print(
                    f"{n_layers:4d}  {q:5.2f}  "
                    f"{('guarded' if guarded else 'plain'):>8s}  {len(rows):5d}  "
                    f"{statistics.fmean(pur_base_vals):8.4f}  {statistics.fmean(pur_pruned_vals):8.4f}  "
                    f"{_mean_se_t(pur_deltas)[0]:+8.4f}  "
                    f"{statistics.fmean(grav_base_vals):+8.4f}  {statistics.fmean(grav_pruned_vals):+8.4f}  "
                    f"{_mean_se_t(grav_deltas)[0]:+8.4f}  "
                    f"{statistics.fmean(vis_base_vals):8.4f}  {statistics.fmean(vis_pruned_vals):8.4f}  "
                    f"{_mean_se_t(vis_deltas)[0]:+8.4f}  "
                    f"{flip_count:5d}  {removed_mean:8.1f}"
                )
        print()

    print("[2] COMPANION BORN / LINEARITY (3D chokepoint family)")
    print(f"  {'seed':>4s}  {'max_rel':>14s}  {'I3/P':>12s}  verdict")
    print(f"  {'-' * 46}")
    born_rows = _born_companion_summary()
    for seed, lin_rel, i3_ratio, verdict in born_rows:
        print(f"  {seed:4d}  {lin_rel:14.6e}  {i3_ratio:12.6e}  {verdict}")

    valid_lin = [row[1] for row in born_rows if math.isfinite(row[1])]
    valid_i3 = [row[2] for row in born_rows if math.isfinite(row[2])]
    if valid_lin and valid_i3:
        print(
            f"  mean max_rel={statistics.fmean(valid_lin):.3e}, "
            f"mean I3/P={statistics.fmean(valid_i3):.3e}"
        )
    print()

    print("[3] SAFE CLAIM GUIDE")
    print("  - If guarded pruning improves pur_cl while keeping gravity and strict")
    print("    visibility at least as good as plain adaptive, it can be described")
    print("    as a broader companion-controlled dense-graph lane.")
    print("  - If gravity is still fragile or visibility weakens materially, keep")
    print("    the claim narrow: a gravity+pur_cl fix with companion sanity checks.")
    print("  - The Born companion control should stay separate from the dense-prune")
    print("    claim unless it remains machine-precision clean.")
    print("=" * 104)


if __name__ == "__main__":
    main()
