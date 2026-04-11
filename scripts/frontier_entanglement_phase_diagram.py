#!/usr/bin/env python3
"""Entanglement entropy phase diagram S(G, R).

Maps the full phase diagram to look for a Hawking-Page-like transition
from area law to volume law as a function of gravitational coupling G.

Context:
  - Holographic probe: area law at G=10, R^2=0.9998
  - BH probe: S ~ |bnd|^1.76 at G=50-300 (super-area)
  - Question: is there a phase transition in G where scaling changes?

Protocol:
  For each G in [0, 1, 2, 5, 10, 20, 50, 100, 200]:
    - 2D staggered lattice side=12, n=144
    - Gaussian init, 30 CN steps with self-gravity (parity coupling)
    - Dirac sea from final Hamiltonian
    - BFS balls R=1..5: compute S_A, |A|, |boundary|
  Fit S vs |bnd| and S vs |A| for each G.
  Plot R^2_area - R^2_vol vs G to identify phase transition.
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
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIGMA = 1.5
SIDE = 12
N = SIDE * SIDE  # 144

G_VALUES = [0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0]
RADII = [1, 2, 3, 4, 5]


# ---------------------------------------------------------------------------
# Lattice construction
# ---------------------------------------------------------------------------

def build_lattice_2d(side: int):
    """Build a 2D periodic square lattice with checkerboard parity."""
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
                jdx = jx * side + jy
                adj[idx].append(jdx)

    return n, pos, adj, col


# ---------------------------------------------------------------------------
# BFS ball and boundary
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

def solve_poisson(adj: dict, n: int, rho: np.ndarray, mu2: float, G: float):
    """Solve screened Poisson (L + mu^2) phi = G * rho."""
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
                      phi: np.ndarray):
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


def cn_step(psi: np.ndarray, H: sparse.csc_matrix, dt: float):
    """One Crank-Nicolson time step."""
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def evolve_and_get_final_H(n: int, pos: np.ndarray, adj: dict,
                            col: np.ndarray, G: float):
    """Evolve Gaussian under self-gravity, return (psi_final, H_final)."""
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
# Dirac sea and entanglement entropy
# ---------------------------------------------------------------------------

def dirac_sea_correlation_matrix(H: sparse.csc_matrix):
    """Fill negative-energy modes, return correlation matrix C."""
    H_dense = H.toarray()
    H_dense = 0.5 * (H_dense + H_dense.conj().T)

    eigenvalues, eigenvectors = np.linalg.eigh(H_dense)
    filled = eigenvalues < 0
    n_filled = np.sum(filled)

    if n_filled == 0:
        n_filled = len(eigenvalues) // 2
        filled = np.zeros(len(eigenvalues), dtype=bool)
        filled[:n_filled] = True

    V = eigenvectors[:, filled]
    C = V @ V.conj().T
    return C, eigenvalues, int(n_filled)


def entanglement_entropy(C: np.ndarray, A_nodes: list[int]):
    """Free-fermion entanglement entropy from restricted correlation matrix."""
    if len(A_nodes) == 0:
        return 0.0

    ix = np.ix_(A_nodes, A_nodes)
    C_A = C[ix]
    C_A = 0.5 * (C_A + C_A.conj().T)

    nu = np.linalg.eigvalsh(C_A).real
    nu = np.clip(nu, 1e-15, 1.0 - 1e-15)
    S = -np.sum(nu * np.log(nu) + (1.0 - nu) * np.log(1.0 - nu))
    return float(S)


# ---------------------------------------------------------------------------
# Fitting utilities
# ---------------------------------------------------------------------------

def safe_linregress(x, y):
    """Linear regression with fallback."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or np.std(x) < 1e-12:
        return 0.0, np.mean(y), 0.0
    res = linregress(x, y)
    return res.slope, res.intercept, res.rvalue**2


