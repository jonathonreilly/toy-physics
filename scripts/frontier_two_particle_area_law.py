#!/usr/bin/env python3
"""Two-particle (multi-filling) area-law entropy: species-counting test.

Tests whether the area-law entropy coefficient scales linearly with the
number of filled single-particle states (species counting), and whether
self-gravity modifies this scaling.

Physics:
  The Dirac sea fills all negative-energy modes of the staggered-fermion
  Hamiltonian.  The "k-particle Dirac sea" fills the k lowest-energy states.
  For free fermions on a lattice, the area-law coefficient alpha(k) in
  S = alpha * |boundary| should grow approximately linearly with k (each
  filled mode contributes independently to the boundary entanglement).

  Self-gravity (screened Poisson: (L + mu^2)Phi = G*rho) modifies the
  single-particle spectrum and can change the filling-dependent coefficient.

Method:
  1. Build 2D periodic lattice, evolve Gaussian wavepacket under CN steps
     with self-consistent gravity to get the final Hamiltonian H.
  2. Diagonalise H to get the full eigenspectrum.
  3. For each filling k, build the correlation matrix C = sum_{m<k} |phi_m><phi_m|.
  4. Restrict C to subsystem A (left half), compute entanglement entropy
     from eigenvalues of C_A via S = -sum[nu*ln(nu) + (1-nu)*ln(1-nu)].
  5. Vary lattice side to get S vs |boundary| at each k.
  6. Fit alpha(k) = S(k) / |boundary| and test linearity in k.

Lattice sides: 6, 8, 10 (eigensolve is O(n^3), n = side^2).
Fillings: k = 1, n//8, n//4, 3*n//8, n//2, 5*n//8, 3*n//4.
G values: 0 (free) and 10 (gravitating).
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
# Physical parameters (same as frontier_area_law_entropy.py)
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
G_VALUES = [0.0, 10.0]
N_STEPS = 30
SIDES = [6, 8, 10]
SIGMA = 1.5


def build_lattice_2d(side: int):
    """Build a 2D periodic square lattice."""
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


def solve_poisson(adj: dict, n: int, rho: np.ndarray, mu2: float, G: float) -> np.ndarray:
    """Solve screened Poisson (L + mu^2) Phi = G * rho on the graph."""
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
    """Build staggered-fermion Hamiltonian with parity coupling."""
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


def get_final_H(n: int, pos: np.ndarray, adj: dict, col: np.ndarray,
                G: float) -> np.ndarray:
    """Evolve Gaussian wavepacket, return the final Hamiltonian (dense)."""
    # Gaussian at center
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)

    for _ in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = solve_poisson(adj, n, rho, MU2, G)
        H = build_hamiltonian(n, pos, adj, col, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)

    # Build final H from final field configuration
    rho_f = np.abs(psi)**2
    phi_f = solve_poisson(adj, n, rho_f, MU2, G)
    H_final = build_hamiltonian(n, pos, adj, col, phi_f)
    return H_final.toarray()


def entropy_from_filling(evecs: np.ndarray, A_sites: list[int], k_fill: int) -> float:
    """Entanglement entropy from correlation matrix of k filled states.

    C[i,j] = sum_{m=0}^{k-1} phi_m(i) * conj(phi_m(j))
    C_A = C restricted to sites in A
    S = -sum [nu*ln(nu) + (1-nu)*ln(1-nu)]  for eigenvalues nu of C_A
    """
    if k_fill == 0:
        return 0.0

    # filled = evecs[:, :k_fill] are the k lowest eigenstates (columns)
    filled = evecs[:, :k_fill]

    # Correlation matrix restricted to A
    filled_A = filled[A_sites, :]  # shape (|A|, k)
    C_A = filled_A @ filled_A.conj().T  # shape (|A|, |A|)

    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)

    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))
    return float(S)


def partition_planar(side: int, n: int, pos: np.ndarray):
    """Left half partition. Returns (A_sites, boundary_size)."""
    mid = side / 2
    A = [i for i in range(n) if pos[i, 0] < mid]
    # Boundary: number of edges crossing the cut
    boundary = side  # periodic: 'side' vertical bonds cross x = mid
    return A, boundary


def main():
    print("=" * 80)
    print("TWO-PARTICLE AREA LAW: SPECIES-COUNTING TEST")
    print("=" * 80)
    print()
    print("Test: does the area-law coefficient alpha(k) = S / |boundary|")
    print("scale linearly with the number k of filled single-particle states?")
    print()
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print(f"Lattice sides: {SIDES}")
    print(f"G values: {G_VALUES}")
    print()

    # Storage: results[G][side] = dict with 'evals', 'evecs', 'A_sites', 'boundary', 'n'
    all_results: dict[float, dict[int, dict]] = {}

    # ------------------------------------------------------------------
    # Phase 1: Build Hamiltonians and diagonalise
    # ------------------------------------------------------------------
    print("-" * 80)
    print("PHASE 1: Hamiltonian construction and diagonalisation")
    print("-" * 80)

    for G in G_VALUES:
        all_results[G] = {}
        for side in SIDES:
            t0 = time.time()
            n, pos, adj, col = build_lattice_2d(side)
            print(f"  side={side}, n={n}, G={G:.1f} ... ", end="", flush=True)

            H_dense = get_final_H(n, pos, adj, col, G)
            evals, evecs = np.linalg.eigh(H_dense)

            A_sites, boundary = partition_planar(side, n, pos)

            all_results[G][side] = {
                'evals': evals,
                'evecs': evecs,
                'A_sites': A_sites,
                'boundary': boundary,
                'n': n,
            }

            dt = time.time() - t0
            print(f"done ({dt:.1f}s), spectrum range [{evals[0]:.4f}, {evals[-1]:.4f}]")

    # ------------------------------------------------------------------
    # Phase 2: Compute entropy for each filling
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("PHASE 2: Entropy vs filling for each (side, G)")
    print("-" * 80)

    # Define filling fractions (as fractions of n)
    fill_fracs = [1, 1/8, 1/4, 3/8, 1/2, 5/8, 3/4]
    fill_labels = ["k=1", "n/8", "n/4", "3n/8", "n/2", "5n/8", "3n/4"]

    # Results storage: entropy_data[G][side] = list of (k, S, boundary)
    entropy_data: dict[float, dict[int, list]] = {G: {} for G in G_VALUES}

    for G in G_VALUES:
        print(f"\n  G = {G:.1f}")
        for side in SIDES:
            info = all_results[G][side]
            n = info['n']
            evecs = info['evecs']
            A_sites = info['A_sites']
            boundary = info['boundary']

            fillings = []
            for frac in fill_fracs:
                if frac == 1:
                    k = 1  # literal 1 state
                else:
                    k = max(1, int(round(frac * n)))
                if k not in [f[0] for f in fillings]:
                    fillings.append((k, fill_labels[fill_fracs.index(frac)]))

            entries = []
            for k, label in fillings:
                S = entropy_from_filling(evecs, A_sites, k)
                entries.append((k, S, boundary, label))

            entropy_data[G][side] = entries

            # Print table
            hdr = f"    side={side}, n={n}, |A|={len(A_sites)}, boundary={boundary}"
            print(hdr)
            print(f"    {'k':>5} {'label':>6} {'S':>10} {'alpha=S/bnd':>12}")
            for k, S, bnd, label in entries:
                alpha = S / bnd if bnd > 0 else 0.0
                print(f"    {k:>5} {label:>6} {S:>10.6f} {alpha:>12.6f}")

    # ------------------------------------------------------------------
    # Phase 3: Test linearity of alpha(k)
    # ------------------------------------------------------------------
    print()
    print("=" * 80)
    print("PHASE 3: LINEARITY OF alpha(k) IN FILLING NUMBER k")
    print("=" * 80)

    for G in G_VALUES:
        print(f"\n  G = {G:.1f}")
        print(f"  {'side':>4} {'slope':>10} {'intercept':>10} {'R^2':>8} {'alpha(1)':>10} {'alpha(n/2)':>10}")
        print(f"  {'-'*60}")

        for side in SIDES:
            entries = entropy_data[G][side]
            n = all_results[G][side]['n']
            boundary = all_results[G][side]['boundary']

            ks = np.array([e[0] for e in entries], dtype=float)
            alphas = np.array([e[1] / boundary for e in entries])

            if len(ks) >= 3:
                sl = linregress(ks, alphas)
                r2 = sl.rvalue**2
            else:
                sl = type('obj', (object,), {'slope': 0, 'intercept': 0})()
                r2 = 0.0

            alpha_1 = alphas[0] if len(alphas) > 0 else 0.0
            # Find alpha at n/2
            half_idx = None
            for idx, (k, S, bnd, label) in enumerate(entries):
                if label == "n/2":
                    half_idx = idx
                    break
            alpha_half = alphas[half_idx] if half_idx is not None else alphas[-1]

            print(f"  {side:>4} {sl.slope:>10.6f} {sl.intercept:>10.6f} {r2:>8.4f} "
                  f"{alpha_1:>10.6f} {alpha_half:>10.6f}")

    # ------------------------------------------------------------------
    # Phase 4: Gravity modification of the filling-dependent coefficient
    # ------------------------------------------------------------------
    print()
    print("=" * 80)
    print("PHASE 4: GRAVITY MODIFICATION OF FILLING-DEPENDENT COEFFICIENT")
    print("=" * 80)

    for side in SIDES:
        print(f"\n  side={side}")
        entries_free = entropy_data[0.0][side]
        entries_grav = entropy_data[10.0][side]

        print(f"  {'k':>5} {'S_free':>10} {'S_grav':>10} {'dS':>10} {'dS/S_free':>10}")
        print(f"  {'-'*50}")

        for i in range(len(entries_free)):
            k = entries_free[i][0]
            S_f = entries_free[i][1]
            S_g = entries_grav[i][1]
            dS = S_g - S_f
            ratio = dS / S_f if abs(S_f) > 1e-12 else float('inf')
            print(f"  {k:>5} {S_f:>10.6f} {S_g:>10.6f} {dS:>+10.6f} {ratio:>+10.4f}")

    # ------------------------------------------------------------------
    # Phase 5: Cross-side scaling at fixed filling fraction
    # ------------------------------------------------------------------
    print()
    print("=" * 80)
    print("PHASE 5: S VS BOUNDARY AT FIXED FILLING FRACTION (AREA LAW TEST)")
    print("=" * 80)
    print()
    print("For each filling fraction, fit S = alpha * boundary + intercept")
    print()

    # Collect (boundary, S) pairs for each filling label and G
    for G in G_VALUES:
        print(f"  G = {G:.1f}")
        print(f"  {'filling':>8} {'alpha':>10} {'intercept':>10} {'R^2':>8}")
        print(f"  {'-'*42}")

        # Get all unique labels in order
        labels_seen = []
        for side in SIDES:
            for _, _, _, label in entropy_data[G][side]:
                if label not in labels_seen:
                    labels_seen.append(label)

        for label in labels_seen:
            bnds = []
            Ss = []
            for side in SIDES:
                for k, S, bnd, lbl in entropy_data[G][side]:
                    if lbl == label:
                        bnds.append(float(bnd))
                        Ss.append(S)
                        break

            if len(bnds) >= 2:
                sl = linregress(np.array(bnds), np.array(Ss))
                print(f"  {label:>8} {sl.slope:>10.6f} {sl.intercept:>10.6f} {sl.rvalue**2:>8.4f}")
            else:
                print(f"  {label:>8}  (insufficient data)")

        print()

    # ------------------------------------------------------------------
    # Phase 6: Key prediction test
    # ------------------------------------------------------------------
    print("=" * 80)
    print("PHASE 6: KEY PREDICTION -- DOES alpha(k) GROW LINEARLY WITH k?")
    print("=" * 80)
    print()

    for G in G_VALUES:
        print(f"  G = {G:.1f}:")

        # Use the largest lattice for best statistics
        largest = max(SIDES)
        entries = entropy_data[G][largest]
        boundary = all_results[G][largest]['boundary']
        n = all_results[G][largest]['n']

        ks = np.array([e[0] for e in entries], dtype=float)
        alphas = np.array([e[1] / boundary for e in entries])

        # Linear fit
        sl = linregress(ks, alphas)
        r2 = sl.rvalue**2

        print(f"    Lattice side={largest}, n={n}, boundary={boundary}")
        print(f"    alpha(k) = {sl.slope:.6f} * k + {sl.intercept:.6f}")
        print(f"    R^2 = {r2:.6f}")
        print(f"    alpha(k=1) = {alphas[0]:.6f}")

        if r2 > 0.95:
            print(f"    ==> STRONG LINEAR SCALING CONFIRMED")
        elif r2 > 0.8:
            print(f"    ==> APPROXIMATELY LINEAR (some curvature)")
        else:
            print(f"    ==> NON-LINEAR -- species counting breaks down")
        print()

    # Gravity comparison
    print("  GRAVITY EFFECT ON LINEAR SLOPE:")
    largest = max(SIDES)
    for G in G_VALUES:
        entries = entropy_data[G][largest]
        boundary = all_results[G][largest]['boundary']
        ks = np.array([e[0] for e in entries], dtype=float)
        alphas = np.array([e[1] / boundary for e in entries])
        sl = linregress(ks, alphas)
        print(f"    G={G:>5.1f}: slope = {sl.slope:.6f}")

    slope_free = linregress(
        np.array([e[0] for e in entropy_data[0.0][largest]], dtype=float),
        np.array([e[1] / all_results[0.0][largest]['boundary'] for e in entropy_data[0.0][largest]])
    ).slope
    slope_grav = linregress(
        np.array([e[0] for e in entropy_data[10.0][largest]], dtype=float),
        np.array([e[1] / all_results[10.0][largest]['boundary'] for e in entropy_data[10.0][largest]])
    ).slope

    if abs(slope_free) > 1e-12:
        change_pct = (slope_grav - slope_free) / abs(slope_free) * 100
        print(f"    Change: {change_pct:+.2f}%")
        if change_pct < -5:
            print(f"    ==> Gravity REDUCES per-species entropy contribution")
            print(f"    ==> Consistent with gravitational entropy reduction")
        elif change_pct > 5:
            print(f"    ==> Gravity ENHANCES per-species entropy contribution")
        else:
            print(f"    ==> Gravity effect on slope is small (<5%)")

    # ------------------------------------------------------------------
    # Phase 7: Plot
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Two-Particle Area Law: Species Counting Test\n'
                     f'Staggered fermion, MASS={MASS}, N_STEPS={N_STEPS}',
                     fontsize=13)

        # Plot 1: alpha(k) for each side, G=0
        ax = axes[0, 0]
        for side in SIDES:
            entries = entropy_data[0.0][side]
            boundary = all_results[0.0][side]['boundary']
            ks = [e[0] for e in entries]
            alphas = [e[1] / boundary for e in entries]
            ax.plot(ks, alphas, 'o-', label=f'side={side}', markersize=5)
        ax.set_xlabel('Number of filled states k')
        ax.set_ylabel('alpha(k) = S / |boundary|')
        ax.set_title('Free (G=0)')
        ax.legend()

        # Plot 2: alpha(k) for each side, G=10
        ax = axes[0, 1]
        for side in SIDES:
            entries = entropy_data[10.0][side]
            boundary = all_results[10.0][side]['boundary']
            ks = [e[0] for e in entries]
            alphas = [e[1] / boundary for e in entries]
            ax.plot(ks, alphas, 'o-', label=f'side={side}', markersize=5)
        ax.set_xlabel('Number of filled states k')
        ax.set_ylabel('alpha(k) = S / |boundary|')
        ax.set_title('Self-gravity (G=10)')
        ax.legend()

        # Plot 3: S vs boundary at fixed filling fractions (G=0)
        ax = axes[1, 0]
        labels_seen = []
        for side in SIDES:
            for _, _, _, label in entropy_data[0.0][side]:
                if label not in labels_seen:
                    labels_seen.append(label)

        for label in labels_seen[::2]:  # every other to avoid crowding
            bnds = []
            Ss = []
            for side in SIDES:
                for k, S, bnd, lbl in entropy_data[0.0][side]:
                    if lbl == label:
                        bnds.append(bnd)
                        Ss.append(S)
                        break
            ax.plot(bnds, Ss, 'o-', label=label, markersize=5)
        ax.set_xlabel('Boundary size')
        ax.set_ylabel('S')
        ax.set_title('S vs boundary (G=0)')
        ax.legend()

        # Plot 4: Gravity comparison at largest side
        ax = axes[1, 1]
        largest = max(SIDES)
        for G, color, lstyle in [(0.0, 'blue', '-'), (10.0, 'red', '--')]:
            entries = entropy_data[G][largest]
            boundary = all_results[G][largest]['boundary']
            ks = [e[0] for e in entries]
            alphas = [e[1] / boundary for e in entries]
            label = f'G={G:.0f}'
            ax.plot(ks, alphas, f'o{lstyle}', color=color, label=label, markersize=5)
        ax.set_xlabel('Number of filled states k')
        ax.set_ylabel('alpha(k) = S / |boundary|')
        ax.set_title(f'Free vs Gravity (side={largest})')
        ax.legend()

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    main()
