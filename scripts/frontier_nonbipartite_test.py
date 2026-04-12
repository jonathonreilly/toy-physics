#!/usr/bin/env python3
"""Triangular/Wilson robustness probe with bounded scope.

This runner tests whether a bounded boundary-law preference seen on the
staggered square lattice can also appear on one periodic triangular lattice
with Wilson fermions. It also carries exploratory internal checks based on a
Hamiltonian-spectrum flow estimator and an entropy-scaling crossover scan.

Architecture:
  - Triangular lattice (6-neighbor, NOT bipartite: has odd cycles)
  - Wilson fermions instead of Kogut-Susskind staggered fermions
  - Scalar gravitational coupling H[i,i] = m + phi(x) (no parity factor)
  - Same screened-Poisson self-gravity as bipartite runs

Three probes:
  1. boundary-law preference for Dirac-sea entropy on BFS-ball cuts
  2. exploratory Hamiltonian-spectrum flow estimator
  3. exploratory entropy-scaling crossover scan
"""

from __future__ import annotations

import math
import time
from collections import deque

import numpy as np
from scipy import sparse
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

# ---------------------------------------------------------------------------
# Physical parameters (matched to bipartite runs)
# ---------------------------------------------------------------------------
MASS = 0.30
MU2 = 0.22
DT = 0.12
WILSON_R = 1.0
N_STEPS = 30
SIGMA = 1.5

# ---------------------------------------------------------------------------
# Triangular lattice construction
# ---------------------------------------------------------------------------

def build_triangular_lattice(side: int):
    """Build a 2D triangular lattice with periodic boundary conditions.

    Each node has 6 neighbors. The lattice is NOT bipartite (contains
    3-cycles). Nodes are arranged in a side x side grid with hex offsets.

    Returns (n, pos, adj).
    """
    n = side * side
    coords = np.zeros((n, 2))
    adj: dict[int, list[int]] = {i: [] for i in range(n)}

    for row in range(side):
        for col in range(side):
            i = row * side + col
            x = col + 0.5 * (row % 2)
            y = row * math.sqrt(3) / 2
            coords[i] = (x, y)

    # Build adjacency: 6 neighbors per node
    for row in range(side):
        for col in range(side):
            i = row * side + col
            neighbors = set()

            # Horizontal neighbors (same row)
            neighbors.add(row * side + (col + 1) % side)
            neighbors.add(row * side + (col - 1) % side)

            # Upper row neighbors
            urow = (row + 1) % side
            offset = row % 2  # offset for hex grid
            neighbors.add(urow * side + (col + offset) % side)
            neighbors.add(urow * side + (col - 1 + offset) % side)

            # Lower row neighbors
            drow = (row - 1) % side
            neighbors.add(drow * side + (col + offset) % side)
            neighbors.add(drow * side + (col - 1 + offset) % side)

            neighbors.discard(i)
            adj[i] = sorted(neighbors)

    return n, coords, adj


def verify_nonbipartite(adj: dict[int, list[int]], n: int) -> bool:
    """Verify the graph is non-bipartite by checking for odd cycles (BFS)."""
    color = np.full(n, -1, dtype=int)
    color[0] = 0
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if color[v] == -1:
                color[v] = 1 - color[u]
                queue.append(v)
            elif color[v] == color[u]:
                return True  # odd cycle found -> non-bipartite
    return False


# ---------------------------------------------------------------------------
# Graph Laplacian and Poisson solver
# ---------------------------------------------------------------------------

def build_laplacian(pos: np.ndarray, adj: dict[int, list[int]], n: int):
    """Graph Laplacian with distance-weighted edges."""
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if j <= i:
                continue
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


def solve_poisson(L_sp, n: int, rho: np.ndarray,
                  mu2: float, G: float) -> np.ndarray:
    """Solve screened Poisson (L + mu^2) phi = G * rho."""
    A = (L_sp + mu2 * speye(n)).tocsc()
    return spsolve(A, G * rho)


# ---------------------------------------------------------------------------
# Wilson fermion Hamiltonian
# ---------------------------------------------------------------------------

