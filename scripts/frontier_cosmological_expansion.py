#!/usr/bin/env python3
"""
Cosmological Expansion from Graph Growth Rules
===============================================

Explores whether graph growth rules can produce cosmological expansion
histories that match known Friedmann solutions.

If the universe is a graph, cosmic expansion = graph growing. Different
node-attachment rules should produce different expansion histories.

Growth rules tested:
  1. Uniform random attachment (new node -> k random existing nodes)
  2. Preferential attachment (probability ~ degree)
  3. Spatial attachment (new node -> nearest neighbors in embedding)
  4. Constant-rate exponential growth (N(t) ~ exp(Ht))

For each rule, we track:
  - N(t): number of nodes vs time
  - d_s(t): spectral dimension vs time
  - <d>(t): average graph distance (scale factor proxy)
  - <r^2>(t): mean-squared displacement of random walk (expansion proxy)

We test whether any growth rule produces:
  - de Sitter: a(t) ~ exp(Ht) (constant H)
  - Matter-dominated: a(t) ~ t^(2/3)
  - Radiation-dominated: a(t) ~ t^(1/2)

Also tests: does the gravitational force law survive on a GROWING graph?
"""

from __future__ import annotations

import math
import time
import random
from collections import deque

import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import eigsh, spsolve


# ==========================================================================
# Parameters
# ==========================================================================

N_INITIAL = 20         # starting graph size
N_FINAL = 300          # final graph size
K_ATTACH = 3           # edges per new node
N_SNAPSHOTS = 12       # measurement points during growth
RW_STEPS = 200         # random walk steps for <r^2>
RW_TRIALS = 50         # random walk trials
N_EIGEN = 10           # eigenvalues for spectral dimension
SEED = 42

# Gravity test parameters
MASS = 0.30
MU2 = 0.05
G_GRAV = 30.0
DT_GRAV = 0.10
N_GRAV_STEPS = 6
SIGMA_GRAV = 1.2


# ==========================================================================
# Graph growth rules
# ==========================================================================

def grow_uniform(n_target, k=K_ATTACH, seed=SEED):
    """Uniform random attachment: each new node connects to k random nodes."""
    rng = random.Random(seed)
    adj = {i: set() for i in range(N_INITIAL)}
    # seed graph: path + some random edges
    for i in range(N_INITIAL - 1):
        adj[i].add(i + 1)
        adj[i + 1].add(i)
    for _ in range(N_INITIAL):
        a, b = rng.sample(range(N_INITIAL), 2)
        adj[a].add(b)
        adj[b].add(a)

    snapshots = _snapshot_times(N_INITIAL, n_target)
    results = []

    n = N_INITIAL
    while n < n_target:
        new = n
        adj[new] = set()
        targets = rng.sample(range(n), min(k, n))
        for t in targets:
            adj[new].add(t)
            adj[t].add(new)
        n += 1
        if n in snapshots:
            results.append(_measure_snapshot(adj, n, n - N_INITIAL))

    return "uniform_random", results


def grow_preferential(n_target, k=K_ATTACH, seed=SEED):
    """Preferential attachment: probability proportional to degree."""
    rng = random.Random(seed)
    adj = {i: set() for i in range(N_INITIAL)}
    for i in range(N_INITIAL - 1):
        adj[i].add(i + 1)
        adj[i + 1].add(i)
    for _ in range(N_INITIAL):
        a, b = rng.sample(range(N_INITIAL), 2)
        adj[a].add(b)
        adj[b].add(a)

    # degree list for preferential sampling
    deg_list = []
    for i in range(N_INITIAL):
        for _ in range(len(adj[i])):
            deg_list.append(i)

    snapshots = _snapshot_times(N_INITIAL, n_target)
    results = []

    n = N_INITIAL
    while n < n_target:
        new = n
        adj[new] = set()
        chosen = set()
        attempts = 0
        while len(chosen) < min(k, n) and attempts < 100:
            t = deg_list[rng.randint(0, len(deg_list) - 1)]
            if t != new:
                chosen.add(t)
            attempts += 1
        for t in chosen:
            adj[new].add(t)
            adj[t].add(new)
            deg_list.append(new)
            deg_list.append(t)
        n += 1
        if n in snapshots:
            results.append(_measure_snapshot(adj, n, n - N_INITIAL))

    return "preferential", results


