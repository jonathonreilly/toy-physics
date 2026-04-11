#!/usr/bin/env python3
"""
Open-Wilson source/response mass check on the two-orbital lane.

This script does NOT by itself establish full Newton closure.

What it really tests:
  - open 3D Wilson lattice, side=15, G=5, mu2=0.001
  - two separate orbitals at fixed separation d=5
  - Poisson source weights source_A, source_B multiply |psi_A|^2, |psi_B|^2
  - early mutual accelerations are extracted from SHARED - SELF_ONLY

What it does NOT test:
  - independent inertial-mass variation of the two orbitals
  - a true M_A * M_B force law
  - a valid momentum-balance / third-law check away from the equal-dynamics lane

So the honest read is:
  - source-linearity slices can be checked on an open Wilson surface
  - full both-masses Newton closure still needs a separate inertial-mass observable
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
    print("OPEN WILSON SOURCE/RESPONSE MASS CHECK")
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
    print("PART 1: SOURCE_A x SOURCE_B GRID")
    print("=" * 88)
    print()
    print("For each (source_A, source_B), measure:")
    print("  a_on_A = mutual acceleration of A from SHARED - SELF_ONLY")
    print("  a_on_B = mutual acceleration of B from SHARED - SELF_ONLY")
    print("  ratio a_A/a_B is only a force-symmetry proxy on this fixed-dynamics surface")
    print()

    # Storage for analysis
    results = {}

    header = (f"{'sA':>5s} {'sB':>5s} | "
              f"{'a_on_A':>12s} {'a_on_B':>12s} | "
              f"{'aA/aB':>8s} | "
              f"{'aA/sB':>10s} {'aB/sA':>10s} | "
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
    # PART 2: a_on_A vs source_B (fixing source_A = 1.0)
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 2: a_on_A vs source_B  (source_A = 1.0 fixed)")
    print("=" * 88)
    print("This checks source-linearity of the A response at fixed source_A.")
    print()

    mb_vals = []
    fa_vals = []
    for m_b in mass_values:
        r = results[(1.0, m_b)]
        mb_vals.append(m_b)
        fa_vals.append(r['f_on_a'])
        print(f"  source_B={m_b:.1f}:  a_on_A = {r['f_on_a']:+.6f}")

    slope, intercept, r2 = linear_fit(mb_vals, fa_vals)
    print(f"\n  Linear fit: a_on_A = {slope:.6f} * source_B + {intercept:.6f}")
    print(f"  R^2 = {r2:.6f}")
    print(f"  Intercept/slope = {abs(intercept/slope):.4f} (should be ~0 for proportionality)")

    # ══════════════════════════════════════════════════════════════════
    # PART 3: a_on_B vs source_A  (source_B = 1.0 fixed)
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 3: a_on_B vs source_A  (source_B = 1.0 fixed)")
    print("=" * 88)
    print("This checks source-linearity of the B response at fixed source_B.")
    print()

    ma_vals = []
    fb_vals = []
    for m_a in mass_values:
        r = results[(m_a, 1.0)]
        ma_vals.append(m_a)
        fb_vals.append(r['f_on_b'])
        print(f"  source_A={m_a:.1f}:  a_on_B = {r['f_on_b']:+.6f}")

    slope_b, intercept_b, r2_b = linear_fit(ma_vals, fb_vals)
    print(f"\n  Linear fit: a_on_B = {slope_b:.6f} * source_A + {intercept_b:.6f}")
    print(f"  R^2 = {r2_b:.6f}")
    print(f"  Intercept/slope = {abs(intercept_b/slope_b):.4f} (should be ~0 for proportionality)")

    # ══════════════════════════════════════════════════════════════════
    # PART 4: acceleration symmetry proxy
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 4: ACCELERATION SYMMETRY PROXY  (a_on_A ?= -a_on_B)")
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
                      f"a_A/a_B = {r['third_law']:+.4f}  "
                      f"(deviation from -1: {deviation:.4f}) [{status}]")

    if third_law_ratios:
        mean_ratio = np.mean(third_law_ratios)
        std_ratio = np.std(third_law_ratios)
        print(f"\n  Mean a_A/a_B = {mean_ratio:+.4f} +/- {std_ratio:.4f}")
        print("  Expected only as a proxy on this equal-dynamics surface, not as a full force law.")

    # ══════════════════════════════════════════════════════════════════
    # PART 5: source-linearity across the full grid
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 5: SOURCE-LINEARITY ACROSS THE FULL GRID")
    print("=" * 88)
    print()
    print("Test: is a_on_A proportional to source_B across ALL (source_A, source_B) pairs?")
    print("This is still a source-only statement:")
    print("  the orbitals remain unit-normalized")
    print("  the Wilson mass term is not varied per orbital")
    print("  so this is NOT a full inertial x source mass law")
    print()

    # For each source_A, plot a_on_A vs source_B and check linearity
    for m_a in mass_values:
        mbs = []
        fas = []
        for m_b in mass_values:
            r = results[(m_a, m_b)]
            mbs.append(m_b)
            fas.append(r['f_on_a'])

        sl, intc, r2_val = linear_fit(mbs, fas)
        print(f"  source_A={m_a:.1f}:  a_on_A = {sl:+.6f} * source_B + {intc:+.6f}  (R^2={r2_val:.6f})")

    print()
    print("If all R^2 ~ 1 with small intercepts, source-linearity survives across source_A slices.")
    print()

    # Similarly for a_on_B vs source_A at each source_B
    print("Test: is a_on_B proportional to source_A across ALL (source_A, source_B) pairs?")
    print()
    for m_b in mass_values:
        mas = []
        fbs = []
        for m_a in mass_values:
            r = results[(m_a, m_b)]
            mas.append(m_a)
            fbs.append(r['f_on_b'])

        sl, intc, r2_val = linear_fit(mas, fbs)
        print(f"  source_B={m_b:.1f}:  a_on_B = {sl:+.6f} * source_A + {intc:+.6f}  (R^2={r2_val:.6f})")

    # ══════════════════════════════════════════════════════════════════
    # PART 6: normalized acceleration tables
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 88)
    print("PART 6: NORMALIZED FORCE TABLES")
    print("=" * 88)
    print()

    print("a_on_A / source_B  (should be constant across columns for each source_A row if source-linear):")
    print(f"{'sA\\sB':>8s}", end="")
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
    print("a_on_B / source_A  (should be constant across rows for each source_B column if source-linear):")
    print(f"{'sA\\sB':>8s}", end="")
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

    print(f"1. a_on_A vs source_B (source_A=1): slope={slope:.6f}, R^2={r2:.6f}")
    if r2 > 0.95:
        print(f"   PASS: a_on_A is LINEAR in source_B on the anchor slice (R^2={r2:.4f})")
    elif r2 > 0.85:
        print(f"   MARGINAL: a_on_A roughly linear in source_B on the anchor slice (R^2={r2:.4f})")
    else:
        print(f"   FAIL: a_on_A NOT linear in source_B on the anchor slice (R^2={r2:.4f})")

    print(f"\n2. a_on_B vs source_A (source_B=1): slope={slope_b:.6f}, R^2={r2_b:.6f}")
    if r2_b > 0.95:
        print(f"   PASS: a_on_B is LINEAR in source_A on the anchor slice (R^2={r2_b:.4f})")
    elif r2_b > 0.85:
        print(f"   MARGINAL: a_on_B roughly linear in source_A on the anchor slice (R^2={r2_b:.4f})")
    else:
        print(f"   FAIL: a_on_B NOT linear in source_A on the anchor slice (R^2={r2_b:.4f})")

    print(f"\n3. acceleration symmetry proxy: mean a_A/a_B = {mean_ratio:+.4f} +/- {std_ratio:.4f}")
    if abs(mean_ratio + 1.0) < 0.1 and std_ratio < 0.1:
        print("   PASS: equal-and-opposite acceleration proxy holds on this fixed-dynamics surface")
    elif abs(mean_ratio + 1.0) < 0.3:
        print("   MARGINAL: equal-and-opposite acceleration proxy approximately holds")
    else:
        print("   FAIL: equal-and-opposite acceleration proxy breaks on the full source grid")

    # Check full product law: F_on_A / M_B should be ~constant for each M_A
    all_fa_per_mb = []
    for m_a in mass_values:
        row_vals = [results[(m_a, m_b)]['f_a_per_mb'] for m_b in mass_values]
        all_fa_per_mb.extend(row_vals)
    fa_per_mb_std = np.std(all_fa_per_mb)
    fa_per_mb_mean = np.mean(all_fa_per_mb)
    cv = abs(fa_per_mb_std / fa_per_mb_mean) if abs(fa_per_mb_mean) > 1e-12 else float('inf')

    print(f"\n4. source-linearity across the full grid: a_on_A/source_B across all pairs:")
    print(f"   mean = {fa_per_mb_mean:+.6f}, std = {fa_per_mb_std:.6f}, CV = {cv:.4f}")
    if cv < 0.15:
        print(f"   PASS: a_on_A/source_B ~ constant (CV={cv:.2%})")
    elif cv < 0.30:
        print(f"   MARGINAL: a_on_A/source_B roughly constant (CV={cv:.2%})")
    else:
        print(f"   FAIL: a_on_A/source_B NOT constant (CV={cv:.2%})")

    # Overall verdict
    print()
    passes = sum([r2 > 0.95, r2_b > 0.95,
                   abs(mean_ratio + 1.0) < 0.1 and std_ratio < 0.1,
                   cv < 0.15])
    total = 4
    print(f"OVERALL: {passes}/{total} checks passed")
    if passes == total:
        print("Source-linearity and equal-dynamics symmetry both look good on this surface.")
    elif passes >= 3:
        print("Strong slice-wise source-linearity survives, but the full source grid is not closed.")
    elif passes >= 2:
        print("Only partial source-linearity survives; this is NOT a retained both-masses law.")
    else:
        print("This surface does not support a retainable both-masses law.")

    print()
    print("NEXT REQUIRED OBSERVABLE:")
    print("  give the two orbitals independent inertial masses in H_A and H_B,")
    print("  then measure early-time mutual momentum transfer")
    print("    P_A^mut = M_A * a_A^(shared-self_only)")
    print("    P_B^mut = M_B * a_B^(shared-self_only)")
    print("  on the same open, weak-screening Wilson surface.")
    print("  That is the first observable that can genuinely test M_A*M_B scaling")
    print("  together with an action-reaction law.")


if __name__ == "__main__":
    main()