def build_H_wilson(pos: np.ndarray, adj: dict[int, list[int]], n: int,
                   phi: np.ndarray, mass: float = MASS,
                   r: float = WILSON_R):
    """Wilson fermion Hamiltonian on triangular lattice.

    Hopping: H[i,j] = (-i/2 + r/2) * w_ij  for neighbors
    Diagonal: H[i,i] = mass + phi[i] + r * (sum_j w_ij) / 2

    No parity factor in the diagonal -- scalar coupling only.
    The Wilson term r * Laplacian / 2 lifts the doublers.
    """
    H = lil_matrix((n, n), dtype=complex)

    for i, nbs in adj.items():
        wilson_diag = 0.0
        for j in nbs:
            d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
            w = 1.0 / max(d, 0.5)
            wilson_diag += w

            if j > i:
                # Kinetic: -i/2 * w  +  Wilson: +r/2 * w
                H[i, j] += (-0.5j + r * 0.5) * w
                H[j, i] += (0.5j + r * 0.5) * w

        # Diagonal: mass + gravity + Wilson mass correction
        H[i, i] = mass + phi[i] + r * wilson_diag / 2.0

    return H.tocsr()


# ---------------------------------------------------------------------------
# Staggered bipartite Hamiltonian (for comparison)
# ---------------------------------------------------------------------------

def build_square_lattice(side: int):
    """Build 2D periodic square lattice with checkerboard parity."""
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


