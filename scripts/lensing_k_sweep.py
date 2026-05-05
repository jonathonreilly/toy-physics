#!/usr/bin/env python3
"""Lensing slope vs k (phase coupling) sweep.

All previous measurements used k·H = 2.5. This sweeps k·H from
0.5 to 5.0 to test whether the -1.40 slope depends on the wave
coupling constant.

If slope is k-INDEPENDENT → the -1.40 is geometric (set by β)
If slope VARIES with k → the eikonal gap is a wave-coupling effect

Uses Fam1 at H=0.25, 3 seeds per k-value (enough to estimate mean
and per-seed variance). Impact parameters b ∈ {3, 4, 5, 6}.
"""

from __future__ import annotations

# Heavy k-sweep over many seeds and slope-fit windows. Empirically
# observed to exceed the 30-min ceiling under concurrency contention,
# so the AUDIT_TIMEOUT_SEC is raised to 60 min (3600 s). If this still
# times out, the right fix is to add a --quick subsample mode or split
# the sweep across multiple runners. See
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 3600

import math
import random
import sys
import time

BETA = 0.8
T_PHYS = 15.0
PW_PHYS = 6.0
MAX_D_PHYS = 3.0
SRC_LAYER_FRAC = 1.0 / 3.0
DRIFT, RESTORE = 0.20, 0.70  # Fam1

B_VALUES = [3.0, 4.0, 5.0, 6.0]
KH_VALUES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
SEEDS = [0, 1, 2]


def grow(seed, NL, PW, H):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos = []
    adj = {}
    nmap = {}
    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    for layer in range(1, NL):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y, z = iy * H, iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, DRIFT * H)
                    z = pz + rng.gauss(0, DRIFT * H)
                    y = y * (1 - RESTORE) + (iy * H) * RESTORE
                    z = z * (1 - RESTORE) + (iz * H) * RESTORE
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            adj.setdefault(si, []).append(di)
    return pos, adj, nmap, NL, hw


def true_kubo(pos, adj, NL, PW, H, k_phase, x_src, z_src):
    n = len(pos)
    A = [0j] * n
    B = [0j] * n
    A[0] = 1.0 + 0j
    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = H * H
    for i in order:
        ai = A[i]
        bi = B[i]
        if abs(ai) < 1e-30 and abs(bi) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            r_field = math.sqrt((mx - x_src) ** 2 + (mz - z_src) ** 2) + 0.1
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            w_eff = w * h2 / (L * L)
            dphi_ds = complex(0.0, -k_phase * L / r_field) * phi
            A[j] += ai * phi * w_eff
            B[j] += (bi * phi + ai * dphi_ds) * w_eff

    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds_idx = n - npl
    weights = [abs(A[k]) ** 2 for k in range(ds_idx, n)]
    zs = [pos[k][2] for k in range(ds_idx, n)]
    T0 = sum(weights)
    if T0 <= 0:
        return float('nan')
    cz_free = sum(w * z for w, z in zip(weights, zs)) / T0
    dT_ds = sum(2.0 * (A[k].conjugate() * B[k]).real for k in range(ds_idx, n))
    dN_ds = sum(2.0 * (A[k].conjugate() * B[k]).real * pos[k][2]
                for k in range(ds_idx, n))
    N0 = T0 * cz_free
    kubo = dN_ds / T0 - N0 * dT_ds / (T0 * T0)
    return kubo


def power_law_fit(bs, ks):
    valid = [(b, k) for b, k in zip(bs, ks) if not math.isnan(k) and k > 0]
    if len(valid) < 3:
        return None
    bs_v, ks_v = zip(*valid)
    n = len(bs_v)
    log_b = [math.log(b) for b in bs_v]
    log_k = [math.log(k) for k in ks_v]
    sx, sy = sum(log_b), sum(log_k)
    sxx = sum(x * x for x in log_b)
    sxy = sum(x * y for x, y in zip(log_b, log_k))
    den = n * sxx - sx * sx
    if abs(den) < 1e-30:
        return None
    slope = (n * sxy - sx * sy) / den
    intercept = (sy - slope * sx) / n
    pred = [slope * x + intercept for x in log_b]
    ss_res = sum((y - p) ** 2 for y, p in zip(log_k, pred))
    ss_tot = sum((y - sy / n) ** 2 for y in log_k)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0
    return slope, math.exp(intercept), r2


