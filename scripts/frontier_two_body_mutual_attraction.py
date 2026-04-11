#!/usr/bin/env python3
"""
Historical single-wavefunction two-lobe probe.
==============================================

Important guardrail:
  this is NOT a genuine two-body experiment. It evolves one normalized
  wavefunction with two lobes and infers 'body' motion from a left/right split,
  so any separation signal is contaminated by self-focusing and intra-state
  interference.

It is kept only as a historical control / negative surface. Use the later
two-orbital and Wilson two-body harnesses for actual mutual-channel tests.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve

# ── Physical parameters ────────────────────────────────────────────
MASS = 0.30
MU2 = 0.02         # low screening -> long-range potential (1/sqrt(mu2) ~ 7)
DT = 0.12
SIDE = 20          # large enough for open-boundary lattice
N_STEPS = 100      # longer evolution for slow gravitational drift
SIGMA = 1.5        # slightly wider packets for more overlap
G_DEFAULT = 100.0  # strong coupling
N_ANDERSON_SEEDS = 5


# ── Lattice ────────────────────────────────────────────────────────

def build_lattice(side: int, periodic: bool = False):
    """2D square lattice with checkerboard parity.

    periodic=False uses open boundaries to avoid wrap-around force cancellation.
    """
    n = side * side
    pos = np.zeros((n, 2))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    col = np.zeros(n, dtype=int)

    for ix in range(side):
        for iy in range(side):
            idx = ix * side + iy
            pos[idx] = (ix, iy)
            col[idx] = (ix + iy) % 2
            for dix, diy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = ix + dix
                jy = iy + diy
                if periodic:
                    jx = jx % side
                    jy = jy % side
                elif not (0 <= jx < side and 0 <= jy < side):
                    continue
                adj[idx].append(jx * side + jy)

    return n, pos, adj, col


def build_laplacian(adj: dict[int, list[int]], n: int):
    """Graph Laplacian (unit weights for regular lattice)."""
    L = lil_matrix((n, n), dtype=float)
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            L[i, j] -= 1.0
            L[j, i] -= 1.0
            L[i, i] += 1.0
            L[j, j] += 1.0
    return L.tocsr()


# ── Hamiltonian and evolution ──────────────────────────────────────

def build_hamiltonian(pos, col, adj, n, phi):
    """Staggered-fermion Hamiltonian with parity coupling."""
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)

    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            d = min(d, 2.0)  # periodic wrap protection
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


def cn_step(psi, H, n):
    """Crank-Nicolson time step."""
    ap = (speye(n, format='csc') + 1j * H * DT / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * DT / 2
    return spsolve(ap, am.dot(psi))


def solve_phi(L, n, rho):
    """Screened Poisson: (L + mu^2 I) Phi = G * rho."""
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + MU2 * speye(n, format='csr')).tocsc()
    return spsolve(A, rho)


# ── Wavepacket initialization ─────────────────────────────────────

def two_gaussians(pos, n, cx_a, cy_a, cx_b, cy_b, sigma, amp_ratio=1.0):
    """Two Gaussians on the lattice. amp_ratio scales packet B."""
    dx_a = pos[:, 0] - cx_a
    dy_a = pos[:, 1] - cy_a
    ga = np.exp(-0.5 * (dx_a**2 + dy_a**2) / sigma**2)

    dx_b = pos[:, 0] - cx_b
    dy_b = pos[:, 1] - cy_b
    gb = amp_ratio * np.exp(-0.5 * (dx_b**2 + dy_b**2) / sigma**2)

    psi = (ga + gb).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


# ── Centroid tracking ──────────────────────────────────────────────

def track_centroids(pos, psi, side):
    """Track left and right packet centroids using x < side/2 split.

    Returns (cx_left, cx_right, separation).
    Uses periodic-aware centroid computation.
    """
    rho = np.abs(psi)**2
    half = side / 2.0

    left_mask = pos[:, 0] < half
    right_mask = ~left_mask

    rho_l = rho * left_mask
    rho_r = rho * right_mask
    sum_l = np.sum(rho_l)
    sum_r = np.sum(rho_r)

    if sum_l > 1e-10:
        cx_l = np.sum(rho_l * pos[:, 0]) / sum_l
    else:
        cx_l = np.nan

    if sum_r > 1e-10:
        cx_r = np.sum(rho_r * pos[:, 0]) / sum_r
    else:
        cx_r = np.nan

    sep = cx_r - cx_l if not (np.isnan(cx_l) or np.isnan(cx_r)) else np.nan
    return cx_l, cx_r, sep


# ── Evolution modes ────────────────────────────────────────────────

def evolve_self_gravity(pos, col, adj, n, L_mat, psi0, G, n_steps):
    """Self-consistent gravity: Phi updated each step from current rho."""
    psi = psi0.copy()
    seps = []
    norms = []

    for step in range(n_steps):
        rho = np.abs(psi)**2
        phi = solve_phi(L_mat, n, G * rho)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(psi, H, n)

        _, _, sep = track_centroids(pos, psi, SIDE)
        seps.append(sep)
        norms.append(float(np.linalg.norm(psi)))

    return np.array(seps), np.array(norms)


def evolve_free(pos, col, adj, n, psi0, n_steps):
    """Free evolution: G=0, no potential."""
    phi_zero = np.zeros(n)
    H = build_hamiltonian(pos, col, adj, n, phi_zero)
    psi = psi0.copy()
    seps = []

    for step in range(n_steps):
        psi = cn_step(psi, H, n)
        _, _, sep = track_centroids(pos, psi, SIDE)
        seps.append(sep)

    return np.array(seps)


def evolve_frozen(pos, col, adj, n, L_mat, psi0, G, n_steps):
    """Frozen potential: Phi from initial rho, held fixed."""
    rho0 = np.abs(psi0)**2
    phi_frozen = solve_phi(L_mat, n, G * rho0)
    H = build_hamiltonian(pos, col, adj, n, phi_frozen)
    psi = psi0.copy()
    seps = []

    for step in range(n_steps):
        psi = cn_step(psi, H, n)
        _, _, sep = track_centroids(pos, psi, SIDE)
        seps.append(sep)

    return np.array(seps)


def evolve_anderson(pos, col, adj, n, L_mat, psi0, G, n_steps, seed):
    """Anderson control: random positive potential with matched statistics."""
    # First compute self-consistent Phi to match its statistics
    rho0 = np.abs(psi0)**2
    phi_ref = solve_phi(L_mat, n, G * rho0)
    phi_mean = np.mean(phi_ref)
    phi_std = np.std(phi_ref)

    rng = np.random.RandomState(seed)
    # Random positive potential with matched mean and std
    phi_rand = np.abs(rng.normal(phi_mean, max(phi_std, 1e-6), n))

    H = build_hamiltonian(pos, col, adj, n, phi_rand)
    psi = psi0.copy()
    seps = []

    for step in range(n_steps):
        psi = cn_step(psi, H, n)
        _, _, sep = track_centroids(pos, psi, SIDE)
        seps.append(sep)

    return np.array(seps)


# ── Analysis ───────────────────────────────────────────────────────

def separation_change(seps):
    """Net change in separation: final - initial. Negative = attraction."""
    valid = seps[np.isfinite(seps)]
    if len(valid) < 2:
        return np.nan
    return valid[-1] - valid[0]


def monotonic_decrease_fraction(seps):
    """Fraction of steps where separation decreased."""
    valid = seps[np.isfinite(seps)]
    if len(valid) < 2:
        return np.nan
    diffs = np.diff(valid)
    return np.sum(diffs < 0) / len(diffs)


# ── Main experiment ────────────────────────────────────────────────

def main():
    t0 = time.time()

    print("=" * 76)
    print("TWO-BODY MUTUAL ATTRACTION VIA SELF-CONSISTENT GRAVITY")
    print("=" * 76)
    print()
    print(f"Lattice: {SIDE}x{SIDE} open-boundary staggered ({SIDE*SIDE} nodes)")
    print(f"Physics: MASS={MASS}, MU2={MU2}, DT={DT}")
    print(f"Packets: sigma={SIGMA}, N_STEPS={N_STEPS}")
    print(f"Anderson seeds: {N_ANDERSON_SEEDS}")
    print()

    # Build lattice (open boundaries to avoid periodic force cancellation)
    n, pos, adj, col = build_lattice(SIDE, periodic=False)
    L_mat = build_laplacian(adj, n)
    print(f"Boundary: open (non-periodic)")

    # ================================================================
    # PART 0: Sanity check -- single packet self-contraction
    # ================================================================
    print("=" * 76)
    print("PART 0: SANITY CHECK -- single packet self-contraction")
    print("=" * 76)
    print()

    cx_single = SIDE / 2.0
    cy_single = SIDE / 2.0
    # Single Gaussian at center
    dx_s = pos[:, 0] - cx_single
    dy_s = pos[:, 1] - cy_single
    psi_single = np.exp(-0.5 * (dx_s**2 + dy_s**2) / SIGMA**2).astype(complex)
    psi_single /= np.linalg.norm(psi_single)

    # Measure width under free vs self-gravity
    psi_f = psi_single.copy()
    psi_g = psi_single.copy()
    phi_zero = np.zeros(n)
    H_free_single = build_hamiltonian(pos, col, adj, n, phi_zero)

    widths_free_s = []
    widths_grav_s = []
    for step in range(40):
        # Width
        rho_f = np.abs(psi_f)**2
        rho_f /= np.sum(rho_f)
        cx_f = np.sum(rho_f * pos[:, 0])
        cy_f = np.sum(rho_f * pos[:, 1])
        w_f = np.sqrt(np.sum(rho_f * ((pos[:, 0] - cx_f)**2 + (pos[:, 1] - cy_f)**2)))
        widths_free_s.append(w_f)

        rho_g = np.abs(psi_g)**2
        rho_g /= np.sum(rho_g)
        cx_g = np.sum(rho_g * pos[:, 0])
        cy_g = np.sum(rho_g * pos[:, 1])
        w_g = np.sqrt(np.sum(rho_g * ((pos[:, 0] - cx_g)**2 + (pos[:, 1] - cy_g)**2)))
        widths_grav_s.append(w_g)

        # Free step
        psi_f = cn_step(psi_f, H_free_single, n)

        # Self-gravity step
        rho_sg = np.abs(psi_g)**2
        phi_sg = solve_phi(L_mat, n, G_DEFAULT * rho_sg)
        H_sg = build_hamiltonian(pos, col, adj, n, phi_sg)
        psi_g = cn_step(psi_g, H_sg, n)

    ratio_final = widths_grav_s[-1] / widths_free_s[-1]
    print(f"Single-packet widths after 40 steps:")
    print(f"  Free:         {widths_free_s[0]:.4f} -> {widths_free_s[-1]:.4f}")
    print(f"  Self-gravity: {widths_grav_s[0]:.4f} -> {widths_grav_s[-1]:.4f}")
    print(f"  Ratio (grav/free): {ratio_final:.4f}")
    print(f"  Self-contraction works: {ratio_final < 1.0}")
    print()

    # Phi diagnostic: show the potential profile
    rho_diag = np.abs(psi_single)**2
    phi_diag = solve_phi(L_mat, n, G_DEFAULT * rho_diag)
    print(f"Phi diagnostic (initial single packet at center):")
    print(f"  max(Phi) = {np.max(phi_diag):.6f}")
    print(f"  min(Phi) = {np.min(phi_diag):.6f}")
    print(f"  mean(Phi) = {np.mean(phi_diag):.6f}")
    print(f"  std(Phi) = {np.std(phi_diag):.6f}")
    print(f"  Phi contrast (max-min)/mean: {(np.max(phi_diag)-np.min(phi_diag))/max(np.mean(phi_diag),1e-10):.4f}")
    print()

    # ================================================================
    # PART 1: Main control comparison (G=80, d=7)
    # ================================================================
    print("=" * 76)
    print("PART 1: CONTROL COMPARISON (G={}, d=7)".format(G_DEFAULT))
    print("=" * 76)
    print()

    cx_a, cy_a = 7.0, 10.0
    cx_b, cy_b = 13.0, 10.0   # separation = 6 on side=20 lattice
    G = G_DEFAULT

    psi0 = two_gaussians(pos, n, cx_a, cy_a, cx_b, cy_b, SIGMA)

    # Initial separation
    _, _, sep0 = track_centroids(pos, psi0, SIDE)
    print(f"Initial separation: {sep0:.4f}")
    print()

    # A. Free
    print("Running FREE (G=0)...")
    seps_free = evolve_free(pos, col, adj, n, psi0, N_STEPS)

    # B. Frozen
    print(f"Running FROZEN (G={G}, Phi fixed at t=0)...")
    seps_frozen = evolve_frozen(pos, col, adj, n, L_mat, psi0, G, N_STEPS)

    # C. Anderson (multiple seeds)
    print(f"Running ANDERSON ({N_ANDERSON_SEEDS} seeds)...")
    anderson_changes = []
    anderson_mono = []
    seps_anderson_all = []
    for seed in range(N_ANDERSON_SEEDS):
        seps_a = evolve_anderson(pos, col, adj, n, L_mat, psi0, G, N_STEPS, seed)
        anderson_changes.append(separation_change(seps_a))
        anderson_mono.append(monotonic_decrease_fraction(seps_a))
        seps_anderson_all.append(seps_a)

    # D. Self-gravity
    print(f"Running SELF-GRAVITY (G={G})...")
    seps_grav, norms_grav = evolve_self_gravity(pos, col, adj, n, L_mat, psi0, G, N_STEPS)

    # Report
    print()
    print(f"{'Mode':<16} | {'Delta sep':>12} | {'Mono frac':>10} | {'Final sep':>10}")
    print("-" * 60)

    dc_free = separation_change(seps_free)
    mf_free = monotonic_decrease_fraction(seps_free)
    print(f"{'FREE':<16} | {dc_free:>+12.6f} | {mf_free:>10.3f} | {seps_free[-1]:>10.4f}")

    dc_frozen = separation_change(seps_frozen)
    mf_frozen = monotonic_decrease_fraction(seps_frozen)
    print(f"{'FROZEN':<16} | {dc_frozen:>+12.6f} | {mf_frozen:>10.3f} | {seps_frozen[-1]:>10.4f}")

    ac_mean = np.mean(anderson_changes)
    ac_std = np.std(anderson_changes)
    am_mean = np.mean(anderson_mono)
    print(f"{'ANDERSON (mean)':<16} | {ac_mean:>+12.6f} | {am_mean:>10.3f} | {'':>10}")
    print(f"{'ANDERSON (std)':<16} | {ac_std:>12.6f} | {'':>10} | {'':>10}")

    dc_grav = separation_change(seps_grav)
    mf_grav = monotonic_decrease_fraction(seps_grav)
    print(f"{'SELF-GRAVITY':<16} | {dc_grav:>+12.6f} | {mf_grav:>10.3f} | {seps_grav[-1]:>10.4f}")

    # Norm check
    norm_drift = np.max(np.abs(norms_grav - 1.0))
    print(f"\nNorm conservation: max drift = {norm_drift:.2e}")

    # Separation time series (sampled)
    print()
    print("Separation time series (every 10 steps):")
    print(f"{'Step':>6} | {'FREE':>10} | {'FROZEN':>10} | {'GRAVITY':>10}")
    print("-" * 48)
    for i in range(0, N_STEPS, 10):
        print(f"{i:>6} | {seps_free[i]:>10.4f} | {seps_frozen[i]:>10.4f} | {seps_grav[i]:>10.4f}")
    print(f"{N_STEPS-1:>6} | {seps_free[-1]:>10.4f} | {seps_frozen[-1]:>10.4f} | {seps_grav[-1]:>10.4f}")

    # ================================================================
    # PART 2: G sweep (G = 10, 20, 50, 100)
    # ================================================================
    print()
    print("=" * 76)
    print("PART 2: G SWEEP (does approach rate increase with G?)")
    print("=" * 76)
    print()

    g_values = [10, 20, 50, 100]
    print(f"{'G':>6} | {'Delta sep':>12} | {'Mono frac':>10} | {'Approach?':>10}")
    print("-" * 48)

    g_deltas = []
    for g_val in g_values:
        seps_g, _ = evolve_self_gravity(pos, col, adj, n, L_mat, psi0, g_val, N_STEPS)
        dc = separation_change(seps_g)
        mf = monotonic_decrease_fraction(seps_g)
        approach = "YES" if dc < -0.01 else "no"
        print(f"{g_val:>6} | {dc:>+12.6f} | {mf:>10.3f} | {approach:>10}")
        g_deltas.append(dc)

    # Check monotonic increase in approach rate with G
    approach_increases = all(g_deltas[i] <= g_deltas[i-1]
                            for i in range(1, len(g_deltas))
                            if not np.isnan(g_deltas[i]))
    print(f"\nApproach rate monotonically increases with G: {approach_increases}")

    # ================================================================
    # PART 3: Separation sweep (d = 4, 6, 8, 10)
    # ================================================================
    print()
    print("=" * 76)
    print("PART 3: SEPARATION SWEEP (does approach rate decrease with d?)")
    print("=" * 76)
    print()

    d_values = [4, 6, 8, 10]
    print(f"{'d':>6} | {'Delta sep':>12} | {'Mono frac':>10}")
    print("-" * 36)

    d_deltas = []
    for d_val in d_values:
        cx_a_d = (SIDE / 2.0) - d_val / 2.0
        cx_b_d = (SIDE / 2.0) + d_val / 2.0
        cy_mid = SIDE / 2.0
        psi_d = two_gaussians(pos, n, cx_a_d, cy_mid, cx_b_d, cy_mid, SIGMA)
        seps_d, _ = evolve_self_gravity(pos, col, adj, n, L_mat, psi_d, G_DEFAULT, N_STEPS)
        dc = separation_change(seps_d)
        mf = monotonic_decrease_fraction(seps_d)
        print(f"{d_val:>6} | {dc:>+12.6f} | {mf:>10.3f}")
        d_deltas.append(dc)

    # Check: approach rate should decrease (become less negative) with distance
    # i.e. |delta| should decrease
    rate_decreases = all(abs(d_deltas[i]) <= abs(d_deltas[i-1])
                         for i in range(1, len(d_deltas))
                         if not (np.isnan(d_deltas[i]) or np.isnan(d_deltas[i-1])))
    print(f"\nApproach rate decreases with separation: {rate_decreases}")

    # ================================================================
    # PART 4: Mass ratio test
    # ================================================================
    print()
    print("=" * 76)
    print("PART 4: MASS RATIO (heavier packet attracts more?)")
    print("=" * 76)
    print()

    # Equal mass
    psi_eq = two_gaussians(pos, n, cx_a, cy_a, cx_b, cy_b, SIGMA, amp_ratio=1.0)
    seps_eq, _ = evolve_self_gravity(pos, col, adj, n, L_mat, psi_eq, G_DEFAULT, N_STEPS)

    # Packet B = 2x amplitude (heavier)
    psi_asym = two_gaussians(pos, n, cx_a, cy_a, cx_b, cy_b, SIGMA, amp_ratio=2.0)
    seps_asym, _ = evolve_self_gravity(pos, col, adj, n, L_mat, psi_asym, G_DEFAULT, N_STEPS)

    # Track individual centroids for asymmetric case
    psi_run = psi_asym.copy()
    cx_l_series = []
    cx_r_series = []
    for step in range(N_STEPS):
        rho = np.abs(psi_run)**2
        phi = solve_phi(L_mat, n, G_DEFAULT * rho)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi_run = cn_step(psi_run, H, n)
        cl, cr, _ = track_centroids(pos, psi_run, SIDE)
        cx_l_series.append(cl)
        cx_r_series.append(cr)

    cx_l_arr = np.array(cx_l_series)
    cx_r_arr = np.array(cx_r_series)

    dc_eq = separation_change(seps_eq)
    dc_asym = separation_change(seps_asym)

    print(f"Equal mass (1:1):   delta sep = {dc_eq:+.6f}")
    print(f"Unequal mass (1:2): delta sep = {dc_asym:+.6f}")
    print()

    # Light packet should move more toward heavy
    if len(cx_l_arr) > 1 and len(cx_r_arr) > 1:
        dl = cx_l_arr[-1] - cx_l_arr[0]  # light packet displacement
        dr = cx_r_arr[-1] - cx_r_arr[0]  # heavy packet displacement
        print(f"Light packet (A) centroid shift: {dl:+.4f}")
        print(f"Heavy packet (B) centroid shift: {dr:+.4f}")
        if not np.isnan(dl) and not np.isnan(dr):
            print(f"Light moves more: {abs(dl) > abs(dr)}")

    # ================================================================
    # VERDICT
    # ================================================================
    print()
    print("=" * 76)
    print("VERDICT")
    print("=" * 76)
    print()

    # --- Primary criterion: mutual attraction ---
    grav_attracts = dc_grav < -0.01
    print(f"PRIMARY: Mutual attraction (delta sep < -0.01): {grav_attracts}")
    print(f"  delta sep (gravity)  = {dc_grav:+.6f}")
    print(f"  delta sep (free)     = {dc_free:+.6f}")
    print(f"  delta sep (frozen)   = {dc_frozen:+.6f}")
    print(f"  delta sep (anderson) = {ac_mean:+.6f} +/- {ac_std:.6f}")
    print()

    # --- Confinement comparison ---
    # Self-gravity confines MUCH better than free (the known single-packet result)
    confinement_ratio = abs(dc_grav) / max(abs(dc_free), 1e-10)
    grav_confines = abs(dc_grav) < abs(dc_free) * 0.1
    grav_vs_frozen = abs(dc_grav - dc_frozen)
    print(f"CONFINEMENT: gravity vs free ratio: {confinement_ratio:.4f}")
    print(f"  Gravity confines better than free: {grav_confines}")
    print(f"  |gravity - frozen| = {grav_vs_frozen:.6f}")
    print(f"  Self-consistent vs frozen: {'indistinguishable' if grav_vs_frozen < 0.05 else 'different'}")
    print()

    # --- Self-consistency test: does dynamic Phi differ from static? ---
    grav_vs_frozen_sig = grav_vs_frozen / max(ac_std, 1e-6)
    print(f"Self-consistency signal (|grav - frozen| / anderson_std): {grav_vs_frozen_sig:.2f}")
    print()

    # Anderson control
    if ac_std > 0:
        anderson_exceeded = dc_grav < ac_mean - 2 * ac_std
    else:
        anderson_exceeded = dc_grav < ac_mean - 0.01

    # --- Sweep results ---
    g_monotonic = approach_increases
    d_monotonic = rate_decreases
    print(f"G sweep: approach rate increases with G: {g_monotonic}")
    print(f"d sweep: approach rate decreases with d: {d_monotonic}")
    print()

    # --- Score card ---
    criteria = [
        ("Mutual attraction (delta < -0.01)", grav_attracts),
        ("Gravity confines vs free (10x better)", grav_confines),
        ("Self-consistent differs from frozen", grav_vs_frozen > 0.05),
        ("Exceeds Anderson 2-sigma", anderson_exceeded),
        ("G-monotonic approach", g_monotonic),
        ("d-monotonic approach", d_monotonic),
    ]

    n_pass = sum(1 for _, v in criteria if v)
    for name, val in criteria:
        print(f"  [{('PASS' if val else 'FAIL'):>4}] {name}")

    print(f"\nSCORE: {n_pass}/{len(criteria)}")
    print()

    # --- Interpretation ---
    if grav_attracts and n_pass >= 4:
        print("STRONG EVIDENCE: Two-body mutual attraction from self-consistent gravity.")
        print("This is Newton's law emerging from the lattice.")
    elif grav_attracts:
        print("WEAK EVIDENCE: Attraction detected but controls not cleanly separated.")
    elif grav_confines and not grav_attracts:
        print("PARTIAL RESULT: Self-gravity confines individual packets (self-contraction)")
        print("but does NOT produce inter-packet attraction at this lattice size/coupling.")
        print()
        print("PHYSICS INTERPRETATION:")
        print("  The self-confining force (packet's own Phi on itself) dominates.")
        print("  The inter-packet force (A's Phi on B) is present but too weak")
        print("  relative to the self-confining force to produce visible centroid motion.")
        print(f"  Screening length 1/sqrt(mu2) = {1/np.sqrt(MU2):.1f} vs separation ~ {abs(cx_b-cx_a):.0f}")
        print("  The inter-packet potential is exponentially suppressed by screening.")
        print()
        print("  To see mutual attraction, would need:")
        print("  - Much lower mu2 (weaker screening, longer range)")
        print("  - Much longer evolution time")
        print("  - Or overlapping packets (but then 'two-body' is ill-defined)")
    else:
        print("NO EVIDENCE: Self-gravity produces no visible effect at these parameters.")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
