#!/usr/bin/env python3
"""3D lattice dispersion relation measurement.

The 2D measurement showed Schrödinger dispersion ω=a·p²+b.
Does the 3D lattice (matching the actual grown-DAG geometry)
give the same result, or does 3D change the functional form?

In 3D, the angular weight is exp(−β·θ²) where θ involves BOTH
transverse dimensions: θ = atan2(√(dy²+dz²), dx).

We excite a plane wave in the z-direction: amp = exp(i·p_z·z)
with p_y = 0, and measure ω(p_z). We also test the (p_y, p_z)
plane to check isotropy.

If 3D gives ω² = p² + m² (Klein-Gordon) while 2D gave ω = a·p² + b
(Schrödinger), then the 3D propagator is fundamentally different
and ALL the 2D-based falsifications need revisiting.
"""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K = 5.0


def generate_3d_lattice(spacing, phys_width, phys_length, max_d_phys):
    """Regular 3D lattice: layers in x, transverse in y and z."""
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
                y = iy * spacing
                z = iz * spacing
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx

    for layer in range(n_layers - 1):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        iyn = iy + dy
                        izn = iz + dz
                        if abs(iyn) > hw or abs(izn) > hw:
                            continue
                        di = nmap.get((layer + 1, iyn, izn))
                        if di is not None:
                            adj[si].append(di)

    return pos, dict(adj), n_layers, hw, md, nmap


