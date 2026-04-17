#!/usr/bin/env python3
"""Persistent-object localization escalation probe.

Goal:
  Start from the retained broad quasi-persistent exact-lattice control and ask
  whether a more localized repeated-update source object can still preserve the
  weak-field sign and linear mass-scaling class.
  The readout stays broad, so any passing subset should still be read as a
  source-side localization check rather than detector-localization closure.

Scope:
  - one compact exact lattice family at h = 0.25
  - one fixed source cluster on the retained exact Green pocket
  - one sweep over every non-empty source-support subset
  - one repeated self-consistency loop per subset
  - one retained observable pair:
      * source localization via effective support N_eff
      * detector response via TOWARD count and F~M exponent

Fast falsifier:
  - any candidate loses TOWARD on the repeated updates
  - or any candidate's step-wise F~M exponent departs strongly from 1
  - or the only passing candidate is the broad full-support object itself
"""

from __future__ import annotations

import itertools
import math
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.25
NL_PHYS = 6
PW = 3
SOURCE_Z = 2.0
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
N_UPDATES = 3
GREEN_EPS = 0.5
GREEN_MU = 0.08
FIELD_TARGET_MAX = 0.02


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


def _entropy_eff(weights: list[float]) -> float:
    norm = _normalize_weights(weights)
    h = -sum(p * math.log(p) for p in norm if p > 0.0)
    return math.exp(h)


