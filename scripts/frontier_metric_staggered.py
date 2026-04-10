#!/usr/bin/env python3
"""
Metric-Coupled Staggered Fermion — Universal Gravity
======================================================
THE KEY INSIGHT: Gravity must enter through the METRIC (kinetic term),
not through a scalar potential. A scalar V·I couples with opposite sign
to R and L movers. A metric modification (position-dependent hopping)
couples IDENTICALLY to both sectors.

In GR: g₀₀(x) = -(1-2Φ) modifies the kinetic term equally for all
spinor components. On the lattice: modify HOPPING AMPLITUDES.

Architecture: staggered fermion (1 scalar per site, Dirac from staggering)
with position-dependent hopping:
  h(x,x') = h_base * metric_factor(x,x')
  metric_factor = 1/(1 + g*S/(r+eps))  (weaker hopping near mass = slower)

CRITICAL TEST: state-family robustness
  Even (particle), Odd (antiparticle), Symmetric, Antisymmetric
  ALL must give TOWARD gravity.
"""

import numpy as np
from scipy import stats
from scipy.sparse import lil_matrix, csr_matrix, diags, eye as speye
from scipy.sparse.linalg import spsolve
import time


# ============================================================================
# Staggered Hamiltonian with metric coupling
# ============================================================================

def staggered_H_metric_1d(n, mass, metric_factor=None):
    """1D staggered Dirac with position-dependent hopping (metric gravity).
    H[x,x+1] = -i/2 * h(x,x+1), H[x,x-1] = +i/2 * h(x,x-1)
    h(x,x') = average of metric_factor at endpoints.
    Mass term: m * (-1)^x (unchanged by metric).
    """
    H = lil_matrix((n, n), dtype=complex)
    for x in range(n):
        xp = (x+1) % n; xm = (x-1) % n
        if metric_factor is not None:
            hf = 0.5 * (metric_factor[x] + metric_factor[xp])
            hb = 0.5 * (metric_factor[x] + metric_factor[xm])
        else:
            hf = hb = 1.0
        H[x, xp] += -1j/2 * hf
        H[x, xm] += 1j/2 * hb
        H[x, x] += mass * ((-1)**x)
    return csr_matrix(H)


def build_metric(n, g, S, mass_pos):
    """Metric factor: 1/(1 + g*S/(r+eps)). Near mass: < 1 (slower hopping)."""
    mf = np.ones(n)
    for y in range(n):
        r = min(abs(y - mass_pos), n - abs(y - mass_pos))
        mf[y] = 1.0 / (1.0 + g * S / (r + 0.1))
    return mf


# ============================================================================
# Crank-Nicolson evolution
# ============================================================================

def evolve_cn(H, N, dt, n_steps, psi0):
    Ap = (speye(N) + 1j*H*dt/2).tocsc()
    Am = speye(N) - 1j*H*dt/2
    psi = psi0.copy()
    for _ in range(n_steps):
        psi = spsolve(Ap, Am.dot(psi))
    return psi


# ============================================================================
# Initial states (state family)
# ============================================================================

def make_state(n, kind="even", sigma=None):
    """Create initial state on different sublattices.
    even: Gaussian on even sites (particle sector)
    odd: Gaussian on odd sites (antiparticle sector)
    sym: equal amplitude on both (symmetric)
    anti: opposite amplitude (antisymmetric)
    gauss: standard Gaussian on all sites
    """
    c = n//2; sigma = sigma or n/8
    psi = np.zeros(n, dtype=complex)
    for y in range(n):
        amp = np.exp(-((y-c)**2)/(2*sigma**2))
        if kind == "even" and y % 2 == 0: psi[y] = amp
        elif kind == "odd" and y % 2 == 1: psi[y] = amp
        elif kind == "sym": psi[y] = amp
        elif kind == "anti": psi[y] = amp * (1 if y%2==0 else -1)
        elif kind == "gauss": psi[y] = amp
    if np.linalg.norm(psi) > 0:
        psi /= np.linalg.norm(psi)
    return psi


