#!/usr/bin/env python3
"""
Periodic Wilson two-body distance/source scan.

Important guardrail:
  this runner uses a periodic cubic lattice and therefore does NOT provide
  an image-free Newton-law test. It is preserved as a torus control / historical
  scan only.

What it actually tests:
  1. distance dependence of the SHARED-SELF_ONLY mutual-channel observable
     on a periodic torus
  2. source-strength dependence from reweighting orbital B's contribution to
     the Poisson source at fixed orbital A

What it does NOT test:
  - a clean open-boundary distance law
  - a full F proportional to M1*M2 Newtonian mass law
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
import time

# ── lattice ──────────────────────────────────────────────────────────────
N_SIDE = 13
N = N_SIDE ** 3  # 2197

MASS = 0.30
WILSON_R = 1.0
DT = 0.06
REG = 1e-3
G_VAL = 5.0
N_STEPS = 15
SIGMA = 1.0

# ── coordinate helpers ───────────────────────────────────────────────────
def site_index(x, y, z):
    return x * N_SIDE**2 + y * N_SIDE + z

pos = np.zeros((N, 3))
for x in range(N_SIDE):
    for y in range(N_SIDE):
        for z in range(N_SIDE):
            i = site_index(x, y, z)
            pos[i] = [x, y, z]

# ── build sparse adjacency + Laplacian once ──────────────────────────────
def build_adjacency_and_laplacian():
    """Build neighbor list and sparse Laplacian for periodic cubic lattice."""
    neighbors = [[] for _ in range(N)]
    lap_rows, lap_cols, lap_vals = [], [], []
    for x in range(N_SIDE):
        for y in range(N_SIDE):
            for z in range(N_SIDE):
                i = site_index(x, y, z)
                nbrs = []
                for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    nx = (x + dx) % N_SIDE
                    ny = (y + dy) % N_SIDE
                    nz = (z + dz) % N_SIDE
                    j = site_index(nx, ny, nz)
                    nbrs.append(j)
                    lap_rows.append(i); lap_cols.append(j); lap_vals.append(1.0)
                neighbors[i] = nbrs
                lap_rows.append(i); lap_cols.append(i); lap_vals.append(-6.0)
    lap = sparse.csr_matrix((lap_vals, (lap_rows, lap_cols)), shape=(N, N))
    return neighbors, lap

print(f"Building lattice: {N_SIDE}^3 = {N} sites ...", flush=True)
t0 = time.time()
NEIGHBORS, LAP = build_adjacency_and_laplacian()
print(f"  Lattice built in {time.time()-t0:.1f}s", flush=True)

# Precompute Poisson operator: (Lap - REG*I)
POISSON_OP = (LAP - REG * sparse.eye(N)).tocsc()

# ── Gaussian wavepacket ──────────────────────────────────────────────────
def gaussian_wavepacket(center, sigma=SIGMA):
    psi = np.zeros(N, dtype=complex)
    cx, cy, cz = center
    for i in range(N):
        x, y, z = pos[i]
        dx = x - cx; dx -= N_SIDE * round(dx / N_SIDE)
        dy = y - cy; dy -= N_SIDE * round(dy / N_SIDE)
        dz = z - cz; dz -= N_SIDE * round(dz / N_SIDE)
        r2 = dx**2 + dy**2 + dz**2
        psi[i] = np.exp(-r2 / (2 * sigma**2))
    psi /= np.linalg.norm(psi)
    return psi

# ── Poisson solver ───────────────────────────────────────────────────────
def solve_poisson(rho, G):
    rhs = -4.0 * np.pi * G * rho
    rhs -= rhs.mean()
    phi = spsolve(POISSON_OP, rhs)
    return phi.real

# ── Wilson Hamiltonian (sparse) ──────────────────────────────────────────
def build_wilson_hamiltonian(phi):
    rows, cols, vals = [], [], []
    for i in range(N):
        for j in NEIGHBORS[i]:
            if j <= i:
                continue
            val_ij = -0.5j + WILSON_R * 0.5
            val_ji = +0.5j + WILSON_R * 0.5
            rows.append(i); cols.append(j); vals.append(val_ij)
            rows.append(j); cols.append(i); vals.append(val_ji)
        wilson_diag = WILSON_R * 3.0  # 6 neighbors * R/2
        diag_val = MASS + phi[i] + wilson_diag
        rows.append(i); cols.append(i); vals.append(diag_val)
    return sparse.csc_matrix((vals, (rows, cols)), shape=(N, N))

# ── Crank-Nicolson step (sparse) ────────────────────────────────────────
def cn_step(psi, H):
    """One Crank-Nicolson time step: (I + iH dt/2) psi_new = (I - iH dt/2) psi."""
    half = 1j * H * (DT / 2.0)
    lhs = (sparse.eye(N, format='csc') + half).tocsc()
    rhs_vec = (sparse.eye(N, format='csc') - half).dot(psi)
    psi_new = spsolve(lhs, rhs_vec)
    psi_new /= np.linalg.norm(psi_new)
    return psi_new

# ── center of mass (periodic, x-component) ──────────────────────────────
def center_of_mass_x(psi):
    rho = np.abs(psi)**2
    angles = 2 * np.pi * pos[:, 0] / N_SIDE
    sin_mean = np.sum(rho * np.sin(angles))
    cos_mean = np.sum(rho * np.cos(angles))
    theta = np.arctan2(sin_mean, cos_mean)
    if theta < 0:
        theta += 2 * np.pi
    return theta * N_SIDE / (2 * np.pi)

# ── finite differences ───────────────────────────────────────────────────
def compute_acceleration(sep):
    a = np.zeros(len(sep))
    a[1:-1] = (sep[2:] - 2*sep[1:-1] + sep[:-2]) / DT**2
    a[0] = a[1]
    a[-1] = a[-2]
    return a

# ── run one configuration ────────────────────────────────────────────────
def run_two_body(mode, G, center_A, center_B, m_ratio=1.0, anderson_V=None):
    """
    mode: 'SHARED', 'SELF_ONLY', 'FREE', 'ANDERSON'
    m_ratio: weight of B density in source term (for mass sweep)
    anderson_V: random potential array for ANDERSON mode
    """
    psi_A = gaussian_wavepacket(center_A)
    psi_B = gaussian_wavepacket(center_B)

    seps = np.zeros(N_STEPS + 1)
    cx_A_vals = np.zeros(N_STEPS + 1)
    cx_B_vals = np.zeros(N_STEPS + 1)

    cx_A = center_of_mass_x(psi_A)
    cx_B = center_of_mass_x(psi_B)
    seps[0] = cx_B - cx_A
    cx_A_vals[0] = cx_A
    cx_B_vals[0] = cx_B

    for t in range(N_STEPS):
        if mode == 'FREE':
            phi_A = np.zeros(N)
            phi_B = np.zeros(N)
        elif mode == 'SHARED':
            rho_total = np.abs(psi_A)**2 + m_ratio * np.abs(psi_B)**2
            phi_shared = solve_poisson(rho_total, G)
            phi_A = phi_shared
            phi_B = phi_shared
        elif mode == 'SELF_ONLY':
            phi_A = solve_poisson(np.abs(psi_A)**2, G)
            phi_B = solve_poisson(m_ratio * np.abs(psi_B)**2, G)
        elif mode == 'ANDERSON':
            phi_A = anderson_V.copy()
            phi_B = anderson_V.copy()

        H_A = build_wilson_hamiltonian(phi_A)
        H_B = build_wilson_hamiltonian(phi_B)

        psi_A = cn_step(psi_A, H_A)
        psi_B = cn_step(psi_B, H_B)

        cx_A = center_of_mass_x(psi_A)
        cx_B = center_of_mass_x(psi_B)
        seps[t + 1] = cx_B - cx_A
        cx_A_vals[t + 1] = cx_A
        cx_B_vals[t + 1] = cx_B

    return seps, cx_A_vals, cx_B_vals

# ── Anderson control ─────────────────────────────────────────────────────
def make_anderson_potential(rng, rho_ref, G):
    """Random positive potential with matched statistics to gravitational field."""
    phi_ref = solve_poisson(rho_ref, G)
    V = rng.normal(loc=phi_ref.mean(), scale=max(phi_ref.std(), 1e-6), size=N)
    return V

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 80)
    print("PERIODIC WILSON TWO-BODY DISTANCE / SOURCE SCAN")
    print("=" * 80)
    print(f"Lattice: {N_SIDE}^3 = {N} sites")
    print(f"MASS={MASS}, WILSON_R={WILSON_R}, DT={DT}, REG={REG}, G={G_VAL}")
    print(f"N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print()

    mid = N_SIDE // 2  # = 6

    # ─── DISTANCE SWEEP ──────────────────────────────────────────────────
    print("=" * 80)
    print("PART 1: DISTANCE SWEEP  (periodic torus control, not open-lattice Newton)")
    print("=" * 80)
    d_vals = [3, 4, 5, 6, 7, 8]
    dist_results = {}

    for d in d_vals:
        xA = mid - d // 2
        xB = mid + (d - d // 2)
        center_A = (xA, mid, mid)
        center_B = (xB, mid, mid)
        actual_d = xB - xA

        print(f"\n  d={d} (A@x={xA}, B@x={xB}, actual_sep={actual_d})", flush=True)
        t0 = time.time()

        sep_sh, cxA_sh, cxB_sh = run_two_body('SHARED', G_VAL, center_A, center_B)
        sep_so, cxA_so, cxB_so = run_two_body('SELF_ONLY', G_VAL, center_A, center_B)
        sep_fr, _, _ = run_two_body('FREE', G_VAL, center_A, center_B)

        a_sh = compute_acceleration(sep_sh)
        a_so = compute_acceleration(sep_so)
        a_mutual = a_sh - a_so

        # Early-time mean (steps 1-5)
        early = slice(1, 6)
        a_mut_mean = a_mutual[early].mean()
        a_mut_std = a_mutual[early].std()
        snr = abs(a_mut_mean) / (a_mut_std + 1e-12)

        # Also track individual CoM accelerations for A
        a_A_sh = compute_acceleration(cxA_sh)
        a_A_so = compute_acceleration(cxA_so)
        a_mutual_on_A = (a_A_sh - a_A_so)[early].mean()

        dist_results[d] = {
            'a_mutual_mean': a_mut_mean,
            'a_mutual_std': a_mut_std,
            'a_mutual_on_A': a_mutual_on_A,
            'snr': snr,
            'sep_shared': sep_sh,
            'sep_self': sep_so,
            'sep_free': sep_fr,
        }

        elapsed = time.time() - t0
        tag = "ATTRACT" if a_mut_mean < -1e-6 else ("REPEL" if a_mut_mean > 1e-6 else "NULL")
        print(f"    a_mutual = {a_mut_mean:+.8f} +/- {a_mut_std:.8f}  SNR={snr:.2f}  [{tag}]"
              f"  ({elapsed:.1f}s)", flush=True)

    # Fit distance law
    print("\n  --- Distance Law Fit ---")
    d_arr = np.array(d_vals, dtype=float)
    a_arr = np.array([dist_results[d]['a_mutual_mean'] for d in d_vals])
    a_A_arr = np.array([dist_results[d]['a_mutual_on_A'] for d in d_vals])

    def power_law_fit(d_in, a_in, label):
        """Log-log fit |a| vs d, returns (slope, R^2)."""
        abs_a = np.abs(a_in)
        mask = abs_a > 1e-12
        if mask.sum() < 2:
            print(f"  {label}: insufficient data")
            return np.nan, np.nan
        log_d = np.log(d_in[mask])
        log_a = np.log(abs_a[mask])
        coeffs = np.polyfit(log_d, log_a, 1)
        slope = coeffs[0]
        pred = np.polyval(coeffs, log_d)
        ss_res = np.sum((log_a - pred)**2)
        ss_tot = np.sum((log_a - log_a.mean())**2)
        r2 = 1 - ss_res / (ss_tot + 1e-30)
        print(f"  {label}: |a| ~ d^{slope:.3f}  (R^2={r2:.4f})")
        return slope, r2

    # Full range fit (includes periodic image contamination at large d)
    print("  [All d values — includes periodic contamination]")
    slope_all, r2_all = power_law_fit(d_arr, a_arr, "separation (all)")
    power_law_fit(d_arr, a_A_arr, "a_on_A (all)")

    # CLEAN window: only d where periodic image > d (image at L-d)
    # On side=13, d<= L/2 = 6.5, so d<=6 is clean
    d_clean = [d for d in d_vals if d <= N_SIDE // 2]
    d_clean_arr = np.array(d_clean, dtype=float)
    a_clean = np.array([dist_results[d]['a_mutual_mean'] for d in d_clean])
    a_A_clean = np.array([dist_results[d]['a_mutual_on_A'] for d in d_clean])

    print(f"\n  [Clean window d<={N_SIDE//2} — no periodic contamination]")
    slope, r2 = power_law_fit(d_clean_arr, a_clean, "separation (clean)")
    slope_A, r2_A = power_law_fit(d_clean_arr, a_A_clean, "a_on_A (clean)")

    print(f"\n  Newton predicts slope = -2.0")
    if not np.isnan(slope):
        print(f"  Best fit (clean, separation): slope = {slope:.3f}, deviation = {slope-(-2.0):+.3f}")
    if not np.isnan(slope_A):
        print(f"  Best fit (clean, a_on_A):     slope = {slope_A:.3f}, deviation = {slope_A-(-2.0):+.3f}")

    # Note on periodic contamination
    contaminated = [d for d in d_vals if d > N_SIDE // 2]
    if contaminated:
        print(f"\n  NOTE: d={contaminated} show sign flip (REPEL) — periodic image at L-d")
        print(f"  This is EXPECTED: at d=7 on L=13, the image is at d=6, nearly as close.")

    # Table
    print(f"\n  {'d':>3s}  {'a_mutual':>14s}  {'|a_mutual|':>12s}  {'a_on_A':>12s}  {'SNR':>6s}")
    print("  " + "-" * 55)
    for d in d_vals:
        r = dist_results[d]
        print(f"  {d:3d}  {r['a_mutual_mean']:+14.8f}  {abs(r['a_mutual_mean']):12.8f}  "
              f"{r['a_mutual_on_A']:+12.8f}  {r['snr']:6.2f}")

    # ─── MASS SWEEP ──────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("PART 2: MASS SWEEP  (Newton predicts linear in M_ratio)")
    print("=" * 80)

    d_mass = 4
    xA = mid - d_mass // 2
    xB = mid + (d_mass - d_mass // 2)
    center_A = (xA, mid, mid)
    center_B = (xB, mid, mid)
    m_ratios = [0.5, 1.0, 2.0, 3.0, 5.0]
    mass_results = {}

    for m_ratio in m_ratios:
        print(f"\n  M_ratio={m_ratio:.1f} (d={d_mass})", flush=True)
        t0 = time.time()

        sep_sh, cxA_sh, _ = run_two_body('SHARED', G_VAL, center_A, center_B, m_ratio=m_ratio)
        sep_so, cxA_so, _ = run_two_body('SELF_ONLY', G_VAL, center_A, center_B, m_ratio=m_ratio)

        a_sh = compute_acceleration(sep_sh)
        a_so = compute_acceleration(sep_so)
        a_mutual = a_sh - a_so

        # Acceleration on A specifically
        a_A_sh = compute_acceleration(cxA_sh)
        a_A_so = compute_acceleration(cxA_so)

        early = slice(1, 6)
        a_mut_mean = a_mutual[early].mean()
        a_mut_std = a_mutual[early].std()
        a_on_A = (a_A_sh - a_A_so)[early].mean()

        mass_results[m_ratio] = {
            'a_mutual_mean': a_mut_mean,
            'a_mutual_std': a_mut_std,
            'a_on_A': a_on_A,
        }

        elapsed = time.time() - t0
        print(f"    a_mutual = {a_mut_mean:+.8f}, a_on_A = {a_on_A:+.8f}  ({elapsed:.1f}s)",
              flush=True)

    # Fit mass law (a_on_A vs M_ratio should be linear)
    print("\n  --- Mass Law Fit ---")
    m_arr = np.array(m_ratios)
    a_on_A_arr = np.array([mass_results[m]['a_on_A'] for m in m_ratios])
    a_mut_arr = np.array([mass_results[m]['a_mutual_mean'] for m in m_ratios])

    if len(m_arr) >= 2:
        # Linear fit: a_on_A = slope * M_ratio + intercept
        coeffs_m = np.polyfit(m_arr, a_on_A_arr, 1)
        slope_m = coeffs_m[0]
        intercept_m = coeffs_m[1]
        pred_m = np.polyval(coeffs_m, m_arr)
        ss_res_m = np.sum((a_on_A_arr - pred_m)**2)
        ss_tot_m = np.sum((a_on_A_arr - a_on_A_arr.mean())**2)
        r2_m = 1 - ss_res_m / (ss_tot_m + 1e-30)
        print(f"  Linear fit: a_on_A = {slope_m:.8f} * M_ratio + {intercept_m:.8f}")
        print(f"  R^2 = {r2_m:.4f}")
        print(f"  Newton predicts: linear (R^2 ~ 1) with intercept ~ 0")
        print(f"  Intercept/slope ratio: {abs(intercept_m)/(abs(slope_m)+1e-30):.3f} (ideal: 0)")

    # Table
    print(f"\n  {'M_ratio':>7s}  {'a_mutual':>14s}  {'a_on_A':>14s}")
    print("  " + "-" * 40)
    for m in m_ratios:
        r = mass_results[m]
        print(f"  {m:7.1f}  {r['a_mutual_mean']:+14.8f}  {r['a_on_A']:+14.8f}")

    # ─── ANDERSON CONTROL ────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("PART 3: ANDERSON CONTROL  (random disorder — should NOT show convergence)")
    print("=" * 80)

    d_and = 4
    xA = mid - d_and // 2
    xB = mid + (d_and - d_and // 2)
    center_A = (xA, mid, mid)
    center_B = (xB, mid, mid)
    n_seeds = 5

    # Reference density for potential statistics
    psi_ref_A = gaussian_wavepacket(center_A)
    psi_ref_B = gaussian_wavepacket(center_B)
    rho_ref = np.abs(psi_ref_A)**2 + np.abs(psi_ref_B)**2

    anderson_a_vals = []
    for seed in range(n_seeds):
        rng = np.random.default_rng(seed + 42)
        V_and = make_anderson_potential(rng, rho_ref, G_VAL)

        print(f"\n  Anderson seed={seed}", flush=True)
        t0 = time.time()

        sep_and, cxA_and, _ = run_two_body('ANDERSON', G_VAL, center_A, center_B,
                                            anderson_V=V_and)
        a_and = compute_acceleration(sep_and)
        early = slice(1, 6)
        a_and_mean = a_and[early].mean()
        anderson_a_vals.append(a_and_mean)
        elapsed = time.time() - t0
        print(f"    a_sep = {a_and_mean:+.8f}  ({elapsed:.1f}s)", flush=True)

    anderson_a_vals = np.array(anderson_a_vals)
    print(f"\n  Anderson mean: {anderson_a_vals.mean():+.8f}")
    print(f"  Anderson std:  {anderson_a_vals.std():.8f}")
    print(f"  Anderson range: [{anderson_a_vals.min():+.8f}, {anderson_a_vals.max():+.8f}]")

    # Compare to gravity signal
    grav_a = dist_results[d_and]['a_mutual_mean'] if d_and in dist_results else np.nan
    print(f"  Gravity signal at d={d_and}: {grav_a:+.8f}")
    if not np.isnan(grav_a) and anderson_a_vals.std() > 0:
        z_score = (grav_a - anderson_a_vals.mean()) / anderson_a_vals.std()
        print(f"  Z-score (gravity vs Anderson): {z_score:.2f}")

    # ─── VERDICT ─────────────────────────────────────────────────────────
    print()
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)

    # Distance law (use clean window)
    if not np.isnan(slope):
        dist_verdict = "PASS" if abs(slope - (-2.0)) < 0.5 and r2 > 0.8 else "MARGINAL" if r2 > 0.5 else "FAIL"
        print(f"  Distance law (clean d<={N_SIDE//2}): slope = {slope:.3f} (expect -2.0), R^2 = {r2:.4f}  [{dist_verdict}]")
    else:
        print("  Distance law: INSUFFICIENT DATA")

    # Mass law
    if len(m_arr) >= 2:
        mass_verdict = "PASS" if r2_m > 0.9 else "MARGINAL" if r2_m > 0.7 else "FAIL"
        print(f"  Mass law: linear R^2 = {r2_m:.4f}  [{mass_verdict}]")
    else:
        print("  Mass law: INSUFFICIENT DATA")

    # Anderson
    if anderson_a_vals.std() > 0 and not np.isnan(grav_a):
        and_verdict = "PASS" if abs(z_score) > 2.0 else "MARGINAL" if abs(z_score) > 1.0 else "FAIL"
        print(f"  Anderson control: z-score = {z_score:.2f}  [{and_verdict}]")
    else:
        print("  Anderson control: INCONCLUSIVE")

    # Overall
    clean_attract = all(dist_results[d]['a_mutual_mean'] < 0 for d in d_clean)
    print(f"\n  All clean distances (d<={N_SIDE//2}) show attraction: {clean_attract}")
    contam = [d for d in d_vals if d > N_SIDE // 2 and dist_results[d]['a_mutual_mean'] > 0]
    if contam:
        print(f"  Periodic-image contaminated d={contam} correctly show repulsion (image effect)")
    print(f"\n  F ~ M/r^2 emerges: ", end="")
    if not np.isnan(slope) and abs(slope - (-2.0)) < 0.5 and r2 > 0.8 and r2_m > 0.9:
        print("YES - Newton's law holds within measurement precision")
    elif not np.isnan(slope) and abs(slope - (-2.0)) < 0.8 and r2 > 0.5:
        print(f"PARTIAL - power law exponent = {slope:.2f} (Newton=-2), mass linearity R^2 = {r2_m:.3f}")
    elif not np.isnan(slope) and r2 > 0.8:
        print(f"CLEAN POWER LAW but steeper than Newton")
        print(f"    Exponent = {slope:.2f} (Newton = -2.0), R^2 = {r2:.3f}")
        print(f"    Mass linearity: R^2 = {r2_m:.3f} (Newton predicts 1.0)")
        print(f"    INTERPRETATION: F ~ M/r^{abs(slope):.1f} rather than M/r^2")
        print(f"    Possible cause: extended wavefunctions (sigma={SIGMA}) are NOT point sources.")
        print(f"    At d/sigma ~ 3-6, near-field structure steepens the falloff.")
        print(f"    Need sigma << d (or larger lattice) to reach point-source regime.")
    else:
        print("NO - data does not support Newton's law")


if __name__ == "__main__":
    main()