def _support_metrics(probs: list[float]) -> tuple[float, float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    if not norm:
        return 0.0, 0.0, 0.0
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    peak = max(norm)
    support_frac = sum(1 for p in norm if p >= 0.01 * peak) / len(norm)
    return eff, peak, support_frac


def _source_cluster_nodes(lat: m.Lattice3D) -> list[int]:
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(SOURCE_Z / lat.h)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw:
            nodes.append(lat.nmap[(gl, y - lat.hw, z - lat.hw)])
    return nodes


def _green_field_layers(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    weights: list[float],
) -> list[list[float]]:
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    if not source_nodes:
        return field
    source_pos = [lat.pos[i] for i in source_nodes]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for w, (mx, my, mz) in zip(weights, source_pos):
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
                val += w * source_strength * math.exp(-GREEN_MU * r) / r
            field[layer][i] = val
    return field


def _field_abs_max(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row) if layers else 0.0


def _source_support_metrics(weights: list[float]) -> tuple[float, float]:
    if not weights:
        return 0.0, 0.0
    norm = _normalize_weights(weights)
    eff = _entropy_eff(norm)
    return eff, max(norm)


def _flatten(rows: list[list[float]]) -> list[float]:
    return [v for row in rows for v in row]


def _escalation_rows(source_nodes: list[int]) -> list[tuple[str, list[int]]]:
    """Curated localization ladder.

    The point is not exhaustive combinatorics. The point is to probe whether a
    substantially smaller source object can survive the repeated-update loop.
    """

    # source_nodes order follows SOURCE_CLUSTER:
    #   0 = center, 1/2 = +/- y arms, 3/4 = +/- z arms
    ladder = [
        ("center", [source_nodes[0]]),
        ("center+y+", [source_nodes[0], source_nodes[1]]),
        ("center+y-", [source_nodes[0], source_nodes[2]]),
        ("center+z+", [source_nodes[0], source_nodes[3]]),
        ("center+z-", [source_nodes[0], source_nodes[4]]),
        ("center+y±", [source_nodes[0], source_nodes[1], source_nodes[2]]),
        ("center+z±", [source_nodes[0], source_nodes[3], source_nodes[4]]),
        ("center+3arms", [source_nodes[0], source_nodes[1], source_nodes[2], source_nodes[3]]),
        ("full", list(source_nodes)),
    ]
    return ladder


def _candidate_case(
    lat: m.Lattice3D,
    source_nodes: list[int],
    subset: list[int],
    gain: float,
    free_z: float,
) -> dict[str, object]:
    weights = [1.0 / len(subset)] * len(subset)
    prev_weights = weights[:]

    step_deltas: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_source_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_det_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_overlaps: list[list[float]] = [[] for _ in range(N_UPDATES)]

    for s in SOURCE_STRENGTHS:
        weights = [1.0 / len(subset)] * len(subset)
        prev_weights = weights[:]
        for step in range(N_UPDATES):
            raw = _green_field_layers(lat, s, subset, weights)
            field = [[gain * v for v in row] for row in raw]
            amps = lat.propagate(field, m.K)

            det_start = lat.layer_start[lat.nl - 1]
            det_probs = [abs(amps[det_start + i]) ** 2 for i in range(lat.npl)]
            det_eff, _, _ = _support_metrics(det_probs)
            delta = m._centroid_z(amps, lat) - free_z
            src_probs = [abs(amps[i]) ** 2 for i in subset]
            src_eff, _ = _source_support_metrics(src_probs)

            n1 = _normalize_weights(prev_weights)
            n2 = _normalize_weights(src_probs)
            overlap_num = sum(a * b for a, b in zip(n1, n2))
            overlap_den = math.sqrt(sum(a * a for a in n1) * sum(b * b for b in n2))
            overlap = overlap_num / overlap_den if overlap_den > 1e-30 else 0.0

            step_deltas[step].append(delta)
            step_source_eff[step].append(src_eff)
            step_det_eff[step].append(det_eff)
            step_overlaps[step].append(overlap)

            prev_weights = weights[:]
            weights = _normalize_weights(src_probs)

    step_alpha: list[float | None] = []
    step_toward: list[int] = []
    for step in range(N_UPDATES):
        alpha = _fit_power(SOURCE_STRENGTHS, [abs(v) for v in step_deltas[step]])
        step_alpha.append(alpha)
        step_toward.append(sum(1 for d in step_deltas[step] if d > 0))

    flat_source = _flatten(step_source_eff)
    flat_det = _flatten(step_det_eff)
    flat_overlap = _flatten(step_overlaps)

    return {
        "subset": subset,
        "label": f"n={len(subset)}:{','.join(str(i) for i in subset)}",
        "step_alpha": step_alpha,
        "step_toward": step_toward,
        "delta_mean": _mean(_flatten(step_deltas)),
        "mean_source_eff": _mean(flat_source),
        "mean_det_eff": _mean(flat_det),
        "mean_overlap": _mean(flat_overlap),
        "source_eff_se": _stdev(flat_source) / math.sqrt(len(flat_source)) if len(flat_source) >= 2 else 0.0,
        "passes": all(t == len(SOURCE_STRENGTHS) for t in step_toward)
        and all(alpha is not None and abs(alpha - 1.0) <= 0.05 for alpha in step_alpha),
    }


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    free_z = m._centroid_z(free, lat)

    # Fixed gain from the retained full-support source at the strongest tested strength.
    full_raw = _green_field_layers(
        lat,
        max(SOURCE_STRENGTHS),
        source_nodes,
        [1.0 / len(source_nodes)] * len(source_nodes),
    )
    gain = FIELD_TARGET_MAX / _field_abs_max(full_raw) if _field_abs_max(full_raw) > 1e-30 else 1.0

    print("=" * 100)
    print("PERSISTENT OBJECT LOCALIZATION ESCALATION")
    print("  compact exact h=0.25 lattice, support-subset sweep under repeated self-consistency updates")
    print("=" * 100)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_z={SOURCE_Z}")
    print(f"full source cluster nodes={len(source_nodes)} -> {source_nodes}")
    print(f"source strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}")
    print(f"kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"fixed gain from full-support max strength: {gain:.6e}")
    print()

    zero_raw = _green_field_layers(lat, 0.0, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes))
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_raw], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - free_z

    print("REDUCTION CHECK")
    print(f"  zero-source shift: {zero_delta:+.6e}")
    print()

    print(
        f"{'subset':>18s} {'n':>2s} {'toward':>7s} {'step α':>24s} "
        f"{'mean src_eff':>13s} {'mean det_eff':>13s} {'mean overlap':>12s} {'PASS':>6s}"
    )
    print("-" * 110)

    candidates: list[dict[str, object]] = []
    for label, subset in _escalation_rows(source_nodes):
        row = _candidate_case(lat, source_nodes, subset, gain, free_z)
        candidates.append(row)
        step_alpha = [
            f"{alpha:.2f}" if alpha is not None else "n/a"
            for alpha in row["step_alpha"]  # type: ignore[index]
        ]
        step_toward = row["step_toward"]  # type: ignore[assignment]
        toward_total = sum(step_toward)
        print(
            f"{label:>18s} {len(subset):2d} {toward_total:7d} "
            f"{('[' + ','.join(step_alpha) + ']'):>24s} "
            f"{row['mean_source_eff']:13.3f} {row['mean_det_eff']:13.2f} "
            f"{row['mean_overlap']:12.3f} {('YES' if row['passes'] else 'no'):>6s}"
        )

    full_row = next(r for r in candidates if len(r["subset"]) == len(source_nodes))
    passers = [r for r in candidates if bool(r["passes"])]
    localized_passers = [r for r in passers if len(r["subset"]) < len(source_nodes)]

    print()
    print("SUMMARY")
    print(
        f"  full-support mean source_eff={full_row['mean_source_eff']:.3f}, "
        f"mean det_eff={full_row['mean_det_eff']:.2f}"
    )

    if localized_passers:
        best = min(localized_passers, key=lambda r: float(r["mean_source_eff"]))
        print(
            "  best localized passing subset: "
            f"{best['label']} with mean source_eff={best['mean_source_eff']:.3f}, "
            f"mean det_eff={best['mean_det_eff']:.2f}"
        )
        print(
            "  localization improved relative to the broad control: "
            f"{float(best['mean_source_eff']) < float(full_row['mean_source_eff'])}"
        )
        print("  readout remains broad; this is source-side localization only.")
    elif passers:
        print("  only the full-support object passes; localization did not improve the control.")
    else:
        print("  no subset preserved both repeated-update TOWARD and step-wise F~M≈1.")

    print()
    print("FASTEST FALSIFIER")
    print("  If every smaller subset loses TOWARD or the step-wise F~M exponent drifts")
    print("  away from 1, then the broad quasi-persistent source object remains the")
    print("  smallest retained source object on this exact-lattice family.")


if __name__ == "__main__":
    main()
