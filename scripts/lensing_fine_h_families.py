#!/usr/bin/env python3
"""Fine-H (H=0.25) lensing slope on ALL THREE families.

The -1.4335 slope at H=0.25 was only measured on Fam1. This script
tests whether Fam2 and Fam3 converge to the same slope at fine H.

If all three families agree at H=0.25:
  → The -1.43 slope is a kernel property, not a Fam1 artifact
  → The eikonal gap (0.158) is also universal

If they disagree:
  → The slope is family-dependent at fine H
  → The H=0.5 consistency was coincidental

Reports per-seed slopes (not just seed-mean) per review requirements.
"""

from __future__ import annotations
import math
import random
import time

BETA = 0.8
K_PER_H = 2.5
T_PHYS = 15.0
PW_PHYS = 6.0
MAX_D_PHYS = 3.0
SRC_LAYER_FRAC = 1.0 / 3.0

FAMILIES = {
    "Fam1": (0.20, 0.70),
    "Fam2": (0.05, 0.30),
    "Fam3": (0.50, 0.90),
}


def grow(seed, drift, restore, NL, PW, H):
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
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
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
    """Returns (slope, prefactor, r2) or None if fit fails."""
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
    seeds = [0, 1, 2, 3, 4]
    b_values = [3.0, 4.0, 5.0, 6.0]

    print("=" * 80)
    print("FINE-H LENSING SLOPE: ALL THREE FAMILIES AT H=0.25")
    print(f"  H={H}, NL={NL}, T_phys≈{(NL-1)*H:.1f}")
    print(f"  k={k_phase:.1f} (k·H={K_PER_H}), β={BETA}")
    print(f"  b ∈ {b_values}, seeds={seeds}")
    print(f"  Reference: Fam1 seed0 at H=0.25 gave slope = −1.4335")
    print("=" * 80)

    all_results = {}

    for fam_name, (drift, restore) in FAMILIES.items():
        print(f"\n{'─' * 70}")
        print(f"  {fam_name}: drift={drift}, restore={restore}")
        print(f"{'─' * 70}")

        # Per-seed kubos: {seed: {b: kubo}}
        seed_kubos = {}

        for seed in seeds:
            t0 = time.time()
            x_src = int(NL * SRC_LAYER_FRAC) * H
            pos, adj, nmap, _, hw = grow(seed, drift, restore, NL, PW_PHYS, H)
            n = len(pos)
            if seed == 0:
                print(f"  nodes={n}, hw={hw}")

            seed_kubos[seed] = {}
            for b in b_values:
                k = true_kubo(pos, adj, NL, PW_PHYS, H, k_phase, x_src, b)
                seed_kubos[seed][b] = k

            dt = time.time() - t0
            print(f"  seed {seed}: {dt:.1f}s  kubos={[f'{seed_kubos[seed][b]:+.3f}' for b in b_values]}")

        # Seed-mean
        print(f"\n  Seed-mean:")
        print(f"  {'b':>5s}  {'<kubo>':>10s}  {'σ':>10s}")
        print(f"  {'-' * 30}")
        mean_kubos = {}
        for b in b_values:
            vals = [seed_kubos[s][b] for s in seeds if not math.isnan(seed_kubos[s][b])]
            if len(vals) < 2:
                continue
            mean_k = sum(vals) / len(vals)
            std_k = math.sqrt(sum((v - mean_k) ** 2 for v in vals) / len(vals))
            mean_kubos[b] = mean_k
            print(f"  {b:5.1f}  {mean_k:+10.4f}  {std_k:10.4f}")

        # Seed-mean slope
        if len(mean_kubos) >= 3:
            fit = power_law_fit(list(mean_kubos.keys()), list(mean_kubos.values()))
            if fit:
                slope, pf, r2 = fit
                print(f"\n  Seed-mean: kubo ≈ {pf:.3f} · b^({slope:.4f})  R² = {r2:.6f}")
                all_results[fam_name] = {"mean_slope": slope, "mean_pf": pf, "mean_r2": r2}

        # Per-seed slopes
        print(f"\n  Per-seed slopes:")
        seed_slopes = []
        for seed in seeds:
            fit = power_law_fit(b_values, [seed_kubos[seed][b] for b in b_values])
            if fit:
                slope, pf, r2 = fit
                print(f"    seed {seed}: slope={slope:+.4f}  R²={r2:.4f}")
                seed_slopes.append(slope)
            else:
                print(f"    seed {seed}: fit failed (mixed signs or NaN)")

        if seed_slopes:
            mean_sl = sum(seed_slopes) / len(seed_slopes)
            std_sl = math.sqrt(sum((s - mean_sl) ** 2 for s in seed_slopes) / len(seed_slopes))
            print(f"    Mean slope: {mean_sl:.4f} ± {std_sl:.4f} (n={len(seed_slopes)})")
            all_results.setdefault(fam_name, {})["per_seed_mean"] = mean_sl
            all_results.setdefault(fam_name, {})["per_seed_std"] = std_sl

    # Cross-family comparison
    print(f"\n{'=' * 80}")
    print("CROSS-FAMILY COMPARISON AT H=0.25")
    print("=" * 80)
    print(f"  {'Family':>10s}  {'mean slope':>10s}  {'per-seed σ':>10s}  {'R² (mean)':>10s}")
    print(f"  {'-' * 50}")
    for name in FAMILIES:
        if name in all_results:
            r = all_results[name]
            ms = r.get("mean_slope", float('nan'))
            ps = r.get("per_seed_std", float('nan'))
            r2 = r.get("mean_r2", float('nan'))
            print(f"  {name:>10s}  {ms:10.4f}  {ps:10.4f}  {r2:10.6f}")

    # Eikonal comparison
    eik_slope = -1.275  # from born_scattering_2d_prediction.py at L=15, x_src=5
    print(f"\n  Eikonal baseline: {eik_slope:.4f}")
    for name in FAMILIES:
        if name in all_results:
            ms = all_results[name].get("mean_slope", float('nan'))
            gap = ms - eik_slope
            print(f"    {name}: gap = {gap:+.4f}")

    # Verdict
    slopes = [all_results[n].get("mean_slope", float('nan')) for n in FAMILIES if n in all_results]
    slopes = [s for s in slopes if not math.isnan(s)]
    if len(slopes) >= 2:
        spread = max(slopes) - min(slopes)
        per_seed_stds = [all_results[n].get("per_seed_std", 0) for n in FAMILIES if n in all_results]
        avg_std = sum(per_seed_stds) / len(per_seed_stds) if per_seed_stds else 0
        print(f"\n  Inter-family spread: {spread:.4f}")
        print(f"  Average per-seed σ: {avg_std:.4f}")
        if spread < avg_std:
            print(f"  → Spread < per-seed σ: families are CONSISTENT (within noise)")
        elif spread < 2 * avg_std:
            print(f"  → Spread < 2σ: families are MARGINALLY consistent")
        else:
            print(f"  → Spread > 2σ: families show REAL differences")


if __name__ == "__main__":
    main()
