#!/usr/bin/env python3
"""
Graph Laplacian Klein-Gordon — The Third Path
===============================================
THESIS: The coin's mixing period is the root of all gravity blockers.
The graph Laplacian DERIVES KG from connectivity (not coin) with no
mixing period. Two gravity mechanisms tested:

  A. POTENTIAL GRAVITY: V(x) = -m*g*S/(r+eps), same as scalar KG
  B. GEOMETRIC GRAVITY: non-uniform graph connectivity near "mass"
     creates spatially-varying effective metric → geometric deflection

Mechanism B is the holy grail: gravity from geometry, like GR, but
derived from a discrete graph. No potential needed.

ARCHITECTURE:
  State: complex scalar phi(x) on a 3D graph
  Kinetic: graph Laplacian Delta_G (nearest-neighbor)
  Evolution: leapfrog (symplectic, local, preserves KG norm)
    pi_new = pi + dt*(Delta_G*phi - m^2*phi)
    phi_new = phi + dt*pi_new
  Two components (phi, pi) = KG first-order form

WHY THIS IS THE THIRD PATH:
  1. KG is DERIVED from graph Laplacian eigenvalues (not coin, not FFT)
  2. Light cone is DERIVED from bounded-degree graph (finite prop speed)
  3. No coin → no mixing period → no N-oscillation
  4. Gravity from GEOMETRY (non-uniform graph) → achromatic, mass-indep
  5. Local updates only (nearest-neighbor)
  6. Born from linearity (structural)

WHAT'S NEW vs scalar KG:
  - Local evolution (no FFT — only nearest-neighbor)
  - Geometric gravity (non-uniform graph → effective metric)
  - Can run on ARBITRARY graphs (DAGs, random, growing)
"""

import numpy as np
from scipy import stats
from scipy.sparse import lil_matrix, csr_matrix
import time

# ============================================================================
# Graph construction
# ============================================================================

def regular_lattice_3d(n):
    """Regular cubic lattice with periodic BCs. Returns adjacency as sparse."""
    N = n**3
    adj = lil_matrix((N, N), dtype=float)
    def idx(x,y,z): return (x%n)*n*n + (y%n)*n + (z%n)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i = idx(x,y,z)
                for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    j = idx(x+dx,y+dy,z+dz)
                    adj[i,j] = 1.0
    return csr_matrix(adj)


def geometric_gravity_lattice_3d(n, mass_pos, g_strength):
    """Lattice with EXTRA connections near mass → higher effective connectivity.
    Near the mass: each node gets additional links to next-nearest neighbors.
    This increases the local Laplacian eigenvalues → changes effective metric.

    The extra connectivity acts like spacetime curvature: waves propagate
    differently in regions of higher connectivity.
    """
    N = n**3
    adj = lil_matrix((N, N), dtype=float)
    c = n // 2

    def idx(x,y,z): return (x%n)*n*n + (y%n)*n + (z%n)

    for x in range(n):
        for y in range(n):
            for z in range(n):
                i = idx(x,y,z)
                # Standard nearest-neighbor
                for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    j = idx(x+dx,y+dy,z+dz)
                    adj[i,j] = 1.0

                # Extra connections near mass (geometric gravity)
                r = np.sqrt(min(abs(x-mass_pos[0]), n-abs(x-mass_pos[0]))**2 +
                           min(abs(y-mass_pos[1]), n-abs(y-mass_pos[1]))**2 +
                           min(abs(z-mass_pos[2]), n-abs(z-mass_pos[2]))**2)

                # Extra weight proportional to field strength / distance
                extra = g_strength / (r + 0.5)
                if extra > 0.01:  # threshold to keep sparse
                    # Add weight to existing NN links (makes Laplacian stronger near mass)
                    for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                        j = idx(x+dx,y+dy,z+dz)
                        adj[i,j] += extra

    return csr_matrix(adj)


def graph_laplacian(adj):
    """L = D - A where D = diag(degree)."""
    degrees = np.array(adj.sum(axis=1)).flatten()
    from scipy.sparse import diags
    D = diags(degrees)
    return D - adj


# ============================================================================
# Leapfrog KG evolution (local, symplectic)
# ============================================================================

