#!/usr/bin/env python3
"""Hawking-Page crossover recheck with unscreened Poisson (mu^2=0.001).

The original entanglement phase diagram used mu^2=0.22, which screened
the gravitational potential differently at each lattice size, causing
G_c to drift 34% across sizes. This recheck uses mu^2=0.001 (effectively
unscreened) to test whether the Hawking-Page transition stabilizes.

Protocol:
  For each (side, G):
    - 2D staggered lattice, periodic boundary conditions
    - Gaussian init, 30 CN steps with self-gravity (parity coupling)
    - Dirac sea from final Hamiltonian
    - BFS ball bipartitions: compute S_A, |A|, |boundary|
  Fit S vs |boundary| and S vs |volume| for each (side, G).
  Report R^2_area - R^2_vol.

For each side, find G_c where R^2_area = R^2_vol (the crossover).
Check: does G_c converge as side increases?

Also compute the area-law exponent alpha(G) = slope of S vs |boundary|.
Does alpha show a sharp kink at G_c?
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
MU2 = 0.001        # unscreened
DT = 0.12
N_STEPS = 30
SIGMA = 1.5

SIDES = [8, 10, 12, 14]
G_VALUES = [1, 3, 5, 7, 9, 10, 11, 13, 15, 20, 30, 50]
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


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment():
    t_start = time.time()
    print("=" * 80)
    print("HAWKING-PAGE CROSSOVER RECHECK: UNSCREENED (mu^2 = 0.001)")
    print("=" * 80)
    print()
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"Sides: {SIDES}")
    print(f"G values: {G_VALUES}")
    print(f"BFS radii: {RADII}")
    print()
    print("Question: does G_c converge with lattice size when screening is removed?")
    print("(Original screened result drifted 34%.)")
    print()

    # ------------------------------------------------------------------
    # data[side][G] = list of dicts {R, nA, bnd, S}
    # ------------------------------------------------------------------
    all_data: dict[int, dict[float, list[dict]]] = {}

    # phase_results[side] = list of (G, R2_area, R2_vol, delta_R2, slope_bnd)
    phase_results: dict[int, list[tuple]] = {}

    for side in SIDES:
        n = side * side
        print(f"\n{'#' * 80}")
        print(f"# SIDE = {side}  (n = {n})")
        print(f"{'#' * 80}")

        n_sites, pos, adj, col = build_lattice_2d(side)
        center = (side // 2) * side + (side // 2)

        # Pre-compute BFS balls
        balls = {}
        max_R = min(RADII[-1], side // 2 - 1)
        usable_radii = [R for R in RADII if R <= max_R]
        for R in usable_radii:
            A_nodes, bnd = bfs_ball(adj, center, R, n_sites)
            if len(A_nodes) < n_sites:
                balls[R] = (A_nodes, len(A_nodes), bnd)

        print(f"  BFS balls: {[(R, balls[R][1], balls[R][2]) for R in sorted(balls)]}")

        all_data[side] = {}
        phase_results[side] = []

        for G in G_VALUES:
            t0 = time.time()
            _, H_final = evolve_and_get_final_H(n_sites, pos, adj, col, float(G))
            C, evals, n_filled = dirac_sea_correlation_matrix(H_final)

            records = []
            for R in sorted(balls):
                A_nodes, nA, bnd = balls[R]
                S = entanglement_entropy(C, A_nodes)
                records.append({'R': R, 'nA': nA, 'bnd': bnd, 'S': S})

            all_data[side][G] = records

            # Fit
            if len(records) >= 3:
                bnd_arr = np.array([r['bnd'] for r in records], dtype=float)
                vol_arr = np.array([r['nA'] for r in records], dtype=float)
                S_arr = np.array([r['S'] for r in records])

                slope_bnd, _, r2_area = safe_linregress(bnd_arr, S_arr)
                _, _, r2_vol = safe_linregress(vol_arr, S_arr)
                delta_r2 = r2_area - r2_vol
                phase_results[side].append((G, r2_area, r2_vol, delta_r2, slope_bnd))
            else:
                phase_results[side].append((G, 0.0, 0.0, 0.0, 0.0))

            dt = time.time() - t0
            tag = "AREA" if phase_results[side][-1][3] > 0.01 else (
                "VOL" if phase_results[side][-1][3] < -0.01 else "~")
            print(f"  G={G:>3}: R2a={phase_results[side][-1][1]:.4f} "
                  f"R2v={phase_results[side][-1][2]:.4f} "
                  f"dR2={phase_results[side][-1][3]:+.4f} "
                  f"slope={phase_results[side][-1][4]:.6f}  [{tag}] ({dt:.1f}s)")

    # ------------------------------------------------------------------
    # Find G_c for each side (interpolate zero crossing of delta_R2)
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("G_c CONVERGENCE ANALYSIS")
    print("=" * 80)

    Gc_by_side: dict[int, float] = {}

    for side in SIDES:
        pdata = phase_results[side]
        Gs = np.array([d[0] for d in pdata], dtype=float)
        deltas = np.array([d[3] for d in pdata])

        print(f"\n  side={side}:")
        print(f"    delta_R2 values: {['%.4f' % d for d in deltas]}")

        crossings = []
        for i in range(len(deltas) - 1):
            if deltas[i] * deltas[i + 1] < 0:
                G_cross = Gs[i] + (Gs[i + 1] - Gs[i]) * abs(deltas[i]) / (
                    abs(deltas[i]) + abs(deltas[i + 1]))
                crossings.append(G_cross)
                print(f"    Crossover between G={Gs[i]:.0f} and G={Gs[i+1]:.0f}: "
                      f"G_c = {G_cross:.2f}")

        if crossings:
            Gc_by_side[side] = crossings[0]  # take the first crossing
        elif np.all(deltas > 0):
            print(f"    Area law at ALL G: no crossover found (G_c > {G_VALUES[-1]})")
        elif np.all(deltas < 0):
            print(f"    Volume law at ALL G: no crossover found (G_c < {G_VALUES[0]})")
        else:
            # no clean sign change; try to find where delta is closest to 0
            idx_min = np.argmin(np.abs(deltas))
            print(f"    No clean sign change; closest to 0 at G={Gs[idx_min]:.0f} "
                  f"(delta={deltas[idx_min]:.4f})")

    # Convergence check
    print(f"\n  --- G_c summary ---")
    if len(Gc_by_side) >= 2:
        sides_found = sorted(Gc_by_side.keys())
        Gc_vals = [Gc_by_side[s] for s in sides_found]

        for s in sides_found:
            print(f"    side={s}: G_c = {Gc_by_side[s]:.2f}")

        Gc_mean = np.mean(Gc_vals)
        Gc_std = np.std(Gc_vals)
        spread_pct = 100 * (max(Gc_vals) - min(Gc_vals)) / Gc_mean if Gc_mean > 0 else 999

        print(f"\n    G_c mean = {Gc_mean:.2f}")
        print(f"    G_c std  = {Gc_std:.2f}")
        print(f"    Spread   = {spread_pct:.1f}%")

        if spread_pct < 10:
            print(f"\n    CONVERGED (spread < 10%): Hawking-Page transition is REAL")
            print(f"    G_c = {Gc_mean:.1f} +/- {Gc_std:.1f}")
        elif spread_pct < 20:
            print(f"\n    MARGINAL (spread {spread_pct:.0f}%): transition likely real but noisy")
        else:
            print(f"\n    NOT CONVERGED (spread {spread_pct:.0f}%): transition may be artifact")
    elif len(Gc_by_side) == 1:
        s = list(Gc_by_side.keys())[0]
        print(f"    Only one size has crossover: side={s}, G_c={Gc_by_side[s]:.2f}")
        print(f"    Cannot assess convergence.")
    else:
        print(f"    No crossovers found at any lattice size.")

    # ------------------------------------------------------------------
    # Alpha exponent kink analysis
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("AREA-LAW EXPONENT alpha(G) = slope of S vs |boundary|")
    print("=" * 80)

    print(f"\n{'side':>5} {'G':>5} {'slope':>10} {'R2_area':>8}")
    print("-" * 36)

    for side in SIDES:
        for G, r2a, r2v, dr2, slope in phase_results[side]:
            marker = " <-- near G_c" if side in Gc_by_side and abs(G - Gc_by_side[side]) < 3 else ""
            print(f"{side:>5} {G:>5} {slope:>10.6f} {r2a:>8.4f}{marker}")
        print()

    # Check for kink: largest |d(slope)/dG| near G_c
    print("  Kink detection (max |d(slope)/dG|):")
    for side in SIDES:
        pdata = phase_results[side]
        if len(pdata) < 2:
            continue
        Gs = [d[0] for d in pdata]
        slopes = [d[4] for d in pdata]
        max_dsdg = 0.0
        max_G_kink = 0.0
        for i in range(len(Gs) - 1):
            dG = Gs[i + 1] - Gs[i]
            if dG > 0:
                dsdg = abs(slopes[i + 1] - slopes[i]) / dG
                if dsdg > max_dsdg:
                    max_dsdg = dsdg
                    max_G_kink = 0.5 * (Gs[i] + Gs[i + 1])
        Gc_str = f"G_c={Gc_by_side[side]:.1f}" if side in Gc_by_side else "no G_c"
        print(f"    side={side}: max |d(slope)/dG| = {max_dsdg:.6f} at G ~ {max_G_kink:.0f}  ({Gc_str})")

    # ------------------------------------------------------------------
    # Raw data
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("RAW DATA")
    print("=" * 80)

    print(f"\n{'side':>5} {'G':>5} {'R':>3} {'|A|':>5} {'|bnd|':>5} {'S':>12}")
    print("-" * 42)

    for side in SIDES:
        for G in G_VALUES:
            for rec in all_data[side][G]:
                print(f"{side:>5} {G:>5} {rec['R']:>3} {rec['nA']:>5} "
                      f"{rec['bnd']:>5} {rec['S']:>12.6f}")

    # ------------------------------------------------------------------
    # Phase diagram table
    # ------------------------------------------------------------------
    print("\n\n" + "=" * 80)
    print("PHASE DIAGRAM TABLE")
    print("=" * 80)

    print(f"\n{'side':>5} {'G':>5} | {'R2_area':>8} {'R2_vol':>8} {'dR2':>8} | {'winner':>8}")
    print("-" * 52)

    for side in SIDES:
        for G, r2a, r2v, dr2, slope in phase_results[side]:
            winner = "AREA" if dr2 > 0.01 else ("VOL" if dr2 < -0.01 else "~")
            print(f"{side:>5} {G:>5} | {r2a:>8.4f} {r2v:>8.4f} {dr2:>+8.4f} | {winner:>8}")
        print()

    # ------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Hawking-Page Crossover Recheck (mu^2={MU2}, unscreened)\n'
                     f'MASS={MASS}, {N_STEPS} CN steps, parity coupling',
                     fontsize=12)

        colors = {8: 'C0', 10: 'C1', 12: 'C2', 14: 'C3'}

        # (a) delta_R2 vs G for each side
        ax = axes[0, 0]
        for side in SIDES:
            pdata = phase_results[side]
            Gs = [d[0] for d in pdata]
            deltas = [d[3] for d in pdata]
            ax.plot(Gs, deltas, 'o-', color=colors[side], label=f'side={side}', markersize=5)
        ax.axhline(0, color='k', ls='--', alpha=0.3)
        ax.set_xlabel('G')
        ax.set_ylabel('R$^2_{area}$ - R$^2_{vol}$')
        ax.set_title('(a) Phase indicator vs G')
        ax.legend(fontsize=8)
        ax.set_xscale('log')

        # (b) G_c vs side
        ax = axes[0, 1]
        if len(Gc_by_side) >= 2:
            ss = sorted(Gc_by_side.keys())
            gc = [Gc_by_side[s] for s in ss]
            ax.plot(ss, gc, 'ko-', markersize=8)
            ax.axhline(np.mean(gc), color='r', ls='--', alpha=0.5, label=f'mean={np.mean(gc):.1f}')
            ax.set_xlabel('Side')
            ax.set_ylabel('G_c')
            ax.set_title('(b) G_c convergence')
            ax.legend(fontsize=8)
        else:
            ax.text(0.5, 0.5, 'Insufficient crossovers', ha='center', va='center',
                    transform=ax.transAxes)
            ax.set_title('(b) G_c convergence')

        # (c) alpha (slope) vs G for each side
        ax = axes[1, 0]
        for side in SIDES:
            pdata = phase_results[side]
            Gs = [d[0] for d in pdata]
            slopes = [d[4] for d in pdata]
            ax.plot(Gs, slopes, 'o-', color=colors[side], label=f'side={side}', markersize=5)
        ax.set_xlabel('G')
        ax.set_ylabel('slope (S vs |bnd|)')
        ax.set_title('(c) Area-law slope vs G')
        ax.legend(fontsize=8)
        ax.set_xscale('log')

        # (d) S vs |bnd| for side=12, selected G values
        ax = axes[1, 1]
        selected_Gs = [1, 5, 10, 15, 30, 50]
        cmap = plt.cm.coolwarm
        for i, G in enumerate(selected_Gs):
            if G in [d[0] for d in phase_results.get(12, [])]:
                recs = all_data.get(12, {}).get(G, [])
                bnd = [r['bnd'] for r in recs]
                S = [r['S'] for r in recs]
                c = cmap(i / max(len(selected_Gs) - 1, 1))
                ax.plot(bnd, S, 'o-', color=c, label=f'G={G}', markersize=5)
        ax.set_xlabel('|boundary|')
        ax.set_ylabel('S')
        ax.set_title('(d) S vs |bnd| (side=12)')
        ax.legend(fontsize=7, ncol=2)

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    elapsed = time.time() - t_start
    print(f"\n\n{'=' * 80}")
    print("SUMMARY")
    print("=" * 80)

    if len(Gc_by_side) >= 2:
        sides_found = sorted(Gc_by_side.keys())
        Gc_vals = [Gc_by_side[s] for s in sides_found]
        Gc_mean = np.mean(Gc_vals)
        spread_pct = 100 * (max(Gc_vals) - min(Gc_vals)) / Gc_mean if Gc_mean > 0 else 999

        print(f"\n  G_c values: {dict((s, f'{Gc_by_side[s]:.2f}') for s in sides_found)}")
        print(f"  Spread: {spread_pct:.1f}%")

        if spread_pct < 10:
            print(f"\n  VERDICT: Hawking-Page transition is REAL at G_c ~ {Gc_mean:.1f}")
            print(f"  The 34% drift was a SCREENING ARTIFACT (mu^2=0.22).")
        elif spread_pct < 20:
            print(f"\n  VERDICT: Transition LIKELY REAL but noisy (spread={spread_pct:.0f}%)")
        else:
            print(f"\n  VERDICT: Still drifting (spread={spread_pct:.0f}%). Not converged.")
    elif len(Gc_by_side) == 1:
        s = list(Gc_by_side.keys())[0]
        print(f"\n  Only one crossover found: side={s}, G_c={Gc_by_side[s]:.2f}")
        print(f"  VERDICT: Inconclusive -- need more sizes with crossovers.")
    else:
        # Check if all area or all volume
        all_area = all(
            all(d[3] > 0 for d in phase_results[side])
            for side in SIDES
        )
        all_vol = all(
            all(d[3] < 0 for d in phase_results[side])
            for side in SIDES
        )
        if all_area:
            print(f"\n  Area law at ALL sizes and ALL G values up to {G_VALUES[-1]}.")
            print(f"  VERDICT: No Hawking-Page transition in this G range.")
        elif all_vol:
            print(f"\n  Volume law at ALL sizes and ALL G values.")
            print(f"  VERDICT: No area-law phase found.")
        else:
            print(f"\n  Mixed results but no clean crossovers.")
            print(f"  VERDICT: Inconclusive.")

    print(f"\n  Total runtime: {elapsed:.1f}s")
    print("=" * 80)


if __name__ == '__main__':
    run_experiment()
