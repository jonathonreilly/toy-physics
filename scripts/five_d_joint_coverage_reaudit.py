#!/usr/bin/env python3
"""5D joint coverage/accounting re-audit.

This re-audit does not try to rescue the 5D claim. It asks a narrower
question about the historical dense 5D joint pilot:

  - how many seeds are actually accepted vs filtered?
  - does the Born read have explicit coverage, or was it implicitly
    reported on a filtered subset?
  - once coverage is made explicit, does any same-family positive story
    survive?

The script intentionally stays on the retained dense 5D modular corner
so that the result is comparable to the original joint pilot, but the
reporting is now accounting-first rather than rescue-first.
"""

from __future__ import annotations

import math
import statistics
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.five_d_dense_pilot import (  # type: ignore
    BETA,
    GAP,
    K_BAND,
    N_LAYERS,
    centroid_y,
    compute_field,
    generate_5d_modular_dag,
    propagate,
    reachable_fraction,
)

LAM = 10.0
BORN_K = 5.0
N_YBINS = 6
N_SEEDS = 8

# Keep the same dense 5D neighborhood as the historical joint pilot.
CONFIGS = [
    ("low-center", 90, 6.50, 5.0),
    ("center-low", 100, 6.25, 5.0),
    ("center", 100, 6.50, 5.0),
    ("center-high", 100, 6.75, 5.0),
    ("top-center", 110, 6.50, 5.0),
]

MASS_COUNTS = (1, 2, 4, 8)
MASS_COUNT_FIXED = 8


