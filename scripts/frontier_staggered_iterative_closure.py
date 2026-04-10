#!/usr/bin/env python3
"""
Iterative Endogenous Closure on Cycle-Bearing Graphs
======================================================
Multi-step backreaction: at each iteration, the matter density |psi|^2
generates Phi via screened Poisson, which feeds back into H for the
next CN step.

Focuses on CYCLE-BEARING bipartite graphs per the work backlog.
Rejects odd-cycle graphs early.

Battery:
  1. Force sign stability across iterations
  2. Force magnitude stability (no wild oscillation)
  3. Norm conservation
  4. Phi convergence
  5. State-family robustness at final iteration
"""

from __future__ import annotations
import math, time, random
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix, eye as speye
from scipy.sparse.linalg import spsolve
from dataclasses import dataclass


# ============================================================================
# Parameters (match existing prototype)
# ============================================================================
DT = 0.12; MASS = 0.30; G = 8.0; SOURCE_SIGMA = 0.90; POISSON_MU2 = 0.22
N_ITER = 20  # iterations of the backreaction loop


# ============================================================================
# Graph construction (cycle-bearing bipartite, from prototype)
# ============================================================================

def _add_edge(adj: dict, a: int, b: int):
    adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)

def _bfs_depth(adj: dict, source: int, n: int) -> np.ndarray:
    from collections import deque
    depth = np.full(n, np.inf)
    depth[source] = 0; q = deque([source])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] == np.inf:
                depth[j] = depth[i] + 1; q.append(j)
    return depth

def _has_odd_cycle(adj: dict, colors: np.ndarray) -> bool:
    """Reject graphs with odd cycles (not truly bipartite)."""
    for i, nbs in adj.items():
        for j in nbs:
            if colors[i] == colors[j]: return True
    return False

@dataclass(frozen=True)
class Graph:
    name: str; positions: np.ndarray; colors: np.ndarray
    adj: dict; source: int; depth: np.ndarray; has_cycle: bool

def make_random_geometric(seed=42, side=6) -> Graph:
    rng = random.Random(seed)
    coords, colors, index, adj = [], [], {}, {}
    idx = 0
    for x in range(side):
        for y in range(side):
            coords.append((x + 0.08*(rng.random()-0.5), y + 0.08*(rng.random()-0.5)))
            colors.append((x+y) % 2); index[(x,y)] = idx; idx += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    for i in range(side):
        for j in range(side):
            a = index[(i,j)]
            for di,dj in ((1,0),(0,1),(1,1),(1,-1)):
                ii,jj = i+di, j+dj
                if (ii,jj) not in index: continue
                b = index[(ii,jj)]
                if col[a] == col[b]: continue
                if math.hypot(pos[b,0]-pos[a,0], pos[b,1]-pos[a,1]) <= 1.28:
                    _add_edge(adj, a, b)
    src = side*side//2; n = len(pos)
    return Graph("random_geometric", pos, col, {k: list(v) for k,v in adj.items()},
                 src, _bfs_depth(adj, src, n), True)

def make_growing(seed=42, n_target=48) -> Graph:
    rng = random.Random(seed)
    coords = [(0.0, 0.0), (1.0, 0.0)]; colors = [0, 1]
    adj: dict[int, set] = {0: {1}, 1: {0}}
    cur = 2
    while cur < n_target:
        px = rng.uniform(-3, 3); py = rng.uniform(-3, 3)
        new_color = cur % 2; coords.append((px, py)); colors.append(new_color)
        opp = [i for i in range(cur) if colors[i] != new_color]
        if opp:
            dists = [(math.hypot(px-coords[i][0], py-coords[i][1]), i) for i in opp]
            dists.sort()
            for _, j in dists[:min(4, len(dists))]:
                _add_edge(adj, cur, j)
        cur += 1
    pos = np.array(coords); col = np.array(colors, dtype=int)
    src = 0; n = len(pos)
    return Graph("growing", pos, col, {k: list(v) for k,v in adj.items()},
                 src, _bfs_depth(adj, src, n), True)


# ============================================================================
# Staggered Hamiltonian + Poisson on graph
# ============================================================================

