#!/usr/bin/env python3
"""
Dirac Walk — Bottleneck Tests from Updated Card
=================================================
Tests the 4-component Dirac walk against the CRITICAL issues from
FULL_TEST_MATRIX_2026-04-10.md, not just the old 10-property card.

CRITICAL BOTTLENECKS:
  1. 3D KG dispersion — ALREADY SOLVED (R^2=1.000 via Hamiltonian)
  2. Equivalence principle / parameter separation — can mass and gravity
     coupling be decoupled? The chiral walk violates this (theta does both).
  3. Achromatic gravity — is the force k-independent?
  4. N-stability — gravity sign stable across N range?
  5. Born rule with proper barrier — fix the barrier geometry

ADDITIONAL KEY TESTS:
  6. Structural: linearity, norm preservation, locality, unitarity
  7. Light cone — does the walk respect v=1?
  8. Decoherence via phase noise on 2-slit visibility
  9. Distance law on adequate lattice
  10. Two-body superposition

Architecture: 4-component Dirac walk with split-step S_z*S_y*S_x*C(m),
  reversed coupling m(r) = m0*(1+f), periodic BCs.
"""

import numpy as np
from scipy import stats
from scipy.linalg import expm
import time

# ============================================================================
# Infrastructure (from v2/v3)
# ============================================================================
gamma0 = np.diag([1,1,-1,-1]).astype(complex)
gamma1 = np.array([[0,0,0,1],[0,0,1,0],[0,-1,0,0],[-1,0,0,0]], dtype=complex)
gamma2 = np.array([[0,0,0,-1j],[0,0,1j,0],[0,1j,0,0],[-1j,0,0,0]], dtype=complex)
gamma3 = np.array([[0,0,1,0],[0,0,0,-1],[-1,0,0,0],[0,1,0,0]], dtype=complex)
gammas_s = [gamma1, gamma2, gamma3]

def get_proj(gp):
    ev, ec = np.linalg.eigh(gp)
    return (sum(np.outer(ec[:,i],ec[:,i].conj()) for i in range(4) if ev[i]>0),
            sum(np.outer(ec[:,i],ec[:,i].conj()) for i in range(4) if ev[i]<0))

Px_p,Px_m = get_proj(gamma0@gamma1)
Py_p,Py_m = get_proj(gamma0@gamma2)
Pz_p,Pz_m = get_proj(gamma0@gamma3)

def coin_step(psi, mf, n):
    cm=np.cos(mf); sm=np.sin(mf)
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

def step(psi,mf,n):
    psi=coin_step(psi,mf,n)
    psi=shift_d(psi,n,Px_p,Px_m,0)
    psi=shift_d(psi,n,Py_p,Py_m,1)
    psi=shift_d(psi,n,Pz_p,Pz_m,2)
    return psi

def min_img(n,mp):
    c=np.arange(n)
    dx=np.minimum(np.abs(c[:,None,None]-mp[0]),n-np.abs(c[:,None,None]-mp[0]))
    dy=np.minimum(np.abs(c[None,:,None]-mp[1]),n-np.abs(c[None,:,None]-mp[1]))
    dz=np.minimum(np.abs(c[None,None,:]-mp[2]),n-np.abs(c[None,None,:]-mp[2]))
    return np.sqrt(dx**2+dy**2+dz**2)

def evolve(n,N,m0,S=0.0,mpos=None):
    psi=np.zeros((4,n,n,n),dtype=np.complex128)
    c=n//2
    for k in range(4): psi[k,c,c,c]=0.5
    mf=np.full((n,n,n),m0)
    if mpos and S>0:
        tf=np.zeros((n,n,n))
        for mp in mpos: tf+=S/(min_img(n,mp)+0.1)
        mf=m0*(1.0+tf)  # reversed coupling
    for _ in range(N): psi=step(psi,mf,n)
    return psi

def prob(psi): return np.sum(np.abs(psi)**2,axis=0)

def dirac_coin(m): return np.cos(m)*np.eye(4,dtype=complex)+1j*np.sin(m)*gamma0


# ============================================================================
# TEST 1: KG Dispersion (Hamiltonian — already confirmed R^2=1.000)
# ============================================================================

