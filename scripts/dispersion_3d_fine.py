#!/usr/bin/env python3
"""3D dispersion at h=0.5 (h=1.0 was all noisy)."""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K = 5.0


def generate_3d_lattice(spacing, phys_width, phys_length, max_d_phys):
    n_layers = int(phys_length / spacing) + 1
    hw = int(phys_width / spacing)
    md = max(1, int(max_d_phys / spacing))
    pos = []
    adj = defaultdict(list)
    nmap = {}
    for layer in range(n_layers):
        x = layer * spacing
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = len(pos)
                pos.append((x, iy * spacing, iz * spacing))
                nmap[(layer, iy, iz)] = idx
    for layer in range(n_layers - 1):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        iyn, izn = iy + dy, iz + dz
                        if abs(iyn) > hw or abs(izn) > hw:
                            continue
                        di = nmap.get((layer + 1, iyn, izn))
                        if di is not None:
                            adj[si].append(di)
    return pos, dict(adj), n_layers, hw, md, nmap


def propagate_3d(pos, adj, n, h, nmap, n_layers, hw, pz, py=0.0):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((0, iy, iz))
            if idx is not None:
                amps[idx] = cmath.exp(1j * (py * iy * h + pz * iz * h))
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1, z1 = pos[i]
            x2, y2, z2 = pos[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            r_perp = math.sqrt(dy * dy + dz * dz)
            theta = math.atan2(r_perp, max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * K * L) * w / L * h * h * h
            amps[j] += amps[i] * ea
    return amps


def extract_mode_3d(amps, nmap, hw, h, layer, pz, py=0.0):
    mode_amp = 0j
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((layer, iy, iz))
            if idx is None:
                continue
            mode_amp += amps[idx] * cmath.exp(-1j * (py * iy * h + pz * iz * h))
    return mode_amp


def measure_omega(pos, adj, n, h, nmap, n_layers, hw, pz, py=0.0):
    amps = propagate_3d(pos, adj, n, h, nmap, n_layers, hw, pz, py)
    start = n_layers // 4
    end = 3 * n_layers // 4
    step = max(1, (end - start) // 8)
    layers = list(range(start, end, step))

    phases, xs, ma_list = [], [], []
    for layer in layers:
        ma = extract_mode_3d(amps, nmap, hw, h, layer, pz, py)
        if abs(ma) < 1e-30:
            continue
        phases.append(cmath.phase(ma))
        ma_list.append(abs(ma))
        xs.append(layer * h)

    if len(phases) < 3:
        return float('nan'), 0.0, 0.0

    # Unwrap
    unwrapped = [phases[0]]
    for i in range(1, len(phases)):
        d = phases[i] - phases[i - 1]
        while d > math.pi: d -= 2 * math.pi
        while d < -math.pi: d += 2 * math.pi
        unwrapped.append(unwrapped[-1] + d)

    np = len(xs)
    sx = sum(xs); sy = sum(unwrapped)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, unwrapped))
    den = np * sxx - sx * sx
    if abs(den) < 1e-30:
        return float('nan'), 0.0, 0.0
    omega = (np * sxy - sx * sy) / den
    b = (sy - omega * sx) / np

    pred = [omega * x + b for x in xs]
    ss_res = sum((u - p) ** 2 for u, p in zip(unwrapped, pred))
    ss_tot = sum((u - sy / np) ** 2 for u in unwrapped)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    return omega, r2, sum(ma_list) / len(ma_list)


