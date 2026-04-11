#!/usr/bin/env python3
"""
Full Newton's law test: F proportional to M_A * M_B / r^2.

Previous results established F proportional to M (R^2=0.987) and 1/r^2
(exponent -2.02 +/- 0.07) separately. This script tests the FULL product
law by sweeping M_A x M_B independently.

Protocol:
  - Wilson 3D, side=15, open BC, G=5, DT=0.08, mu2=0.001
  - Two Gaussians sigma=1.0 at separation d=5
  - Source for Phi = M_B_weight * |psi_B|^2 + M_A_weight * |psi_A|^2
  - Measure individual centroid accelerations (not just separation)
  - F_on_A should scale with M_B (source strength of B)
  - F_on_B should scale with M_A (source strength of A)
  - Newton's third law: F_on_A = -F_on_B

Sweep: M_weight in [0.5, 1.0, 2.0, 3.0] for both A and B independently.
"""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import expm_multiply, spsolve


# ── parameters ──────────────────────────────────────────────────────────
SIDE = 15
N = SIDE ** 3
MASS = 0.30
WILSON_R = 1.0
DT = 0.08
REG = 1e-3
N_STEPS = 20
SIGMA = 1.0
G_VAL = 5.0
MU2 = 0.001
D_SEP = 5


# ── lattice setup (open BC) ────────────────────────────────────────────
pos = np.zeros((N, 3))
adj: dict[int, list[int]] = {}

for x in range(SIDE):
    for y in range(SIDE):
        for z in range(SIDE):
            i = x * SIDE**2 + y * SIDE + z
            pos[i] = [x, y, z]
            adj[i] = []
            for dx, dy, dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < SIDE and 0 <= ny < SIDE and 0 <= nz < SIDE:
                    adj[i].append(nx * SIDE**2 + ny * SIDE + nz)


def build_laplacian():
    rows, cols, vals = [], [], []
    for i in range(N):
        rows.append(i); cols.append(i); vals.append(-len(adj[i]))
        for j in adj[i]:
            rows.append(i); cols.append(j); vals.append(1.0)
    return sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))

LAP = build_laplacian()


def solve_poisson(rho):
    A = LAP - MU2 * sparse.eye(N) - REG * sparse.eye(N)
    rhs = -4.0 * np.pi * G_VAL * rho
    return spsolve(A.tocsc(), rhs).real


def build_wilson_hamiltonian(phi):
    rows, cols, vals = [], [], []
    for i in range(N):
        for j in adj[i]:
            if j <= i:
                continue
            rows.append(i); cols.append(j); vals.append(-0.5j + 0.5 * WILSON_R)
            rows.append(j); cols.append(i); vals.append(+0.5j + 0.5 * WILSON_R)
        diag = MASS + phi[i] + 0.5 * WILSON_R * len(adj[i])
        rows.append(i); cols.append(i); vals.append(diag)
    return sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))


def gaussian_wavepacket(center, sigma=SIGMA):
    psi = np.zeros(N, dtype=complex)
    cx, cy, cz = center
    for i in range(N):
        x, y, z = pos[i]
        r2 = (x - cx)**2 + (y - cy)**2 + (z - cz)**2
        psi[i] = np.exp(-r2 / (2 * sigma**2))
    psi /= np.linalg.norm(psi)
    return psi


def center_of_mass_x(psi):
    rho = np.abs(psi)**2
    return float(np.sum(rho * pos[:, 0]) / max(np.sum(rho), 1e-30))


def evolve_step(psi, H):
    return expm_multiply(-1j * DT * H, psi)