def evolve_leapfrog(L, mass, dt, n_steps, phi0, V=None):
    """Leapfrog (Verlet) integration of lattice KG.
    pi_new = pi + dt * (L*phi - m^2*phi - V*phi)
    phi_new = phi + dt * pi_new
    Note: L = -(graph Laplacian) for the kinetic term (Laplacian has negative eigenvalues)
    """
    N = len(phi0)
    phi = phi0.copy().astype(complex)
    pi = np.zeros(N, dtype=complex)

    # The KG equation: d^2 phi/dt^2 = Delta*phi - m^2*phi - V*phi
    # = -L*phi - m^2*phi - V*phi  (L = D-A, -L has positive eigenvalues)
    m2 = mass**2
    V_arr = V if V is not None else np.zeros(N)

    for _ in range(n_steps):
        # Half step for pi
        force = -L.dot(phi) - m2 * phi - V_arr * phi
        pi = pi + 0.5 * dt * force
        # Full step for phi
        phi = phi + dt * pi
        # Half step for pi
        force = -L.dot(phi) - m2 * phi - V_arr * phi
        pi = pi + 0.5 * dt * force

    return phi, pi


# ============================================================================
# Helpers
# ============================================================================

def gaussian_3d(n, sigma=None):
    if sigma is None: sigma = max(2.0, n/8)
    c = n//2; x = np.arange(n)
    gx = np.exp(-(x-c)**2/(2*sigma**2))
    phi_3d = gx[:,None,None]*gx[None,:,None]*gx[None,None,:]
    return phi_3d.flatten() / np.linalg.norm(phi_3d.flatten())


def centroid_z(phi, n):
    prob = np.abs(phi.reshape(n,n,n))**2
    c = n//2; z = np.arange(n) - c
    pz = np.sum(prob, axis=(0,1))
    return np.sum(z*pz)/np.sum(pz) if np.sum(pz) > 0 else 0


def kg_norm(phi, pi, mass):
    """KG conserved norm: integral of |pi|^2 + |grad phi|^2 + m^2|phi|^2."""
    return np.sum(np.abs(pi)**2) + mass**2 * np.sum(np.abs(phi)**2)


# ============================================================================
# TESTS
# ============================================================================

def test_kg_dispersion(n=11):
    """Verify KG dispersion from graph Laplacian."""
    print("=" * 70)
    print("TEST: KG Dispersion from Graph Laplacian")
    print("=" * 70)

    adj = regular_lattice_3d(n)
    L = graph_laplacian(adj)

    # Eigenvalues of -L should be k^2_lattice = 2*sum(1-cos(k_j))
    # For small matrix, compute directly
    if n <= 9:
        L_dense = L.toarray()
        evals = np.sort(np.linalg.eigvalsh(-L_dense))
        print(f"  First 10 eigenvalues of -L: {evals[:10]}")
        print(f"  Expected: 0, 2*(1-cos(2pi/n))*{1,2,3}...")

    # Evolve a plane wave and measure dispersion
    mass = 0.3; dt = 0.2
    f = np.fft.fftfreq(n)*2*np.pi
    all_E2, all_k2 = [], []

    for kz_idx in range(n):
        kz = f[kz_idx]
        # Plane wave in z
        phi0 = np.zeros(n**3, dtype=complex)
        c = n//2
        for iz in range(n):
            for ix in range(n):
                for iy in range(n):
                    idx = ix*n*n + iy*n + iz
                    phi0[idx] = np.exp(1j*kz*iz) * np.exp(-((ix-c)**2+(iy-c)**2)/(2*(n/4)**2))
        phi0 /= np.linalg.norm(phi0)

        # Evolve 1 step, measure phase advance
        phi1, pi1 = evolve_leapfrog(L, mass, dt, 1, phi0)
        # Overlap to get phase
        overlap = np.sum(phi0.conj() * phi1)
        E_eff = -np.angle(overlap) / dt
        k2 = kz**2
        all_E2.append(E_eff**2)
        all_k2.append(k2)

    all_E2 = np.array(all_E2); all_k2 = np.array(all_k2)
    mask = all_k2 < 1.5
    if np.sum(mask) > 3:
        sl,ic,rv,_,_ = stats.linregress(all_k2[mask], all_E2[mask])
        r2 = rv**2
        print(f"  KG fit (E^2 vs k^2): R^2={r2:.6f}, m_fit={np.sqrt(abs(ic)):.4f}")
    else:
        r2 = 0
    print(f"  {'PASS' if r2 > 0.9 else 'FAIL'}")
    return r2


