#!/usr/bin/env python3
"""Dispersion relation on the ACTUAL grown DAG (Fam1).

This is the correct measurement: the grown DAG is what produces
the -1.43 lensing slope, so ITS dispersion relation is what we
need. The 2D lattice gave Schrödinger, the 3D lattice gave
band-structure — what does the grown DAG give?

Uses the SAME kernel as kubo_continuum_limit.py:
  weight = exp(i·k·L) · exp(-β·θ²) · H² / L²

Plane wave source: amp_j = exp(i·pz·z_j) at layer 0.
Average over multiple seeds to reduce noise from randomness.

Key question: is the 3D grown-DAG dispersion fundamentally
different from the 2D lattice result?
"""

from __future__ import annotations
import math
import cmath
import random
import time

BETA = 0.8
K_PER_H = 2.5  # k * H = 2.5, matching kubo_continuum_limit.py

# Fam1 parameters (matching the lensing configuration)
DRIFT = 0.20
RESTORE = 0.70
T_PHYS = 15.0
PW_PHYS = 6.0
MAX_D_PHYS = 3.0


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


def propagate_planewave_dag(pos, adj, nmap, NL, hw, H, pz, py=0.0):
    """Plane wave propagation on the grown DAG.

    Source: amp_j = exp(i·(py·y_j + pz·z_j)) for nodes at layer 0.
    Kernel: exp(i·k·L) · exp(-β·θ²) · H² / L²  (matching kubo code)
    """
    n = len(pos)
    k = K_PER_H / H  # k_phase = K_PER_H / H so that k*H = K_PER_H
    h2 = H * H
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n

    # Initialize layer 0
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((0, iy, iz))
            if idx is not None:
                _, y, z = pos[idx]
                amps[idx] = cmath.exp(1j * (py * y + pz * z))

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
            phase = k * L
            phi = complex(math.cos(phase), math.sin(phase))
            w_eff = w * h2 / (L * L)
            amps[j] += amps[i] * phi * w_eff
    return amps


def extract_mode_dag(amps, pos, nmap, hw, layer, pz, py=0.0):
    """Project onto exp(-i·(py·y+pz·z)) at given layer using GRID positions."""
    mode_amp = 0j
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((layer, iy, iz))
            if idx is None:
                continue
            _, y, z = pos[idx]
            mode_amp += amps[idx] * cmath.exp(-1j * (py * y + pz * z))
    return mode_amp


def measure_omega_dag(pos, adj, nmap, NL, hw, H, pz, py=0.0):
    """Measure omega for given transverse momentum on DAG."""
    amps = propagate_planewave_dag(pos, adj, nmap, NL, hw, H, pz, py)

    start = NL // 4
    end = 3 * NL // 4
    step = max(1, (end - start) // 8)
    layers = list(range(start, end, step))

    phases, xs, ma_list = [], [], []
    for layer in layers:
        ma = extract_mode_dag(amps, pos, nmap, hw, layer, pz, py)
        if abs(ma) < 1e-30:
            continue
        phases.append(cmath.phase(ma))
        ma_list.append(abs(ma))
        xs.append(layer * H)

    if len(phases) < 3:
        return float('nan'), 0.0, 0.0

    unwrapped = [phases[0]]
    for i in range(1, len(phases)):
        d = phases[i] - phases[i - 1]
        while d > math.pi: d -= 2 * math.pi
        while d < -math.pi: d += 2 * math.pi
        unwrapped.append(unwrapped[-1] + d)

    np_pts = len(xs)
    sx = sum(xs); sy = sum(unwrapped)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, unwrapped))
    den = np_pts * sxx - sx * sx
    if abs(den) < 1e-30:
        return float('nan'), 0.0, 0.0
    omega = (np_pts * sxy - sx * sy) / den
    b = (sy - omega * sx) / np_pts

    pred = [omega * x + b for x in xs]
    ss_res = sum((u - p) ** 2 for u, p in zip(unwrapped, pred))
    ss_tot = sum((u - sy / np_pts) ** 2 for u in unwrapped)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    return omega, r2, sum(ma_list) / len(ma_list)


