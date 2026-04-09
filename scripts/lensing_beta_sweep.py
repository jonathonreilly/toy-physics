#!/usr/bin/env python3
"""Lane L#: BETA sweep on the lensing slope.

After Lane L++ falsified the finite-path ray-integral explanation
of the measured −1.43 slope, the open question is: what determines
the slope?

The leading hypothesis is that the slope is a property of the
wave-mechanical Kubo response of a diffracting beam. Our propagator
has angular weight `exp(−β·θ²)` per edge, where θ is the angle from
forward. At the default β = 0.8:
  - 1/e angular width θ₀ = 1/√(2·0.8) ≈ 0.79 rad ≈ 45°
  - the beam is heavily diffracted; paths up to 45° contribute

If the slope comes from wave-mechanical diffraction, varying β
should change the slope:
  - **large β** (narrow angular window, approaching ray limit):
    slope should approach the analytical ray formula prediction
    (−1.28 at T=15 for the asymmetric formula, or −1.42 for the
    centered surrogate)
  - **small β** (heavily delocalized beam): slope may be different
    from both the ray formula AND from the default-β measurement
  - **default β = 0.8**: should give slope ≈ −1.43 (the measured value)

If the slope tracks β predictably, the mechanism is diffraction.
If it's stuck near −1.43 regardless of β, something deeper is at work.

Cost: 5 β values × 4 b values × 1 H = 20 runs at H=0.5 T=15.
Each ~5-10 sec. Total ~2-5 min.
"""

from __future__ import annotations

import math
import os
import random
import sys

# Constants matching kubo_continuum_limit.py
T_PHYS = 15.0
PW_PHYS = 6.0
K_PER_H = 2.5
S_PHYS = 0.004
MASS_Z_PHYS = 3.0
SRC_LAYER_FRAC = 1.0 / 3.0

B_VALUES = [3.0, 4.0, 5.0, 6.0]
BETA_VALUES = [0.1, 0.4, 0.8, 2.0, 5.0]


def grow(seed, drift, restore, NL, PW, max_d_phys, H):
    """Grow a Fam1-style DAG (same as kubo_continuum_limit.grow)."""
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(max_d_phys / H))
    pos = [(0.0, 0.0, 0.0)]
    adj = {}
    nmap = {(0, 0, 0): 0}
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
    return pos, adj, nmap


def true_kubo_at_H(pos, adj, NL, PW, H, k_phase, x_src, z_src, beta):
    """Parallel perturbation propagator with explicit BETA parameter."""
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
            w = math.exp(-beta * theta * theta)  # ← β is the sweep variable
            w_eff = w * h2 / (L * L)
            weight = phi * w_eff
            dphi_ds = complex(0.0, -k_phase * L / r_field) * phi
            A[j] += ai * weight
            B[j] += (bi * phi + ai * dphi_ds) * w_eff

    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds_idx = n - npl
    weights = [abs(A[k]) ** 2 for k in range(ds_idx, n)]
    zs = [pos[k][2] for k in range(ds_idx, n)]
    T0 = sum(weights)
    if T0 <= 0:
        return 0.0, 0.0, 0.0
    cz_free = sum(w * z for w, z in zip(weights, zs)) / T0
    dT_ds = sum(2.0 * (A[k].conjugate() * B[k]).real for k in range(ds_idx, n))
    dN_ds = sum(2.0 * (A[k].conjugate() * B[k]).real * pos[k][2]
                for k in range(ds_idx, n))
    N0 = T0 * cz_free
    kubo = dN_ds / T0 - N0 * dT_ds / (T0 * T0)
    return kubo, cz_free, T0


