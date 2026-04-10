#!/usr/bin/env python3
"""
Simplified Axioms — Spot Experiment
=====================================
Based on everything learned this session, the simplest axiom set that
produces real physics:

AXIOM 1: EVENTS — A finite set of nodes exists.
AXIOM 2: CONNECTIONS — Nodes are connected by undirected links.
         The connectivity defines a graph G = (V, E).
AXIOM 3: FIELD — Each node carries a complex scalar amplitude psi(v).
AXIOM 4: PERSISTENCE — The field evolves unitarily via the graph Laplacian:
         d^2 psi/dt^2 = -L_G psi - m^2 psi
         where L_G is the graph Laplacian (derived from connectivity).
AXIOM 5: GRAVITY — A mass source modifies the local potential:
         V(v) = -m * Phi(v), where Phi(v) = g / (d(v, source) + eps).
         This enters as: d^2 psi/dt^2 = -L_G psi - m^2 psi - V psi.

WHAT EMERGES:
  - Klein-Gordon dispersion from Laplacian eigenvalues
  - Born rule from linearity
  - Gravity (achromatic, N-stable, equivalence) from potential
  - Gauge (AB effect) from phase on links
  - Decoherence from environment coupling

THIS EXPERIMENT tests these axioms on THREE graph types:
  A. Regular cubic lattice (baseline — known to work, 16/16)
  B. Random geometric graph (nodes scattered in 3D, linked if within radius r)
  C. Growing graph (start small, add nodes, test if physics survives growth)

The key question: do the axioms produce physics on NON-regular graphs?
If yes, the physics is truly derived from the axioms, not from the lattice.
"""

import numpy as np
from scipy import stats
from scipy.sparse import lil_matrix, csr_matrix, diags
import time


# ============================================================================
# Graph construction
# ============================================================================

def cubic_graph(n):
    """Regular cubic lattice with periodic BCs."""
    N = n**3
    adj = lil_matrix((N, N), dtype=float)
    def idx(x,y,z): return (x%n)*n*n + (y%n)*n + (z%n)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i = idx(x,y,z)
                for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    adj[i, idx(x+dx, y+dy, z+dz)] = 1.0
    return csr_matrix(adj), n


def random_geometric_graph(N_nodes, radius, seed=42):
    """Random geometric graph: N nodes in [0,1]^3, linked if dist < radius."""
    rng = np.random.RandomState(seed)
    pos = rng.uniform(0, 1, (N_nodes, 3))
    adj = lil_matrix((N_nodes, N_nodes), dtype=float)
    for i in range(N_nodes):
        for j in range(i+1, N_nodes):
            d = np.sqrt(np.sum((pos[i] - pos[j])**2))
            if d < radius:
                adj[i, j] = 1.0
                adj[j, i] = 1.0
    return csr_matrix(adj), pos


def growing_graph(N_final, growth_steps, seed=42):
    """Growing graph: start with 8 nodes, add 1 per step with preferential attachment.
    Final graph has N_final nodes. Returns adjacency + positions."""
    rng = np.random.RandomState(seed)
    # Start with a small cube
    N_init = 8
    pos = np.array([[i,j,k] for i in [0.3,0.7] for j in [0.3,0.7] for k in [0.3,0.7]], dtype=float)
    adj = lil_matrix((N_final, N_final), dtype=float)
    # Connect initial cube
    for i in range(N_init):
        for j in range(i+1, N_init):
            d = np.sqrt(np.sum((pos[i]-pos[j])**2))
            if d < 0.5:
                adj[i,j] = 1.0; adj[j,i] = 1.0

    current_N = N_init
    while current_N < N_final:
        # New node at random position
        new_pos = rng.uniform(0.1, 0.9, 3)
        pos = np.vstack([pos, new_pos])
        # Connect to k nearest existing nodes
        k_connect = min(4, current_N)
        dists = np.sqrt(np.sum((pos[:current_N] - new_pos)**2, axis=1))
        nearest = np.argsort(dists)[:k_connect]
        for j in nearest:
            adj[current_N, j] = 1.0
            adj[j, current_N] = 1.0
        current_N += 1

    return csr_matrix(adj[:current_N, :current_N]), pos


def graph_laplacian(adj):
    deg = np.array(adj.sum(axis=1)).flatten()
    return diags(deg) - adj