def test_kg():
    print("=" * 70)
    print("TEST 1: Klein-Gordon Dispersion (Hamiltonian Bloch)")
    print("=" * 70)
    m0 = 0.1; n = 9
    g0g = [gamma0@g for g in gammas_s]
    ks = 2*np.pi*np.arange(n)/n
    allE2, allk2 = [], []
    for mx in range(n):
        kx=ks[mx]; kxc=kx if kx<=np.pi else kx-2*np.pi
        for my in range(n):
            ky=ks[my]; kyc=ky if ky<=np.pi else ky-2*np.pi
            for mz in range(n):
                kz=ks[mz]; kzc=kz if kz<=np.pi else kz-2*np.pi
                H=m0*gamma0
                for j,(kv) in enumerate([kx,ky,kz]): H+=np.sin(kv)*g0g[j]
                Uk=expm(-1j*H)
                for ph in np.angle(np.linalg.eigvals(Uk)):
                    allE2.append(ph**2); allk2.append(kxc**2+kyc**2+kzc**2)
    allE2=np.array(allE2); allk2=np.array(allk2)
    m=allk2<1.0
    sl,ic,rv,_,_=stats.linregress(allk2[m],allE2[m])
    r2=rv**2
    print(f"  R^2 = {r2:.6f}, mass_fit = {np.sqrt(abs(ic)):.4f}")
    print(f"  PASS" if r2>0.99 else f"  FAIL")
    return r2


# ============================================================================
# TEST 2: Equivalence Principle / Parameter Separation
# ============================================================================

def test_equivalence():
    """Can we separate mass from gravity coupling?
    In the chiral walk, theta is BOTH mass (dispersion) AND gravity
    coupling (amplitude of force). This violates equivalence.

    In the Dirac walk with reversed coupling m(r) = m0*(1+f):
    - m0 sets the REST MASS (dispersion relation)
    - f(r) sets the GRAVITATIONAL FIELD (spatial variation)
    - The force should depend on f, not on m0 (at least at leading order)

    Test: fix f (same field), vary m0. Does force scale with m0?
    If force is independent of m0, mass and gravity are separated.
    If force ~ m0, they're coupled (like the chiral walk).
    """
    print("\n" + "=" * 70)
    print("TEST 2: Equivalence Principle / Parameter Separation")
    print("=" * 70)

    n = 17; N = 10; S = 5e-4; c = n//2

    masses = [0.05, 0.1, 0.15, 0.2, 0.3]
    forces = []
    for m0 in masses:
        r0 = prob(evolve(n, N, m0, 0.0))
        r1 = prob(evolve(n, N, m0, S, [(c,c,c+3)]))
        d = r1 - r0
        f = sum(d[c,c,c+dz] for dz in range(1,4))
        forces.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  m0={m0:.3f}: force={f:+.4e} {tag}")

    # Check: does force depend on m0?
    fa = np.array(forces)
    ma = np.array(masses)
    # If force is constant (independent of m0), R^2 of force vs m0 ~ 0
    # If force ~ m0, R^2 ~ 1
    valid = np.abs(fa) > 1e-30
    if np.sum(valid) >= 3:
        _, _, rv, _, _ = stats.linregress(ma[valid], fa[valid])
        r2_mass = rv**2
    else:
        r2_mass = 0.0

    # Also check: is force proportional to strength (F~M)?
    print(f"\n  R^2(force vs m0) = {r2_mass:.4f}")
    if r2_mass < 0.3:
        print("  -> Force is INDEPENDENT of rest mass m0")
        print("  -> Mass and gravity coupling ARE separated")
        print("  -> EQUIVALENCE PRINCIPLE: NOT VIOLATED (mass-gravity decoupled)")
    elif r2_mass > 0.7:
        print("  -> Force DEPENDS on rest mass m0")
        print("  -> Mass and gravity coupling are COUPLED")
        dep = "linear" if r2_mass > 0.9 else "nonlinear"
        print(f"  -> EQUIVALENCE PRINCIPLE: VIOLATED ({dep} mass-gravity coupling)")
    else:
        print("  -> Ambiguous mass dependence")

    return r2_mass


# ============================================================================
# TEST 3: Achromatic Gravity (k-independence)
# ============================================================================

