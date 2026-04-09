#!/usr/bin/env python3
"""Lensing slope measurement on ALL THREE families.

The -1.43 slope was only measured on Fam1. Does it hold for Fam2 and Fam3?
If the slope is family-independent, it's structural. If it varies, the
DAG geometry determines the lensing response.

Uses the same true Kubo measurement as kubo_continuum_limit.py.
Tests at H=0.5 (cheapest) on b ∈ {3,4,5,6} for each family.
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
S_PHYS = 0.004

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
    """Parallel perturbation propagator for Kubo coefficient."""
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
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            r_field = math.sqrt((mx - x_src)**2 + (mz - z_src)**2) + 0.1
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            w_eff = w * h2 / (L * L)
            weight = phi * w_eff
            dphi_ds = complex(0.0, -k_phase * L / r_field) * phi
            A[j] += ai * weight
            B[j] += (bi * phi + ai * dphi_ds) * w_eff

    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds_idx = n - npl
    weights = [abs(A[k])**2 for k in range(ds_idx, n)]
    zs = [pos[k][2] for k in range(ds_idx, n)]
    T0 = sum(weights)
    if T0 <= 0:
        return 0.0
    cz_free = sum(w * z for w, z in zip(weights, zs)) / T0
    dT_ds = sum(2.0 * (A[k].conjugate() * B[k]).real for k in range(ds_idx, n))
    dN_ds = sum(2.0 * (A[k].conjugate() * B[k]).real * pos[k][2]
                for k in range(ds_idx, n))
    N0 = T0 * cz_free
    kubo = dN_ds / T0 - N0 * dT_ds / (T0 * T0)
    return kubo


def main():
    H = 0.5
    NL = int(T_PHYS / H) + 1
    k_phase = K_PER_H / H
    seeds = [0, 1, 2, 3, 4]
    b_values = [3.0, 4.0, 5.0, 6.0]

    print("=" * 80)
    print("LENSING SLOPE: ALL THREE FAMILIES")
    print(f"  H={H}, NL={NL}, k={k_phase}, β={BETA}")
    print(f"  b ∈ {b_values}, seeds={seeds}")
    print("=" * 80)

    summary = {}

    for fam_name, (drift, restore) in FAMILIES.items():
        print(f"\n{'─'*60}")
        print(f"  {fam_name}: drift={drift}, restore={restore}")
        print(f"{'─'*60}")

        b_kubos = {b: [] for b in b_values}

        for seed in seeds:
            x_src = int(NL * SRC_LAYER_FRAC) * H
            pos, adj, nmap, _, hw = grow(seed, drift, restore, NL, PW_PHYS, H)

            for b in b_values:
                t0 = time.time()
                k = true_kubo(pos, adj, NL, PW_PHYS, H, k_phase, x_src, b)
                dt = time.time() - t0
                b_kubos[b].append(k)

        print(f"\n  {'b':>5s}  {'<kubo>':>10s}  {'σ':>10s}  {'n':>3s}")
        print(f"  {'-'*35}")

        mean_kubos = []
        valid_b = []
        for b in b_values:
            kubos = b_kubos[b]
            if len(kubos) < 2:
                continue
            mean_k = sum(kubos) / len(kubos)
            std_k = math.sqrt(sum((k - mean_k)**2 for k in kubos) / len(kubos))
            print(f"  {b:5.1f}  {mean_k:+10.4f}  {std_k:10.4f}  {len(kubos):3d}")
            if abs(mean_k) > 1e-6:
                mean_kubos.append(mean_k)
                valid_b.append(b)

        # Power-law fit
        if len(valid_b) >= 3 and all(k > 0 for k in mean_kubos):
            n = len(valid_b)
            log_b = [math.log(b) for b in valid_b]
            log_k = [math.log(k) for k in mean_kubos]
            sx, sy = sum(log_b), sum(log_k)
            sxx = sum(x*x for x in log_b)
            sxy = sum(x*y for x,y in zip(log_b, log_k))
            den = n * sxx - sx * sx
            slope = (n * sxy - sx * sy) / den
            intercept = (sy - slope * sx) / n
            prefactor = math.exp(intercept)
            pred = [slope * x + intercept for x in log_b]
            ss_res = sum((y-p)**2 for y,p in zip(log_k, pred))
            ss_tot = sum((y - sy/n)**2 for y in log_k)
            r2 = 1 - ss_res/ss_tot if ss_tot > 1e-30 else 0

            print(f"\n  kubo(b) ≈ {prefactor:.3f} · b^({slope:.4f})  R² = {r2:.6f}")
            summary[fam_name] = {"slope": slope, "prefactor": prefactor, "r2": r2}
        elif len(valid_b) >= 3:
            # Mixed signs — fit on absolute values
            n = len(valid_b)
            log_b = [math.log(b) for b in valid_b]
            log_k = [math.log(abs(k)) for k in mean_kubos]
            sx, sy = sum(log_b), sum(log_k)
            sxx = sum(x*x for x in log_b)
            sxy = sum(x*y for x,y in zip(log_b, log_k))
            den = n * sxx - sx * sx
            slope = (n * sxy - sx * sy) / den
            signs = ["+" if k > 0 else "−" for k in mean_kubos]
            print(f"\n  |kubo| slope ≈ {slope:.4f} (signs: {signs})")
            summary[fam_name] = {"slope": slope, "prefactor": 0, "r2": 0, "note": "mixed signs"}
        else:
            print(f"\n  Insufficient data for fit")
            summary[fam_name] = {"slope": float('nan'), "note": "insufficient"}

    # Cross-family
    print(f"\n{'='*80}")
    print("CROSS-FAMILY LENSING COMPARISON")
    print("=" * 80)
    print(f"  {'Family':>10s}  {'slope':>8s}  {'prefactor':>10s}  {'R²':>8s}")
    print(f"  {'-'*45}")
    for name, s in summary.items():
        slope = s.get("slope", float('nan'))
        pf = s.get("prefactor", 0)
        r2 = s.get("r2", 0)
        note = s.get("note", "")
        print(f"  {name:>10s}  {slope:8.4f}  {pf:10.3f}  {r2:8.6f}  {note}")

    print(f"\n  Reference: Fam1 at H=0.25 gave slope = −1.4335")
    print(f"  (this test is at H=0.5 so slopes may differ from the fine-H value)")

    slopes = [s["slope"] for s in summary.values() if not math.isnan(s.get("slope", float('nan')))]
    if len(slopes) >= 2:
        spread = max(slopes) - min(slopes)
        print(f"\n  Slope spread across families: {spread:.4f}")
        if spread < 0.1:
            print(f"  → Slopes are CONSISTENT across families (spread < 0.1)")
        elif spread < 0.3:
            print(f"  → Slopes show MODERATE family dependence")
        else:
            print(f"  → Slopes are STRONGLY family-dependent")


if __name__ == "__main__":
    main()