def propagate_planewave_3d(pos, adj, n, spacing, nmap, n_layers, hw, pz, py=0.0):
    """Plane wave in z-direction (and optionally y): amp = exp(i·(py·y + pz·z))."""
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n

    # Initialize source layer
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((0, iy, iz))
            if idx is not None:
                y = iy * spacing
                z = iz * spacing
                amps[idx] = cmath.exp(1j * (py * y + pz * z))

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1, z1 = pos[i]
            x2, y2, z2 = pos[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            # 3D angular weight: θ = atan2(transverse, longitudinal)
            r_perp = math.sqrt(dy * dy + dz * dz)
            theta = math.atan2(r_perp, max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            act = L  # free propagator
            ea = cmath.exp(1j * K * act) * w / L * spacing * spacing * spacing
            # NOTE: spacing³ for 3D measure (was spacing² in 2D)
            amps[j] += amps[i] * ea
    return amps


def extract_mode_3d(amps, nmap, hw, spacing, layer, pz, py=0.0):
    """Project onto exp(-i·(py·y+pz·z)) at given layer."""
    mode_amp = 0j
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((layer, iy, iz))
            if idx is None:
                continue
            y = iy * spacing
            z = iz * spacing
            mode_amp += amps[idx] * cmath.exp(-1j * (py * y + pz * z))
    return mode_amp


def measure_omega(pos, adj, n, spacing, nmap, n_layers, hw, pz, py=0.0):
    """Measure omega for given transverse momentum."""
    amps = propagate_planewave_3d(pos, adj, n, spacing, nmap, n_layers, hw, pz, py)

    start_layer = n_layers // 4
    end_layer = 3 * n_layers // 4
    step = max(1, (end_layer - start_layer) // 8)
    layers = list(range(start_layer, end_layer, step))

    phases = []
    xs = []
    mode_amps_list = []
    for layer in layers:
        ma = extract_mode_3d(amps, nmap, hw, spacing, layer, pz, py)
        if abs(ma) < 1e-30:
            continue
        phases.append(cmath.phase(ma))
        mode_amps_list.append(abs(ma))
        xs.append(layer * spacing)

    if len(phases) < 3:
        return float('nan'), 0.0, 0.0

    # Unwrap phases
    unwrapped = [phases[0]]
    for i in range(1, len(phases)):
        diff = phases[i] - phases[i - 1]
        while diff > math.pi:
            diff -= 2 * math.pi
        while diff < -math.pi:
            diff += 2 * math.pi
        unwrapped.append(unwrapped[-1] + diff)

    # Linear fit
    n_pts = len(xs)
    sx = sum(xs)
    sy = sum(unwrapped)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, unwrapped))
    denom = n_pts * sxx - sx * sx
    if abs(denom) < 1e-30:
        return float('nan'), 0.0, 0.0
    omega = (n_pts * sxy - sx * sy) / denom
    intercept = (sy - omega * sx) / n_pts

    predicted = [omega * x + intercept for x in xs]
    ss_res = sum((u - p) ** 2 for u, p in zip(unwrapped, predicted))
    ss_tot = sum((u - sy / n_pts) ** 2 for u in unwrapped)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    mean_amp = sum(mode_amps_list) / len(mode_amps_list)
    return omega, r2, mean_amp


def main():
    # Use smaller physical size for 3D (memory: nodes ∝ (W/h)² × (L/h))
    phys_width = 6.0   # Half-width (PW=6 matches the grown DAG)
    phys_length = 15.0  # T_phys = 15 matches the grown DAG
    max_d_phys = 3.0    # Transverse reach

    spacing = 1.0  # Start coarse (finer requires much more memory in 3D)

    print("=" * 80)
    print("3D LATTICE DISPERSION RELATION")
    print(f"  W={phys_width}, L={phys_length}, max_d={max_d_phys}")
    print(f"  h={spacing}, K={K}, β={BETA}")
    print("=" * 80)

    t0 = time.time()
    pos, adj, n_layers, hw, md, nmap = generate_3d_lattice(
        spacing, phys_width, phys_length, max_d_phys)
    n = len(pos)
    dt_gen = time.time() - t0
    npl = (2 * hw + 1) ** 2
    print(f"  nodes={n}, layers={n_layers}, npl={npl}, gen time={dt_gen:.1f}s")
    print(f"  Nyquist: p_max = π/h = {math.pi/spacing:.2f}")

    # Sweep p_z at p_y=0
    p_values = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5]

    print(f"\n  Z-direction sweep (p_y=0):")
    print(f"  {'p_z':>6s}  {'omega':>10s}  {'R²':>10s}  {'|mode|':>10s}  {'t':>5s}")
    print(f"  {'-'*55}")

    good_p = []
    good_omega = []
    for pz in p_values:
        t0 = time.time()
        omega, r2, amp = measure_omega(pos, adj, n, spacing, nmap, n_layers, hw, pz)
        dt = time.time() - t0
        flag = ""
        if r2 < 0.99:
            flag = " ← noisy"
        if math.isnan(omega):
            flag = " ← FAIL"
        print(f"  {pz:6.2f}  {omega:+10.4f}  {r2:10.7f}  {amp:10.2e}  {dt:4.1f}s{flag}")
        if r2 >= 0.99 and not math.isnan(omega):
            good_p.append(pz)
            good_omega.append(omega)

    # Also test a few diagonal momenta for isotropy check
    print(f"\n  Diagonal (p_y=p_z) sweep:")
    print(f"  {'|p|':>6s}  {'omega':>10s}  {'R²':>10s}  {'|mode|':>10s}")
    print(f"  {'-'*50}")

    for p_diag in [0.1, 0.3, 0.5, 1.0]:
        py_d = p_diag / math.sqrt(2)
        pz_d = p_diag / math.sqrt(2)
        omega, r2, amp = measure_omega(pos, adj, n, spacing, nmap, n_layers, hw, pz_d, py_d)
        flag = ""
        if r2 < 0.99:
            flag = " ← noisy"
        print(f"  {p_diag:6.2f}  {omega:+10.4f}  {r2:10.7f}  {amp:10.2e}{flag}")

    # Fit dispersion
    if len(good_p) >= 4:
        print(f"\n  FITTING omega(p_z) on {len(good_p)} clean points:")

        # Schrödinger: omega = a·p² + b
        n_g = len(good_p)
        p2 = [pp ** 2 for pp in good_p]
        sp2 = sum(p2)
        sw = sum(good_omega)
        sp2p2 = sum(x * x for x in p2)
        sp2w = sum(x * y for x, y in zip(p2, good_omega))
        denom = n_g * sp2p2 - sp2 * sp2
        if abs(denom) > 1e-30:
            a_fit = (n_g * sp2w - sp2 * sw) / denom
            b_fit = (sw - a_fit * sp2) / n_g
            pred = [a_fit * pp ** 2 + b_fit for pp in good_p]
            ss_res = sum((w - p) ** 2 for w, p in zip(good_omega, pred))
            ss_tot = sum((w - sw / n_g) ** 2 for w in good_omega)
            r2_s = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0

            # Klein-Gordon: omega² = a·p² + m²
            w2 = [w ** 2 for w in good_omega]
            sw2 = sum(w2)
            sp2w2 = sum(x * y for x, y in zip(p2, w2))
            a_kg = (n_g * sp2w2 - sp2 * sw2) / denom
            m2_kg = (sw2 - a_kg * sp2) / n_g
            pred_kg = [a_kg * pp ** 2 + m2_kg for pp in good_p]
            ss_res_kg = sum((w2i - p) ** 2 for w2i, p in zip(w2, pred_kg))
            ss_tot_kg = sum((w2i - sw2 / n_g) ** 2 for w2i in w2)
            r2_kg = 1 - ss_res_kg / ss_tot_kg if ss_tot_kg > 1e-30 else 0

            # Linear: omega = c·|p| + d
            ap = [abs(pp) for pp in good_p]
            sap = sum(ap)
            sapap = sum(x * x for x in ap)
            sapw = sum(x * y for x, y in zip(ap, good_omega))
            denom_l = n_g * sapap - sap * sap
            if abs(denom_l) > 1e-30:
                c_l = (n_g * sapw - sap * sw) / denom_l
                d_l = (sw - c_l * sap) / n_g
                pred_l = [c_l * abs(pp) + d_l for pp in good_p]
                ss_res_l = sum((w - p) ** 2 for w, p in zip(good_omega, pred_l))
                r2_l = 1 - ss_res_l / ss_tot if ss_tot > 1e-30 else 0
            else:
                r2_l = 0

            print(f"    Schrödinger: ω = {a_fit:.6f}·p² + {b_fit:.6f}    R² = {r2_s:.7f}")
            print(f"    Klein-Gordon: ω² = {a_kg:.6f}·p² + {m2_kg:.6f}   R² = {r2_kg:.7f}")
            print(f"    Linear: ω = {c_l:.6f}·|p| + {d_l:.6f}           R² = {r2_l:.7f}")

            m_eff = -1 / (2 * a_fit) if abs(a_fit) > 1e-30 else float('inf')
            print(f"\n    Effective mass (Schrödinger): m_eff = {m_eff:.4f}")

            # Winner
            winner = "Schrödinger" if r2_s > r2_kg and r2_s > r2_l else (
                "Klein-Gordon" if r2_kg > r2_l else "Linear")
            print(f"\n    WINNER: {winner}")
            print(f"    2D result was: Schrödinger (R²=0.9995)")
            if winner == "Klein-Gordon":
                print(f"    *** 3D CHANGES THE PHYSICS — RELATIVISTIC IN 3D! ***")
            elif winner == "Schrödinger":
                print(f"    3D confirms 2D: still non-relativistic")
            else:
                print(f"    3D gives linear (massless relativistic)?!")


if __name__ == "__main__":
    main()