def build_H_staggered(pos: np.ndarray, col: np.ndarray,
                      adj: dict[int, list[int]], n: int,
                      phi: np.ndarray, mass: float = MASS):
    """Staggered (Kogut-Susskind) Hamiltonian on bipartite lattice."""
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((mass + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if j > i:
                d = math.hypot(pos[j, 0] - pos[i, 0], pos[j, 1] - pos[i, 1])
                w = 1.0 / max(d, 0.5)
                H[i, j] += -0.5j * w
                H[j, i] += 0.5j * w
    return H.tocsr()


# ---------------------------------------------------------------------------
# Evolution and wavepacket utilities
# ---------------------------------------------------------------------------

def gaussian_wavepacket(pos: np.ndarray, n: int, sigma: float = SIGMA):
    """Gaussian wavepacket centered on lattice centroid."""
    center = np.mean(pos, axis=0)
    dx = pos[:, 0] - center[0]
    dy = pos[:, 1] - center[1]
    psi = np.exp(-0.5 * (dx**2 + dy**2) / sigma**2).astype(complex)
    psi /= np.sqrt(np.sum(np.abs(psi)**2))
    return psi


def cn_step(psi: np.ndarray, H, dt: float, n: int) -> np.ndarray:
    """Crank-Nicolson time step."""
    I = speye(n, dtype=complex, format="csc")
    A_plus = (I + 0.5j * dt * H).tocsc()
    A_minus = I - 0.5j * dt * H
    psi_new = spsolve(A_plus, A_minus.dot(psi))
    return psi_new


def evolve_self_gravity(n, pos, adj, L_sp, G, build_H_fn, **kw):
    """Evolve Gaussian under self-gravity for N_STEPS.

    build_H_fn(pos, adj, n, phi, ...) -> H
    Returns (psi_final, H_final).
    """
    psi = gaussian_wavepacket(pos, n)
    H_final = None
    for _ in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = solve_poisson(L_sp, n, rho, MU2, G)
        H_final = build_H_fn(pos, adj, n, phi, **kw)
        psi = cn_step(psi, H_final, DT, n)
        psi /= np.sqrt(np.sum(np.abs(psi)**2))
    return psi, H_final


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
# Dirac sea correlation matrix and entanglement entropy
# ---------------------------------------------------------------------------

def dirac_sea_correlation_matrix(H):
    """Fill negative-energy modes -> correlation matrix C."""
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
    return C, n_filled


def entropy_from_C(C: np.ndarray, A_nodes: list[int]):
    """Entanglement entropy for region A from correlation matrix."""
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
# Spectral dimension from diffusion return probability
# ---------------------------------------------------------------------------

def diffusion_ds(evals: np.ndarray, n: int,
                 t_min: float = 0.01, t_max: float = 100.0, n_t: int = 200):
    """d_s(t) from return probability P(t) = (1/n) sum exp(-t E_i^2).

    Short t = UV, long t = IR.
    Returns (t_vals, d_s_vals).
    """
    E2 = evals**2
    t_vals = np.logspace(np.log10(t_min), np.log10(t_max), n_t)
    P_vals = np.array([np.mean(np.exp(-t * E2)) for t in t_vals])

    mask = P_vals > 1e-30
    if np.sum(mask) < 5:
        return t_vals, np.full(len(t_vals), np.nan)

    log_t = np.log(t_vals[mask])
    log_P = np.log(P_vals[mask])
    d_log_P = np.gradient(log_P, log_t)
    d_s = -2.0 * d_log_P

    d_s_full = np.full(len(t_vals), np.nan)
    d_s_full[mask] = d_s
    return t_vals, d_s_full


def summarize_ds_flow(t_vals, d_s):
    """Extract UV, mid, IR averages of spectral dimension."""
    valid = ~np.isnan(d_s)
    if np.sum(valid) < 6:
        return None, None, None
    n_pts = np.sum(valid)
    ds_valid = d_s[valid]
    n_third = max(1, n_pts // 3)
    ds_uv = float(np.mean(ds_valid[:n_third]))
    ds_mid = float(np.mean(ds_valid[n_third:2*n_third]))
    ds_ir = float(np.mean(ds_valid[-n_third:]))
    return ds_uv, ds_mid, ds_ir


# ---------------------------------------------------------------------------
# Linear regression helpers
# ---------------------------------------------------------------------------

def safe_linregress(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) < 2 or np.std(x) < 1e-12:
        return 0.0, np.mean(y), 0.0
    res = linregress(x, y)
    return res.slope, res.intercept, res.rvalue**2


# ===================================================================
# PROBE 1: Area law test
# ===================================================================

def probe_area_law(label, n, pos, adj, L_sp, build_H_fn, G=10.0, **kw):
    """Test area-law scaling of entanglement entropy."""
    print(f"\n  --- Probe 1: Area Law ({label}) ---")
    print(f"  G = {G}, N_STEPS = {N_STEPS}")

    psi, H = evolve_self_gravity(n, pos, adj, L_sp, G, build_H_fn, **kw)
    C, n_filled = dirac_sea_correlation_matrix(H)
    print(f"  Dirac sea: {n_filled} filled modes out of {n}")

    # Find centroid
    prob = np.abs(psi)**2
    prob /= np.sum(prob)
    cx = np.sum(prob * pos[:, 0])
    cy = np.sum(prob * pos[:, 1])
    dists = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    center = int(np.argmin(dists))

    side = int(round(math.sqrt(n)))
    max_R = side // 2 - 1
    radii = list(range(1, max_R + 1))

    results = []
    for R in radii:
        A_nodes, bnd = bfs_ball(adj, center, R, n)
        if len(A_nodes) < 2 or len(A_nodes) > n - 2:
            continue
        S = entropy_from_C(C, A_nodes)
        results.append((R, len(A_nodes), bnd, S))
        print(f"    R={R}: |A|={len(A_nodes):4d}  |bnd|={bnd:4d}  S={S:.4f}")

    if len(results) < 3:
        print("  Too few data points for fit")
        return None, None

    _, vols, bnds, entropies = zip(*results)
    slope_a, _, r2_a = safe_linregress(bnds, entropies)
    slope_v, _, r2_v = safe_linregress(vols, entropies)
    print(f"  S vs |bnd|: slope={slope_a:.4f}, R^2={r2_a:.4f}")
    print(f"  S vs |A|:   slope={slope_v:.4f}, R^2={r2_v:.4f}")
    print(f"  Area law {'HOLDS' if r2_a > r2_v and r2_a > 0.8 else 'WEAK'}: "
          f"R^2_area={r2_a:.4f} vs R^2_vol={r2_v:.4f}")

    return r2_a, r2_v


# ===================================================================
# PROBE 2: exploratory spectrum-flow estimator
# ===================================================================

def probe_cdt_flow(label, n, pos, adj, L_sp, build_H_fn, G=10.0, **kw):
    """Exploratory Hamiltonian-spectrum UV->IR flow estimator."""
    print(f"\n  --- Probe 2: Spectrum-Flow Estimator ({label}) ---")

    # Free Hamiltonian
    phi_zero = np.zeros(n)
    H_free = build_H_fn(pos, adj, n, phi_zero, **kw)
    evals_free = np.linalg.eigvalsh(H_free.toarray())

    # Gravitating Hamiltonian
    psi, H_grav = evolve_self_gravity(n, pos, adj, L_sp, G, build_H_fn, **kw)
    evals_grav = np.linalg.eigvalsh(H_grav.toarray())

    for tag, ev in [("free", evals_free), ("grav", evals_grav)]:
        t_vals, ds = diffusion_ds(ev, n)
        ds_uv, ds_mid, ds_ir = summarize_ds_flow(t_vals, ds)
        if ds_uv is None:
            print(f"  {tag}: insufficient data for flow")
            continue

        delta = ds_ir - ds_uv
        flow_dir = "UV->IR increase" if delta > 0 else "UV->IR decrease"
        print(f"  {tag}: d_s(UV)={ds_uv:.3f}  d_s(mid)={ds_mid:.3f}  "
              f"d_s(IR)={ds_ir:.3f}  [{flow_dir}, delta={delta:+.3f}]")

    return evals_free, evals_grav


# ===================================================================
# PROBE 3: exploratory entropy-scaling crossover
# ===================================================================

def probe_hawking_page(label, n, pos, adj, L_sp, build_H_fn,
                       G_values=None, **kw):
    """Sweep G to find an entropy-fit crossover on this specific runner."""
    if G_values is None:
        G_values = [0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]
    print(f"\n  --- Probe 3: Entropy-Scaling Crossover ({label}) ---")
    print(f"  G sweep: {G_values}")

    side = int(round(math.sqrt(n)))
    max_R = side // 2 - 1
    radii = list(range(1, max_R + 1))

    results_by_G = []
    for G in G_values:
        t0 = time.time()
        psi, H = evolve_self_gravity(n, pos, adj, L_sp, G, build_H_fn, **kw)
        C, n_filled = dirac_sea_correlation_matrix(H)

        prob = np.abs(psi)**2
        prob /= np.sum(prob)
        cx = np.sum(prob * pos[:, 0])
        cy = np.sum(prob * pos[:, 1])
        dists = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
        center = int(np.argmin(dists))

        vols, bnds, entropies = [], [], []
        for R in radii:
            A_nodes, bnd = bfs_ball(adj, center, R, n)
            if len(A_nodes) < 2 or len(A_nodes) > n - 2:
                continue
            S = entropy_from_C(C, A_nodes)
            vols.append(len(A_nodes))
            bnds.append(bnd)
            entropies.append(S)

        if len(entropies) < 3:
            print(f"  G={G:6.1f}: insufficient data")
            continue

        _, _, r2_a = safe_linregress(bnds, entropies)
        _, _, r2_v = safe_linregress(vols, entropies)
        dt = time.time() - t0
        dominant = "AREA" if r2_a > r2_v else "VOL"
        print(f"  G={G:6.1f}: R^2_area={r2_a:.4f}  R^2_vol={r2_v:.4f}  "
              f"[{dominant}]  ({dt:.1f}s)")
        results_by_G.append((G, r2_a, r2_v))

    # Find crossing point
    if len(results_by_G) >= 2:
        G_arr = np.array([r[0] for r in results_by_G])
        diff_arr = np.array([r[1] - r[2] for r in results_by_G])
        # Look for sign change in R^2_area - R^2_vol
        crossings = []
        for i in range(len(diff_arr) - 1):
            if diff_arr[i] * diff_arr[i + 1] < 0:
                # Linear interpolation
                G_cross = G_arr[i] - diff_arr[i] * (G_arr[i + 1] - G_arr[i]) / (
                    diff_arr[i + 1] - diff_arr[i])
                crossings.append(G_cross)

        if crossings:
            print(f"\n  entropy-fit crossing at G ~ {crossings[0]:.1f}")
        else:
            if np.all(diff_arr > 0):
                print(f"\n  Boundary-law preference dominates throughout (no crossover in range)")
            elif np.all(diff_arr < 0):
                print(f"\n  Volume fit dominates throughout")
            else:
                print(f"\n  Mixed behavior, no clean crossing detected")

    return results_by_G


# ===================================================================
# MAIN
# ===================================================================

def main():
    print("=" * 80)
    print("TRIANGULAR/WILSON ROBUSTNESS PROBE")
    print("Bounded boundary-law transfer on one non-bipartite alternative lattice")
    print("=" * 80)
    print()
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, WILSON_R={WILSON_R}")
    print(f"Evolution: N_STEPS={N_STEPS}, SIGMA={SIGMA}")
    print()

    # ==================================================================
    # Build lattices
    # ==================================================================
    sides = [8, 10, 12]

    print("=" * 80)
    print("SECTION A: TRIANGULAR LATTICE (Wilson fermions, NON-BIPARTITE)")
    print("=" * 80)

    for side in sides:
        n, pos, adj = build_triangular_lattice(side)
        L_sp = build_laplacian(pos, adj, n)

        is_nonbip = verify_nonbipartite(adj, n)
        avg_deg = np.mean([len(adj[i]) for i in range(n)])

        print(f"\n{'='*70}")
        print(f"  Triangular side={side}, n={n}, avg_degree={avg_deg:.1f}, "
              f"non-bipartite={is_nonbip}")
        print(f"{'='*70}")

        if not is_nonbip:
            print("  WARNING: lattice is bipartite! Check construction.")

        # Wrapper for build_H_wilson that matches the signature
        def _build_H(pos, adj, n, phi, mass=MASS):
            return build_H_wilson(pos, adj, n, phi, mass=mass, r=WILSON_R)

        # Probe 1: Area law at moderate G
        t0 = time.time()
        r2_a, r2_v = probe_area_law(f"tri_{side}", n, pos, adj, L_sp,
                                     _build_H, G=10.0)
        print(f"  [Probe 1 time: {time.time()-t0:.1f}s]")

        # Probe 2: spectrum-flow estimator
        t0 = time.time()
        probe_cdt_flow(f"tri_{side}", n, pos, adj, L_sp, _build_H, G=10.0)
        print(f"  [Probe 2 time: {time.time()-t0:.1f}s]")

        # Probe 3: entropy-scaling crossover (only on side=12 to save time)
        # Extended G range for triangular -- any crossover may be at higher G
        if side >= 12:
            t0 = time.time()
            hp_tri = probe_hawking_page(
                f"tri_{side}", n, pos, adj, L_sp, _build_H,
                G_values=[0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0,
                          100.0, 200.0, 400.0])
            print(f"  [Probe 3 time: {time.time()-t0:.1f}s]")

    # ==================================================================
    # Comparison: bipartite square lattice with staggered fermions
    # ==================================================================
    print()
    print("=" * 80)
    print("SECTION B: SQUARE LATTICE (Staggered fermions, BIPARTITE) -- Reference")
    print("=" * 80)

    side = 12
    n, pos, adj, col = build_square_lattice(side)
    L_sp = build_laplacian(pos, adj, n)

    is_nonbip = verify_nonbipartite(adj, n)
    avg_deg = np.mean([len(adj[i]) for i in range(n)])
    print(f"\n  Square side={side}, n={n}, avg_degree={avg_deg:.1f}, "
          f"non-bipartite={is_nonbip}")

    def _build_H_stag(pos, adj, n, phi, mass=MASS):
        return build_H_staggered(pos, col, adj, n, phi, mass=mass)

    t0 = time.time()
    r2_a_ref, r2_v_ref = probe_area_law("square_12", n, pos, adj, L_sp,
                                          _build_H_stag, G=10.0)
    print(f"  [Probe 1 time: {time.time()-t0:.1f}s]")

    t0 = time.time()
    probe_cdt_flow("square_12", n, pos, adj, L_sp, _build_H_stag, G=10.0)
    print(f"  [Probe 2 time: {time.time()-t0:.1f}s]")

    t0 = time.time()
    probe_hawking_page("square_12", n, pos, adj, L_sp, _build_H_stag)
    print(f"  [Probe 3 time: {time.time()-t0:.1f}s]")

    # ==================================================================
    # Summary
    # ==================================================================
    print()
    print("=" * 80)
    print("SUMMARY: Non-Bipartite vs Bipartite")
    print("=" * 80)
    print()
    print("This is a bounded robustness check, not a clean isolation test.")
    print("It changes graph family, fermion discretization, and coupling")
    print("structure at the same time.")
    print()
    print("Key questions:")
    print("  1. Does boundary-law preference survive on triangular/Wilson?")
    print("  2. Does the internal spectrum-flow estimator still rise UV -> IR?")
    print("  3. Does an entropy-fit crossover appear on this different setup?")


if __name__ == "__main__":
    main()
