#!/usr/bin/env python3
"""Adaptive readout audit on the compact repeated-update source object.

Question:
  Can a genuinely different detector-side architecture recover some readout
  localization without destroying the weak-field mass law?

Architecture:
  - start from the retained compact repeated-update source object
  - replace fixed windows / tapers with an entropy-guided diffusion contour on
    the detector layer
  - use the diffused detector profile to define a soft contour mask rather than
    a fixed geometric crop

This stays narrow:
  - one exact 3D lattice family at h = 0.25
  - one compact repeated-update source object
  - one broad readout reference
  - one adaptive diffusion-contour readout
  - one exact zero-source reduction check

Fast falsifier:
  - adaptive readout flips AWAY
  - or adaptive readout loses the weak-field F~M class
  - or adaptive readout does not meaningfully reduce detector support relative
    to the broad readout
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

DIFFUSE_STEPS = 2
DIFFUSE_LAMBDA = 0.35
BLEND_WITH_RAW = 0.50
TARGET_MASS_BASE = 0.32
TARGET_MASS_GAIN = 0.26
MASK_SLOPE_FLOOR = 0.10


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
    mean_alpha: float | None
    zero_shift: float


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


def _support_eff(weights: list[float]) -> tuple[float, float, int]:
    if not weights:
        return 0.0, 0.0, 0
    norm = _normalize_weights(weights)
    h = -sum(p * math.log(p) for p in norm if p > 0.0)
    eff = math.exp(h)
    support = sum(1 for p in norm if p > 1e-30)
    return eff, max(norm), support


def _detector_probs(amps: list[complex], lat: m.Lattice3D) -> list[float]:
    det_start = lat.layer_start[lat.nl - 1]
    return [abs(amps[det_start + i]) ** 2 for i in range(lat.npl)]


def _grid_from_probs(lat: m.Lattice3D, probs: list[float]) -> list[list[float]]:
    grid = [[0.0 for _ in range(lat.nw)] for _ in range(lat.nw)]
    det_start = lat.layer_start[lat.nl - 1]
    for i, p in enumerate(probs):
        _, y, z = lat.pos[det_start + i]
        iy = int(round(y / lat.h)) + lat.hw
        iz = int(round(z / lat.h)) + lat.hw
        grid[iy][iz] = p
    return grid


def _probs_from_grid(grid: list[list[float]]) -> list[float]:
    return [v for row in grid for v in row]


def _normalize_grid(grid: list[list[float]]) -> list[list[float]]:
    total = sum(sum(row) for row in grid)
    if total <= 1e-30:
        n = len(grid)
        return [[1.0 / (n * n) for _ in range(n)] for _ in range(n)]
    return [[v / total for v in row] for row in grid]


def _diffuse_once(grid: list[list[float]]) -> list[list[float]]:
    n = len(grid)
    out = [[0.0 for _ in range(n)] for _ in range(n)]
    for y in range(n):
        for z in range(n):
            total = grid[y][z]
            count = 1
            if y > 0:
                total += grid[y - 1][z]
                count += 1
            if y + 1 < n:
                total += grid[y + 1][z]
                count += 1
            if z > 0:
                total += grid[y][z - 1]
                count += 1
            if z + 1 < n:
                total += grid[y][z + 1]
                count += 1
            out[y][z] = total / count
    return out


def _adaptive_readout_weights(lat: m.Lattice3D, det_probs: list[float]) -> tuple[list[float], float, float, float]:
    grid = _normalize_grid(_grid_from_probs(lat, det_probs))
    u = grid
    for _ in range(DIFFUSE_STEPS):
        smooth = _diffuse_once(u)
        blended = [[(1.0 - DIFFUSE_LAMBDA) * a + DIFFUSE_LAMBDA * b for a, b in zip(row_u, row_s)]
                   for row_u, row_s in zip(u, smooth)]
        u = _normalize_grid(blended)

    raw = _probs_from_grid(u)
    det_norm = _normalize_weights(det_probs)
    blended = [BLEND_WITH_RAW * p + (1.0 - BLEND_WITH_RAW) * q for p, q in zip(det_norm, raw)]
    total = sum(blended)
    if total <= 1e-30:
        blended = [1.0 / len(blended)] * len(blended)
    else:
        blended = [v / total for v in blended]

    n = len(blended)
    h = -sum(p * math.log(p) for p in blended if p > 0.0)
    hnorm = h / math.log(n) if n > 1 else 0.0
    target_mass = TARGET_MASS_BASE + TARGET_MASS_GAIN * max(0.0, 1.0 - hnorm)
    target_mass = min(max(target_mass, 0.10), 0.80)

    ranked = sorted(blended, reverse=True)
    running = 0.0
    tau = ranked[-1] if ranked else 0.0
    for v in ranked:
        running += v
        tau = v
        if running >= target_mass:
            break

    spread = max(statistics.pstdev(blended), 1e-12)
    beta = max(MASK_SLOPE_FLOOR * spread, 1e-12)
    mask = [1.0 / (1.0 + math.exp(-(v - tau) / beta)) for v in blended]
    return mask, tau, target_mass, hnorm


def _centroid_from_probs(lat: m.Lattice3D, probs: list[float]) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    total = sum(probs)
    if total <= 1e-30:
        return 0.0
    return sum(p * lat.pos[det_start + i][2] for i, p in enumerate(probs)) / total


def _run_mode(
    lat: m.Lattice3D,
    source_nodes: list[int],
    free_z: float,
    gain: float,
    mode: str,
) -> ModeResult:
    step_deltas: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_det_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_support_frac: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_capture: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_weight_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_target_obs: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_tau_obs: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_hnorm_obs: list[list[float]] = [[] for _ in range(N_UPDATES)]

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
                target_obs = None
                tau_obs = None
                hnorm_obs = None
            elif mode == "adaptive":
                readout_weights, tau_obs, target_obs, hnorm_obs = _adaptive_readout_weights(lat, det_probs)
            else:
                raise ValueError(mode)

            readout_probs = [p * w for p, w in zip(det_probs, readout_weights)]
            total = sum(readout_probs)
            norm_probs = [p / total for p in readout_probs if p > 0.0] if total > 1e-30 else []
            if norm_probs:
                h = -sum(p * math.log(p) for p in norm_probs)
                det_eff = math.exp(h)
                peak = max(norm_probs)
                support_frac = sum(1 for p in norm_probs if p >= 0.01 * peak) / len(norm_probs)
            else:
                det_eff = 0.0
                support_frac = 0.0
            capture = total / base_total if base_total > 1e-30 else 0.0
            weight_eff, _, _ = _support_eff(readout_weights)
            delta = _centroid_from_probs(lat, readout_probs) - free_z

            step_deltas[step].append(delta)
            step_det_eff[step].append(det_eff)
            step_support_frac[step].append(support_frac)
            step_capture[step].append(capture)
            step_weight_eff[step].append(weight_eff)
            if target_obs is not None:
                step_target_obs[step].append(target_obs)
                step_tau_obs[step].append(tau_obs)
                step_hnorm_obs[step].append(hnorm_obs)

            src_probs = [abs(amps[i]) ** 2 for i in source_nodes]
            weights = _topk_weights(src_probs, TOP_KEEP)

    step_alpha: list[float | None] = []
    step_toward: list[int] = []
    for step in range(N_UPDATES):
        alpha = _fit_power(SOURCE_STRENGTHS, [abs(v) for v in step_deltas[step]])
        step_alpha.append(alpha)
        step_toward.append(sum(1 for d in step_deltas[step] if d > 0))

    target_mean = _mean([v for row in step_target_obs for v in row]) if mode == "adaptive" else None
    tau_mean = _mean([v for row in step_tau_obs for v in row]) if mode == "adaptive" else None
    hnorm_mean = _mean([v for row in step_hnorm_obs for v in row]) if mode == "adaptive" else None

    return ModeResult(
        label=mode,
        step_alpha=step_alpha,
        step_toward=step_toward,
        mean_det_eff=_mean([v for row in step_det_eff for v in row]),
        mean_support_frac=_mean([v for row in step_support_frac for v in row]),
        mean_capture=_mean([v for row in step_capture for v in row]),
        mean_weight_eff=_mean([v for row in step_weight_eff for v in row]),
        mean_delta=_mean([v for row in step_deltas for v in row]),
        mean_alpha=target_mean,
        zero_shift=0.0,
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
    print("PERSISTENT OBJECT ADAPTIVE READOUT PROBE")
    print("  exact h=0.25 lattice, compact repeated-update source object")
    print("  broad readout reference vs entropy-guided diffusion contour")
    print("=" * 100)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_z={SOURCE_Z}, source_nodes={source_nodes}")
    print(f"source strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}, top_keep={TOP_KEEP}")
    print(
        "adaptive readout: "
        f"diffuse_steps={DIFFUSE_STEPS}, diffuse_lambda={DIFFUSE_LAMBDA}, "
        f"target_mass_base={TARGET_MASS_BASE}, target_mass_gain={TARGET_MASS_GAIN}, "
        f"mask_slope_floor={MASK_SLOPE_FLOOR}, blend_with_raw={BLEND_WITH_RAW}"
    )
    print(f"kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"field target max={FIELD_TARGET_MAX}, fixed gain={gain:.6e}")
    print()

    zero_raw = _green_field_layers(lat, 0.0, source_nodes, base_weights)
    zero_dynamic = [[gain * v for v in row] for row in zero_raw]
    zero_amps = lat.propagate(zero_dynamic, m.K)
    zero_broad_shift = m._centroid_z(zero_amps, lat) - free_z
    zero_probs = _detector_probs(zero_amps, lat)
    zero_weights, zero_tau, zero_target, zero_hnorm = _adaptive_readout_weights(lat, zero_probs)
    zero_readout = [p * w for p, w in zip(zero_probs, zero_weights)]
    zero_adaptive_shift = _centroid_from_probs(lat, zero_readout) - free_z

    print("REDUCTION CHECK")
    print(f"  zero-source broad shift:    {zero_broad_shift:+.6e}")
    print(f"  zero-source adaptive shift: {zero_adaptive_shift:+.6e}")
    print(f"  zero-source adaptive target: {zero_target:.6f}")
    print(f"  zero-source adaptive tau:    {zero_tau:.6e}")
    print(f"  zero-source adaptive Hnorm:  {zero_hnorm:.6f}")
    print(f"  fixed dynamic field gain:    {gain:.6e}")
    print()

    broad = _run_mode(lat, source_nodes, free_z, gain, "broad")
    adaptive = _run_mode(lat, source_nodes, free_z, gain, "adaptive")

    print("FROZEN READOUT")
    print(
        f"{'mode':<10s} {'F~M(step)':>20s} {'TOWARD':>8s} {'det N_eff':>12s} "
        f"{'support frac':>13s} {'capture':>10s} {'w N_eff':>10s} {'mean delta':>12s} {'target':>8s}"
    )
    print("-" * 100)
    for result in (broad, adaptive):
        step_alpha = ",".join("—" if a is None else f"{a:.2f}" for a in result.step_alpha)
        toward = f"{sum(result.step_toward)}/{len(result.step_toward) * len(SOURCE_STRENGTHS)}"
        alpha_str = "n/a" if result.mean_alpha is None else f"{result.mean_alpha:.3f}"
        print(
            f"{result.label:<10s} {step_alpha:>20s} {toward:>8s} "
            f"{result.mean_det_eff:12.3f} {result.mean_support_frac:13.3f} "
            f"{result.mean_capture:10.3f} {result.mean_weight_eff:10.3f} "
            f"{result.mean_delta:12.3e} {alpha_str:>8s}"
        )

    broad_delta = broad.mean_delta
    adaptive_delta = adaptive.mean_delta
    broad_support = broad.mean_support_frac
    adaptive_support = adaptive.mean_support_frac
    broad_capture = broad.mean_capture
    adaptive_capture = adaptive.mean_capture

    print()
    print("COMPARISON")
    print(f"  adaptive vs broad delta ratio: {adaptive_delta / broad_delta if abs(broad_delta) > 1e-30 else math.nan:.3f}")
    print(f"  adaptive vs broad support frac: {adaptive_support / broad_support if broad_support > 1e-30 else math.nan:.3f}")
    print(f"  adaptive vs broad capture:      {adaptive_capture / broad_capture if broad_capture > 1e-30 else math.nan:.3f}")


if __name__ == "__main__":
    main()
