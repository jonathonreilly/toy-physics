#!/usr/bin/env python3
"""
Scalar Potential Gravity on 4-Component Dirac Walk
====================================================
THE ROOT CAUSE: All three gravity blockers (chromaticity, equivalence
  violation, N-oscillation) stem from encoding gravity in the COIN
  (amplitude coupling). The coin phase goes through exp(i·k·S), making
  everything k-dependent, mass-dependent, and oscillatory.

THE FIX: Move gravity to a SCALAR POTENTIAL. After each coin+shift step,
  apply psi(x) *= exp(i * g * Phi(x)) where Phi = -strength/(r+eps).

  - Phi has no k dependence → achromatic
  - Phi has no mass dependence → equivalence principle
  - Phase accumulates linearly with N → N-stable

This is how potentials work in quantum mechanics (Ehrenfest theorem:
  d<x>/dt ~ <p>, d<p>/dt ~ -<∂V/∂x>). The gradient of Phi deflects
  the wavepacket group velocity.

HYPOTHESIS: Scalar potential gravity is achromatic (CV<0.3),
  mass-independent (R²<0.1), and N-stable (>80% TOWARD).
FALSIFICATION: If centroid shift is zero for all g values, the
  scalar potential mechanism cannot produce gravity on a discrete walk.
"""

import numpy as np
from scipy import stats
import time

# ============================================================================
# Gamma matrices + infrastructure
# ============================================================================
gamma0 = np.diag([1,1,-1,-1]).astype(complex)
gamma1 = np.array([[0,0,0,1],[0,0,1,0],[0,-1,0,0],[-1,0,0,0]], dtype=complex)
gamma2 = np.array([[0,0,0,-1j],[0,0,1j,0],[0,1j,0,0],[-1j,0,0,0]], dtype=complex)
gamma3 = np.array([[0,0,1,0],[0,0,0,-1],[-1,0,0,0],[0,1,0,0]], dtype=complex)

def get_proj(gp):
    ev,ec=np.linalg.eigh(gp)
    return (sum(np.outer(ec[:,i],ec[:,i].conj()) for i in range(4) if ev[i]>0),
            sum(np.outer(ec[:,i],ec[:,i].conj()) for i in range(4) if ev[i]<0))

Px_p,Px_m = get_proj(gamma0@gamma1)
Py_p,Py_m = get_proj(gamma0@gamma2)
Pz_p,Pz_m = get_proj(gamma0@gamma3)

def coin_step(psi, m0, n):
    """UNIFORM mass coin — same mass everywhere."""
    cm=np.cos(m0); sm=np.sin(m0)
    o=np.zeros_like(psi)
    o[0]=(cm+1j*sm)*psi[0]; o[1]=(cm+1j*sm)*psi[1]
    o[2]=(cm-1j*sm)*psi[2]; o[3]=(cm-1j*sm)*psi[3]
    return o

def shift_d(psi,n,Pp,Pm,ax):
    o=np.zeros_like(psi)
    for c in range(4):
        pp=sum(Pp[c,d]*psi[d] for d in range(4))
        pm=sum(Pm[c,d]*psi[d] for d in range(4))
        o[c]+=np.roll(pp,-1,axis=ax); o[c]+=np.roll(pm,+1,axis=ax)
    return o

def potential_step(psi, Phi):
    """Apply scalar potential: psi(x) *= exp(i * Phi(x))."""
    phase = np.exp(1j * Phi)
    o = np.zeros_like(psi)
    for k in range(4):
        o[k] = psi[k] * phase
    return o

def step_with_potential(psi, m0, Phi, n):
    """One full step: coin(m0) + shift_x + shift_y + shift_z + potential."""
    psi = coin_step(psi, m0, n)
    psi = shift_d(psi, n, Px_p, Px_m, 0)
    psi = shift_d(psi, n, Py_p, Py_m, 1)
    psi = shift_d(psi, n, Pz_p, Pz_m, 2)
    psi = potential_step(psi, Phi)
    return psi

def min_img(n, mp):
    c=np.arange(n)
    dx=np.minimum(np.abs(c[:,None,None]-mp[0]),n-np.abs(c[:,None,None]-mp[0]))
    dy=np.minimum(np.abs(c[None,:,None]-mp[1]),n-np.abs(c[None,:,None]-mp[1]))
    dz=np.minimum(np.abs(c[None,None,:]-mp[2]),n-np.abs(c[None,None,:]-mp[2]))
    return np.sqrt(dx**2+dy**2+dz**2)

