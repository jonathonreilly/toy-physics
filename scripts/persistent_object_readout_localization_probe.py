#!/usr/bin/env python3
"""Detector/readout localization probe on the compact repeated-update source.

Moonshot goal:
  Starting from the retained compact top-3 repeated-update source object, ask
  whether a peak-centered detector readout can shrink detector effective
  support while preserving the weak-field sign and linear mass-scaling class.

This stays narrow:
  - one exact 3D lattice family at h = 0.25
  - one compact top-3 repeated-update source object
  - one broad detector readout
  - one peak-centered 3x3 readout window
  - one reduction check: zero source recovers free propagation exactly
  - one observable pair:
      * detector effective support N_eff
      * weak-field sign / F~M exponent

Fast falsifier:
  - localized readout flips AWAY
  - or localized readout loses near-linear F~M
  - or the localized readout does not meaningfully shrink detector support
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
READOUT_RADIUS = 1


@dataclass(frozen=True)
class ModeResult:
    label: str
    step_alpha: list[float | None]
    step_toward: list[int]
    mean_det_eff: float
    mean_det_support: float
    mean_capture: float
    mean_window_bins: float
    mean_delta: float


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


def _detector_probs(amps: list[complex], lat: m.Lattice3D) -> list[float]:
    det_start = lat.layer_start[lat.nl - 1]
    return [abs(amps[det_start + i]) ** 2 for i in range(lat.npl)]


def _support_metrics(probs: list[float]) -> tuple[float, float, float, float]:
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


def _window_mask(lat: m.Lattice3D, det_probs: list[float], radius: int) -> list[bool]:
    det_start = lat.layer_start[lat.nl - 1]
    peak_idx = max(range(len(det_probs)), key=lambda i: det_probs[i])
    peak_pos = lat.pos[det_start + peak_idx]
    py, pz = peak_pos[1], peak_pos[2]
    mask: list[bool] = []
    for i in range(lat.npl):
        _, y, z = lat.pos[det_start + i]
        mask.append(abs(y - py) <= radius * lat.h + 1e-12 and abs(z - pz) <= radius * lat.h + 1e-12)
    return mask


def _masked_probs(probs: list[float], mask: list[bool]) -> list[float]:
    return [p if keep else 0.0 for p, keep in zip(probs, mask)]


def _centroid_z_from_probs(lat: m.Lattice3D, probs: list[float], mask: list[bool] | None = None) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    total = 0.0
    weighted = 0.0
    for i, p in enumerate(probs):
        if mask is not None and not mask[i]:
            continue
        total += p
        weighted += p * lat.pos[det_start + i][2]
    return weighted / total if total > 1e-30 else 0.0


def _run_modes(
    lat: m.Lattice3D,
    source_nodes: list[int],
    free_z: float,
    gain: float,
) -> dict[str, ModeResult]:
    step_deltas_broad: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_deltas_local: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_broad_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_broad_support: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_local_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_local_support: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_local_capture: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_local_bins: list[list[float]] = [[] for _ in range(N_UPDATES)]

    for s in SOURCE_STRENGTHS:
        weights = [1.0 / len(source_nodes)] * len(source_nodes)
        for step in range(N_UPDATES):
            raw = _green_field_layers(lat, s, source_nodes, weights)
            field = [[gain * v for v in row] for row in raw]
            amps = lat.propagate(field, m.K)

            det_probs = _detector_probs(amps, lat)
            broad_delta = _centroid_z_from_probs(lat, det_probs) - free_z
            _, broad_eff, _, broad_support = _support_metrics(det_probs)

            mask = _window_mask(lat, det_probs, READOUT_RADIUS)
            local_probs = _masked_probs(det_probs, mask)
            local_delta = _centroid_z_from_probs(lat, local_probs, mask) - free_z
            _, local_eff, _, local_support = _support_metrics(local_probs)
            local_capture = sum(local_probs) / sum(det_probs) if sum(det_probs) > 1e-30 else 0.0
            local_bins = sum(1 for keep in mask if keep)

            step_deltas_broad[step].append(broad_delta)
            step_deltas_local[step].append(local_delta)
            step_broad_eff[step].append(broad_eff)
            step_broad_support[step].append(broad_support)
            step_local_eff[step].append(local_eff)
            step_local_support[step].append(local_support)
            step_local_capture[step].append(local_capture)
            step_local_bins[step].append(float(local_bins))

            src_probs = [abs(amps[i]) ** 2 for i in source_nodes]
            weights = _topk_weights(src_probs, TOP_KEEP)

    def _make_result(label: str, deltas: list[list[float]], det_eff: list[list[float]], det_support: list[list[float]], capture: list[list[float]], bins: list[list[float]]) -> ModeResult:
        step_alpha: list[float | None] = []
        step_toward: list[int] = []
        for step in range(N_UPDATES):
            step_alpha.append(_fit_power(SOURCE_STRENGTHS, [abs(v) for v in deltas[step]]))
            step_toward.append(sum(1 for d in deltas[step] if d > 0))
        return ModeResult(
            label=label,
            step_alpha=step_alpha,
            step_toward=step_toward,
            mean_det_eff=_mean([v for row in det_eff for v in row]),
            mean_det_support=_mean([v for row in det_support for v in row]),
            mean_capture=_mean([v for row in capture for v in row]),
            mean_window_bins=_mean([v for row in bins for v in row]),
            mean_delta=_mean([v for row in deltas for v in row]),
        )

    return {
        "broad": _make_result(
            "broad",
            step_deltas_broad,
            step_broad_eff,
            step_broad_support,
            [[1.0] * len(SOURCE_STRENGTHS) for _ in range(N_UPDATES)],
            [[float(lat.npl)] * len(SOURCE_STRENGTHS) for _ in range(N_UPDATES)],
        ),
        "local": _make_result("local", step_deltas_local, step_local_eff, step_local_support, step_local_capture, step_local_bins),
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
    print("PERSISTENT OBJECT READOUT LOCALIZATION PROBE")
    print("  exact h=0.25 lattice, compact source object, broad vs peak-window detector readout")
    print("=" * 100)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_z={SOURCE_Z}, source_nodes={source_nodes}")
    print(f"source strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}, top_keep={TOP_KEEP}")
    print(f"readout window radius={READOUT_RADIUS} (peak-centered)")
    print(f"kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"field target max={FIELD_TARGET_MAX}, fixed gain={gain:.6e}")
    print()

    zero_raw = _green_field_layers(lat, 0.0, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes))
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_raw], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - free_z

    print("REDUCTION CHECK")
    print(f"  zero-source shift: {zero_delta:+.6e}")
    print()

    results = _run_modes(lat, source_nodes, free_z, gain)

    print(f"{'mode':>8s} {'step α':>24s} {'toward':>7s} {'mean N_eff':>12s} {'supp frac':>10s} {'capture':>9s} {'win bins':>9s} {'mean delta':>12s}")
    print("-" * 108)
    for label in ("broad", "local"):
        row = results[label]
        step_alpha = [f"{a:.2f}" if a is not None else "n/a" for a in row.step_alpha]
        print(
            f"{label:>8s} {('[' + ','.join(step_alpha) + ']'):>24s} "
            f"{sum(row.step_toward):7d} {row.mean_det_eff:12.3f} {row.mean_det_support:10.3f} "
            f"{row.mean_capture:9.3f} {row.mean_window_bins:9.2f} {row.mean_delta:12.6e}"
        )

    broad = results["broad"]
    local = results["local"]
    print()
    print("SUMMARY")
    print(f"  broad detector readout mean N_eff = {broad.mean_det_eff:.3f}")
    print(f"  localized readout mean N_eff = {local.mean_det_eff:.3f}")
    print(f"  broad support fraction = {broad.mean_det_support:.3f}")
    print(f"  localized support fraction = {local.mean_det_support:.3f}")
    print(f"  localized capture fraction = {local.mean_capture:.3f}")
    print(f"  localized window bins = {local.mean_window_bins:.2f}")
    print(
        "  broad step-wise F~M exponents: "
        + ", ".join(f"{a:.2f}" if a is not None else "n/a" for a in broad.step_alpha)
    )
    print(
        "  localized step-wise F~M exponents: "
        + ", ".join(f"{a:.2f}" if a is not None else "n/a" for a in local.step_alpha)
    )
    print(
        "  localized TOWARD rows: "
        f"{sum(local.step_toward)}/{N_UPDATES * len(SOURCE_STRENGTHS)}"
    )
    print()
    print("SAFE READ")
    print("  - The compact repeated-update source object is retained from the earlier")
    print("    source-object compact-update probe.")
    print("  - The readout-side window is the new ingredient: a peak-centered 3x3")
    print("    detector patch on the final layer.")
    print("  - If the localized readout keeps TOWARD and F~M≈1 while cutting N_eff,")
    print("    the detector/readout sector is no longer irreducibly broad.")
    print("  - If it loses sign or mass scaling, the readout sector remains broad")
    print("    and the compact source object is not enough.")


if __name__ == "__main__":
    main()
