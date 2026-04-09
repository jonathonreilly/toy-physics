#!/usr/bin/env python3
"""Frozen-field control for the dense-prune gravity sign flip.

The narrow question here is whether the gravity flip seen after dense pruning
is better explained by:

  1. field distortion from recomputing the Laplacian on the pruned graph, or
  2. loss of mass-coupled detector support after the field is fixed.

We keep the setup aligned with the q=0.03 dense-prune same-graph lane:
  - same seed-generated dense 3D graphs
  - same barrier / mass placement rules
  - same prune quantile and iteration count
  - same k-band and same detector-side readout

The two arms we compare on the pruned graph are:
  - frozen field: field computed on the original graph, propagated on pruned graph
  - recomputed field: field computed on the pruned graph, propagated on pruned graph

If the frozen-field arm keeps the sign while the recomputed arm flips, the
field geometry is doing the damage. If both arms flip together, path severing
is the better explanation.

PStack experiment: dense-prune-frozen-field-control
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
    _barrier_slices,
    _layer_map,
    _prune_graph,
    _select_mass_nodes,
)
from scripts.three_d_joint_test import (  # type: ignore  # noqa: E402
    BETA,
    cl_purity,
    generate_3d_dag,
    propagate_3d,
)

PRUNE_Q = float(os.environ.get("DENSE_PRUNE_Q", "0.03"))
PRUNE_ITERS = int(os.environ.get("DENSE_PRUNE_ITERS", "1"))
FIXED_MASS_COUNT = 8
FIXED_B_OFFSET = 3.0


@dataclass(frozen=True)
class SeedSummary:
    pur_base: float
    pur_frozen: float
    pur_recomp: float
    grav_base: float
    grav_frozen: float
    grav_recomp: float
    flow_base: float
    flow_frozen: float
    flow_recomp: float
    reach_base: float
    reach_pruned: float
    core_base: float
    core_pruned: float
    removed_total: int

    @property
    def grav_delta_frozen(self) -> float:
        return self.grav_frozen - self.grav_base

    @property
    def grav_delta_recomp(self) -> float:
        return self.grav_recomp - self.grav_base

    @property
    def pur_delta_frozen(self) -> float:
        return self.pur_frozen - self.pur_base

    @property
    def pur_delta_recomp(self) -> float:
        return self.pur_recomp - self.pur_base

    @property
    def flow_delta_frozen(self) -> float:
        return self.flow_frozen - self.flow_base

    @property
    def flow_delta_recomp(self) -> float:
        return self.flow_recomp - self.flow_base


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


def _mass_to_detector_reach(
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
) -> tuple[float, set[int]]:
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


def _field_metrics(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    n_layers: int,
    *,
    field_override: list[float] | None = None,
) -> tuple[float, float, float]:
    by_layer, layers = _layer_map(positions)
    blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
        positions, by_layer, layers
    )
    if not slit_upper or not slit_lower:
        return math.nan, math.nan

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return math.nan, math.nan, math.nan

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
    flow_vals: list[float] = []

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

        flow_vals.append(_mass_coupled_detector_flow(positions, adj, field_base, src, det_list, mass_nodes, k, blocked_barrier))

    if not grav_vals or not pur_vals or not flow_vals:
        return math.nan, math.nan, math.nan
    return statistics.fmean(pur_vals), statistics.fmean(grav_vals), statistics.fmean(flow_vals)


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


def _mass_coupled_detector_flow(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    k: float,
    blocked: set[int],
) -> float:
    """Fraction of detector probability whose amplitude has visited mass nodes."""

    n = len(positions)
    order = _topo_order(adj, n)
    mass_set = set(mass_nodes)
    amps_free = [0j] * n
    amps_mass = [0j] * n
    for s in src:
        amps_free[s] = 1.0 / len(src)

    for i in order:
        if i in blocked:
            continue
        if abs(amps_free[i]) < 1e-30 and abs(amps_mass[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = complex(math.cos(k * act), math.sin(k * act)) * w / L

            if j in mass_set:
                amps_mass[j] += (amps_free[i] + amps_mass[i]) * ea
            else:
                amps_free[j] += amps_free[i] * ea
                amps_mass[j] += amps_mass[i] * ea

    p_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
    p_free = sum(abs(amps_free[d]) ** 2 for d in det_list)
    tot = p_mass + p_free
    return p_mass / tot if tot > 1e-30 else math.nan


def _seed_summary(n_layers: int, seed: int) -> SeedSummary | None:
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

    pur_base, grav_base, flow_base = _field_metrics(positions, adj, mass_nodes, n_layers)
    field_orig = field_laplacian(positions, adj, mass_nodes)
    pur_frozen, grav_frozen, flow_frozen = _field_metrics(
        positions,
        pruned_adj,
        mass_nodes,
        n_layers,
        field_override=field_orig,
    )
    field_pruned = field_laplacian(positions, pruned_adj, mass_nodes)
    pur_recomp, grav_recomp, flow_recomp = _field_metrics(
        positions,
        pruned_adj,
        mass_nodes,
        n_layers,
        field_override=field_pruned,
    )

    if any(
        math.isnan(v)
        for v in (
            pur_base,
            grav_base,
            flow_base,
            pur_frozen,
            grav_frozen,
            flow_frozen,
            pur_recomp,
            grav_recomp,
            flow_recomp,
        )
    ):
        return None

    reach_base, _ = _mass_to_detector_reach(adj, mass_nodes, det_nodes)
    reach_pruned, _ = _mass_to_detector_reach(pruned_adj, mass_nodes, det_nodes)

    post_nodes = [i for i, (x, y, z) in enumerate(positions) if x > layers[len(layers) // 3] and x < layers[-1]]
    core_base = len(_path_core_nodes(adj, mass_nodes, det_nodes)) / len(post_nodes) if post_nodes else 0.0
    core_pruned = len(_path_core_nodes(pruned_adj, mass_nodes, det_nodes)) / len(post_nodes) if post_nodes else 0.0

    return SeedSummary(
        pur_base=pur_base,
        pur_frozen=pur_frozen,
        pur_recomp=pur_recomp,
        grav_base=grav_base,
        grav_frozen=grav_frozen,
        grav_recomp=grav_recomp,
        flow_base=flow_base,
        flow_frozen=flow_frozen,
        flow_recomp=flow_recomp,
        reach_base=reach_base,
        reach_pruned=reach_pruned,
        core_base=core_base,
        core_pruned=core_pruned,
        removed_total=removed_total,
    )


def main() -> None:
    print("=" * 100)
    print("DENSE + PRUNE FROZEN-FIELD CONTROL")
    print("  Same seed-generated dense 3D graphs; ask whether gravity flips because")
    print("  the Laplacian field geometry changes or because mass-coupled support is cut.")
    print("=" * 100)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune quantile: {PRUNE_Q}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  fixed mass count: {FIXED_MASS_COUNT}")
    print(f"  fixed b offset: {FIXED_B_OFFSET}")
    print(f"  k-band: {K_BAND}")
    print()
    print(
        f"{'N':>4s}  {'valid':>5s}  {'pur_base':>8s}  {'pur_froz':>8s}  {'pur_recomp':>10s}  "
        f"{'g_base':>8s}  {'g_frozen':>9s}  {'g_recomp':>9s}  "
        f"{'flow_b':>7s}  {'flow_p':>7s}  {'reach_b':>7s}  {'reach_p':>7s}  "
        f"{'core_b':>7s}  {'core_p':>7s}  {'flipF':>5s}  {'flipR':>5s}"
    )
    print("-" * 144)

    for n_layers in N_LAYERS_LIST:
        rows: list[SeedSummary] = []
        for seed in range(N_SEEDS):
            row = _seed_summary(n_layers, seed)
            if row is not None:
                rows.append(row)

        if not rows:
            print(
                f"{n_layers:4d}  {0:5d}  {'NA':>8s}  {'NA':>8s}  {'NA':>10s}  "
                f"{'NA':>8s}  {'NA':>9s}  {'NA':>9s}  "
                f"{'NA':>7s}  {'NA':>7s}  {'NA':>7s}  {'NA':>7s}  "
                f"{'NA':>5s}  {'NA':>5s}"
            )
            continue

        pur_base = statistics.fmean(r.pur_base for r in rows)
        pur_frozen = statistics.fmean(r.pur_frozen for r in rows)
        pur_recomp = statistics.fmean(r.pur_recomp for r in rows)
        grav_base = statistics.fmean(r.grav_base for r in rows)
        grav_frozen = statistics.fmean(r.grav_frozen for r in rows)
        grav_recomp = statistics.fmean(r.grav_recomp for r in rows)
        flow_base = statistics.fmean(r.flow_base for r in rows)
        flow_pruned = statistics.fmean(r.flow_recomp for r in rows)
        reach_base = statistics.fmean(r.reach_base for r in rows)
        reach_pruned = statistics.fmean(r.reach_pruned for r in rows)
        core_base = statistics.fmean(r.core_base for r in rows)
        core_pruned = statistics.fmean(r.core_pruned for r in rows)
        flip_frozen = sum(1 for r in rows if r.grav_base > 0 and r.grav_frozen < 0) / len(rows)
        flip_recomp = sum(1 for r in rows if r.grav_base > 0 and r.grav_recomp < 0) / len(rows)

        print(
            f"{n_layers:4d}  {len(rows):5d}  {pur_base:8.4f}  {pur_frozen:8.4f}  {pur_recomp:10.4f}  "
            f"{grav_base:+8.4f}  {grav_frozen:+9.4f}  {grav_recomp:+9.4f}  "
            f"{flow_base:7.3f}  {flow_pruned:7.3f}  {reach_base:7.3f}  {reach_pruned:7.3f}  {core_base:7.3f}  {core_pruned:7.3f}  "
            f"{flip_frozen:5.2f}  {flip_recomp:5.2f}"
        )

        dg_frozen = [r.grav_delta_frozen for r in rows]
        dg_recomp = [r.grav_delta_recomp for r in rows]
        df_frozen = [r.flow_delta_frozen for r in rows]
        df_recomp = [r.flow_delta_recomp for r in rows]
        dr = [r.reach_pruned - r.reach_base for r in rows]
        dc = [r.core_pruned - r.core_base for r in rows]
        dfr = [r.grav_frozen - r.grav_recomp for r in rows]

        print(
            f"      delta_grav frozen={statistics.fmean(dg_frozen):+.4f}, "
            f"recomp={statistics.fmean(dg_recomp):+.4f}, frozen-recomp={statistics.fmean(dfr):+.4f}"
        )
        print(
            f"      delta_flow frozen={statistics.fmean(df_frozen):+.4f}, "
            f"recomp={statistics.fmean(df_recomp):+.4f}"
        )
        print(
            f"      corr(delta_grav_recomp, delta_flow_recomp)={_pearson(dg_recomp, df_recomp):+.3f}, "
            f"corr(delta_grav_frozen, delta_flow_frozen)={_pearson(dg_frozen, df_frozen):+.3f}"
        )
        print(
            f"      corr(delta_grav_recomp, delta_reach)={_pearson(dg_recomp, dr):+.3f}, "
            f"corr(delta_grav_recomp, delta_core)={_pearson(dg_recomp, dc):+.3f}"
        )
        print(
            f"      reach {reach_base:.3f} -> {reach_pruned:.3f} | "
            f"core {core_base:.3f} -> {core_pruned:.3f}"
        )
        print()

    print("INTERPRETATION")
    print("  If the frozen and recomputed pruned arms both weaken together and track")
    print("  reach/core collapse, path severing is the better explanation.")
    print("  If the frozen arm stays near baseline while the recomputed arm flips,")
    print("  the Laplacian field geometry itself is doing most of the damage.")
    print("  Keep the claim narrow either way: this is a control audit, not a repair.")
    print("=" * 100)


if __name__ == "__main__":
    main()