def graph_laplacian(g: Graph) -> csr_matrix:
    n = g.positions.shape[0]; L = lil_matrix((n,n), dtype=float)
    for i, nbs in g.adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(g.positions[j,0]-g.positions[i,0], g.positions[j,1]-g.positions[i,1])
            w = 1.0/max(d, 0.5)
            L[i,j] -= w; L[j,i] -= w; L[i,i] += w; L[j,j] += w
    return L.tocsr()

def solve_phi(g: Graph, rho: np.ndarray) -> np.ndarray:
    if np.allclose(rho, 0): return np.zeros_like(rho)
    L = graph_laplacian(g)
    A = (L + POISSON_MU2 * speye(L.shape[0], format="csr")).tocsc()
    return spsolve(A, rho).astype(float)

def build_H(g: Graph, mass: float, phi: np.ndarray) -> csr_matrix:
    n = g.positions.shape[0]; H = lil_matrix((n,n), dtype=complex)
    parity = np.where(g.colors == 0, 1.0, -1.0)
    H.setdiag(mass * parity - mass * phi)
    for i, nbs in g.adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(g.positions[j,0]-g.positions[i,0], g.positions[j,1]-g.positions[i,1])
            w = 1.0/max(d, 0.5); hop = -0.5j * w
            H[i,j] += hop; H[j,i] += np.conj(hop)
    return H.tocsr()

def cn_step(H: csr_matrix, psi: np.ndarray, dt: float) -> np.ndarray:
    n = H.shape[0]
    ap = (speye(n, format="csc") + 1j*H*dt/2).tocsc()
    am = speye(n, format="csr") - 1j*H*dt/2
    return spsolve(ap, am.dot(psi))

def shell_force(g: Graph, psi: np.ndarray, phi: np.ndarray) -> float:
    """Force from shell-averaged Phi gradient, weighted by rho."""
    n = g.positions.shape[0]
    rho = np.abs(psi)**2; phi_arr = phi
    # Shell by BFS depth from source
    max_d = int(np.max(g.depth[np.isfinite(g.depth)])) if np.any(np.isfinite(g.depth)) else 0
    if max_d <= 0: return 0.0
    phi_shell = np.zeros(max_d+1); rho_shell = np.zeros(max_d+1); counts = np.zeros(max_d+1)
    for i in range(n):
        d = int(g.depth[i]) if np.isfinite(g.depth[i]) else -1
        if 0 <= d <= max_d:
            phi_shell[d] += phi_arr[i]; rho_shell[d] += rho[i]; counts[d] += 1
    for d in range(max_d+1):
        if counts[d] > 0: phi_shell[d] /= counts[d]; rho_shell[d] /= counts[d]
    # Gradient: toward-pointing gradient (decreasing phi toward source)
    grad = np.zeros(max_d+1)
    for d in range(max_d+1):
        if d == 0: grad[d] = phi_shell[0] - phi_shell[min(1,max_d)]
        elif d == max_d: grad[d] = phi_shell[d-1] - phi_shell[d]
        else: grad[d] = 0.5*(phi_shell[d-1] - phi_shell[d+1])
    return float(np.sum(rho_shell * grad))

def source_density(g: Graph, strength: float = 1.0) -> np.ndarray:
    center = g.positions[g.source]
    rel = g.positions - center
    w = np.exp(-0.5*(rel[:,0]**2+rel[:,1]**2)/(SOURCE_SIGMA**2))
    w /= max(np.sum(w), 1e-30)
    return strength * w

def gauss_state(g: Graph, sigma: float = 1.15) -> np.ndarray:
    center = g.positions[g.source]
    rel = g.positions - center
    psi = np.exp(-0.5*(rel[:,0]**2+rel[:,1]**2)/(sigma**2)).astype(complex)
    return psi / np.linalg.norm(psi)


# ============================================================================
# Iterative closure loop
# ============================================================================