def main():
    H_values = [0.5, 0.35]  # Two refinements
    seeds = [0, 1, 2, 3, 4]  # Average over seeds
    p_values = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]

    for H in H_values:
        NL = int(T_PHYS / H) + 1

        print("=" * 80)
        print(f"GROWN DAG DISPERSION (Fam1: drift={DRIFT}, restore={RESTORE})")
        print(f"  H={H}, NL={NL}, T_phys≈{(NL-1)*H:.1f}, PW={PW_PHYS}")
        print(f"  k={K_PER_H/H:.1f} (k·H={K_PER_H}), β={BETA}")
        print(f"  Seeds: {seeds}")
        print("=" * 80)

        # Collect omega across seeds for each p
        p_omegas = {p: [] for p in p_values}
        p_r2s = {p: [] for p in p_values}

        for seed in seeds:
            t0 = time.time()
            pos, adj, nmap, _, hw = grow(seed, NL, PW_PHYS, H)
            dt_grow = time.time() - t0
            n = len(pos)
            if seed == 0:
                print(f"  nodes={n}, hw={hw}, grow={dt_grow:.1f}s")

            for p in p_values:
                omega, r2, amp = measure_omega_dag(pos, adj, nmap, NL, hw, H, p)
                if not math.isnan(omega) and r2 > 0.9:
                    p_omegas[p].append(omega)
                    p_r2s[p].append(r2)

        # Report seed-averaged results
        print(f"\n  {'p_z':>6s}  {'<omega>':>10s}  {'σ_omega':>10s}  {'<R²>':>10s}  {'n_good':>6s}")
        print(f"  {'-'*55}")

        good_p, good_omega = [], []
        for p in p_values:
            omegas = p_omegas[p]
            r2s = p_r2s[p]
            if len(omegas) < 2:
                print(f"  {p:6.2f}  {'<2 good':>10s}")
                continue
            mean_w = sum(omegas) / len(omegas)
            std_w = math.sqrt(sum((w - mean_w) ** 2 for w in omegas) / len(omegas))
            mean_r2 = sum(r2s) / len(r2s)
            flag = ""
            if mean_r2 < 0.99:
                flag = " ← noisy"
            print(f"  {p:6.2f}  {mean_w:+10.4f}  {std_w:10.4f}  {mean_r2:10.5f}  {len(omegas):6d}{flag}")
            if mean_r2 >= 0.95 and std_w < abs(mean_w) * 0.3:
                good_p.append(p)
                good_omega.append(mean_w)

        # Fit
        if len(good_p) >= 4:
            n_g = len(good_p)
            p2 = [pp ** 2 for pp in good_p]
            sp2, sw = sum(p2), sum(good_omega)
            sp2p2 = sum(x * x for x in p2)
            sp2w = sum(x * y for x, y in zip(p2, good_omega))
            den = n_g * sp2p2 - sp2 * sp2

            if abs(den) > 1e-30:
                a = (n_g * sp2w - sp2 * sw) / den
                b = (sw - a * sp2) / n_g
                pred = [a * pp ** 2 + b for pp in good_p]
                ss_res = sum((w - p) ** 2 for w, p in zip(good_omega, pred))
                ss_tot = sum((w - sw / n_g) ** 2 for w in good_omega)
                r2_s = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0

                w2 = [w ** 2 for w in good_omega]
                sw2 = sum(w2)
                sp2w2 = sum(x * y for x, y in zip(p2, w2))
                a_kg = (n_g * sp2w2 - sp2 * sw2) / den
                m2 = (sw2 - a_kg * sp2) / n_g
                pred_kg = [a_kg * pp ** 2 + m2 for pp in good_p]
                ss_res_kg = sum((w2i - p) ** 2 for w2i, p in zip(w2, pred_kg))
                ss_tot_kg = sum((w2i - sw2 / n_g) ** 2 for w2i in w2)
                r2_kg = 1 - ss_res_kg / ss_tot_kg if ss_tot_kg > 1e-30 else 0

                ap = [abs(pp) for pp in good_p]
                sap = sum(ap); sapap = sum(x * x for x in ap)
                sapw = sum(x * y for x, y in zip(ap, good_omega))
                den_l = n_g * sapap - sap * sap
                r2_l = 0; c_l = 0; d_l = 0
                if abs(den_l) > 1e-30:
                    c_l = (n_g * sapw - sap * sw) / den_l
                    d_l = (sw - c_l * sap) / n_g
                    pred_l = [c_l * abs(pp) + d_l for pp in good_p]
                    ss_res_l = sum((w - p) ** 2 for w, p in zip(good_omega, pred_l))
                    r2_l = 1 - ss_res_l / ss_tot if ss_tot > 1e-30 else 0

                m_eff = -1 / (2 * a) if abs(a) > 1e-30 else float('inf')
                print(f"\n  FITS (H={H}):")
                print(f"    Schrödinger: ω = {a:.6f}·p² + {b:.6f}    R² = {r2_s:.7f}")
                print(f"    Klein-Gordon: ω² = {a_kg:.6f}·p² + {m2:.6f}   R² = {r2_kg:.7f}")
                print(f"    Linear: ω = {c_l:.6f}·|p| + {d_l:.6f}         R² = {r2_l:.7f}")
                print(f"    m_eff = {m_eff:.4f}")

                winner = "Schrödinger" if r2_s >= r2_kg and r2_s >= r2_l else (
                    "Klein-Gordon" if r2_kg >= r2_l else "Linear")
                print(f"    WINNER: {winner}")
        else:
            print(f"\n  Only {len(good_p)} clean points — not enough to fit.")

    print(f"\n{'='*80}")
    print("CROSS-COMPARISON")
    print("=" * 80)
    print("  2D lattice h=0.5: Schrödinger R²=0.9995")
    print("  3D lattice h=0.5: None fits well (band structure, R²<0.68)")
    print("  3D grown DAG:     see results above")
    print("  If DAG matches 3D lattice → dimension matters, not randomness")
    print("  If DAG matches 2D lattice → randomness matters, not dimension")
    print("  If DAG matches neither   → grown DAG has its own physics")


if __name__ == "__main__":
    main()