def fit_and_report(good_p, good_omega, label):
    n_g = len(good_p)
    p2 = [pp ** 2 for pp in good_p]
    sp2, sw = sum(p2), sum(good_omega)
    sp2p2 = sum(x * x for x in p2)
    sp2w = sum(x * y for x, y in zip(p2, good_omega))
    den = n_g * sp2p2 - sp2 * sp2
    if abs(den) < 1e-30:
        return

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
    sap, sapap = sum(ap), sum(x * x for x in ap)
    sapw = sum(x * y for x, y in zip(ap, good_omega))
    den_l = n_g * sapap - sap * sap
    r2_l = 0
    c_l, d_l = 0, 0
    if abs(den_l) > 1e-30:
        c_l = (n_g * sapw - sap * sw) / den_l
        d_l = (sw - c_l * sap) / n_g
        pred_l = [c_l * abs(pp) + d_l for pp in good_p]
        ss_res_l = sum((w - p) ** 2 for w, p in zip(good_omega, pred_l))
        r2_l = 1 - ss_res_l / ss_tot if ss_tot > 1e-30 else 0

    print(f"\n  {label} FITS ({n_g} points):")
    print(f"    Schrödinger: ω = {a:.6f}·p² + {b:.6f}    R² = {r2_s:.7f}")
    print(f"    Klein-Gordon: ω² = {a_kg:.6f}·p² + {m2:.6f}   R² = {r2_kg:.7f}")
    print(f"    Linear: ω = {c_l:.6f}·|p| + {d_l:.6f}         R² = {r2_l:.7f}")

    m_eff = -1 / (2 * a) if abs(a) > 1e-30 else float('inf')
    print(f"    m_eff (Schrödinger) = {m_eff:.4f}")

    winner = "Schrödinger" if r2_s >= r2_kg and r2_s >= r2_l else (
        "Klein-Gordon" if r2_kg >= r2_l else "Linear")
    print(f"    WINNER: {winner}  (R² = {max(r2_s, r2_kg, r2_l):.7f})")
    return winner, r2_s, r2_kg, r2_l


def main():
    h = 0.5
    W = 6.0
    L = 15.0
    max_d = 3.0

    print("=" * 80)
    print(f"3D LATTICE DISPERSION at h={h}")
    print(f"  W={W}, L={L}, max_d={max_d}, K={K}, β={BETA}")
    print("=" * 80)

    t0 = time.time()
    pos, adj, n_layers, hw, md, nmap = generate_3d_lattice(h, W, L, max_d)
    n = len(pos)
    dt = time.time() - t0
    npl = (2 * hw + 1) ** 2
    print(f"  nodes={n}, layers={n_layers}, npl={npl}, gen={dt:.1f}s")

    p_values = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5]

    print(f"\n  Z-direction (p_y=0):")
    print(f"  {'p_z':>6s}  {'omega':>10s}  {'R²':>10s}  {'|mode|':>10s}  {'t':>5s}")
    print(f"  {'-'*55}")

    good_p, good_omega = [], []
    for pz in p_values:
        t0 = time.time()
        omega, r2, amp = measure_omega(pos, adj, n, h, nmap, n_layers, hw, pz)
        dt = time.time() - t0
        flag = ""
        if r2 < 0.99: flag = " ← noisy"
        if math.isnan(omega): flag = " ← FAIL"
        print(f"  {pz:6.2f}  {omega:+10.4f}  {r2:10.7f}  {amp:10.2e}  {dt:4.1f}s{flag}")
        if r2 >= 0.99 and not math.isnan(omega):
            good_p.append(pz)
            good_omega.append(omega)

    # Diagonal
    print(f"\n  Diagonal (p_y=p_z):")
    print(f"  {'|p|':>6s}  {'omega':>10s}  {'R²':>10s}  {'|mode|':>10s}")
    print(f"  {'-'*50}")
    for pd in [0.1, 0.3, 0.5, 1.0]:
        pc = pd / math.sqrt(2)
        omega, r2, amp = measure_omega(pos, adj, n, h, nmap, n_layers, hw, pc, pc)
        flag = ""
        if r2 < 0.99: flag = " ← noisy"
        print(f"  {pd:6.2f}  {omega:+10.4f}  {r2:10.7f}  {amp:10.2e}{flag}")

    if len(good_p) >= 4:
        fit_and_report(good_p, good_omega, "3D h=0.5")

        # Comparison with 2D
        print(f"\n  2D vs 3D COMPARISON:")
        print(f"    2D h=0.5: Schrödinger R²=0.9995, KG R²=0.9616")
        print(f"    3D h=0.5: see fits above")
    else:
        print(f"\n  Only {len(good_p)} clean points — insufficient for fitting.")
        print(f"  3D at h=0.5 may still be too coarse.")


if __name__ == "__main__":
    main()