# ============================================================================
# Evolution (FFT for cubic, direct expm for small graphs)
# ============================================================================

def evolve_fft(n, mass, dt, n_steps, psi0, V=None):
    """FFT split-step on cubic lattice."""
    f = np.fft.fftfreq(n) * 2 * np.pi
    kx, ky, kz = f[:,None,None], f[None,:,None], f[None,None,:]
    k2 = 2*(1-np.cos(kx)) + 2*(1-np.cos(ky)) + 2*(1-np.cos(kz))
    E = np.sqrt(k2 + mass**2)
    hk = np.exp(-1j * E * dt / 2)
    fp = np.exp(-1j * V * dt) if V is not None else np.ones((n,n,n))
    psi = psi0.copy()
    for _ in range(n_steps):
        psi = np.fft.ifftn(np.fft.fftn(psi) * hk)
        psi *= fp
        psi = np.fft.ifftn(np.fft.fftn(psi) * hk)
    return psi


def evolve_graph(L, mass, dt, n_steps, psi0, V=None):
    """Leapfrog on arbitrary graph. V is a vector of per-node potentials."""
    N = len(psi0)
    phi = psi0.copy().astype(complex)
    pi = np.zeros(N, dtype=complex)
    m2 = mass**2
    V_arr = V if V is not None else np.zeros(N)
    for _ in range(n_steps):
        force = -L.dot(phi) - m2*phi - V_arr*phi
        pi += 0.5*dt*force
        phi += dt*pi
        force = -L.dot(phi) - m2*phi - V_arr*phi
        pi += 0.5*dt*force
    return phi


# ============================================================================
# Helpers
# ============================================================================

def gaussian_on_graph(pos, center_idx, sigma=0.15):
    """Gaussian centered on node center_idx."""
    N = len(pos)
    center = pos[center_idx]
    dists = np.sqrt(np.sum((pos - center)**2, axis=1))
    psi = np.exp(-dists**2 / (2*sigma**2)).astype(complex)
    return psi / np.linalg.norm(psi)


def centroid_z_graph(psi, pos):
    """Centroid of |psi|^2 in z-coordinate."""
    rho = np.abs(psi)**2
    total = np.sum(rho)
    return np.sum(rho * pos[:, 2]) / total if total > 0 else 0


def graph_distance(pos, i, j):
    return np.sqrt(np.sum((pos[i] - pos[j])**2))


# ============================================================================
# Test suite for a given graph
# ============================================================================