def _mean(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else math.nan


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
    """Remove edges that jump across the barrier layer for Born sanity."""
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


def _born_sanity(positions, adj, layer_indices, field, src, det_list, k: float = BORN_K, order=None):
    partition = _slit_partition(positions, layer_indices)
    if partition is None:
        return None
    barrier_layer, barrier, src, blocked, det_list, slit_a, slit_b, slit_c = partition
    born_adj = _prune_bypass_edges(adj, layer_indices, barrier_layer)
    born_order = order if order is not None else None
    all_slits = set(slit_a) | set(slit_b) | set(slit_c)

    def prob(open_set: set[int]):
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


def _fmt(v: float | None) -> str:
    if v is None or not math.isfinite(v):
        return "NA"
    return f"{v:.3f}"


def _fmt_count(num: int, den: int) -> str:
    return f"{num}/{den}" if den else "0/0"


def _measure_seed(
    positions,
    adj,
    layer_indices,
    nodes_per_layer: int,
    seed: int,
):
    node_count = len(positions)
    edge_count = sum(len(v) for v in adj.values())
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    reach_frac = reachable_fraction(adj, src, det_list)
    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)
    mid = len(layer_indices) // 2
    candidates = sorted(
        [i for i in layer_indices[mid] if positions[i][1] > cy + 1],
        key=lambda i: -positions[i][1],
    )

    partition = _slit_partition(positions, layer_indices)
    if partition is None:
        return {
            "accepted": False,
            "reason": "no_partition",
            "seed": seed,
            "reach_frac": reach_frac,
            "candidates": len(candidates),
            "node_count": node_count,
            "edge_count": edge_count,
        }

    barrier_layer, barrier, _src, blocked, _det, slit_a, slit_b, slit_c = partition
    mid_nodes = [
        i
        for li in range(barrier_layer + 1, len(layer_indices) - 1)
        for i in layer_indices[li]
        if i not in blocked and i not in set(det_list)
    ]

    if reach_frac <= 0.05:
        return {
            "accepted": False,
            "reason": "low_reach",
            "seed": seed,
            "reach_frac": reach_frac,
            "candidates": len(candidates),
            "node_count": node_count,
            "edge_count": edge_count,
        }
    if len(candidates) < max(MASS_COUNTS):
        return {
            "accepted": False,
            "reason": "few_candidates",
            "seed": seed,
            "reach_frac": reach_frac,
            "candidates": len(candidates),
            "node_count": node_count,
            "edge_count": edge_count,
        }
    if len(mid_nodes) < 4:
        return {
            "accepted": False,
            "reason": "too_few_mid_nodes",
            "seed": seed,
            "reach_frac": reach_frac,
            "candidates": len(candidates),
            "node_count": node_count,
            "edge_count": edge_count,
        }
    if len(candidates) < MASS_COUNT_FIXED:
        return {
            "accepted": False,
            "reason": "no_mass_count_fixed",
            "seed": seed,
            "reach_frac": reach_frac,
            "candidates": len(candidates),
            "node_count": node_count,
            "edge_count": edge_count,
        }

    free_f = [0.0] * len(positions)

    per_mass: dict[int, list[float]] = {target: [] for target in MASS_COUNTS}
    seed_gravity = []
    seed_pur = []
    seed_pmin = []
    seed_snorm = []
    born_vals = []
    born_ratios = []
    born_available = False

    for target_n in MASS_COUNTS:
        mass_nodes = candidates[:target_n]
        field = compute_field(positions, adj, mass_nodes)
        shifts = []
        for k in K_BAND:
            amps_m = propagate(positions, adj, field, src, k)
            amps_f = propagate(positions, adj, free_f, src, k)
            shifts.append(centroid_y(amps_m, positions, det_list) - centroid_y(amps_f, positions, det_list))
        if shifts:
            per_mass[target_n].append(sum(shifts) / len(shifts))

    mass_nodes = candidates[:MASS_COUNT_FIXED]
    field = compute_field(positions, adj, mass_nodes)
    for k in K_BAND:
        amps_a = propagate(positions, adj, field, src, k, blocked | set(slit_b))
        amps_b = propagate(positions, adj, field, src, k, blocked | set(slit_a))
        S, s_norm = _cl_contrast(amps_a, amps_b, mid_nodes, positions)
        D = math.exp(-(LAM ** 2) * s_norm)
        pur_cl = _cl_purity(amps_a, amps_b, D, det_list)
        pur_min = _cl_purity(amps_a, amps_b, 0.0, det_list)
        born = _born_sanity(positions, adj, layer_indices, field, src, det_list, k=BORN_K)
        if born is not None:
            born_available = True
            born_lin, born_i3, born_ratio = born
            born_vals.append(born_ratio)
            born_ratios.append(born_ratio)
        if not math.isnan(pur_cl):
            seed_pur.append(pur_cl)
            seed_pmin.append(pur_min)
            seed_snorm.append(s_norm)
            seed_gravity.append(
                centroid_y(propagate(positions, adj, field, src, k), positions, det_list)
                - centroid_y(propagate(positions, adj, free_f, src, k), positions, det_list)
            )

    accepted = bool(seed_pur)
    if not accepted:
        return {
            "accepted": False,
            "reason": "no_joint_read",
            "seed": seed,
            "reach_frac": reach_frac,
            "candidates": len(candidates),
            "node_count": node_count,
            "edge_count": edge_count,
        }

    mass_summary_rows = []
    for target_n, vals in per_mass.items():
        if not vals:
            continue
        avg = sum(vals) / len(vals)
        se = statistics.stdev(vals) / math.sqrt(len(vals)) if len(vals) > 1 else math.nan
        t = avg / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        mass_summary_rows.append((target_n, avg, se, t))

    alpha_fit = _fit_power_law([n for n, _avg, _se, _t in mass_summary_rows], [avg for _n, avg, _se, _t in mass_summary_rows])

    return {
        "accepted": True,
        "reason": "accepted",
        "seed": seed,
        "reach_frac": reach_frac,
        "candidates": len(candidates),
        "node_count": node_count,
        "edge_count": edge_count,
        "grav_shift": _mean(seed_gravity) if seed_gravity else math.nan,
        "pur_cl": _mean(seed_pur) if seed_pur else math.nan,
        "pur_min": _mean(seed_pmin) if seed_pmin else math.nan,
        "s_norm": _mean(seed_snorm) if seed_snorm else math.nan,
        "born_available": born_available,
        "born_ratio": _mean(born_ratios) if born_ratios else math.nan,
        "born_nonzero": sum(1 for v in born_ratios if v > 1e-12),
        "mass_summary_rows": mass_summary_rows,
        "alpha": alpha_fit[0] if alpha_fit is not None else None,
    }


