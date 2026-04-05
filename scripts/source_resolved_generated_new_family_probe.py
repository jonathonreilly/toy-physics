#!/usr/bin/env python3
"""Generated-family new-family probe.

Question:
  Can a genuinely different generated-family geometry widen detector support
  enough for the retained exact-lattice wavefield mechanism to matter more
  than it does on the compact bridge family?

Scope:
  - retained compact bridge family as the baseline control
  - a new three-band split-shell family with wider support by construction
  - static Green vs wavefield on each family
  - exact zero-source reduction check
  - detector effective support N_eff
  - centroid sign counts and weak-field F~M fit

This probe is intentionally narrow. It does not try to close generated-family
physics. It asks whether a radically different support geometry can move the
wavefield lane out of the compact-family bottleneck.
"""

from __future__ import annotations

import math
import os
import random
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts import source_resolved_generated_wavefield_bridge as bridge  # noqa: E402


N_LAYERS = 16
NODES_PER_LAYER = 30
N_SEEDS = 4
K = 5.0
TARGET_Y = 3.0
MASS_RADIUS = 2.5
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
FIELD_TARGET_MAX = 0.02

X_STEP = 0.75
BAND_CENTERS = (-7.5, 0.0, 7.5)
BAND_Z_CENTERS = (-3.5, 0.0, 3.5)
BAND_Y_JITTER = 0.85
BAND_Z_JITTER = 0.95
BAND_LAYER_Y_DRIFT = 0.12
BAND_LAYER_Z_DRIFT = 0.10
BAND_FLOOR = 7


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


def _entropy_and_support(probs: list[float]) -> tuple[float, float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    support_frac = sum(1 for p in norm if p >= 0.01 * max(norm)) / len(norm)
    return h, eff, support_frac


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
    rng = random.Random(seed * 41 + 11)
    positions: list[tuple[float, float, float]] = []
    layers: list[list[int]] = []

    for layer in range(N_LAYERS):
        layer_nodes: list[int] = []
        x = layer * X_STEP
        for idx in range(NODES_PER_LAYER):
            band = idx % 3
            y = (
                BAND_CENTERS[band]
                + BAND_LAYER_Y_DRIFT * (layer - (N_LAYERS - 1) / 2.0)
                + rng.uniform(-BAND_Y_JITTER, BAND_Y_JITTER)
            )
            z = (
                BAND_Z_CENTERS[band]
                + BAND_LAYER_Z_DRIFT * (layer - (N_LAYERS - 1) / 2.0)
                + rng.uniform(-BAND_Z_JITTER, BAND_Z_JITTER)
            )
            positions.append((x, y, z))
            layer_nodes.append(len(positions) - 1)
        layers.append(layer_nodes)

    adj: dict[int, list[int]] = {}
    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_positions = [positions[i] for i in dst_nodes]
        dst_band_ids = [
            min(range(len(BAND_CENTERS)), key=lambda b: abs(y - BAND_CENTERS[b]))
            for _, y, _ in dst_positions
        ]

        for src in layers[layer]:
            sx, sy, sz = positions[src]
            ranked: list[tuple[float, int, int]] = []
            for dst, (dx, dy, dz), band_id in zip(dst_nodes, dst_positions, dst_band_ids):
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, dst, band_id))
            ranked.sort(key=lambda item: item[0])

            selected: list[int] = []
            for band_id in range(len(BAND_CENTERS)):
                band_candidates = [item for item in ranked if item[2] == band_id]
                if band_candidates:
                    dst = min(band_candidates, key=lambda item: item[0])[1]
                    if dst not in selected:
                        selected.append(dst)

            for _, dst, _ in ranked:
                if len(selected) >= BAND_FLOOR:
                    break
                if dst not in selected:
                    selected.append(dst)

            adj[src] = selected

    return Family(positions=positions, adj=adj, layers=layers)


def _summarize(rows: list[dict[str, float]], zero_shift: float) -> dict[str, float]:
    deltas = [r["delta"] for r in rows]
    effs = [r["eff_support"] for r in rows]
    sups = [r["support_frac"] for r in rows]
    toward = sum(1 for d in deltas if d > 0)
    alpha = _fit_power([r["s"] for r in rows], [r["abs_delta"] for r in rows])
    return {
        "delta_mean": _mean(deltas),
        "delta_se": _stdev(deltas) / math.sqrt(len(deltas)) if len(deltas) >= 2 else 0.0,
        "toward_count": toward,
        "total": len(deltas),
        "eff_support": _mean(effs),
        "support_frac": _mean(sups),
        "zero_shift": abs(zero_shift),
        "alpha": alpha if alpha is not None else math.nan,
    }