def test_potential_gravity(n=15):
    """Test A: potential gravity on regular lattice."""
    print("\n" + "=" * 70)
    print("TEST A: Potential Gravity (V(x) on regular lattice)")
    print("=" * 70)

    mass = 0.3; g = 5.0; S = 5e-4; c = n//2; dt = 0.2

    adj = regular_lattice_3d(n)
    L = graph_laplacian(adj)
    phi0 = gaussian_3d(n)

    # Build potential (attractive well near mass)
    V = np.zeros(n**3)
    mass_pos = (c, c, c+3)
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                dx = min(abs(ix-mass_pos[0]), n-abs(ix-mass_pos[0]))
                dy = min(abs(iy-mass_pos[1]), n-abs(iy-mass_pos[1]))
                dz = min(abs(iz-mass_pos[2]), n-abs(iz-mass_pos[2]))
                r = np.sqrt(dx**2+dy**2+dz**2)
                V[ix*n*n+iy*n+iz] = -mass * g * S / (r + 0.1)

    # N-stability sweep
    print(f"\n  N-stability (n={n}, mass={mass}):")
    n_tw = 0; n_tot = 0
    for ns in range(2, 16):
        phi_f, _ = evolve_leapfrog(L, mass, dt, ns, phi0, V=None)
        phi_g, _ = evolve_leapfrog(L, mass, dt, ns, phi0, V=V)
        d = centroid_z(phi_g, n) - centroid_z(phi_f, n)
        tw = d > 0; n_tw += tw; n_tot += 1
        print(f"    N={ns:2d}: delta_cz={d:+.4e} {'TOWARD' if tw else 'AWAY'}")

    frac = n_tw / n_tot
    print(f"  TOWARD: {n_tw}/{n_tot} = {frac:.0%}")
    return frac


def test_geometric_gravity(n=15):
    """Test B: GEOMETRIC gravity from non-uniform connectivity."""
    print("\n" + "=" * 70)
    print("TEST B: GEOMETRIC Gravity (non-uniform graph connectivity)")
    print("=" * 70)

    mass = 0.3; dt = 0.2; c = n//2

    # Regular lattice (control)
    adj_flat = regular_lattice_3d(n)
    L_flat = graph_laplacian(adj_flat)

    # Geometric lattice (extra connections near mass)
    mass_pos = (c, c, c+3)
    for g_str in [0.1, 0.5, 1.0, 2.0, 5.0]:
        adj_geo = geometric_gravity_lattice_3d(n, mass_pos, g_str)
        L_geo = graph_laplacian(adj_geo)

        phi0 = gaussian_3d(n)

        # Evolve on both
        phi_flat, _ = evolve_leapfrog(L_flat, mass, dt, 10, phi0)
        phi_geo, _ = evolve_leapfrog(L_geo, mass, dt, 10, phi0)

        cz_flat = centroid_z(phi_flat, n)
        cz_geo = centroid_z(phi_geo, n)
        delta = cz_geo - cz_flat
        tag = "TOWARD" if delta > 0 else "AWAY"
        print(f"  g={g_str:.1f}: cz_flat={cz_flat:+.4e}, cz_geo={cz_geo:+.4e}, delta={delta:+.4e} {tag}")

    # N-stability for best g
    print(f"\n  N-stability (geometric, g=2.0):")
    adj_geo = geometric_gravity_lattice_3d(n, mass_pos, 2.0)
    L_geo = graph_laplacian(adj_geo)
    n_tw = 0; n_tot = 0
    for ns in range(2, 14):
        phi_flat, _ = evolve_leapfrog(L_flat, mass, dt, ns, gaussian_3d(n))
        phi_geo, _ = evolve_leapfrog(L_geo, mass, dt, ns, gaussian_3d(n))
        d = centroid_z(phi_geo, n) - centroid_z(phi_flat, n)
        tw = d > 0; n_tw += tw; n_tot += 1
        print(f"    N={ns:2d}: delta={d:+.4e} {'TOWARD' if tw else 'AWAY'}")
    frac = n_tw / n_tot
    print(f"  TOWARD: {n_tw}/{n_tot} = {frac:.0%}")

    # Achromatic test: does geometric gravity depend on k?
    print(f"\n  Achromaticity (geometric):")
    adj_geo = geometric_gravity_lattice_3d(n, mass_pos, 2.0)
    L_geo = graph_laplacian(adj_geo)
    forces_k = []
    for k0 in [0, 0.3, 0.6, 0.9]:
        phi0 = np.zeros(n**3, dtype=complex)
        sigma = n/4
        for ix in range(n):
            for iy in range(n):
                for iz in range(n):
                    env = np.exp(-((ix-c)**2+(iy-c)**2+(iz-c)**2)/(2*sigma**2))
                    phi0[ix*n*n+iy*n+iz] = env * np.exp(1j*k0*iz)
        phi0 /= np.linalg.norm(phi0)
        phi_f, _ = evolve_leapfrog(L_flat, mass, dt, 10, phi0)
        phi_g, _ = evolve_leapfrog(L_geo, mass, dt, 10, phi0)
        d = centroid_z(phi_g, n) - centroid_z(phi_f, n)
        forces_k.append(d)
        print(f"    k={k0:.1f}: delta={d:+.4e} {'TOWARD' if d>0 else 'AWAY'}")
    fa = np.array(forces_k)
    same_sign = all(f>0 for f in fa) or all(f<0 for f in fa)
    cv = np.std(fa)/np.mean(np.abs(fa)) if np.mean(np.abs(fa))>0 else 999
    print(f"  Same sign: {same_sign}, CV: {cv:.4f}")

    return frac


