#!/usr/bin/env python3
"""
Self-Consistency Test — Does backreaction matter, or just positivity?
=====================================================================

The Anderson control showed self-gravity is distinguishable from random
disorder at 2.7 sigma (boundary coefficient) and in sign consistency
(300/300 vs 6/10).  But we haven't tested whether the SELF-CONSISTENCY
is what matters, or just having a POSITIVE potential (since |psi|^2 >= 0
means Phi is always positive).

Protocol on 2D staggered lattice (side=10):

Compare FOUR potential types:
  1. SELF-CONSISTENT   Phi = (L + mu^2)^{-1} G |psi|^2  (updates each step)
  2. STATIC-FROM-INITIAL  Phi = (L + mu^2)^{-1} G |psi_0|^2  (frozen at t=0)
  3. POSITIVE RANDOM   Phi_i = |N(mean_Phi, std_Phi)|  (positive, uncorrelated)
  4. NEGATIVE RANDOM   Phi_i = -|N(mean_Phi, std_Phi)| (negative, uncorrelated)

For each, measure:
  a. Sign selectivity   — attract vs repulse shell-force margin (G=5, 40 iter)
  b. Width contraction   — w_grav / w_free after 40 steps (G=50)
  c. Boundary-law alpha  — from Dirac sea

KEY discriminators:
  - SELF-CONSISTENT != STATIC-FROM-INITIAL  =>  backreaction matters
  - STATIC-FROM-INITIAL = POSITIVE RANDOM   =>  spatial correlations don't matter
  - POSITIVE RANDOM != NEGATIVE RANDOM      =>  sign of Phi matters

Important reporting note:
  The self-consistent and static-from-initial surfaces are deterministic on
  this fixed lattice, so repeated seeds there are not a genuine sampling
  distribution. Large deterministic splits should be described as exact
  separations on this surface, not as literal infinite-sigma statements.
"""

from __future__ import annotations

import math
import time
from collections import deque

import numpy as np
from scipy import sparse
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

# ── Physical parameters ────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 40
SIGMA = 1.5
SIDE = 10

G_SIGN = 5.0       # for sign selectivity probe
G_WIDTH = 50.0      # for width contraction probe
G_BOUNDARY = 10.0   # for boundary law probe
SIGN_ITER = 40
WIDTH_STEPS = 40
N_SEEDS = 5


# ── Lattice ────────────────────────────────────────────────────────

def build_lattice_2d(side: int):
    """2D periodic square lattice with checkerboard parity."""
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
                jx = (ix + dix) % side
                jy = (iy + diy) % side
                adj[idx].append(jx * side + jy)

    return n, pos, adj, col


# ── Hamiltonian and evolution ──────────────────────────────────────

def build_laplacian(adj: dict[int, list[int]], n: int):
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


def build_hamiltonian(pos: np.ndarray, col: np.ndarray,
                      adj: dict[int, list[int]], n: int,
                      phi: np.ndarray) -> sparse.csc_matrix:
    """Staggered-fermion Hamiltonian with parity coupling."""
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)

    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


def cn_step(psi: np.ndarray, H: sparse.csc_matrix, dt: float) -> np.ndarray:
    """Crank-Nicolson time step."""
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def make_gaussian(pos: np.ndarray, n: int):
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


def rms_width(psi: np.ndarray, pos: np.ndarray) -> float:
    rho = np.abs(psi)**2
    rho /= np.sum(rho)
    cx = np.sum(rho * pos[:, 0])
    cy = np.sum(rho * pos[:, 1])
    return float(np.sqrt(np.sum(rho * ((pos[:, 0] - cx)**2 +
                                        (pos[:, 1] - cy)**2))))


# ── BFS utilities ──────────────────────────────────────────────────

