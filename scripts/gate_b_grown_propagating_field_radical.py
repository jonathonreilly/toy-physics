#!/usr/bin/env python3
"""Gate B grown propagating-field radical probe.

This is a materially different follow-up to the closed memory/gamma variants.

Goal:
  Ask whether a self-consistent beam-sourced field on the retained grown row
  can produce a causal observable while still reducing exactly to the retained
  grown baseline when the feedback coupling is zero.

Architecture:
  - retained grown geometry row only: drift=0.2, restore=0.7
  - a static source-resolved baseline field
  - a beam-sourced feedback field built from propagated density/current
  - an iterative fixed-point update of the field itself
  - exact alpha = 0 reduction to the retained baseline

Observable:
  - detector-line phase ramp relative to the alpha=0 baseline
  - detector escape ratio relative to the alpha=0 baseline
  - weak-field mass-scaling exponent as a sanity check

The claim surface is intentionally narrow:
  if the feedback field stays phase-flat or escape-flat once the exact
  reduction is enforced, the correct outcome is a bounded no-go.
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
import time
from dataclasses import dataclass

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 25
PW = 8
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0]
ALPHAS = [0.0, 0.25, 0.5]
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
Z_MASS = 3.0
FIELD_STRENGTH = 5e-5
FIELD_EPS = 0.1
TARGET_FIELD_MAX = 0.08
LAYER_MEMORY = 0.72
REAL_FEEDBACK_GAIN = 1.0
IMAG_FEEDBACK_GAIN = 0.70
ITERATIONS = 1


@dataclass(frozen=True)
class SeedResult:
    seed: int
    escape: dict[float, float]
    delta_z: dict[float, float]
    phase_slope: dict[float, float]
    phase_r2: dict[float, float]
    phase_span: dict[float, float]
    residual: dict[float, float]
    fm_alpha0: float | None
    fm_alpha05: float | None
    exact_alpha0: float


def _mean(values):
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


def grow(seed: int):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    layers: list[list[int]] = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, NL):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y = iy * H
                    z = iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0.0, DRIFT * H)
                    z = pz + rng.gauss(0.0, DRIFT * H)
                    y = y * (1.0 - RESTORE) + (iy * H) * RESTORE
                    z = z * (1.0 - RESTORE) + (iz * H) * RESTORE
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
                nodes.append(idx)
        layers.append(nodes)

        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                edges: list[int] = []
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers, nmap


def _static_field(pos, source_idx):
    mx, my, mz = pos[source_idx]
    field = [0.0] * len(pos)
    for i, (x, y, z) in enumerate(pos):
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + FIELD_EPS
        field[i] = FIELD_STRENGTH / r
    return field


def _layer_laplacian(values: list[float], hw: int) -> list[float]:
    grid_n = 2 * hw + 1
    out = [0.0] * len(values)
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            k = (iy + hw) * grid_n + (iz + hw)
            center = values[k]
            total = 0.0
            degree = 0
            for dy, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny = iy + dy
                nz = iz + dz
                if -hw <= ny <= hw and -hw <= nz <= hw:
                    nk = (ny + hw) * grid_n + (nz + hw)
                    total += values[nk]
                    degree += 1
            out[k] = total - degree * center
    return out


def _centered(values: list[float]) -> list[float]:
    if not values:
        return []
    m = sum(values) / len(values)
    return [v - m for v in values]


def _smooth_layer(values: list[float], hw: int, mix: float) -> list[float]:
    grid_n = 2 * hw + 1
    lap = _layer_laplacian(values, hw)
    out = [0.0] * len(values)
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            k = (iy + hw) * grid_n + (iz + hw)
            out[k] = (1.0 - mix) * values[k] + mix * (values[k] + 0.25 * lap[k])
    return out


def _normalize_layers(layers: list[list[float]]) -> list[list[float]]:
    mx = max((abs(v) for row in layers for v in row), default=0.0)
    if mx < 1e-30:
        return [[0.0 for _ in row] for row in layers]
    return [[v / mx for v in row] for row in layers]


def _layer_density(amps: list[complex], layers: list[list[int]]) -> list[list[float]]:
    return [[abs(amps[idx]) ** 2 for idx in layer_nodes] for layer_nodes in layers]


def _layer_current(density_layers: list[list[float]]) -> list[list[float]]:
    out: list[list[float]] = []
    prev = [0.0 for _ in density_layers[0]]
    for layer_idx, row in enumerate(density_layers):
        if layer_idx == 0:
            out.append(row[:])
        else:
            if len(prev) == 1:
                prev_vals = [prev[0] for _ in range(len(row))]
            else:
                prev_vals = prev
            out.append([row[k] - prev_vals[k] for k in range(len(row))])
        prev = row
    return out


def _build_feedback_field(
    density_layers: list[list[float]],
    current_layers: list[list[float]],
    hw: int,
) -> tuple[list[list[float]], list[list[float]]]:
    real_fb: list[list[float]] = []
    imag_fb: list[list[float]] = []
    for layer_idx in range(len(density_layers)):
        if layer_idx == 0:
            # The grown geometry starts from a single source node at layer 0.
            # Seed the causal recurrence with that scalar before the full grid
            # opens up on later layers.
            real_fb.append([density_layers[0][0]])
            imag_fb.append([current_layers[0][0]])
            continue

        real_src = _smooth_layer(_centered(density_layers[layer_idx]), hw, 0.35)
        imag_src = _smooth_layer(_centered(current_layers[layer_idx]), hw, 0.35)
        if layer_idx == 1:
            seed_real = density_layers[0][0]
            seed_imag = current_layers[0][0]
            real_fb.append(
                [
                    LAYER_MEMORY * seed_real + (1.0 - LAYER_MEMORY) * real_src[k]
                    for k in range(len(real_src))
                ]
            )
            imag_fb.append(
                [
                    LAYER_MEMORY * seed_imag + (1.0 - LAYER_MEMORY) * imag_src[k]
                    for k in range(len(imag_src))
                ]
            )
        else:
            real_fb.append(
                [
                    LAYER_MEMORY * real_fb[layer_idx - 1][k]
                    + (1.0 - LAYER_MEMORY) * real_src[k]
                    for k in range(len(real_src))
                ]
            )
            imag_fb.append(
                [
                    LAYER_MEMORY * imag_fb[layer_idx - 1][k]
                    + (1.0 - LAYER_MEMORY) * imag_src[k]
                    for k in range(len(imag_src))
                ]
            )
    return _normalize_layers(real_fb), _normalize_layers(imag_fb)


def _propagate(pos, adj, field):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            act = L * (1.0 - lf.real)
            phase = 0.70 * lf.imag
            amps[j] += amps[i] * cmath.exp(1j * (K * act + phase)) * w * hm / (L * L)
    return amps


def _source_field_layers(pos, source_idx, source_strength):
    mx, my, mz = pos[source_idx]
    field = []
    for x, y, z in pos:
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + FIELD_EPS
        field.append(source_strength / r)
    return field


def _phase_ramp_metrics(pos, det, ref_amps, test_amps):
    z_vals = [pos[i][2] for i in det]
    ref_probs = [abs(ref_amps[i]) ** 2 for i in det]
    test_probs = [abs(test_amps[i]) ** 2 for i in det]
    peak = max(max(ref_probs), max(test_probs), 1e-30)
    use = [i for i, (pr, pt) in enumerate(zip(ref_probs, test_probs)) if max(pr, pt) >= 0.02 * peak]
    if len(use) < 3:
        use = [i for i, (pr, pt) in enumerate(zip(ref_probs, test_probs)) if max(pr, pt) >= 1e-4 * peak]
    if len(use) < 3:
        use = list(range(len(det)))

    diffs = []
    prev = None
    acc = 0.0
    for j in use:
        d = cmath.phase(test_amps[det[j]]) - cmath.phase(ref_amps[det[j]])
        while d <= -math.pi:
            d += 2.0 * math.pi
        while d > math.pi:
            d -= 2.0 * math.pi
        if prev is None:
            acc = d
        else:
            step = d - prev
            while step <= -math.pi:
                step += 2.0 * math.pi
            while step > math.pi:
                step -= 2.0 * math.pi
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


def _self_consistent_field(pos, adj, layers, base_field, alpha):
    """Iterate a beam-sourced feedback field on the grown row."""
    if alpha <= 0.0:
        return [complex(v, 0.0) for v in base_field], 0.0

    hw = int(PW / H)
    field = [complex(v, 0.0) for v in base_field]
    residual = 0.0
    for _ in range(ITERATIONS):
        amps = _propagate(pos, adj, field)
        dens = _layer_density(amps, layers)
        current = _layer_current(dens)
        real_fb, imag_fb = _build_feedback_field(dens, current, hw)

        next_field: list[complex] = []
        diff_acc = 0.0
        for layer_idx, layer_nodes in enumerate(layers):
            for k, idx in enumerate(layer_nodes):
                next_field.append(
                    complex(
                        base_field[idx]
                        + alpha * TARGET_FIELD_MAX * REAL_FEEDBACK_GAIN * real_fb[layer_idx][k],
                        alpha * TARGET_FIELD_MAX * IMAG_FEEDBACK_GAIN * imag_fb[layer_idx][k],
                    )
                )
                diff_acc += abs(next_field[-1] - field[idx])
        residual = diff_acc / max(1, len(pos))
        field = next_field

    return field, residual


def _run_seed(seed: int):
    pos, adj, layers, nmap = grow(seed)
    det = layers[-1]
    gl = 2 * NL // 3
    source_idx = min(
        layers[gl],
        key=lambda i: (pos[i][1]) ** 2 + (pos[i][2] - Z_MASS) ** 2,
    )

    free_amps = _propagate(pos, adj, [0j] * len(pos))
    z_free = (
        sum(abs(free_amps[d]) ** 2 * pos[d][2] for d in det) /
        sum(abs(free_amps[d]) ** 2 for d in det)
    ) if sum(abs(free_amps[d]) ** 2 for d in det) > 1e-30 else 0.0

    base_raw = _source_field_layers(pos, source_idx, FIELD_STRENGTH)
    ref_max = max(abs(v) for v in base_raw) if base_raw else 0.0
    gain = TARGET_FIELD_MAX / ref_max if ref_max > 1e-30 else 1.0

    out = {
        "escape": {},
        "delta_z": {},
        "phase_slope": {},
        "phase_r2": {},
        "phase_span": {},
        "residual": {},
    }

    ref_amps = None
    p0 = None

    for alpha in ALPHAS:
        base_scaled = [gain * v for v in base_raw]
        field, residual = _self_consistent_field(pos, adj, layers, base_scaled, alpha)
        amps = _propagate(pos, adj, field)
        p_det = sum(abs(amps[d]) ** 2 for d in det)
        z_det = sum(abs(amps[d]) ** 2 * pos[d][2] for d in det) / p_det if p_det > 1e-30 else 0.0
        if alpha == 0.0:
            ref_amps = amps
            p0 = p_det
        slope, r2, span = _phase_ramp_metrics(pos, det, ref_amps or amps, amps)
        out["escape"][alpha] = p_det / p0 if p0 and p0 > 1e-30 else 0.0
        out["delta_z"][alpha] = z_det - z_free
        out["phase_slope"][alpha] = slope
        out["phase_r2"][alpha] = r2
        out["phase_span"][alpha] = span
        out["residual"][alpha] = residual

    fm = {0.0: None, 0.5: None}
    for alpha in fm:
        deltas = []
        strengths = []
        for s in SOURCE_STRENGTHS:
            raw = _source_field_layers(pos, source_idx, s)
            base_scaled = [gain * v for v in raw]
            field, _ = _self_consistent_field(pos, adj, layers, base_scaled, alpha)
            amps = _propagate(pos, adj, field)
            p_det = sum(abs(amps[d]) ** 2 for d in det)
            z_det = sum(abs(amps[d]) ** 2 * pos[d][2] for d in det) / p_det if p_det > 1e-30 else 0.0
            deltas.append(abs(z_det - z_free))
            strengths.append(s)
        fm[alpha] = _fit_power(strengths, deltas)

    return SeedResult(
        seed=seed,
        escape=out["escape"],
        delta_z=out["delta_z"],
        phase_slope=out["phase_slope"],
        phase_r2=out["phase_r2"],
        phase_span=out["phase_span"],
        residual=out["residual"],
        fm_alpha0=fm[0.0],
        fm_alpha05=fm[0.5],
        exact_alpha0=out["escape"][0.0],
    )


def main() -> None:
    t0 = time.time()
    print("=" * 108)
    print("GATE B GROWN PROPAGATING FIELD RADICAL")
    print("  retained moderate-drift grown row, beam-sourced self-consistent field")
    print("  comparison: alpha=0 static baseline vs alpha-activated feedback field")
    print("=" * 108)
    print(f"row: drift={DRIFT}, restore={RESTORE}, seeds={SEEDS}")
    print(f"source z = {Z_MASS}, field strength = {FIELD_STRENGTH:.1e}, field eps = {FIELD_EPS}")
    print(f"alpha sweep = {ALPHAS}")
    print(f"iterations = {ITERATIONS}, layer memory = {LAYER_MEMORY}, real gain = {REAL_FEEDBACK_GAIN}, imag gain = {IMAG_FEEDBACK_GAIN}")
    print()

    rows: list[SeedResult] = []
    for seed in SEEDS:
        rows.append(_run_seed(seed))

    print("REDUCTION CHECK")
    print("  alpha=0 field is exactly the retained grown baseline by construction")
    print()

    header = ["seed"] + [f"esc({alpha:.2f})" for alpha in ALPHAS[1:]] + [
        f"phase_slope({ALPHAS[-1]:.2f})",
        f"phase_span({ALPHAS[-1]:.2f})",
        f"resid({ALPHAS[-1]:.2f})",
        "F~M(0.0)",
        f"F~M({ALPHAS[-1]:.1f})",
    ]
    print(" ".join(f"{h:>15s}" for h in header))
    print("-" * 164)

    for row in rows:
        vals = [f"{row.seed:15d}"]
        for alpha in ALPHAS[1:]:
            vals.append(f"{row.escape[alpha]:15.3f}")
        vals.extend(
            [
                f"{row.phase_slope[ALPHAS[-1]]:15.4f}",
                f"{row.phase_span[ALPHAS[-1]]:15.3f}",
                f"{row.residual[ALPHAS[-1]]:15.3e}",
                f"{row.fm_alpha0:15.2f}" if row.fm_alpha0 is not None else f"{'n/a':>15s}",
                f"{row.fm_alpha05:15.2f}" if row.fm_alpha05 is not None else f"{'n/a':>15s}",
            ]
        )
        print(" ".join(vals))

    print()
    print("AGGREGATE")
    for alpha in ALPHAS:
        esc = [r.escape[alpha] for r in rows]
        dz = [r.delta_z[alpha] for r in rows]
        slope = [r.phase_slope[alpha] for r in rows]
        r2 = [r.phase_r2[alpha] for r in rows]
        span = [r.phase_span[alpha] for r in rows]
        resid = [r.residual[alpha] for r in rows]
        print(
            f"  alpha={alpha:>4.2f} "
            f"escape={_mean(esc):.3f} "
            f"delta_z={_mean(dz):+.6e} "
            f"phase_slope={_mean(slope):+.4f} "
            f"R2={_mean(r2):.3f} "
            f"span={_mean(span):.3f} "
            f"resid={_mean(resid):.3e}"
        )

    fm0 = [r.fm_alpha0 for r in rows if r.fm_alpha0 is not None]
    fm05 = [r.fm_alpha05 for r in rows if r.fm_alpha05 is not None]
    print()
    print("WEAK-FIELD SANITY")
    print(
        f"  F~M exponent at alpha=0: {statistics.mean(fm0):.3f}"
        if fm0
        else "  F~M exponent at alpha=0: n/a"
    )
    print(
        f"  F~M exponent at alpha=0.5: {statistics.mean(fm05):.3f}"
        if fm05
        else "  F~M exponent at alpha=0.5: n/a"
    )

    print()
    print("SAFE READ")
    print("  alpha=0 is an exact reduction to the retained grown baseline")
    print("  the promoted observable is the detector-line phase ramp")
    print("  if the phase ramp and escape stay flat once the feedback field is")
    print("  self-consistent, this is a bounded no-go for the radical attempt")
    print(f"\nTotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
