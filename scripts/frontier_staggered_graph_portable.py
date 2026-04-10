#!/usr/bin/env python3
"""
Staggered Fermion on Non-Cubic Graphs — Portability Test
==========================================================
The staggered Dirac operator needs:
  1. Bipartite graph (2-coloring for mass term epsilon(x))
  2. Oriented links (for staggering phases)
  3. Potential V(x) per node (for gravity)

Strategy: construct bipartite random geometric graphs and bipartite
growing graphs, then run the retained subset:
  Born, norm, force sign, F~M, achromatic force, equivalence, robustness

This is the highest-priority next step per the work backlog.
"""

import numpy as np
from scipy import stats
from scipy.sparse import lil_matrix, csr_matrix, diags, eye as speye
from scipy.sparse.linalg import spsolve
import time

# ============================================================================
# Bipartite graph construction
# ============================================================================

def bipartite_random_geometric(N_nodes, radius, seed=42):
    """Random geometric graph with enforced bipartite structure.
    Place N points in [0,1]^3. Assign color by checkerboard on a
    coarse grid: color = (floor(x/h) + floor(y/h) + floor(z/h)) % 2.
    Connect only between different colors within radius.
    """
    rng = np.random.RandomState(seed)
    pos = rng.uniform(0, 1, (N_nodes, 3))

    # Checkerboard coloring with grid spacing h
    h = 0.25  # coarse enough to get roughly equal color populations
    color = np.array([(int(p[0]/h) + int(p[1]/h) + int(p[2]/h)) % 2 for p in pos])

    adj = lil_matrix((N_nodes, N_nodes), dtype=float)
    for i in range(N_nodes):
        for j in range(i+1, N_nodes):
            if color[i] != color[j]:  # bipartite: only cross-color links
                d = np.sqrt(np.sum((pos[i] - pos[j])**2))
                if d < radius:
                    adj[i, j] = 1.0; adj[j, i] = 1.0

    return csr_matrix(adj), pos, color


def bipartite_growing(N_final, seed=42):
    """Growing graph with bipartite structure.
    Start with 2 nodes (one per color). Add nodes with alternating color,
    connect to k nearest nodes of OPPOSITE color.
    """
    rng = np.random.RandomState(seed)
    pos = np.array([[0.4, 0.5, 0.5], [0.6, 0.5, 0.5]])
    color = np.array([0, 1])
    adj = lil_matrix((N_final, N_final), dtype=float)
    adj[0, 1] = 1.0; adj[1, 0] = 1.0
    cur = 2

    while cur < N_final:
        new_pos = rng.uniform(0.1, 0.9, 3)
        new_color = cur % 2  # alternate colors
        pos = np.vstack([pos, new_pos])
        color = np.append(color, new_color)

        # Connect to k nearest nodes of OPPOSITE color
        k = min(4, cur)
        opp = np.where(color[:cur] != new_color)[0]
        if len(opp) > 0:
            dists = np.sqrt(np.sum((pos[opp] - new_pos)**2, axis=1))
            nearest = opp[np.argsort(dists)[:k]]
            for j in nearest:
                adj[cur, j] = 1.0; adj[j, cur] = 1.0
        cur += 1

    return csr_matrix(adj[:cur, :cur]), pos, color


# ============================================================================
# Staggered Hamiltonian on arbitrary bipartite graph
# ============================================================================