# ── run one pair returning INDIVIDUAL centroid trajectories ─────────────
def run_pair(mode, center_a, center_b, mass_a, mass_b):
    """
    Evolve two orbitals and return individual centroid-x trajectories.

    mode: 'SHARED' or 'SELF_ONLY'
    mass_a, mass_b: source weights for Poisson equation
    """
    psi_a = gaussian_wavepacket(center_a)
    psi_b = gaussian_wavepacket(center_b)

    cx_a = np.zeros(N_STEPS + 1)
    cx_b = np.zeros(N_STEPS + 1)
    cx_a[0] = center_of_mass_x(psi_a)
    cx_b[0] = center_of_mass_x(psi_b)

    for t in range(N_STEPS):
        if mode == "SHARED":
            rho_total = mass_a * np.abs(psi_a)**2 + mass_b * np.abs(psi_b)**2
            phi = solve_poisson(rho_total)
            H_a = build_wilson_hamiltonian(phi)
            H_b = build_wilson_hamiltonian(phi)
        elif mode == "SELF_ONLY":
            phi_a = solve_poisson(mass_a * np.abs(psi_a)**2)
            phi_b = solve_poisson(mass_b * np.abs(psi_b)**2)
            H_a = build_wilson_hamiltonian(phi_a)
            H_b = build_wilson_hamiltonian(phi_b)
        else:
            H_a = build_wilson_hamiltonian(np.zeros(N))
            H_b = build_wilson_hamiltonian(np.zeros(N))

        psi_a = evolve_step(psi_a, H_a)
        psi_b = evolve_step(psi_b, H_b)
        psi_a /= np.linalg.norm(psi_a)
        psi_b /= np.linalg.norm(psi_b)

        cx_a[t + 1] = center_of_mass_x(psi_a)
        cx_b[t + 1] = center_of_mass_x(psi_b)

    return cx_a, cx_b