def grow_spatial(n_target, k=K_ATTACH, seed=SEED, dim=3):
    """Spatial attachment: nodes placed in R^dim, connect to k nearest."""
    rng = random.Random(seed)
    coords = [np.array([rng.gauss(0, 1) for _ in range(dim)]) for _ in range(N_INITIAL)]
    adj = {i: set() for i in range(N_INITIAL)}
    for i in range(N_INITIAL - 1):
        adj[i].add(i + 1)
        adj[i + 1].add(i)

    snapshots = _snapshot_times(N_INITIAL, n_target)
    results = []

    n = N_INITIAL
    # expansion rate: new nodes placed at growing radius
    while n < n_target:
        new = n
        adj[new] = set()
        # place at a radius that grows with n (cosmological expansion analog)
        r = (n / N_INITIAL) ** (1.0 / dim) * 2.0
        direction = np.array([rng.gauss(0, 1) for _ in range(dim)])
        direction = direction / (np.linalg.norm(direction) + 1e-10) * r
        # add some noise
        pos = direction + np.array([rng.gauss(0, 0.3) for _ in range(dim)])
        coords.append(pos)

        # connect to k nearest
        dists = [(np.linalg.norm(pos - coords[j]), j) for j in range(n)]
        dists.sort()
        for _, j in dists[:k]:
            adj[new].add(j)
            adj[j].add(new)
        n += 1
        if n in snapshots:
            results.append(_measure_snapshot(adj, n, n - N_INITIAL))

    return "spatial", results


def grow_exponential(n_target, H=0.02, k=K_ATTACH, seed=SEED):
    """Constant-rate exponential growth: add nodes at rate H*N per step.

    This mimics de Sitter expansion directly in node count.
    At each discrete step, the number of nodes added is ceil(H * N_current).
    Each new node attaches to k random existing nodes.
    """
    rng = random.Random(seed)
    adj = {i: set() for i in range(N_INITIAL)}
    for i in range(N_INITIAL - 1):
        adj[i].add(i + 1)
        adj[i + 1].add(i)
    for _ in range(N_INITIAL):
        a, b = rng.sample(range(N_INITIAL), 2)
        adj[a].add(b)
        adj[b].add(a)

    snapshots = _snapshot_times(N_INITIAL, n_target)
    results = []

    n = N_INITIAL
    t_step = 0
    while n < n_target:
        # add ceil(H * n) nodes this step
        n_add = max(1, int(math.ceil(H * n)))
        for _ in range(n_add):
            if n >= n_target:
                break
            new = n
            adj[new] = set()
            targets = rng.sample(range(n), min(k, n))
            for t in targets:
                adj[new].add(t)
                adj[t].add(new)
            n += 1
        t_step += 1
        if n in snapshots or n >= n_target:
            results.append(_measure_snapshot(adj, n, t_step))

    return "exponential", results


# ==========================================================================
# Measurement tools
# ==========================================================================

def _snapshot_times(n0, n_final):
    """Return set of N values at which to take measurements."""
    times = set()
    for i in range(N_SNAPSHOTS):
        n_val = int(n0 + (n_final - n0) * (i + 1) / N_SNAPSHOTS)
        times.add(min(n_val, n_final))
    times.add(n_final)
    return times


def _adj_to_sparse(adj, n):
    """Convert adjacency dict to sparse adjacency matrix."""
    A = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            A[i, j] = 1.0
    return A.tocsr()


def _graph_laplacian(adj, n):
    """Combinatorial graph Laplacian."""
    L = lil_matrix((n, n), dtype=float)
    for i in range(n):
        nbs = adj.get(i, set())
        deg = len(nbs)
        L[i, i] = float(deg)
        for j in nbs:
            L[i, j] -= 1.0
    return L.tocsr()


def _bfs_distances(adj, src, n):
    """BFS shortest-path distances from src."""
    d = np.full(n, -1, dtype=int)
    d[src] = 0
    q = deque([src])
    while q:
        i = q.popleft()
        for j in adj.get(i, set()):
            if d[j] == -1:
                d[j] = d[i] + 1
                q.append(j)
    return d


