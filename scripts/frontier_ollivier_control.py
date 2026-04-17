#!/usr/bin/env python3
"""
Ollivier-Ricci Curvature Control Experiment
===========================================

CRITICAL CONTROL: Does Delta_kappa ~ G*T survive when Phi is random
instead of self-consistent?

The concern: V is sourced by |psi|^2, curvature reflects V, T is |psi|^2.
So R^2=0.97 might just be "a function of |psi|^2 correlates with |psi|^2"
-- trivially true.

This runner is mu2-configurable and compares five conditions at each
G in [1, 5, 10, 20, 50]:

1. SELF-CONSISTENT: Phi from screened Poisson sourced by |psi|^2
2. STATIC-INITIAL: Phi from screened Poisson sourced by the initial packet,
   then held fixed throughout the evolution
3. SHELL-AVERAGED: Phi is radially shell-averaged from the self-consistent Phi
   (smooth structured control that removes exact nodewise correlations)
4. RANDOM-MATCHED: Phi is random with same mean/std as self-consistent Phi
   (same |psi|^2 for T, but Phi has no spatial correlation with |psi|^2)
5. SHUFFLED: Phi = self-consistent Phi but randomly permuted across nodes
   (same values/distribution, spatial correlation with |psi|^2 destroyed)

If STATIC-INITIAL also matches SELF-CONSISTENT: the signal is a structured
potential effect, not evidence that dynamic backreaction is load-bearing.
If SHELL-AVERAGED also matches SELF-CONSISTENT: the signal survives smooth
structured controls but still does not isolate the exact self-consistent
update as the essential ingredient.
If SELF-CONSISTENT still wins cleanly: dynamic backreaction matters here too.
"""

from __future__ import annotations

import argparse

import math
import time
from collections import deque

import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from scipy.sparse import eye as speye, lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.stats import linregress

# ── Physical parameters ────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIGMA = 1.5
SIDE = 10

G_VALUES = [1, 5, 10, 20, 50]
N_RANDOM_SEEDS = 10


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


def minimum_image_delta(a: float, b: float, side: int) -> float:
    """Periodic displacement on a 1D torus."""
    delta = b - a
    half = side / 2.0
    if delta > half:
        delta -= side
    elif delta < -half:
        delta += side
    return delta


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


def build_hamiltonian(pos, col, adj, n, phi):
    """Staggered-fermion Hamiltonian with parity coupling."""
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((MASS + phi) * par)

    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            dx = minimum_image_delta(pos[i, 0], pos[j, 0], SIDE)
            dy = minimum_image_delta(pos[i, 1], pos[j, 1], SIDE)
            d = math.hypot(dx, dy)
            d = min(d, 2.0)
            w = 1.0 / max(d, 0.5)
            H[i, j] += -0.5j * w
            H[j, i] += 0.5j * w

    return H.tocsc()


def cn_step(psi, H, dt):
    """Crank-Nicolson time step."""
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


def make_gaussian(pos, n):
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    r2 = (pos[:, 0] - cx)**2 + (pos[:, 1] - cy)**2
    psi = np.exp(-r2 / (2 * SIGMA**2)).astype(complex)
    psi /= np.linalg.norm(psi)
    return psi


def torus_radius_from_center(pos, side: int):
    """Periodic radius from the packet center used by make_gaussian()."""
    cx = (pos[:, 0].max() + pos[:, 0].min()) / 2
    cy = (pos[:, 1].max() + pos[:, 1].min()) / 2
    dx = np.array([minimum_image_delta(cx, x, side) for x in pos[:, 0]])
    dy = np.array([minimum_image_delta(cy, y, side) for y in pos[:, 1]])
    return np.hypot(dx, dy)


def build_shell_averaged_phi(phi, pos, side: int):
    """
    Smooth structured control: preserve the radial profile of Phi but discard
    the exact nodewise self-consistent update.
    """
    radii = torus_radius_from_center(pos, side)
    shell_phi = np.zeros_like(phi)
    rounded = np.round(radii, 8)
    for shell in np.unique(rounded):
        mask = rounded == shell
        shell_phi[mask] = phi[mask].mean()
    return shell_phi


# ── Shortest paths ────────────────────────────────────────────────