def measure_config(nodes_per_layer: int, connect_radius: float, spatial_range: float, gap: float = GAP):
    rows = []
    filtered = Counter()
    attempted = 0

    for seed in range(N_SEEDS):
        attempted += 1
        positions, adj, layer_indices = generate_5d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=nodes_per_layer,
            spatial_range=spatial_range,
            connect_radius=connect_radius,
            rng_seed=seed * 17 + 3,
            gap=gap,
        )
        row = _measure_seed(positions, adj, layer_indices, nodes_per_layer, seed)
        if row["accepted"]:
            rows.append(row)
        else:
            filtered[row["reason"]] += 1

    mass_rows: dict[int, list[float]] = {target: [] for target in MASS_COUNTS}
    grav_vals = []
    pur_vals = []
    pmin_vals = []
    snorm_vals = []
    born_vals = []
    born_nonzero = 0
    alpha_vals = []

    for row in rows:
        for target_n, avg, _se, _t in row["mass_summary_rows"]:
            mass_rows[target_n].append(avg)
        grav_vals.append(row["grav_shift"])
        pur_vals.append(row["pur_cl"])
        pmin_vals.append(row["pur_min"])
        snorm_vals.append(row["s_norm"])
        if row.get("born_available", False):
            born_vals.append(row["born_ratio"])
            born_nonzero += row.get("born_nonzero", 0)
        if row["alpha"] is not None:
            alpha_vals.append(row["alpha"])

    mass_summaries = []
    for target_n, vals in mass_rows.items():
        if not vals:
            continue
        avg = sum(vals) / len(vals)
        se = statistics.stdev(vals) / math.sqrt(len(vals)) if len(vals) > 1 else math.nan
        t = avg / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        mass_summaries.append((target_n, avg, se, t))

    alpha_fit = _fit_power_law([n for n, _avg, _se, _t in mass_summaries], [avg for _n, avg, _se, _t in mass_summaries])
    accepted = len(rows)
    born_coverage = accepted / accepted if accepted and born_vals else 0.0
    born_ratio_mean = _mean(born_vals) if born_vals else math.nan
    grav_mean = _mean(grav_vals)
    pur_mean = _mean(pur_vals)
    pmin_mean = _mean(pmin_vals)
    sn_mean = _mean(snorm_vals)

    joint_positive = sum(
        1
        for row in rows
        if math.isfinite(row["grav_shift"]) and row["grav_shift"] > 0 and math.isfinite(row["pur_cl"]) and row["pur_cl"] < 0.96 and row.get("born_ratio", 0.0) > 1e-12
    )

    return {
        "nodes_per_layer": nodes_per_layer,
        "connect_radius": connect_radius,
        "spatial_range": spatial_range,
        "gap": gap,
        "attempted": attempted,
        "accepted": accepted,
        "accepted_rate": accepted / attempted if attempted else 0.0,
        "filtered": sum(filtered.values()),
        "filtered_reasons": filtered,
        "born_coverage": born_coverage,
        "born_ratio_mean": born_ratio_mean,
        "born_nonzero": born_nonzero,
        "grav_mean": grav_mean,
        "pur_cl_mean": pur_mean,
        "pur_min_mean": pmin_mean,
        "s_norm_mean": sn_mean,
        "alpha": alpha_fit[0] if alpha_fit is not None else None,
        "mass_summaries": mass_summaries,
        "joint_positive": joint_positive,
    }


def _fmt_reason_counts(filtered: Counter) -> str:
    if not filtered:
        return "-"
    return ", ".join(f"{k}={v}" for k, v in sorted(filtered.items()))