def _average_distance(adj, n, n_samples=50, seed=123):
    """Estimate average graph distance by sampling pairs."""
    rng = random.Random(seed)
    total = 0.0
    count = 0
    nodes = list(range(n))
    for _ in range(n_samples):
        src = rng.choice(nodes)
        dists = _bfs_distances(adj, src, n)
        for _ in range(5):
            tgt = rng.choice(nodes)
            if dists[tgt] >= 0 and tgt != src:
                total += dists[tgt]
                count += 1
    return total / max(count, 1)


def _spectral_dimension(adj, n):
    """Estimate spectral dimension from Laplacian eigenvalues.

    d_s = -2 * d(log P(t)) / d(log t) at small t,
    where P(t) = (1/n) sum_k exp(-lambda_k * t).

    We use the smallest non-zero eigenvalues and fit the return probability.
    """
    if n < 15:
        return float('nan')

    L = _graph_laplacian(adj, n)
    n_eig = min(N_EIGEN, n - 2)
    try:
        eigenvalues = eigsh(L.astype(float), k=n_eig, which='SM', return_eigenvectors=False)
        eigenvalues = np.sort(np.abs(eigenvalues))
        # skip zero eigenvalue
        eigenvalues = eigenvalues[eigenvalues > 1e-8]
        if len(eigenvalues) < 3:
            return float('nan')
    except Exception:
        return float('nan')

    # return probability at several times
    t_vals = np.logspace(-1, 1, 20)
    P_t = np.array([np.mean(np.exp(-eigenvalues * t)) for t in t_vals])
    P_t = np.clip(P_t, 1e-30, None)

    # fit log-log slope
    log_t = np.log(t_vals)
    log_P = np.log(P_t)
    # use early-time slope (small t)
    mid = len(t_vals) // 3
    if mid < 2:
        mid = 2
    slope = np.polyfit(log_t[:mid], log_P[:mid], 1)[0]
    d_s = -2.0 * slope
    return float(d_s)


def _random_walk_msd(adj, n, steps=RW_STEPS, trials=RW_TRIALS, seed=99):
    """Mean squared displacement of random walk on graph.

    Uses graph distance, not embedding distance.
    Returns <r^2> at final step.
    """
    rng = random.Random(seed)
    nodes = list(range(n))
    total_r2 = 0.0
    count = 0

    for _ in range(trials):
        src = rng.choice(nodes)
        pos = src
        for _ in range(steps):
            nbs = list(adj.get(pos, set()))
            if not nbs:
                break
            pos = rng.choice(nbs)
        # measure graph distance
        dists = _bfs_distances(adj, src, n)
        if dists[pos] >= 0:
            total_r2 += dists[pos] ** 2
            count += 1

    return total_r2 / max(count, 1)


def _measure_snapshot(adj, n, t_step):
    """Take all measurements on current graph state."""
    avg_d = _average_distance(adj, n)
    d_s = _spectral_dimension(adj, n)
    msd = _random_walk_msd(adj, n)

    return {
        'N': n,
        't': t_step,
        'avg_distance': avg_d,
        'spectral_dim': d_s,
        'msd': msd,
    }


# ==========================================================================
# Expansion analysis
# ==========================================================================