def test_achromatic():
    """Is the gravity force k-independent?
    The chiral walk at fixed theta is achromatic (k doesn't appear in the
    coin), but the overall gravity depends on theta which is coupled to k.

    The Dirac walk: the gravity field modulates mass m. At different k,
    the coin effect is different: C(m) = exp(im)·γ^0. But the gravity
    force should be the same for all k if the coupling is truly via the
    amplitude mechanism.

    Test: for different initial k-states (plane waves), measure the
    centroid shift. If all give the same shift, gravity is achromatic.
    """
    print("\n" + "=" * 70)
    print("TEST 3: Achromatic Gravity (k-independence)")
    print("=" * 70)

    n = 17; N = 10; m0 = 0.1; S = 5e-4; c = n//2

    forces_by_k = []
    for k_idx in [0, 1, 2, 3, 4]:
        k = 2*np.pi*k_idx/n
        # Initialize with plane wave in z-direction
        psi0 = np.zeros((4,n,n,n), dtype=np.complex128)
        amp = 0.5 / np.sqrt(n)
        for iz in range(n):
            phase = np.exp(1j * k * iz)
            for comp in range(4):
                psi0[comp, c, c, iz] = amp * phase

        # Evolve with and without mass
        mf_flat = np.full((n,n,n), m0)
        mf_grav = np.full((n,n,n), m0)
        r = min_img(n, (c,c,c+3))
        mf_grav = m0 * (1.0 + S/(r+0.1))

        psi_flat = psi0.copy()
        psi_grav = psi0.copy()
        for _ in range(N):
            psi_flat = step(psi_flat, mf_flat, n)
            psi_grav = step(psi_grav, mf_grav, n)

        rho_flat = prob(psi_flat)
        rho_grav = prob(psi_grav)
        d = rho_grav - rho_flat
        f = sum(d[c,c,c+dz] for dz in range(1,4))
        forces_by_k.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  k={k:.4f} (idx={k_idx}): force={f:+.4e} {tag}")

    fa = np.array(forces_by_k)
    # Achromatic = force is same sign and similar magnitude for all k
    all_toward = all(f > 0 for f in fa)
    all_away = all(f < 0 for f in fa)
    same_sign = all_toward or all_away

    if len(fa) > 0 and np.mean(np.abs(fa)) > 0:
        cv = np.std(fa) / np.mean(np.abs(fa))
    else:
        cv = float('inf')

    print(f"\n  Same sign: {same_sign}")
    print(f"  CV of force magnitudes: {cv:.4f}")
    if same_sign and cv < 0.5:
        print("  -> ACHROMATIC (k-independent gravity)")
    elif same_sign:
        print(f"  -> PARTIALLY achromatic (same sign but CV={cv:.2f})")
    else:
        print("  -> CHROMATIC (sign flips with k)")

    return same_sign, cv


# ============================================================================
# TEST 4: N-stability (gravity sign across N range)
# ============================================================================

def test_n_stability():
    print("\n" + "=" * 70)
    print("TEST 4: N-Stability (gravity sign vs layer count)")
    print("=" * 70)

    n = 17; m0 = 0.1; S = 5e-4; c = n//2
    n_toward = 0; n_total = 0

    for N in range(6, 15):
        r0 = prob(evolve(n, N, m0, 0.0))
        r1 = prob(evolve(n, N, m0, S, [(c,c,c+3)]))
        d = r1 - r0
        tw = sum(d[c,c,c+dz] for dz in range(1,4))
        aw = sum(d[c,c,c-dz] for dz in range(1,4))
        is_tw = tw > aw
        if is_tw: n_toward += 1
        n_total += 1
        print(f"  N={N:2d}: tw={tw:+.4e}, aw={aw:+.4e} {'TOWARD' if is_tw else 'AWAY'}")

    frac = n_toward / n_total
    print(f"\n  TOWARD fraction: {n_toward}/{n_total} = {frac:.2f}")
    if frac > 0.8:
        print("  -> N-STABLE (>80% TOWARD)")
    elif frac > 0.5:
        print(f"  -> PARTIAL N-stability ({frac:.0%} TOWARD)")
    else:
        print("  -> N-UNSTABLE")
    return frac


# ============================================================================
# TEST 5: Born Rule with Fixed Barrier
# ============================================================================