def main():
    H = 0.25
    NL = int(T_PHYS / H) + 1
    x_src = int(NL * SRC_LAYER_FRAC) * H

    print("=" * 80)
    print("LENSING SLOPE vs k (PHASE COUPLING) SWEEP")
    print(f"  H={H}, Fam1, seeds={SEEDS}")
    print(f"  k·H sweep: {KH_VALUES}")
    print(f"  b ∈ {B_VALUES}")
    print(f"  Reference: k·H=2.5 gives slope ≈ -1.40")
    print("=" * 80)

    # Pre-grow DAGs (reused across k values)
    dags = {}
    for seed in SEEDS:
        t0 = time.time()
        pos, adj, nmap, _, hw = grow(seed, NL, PW_PHYS, H)
        dt = time.time() - t0
        dags[seed] = (pos, adj, nmap, NL, hw)
        print(f"  Grew seed {seed}: nodes={len(pos)}, {dt:.1f}s", flush=True)

    # Sweep k·H
    results = {}  # {kH: {seed: [kubo_b3, kubo_b4, kubo_b5, kubo_b6]}}

    for kH in KH_VALUES:
        k_phase = kH / H
        print(f"\n{'─' * 60}")
        print(f"  k·H = {kH}  (k = {k_phase:.1f})")
        print(f"{'─' * 60}")

        results[kH] = {}
        seed_slopes = []

        for seed in SEEDS:
            pos, adj, nmap, NL_d, hw = dags[seed]
            kubos = []
            for b in B_VALUES:
                t0 = time.time()
                k = true_kubo(pos, adj, NL_d, PW_PHYS, H, k_phase, x_src, b)
                dt = time.time() - t0
                kubos.append(k)
            results[kH][seed] = kubos

            fit = power_law_fit(B_VALUES, kubos)
            if fit:
                sl, pf, r2 = fit
                seed_slopes.append(sl)
                print(f"    seed {seed}: slope={sl:+.4f}  R²={r2:.4f}  "
                      f"kubo(3)={kubos[0]:+.3f}", flush=True)
            else:
                signs = ['+' if k > 0 else ('-' if k < 0 else '0') for k in kubos]
                print(f"    seed {seed}: fit failed  signs={signs}  "
                      f"kubos={[f'{k:+.3f}' for k in kubos]}", flush=True)

        if seed_slopes:
            mean_sl = sum(seed_slopes) / len(seed_slopes)
            std_sl = math.sqrt(sum((s - mean_sl) ** 2 for s in seed_slopes) / len(seed_slopes)) if len(seed_slopes) > 1 else 0
            print(f"    Mean: {mean_sl:.4f} ± {std_sl:.4f}")

    # Summary table
    print(f"\n{'=' * 80}")
    print("SLOPE vs k·H SUMMARY")
    print("=" * 80)
    print(f"  {'k·H':>6s}  {'mean slope':>10s}  {'σ':>8s}  {'n_good':>6s}  {'kubo(3) mean':>12s}")
    print(f"  {'-' * 50}")

    slope_curve = []
    for kH in KH_VALUES:
        seed_slopes = []
        kubo3_vals = []
        for seed in SEEDS:
            kubos = results[kH][seed]
            fit = power_law_fit(B_VALUES, kubos)
            if fit:
                seed_slopes.append(fit[0])
                kubo3_vals.append(kubos[0])

        if seed_slopes:
            ms = sum(seed_slopes) / len(seed_slopes)
            ss = math.sqrt(sum((s - ms) ** 2 for s in seed_slopes) / len(seed_slopes)) if len(seed_slopes) > 1 else 0
            mk3 = sum(kubo3_vals) / len(kubo3_vals)
            print(f"  {kH:6.1f}  {ms:10.4f}  {ss:8.4f}  {len(seed_slopes):6d}  {mk3:12.4f}")
            slope_curve.append((kH, ms, ss))
        else:
            print(f"  {kH:6.1f}  {'N/A':>10s}")

    # Verdict
    if len(slope_curve) >= 3:
        slopes_only = [s for _, s, _ in slope_curve]
        slope_range = max(slopes_only) - min(slopes_only)
        slope_mean = sum(slopes_only) / len(slopes_only)
        print(f"\n  Slope range across k·H sweep: {slope_range:.4f}")
        print(f"  Mean slope across all k·H: {slope_mean:.4f}")

        if slope_range < 0.1:
            print(f"  → Slope is k-INDEPENDENT (range < 0.1)")
            print(f"  → The -1.40 is GEOMETRIC, set by β={BETA}")
        elif slope_range < 0.3:
            print(f"  → Slope shows MODERATE k-dependence")
        else:
            print(f"  → Slope is STRONGLY k-dependent (range = {slope_range:.2f})")
            print(f"  → The eikonal gap is a wave-coupling effect")

    # Eikonal comparison
    eik_slope = -1.275
    print(f"\n  Eikonal baseline: {eik_slope}")
    print(f"  Eikonal gap vs k·H:")
    for kH, ms, ss in slope_curve:
        gap = ms - eik_slope
        print(f"    k·H={kH:.1f}: gap={gap:+.4f}")


if __name__ == "__main__":
    main()
