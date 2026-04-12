#!/usr/bin/env python3
"""Quantum error correction structure in the self-gravitating Dirac sea.

Tests whether the Dirac sea on a 2D staggered lattice with self-gravity
has holographic quantum error-correcting (QEC) structure.

Protocol:
  1. Build staggered-fermion H with parity coupling on 2D periodic lattice.
     Evolve under self-gravity (30 CN steps, G=10, mu2=0.001).
  2. Fill the Dirac sea (all negative-energy modes).
  3. Compute correlation matrix C = V_filled @ V_filled^dagger.
  4. For BFS-ball region A of radius R around center:
     - "Erase" A: replace C_A with maximally mixed (0.5*I).
     - Measure recovery fidelity: how close can we reconstruct the
       original C_A from the boundary information?
  5. The Petz recovery channel for free fermions reduces to checking
     whether S_A ~ S_{boundary(A)}.  If entanglement is boundary-dominated,
     information in A can be reconstructed from its complement.
  6. Sweep erasure fraction from 0.1 to 0.9: randomly erase f fraction
     of A nodes and measure whether the remaining boundary information
     suffices for recovery.
  7. Compare G=0 (free) vs G=10 (gravitating).

Key metric: "code distance" = largest erasure fraction where recovery
fidelity > 0.5.
"""

from __future__ import annotations

import math
import time
from collections import deque

import numpy as np
from scipy import sparse
from scipy.sparse import eye as speye
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.001
DT = 0.12
G_SELF = 10.0
N_STEPS = 30
SIGMA = 1.5
SIDE = 10


# ---------------------------------------------------------------------------
# Lattice
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# BFS ball
# ---------------------------------------------------------------------------

def bfs_ball(adj: dict[int, list[int]], center: int, radius: int, n: int):
    """BFS ball of given radius. Returns (A_nodes, boundary_edges)."""
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

    boundary_edges = 0
    for i in A_nodes:
        for j in adj[i]:
            if j not in A_set:
                boundary_edges += 1

    return A_nodes, boundary_edges


# ---------------------------------------------------------------------------
# Hamiltonian and evolution
# ---------------------------------------------------------------------------

def solve_poisson(adj: dict, n: int, rho: np.ndarray, mu2: float,
                  G: float) -> np.ndarray:
    """Screened Poisson: (L + mu^2) Phi = G * rho."""
    if G == 0.0:
        return np.zeros(n)

    rows, cols, vals = [], [], []
    for i in range(n):
        degree = len(adj[i])
        rows.append(i); cols.append(i); vals.append(float(degree) + mu2)
        for j in adj[i]:
            rows.append(i); cols.append(j); vals.append(-1.0)

    L = sparse.csc_matrix((vals, (rows, cols)), shape=(n, n))
    return spsolve(L, G * rho)


def build_hamiltonian(n: int, pos: np.ndarray, adj: dict, col: np.ndarray,
                      phi: np.ndarray) -> sparse.csc_matrix:
    """Staggered-fermion Hamiltonian with parity coupling."""
    H = sparse.lil_matrix((n, n), dtype=complex)

    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)

    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


def cn_step(psi: np.ndarray, H: sparse.csc_matrix, dt: float) -> np.ndarray:
    """One Crank-Nicolson time step."""
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def evolve_and_get_final_H(n: int, pos: np.ndarray, adj: dict,
                            col: np.ndarray, G: float):
    """Evolve Gaussian wavepacket under self-gravity, return final H."""
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)

    H_final = None
    for step in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = solve_poisson(adj, n, rho, MU2, G)
        H = build_hamiltonian(n, pos, adj, col, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)
        H_final = H

    return psi, H_final


# ---------------------------------------------------------------------------
# Dirac sea correlation matrix
# ---------------------------------------------------------------------------

def dirac_sea_correlation_matrix(H: sparse.csc_matrix):
    """Diagonalise H, fill negative-energy modes, return C."""
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
    C = V @ V.conj().T

    return C, eigenvalues, n_filled


# ---------------------------------------------------------------------------
# Entanglement entropy from correlation matrix
# ---------------------------------------------------------------------------

def entanglement_entropy_from_C(C: np.ndarray, nodes: list[int]):
    """Free-fermion entanglement entropy from restricted correlation matrix."""
    if len(nodes) == 0:
        return 0.0, np.array([])

    ix = np.ix_(nodes, nodes)
    C_A = C[ix]
    C_A = 0.5 * (C_A + C_A.conj().T)

    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)

    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))
    return float(S), nu


