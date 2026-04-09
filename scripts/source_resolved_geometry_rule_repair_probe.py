#!/usr/bin/env python3
"""Generated-family geometry-rule repair probe.

Question:
  The discriminator says the current generated-family bridge is geometry-limited.
  Can a single geometry-construction change widen detector support enough for the
  weak-field sign and mass-scaling read to improve, without changing the field
  rule itself?

Scope:
  - compact generated 3D DAG family
  - retained k-nearest floor bridge as the baseline control
  - one geometry-rule repair: retained kNN-floor bridge + adaptive sector fan
  - exact zero-source reduction check
  - one field rule only: static Green kernel
  - observables: TOWARD count, detector effective support N_eff,
    detector support fraction, and centroid-shift exponent

This is intentionally geometry-only. It does not compare static vs wavefield
rules. The point is to test whether widening the generated support structure
helps the retained weak-field lane more than further field tuning.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.causal_field_gravity import centroid_y, generate_3d_dag, propagate  # noqa: E402


N_LAYERS = 16
NODES_PER_LAYER = 24
Y_RANGE = 10.0
CONNECT_RADIUS = 3.2
N_SEEDS = 4
K = 5.0
TARGET_Y = 3.0
MASS_RADIUS = 2.5
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08

K_NEAREST = 3
MIN_EDGES = 5
SECTOR_FLOOR = 9


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    adj: dict[int, list[int]]
    layers: list[list[int]]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _stdev(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) >= 2 else math.nan


def _fit_power(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def _entropy_and_support(probs: list[float]) -> tuple[float, float, float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    peak = max(norm)
    top10 = sum(sorted(norm, reverse=True)[: min(10, len(norm))])
    support_frac = sum(1 for p in norm if p >= 0.01 * peak) / len(norm)
    return h, eff, top10, support_frac


def _select_mass_nodes(
    positions: list[tuple[float, float, float]],
    layer_nodes: list[int],
    cy: float,
) -> list[int]:
    target_y = cy + TARGET_Y
    ranked = sorted(
        layer_nodes,
        key=lambda i: (
            (positions[i][1] - target_y) ** 2 + positions[i][2] ** 2,
            abs(positions[i][1] - target_y),
        ),
    )
    chosen: list[int] = []
    for idx in ranked:
        if abs(positions[idx][1] - target_y) <= MASS_RADIUS:
            chosen.append(idx)
    return chosen[:4] if len(chosen) >= 4 else ranked[:4]


def _family(seed: int) -> Family:
    positions, adj, layers = generate_3d_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=NODES_PER_LAYER,
        yz_range=Y_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=seed * 19 + 7,
    )
    return Family(positions=positions, adj=adj, layers=layers)


def _augment_knn_floor(family: Family) -> Family:
    positions = family.positions
    layers = family.layers
    adj: dict[int, list[int]] = {i: list(nbs) for i, nbs in family.adj.items()}

    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        for src in layers[layer]:
            sx, sy, sz = positions[src]
            ranked: list[tuple[float, int]] = []
            for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, dst))
            ranked.sort(key=lambda item: item[0])
            selected = list(dict.fromkeys(adj.get(src, [])))
            for _, dst in ranked[:K_NEAREST]:
                if dst not in selected:
                    selected.append(dst)
            for _, dst in ranked:
                if len(selected) >= MIN_EDGES:
                    break
                if dst not in selected:
                    selected.append(dst)
            adj[src] = selected

    return Family(positions=positions, adj=adj, layers=layers)


def _augment_sector_repair(family: Family) -> Family:
    """Geometry-only repair layered on an existing bridge family.

    Use the actual positions to add one nearest child in each adaptive
    3x3 sector of the next layer, then backfill to a nine-edge floor.

    The sectors are adaptive in the local y/z spread, so the rule can widen
    support without being tied to grid labels. The input family should already
    carry the retained kNN-floor bridge.
    """

    positions = family.positions
    layers = family.layers
    adj: dict[int, list[int]] = {i: list(nbs) for i, nbs in family.adj.items()}

    def sector_key(values: list[float], v: float) -> int:
        if len(values) < 3:
            return 1
        ordered = sorted(values)
        t1 = ordered[len(ordered) // 3]
        t2 = ordered[(2 * len(ordered)) // 3]
        if v <= t1:
            return 0
        if v <= t2:
            return 1
        return 2

    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        for src in layers[layer]:
            sx, sy, sz = positions[src]
            dy_offsets = [dy - sy for (_, dy, _) in dst_positions]
            dz_offsets = [dz - sz for (_, _, dz) in dst_positions]
            sector_best: dict[tuple[int, int], tuple[float, int]] = {}
            ranked: list[tuple[float, int]] = []
            for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, dst))
                key = (sector_key(dy_offsets, dy - sy), sector_key(dz_offsets, dz - sz))
                prev = sector_best.get(key)
                if prev is None or dist2 < prev[0]:
                    sector_best[key] = (dist2, dst)

            selected = [dst for _, dst in sorted(sector_best.values(), key=lambda item: item[0])]
            for _, dst in sorted(ranked, key=lambda item: item[0]):
                if len(selected) >= SECTOR_FLOOR:
                    break
                if dst not in selected:
                    selected.append(dst)
            adj[src] = selected

    return Family(positions=positions, adj=adj, layers=layers)


def _green_field(
    positions: list[tuple[float, float, float]],
    mass_ids: list[int],
    weights: list[float],
    strength: float,
) -> list[float]:
    field = [0.0] * len(positions)
    source_pos = [positions[i] for i in mass_ids]
    if not source_pos:
        return field
    for i, (x, y, z) in enumerate(positions):
        val = 0.0
        for w, (mx, my, mz) in zip(weights, source_pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
            val += w * strength * math.exp(-GREEN_MU * r) / r
        field[i] = val / len(source_pos)
    return field


def _field_abs_max(field: list[float]) -> float:
    return max(abs(v) for v in field) if field else 0.0


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _detector_metrics(probs: list[float]) -> tuple[float, float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0
    _, eff, top10, support_frac = _entropy_and_support(probs)
    return eff, top10, support_frac


def _evaluate_family(family: Family, gain: float) -> tuple[list[dict[str, float]], float]:
    positions = family.positions
    adj = family.adj
    layers = family.layers
    det = layers[-1]
    all_ys = [y for _, y, _ in positions]
    cy = sum(all_ys) / len(all_ys)
    mass_ids = _select_mass_nodes(positions, layers[len(layers) // 2], cy)
    if not mass_ids:
        return [], 1.0

    free = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
    z_free = centroid_y(free, positions, det)

    zero_field = [0.0] * len(positions)
    zero_amps = propagate(positions, adj, zero_field, layers[0], K)
    zero_shift = centroid_y(zero_amps, positions, det) - z_free

    rows: list[dict[str, float]] = []
    for s in SOURCE_STRENGTHS:
        weights = [1.0 / len(mass_ids)] * len(mass_ids)
        field = [gain * v for v in _green_field(positions, mass_ids, weights, s)]
        amps = propagate(positions, adj, field, layers[0], K)
        delta = centroid_y(amps, positions, det) - z_free
        det_probs = [abs(amps[d]) ** 2 for d in det]
        eff_support, _, support_frac = _detector_metrics(det_probs)
        rows.append(
            {
                "s": s,
                "delta": delta,
                "abs_delta": abs(delta),
                "toward": 1.0 if delta > 0 else 0.0,
                "eff_support": eff_support,
                "support_frac": support_frac,
                "zero_shift": zero_shift,
            }
        )

    return rows, zero_shift


def _summarize(rows: list[dict[str, float]], zero_shift: float) -> dict[str, float]:
    deltas = [r["delta"] for r in rows]
    effs = [r["eff_support"] for r in rows]
    sups = [r["support_frac"] for r in rows]
    toward = sum(1 for d in deltas if d > 0)
    alpha = _fit_power([r["s"] for r in rows], [abs(r["delta"]) for r in rows])
    return {
        "delta_mean": _mean(deltas),
        "toward_count": toward,
        "total": len(deltas),
        "eff_support": _mean(effs),
        "support_frac": _mean(sups),
        "zero_shift": abs(zero_shift),
        "alpha": alpha,
    }


def main() -> None:
    print("=" * 104)
    print("SOURCE-RESOLVED GEOMETRY-RULE REPAIR PROBE")
    print("  compact generated DAG family, geometry-sector repair vs kNN-floor bridge")
    print("=" * 104)
    print(f"family seeds=0..{N_SEEDS - 1}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, connect_radius={CONNECT_RADIUS}")
    print(f"baseline bridge: k-nearest floor augmentation (k={K_NEAREST}, min_edges={MIN_EDGES})")
    print(f"repair bridge: adaptive sector stencil + floor={SECTOR_FLOOR}")
    print(f"static Green kernel: exp(-mu r)/(r+eps), mu={GREEN_MU:.2f}, eps={GREEN_EPS:.2f}")
    print(f"source strengths={SOURCE_STRENGTHS}")
    print(f"field target max={FIELD_TARGET_MAX}")
    print("observables: zero-source reduction, centroid sign counts, F~M exponent, detector N_eff")
    print("diagnostic: does a geometry repair widen support enough to improve the weak-field read?")
    print()

    per_case_results: dict[str, list[dict[str, float]]] = {}
    per_case_zero: dict[str, float] = {}

    for seed in range(N_SEEDS):
        base = _family(seed)
        tweak = _augment_knn_floor(base)
        repair = _augment_sector_repair(tweak)
        all_ys = [y for _, y, _ in tweak.positions]
        cy = sum(all_ys) / len(all_ys)
        mass_ids = _select_mass_nodes(tweak.positions, tweak.layers[len(tweak.layers) // 2], cy)
        gain_probe_strength = max(SOURCE_STRENGTHS)
        ref_raw = _green_field(tweak.positions, mass_ids, [1.0 / len(mass_ids)] * len(mass_ids), gain_probe_strength)
        base_gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0
        for family_label, family in [("baseline", tweak), ("repair", repair)]:
            rows, zero_shift = _evaluate_family(family, base_gain)
            per_case_results.setdefault(family_label, []).extend(rows)
            per_case_zero[family_label] = max(per_case_zero.get(family_label, 0.0), abs(zero_shift))
            summary = _summarize(rows, zero_shift)
            alpha_str = f"{summary['alpha']:.3f}" if summary["alpha"] is not None else "n/a"
            print(
                f"seed={seed} {family_label:>8s} "
                f"zero={summary['zero_shift']:.3e} "
                f"TOWARD={summary['toward_count']}/{summary['total']} "
                f"F~M={alpha_str} N_eff={summary['eff_support']:.2f}"
            )

    print()
    print("SUMMARY")
    for family_label in ["baseline", "repair"]:
        rows = per_case_results[family_label]
        summary = _summarize(rows, per_case_zero[family_label])
        alpha_str = f"{summary['alpha']:.3f}" if summary["alpha"] is not None else "n/a"
        print(
            f"{family_label:>8s}  zero={summary['zero_shift']:.3e}  "
            f"TOWARD={summary['toward_count']}/{summary['total']}  "
            f"F~M={alpha_str}  N_eff={summary['eff_support']:.2f}  "
            f"support_frac={summary['support_frac']:.3f}"
        )

    base = _summarize(per_case_results["baseline"], per_case_zero["baseline"])
    repair = _summarize(per_case_results["repair"], per_case_zero["repair"])
    delta_toward = repair["toward_count"] - base["toward_count"]
    delta_neff = repair["eff_support"] - base["eff_support"]
    base_alpha = base["alpha"]
    repair_alpha = repair["alpha"]

    print()
    print("REPAIR DELTA")
    base_alpha_str = f"{base_alpha:.3f}" if base_alpha is not None else "n/a"
    repair_alpha_str = f"{repair_alpha:.3f}" if repair_alpha is not None else "n/a"
    print(
        f"  delta_TOWARD={delta_toward:+d}  delta_N_eff={delta_neff:+.2f}  "
        f"baseline_alpha={base_alpha_str}  repair_alpha={repair_alpha_str}"
    )

    print()
    print("SAFE READ")
    print("  - The baseline kNN-floor bridge is the retained control.")
    print("  - The repair is only interesting if it widens support and improves")
    print("    the weak-field sign or mass-law read without a field-rule change.")
    print("  - If support broadens but sign and F~M do not improve, the family is")
    print("    still geometry-limited, just with a wider bottleneck.")
    print("  - If the repair worsens both support and sign, that is a clean no-go")
    print("    for this geometry-rule idea on the compact generated family.")


if __name__ == "__main__":
    main()
