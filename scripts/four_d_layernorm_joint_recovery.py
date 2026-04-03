#!/usr/bin/env python3
"""Reconstruct the claimed 4D layer-norm + scaled-gravity joint lane.

This is the audit/recovery script for the older 4D joint claim behind the
a2f2132 / a3dd7ee commit pair. It keeps the retained 4D modular family fixed,
adds per-layer normalization, applies a scaled gravity field, and checks:

  1. gravity deflection on the same graphs
  2. actual CL-bath purity / floor on the same graphs
  3. Born-rule / Sorkin cleanliness on the same-family barrier-pruned view

The goal is review-safe reconstruction, not promotion:
  - If the same-family lane is clean and gravity survives, the claim is
    supportable.
  - If only part of the lane survives, the claim is provisional.
  - If gravity or Born cleanliness fails, retire the strong joint wording.
"""

from __future__ import annotations

import argparse
import cmath
import math
import os
import statistics
import sys
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.four_d_decoherence_large_n import (  # type: ignore
    BETA,
    CONNECT_RADIUS,
    NODES_PER_LAYER,
    SPATIAL_RANGE,
    cl_purity,
    compute_field_4d,
    generate_4d_modular_dag,
)

LAM = 10.0
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 12
N_LAYERS_LIST = (25, 30, 40)
GAP = 3.0
FIELD_SCALE = 0.5


def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else math.nan


def _se(vals: list[float]) -> float:
    if len(vals) < 2:
        return math.nan
    return statistics.stdev(vals) / math.sqrt(len(vals))


def _t_stat(vals: list[float]) -> float:
    se = _se(vals)
    if not vals or not math.isfinite(se) or se <= 1e-30:
        return math.nan
    return _mean(vals) / se


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
    """Same-family chokepoint view: remove edges that jump across barrier."""
    by_idx = _layer_map(layer_indices)
    pruned: defaultdict[int, list[int]] = defaultdict(list)
    for i, nbs in adj.items():
        li = by_idx.get(i, -1)
        for j in nbs:
            lj = by_idx.get(j, -1)
            if li < barrier_layer and lj > barrier_layer:
                continue
            pruned[i].append(j)
    return dict(pruned)


def _propagate_layernorm(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    k: float,
    blocked: set[int] | None = None,
) -> list[complex]:
    """Layer-by-layer propagation with explicit per-layer renormalization."""
    blocked = blocked or set()
    by_layer: defaultdict[int, list[int]] = defaultdict(list)
    for idx, (x, _y, _z, _w) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * len(positions)
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if i in blocked or abs(amps[i]) < 1e-30:
                continue
            x1, y1, z1, w1 = positions[i]
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x2, y2, z2, w2 = positions[j]
                dx = x2 - x1
                dy = y2 - y1
                dz = z2 - z1
                dw = w2 - w1
                L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
                if L < 1e-10:
                    continue
                cos_theta = dx / L
                theta = math.acos(min(max(cos_theta, -1.0), 1.0))
                wt = math.exp(-BETA * theta * theta)
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1.0 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0.0))
                act = dl - ret
                amps[j] += amps[i] * cmath.exp(1j * k * act) * wt / L

        if li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm
    return amps


def _slit_partition(
    positions: list[tuple[float, float, float, float]],
    layer_indices: list[list[int]],
) -> tuple[int, list[int], list[int], set[int], list[int], list[int], list[int]] | None:
    n_layers = len(layer_indices)
    if n_layers < 7:
        return None

    barrier_layer = n_layers // 3
    barrier = list(layer_indices[barrier_layer])
    ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(ys) / len(ys)

    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if abs(positions[i][1] - cy) < 2][:5]
    slit_c = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b or not slit_c:
        return None

    all_slits = slit_a + slit_b + slit_c
    blocked = set(barrier) - set(all_slits)
    src = list(layer_indices[0])
    det_list = list(layer_indices[-1])
    if not src or not det_list:
        return None
    return barrier_layer, barrier, src, blocked, slit_a, slit_b, slit_c