def bfs_depth(adj: dict[int, list[int]], src: int, n: int):
    depth = np.full(n, np.inf)
    depth[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj[i]:
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1
                q.append(j)
    return depth


def bfs_ball(adj: dict[int, list[int]], center: int, radius: int, n: int):
    dist = np.full(n, -1, dtype=int)
    dist[center] = 0
    queue = deque([center])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                if dist[v] <= radius:
                    queue.append(v)

    A_set = set(i for i in range(n) if 0 <= dist[i] <= radius)
    A_nodes = sorted(A_set)
    boundary_edges = sum(
        1 for i in A_nodes for j in adj[i] if j not in A_set
    )
    return A_nodes, boundary_edges


# ── Probe A: Sign selectivity ─────────────────────────────────────

def shell_force_toward(depth: np.ndarray, n: int,
                       psi: np.ndarray, phi: np.ndarray) -> bool:
    finite = depth[np.isfinite(depth)]
    max_d = int(np.max(finite)) if finite.size else 0
    if max_d <= 0:
        return False

    rho = np.abs(psi)**2
    rho_n = rho / np.sum(rho)
    shell_phi = np.zeros(max_d + 1)
    shell_count = np.zeros(max_d + 1)
    shell_prob = np.zeros(max_d + 1)

    for i in range(n):
        d = int(depth[i]) if np.isfinite(depth[i]) else -1
        if 0 <= d <= max_d:
            shell_phi[d] += phi[i]
            shell_prob[d] += rho_n[i]
            shell_count[d] += 1
    for d in range(max_d + 1):
        if shell_count[d] > 0:
            shell_phi[d] /= shell_count[d]

    grad = np.zeros(max_d + 1)
    for d in range(max_d + 1):
        if d == 0:
            grad[d] = shell_phi[0] - shell_phi[min(1, max_d)]
        elif d == max_d:
            grad[d] = shell_phi[d - 1] - shell_phi[d]
        else:
            grad[d] = 0.5 * (shell_phi[d - 1] - shell_phi[d + 1])

    force = float(np.sum(shell_prob * grad))
    return force > 0


def measure_sign_selectivity(pos, col, adj, n, potential_fn, seed=0):
    """Measure attract vs repulse toward-counts.

    potential_fn(psi, sign, rng) -> phi  is called each step.
    """
    center_idx = (SIDE // 2) * SIDE + (SIDE // 2)
    depth = bfs_depth(adj, center_idx, n)

    results = {}
    for label, sign in [("attract", +1.0), ("repulse", -1.0)]:
        rng = np.random.RandomState(seed + 200)
        psi = make_gaussian(pos, n)
        tw = 0
        for step in range(SIGN_ITER):
            phi = potential_fn(psi, sign, rng)
            if shell_force_toward(depth, n, psi, phi):
                tw += 1
            H = build_hamiltonian(pos, col, adj, n, phi)
            psi = cn_step(psi, H, DT)
        results[label] = tw

    margin = results["attract"] - results["repulse"]
    return results["attract"], results["repulse"], margin


# ── Probe B: Width contraction ─────────────────────────────────────

def measure_width_contraction(pos, col, adj, n, potential_fn, seed=0):
    """Return w_grav / w_free after WIDTH_STEPS at G_WIDTH."""
    rng = np.random.RandomState(seed + 300)

    # Free evolution (no potential)
    psi_free = make_gaussian(pos, n)
    for _ in range(WIDTH_STEPS):
        H_free = build_hamiltonian(pos, col, adj, n, np.zeros(n))
        psi_free = cn_step(psi_free, H_free, DT)
        psi_free /= np.linalg.norm(psi_free)
    w_free = rms_width(psi_free, pos)

    # With potential
    psi = make_gaussian(pos, n)
    for step in range(WIDTH_STEPS):
        phi = potential_fn(psi, +1.0, rng)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)
    w_grav = rms_width(psi, pos)

    ratio = w_grav / w_free if w_free > 1e-12 else float('nan')
    return ratio, w_grav, w_free


# ── Probe C: Boundary-law coefficient ─────────────────────────────

def dirac_sea_correlation_matrix(H: sparse.csc_matrix):
    H_dense = H.toarray()
    H_dense = 0.5 * (H_dense + H_dense.conj().T)
    eigenvalues, eigenvectors = np.linalg.eigh(H_dense)

    filled = eigenvalues < 0
    n_filled = int(np.sum(filled))
    if n_filled == 0:
        n_filled = len(eigenvalues) // 2
        filled = np.zeros(len(eigenvalues), dtype=bool)
        filled[:n_filled] = True

    V = eigenvectors[:, filled]
    return V @ V.conj().T


def entanglement_entropy_from_C(C: np.ndarray, A_nodes: list[int]):
    if len(A_nodes) == 0:
        return 0.0
    ix = np.ix_(A_nodes, A_nodes)
    C_A = C[ix]
    C_A = 0.5 * (C_A + C_A.conj().T)
    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)
    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))
    return float(S)