def dijkstra(adj, edge_weight, src, n):
    import heapq
    dist = np.full(n, np.inf)
    dist[src] = 0.0
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v in adj[u]:
            key = (min(u, v), max(u, v))
            w = edge_weight.get(key, 1.0)
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def all_pairs_dijkstra(adj, edge_weight, n):
    D = np.zeros((n, n))
    for i in range(n):
        D[i] = dijkstra(adj, edge_weight, i, n)
    return D


def bfs_distances(adj, src, n):
    dist = np.full(n, -1, dtype=int)
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def all_pairs_bfs(adj, n):
    D = np.zeros((n, n), dtype=int)
    for i in range(n):
        D[i] = bfs_distances(adj, i, n)
    return D


# ── Wasserstein-1 distance ────────────────────────────────────────

def wasserstein_1(support_i, weights_i, support_j, weights_j, D):
    m = len(support_i)
    k = len(support_j)
    if m == 0 or k == 0:
        return 0.0

    cost = np.zeros((m, k))
    for a in range(m):
        for b in range(k):
            cost[a, b] = D[support_i[a], support_j[b]]

    n_vars = m * k
    c = cost.flatten()

    A_eq = np.zeros((m + k, n_vars))
    b_eq = np.zeros(m + k)

    for a in range(m):
        for b in range(k):
            A_eq[a, a * k + b] = 1.0
        b_eq[a] = weights_i[a]

    for b in range(k):
        for a in range(m):
            A_eq[m + b, a * k + b] = 1.0
        b_eq[m + b] = weights_j[b]

    result = linprog(c, A_eq=A_eq, b_eq=b_eq,
                     bounds=(0, None), method='highs')

    return result.fun if result.success else 0.0


# ── Ollivier-Ricci curvature (potential-weighted) ─────────────────

def compute_OR_potential_weighted(adj, n, phi):
    """
    Ollivier-Ricci on effective metric: edge distance = 1 + Phi_avg(e).
    Uniform measures, weighted graph distances.
    Matches frontier_ollivier_einstein.py exactly.
    """
    phi_min = phi.min()
    offset = max(0.0, -phi_min + 0.01)

    edge_weight = {}
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            key = (i, j)
            phi_avg = 0.5 * (phi[i] + phi[j])
            edge_weight[key] = 1.0 + phi_avg + offset

    D_w = all_pairs_dijkstra(adj, edge_weight, n)

    kappa = {}
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            key = (i, j)
            d_ij = edge_weight[key]
            if d_ij < 1e-15:
                continue
            nb_i = adj[i]
            nb_j = adj[j]
            m_i = len(nb_i)
            m_j = len(nb_j)
            w_i = np.ones(m_i) / m_i
            w_j = np.ones(m_j) / m_j
            w1 = wasserstein_1(nb_i, w_i, nb_j, w_j, D_w)
            kappa[key] = 1.0 - w1 / d_ij

    return kappa


def compute_OR_uniform(adj, n, D):
    """Standard Ollivier-Ricci with uniform measures on flat graph."""
    kappa = {}
    for i in range(n):
        for j in adj[i]:
            if i >= j:
                continue
            d_ij = D[i, j]
            if d_ij == 0:
                continue
            nb_i = adj[i]
            nb_j = adj[j]
            m_i = len(nb_i)
            m_j = len(nb_j)
            w_i = np.ones(m_i) / m_i
            w_j = np.ones(m_j) / m_j
            w1 = wasserstein_1(nb_i, w_i, nb_j, w_j, D)
            kappa[(i, j)] = 1.0 - w1 / d_ij
    return kappa


# ── Self-consistent gravity evolution ─────────────────────────────

def evolve_with_gravity(pos, col, adj, n, G, L_csr, mu2):
    """Evolve N_STEPS with self-consistent gravity. Return final psi, phi."""
    solve_op = (L_csr + mu2 * speye(n, format='csr')).tocsc()
    psi = make_gaussian(pos, n)
    phi = np.zeros(n)

    for step in range(N_STEPS):
        rho = np.abs(psi)**2
        phi = spsolve(solve_op, G * rho)
        H = build_hamiltonian(pos, col, adj, n, phi)
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)

    return psi, phi


def evolve_with_fixed_phi(pos, col, adj, n, phi):
    """Evolve N_STEPS under a fixed external potential."""
    psi = make_gaussian(pos, n)
    H = build_hamiltonian(pos, col, adj, n, phi)
    for step in range(N_STEPS):
        psi = cn_step(psi, H, DT)
        psi /= np.linalg.norm(psi)
    return psi


