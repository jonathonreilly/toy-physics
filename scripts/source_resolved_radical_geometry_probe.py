#!/usr/bin/env python3
"""Radical generated-family geometry probe.

Question:
  Can a materially different geometry construction widen downstream support
  enough for the retained exact-lattice wavefield mechanism to matter on the
  generated family?

Scope:
  - compact generated 3D DAG family
  - retained kNN-floor bridge as the baseline geometry
  - radical downstream-reach fan as the tested geometry construction
  - static Green vs wavefield on each geometry
  - exact zero-source reduction check
  - detector effective support N_eff
  - mass-law fit F~M across the source ladder
  - narrow geometry-vs-field discriminator from the geometry delta

The new geometry rule is intentionally different from the earlier repairs:

  - do not just widen local z sectors
  - do not just add another small fan on top of kNN
  - instead, use downstream detector reach as the geometry selector and pick
    children that maximize downstream coverage while still preserving a floor

This keeps the field rule close to the retained exact-lattice controls while
changing the geometry construction itself.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts import source_resolved_generated_wavefield_bridge as base  # noqa: E402


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

K_NEAREST = 3
MIN_EDGES = 5
REACH_FAN_BINS = 5
REACH_FAN_FLOOR = 10


Family = base.Family  # type: ignore[attr-defined]


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
    fam = base._family(seed)  # type: ignore[attr-defined]
    return Family(positions=fam.positions, adj=fam.adj, layers=fam.layers)


def _augment_knn_floor(family: Family) -> Family:
    aug = base._augment_knn_floor(base.Family(family.positions, family.adj, family.layers))  # type: ignore[attr-defined]
    return Family(positions=aug.positions, adj=aug.adj, layers=aug.layers)


def _detector_reach_sets(family: Family) -> dict[int, set[int]]:
    """How many detector nodes can each node reach in the baseline geometry?"""

    layers = family.layers
    adj = family.adj
    reach: dict[int, set[int]] = {i: set() for layer in layers for i in layer}
    detector = set(layers[-1])
    for i in layers[-1]:
        reach[i] = {i}

    for layer in range(len(layers) - 2, -1, -1):
        for i in layers[layer]:
            acc: set[int] = set()
            for j in adj.get(i, []):
                acc.update(reach.get(j, set()))
            if i in detector:
                acc.add(i)
            reach[i] = acc
    return reach


def _augment_downstream_reach_fan(family: Family) -> Family:
    positions = family.positions
    layers = family.layers
    base_adj = family.adj
    adj: dict[int, list[int]] = {i: list(nbs) for i, nbs in base_adj.items()}
    reach_sets = _detector_reach_sets(family)

    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        for src in layers[layer]:
            sx, sy, sz = positions[src]
            scored: list[tuple[int, float, float, int]] = []
            for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                reach = len(reach_sets.get(dst, set()))
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                dz_off = abs(dz - sz)
                scored.append((reach, dist2, dz_off, dst))

            selected = list(dict.fromkeys(adj.get(src, [])))

            # Split the candidate set into downstream-reach bins so the geometry
            # deliberately keeps a wide support footprint instead of only chasing
            # local nearest neighbors.
            scored_sorted = sorted(scored, key=lambda item: (item[0], -item[1]), reverse=True)
            bins: list[list[tuple[int, float, float, int]]] = []
            if scored_sorted:
                bin_size = max(1, len(scored_sorted) // REACH_FAN_BINS)
                for i in range(0, len(scored_sorted), bin_size):
                    bins.append(scored_sorted[i : i + bin_size])

            for bucket in bins[:REACH_FAN_BINS]:
                best = min(bucket, key=lambda item: (item[1], item[2], -item[0]))
                if best[3] not in selected:
                    selected.append(best[3])

            # Backfill to a floor using downstream reach first, geometry second.
            for reach, dist2, _, dst in sorted(scored, key=lambda item: (-item[0], item[1], item[2])):
                if len(selected) >= REACH_FAN_FLOOR:
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
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + base.GREEN_EPS  # type: ignore[attr-defined]
            val += w * strength * math.exp(-base.GREEN_MU * r) / r  # type: ignore[attr-defined]
        field[i] = val / len(source_pos)
    return field


def _field_abs_max(field: list[float]) -> float:
    return max(abs(v) for v in field) if field else 0.0


def _same_layer_neighbors(family: Family) -> dict[int, list[int]]:
    neighbors: dict[int, list[int]] = {}
    positions = family.positions
    for layer in family.layers:
        for i in layer:
            sx, sy, sz = positions[i]
            ranked: list[tuple[float, int]] = []
            for j in layer:
                if j == i:
                    continue
                dx, dy, dz = positions[j]
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, j))
            ranked.sort(key=lambda item: item[0])
            neighbors[i] = [j for _, j in ranked[: base.WAVE_NEIGHBOR_K]]  # type: ignore[attr-defined]
    return neighbors


def _wavefield_field(
    family: Family,
    adj: dict[int, list[int]],
    mass_ids: list[int],
    weights: list[float],
    strength: float,
) -> list[float]:
    causal = _causal_field(family.positions, adj, mass_ids, weights, strength)
    neighbors = _same_layer_neighbors(family)
    field = causal[:]
    for i in range(len(field)):
        nbs = neighbors.get(i, [])
        if not nbs:
            continue
        neigh_mean = sum(causal[j] for j in nbs) / len(nbs)
        field[i] = base.WAVE_BLEND * causal[i] + (1.0 - base.WAVE_BLEND) * neigh_mean  # type: ignore[attr-defined]
    return field


def _causal_field(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_ids: list[int],
    weights: list[float],
    strength: float,
) -> list[float]:
    n = len(positions)
    order = base._topo_order(adj, n)  # type: ignore[attr-defined]
    green = _green_field(positions, mass_ids, weights, strength)
    field = [0.0] * n
    parents: dict[int, list[int]] = {}
    for src, nbs in adj.items():
        for dst in nbs:
            parents.setdefault(dst, []).append(src)

    mass_set = set(mass_ids)
    for i in order:
        if i in mass_set:
            field[i] = green[i]
            continue
        ps = parents.get(i, [])
        if not ps:
            field[i] = green[i]
            continue
        parent_mean = sum(field[p] for p in ps) / len(ps)
        field[i] = base.CAUSAL_MIX * parent_mean + (1.0 - base.CAUSAL_MIX) * green[i]  # type: ignore[attr-defined]
    return field


def _detector_metrics(probs: list[float]) -> tuple[float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0
    _, eff, _, _ = _entropy_and_support(probs)
    return eff, total


def _evaluate_family(family: Family, mode: str) -> tuple[list[dict[str, float]], float]:
    positions = family.positions
    adj = family.adj
    layers = family.layers
    det = layers[-1]
    all_ys = [y for _, y, _ in positions]
    cy = sum(all_ys) / len(all_ys)
    mass_ids = _select_mass_nodes(positions, layers[len(layers) // 2], cy)
    if not mass_ids:
        return [], 1.0

    gain_probe_strength = max(SOURCE_STRENGTHS)
    ref_raw = _green_field(positions, mass_ids, [1.0 / len(mass_ids)] * len(mass_ids), gain_probe_strength)
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    free = base.propagate(positions, adj, [0.0] * len(positions), layers[0], K)  # type: ignore[attr-defined]
    z_free = base.centroid_y(free, positions, det)  # type: ignore[attr-defined]

    zero_field = [0.0] * len(positions)
    zero_amps = base.propagate(positions, adj, zero_field, layers[0], K)  # type: ignore[attr-defined]
    zero_shift = base.centroid_y(zero_amps, positions, det) - z_free  # type: ignore[attr-defined]

    rows: list[dict[str, float]] = []
    for s in SOURCE_STRENGTHS:
        base_weights = [1.0 / len(mass_ids)] * len(mass_ids)
        field0 = [gain * v for v in _green_field(positions, mass_ids, base_weights, s)]
        amps0 = base.propagate(positions, adj, field0, layers[0], K)  # type: ignore[attr-defined]
        cluster_power = [abs(amps0[i]) ** 2 for i in mass_ids]
        weights_sc = base._normalize_weights(cluster_power)  # type: ignore[attr-defined]

        if mode == "static":
            field = [gain * v for v in _green_field(positions, mass_ids, weights_sc, s)]
        elif mode == "wavefield":
            field = [gain * v for v in _wavefield_field(family, adj, mass_ids, weights_sc, s)]
        else:
            raise ValueError(f"unknown mode: {mode}")

        amps = base.propagate(positions, adj, field, layers[0], K)  # type: ignore[attr-defined]
        delta = base.centroid_y(amps, positions, det) - z_free  # type: ignore[attr-defined]
        det_probs = [abs(amps[d]) ** 2 for d in det]
        eff_support, _ = _detector_metrics(det_probs)
        rows.append(
            {
                "s": s,
                "delta": delta,
                "abs_delta": abs(delta),
                "toward": 1.0 if delta > 0 else 0.0,
                "eff_support": eff_support,
                "zero_shift": zero_shift,
            }
        )

    return rows, zero_shift


def _summarize(rows: list[dict[str, float]], zero_shift: float) -> dict[str, float]:
    deltas = [r["delta"] for r in rows]
    effs = [r["eff_support"] for r in rows]
    toward = sum(1 for d in deltas if d > 0)
    alpha = _fit_power([r["s"] for r in rows], [abs(r["delta"]) for r in rows])
    return {
        "delta_mean": _mean(deltas),
        "delta_se": _stdev(deltas) / math.sqrt(len(deltas)) if len(deltas) >= 2 else 0.0,
        "toward_count": toward,
        "total": len(deltas),
        "eff_support": _mean(effs),
        "zero_shift": abs(zero_shift),
        "alpha": alpha,
    }


def main() -> None:
    print("=" * 108)
    print("SOURCE-RESOLVED RADICAL GEOMETRY PROBE")
    print("  generated-family downstream-reach fan vs retained kNN-floor bridge")
    print("=" * 108)
    print(f"family seeds=0..{N_SEEDS - 1}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, connect_radius={CONNECT_RADIUS}")
    print(f"baseline bridge: k-nearest floor augmentation (k={K_NEAREST}, min_edges={MIN_EDGES})")
    print(f"radical geometry: downstream-reach fan (bins={REACH_FAN_BINS}, floor={REACH_FAN_FLOOR})")
    print("field modes: static Green vs wavefield")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"field target max: {FIELD_TARGET_MAX}")
    print("observables: zero-source reduction, centroid sign counts, F~M exponent, detector N_eff")
    print("diagnostic: geometry-rule delta from bridge to reach-fan")
    print()

    per_case_results: dict[tuple[str, str], list[dict[str, float]]] = {}
    per_case_zero: dict[tuple[str, str], float] = {}

    for seed in range(N_SEEDS):
        base_family = _family(seed)
        bridge_family = _augment_knn_floor(base_family)
        radical_family = _augment_downstream_reach_fan(base_family)
        for family_label, family in [("bridge", bridge_family), ("radical", radical_family)]:
            for mode in ["static", "wavefield"]:
                rows, zero_shift = _evaluate_family(family, mode)
                key = (family_label, mode)
                per_case_results.setdefault(key, []).extend(rows)
                per_case_zero[key] = max(per_case_zero.get(key, 0.0), abs(zero_shift))
                summary = _summarize(rows, zero_shift)
                alpha_str = f"{summary['alpha']:.3f}" if summary["alpha"] is not None else "n/a"
                print(
                    f"seed={seed} {family_label:>8s}/{mode:<9s} "
                    f"zero={summary['zero_shift']:.3e} "
                    f"TOWARD={summary['toward_count']}/{summary['total']} "
                    f"F~M={alpha_str} N_eff={summary['eff_support']:.2f}"
                )

    print()
    print("SUMMARY")
    for family_label in ["bridge", "radical"]:
        for mode in ["static", "wavefield"]:
            key = (family_label, mode)
            rows = per_case_results[key]
            summary = _summarize(rows, per_case_zero[key])
            alpha_str = f"{summary['alpha']:.3f}" if summary["alpha"] is not None else "n/a"
            print(
                f"{family_label:>8s}/{mode:<9s}  zero={summary['zero_shift']:.3e}  "
                f"TOWARD={summary['toward_count']}/{summary['total']}  "
                f"F~M={alpha_str}  N_eff={summary['eff_support']:.2f}"
            )

    print()
    print("GEOMETRY DELTA")
    for mode in ["static", "wavefield"]:
        bridge_rows = per_case_results[("bridge", mode)]
        radical_rows = per_case_results[("radical", mode)]
        bridge_summary = _summarize(bridge_rows, per_case_zero[("bridge", mode)])
        radical_summary = _summarize(radical_rows, per_case_zero[("radical", mode)])
        delta_toward = radical_summary["toward_count"] - bridge_summary["toward_count"]
        delta_neff = radical_summary["eff_support"] - bridge_summary["eff_support"]
        delta_alpha = (
            (radical_summary["alpha"] or math.nan) - (bridge_summary["alpha"] or math.nan)
            if radical_summary["alpha"] is not None and bridge_summary["alpha"] is not None
            else math.nan
        )
        print(
            f"  {mode:>9s}: delta_TOWARD={delta_toward:+d}  "
            f"delta_N_eff={delta_neff:+.2f}  delta_F~M={delta_alpha:+.3f}"
        )

    print()
    print("SAFE READ")
    print("  - The retained kNN-floor bridge remains the baseline control.")
    print("  - The downstream-reach fan is the new geometry rule, designed to")
    print("    target support width rather than local support repairs.")
    print("  - If the fan improves sign and detector support while keeping F~M near 1,")
    print("    then the wavefield lane is becoming geometry-transfer relevant.")
    print("  - If it only reshuffles support without improving the weak-field law,")
    print("    this is a bounded no-go for this radical geometry rule.")


if __name__ == "__main__":
    main()