def _sorkin_ratio_layernorm(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    blocked: set[int],
    slit_a: list[int],
    slit_b: list[int],
    slit_c: list[int],
    field: list[float],
    k: float,
) -> tuple[float, float] | None:
    all_slits = set(slit_a) | set(slit_b) | set(slit_c)

    def prob(open_set: set[int]) -> float:
        closed = all_slits - open_set
        amps = _propagate_layernorm(positions, adj, field, src, k, blocked | closed)
        return sum(abs(amps[d]) ** 2 for d in det_list)

    p_abc = prob(all_slits)
    p_ab = prob(set(slit_a) | set(slit_b))
    p_ac = prob(set(slit_a) | set(slit_c))
    p_bc = prob(set(slit_b) | set(slit_c))
    p_a = prob(set(slit_a))
    p_b = prob(set(slit_b))
    p_c = prob(set(slit_c))
    i3 = p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c
    return i3, p_abc


def _measure_seed(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    layer_indices: list[list[int]],
    field_scale: float,
) -> dict[str, float] | None:
    info = _slit_partition(positions, layer_indices)
    if info is None:
        return None
    barrier_layer, barrier, src, blocked, slit_a, slit_b, slit_c = info
    det_list = list(layer_indices[-1])
    n_actual = len(layer_indices)
    if len(det_list) < 1:
        return None

    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)
    grav_idx = 2 * n_actual // 3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1][:8]
    if not grav_mass:
        return None

    bath_mass: list[int] = []
    for li in range(barrier_layer + 1, min(n_actual, barrier_layer + 3)):
        for i in layer_indices[li]:
            if abs(positions[i][1] - cy) <= 3:
                bath_mass.append(i)
    all_mass = set(bath_mass) | set(grav_mass)
    raw_field = compute_field_4d(positions, adj, list(all_mass)) if all_mass else [0.0] * len(positions)
    field = [field_scale * v for v in raw_field]
    free_field = [0.0] * len(positions)

    grav_vals: list[float] = []
    pur_vals: list[float] = []
    min_vals: list[float] = []
    born_vals: list[float] = []

    mid_nodes = [
        i
        for li in range(barrier_layer + 1, n_actual - 1)
        for i in layer_indices[li]
        if i not in blocked and i not in set(det_list)
    ]
    if len(mid_nodes) < 4:
        return None

    for k in K_BAND:
        amps_mass = _propagate_layernorm(positions, adj, field, src, k, blocked)
        amps_flat = _propagate_layernorm(positions, adj, free_field, src, k, blocked)
        prob_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        prob_flat = sum(abs(amps_flat[d]) ** 2 for d in det_list)
        if prob_mass > 1e-30 and prob_flat > 1e-30:
            y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / prob_mass
            y_flat = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / prob_flat
            grav_vals.append(y_mass - y_flat)

        amps_a = _propagate_layernorm(positions, adj, field, src, k, blocked | set(slit_b))
        amps_b = _propagate_layernorm(positions, adj, field, src, k, blocked | set(slit_a))

        ba = [0j] * 8
        bb = [0j] * 8
        y_min = min(positions[i][1] for i in mid_nodes) - 1e-3
        y_max = max(positions[i][1] for i in mid_nodes) + 1e-3
        if y_max > y_min:
            bw = (y_max - y_min) / 8
            for m in mid_nodes:
                y = positions[m][1]
                b = int((y - y_min) / bw)
                b = max(0, min(7, b))
                ba[b] += amps_a[m]
                bb[b] += amps_b[m]
            denom = sum(abs(a) ** 2 for a in ba) + sum(abs(b) ** 2 for b in bb)
            if denom > 1e-30:
                sn = sum(abs(a - b) ** 2 for a, b in zip(ba, bb)) / denom
                D = math.exp(-(LAM**2) * sn)
                pur = cl_purity(amps_a, amps_b, D, det_list)
                pur_min = cl_purity(amps_a, amps_b, 0.0, det_list)
                if math.isfinite(pur):
                    pur_vals.append(pur)
                if math.isfinite(pur_min):
                    min_vals.append(pur_min)

        born = _sorkin_ratio_layernorm(
            positions,
            adj,
            src,
            det_list,
            blocked,
            slit_a,
            slit_b,
            slit_c,
            field,
            k,
        )
        if born is not None and born[1] > 1e-30:
            born_vals.append(abs(born[0]) / born[1])

    if not grav_vals or not pur_vals or not min_vals or not born_vals:
        return None

    return {
        "grav_d": _mean(grav_vals),
        "pur_cl": _mean(pur_vals),
        "pur_min": _mean(min_vals),
        "born_i3": _mean(born_vals),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=list(N_LAYERS_LIST))
    parser.add_argument("--n-seeds", type=int, default=N_SEEDS)
    parser.add_argument("--gap", type=float, default=GAP)
    parser.add_argument("--field-scale", type=float, default=FIELD_SCALE)
    args = parser.parse_args()

    print("=" * 88)
    print("4D LAYERNORM + SCALED GRAVITY JOINT RECOVERY")
    print("  Goal: reconstruct the old 4D joint claim on current tracked code")
    print(f"  family: dense 4D modular DAGs, gap={args.gap}, field_scale={args.field_scale}")
    print(f"  nodes/layer={NODES_PER_LAYER}, spatial_range={SPATIAL_RANGE}, connect_radius={CONNECT_RADIUS}")
    print(f"  N list={list(args.n_layers)}, seeds={args.n_seeds}")
    print("=" * 88)
    print()

    rows: list[dict[str, float | int | str]] = []
    seeds = [s * 13 + 5 for s in range(args.n_seeds)]

    print(
        f"  {'N':>4s}  {'grav_d':>8s}  {'grav_t':>6s}  {'pur_cl':>8s}  {'pur_min':>8s}  "
        f"{'Born |I3|/P':>12s}  {'n_ok':>4s}  verdict"
    )
    print(f"  {'-' * 84}")

    for nl in args.n_layers:
        grav_vals: list[float] = []
        pur_vals: list[float] = []
        min_vals: list[float] = []
        born_vals: list[float] = []
        n_ok = 0

        for seed in seeds:
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=nl,
                nodes_per_layer=NODES_PER_LAYER,
                spatial_range=SPATIAL_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed,
                gap=args.gap,
            )
            metrics = _measure_seed(positions, adj, layer_indices, args.field_scale)
            if metrics is None:
                continue
            grav_vals.append(metrics["grav_d"])
            pur_vals.append(metrics["pur_cl"])
            min_vals.append(metrics["pur_min"])
            born_vals.append(metrics["born_i3"])
            n_ok += 1

        if not n_ok:
            print(f"  {nl:4d}  FAIL")
            continue

        grav_mean = _mean(grav_vals)
        grav_t = _t_stat(grav_vals)
        pur_cl = _mean(pur_vals)
        pur_min = _mean(min_vals)
        born_i3 = _mean(born_vals)
        grav_pass = math.isfinite(grav_t) and grav_t > 2.0 and grav_mean > 0.0
        decoh_pass = pur_cl < 0.96
        born_pass = born_i3 < 1e-10

        if grav_pass and decoh_pass and born_pass:
            verdict = "SUPPORTABLE"
        elif (grav_pass and decoh_pass) or (born_pass and decoh_pass):
            verdict = "PROVISIONAL"
        else:
            verdict = "REMOVE"

        print(
            f"  {nl:4d}  {grav_mean:+8.3f}  {grav_t:6.2f}  {pur_cl:8.3f}  {pur_min:8.3f}  "
            f"{born_i3:12.2e}  {n_ok:4d}  {verdict}"
        )
        rows.append(
            {
                "N": nl,
                "grav_d": grav_mean,
                "grav_t": grav_t,
                "pur_cl": pur_cl,
                "pur_min": pur_min,
                "born_i3": born_i3,
                "n_ok": n_ok,
                "verdict": verdict,
            }
        )

    print()
    if rows:
        supportable = [r for r in rows if r["verdict"] == "SUPPORTABLE"]
        provisional = [r for r in rows if r["verdict"] == "PROVISIONAL"]
        if supportable:
            best = max(supportable, key=lambda r: (r["grav_t"], -r["pur_cl"]))
            print(
                f"  Strongest supportable row: N={best['N']} "
                f"grav={best['grav_d']:+.3f} (t={best['grav_t']:.2f}), "
                f"pur_cl={best['pur_cl']:.3f}, Born={best['born_i3']:.2e}"
            )
        elif provisional:
            best = max(provisional, key=lambda r: (r["grav_t"], -r["pur_cl"]))
            print(
                f"  Strongest provisional row: N={best['N']} "
                f"grav={best['grav_d']:+.3f} (t={best['grav_t']:.2f}), "
                f"pur_cl={best['pur_cl']:.3f}, Born={best['born_i3']:.2e}"
            )
        else:
            print("  Retirement recommendation: remove the 4D joint champion claim.")


if __name__ == "__main__":
    main()