def test_born():
    """Born rule using higher mass for more spreading + later barrier."""
    print("\n" + "=" * 70)
    print("TEST 5: Born Rule (adapted barrier geometry)")
    print("=" * 70)

    n = 15; m0 = 0.5; N = 12  # higher mass for more chirality mixing
    c = n//2
    bl = N // 2  # barrier at midpoint
    slits = [c-1, c, c+1]

    def ev(sl_list):
        psi = np.zeros((4,n,n,n), dtype=np.complex128)
        for k in range(4): psi[k,c,c,c] = 0.5
        mf = np.full((n,n,n), m0)
        for layer in range(N):
            psi = step(psi, mf, n)
            if layer == bl - 1:
                mask = np.zeros((n,n,n), dtype=bool)
                for sy in sl_list: mask[sy,:,:] = True
                for k in range(4): psi[k] *= mask
        return prob(psi)

    rf = ev(slits)
    P_total = np.sum(rf)
    print(f"  Total P after barrier: {P_total:.6e}")

    if P_total < 1e-20:
        print("  No probability passes barrier — trying z-direction slits")
        # Try slits in z instead
        def ev_z(sl_list):
            psi = np.zeros((4,n,n,n), dtype=np.complex128)
            for k in range(4): psi[k,c,c,c] = 0.5
            mf = np.full((n,n,n), m0)
            for layer in range(N):
                psi = step(psi, mf, n)
                if layer == bl - 1:
                    mask = np.zeros((n,n,n), dtype=bool)
                    for sz in sl_list: mask[:,:,sz] = True
                    for k in range(4): psi[k] *= mask
            return prob(psi)

        slits_z = [c-1, c, c+1]
        rf = ev_z(slits_z)
        P_total = np.sum(rf)
        print(f"  P with z-slits: {P_total:.6e}")
        if P_total > 1e-20:
            rs = [ev_z([s]) for s in slits_z]
            born = np.sum(np.abs(rf - sum(rs))) / P_total
            print(f"  Born |I3|/P = {born:.6f}")
            print(f"  {'PASS' if born > 0.01 else 'FAIL'}")
            return born
        else:
            # Try no barrier, just measure I3 on the free walk
            print("  No barrier works — testing Born on free propagation")
            psi = np.zeros((4,n,n,n), dtype=np.complex128)
            for k in range(4): psi[k,c,c,c] = 0.5
            mf = np.full((n,n,n), m0)
            for _ in range(N): psi = step(psi, mf, n)
            rho = prob(psi)
            norm = np.sum(rho)
            print(f"  Free norm = {norm:.6e} (should be ~1)")
            # Born is structural (linearity) — check norm preservation
            print(f"  Norm preservation: {'PASS' if abs(norm-1)<1e-6 else 'FAIL'}")
            return -1  # couldn't test with barriers
    else:
        rs = [ev([s]) for s in slits]
        born = np.sum(np.abs(rf - sum(rs))) / P_total
        print(f"  Born |I3|/P = {born:.6f}")
        print(f"  {'PASS' if born > 0.01 else 'FAIL'}")
        return born


# ============================================================================
# TEST 6: Structural Properties
# ============================================================================

def test_structural():
    print("\n" + "=" * 70)
    print("TEST 6: Structural Properties")
    print("=" * 70)

    m0 = 0.1; n = 5
    dim = 4*n**3

    # Build full unitary
    print(f"  Building {dim}x{dim} evolution matrix...")
    mf = np.full((n,n,n), m0)
    U = np.zeros((dim,dim), dtype=complex)
    for col in range(dim):
        psi = np.zeros((4,n,n,n), dtype=complex)
        comp = col // (n**3)
        spatial = col % (n**3)
        ix = spatial//(n*n); iy = (spatial//n)%n; iz = spatial%n
        psi[comp,ix,iy,iz] = 1.0
        psi = step(psi, mf, n)
        U[:,col] = psi.reshape(-1)

    # Linearity: automatic (matrix multiplication is linear)
    print("  Linearity: YES (matrix operator)")

    # Unitarity
    err = np.max(np.abs(U@U.conj().T - np.eye(dim)))
    print(f"  Unitarity: max|UU†-I| = {err:.2e} {'PASS' if err<1e-10 else 'FAIL'}")

    # Norm preservation (follows from unitarity)
    print(f"  Norm preserved: {'YES' if err<1e-10 else 'NO'}")

    # Locality (sparse)
    nnz = np.sum(np.abs(U) > 1e-15)
    sparsity = nnz / (dim*dim)
    print(f"  Sparsity: {nnz}/{dim*dim} = {sparsity:.4f} ({'sparse' if sparsity < 0.1 else 'dense'})")

    # Light cone check: source at center, check max spread after 1 step
    psi = np.zeros((4,n,n,n), dtype=complex)
    c=n//2
    for k in range(4): psi[k,c,c,c]=0.5
    psi1 = step(psi, mf, n)
    rho = prob(psi1)
    # Max distance with nonzero probability
    max_dist = 0
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                if rho[ix,iy,iz] > 1e-20:
                    d = abs(ix-c)+abs(iy-c)+abs(iz-c)
                    max_dist = max(max_dist, d)
    print(f"  Light cone: max spread after 1 step = {max_dist} sites")
    print(f"  v_max = {max_dist} {'(v=3, one step per axis)' if max_dist == 3 else ''}")

    return err < 1e-10