# ---------------------------------------------------------------------------
# QEC fidelity measure
# ---------------------------------------------------------------------------

def recovery_fidelity(C_original: np.ndarray, A_nodes: list[int],
                      erased_nodes: list[int]) -> float:
    """Measure how well erased information can be recovered from the boundary.

    Method: Erase the correlation matrix entries for erased_nodes by replacing
    with maximally mixed (C_erased = 0.5 * I on erased sites). Then measure
    how close the reconstructed C_A is to the original.

    The Petz recovery map for Gaussian states acts on the correlation matrix.
    For the restricted subspace, the recovery fidelity is:

        F = 1 - ||C_A^{original} - C_A^{recovered}||_F^2 / ||C_A^{original}||_F^2

    where C_A^{recovered} is obtained by:
      1. Set C_erased = 0.5 * I (maximally mixed on erased sites)
      2. Use the Schur complement to reconstruct from the complement

    For free fermions, the optimal recovery uses the conditional correlation:
      C_{A|B} = C_A - C_{AB} @ inv(C_B) @ C_{BA}
    The recovery is good if C_{A|B} ~ 0 (all info in A is encoded in B).
    """
    n = C_original.shape[0]
    all_nodes = list(range(n))
    erased_set = set(erased_nodes)
    complement = sorted(set(all_nodes) - erased_set)

    if len(complement) == 0 or len(erased_nodes) == 0:
        return 1.0

    # Original restricted matrices
    ix_e = np.ix_(erased_nodes, erased_nodes)
    ix_c = np.ix_(complement, complement)
    ix_ec = np.ix_(erased_nodes, complement)
    ix_ce = np.ix_(complement, erased_nodes)

    C_E = C_original[ix_e]
    C_C = C_original[ix_c]
    C_EC = C_original[ix_ec]

    # Regularize C_C for inversion
    C_C_reg = 0.5 * (C_C + C_C.conj().T)
    reg = 1e-10 * np.eye(len(complement))
    try:
        C_C_inv = np.linalg.inv(C_C_reg + reg)
    except np.linalg.LinAlgError:
        return 0.0

    # Conditional correlation: C_{E|C} = C_E - C_{EC} @ inv(C_C) @ C_{CE}
    C_cond = C_E - C_EC @ C_C_inv @ C_EC.conj().T
    C_cond = 0.5 * (C_cond + C_cond.conj().T)

    # The recovered state on erased sites uses the Schur complement prediction:
    C_E_recovered = C_EC @ C_C_inv @ C_EC.conj().T

    # Fidelity: 1 - ||C_E - C_E_recovered||_F^2 / ||C_E||_F^2
    diff_norm = np.linalg.norm(C_E - C_E_recovered, 'fro')
    orig_norm = np.linalg.norm(C_E, 'fro')

    if orig_norm < 1e-15:
        return 1.0

    fidelity = 1.0 - (diff_norm / orig_norm)**2
    return max(0.0, min(1.0, float(fidelity)))


def conditional_mutual_information(C: np.ndarray, A_nodes: list[int],
                                   B_nodes: list[int]) -> float:
    """Compute I(A:R|B) proxy using S_A + S_B - S_AB for the Dirac sea.

    For a QEC code, I(A:R|B) ~ 0 means the code protects information in A.
    We use: I(A:B) = S_A + S_B - S_{AB} as a proxy.
    When I(A:B) is high relative to S_A, the boundary B contains most of A's info.
    """
    S_A, _ = entanglement_entropy_from_C(C, A_nodes)
    S_B, _ = entanglement_entropy_from_C(C, B_nodes)
    AB_nodes = sorted(set(A_nodes) | set(B_nodes))
    S_AB, _ = entanglement_entropy_from_C(C, AB_nodes)

    # Mutual information
    I_AB = S_A + S_B - S_AB
    return float(I_AB)


# ---------------------------------------------------------------------------
# Code distance measurement
# ---------------------------------------------------------------------------