def make_potential(n, g, strength, mass_positions):
    """Phi(x) = -g * sum_masses strength/(r+eps)."""
    Phi = np.zeros((n,n,n))
    for mp in mass_positions:
        r = min_img(n, mp)
        Phi += -g * strength / (r + 0.1)
    return Phi

def evolve(n, N, m0, g=0.0, strength=0.0, mpos=None):
    psi = np.zeros((4,n,n,n), dtype=np.complex128)
    c=n//2
    for k in range(4): psi[k,c,c,c] = 0.5
    Phi = make_potential(n, g, strength, mpos) if mpos and g > 0 else np.zeros((n,n,n))
    for _ in range(N):
        psi = step_with_potential(psi, m0, Phi, n)
    return psi

def prob(psi): return np.sum(np.abs(psi)**2, axis=0)


# ============================================================================
# TEST 1: Gravity Direction + Coupling Strength Sweep
# ============================================================================

def test_gravity_direction():
    print("=" * 70)
    print("TEST 1: Gravity Direction (scalar potential)")
    print("=" * 70)

    n=17; m0=0.1; S=5e-4; c=n//2

    print("\n  g sweep (fixed mass, strength, N=10):")
    for g in [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        r0 = prob(evolve(n, 10, m0, 0.0, 0.0))
        r1 = prob(evolve(n, 10, m0, g, S, [(c,c,c+3)]))
        d = r1 - r0
        tw = sum(d[c,c,c+dz] for dz in range(1,4))
        aw = sum(d[c,c,c-dz] for dz in range(1,4))
        tag = "TOWARD" if tw > aw else "AWAY"
        print(f"    g={g:6.2f}: tw={tw:+.4e}, aw={aw:+.4e} -> {tag}")

    # Also try negative g
    print("\n  Negative g (should flip direction):")
    for g in [-0.1, -1.0, -5.0]:
        r0 = prob(evolve(n, 10, m0, 0.0, 0.0))
        r1 = prob(evolve(n, 10, m0, g, S, [(c,c,c+3)]))
        d = r1 - r0
        tw = sum(d[c,c,c+dz] for dz in range(1,4))
        aw = sum(d[c,c,c-dz] for dz in range(1,4))
        tag = "TOWARD" if tw > aw else "AWAY"
        print(f"    g={g:6.2f}: tw={tw:+.4e}, aw={aw:+.4e} -> {tag}")


# ============================================================================
# TEST 2: N-Stability
# ============================================================================

def test_n_stability():
    print("\n" + "=" * 70)
    print("TEST 2: N-Stability")
    print("=" * 70)

    n=17; m0=0.1; S=5e-4; c=n//2

    for g in [1.0, 5.0]:
        print(f"\n  g={g}:")
        n_tw = 0; n_tot = 0
        forces = []
        for N in range(4, 15):
            r0 = prob(evolve(n, N, m0, 0.0, 0.0))
            r1 = prob(evolve(n, N, m0, g, S, [(c,c,c+3)]))
            d = r1 - r0
            tw = sum(d[c,c,c+dz] for dz in range(1,4))
            aw = sum(d[c,c,c-dz] for dz in range(1,4))
            is_tw = tw > aw
            if is_tw: n_tw += 1
            n_tot += 1
            forces.append(tw - aw)
            print(f"    N={N:2d}: tw={tw:+.4e}, aw={aw:+.4e} {'TOWARD' if is_tw else 'AWAY'}")

        frac = n_tw/n_tot
        # Check monotonic growth of |force|
        abs_f = [abs(f) for f in forces]
        growing = sum(1 for i in range(len(abs_f)-1) if abs_f[i+1] >= abs_f[i]*0.8)
        print(f"    TOWARD fraction: {n_tw}/{n_tot} = {frac:.2f}")
        print(f"    Force growing: {growing}/{len(abs_f)-1}")
        print(f"    {'PASS' if frac > 0.8 else 'FAIL'}")


# ============================================================================
# TEST 3: Chromaticity (achromatic gravity)
# ============================================================================

def test_achromatic():
    print("\n" + "=" * 70)
    print("TEST 3: Achromatic Gravity (k-independence)")
    print("=" * 70)

    n=17; m0=0.1; g=5.0; S=5e-4; c=n//2; N=10

    forces = []
    for k_idx in range(n//2 + 1):
        k = 2*np.pi*k_idx/n
        # Plane wave initial state in z-direction
        psi0 = np.zeros((4,n,n,n), dtype=np.complex128)
        amp = 0.5 / np.sqrt(n)
        for iz in range(n):
            phase = np.exp(1j * k * iz)
            for comp in range(4):
                psi0[comp, c, c, iz] = amp * phase

        Phi_flat = np.zeros((n,n,n))
        Phi_grav = make_potential(n, g, S, [(c,c,c+3)])

        psi_flat = psi0.copy()
        psi_grav = psi0.copy()
        for _ in range(N):
            psi_flat = step_with_potential(psi_flat, m0, Phi_flat, n)
            psi_grav = step_with_potential(psi_grav, m0, Phi_grav, n)

        rho_f = prob(psi_flat); rho_g = prob(psi_grav)
        d = rho_g - rho_f
        f = sum(d[c,c,c+dz] for dz in range(1,4))
        forces.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  k={k:.4f} (idx={k_idx}): force={f:+.4e} {tag}")

    fa = np.array(forces)
    all_toward = all(f > 0 for f in fa)
    all_away = all(f < 0 for f in fa)
    same_sign = all_toward or all_away

    mean_abs = np.mean(np.abs(fa))
    cv = np.std(fa) / mean_abs if mean_abs > 0 else float('inf')

    print(f"\n  Same sign: {same_sign} ({'all TOWARD' if all_toward else 'all AWAY' if all_away else 'MIXED'})")
    print(f"  CV = {cv:.4f}")
    if same_sign and cv < 0.3:
        print("  -> ACHROMATIC PASS")
    elif same_sign and cv < 1.0:
        print("  -> PARTIALLY achromatic")
    else:
        print("  -> CHROMATIC FAIL")

    return same_sign, cv


# ============================================================================
# TEST 4: Equivalence Principle (mass independence)
# ============================================================================

def test_equivalence():
    print("\n" + "=" * 70)
    print("TEST 4: Equivalence Principle (force vs rest mass)")
    print("=" * 70)

    n=17; g=5.0; S=5e-4; c=n//2; N=10

    forces = []
    masses = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5]
    for m0 in masses:
        r0 = prob(evolve(n, N, m0, 0.0, 0.0))
        r1 = prob(evolve(n, N, m0, g, S, [(c,c,c+3)]))
        d = r1 - r0
        f = sum(d[c,c,c+dz] for dz in range(1,4))
        forces.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  m0={m0:.3f}: force={f:+.4e} {tag}")

    fa = np.array(forces)
    ma = np.array(masses)
    valid = np.abs(fa) > 1e-30
    if np.sum(valid) >= 3:
        _, _, rv, _, _ = stats.linregress(ma[valid], fa[valid])
        r2 = rv**2
    else:
        r2 = 0.0

    print(f"\n  R^2(force vs mass) = {r2:.4f}")
    if r2 < 0.1:
        print("  -> EQUIVALENCE PRINCIPLE HOLDS (force independent of mass)")
    elif r2 < 0.5:
        print("  -> PARTIAL mass dependence")
    else:
        print("  -> EQUIVALENCE VIOLATED (force depends on mass)")

    return r2


# ============================================================================
# TEST 5: F proportional to M (field strength)
# ============================================================================

def test_fpm():
    print("\n" + "=" * 70)
    print("TEST 5: F proportional to M")
    print("=" * 70)

    n=17; m0=0.1; g=5.0; c=n//2; N=10

    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    r0 = prob(evolve(n, N, m0, 0.0, 0.0))
    for S in strengths:
        r1 = prob(evolve(n, N, m0, g, S, [(c,c,c+3)]))
        d = r1 - r0
        f = sum(d[c,c,c+dz] for dz in range(1,4))
        forces.append(f)
        print(f"  S={S:.0e}: force={f:+.4e}")

    fa = np.array(forces); sa = np.array(strengths)
    co = np.polyfit(sa, fa, 1); pred = np.polyval(co, sa)
    ss_r = np.sum((fa-pred)**2); ss_t = np.sum((fa-np.mean(fa))**2)
    r2 = 1 - ss_r/ss_t if ss_t > 0 else 0
    print(f"\n  F~M R^2 = {r2:.6f}")
    print(f"  {'PASS' if r2 > 0.9 else 'FAIL'}")
    return r2


# ============================================================================
# TEST 6: Distance Law
# ============================================================================

def test_distance():
    print("\n" + "=" * 70)
    print("TEST 6: Distance Law")
    print("=" * 70)

    n=21; m0=0.1; g=5.0; S=5e-4; c=n//2; N=10
    max_off = n // 4
    offs = list(range(2, max_off+1))

    r0 = prob(evolve(n, N, m0, 0.0, 0.0))
    forces = []
    for dz in offs:
        r1 = prob(evolve(n, N, m0, g, S, [(c,c,c+dz)]))
        d = r1 - r0
        f = sum(d[c,c,c+dd] for dd in range(1, dz+1))
        forces.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  offset={dz}: force={f:+.4e} {tag}")

    n_tw = sum(1 for f in forces if f > 0)
    print(f"\n  TOWARD: {n_tw}/{len(forces)}")

    fa = np.array(forces); oa = np.array(offs, dtype=float)
    tw = fa > 0
    if np.sum(tw) >= 3:
        lr=np.log(oa[tw]); lf=np.log(fa[tw])
        cf=np.polyfit(lr,lf,1); pf=np.polyval(cf,lr)
        sr=np.sum((lf-pf)**2); st=np.sum((lf-np.mean(lf))**2)
        r2=1-sr/st if st>0 else 0; alpha=cf[0]
        print(f"  Power law: alpha={alpha:.3f}, R^2={r2:.4f}")
    else:
        alpha, r2 = 0.0, 0.0


# ============================================================================
# TEST 7: Two-Body Superposition
# ============================================================================

def test_superposition():
    print("\n" + "=" * 70)
    print("TEST 7: Two-Body Superposition")
    print("=" * 70)

    n=17; m0=0.1; g=5.0; S=5e-4; c=n//2; N=10

    r0 = prob(evolve(n, N, m0, 0.0, 0.0))
    rA = prob(evolve(n, N, m0, g, S, [(c,c,c+3)]))
    rB = prob(evolve(n, N, m0, g, S, [(c,c,c-3)]))
    rAB = prob(evolve(n, N, m0, g, S, [(c,c,c+3),(c,c,c-3)]))

    dA=rA-r0; dB=rB-r0; dAB=rAB-r0
    err = np.sum(np.abs(dAB-dA-dB))/np.sum(np.abs(dAB)) if np.sum(np.abs(dAB))>0 else 0
    print(f"  |dAB - dA - dB| / |dAB| = {err*100:.4f}%")
    print(f"  {'PASS' if err<0.01 else 'MARGINAL' if err<0.05 else 'FAIL'}")
    return err


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("SCALAR POTENTIAL GRAVITY ON 4-COMPONENT DIRAC WALK")
    print("=" * 70)
    print("ROOT CAUSE: amplitude coupling (coin) makes gravity chromatic,")
    print("  mass-coupled, and N-oscillatory.")
    print("FIX: scalar potential Phi(x) applied after each step.")
    print("PREDICTION: achromatic, mass-independent, N-stable gravity.")
    print()

    test_gravity_direction()
    test_n_stability()
    same_sign, cv = test_achromatic()
    r2_eq = test_equivalence()
    r2_fm = test_fpm()
    test_distance()
    sup = test_superposition()

    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("SUMMARY — SCALAR POTENTIAL GRAVITY")
    print(f"{'='*70}")
    print(f"  Achromatic:    same_sign={same_sign}, CV={cv:.4f} {'PASS' if same_sign and cv<0.3 else 'FAIL'}")
    print(f"  Equivalence:   R^2(force vs m)={r2_eq:.4f} {'PASS' if r2_eq<0.1 else 'FAIL'}")
    print(f"  F~M:           R^2={r2_fm:.6f} {'PASS' if r2_fm>0.9 else 'FAIL'}")
    print(f"  Superposition: {sup*100:.4f}% {'PASS' if sup<0.01 else 'FAIL'}")
    print(f"  Total time: {elapsed:.1f}s")