# ============================================================================
# TEST 7: Decoherence (phase noise suppresses interference)
# ============================================================================

def test_decoherence():
    """Use norm of off-diagonal coherences as the decoherence measure."""
    print("\n" + "=" * 70)
    print("TEST 7: Decoherence (coherence suppression by noise)")
    print("=" * 70)

    n = 13; m0 = 0.3; N = 10; c = n//2

    def coherence_measure(noise_str, seed=42):
        """Evolve and measure off-diagonal coherence of the reduced density matrix."""
        psi = np.zeros((4,n,n,n), dtype=np.complex128)
        for k in range(4): psi[k,c,c,c] = 0.5
        mf = np.full((n,n,n), m0)
        rng = np.random.RandomState(seed) if noise_str > 0 else None
        for layer in range(N):
            if noise_str > 0:
                ph = rng.uniform(-noise_str, noise_str, (n,n,n))
                for k in range(4): psi[k] *= np.exp(1j*ph)
            psi = step(psi, mf, n)

        # Reduced density matrix: trace over spatial DOF
        # rho_internal[a,b] = sum_x psi[a,x]*conj(psi[b,x])
        psi_flat = psi.reshape(4, -1)  # (4, n^3)
        rho = psi_flat @ psi_flat.conj().T  # (4, 4)
        # Coherence = sum of off-diagonal |rho_ab| / trace
        tr = np.real(np.trace(rho))
        offdiag = np.sum(np.abs(rho)) - np.sum(np.abs(np.diag(rho)))
        coh = offdiag / tr if tr > 0 else 0
        return coh

    print("  Noise vs coherence:")
    cohs = []
    for noise in [0.0, 0.1, 0.3, 0.5, 1.0, 2.0]:
        coh = coherence_measure(noise)
        cohs.append((noise, coh))
        print(f"    noise={noise:.1f}: coherence={coh:.6f}")

    c0 = cohs[0][1]  # clean
    cn = cohs[-1][1]  # noisiest
    passes = cn < c0 * 0.9  # noise reduces coherence by at least 10%
    print(f"\n  Clean coherence: {c0:.6f}")
    print(f"  Noisy coherence: {cn:.6f}")
    print(f"  Reduction: {(1-cn/c0)*100:.1f}%")
    print(f"  {'PASS' if passes else 'FAIL'} (need >10% reduction)")
    return passes, c0, cn


# ============================================================================
# TEST 8: Distance Law (large lattice)
# ============================================================================

def test_distance_law():
    print("\n" + "=" * 70)
    print("TEST 8: Distance Law")
    print("=" * 70)

    n = 21; N = 10; m0 = 0.1; S = 5e-4; c = n//2
    max_off = n // 4
    offs = list(range(2, max_off+1))

    r0 = prob(evolve(n, N, m0, 0.0))
    forces = []
    for dz in offs:
        r1 = prob(evolve(n, N, m0, S, [(c,c,c+dz)]))
        d = r1 - r0
        f = sum(d[c,c,c+dd] for dd in range(1,dz+1))
        forces.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        print(f"  offset={dz}: force={f:+.4e} {tag}")

    n_tw = sum(1 for f in forces if f > 0)
    print(f"\n  TOWARD: {n_tw}/{len(forces)}")

    fa = np.array(forces); oa = np.array(offs, dtype=float)
    tw_mask = fa > 0
    if np.sum(tw_mask) >= 3:
        lr = np.log(oa[tw_mask]); lf = np.log(fa[tw_mask])
        cf = np.polyfit(lr, lf, 1)
        pf = np.polyval(cf, lr)
        sr = np.sum((lf-pf)**2); st = np.sum((lf-np.mean(lf))**2)
        r2 = 1-sr/st if st > 0 else 0; alpha = cf[0]
        print(f"  Power law (TOWARD pts): alpha={alpha:.3f}, R^2={r2:.4f}")
    else:
        alpha, r2 = 0.0, 0.0

    return n_tw, len(forces), alpha, r2


# ============================================================================
# TEST 9: Two-Body Superposition
# ============================================================================