def get_edges(adj, n):
    edges = []
    for i in range(n):
        for j in adj[i]:
            if i < j:
                edges.append((i, j))
    return edges


# ── Analysis helper ───────────────────────────────────────────────

def analyze_curvature(kappa_after, kappa_before, edges, rho, G):
    """Compute R^2(Dk vs GT), R^2(Dk vs T), and slope."""
    T_vals = np.array([0.5 * (rho[i] + rho[j]) for (i, j) in edges])
    dk_vals = np.array([kappa_after[e] - kappa_before[e] for e in edges])
    GT_vals = G * T_vals

    mask = np.isfinite(dk_vals) & np.isfinite(GT_vals)
    dk_f = dk_vals[mask]
    GT_f = GT_vals[mask]
    T_f = T_vals[mask]

    if len(dk_f) > 2 and np.std(GT_f) > 1e-15:
        res_GT = linregress(GT_f, dk_f)
        r2_GT = res_GT.rvalue**2
        slope_GT = res_GT.slope
    else:
        r2_GT, slope_GT = 0.0, 0.0

    if len(dk_f) > 2 and np.std(T_f) > 1e-15:
        res_T = linregress(T_f, dk_f)
        r2_T = res_T.rvalue**2
        slope_T = res_T.slope
    else:
        r2_T, slope_T = 0.0, 0.0

    return {
        'r2_GT': r2_GT, 'slope_GT': slope_GT,
        'r2_T': r2_T, 'slope_T': slope_T,
        'dk_mean': dk_vals.mean(), 'dk_std': dk_vals.std(),
        'dk': dk_vals, 'T': T_vals, 'GT': GT_vals,
    }


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mu2", type=float, default=MU2)
    parser.add_argument("--random-seeds", type=int, default=N_RANDOM_SEEDS)
    return parser.parse_args()