def main() -> None:
    print("=" * 96)
    print("5D JOINT COVERAGE RE-AUDIT")
    print("  4 spatial dims + 1 causal dim")
    print("  Goal: settle the historical 5D joint pilot by making coverage/accounting explicit")
    print("=" * 96)
    print()
    print(f"  seeds/config: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  fixed mass count for sanity read: {MASS_COUNT_FIXED}")
    print(f"  mass counts: {MASS_COUNTS}")
    print(f"  k-band: {K_BAND}")
    print(f"  Born k: {BORN_K}")
    print("  readout: accepted/filtered seeds, Born coverage, and whether same-family positivity survives")
    print()

    rows = []
    for label, nodes_per_layer, connect_radius, spatial_range in CONFIGS:
        row = measure_config(nodes_per_layer, connect_radius, spatial_range, gap=GAP)
        row["label"] = label
        rows.append(row)

    print("CONFIG SWEEP")
    print(
        f"  {'label':>12s}  {'nodes':>5s}  {'rad':>4s}  {'range':>5s}  {'acc':>5s}  {'filt':>5s}  "
        f"{'born_cov':>8s}  {'born0':>5s}  {'alpha':>7s}  {'grav':>7s}  {'pur_cl':>8s}  verdict"
    )
    print(f"  {'-' * 116}")

    for row in rows:
        born_cov = row["born_coverage"]
        born_ok = row["born_nonzero"]
        if row["accepted"] and row["grav_mean"] > 0 and row["pur_cl_mean"] < 0.96 and born_ok > 0:
            verdict = "NARROW PASS"
        elif row["accepted"] and row["grav_mean"] > 0 and row["pur_cl_mean"] < 0.96:
            verdict = "GRAV+DECOH ONLY"
        elif row["accepted"] and row["grav_mean"] > 0:
            verdict = "GRAV ONLY"
        else:
            verdict = "FILTERED / MARGINAL"

        print(
            f"  {row['label']:>12s}  {row['nodes_per_layer']:5d}  {row['connect_radius']:4.2f}  "
            f"{row['spatial_range']:5.2f}  {_fmt_count(row['accepted'], row['attempted']):>5s}  "
            f"{row['filtered']:5d}  {born_cov:8.2f}  {born_ok:5d}  {_fmt(row['alpha']):>7s}  "
            f"{_fmt(row['grav_mean']):>7s}  {_fmt(row['pur_cl_mean']):>8s}  {verdict}"
        )

    print()
    print("FILTER ACCOUNTING")
    for row in rows:
        print(
            f"  {row['label']}: accepted={row['accepted']}/{row['attempted']}, "
            f"born_cov={row['born_coverage']:.2f}, born_nonzero={row['born_nonzero']}, "
            f"filters={_fmt_reason_counts(row['filtered_reasons'])}"
        )

    print()
    print("MASS-LAW DETAIL")
    for row in rows:
        print(
            f"  {row['label']}: alpha={_fmt(row['alpha'])}, grav={_fmt(row['grav_mean'])}, "
            f"pur_cl={_fmt(row['pur_cl_mean'])}, born_ratio={_fmt(row['born_ratio_mean'])}"
        )
        for target_n, avg, se, t in row["mass_summaries"]:
            print(f"    n={target_n:2d}, shift={avg:+.4f}, SE={se:.4f}, t={t:+.2f}")

    print()
    best = max(rows, key=lambda r: (r["accepted"], r["grav_mean"] if math.isfinite(r["grav_mean"]) else -1e9, -(abs((r["alpha"] or 0.0) - 0.6))))
    print("VERDICT")
    print(
        f"  Best row = {best['label']} at nodes={best['nodes_per_layer']}, "
        f"rad={best['connect_radius']}, range={best['spatial_range']}."
    )
    print(
        f"  Accepted={best['accepted']}/{best['attempted']}, born_cov={best['born_coverage']:.2f}, "
        f"born_nonzero={best['born_nonzero']}, grav={_fmt(best['grav_mean'])}, "
        f"pur_cl={_fmt(best['pur_cl_mean'])}, alpha={_fmt(best['alpha'])}."
    )
    if best["accepted"] and best["grav_mean"] > 0 and best["pur_cl_mean"] < 0.96 and best["born_nonzero"] > 0:
        print("  Conservative headline: a narrow same-family positive survives, but only inside the accepted subset.")
    else:
        print("  Conservative headline: once Born coverage is explicit, the 5D joint story remains a narrow non-closure.")
    print("=" * 96)


if __name__ == "__main__":
    main()