def measure_code_distance(C: np.ndarray, A_nodes: list[int],
                          adj: dict[int, list[int]],
                          n_trials: int = 10, seed: int = 42) -> dict:
    """Sweep erasure fraction and measure recovery fidelity.

    Code distance: largest erasure fraction with F > 0.5.
    """
    rng = np.random.default_rng(seed)
    fractions = np.arange(0.1, 0.95, 0.1)
    nA = len(A_nodes)

    results = []
    for frac in fractions:
        n_erase = max(1, int(frac * nA))
        fidelities = []

        for trial in range(n_trials):
            # Randomly select nodes to erase from A
            perm = rng.permutation(nA)
            erased = [A_nodes[i] for i in perm[:n_erase]]
            F = recovery_fidelity(C, A_nodes, erased)
            fidelities.append(F)

        mean_F = float(np.mean(fidelities))
        std_F = float(np.std(fidelities))
        results.append({
            'frac': float(frac),
            'n_erase': n_erase,
            'mean_F': mean_F,
            'std_F': std_F,
            'min_F': float(np.min(fidelities)),
            'max_F': float(np.max(fidelities)),
        })

    # Code distance: largest fraction with mean F > 0.5
    code_distance = 0.0
    for r in results:
        if r['mean_F'] > 0.5:
            code_distance = r['frac']

    return {'erasure_sweep': results, 'code_distance': code_distance}


# ---------------------------------------------------------------------------
# Boundary entropy analysis
# ---------------------------------------------------------------------------

def boundary_nodes(adj: dict[int, list[int]], A_nodes: list[int],
                   n: int) -> list[int]:
    """Nodes in complement B that share an edge with A."""
    A_set = set(A_nodes)
    bnd = set()
    for i in A_nodes:
        for j in adj[i]:
            if j not in A_set:
                bnd.add(j)
    return sorted(bnd)


def boundary_entropy_test(C: np.ndarray, A_nodes: list[int],
                           adj: dict[int, list[int]], n: int) -> dict:
    """Test whether S_A ~ S_{boundary(A)}.

    If true, the Petz recovery map can reconstruct A from the boundary,
    indicating QEC structure.
    """
    bnd_nodes = boundary_nodes(adj, A_nodes, n)

    S_A, nu_A = entanglement_entropy_from_C(C, A_nodes)
    S_bnd, nu_bnd = entanglement_entropy_from_C(C, bnd_nodes)

    # Also compute mutual information between A and boundary
    I_A_bnd = conditional_mutual_information(C, A_nodes, bnd_nodes)

    # Recovery capacity: fraction of S_A captured by boundary
    if S_A > 1e-10:
        recovery_ratio = I_A_bnd / S_A
    else:
        recovery_ratio = 1.0

    return {
        'S_A': S_A,
        'S_bnd': S_bnd,
        'I_A_bnd': I_A_bnd,
        'recovery_ratio': min(1.0, recovery_ratio),
        'n_A': len(A_nodes),
        'n_bnd': len(bnd_nodes),
    }


# ---------------------------------------------------------------------------
# Safe linear regression
# ---------------------------------------------------------------------------