def measure_kubo(H_val, b_phys, T_phys, beta):
    NL = max(3, round(T_phys / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    x_src = round(NL * SRC_LAYER_FRAC) * H_val
    z_src = b_phys

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    kubo, _, _ = true_kubo_at_H(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, beta)
    return kubo, len(pos)


def slope_loglog(xs, ys):
    n = len(xs)
    lx = [math.log(x) for x in xs]
    ly = [math.log(abs(y)) for y in ys]
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    syy = sum((y - my) ** 2 for y in ly)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    s = sxy / sxx if sxx > 0 else 0.0
    r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 1.0
    return s, r2


def main():
    H_val = 0.5  # coarse but cheap; default β = 0.8 at H=0.5 gave slope -1.28 previously
    print("=" * 80)
    print("LANE L#: BETA SWEEP on lensing slope")
    print("=" * 80)
    print(f"  T_phys = {T_PHYS}  H = {H_val}  b ∈ {B_VALUES}")
    print(f"  β values: {BETA_VALUES}")
    print(f"  Reference: at β=0.8 H=0.5 we measured slope -1.28 (Lane L)")
    print(f"             at β=0.8 H=0.25 we measured slope -1.43 (Lane L+)")
    print()

    results = {}  # results[β] = {b: kubo}

    for beta in BETA_VALUES:
        print(f"--- β = {beta} ---", flush=True)
        results[beta] = {}
        for b in B_VALUES:
            kubo, n_nodes = measure_kubo(H_val, b, T_PHYS, beta)
            results[beta][b] = kubo
            print(f"  b={b}  kubo_true = {kubo:+.4f}", flush=True)
        s, r2 = slope_loglog(B_VALUES, [results[beta][b] for b in B_VALUES])
        print(f"  slope = {s:+.4f}  R² = {r2:.4f}")
        print()

    # Summary table
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'β':>6s}  {'slope':>10s}  {'R²':>8s}  {'interpretation':>30s}")
    for beta in BETA_VALUES:
        kubos = [results[beta][b] for b in B_VALUES]
        s, r2 = slope_loglog(B_VALUES, kubos)
        interp = ""
        if abs(s + 1.0) < 0.1:
            interp = "→ 1/b (ray limit?)"
        elif abs(s + 1.43) < 0.1:
            interp = "≈ -1.43 (default β match)"
        elif abs(s + 2.0) < 0.1:
            interp = "→ 1/b² (short-path limit)"
        else:
            interp = "transition / other"
        print(f"{beta:6.2f}  {s:+10.4f}  {r2:8.4f}  {interp:>30s}")

    # Analytical reference
    print()
    print("For reference, analytical predictions on b ∈ {3..6} at T=15:")
    print(f"  Symmetric L=10 (coincidence at β=0.8 H=0.25): slope = -1.42")
    print(f"  Asymmetric [−T/3, +2T/3] (literal geometry):  slope = -1.28")
    print(f"  Canonical 1/b:                                 slope = -1.00")
    print(f"  Short-path 1/b²:                               slope = -2.00")

    # Verdict
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)

    slopes_vs_beta = [(beta, slope_loglog(B_VALUES, [results[beta][b] for b in B_VALUES])[0])
                      for beta in BETA_VALUES]

    max_spread = max(s for _, s in slopes_vs_beta) - min(s for _, s in slopes_vs_beta)
    print(f"  Slope spread across β ∈ {BETA_VALUES}: {max_spread:.4f}")

    if max_spread < 0.1:
        print(f"  STUCK — slope is approximately invariant under β.")
        print(f"  The mechanism is NOT simple wave-mechanical diffraction; changing")
        print(f"  angular weight doesn't change the slope. Something deeper fixes")
        print(f"  the slope at ~-1.43 in this b range and lattice configuration.")
    elif max_spread < 0.3:
        print(f"  MILD DEPENDENCE — slope varies modestly with β.")
        print(f"  Diffraction plays a role but isn't the only factor.")
    else:
        print(f"  STRONG DEPENDENCE — slope varies significantly with β.")
        print(f"  The mechanism is wave-mechanical diffraction, as hypothesized.")

    # Does large β approach the ray formula?
    largest_beta_slope = slopes_vs_beta[-1][1]
    ray_asym = -1.28  # asymmetric literal geometry
    ray_sym = -1.42   # centered surrogate
    dist_ray_asym = abs(largest_beta_slope - ray_asym)
    dist_ray_sym = abs(largest_beta_slope - ray_sym)
    print()
    print(f"  At largest β = {BETA_VALUES[-1]}: slope = {largest_beta_slope:+.4f}")
    print(f"    distance from asymmetric ray formula ({ray_asym}): {dist_ray_asym:.4f}")
    print(f"    distance from symmetric ray formula  ({ray_sym}): {dist_ray_sym:.4f}")
    print(f"    distance from canonical 1/b (-1.00):            {abs(largest_beta_slope+1.0):.4f}")


if __name__ == "__main__":
    main()