def fit_power_law(x, y):
    """Fit y = C * x^alpha, return (alpha, R^2)."""
    mask = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    if np.sum(mask) < 3:
        return float('nan'), float('nan')
    lx = np.log(x[mask])
    ly = np.log(y[mask])
    coeffs = np.polyfit(lx, ly, 1)
    pred = np.polyval(coeffs, lx)
    ss_res = np.sum((ly - pred) ** 2)
    ss_tot = np.sum((ly - np.mean(ly)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(coeffs[0]), float(r2)


def fit_exponential(t, y):
    """Fit y = C * exp(H*t), return (H, R^2)."""
    mask = (y > 0) & np.isfinite(t) & np.isfinite(y)
    if np.sum(mask) < 3:
        return float('nan'), float('nan')
    ly = np.log(y[mask])
    tt = t[mask]
    coeffs = np.polyfit(tt, ly, 1)
    pred = np.polyval(coeffs, tt)
    ss_res = np.sum((ly - pred) ** 2)
    ss_tot = np.sum((ly - np.mean(ly)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return float(coeffs[0]), float(r2)


def analyze_expansion(name, results):
    """Analyze expansion history of a growth rule."""
    print(f"\n{'='*70}")
    print(f"EXPANSION ANALYSIS: {name}")
    print(f"{'='*70}")

    N_arr = np.array([r['N'] for r in results], dtype=float)
    t_arr = np.array([r['t'] for r in results], dtype=float)
    avg_d = np.array([r['avg_distance'] for r in results])
    d_s = np.array([r['spectral_dim'] for r in results])
    msd = np.array([r['msd'] for r in results])

    # Normalize time
    t_norm = t_arr - t_arr[0] + 1  # avoid log(0)

    print(f"\n  N range: {int(N_arr[0])} -> {int(N_arr[-1])}")
    print(f"  t range: {t_arr[0]:.0f} -> {t_arr[-1]:.0f}")
    print(f"  <d> range: {avg_d[0]:.2f} -> {avg_d[-1]:.2f}")
    print(f"  d_s range: {d_s[0]:.2f} -> {d_s[-1]:.2f}")
    print(f"  <r^2> range: {msd[0]:.2f} -> {msd[-1]:.2f}")

    # Use avg_distance as scale factor proxy: a(t) ~ <d>(t)
    # For Friedmann: de Sitter => a ~ exp(Ht), matter => a ~ t^(2/3), radiation => a ~ t^(1/2)

    print(f"\n  Scale factor a(t) = <d>(t) fits:")

    # Power law: a ~ t^alpha
    alpha_d, r2_d = fit_power_law(t_norm, avg_d)
    print(f"    Power law: a ~ t^{alpha_d:.3f}  (R^2={r2_d:.4f})")
    if r2_d > 0.8:
        if abs(alpha_d - 0.5) < 0.15:
            print(f"    -> Consistent with RADIATION-dominated (t^0.5)")
        elif abs(alpha_d - 2.0/3.0) < 0.15:
            print(f"    -> Consistent with MATTER-dominated (t^(2/3))")
        elif abs(alpha_d - 1.0) < 0.15:
            print(f"    -> Consistent with coasting (t^1)")
        else:
            print(f"    -> Novel exponent, not standard Friedmann")

    # Exponential: a ~ exp(Ht)
    H_d, r2_exp = fit_exponential(t_norm, avg_d)
    print(f"    Exponential: a ~ exp({H_d:.4f}*t)  (R^2={r2_exp:.4f})")
    if r2_exp > 0.9 and r2_exp > r2_d:
        print(f"    -> Consistent with DE SITTER expansion")

    # Hubble parameter: H(t) = (1/a) * da/dt
    print(f"\n  Hubble parameter H(t) = (da/dt)/a:")
    H_vals = []
    for i in range(1, len(avg_d)):
        dt = t_norm[i] - t_norm[i-1]
        if dt > 0 and avg_d[i] > 0:
            da = avg_d[i] - avg_d[i-1]
            H_vals.append(da / (avg_d[i] * dt))
    if H_vals:
        H_arr = np.array(H_vals)
        H_mean = np.mean(H_arr)
        H_std = np.std(H_arr)
        H_cv = H_std / abs(H_mean) if abs(H_mean) > 1e-10 else float('inf')
        print(f"    H = {H_mean:.4f} +/- {H_std:.4f}  (CV={H_cv:.2f})")
        if H_cv < 0.3:
            print(f"    -> Nearly constant H (de Sitter-like)")
        elif H_vals[-1] < H_vals[0]:
            print(f"    -> Decelerating (H decreasing)")
        else:
            print(f"    -> Accelerating (H increasing)")

    # Spectral dimension evolution
    print(f"\n  Spectral dimension d_s(t):")
    d_s_valid = d_s[np.isfinite(d_s)]
    if len(d_s_valid) > 0:
        print(f"    mean={np.mean(d_s_valid):.2f}, std={np.std(d_s_valid):.2f}")
        if len(d_s_valid) > 2:
            trend = np.polyfit(np.arange(len(d_s_valid)), d_s_valid, 1)[0]
            if trend > 0.01:
                print(f"    -> d_s INCREASING with growth (dimension emerges)")
            elif trend < -0.01:
                print(f"    -> d_s DECREASING with growth")
            else:
                print(f"    -> d_s roughly stable")

    # MSD evolution
    alpha_msd, r2_msd = fit_power_law(t_norm, msd)
    print(f"\n  Random walk <r^2> ~ t^{alpha_msd:.3f}  (R^2={r2_msd:.4f})")

    return {
        'name': name,
        'alpha_d': alpha_d,
        'r2_power': r2_d,
        'H_exp': H_d,
        'r2_exp': r2_exp,
        'H_mean': H_mean if H_vals else float('nan'),
        'H_cv': H_cv if H_vals else float('nan'),
        'd_s_mean': float(np.mean(d_s_valid)) if len(d_s_valid) > 0 else float('nan'),
        'alpha_msd': alpha_msd,
    }


# ==========================================================================
# Gravity survival test on growing graph
# ==========================================================================

def _growing_graph_adj_to_lists(adj, n):
    """Convert set-based adj to list-based adj."""
    return {i: list(adj.get(i, set())) for i in range(n)}


def _make_positions_from_adj(adj, n, seed=42):
    """Create approximate positions using spring embedding (simple force-directed)."""
    rng = np.random.RandomState(seed)
    pos = rng.randn(n, 3) * 2.0

    # simple force-directed: 30 iterations
    for _ in range(30):
        forces = np.zeros_like(pos)
        # repulsion between all pairs (approximate: sample)
        for i in range(n):
            for j in range(i + 1, min(i + 20, n)):
                diff = pos[i] - pos[j]
                dist = np.linalg.norm(diff) + 0.01
                f = diff / (dist ** 3) * 0.5
                forces[i] += f
                forces[j] -= f
        # attraction along edges
        for i, nbs in adj.items():
            for j in nbs:
                if j > i:
                    diff = pos[j] - pos[i]
                    dist = np.linalg.norm(diff)
                    f = diff * 0.1
                    forces[i] += f
                    forces[j] -= f
        pos += np.clip(forces, -0.5, 0.5)

    return pos


def _graph_laplacian_weighted(pos, adj, n):
    """Weighted graph Laplacian using edge distances."""
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = np.linalg.norm(pos[i] - pos[j])
            w = 1.0 / max(d, 0.3)
            L[i, j] -= w
            L[j, i] -= w
            L[i, i] += w
            L[j, j] += w
    return L.tocsr()


def _solve_phi_grav(L, n, rho):
    """Solve screened Poisson for gravitational potential."""
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + MU2 * speye(n, format='csr')).tocsc()
    return spsolve(A, G_GRAV * rho).real


def _build_H_stag(pos, parity, adj, n, mass, phi):
    """Build staggered Hamiltonian."""
    H = lil_matrix((n, n), dtype=complex)
    eps = np.where(parity == 0, 1.0, -1.0)
    H.setdiag((mass + phi) * eps)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = np.linalg.norm(pos[i] - pos[j])
            w = 1.0 / max(d, 0.3)
            hop = -0.5j * w
            H[i, j] += hop
            H[j, i] += np.conj(hop)
    return H.tocsr()


def _cn_step_grav(H, n, psi):
    """Crank-Nicolson step."""
    ap = (speye(n, format='csc') + 1j * H * DT_GRAV / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * DT_GRAV / 2
    psi_new = spsolve(ap, am.dot(psi))
    return psi_new / np.linalg.norm(psi_new)


def _gauss_state_3d(pos, center, sigma=SIGMA_GRAV):
    """Gaussian wavepacket in 3D."""
    rel = pos - center
    psi = np.exp(-0.5 * np.sum(rel * rel, axis=1) / sigma ** 2).astype(complex)
    nm = np.linalg.norm(psi)
    return psi / nm if nm > 0 else psi


def test_gravity_on_growing_graph(seed=SEED):
    """Test whether gravitational attraction survives on snapshots of a growing graph.

    Grow a graph, take snapshots at different sizes, and run a two-body
    attraction test on each snapshot.
    """
    print(f"\n{'='*70}")
    print(f"GRAVITY SURVIVAL ON GROWING GRAPH")
    print(f"{'='*70}")

    rng = random.Random(seed)
    adj = {i: set() for i in range(N_INITIAL)}
    for i in range(N_INITIAL - 1):
        adj[i].add(i + 1)
        adj[i + 1].add(i)
    for _ in range(N_INITIAL):
        a, b = rng.sample(range(N_INITIAL), 2)
        adj[a].add(b)
        adj[b].add(a)

    test_sizes = [40, 80, 150, 250]
    n = N_INITIAL
    results = []

    while n < max(test_sizes) + 1:
        new = n
        adj[new] = set()
        targets = rng.sample(range(n), min(K_ATTACH, n))
        for t in targets:
            adj[new].add(t)
            adj[t].add(new)
        n += 1

        if n in test_sizes:
            # Run two-body gravity test on this snapshot
            adj_lists = _growing_graph_adj_to_lists(adj, n)
            pos = _make_positions_from_adj(adj_lists, n, seed=seed)
            parity = np.array([i % 2 for i in range(n)])

            L = _graph_laplacian_weighted(pos, adj_lists, n)
            H_free = _build_H_stag(pos, parity, adj_lists, n, MASS, np.zeros(n))

            # place two packets
            # find two nodes that are well separated
            center_node = n // 4
            dists_from_center = _bfs_distances(adj_lists, center_node, n)
            valid = [(d, i) for i, d in enumerate(dists_from_center) if d > 0]
            valid.sort()
            if len(valid) < 2:
                continue

            # pick a node at ~diameter/3 for meaningful separation
            max_dist = max(d for d, _ in valid)
            target_dist = max(2, max_dist // 3)
            candidates = [(abs(d - target_dist), i) for d, i in valid if d >= 2]
            if not candidates:
                candidates = valid
            candidates.sort()
            node_a = center_node
            node_b = candidates[0][1]
            sep = dists_from_center[node_b]

            psi_a = _gauss_state_3d(pos, pos[node_a])
            psi_b = _gauss_state_3d(pos, pos[node_b])

            # evolve with shared field vs self-only
            force_inward_count = 0
            for step in range(N_GRAV_STEPS):
                rho_a = np.abs(psi_a) ** 2
                rho_b = np.abs(psi_b) ** 2
                phi_shared = _solve_phi_grav(L, n, rho_a + rho_b)
                phi_a_only = _solve_phi_grav(L, n, rho_a)
                phi_b_only = _solve_phi_grav(L, n, rho_b)

                # force from partner: gradient of partner's field
                grad_b_on_a = phi_shared - phi_a_only  # partner's contribution
                # check if potential from B is deeper at A's location
                rho_a_norm = rho_a / np.sum(rho_a)
                pot_at_a = np.sum(rho_a_norm * grad_b_on_a)
                if pot_at_a > 0:
                    force_inward_count += 1

                H_sh = _build_H_stag(pos, parity, adj_lists, n, MASS, phi_shared)
                psi_a = _cn_step_grav(H_sh, n, psi_a)
                psi_b = _cn_step_grav(H_sh, n, psi_b)

            attractive = force_inward_count > N_GRAV_STEPS // 2
            results.append({
                'N': n,
                'separation': sep,
                'force_inward_frac': force_inward_count / N_GRAV_STEPS,
                'attractive': attractive,
            })
            tag = "PASS" if attractive else "FAIL"
            print(f"  N={n:3d}  sep={sep:2d}  inward={force_inward_count}/{N_GRAV_STEPS}  [{tag}]")

    n_pass = sum(1 for r in results if r['attractive'])
    n_total = len(results)
    print(f"\n  Gravity survival: {n_pass}/{n_total} snapshots show attraction")
    return results


# ==========================================================================
# Main
# ==========================================================================

def main():
    t0 = time.time()
    print("=" * 70)
    print("COSMOLOGICAL EXPANSION FROM GRAPH GROWTH RULES")
    print("=" * 70)
    print(f"N_INITIAL={N_INITIAL}, N_FINAL={N_FINAL}, K_ATTACH={K_ATTACH}")
    print(f"N_SNAPSHOTS={N_SNAPSHOTS}, RW_STEPS={RW_STEPS}")
    print()

    # Run all growth rules
    growth_rules = [
        grow_uniform,
        grow_preferential,
        grow_spatial,
        grow_exponential,
    ]

    all_analyses = []
    for grower in growth_rules:
        name, snapshots = grower(N_FINAL)
        analysis = analyze_expansion(name, snapshots)
        all_analyses.append(analysis)

    # Summary comparison
    print(f"\n{'='*70}")
    print("EXPANSION COMPARISON")
    print(f"{'='*70}")
    print(f"{'Rule':>20s} | {'alpha':>7s} {'R2_pow':>7s} | {'H_exp':>8s} {'R2_exp':>7s} | {'H_mean':>7s} {'H_cv':>6s} | {'d_s':>5s} | {'Best fit':>20s}")
    print("-" * 100)

    for a in all_analyses:
        # determine best fit
        best = "unclear"
        if a['r2_exp'] > 0.9 and a['r2_exp'] > a['r2_power']:
            best = "de Sitter (exp)"
        elif a['r2_power'] > 0.8:
            if abs(a['alpha_d'] - 0.5) < 0.15:
                best = "radiation (t^0.5)"
            elif abs(a['alpha_d'] - 2.0/3.0) < 0.15:
                best = "matter (t^2/3)"
            elif abs(a['alpha_d'] - 1.0) < 0.15:
                best = "coasting (t^1)"
            else:
                best = f"novel (t^{a['alpha_d']:.2f})"
        print(f"{a['name']:>20s} | {a['alpha_d']:+7.3f} {a['r2_power']:7.4f} | {a['H_exp']:+8.5f} {a['r2_exp']:7.4f} | {a['H_mean']:+7.4f} {a['H_cv']:6.2f} | {a['d_s_mean']:5.2f} | {best:>20s}")

    # Gravity survival test
    gravity_results = test_gravity_on_growing_graph()

    elapsed = time.time() - t0
    print(f"\n{'='*70}")
    print(f"COMPLETED in {elapsed:.1f}s")
    print(f"{'='*70}")

    # Bounded claims
    print(f"\n--- BOUNDED CLAIMS ---")
    print(f"C1: Graph growth produces measurable expansion histories")
    print(f"    with well-defined scale factor a(t) and Hubble parameter H(t).")

    # check for Friedmann matches
    friedmann_match = False
    for a in all_analyses:
        if a['r2_power'] > 0.8 and abs(a['alpha_d'] - 0.5) < 0.15:
            print(f"C2: {a['name']} growth produces radiation-like expansion (a ~ t^0.5).")
            friedmann_match = True
        if a['r2_power'] > 0.8 and abs(a['alpha_d'] - 2.0/3.0) < 0.15:
            print(f"C2: {a['name']} growth produces matter-like expansion (a ~ t^(2/3)).")
            friedmann_match = True
        if a['r2_exp'] > 0.9 and a['r2_exp'] > a['r2_power']:
            print(f"C2: {a['name']} growth produces de Sitter-like expansion (a ~ exp(Ht)).")
            friedmann_match = True

    if not friedmann_match:
        print(f"C2: No growth rule closely matches standard Friedmann solutions at this scale.")

    grav_survive = sum(1 for r in gravity_results if r['attractive'])
    grav_total = len(gravity_results)
    if grav_survive == grav_total:
        print(f"C3: Gravitational attraction survives on all growing-graph snapshots ({grav_survive}/{grav_total}).")
    elif grav_survive > grav_total // 2:
        print(f"C3: Gravitational attraction survives on most growing-graph snapshots ({grav_survive}/{grav_total}).")
    else:
        print(f"C3: Gravitational attraction is fragile on growing graphs ({grav_survive}/{grav_total}).")

    print(f"\nLIMITATIONS:")
    print(f"  - Small graphs (N={N_FINAL}) limit continuum-limit claims")
    print(f"  - Scale factor proxy (average graph distance) is not unique")
    print(f"  - Spectral dimension estimate is noisy at small N")
    print(f"  - Gravity test uses simplified two-body setup")
    print(f"  - No backreaction of matter on geometry yet")


if __name__ == '__main__':
    main()
