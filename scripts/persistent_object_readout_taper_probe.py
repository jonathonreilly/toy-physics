#!/usr/bin/env python3
"""Readout taper audit on the compact repeated-update source object.

Failure-audit goal:
  Check whether the hard 3x3 detector window was simply too lossy by testing a
  small family of softer localized readouts on top of the retained compact
  repeated-update source object.

Scope:
  - one exact 3D lattice family at h = 0.25
  - one compact repeated-update source object from the retained top-3 update
  - one broad detector readout reference
  - one hard 3x3 window reference
  - one small tapered family: Gaussian readouts with several widths
  - one reduction check: zero source recovers free propagation exactly

Fast falsifier:
  - any tapered readout still loses the weak-field F~M class, or
  - the only surviving mode is the broad readout itself, or
  - the softer taper does not meaningfully improve on the hard 3x3 window
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

HARD_RADIUS = 1
GAUSSIAN_SIGMAS = [1.5, 2.5, 4.0]


@dataclass(frozen=True)
class ModeResult:
    label: str
    step_alpha: list[float | None]
    step_toward: list[int]
    mean_det_eff: float
    mean_support_frac: float
    mean_capture: float
    mean_weight_eff: float
    mean_delta: float


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


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
    support_frac = sum(1 for p in norm if p >= 0.01 * peak) / len(norm)
    top10 = sum(sorted(norm, reverse=True)[: min(10, len(norm))])
    return h, eff, support_frac, top10


def _centroid_z_from_probs(lat: m.Lattice3D, probs: list[float], weights: list[float] | None = None) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    total = 0.0
    weighted = 0.0
    for i, p in enumerate(probs):
        w = 1.0 if weights is None else weights[i]
        if w <= 0.0:
            continue
        total += p * w
        weighted += p * w * lat.pos[det_start + i][2]
    return weighted / total if total > 1e-30 else 0.0


def _window_mask(lat: m.Lattice3D, det_probs: list[float], radius: int) -> list[float]:
    det_start = lat.layer_start[lat.nl - 1]
    peak_idx = max(range(len(det_probs)), key=lambda i: det_probs[i])
    peak_pos = lat.pos[det_start + peak_idx]
    py, pz = peak_pos[1], peak_pos[2]
    mask: list[float] = []
    for i in range(lat.npl):
        _, y, z = lat.pos[det_start + i]
        keep = abs(y - py) <= radius * lat.h + 1e-12 and abs(z - pz) <= radius * lat.h + 1e-12
        mask.append(1.0 if keep else 0.0)
    return mask


def _gaussian_weights(lat: m.Lattice3D, det_probs: list[float], sigma_cells: float) -> list[float]:
    det_start = lat.layer_start[lat.nl - 1]
    peak_idx = max(range(len(det_probs)), key=lambda i: det_probs[i])
    peak_pos = lat.pos[det_start + peak_idx]
    py, pz = peak_pos[1], peak_pos[2]
    sigma = max(sigma_cells * lat.h, 1e-12)
    weights: list[float] = []
    for i in range(lat.npl):
        _, y, z = lat.pos[det_start + i]
        dy = y - py
        dz = z - pz
        d2 = dy * dy + dz * dz
        weights.append(math.exp(-0.5 * d2 / (sigma * sigma)))
    return weights


def _weighted_probs(probs: list[float], weights: list[float]) -> list[float]:
    return [p * w for p, w in zip(probs, weights)]


def _run_mode(
    lat: m.Lattice3D,
    source_nodes: list[int],
    free_z: float,
    gain: float,
    mode: str,
    sigma_cells: float | None = None,
) -> ModeResult:
    step_deltas: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_det_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_support_frac: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_capture: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_weight_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]

    for s in SOURCE_STRENGTHS:
        weights = [1.0 / len(source_nodes)] * len(source_nodes)
        for step in range(N_UPDATES):
            raw = _green_field_layers(lat, s, source_nodes, weights)
            field = [[gain * v for v in row] for row in raw]
            amps = lat.propagate(field, m.K)
            det_probs = _detector_probs(amps, lat)
            base_total = sum(det_probs)

            if mode == "broad":
                readout_weights = [1.0] * len(det_probs)
            elif mode == "hard":
                readout_weights = _window_mask(lat, det_probs, HARD_RADIUS)
            elif mode == "gauss":
                assert sigma_cells is not None
                readout_weights = _gaussian_weights(lat, det_probs, sigma_cells)
            else:
                raise ValueError(mode)

            readout_probs = _weighted_probs(det_probs, readout_weights)
            _, det_eff, support_frac, _ = _support_metrics(readout_probs)
            capture = sum(readout_probs) / base_total if base_total > 1e-30 else 0.0
            _, readout_weight_eff, _, _ = _support_metrics(readout_weights)
            delta = _centroid_z_from_probs(lat, readout_probs, readout_weights) - free_z

            step_deltas[step].append(delta)
            step_det_eff[step].append(det_eff)
            step_support_frac[step].append(support_frac)
            step_capture[step].append(capture)
            step_weight_eff[step].append(readout_weight_eff)

            src_probs = [abs(amps[i]) ** 2 for i in source_nodes]
            weights = _topk_weights(src_probs, TOP_KEEP)

    step_alpha: list[float | None] = []
    step_toward: list[int] = []
    for step in range(N_UPDATES):
        alpha = _fit_power(SOURCE_STRENGTHS, [abs(v) for v in step_deltas[step]])
        step_alpha.append(alpha)
        step_toward.append(sum(1 for d in step_deltas[step] if d > 0))

    return ModeResult(
        label=mode if sigma_cells is None else f"gauss_{sigma_cells:g}",
        step_alpha=step_alpha,
        step_toward=step_toward,
        mean_det_eff=_mean([v for row in step_det_eff for v in row]),
        mean_support_frac=_mean([v for row in step_support_frac for v in row]),
        mean_capture=_mean([v for row in step_capture for v in row]),
        mean_weight_eff=_mean([v for row in step_weight_eff for v in row]),
        mean_delta=_mean([v for row in step_deltas for v in row]),
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

    print("=" * 108)
    print("PERSISTENT OBJECT READOUT TAPER AUDIT")
    print("  exact h=0.25 lattice, compact source object, broad vs hard vs tapered readout")
    print("=" * 108)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_z={SOURCE_Z}, source_nodes={source_nodes}")
    print(f"source strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}, top_keep={TOP_KEEP}")
    print(f"kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"field target max={FIELD_TARGET_MAX}, fixed gain={gain:.6e}")
    print(f"hard radius={HARD_RADIUS}, gaussian sigmas={GAUSSIAN_SIGMAS}")
    print()

    zero_raw = _green_field_layers(lat, 0.0, source_nodes, base_weights)
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_raw], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - free_z

    print("REDUCTION CHECK")
    print(f"  zero-source shift: {zero_delta:+.6e}")
    print()

    modes: list[ModeResult] = []
    modes.append(_run_mode(lat, source_nodes, free_z, gain, "broad"))
    modes.append(_run_mode(lat, source_nodes, free_z, gain, "hard"))
    for sigma in GAUSSIAN_SIGMAS:
        modes.append(_run_mode(lat, source_nodes, free_z, gain, "gauss", sigma_cells=sigma))

    print(
        f"{'mode':>12s} {'step F~M':>20s} {'TOWARD':>8s} {'det N_eff':>12s} "
        f"{'support_frac':>13s} {'capture':>10s} {'w_eff':>10s} {'delta_z':>12s}"
    )
    print("-" * 112)

    for row in modes:
        step_alpha = ",".join(f"{a:.2f}" if a is not None else "n/a" for a in row.step_alpha)
        print(
            f"{row.label:>12s} {('[' + step_alpha + ']'):>20s} {sum(row.step_toward):8d} "
            f"{row.mean_det_eff:12.3f} {row.mean_support_frac:13.3f} {row.mean_capture:10.3f} "
            f"{row.mean_weight_eff:10.3f} {row.mean_delta:+12.6e}"
        )

    broad = next(r for r in modes if r.label == "broad")
    hard = next(r for r in modes if r.label == "hard")
    gaussians = [r for r in modes if r.label.startswith("gauss_")]
    best_soft = max(gaussians, key=lambda r: r.mean_support_frac, default=None)

    print()
    print("SAFE READ")
    print(
        f"  broad readout stays linear and fully supported: det N_eff={broad.mean_det_eff:.3f}, "
        f"capture={broad.mean_capture:.3f}"
    )
    print(
        f"  hard 3x3 readout is the harshest case: det N_eff={hard.mean_det_eff:.3f}, "
        f"capture={hard.mean_capture:.3f}, step F~M={hard.step_alpha}"
    )
    if best_soft is not None:
        print(
            f"  best tapered readout candidate: {best_soft.label} with det N_eff={best_soft.mean_det_eff:.3f}, "
            f"capture={best_soft.mean_capture:.3f}, support_frac={best_soft.mean_support_frac:.3f}, "
            f"step F~M={best_soft.step_alpha}"
        )

    print()
    print("FASTEST FALSIFIER")
    print("  If every tapered readout still collapses step-wise F~M away from 1,")
    print("  or the only way to localize support is to make the readout too lossy,")
    print("  then the detector/readout localization lane remains a bounded no-go.")


if __name__ == "__main__":
    main()