# ============================================================================
# Observables
# ============================================================================

def centroid(psi, n):
    rho = np.abs(psi)**2; c = n//2; z = np.arange(n) - c
    return np.sum(z*rho) / np.sum(rho) if np.sum(rho) > 0 else 0


# ============================================================================
# Tests
# ============================================================================

def test_state_family_robustness():
    """THE CRITICAL TEST: all state families must give TOWARD gravity."""
    print("=" * 70)
    print("STATE-FAMILY ROBUSTNESS GATE")
    print("=" * 70)

    n = 61; mass = 0.3; c = n//2; mass_pos = c+4; dt = 0.15; ns = 15

    H_flat = staggered_H_metric_1d(n, mass)

    # Sweep metric coupling strength
    for g in [5, 50, 500]:
        mf = build_metric(n, g, 5e-4, mass_pos)
        H_grav = staggered_H_metric_1d(n, mass, mf)

        print(f"\n  g={g}, metric_min={np.min(mf):.4f}:")
        all_toward = True
        for kind in ["even", "odd", "sym", "anti", "gauss"]:
            psi0 = make_state(n, kind)
            if np.linalg.norm(psi0) < 1e-10: continue
            pf = evolve_cn(H_flat, n, dt, ns, psi0)
            pg = evolve_cn(H_grav, n, dt, ns, psi0)
            d = centroid(pg, n) - centroid(pf, n)
            tw = d > 0
            if not tw: all_toward = False
            print(f"    {kind:6s}: delta={d:+.4e} {'TOWARD' if tw else 'AWAY'}")

        print(f"    ALL TOWARD: {all_toward}")


def test_n_stability():
    """N-stability for ALL state families."""
    print("\n" + "=" * 70)
    print("N-STABILITY (all states)")
    print("=" * 70)

    n = 61; mass = 0.3; c = n//2; mass_pos = c+4; dt = 0.15; g = 50

    H_flat = staggered_H_metric_1d(n, mass)
    mf = build_metric(n, g, 5e-4, mass_pos)
    H_grav = staggered_H_metric_1d(n, mass, mf)

    for kind in ["even", "odd", "sym"]:
        psi0 = make_state(n, kind)
        n_tw = 0
        forces = []
        for ns in range(2, 21):
            pf = evolve_cn(H_flat, n, dt, ns, psi0)
            pg = evolve_cn(H_grav, n, dt, ns, psi0)
            d = centroid(pg, n) - centroid(pf, n)
            tw = d > 0; n_tw += tw; forces.append(d)
        frac = n_tw / 19
        mono = all(forces[i] <= forces[i+1] for i in range(len(forces)-1)) if len(forces) > 1 else False
        print(f"  {kind:6s}: TOWARD={n_tw}/19 ({frac:.0%}), mono={mono}")


def test_equivalence():
    """Mass-independent acceleration via metric coupling."""
    print("\n" + "=" * 70)
    print("EQUIVALENCE (metric coupling)")
    print("=" * 70)

    n = 61; c = n//2; mass_pos = c+4; dt = 0.15; ns = 10; g = 50

    # Force measurement: <dH/dx> depends on metric, not on mass
    accels = []
    masses = [0.1, 0.2, 0.3, 0.5, 0.8]
    for m in masses:
        mf = build_metric(n, g, 5e-4, mass_pos)
        H_flat = staggered_H_metric_1d(n, m)
        H_grav = staggered_H_metric_1d(n, m, mf)
        psi0 = make_state(n, "gauss")
        pf = evolve_cn(H_flat, n, dt, ns, psi0)
        pg = evolve_cn(H_grav, n, dt, ns, psi0)
        d = centroid(pg, n) - centroid(pf, n)
        accels.append(d)
        print(f"  m={m:.2f}: delta={d:+.4e}")

    fa = np.array(accels); ma = np.array(masses)
    _, _, rv, _, _ = stats.linregress(ma, fa)
    r2 = rv**2
    print(f"  R^2(defl vs mass) = {r2:.4f}")


