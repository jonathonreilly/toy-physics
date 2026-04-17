#!/usr/bin/env python3
"""High-p dispersion to break the Schrödinger/KG tie.

At low p, both forms are quadratic and indistinguishable.
At high p (p >> m_eff):
  Schrödinger: ω = a·p² + b  →  keeps growing quadratically
  Klein-Gordon: ω = √(c²p² + m²c⁴)  →  becomes LINEAR in p

With m_eff ≈ 6, the crossover is around p ≈ 6.
Previous tests only went to p=2. This test pushes to p=8.

We also fit a FOURTH form:
  ω² = c²·p² + m²·c⁴  (full KG, not linearized)
to handle the transition region properly.

Per-seed fits reported (not just seed-mean) per review P2.
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

DRIFT, RESTORE = 0.20, 0.70  # Fam1


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
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            r_perp = math.sqrt(dy * dy + dz * dz)
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
        d = phases[i] - phases[i - 1]
        while d > math.pi: d -= 2 * math.pi
        while d < -math.pi: d += 2 * math.pi
        unwrapped.append(unwrapped[-1] + d)
    np_ = len(xs)
    sx = sum(xs); sy = sum(unwrapped)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, unwrapped))
    den = np_ * sxx - sx * sx
    if abs(den) < 1e-30:
        return float('nan'), 0.0
    omega = (np_ * sxy - sx * sy) / den
    b = (sy - omega * sx) / np_
    pred = [omega * x + b for x in xs]
    ss_res = sum((u - p) ** 2 for u, p in zip(unwrapped, pred))
    ss_tot = sum((u - sy / np_) ** 2 for u in unwrapped)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    return omega, r2


def fit_models(ps, ws):
    """Fit four dispersion models. Returns dict of {name: (r2, params)}."""
    n = len(ps)
    if n < 4:
        return {}
    results = {}

    # 1. Schrödinger: ω = a·p² + b
    p2 = [p ** 2 for p in ps]
    sp2, sw = sum(p2), sum(ws)
    sp2p2 = sum(x * x for x in p2)
    sp2w = sum(x * y for x, y in zip(p2, ws))
    den = n * sp2p2 - sp2 * sp2
    if abs(den) > 1e-30:
        a = (n * sp2w - sp2 * sw) / den
        b = (sw - a * sp2) / n
        pred = [a * p ** 2 + b for p in ps]
        ss_res = sum((w - p) ** 2 for w, p in zip(ws, pred))
        ss_tot = sum((w - sw / n) ** 2 for w in ws)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0
        results["Schrödinger"] = (r2, {"a": a, "b": b, "m_eff": -1 / (2 * a) if abs(a) > 1e-30 else 0})

    # 2. Klein-Gordon (linearized): ω² = a·p² + m²
    w2 = [w ** 2 for w in ws]
    sw2 = sum(w2)
    sp2w2 = sum(x * y for x, y in zip(p2, w2))
    if abs(den) > 1e-30:
        a_kg = (n * sp2w2 - sp2 * sw2) / den
        m2 = (sw2 - a_kg * sp2) / n
        pred_kg = [a_kg * p ** 2 + m2 for p in ps]
        ss_res_kg = sum((w2i - p) ** 2 for w2i, p in zip(w2, pred_kg))
        ss_tot_kg = sum((w2i - sw2 / n) ** 2 for w2i in w2)
        r2_kg = 1 - ss_res_kg / ss_tot_kg if ss_tot_kg > 1e-30 else 0
        results["Klein-Gordon"] = (r2_kg, {"c²": a_kg, "m²": m2})

    # 3. Linear: ω = c·|p| + d
    ap = [abs(p) for p in ps]
    sap = sum(ap); sapap = sum(x * x for x in ap)
    sapw = sum(x * y for x, y in zip(ap, ws))
    den_l = n * sapap - sap * sap
    if abs(den_l) > 1e-30:
        c_l = (n * sapw - sap * sw) / den_l
        d_l = (sw - c_l * sap) / n
        pred_l = [c_l * abs(p) + d_l for p in ps]
        ss_res_l = sum((w - p) ** 2 for w, p in zip(ws, pred_l))
        ss_tot_l = sum((w - sw / n) ** 2 for w in ws)
        r2_l = 1 - ss_res_l / ss_tot_l if ss_tot_l > 1e-30 else 0
        results["Linear"] = (r2_l, {"c": c_l, "d": d_l})

    # 4. sqrt-KG: ω = sqrt(c²p² + m²) fit via nonlinear least squares
    # Use grid search over (c, m) since we don't have scipy
    best_r2_sqkg = -1e30
    best_c_sq, best_m_sq = 0, 0
    w0 = ws[0]  # omega at p=0 → m ≈ |w0|
    for c_trial in [x * 0.02 for x in range(1, 30)]:
        m_trial = abs(w0)
        # Predict
        try:
            pred_sq = [math.copysign(math.sqrt(c_trial ** 2 * p ** 2 + m_trial ** 2), w0) for p in ps]
        except ValueError:
            continue
        ss_res_sq = sum((w - p) ** 2 for w, p in zip(ws, pred_sq))
        ss_tot_sq = sum((w - sw / n) ** 2 for w in ws)
        r2_sq = 1 - ss_res_sq / ss_tot_sq if ss_tot_sq > 1e-30 else 0
        if r2_sq > best_r2_sqkg:
            best_r2_sqkg = r2_sq
            best_c_sq = c_trial
            best_m_sq = m_trial
    # Refine m around best
    for m_trial in [best_m_sq * (0.8 + 0.04 * i) for i in range(11)]:
        for c_trial in [best_c_sq * (0.8 + 0.04 * i) for i in range(11)]:
            try:
                pred_sq = [math.copysign(math.sqrt(c_trial ** 2 * p ** 2 + m_trial ** 2), w0) for p in ps]
            except ValueError:
                continue
            ss_res_sq = sum((w - p) ** 2 for w, p in zip(ws, pred_sq))
            ss_tot_sq = sum((w - sw / n) ** 2 for w in ws)
            r2_sq = 1 - ss_res_sq / ss_tot_sq if ss_tot_sq > 1e-30 else 0
            if r2_sq > best_r2_sqkg:
                best_r2_sqkg = r2_sq
                best_c_sq = c_trial
                best_m_sq = m_trial

    results["sqrt-KG"] = (best_r2_sqkg, {"c": best_c_sq, "m": best_m_sq})

    return results


def main():
    H = 0.5
    NL = int(T_PHYS / H) + 1
    seeds = [0, 1, 2, 3, 4, 5, 6, 7]  # 8 seeds for per-seed stats
    # Extended p range: 0 to 6 (Nyquist = π/0.5 = 6.28)
    p_values = [0.0, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]

    print("=" * 90)
    print("HIGH-p DISPERSION TIEBREAKER (Fam1 grown DAG)")
    print(f"  H={H}, NL={NL}, k={K_PER_H/H}, β={BETA}")
    print(f"  p range: 0–6 (Nyquist = {math.pi/H:.2f})")
    print(f"  Seeds: {seeds}")
    print(f"  Key test: at p >> m_eff ≈ 6:")
    print(f"    Schrödinger → ω ∝ p²  (accelerating)")
    print(f"    Klein-Gordon → ω ∝ |p| (linear)")
    print("=" * 90)

    # Collect per-seed results keyed by (p, seed)
    # Using dicts keyed by seed to avoid misindexing when seeds drop out
    all_seed_omegas = {p: {} for p in p_values}  # p -> {seed: omega}
    all_seed_r2s = {p: {} for p in p_values}      # p -> {seed: r2}

    for seed in seeds:
        t0 = time.time()
        pos, adj, nmap, _, hw = grow(seed, NL, PW_PHYS, H)
        for p in p_values:
            omega, r2 = measure_omega(pos, adj, nmap, NL, hw, H, p)
            if not math.isnan(omega) and r2 > 0.9:
                all_seed_omegas[p][seed] = omega
                all_seed_r2s[p][seed] = r2
        dt = time.time() - t0
        if seed == 0:
            print(f"  nodes={len(pos)}, time per seed ≈ {dt:.1f}s")

    # Report seed-mean curve
    print(f"\n  {'p':>5s}  {'<ω>':>10s}  {'σ_ω':>8s}  {'<R²>':>8s}  {'n':>3s}")
    print(f"  {'-'*45}")

    good_p, good_omega = [], []
    for p in p_values:
        ws_dict = all_seed_omegas[p]
        r2_dict = all_seed_r2s[p]
        ws = list(ws_dict.values())
        r2s = list(r2_dict.values())
        if len(ws) < 3:
            print(f"  {p:5.1f}  {'<3 good':>10s}")
            continue
        mean_w = sum(ws) / len(ws)
        std_w = math.sqrt(sum((w - mean_w) ** 2 for w in ws) / len(ws))
        mean_r2 = sum(r2s) / len(r2s)
        flag = " ←noisy" if mean_r2 < 0.99 else ""
        print(f"  {p:5.1f}  {mean_w:+10.4f}  {std_w:8.4f}  {mean_r2:8.5f}  {len(ws):3d}{flag}")
        if mean_r2 >= 0.95:
            good_p.append(p)
            good_omega.append(mean_w)

    # Seed-mean fits
    if len(good_p) >= 6:
        print(f"\n  SEED-MEAN FITS ({len(good_p)} points, p up to {max(good_p):.1f}):")
        fits = fit_models(good_p, good_omega)
        for name in ["Schrödinger", "Klein-Gordon", "Linear", "sqrt-KG"]:
            if name in fits:
                r2, params = fits[name]
                ps = ", ".join(f"{k}={v:.4f}" for k, v in params.items())
                print(f"    {name:15s}  R² = {r2:.7f}  {ps}")

        # Determine winner
        ranked = sorted(fits.items(), key=lambda x: -x[1][0])
        print(f"\n    WINNER: {ranked[0][0]} (R² = {ranked[0][1][0]:.7f})")
        print(f"    Runner: {ranked[1][0]} (R² = {ranked[1][1][0]:.7f})")
        print(f"    Gap: Δ = {ranked[0][1][0] - ranked[1][1][0]:.6f}")

        if ranked[0][1][0] - ranked[1][1][0] > 0.01:
            print(f"    → TIE BROKEN (Δ > 0.01)")
        else:
            print(f"    → TIE NOT BROKEN (Δ < 0.01)")

    # Per-seed fits (keyed by actual seed ID, not list index)
    print(f"\n  PER-SEED FITS (winner per seed):")
    seed_winners = []
    for seed in seeds:
        seed_p, seed_w = [], []
        for p in p_values:
            if seed in all_seed_omegas[p]:
                seed_p.append(p)
                seed_w.append(all_seed_omegas[p][seed])
        if len(seed_p) >= 6:
            fits = fit_models(seed_p, seed_w)
            ranked = sorted(fits.items(), key=lambda x: -x[1][0])
            winner = ranked[0][0]
            gap = ranked[0][1][0] - ranked[1][1][0]
            seed_winners.append(winner)
            print(f"    seed {seed}: {winner:15s}  (Δ = {gap:.4f})", end="")
            print(f"  [{ranked[0][0][:3]}={ranked[0][1][0]:.4f}, {ranked[1][0][:3]}={ranked[1][1][0]:.4f}]")
        else:
            print(f"    seed {seed}: <6 clean p-values, skipped")

    # Tally
    from collections import Counter
    tally = Counter(seed_winners)
    print(f"\n    Winner tally: {dict(tally)}")

    # Key diagnostic: plot omega vs p to see if it curves up (Schrö) or flattens (KG)
    print(f"\n  CURVATURE DIAGNOSTIC:")
    print(f"  If omega curves UP at high p → Schrödinger (∝ p²)")
    print(f"  If omega flattens/becomes linear at high p → Klein-Gordon (∝ √(p²+m²))")
    print(f"  If omega turns over → band structure / lattice artifact")
    if len(good_p) >= 4:
        # Check: is d²ω/dp² positive (Schrödinger) or negative (KG)?
        for i in range(1, len(good_omega) - 1):
            dp = good_p[i + 1] - good_p[i - 1]
            if dp > 0:
                d2w = (good_omega[i + 1] - 2 * good_omega[i] + good_omega[i - 1]) / (dp / 2) ** 2
                print(f"    p={good_p[i]:.1f}: d²ω/dp² = {d2w:+.4f}", end="")
                if d2w < -0.01:
                    print("  (concave down → KG-like)")
                elif d2w > 0.01:
                    print("  (concave up → Schrö-like)")
                else:
                    print("  (flat)")


if __name__ == "__main__":
    main()
