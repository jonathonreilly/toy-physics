#!/usr/bin/env python3
"""Dispersion relation on ALL THREE grown-DAG families.

Previous measurement was Fam1 only. This tests whether the
Schrödinger/KG near-tie is family-specific or universal.

Families:
  Fam1: drift=0.20, restore=0.70 (center family)
  Fam2: drift=0.05, restore=0.30 (low drift, nearly regular)
  Fam3: drift=0.50, restore=0.90 (high drift, most random)

If all three give Schrödinger ≈ KG, the near-tie is structural.
If one family breaks the tie, the DAG geometry determines the
dispersion type.
"""

from __future__ import annotations
import math
import cmath
import random
import time

BETA = 0.8
K_PER_H = 2.5
T_PHYS = 15.0
PW_PHYS = 6.0
MAX_D_PHYS = 3.0

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


def propagate_pw(pos, adj, nmap, NL, hw, H, pz):
    n = len(pos)
    k = K_PER_H / H
    h2 = H * H
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((0, iy, iz))
            if idx is not None:
                _, y, z = pos[idx]
                amps[idx] = cmath.exp(1j * pz * z)
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            r_perp = math.sqrt(dy*dy + dz*dz)
            theta = math.atan2(r_perp, max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            phi = cmath.exp(1j * k * L)
            amps[j] += amps[i] * phi * w * h2 / (L * L)
    return amps


def measure_omega(pos, adj, nmap, NL, hw, H, pz):
    amps = propagate_pw(pos, adj, nmap, NL, hw, H, pz)
    start = NL // 4
    end = 3 * NL // 4
    step = max(1, (end - start) // 8)
    layers = list(range(start, end, step))

    phases, xs = [], []
    for layer in layers:
        ma = 0j
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = nmap.get((layer, iy, iz))
                if idx is None:
                    continue
                _, y, z = pos[idx]
                ma += amps[idx] * cmath.exp(-1j * pz * z)
        if abs(ma) < 1e-30:
            continue
        phases.append(cmath.phase(ma))
        xs.append(layer * H)

    if len(phases) < 3:
        return float('nan'), 0.0

    unwrapped = [phases[0]]
    for i in range(1, len(phases)):
        d = phases[i] - phases[i-1]
        while d > math.pi: d -= 2*math.pi
        while d < -math.pi: d += 2*math.pi
        unwrapped.append(unwrapped[-1] + d)

    np_ = len(xs)
    sx = sum(xs); sy = sum(unwrapped)
    sxx = sum(x*x for x in xs)
    sxy = sum(x*y for x,y in zip(xs, unwrapped))
    den = np_ * sxx - sx * sx
    if abs(den) < 1e-30:
        return float('nan'), 0.0
    omega = (np_ * sxy - sx * sy) / den
    b = (sy - omega * sx) / np_
    pred = [omega * x + b for x in xs]
    ss_res = sum((u-p)**2 for u,p in zip(unwrapped, pred))
    ss_tot = sum((u - sy/np_)**2 for u in unwrapped)
    r2 = 1 - ss_res/ss_tot if ss_tot > 1e-30 else 0.0
    return omega, r2


def fit_dispersion(good_p, good_omega):
    """Returns (r2_schrodinger, r2_kg, r2_linear, a_schro, b_schro)."""
    n = len(good_p)
    if n < 4:
        return 0, 0, 0, 0, 0
    p2 = [pp**2 for pp in good_p]
    sp2, sw = sum(p2), sum(good_omega)
    sp2p2 = sum(x*x for x in p2)
    sp2w = sum(x*y for x,y in zip(p2, good_omega))
    den = n * sp2p2 - sp2 * sp2
    if abs(den) < 1e-30:
        return 0, 0, 0, 0, 0

    a = (n * sp2w - sp2 * sw) / den
    b = (sw - a * sp2) / n
    pred = [a*pp**2 + b for pp in good_p]
    ss_res = sum((w-p)**2 for w,p in zip(good_omega, pred))
    ss_tot = sum((w - sw/n)**2 for w in good_omega)
    r2_s = 1 - ss_res/ss_tot if ss_tot > 1e-30 else 0

    w2 = [w**2 for w in good_omega]
    sw2 = sum(w2)
    sp2w2 = sum(x*y for x,y in zip(p2, w2))
    a_kg = (n * sp2w2 - sp2 * sw2) / den
    m2 = (sw2 - a_kg * sp2) / n
    pred_kg = [a_kg*pp**2 + m2 for pp in good_p]
    ss_res_kg = sum((w2i-p)**2 for w2i,p in zip(w2, pred_kg))
    ss_tot_kg = sum((w2i - sw2/n)**2 for w2i in w2)
    r2_kg = 1 - ss_res_kg/ss_tot_kg if ss_tot_kg > 1e-30 else 0

    ap = [abs(pp) for pp in good_p]
    sap = sum(ap); sapap = sum(x*x for x in ap)
    sapw = sum(x*y for x,y in zip(ap, good_omega))
    den_l = n * sapap - sap * sap
    r2_l = 0
    if abs(den_l) > 1e-30:
        c_l = (n * sapw - sap * sw) / den_l
        d_l = (sw - c_l * sap) / n
        pred_l = [c_l*abs(pp) + d_l for pp in good_p]
        ss_res_l = sum((w-p)**2 for w,p in zip(good_omega, pred_l))
        r2_l = 1 - ss_res_l/ss_tot if ss_tot > 1e-30 else 0

    return r2_s, r2_kg, r2_l, a, b


def main():
    H = 0.5
    NL = int(T_PHYS / H) + 1
    seeds = [0, 1, 2, 3, 4]
    p_values = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]

    print("=" * 90)
    print("DISPERSION RELATION: ALL THREE FAMILIES")
    print(f"  H={H}, NL={NL}, T_phys≈{(NL-1)*H:.1f}, PW={PW_PHYS}")
    print(f"  k={K_PER_H/H:.1f}, β={BETA}, seeds={seeds}")
    print("=" * 90)

    summary = {}

    for fam_name, (drift, restore) in FAMILIES.items():
        print(f"\n{'─'*70}")
        print(f"  {fam_name}: drift={drift}, restore={restore}")
        print(f"{'─'*70}")

        p_omegas = {p: [] for p in p_values}
        p_r2s = {p: [] for p in p_values}

        for seed in seeds:
            pos, adj, nmap, _, hw = grow(seed, drift, restore, NL, PW_PHYS, H)
            for p in p_values:
                omega, r2 = measure_omega(pos, adj, nmap, NL, hw, H, p)
                if not math.isnan(omega) and r2 > 0.9:
                    p_omegas[p].append(omega)
                    p_r2s[p].append(r2)

        print(f"\n  {'p':>6s}  {'<ω>':>10s}  {'σ_ω':>10s}  {'<R²>':>10s}  {'n':>3s}")
        print(f"  {'-'*50}")

        good_p, good_omega = [], []
        for p in p_values:
            omegas = p_omegas[p]
            r2s = p_r2s[p]
            if len(omegas) < 2:
                print(f"  {p:6.2f}  {'<2':>10s}")
                continue
            mean_w = sum(omegas) / len(omegas)
            std_w = math.sqrt(sum((w - mean_w)**2 for w in omegas) / len(omegas))
            mean_r2 = sum(r2s) / len(r2s)
            flag = " ←noisy" if mean_r2 < 0.99 else ""
            print(f"  {p:6.2f}  {mean_w:+10.4f}  {std_w:10.4f}  {mean_r2:10.5f}  {len(omegas):3d}{flag}")
            if mean_r2 >= 0.95 and std_w < abs(mean_w) * 0.5:
                good_p.append(p)
                good_omega.append(mean_w)

        r2_s, r2_kg, r2_l, a_s, b_s = fit_dispersion(good_p, good_omega)
        m_eff = -1/(2*a_s) if abs(a_s) > 1e-30 else float('inf')

        winner = "Schrödinger" if r2_s >= r2_kg and r2_s >= r2_l else (
            "Klein-Gordon" if r2_kg >= r2_l else "Linear")

        print(f"\n  FITS:")
        print(f"    Schrödinger: R² = {r2_s:.7f}  (ω = {a_s:.6f}·p² + {b_s:.6f}, m_eff={m_eff:.2f})")
        print(f"    Klein-Gordon: R² = {r2_kg:.7f}")
        print(f"    Linear: R² = {r2_l:.7f}")
        print(f"    WINNER: {winner}  (Δ_SKG = {abs(r2_s - r2_kg):.6f})")

        summary[fam_name] = {
            "r2_s": r2_s, "r2_kg": r2_kg, "r2_l": r2_l,
            "winner": winner, "delta": abs(r2_s - r2_kg),
            "a": a_s, "m_eff": m_eff
        }

    # Cross-family comparison
    print(f"\n{'='*90}")
    print("CROSS-FAMILY COMPARISON")
    print("=" * 90)
    print(f"  {'Family':>10s}  {'Schrö R²':>10s}  {'KG R²':>10s}  {'Δ(S-KG)':>10s}  {'Winner':>12s}  {'m_eff':>8s}")
    print(f"  {'-'*70}")
    for name, s in summary.items():
        print(f"  {name:>10s}  {s['r2_s']:10.7f}  {s['r2_kg']:10.7f}  "
              f"{s['delta']:10.6f}  {s['winner']:>12s}  {s['m_eff']:8.2f}")

    # Check if any family breaks the tie
    all_tied = all(s['delta'] < 0.01 for s in summary.values())
    any_decisive = any(s['delta'] > 0.05 for s in summary.values())

    print()
    if all_tied:
        print("  → ALL families show Schrödinger ≈ KG (Δ < 0.01)")
        print("  → The near-tie is STRUCTURAL, not family-specific")
    elif any_decisive:
        decisive = [n for n, s in summary.items() if s['delta'] > 0.05]
        print(f"  → Family {decisive} BREAKS the tie (Δ > 0.05)!")
        print(f"  → The dispersion type IS family-dependent")
    else:
        print(f"  → Mixed: some families tighter than others")


if __name__ == "__main__":
    main()