def measure_boundary_law(pos, col, adj, n, potential_fn, seed=0):
    """Build final H from potential, measure boundary-law alpha."""
    rng = np.random.RandomState(seed + 400)
    psi = make_gaussian(pos, n)

    # Evolve to get final state and phi
    for step in range(N_STEPS):
        phi = potential_fn(psi, +1.0, rng)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)

    # Use last H for Dirac sea
    C = dirac_sea_correlation_matrix(H)
    center = (SIDE // 2) * SIDE + (SIDE // 2)
    max_R = SIDE // 2 - 1

    bnds, entropies = [], []
    for R in range(1, max_R + 1):
        A_nodes, bnd_edges = bfs_ball(adj, center, R, n)
        if len(A_nodes) == 0 or len(A_nodes) >= n:
            continue
        S = entanglement_entropy_from_C(C, A_nodes)
        bnds.append(bnd_edges)
        entropies.append(S)

    if len(bnds) < 2:
        return 0.0, 0.0

    res = linregress(np.asarray(bnds, dtype=float),
                     np.asarray(entropies, dtype=float))
    return res.slope, res.rvalue**2


# ═══════════════════════════════════════════════════════════════════
# Potential factories
# ═══════════════════════════════════════════════════════════════════

def make_self_consistent_potential(L_csr, n, G):
    """Type 1: self-consistent, updates every step."""
    solve_op = (L_csr + MU2 * speye(n, format='csr')).tocsc()

    def potential_fn(psi, sign, rng):
        rho = np.abs(psi)**2
        phi = spsolve(solve_op, G * rho)
        return sign * phi

    return potential_fn


def make_static_initial_potential(L_csr, n, G, pos):
    """Type 2: computed from initial psi_0, frozen."""
    solve_op = (L_csr + MU2 * speye(n, format='csr')).tocsc()
    psi0 = make_gaussian(pos, n)
    rho0 = np.abs(psi0)**2
    phi_static = spsolve(solve_op, G * rho0)

    def potential_fn(psi, sign, rng):
        return sign * phi_static

    return potential_fn


def make_positive_random_potential(mean_phi, std_phi, n):
    """Type 3: |N(mean, std)|, positive random, matched stats."""
    def potential_fn(psi, sign, rng):
        return sign * np.abs(rng.normal(mean_phi, std_phi, n))

    return potential_fn


def make_negative_random_potential(mean_phi, std_phi, n):
    """Type 4: -|N(mean, std)|, negative random."""
    def potential_fn(psi, sign, rng):
        return sign * (-np.abs(rng.normal(mean_phi, std_phi, n)))

    return potential_fn


# ═══════════════════════════════════════════════════════════════════
# MAIN EXPERIMENT
# ═══════════════════════════════════════════════════════════════════

def main():
    t0 = time.time()

    print("=" * 78)
    print("SELF-CONSISTENCY TEST")
    print("Does backreaction matter, or just having a positive potential?")
    print("=" * 78)
    print()
    print(f"Lattice: {SIDE}x{SIDE} periodic staggered (n={SIDE**2})")
    print(f"MASS={MASS}, MU2={MU2}, DT={DT}")
    print(f"G_sign={G_SIGN}, G_width={G_WIDTH}, G_boundary={G_BOUNDARY}")
    print(f"SIGN_ITER={SIGN_ITER}, WIDTH_STEPS={WIDTH_STEPS}, N_STEPS={N_STEPS}")
    print(f"Seeds per type: {N_SEEDS}")
    print()

    n, pos, adj, col = build_lattice_2d(SIDE)
    L = build_laplacian(adj, n)

    # ── Compute reference phi stats from self-consistent evolution ──
    print("Computing reference Phi statistics from self-consistent run...")
    solve_op = (L + MU2 * speye(n, format='csr')).tocsc()
    psi_ref = make_gaussian(pos, n)
    phi_ref = np.zeros(n)
    for step in range(N_STEPS):
        rho = np.abs(psi_ref)**2
        phi_ref = spsolve(solve_op, G_BOUNDARY * rho)
        H_ref = build_hamiltonian(pos, col, adj, n, phi_ref)
        psi_ref = cn_step(psi_ref, H_ref, DT)
        psi_ref /= np.linalg.norm(psi_ref)

    phi_mean = float(np.mean(phi_ref))
    phi_std = float(np.std(phi_ref))
    print(f"  Reference Phi: mean={phi_mean:.6f}, std={phi_std:.6f}, "
          f"min={np.min(phi_ref):.6f}, max={np.max(phi_ref):.6f}")
    print(f"  All positive: {np.all(phi_ref >= 0)}")
    print()

    # ── Build potential factories ──────────────────────────────────

    types = {
        "1-SelfConsist": {
            "sign": lambda G: make_self_consistent_potential(L, n, G),
            "width": lambda: make_self_consistent_potential(L, n, G_WIDTH),
            "boundary": lambda: make_self_consistent_potential(L, n, G_BOUNDARY),
        },
        "2-StaticInit": {
            "sign": lambda G: make_static_initial_potential(L, n, G, pos),
            "width": lambda: make_static_initial_potential(L, n, G_WIDTH, pos),
            "boundary": lambda: make_static_initial_potential(L, n, G_BOUNDARY, pos),
        },
        "3-PosRandom": {
            "sign": lambda G: make_positive_random_potential(phi_mean, phi_std, n),
            "width": lambda: make_positive_random_potential(phi_mean, phi_std, n),
            "boundary": lambda: make_positive_random_potential(phi_mean, phi_std, n),
        },
        "4-NegRandom": {
            "sign": lambda G: make_negative_random_potential(phi_mean, phi_std, n),
            "width": lambda: make_negative_random_potential(phi_mean, phi_std, n),
            "boundary": lambda: make_negative_random_potential(phi_mean, phi_std, n),
        },
    }

    # ── Run all probes ─────────────────────────────────────────────

    results = {}

    for tname, factories in types.items():
        print("=" * 78)
        print(f"TYPE: {tname}")
        print("=" * 78)
        t1 = time.time()

        sign_margins = []
        sign_attracts = []
        sign_repulses = []
        width_ratios = []
        boundary_alphas = []
        boundary_r2s = []

        for seed in range(N_SEEDS):
            # Probe A: sign selectivity
            pfn_sign = factories["sign"](G_SIGN)
            tw_a, tw_r, margin = measure_sign_selectivity(
                pos, col, adj, n, pfn_sign, seed=seed)
            sign_attracts.append(tw_a)
            sign_repulses.append(tw_r)
            sign_margins.append(margin)

            # Probe B: width contraction
            pfn_width = factories["width"]()
            ratio, w_g, w_f = measure_width_contraction(
                pos, col, adj, n, pfn_width, seed=seed)
            width_ratios.append(ratio)

            # Probe C: boundary law
            pfn_bnd = factories["boundary"]()
            alpha, r2 = measure_boundary_law(
                pos, col, adj, n, pfn_bnd, seed=seed)
            boundary_alphas.append(alpha)
            boundary_r2s.append(r2)

            print(f"  seed={seed}: sign_margin={margin:>+3d}  "
                  f"w_ratio={ratio:.4f}  alpha={alpha:.6f}  R2={r2:.4f}")

        results[tname] = {
            "sign_margins": np.array(sign_margins),
            "sign_attracts": np.array(sign_attracts),
            "sign_repulses": np.array(sign_repulses),
            "width_ratios": np.array(width_ratios),
            "boundary_alphas": np.array(boundary_alphas),
            "boundary_r2s": np.array(boundary_r2s),
        }

        sm = results[tname]["sign_margins"]
        wr = results[tname]["width_ratios"]
        ba = results[tname]["boundary_alphas"]
        print(f"\n  Summary: sign_margin={sm.mean():+.1f}+/-{sm.std():.1f}  "
              f"w_ratio={wr.mean():.4f}+/-{wr.std():.4f}  "
              f"alpha={ba.mean():.6f}+/-{ba.std():.6f}")
        print(f"  Sign consistency: {np.sum(sm > 0)}/{N_SEEDS} positive margins")
        print(f"  Time: {time.time() - t1:.1f}s")
        print()

    # ═══════════════════════════════════════════════════════════════
    # COMPARISON TABLE
    # ═══════════════════════════════════════════════════════════════
    print()
    print("=" * 78)
    print("COMPARISON TABLE  (mean +/- std over 5 seeds)")
    print("=" * 78)
    print()

    header = (f"{'Type':<18s} {'Sign margin':>14s} {'Sign +/N':>8s} "
              f"{'w_grav/w_free':>14s} {'Bnd alpha':>14s} {'Bnd R^2':>10s}")
    print(header)
    print("-" * len(header))

    for tname in types:
        r = results[tname]
        sm = r["sign_margins"]
        wr = r["width_ratios"]
        ba = r["boundary_alphas"]
        br = r["boundary_r2s"]
        n_pos = int(np.sum(sm > 0))

        print(f"{tname:<18s} "
              f"{sm.mean():>+6.1f}+/-{sm.std():<5.1f} "
              f"{n_pos:>3d}/{N_SEEDS:<3d} "
              f"{wr.mean():>6.4f}+/-{wr.std():<6.4f} "
              f"{ba.mean():>7.6f}+/-{ba.std():<7.6f} "
              f"{br.mean():>5.4f}")

    # ═══════════════════════════════════════════════════════════════
    # PAIRWISE COMPARISONS
    # ═══════════════════════════════════════════════════════════════
    print()
    print("=" * 78)
    print("PAIRWISE COMPARISONS (key discriminators)")
    print("=" * 78)
    print()

    def sigma_diff(a, b):
        """Sigma-like separation when both sides have real spread."""
        pooled_std = np.sqrt((a.std()**2 + b.std()**2) / 2)
        if pooled_std < 1e-12:
            diff = abs(a.mean() - b.mean())
            return float('nan') if diff > 1e-12 else 0.0
        return abs(a.mean() - b.mean()) / pooled_std

    def fmt_sep(sig):
        if np.isnan(sig):
            return "deterministic split"
        return f"{sig:.1f} sigma"

    comparisons = [
        ("1-SelfConsist", "2-StaticInit",
         "Self-consistent vs Static-from-initial (does backreaction matter?)"),
        ("2-StaticInit", "3-PosRandom",
         "Static-from-initial vs Positive random (do spatial correlations matter?)"),
        ("3-PosRandom", "4-NegRandom",
         "Positive random vs Negative random (does sign of Phi matter?)"),
        ("1-SelfConsist", "3-PosRandom",
         "Self-consistent vs Positive random (full self-consistency vs just positivity)"),
    ]

    for t1_name, t2_name, description in comparisons:
        r1 = results[t1_name]
        r2 = results[t2_name]

        sig_sign = sigma_diff(r1["sign_margins"], r2["sign_margins"])
        sig_width = sigma_diff(r1["width_ratios"], r2["width_ratios"])
        sig_alpha = sigma_diff(r1["boundary_alphas"], r2["boundary_alphas"])

        print(f"  {description}")
        print(f"    Sign margin:   {r1['sign_margins'].mean():>+6.1f} vs "
              f"{r2['sign_margins'].mean():>+6.1f}  ({fmt_sep(sig_sign)})")
        print(f"    Width ratio:   {r1['width_ratios'].mean():>.4f} vs "
              f"{r2['width_ratios'].mean():>.4f}  ({fmt_sep(sig_width)})")
        print(f"    Bnd alpha:     {r1['boundary_alphas'].mean():>.6f} vs "
              f"{r2['boundary_alphas'].mean():>.6f}  ({fmt_sep(sig_alpha)})")

        # Sign consistency comparison
        n1_pos = int(np.sum(r1["sign_margins"] > 0))
        n2_pos = int(np.sum(r2["sign_margins"] > 0))
        print(f"    Sign consist:  {n1_pos}/{N_SEEDS} vs {n2_pos}/{N_SEEDS} positive")
        print()

    # ═══════════════════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════════════════
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print()

    threshold = 2.0

    # Q1: Does backreaction matter?
    r_sc = results["1-SelfConsist"]
    r_si = results["2-StaticInit"]
    sigs_q1 = [
        sigma_diff(r_sc["sign_margins"], r_si["sign_margins"]),
        sigma_diff(r_sc["width_ratios"], r_si["width_ratios"]),
        sigma_diff(r_sc["boundary_alphas"], r_si["boundary_alphas"]),
    ]
    max_q1 = max(sigs_q1)
    q1_det = np.any(np.isnan(sigs_q1))
    if q1_det or max_q1 > threshold:
        label = "deterministic separation on this fixed surface" if q1_det else f"{max_q1:.1f} sigma"
        print(f"  Q1: BACKREACTION MATTERS ({label})")
        print(f"      Self-consistent differs from static-from-initial.")
        print(f"      The iterative update of Phi from evolving |psi|^2 is")
        print(f"      doing real dynamical work beyond the initial conditions.")
    else:
        print(f"  Q1: Backreaction NOT distinguished ({max_q1:.1f} sigma)")
        print(f"      Static-from-initial is as good as self-consistent.")

    print()

    # Q2: Do spatial correlations matter?
    r_pr = results["3-PosRandom"]
    sigs_q2 = [
        sigma_diff(r_si["sign_margins"], r_pr["sign_margins"]),
        sigma_diff(r_si["width_ratios"], r_pr["width_ratios"]),
        sigma_diff(r_si["boundary_alphas"], r_pr["boundary_alphas"]),
    ]
    max_q2 = max(sigs_q2)
    if max_q2 > threshold:
        print(f"  Q2: SPATIAL CORRELATIONS MATTER ({max_q2:.1f} sigma)")
        print(f"      Static-from-initial differs from positive random.")
        print(f"      The spatial structure of |psi_0|^2 provides information")
        print(f"      beyond mere positivity of the potential.")
    else:
        print(f"  Q2: Spatial correlations NOT distinguished ({max_q2:.1f} sigma)")
        print(f"      Any positive potential of matching stats works the same.")

    print()

    # Q3: Does sign of Phi matter?
    r_nr = results["4-NegRandom"]
    sigs_q3 = [
        sigma_diff(r_pr["sign_margins"], r_nr["sign_margins"]),
        sigma_diff(r_pr["width_ratios"], r_nr["width_ratios"]),
        sigma_diff(r_pr["boundary_alphas"], r_nr["boundary_alphas"]),
    ]
    max_q3 = max(sigs_q3)
    if max_q3 > threshold:
        print(f"  Q3: SIGN OF PHI MATTERS ({max_q3:.1f} sigma)")
        print(f"      Positive random differs from negative random.")
        print(f"      Confirms parity-coupling sign selection is physical.")
    else:
        print(f"  Q3: Sign of Phi NOT distinguished ({max_q3:.1f} sigma)")
        print(f"      Positive and negative random give same results.")

    print()

    # Overall
    r_sc_vs_pr = [
        sigma_diff(r_sc["sign_margins"], r_pr["sign_margins"]),
        sigma_diff(r_sc["width_ratios"], r_pr["width_ratios"]),
        sigma_diff(r_sc["boundary_alphas"], r_pr["boundary_alphas"]),
    ]
    finite_overall = [x for x in r_sc_vs_pr if not np.isnan(x)]
    max_overall = max(finite_overall) if finite_overall else float('nan')
    overall_label = fmt_sep(max_overall)
    print(f"  OVERALL: Self-consistent vs Positive random = {overall_label}")
    if (not np.isnan(max_overall)) and max_overall > threshold:
        print(f"  Self-consistency provides information BEYOND just having")
        print(f"  a positive potential. The gravitational backreaction is real.")
    else:
        print(f"  Self-consistency is NOT distinguished from mere positivity.")

    elapsed = time.time() - t0
    print(f"\n  Total time: {elapsed:.1f}s")

    # ── Plot ───────────────────────────────────────────────────────
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Self-Consistency Test\n'
                     'Does backreaction matter, or just positivity?',
                     fontsize=13, fontweight='bold')

        type_names = list(types.keys())
        short_names = ["Self-\nconsist", "Static\ninit", "Pos\nrandom", "Neg\nrandom"]
        colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4']
        x = np.arange(len(type_names))

        # (a) Sign margin
        ax = axes[0]
        means = [results[t]["sign_margins"].mean() for t in type_names]
        stds = [results[t]["sign_margins"].std() for t in type_names]
        ax.bar(x, means, yerr=stds, capsize=5, color=colors, alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(short_names, fontsize=9)
        ax.set_ylabel('Sign margin (attract - repulse)')
        ax.set_title('(a) Sign Selectivity')
        ax.axhline(0, color='gray', linestyle='--', alpha=0.5)

        # (b) Width contraction
        ax = axes[1]
        means = [results[t]["width_ratios"].mean() for t in type_names]
        stds = [results[t]["width_ratios"].std() for t in type_names]
        ax.bar(x, means, yerr=stds, capsize=5, color=colors, alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(short_names, fontsize=9)
        ax.set_ylabel('w_grav / w_free')
        ax.set_title('(b) Width Contraction')
        ax.axhline(1.0, color='gray', linestyle='--', alpha=0.5)

        # (c) Boundary alpha
        ax = axes[2]
        means = [results[t]["boundary_alphas"].mean() for t in type_names]
        stds = [results[t]["boundary_alphas"].std() for t in type_names]
        ax.bar(x, means, yerr=stds, capsize=5, color=colors, alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(short_names, fontsize=9)
        ax.set_ylabel('Boundary-law alpha')
        ax.set_title('(c) Boundary Law Coefficient')

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    main()
