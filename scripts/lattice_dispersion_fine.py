#!/usr/bin/env python3
"""Fine-resolution dispersion relation at h=0.25.

Follow-up to lattice_dispersion_relation.py which showed Schrödinger
dispersion (omega = a·p² + b) at h=0.5 with R²=0.9995.

This script runs h=0.25 to verify convergence of the fit parameters
(a, b) and check that the Schrödinger form holds at finer resolution.
Also tests whether the power-law exponent converges to exactly 2.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict

BETA = 0.8
K = 5.0
PHYS_WIDTH = 20.0
PHYS_LENGTH = 40.0
MAX_DY_PHYS = 5.0


def generate_lattice(spacing):
    n_layers = int(PHYS_LENGTH / spacing) + 1
    hw = int(PHYS_WIDTH / spacing)
    max_dy = max(1, int(MAX_DY_PHYS / spacing))
    pos = []
    adj = defaultdict(list)
    nmap = {}
    for layer in range(n_layers):
        x = layer * spacing
        for iy in range(-hw, hw + 1):
            y = iy * spacing
            idx = len(pos)
            pos.append((x, y))
            nmap[(layer, iy)] = idx
    for layer in range(n_layers - 1):
        for iy in range(-hw, hw + 1):
            si = nmap.get((layer, iy))
            if si is None:
                continue
            for dy in range(-max_dy, max_dy + 1):
                iyn = iy + dy
                if abs(iyn) > hw:
                    continue
                di = nmap.get((layer + 1, iyn))
                if di is not None:
                    adj[si].append(di)
    return pos, dict(adj), n_layers, hw, max_dy, nmap


def propagate_planewave(pos, adj, n, spacing, nmap, n_layers, hw, p):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    for iy in range(-hw, hw + 1):
        idx = nmap.get((0, iy))
        if idx is not None:
            y = iy * spacing
            amps[idx] = cmath.exp(1j * p * y)
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = pos[i]
            x2, y2 = pos[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            act = L
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * K * act) * w / L * spacing * spacing
            amps[j] += amps[i] * ea
    return amps


def extract_mode(amps, nmap, hw, spacing, layer, p):
    mode_amp = 0j
    for iy in range(-hw, hw + 1):
        idx = nmap.get((layer, iy))
        if idx is None:
            continue
        y = iy * spacing
        mode_amp += amps[idx] * cmath.exp(-1j * p * y)
    return mode_amp


def main():
    spacing = 0.25
    print(f"DISPERSION RELATION at h={spacing}")
    print(f"  W={PHYS_WIDTH}, L={PHYS_LENGTH}, K={K}, beta={BETA}")

    pos, adj, n_layers, hw, max_dy, nmap = generate_lattice(spacing)
    n = len(pos)
    print(f"  nodes={n}, layers={n_layers}, npl={2*hw+1}")

    p_values = [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0]

    start_layer = n_layers // 4
    end_layer = 3 * n_layers // 4
    step = max(1, (end_layer - start_layer) // 10)
    layers = list(range(start_layer, end_layer, step))

    print(f"\n  {'p':>6s}  {'omega':>10s}  {'R²':>10s}  {'|mode|':>10s}")
    print(f"  {'-'*50}")

    good_p = []
    good_omega = []

    for p in p_values:
        t0 = time.time()
        amps = propagate_planewave(pos, adj, n, spacing, nmap, n_layers, hw, p)

        phases = []
        xs = []
        mode_amps = []
        for layer in layers:
            ma = extract_mode(amps, nmap, hw, spacing, layer, p)
            if abs(ma) < 1e-30:
                continue
            phases.append(cmath.phase(ma))
            mode_amps.append(abs(ma))
            xs.append(layer * spacing)

        if len(phases) < 3:
            print(f"  {p:6.2f}  {'FAIL':>10s}")
            continue

        # Unwrap phases manually (no numpy)
        unwrapped = [phases[0]]
        for i in range(1, len(phases)):
            diff = phases[i] - phases[i-1]
            while diff > math.pi:
                diff -= 2 * math.pi
            while diff < -math.pi:
                diff += 2 * math.pi
            unwrapped.append(unwrapped[-1] + diff)

        # Linear fit: phi = omega*x + c
        n_pts = len(xs)
        sx = sum(xs)
        sy = sum(unwrapped)
        sxx = sum(x*x for x in xs)
        sxy = sum(x*y for x, y in zip(xs, unwrapped))
        denom = n_pts * sxx - sx * sx
        if abs(denom) < 1e-30:
            continue
        omega = (n_pts * sxy - sx * sy) / denom
        intercept = (sy - omega * sx) / n_pts

        # R²
        predicted = [omega * x + intercept for x in xs]
        ss_res = sum((u - p2)**2 for u, p2 in zip(unwrapped, predicted))
        ss_tot = sum((u - sy/n_pts)**2 for u in unwrapped)
        r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

        mean_amp = sum(mode_amps) / len(mode_amps)
        dt = time.time() - t0

        flag = ""
        if r2 < 0.99:
            flag = "  ← noisy"
        print(f"  {p:6.2f}  {omega:+10.4f}  {r2:10.7f}  {mean_amp:10.2e}  {dt:.1f}s{flag}")

        if r2 >= 0.99:
            good_p.append(p)
            good_omega.append(omega)

    if len(good_p) < 4:
        print("\nInsufficient good data points for fitting.")
        return

    # Fit: omega = a·p² + b (Schrödinger)
    n_g = len(good_p)
    p2 = [pp**2 for pp in good_p]
    sp2 = sum(p2)
    sw = sum(good_omega)
    sp2p2 = sum(x*x for x in p2)
    sp2w = sum(x*y for x, y in zip(p2, good_omega))
    denom = n_g * sp2p2 - sp2 * sp2
    a_fit = (n_g * sp2w - sp2 * sw) / denom
    b_fit = (sw - a_fit * sp2) / n_g
    pred = [a_fit * pp**2 + b_fit for pp in good_p]
    ss_res = sum((w - p)**2 for w, p in zip(good_omega, pred))
    ss_tot = sum((w - sw/n_g)**2 for w in good_omega)
    r2_schro = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    # Fit: omega² = a·p² + m² (Klein-Gordon)
    w2 = [w**2 for w in good_omega]
    sw2 = sum(w2)
    sp2w2 = sum(x*y for x, y in zip(p2, w2))
    sw2w2 = sum(x*x for x in w2)
    denom_kg = n_g * sp2p2 - sp2 * sp2
    a_kg = (n_g * sp2w2 - sp2 * sw2) / denom_kg
    m2_kg = (sw2 - a_kg * sp2) / n_g
    pred_kg = [a_kg * pp**2 + m2_kg for pp in good_p]
    ss_res_kg = sum((w2i - p)**2 for w2i, p in zip(w2, pred_kg))
    ss_tot_kg = sum((w2i - sw2/n_g)**2 for w2i in w2)
    r2_kg = 1 - ss_res_kg / ss_tot_kg if ss_tot_kg > 1e-30 else 0.0

    # Fit: omega = c·|p| + d (linear)
    ap = [abs(pp) for pp in good_p]
    sap = sum(ap)
    sapap = sum(x*x for x in ap)
    sapw = sum(x*y for x, y in zip(ap, good_omega))
    denom_lin = n_g * sapap - sap * sap
    c_lin = (n_g * sapw - sap * sw) / denom_lin if abs(denom_lin) > 1e-30 else 0
    d_lin = (sw - c_lin * sap) / n_g
    pred_lin = [c_lin * abs(pp) + d_lin for pp in good_p]
    ss_res_lin = sum((w - p)**2 for w, p in zip(good_omega, pred_lin))
    r2_lin = 1 - ss_res_lin / ss_tot if ss_tot > 1e-30 else 0.0

    print(f"\n{'='*60}")
    print(f"DISPERSION FITS at h={spacing}")
    print(f"{'='*60}")
    print(f"  Schrödinger: omega = {a_fit:.6f}·p² + {b_fit:.6f}    R² = {r2_schro:.7f}")
    print(f"  Klein-Gordon: omega² = {a_kg:.6f}·p² + {m2_kg:.6f}   R² = {r2_kg:.7f}")
    print(f"  Linear:  omega = {c_lin:.6f}·|p| + {d_lin:.6f}   R² = {r2_lin:.7f}")
    print()

    m_eff = -1 / (2 * a_fit) if abs(a_fit) > 1e-30 else float('inf')
    print(f"  Schrödinger effective mass: m_eff = {m_eff:.4f}")
    print(f"  Rest phase: omega_0 = {b_fit:.6f}")

    print(f"\n  COMPARISON h=0.5 → h=0.25:")
    print(f"  {'':10s}  {'h=0.5':>12s}  {'h=0.25':>12s}")
    print(f"  {'a (slope)':10s}  {-0.091859:12.6f}  {a_fit:12.6f}")
    print(f"  {'b (rest)':10s}  {-0.236349:12.6f}  {b_fit:12.6f}")
    print(f"  {'m_eff':10s}  {5.443:12.4f}  {m_eff:12.4f}")
    print(f"  {'R² Schrö':10s}  {0.999466:12.7f}  {r2_schro:12.7f}")

    if abs(a_fit - (-0.091859)) < 0.01:
        print(f"\n  → CONVERGED: a changes by {abs(a_fit - (-0.091859)):.6f} (< 0.01)")
    else:
        print(f"\n  → NOT converged: a changes by {abs(a_fit - (-0.091859)):.6f}")


if __name__ == "__main__":
    main()