def run_iterative(g: Graph, n_iter: int = N_ITER):
    print(f"\n{'='*70}")
    print(f"ITERATIVE CLOSURE: {g.name} ({g.positions.shape[0]} nodes, cycles={g.has_cycle})")
    print(f"{'='*70}")

    # Reject odd-cycle graphs
    if _has_odd_cycle(g.adj, g.colors):
        print("  REJECTED: odd-cycle defect detected.")
        return None

    n = g.positions.shape[0]
    psi = gauss_state(g)

    # Seed the source: use a fixed external source density for the FIRST Phi
    rho_source = source_density(g, strength=1.0)

    forces = []; norms = []; phi_changes = []
    phi_prev = None

    for it in range(n_iter):
        # Density for Phi: mix source + matter
        rho_matter = np.abs(psi)**2
        rho_matter *= np.sum(rho_source) / max(np.sum(rho_matter), 1e-30)  # normalize to same scale
        rho_total = rho_source + G * rho_matter  # source + self-gravity

        phi = solve_phi(g, rho_total)
        H = build_H(g, MASS, phi)
        psi = cn_step(H, psi, DT)

        F = shell_force(g, psi, phi)
        forces.append(F)
        norms.append(float(np.linalg.norm(psi)))
        if phi_prev is not None:
            phi_changes.append(float(np.linalg.norm(phi - phi_prev) / max(np.linalg.norm(phi), 1e-30)))
        phi_prev = phi.copy()

        if it < 5 or it == n_iter-1 or it % 5 == 0:
            print(f"  iter {it:3d}: F={F:+.4e} {'TW' if F>0 else 'AW'}, "
                  f"norm={norms[-1]:.10f}, "
                  f"dphi={phi_changes[-1]:.4e}" if phi_changes else
                  f"  iter {it:3d}: F={F:+.4e} {'TW' if F>0 else 'AW'}, "
                  f"norm={norms[-1]:.10f}")

    # Battery
    n_tw = sum(1 for f in forces if f > 0)
    norm_drift = max(abs(nm - 1.0) for nm in norms)
    phi_settled = phi_changes[-1] < 0.1 if phi_changes else False
    force_cv = np.std(forces) / np.mean(np.abs(forces)) if np.mean(np.abs(forces)) > 0 else 999

    print(f"\n  BATTERY:")
    print(f"    Force sign: {n_tw}/{n_iter} TOWARD {'PASS' if n_tw == n_iter else 'FAIL'}")
    print(f"    Force CV: {force_cv:.4f} {'PASS' if force_cv < 1.0 else 'FAIL'}")
    print(f"    Norm drift: {norm_drift:.4e} {'PASS' if norm_drift < 1e-3 else 'FAIL'}")
    print(f"    Phi settled: {phi_settled} (dphi={phi_changes[-1]:.4e})" if phi_changes else "")

    # State-family robustness at final iteration
    print(f"\n  STATE FAMILIES (final iteration):")
    rho_final = rho_source + G * np.abs(psi)**2
    rho_final *= np.sum(rho_source) / max(np.sum(rho_final), 1e-30)
    phi_final = solve_phi(g, rho_final)
    H_final = build_H(g, MASS, phi_final)

    fam_tw = 0
    for label, psi_init in [("gauss", gauss_state(g)),
                             ("color-0", _color_state(g, 0)),
                             ("color-1", _color_state(g, 1))]:
        psi_f = cn_step(H_final, psi_init, DT)
        F_f = shell_force(g, psi_f, phi_final)
        tw = F_f > 0; fam_tw += tw
        print(f"    {label:10s}: F={F_f:+.4e} {'TOWARD' if tw else 'AWAY'}")
    print(f"    Robustness: {fam_tw}/3 TOWARD {'PASS' if fam_tw == 3 else 'FAIL'}")

    return forces, norms, phi_changes


def _color_state(g: Graph, target_color: int) -> np.ndarray:
    psi = gauss_state(g).copy()
    psi[g.colors != target_color] = 0
    nm = np.linalg.norm(psi)
    return psi / nm if nm > 0 else psi


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t0 = time.time()
    print("="*70)
    print("ITERATIVE ENDOGENOUS CLOSURE — CYCLE-BEARING GRAPHS")
    print("="*70)
    print(f"DT={DT}, MASS={MASS}, G={G}, POISSON_MU2={POISSON_MU2}, N_ITER={N_ITER}")

    graphs = [make_random_geometric(seed=42), make_growing(seed=42)]

    for g in graphs:
        run_iterative(g)

    print(f"\nTotal time: {time.time()-t0:.1f}s")
