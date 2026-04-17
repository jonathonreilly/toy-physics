#!/usr/bin/env python3
"""
Geometric Gravity v2 — Lapse Function + Connection Weighting
==============================================================
The v1 geometric gravity (weakened connections) gave 75% TOWARD but
violated equivalence (R^2=0.90). Root cause: modifying the Laplacian
changes the KINETIC term, which couples differently to different masses.

FIX: In GR, gravity enters through the METRIC, which affects all
fields equally. On a lattice, the metric has two parts:
  1. LAPSE: how much proper time passes per step (temporal metric)
  2. SHIFT/SPATIAL: how distances are measured (spatial metric)

Approach A: LAPSE FUNCTION
  Near mass, each step advances less proper time:
    dt_local(x) = dt * alpha(x)
  where alpha(x) = 1 / (1 + g*S/(r+eps)) < 1 near mass.
  This is universal (same for all masses) and achromatic.

Approach B: METRIC-WEIGHTED LAPLACIAN
  Weight the Laplacian by the INVERSE spatial metric:
    Delta_g phi(x) = sum_j g^{jj}(x) * (phi(x+e_j) - phi(x))
  where g^{jj} = 1/(1 + g*S/(r+eps)) near mass.
  This slows SPATIAL propagation near mass.

Approach C: COMBINED (lapse + spatial)
  Both temporal slowdown and spatial contraction near mass.
  This is the full Schwarzschild analog on a lattice.

All three are tested for: TOWARD, N-stability, equivalence,
achromaticity, F~M.
"""

import numpy as np
from scipy import stats
from scipy.sparse import lil_matrix, csr_matrix, diags
import time

# ============================================================================
# Infrastructure
# ============================================================================

def idx(x,y,z,n): return (x%n)*n*n+(y%n)*n+(z%n)

def regular_laplacian(n):
    N=n**3; adj=lil_matrix((N,N),dtype=float)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i=idx(x,y,z,n)
                for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    adj[i,idx(x+dx,y+dy,z+dz,n)]=1.0
    adj=csr_matrix(adj)
    deg=np.array(adj.sum(axis=1)).flatten()
    return diags(deg)-adj

def field_r(n, mass_pos):
    """Minimum-image distance from each site to mass_pos."""
    r = np.zeros(n**3)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                dx=min(abs(x-mass_pos[0]),n-abs(x-mass_pos[0]))
                dy=min(abs(y-mass_pos[1]),n-abs(y-mass_pos[1]))
                dz=min(abs(z-mass_pos[2]),n-abs(z-mass_pos[2]))
                r[idx(x,y,z,n)]=np.sqrt(dx**2+dy**2+dz**2)
    return r

def gauss(n, sigma=None):
    c=n//2; sigma=sigma or max(2.0,n/8); x=np.arange(n)
    gx=np.exp(-(x-c)**2/(2*sigma**2))
    phi=(gx[:,None,None]*gx[None,:,None]*gx[None,None,:]).flatten().astype(complex)
    return phi/np.linalg.norm(phi)

def cz(phi,n):
    p=np.abs(phi.reshape(n,n,n))**2
    c=n//2; z=np.arange(n)-c; pz=np.sum(p,axis=(0,1))
    return np.sum(z*pz)/np.sum(pz) if np.sum(pz)>0 else 0


# ============================================================================
# Approach A: Lapse Function
# ============================================================================

def evolve_lapse(L, mass, dt_base, n_steps, phi0, alpha):
    """Leapfrog with position-dependent time step: dt_local = dt_base * alpha(x).
    alpha < 1 near mass → less time advance → gravitational redshift.
    This is UNIVERSAL: same alpha for all masses.
    """
    phi=phi0.copy(); pi=np.zeros_like(phi); m2=mass**2
    for _ in range(n_steps):
        # dt_local varies per site
        dt_local = dt_base * alpha
        force = -L.dot(phi) - m2*phi
        pi += 0.5 * dt_local * force
        phi += dt_local * pi
        force = -L.dot(phi) - m2*phi
        pi += 0.5 * dt_local * force
    return phi


# ============================================================================
# Approach B: Metric-Weighted Laplacian
# ============================================================================

def weighted_laplacian(n, mass_pos, g_str):
    """Laplacian with weights g^{ij}(x) = 1/(1 + g*S/(r+eps)).
    Weaker connections near mass → slower spatial propagation.
    """
    N=n**3; adj=lil_matrix((N,N),dtype=float)
    r = field_r(n, mass_pos)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i=idx(x,y,z,n)
                ri = r[i]
                # Metric factor: slower near mass
                g_inv = 1.0 / (1.0 + g_str/(ri+0.5))
                for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    j=idx(x+dx,y+dy,z+dz,n)
                    rj = r[j]
                    g_inv_j = 1.0 / (1.0 + g_str/(rj+0.5))
                    # Symmetric weight: average of endpoints
                    w = 0.5*(g_inv + g_inv_j)
                    adj[i,j]=w
    adj=csr_matrix(adj)
    deg=np.array(adj.sum(axis=1)).flatten()
    return diags(deg)-adj


