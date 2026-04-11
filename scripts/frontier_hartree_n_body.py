#!/usr/bin/env python3
"""Hartree N-body limit: semiclassical gravity from single-particle wavefunction.

Hartree trick: instead of N particles, use ONE wavefunction but source the
gravitational field with rho = N * |psi|^2. This gives effective mass M = N*m
while keeping the computation single-particle.

Tests whether the large-N Hartree limit recovers semiclassical gravity:
  1. Self-gravity contraction:  w_grav / w_free  vs  N
  2. Quantum Zeno threshold:    G_eff where spreading freezes
  3. Penrose collapse scaling:  Zeno timescale ~ 1/(G * N^2 * m^2)?
  4. Diosi-Penrose decoherence: Gamma ~ G * N^2 * m^2 / d?

On 2D staggered lattice, side=10, MASS=0.30, MU2=0.001 (unscreened), DT=0.12.

PStack experiment: hartree-n-body
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.001        # unscreened!
DT = 0.12
N_STEPS = 40
SIDE = 10
SIGMA = 1.5         # Gaussian width in lattice units
G_BASE = 1.0        # base gravitational coupling

N_VALUES = [1, 5, 10, 20, 50, 100]


# ---------------------------------------------------------------------------
# 2D periodic lattice
# ---------------------------------------------------------------------------
def build_lattice(side: int):
    """Build 2D periodic square lattice.

    Returns pos, col (parity), adj (dict), Laplacian (sparse), n_sites.
    """
    pos = [(x, y) for x in range(side) for y in range(side)]
    n = len(pos)
    col = np.array([(x + y) % 2 for x, y in pos], dtype=float)

    idx = {}
    for i, (x, y) in enumerate(pos):
        idx[(x, y)] = i

    adj = {}
    for i, (x, y) in enumerate(pos):
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = (x + dx) % side, (y + dy) % side
            neighbors.append(idx[(nx, ny)])
        adj[i] = neighbors

    # Laplacian
    rows, cols_arr, vals = [], [], []
    for i in range(n):
        nbrs = adj[i]
        rows.append(i); cols_arr.append(i); vals.append(-float(len(nbrs)))
        for j in nbrs:
            rows.append(i); cols_arr.append(j); vals.append(1.0)
    L = sparse.csc_matrix((vals, (rows, cols_arr)), shape=(n, n))

    return pos, col, adj, L, n


# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------
def solve_phi(rho: np.ndarray, L: sparse.csc_matrix, mu2: float,
              G_eff: float, n: int) -> np.ndarray:
    """Screened Poisson: (L + mu^2 I) phi = G_eff * rho."""
    A = (L + mu2 * sparse.eye(n)).tocsc()
    return spsolve(A, G_eff * rho)


def build_hamiltonian(col, adj, n, phi, mass):
    """Staggered 2D Hamiltonian with parity coupling.

    H_diag = (mass + phi) * epsilon,  epsilon = (-1)^(x+y)
    H_hop = antisymmetric nearest-neighbor hopping
    """
    par = np.where(col == 0, 1.0, -1.0)
    diag = (mass + phi) * par

    rows, cols_arr, vals = [], [], []
    for i in range(n):
        rows.append(i); cols_arr.append(i); vals.append(diag[i])

    for i in range(n):
        for j in adj[i]:
            if j > i:
                rows.append(i); cols_arr.append(j); vals.append(-0.5j)
                rows.append(j); cols_arr.append(i); vals.append(0.5j)

    return sparse.csc_matrix((vals, (rows, cols_arr)), shape=(n, n), dtype=complex)


def cn_step(H, psi, dt, n):
    """Crank-Nicolson step."""
    I = sparse.eye(n, dtype=complex, format="csc")
    A_plus = (I + 1j * H * dt / 2).tocsc()
    A_minus = I - 1j * H * dt / 2
    return spsolve(A_plus, A_minus.dot(psi))


# ---------------------------------------------------------------------------
# Wavepacket utilities
# ---------------------------------------------------------------------------
def gaussian_2d(cx, cy, sigma, pos, n):
    """Normalized 2D Gaussian."""
    psi = np.zeros(n, dtype=complex)
    for i, (x, y) in enumerate(pos):
        psi[i] = np.exp(-0.5 * ((x - cx)**2 + (y - cy)**2) / sigma**2)
    norm = np.sqrt(np.sum(np.abs(psi)**2))
    return psi / norm


def rms_width(psi, pos, n):
    """RMS width of wavepacket."""
    prob = np.abs(psi)**2
    prob /= np.sum(prob)
    cx = sum(prob[i] * pos[i][0] for i in range(n))
    cy = sum(prob[i] * pos[i][1] for i in range(n))
    r2 = sum(prob[i] * ((pos[i][0] - cx)**2 + (pos[i][1] - cy)**2)
             for i in range(n))
    return np.sqrt(r2)


# ---------------------------------------------------------------------------
# Part 1: Self-gravity contraction vs N
# ---------------------------------------------------------------------------
def run_contraction(N_particle, pos, col, adj, L, n, psi0, w0):
    """Evolve single wavefunction with rho = N * |psi|^2.

    G_eff = G_BASE * N  (the Hartree trick: effective gravitational mass = N*m).
    Returns final width and width trajectory.
    """
    G_eff = G_BASE * N_particle
    psi = psi0.copy()
    widths = [w0]

    for step in range(N_STEPS):
        rho = N_particle * np.abs(psi)**2   # Hartree source: N * |psi|^2
        phi = solve_phi(rho, L, MU2, G_BASE, n)  # G_BASE * (N * |psi|^2)
        H = build_hamiltonian(col, adj, n, phi, MASS)
        psi = cn_step(H, psi, DT, n)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
        widths.append(rms_width(psi, pos, n))

    return np.array(widths)


# ---------------------------------------------------------------------------
# Part 2: Zeno threshold scan
# ---------------------------------------------------------------------------
def find_zeno_threshold(N_particle, pos, col, adj, L, n, psi0, w0):
    """Binary search for G_eff where spreading freezes.

    Returns G_Zeno such that w_final / w_init < 1.05.
    """
    # Coarse scan first
    G_test_values = [0.1, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500]
    spread_ratios = []

    for G_mult in G_test_values:
        G_eff = G_mult * N_particle
        psi = psi0.copy()
        for step in range(N_STEPS):
            rho = N_particle * np.abs(psi)**2
            phi = solve_phi(rho, L, MU2, G_mult, n)
            H = build_hamiltonian(col, adj, n, phi, MASS)
            psi = cn_step(H, psi, DT, n)
            psi /= np.sqrt(np.sum(np.abs(psi)**2))
        w_final = rms_width(psi, pos, n)
        ratio = w_final / w0
        spread_ratios.append(ratio)

    # Find crossover
    for i in range(len(spread_ratios)):
        if spread_ratios[i] < 1.05:
            if i == 0:
                return G_test_values[0], spread_ratios[0]
            # Interpolate in log space
            g_lo = G_test_values[i - 1]
            g_hi = G_test_values[i]
            r_lo = spread_ratios[i - 1]
            r_hi = spread_ratios[i]
            if abs(r_lo - r_hi) < 1e-12:
                return g_lo, r_lo
            frac = (1.05 - r_lo) / (r_hi - r_lo)
            if g_lo > 0 and g_hi > 0:
                g_crit = np.exp(np.log(g_lo) + frac * (np.log(g_hi) - np.log(g_lo)))
            else:
                g_crit = g_lo + frac * (g_hi - g_lo)
            return g_crit, 1.05

    return float("inf"), spread_ratios[-1] if spread_ratios else float("nan")


# ---------------------------------------------------------------------------
# Part 3: Zeno timescale vs N
# ---------------------------------------------------------------------------
def measure_zeno_timescale(N_particle, G_mult, pos, col, adj, L, n, psi0, w0):
    """Measure time at which width first exceeds w0 * 1.1 (or N_STEPS if frozen).

    Returns timescale in lattice-time units.
    """
    psi = psi0.copy()
    threshold = w0 * 1.10

    for step in range(N_STEPS):
        rho = N_particle * np.abs(psi)**2
        phi = solve_phi(rho, L, MU2, G_mult, n)
        H = build_hamiltonian(col, adj, n, phi, MASS)
        psi = cn_step(H, psi, DT, n)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
        w = rms_width(psi, pos, n)
        if w > threshold:
            return (step + 1) * DT

    return N_STEPS * DT  # fully frozen


# ---------------------------------------------------------------------------
# Part 4: Decoherence rate (Diosi-Penrose)
# ---------------------------------------------------------------------------
def measure_coherence(psi, psi_L, psi_R):
    """Coherence C = |<psi_L|psi><psi|psi_R>|."""
    return np.abs(np.vdot(psi_L, psi) * np.vdot(psi, psi_R))


def run_decoherence(N_particle, separation, pos, col, adj, L, n):
    """Evolve superposition under Hartree self-gravity.

    rho = N * |psi|^2 sources the gravitational field.
    Returns coherence time series.
    """
    cy = SIDE / 2.0
    cx_L = SIDE / 2.0 - separation / 2.0
    cx_R = SIDE / 2.0 + separation / 2.0

    psi_L = gaussian_2d(cx_L, cy, SIGMA, pos, n)
    psi_R = gaussian_2d(cx_R, cy, SIGMA, pos, n)
    psi = (psi_L + psi_R) / np.sqrt(2)
    psi /= np.sqrt(np.sum(np.abs(psi)**2))

    coherence = np.zeros(N_STEPS + 1)
    coherence[0] = measure_coherence(psi, psi_L, psi_R)

    for step in range(N_STEPS):
        rho = N_particle * np.abs(psi)**2
        phi = solve_phi(rho, L, MU2, G_BASE, n)
        H = build_hamiltonian(col, adj, n, phi, MASS)
        psi = cn_step(H, psi, DT, n)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
        coherence[step + 1] = measure_coherence(psi, psi_L, psi_R)

    return coherence


def fit_gamma(coherence, dt):
    """Fit C(t) = C(0)*exp(-Gamma*t). Return Gamma."""
    c0 = coherence[0]
    if c0 < 1e-30:
        return 0.0

    valid = []
    for i, c in enumerate(coherence):
        if c > 1e-20 and c / c0 > 1e-10:
            valid.append((i * dt, np.log(c / c0)))

    if len(valid) < 3:
        return 0.0

    times = np.array([v[0] for v in valid])
    log_ratio = np.array([v[1] for v in valid])
    coeffs = np.polyfit(times, log_ratio, 1)
    return -coeffs[0]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 76)
    print("FRONTIER: Hartree N-Body Limit -- Semiclassical Gravity")
    print("=" * 76)
    print(f"  MASS={MASS}, MU2={MU2} (unscreened!), DT={DT}, N_STEPS={N_STEPS}")
    print(f"  SIDE={SIDE} (n={SIDE**2}), SIGMA={SIGMA}, G_BASE={G_BASE}")
    print(f"  Hartree trick: rho = N * |psi|^2, G_eff = G_BASE * N")
    print(f"  N values: {N_VALUES}")
    print()

    # Build lattice once
    pos, col, adj, L, n = build_lattice(SIDE)
    center = (SIDE / 2.0, SIDE / 2.0)
    psi0 = gaussian_2d(center[0], center[1], SIGMA, pos, n)
    w0 = rms_width(psi0, pos, n)
    print(f"  Initial wavepacket width: {w0:.4f}")
    print()

    # ==================================================================
    # Part 1: Self-gravity contraction
    # ==================================================================
    print("=" * 76)
    print("PART 1: Self-Gravity Contraction  (w_grav / w_free  vs  N)")
    print("=" * 76)
    print()

    # Free evolution (N=0, no gravity)
    w_free_traj = run_contraction(0, pos, col, adj, L, n, psi0, w0)
    w_free = w_free_traj[-1]
    print(f"  Free evolution: w_init={w0:.4f}, w_final={w_free:.4f}, "
          f"ratio={w_free / w0:.4f}")
    print()

    print(f"{'N':>6s}  {'G_eff':>8s}  {'w_final':>10s}  {'w/w_free':>10s}  "
          f"{'w/w_init':>10s}  {'status':>10s}")
    print("-" * 66)

    contraction_ratios = {}
    for N_p in N_VALUES:
        w_traj = run_contraction(N_p, pos, col, adj, L, n, psi0, w0)
        w_f = w_traj[-1]
        ratio_free = w_f / w_free if w_free > 0 else float("inf")
        ratio_init = w_f / w0
        contraction_ratios[N_p] = ratio_free
        status = ("CONTRACT" if ratio_free < 0.95
                  else ("FROZEN" if ratio_free < 1.05 else "SPREAD"))
        print(f"{N_p:>6d}  {G_BASE * N_p:>8.1f}  {w_f:>10.4f}  "
              f"{ratio_free:>10.4f}  {ratio_init:>10.4f}  {status:>10s}")

    print()

    # ==================================================================
    # Part 2: Zeno threshold
    # ==================================================================
    print("=" * 76)
    print("PART 2: Quantum Zeno Threshold  (G_Zeno  vs  N)")
    print("  Find G_mult where spreading freezes (w_final / w_init < 1.05)")
    print("=" * 76)
    print()

    print(f"{'N':>6s}  {'G_Zeno':>10s}  {'G_eff=G*N':>12s}")
    print("-" * 34)

    g_zenos = {}
    for N_p in N_VALUES:
        g_z, _ = find_zeno_threshold(N_p, pos, col, adj, L, n, psi0, w0)
        g_zenos[N_p] = g_z
        g_eff = g_z * N_p if g_z < float("inf") else float("inf")
        print(f"{N_p:>6d}  {g_z:>10.2f}  {g_eff:>12.2f}")

    print()

    # Fit: G_Zeno vs N
    valid_gz = [(N_p, g_zenos[N_p]) for N_p in N_VALUES
                if g_zenos[N_p] < float("inf") and g_zenos[N_p] > 0]
    if len(valid_gz) >= 2:
        log_n = np.log([v[0] for v in valid_gz])
        log_gz = np.log([v[1] for v in valid_gz])
        slope_gz = np.polyfit(log_n, log_gz, 1)[0]
        print(f"  Power-law fit: G_Zeno ~ N^{slope_gz:.3f}")
        print(f"  (Penrose prediction: if Zeno from self-gravity, G_Zeno ~ 1/N)")
        print(f"  (because G_eff = G*N -> threshold G_eff constant -> G_Zeno ~ 1/N, slope=-1)")
    print()

    # ==================================================================
    # Part 3: Zeno timescale vs N^2
    # ==================================================================
    print("=" * 76)
    print("PART 3: Zeno Timescale  (does t_Zeno ~ 1/(G*N^2*m^2)?)")
    print("  At fixed G_mult=10, measure time for width to exceed 1.1*w0")
    print("=" * 76)
    print()

    G_FIXED = 10.0

    print(f"{'N':>6s}  {'G_eff':>8s}  {'t_Zeno':>10s}  {'1/(G*N^2*m^2)':>16s}  {'ratio':>10s}")
    print("-" * 58)

    zeno_times = {}
    for N_p in N_VALUES:
        t_z = measure_zeno_timescale(N_p, G_FIXED, pos, col, adj, L, n, psi0, w0)
        zeno_times[N_p] = t_z
        penrose_scale = 1.0 / (G_FIXED * N_p**2 * MASS**2) if N_p > 0 else float("inf")
        ratio = t_z / penrose_scale if penrose_scale > 0 and penrose_scale < 1e10 else float("nan")
        print(f"{N_p:>6d}  {G_FIXED * N_p:>8.1f}  {t_z:>10.4f}  "
              f"{penrose_scale:>16.6f}  {ratio:>10.4f}")

    print()

    # Fit: t_Zeno vs N
    valid_tz = [(N_p, zeno_times[N_p]) for N_p in N_VALUES
                if zeno_times[N_p] > 0 and zeno_times[N_p] < N_STEPS * DT * 0.99]
    if len(valid_tz) >= 2:
        log_n = np.log([v[0] for v in valid_tz])
        log_tz = np.log([v[1] for v in valid_tz])
        slope_tz = np.polyfit(log_n, log_tz, 1)[0]
        print(f"  Power-law fit: t_Zeno ~ N^{slope_tz:.3f}")
        print(f"  Penrose prediction: t_Zeno ~ 1/(G*N^2*m^2) => slope = -2.0")
    else:
        slope_tz = float("nan")
        print("  Insufficient variation for t_Zeno fit (all frozen or all spreading)")
    print()

    # ==================================================================
    # Part 4: Diosi-Penrose decoherence rate
    # ==================================================================
    print("=" * 76)
    print("PART 4: Diosi-Penrose Decoherence  (Gamma ~ G*N^2*m^2/d?)")
    print("  Superposition of two Gaussians, separation d=4")
    print("=" * 76)
    print()

    SEP = 4  # separation in lattice units

    print(f"{'N':>6s}  {'G_eff':>8s}  {'Gamma':>14s}  {'Gamma_DP':>14s}  "
          f"{'ratio':>10s}  {'C(0)':>8s}  {'C(end)':>8s}")
    print("-" * 76)

    gammas = {}
    for N_p in N_VALUES:
        coh = run_decoherence(N_p, SEP, pos, col, adj, L, n)
        gamma = fit_gamma(coh, DT)
        gammas[N_p] = gamma
        # DP prediction: Gamma_DP = G * (N*m)^2 / d = G * N^2 * m^2 / d
        gamma_dp = G_BASE * N_p**2 * MASS**2 / SEP
        ratio = gamma / gamma_dp if gamma_dp > 0 else float("inf")
        print(f"{N_p:>6d}  {G_BASE * N_p:>8.1f}  {gamma:>14.6e}  "
              f"{gamma_dp:>14.6e}  {ratio:>10.4f}  "
              f"{coh[0]:>8.5f}  {coh[-1]:>8.5f}")

    print()

    # Fit Gamma vs N
    valid_gam = [(N_p, gammas[N_p]) for N_p in N_VALUES if gammas[N_p] > 1e-20]
    if len(valid_gam) >= 2:
        log_n = np.log([v[0] for v in valid_gam])
        log_gam = np.log([v[1] for v in valid_gam])
        slope_gam = np.polyfit(log_n, log_gam, 1)[0]
        print(f"  Power-law fit: Gamma ~ N^{slope_gam:.3f}")
        print(f"  DP prediction: Gamma ~ N^2.0  (from M = N*m, Gamma ~ G*M^2/d)")
    else:
        slope_gam = float("nan")
        print("  Insufficient decoherence data for fit")
    print()

    # Additional: sweep separation at fixed large N
    print("-" * 76)
    print(f"  Gamma vs separation d  (N=50, G_BASE={G_BASE})")
    print("-" * 76)
    N_TEST = 50
    d_values = [2, 3, 4, 6, 8]

    gammas_d = {}
    for d in d_values:
        if d >= SIDE - 2:
            continue
        coh = run_decoherence(N_TEST, d, pos, col, adj, L, n)
        gamma = fit_gamma(coh, DT)
        gammas_d[d] = gamma
        gamma_dp = G_BASE * N_TEST**2 * MASS**2 / d
        ratio = gamma / gamma_dp if gamma_dp > 0 else float("inf")
        print(f"  d={d:>2d}  Gamma={gamma:>14.6e}  Gamma_DP={gamma_dp:>14.6e}  "
              f"ratio={ratio:>10.4f}")

    valid_gd = [(d, gammas_d[d]) for d in gammas_d if gammas_d[d] > 1e-20]
    if len(valid_gd) >= 2:
        log_d = np.log([v[0] for v in valid_gd])
        log_gam = np.log([v[1] for v in valid_gd])
        slope_d = np.polyfit(log_d, log_gam, 1)[0]
        print(f"\n  Power-law fit: Gamma ~ d^{slope_d:.3f}  (DP predicts d^-1.0)")
    else:
        slope_d = float("nan")
    print()

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print("=" * 76)
    print("SUMMARY: Hartree N-Body -> Semiclassical Gravity")
    print("=" * 76)
    print()

    # Contraction
    print("1. Self-gravity contraction:")
    for N_p in N_VALUES:
        if N_p in contraction_ratios:
            print(f"     N={N_p:>3d}: w_grav/w_free = {contraction_ratios[N_p]:.4f}")

    # Zeno threshold
    print()
    print("2. Zeno threshold scaling:")
    if len(valid_gz) >= 2:
        print(f"     G_Zeno ~ N^{slope_gz:.3f}  (predict -1.0 for constant G_eff threshold)")
        if abs(slope_gz + 1.0) < 0.5:
            print("     CONSISTENT with Penrose self-gravity threshold")
        else:
            print("     DEVIATES from simple Penrose scaling")

    # Zeno timescale
    print()
    print("3. Zeno timescale:")
    if not np.isnan(slope_tz):
        print(f"     t_Zeno ~ N^{slope_tz:.3f}  (DP predicts -2.0)")
        if abs(slope_tz + 2.0) < 0.5:
            print("     MATCHES Penrose collapse timescale 1/(G*N^2*m^2)")
        else:
            print(f"     DEVIATES from 1/(G*N^2*m^2) prediction")
    else:
        print("     Insufficient data")

    # Decoherence
    print()
    print("4. Decoherence rate:")
    if not np.isnan(slope_gam):
        print(f"     Gamma ~ N^{slope_gam:.3f}  (DP predicts +2.0)")
        if abs(slope_gam - 2.0) < 0.5:
            print("     MATCHES Diosi-Penrose: Gamma ~ G*(N*m)^2/d")
        else:
            print(f"     DEVIATES from DP N^2 scaling")
    else:
        print("     Insufficient data")

    if not np.isnan(slope_d):
        print(f"     Gamma ~ d^{slope_d:.3f}  (DP predicts -1.0)")

    # Overall verdict
    print()
    print("-" * 76)
    checks_passed = 0
    checks_total = 0

    if len(valid_gz) >= 2:
        checks_total += 1
        if abs(slope_gz + 1.0) < 0.5:
            checks_passed += 1

    if not np.isnan(slope_tz):
        checks_total += 1
        if abs(slope_tz + 2.0) < 0.5:
            checks_passed += 1

    if not np.isnan(slope_gam):
        checks_total += 1
        if abs(slope_gam - 2.0) < 0.5:
            checks_passed += 1

    if not np.isnan(slope_d):
        checks_total += 1
        if abs(slope_d + 1.0) < 0.5:
            checks_passed += 1

    print(f"  Semiclassical gravity checks: {checks_passed}/{checks_total} passed")
    if checks_total > 0 and checks_passed >= checks_total * 0.75:
        print("  VERDICT: Hartree N-body limit RECOVERS semiclassical gravity")
        print("           at large N. Penrose collapse and DP decoherence emerge.")
    elif checks_total > 0 and checks_passed >= checks_total * 0.5:
        print("  VERDICT: PARTIAL recovery of semiclassical gravity.")
        print("           Some scaling exponents deviate from GR predictions.")
    else:
        print("  VERDICT: Hartree limit does NOT reproduce semiclassical gravity")
        print("           in the tested parameter regime.")

    print()
    print("=" * 76)
    print("DONE")
    print("=" * 76)


if __name__ == "__main__":
    main()
