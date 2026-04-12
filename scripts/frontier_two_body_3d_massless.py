#!/usr/bin/env python3
"""
Two-Body Mutual Attraction: 3D Massless Field (mu=0)
=====================================================

The 2D two-body test failed because Yukawa screening (mu^2=0.22) killed
the inter-packet force at separation d=4. Two simultaneous fixes:

1. mu=0 (massless field): no Yukawa screening, pure 1/r potential in 3D
2. 3D lattice: Green's function is 1/r (not log(r) in 2D), giving 1/r^2 force

Protocol on 3D staggered cubic lattice (n=9, 729 nodes):
  1. Two Gaussians: A at (2,4,4), B at (6,4,4), sigma=1.0
  2. Self-consistent evolution with mu=0:
     Regularize: (L + eps*I) Phi = G*rho, then subtract mean(Phi)
  3. Track centroids of left (x<4.5) and right (x>=4.5) density

Controls:
  A. FREE (G=0)
  B. FROZEN (Phi from t=0 held fixed)
  C. ANDERSON (random positive potential, matched stats)
  D. SELF-GRAVITY mu=0 (the test)
  E. SELF-GRAVITY mu^2=0.22 (expect failure as in 2D)

Sweeps: G = [10, 50, 100] at d=4
Also: 2D side=12 with mu=0 for comparison
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve

# ── Physical parameters ────────────────────────────────────────────
MASS = 0.30
DT = 0.10           # smaller DT for 3D stability
N_STEPS = 40
SIGMA = 1.0
G_DEFAULT = 50.0
N_ANDERSON_SEEDS = 5
REG_EPS = 1e-4       # regularization for massless Laplacian

# 3D lattice
N_SIDE_3D = 9
N_3D = N_SIDE_3D ** 3  # 729

# 2D lattice for comparison
N_SIDE_2D = 12
N_2D = N_SIDE_2D ** 2  # 144


# ── 3D Lattice ────────────────────────────────────────────────────

def build_3d_lattice(n_side: int):
    """3D periodic cubic lattice with staggered parity."""
    n = n_side ** 3
    pos = np.zeros((n, 3))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    parity = np.zeros(n, dtype=int)

    for x in range(n_side):
        for y in range(n_side):
            for z in range(n_side):
                i = x * n_side * n_side + y * n_side + z
                pos[i] = (x, y, z)
                parity[i] = (x + y + z) % 2

                # x-neighbor (periodic)
                jx = ((x + 1) % n_side) * n_side * n_side + y * n_side + z
                adj[i].append(jx)
                # -x neighbor
                jx2 = ((x - 1) % n_side) * n_side * n_side + y * n_side + z
                adj[i].append(jx2)
                # y-neighbor
                jy = x * n_side * n_side + ((y + 1) % n_side) * n_side + z
                adj[i].append(jy)
                jy2 = x * n_side * n_side + ((y - 1) % n_side) * n_side + z
                adj[i].append(jy2)
                # z-neighbor
                jz = x * n_side * n_side + y * n_side + ((z + 1) % n_side)
                adj[i].append(jz)
                jz2 = x * n_side * n_side + y * n_side + ((z - 1) % n_side)
                adj[i].append(jz2)

    return n, pos, adj, parity


def build_2d_lattice(n_side: int):
    """2D periodic square lattice with checkerboard parity."""
    n = n_side * n_side
    pos = np.zeros((n, 2))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    parity = np.zeros(n, dtype=int)

    for x in range(n_side):
        for y in range(n_side):
            i = x * n_side + y
            pos[i] = (x, y)
            parity[i] = (x + y) % 2
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = (x + dx) % n_side
                jy = (y + dy) % n_side
                adj[i].append(jx * n_side + jy)

    return n, pos, adj, parity


# ── Graph Laplacian ───────────────────────────────────────────────

def build_laplacian(adj: dict[int, list[int]], n: int):
    """Graph Laplacian (unit weights)."""
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


# ── Hamiltonian ───────────────────────────────────────────────────

def build_hamiltonian_3d(pos, parity, adj, n, phi, n_side):
    """3D staggered-fermion Hamiltonian with parity coupling.

    Hopping with staggered phases eta_mu:
      x-direction: eta_1 = 1
      y-direction: eta_2 = (-1)^x
      z-direction: eta_3 = (-1)^(x+y)
    Mass + gravity: (MASS + phi) * epsilon, epsilon = (-1)^(x+y+z)
    """
    H = lil_matrix((n, n), dtype=complex)
    eps = np.where(parity == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * eps)

    for x in range(n_side):
        for y in range(n_side):
            for z in range(n_side):
                i = x * n_side * n_side + y * n_side + z

                # x-direction: eta_1 = 1
                j = ((x + 1) % n_side) * n_side * n_side + y * n_side + z
                H[i, j] += -1j / 2
                H[j, i] += 1j / 2

                # y-direction: eta_2 = (-1)^x
                e2 = (-1) ** x
                j = x * n_side * n_side + ((y + 1) % n_side) * n_side + z
                H[i, j] += e2 * (-1j / 2)
                H[j, i] += e2 * (1j / 2)

                # z-direction: eta_3 = (-1)^(x+y)
                e3 = (-1) ** (x + y)
                j = x * n_side * n_side + y * n_side + ((z + 1) % n_side)
                H[i, j] += e3 * (-1j / 2)
                H[j, i] += e3 * (1j / 2)

    return H.tocsc()


def build_hamiltonian_2d(pos, parity, adj, n, phi, n_side):
    """2D staggered-fermion Hamiltonian."""
    H = lil_matrix((n, n), dtype=complex)
    eps = np.where(parity == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * eps)

    for x in range(n_side):
        for y in range(n_side):
            i = x * n_side + y

            # x-direction: eta_1 = 1
            j = ((x + 1) % n_side) * n_side + y
            H[i, j] += -1j / 2
            H[j, i] += 1j / 2

            # y-direction: eta_2 = (-1)^x
            e2 = (-1) ** x
            j = x * n_side + ((y + 1) % n_side)
            H[i, j] += e2 * (-1j / 2)
            H[j, i] += e2 * (1j / 2)

    return H.tocsc()


# ── Solvers ───────────────────────────────────────────────────────

def cn_step(psi, H, n, dt):
    """Crank-Nicolson time step."""
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def solve_phi_massless(L, n, rho):
    """Massless Poisson: (L + eps*I) Phi = rho, then subtract mean."""
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + REG_EPS * speye(n, format='csr')).tocsc()
    phi = spsolve(A, rho)
    phi -= np.mean(phi)
    return phi


def solve_phi_screened(L, n, rho, mu2):
    """Screened Poisson: (L + mu2*I) Phi = rho."""
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + mu2 * speye(n, format='csr')).tocsc()
    return spsolve(A, rho)


# ── Wavepacket initialization ────────────────────────────────────

def two_gaussians_3d(pos, n, ca, cb, sigma):
    """Two 3D Gaussians. ca, cb are (x,y,z) centers."""
    ca = np.array(ca, dtype=float)
    cb = np.array(cb, dtype=float)
    da = np.sum((pos - ca) ** 2, axis=1)
    db = np.sum((pos - cb) ** 2, axis=1)
    ga = np.exp(-0.5 * da / sigma ** 2)
    gb = np.exp(-0.5 * db / sigma ** 2)
    psi = (ga + gb).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


def two_gaussians_2d(pos, n, ca, cb, sigma):
    """Two 2D Gaussians."""
    ca = np.array(ca, dtype=float)
    cb = np.array(cb, dtype=float)
    da = np.sum((pos - ca) ** 2, axis=1)
    db = np.sum((pos - cb) ** 2, axis=1)
    ga = np.exp(-0.5 * da / sigma ** 2)
    gb = np.exp(-0.5 * db / sigma ** 2)
    psi = (ga + gb).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


# ── Centroid tracking ─────────────────────────────────────────────

def track_centroids_x(pos_x, psi, x_split):
    """Track left and right centroids using x < x_split."""
    rho = np.abs(psi) ** 2
    left_mask = pos_x < x_split
    right_mask = ~left_mask

    rho_l = rho * left_mask
    rho_r = rho * right_mask
    sum_l = np.sum(rho_l)
    sum_r = np.sum(rho_r)

    cx_l = np.sum(rho_l * pos_x) / sum_l if sum_l > 1e-10 else np.nan
    cx_r = np.sum(rho_r * pos_x) / sum_r if sum_r > 1e-10 else np.nan

    sep = cx_r - cx_l if not (np.isnan(cx_l) or np.isnan(cx_r)) else np.nan
    return cx_l, cx_r, sep


# ── Evolution modes (3D) ─────────────────────────────────────────

def evolve_free_3d(pos, parity, adj, n, psi0, n_side, n_steps):
    """Free evolution G=0."""
    phi_zero = np.zeros(n)
    H = build_hamiltonian_3d(pos, parity, adj, n, phi_zero, n_side)
    psi = psi0.copy()
    seps = []
    for _ in range(n_steps):
        psi = cn_step(psi, H, n, DT)
        _, _, sep = track_centroids_x(pos[:, 0], psi, n_side / 2.0)
        seps.append(sep)
    return np.array(seps)


def evolve_frozen_3d(pos, parity, adj, n, L_mat, psi0, G, n_side, n_steps):
    """Frozen potential from initial rho."""
    rho0 = np.abs(psi0) ** 2
    phi = solve_phi_massless(L_mat, n, G * rho0)
    H = build_hamiltonian_3d(pos, parity, adj, n, phi, n_side)
    psi = psi0.copy()
    seps = []
    for _ in range(n_steps):
        psi = cn_step(psi, H, n, DT)
        _, _, sep = track_centroids_x(pos[:, 0], psi, n_side / 2.0)
        seps.append(sep)
    return np.array(seps)


def evolve_anderson_3d(pos, parity, adj, n, L_mat, psi0, G, n_side, n_steps, seed):
    """Anderson control: random positive potential matched to self-gravity stats."""
    rho0 = np.abs(psi0) ** 2
    phi_ref = solve_phi_massless(L_mat, n, G * rho0)
    phi_mean = np.mean(phi_ref)
    phi_std = np.std(phi_ref)

    rng = np.random.RandomState(seed)
    phi_rand = np.abs(rng.normal(phi_mean, max(phi_std, 1e-6), n))

    H = build_hamiltonian_3d(pos, parity, adj, n, phi_rand, n_side)
    psi = psi0.copy()
    seps = []
    for _ in range(n_steps):
        psi = cn_step(psi, H, n, DT)
        _, _, sep = track_centroids_x(pos[:, 0], psi, n_side / 2.0)
        seps.append(sep)
    return np.array(seps)


def evolve_selfgrav_3d(pos, parity, adj, n, L_mat, psi0, G, n_side, n_steps,
                       mu2=0.0):
    """Self-consistent gravity. mu2=0 for massless, mu2>0 for screened."""
    psi = psi0.copy()
    seps = []
    norms = []
    for _ in range(n_steps):
        rho = np.abs(psi) ** 2
        if mu2 == 0.0:
            phi = solve_phi_massless(L_mat, n, G * rho)
        else:
            phi = solve_phi_screened(L_mat, n, G * rho, mu2)
        H = build_hamiltonian_3d(pos, parity, adj, n, phi, n_side)
        psi = cn_step(psi, H, n, DT)
        _, _, sep = track_centroids_x(pos[:, 0], psi, n_side / 2.0)
        seps.append(sep)
        norms.append(float(np.linalg.norm(psi)))
    return np.array(seps), np.array(norms)


# ── Evolution modes (2D) ─────────────────────────────────────────

def evolve_selfgrav_2d(pos, parity, adj, n, L_mat, psi0, G, n_side, n_steps,
                       mu2=0.0):
    """Self-consistent gravity on 2D lattice."""
    psi = psi0.copy()
    seps = []
    norms = []
    for _ in range(n_steps):
        rho = np.abs(psi) ** 2
        if mu2 == 0.0:
            phi = solve_phi_massless(L_mat, n, G * rho)
        else:
            phi = solve_phi_screened(L_mat, n, G * rho, mu2)
        H = build_hamiltonian_2d(pos, parity, adj, n, phi, n_side)
        psi = cn_step(psi, H, n, DT)
        _, _, sep = track_centroids_x(pos[:, 0], psi, n_side / 2.0)
        seps.append(sep)
        norms.append(float(np.linalg.norm(psi)))
    return np.array(seps), np.array(norms)


def evolve_free_2d(pos, parity, adj, n, psi0, n_side, n_steps):
    """Free evolution on 2D lattice."""
    phi_zero = np.zeros(n)
    H = build_hamiltonian_2d(pos, parity, adj, n, phi_zero, n_side)
    psi = psi0.copy()
    seps = []
    for _ in range(n_steps):
        psi = cn_step(psi, H, n, DT)
        _, _, sep = track_centroids_x(pos[:, 0], psi, n_side / 2.0)
        seps.append(sep)
    return np.array(seps)


# ── Analysis helpers ──────────────────────────────────────────────

def separation_change(seps):
    """Final - initial separation. Negative = attraction."""
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


# ── Main ──────────────────────────────────────────────────────────

def main():
    t0 = time.time()

    print("=" * 76)
    print("TWO-BODY MUTUAL ATTRACTION: 3D MASSLESS FIELD (mu=0)")
    print("=" * 76)
    print()
    print(f"3D lattice: {N_SIDE_3D}^3 = {N_3D} nodes, periodic")
    print(f"Physics: MASS={MASS}, DT={DT}, sigma={SIGMA}")
    print(f"Massless field: regularize with eps={REG_EPS}")
    print(f"Packets: A at (2,4,4), B at (6,4,4), separation d=4")
    print(f"Evolution: {N_STEPS} steps")
    print()

    # ================================================================
    # PART 1: 3D Control Comparison
    # ================================================================
    print("=" * 76)
    print("PART 1: 3D CONTROL COMPARISON")
    print("=" * 76)
    print()

    # Build 3D lattice
    print("Building 3D lattice...")
    n3, pos3, adj3, par3 = build_3d_lattice(N_SIDE_3D)
    L3 = build_laplacian(adj3, n3)

    # Initial state
    ca = (2, 4, 4)
    cb = (6, 4, 4)
    psi0_3d = two_gaussians_3d(pos3, n3, ca, cb, SIGMA)

    _, _, sep0 = track_centroids_x(pos3[:, 0], psi0_3d, N_SIDE_3D / 2.0)
    print(f"Initial separation: {sep0:.4f}")
    print()

    # Phi diagnostic
    rho_diag = np.abs(psi0_3d) ** 2
    phi_diag = solve_phi_massless(L3, n3, G_DEFAULT * rho_diag)
    print("Phi diagnostic (massless, G=50):")
    print(f"  max(Phi) = {np.max(phi_diag):.6f}")
    print(f"  min(Phi) = {np.min(phi_diag):.6f}")
    print(f"  mean(Phi) = {np.mean(phi_diag):.6f} (should be ~0)")
    print(f"  std(Phi) = {np.std(phi_diag):.6f}")
    print()

    G = G_DEFAULT

    # A. FREE
    print("Running FREE (G=0)...")
    seps_free = evolve_free_3d(pos3, par3, adj3, n3, psi0_3d, N_SIDE_3D, N_STEPS)

    # B. FROZEN
    print(f"Running FROZEN (G={G}, Phi fixed at t=0, mu=0)...")
    seps_frozen = evolve_frozen_3d(pos3, par3, adj3, n3, L3, psi0_3d, G,
                                   N_SIDE_3D, N_STEPS)

    # C. ANDERSON
    print(f"Running ANDERSON ({N_ANDERSON_SEEDS} seeds)...")
    anderson_changes = []
    anderson_mono = []
    for seed in range(N_ANDERSON_SEEDS):
        seps_a = evolve_anderson_3d(pos3, par3, adj3, n3, L3, psi0_3d, G,
                                    N_SIDE_3D, N_STEPS, seed)
        anderson_changes.append(separation_change(seps_a))
        anderson_mono.append(monotonic_decrease_fraction(seps_a))

    # D. SELF-GRAVITY mu=0
    print(f"Running SELF-GRAVITY mu=0 (G={G})...")
    seps_grav0, norms_grav0 = evolve_selfgrav_3d(
        pos3, par3, adj3, n3, L3, psi0_3d, G, N_SIDE_3D, N_STEPS, mu2=0.0)

    # E. SELF-GRAVITY mu^2=0.22
    print(f"Running SELF-GRAVITY mu^2=0.22 (G={G})...")
    seps_grav_screened, norms_grav_s = evolve_selfgrav_3d(
        pos3, par3, adj3, n3, L3, psi0_3d, G, N_SIDE_3D, N_STEPS, mu2=0.22)

    # Report
    print()
    print(f"{'Mode':<22} | {'Delta sep':>12} | {'Mono frac':>10} | {'Final sep':>10}")
    print("-" * 66)

    dc_free = separation_change(seps_free)
    mf_free = monotonic_decrease_fraction(seps_free)
    print(f"{'FREE':<22} | {dc_free:>+12.6f} | {mf_free:>10.3f} | {seps_free[-1]:>10.4f}")

    dc_frozen = separation_change(seps_frozen)
    mf_frozen = monotonic_decrease_fraction(seps_frozen)
    print(f"{'FROZEN':<22} | {dc_frozen:>+12.6f} | {mf_frozen:>10.3f} | {seps_frozen[-1]:>10.4f}")

    ac_mean = np.mean(anderson_changes)
    ac_std = np.std(anderson_changes)
    am_mean = np.mean(anderson_mono)
    print(f"{'ANDERSON (mean)':<22} | {ac_mean:>+12.6f} | {am_mean:>10.3f} | {'':>10}")
    print(f"{'ANDERSON (std)':<22} | {ac_std:>12.6f} | {'':>10} | {'':>10}")

    dc_grav0 = separation_change(seps_grav0)
    mf_grav0 = monotonic_decrease_fraction(seps_grav0)
    print(f"{'SELF-GRAV mu=0':<22} | {dc_grav0:>+12.6f} | {mf_grav0:>10.3f} | {seps_grav0[-1]:>10.4f}")

    dc_grav_s = separation_change(seps_grav_screened)
    mf_grav_s = monotonic_decrease_fraction(seps_grav_screened)
    print(f"{'SELF-GRAV mu2=0.22':<22} | {dc_grav_s:>+12.6f} | {mf_grav_s:>10.3f} | {seps_grav_screened[-1]:>10.4f}")

    # Norm check
    norm_drift_0 = np.max(np.abs(norms_grav0 - 1.0))
    norm_drift_s = np.max(np.abs(norms_grav_s - 1.0))
    print(f"\nNorm conservation: mu=0 max drift = {norm_drift_0:.2e}, "
          f"mu2=0.22 max drift = {norm_drift_s:.2e}")

    # Separation time series
    print()
    print("Separation time series (every 5 steps):")
    print(f"{'Step':>6} | {'FREE':>10} | {'FROZEN':>10} | {'GRAV mu=0':>10} | {'GRAV mu2=.22':>12}")
    print("-" * 60)
    for i in range(0, N_STEPS, 5):
        print(f"{i:>6} | {seps_free[i]:>10.4f} | {seps_frozen[i]:>10.4f} | "
              f"{seps_grav0[i]:>10.4f} | {seps_grav_screened[i]:>12.4f}")
    print(f"{N_STEPS-1:>6} | {seps_free[-1]:>10.4f} | {seps_frozen[-1]:>10.4f} | "
          f"{seps_grav0[-1]:>10.4f} | {seps_grav_screened[-1]:>12.4f}")

    # ================================================================
    # PART 2: G SWEEP (3D, mu=0)
    # ================================================================
    print()
    print("=" * 76)
    print("PART 2: G SWEEP (3D, mu=0)")
    print("=" * 76)
    print()

    g_values = [10, 50, 100]
    print(f"{'G':>6} | {'Delta sep':>12} | {'Mono frac':>10} | {'Approach?':>10}")
    print("-" * 48)

    g_deltas = []
    for g_val in g_values:
        seps_g, _ = evolve_selfgrav_3d(
            pos3, par3, adj3, n3, L3, psi0_3d, g_val, N_SIDE_3D, N_STEPS, mu2=0.0)
        dc = separation_change(seps_g)
        mf = monotonic_decrease_fraction(seps_g)
        approach = "YES" if dc < -0.01 else "no"
        print(f"{g_val:>6} | {dc:>+12.6f} | {mf:>10.3f} | {approach:>10}")
        g_deltas.append(dc)

    approach_increases = all(
        g_deltas[i] <= g_deltas[i - 1]
        for i in range(1, len(g_deltas))
        if not np.isnan(g_deltas[i])
    )
    print(f"\nApproach rate increases with G: {approach_increases}")

    # ================================================================
    # PART 3: 2D COMPARISON (mu=0)
    # ================================================================
    print()
    print("=" * 76)
    print("PART 3: 2D COMPARISON (side=12, mu=0)")
    print("=" * 76)
    print()

    n2, pos2, adj2, par2 = build_2d_lattice(N_SIDE_2D)
    L2 = build_laplacian(adj2, n2)

    ca_2d = (3, 6)
    cb_2d = (9, 6)
    psi0_2d = two_gaussians_2d(pos2, n2, ca_2d, cb_2d, SIGMA)

    _, _, sep0_2d = track_centroids_x(pos2[:, 0], psi0_2d, N_SIDE_2D / 2.0)
    print(f"2D initial separation: {sep0_2d:.4f}")

    print("Running 2D FREE...")
    seps_free_2d = evolve_free_2d(pos2, par2, adj2, n2, psi0_2d, N_SIDE_2D, N_STEPS)

    print(f"Running 2D SELF-GRAVITY mu=0 (G={G})...")
    seps_grav_2d, norms_2d = evolve_selfgrav_2d(
        pos2, par2, adj2, n2, L2, psi0_2d, G, N_SIDE_2D, N_STEPS, mu2=0.0)

    print(f"Running 2D SELF-GRAVITY mu2=0.22 (G={G})...")
    seps_grav_2d_s, _ = evolve_selfgrav_2d(
        pos2, par2, adj2, n2, L2, psi0_2d, G, N_SIDE_2D, N_STEPS, mu2=0.22)

    dc_free_2d = separation_change(seps_free_2d)
    dc_grav_2d = separation_change(seps_grav_2d)
    dc_grav_2d_s = separation_change(seps_grav_2d_s)

    print()
    print(f"{'Mode':<22} | {'Delta sep':>12}")
    print("-" * 40)
    print(f"{'2D FREE':<22} | {dc_free_2d:>+12.6f}")
    print(f"{'2D GRAV mu=0':<22} | {dc_grav_2d:>+12.6f}")
    print(f"{'2D GRAV mu2=0.22':<22} | {dc_grav_2d_s:>+12.6f}")

    print()
    print("2D separation time series (every 5 steps):")
    print(f"{'Step':>6} | {'FREE':>10} | {'GRAV mu=0':>10} | {'GRAV mu2=.22':>12}")
    print("-" * 48)
    for i in range(0, N_STEPS, 5):
        print(f"{i:>6} | {seps_free_2d[i]:>10.4f} | {seps_grav_2d[i]:>10.4f} | "
              f"{seps_grav_2d_s[i]:>12.4f}")
    print(f"{N_STEPS-1:>6} | {seps_free_2d[-1]:>10.4f} | {seps_grav_2d[-1]:>10.4f} | "
          f"{seps_grav_2d_s[-1]:>12.4f}")

    # ================================================================
    # VERDICT
    # ================================================================
    print()
    print("=" * 76)
    print("VERDICT")
    print("=" * 76)
    print()

    # Primary: does 3D mu=0 show attraction?
    grav_attracts = dc_grav0 < -0.01
    grav_vs_free = dc_grav0 - dc_free
    screened_attracts = dc_grav_s < -0.01

    print(f"3D mu=0 delta sep:     {dc_grav0:+.6f}")
    print(f"3D mu2=0.22 delta sep: {dc_grav_s:+.6f}")
    print(f"3D FREE delta sep:     {dc_free:+.6f}")
    print(f"3D FROZEN delta sep:   {dc_frozen:+.6f}")
    print(f"ANDERSON mean +/- std: {ac_mean:+.6f} +/- {ac_std:.6f}")
    print()

    # Specific comparison: mu=0 vs mu2=0.22
    print("KEY COMPARISON: massless vs screened")
    print(f"  mu=0 attraction:     {dc_grav0:+.6f}  {'PASS' if grav_attracts else 'FAIL'}")
    print(f"  mu2=0.22 attraction: {dc_grav_s:+.6f}  {'PASS' if screened_attracts else 'FAIL'}")
    print(f"  Screening kills force: {not screened_attracts and grav_attracts}")
    print()

    # 3D vs 2D comparison
    print("DIMENSIONALITY COMPARISON:")
    print(f"  3D mu=0: {dc_grav0:+.6f}")
    print(f"  2D mu=0: {dc_grav_2d:+.6f}")
    print(f"  3D stronger than 2D: {dc_grav0 < dc_grav_2d}")
    print()

    # Self-consistency: dynamic vs frozen
    grav_vs_frozen_diff = abs(dc_grav0 - dc_frozen)
    print(f"Self-consistency (|grav - frozen|): {grav_vs_frozen_diff:.6f}")
    print(f"  Dynamic differs from frozen: {grav_vs_frozen_diff > 0.05}")
    print()

    # Anderson exceeded
    if ac_std > 0:
        anderson_exceeded = dc_grav0 < ac_mean - 2 * ac_std
    else:
        anderson_exceeded = dc_grav0 < ac_mean - 0.01

    # Score card
    criteria = [
        ("3D mu=0 mutual attraction (delta < -0.01)", grav_attracts),
        ("Screened (mu2=0.22) fails to attract", not screened_attracts),
        ("mu=0 beats all controls", dc_grav0 < min(dc_free, dc_frozen, ac_mean)),
        ("Exceeds Anderson 2-sigma", anderson_exceeded),
        ("G-monotonic approach rate", approach_increases),
        ("3D stronger than 2D (mu=0)", dc_grav0 < dc_grav_2d),
    ]

    n_pass = sum(1 for _, v in criteria if v)
    for name, val in criteria:
        print(f"  [{'PASS' if val else 'FAIL':>4}] {name}")

    print(f"\nSCORE: {n_pass}/{len(criteria)}")
    print()

    if grav_attracts and n_pass >= 4:
        print("STRONG EVIDENCE: Massless 3D self-gravity produces mutual attraction.")
        print("Yukawa screening was the culprit in the 2D test.")
    elif grav_attracts:
        print("WEAK EVIDENCE: Attraction detected but controls not cleanly separated.")
    elif dc_grav0 < dc_free:
        print("PARTIAL: Self-gravity confines better than free but no net attraction.")
        print("The self-consistent field is attractive but self-confinement dominates")
        print("over inter-packet force at this lattice size.")
    else:
        print("NO EVIDENCE: mu=0 does not produce visible mutual attraction.")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