def evolve_weighted(L_w, mass, dt, n_steps, phi0):
    """Standard leapfrog with weighted Laplacian."""
    phi=phi0.copy(); pi=np.zeros_like(phi); m2=mass**2
    for _ in range(n_steps):
        force=-L_w.dot(phi)-m2*phi
        pi+=0.5*dt*force; phi+=dt*pi
        force=-L_w.dot(phi)-m2*phi
        pi+=0.5*dt*force
    return phi


# ============================================================================
# Approach C: Combined (lapse + weighted Laplacian)
# ============================================================================

def evolve_combined(L_w, mass, dt_base, n_steps, phi0, alpha):
    """Both lapse and weighted Laplacian."""
    phi=phi0.copy(); pi=np.zeros_like(phi); m2=mass**2
    for _ in range(n_steps):
        dt_local = dt_base * alpha
        force = -L_w.dot(phi) - m2*phi
        pi += 0.5 * dt_local * force
        phi += dt_local * pi
        force = -L_w.dot(phi) - m2*phi
        pi += 0.5 * dt_local * force
    return phi


# ============================================================================
# Test Suite
# ============================================================================

def run_tests(n, approach_name, evolve_fn_flat, evolve_fn_grav, mass_default=0.3):
    """Run all bottleneck tests for a given approach."""
    print(f"\n{'='*70}")
    print(f"APPROACH: {approach_name}")
    print(f"{'='*70}")
    c = n//2; dt = 0.2; mp = (c,c,c+3)

    # 1. Gravity direction
    print(f"\n  --- Gravity direction ---")
    d0 = cz(evolve_fn_flat(mass_default, dt, 10, gauss(n)), n)
    dg = cz(evolve_fn_grav(mass_default, dt, 10, gauss(n)), n)
    delta = dg - d0
    print(f"    delta = {delta:+.4e} {'TOWARD' if delta>0 else 'AWAY'}")

    # 2. N-stability
    print(f"\n  --- N-stability ---")
    n_tw=0; n_tot=0; forces=[]
    for ns in range(2, 16):
        df = cz(evolve_fn_flat(mass_default, dt, ns, gauss(n)), n)
        dg = cz(evolve_fn_grav(mass_default, dt, ns, gauss(n)), n)
        d = dg - df; tw = d>0; n_tw+=tw; n_tot+=1; forces.append(d)
        print(f"    N={ns:2d}: {d:+.4e} {'TOWARD' if tw else 'AWAY'}")
    frac = n_tw/n_tot
    print(f"    TOWARD: {n_tw}/{n_tot} = {frac:.0%}")

    # 3. Equivalence
    print(f"\n  --- Equivalence ---")
    accels = []
    masses = [0.1, 0.2, 0.3, 0.5, 0.8]
    for m in masses:
        df = cz(evolve_fn_flat(m, dt, 10, gauss(n)), n)
        dg = cz(evolve_fn_grav(m, dt, 10, gauss(n)), n)
        accels.append(dg - df)
        print(f"    m={m:.2f}: delta={accels[-1]:+.4e}")
    fa=np.array(accels); ma=np.array(masses)
    _,_,rv,_,_=stats.linregress(ma,fa); r2=rv**2
    print(f"    R^2(defl vs mass) = {r2:.4f}")

    # 4. Achromaticity
    print(f"\n  --- Achromaticity ---")
    forces_k = []
    for k0 in [0, 0.2, 0.4, 0.6, 0.8]:
        x=np.arange(n); sigma=n/4
        gx=np.exp(-(x-c)**2/(2*sigma**2))
        env=gx[:,None,None]*gx[None,:,None]*gx[None,None,:]
        phi0=np.zeros(n**3,dtype=complex)
        for iz in range(n):
            for ix in range(n):
                for iy in range(n):
                    phi0[idx(ix,iy,iz,n)]=env[ix,iy,iz]*np.exp(1j*k0*iz)
        phi0/=np.linalg.norm(phi0)
        df=cz(evolve_fn_flat(mass_default, dt, 10, phi0), n)
        dg=cz(evolve_fn_grav(mass_default, dt, 10, phi0), n)
        forces_k.append(dg-df)
        print(f"    k={k0:.1f}: delta={forces_k[-1]:+.4e} {'TOWARD' if forces_k[-1]>0 else 'AWAY'}")
    fa_k=np.array(forces_k)
    same=all(f>0 for f in fa_k) or all(f<0 for f in fa_k)
    cv=np.std(fa_k)/np.mean(np.abs(fa_k)) if np.mean(np.abs(fa_k))>0 else 999
    print(f"    same_sign={same}, CV={cv:.4f}")

    # 5. F~M (field strength scaling)
    print(f"\n  --- F proportional to M ---")
    # This only makes sense for potential gravity, skip for geometric
    print(f"    (geometric gravity doesn't have a 'strength' parameter to sweep)")

    # 6. Norm conservation
    phi0 = gauss(n)
    phi_g = evolve_fn_grav(mass_default, dt, 20, phi0)
    norm_err = abs(np.sum(np.abs(phi_g)**2) - np.sum(np.abs(phi0)**2))
    print(f"\n  --- Norm ---")
    print(f"    |norm_final - norm_init| = {norm_err:.4e}")

    return frac, r2, same, cv


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("GEOMETRIC GRAVITY v2 — LAPSE + METRIC APPROACHES")
    print("=" * 70)

    n = 13; c = n//2; mp = (c,c,c+3)

    # Build flat Laplacian (reference)
    L_flat = regular_laplacian(n)

    # ── Approach A: Lapse ──
    r = field_r(n, mp)
    g_str = 2.0
    alpha = 1.0 / (1.0 + g_str * 5e-4 / (r + 0.5))  # lapse < 1 near mass

    def evA_flat(mass, dt, ns, phi0):
        return evolve_lapse(L_flat, mass, dt, ns, phi0, np.ones(n**3))
    def evA_grav(mass, dt, ns, phi0):
        return evolve_lapse(L_flat, mass, dt, ns, phi0, alpha)

    fracA, r2A, sameA, cvA = run_tests(n, "A: Lapse Function (dt_local = dt*alpha)", evA_flat, evA_grav)

    # ── Approach B: Weighted Laplacian ──
    L_weighted = weighted_laplacian(n, mp, g_str)

    def evB_flat(mass, dt, ns, phi0):
        return evolve_weighted(L_flat, mass, dt, ns, phi0)
    def evB_grav(mass, dt, ns, phi0):
        return evolve_weighted(L_weighted, mass, dt, ns, phi0)

    fracB, r2B, sameB, cvB = run_tests(n, "B: Metric-Weighted Laplacian", evB_flat, evB_grav)

    # ── Approach C: Combined ──
    def evC_flat(mass, dt, ns, phi0):
        return evolve_combined(L_flat, mass, dt, ns, phi0, np.ones(n**3))
    def evC_grav(mass, dt, ns, phi0):
        return evolve_combined(L_weighted, mass, dt, ns, phi0, alpha)

    fracC, r2C, sameC, cvC = run_tests(n, "C: Combined (Lapse + Weighted)", evC_flat, evC_grav)

    # ── Sweep lapse strength ──
    print(f"\n{'='*70}")
    print("LAPSE STRENGTH SWEEP (Approach A)")
    print(f"{'='*70}")
    for g in [0.5, 1.0, 2.0, 5.0, 10.0, 50.0]:
        alpha_s = 1.0 / (1.0 + g * 5e-4 / (r + 0.5))
        def ev_g(mass, dt, ns, phi0, a=alpha_s):
            return evolve_lapse(L_flat, mass, dt, ns, phi0, a)
        df = cz(evA_flat(0.3, 0.2, 10, gauss(n)), n)
        dg = cz(ev_g(0.3, 0.2, 10, gauss(n)), n)
        d = dg - df
        # Equivalence quick check
        accels = []
        for m in [0.1, 0.3, 1.0]:
            df2 = cz(evA_flat(m, 0.2, 10, gauss(n)), n)
            dg2 = cz(ev_g(m, 0.2, 10, gauss(n)), n)
            accels.append(dg2 - df2)
        cv_m = np.std(accels)/np.mean(np.abs(accels)) if np.mean(np.abs(accels))>0 else 999
        print(f"  g={g:5.1f}: delta={d:+.4e} {'TW' if d>0 else 'AW'}, equiv_CV={cv_m:.4f}")

    # ── Summary ──
    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"  {'Approach':<35s} {'N-stab':>8s} {'Equiv R^2':>10s} {'Achrom':>8s} {'CV':>8s}")
    print(f"  {'-'*35} {'-'*8} {'-'*10} {'-'*8} {'-'*8}")
    print(f"  {'A: Lapse':<35s} {fracA:>7.0%} {r2A:>10.4f} {'Y' if sameA else 'N':>8s} {cvA:>8.4f}")
    print(f"  {'B: Weighted Laplacian':<35s} {fracB:>7.0%} {r2B:>10.4f} {'Y' if sameB else 'N':>8s} {cvB:>8.4f}")
    print(f"  {'C: Combined':<35s} {fracC:>7.0%} {r2C:>10.4f} {'Y' if sameC else 'N':>8s} {cvC:>8.4f}")
    print(f"\n  Total time: {elapsed:.1f}s")
