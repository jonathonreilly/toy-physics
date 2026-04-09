#!/usr/bin/env python3
"""Compact-update persistent-object probe on the retained exact lattice.

Moonshot goal:
  Starting from the retained broad quasi-persistent exact-lattice control, ask
  whether a tighter localization update can produce a smaller repeated-update
  source object while preserving the weak-field gates.

This stays narrow:
  - one exact 3D lattice family at h = 0.25
  - one fixed cross-shaped source object
  - one broad self-consistent control
  - one compact top-3 update rule
  - one reduction check: zero source recovers free propagation exactly
  - one observable pair:
      * source-object effective support
      * detector response / weak-field sign / F~M

Fast falsifier:
  - compact update flips AWAY
  - or compact update's step-wise F~M drifts away from 1
  - or compact update never reduces the source support below the broad control
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

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
TOP_KEEP = 3


@dataclass(frozen=True)
class ModeResult:
    label: str
    step_alpha: list[float | None]
    step_toward: list[int]
    mean_source_eff: float
    mean_weight_eff: float
    mean_weight_support: float
    mean_det_eff: float
    mean_source_support: float
    mean_overlap: float


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


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _topk_weights(vals: list[float], k: int) -> list[float]:
    if not vals:
        return []
    ranked = sorted(range(len(vals)), key=lambda i: vals[i], reverse=True)
    keep = set(ranked[: min(k, len(vals))])
    out = [vals[i] if i in keep else 0.0 for i in range(len(vals))]
    return _normalize_weights(out)


def _support_eff(weights: list[float]) -> tuple[float, float, int]:
    if not weights:
        return 0.0, 0.0, 0
    norm = _normalize_weights(weights)
    h = -sum(p * math.log(p) for p in norm if p > 0.0)
    eff = math.exp(h)
    support = sum(1 for p in norm if p > 1e-30)
    return eff, max(norm), support


def _detector_metrics(amps: list[complex], lat: m.Lattice3D) -> tuple[float, float, float, float]:
    det_start = lat.layer_start[lat.nl - 1]
    probs = [abs(amps[det_start + i]) ** 2 for i in range(lat.npl)]
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    peak = max(norm)
    top10 = sum(sorted(norm, reverse=True)[: min(10, len(norm))])
    support_frac = sum(1 for p in norm if p >= 0.01 * peak) / len(norm)
    return eff, top10, support_frac, peak


def _run_mode(
    lat: m.Lattice3D,
    source_nodes: list[int],
    free_z: float,
    gain: float,
    mode: str,
) -> ModeResult:
    step_deltas: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_source_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_weight_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_det_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_source_support: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_weight_support: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_overlap: list[list[float]] = [[] for _ in range(N_UPDATES)]

    for s in SOURCE_STRENGTHS:
        weights = [1.0 / len(source_nodes)] * len(source_nodes)
        prev_weights = weights[:]
        for step in range(N_UPDATES):
            raw = _green_field_layers(lat, s, source_nodes, weights)
            field = [[gain * v for v in row] for row in raw]
            amps = lat.propagate(field, m.K)

            det_eff, _, _, _ = _detector_metrics(amps, lat)
            delta = m._centroid_z(amps, lat) - free_z
            src_probs = [abs(amps[i]) ** 2 for i in source_nodes]
            src_eff, src_peak, src_support = _support_eff(src_probs)
            weight_eff, _, weight_support = _support_eff(weights)

            n1 = _normalize_weights(prev_weights)
            n2 = _normalize_weights(src_probs)
            overlap_num = sum(a * b for a, b in zip(n1, n2))
            overlap_den = math.sqrt(sum(a * a for a in n1) * sum(b * b for b in n2))
            overlap = overlap_num / overlap_den if overlap_den > 1e-30 else 0.0

            step_deltas[step].append(delta)
            step_source_eff[step].append(src_eff)
            step_weight_eff[step].append(weight_eff)
            step_det_eff[step].append(det_eff)
            step_source_support[step].append(src_support)
            step_weight_support[step].append(weight_support)
            step_overlap[step].append(overlap)

            prev_weights = weights[:]
            if mode == "broad":
                weights = _normalize_weights(src_probs)
            elif mode == "compact":
                weights = _topk_weights(src_probs, TOP_KEEP)
            else:
                raise ValueError(mode)

    step_alpha: list[float | None] = []
    step_toward: list[int] = []
    for step in range(N_UPDATES):
        alpha = _fit_power(SOURCE_STRENGTHS, [abs(v) for v in step_deltas[step]])
        step_alpha.append(alpha)
        step_toward.append(sum(1 for d in step_deltas[step] if d > 0))

    return ModeResult(
        label=mode,
        step_alpha=step_alpha,
        step_toward=step_toward,
        mean_source_eff=_mean([v for row in step_source_eff for v in row]),
        mean_weight_eff=_mean([v for row in step_weight_eff for v in row]),
        mean_weight_support=_mean([v for row in step_weight_support for v in row]),
        mean_det_eff=_mean([v for row in step_det_eff for v in row]),
        mean_source_support=_mean([v for row in step_source_support for v in row]),
        mean_overlap=_mean([v for row in step_overlap for v in row]),
    )


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    free_z = m._centroid_z(free, lat)

    base_weights = [1.0 / len(source_nodes)] * len(source_nodes)
    ref_raw = _green_field_layers(lat, max(SOURCE_STRENGTHS), source_nodes, base_weights)
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    print("=" * 100)
    print("PERSISTENT OBJECT COMPACT UPDATE PROBE")
    print("  exact h=0.25 lattice, broad control vs compact top-3 update")
    print("=" * 100)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_z={SOURCE_Z}, source_nodes={source_nodes}")
    print(f"source strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}, top_keep={TOP_KEEP}")
    print(f"kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"field target max={FIELD_TARGET_MAX}, fixed gain={gain:.6e}")
    print()

    zero_raw = _green_field_layers(lat, 0.0, source_nodes, base_weights)
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_raw], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - free_z
    print("REDUCTION CHECK")
    print(f"  zero-source shift: {zero_delta:+.6e}")
    print()

    modes = [
        ("broad", _run_mode(lat, source_nodes, free_z, gain, "broad")),
        ("compact", _run_mode(lat, source_nodes, free_z, gain, "compact")),
    ]

    print(
        f"{'mode':>8s} {'step':>5s} {'F~M':>8s} {'TOWARD':>8s} "
        f"{'obj_eff':>9s} {'obj_sup':>8s} {'resp_eff':>9s}"
    )
    print("-" * 84)
    for label, res in modes:
        for step, alpha in enumerate(res.step_alpha):
            alpha_str = f"{alpha:.2f}" if alpha is not None else "n/a"
            print(
                f"{label:>8s} {step:5d} {alpha_str:>8s} "
                f"{res.step_toward[step]:8d}/{len(SOURCE_STRENGTHS)} "
                f"{res.mean_weight_eff:9.3f} {res.mean_weight_support:8.3f} "
                f"{res.mean_det_eff:9.2f}"
            )

    broad, compact = modes[0][1], modes[1][1]
    broad_pass = all(t == len(SOURCE_STRENGTHS) for t in broad.step_toward) and all(
        alpha is not None and abs(alpha - 1.0) <= 0.05 for alpha in broad.step_alpha
    )
    compact_pass = all(t == len(SOURCE_STRENGTHS) for t in compact.step_toward) and all(
        alpha is not None and abs(alpha - 1.0) <= 0.05 for alpha in compact.step_alpha
    )

    print()
    print("SUMMARY")
    print(
        f"  broad obj_eff={broad.mean_weight_eff:.3f}, obj_sup={broad.mean_weight_support:.3f}, "
        f"resp_eff={broad.mean_source_eff:.3f}, resp_sup={broad.mean_source_support:.3f}, "
        f"det_eff={broad.mean_det_eff:.2f}, overlap={broad.mean_overlap:.3f}, pass={broad_pass}"
    )
    print(
        f"  compact obj_eff={compact.mean_weight_eff:.3f}, obj_sup={compact.mean_weight_support:.3f}, "
        f"resp_eff={compact.mean_source_eff:.3f}, resp_sup={compact.mean_source_support:.3f}, "
        f"det_eff={compact.mean_det_eff:.2f}, overlap={compact.mean_overlap:.3f}, pass={compact_pass}"
    )

    if compact_pass and compact.mean_weight_eff < broad.mean_weight_eff:
        print("  result: compact update is a smaller retained object on this family.")
    elif compact_pass:
        print("  result: compact update passes, but it is not smaller than the broad control.")
    else:
        print("  result: compact update does not beat the broad control on this family.")

    print()
    print("FASTEST FALSIFIER")
    print("  If the compact update loses TOWARD, drifts away from F~M≈1, or fails to")
    print("  reduce source effective support below the broad control, then the broad")
    print("  quasi-persistent object remains the smallest retained object on this family.")


if __name__ == "__main__":
    main()