def acceleration_array(cx):
    """Second-order finite difference acceleration of centroid trajectory."""
    a = np.zeros(len(cx))
    a[1:-1] = (cx[2:] - 2 * cx[1:-1] + cx[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a


def mutual_acceleration(cx_shared, cx_self):
    """Mutual acceleration = acceleration in shared field minus self-only."""
    return acceleration_array(cx_shared) - acceleration_array(cx_self)


def early_mean(arr, t_start=2, t_end=11):
    """Mean over early timesteps [t_start, t_end)."""
    sl = slice(t_start, min(t_end, len(arr)))
    return float(np.mean(arr[sl]))


def linear_fit(xs, ys):
    """Linear fit y = a*x + b, return (slope, intercept, R^2)."""
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    slope, intercept = np.polyfit(xs, ys, 1)
    fit = slope * xs + intercept
    ss_res = float(np.sum((ys - fit)**2))
    ss_tot = float(np.sum((ys - np.mean(ys))**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2


# ── main ────────────────────────────────────────────────────────────────
def main():
    center = SIDE // 2  # = 7
    x_a = center - D_SEP // 2          # 7 - 2 = 5
    x_b = center + (D_SEP - D_SEP // 2)  # 7 + 3 = 10
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    print("=" * 88)
    print("FULL NEWTON'S LAW TEST: F ~ M_A * M_B / r^2")
    print("=" * 88)
    print(f"Lattice: {SIDE}^3 = {N} sites, open BC")
    print(f"Wilson: MASS={MASS}, r={WILSON_R}, DT={DT}")
    print(f"Gravity: G={G_VAL}, mu2={MU2}, REG={REG}")
    print(f"Gaussians: sigma={SIGMA}, separation d={D_SEP}")
    print(f"Positions: A at x={x_a}, B at x={x_b} (center at {center})")
    print(f"N_STEPS={N_STEPS}")
    print()

    mass_values = [0.5, 1.0, 2.0, 3.0]

    # ══════════════════════════════════════════════════════════════════
    # PART 1: Full M_A x M_B grid
    # ══════════════════════════════════════════════════════════════════
    print("=" * 88)
    print("PART 1: M_A x M_B GRID")
    print("=" * 88)
    print()
    print("For each (M_A, M_B), measure:")
    print("  F_on_A = mutual acceleration of A (should scale with M_B)")
    print("  F_on_B = mutual acceleration of B (should scale with M_A)")
    print("  Third law ratio = F_on_A / F_on_B  (should be ~ -1)")
    print()

    # Storage for analysis
    results = {}

    header = (f"{'M_A':>5s} {'M_B':>5s} | "
              f"{'F_on_A':>12s} {'F_on_B':>12s} | "
              f"{'3rd_law':>8s} | "
              f"{'F_A/M_B':>10s} {'F_B/M_A':>10s} | "
              f"{'time':>5s}")
    print(header)
    print("-" * len(header))

    t_total_start = time.time()

    for m_a in mass_values:
        for m_b in mass_values:
            t0 = time.time()

            cx_a_sh, cx_b_sh = run_pair("SHARED", center_a, center_b, m_a, m_b)
            cx_a_so, cx_b_so = run_pair("SELF_ONLY", center_a, center_b, m_a, m_b)

            f_on_a = early_mean(mutual_acceleration(cx_a_sh, cx_a_so))
            f_on_b = early_mean(mutual_acceleration(cx_b_sh, cx_b_so))

            elapsed = time.time() - t0

            # Third law ratio
            if abs(f_on_b) > 1e-12:
                third_law = f_on_a / f_on_b
            else:
                third_law = float('nan')

            # Normalized force per source mass
            f_a_per_mb = f_on_a / m_b if m_b > 0 else float('nan')
            f_b_per_ma = f_on_b / m_a if m_a > 0 else float('nan')

            results[(m_a, m_b)] = {
                'f_on_a': f_on_a,
                'f_on_b': f_on_b,
                'third_law': third_law,
                'f_a_per_mb': f_a_per_mb,
                'f_b_per_ma': f_b_per_ma,
            }

            print(f"{m_a:5.1f} {m_b:5.1f} | "
                  f"{f_on_a:+12.6f} {f_on_b:+12.6f} | "
                  f"{third_law:+8.3f} | "
                  f"{f_a_per_mb:+10.6f} {f_b_per_ma:+10.6f} | "
                  f"{elapsed:5.1f}s")

    t_total = time.time() - t_total_start
    print(f"\nTotal grid time: {t_total:.0f}s")

    # ══════════════════════════════════════════════════════════════════
    # PART 2: F_on_A vs M_B (fixing M_A = 1.0)
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 2: F_on_A vs M_B  (M_A = 1.0 fixed)")
    print("=" * 88)
    print("If Newton's law holds, F_on_A should be LINEAR in M_B.")
    print()

    mb_vals = []
    fa_vals = []
    for m_b in mass_values:
        r = results[(1.0, m_b)]
        mb_vals.append(m_b)
        fa_vals.append(r['f_on_a'])
        print(f"  M_B={m_b:.1f}:  F_on_A = {r['f_on_a']:+.6f}")

    slope, intercept, r2 = linear_fit(mb_vals, fa_vals)
    print(f"\n  Linear fit: F_on_A = {slope:.6f} * M_B + {intercept:.6f}")
    print(f"  R^2 = {r2:.6f}")
    print(f"  Intercept/slope = {abs(intercept/slope):.4f} (should be ~0 for proportionality)")

    # ══════════════════════════════════════════════════════════════════
    # PART 3: F_on_B vs M_A  (M_B = 1.0 fixed)
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 3: F_on_B vs M_A  (M_B = 1.0 fixed)")
    print("=" * 88)
    print("If Newton's law holds, F_on_B should be LINEAR in M_A.")
    print()

    ma_vals = []
    fb_vals = []
    for m_a in mass_values:
        r = results[(m_a, 1.0)]
        ma_vals.append(m_a)
        fb_vals.append(r['f_on_b'])
        print(f"  M_A={m_a:.1f}:  F_on_B = {r['f_on_b']:+.6f}")

    slope_b, intercept_b, r2_b = linear_fit(ma_vals, fb_vals)
    print(f"\n  Linear fit: F_on_B = {slope_b:.6f} * M_A + {intercept_b:.6f}")
    print(f"  R^2 = {r2_b:.6f}")
    print(f"  Intercept/slope = {abs(intercept_b/slope_b):.4f} (should be ~0 for proportionality)")

    # ══════════════════════════════════════════════════════════════════
    # PART 4: Newton's third law check
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 4: NEWTON'S THIRD LAW  (F_on_A = -F_on_B)")
    print("=" * 88)
    print()

    third_law_ratios = []
    for m_a in mass_values:
        for m_b in mass_values:
            r = results[(m_a, m_b)]
            if not np.isnan(r['third_law']):
                third_law_ratios.append(r['third_law'])
                deviation = abs(r['third_law'] + 1.0)
                status = "PASS" if deviation < 0.2 else ("MARGINAL" if deviation < 0.5 else "FAIL")
                print(f"  M_A={m_a:.1f}, M_B={m_b:.1f}: "
                      f"F_A/F_B = {r['third_law']:+.4f}  "
                      f"(deviation from -1: {deviation:.4f}) [{status}]")

    if third_law_ratios:
        mean_ratio = np.mean(third_law_ratios)
        std_ratio = np.std(third_law_ratios)
        print(f"\n  Mean F_A/F_B = {mean_ratio:+.4f} +/- {std_ratio:.4f}")
        print(f"  Expected: -1.000")

    # ══════════════════════════════════════════════════════════════════
    # PART 5: Full product law F ~ M_A * M_B
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 5: PRODUCT LAW  F_on_A ~ M_A_inertial * M_B_source ?")
    print("=" * 88)
    print()
    print("Test: is F_on_A proportional to M_B across ALL (M_A, M_B) pairs?")
    print("(The inertial response of A is the same regardless of M_A_source,")
    print(" since wavepackets are unit-normalized before mass_weight scaling.)")
    print()

    # For each M_A, plot F_on_A vs M_B and check linearity
    for m_a in mass_values:
        mbs = []
        fas = []
        for m_b in mass_values:
            r = results[(m_a, m_b)]
            mbs.append(m_b)
            fas.append(r['f_on_a'])

        sl, intc, r2_val = linear_fit(mbs, fas)
        print(f"  M_A={m_a:.1f}:  F_on_A = {sl:+.6f} * M_B + {intc:+.6f}  (R^2={r2_val:.6f})")

    print()
    print("If all R^2 ~ 1 with small intercepts, F_on_A ~ M_B confirmed for all M_A.")
    print()

    # Similarly for F_on_B vs M_A at each M_B
    print("Test: is F_on_B proportional to M_A across ALL (M_A, M_B) pairs?")
    print()
    for m_b in mass_values:
        mas = []
        fbs = []
        for m_a in mass_values:
            r = results[(m_a, m_b)]
            mas.append(m_a)
            fbs.append(r['f_on_b'])

        sl, intc, r2_val = linear_fit(mas, fbs)
        print(f"  M_B={m_b:.1f}:  F_on_B = {sl:+.6f} * M_A + {intc:+.6f}  (R^2={r2_val:.6f})")

    # ══════════════════════════════════════════════════════════════════
    # PART 6: Product scaling test: F_on_A / (M_B) should be constant
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 6: NORMALIZED FORCE TABLES")
    print("=" * 88)
    print()

    print("F_on_A / M_B  (should be constant across columns for each M_A row):")
    print(f"{'M_A\\M_B':>8s}", end="")
    for m_b in mass_values:
        print(f"  {m_b:>10.1f}", end="")
    print()
    print("-" * (8 + 12 * len(mass_values)))
    for m_a in mass_values:
        print(f"{m_a:8.1f}", end="")
        for m_b in mass_values:
            r = results[(m_a, m_b)]
            print(f"  {r['f_a_per_mb']:+10.6f}", end="")
        print()

    print()
    print("F_on_B / M_A  (should be constant across rows for each M_B column):")
    print(f"{'M_A\\M_B':>8s}", end="")
    for m_b in mass_values:
        print(f"  {m_b:>10.1f}", end="")
    print()
    print("-" * (8 + 12 * len(mass_values)))
    for m_a in mass_values:
        print(f"{m_a:8.1f}", end="")
        for m_b in mass_values:
            r = results[(m_a, m_b)]
            print(f"  {r['f_b_per_ma']:+10.6f}", end="")
        print()

    # ══════════════════════════════════════════════════════════════════
    # SUMMARY
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("SUMMARY")
    print("=" * 88)
    print()

    print(f"1. F_on_A vs M_B (M_A=1): slope={slope:.6f}, R^2={r2:.6f}")
    if r2 > 0.95:
        print(f"   PASS: F_on_A is LINEAR in M_B (R^2={r2:.4f})")
    elif r2 > 0.85:
        print(f"   MARGINAL: F_on_A roughly linear in M_B (R^2={r2:.4f})")
    else:
        print(f"   FAIL: F_on_A NOT linear in M_B (R^2={r2:.4f})")

    print(f"\n2. F_on_B vs M_A (M_B=1): slope={slope_b:.6f}, R^2={r2_b:.6f}")
    if r2_b > 0.95:
        print(f"   PASS: F_on_B is LINEAR in M_A (R^2={r2_b:.4f})")
    elif r2_b > 0.85:
        print(f"   MARGINAL: F_on_B roughly linear in M_A (R^2={r2_b:.4f})")
    else:
        print(f"   FAIL: F_on_B NOT linear in M_A (R^2={r2_b:.4f})")

    print(f"\n3. Newton's third law: mean F_A/F_B = {mean_ratio:+.4f} +/- {std_ratio:.4f}")
    if abs(mean_ratio + 1.0) < 0.1 and std_ratio < 0.1:
        print(f"   PASS: Third law holds (ratio ~ -1)")
    elif abs(mean_ratio + 1.0) < 0.3:
        print(f"   MARGINAL: Third law approximately holds")
    else:
        print(f"   FAIL: Third law violated")

    # Check full product law: F_on_A / M_B should be ~constant for each M_A
    all_fa_per_mb = []
    for m_a in mass_values:
        row_vals = [results[(m_a, m_b)]['f_a_per_mb'] for m_b in mass_values]
        all_fa_per_mb.extend(row_vals)
    fa_per_mb_std = np.std(all_fa_per_mb)
    fa_per_mb_mean = np.mean(all_fa_per_mb)
    cv = abs(fa_per_mb_std / fa_per_mb_mean) if abs(fa_per_mb_mean) > 1e-12 else float('inf')

    print(f"\n4. Product law: F_on_A/M_B across all pairs:")
    print(f"   mean = {fa_per_mb_mean:+.6f}, std = {fa_per_mb_std:.6f}, CV = {cv:.4f}")
    if cv < 0.15:
        print(f"   PASS: F_on_A/M_B ~ constant (CV={cv:.2%})")
    elif cv < 0.30:
        print(f"   MARGINAL: F_on_A/M_B roughly constant (CV={cv:.2%})")
    else:
        print(f"   FAIL: F_on_A/M_B NOT constant (CV={cv:.2%})")

    # Overall verdict
    print()
    passes = sum([r2 > 0.95, r2_b > 0.95,
                   abs(mean_ratio + 1.0) < 0.1 and std_ratio < 0.1,
                   cv < 0.15])
    total = 4
    print(f"OVERALL: {passes}/{total} tests passed")
    if passes == total:
        print("FULL NEWTON'S LAW F ~ M_A * M_B CONFIRMED")
    elif passes >= 3:
        print("Newton's law mostly confirmed, minor deviations")
    elif passes >= 2:
        print("Partial Newton's law; some aspects hold, others don't")
    else:
        print("Newton's law NOT confirmed at this parameter point")


if __name__ == "__main__":
    main()