def safe_linregress(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or np.std(x) < 1e-12:
        return 0.0, np.mean(y), 0.0
    res = linregress(x, y)
    return res.slope, res.intercept, res.rvalue**2


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def main():
    print("=" * 80)
    print("QUANTUM ERROR CORRECTION IN THE SELF-GRAVITATING DIRAC SEA")
    print("=" * 80)
    print()
    print("Does the Dirac sea have holographic QEC structure?")
    print("  - Can erased information in region A be recovered from boundary?")
    print("  - Does gravity INCREASE or DECREASE the code distance?")
    print()
    print(f"Parameters: side={SIDE}, n={SIDE**2}, MASS={MASS}, MU2={MU2}, "
          f"DT={DT}, N_STEPS={N_STEPS}")
    print(f"Self-gravity: G={G_SELF}, Screening: mu^2={MU2}")
    print()

    # Build lattice
    n, pos, adj, col = build_lattice_2d(SIDE)
    center = (SIDE // 2) * SIDE + (SIDE // 2)

    # ======================================================================
    # Evolve: gravitating and free
    # ======================================================================
    print("Evolving with self-gravity (G=10)...")
    t0 = time.time()
    psi_grav, H_grav = evolve_and_get_final_H(n, pos, adj, col, G_SELF)
    print(f"  Done in {time.time() - t0:.1f}s")

    print("Evolving free (G=0)...")
    t0 = time.time()
    psi_free, H_free = evolve_and_get_final_H(n, pos, adj, col, 0.0)
    print(f"  Done in {time.time() - t0:.1f}s")

    # ======================================================================
    # Dirac sea correlation matrices
    # ======================================================================
    print("\nComputing Dirac sea correlation matrices...")
    C_grav, eigs_grav, n_filled_g = dirac_sea_correlation_matrix(H_grav)
    C_free, eigs_free, n_filled_f = dirac_sea_correlation_matrix(H_free)

    print(f"  Filled modes: grav={n_filled_g}, free={n_filled_f}")
    print(f"  Energy range: grav=[{eigs_grav[0]:.4f}, {eigs_grav[-1]:.4f}], "
          f"free=[{eigs_free[0]:.4f}, {eigs_free[-1]:.4f}]")

    # ======================================================================
    # TEST 1: Boundary entropy test across radii
    # ======================================================================
    print("\n\n" + "=" * 80)
    print("TEST 1: BOUNDARY ENTROPY TEST  (S_A vs S_{boundary})")
    print("Does S_A ~ S_{boundary(A)}?  If so => QEC structure.")
    print("=" * 80)

    max_R = SIDE // 2
    radii = list(range(1, max_R + 1))

    header = (f"  {'R':>2} {'|A|':>4} {'|bnd|':>5} "
              f"{'S_A_g':>9} {'S_bnd_g':>9} {'I/S_g':>7} "
              f"{'S_A_f':>9} {'S_bnd_f':>9} {'I/S_f':>7}")
    print()
    print(header)
    print("  " + "-" * (len(header) - 2))

    bnd_data_grav = []
    bnd_data_free = []

    for R in radii:
        A_nodes, bnd_edges = bfs_ball(adj, center, R, n)
        if len(A_nodes) == 0 or len(A_nodes) >= n:
            continue

        bg = boundary_entropy_test(C_grav, A_nodes, adj, n)
        bf = boundary_entropy_test(C_free, A_nodes, adj, n)

        bnd_data_grav.append(bg)
        bnd_data_free.append(bf)

        print(f"  {R:>2} {bg['n_A']:>4} {bg['n_bnd']:>5} "
              f"{bg['S_A']:>9.4f} {bg['S_bnd']:>9.4f} {bg['recovery_ratio']:>7.4f} "
              f"{bf['S_A']:>9.4f} {bf['S_bnd']:>9.4f} {bf['recovery_ratio']:>7.4f}")

    # Recovery ratio statistics
    print("\n  Recovery ratio I(A:bnd)/S_A statistics:")
    for tag, data in [("grav", bnd_data_grav), ("free", bnd_data_free)]:
        ratios = [d['recovery_ratio'] for d in data]
        if ratios:
            print(f"    {tag}: mean={np.mean(ratios):.4f}, "
                  f"min={np.min(ratios):.4f}, max={np.max(ratios):.4f}")

    # ======================================================================
    # TEST 2: Erasure sweep - code distance measurement
    # ======================================================================
    print("\n\n" + "=" * 80)
    print("TEST 2: ERASURE SWEEP - CODE DISTANCE MEASUREMENT")
    print("Erase fraction f of A nodes, measure recovery fidelity.")
    print("Code distance = largest f with mean fidelity > 0.5")
    print("=" * 80)

    # Use R = side//3 as the canonical region
    R_test = max(2, SIDE // 3)
    A_nodes_test, bnd_edges_test = bfs_ball(adj, center, R_test, n)
    print(f"\n  Region A: BFS ball R={R_test}, |A|={len(A_nodes_test)}, "
          f"|boundary|={bnd_edges_test}")

    print("\n  --- GRAVITATING (G=10) ---")
    cd_grav = measure_code_distance(C_grav, A_nodes_test, adj)

    print(f"\n  {'frac':>6} {'n_erase':>7} {'mean_F':>8} {'std_F':>8} "
          f"{'min_F':>8} {'max_F':>8}")
    print("  " + "-" * 52)
    for r in cd_grav['erasure_sweep']:
        marker = " <-- code dist" if abs(r['frac'] - cd_grav['code_distance']) < 0.01 else ""
        print(f"  {r['frac']:>6.2f} {r['n_erase']:>7} {r['mean_F']:>8.4f} "
              f"{r['std_F']:>8.4f} {r['min_F']:>8.4f} {r['max_F']:>8.4f}{marker}")
    print(f"\n  Code distance (gravity): {cd_grav['code_distance']:.2f}")

    print("\n  --- FREE (G=0) ---")
    cd_free = measure_code_distance(C_free, A_nodes_test, adj)

    print(f"\n  {'frac':>6} {'n_erase':>7} {'mean_F':>8} {'std_F':>8} "
          f"{'min_F':>8} {'max_F':>8}")
    print("  " + "-" * 52)
    for r in cd_free['erasure_sweep']:
        marker = " <-- code dist" if abs(r['frac'] - cd_free['code_distance']) < 0.01 else ""
        print(f"  {r['frac']:>6.2f} {r['n_erase']:>7} {r['mean_F']:>8.4f} "
              f"{r['std_F']:>8.4f} {r['min_F']:>8.4f} {r['max_F']:>8.4f}{marker}")
    print(f"\n  Code distance (free):    {cd_free['code_distance']:.2f}")

    # ======================================================================
    # TEST 3: Code distance vs region size
    # ======================================================================
    print("\n\n" + "=" * 80)
    print("TEST 3: CODE DISTANCE VS REGION SIZE")
    print("Does code distance depend on R?")
    print("=" * 80)

    cd_vs_R_grav = []
    cd_vs_R_free = []

    print(f"\n  {'R':>2} {'|A|':>4} {'|bnd|':>5} {'cd_grav':>8} {'cd_free':>8} {'delta':>8}")
    print("  " + "-" * 42)

    for R in radii:
        A_nodes_r, bnd_r = bfs_ball(adj, center, R, n)
        if len(A_nodes_r) < 3 or len(A_nodes_r) >= n - 3:
            continue

        cdg = measure_code_distance(C_grav, A_nodes_r, adj, n_trials=5)
        cdf = measure_code_distance(C_free, A_nodes_r, adj, n_trials=5)

        cd_vs_R_grav.append({'R': R, 'nA': len(A_nodes_r), 'bnd': bnd_r,
                             'cd': cdg['code_distance']})
        cd_vs_R_free.append({'R': R, 'nA': len(A_nodes_r), 'bnd': bnd_r,
                             'cd': cdf['code_distance']})

        delta = cdg['code_distance'] - cdf['code_distance']
        print(f"  {R:>2} {len(A_nodes_r):>4} {bnd_r:>5} "
              f"{cdg['code_distance']:>8.2f} {cdf['code_distance']:>8.2f} "
              f"{delta:>+8.2f}")

    # ======================================================================
    # TEST 4: Conditional entropy diagnostic
    # ======================================================================
    print("\n\n" + "=" * 80)
    print("TEST 4: PURITY AND BOUNDARY-INTERIOR ENTROPY DIAGNOSTIC")
    print("For a pure Dirac sea: S(A) = S(B) exactly (purity check).")
    print("QEC structure: S(A) ~ S(boundary_layer) where boundary_layer")
    print("is the 1-hop shell around A (not the full complement).")
    print("=" * 80)

    # For pure states S(A|B) = -S(A) always, so instead compare
    # S(interior of A) vs S(A) to see if bulk adds entropy beyond boundary.

    print(f"\n  {'R':>2} {'S_A_g':>8} {'S_B_g':>8} {'purity_g':>9} "
          f"{'S_A_f':>8} {'S_B_f':>8} {'purity_f':>9} "
          f"{'S_bnd1_g':>9} {'S_bnd1_f':>9}")
    print("  " + "-" * 82)

    cond_data_grav = []
    cond_data_free = []

    for R in radii:
        A_nodes_r, _ = bfs_ball(adj, center, R, n)
        if len(A_nodes_r) == 0 or len(A_nodes_r) >= n:
            continue

        B_nodes = sorted(set(range(n)) - set(A_nodes_r))
        if len(B_nodes) == 0:
            continue

        S_A_g, _ = entanglement_entropy_from_C(C_grav, A_nodes_r)
        S_B_g, _ = entanglement_entropy_from_C(C_grav, B_nodes)
        purity_g = abs(S_A_g - S_B_g) / max(S_A_g, 1e-15)

        S_A_f, _ = entanglement_entropy_from_C(C_free, A_nodes_r)
        S_B_f, _ = entanglement_entropy_from_C(C_free, B_nodes)
        purity_f = abs(S_A_f - S_B_f) / max(S_A_f, 1e-15)

        # 1-hop boundary shell entropy
        bnd1 = boundary_nodes(adj, A_nodes_r, n)
        S_bnd1_g, _ = entanglement_entropy_from_C(C_grav, bnd1)
        S_bnd1_f, _ = entanglement_entropy_from_C(C_free, bnd1)

        # QEC ratio: S(A)/S(boundary_shell) -- should be ~ 1 for QEC
        qec_ratio_g = S_A_g / S_bnd1_g if S_bnd1_g > 1e-10 else 0.0
        qec_ratio_f = S_A_f / S_bnd1_f if S_bnd1_f > 1e-10 else 0.0

        cond_data_grav.append({'R': R, 'S_A': S_A_g, 'S_bnd1': S_bnd1_g,
                               'ratio': qec_ratio_g})
        cond_data_free.append({'R': R, 'S_A': S_A_f, 'S_bnd1': S_bnd1_f,
                               'ratio': qec_ratio_f})

        print(f"  {R:>2} {S_A_g:>8.4f} {S_B_g:>8.4f} {purity_g:>9.6f} "
              f"{S_A_f:>8.4f} {S_B_f:>8.4f} {purity_f:>9.6f} "
              f"{S_bnd1_g:>9.4f} {S_bnd1_f:>9.4f}")

    print(f"\n  S(A)/S(boundary_shell) ratio (QEC ~ 1.0):")
    for tag, data in [("grav", cond_data_grav), ("free", cond_data_free)]:
        ratios = [d['ratio'] for d in data if d['ratio'] > 0]
        if ratios:
            print(f"    {tag}: mean={np.mean(ratios):.4f}, "
                  f"min={np.min(ratios):.4f}, max={np.max(ratios):.4f}")

    # ======================================================================
    # SUMMARY
    # ======================================================================
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"\n1. CODE DISTANCE (region R={R_test}, |A|={len(A_nodes_test)}):")
    print(f"   Gravity (G={G_SELF}):  code distance = {cd_grav['code_distance']:.2f}")
    print(f"   Free    (G=0):    code distance = {cd_free['code_distance']:.2f}")
    delta_cd = cd_grav['code_distance'] - cd_free['code_distance']
    if delta_cd > 0.05:
        print(f"   ==> Gravity INCREASES code distance by {delta_cd:.2f}")
        print(f"       Self-gravity enhances QEC protection.")
    elif delta_cd < -0.05:
        print(f"   ==> Gravity DECREASES code distance by {abs(delta_cd):.2f}")
        print(f"       Self-gravity degrades QEC protection.")
    else:
        print(f"   ==> Code distance roughly equal (delta={delta_cd:.2f})")

    print(f"\n2. BOUNDARY RECOVERY RATIO (I(A:bnd)/S_A):")
    for tag, data in [("Gravity", bnd_data_grav), ("Free", bnd_data_free)]:
        ratios = [d['recovery_ratio'] for d in data]
        if ratios:
            mean_r = np.mean(ratios)
            print(f"   {tag:>8}: mean ratio = {mean_r:.4f}", end="")
            if mean_r > 0.8:
                print("  (STRONG boundary encoding)")
            elif mean_r > 0.5:
                print("  (MODERATE boundary encoding)")
            else:
                print("  (WEAK boundary encoding)")

    print(f"\n3. S(A)/S(boundary_shell) RATIO (QEC ~ 1.0):")
    for tag, data in [("Gravity", cond_data_grav), ("Free", cond_data_free)]:
        if data:
            ratios = [d['ratio'] for d in data if d['ratio'] > 0]
            if ratios:
                mean_r = np.mean(ratios)
                print(f"   {tag:>8}: mean S(A)/S(bnd_shell) = {mean_r:.4f}", end="")
                if 0.5 < mean_r < 2.0:
                    print("  (QEC-like: entropy ~ boundary shell)")
                elif mean_r < 0.5:
                    print("  (Sub-boundary: strong QEC)")
                else:
                    print("  (Volume-law: entropy exceeds boundary)")

    print(f"\n4. GRAVITY'S EFFECT ON QEC:")
    if cd_vs_R_grav and cd_vs_R_free:
        mean_cd_g = np.mean([d['cd'] for d in cd_vs_R_grav])
        mean_cd_f = np.mean([d['cd'] for d in cd_vs_R_free])
        print(f"   Mean code distance across radii: grav={mean_cd_g:.2f}, "
              f"free={mean_cd_f:.2f}")

        if mean_cd_g > mean_cd_f + 0.05:
            print(f"   ==> GRAVITY ENHANCES QEC")
            print(f"       Consistent with holographic QEC (AdS/CFT-like)")
        elif mean_cd_g < mean_cd_f - 0.05:
            print(f"   ==> GRAVITY DEGRADES QEC")
            print(f"       Gravitational focusing disrupts error correction")
        else:
            print(f"   ==> GRAVITY NEUTRAL on QEC (within noise)")

    # ======================================================================
    # Plot
    # ======================================================================
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 11))
        fig.suptitle('Quantum Error Correction in Self-Gravitating Dirac Sea\n'
                     f'side={SIDE}, G={G_SELF}, MU2={MU2}, {N_STEPS} CN steps',
                     fontsize=13)

        # (a) Recovery fidelity vs erasure fraction
        ax = axes[0, 0]
        fracs_g = [r['frac'] for r in cd_grav['erasure_sweep']]
        F_g = [r['mean_F'] for r in cd_grav['erasure_sweep']]
        Fstd_g = [r['std_F'] for r in cd_grav['erasure_sweep']]
        fracs_f = [r['frac'] for r in cd_free['erasure_sweep']]
        F_f = [r['mean_F'] for r in cd_free['erasure_sweep']]
        Fstd_f = [r['std_F'] for r in cd_free['erasure_sweep']]

        ax.errorbar(fracs_g, F_g, yerr=Fstd_g, marker='o', color='red',
                    label=f'G={G_SELF} (grav)', capsize=3)
        ax.errorbar(fracs_f, F_f, yerr=Fstd_f, marker='s', color='blue',
                    label='G=0 (free)', capsize=3)
        ax.axhline(0.5, color='gray', linestyle='--', alpha=0.5, label='F=0.5 threshold')
        ax.set_xlabel('Erasure fraction')
        ax.set_ylabel('Recovery fidelity')
        ax.set_title(f'(a) Erasure test (R={R_test}, |A|={len(A_nodes_test)})')
        ax.legend(fontsize=8)
        ax.set_ylim(-0.05, 1.05)

        # (b) Code distance vs R
        ax = axes[0, 1]
        if cd_vs_R_grav and cd_vs_R_free:
            Rs_g = [d['R'] for d in cd_vs_R_grav]
            cds_g = [d['cd'] for d in cd_vs_R_grav]
            Rs_f = [d['R'] for d in cd_vs_R_free]
            cds_f = [d['cd'] for d in cd_vs_R_free]
            ax.plot(Rs_g, cds_g, 'ro-', label=f'G={G_SELF}', markersize=6)
            ax.plot(Rs_f, cds_f, 'bs--', label='G=0', markersize=6)
        ax.set_xlabel('BFS radius R')
        ax.set_ylabel('Code distance')
        ax.set_title('(b) Code distance vs region size')
        ax.legend(fontsize=8)

        # (c) Boundary recovery ratio vs R
        ax = axes[1, 0]
        if bnd_data_grav and bnd_data_free:
            Rs_bg = list(range(1, len(bnd_data_grav) + 1))
            rr_g = [d['recovery_ratio'] for d in bnd_data_grav]
            rr_f = [d['recovery_ratio'] for d in bnd_data_free]
            ax.plot(Rs_bg, rr_g, 'ro-', label=f'G={G_SELF}', markersize=6)
            ax.plot(Rs_bg, rr_f, 'bs--', label='G=0', markersize=6)
        ax.set_xlabel('BFS radius R')
        ax.set_ylabel('I(A:bnd) / S(A)')
        ax.set_title('(c) Boundary recovery ratio')
        ax.legend(fontsize=8)
        ax.set_ylim(-0.05, 1.05)

        # (d) Conditional entropy ratio vs R
        ax = axes[1, 1]
        if cond_data_grav and cond_data_free:
            Rs_cg = [d['R'] for d in cond_data_grav]
            cr_g = [d['ratio'] for d in cond_data_grav]
            cr_f = [d['ratio'] for d in cond_data_free]
            ax.plot(Rs_cg, cr_g, 'ro-', label=f'G={G_SELF}', markersize=6)
            ax.plot(Rs_cg, cr_f, 'bs--', label='G=0', markersize=6)
        ax.set_xlabel('BFS radius R')
        ax.set_ylabel('|S(A|B)| / S(A)')
        ax.set_title('(d) Conditional entropy ratio (QEC: should be ~ 0)')
        ax.legend(fontsize=8)

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    main()