def test_superposition():
    print("\n" + "=" * 70)
    print("TEST 9: Two-Body Superposition")
    print("=" * 70)

    n = 15; N = 10; m0 = 0.1; S = 5e-4; c = n//2

    # Individual masses
    r0 = prob(evolve(n, N, m0, 0.0))
    rA = prob(evolve(n, N, m0, S, [(c,c,c+3)]))
    rB = prob(evolve(n, N, m0, S, [(c,c,c-3)]))
    rAB = prob(evolve(n, N, m0, S, [(c,c,c+3),(c,c,c-3)]))

    dA = rA - r0; dB = rB - r0; dAB = rAB - r0
    # Superposition: dAB should be ~ dA + dB
    sup_err = np.sum(np.abs(dAB - dA - dB)) / np.sum(np.abs(dAB)) if np.sum(np.abs(dAB)) > 0 else 0
    print(f"  |dAB - dA - dB| / |dAB| = {sup_err*100:.2f}%")
    print(f"  {'PASS' if sup_err < 0.01 else 'MARGINAL' if sup_err < 0.05 else 'FAIL'} (need <1%)")
    return sup_err


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("DIRAC WALK — BOTTLENECK TESTS FROM UPDATED CARD")
    print("=" * 70)

    results = {}

    # 1. KG
    r2_kg = test_kg()
    results['KG R^2'] = r2_kg

    # 2. Equivalence
    r2_eq = test_equivalence()
    results['Equiv R^2(force vs m)'] = r2_eq

    # 3. Achromatic
    same_sign, cv_k = test_achromatic()
    results['Achromatic same_sign'] = same_sign
    results['Achromatic CV'] = cv_k

    # 4. N-stability
    frac_tw = test_n_stability()
    results['N-stability TOWARD%'] = frac_tw

    # 5. Born
    born = test_born()
    results['Born'] = born

    # 6. Structural
    unitary = test_structural()
    results['Unitary'] = unitary

    # 7. Decoherence
    decoh_pass, c0, cn = test_decoherence()
    results['Decoherence'] = decoh_pass

    # 8. Distance law
    n_tw, n_tot, alpha, r2_dl = test_distance_law()
    results['Dist TOWARD frac'] = f"{n_tw}/{n_tot}"
    results['Dist alpha'] = alpha

    # 9. Superposition
    sup = test_superposition()
    results['Superposition err'] = sup

    # ── SUMMARY ───────────────────────────────────────────────────────
    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("SUMMARY — DIRAC WALK vs UPDATED CARD BOTTLENECKS")
    print(f"{'='*70}")

    print(f"\n  {'Test':<30s} {'Result':<20s} {'Status'}")
    print(f"  {'-'*30} {'-'*20} {'-'*10}")
    print(f"  {'KG dispersion':<30s} {'R^2='+f'{r2_kg:.6f}':<20s} {'PASS' if r2_kg>0.99 else 'FAIL'}")
    print(f"  {'Equivalence (m-g sep)':<30s} {'R^2='+f'{r2_eq:.4f}':<20s} {'SEPARATED' if r2_eq<0.3 else 'COUPLED'}")
    print(f"  {'Achromatic gravity':<30s} {'CV='+f'{cv_k:.4f}':<20s} {'PASS' if same_sign and cv_k<0.5 else 'PARTIAL' if same_sign else 'FAIL'}")
    print(f"  {'N-stability':<30s} {f'{frac_tw:.0%} TOWARD':<20s} {'PASS' if frac_tw>0.8 else 'PARTIAL' if frac_tw>0.5 else 'FAIL'}")
    print(f"  {'Born rule':<30s} {f'{born:.6f}' if born>=0 else 'barrier fail':<20s} {'PASS' if born>0.01 else 'FAIL'}")
    print(f"  {'Unitarity':<30s} {'exact':<20s} {'PASS' if unitary else 'FAIL'}")
    print(f"  {'Decoherence':<30s} {f'{(1-cn/c0)*100:.0f}% reduction':<20s} {'PASS' if decoh_pass else 'FAIL'}")
    print(f"  {'Distance law':<30s} {f'{n_tw}/{n_tot} TOWARD':<20s} {'PASS' if n_tw>n_tot//2 else 'FAIL'}")
    print(f"  {'Superposition':<30s} {f'{sup*100:.2f}%':<20s} {'PASS' if sup<0.01 else 'MARGINAL' if sup<0.05 else 'FAIL'}")

    print(f"\n  Total time: {elapsed:.1f}s")
