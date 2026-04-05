#!/usr/bin/env python3
"""Generated-family wavefield transfer v2 probe.

Question:
  Can a geometry-rule change that widens detector support let the retained
  exact-lattice wavefield mechanism matter on the generated family?

Scope:
  - compact generated 3D DAG family
  - retained kNN-floor bridge as the baseline geometry
  - new z-spread stencil geometry rule as the tested modification
  - static Green vs wavefield on each geometry
  - exact zero-source reduction check
  - detector effective support N_eff
  - mass-law fit F~M across the source ladder
  - narrow geometry-vs-field discriminator from the geometry delta

This probe is intentionally narrow. It does not try to close generated-family
physics. It asks only whether a geometry-rule change can widen the detector
support enough for the wavefield update to become more relevant than on the
current retained bridge family.
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
Z_SPREAD_BUCKETS = 5
Z_SPREAD_FLOOR = 7


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


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _entropy_and_support(probs: list[float]) -> tuple[float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    return h, eff


def _detector_metrics(probs: list[float]) -> tuple[float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0
    _, eff = _entropy_and_support(probs)
    return eff, total


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
    augmented = base._augment_knn_floor(base.Family(family.positions, family.adj, family.layers))  # type: ignore[attr-defined]
    return Family(positions=augmented.positions, adj=augmented.adj, layers=augmented.layers)


def _augment_z_spread_stencil(family: Family) -> Family:
    positions = family.positions
    layers = family.layers
    adj: dict[int, list[int]] = {i: list(nbs) for i, nbs in family.adj.items()}

    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        for src in layers[layer]:
            sx, sy, sz = positions[src]
            ranked: list[tuple[float, float, int]] = []
            for dst, (dx, dy, dz) in zip(dst_nodes, dst_positions):
                dz_off = dz - sz
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dz_off, dist2, dst))
            ranked.sort(key=lambda item: item[0])

            selected = list(dict.fromkeys(adj.get(src, [])))
            buckets = [ranked[i::Z_SPREAD_BUCKETS] for i in range(Z_SPREAD_BUCKETS)]
            for bucket in buckets:
                if not bucket:
                    continue
                _, _, dst = min(bucket, key=lambda item: item[1])
                if dst not in selected:
                    selected.append(dst)

            by_dist = sorted(ranked, key=lambda item: item[1])
            for _, _, dst in by_dist:
                if len(selected) >= Z_SPREAD_FLOOR:
                    break
                if dst not in selected:
                    selected.append(dst)

            adj[src] = selected

    return Family(positions=positions, adj=adj, layers=layers)


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    indeg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            indeg[j] += 1
    from collections import deque

    q = deque(i for i in range(n) if indeg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            indeg[j] -= 1
            if indeg[j] == 0:
                q.append(j)
    return order


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
    order = _topo_order(adj, n)
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


def _phase_ramp_metrics(
    family: Family,
    same_amps: list[complex],
    wave_amps: list[complex],
    det_line: list[int],
) -> tuple[float, float, float]:
    z_vals = [family.positions[i][2] for i in det_line]
    same_probs = [abs(same_amps[i]) ** 2 for i in det_line]
    wave_probs = [abs(wave_amps[i]) ** 2 for i in det_line]
    peak = max(max(same_probs), max(wave_probs), 1e-30)
    use = [i for i, (ps, pw) in enumerate(zip(same_probs, wave_probs)) if max(ps, pw) >= 0.02 * peak]
    if len(use) < 3:
        use = [i for i, (ps, pw) in enumerate(zip(same_probs, wave_probs)) if max(ps, pw) >= 1e-4 * peak]
    if len(use) < 3:
        use = list(range(len(det_line)))

    diffs: list[float] = []
    acc = 0.0
    prev = None
    for j in use:
        d = base._wrap_phase(  # type: ignore[attr-defined]
            math.atan2(wave_amps[det_line[j]].imag, wave_amps[det_line[j]].real)
            - math.atan2(same_amps[det_line[j]].imag, same_amps[det_line[j]].real)
        )
        if prev is None:
            acc = d
        else:
            step = base._wrap_phase(d - prev)  # type: ignore[attr-defined]
            acc += step
        diffs.append(acc)
        prev = d

    z_use = [z_vals[j] for j in use]
    mz = sum(z_use) / len(z_use)
    md = sum(diffs) / len(diffs)
    szz = sum((z - mz) ** 2 for z in z_use)
    if szz < 1e-12:
        return 0.0, 0.0, 0.0
    szd = sum((z - mz) * (d - md) for z, d in zip(z_use, diffs))
    slope = szd / szz
    ss_tot = sum((d - md) ** 2 for d in diffs)
    ss_res = sum((d - (slope * (z - mz) + md)) ** 2 for z, d in zip(z_use, diffs))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
    span = max(diffs) - min(diffs)
    return slope, r2, span


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
        weights_sc = _normalize_weights(cluster_power)

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
    alpha = _fit_power([r["s"] for r in rows], [r["abs_delta"] for r in rows])
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
    print("SOURCE-RESOLVED GENERATED WAVEFIELD TRANSFER V2")
    print("  generated-family z-spread stencil vs retained kNN-floor bridge")
    print("=" * 108)
    print(f"family seeds=0..{N_SEEDS - 1}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, connect_radius={CONNECT_RADIUS}")
    print(f"bridge family: k-nearest floor augmentation (k={K_NEAREST}, min_edges={MIN_EDGES})")
    print(f"geometry-rule change: z-spread stencil (buckets={Z_SPREAD_BUCKETS}, floor={Z_SPREAD_FLOOR})")
    print(f"field modes: static Green vs wavefield")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"field target max: {FIELD_TARGET_MAX}")
    print("observables: zero-source reduction, centroid sign counts, F~M exponent, detector N_eff")
    print("diagnostic: geometry-rule delta from bridge to z-stencil")
    print()

    per_case_results: dict[tuple[str, str], list[dict[str, float]]] = {}
    per_case_zero: dict[tuple[str, str], float] = {}

    for seed in range(N_SEEDS):
        base_family = _family(seed)
        bridge_family = _augment_knn_floor(base_family)
        stencil_family = _augment_z_spread_stencil(base_family)
        for family_label, family in [("bridge", bridge_family), ("zstencil", stencil_family)]:
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
    for family_label in ["bridge", "zstencil"]:
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
        stencil_rows = per_case_results[("zstencil", mode)]
        bridge_summary = _summarize(bridge_rows, per_case_zero[("bridge", mode)])
        stencil_summary = _summarize(stencil_rows, per_case_zero[("zstencil", mode)])
        delta_toward = stencil_summary["toward_count"] - bridge_summary["toward_count"]
        delta_neff = stencil_summary["eff_support"] - bridge_summary["eff_support"]
        delta_alpha = (
            (stencil_summary["alpha"] or math.nan) - (bridge_summary["alpha"] or math.nan)
            if stencil_summary["alpha"] is not None and bridge_summary["alpha"] is not None
            else math.nan
        )
        print(
            f"  {mode:>9s}: delta_TOWARD={delta_toward:+d}  "
            f"delta_N_eff={delta_neff:+.2f}  delta_F~M={delta_alpha:+.3f}"
        )

    print()
    print("SAFE READ")
    print("  - The retained kNN-floor bridge remains the baseline control.")
    print("  - The z-spread stencil is the tested geometry-rule change.")
    print("  - If the stencil improves sign and detector support while keeping F~M near 1,")
    print("    then the wavefield lane is becoming geometry-transfer relevant.")
    print("  - If it only reshuffles support without improving the weak-field law,")
    print("    this is a bounded no-go for this geometry rule.")


if __name__ == "__main__":
    main()
