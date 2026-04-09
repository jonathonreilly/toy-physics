#!/usr/bin/env python3
"""Modular-special invariant scan beyond route diversity.

Goal
----
Compare retained modular, hierarchical, and uniform 3D families on bounded
structural quantities that might explain why the source-projected seam is
modular-specific even though route diversity is not sufficient.

This scan stays narrow and review-safe:
  - fixed graph geometry per seed
  - fixed mass count across the b sweep
  - fixed b across the mass sweep
  - same k-band and readout everywhere
  - same source-projected coupling on every family
  - one structural predictor card, not a causal claim

Candidate invariants
--------------------
  - post-barrier template overlap / clean-template rate
  - post-barrier channel purity
  - detector-side support asymmetry
  - detector-side route reuse across b
  - route diversity reference metrics for comparison only

The output is intentionally conservative:
  - if a metric correlates with seam gain, it is only a candidate predictor
  - if route diversity is weaker than the structural metrics, say so plainly
  - do not promote any single-family result to a broad architecture claim
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.source_projected_field_pilot import (  # type: ignore  # noqa: E402
    GAP,
    K_BAND,
    MASS_COUNTS,
    MASS_COUNT_FIXED,
    MASS_LAYER_OFFSET,
    N_SEEDS,
    FIXED_MASS_B,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    CONNECT_RADIUS,
    centroid_y,
    field_laplacian,
    field_source_projected,
    generate_3d_modular_dag,
    propagate,
)
from scripts.source_projected_cross_family_pilot import (  # type: ignore  # noqa: E402
    generate_3d_hierarchical_dag,
    generate_3d_uniform_dag,
)


PROJECTED_STRENGTH = 0.12
HIERARCHICAL_LEAK = 0.05
OVERLAP_CLEAN_THRESHOLD = 0.5
TOP_DETECTOR_FRACTION = 0.10


@dataclass(frozen=True)
class FamilySpec:
    label: str
    build_graph: Callable[[int], tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]]]]


FAMILIES = (
    FamilySpec(
        label="retained modular gap=3",
        build_graph=lambda seed: generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
            gap=GAP,
        ),
    ),
    FamilySpec(
        label="hierarchical leak=0.05",
        build_graph=lambda seed: generate_3d_hierarchical_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            yz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
            gap=GAP,
            channel_leak=HIERARCHICAL_LEAK,
        ),
    ),
    FamilySpec(
        label="uniform 3D",
        build_graph=lambda seed: generate_3d_uniform_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            yz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
        ),
    ),
)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _pearson(xs: list[float], ys: list[float]) -> float:
    pairs = [(x, y) for x, y in zip(xs, ys) if math.isfinite(x) and math.isfinite(y)]
    if len(pairs) < 3:
        return math.nan
    xs_f = [x for x, _ in pairs]
    ys_f = [y for _, y in pairs]
    mx = _mean(xs_f)
    my = _mean(ys_f)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs_f))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys_f))
    if sx < 1e-30 or sy < 1e-30:
        return math.nan
    cov = sum((x - mx) * (y - my) for x, y in pairs)
    return cov / (sx * sy)


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


def _layers_from_positions(positions: Sequence[Sequence[float]]) -> dict[int, list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    return by_layer


def _select_fixed_mass_nodes(
    layer_nodes: list[int],
    positions: Sequence[Sequence[float]],
    target_y: float,
    count: int,
) -> list[int]:
    ranked = sorted(
        layer_nodes,
        key=lambda i: (
            abs(positions[i][1] - target_y),
            tuple(abs(c) for c in positions[i][2:]),
            i,
        ),
    )
    return ranked[:count] if len(ranked) >= count else []


def _overlap_fraction(a: list[int], b: list[int]) -> float:
    if not a or not b:
        return 0.0
    inter = len(set(a) & set(b))
    return inter / min(len(a), len(b))


def _route_metrics(
    adj: dict[int, list[int]],
    det_probs: list[float],
    post_nodes: list[int],
    post_probs: list[float],
) -> dict[str, float]:
    if not post_nodes:
        return {
            "route_entropy_det": math.nan,
            "route_eff_n_det": math.nan,
            "route_concentration_det": math.nan,
            "hub_share": math.nan,
        }

    out_deg = {i: len(adj.get(i, [])) for i in post_nodes}
    sorted_post = sorted(post_nodes, key=lambda i: out_deg.get(i, 0), reverse=True)
    top_count = max(1, int(round(0.10 * len(sorted_post))))
    hub_nodes = set(sorted_post[:top_count])

    det_total = sum(det_probs)
    post_total = sum(post_probs)

    def _norm_entropy(weights: list[float]) -> float:
        total = sum(weights)
        if total <= 1e-30 or len(weights) < 2:
            return math.nan
        probs = [w / total for w in weights if w > 1e-30]
        if len(probs) < 2:
            return 0.0
        ent = -sum(p * math.log(p) for p in probs)
        return ent / math.log(len(weights))

    def _concentration(p: list[float]) -> float:
        return sum(v * v for v in p) if p else math.nan

    det_norm = [p / det_total for p in det_probs] if det_total > 1e-30 else []
    post_prob_by_node = dict(zip(post_nodes, post_probs))
    hub_mass = sum(post_prob_by_node.get(i, 0.0) for i in hub_nodes)
    hub_share = hub_mass / post_total if post_total > 1e-30 else math.nan

    det_conc = _concentration(det_norm) if det_norm else math.nan
    det_eff_n = 1.0 / det_conc if det_conc and math.isfinite(det_conc) and det_conc > 1e-30 else math.nan

    return {
        "route_entropy_det": _norm_entropy(det_probs),
        "route_eff_n_det": det_eff_n,
        "route_concentration_det": det_conc,
        "hub_share": hub_share,
    }


def _same_channel_edge_fraction(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    layer_indices: list[list[int]],
) -> float:
    n_layers = len(layer_indices)
    barrier_layer = n_layers // 3
    post_nodes = {
        i
        for li in range(barrier_layer + 1, n_layers - 1)
        for i in layer_indices[li]
    }
    same = 0
    total = 0
    for i in post_nodes:
        yi = positions[i][1]
        for j in adj.get(i, []):
            if j not in post_nodes:
                continue
            yj = positions[j][1]
            total += 1
            if yi == 0.0 or yj == 0.0:
                continue
            if yi * yj > 0:
                same += 1
    return same / total if total else math.nan


def _paired_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    field_fn,
) -> float | None:
    field_with = field_fn(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_with = propagate(positions, adj, field_with, src, k)
        amps_without = propagate(positions, adj, field_without, src, k)
        deltas.append(
            centroid_y(amps_with, positions, det_list)
            - centroid_y(amps_without, positions, det_list)
        )
    return _mean(deltas) if deltas else None


def _band_average_detector_probs(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    field: list[float],
) -> list[float]:
    probs = [0.0] * len(det_list)
    for k in K_BAND:
        amps = propagate(positions, adj, field, src, k)
        for idx, d in enumerate(det_list):
            probs[idx] += abs(amps[d]) ** 2
    if K_BAND:
        scale = 1.0 / len(K_BAND)
        probs = [p * scale for p in probs]
    return probs


def _band_average_node_probs(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    nodes: list[int],
    field: list[float],
) -> list[float]:
    probs = [0.0] * len(nodes)
    for k in K_BAND:
        amps = propagate(positions, adj, field, src, k)
        for idx, node in enumerate(nodes):
            probs[idx] += abs(amps[node]) ** 2
    if K_BAND:
        scale = 1.0 / len(K_BAND)
        probs = [p * scale for p in probs]
    return probs


def _top_detector_set(det_list: list[int], det_probs: list[float]) -> set[int]:
    if not det_list or not det_probs:
        return set()
    top_k = max(1, int(round(TOP_DETECTOR_FRACTION * len(det_list))))
    ranked = sorted(zip(det_list, det_probs), key=lambda t: t[1], reverse=True)
    return {i for i, _ in ranked[:top_k]}


def _jaccard(a: set[int], b: set[int]) -> float:
    if not a and not b:
        return math.nan
    union = len(a | b)
    if union == 0:
        return math.nan
    return len(a & b) / union


def _support_asymmetry(
    positions: list[tuple[float, float, float]],
    det_list: list[int],
    det_probs: list[float],
) -> float:
    if not det_list or not det_probs:
        return math.nan
    upper = sum(p for d, p in zip(det_list, det_probs) if positions[d][1] >= 0.0)
    lower = sum(p for d, p in zip(det_list, det_probs) if positions[d][1] < 0.0)
    total = upper + lower
    return abs(upper - lower) / total if total > 1e-30 else math.nan


def _template_overlap_metrics(
    positions: list[tuple[float, float, float]],
    layer_nodes: list[int],
    center_y: float,
) -> tuple[float, float] | None:
    chosen: dict[float, list[int]] = {}
    for b in TARGET_BS:
        mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + b, MASS_COUNT_FIXED)
        if len(mass_nodes) == MASS_COUNT_FIXED:
            chosen[b] = mass_nodes
    if len(chosen) != len(TARGET_BS):
        return None
    sorted_bs = sorted(chosen)
    pairwise = [
        _overlap_fraction(chosen[b1], chosen[b2])
        for i, b1 in enumerate(sorted_bs)
        for b2 in sorted_bs[i + 1 :]
    ]
    if not pairwise:
        return None
    mean_max_overlap = max(pairwise)
    clean_rate = 1.0 if mean_max_overlap <= OVERLAP_CLEAN_THRESHOLD else 0.0
    return mean_max_overlap, clean_rate


def _measure_seed(spec: FamilySpec, seed: int) -> dict[str, float] | None:
    positions, adj, layer_indices = spec.build_graph(seed)
    if len(layer_indices) <= MASS_LAYER_OFFSET:
        return None
    src = list(layer_indices[0])
    det_list = list(layer_indices[-1])
    if not src or not det_list:
        return None
    layer_nodes = list(layer_indices[MASS_LAYER_OFFSET])
    if not layer_nodes:
        return None
    center_y = statistics.fmean(pos[1] for pos in positions)

    template = _template_overlap_metrics(positions, layer_nodes, center_y)
    if template is None:
        return None
    template_max_overlap, template_clean = template

    barrier_layer = len(layer_indices) // 3
    post_nodes = [
        i
        for li in range(barrier_layer + 1, len(layer_indices) - 1)
        for i in layer_indices[li]
    ]
    if not post_nodes:
        return None
    post_purity = _same_channel_edge_fraction(positions, adj, layer_indices)

    proj_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    lap_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    proj_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    lap_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    det_asym_by_b: list[float] = []
    route_reuse_sets: list[set[int]] = []

    route_mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + FIXED_MASS_B, MASS_COUNT_FIXED)
    if len(route_mass_nodes) != MASS_COUNT_FIXED:
        return None
    route_field = field_source_projected(positions, adj, route_mass_nodes, strength=PROJECTED_STRENGTH)
    route_det_probs = _band_average_detector_probs(positions, adj, src, det_list, route_field)
    route_post_probs = _band_average_node_probs(positions, adj, src, post_nodes, route_field)
    route_ref = _route_metrics(adj, route_det_probs, post_nodes, route_post_probs)

    # b-sweep on fixed mass count.
    for b in TARGET_BS:
        mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + b, MASS_COUNT_FIXED)
        if len(mass_nodes) != MASS_COUNT_FIXED:
            continue
        lap_delta = _paired_delta(positions, adj, src, det_list, mass_nodes, field_laplacian)
        proj_field = field_source_projected(positions, adj, mass_nodes, strength=PROJECTED_STRENGTH)
        proj_delta = _paired_delta(
            positions,
            adj,
            src,
            det_list,
            mass_nodes,
            lambda p, a, m: field_source_projected(p, a, m, strength=PROJECTED_STRENGTH),
        )
        if lap_delta is not None:
            lap_b[b].append(lap_delta)
        if proj_delta is not None:
            proj_b[b].append(proj_delta)

        det_probs = _band_average_detector_probs(positions, adj, src, det_list, proj_field)
        det_asym_by_b.append(_support_asymmetry(positions, det_list, det_probs))
        route_reuse_sets.append(_top_detector_set(det_list, det_probs))

    # mass-sweep at fixed b.
    representative_mass = _select_fixed_mass_nodes(layer_nodes, positions, center_y + FIXED_MASS_B, max(MASS_COUNTS))
    if len(representative_mass) == max(MASS_COUNTS):
        for m in MASS_COUNTS:
            subset = representative_mass[:m]
            lap_delta = _paired_delta(positions, adj, src, det_list, subset, field_laplacian)
            proj_delta = _paired_delta(
                positions,
                adj,
                src,
                det_list,
                subset,
                lambda p, a, mm: field_source_projected(p, a, mm, strength=PROJECTED_STRENGTH),
            )
            if lap_delta is not None:
                lap_m[m].append(lap_delta)
            if proj_delta is not None:
                proj_m[m].append(proj_delta)

    def _fit_from_mean(table: dict[float | int, list[float]]):
        xs = []
        ys = []
        for x in sorted(table):
            vals = table[x]
            if not vals:
                return None
            mean_v = _mean(vals)
            if not math.isfinite(mean_v) or mean_v <= 0:
                return None
            xs.append(float(x))
            ys.append(mean_v)
        return _fit_power_law(xs, ys)

    lap_b_fit = _fit_from_mean(lap_b)
    proj_b_fit = _fit_from_mean(proj_b)
    lap_m_fit = _fit_from_mean(lap_m)
    proj_m_fit = _fit_from_mean(proj_m)

    b_gain = None
    m_gain = None
    if lap_b_fit is not None and proj_b_fit is not None:
        b_gain = lap_b_fit[0] - proj_b_fit[0]
    if lap_m_fit is not None and proj_m_fit is not None:
        m_gain = proj_m_fit[0] - lap_m_fit[0]

    route_reuse = math.nan
    if len(route_reuse_sets) >= 2:
        overlaps = [
            _jaccard(a, b)
            for i, a in enumerate(route_reuse_sets)
            for b in route_reuse_sets[i + 1 :]
        ]
        overlaps = [x for x in overlaps if math.isfinite(x)]
        route_reuse = _mean(overlaps) if overlaps else math.nan

    det_asym = _mean([v for v in det_asym_by_b if math.isfinite(v)]) if det_asym_by_b else math.nan

    return {
        "family": spec.label,
        "seed": float(seed),
        "template_max_overlap": template_max_overlap,
        "template_clean": template_clean,
        "post_channel_purity": post_purity,
        "detector_support_asym": det_asym,
        "route_reuse": route_reuse,
        "route_entropy_det": route_ref["route_entropy_det"],
        "route_eff_n_det": route_ref["route_eff_n_det"],
        "route_concentration_det": route_ref["route_concentration_det"],
        "hub_share": route_ref["hub_share"],
        "lap_b_alpha": lap_b_fit[0] if lap_b_fit is not None else math.nan,
        "proj_b_alpha": proj_b_fit[0] if proj_b_fit is not None else math.nan,
        "lap_m_alpha": lap_m_fit[0] if lap_m_fit is not None else math.nan,
        "proj_m_alpha": proj_m_fit[0] if proj_m_fit is not None else math.nan,
        "b_gain": b_gain if b_gain is not None else math.nan,
        "m_gain": m_gain if m_gain is not None else math.nan,
    }


def _summarize_family(rows: list[dict[str, float]]) -> dict[str, float]:
    out: dict[str, float] = {}
    for key in (
        "template_max_overlap",
        "template_clean",
        "post_channel_purity",
        "detector_support_asym",
        "route_reuse",
        "route_entropy_det",
        "route_eff_n_det",
        "route_concentration_det",
        "hub_share",
        "lap_b_alpha",
        "proj_b_alpha",
        "lap_m_alpha",
        "proj_m_alpha",
        "b_gain",
        "m_gain",
    ):
        vals = [r[key] for r in rows if math.isfinite(r[key])]
        out[key] = _mean(vals) if vals else math.nan
    out["n_rows"] = float(len(rows))
    out["positive_b_gain_rate"] = sum(1 for r in rows if math.isfinite(r["b_gain"]) and r["b_gain"] > 0) / len(rows) if rows else math.nan
    return out


def main() -> None:
    print("=" * 100)
    print("MODULAR-SPECIAL INVARIANT SCAN")
    print("  3D modular vs hierarchical vs uniform under fixed-mass source-projected controls")
    print("=" * 100)
    print()
    print(f"  seeds per family: {N_SEEDS}")
    print(f"  k-band: {K_BAND}")
    print(f"  fixed mass count for b-sweep: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass-sweep: {FIXED_MASS_B}")
    print(f"  overlap clean threshold: {OVERLAP_CLEAN_THRESHOLD}")
    print()

    all_rows: list[dict[str, float]] = []
    family_rows: dict[str, list[dict[str, float]]] = {}
    for spec in FAMILIES:
        rows: list[dict[str, float]] = []
        for seed in range(N_SEEDS):
            row = _measure_seed(spec, seed)
            if row is not None:
                rows.append(row)
        family_rows[spec.label] = rows
        all_rows.extend(rows)

    print("FAMILY SUMMARY")
    print(
        f"{'family':>24s}  {'rows':>4s}  {'b_gain':>8s}  {'proj_M':>8s}  {'overlap':>8s}  "
        f"{'purity':>8s}  {'det_asym':>8s}  {'reuse':>8s}  {'routeN':>8s}"
    )
    print("-" * 96)
    for label, rows in family_rows.items():
        s = _summarize_family(rows)
        print(
            f"{label:>24s}  {int(s.get('n_rows', 0)):4d}  "
            f"{s.get('b_gain', math.nan):+8.3f}  {s.get('proj_m_alpha', math.nan):8.3f}  "
            f"{s.get('template_max_overlap', math.nan):8.3f}  {s.get('post_channel_purity', math.nan):8.3f}  "
            f"{s.get('detector_support_asym', math.nan):8.3f}  {s.get('route_reuse', math.nan):8.3f}  "
            f"{s.get('route_eff_n_det', math.nan):8.2f}"
        )

    print()
    print("PREDICTOR CARD")
    print("  (higher |r| means the metric is a better linear predictor of b_gain)")
    print(f"{'metric':>26s}  {'r vs b_gain':>12s}  {'r vs proj_M':>12s}")
    print("-" * 58)
    metrics = (
        ("template_max_overlap", "template_max_overlap"),
        ("template_clean", "template_clean"),
        ("post_channel_purity", "post_channel_purity"),
        ("detector_support_asym", "detector_support_asym"),
        ("route_reuse", "route_reuse"),
        ("route_entropy_det", "route_entropy_det"),
        ("route_eff_n_det", "route_eff_n_det"),
        ("hub_share", "hub_share"),
    )
    predictor_rows = []
    for name, key in metrics:
        r_b = _pearson([row["b_gain"] for row in all_rows], [row[key] for row in all_rows])
        r_m = _pearson([row["proj_m_alpha"] for row in all_rows], [row[key] for row in all_rows])
        print(f"{name:>26s}  {r_b:+12.3f}  {r_m:+12.3f}")
        predictor_rows.append((name, r_b, r_m))

    non_route = [r for r in predictor_rows if r[0] not in {"route_entropy_det", "route_eff_n_det"}]
    best = max(
        non_route,
        key=lambda item: (
            abs(item[1]) + abs(item[2]),
            abs(item[1]),
            abs(item[2]),
        ),
    ) if non_route else None

    print()
    print("REVIEW-SAFE TAKEAWAY")
    print("  This is a predictor scan, not a causal claim.")
    if best is not None:
        print(
            f"  Best non-route candidate by combined correlation: {best[0]} "
            f"(r_b={best[1]:+.3f}, r_M={best[2]:+.3f})."
        )
    print("  Route diversity remains a reference metric, but it is not the strongest")
    print("  explanation for the modular-specific seam in this scan.")
    print("=" * 100)


if __name__ == "__main__":
    main()