def _evaluate(family: Family, mode: str) -> tuple[list[dict[str, float]], float]:
    return bridge._evaluate_family(family, mode)  # type: ignore[attr-defined]


def main() -> None:
    print("=" * 108)
    print("SOURCE-RESOLVED GENERATED NEW FAMILY PROBE")
    print("  compact bridge family versus new split-shell support family")
    print("=" * 108)
    print(f"family seeds=0..{N_SEEDS - 1}")
    print(f"baseline family: retained compact kNN-floor bridge")
    print(
        "new family: three-band split-shell geometry "
        f"(bands={BAND_CENTERS}, floor={BAND_FLOOR})"
    )
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"field target max: {FIELD_TARGET_MAX}")
    print("modes: static Green vs wavefield")
    print("observables: zero-source reduction, centroid sign counts, F~M exponent, detector N_eff")
    print()

    per_case_results: dict[tuple[str, str], list[dict[str, float]]] = {}
    per_case_zero: dict[tuple[str, str], float] = {}

    for seed in range(N_SEEDS):
        compact = bridge._augment_knn_floor(bridge._family(seed))  # type: ignore[attr-defined]
        split_shell = _family(seed)
        for family_label, family in [("bridge", compact), ("split", split_shell)]:
            for mode in ["static", "wavefield"]:
                rows, zero_shift = _evaluate(family, mode)
                key = (family_label, mode)
                per_case_results.setdefault(key, []).extend(rows)
                per_case_zero[key] = max(per_case_zero.get(key, 0.0), abs(zero_shift))
                summary = _summarize(rows, zero_shift)
                alpha = summary["alpha"]
                alpha_str = f"{alpha:.3f}" if math.isfinite(alpha) else "n/a"
                print(
                    f"seed={seed} {family_label:>7s}/{mode:<9s} "
                    f"zero={summary['zero_shift']:.3e} "
                    f"TOWARD={summary['toward_count']}/{summary['total']} "
                    f"F~M={alpha_str} N_eff={summary['eff_support']:.2f} "
                    f"support_frac={summary['support_frac']:.3f}"
                )

    print()
    print("SUMMARY")
    for family_label in ["bridge", "split"]:
        for mode in ["static", "wavefield"]:
            key = (family_label, mode)
            rows = per_case_results[key]
            summary = _summarize(rows, per_case_zero[key])
            alpha = summary["alpha"]
            alpha_str = f"{alpha:.3f}" if math.isfinite(alpha) else "n/a"
            print(
                f"{family_label:>7s}/{mode:<9s}  zero={summary['zero_shift']:.3e}  "
                f"TOWARD={summary['toward_count']}/{summary['total']}  "
                f"F~M={alpha_str}  N_eff={summary['eff_support']:.2f}  "
                f"support_frac={summary['support_frac']:.3f}"
            )

    print()
    print("GEOMETRY DELTA")
    for mode in ["static", "wavefield"]:
        bridge_rows = per_case_results[("bridge", mode)]
        split_rows = per_case_results[("split", mode)]
        bridge_summary = _summarize(bridge_rows, per_case_zero[("bridge", mode)])
        split_summary = _summarize(split_rows, per_case_zero[("split", mode)])
        delta_toward = split_summary["toward_count"] - bridge_summary["toward_count"]
        delta_neff = split_summary["eff_support"] - bridge_summary["eff_support"]
        delta_alpha = (
            split_summary["alpha"] - bridge_summary["alpha"]
            if math.isfinite(split_summary["alpha"]) and math.isfinite(bridge_summary["alpha"])
            else math.nan
        )
        delta_alpha_str = f"{delta_alpha:+.3f}" if math.isfinite(delta_alpha) else "n/a"
        print(
            f"  {mode:>9s}: delta_TOWARD={delta_toward:+d}  "
            f"delta_N_eff={delta_neff:+.2f}  delta_F~M={delta_alpha_str}"
        )

    print()
    print("SAFE READ")
    print("  - The retained compact bridge remains the baseline control.")
    print("  - The split-shell family is a genuinely different support geometry.")
    print("  - If it broadens detector support enough and improves the weak-field law,")
    print("    that would be a real reopening of the generated-family transfer story.")
    print("  - If it only widens support without improving the field relevance,")
    print("    it is a bounded no-go for this new family.")


if __name__ == "__main__":
    main()