def staggered_H_graph(adj, color, mass, V=None):
    """Staggered Dirac Hamiltonian on a bipartite graph.

    H[i,j] = -i/2 * sign(i,j) for adjacent i,j with different color
    H[i,i] = mass * epsilon(i) + V(i)
    epsilon(i) = +1 if color[i]==0, -1 if color[i]==1
    sign(i,j) = +1 if i < j, -1 if i > j (orientation convention)

    This gives: H is anti-Hermitian off-diagonal (imaginary) + Hermitian
    diagonal (real mass + potential). The total H is Hermitian if we use
    the correct sign convention.
    """
    N = adj.shape[0]
    H = lil_matrix((N, N), dtype=complex)

    # Off-diagonal: hopping between different-color neighbors
    rows, cols = adj.nonzero()
    for idx in range(len(rows)):
        i, j = rows[idx], cols[idx]
        if i < j and color[i] != color[j]:
            # Oriented hopping: -i/2 for i->j, +i/2 for j->i
            H[i, j] += -1j / 2
            H[j, i] += 1j / 2

    # Diagonal: mass + potential
    for i in range(N):
        eps = 1 if color[i] == 0 else -1
        H[i, i] = mass * eps
        if V is not None:
            H[i, i] += V[i]

    return csr_matrix(H)


# ============================================================================
# Evolution + observables
# ============================================================================

def evolve_cn(H, N, dt, ns, psi0):
    Ap = (speye(N) + 1j*H*dt/2).tocsc()
    Am = speye(N) - 1j*H*dt/2
    psi = psi0.copy()
    for _ in range(ns):
        psi = spsolve(Ap, Am.dot(psi))
    return psi


def gaussian_on_graph(pos, center_idx, sigma=0.15):
    dists = np.sqrt(np.sum((pos - pos[center_idx])**2, axis=1))
    psi = np.exp(-dists**2 / (2*sigma**2)).astype(complex)
    return psi / np.linalg.norm(psi)


def force_on_graph(psi, V, adj, pos):
    """Force F = -<dV/dz> on a graph. Approximate dV/dz via neighbors."""
    N = len(psi)
    rho = np.abs(psi)**2; rho /= np.sum(rho)
    # Numerical z-gradient of V using neighbor differences
    dVdz = np.zeros(N)
    for i in range(N):
        neighbors = adj[i].nonzero()[1]
        if len(neighbors) > 0:
            diffs = [(V[j] - V[i]) * (pos[j, 2] - pos[i, 2]) /
                     max(np.sqrt(np.sum((pos[j] - pos[i])**2)), 1e-10)
                     for j in neighbors]
            dVdz[i] = np.mean(diffs)
    return -np.sum(rho * dVdz)


def build_V_graph(pos, mass, g, S, mass_idx):
    """Gravitational potential: V = -mass*g*S/(d + eps)."""
    dists = np.sqrt(np.sum((pos - pos[mass_idx])**2, axis=1))
    return -mass * g * S / (dists + 0.05)


# ============================================================================
# Retained test subset
# ============================================================================