def main():
    args = parse_args()
    mu2 = args.mu2
    n_random_seeds = args.random_seeds
    t0 = time.time()

    screening_length = float("inf") if mu2 <= 0 else 1.0 / math.sqrt(mu2)

    print("=" * 78)
    print("OLLIVIER CURVATURE CONTROL EXPERIMENT")
    print("Does Delta_kappa ~ G*T survive with structured controls?")
    print("=" * 78)
    print()
    print(f"Lattice: {SIDE}x{SIDE} periodic staggered (n={SIDE**2})")
    print(f"MASS={MASS}, MU2={mu2}, DT={DT}, N_STEPS={N_STEPS}")
    if math.isfinite(screening_length):
        print(f"screening length ~ {screening_length:.2f} sites")
    else:
        print("screening length = inf")
    print(f"G values: {G_VALUES}")
    print(f"Random seeds per condition: {n_random_seeds}")
    print()

    n, pos, adj, col = build_lattice_2d(SIDE)
    L = build_laplacian(adj, n)
    edges = get_edges(adj, n)
    n_edges = len(edges)
    print(f"Graph: {n} nodes, {n_edges} edges")

    # Baseline curvature (flat, no gravity)
    print("Computing baseline curvature (flat graph, Phi=0)...")
    D0 = all_pairs_bfs(adj, n)
    kappa_before = compute_OR_uniform(adj, n, D0)
    kb_vals = np.array([kappa_before[e] for e in edges])
    print(f"  kappa_before: mean={kb_vals.mean():.6f}, std={kb_vals.std():.6f}")
    print()

    # Storage for results
    results = {
        'self_consistent': {},
        'static_initial': {},
        'shell_averaged': {},
        'random_matched': {},
        'shuffled': {},
    }

    for G in G_VALUES:
        print(f"\n{'='*35} G = {G} {'='*35}")
        tg = time.time()

        # ── Condition 1: SELF-CONSISTENT ──────────────────────────
        print("  [SELF-CONSISTENT] Evolving with self-consistent gravity...")
        psi_sc, phi_sc = evolve_with_gravity(pos, col, adj, n, G, L, mu2)
        rho_sc = np.abs(psi_sc)**2
        print(f"    rho: mean={rho_sc.mean():.6f}, std={rho_sc.std():.6f}")
        print(f"    phi: mean={phi_sc.mean():.6f}, std={phi_sc.std():.6f}")

        kappa_sc = compute_OR_potential_weighted(adj, n, phi_sc)
        res_sc = analyze_curvature(kappa_sc, kappa_before, edges, rho_sc, G)
        results['self_consistent'][G] = res_sc
        print(f"    R2(Dk,GT)={res_sc['r2_GT']:.4f}  "
              f"R2(Dk,T)={res_sc['r2_T']:.4f}  "
              f"slope_GT={res_sc['slope_GT']:.6f}")

        # ── Condition 2: STATIC-INITIAL ───────────────────────────
        print("  [STATIC-INITIAL] Fixed Phi sourced by the initial packet...")
        rho0 = np.abs(make_gaussian(pos, n))**2
        phi_init = spsolve((L + MU2 * speye(n, format='csr')).tocsc(), G * rho0)
        psi_init = evolve_with_fixed_phi(pos, col, adj, n, phi_init)
        rho_init = np.abs(psi_init)**2
        kappa_init = compute_OR_potential_weighted(adj, n, phi_init)
        res_init = analyze_curvature(kappa_init, kappa_before, edges, rho_init, G)
        results['static_initial'][G] = res_init
        print(f"    R2(Dk,GT)={res_init['r2_GT']:.4f}  "
              f"R2(Dk,T)={res_init['r2_T']:.4f}  "
              f"slope_GT={res_init['slope_GT']:.6f}")

        # ── Condition 3: SHELL-AVERAGED ───────────────────────────
        print("  [SHELL-AVERAGED] Smooth radial Phi with exact nodewise structure removed...")
        phi_shell = build_shell_averaged_phi(phi_sc, pos, SIDE)
        psi_shell = evolve_with_fixed_phi(pos, col, adj, n, phi_shell)
        rho_shell = np.abs(psi_shell)**2
        kappa_shell = compute_OR_potential_weighted(adj, n, phi_shell)
        res_shell = analyze_curvature(kappa_shell, kappa_before, edges, rho_shell, G)
        results['shell_averaged'][G] = res_shell
        print(f"    R2(Dk,GT)={res_shell['r2_GT']:.4f}  "
              f"R2(Dk,T)={res_shell['r2_T']:.4f}  "
              f"slope_GT={res_shell['slope_GT']:.6f}")

        # ── Condition 4: RANDOM-MATCHED (10 seeds) ────────────────
        print(f"  [RANDOM-MATCHED] {n_random_seeds} random Phi samples "
              f"(same mean/std as self-consistent)...")
        r2_GT_list = []
        r2_T_list = []
        slope_GT_list = []

        phi_mean = phi_sc.mean()
        phi_std = phi_sc.std()

        for seed in range(n_random_seeds):
            rng = np.random.default_rng(seed + 1000)
            phi_rand = rng.normal(phi_mean, phi_std, size=n)

            # Evolve with random Phi (fixed, not self-consistent)
            # Use same initial psi, evolve under random potential
            psi_rand = make_gaussian(pos, n)
            for step in range(N_STEPS):
                H = build_hamiltonian(pos, col, adj, n, phi_rand)
                psi_rand = cn_step(psi_rand, H, DT)
                psi_rand /= np.linalg.norm(psi_rand)

            rho_rand = np.abs(psi_rand)**2

            kappa_rand = compute_OR_potential_weighted(adj, n, phi_rand)
            res_rand = analyze_curvature(
                kappa_rand, kappa_before, edges, rho_rand, G)
            r2_GT_list.append(res_rand['r2_GT'])
            r2_T_list.append(res_rand['r2_T'])
            slope_GT_list.append(res_rand['slope_GT'])

        results['random_matched'][G] = {
            'r2_GT_mean': np.mean(r2_GT_list),
            'r2_GT_std': np.std(r2_GT_list),
            'r2_T_mean': np.mean(r2_T_list),
            'r2_T_std': np.std(r2_T_list),
            'slope_GT_mean': np.mean(slope_GT_list),
            'slope_GT_std': np.std(slope_GT_list),
        }
        print(f"    R2(Dk,GT)={np.mean(r2_GT_list):.4f} +/- {np.std(r2_GT_list):.4f}  "
              f"R2(Dk,T)={np.mean(r2_T_list):.4f} +/- {np.std(r2_T_list):.4f}")

        # ── Condition 5: SHUFFLED (10 seeds) ──────────────────────
        print(f"  [SHUFFLED] {n_random_seeds} shuffled Phi samples "
              f"(spatial correlation destroyed)...")
        r2_GT_list = []
        r2_T_list = []
        slope_GT_list = []

        for seed in range(n_random_seeds):
            rng = np.random.default_rng(seed + 2000)
            phi_shuf = phi_sc.copy()
            rng.shuffle(phi_shuf)

            # Evolve with shuffled Phi (fixed, not self-consistent)
            psi_shuf = make_gaussian(pos, n)
            for step in range(N_STEPS):
                H = build_hamiltonian(pos, col, adj, n, phi_shuf)
                psi_shuf = cn_step(psi_shuf, H, DT)
                psi_shuf /= np.linalg.norm(psi_shuf)

            rho_shuf = np.abs(psi_shuf)**2

            kappa_shuf = compute_OR_potential_weighted(adj, n, phi_shuf)
            res_shuf = analyze_curvature(
                kappa_shuf, kappa_before, edges, rho_shuf, G)
            r2_GT_list.append(res_shuf['r2_GT'])
            r2_T_list.append(res_shuf['r2_T'])
            slope_GT_list.append(res_shuf['slope_GT'])

        results['shuffled'][G] = {
            'r2_GT_mean': np.mean(r2_GT_list),
            'r2_GT_std': np.std(r2_GT_list),
            'r2_T_mean': np.mean(r2_T_list),
            'r2_T_std': np.std(r2_T_list),
            'slope_GT_mean': np.mean(slope_GT_list),
            'slope_GT_std': np.std(slope_GT_list),
        }
        print(f"    R2(Dk,GT)={np.mean(r2_GT_list):.4f} +/- {np.std(r2_GT_list):.4f}  "
              f"R2(Dk,T)={np.mean(r2_T_list):.4f} +/- {np.std(r2_T_list):.4f}")

        print(f"  G={G} done ({time.time()-tg:.1f}s)")

    # ═══════════════════════════════════════════════════════════════
    # SUMMARY TABLE
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 78)
    print("SUMMARY TABLE: R^2(Delta_kappa vs G*T)")
    print("=" * 78)
    print(f"\n{'G':>5s}  {'SELF-CONSIST':>14s}  {'STATIC-INIT':>14s}  "
          f"{'SHELL-AVG':>14s}  {'RANDOM-MATCH':>20s}  {'SHUFFLED':>20s}")
    print("-" * 100)

    for G in G_VALUES:
        sc = results['self_consistent'][G]
        si = results['static_initial'][G]
        sa = results['shell_averaged'][G]
        rm = results['random_matched'][G]
        sh = results['shuffled'][G]
        print(f"{G:>5d}  {sc['r2_GT']:>14.4f}  {si['r2_GT']:>14.4f}  "
              f"{sa['r2_GT']:>14.4f}  "
              f"{rm['r2_GT_mean']:>8.4f} +/- {rm['r2_GT_std']:.4f}  "
              f"{sh['r2_GT_mean']:>8.4f} +/- {sh['r2_GT_std']:.4f}")

    print(f"\n{'G':>5s}  {'SELF-CONSIST':>14s}  {'STATIC-INIT':>14s}  "
          f"{'SHELL-AVG':>14s}  {'RANDOM-MATCH':>20s}  {'SHUFFLED':>20s}")
    print("-" * 100)
    print("R^2(Delta_kappa vs T):")
    for G in G_VALUES:
        sc = results['self_consistent'][G]
        si = results['static_initial'][G]
        sa = results['shell_averaged'][G]
        rm = results['random_matched'][G]
        sh = results['shuffled'][G]
        print(f"{G:>5d}  {sc['r2_T']:>14.4f}  {si['r2_T']:>14.4f}  "
              f"{sa['r2_T']:>14.4f}  "
              f"{rm['r2_T_mean']:>8.4f} +/- {rm['r2_T_std']:.4f}  "
              f"{sh['r2_T_mean']:>8.4f} +/- {sh['r2_T_std']:.4f}")

    # ═══════════════════════════════════════════════════════════════
    # SLOPE SCALING: slope(Dk vs T) vs G
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 78)
    print("SLOPE SCALING: slope(Delta_kappa vs T) vs G")
    print("=" * 78)

    G_arr = np.array(G_VALUES, dtype=float)

    for label in ['self_consistent', 'static_initial', 'shell_averaged', 'random_matched', 'shuffled']:
        if label in {'self_consistent', 'static_initial', 'shell_averaged'}:
            slopes = [results[label][G]['slope_T'] for G in G_VALUES]
        else:
            slopes = [results[label][G]['slope_GT_mean'] for G in G_VALUES]
        slopes_arr = np.array(slopes)
        if np.std(slopes_arr) > 1e-15:
            meta = linregress(G_arr, slopes_arr)
            meta_r2 = meta.rvalue**2
        else:
            meta_r2 = 0.0
        print(f"  {label:>18s}: R2(slope vs G) = {meta_r2:.4f}")

    # ═══════════════════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)

    sc_r2s = [results['self_consistent'][G]['r2_GT'] for G in G_VALUES]
    si_r2s = [results['static_initial'][G]['r2_GT'] for G in G_VALUES]
    sa_r2s = [results['shell_averaged'][G]['r2_GT'] for G in G_VALUES]
    rm_r2s = [results['random_matched'][G]['r2_GT_mean'] for G in G_VALUES]
    sh_r2s = [results['shuffled'][G]['r2_GT_mean'] for G in G_VALUES]

    mean_sc = np.mean(sc_r2s)
    mean_si = np.mean(si_r2s)
    mean_sa = np.mean(sa_r2s)
    mean_rm = np.mean(rm_r2s)
    mean_sh = np.mean(sh_r2s)

    print(f"\n  Mean R^2(Dk vs GT) across G values:")
    print(f"    SELF-CONSISTENT: {mean_sc:.4f}")
    print(f"    STATIC-INITIAL:  {mean_si:.4f}")
    print(f"    SHELL-AVERAGED:  {mean_sa:.4f}")
    print(f"    RANDOM-MATCHED:  {mean_rm:.4f}")
    print(f"    SHUFFLED:        {mean_sh:.4f}")

    ratio_si = mean_sc / max(mean_si, 1e-10)
    ratio_sa = mean_sc / max(mean_sa, 1e-10)
    ratio_rm = mean_sc / max(mean_rm, 1e-10)
    ratio_sh = mean_sc / max(mean_sh, 1e-10)
    print(f"\n  R^2 ratio (self-consistent / static-initial): {ratio_si:.2f}x")
    print(f"  R^2 ratio (self-consistent / shell-averaged): {ratio_sa:.2f}x")
    print(f"\n  R^2 ratio (self-consistent / random):  {ratio_rm:.2f}x")
    print(f"  R^2 ratio (self-consistent / shuffled): {ratio_sh:.2f}x")

    # The key discriminant: does self-consistent beat controls?
    if mean_sc > 0.5 and mean_si < 0.3 and mean_sa < 0.3 and mean_rm < 0.3 and mean_sh < 0.3:
        print("\n  GENUINE: Self-consistent Phi produces much higher R^2")
        print("  than static, shell-averaged, random, or shuffled controls. Dynamic")
        print("  backreaction matters; this is not just a structured potential.")
    elif mean_sc > 0.5 and (mean_si > 0.8 * mean_sc or mean_sa > 0.8 * mean_sc) and mean_rm < 0.1 and mean_sh < 0.1:
        print("\n  STRUCTURED-POTENTIAL: Self-consistent and at least one")
        print("  smooth structured control produce the correlation, while")
        print("  random/shuffled do not. The signal is real but does not")
        print("  isolate dynamic backreaction.")
    elif mean_sc > mean_rm * 1.5 and mean_sc > mean_sh * 1.5:
        print("\n  PARTIAL: Self-consistent Phi gives meaningfully higher R^2")
        print("  than controls, but the gap is not overwhelming.")
        print("  Spatial self-consistency matters, but result needs scrutiny.")
    elif mean_sc > 0.5 and (mean_rm > 0.3 or mean_sh > 0.3):
        print("\n  SUSPICIOUS: Controls also show high R^2.")
        print("  The Dk~G*T correlation may be partly tautological.")
        print("  The potential-weighted curvature inherently reflects |psi|^2.")
    else:
        print("\n  INCONCLUSIVE: Neither self-consistent nor controls show")
        print("  strong Dk~G*T correlation at this lattice size.")

    elapsed = time.time() - t0
    print(f"\n  Total time: {elapsed:.1f}s")

    # ── Plot ───────────────────────────────────────────────────────
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(4, len(G_VALUES),
                                 figsize=(4 * len(G_VALUES), 12))
        fig.suptitle('Ollivier Curvature Control Experiment\n'
                     r'$\Delta\kappa$ vs $G \cdot T$: '
                     r'Self-Consistent vs Static vs Random vs Shuffled $\Phi$',
                     fontsize=13, fontweight='bold')

        conditions = ['self_consistent', 'static_initial', 'shell_averaged', 'random_matched', 'shuffled']
        condition_labels = ['Self-Consistent', 'Static-Initial', 'Shell-Averaged', 'Random-Matched', 'Shuffled']
        colors = ['steelblue', 'darkorange', 'purple', 'firebrick', 'forestgreen']

        for row, (cond, clabel, cc) in enumerate(
                zip(conditions, condition_labels, colors)):
            for col_idx, G in enumerate(G_VALUES):
                ax = axes[row, col_idx]
                if cond in {'self_consistent', 'static_initial', 'shell_averaged'}:
                    r = results[cond][G]
                    GT = r['GT'] if 'GT' in r else G * r['T']
                    ax.scatter(GT, r['dk'], alpha=0.4, s=12, c=cc)
                    r2 = r['r2_GT']

                    if r2 > 0:
                        x_line = np.linspace(GT.min(), GT.max(), 50)
                        sl = r['slope_GT']
                        inter = r['dk'].mean() - sl * GT.mean()
                        ax.plot(x_line, sl * x_line + inter, 'k-', lw=2)

                    ax.set_title(f'{clabel} G={G}\nR2={r2:.3f}', fontsize=9)
                else:
                    r = results[cond][G]
                    r2 = r['r2_GT_mean']
                    r2_std = r['r2_GT_std']
                    ax.text(0.5, 0.5,
                            f'R2 = {r2:.3f}\n+/- {r2_std:.3f}',
                            transform=ax.transAxes, ha='center', va='center',
                            fontsize=14, fontweight='bold', color=cc)
                    ax.set_title(f'{clabel} G={G}', fontsize=9)

                if col_idx == 0:
                    ax.set_ylabel(r'$\Delta\kappa$')
                if row == len(conditions) - 1:
                    ax.set_xlabel(r'$G \cdot T$')

        plt.tight_layout()
        out_path = __file__.replace('.py', '.png')
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")

        # Bar chart comparison
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        fig2.suptitle('Control Experiment: R^2 by Condition and G',
                      fontsize=13, fontweight='bold')

        x = np.arange(len(G_VALUES))
        width = 0.2

        sc_vals = [results['self_consistent'][G]['r2_GT'] for G in G_VALUES]
        si_vals = [results['static_initial'][G]['r2_GT'] for G in G_VALUES]
        sa_vals = [results['shell_averaged'][G]['r2_GT'] for G in G_VALUES]
        rm_vals = [results['random_matched'][G]['r2_GT_mean'] for G in G_VALUES]
        rm_errs = [results['random_matched'][G]['r2_GT_std'] for G in G_VALUES]
        sh_vals = [results['shuffled'][G]['r2_GT_mean'] for G in G_VALUES]
        sh_errs = [results['shuffled'][G]['r2_GT_std'] for G in G_VALUES]

        ax2.bar(x - 2.0 * width, sc_vals, width, label='Self-Consistent',
                color='steelblue', alpha=0.8)
        ax2.bar(x - 1.0 * width, si_vals, width, label='Static-Initial',
                color='darkorange', alpha=0.8)
        ax2.bar(x + 0.0 * width, sa_vals, width, label='Shell-Averaged',
                color='purple', alpha=0.8)
        ax2.bar(x + 1.0 * width, rm_vals, width, yerr=rm_errs, label='Random-Matched',
                color='firebrick', alpha=0.8, capsize=4)
        ax2.bar(x + 2.0 * width, sh_vals, width, yerr=sh_errs, label='Shuffled',
                color='forestgreen', alpha=0.8, capsize=4)

        ax2.set_xlabel('G')
        ax2.set_ylabel(r'$R^2(\Delta\kappa, G \cdot T)$')
        ax2.set_xticks(x)
        ax2.set_xticklabels([str(g) for g in G_VALUES])
        ax2.legend()
        ax2.set_ylim(0, 1.05)
        ax2.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5,
                     label='threshold')

        plt.tight_layout()
        out2 = __file__.replace('.py', '_bars.png')
        plt.savefig(out2, dpi=150)
        print(f"Bar chart saved to {out2}")

    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    print("\nDone.")


if __name__ == '__main__':
    main()