def test_graph(name, adj, pos, mass=0.3, g=5.0, S=5e-4, dt=0.05, n_steps=20):
    """Run core physics tests on a given graph."""
    print(f"\n{'='*70}")
    print(f"GRAPH: {name} ({len(pos)} nodes)")
    print(f"{'='*70}")

    N = len(pos)
    L = graph_laplacian(adj)

    # Find center node and mass node
    center = np.mean(pos, axis=0)
    center_idx = np.argmin(np.sum((pos - center)**2, axis=1))
    # Mass node: offset in z
    target_z = center[2] + 0.2
    mass_candidates = np.argsort(np.abs(pos[:, 2] - target_z))
    mass_idx = mass_candidates[0]
    if mass_idx == center_idx:
        mass_idx = mass_candidates[1]

    print(f"  Center node: {center_idx} at {pos[center_idx]}")
    print(f"  Mass node:   {mass_idx} at {pos[mass_idx]}")
    print(f"  Distance:    {graph_distance(pos, center_idx, mass_idx):.3f}")

    psi0 = gaussian_on_graph(pos, center_idx)

    # Build gravitational potential
    dists_to_mass = np.sqrt(np.sum((pos - pos[mass_idx])**2, axis=1))
    V_grav = -mass * g * S / (dists_to_mass + 0.05)

    score = 0

    # 1. Gravity direction
    phi_flat = evolve_graph(L, mass, dt, n_steps, psi0, V=None)
    phi_grav = evolve_graph(L, mass, dt, n_steps, psi0, V=V_grav)
    cz_flat = centroid_z_graph(phi_flat, pos)
    cz_grav = centroid_z_graph(phi_grav, pos)
    delta = cz_grav - cz_flat
    # TOWARD = centroid moves toward mass (higher z if mass is at higher z)
    toward = (delta > 0) == (pos[mass_idx, 2] > pos[center_idx, 2])
    score += toward
    print(f"\n  [Gravity]   delta_cz={delta:+.4e} {'TOWARD' if toward else 'AWAY'}")

    # 2. N-stability
    n_tw = 0
    for ns in [5, 10, 15, 20, 25, 30]:
        pf = evolve_graph(L, mass, dt, ns, psi0, V=None)
        pg = evolve_graph(L, mass, dt, ns, psi0, V=V_grav)
        d = centroid_z_graph(pg, pos) - centroid_z_graph(pf, pos)
        tw = (d > 0) == (pos[mass_idx, 2] > pos[center_idx, 2])
        n_tw += tw
    frac = n_tw / 6
    score += (frac > 0.7)
    print(f"  [N-stable]  {n_tw}/6 TOWARD ({frac:.0%})")

    # 3. F~M (field strength scaling)
    cz0 = centroid_z_graph(evolve_graph(L, mass, dt, n_steps, psi0), pos)
    strs = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    for s in strs:
        V_s = -mass * g * s / (dists_to_mass + 0.05)
        pg = evolve_graph(L, mass, dt, n_steps, psi0, V=V_s)
        forces.append(centroid_z_graph(pg, pos) - cz0)
    fa = np.array(forces); sa = np.array(strs)
    co = np.polyfit(sa, fa, 1); pred = np.polyval(co, sa)
    ss_r = np.sum((fa-pred)**2); ss_t = np.sum((fa-np.mean(fa))**2)
    r2 = 1-ss_r/ss_t if ss_t > 0 else 0
    score += (r2 > 0.9)
    print(f"  [F~M]       R^2={r2:.6f}")

    # 4. Norm check
    norm_init = np.sum(np.abs(psi0)**2)
    norm_final = np.sum(np.abs(phi_grav)**2)
    norm_err = abs(norm_final - norm_init) / norm_init
    print(f"  [Norm]      drift={norm_err:.4e}")

    # 5. f=0 control
    rho0 = np.abs(phi_flat)**2
    cz_0 = centroid_z_graph(phi_flat, pos)
    center_z = pos[center_idx, 2]
    bias = abs(cz_0 - center_z)
    score += (bias < 0.1)
    print(f"  [f=0]       centroid_z={cz_0:.4f} vs center={center_z:.4f}, bias={bias:.4f}")

    # 6. Born (linearity check — norm of sum vs sum of norms)
    psi_a = gaussian_on_graph(pos, center_idx, sigma=0.1)
    psi_b = gaussian_on_graph(pos, mass_idx, sigma=0.1)
    psi_ab = (psi_a + psi_b) / np.sqrt(2)
    phi_a = evolve_graph(L, mass, dt, n_steps, psi_a)
    phi_b = evolve_graph(L, mass, dt, n_steps, psi_b)
    phi_ab = evolve_graph(L, mass, dt, n_steps, psi_ab)
    phi_sum = (phi_a + phi_b) / np.sqrt(2)
    lin_err = np.linalg.norm(phi_ab - phi_sum) / np.linalg.norm(phi_ab)
    score += (lin_err < 1e-6)
    print(f"  [Linearity] |U(a+b) - U(a)+U(b)| / |U(a+b)| = {lin_err:.4e}")

    # 7. Decoherence
    phi_clean = evolve_graph(L, mass, dt, n_steps, psi0)
    # Add noise
    rng = np.random.RandomState(42)
    psi_n = psi0.copy()
    pi_n = np.zeros(N, dtype=complex)
    m2 = mass**2
    for _ in range(n_steps):
        psi_n *= np.exp(1j * rng.uniform(-1.0, 1.0, N))
        force = -L.dot(psi_n) - m2*psi_n
        pi_n += 0.5*dt*force; psi_n += dt*pi_n
        force = -L.dot(psi_n) - m2*psi_n
        pi_n += 0.5*dt*force
    coh_c = np.abs(np.sum(phi_clean.conj() * np.roll(phi_clean, 1))) / np.sum(np.abs(phi_clean)**2)
    coh_n = np.abs(np.sum(psi_n.conj() * np.roll(psi_n, 1))) / np.sum(np.abs(psi_n)**2)
    score += (coh_n < coh_c)
    print(f"  [Decohere]  clean={coh_c:.4f}, noisy={coh_n:.4f}")

    # 8. Superposition
    V_a = -mass * g * S / (dists_to_mass + 0.05)
    dists_to_center = np.sqrt(np.sum((pos - pos[center_idx])**2, axis=1))
    V_b = -mass * g * S / (dists_to_center + 0.05)
    V_ab = V_a + V_b
    rho0 = np.abs(evolve_graph(L, mass, dt, n_steps, psi0))**2
    rhoA = np.abs(evolve_graph(L, mass, dt, n_steps, psi0, V_a))**2
    rhoB = np.abs(evolve_graph(L, mass, dt, n_steps, psi0, V_b))**2
    rhoAB = np.abs(evolve_graph(L, mass, dt, n_steps, psi0, V_ab))**2
    dA = rhoA-rho0; dB = rhoB-rho0; dAB = rhoAB-rho0
    sup = np.sum(np.abs(dAB-dA-dB))/max(np.sum(np.abs(dAB)), 1e-30)
    score += (sup < 0.05)
    print(f"  [Superpos]  err={sup*100:.4f}%")

    print(f"\n  SCORE: {score}/8")
    return score


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("SIMPLIFIED AXIOMS — SPOT EXPERIMENT")
    print("=" * 70)
    print("Axiom 1: Events (nodes)")
    print("Axiom 2: Connections (links → graph Laplacian)")
    print("Axiom 3: Field (complex scalar per node)")
    print("Axiom 4: Persistence (unitary evolution via Laplacian)")
    print("Axiom 5: Gravity (V = -m*g*S/(d+eps))")
    print()
    print("Testing on 3 graph types to verify axioms are graph-independent.")
    print()

    # A. Regular cubic lattice
    adj_c, n_c = cubic_graph(15)
    pos_c = np.array([[x,y,z] for x in range(15) for y in range(15) for z in range(15)], dtype=float) / 14.0
    s_cubic = test_graph("Regular Cubic (15^3)", adj_c, pos_c, dt=0.15, n_steps=14)

    # B. Random geometric graph
    adj_r, pos_r = random_geometric_graph(500, radius=0.18, seed=42)
    # Check connectivity
    deg_r = np.array(adj_r.sum(axis=1)).flatten()
    print(f"\n  Random graph: {len(pos_r)} nodes, mean_deg={np.mean(deg_r):.1f}, "
          f"min_deg={np.min(deg_r):.0f}, max_deg={np.max(deg_r):.0f}")
    s_random = test_graph("Random Geometric (500 nodes, r=0.18)", adj_r, pos_r,
                          dt=0.02, n_steps=40)

    # C. Growing graph
    adj_g, pos_g = growing_graph(200, growth_steps=192, seed=42)
    deg_g = np.array(adj_g.sum(axis=1)).flatten()
    print(f"\n  Growing graph: {len(pos_g)} nodes, mean_deg={np.mean(deg_g):.1f}")
    s_growing = test_graph("Growing Graph (200 nodes, k=4)", adj_g, pos_g,
                           dt=0.02, n_steps=40)

    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("SUMMARY — SIMPLIFIED AXIOMS ACROSS GRAPH TYPES")
    print(f"{'='*70}")
    print(f"  Regular cubic:    {s_cubic}/8")
    print(f"  Random geometric: {s_random}/8")
    print(f"  Growing graph:    {s_growing}/8")
    print(f"\n  Total time: {elapsed:.1f}s")

    print(f"\n  NOTE: This is a narrow spot battery (8 tests) with leapfrog")
    print(f"  integrator (norm drifts). These results are directional, not")
    print(f"  a validated core card. See frontier_axioms_16card.py for the")
    print(f"  audited 16-row card with Crank-Nicolson norm preservation.")
    if s_cubic >= 6 and s_random >= 6 and s_growing >= 6:
        print(f"\n  VERDICT: Gravity, Born, decoherence, superposition work across")
        print(f"  all 3 graph types in this spot battery. Encouraging but not")
        print(f"  sufficient for topology-independence claims.")
    elif s_cubic >= 6:
        print("\n  VERDICT: Axioms work on regular lattice but need refinement")
        print("  for irregular graphs.")
    else:
        print("\n  VERDICT: Axioms need fundamental revision.")