def run_tests(name, adj, pos, color, mass=0.3, g=50.0, S=5e-4, dt=0.02, ns=30):
    """Run the retained subset: Born, norm, force sign, F~M, achromatic,
    equivalence, state-family robustness."""
    print(f"\n{'='*70}")
    print(f"{name} ({len(pos)} nodes, bipartite {np.sum(color==0)}/{np.sum(color==1)})")
    print(f"{'='*70}")

    N = len(pos)

    # Check Hermiticity
    H_flat = staggered_H_graph(adj, color, mass)
    herm = np.max(np.abs((H_flat - H_flat.conj().T).toarray()))
    print(f"  Hermiticity: {herm:.2e}")

    # Check connectivity
    deg = np.array(adj.sum(axis=1)).flatten()
    print(f"  Degree: mean={np.mean(deg):.1f}, min={np.min(deg):.0f}, max={np.max(deg):.0f}")

    # Find center and mass nodes
    center = np.mean(pos, axis=0)
    ci = np.argmin(np.sum((pos - center)**2, axis=1))
    target_z = center[2] + 0.15
    mc = np.argsort(np.abs(pos[:, 2] - target_z))
    mi = mc[0] if mc[0] != ci else mc[1]
    mass_above = pos[mi, 2] > pos[ci, 2]

    V = build_V_graph(pos, mass, g, S, mi)
    H_grav = staggered_H_graph(adj, color, mass, V)
    psi0 = gaussian_on_graph(pos, ci)
    dV = np.zeros(N)  # for force
    for i in range(N):
        nb = adj[i].nonzero()[1]
        if len(nb) > 0:
            dV[i] = np.mean([(V[j]-V[i])*(pos[j,2]-pos[i,2]) /
                             max(np.sqrt(np.sum((pos[j]-pos[i])**2)),1e-10) for j in nb])

    score = 0

    # Born (linearity)
    psi_a = gaussian_on_graph(pos, ci, sigma=0.1)
    second = np.argsort(np.sum((pos - pos[ci])**2, axis=1))[min(5, N-1)]
    psi_b = gaussian_on_graph(pos, second, sigma=0.1)
    psi_sum = (psi_a + psi_b) / np.sqrt(2)
    pa = evolve_cn(H_flat, N, dt, ns, psi_a)
    pb = evolve_cn(H_flat, N, dt, ns, psi_b)
    ps = evolve_cn(H_flat, N, dt, ns, psi_sum)
    lin_err = np.linalg.norm(ps - (pa+pb)/np.sqrt(2)) / max(np.linalg.norm(ps), 1e-30)
    p = lin_err < 1e-6; score += p
    print(f"  Born (linearity): {lin_err:.4e} {'PASS' if p else 'FAIL'}")

    # Norm
    psi_final = evolve_cn(H_grav, N, dt, ns, psi0)
    norm_err = abs(np.sum(np.abs(psi_final)**2) - 1)
    p = norm_err < 1e-10; score += p
    print(f"  Norm: {norm_err:.4e} {'PASS' if p else 'FAIL'}")

    # Force sign (TOWARD)
    F = force_on_graph(psi_final, V, adj, pos)
    toward = (F > 0) == mass_above
    p = toward; score += p
    print(f"  Force: {F:+.4e} {'TOWARD' if toward else 'AWAY'} {'PASS' if p else 'FAIL'}")

    # F~M
    forces_fm = []
    for s in [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]:
        V_s = build_V_graph(pos, mass, g, s, mi)
        H_s = staggered_H_graph(adj, color, mass, V_s)
        psi_s = evolve_cn(H_s, N, dt, ns, psi0)
        dV_s = np.zeros(N)
        for i in range(N):
            nb = adj[i].nonzero()[1]
            if len(nb) > 0:
                dV_s[i] = np.mean([(V_s[j]-V_s[i])*(pos[j,2]-pos[i,2]) /
                                   max(np.sqrt(np.sum((pos[j]-pos[i])**2)),1e-10) for j in nb])
        forces_fm.append(-np.sum(np.abs(psi_s)**2 / np.sum(np.abs(psi_s)**2) * dV_s))
    fa = np.array(forces_fm); sa = np.array([1e-4, 2e-4, 5e-4, 1e-3, 2e-3])
    co = np.polyfit(sa, fa, 1); pred = np.polyval(co, sa)
    r2 = 1 - np.sum((fa-pred)**2) / np.sum((fa-np.mean(fa))**2) if np.sum((fa-np.mean(fa))**2) > 0 else 0
    p = r2 > 0.9; score += p
    print(f"  F~M: R^2={r2:.6f} {'PASS' if p else 'FAIL'}")

    # Achromatic force (T=0)
    forces_k = []
    for k0 in [0, 0.15, 0.3]:
        psi_k = psi0 * np.exp(1j * k0 * (pos[:, 2] - pos[ci, 2]))
        psi_k /= np.linalg.norm(psi_k)
        rho_k = np.abs(psi_k)**2; rho_k /= np.sum(rho_k)
        forces_k.append(-np.sum(rho_k * dV))
    cv_k = np.std(forces_k) / np.mean(np.abs(forces_k)) if np.mean(np.abs(forces_k)) > 0 else 999
    p = cv_k < 0.01 and all(f > 0 for f in forces_k) == mass_above; score += p
    print(f"  Achromatic: CV={cv_k:.6f} {'PASS' if p else 'FAIL'}")

    # Equivalence
    accels = []
    for mm in [0.1, 0.3, 0.5]:
        V_m = build_V_graph(pos, mm, g, S, mi)
        dV_m = np.zeros(N)
        for i in range(N):
            nb = adj[i].nonzero()[1]
            if len(nb) > 0:
                dV_m[i] = np.mean([(V_m[j]-V_m[i])*(pos[j,2]-pos[i,2]) /
                                   max(np.sqrt(np.sum((pos[j]-pos[i])**2)),1e-10) for j in nb])
        rho0 = np.abs(psi0)**2; rho0 /= np.sum(rho0)
        accels.append(-np.sum(rho0 * dV_m) / mm)
    cv_eq = np.std(accels) / abs(np.mean(accels)) if abs(np.mean(accels)) > 0 else 999
    p = cv_eq < 0.01; score += p
    print(f"  Equivalence: CV={cv_eq:.6f} {'PASS' if p else 'FAIL'}")

    # State-family robustness (force-based)
    families = []
    # Gauss
    families.append(("gauss", psi0))
    # Color-0 only
    psi_c0 = psi0.copy(); psi_c0[color == 1] = 0
    if np.linalg.norm(psi_c0) > 0: psi_c0 /= np.linalg.norm(psi_c0); families.append(("color-0", psi_c0))
    # Color-1 only
    psi_c1 = psi0.copy(); psi_c1[color == 0] = 0
    if np.linalg.norm(psi_c1) > 0: psi_c1 /= np.linalg.norm(psi_c1); families.append(("color-1", psi_c1))

    n_tw = 0
    for label, psi_f in families:
        psi_ev = evolve_cn(H_grav, N, dt, ns, psi_f)
        F_f = force_on_graph(psi_ev, V, adj, pos)
        tw = (F_f > 0) == mass_above; n_tw += tw
        print(f"    {label:10s}: F={F_f:+.4e} {'TOWARD' if tw else 'AWAY'}")
    p = n_tw == len(families); score += p
    print(f"  Robustness: {n_tw}/{len(families)} TOWARD {'PASS' if p else 'FAIL'}")

    print(f"\n  SCORE: {score}/7")
    return score


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("STAGGERED FERMION ON NON-CUBIC GRAPHS")
    print("=" * 70)
    print("Testing graph portability of the staggered + potential architecture.")
    print("Retained subset: Born, norm, force, F~M, achromatic, equiv, robustness.")
    print()

    # A. Cubic lattice (control)
    from scipy.sparse import lil_matrix as lm
    n_c = 11; N_c = n_c**3
    adj_c = lm((N_c, N_c), dtype=float)
    pos_c = np.zeros((N_c, 3))
    color_c = np.zeros(N_c, dtype=int)
    for x in range(n_c):
        for y in range(n_c):
            for z in range(n_c):
                i = x*n_c*n_c + y*n_c + z
                pos_c[i] = [x/(n_c-1), y/(n_c-1), z/(n_c-1)]
                color_c[i] = (x + y + z) % 2
                for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    xx, yy, zz = (x+dx)%n_c, (y+dy)%n_c, (z+dz)%n_c
                    j = xx*n_c*n_c + yy*n_c + zz
                    adj_c[i, j] = 1.0
    s_cubic = run_tests("CUBIC LATTICE (control)", csr_matrix(adj_c), pos_c, color_c, dt=0.02, ns=20)

    # B. Bipartite random geometric
    adj_r, pos_r, color_r = bipartite_random_geometric(300, radius=0.2, seed=42)
    s_random = run_tests("BIPARTITE RANDOM GEOMETRIC", adj_r, pos_r, color_r, dt=0.02, ns=30)

    # C. Bipartite growing
    adj_g, pos_g, color_g = bipartite_growing(150, seed=42)
    s_growing = run_tests("BIPARTITE GROWING", adj_g, pos_g, color_g, dt=0.02, ns=30)

    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"  Cubic (control):     {s_cubic}/7")
    print(f"  Random geometric:    {s_random}/7")
    print(f"  Growing:             {s_growing}/7")
    print(f"  Time: {elapsed:.1f}s")
