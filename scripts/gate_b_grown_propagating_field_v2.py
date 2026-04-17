#!/usr/bin/env python3
"""Gate B grown propagating-field v2 probe.

This is a stricter follow-up to the minimal causal-memory no-go.

Goal:
  Test whether a minimally stronger retained-grown architecture than simple
  layer-memory / gamma blending can produce a causal observable on the
  moderate-drift Gate B row while still reducing exactly to the retained
  grown baseline at gamma = 0.

Architecture:
  - retained grown geometry row only: drift=0.2, restore=0.7
  - static source-resolved field as the zero-coupling baseline
  - a separate complex transport envelope on the grown graph
  - second-order layer recurrence + transverse coupling + phase-tilted drive
  - gamma activates the transport envelope without changing the gamma=0
    baseline

Observable:
  - detector escape ratio relative to gamma=0
  - detector-line phase ramp relative to the static baseline
  - weak-field mass-scaling exponent as a sanity check

The claim surface is intentionally narrow:
  if the transport envelope does not produce a coherent causal observable, the
  correct outcome is a bounded no-go for this stronger grown-row architecture.
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
SEEDS = list(range(4))
GAMMAS = [0.0, 0.05, 0.1, 0.2, 0.5]
SOURCE_STRENGTHS = [1e-6, 1e-5, 5e-5]
Z_MASS = 3.0
FIELD_STRENGTH = 5e-5
FIELD_EPS = 0.1
TRANSPORT_WAVE_SPEED2 = 0.18
TRANSPORT_DAMP = 0.08
TRANSPORT_SOURCE_BLEND = 0.58
TRANSPORT_PHASE_RATE = 0.45
TRANSPORT_IMAG_GAIN = 0.75


@dataclass(frozen=True)
class SeedResult:
    seed: int
    escape: dict[float, float]
    delta_z: dict[float, float]
    phase_slope: dict[float, float]
    phase_r2: dict[float, float]
    phase_span: dict[float, float]
    fm_gamma0: float | None
    fm_gamma05: float | None
    exact_gamma0: float


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


def _layer_laplacian(values: list[complex], hw: int) -> list[complex]:
    grid_n = 2 * hw + 1
    out = [0j] * len(values)
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            k = (iy + hw) * grid_n + (iz + hw)
            center = values[k]
            total = 0j
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


def _flatten_layers(layer_values: list[list[complex]], layers: list[list[int]], n: int) -> list[complex]:
    out = [0j] * n
    for layer_idx, layer_nodes in enumerate(layers):
        row = layer_values[layer_idx]
        for k, idx in enumerate(layer_nodes):
            out[idx] = row[k]
    return out


def _transport_field(pos, layers, static_field, gamma):
    """Complex transport envelope on top of the static baseline.

    gamma controls only the transported component. When gamma=0, the returned
    field reduces exactly to the static baseline.
    """

    n = len(pos)
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    static_layers: list[list[float]] = []
    for layer_nodes in layers:
        static_layers.append([static_field[idx] for idx in layer_nodes])

    if gamma <= 0.0:
        return [complex(v, 0.0) for v in static_field]

    q: list[list[complex]] = [[0j for _ in range(npl)] for _ in range(len(layers))]
    q[0] = [0j]
    if len(layers) > 1:
        q[1] = [
            TRANSPORT_SOURCE_BLEND
            * static_layers[1][k]
            * cmath.exp(1j * TRANSPORT_PHASE_RATE * H)
            for k in range(npl)
        ]

    for layer_idx in range(2, len(layers)):
        lap = _layer_laplacian(q[layer_idx - 1], hw)
        drive_phase = cmath.exp(1j * TRANSPORT_PHASE_RATE * layer_idx * H)
        for k in range(npl):
            drive = static_layers[layer_idx][k] * drive_phase
            prev2 = q[layer_idx - 2][k] if layer_idx > 2 else 0j
            q[layer_idx][k] = (
                (2.0 - TRANSPORT_DAMP) * q[layer_idx - 1][k]
                - (1.0 - TRANSPORT_DAMP) * prev2
                + TRANSPORT_WAVE_SPEED2 * lap[k]
                + TRANSPORT_SOURCE_BLEND * drive
            )

    transported = [[complex(static_layers[0][0], 0.0)]]
    for layer_idx in range(1, len(layers)):
        transported.append(
            [complex(static_layers[layer_idx][k], 0.0) + gamma * q[layer_idx][k] for k in range(npl)]
        )
    return _flatten_layers(transported, layers, n)


def propagate(pos, adj, field):
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
            phase = TRANSPORT_IMAG_GAIN * lf.imag
            amps[j] += amps[i] * cmath.exp(1j * (K * act + phase)) * w * hm / (L * L)
    return amps


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


def _detector_probs(amps, det):
    return [abs(amps[i]) ** 2 for i in det]


def _run_seed(seed):
    pos, adj, layers, nmap = grow(seed)
    det = layers[-1]
    gl = 2 * NL // 3
    source_idx = min(
        layers[gl],
        key=lambda i: (pos[i][1]) ** 2 + (pos[i][2] - Z_MASS) ** 2,
    )
    static = _static_field(pos, source_idx)
    free_field = [0.0] * len(pos)
    free_amps = propagate(pos, adj, free_field)
    p_free = sum(abs(free_amps[d]) ** 2 for d in det)
    z_free = sum(abs(free_amps[d]) ** 2 * pos[d][2] for d in det) / p_free if p_free > 1e-30 else 0.0

    out = {
        "escape": {},
        "delta_z": {},
        "phase_slope": {},
        "phase_r2": {},
        "phase_span": {},
    }

    ref_amps = None
    p0 = None
    for gamma in GAMMAS:
        field = _transport_field(pos, layers, static, gamma)
        amps = propagate(pos, adj, field)
        p_det = sum(abs(amps[d]) ** 2 for d in det)
        z_det = sum(abs(amps[d]) ** 2 * pos[d][2] for d in det) / p_det if p_det > 1e-30 else 0.0
        if gamma == 0.0:
            ref_amps = amps
            p0 = p_det
        slope, r2, span = _phase_ramp_metrics(pos, det, ref_amps or amps, amps)
        out["escape"][gamma] = p_det / p0 if p0 and p0 > 1e-30 else 0.0
        out["delta_z"][gamma] = z_det - z_free
        out["phase_slope"][gamma] = slope
        out["phase_r2"][gamma] = r2
        out["phase_span"][gamma] = span

    # Weak-field mass-scaling sanity check at gamma=0 and gamma=0.5.
    fm = {0.0: None, 0.5: None}
    for gamma in fm:
        deltas = []
        strengths = []
        for s in SOURCE_STRENGTHS:
            sf = [v * (s / FIELD_STRENGTH) for v in static]
            field = _transport_field(pos, layers, sf, gamma)
            amps = propagate(pos, adj, field)
            p_det = sum(abs(amps[d]) ** 2 for d in det)
            z_det = sum(abs(amps[d]) ** 2 * pos[d][2] for d in det) / p_det if p_det > 1e-30 else 0.0
            deltas.append(abs(z_det - z_free))
            strengths.append(s)
        fm[gamma] = _fit_power(strengths, deltas)

    return SeedResult(
        seed=seed,
        escape=out["escape"],
        delta_z=out["delta_z"],
        phase_slope=out["phase_slope"],
        phase_r2=out["phase_r2"],
        phase_span=out["phase_span"],
        fm_gamma0=fm[0.0],
        fm_gamma05=fm[0.5],
        exact_gamma0=out["escape"][0.0],
    )


def main():
    t0 = time.time()
    print("=" * 104)
    print("GATE B GROWN PROPAGATING FIELD V2")
    print("  retained moderate-drift grown row, complex transport-envelope architecture")
    print("  comparison: gamma=0 static baseline vs gamma-activated transport field")
    print("=" * 104)
    print(f"row: drift={DRIFT}, restore={RESTORE}, seeds={SEEDS}")
    print(f"source z = {Z_MASS}, field strength = {FIELD_STRENGTH:.1e}, field eps = {FIELD_EPS}")
    print(f"gamma sweep = {GAMMAS}")
    print(
        "transport constants: "
        f"wave_speed2={TRANSPORT_WAVE_SPEED2}, damp={TRANSPORT_DAMP}, "
        f"source_blend={TRANSPORT_SOURCE_BLEND}, phase_rate={TRANSPORT_PHASE_RATE}, "
        f"imag_gain={TRANSPORT_IMAG_GAIN}"
    )
    print()

    rows: list[SeedResult] = []
    for seed in SEEDS:
        rows.append(_run_seed(seed))

    print("REDUCTION CHECK")
    print("  gamma=0 field is exactly the retained grown baseline by construction")
    print()

    header = ["seed", "P_escape(0.05)", "P_escape(0.10)", "P_escape(0.20)", "P_escape(0.50)", "phase_slope(0.50)", "phase_span(0.50)", "F~M(0.0)", "F~M(0.5)"]
    print(" ".join(f"{h:>15s}" for h in header))
    print("-" * 136)

    for row in rows:
        vals = [
            f"{row.seed:15d}",
            f"{row.escape[0.05]:15.3f}",
            f"{row.escape[0.10]:15.3f}",
            f"{row.escape[0.20]:15.3f}",
            f"{row.escape[0.50]:15.3f}",
            f"{row.phase_slope[0.50]:15.4f}",
            f"{row.phase_span[0.50]:15.3f}",
            f"{row.fm_gamma0:15.2f}" if row.fm_gamma0 is not None else f"{'n/a':>15s}",
            f"{row.fm_gamma05:15.2f}" if row.fm_gamma05 is not None else f"{'n/a':>15s}",
        ]
        print(" ".join(vals))

    print()
    print("AGGREGATE")
    for gamma in [0.0, 0.05, 0.1, 0.2, 0.5]:
        esc = [r.escape[gamma] for r in rows]
        dz = [r.delta_z[gamma] for r in rows]
        slope = [r.phase_slope[gamma] for r in rows]
        r2 = [r.phase_r2[gamma] for r in rows]
        span = [r.phase_span[gamma] for r in rows]
        print(
            f"  gamma={gamma:>4.2f} "
            f"escape={_mean(esc):.3f} "
            f"delta_z={_mean(dz):+.6e} "
            f"phase_slope={_mean(slope):+.4f} "
            f"R2={_mean(r2):.3f} "
            f"span={_mean(span):.3f}"
        )

    fm0 = [r.fm_gamma0 for r in rows if r.fm_gamma0 is not None]
    fm05 = [r.fm_gamma05 for r in rows if r.fm_gamma05 is not None]
    print()
    print("WEAK-FIELD SANITY")
    print(
        f"  F~M exponent at gamma=0: {statistics.mean(fm0):.3f}"
        if fm0
        else "  F~M exponent at gamma=0: n/a"
    )
    print(
        f"  F~M exponent at gamma=0.5: {statistics.mean(fm05):.3f}"
        if fm05
        else "  F~M exponent at gamma=0.5: n/a"
    )

    print()
    print("SAFE READ")
    print("  gamma=0 is an exact reduction to the retained grown baseline")
    print("  any retained causal signal must show up as a nontrivial escape or phase observable at gamma>0")
    print("  if both stay flat, the stronger transport-envelope architecture is still a no-go")
    print(f"\nTotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