def test_born():
    """Sorkin Born test."""
    print("\n" + "=" * 70)
    print("BORN (Sorkin I3)")
    print("=" * 70)

    n = 61; mass = 0.3; c = n//2; dt = 0.15; ns = 15; bl = 4
    H = staggered_H_metric_1d(n, mass)
    slits = [c-2, c, c+2]

    def ev_born(sl):
        psi = make_state(n, "gauss")
        psi = evolve_cn(H, n, dt, bl, psi)
        mask = np.zeros(n);
        for s in sl: mask[s] = 1
        psi *= mask
        return evolve_cn(H, n, dt, ns-bl, psi)

    rho123 = np.abs(ev_born(slits))**2; P_t = np.sum(rho123)
    rho_s = [np.abs(ev_born([s]))**2 for s in slits]
    rho_p = [np.abs(ev_born([slits[i],slits[j]]))**2 for i,j in [(0,1),(0,2),(1,2)]]
    I3 = rho123 - sum(rho_p) + sum(rho_s)
    born = np.sum(np.abs(I3)) / P_t if P_t > 1e-20 else 0
    print(f"  Sorkin |I3|/P = {born:.4e}")


def test_norm():
    print("\n" + "=" * 70)
    print("NORM")
    print("=" * 70)
    n = 61; mass = 0.3; c = n//2; mass_pos = c+4; g = 50
    mf = build_metric(n, g, 5e-4, mass_pos)
    H = staggered_H_metric_1d(n, mass, mf)
    psi0 = make_state(n, "gauss")
    psi = evolve_cn(H, n, 0.15, 20, psi0)
    norm = np.sum(np.abs(psi)**2)
    print(f"  Norm after 20 steps: {norm:.10f}")
    print(f"  Drift: {abs(norm-1):.4e}")


# ============================================================================
# Also test the OPPOSITE metric direction to verify sign
# ============================================================================

def test_metric_sign():
    """Verify that weaker hopping near mass → TOWARD,
    stronger hopping near mass → AWAY."""
    print("\n" + "=" * 70)
    print("METRIC SIGN VERIFICATION")
    print("=" * 70)

    n = 61; mass = 0.3; c = n//2; mass_pos = c+4; dt = 0.15; ns = 15; g = 50

    H_flat = staggered_H_metric_1d(n, mass)

    # Weaker near mass (correct GR: time slows → less hopping)
    mf_weak = build_metric(n, g, 5e-4, mass_pos)
    H_weak = staggered_H_metric_1d(n, mass, mf_weak)

    # Stronger near mass (opposite)
    mf_strong = 2.0 - mf_weak  # > 1 near mass
    H_strong = staggered_H_metric_1d(n, mass, mf_strong)

    psi0 = make_state(n, "gauss")
    pf = evolve_cn(H_flat, n, dt, ns, psi0)
    pw = evolve_cn(H_weak, n, dt, ns, psi0)
    ps = evolve_cn(H_strong, n, dt, ns, psi0)

    d_weak = centroid(pw, n) - centroid(pf, n)
    d_strong = centroid(ps, n) - centroid(pf, n)

    print(f"  Weaker hopping near mass: delta={d_weak:+.4e} {'TOWARD' if d_weak>0 else 'AWAY'}")
    print(f"  Stronger hopping near mass: delta={d_strong:+.4e} {'TOWARD' if d_strong>0 else 'AWAY'}")
    print(f"  Opposite signs: {(d_weak>0) != (d_strong>0)}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("METRIC-COUPLED STAGGERED FERMION — UNIVERSAL GRAVITY TEST")
    print("=" * 70)
    print("Gravity enters through hopping amplitude (metric), not potential.")
    print("Both sublattices (even/odd = particle/antiparticle) should see")
    print("the SAME gravity because the metric modifies the kinetic term.")
    print()

    test_state_family_robustness()
    test_metric_sign()
    test_n_stability()
    test_equivalence()
    test_born()
    test_norm()

    elapsed = time.time() - t_start
    print(f"\n  Total time: {elapsed:.1f}s")
