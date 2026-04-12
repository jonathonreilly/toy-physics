#!/usr/bin/env python3
"""Area-law entanglement entropy for self-gravitating staggered fermions.

Tests whether entanglement entropy of a parity-coupled staggered fermion
under self-gravity (screened Poisson) scales with boundary area or volume.

Probe:
  - 2D periodic square lattices, side = 6..14
  - Gaussian wavepacket at center, 30 Crank-Nicolson steps
  - Self-gravity: (L + mu^2)Phi = G * rho, rho = |psi|^2
  - Parity coupling: H_diag = (m + Phi) * epsilon(x)
  - Staggered hopping: -0.5j/d forward, +0.5j/d backward
  - Three partition geometries: planar cut, circular, random
  - von Neumann entropy from Schmidt decomposition of |psi>

Physics:
  For a free lattice fermion the entanglement entropy across a planar cut
  is expected to obey an area law: S ~ L^{d-1}.  Self-gravity can modify
  this by correlating the wavefunction with its own density.  We check
  whether the area-law coefficient changes and whether volume scaling
  is preferred.
"""

from __future__ import annotations

import math
import sys
import time

import numpy as np
from scipy import sparse
from scipy.sparse import eye as speye
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

# ---------------------------------------------------------------------------
# Physical parameters
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
G_SELF = 10.0
N_STEPS = 30
SIDES = [6, 8, 10, 12, 14]
SIGMA = 1.5  # Gaussian width in lattice units


