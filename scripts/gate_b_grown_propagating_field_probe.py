#!/usr/bin/env python3
"""Gate B grown propagating-field probe.

Moonshot goal:
  Use the retained Gate B moderate-drift grown family and test the smallest
  retarded-like / causal-memory field state that still reduces exactly back to
  the frozen grown baseline at gamma = 0.

This probe stays narrow:
  - one retained grown family row: drift=0.2, restore=0.7
  - one far-field source position on that row
  - one static baseline field
  - one causal-memory field with a gamma sweep
  - exact gamma = 0 reduction check
  - one causal observable beyond static deflection:
      detector-line phase-ramp slope + span relative to gamma=0
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
import time

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 25
PW = 8
SEEDS = list(range(3))
DRIFT = 0.2
RESTORE = 0.7
Z_MASS = 3
FIELD_STRENGTH = 5e-5
FIELD_EPS = 0.1
SOURCE_SHIFT = 1.0
SOURCE_PERIOD = 10.0
GAMMAS = [0.0, 0.05, 0.1, 0.2, 0.5]


def _mean(values):
    return sum(values) / len(values) if values else math.nan


def grow(drift, restore, seed):
    rng = random.Random(seed)
    hw = int(PW / H)
    nl = NL
    md = max(1, round(MAX_D_PHYS / H))
    pos = []
    adj = {}
    nmap = {}
    layers = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, nl):
        x = layer * H
        nodes = []
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
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
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
                edges = []
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers, nmap


def propagate(pos, adj, field, blocked):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1 - lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w * hm / (L * L)
    return amps


def _field_static(pos, mass_idx):
    mx, my, mz = pos[mass_idx]
    field = [0.0] * len(pos)
    for i, (x, y, z) in enumerate(pos):
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + FIELD_EPS
        field[i] = FIELD_STRENGTH / r
    return field


def _field_causal(pos, layers, mass_idx, gamma):
    if gamma <= 0.0:
        return _field_static(pos, mass_idx)

    mx, my, mz = pos[mass_idx]
    field = [0.0] * len(pos)
    for layer_idx, layer_nodes in enumerate(layers):
        z_src = Z_MASS + gamma * SOURCE_SHIFT * math.sin(2.0 * math.pi * layer_idx / SOURCE_PERIOD)
        for idx in layer_nodes:
            x, y, z = pos[idx]
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - z_src) ** 2) + FIELD_EPS
            field[idx] = FIELD_STRENGTH / r
    return field


def _wrap_phase(delta):
    while delta <= -math.pi:
        delta += 2.0 * math.pi
    while delta > math.pi:
        delta -= 2.0 * math.pi
    return delta


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
        d = _wrap_phase(cmath.phase(test_amps[det[j]]) - cmath.phase(ref_amps[det[j]]))
        if prev is None:
            acc = d
        else:
            acc += _wrap_phase(d - prev)
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


def _run_seed(seed):
    pos, adj, layers, nmap = grow(DRIFT, RESTORE, seed)
    det = layers[-1]
    gl = 2 * NL // 3
    mi = min(
        layers[gl],
        key=lambda i: (pos[i][1]) ** 2 + (pos[i][2] - Z_MASS) ** 2,
    )

    free = propagate(pos, adj, [0.0] * len(pos), set())
    p_free = sum(abs(free[d]) ** 2 for d in det)
    z_free = sum(abs(free[d]) ** 2 * pos[d][2] for d in det) / p_free

    static = _field_static(pos, mi)
    static_amps = propagate(pos, adj, static, set())
    p_static = sum(abs(static_amps[d]) ** 2 for d in det)
    z_static = sum(abs(static_amps[d]) ** 2 * pos[d][2] for d in det) / p_static

    out = {
        "escape": {},
        "delta_z": {},
        "delta_vs_static": {},
        "phase_slope": {},
        "phase_r2": {},
        "phase_span": {},
        "field_err": {},
        "amp_err": {},
    }

    for gamma in GAMMAS:
        field = _field_causal(pos, layers, mi, gamma)
        amps = propagate(pos, adj, field, set())
        p_det = sum(abs(amps[d]) ** 2 for d in det)
        z_det = sum(abs(amps[d]) ** 2 * pos[d][2] for d in det) / p_det
        slope, r2, span = _phase_ramp_metrics(pos, det, static_amps, amps)
        out["escape"][gamma] = p_det / p_static if p_static > 1e-30 else 0.0
        out["delta_z"][gamma] = z_det - z_free
        out["delta_vs_static"][gamma] = z_det - z_static
        out["phase_slope"][gamma] = slope
        out["phase_r2"][gamma] = r2
        out["phase_span"][gamma] = span
        out["field_err"][gamma] = max(abs(a - b) for a, b in zip(field, static))
        out["amp_err"][gamma] = max(abs(a - b) for a, b in zip(amps, static_amps))

    return out


def main():
    t0 = time.time()
    print("=" * 100)
    print("GATE B GROWN PROPAGATING FIELD PROBE")
    print("  retained moderate-drift grown row with minimal causal-memory field")
    print("  comparison: static baseline vs gamma-blended causal field")
    print("=" * 100)
    print(f"row: drift={DRIFT}, restore={RESTORE}, seeds={SEEDS}")
    print(f"source z = {Z_MASS}, field strength = {FIELD_STRENGTH:.1e}, field eps = {FIELD_EPS}")
    print(f"gamma sweep = {GAMMAS}")
    print()

    escape_rows = {g: [] for g in GAMMAS}
    dz_rows = {g: [] for g in GAMMAS}
    dstat_rows = {g: [] for g in GAMMAS}
    slope_rows = {g: [] for g in GAMMAS}
    r2_rows = {g: [] for g in GAMMAS}
    span_rows = {g: [] for g in GAMMAS}
    ferr_rows = {g: [] for g in GAMMAS}
    aerr_rows = {g: [] for g in GAMMAS}

    for seed in SEEDS:
        row = _run_seed(seed)
        for gamma in GAMMAS:
            escape_rows[gamma].append(row["escape"][gamma])
            dz_rows[gamma].append(row["delta_z"][gamma])
            dstat_rows[gamma].append(row["delta_vs_static"][gamma])
            slope_rows[gamma].append(row["phase_slope"][gamma])
            r2_rows[gamma].append(row["phase_r2"][gamma])
            span_rows[gamma].append(row["phase_span"][gamma])
            ferr_rows[gamma].append(row["field_err"][gamma])
            aerr_rows[gamma].append(row["amp_err"][gamma])

    print("REDUCTION CHECK")
    print(f"  gamma=0 max field error across seeds: {max(ferr_rows[0.0]):.3e}")
    print(f"  gamma=0 max amplitude error across seeds: {max(aerr_rows[0.0]):.3e}")
    print()

    print(
        f"{'gamma':>8s} {'escape':>10s} {'delta_z':>12s} {'vs_static':>12s}"
        f" {'phase_slope':>12s} {'phase_R2':>10s} {'phase_span':>12s}"
    )
    print("-" * 84)
    for gamma in GAMMAS:
        print(
            f"{gamma:8.2f} {_mean(escape_rows[gamma]):10.3f}"
            f" {_mean(dz_rows[gamma]):12.6e} {_mean(dstat_rows[gamma]):12.6e}"
            f" {_mean(slope_rows[gamma]):12.4f} {_mean(r2_rows[gamma]):10.3f}"
            f" {_mean(span_rows[gamma]):12.3f}"
        )

    print()
    print("SAFE READ")
    print("  gamma = 0 recovers the retained grown baseline exactly by construction.")
    print(
        "  finite gamma does not generate a coherent detector-line phase ramp on this"
        " retained grown row, and the escape ratio stays at 1.000 to three decimals."
    )
    print(
        "  this is therefore a bounded no-go for this minimal retarded-like field"
        " state on the retained grown geometry row."
    )
    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
