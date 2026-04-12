#!/usr/bin/env python3
"""Lensing slope vs β (angular weight) sweep at H=0.25 on grown DAG.

Companion to the k-sweep. All previous measurements used β=0.8.
This sweeps β from 0.2 to 5.0 at fixed k·H=2.5 to test whether
the slope depends on the angular weight width.

If slope varies with β → full wave-mechanical (both k and β matter)
If slope is β-independent → angular weight is geometric, only k matters
"""

from __future__ import annotations
import math
import random
import time

K_PER_H = 2.5
T_PHYS = 15.0
PW_PHYS = 6.0
MAX_D_PHYS = 3.0
SRC_LAYER_FRAC = 1.0 / 3.0
DRIFT, RESTORE = 0.20, 0.70

B_VALUES = [3.0, 4.0, 5.0, 6.0]
BETA_VALUES = [0.2, 0.4, 0.8, 1.5, 3.0, 5.0]
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


def true_kubo_beta(pos, adj, NL, PW, H, k_phase, x_src, z_src, beta):
    """Kubo with variable β."""
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
            w = math.exp(-beta * theta * theta)
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
    k_phase = K_PER_H / H
    x_src = int(NL * SRC_LAYER_FRAC) * H

    print("=" * 80)
    print("LENSING SLOPE vs β (ANGULAR WEIGHT) SWEEP")
    print(f"  H={H}, Fam1, k·H={K_PER_H}, seeds={SEEDS}")
    print(f"  β sweep: {BETA_VALUES}")
    print(f"  σ_θ = 1/√(2β): {[f'{1/math.sqrt(2*b):.2f}' for b in BETA_VALUES]}")
    print(f"  Reference: β=0.8 gives slope ≈ -1.40")
    print("=" * 80)

    # Pre-grow DAGs
    dags = {}
    for seed in SEEDS:
        t0 = time.time()
        pos, adj, nmap, _, hw = grow(seed, NL, PW_PHYS, H)
        dt = time.time() - t0
        dags[seed] = (pos, adj, nmap, NL, hw)
        print(f"  Grew seed {seed}: nodes={len(pos)}, {dt:.1f}s", flush=True)

    results = {}

    for beta in BETA_VALUES:
        sigma_theta = 1.0 / math.sqrt(2 * beta)
        print(f"\n{'─' * 60}")
        print(f"  β = {beta}  (σ_θ = {sigma_theta:.3f} rad = {math.degrees(sigma_theta):.1f}°)")
        print(f"{'─' * 60}")

        seed_slopes = []
        for seed in SEEDS:
            pos, adj, nmap, NL_d, hw = dags[seed]
            kubos = []
            for b in B_VALUES:
                t0 = time.time()
                k = true_kubo_beta(pos, adj, NL_d, PW_PHYS, H, k_phase, x_src, b, beta)
                dt = time.time() - t0
                kubos.append(k)

            fit = power_law_fit(B_VALUES, kubos)
            if fit:
                sl, pf, r2 = fit
                seed_slopes.append(sl)
                print(f"    seed {seed}: slope={sl:+.4f}  R²={r2:.4f}  "
                      f"kubo(3)={kubos[0]:+.3f}", flush=True)
            else:
                signs = ['+' if k > 0 else '-' for k in kubos]
                print(f"    seed {seed}: fit failed  signs={signs}", flush=True)

        if seed_slopes:
            mean_sl = sum(seed_slopes) / len(seed_slopes)
            std_sl = math.sqrt(sum((s - mean_sl) ** 2 for s in seed_slopes) / len(seed_slopes)) if len(seed_slopes) > 1 else 0
            print(f"    Mean: {mean_sl:.4f} ± {std_sl:.4f}")
            results[beta] = (mean_sl, std_sl, len(seed_slopes))

    # Summary
    print(f"\n{'=' * 80}")
    print("SLOPE vs β SUMMARY")
    print("=" * 80)
    print(f"  {'β':>6s}  {'σ_θ':>8s}  {'slope':>8s}  {'σ':>8s}  {'n':>3s}")
    print(f"  {'-' * 40}")
    for beta in BETA_VALUES:
        if beta in results:
            ms, ss, n = results[beta]
            st = 1.0 / math.sqrt(2 * beta)
            print(f"  {beta:6.1f}  {st:8.3f}  {ms:8.4f}  {ss:8.4f}  {n:3d}")

    if len(results) >= 3:
        slopes = [results[b][0] for b in BETA_VALUES if b in results]
        slope_range = max(slopes) - min(slopes)
        print(f"\n  Slope range across β sweep: {slope_range:.4f}")
        if slope_range < 0.1:
            print(f"  → Slope is β-INDEPENDENT (range < 0.1)")
        elif slope_range < 0.3:
            print(f"  → Slope shows MODERATE β-dependence (range = {slope_range:.2f})")
        else:
            print(f"  → Slope is STRONGLY β-dependent (range = {slope_range:.2f})")

    # Cross-reference with k-sweep
    print(f"\n  PARAMETER DEPENDENCE SUMMARY:")
    print(f"    k-sweep range (β=0.8 fixed): ~2.0 (from +0.58 to -1.43)")
    if len(results) >= 3:
        slopes = [results[b][0] for b in BETA_VALUES if b in results]
        print(f"    β-sweep range (k·H=2.5 fixed): {max(slopes)-min(slopes):.2f}")
        print(f"    → {'k dominates' if slope_range < 1.0 else 'Both matter comparably'}")


if __name__ == "__main__":
    main()