def build_lattice_2d(side: int):
    """Build a 2D periodic square lattice.

    Returns
    -------
    n : int
        Number of sites.
    pos : ndarray, shape (n, 2)
        Coordinates of each site.
    adj : dict[int, list[int]]
        Adjacency list (periodic boundary).
    col : ndarray, shape (n,)
        Checkerboard colouring: 0 or 1.
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

            # periodic neighbours
            for dix, diy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                jx = (ix + dix) % side
                jy = (iy + diy) % side
                jdx = jx * side + jy
                adj[idx].append(jdx)

    return n, pos, adj, col


def solve_poisson(adj: dict, n: int, rho: np.ndarray, mu2: float, G: float) -> np.ndarray:
    """Solve screened Poisson (L + mu^2) Phi = G * rho on the graph."""
    if G == 0.0:
        return np.zeros(n)

    # Build graph Laplacian
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
    """Build the staggered-fermion Hamiltonian with parity coupling."""
    H = sparse.lil_matrix((n, n), dtype=complex)

    # Diagonal: parity coupling
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)

    # Hopping
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            # periodic wrapping can give large d; clamp to 1 for nearest-neighbour
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


def evolve(n: int, pos: np.ndarray, adj: dict, col: np.ndarray,
           G: float) -> np.ndarray:
    """Evolve a Gaussian wavepacket for N_STEPS under self-gravity G."""
    # Gaussian at center
    cx, cy = (pos[:, 0].max() + pos[:, 0].min()) / 2, (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)

    for _ in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = solve_poisson(adj, n, rho, MU2, G)
        H = build_hamiltonian(n, pos, adj, col, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)  # maintain normalisation

    return psi


def von_neumann_entropy(psi: np.ndarray, sites_A: list[int], sites_B: list[int]) -> float:
    """Compute von Neumann entropy of the reduced density matrix rho_A.

    For a single-particle pure state |psi> on a graph, the reduced density
    matrix for subsystem A is simply the |A| x |A| matrix:

        rho_A[i,j] = psi[a_i] * conj(psi[a_j])    (rank-1 projector traced over B)

    But this is rank 1 and gives S = 0 for any pure product state.

    The correct approach for the single-particle Hilbert space: the state
    |psi> lives in H = C^n.  We split sites into A and B.  The "entanglement"
    of a single-particle state across a bipartition is captured by treating
    the amplitude vector as a matrix M[a, b] where a indexes A-sites and
    b indexes B-sites.  For this to work we need n = |A| * |B|, which is
    not generally true.

    Instead, we use the correct single-particle entanglement entropy:
    the state vector restricted to A has norm^2 = p_A, and to B has p_B = 1 - p_A.
    The Shannon entropy of (p_A, p_B) gives the "which-subsystem" entropy.
    But for finer structure, we compute the eigenvalues of the |A| x |A|
    matrix rho_A = outer product projected:

        rho_A[i,j] = psi[a_i] * conj(psi[a_j])

    This has rank 1, so S = 0 for a pure state -- that's correct for a
    single particle.  To get nontrivial entanglement entropy we need a
    many-body state.

    For this probe, we use the CORRELATION MATRIX method: given the
    single-particle state psi, we build the one-body density matrix
    C[i,j] = psi[i] * conj(psi[j]) restricted to subsystem A.
    The eigenvalues nu_k of C_A give the entanglement entropy via:
        S = -sum_k [nu_k * log(nu_k) + (1-nu_k) * log(1-nu_k)]
    This is the entanglement entropy of the Slater determinant with
    one filled orbital.
    """
    nA = len(sites_A)
    if nA == 0:
        return 0.0

    # Correlation matrix restricted to A
    psi_A = psi[sites_A]
    C_A = np.outer(psi_A, np.conj(psi_A))

    # Eigenvalues (should be real, non-negative)
    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-30, 1.0 - 1e-30)

    # Single-particle entanglement entropy (free-fermion formula)
    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))
    return S


def partition_planar(side: int, n: int, pos: np.ndarray):
    """Left/right half-plane partition. Boundary = side edges."""
    mid = side / 2
    A = [i for i in range(n) if pos[i, 0] < mid]
    B = [i for i in range(n) if pos[i, 0] >= mid]
    # Boundary edges: edges crossing the cut
    boundary = side  # periodic lattice: side vertical bonds cross x = mid
    return A, B, boundary


def partition_circular(side: int, n: int, pos: np.ndarray, adj: dict):
    """Inner/outer circular partition. Boundary ~ circumference."""
    cx = (side - 1) / 2.0
    cy = (side - 1) / 2.0
    r_cut = side / 4.0
    A = [i for i in range(n) if (pos[i, 0] - cx)**2 + (pos[i, 1] - cy)**2 <= r_cut**2]
    B = [i for i in range(n) if i not in set(A)]

    # Count boundary edges
    setA = set(A)
    boundary = 0
    for i in A:
        for j in adj[i]:
            if j not in setA:
                boundary += 1
    return A, B, boundary


def partition_random(side: int, n: int, adj: dict, seed: int = 42):
    """Random half-partition. Boundary typically proportional to volume."""
    rng = np.random.default_rng(seed)
    indices = rng.permutation(n)
    half = n // 2
    A = sorted(indices[:half].tolist())
    B = sorted(indices[half:].tolist())

    setA = set(A)
    boundary = 0
    for i in A:
        for j in adj[i]:
            if j not in setA:
                boundary += 1
    return A, B, boundary


def run_experiment():
    """Main experiment: sweep lattice sizes, compute entropies."""
    print("=" * 78)
    print("FRONTIER AREA-LAW ENTROPY PROBE")
    print("Staggered fermion with parity coupling + screened-Poisson self-gravity")
    print("=" * 78)
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, G_SELF={G_SELF}, "
          f"N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print(f"Lattice sides: {SIDES}")
    print()

    results = {
        'planar': {'grav': [], 'free': [], 'boundary': [], 'volume': []},
        'circular': {'grav': [], 'free': [], 'boundary': [], 'volume': []},
        'random': {'grav': [], 'free': [], 'boundary': [], 'volume': []},
    }

    for side in SIDES:
        t0 = time.time()
        n, pos, adj, col = build_lattice_2d(side)
        volume = n // 2  # |A| for half-partition

        print(f"--- side={side}, n={n} ---")

        # Evolve
        psi_grav = evolve(n, pos, adj, col, G_SELF)
        psi_free = evolve(n, pos, adj, col, 0.0)

        # Partitions
        A_p, B_p, bnd_p = partition_planar(side, n, pos)
        A_c, B_c, bnd_c = partition_circular(side, n, pos, adj)
        A_r, B_r, bnd_r = partition_random(side, n, adj)

        # Entropies
        for label, A, B, bnd in [
            ('planar', A_p, B_p, bnd_p),
            ('circular', A_c, B_c, bnd_c),
            ('random', A_r, B_r, bnd_r),
        ]:
            # Ensure equal partition sizes for SVD reshape
            # If unequal, pad the smaller side (only relevant for circular/random)
            if len(A) == 0 or len(B) == 0:
                print(f"  {label}: SKIP (degenerate partition)")
                continue

            S_grav = von_neumann_entropy(psi_grav, A, B)
            S_free = von_neumann_entropy(psi_free, A, B)

            results[label]['grav'].append(S_grav)
            results[label]['free'].append(S_free)
            results[label]['boundary'].append(bnd)
            results[label]['volume'].append(len(A))

            print(f"  {label}: |A|={len(A)}, |B|={len(B)}, "
                  f"boundary={bnd}, S_grav={S_grav:.6f}, S_free={S_free:.6f}")

        dt_sec = time.time() - t0
        print(f"  elapsed: {dt_sec:.1f}s")
        print()

    # ------------------------------------------------------------------
    # Analysis: fit S vs boundary and S vs volume
    # ------------------------------------------------------------------
    print("=" * 78)
    print("SCALING ANALYSIS")
    print("=" * 78)

    for label in ['planar', 'circular', 'random']:
        d = results[label]
        if len(d['boundary']) < 3:
            print(f"\n{label}: insufficient data for fit")
            continue

        bnd = np.array(d['boundary'], dtype=float)
        vol = np.array(d['volume'], dtype=float)

        for tag, S_arr in [('GRAV', d['grav']), ('FREE', d['free'])]:
            S = np.array(S_arr)

            # S vs boundary
            sl_b = linregress(bnd, S)
            # S vs volume
            sl_v = linregress(vol, S)

            print(f"\n  {label} / {tag}:")
            print(f"    S vs boundary:  S = {sl_b.slope:.6f} * bnd + {sl_b.intercept:.6f}  "
                  f"R^2 = {sl_b.rvalue**2:.6f}")
            print(f"    S vs volume:    S = {sl_v.slope:.6f} * vol + {sl_v.intercept:.6f}  "
                  f"R^2 = {sl_v.rvalue**2:.6f}")

            if sl_b.rvalue**2 > sl_v.rvalue**2:
                print(f"    --> AREA LAW preferred (R^2_bnd > R^2_vol)")
            else:
                print(f"    --> VOLUME LAW preferred (R^2_vol > R^2_bnd)")

    # ------------------------------------------------------------------
    # Gravity modification check
    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("GRAVITY MODIFICATION OF ENTROPY COEFFICIENT")
    print("=" * 78)

    for label in ['planar', 'circular', 'random']:
        d = results[label]
        if len(d['boundary']) < 3:
            continue

        bnd = np.array(d['boundary'], dtype=float)
        S_g = np.array(d['grav'])
        S_f = np.array(d['free'])

        sl_g = linregress(bnd, S_g)
        sl_f = linregress(bnd, S_f)

        ratio = sl_g.slope / sl_f.slope if abs(sl_f.slope) > 1e-12 else float('inf')
        diff_pct = (sl_g.slope - sl_f.slope) / abs(sl_f.slope) * 100 if abs(sl_f.slope) > 1e-12 else float('inf')

        print(f"\n  {label}:")
        print(f"    Gravity slope:  {sl_g.slope:.6f}")
        print(f"    Free slope:     {sl_f.slope:.6f}")
        print(f"    Ratio (G/F):    {ratio:.4f}")
        print(f"    Difference:     {diff_pct:+.2f}%")

    # ------------------------------------------------------------------
    # Raw data table
    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("RAW DATA TABLE")
    print("=" * 78)
    print(f"{'side':>4} {'partition':>10} {'|A|':>5} {'bnd':>5} "
          f"{'S_grav':>10} {'S_free':>10} {'dS':>10}")
    print("-" * 66)

    for label in ['planar', 'circular', 'random']:
        d = results[label]
        for k in range(len(d['boundary'])):
            side = SIDES[k]
            dS = d['grav'][k] - d['free'][k]
            print(f"{side:>4} {label:>10} {d['volume'][k]:>5} {d['boundary'][k]:>5} "
                  f"{d['grav'][k]:>10.6f} {d['free'][k]:>10.6f} {dS:>+10.6f}")

    # ------------------------------------------------------------------
    # Save plot
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 3, figsize=(15, 9))
        fig.suptitle('Entanglement Entropy: Area vs Volume Scaling\n'
                     f'Staggered fermion, MASS={MASS}, G={G_SELF}, {N_STEPS} CN steps',
                     fontsize=13)

        for col_idx, label in enumerate(['planar', 'circular', 'random']):
            d = results[label]
            if len(d['boundary']) < 2:
                continue

            bnd = np.array(d['boundary'], dtype=float)
            vol = np.array(d['volume'], dtype=float)
            S_g = np.array(d['grav'])
            S_f = np.array(d['free'])

            # S vs boundary
            ax = axes[0, col_idx]
            ax.plot(bnd, S_g, 'ro-', label='Self-gravity', markersize=6)
            ax.plot(bnd, S_f, 'bs-', label='Free', markersize=6)
            sl = linregress(bnd, S_g)
            ax.plot(bnd, sl.slope * bnd + sl.intercept, 'r--', alpha=0.5,
                    label=f'Grav fit R$^2$={sl.rvalue**2:.3f}')
            sl = linregress(bnd, S_f)
            ax.plot(bnd, sl.slope * bnd + sl.intercept, 'b--', alpha=0.5,
                    label=f'Free fit R$^2$={sl.rvalue**2:.3f}')
            ax.set_xlabel('Boundary size')
            ax.set_ylabel('von Neumann entropy S')
            ax.set_title(f'{label} partition')
            ax.legend(fontsize=8)

            # S vs volume
            ax = axes[1, col_idx]
            ax.plot(vol, S_g, 'ro-', label='Self-gravity', markersize=6)
            ax.plot(vol, S_f, 'bs-', label='Free', markersize=6)
            sl = linregress(vol, S_g)
            ax.plot(vol, sl.slope * vol + sl.intercept, 'r--', alpha=0.5,
                    label=f'Grav fit R$^2$={sl.rvalue**2:.3f}')
            sl = linregress(vol, S_f)
            ax.plot(vol, sl.slope * vol + sl.intercept, 'b--', alpha=0.5,
                    label=f'Free fit R$^2$={sl.rvalue**2:.3f}')
            ax.set_xlabel('Volume |A|')
            ax.set_ylabel('von Neumann entropy S')
            ax.set_title(f'{label} partition')
            ax.legend(fontsize=8)

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    run_experiment()