def power_law_fit(x, y):
    """Fit y = a * x^alpha via log-log regression. Returns (a, alpha, R^2)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = (x > 0) & (y > 0)
    if mask.sum() < 2:
        return 1.0, 1.0, 0.0
    lx = np.log(x[mask])
    ly = np.log(y[mask])
    if np.std(lx) < 1e-12:
        return 1.0, 1.0, 0.0
    res = linregress(lx, ly)
    return np.exp(res.intercept), res.slope, res.rvalue**2


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment():
    print("=" * 80)
    print("ENTANGLEMENT ENTROPY PHASE DIAGRAM  S(G, R)")
    print("Looking for Hawking-Page-like area-to-volume law transition")
    print("=" * 80)
    print()
    print(f"Lattice: 2D periodic, side={SIDE}, n={N}")
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"G values: {G_VALUES}")
    print(f"BFS radii: {RADII}")
    print()

    n, pos, adj, col = build_lattice_2d(SIDE)
    center = (SIDE // 2) * SIDE + (SIDE // 2)

    # Pre-compute BFS balls (independent of G)
    balls = {}
    for R in RADII:
        A_nodes, bnd = bfs_ball(adj, center, R, n)
        balls[R] = (A_nodes, len(A_nodes), bnd)
        print(f"  R={R}: |A|={len(A_nodes)}, |bnd|={bnd}")

    print()

    # ------------------------------------------------------------------
    # Sweep G values
    # ------------------------------------------------------------------
    # data[G] = list of dicts with R, nA, bnd, S
    data: dict[float, list[dict]] = {}

    for G in G_VALUES:
        t0 = time.time()
        print(f"--- G = {G:.1f} ---")

        _, H_final = evolve_and_get_final_H(n, pos, adj, col, G)
        C, evals, n_filled = dirac_sea_correlation_matrix(H_final)

        n_neg = np.sum(evals < 0)
        gap = evals[n_neg] - evals[n_neg - 1] if n_neg > 0 and n_neg < len(evals) else 0.0

        print(f"  Filled modes: {n_filled}, spectral gap: {gap:.6f}")
        print(f"  Energy range: [{evals[0]:.4f}, {evals[-1]:.4f}]")

        records = []
        for R in RADII:
            A_nodes, nA, bnd = balls[R]
            if nA >= n:
                continue
            S = entanglement_entropy(C, A_nodes)
            records.append({'R': R, 'nA': nA, 'bnd': bnd, 'S': S})
            print(f"    R={R}: |A|={nA:>3}, |bnd|={bnd:>3}, S={S:.6f}")

        data[G] = records
        dt = time.time() - t0
        print(f"  [{dt:.1f}s]")
        print()

    # ------------------------------------------------------------------
    # Phase diagram analysis
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PHASE DIAGRAM ANALYSIS")
    print("=" * 80)

    # Table header
    print(f"\n{'G':>6} | {'R2_area':>8} {'R2_vol':>8} {'R2_a-R2_v':>10} | "
          f"{'alpha_bnd':>9} {'R2_pw':>6} | {'winner':>10}")
    print("-" * 72)

    phase_data = []  # (G, R2_area, R2_vol, delta_R2, alpha_bnd)

    for G in G_VALUES:
        recs = data[G]
        if len(recs) < 3:
            print(f"{G:>6.1f} | insufficient data")
            continue

        bnd = np.array([r['bnd'] for r in recs], dtype=float)
        vol = np.array([r['nA'] for r in recs], dtype=float)
        S = np.array([r['S'] for r in recs])

        _, _, r2_area = safe_linregress(bnd, S)
        _, _, r2_vol = safe_linregress(vol, S)
        delta_r2 = r2_area - r2_vol

        # Power-law fit: S = a * |bnd|^alpha
        _, alpha_bnd, r2_pw = power_law_fit(bnd, S)

        winner = "AREA" if delta_r2 > 0.01 else ("VOLUME" if delta_r2 < -0.01 else "MARGINAL")

        print(f"{G:>6.1f} | {r2_area:>8.4f} {r2_vol:>8.4f} {delta_r2:>+10.4f} | "
              f"{alpha_bnd:>9.4f} {r2_pw:>6.3f} | {winner:>10}")

        phase_data.append((G, r2_area, r2_vol, delta_r2, alpha_bnd))

    # ------------------------------------------------------------------
    # Entropy density and boundary entropy
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("ENTROPY DENSITY AND BOUNDARY ENTROPY")
    print("=" * 80)

    print(f"\n{'G':>6} | ", end="")
    for R in RADII:
        print(f"s(R={R}):>8 ", end="")
    print(f"| ", end="")
    for R in RADII:
        print(f"sig(R={R}):>8 ", end="")
    print()

    # Nicer header
    print(f"\n{'G':>6} | ", end="")
    for R in RADII:
        print(f"{'s(R='+str(R)+')':>8} ", end="")
    print("| ", end="")
    for R in RADII:
        print(f"{'sig(R='+str(R)+')':>8} ", end="")
    print()
    print("-" * (8 + 9 * len(RADII) + 3 + 9 * len(RADII)))

    density_table = []  # For checking constancy of sigma

    for G in G_VALUES:
        recs = data[G]
        print(f"{G:>6.1f} | ", end="")
        sigmas = []
        for rec in recs:
            s_density = rec['S'] / rec['nA'] if rec['nA'] > 0 else 0.0
            print(f"{s_density:>8.4f} ", end="")
        print("| ", end="")
        for rec in recs:
            sigma = rec['S'] / rec['bnd'] if rec['bnd'] > 0 else 0.0
            sigmas.append(sigma)
            print(f"{sigma:>8.4f} ", end="")
        print()
        density_table.append((G, sigmas))

    # Check constancy of sigma for each G
    print(f"\n{'G':>6} | {'sigma_mean':>10} {'sigma_std':>10} {'CV(%)':>8} | {'area_law_exact':>14}")
    print("-" * 55)
    for G, sigmas in density_table:
        arr = np.array(sigmas)
        mean_s = np.mean(arr)
        std_s = np.std(arr)
        cv = 100 * std_s / mean_s if mean_s > 1e-12 else 0.0
        exact = "YES" if cv < 10 else ("APPROX" if cv < 25 else "NO")
        print(f"{G:>6.1f} | {mean_s:>10.6f} {std_s:>10.6f} {cv:>8.2f} | {exact:>14}")

    # ------------------------------------------------------------------
    # Hawking-Page transition detection
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("HAWKING-PAGE TRANSITION DETECTION")
    print("=" * 80)

    if len(phase_data) < 3:
        print("  Insufficient data for transition detection.")
    else:
        Gs = np.array([d[0] for d in phase_data])
        deltas = np.array([d[3] for d in phase_data])
        alphas = np.array([d[4] for d in phase_data])

        # Look for sign change in delta_R2
        print("\n  delta_R2 = R2_area - R2_vol:")
        sign_changes = []
        for i in range(len(deltas) - 1):
            if deltas[i] * deltas[i + 1] < 0:
                # Linear interpolation for zero crossing
                G_cross = Gs[i] + (Gs[i + 1] - Gs[i]) * abs(deltas[i]) / (abs(deltas[i]) + abs(deltas[i + 1]))
                sign_changes.append(G_cross)
                print(f"    Sign change between G={Gs[i]:.1f} and G={Gs[i+1]:.1f}")
                print(f"    Interpolated G_HP = {G_cross:.2f}")

        if not sign_changes:
            if np.all(deltas > 0):
                print("    Area law dominant at ALL G values tested.")
                print("    No Hawking-Page transition found in this range.")
            elif np.all(deltas < 0):
                print("    Volume law dominant at ALL G values tested.")
            else:
                print("    Mixed results but no clean sign change.")

        # Look for discontinuity in entropy
        print("\n  Entropy jump detection (largest R ball):")
        largest_R = RADII[-1]
        S_at_max_R = []
        for G in G_VALUES:
            for rec in data[G]:
                if rec['R'] == largest_R:
                    S_at_max_R.append((G, rec['S']))

        if len(S_at_max_R) >= 2:
            for i in range(len(S_at_max_R) - 1):
                G1, S1 = S_at_max_R[i]
                G2, S2 = S_at_max_R[i + 1]
                dS = S2 - S1
                dG = G2 - G1
                dS_dG = dS / dG if dG > 0 else 0.0
                jump = "JUMP" if abs(dS / max(S1, 1e-12)) > 0.3 else ""
                print(f"    G={G1:.0f}->{G2:.0f}: dS={dS:+.4f}, dS/dG={dS_dG:+.6f} {jump}")

        # Alpha exponent evolution
        print(f"\n  Power-law exponent alpha(G) for S ~ |bnd|^alpha:")
        for G_val, _, _, _, alpha in phase_data:
            label = ""
            if abs(alpha - 1.0) < 0.1:
                label = "  [area law: alpha ~ 1]"
            elif alpha > 1.5:
                label = "  [super-area]"
            elif alpha < 0.5:
                label = "  [sub-area]"
            print(f"    G={G_val:>6.1f}: alpha = {alpha:.4f}{label}")

    # ------------------------------------------------------------------
    # Raw data table
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("RAW DATA TABLE")
    print("=" * 80)
    print(f"{'G':>6} {'R':>3} {'|A|':>5} {'|bnd|':>5} {'S':>12} {'s=S/|A|':>10} {'sig=S/|bnd|':>12}")
    print("-" * 58)

    for G in G_VALUES:
        for rec in data[G]:
            s_dens = rec['S'] / rec['nA'] if rec['nA'] > 0 else 0.0
            sigma = rec['S'] / rec['bnd'] if rec['bnd'] > 0 else 0.0
            print(f"{G:>6.1f} {rec['R']:>3} {rec['nA']:>5} {rec['bnd']:>5} "
                  f"{rec['S']:>12.6f} {s_dens:>10.6f} {sigma:>12.6f}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if phase_data:
        low_G = [d for d in phase_data if d[0] <= 10]
        high_G = [d for d in phase_data if d[0] >= 50]

        if low_G:
            avg_delta_low = np.mean([d[3] for d in low_G])
            avg_alpha_low = np.mean([d[4] for d in low_G])
            print(f"\n  Low G (<=10):  mean delta_R2 = {avg_delta_low:+.4f}, "
                  f"mean alpha = {avg_alpha_low:.4f}")

        if high_G:
            avg_delta_high = np.mean([d[3] for d in high_G])
            avg_alpha_high = np.mean([d[4] for d in high_G])
            print(f"  High G (>=50): mean delta_R2 = {avg_delta_high:+.4f}, "
                  f"mean alpha = {avg_alpha_high:.4f}")

        if low_G and high_G:
            if avg_delta_low > 0 and avg_delta_high < 0:
                print("\n  PHASE TRANSITION DETECTED: area law at low G, volume law at high G")
            elif avg_delta_low > 0 and avg_delta_high > 0:
                if avg_alpha_high > avg_alpha_low + 0.3:
                    print("\n  CROSSOVER: area law persists but exponent grows with G (super-area)")
                else:
                    print("\n  NO TRANSITION: area law at all G values")
            else:
                print(f"\n  Regime: low-G delta={avg_delta_low:+.3f}, "
                      f"high-G delta={avg_delta_high:+.3f}")

    # ------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 3, figsize=(18, 11))
        fig.suptitle('Entanglement Entropy Phase Diagram S(G, R)\n'
                     f'2D lattice side={SIDE}, MASS={MASS}, {N_STEPS} CN steps',
                     fontsize=13)

        cmap = plt.cm.viridis
        G_colors = {G: cmap(i / max(len(G_VALUES) - 1, 1))
                    for i, G in enumerate(G_VALUES)}

        # (a) S vs |bnd| for each G
        ax = axes[0, 0]
        for G in G_VALUES:
            recs = data[G]
            bnd = [r['bnd'] for r in recs]
            S = [r['S'] for r in recs]
            ax.plot(bnd, S, 'o-', color=G_colors[G], label=f'G={G:.0f}', markersize=4)
        ax.set_xlabel('|boundary|')
        ax.set_ylabel('S')
        ax.set_title('(a) S vs |boundary|')
        ax.legend(fontsize=6, ncol=2)

        # (b) S vs |A| for each G
        ax = axes[0, 1]
        for G in G_VALUES:
            recs = data[G]
            vol = [r['nA'] for r in recs]
            S = [r['S'] for r in recs]
            ax.plot(vol, S, 'o-', color=G_colors[G], label=f'G={G:.0f}', markersize=4)
        ax.set_xlabel('|A|')
        ax.set_ylabel('S')
        ax.set_title('(b) S vs volume')
        ax.legend(fontsize=6, ncol=2)

        # (c) R2_area - R2_vol vs G
        ax = axes[0, 2]
        if phase_data:
            Gs_plot = [d[0] for d in phase_data]
            deltas_plot = [d[3] for d in phase_data]
            ax.plot(Gs_plot, deltas_plot, 'ko-', markersize=6)
            ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
            ax.set_xlabel('G')
            ax.set_ylabel('R$^2_{area}$ - R$^2_{vol}$')
            ax.set_title('(c) Phase indicator')
            ax.set_xscale('symlog', linthresh=1)

        # (d) Power-law exponent alpha vs G
        ax = axes[1, 0]
        if phase_data:
            Gs_plot = [d[0] for d in phase_data]
            alphas_plot = [d[4] for d in phase_data]
            ax.plot(Gs_plot, alphas_plot, 'bs-', markersize=6)
            ax.axhline(y=1.0, color='g', linestyle='--', alpha=0.5, label='area law (alpha=1)')
            ax.set_xlabel('G')
            ax.set_ylabel('alpha (S ~ |bnd|^alpha)')
            ax.set_title('(d) Power-law exponent')
            ax.set_xscale('symlog', linthresh=1)
            ax.legend(fontsize=8)

        # (e) Boundary entropy sigma = S/|bnd| vs R for each G
        ax = axes[1, 1]
        for G in G_VALUES:
            recs = data[G]
            Rs = [r['R'] for r in recs]
            sigmas = [r['S'] / r['bnd'] if r['bnd'] > 0 else 0 for r in recs]
            ax.plot(Rs, sigmas, 'o-', color=G_colors[G], label=f'G={G:.0f}', markersize=4)
        ax.set_xlabel('R')
        ax.set_ylabel('sigma = S / |bnd|')
        ax.set_title('(e) Boundary entropy density')
        ax.legend(fontsize=6, ncol=2)

        # (f) S at largest R vs G (entropy jump detection)
        ax = axes[1, 2]
        if S_at_max_R:
            Gs_s = [x[0] for x in S_at_max_R]
            Ss_s = [x[1] for x in S_at_max_R]
            ax.plot(Gs_s, Ss_s, 'ro-', markersize=6)
            ax.set_xlabel('G')
            ax.set_ylabel(f'S (R={largest_R})')
            ax.set_title(f'(f) Entropy at R={largest_R} vs G')
            ax.set_xscale('symlog', linthresh=1)

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    run_experiment()