def test_equivalence_geometric(n=13):
    """Does geometric gravity produce mass-independent deflection?"""
    print("\n" + "=" * 70)
    print("TEST: Equivalence Principle (geometric gravity)")
    print("=" * 70)

    c = n//2; dt = 0.2; mass_pos = (c,c,c+3)
    adj_flat = regular_lattice_3d(n); L_flat = graph_laplacian(adj_flat)
    adj_geo = geometric_gravity_lattice_3d(n, mass_pos, 2.0); L_geo = graph_laplacian(adj_geo)

    accels = []
    masses = [0.1, 0.2, 0.3, 0.5, 0.8]
    for mass in masses:
        phi0 = gaussian_3d(n)
        phi_f, _ = evolve_leapfrog(L_flat, mass, dt, 8, phi0)
        phi_g, _ = evolve_leapfrog(L_geo, mass, dt, 8, phi0)
        d = centroid_z(phi_g, n) - centroid_z(phi_f, n)
        accels.append(d)
        print(f"  mass={mass:.2f}: delta={d:+.4e}")

    fa = np.array(accels); ma = np.array(masses)
    _,_,rv,_,_ = stats.linregress(ma, fa)
    r2 = rv**2
    print(f"  R^2(deflection vs mass) = {r2:.4f}")
    if r2 < 0.1:
        print("  -> MASS-INDEPENDENT (equivalence holds!)")
    elif r2 < 0.5:
        print("  -> PARTIAL mass dependence")
    else:
        print("  -> MASS-DEPENDENT")
    return r2


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("GRAPH LAPLACIAN KLEIN-GORDON — THE THIRD PATH")
    print("=" * 70)
    print("KG from graph Laplacian (not coin, not FFT)")
    print("Gravity from geometry (non-uniform connectivity)")
    print("Local evolution (leapfrog, nearest-neighbor only)")
    print("No coin. No mixing period. No FFT.")
    print()

    r2_kg = test_kg_dispersion(n=9)
    frac_pot = test_potential_gravity(n=13)
    frac_geo = test_geometric_gravity(n=13)
    r2_eq = test_equivalence_geometric(n=11)

    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("SUMMARY — GRAPH LAPLACIAN KG")
    print(f"{'='*70}")
    print(f"  KG from Laplacian:      R^2={r2_kg:.4f}")
    print(f"  Potential gravity:      {frac_pot:.0%} TOWARD")
    print(f"  Geometric gravity:      {frac_geo:.0%} TOWARD")
    print(f"  Equivalence (geo):      R^2={r2_eq:.4f}")
    print(f"  Local evolution:        YES (leapfrog, nearest-neighbor)")
    print(f"  No coin:                YES")
    print(f"  No FFT:                 YES")
    print(f"  Total time: {elapsed:.1f}s")

    print(f"\n  KEY QUESTION: Does geometric gravity (non-uniform connectivity)")
    print(f"  produce mass-independent, achromatic, N-stable TOWARD deflection?")
