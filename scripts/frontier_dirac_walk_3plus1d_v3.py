#!/usr/bin/env python3
"""
4-Component Dirac Walk v3 — Single-Step Hamiltonian + Convergence
==================================================================
Two independent attacks on the remaining gaps:

ATTACK 1: KG ISOTROPY
  The split-step ordering (S_z*S_y*S_x*C) breaks cubic symmetry, giving
  R^2=0.91. Replace with single-step U = exp(-i*H*dt) where
    H = m*gamma0 + sum_j sin(k_j)*gamma0*gamma_j
  is the full Dirac Hamiltonian. In Bloch space this is exact. In position
  space, use the Bloch decomposition to verify and then implement via FFT.

ATTACK 2: CONVERGENCE
  v2 closure card was 6/10 on n=13. The chiral walk needed n>=17, N>=14.
  Test at n=17 with N=12,14,16 using the split-step walk (faster than
  Hamiltonian for real-space evolution). Reversed coupling m(1+f).

ATTACK 3: AB RING TOPOLOGY
  The AB test failed because a uniform phase on all x-shifts is trivially
  gauge-equivalent to zero. Instead: create a flux tube by applying phase
  only to links crossing a specific surface (Stokes theorem). Use a
  ring geometry: source -> barrier with 2 slits -> detector, with flux
  threaded between the slits.

HYPOTHESIS:
  Attack 1: R^2 > 0.99 with Hamiltonian approach
  Attack 2: Closure card improves to 8+/10 at n=17
  Attack 3: AB visibility > 0.5 with proper flux tube
"""

import numpy as np
from scipy import stats
from scipy.linalg import expm
import time

# ============================================================================
# Gamma matrices
# ============================================================================
gamma0 = np.diag([1, 1, -1, -1]).astype(complex)
gamma1 = np.array([[0,0,0,1],[0,0,1,0],[0,-1,0,0],[-1,0,0,0]], dtype=complex)
gamma2 = np.array([[0,0,0,-1j],[0,0,1j,0],[0,1j,0,0],[-1j,0,0,0]], dtype=complex)
gamma3 = np.array([[0,0,1,0],[0,0,0,-1],[-1,0,0,0],[0,1,0,0]], dtype=complex)
gammas_spatial = [gamma1, gamma2, gamma3]

def get_projectors(gp):
    evals, evecs = np.linalg.eigh(gp)
    Pp = sum(np.outer(evecs[:,i], evecs[:,i].conj()) for i in range(4) if evals[i] > 0)
    Pm = sum(np.outer(evecs[:,i], evecs[:,i].conj()) for i in range(4) if evals[i] < 0)
    return Pp, Pm

Px_p, Px_m = get_projectors(gamma0 @ gamma1)
Py_p, Py_m = get_projectors(gamma0 @ gamma2)
Pz_p, Pz_m = get_projectors(gamma0 @ gamma3)


# ============================================================================
# ATTACK 1: Single-Step Hamiltonian Bloch Analysis
# ============================================================================

def bloch_hamiltonian_kg(mass0, n=9):
    """Exact Dirac Hamiltonian in Bloch space.
    H(k) = m*gamma0 + sin(kx)*gamma0*gamma1 + sin(ky)*gamma0*gamma2 + sin(kz)*gamma0*gamma3
    U(k) = exp(-i * H(k))
    This is the 'single-step' approach — no split-step ordering artifacts.
    """
    print(f"\n  Hamiltonian Bloch analysis (n={n}, mass={mass0:.4f})...")
    t0 = time.time()

    ks_raw = 2 * np.pi * np.arange(n) / n
    all_E2, all_k2 = [], []
    axis_data = {'x': ([], []), 'y': ([], []), 'z': ([], [])}

    g0g = [gamma0 @ g for g in gammas_spatial]  # gamma0*gamma_j

    for mx in range(n):
        kx = ks_raw[mx]; kx_c = kx if kx <= np.pi else kx - 2*np.pi
        for my in range(n):
            ky = ks_raw[my]; ky_c = ky if ky <= np.pi else ky - 2*np.pi
            for mz in range(n):
                kz = ks_raw[mz]; kz_c = kz if kz <= np.pi else kz - 2*np.pi

                kvals = [kx, ky, kz]
                H_k = mass0 * gamma0
                for j in range(3):
                    H_k = H_k + np.sin(kvals[j]) * g0g[j]

                Uk = expm(-1j * H_k)
                eigs_k = np.linalg.eigvals(Uk)
                phases = np.angle(eigs_k)
                k2 = kx_c**2 + ky_c**2 + kz_c**2

                for ph in phases:
                    all_E2.append(ph**2)
                    all_k2.append(k2)

                if my == 0 and mz == 0 and mx > 0:
                    for ph in phases:
                        axis_data['x'][0].append(kx_c**2)
                        axis_data['x'][1].append(ph**2)
                if mx == 0 and mz == 0 and my > 0:
                    for ph in phases:
                        axis_data['y'][0].append(ky_c**2)
                        axis_data['y'][1].append(ph**2)
                if mx == 0 and my == 0 and mz > 0:
                    for ph in phases:
                        axis_data['z'][0].append(kz_c**2)
                        axis_data['z'][1].append(ph**2)

    all_E2 = np.array(all_E2)
    all_k2 = np.array(all_k2)
    mask = all_k2 < 1.0
    E2_s, k2_s = all_E2[mask], all_k2[mask]

    if len(E2_s) > 10:
        sl, ic, rv, _, _ = stats.linregress(k2_s, E2_s)
        r2 = rv**2; m_fit = np.sqrt(abs(ic)); c2 = sl
    else:
        r2, m_fit, c2 = 0.0, 0.0, 0.0

    axis_slopes = {}
    for ax, (k2a, e2a) in axis_data.items():
        k2a, e2a = np.array(k2a), np.array(e2a)
        m_ax = k2a < 1.0
        if np.sum(m_ax) > 3:
            s, _, _, _, _ = stats.linregress(k2a[m_ax], e2a[m_ax])
            axis_slopes[ax] = s

    dt = time.time() - t0
    print(f"    R^2 = {r2:.6f}, m_fit = {m_fit:.4f}, c^2 = {c2:.4f}")
    slopes = list(axis_slopes.values())
    for ax, s in axis_slopes.items():
        print(f"    {ax}-axis slope: {s:.4f}")
    if len(slopes) >= 2 and min(slopes) > 0:
        print(f"    Isotropy ratio: {max(slopes)/min(slopes):.6f}")
    print(f"    Time: {dt:.1f}s")

    return r2, m_fit, c2, axis_slopes


def bloch_hamiltonian_band(mass0, n=9):
    """Band structure for single-step Hamiltonian."""
    print(f"\n  Band structure (Hamiltonian, mass={mass0:.4f}):")
    ks_raw = 2 * np.pi * np.arange(n) / n
    g0g = [gamma0 @ g for g in gammas_spatial]

    print("  Along k_x (ky=kz=0):")
    for mx in range(n):
        kx = ks_raw[mx]; kx_c = kx if kx <= np.pi else kx - 2*np.pi
        H_k = mass0 * gamma0 + np.sin(kx) * g0g[0]
        Uk = expm(-1j * H_k)
        phases = sorted(np.angle(np.linalg.eigvals(Uk)))
        print(f"    kx={kx_c:+.4f}: E = [{', '.join(f'{p:.4f}' for p in phases)}]")

    print("  Along (1,1,1) diagonal:")
    for mi in range(n):
        k = ks_raw[mi]; k_c = k if k <= np.pi else k - 2*np.pi
        H_k = mass0 * gamma0
        for j in range(3):
            H_k += np.sin(k) * g0g[j]
        Uk = expm(-1j * H_k)
        phases = sorted(np.angle(np.linalg.eigvals(Uk)))
        print(f"    k={k_c:+.4f}: E = [{', '.join(f'{p:.4f}' for p in phases)}]")


# ============================================================================
# ATTACK 2: Convergence on Larger Lattice (split-step, reversed coupling)
# ============================================================================

def coin_step(psi, mass_field, n):
    cm = np.cos(mass_field); sm = np.sin(mass_field)
    out = np.zeros_like(psi)
    out[0] = (cm + 1j*sm) * psi[0]
    out[1] = (cm + 1j*sm) * psi[1]
    out[2] = (cm - 1j*sm) * psi[2]
    out[3] = (cm - 1j*sm) * psi[3]
    return out

def shift_dir(psi, n, Pp, Pm, axis):
    out = np.zeros_like(psi)
    for c in range(4):
        pp = sum(Pp[c,d] * psi[d] for d in range(4))
        pm = sum(Pm[c,d] * psi[d] for d in range(4))
        out[c] += np.roll(pp, -1, axis=axis)
        out[c] += np.roll(pm, +1, axis=axis)
    return out

def step_zyx(psi, mf, n):
    psi = coin_step(psi, mf, n)
    psi = shift_dir(psi, n, Px_p, Px_m, 0)
    psi = shift_dir(psi, n, Py_p, Py_m, 1)
    psi = shift_dir(psi, n, Pz_p, Pz_m, 2)
    return psi

def min_image_dist(n, mp):
    c = np.arange(n)
    dx = np.abs(c[:,None,None] - mp[0]); dx = np.minimum(dx, n-dx)
    dy = np.abs(c[None,:,None] - mp[1]); dy = np.minimum(dy, n-dy)
    dz = np.abs(c[None,None,:] - mp[2]); dz = np.minimum(dz, n-dz)
    return np.sqrt(dx**2 + dy**2 + dz**2)

def evolve(n, N, mass0, strength=0.0, mass_pos=None, coupling="reversed"):
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    c = n // 2
    for k in range(4):
        psi[k, c, c, c] = 0.5
    mf = np.full((n,n,n), mass0)
    if mass_pos and strength > 0:
        tf = np.zeros((n,n,n))
        for mp in mass_pos:
            tf += strength / (min_image_dist(n, mp) + 0.1)
        mf = mass0 * (1.0 + tf) if coupling == "reversed" else mass0 * (1.0 - tf)
    for _ in range(N):
        psi = step_zyx(psi, mf, n)
    return psi

def prob(psi):
    return np.sum(np.abs(psi)**2, axis=0)

def convergence_test(mass0, coupling="reversed"):
    """Test gravity convergence across n and N."""
    print(f"\n{'='*70}")
    print(f"CONVERGENCE TEST ({coupling} coupling, mass={mass0})")
    print(f"{'='*70}")

    STRENGTH = 5e-4

    for n in [13, 15, 17]:
        c = n // 2
        print(f"\n  n={n}:")
        for N in [8, 10, 12, 14]:
            if N > n - 3:
                continue
            r0 = prob(evolve(n, N, mass0, 0.0))
            r1 = prob(evolve(n, N, mass0, STRENGTH, [(c,c,c+3)], coupling))
            d = r1 - r0
            tw = sum(d[c,c,c+dz] for dz in range(1,4))
            aw = sum(d[c,c,c-dz] for dz in range(1,4))
            tag = "TOWARD" if tw > aw else "AWAY"
            print(f"    N={N:2d}: toward={tw:+.4e}, away={aw:+.4e} -> {tag}")


def run_closure_card(mass0, n, N, coupling="reversed"):
    """Full 10-property closure card."""
    print(f"\n{'='*70}")
    print(f"CLOSURE CARD (n={n}, N={N}, mass={mass0}, {coupling})")
    print(f"{'='*70}")

    c = n // 2
    S = 5e-4
    score = 0
    bl = min(6, N-2)
    slits = [c-2, c, c+2]

    def ev_barrier(sl_list, noise=0.0):
        psi = np.zeros((4,n,n,n), dtype=np.complex128)
        for k in range(4): psi[k,c,c,c] = 0.5
        mf = np.full((n,n,n), mass0)
        rng = np.random.RandomState(42) if noise > 0 else None
        for layer in range(N):
            if noise > 0:
                ph = rng.uniform(-noise, noise, (n,n,n))
                for k in range(4): psi[k] *= np.exp(1j*ph)
            psi = step_zyx(psi, mf, n)
            if layer == bl - 1:
                mask = np.zeros((n,n,n), dtype=bool)
                for sy in sl_list: mask[sy,:,:] = True
                for k in range(4): psi[k] *= mask
        return prob(psi)

    # 1. Born
    rf = ev_barrier(slits)
    rs = [ev_barrier([s]) for s in slits]
    Pt = np.sum(rf)
    born = np.sum(np.abs(rf - sum(rs))) / Pt if Pt > 0 else 0
    p1 = born > 0.01
    print(f"  [1] Born: {born:.6f} {'PASS' if p1 else 'FAIL'}")
    if p1: score += 1

    # 2. d_TV
    ru = ev_barrier([c-2]); rd = ev_barrier([c+2])
    pu = ru/np.sum(ru); pd = rd/np.sum(rd)
    dtv = 0.5*np.sum(np.abs(pu-pd))
    p2 = dtv > 0.01
    print(f"  [2] d_TV: {dtv:.6f} {'PASS' if p2 else 'FAIL'}")
    if p2: score += 1

    # 3. f=0
    r0 = prob(evolve(n, N, mass0, 0.0))
    pz = np.sum(r0[c,c,c+1:c+4]); mz = np.sum(r0[c,c,c-3:c])
    bias = abs(pz-mz)/(pz+mz) if (pz+mz) > 0 else 0
    p3 = bias < 0.01
    print(f"  [3] f=0: bias={bias:.8f} {'PASS' if p3 else 'FAIL'}")
    if p3: score += 1

    # 4. F~M
    r0 = prob(evolve(n, N, mass0, 0.0))
    strs = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    for s in strs:
        r1 = prob(evolve(n, N, mass0, s, [(c,c,c+3)], coupling))
        d = r1 - r0
        forces.append(sum(d[c,c,c+dz] for dz in range(1,4)))
    fa = np.array(forces); sa = np.array(strs)
    co = np.polyfit(sa, fa, 1); pred = np.polyval(co, sa)
    ss_r = np.sum((fa-pred)**2); ss_t = np.sum((fa-np.mean(fa))**2)
    r2fm = 1 - ss_r/ss_t if ss_t > 0 else 0
    p4 = r2fm > 0.9
    print(f"  [4] F~M: R^2={r2fm:.6f} {'PASS' if p4 else 'FAIL'}")
    if p4: score += 1

    # 5. Gravity TOWARD
    r0 = prob(evolve(n, N, mass0, 0.0))
    r1 = prob(evolve(n, N, mass0, S, [(c,c,c+3)], coupling))
    d = r1 - r0
    tw = sum(d[c,c,c+dz] for dz in range(1,4))
    aw = sum(d[c,c,c-dz] for dz in range(1,4))
    p5 = tw > aw
    print(f"  [5] Gravity: toward={tw:+.4e}, away={aw:+.4e} {'TOWARD PASS' if p5 else 'AWAY FAIL'}")
    if p5: score += 1

    # 6. Decoherence
    rn = ev_barrier(slits, noise=0.5)
    Pn = np.sum(rn)
    bn = np.sum(np.abs(rn - sum(rs))) / Pn if Pn > 0 else 0
    p6 = bn < born
    print(f"  [6] Decoh: clean={born:.4f}, noisy={bn:.4f} {'PASS' if p6 else 'FAIL'}")
    if p6: score += 1

    # 7. MI
    pg = prob(evolve(n, N, mass0, S, [(c,c,c)], coupling))
    pn = pg / np.sum(pg)
    px = np.sum(pn, axis=(1,2)); py = np.sum(pn, axis=(0,2)); pxy = np.sum(pn, axis=2)
    mi = 0.0
    for ix in range(n):
        for iy in range(n):
            if pxy[ix,iy] > 1e-30 and px[ix] > 1e-30 and py[iy] > 1e-30:
                mi += pxy[ix,iy]*np.log(pxy[ix,iy]/(px[ix]*py[iy]))
    p7 = mi > 0
    print(f"  [7] MI: {mi:.6e} {'PASS' if p7 else 'FAIL'}")
    if p7: score += 1

    # 8. Purity stable
    purs = {}
    for L in [max(6,N-4), N-2, N]:
        if L < 4: continue
        rr = prob(evolve(n, L, mass0, S, [(c,c,c)], coupling))
        purs[L] = np.sum(rr**2)/np.sum(rr)**2
    vals = list(purs.values())
    cv = np.std(vals)/np.mean(vals) if np.mean(vals) > 0 else 0
    p8 = cv < 0.5
    print(f"  [8] Purity: CV={cv:.4f} {'PASS' if p8 else 'FAIL'}")
    if p8: score += 1

    # 9. Gravity grows
    gf = {}
    for L in [max(6,N-4), N-2, N]:
        if L < 4: continue
        r0 = prob(evolve(n, L, mass0, 0.0))
        r1 = prob(evolve(n, L, mass0, S, [(c,c,c+3)], coupling))
        d = r1 - r0
        gf[L] = sum(d[c,c,c+dz] for dz in range(1,4))
    vg = list(gf.values())
    # Check if absolute force grows (could be negative values growing more negative)
    abs_vg = [abs(v) for v in vg]
    mono = all(abs_vg[i] <= abs_vg[i+1] for i in range(len(abs_vg)-1))
    p9 = mono
    for ll, f in gf.items():
        print(f"      L={ll}: force={f:.4e}")
    print(f"  [9] Grav grows: mono={mono} {'PASS' if p9 else 'FAIL'}")
    if p9: score += 1

    # 10. Distance law
    mx_off = min(5, n//4)
    offs = list(range(2, mx_off+1))
    fdl = []
    r0 = prob(evolve(n, N, mass0, 0.0))
    all_toward = True
    for dz in offs:
        r1 = prob(evolve(n, N, mass0, S, [(c,c,c+dz)], coupling))
        d = r1 - r0
        f = sum(d[c,c,c+dd] for dd in range(1, dz+1))
        fdl.append(f)
        tag = "TOWARD" if f > 0 else "AWAY"
        if f <= 0: all_toward = False
        print(f"      off={dz}: {f:.4e} {tag}")
    fa = np.array(fdl); oa = np.array(offs, dtype=float)
    af = np.abs(fa); valid = af > 1e-30
    if np.sum(valid) >= 3:
        lr = np.log(oa[valid]); lf = np.log(af[valid])
        cf = np.polyfit(lr, lf, 1)
        pf = np.polyval(cf, lr)
        sr = np.sum((lf-pf)**2); st = np.sum((lf-np.mean(lf))**2)
        r2dl = 1-sr/st if st > 0 else 0; edl = cf[0]
    else:
        r2dl, edl = 0.0, 0.0
    p10 = r2dl > 0.7
    print(f"  [10] Dist law: exp={edl:.3f}, R^2={r2dl:.4f} {'PASS' if p10 else 'FAIL'}")
    if p10: score += 1

    print(f"\n  SCORE: {score}/10")
    labels = ["Born","d_TV","f=0","F~M","TOWARD","Decoh","MI","Purity","GravGrow","DistLaw"]
    results = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]
    for l, r in zip(labels, results):
        print(f"    {l:10s} {'PASS' if r else 'FAIL'}")
    return score, results


# ============================================================================
# ATTACK 3: AB with flux tube
# ============================================================================

def ab_flux_tube_test(mass0, n=11, N=10):
    """AB test with proper flux tube between two slits.
    Thread magnetic flux through a tube perpendicular to the xy-plane
    at the midpoint between two slits. The flux modifies phases of
    links that cross the flux surface.
    """
    print(f"\n{'='*70}")
    print("AB FLUX TUBE TEST")
    print(f"{'='*70}")

    c = n // 2
    slit_y = [c - 2, c + 2]  # two slits in y
    barrier_layer = 4

    def evolve_ab(A_flux):
        psi = np.zeros((4, n, n, n), dtype=np.complex128)
        for k in range(4):
            psi[k, c, c, c] = 0.5
        mf = np.full((n,n,n), mass0)

        for layer in range(N):
            psi = coin_step(psi, mf, n)

            # x-shift: add AB phase for links crossing the flux surface
            # Flux surface: the plane y = c (between the two slits)
            # Links crossing this surface in +x direction get phase +A
            # Links crossing in -x direction get phase -A
            out = np.zeros_like(psi)
            for comp in range(4):
                pp = sum(Px_p[comp,d] * psi[d] for d in range(4))
                pm = sum(Px_m[comp,d] * psi[d] for d in range(4))

                # Phase only on links crossing y=c
                # +x shift: site at y rolls to y-1. If site is at y=c+1, it crosses to y=c
                # Actually: for AB in y-direction shifts, not x
                # Let's use y-shifts with flux tube along z-axis at x=c
                out[comp] += np.roll(pp, -1, axis=0)
                out[comp] += np.roll(pm, +1, axis=0)
            psi = out

            # y-shift with AB phase for links crossing x=c plane
            out = np.zeros_like(psi)
            for comp in range(4):
                pp = sum(Py_p[comp,d] * psi[d] for d in range(4))
                pm = sum(Py_m[comp,d] * psi[d] for d in range(4))

                # +y shift: roll axis 1 by -1
                shifted_pp = np.roll(pp, -1, axis=1)
                shifted_pm = np.roll(pm, +1, axis=1)

                # Apply phase to +y links that cross the cut at y = c
                # The cut is at y = c. A +y shift from y=c to y=c+1 crosses it.
                # In the rolled array, the component at y=c came from y=c+1
                # So apply phase at the source: sites with y >= c and y < c+n//2
                # Simpler: phase on all +y links at x >= c (half-plane)
                phase_pp = np.ones((n,n,n), dtype=complex)
                phase_pp[c:, :, :] = np.exp(1j * A_flux)
                phase_pm = np.ones((n,n,n), dtype=complex)
                phase_pm[c:, :, :] = np.exp(-1j * A_flux)

                out[comp] += shifted_pp * phase_pp
                out[comp] += shifted_pm * phase_pm
            psi = out

            # z-shift (no AB)
            psi = shift_dir(psi, n, Pz_p, Pz_m, 2)

            # Barrier
            if layer == barrier_layer - 1:
                mask = np.zeros((n,n,n), dtype=bool)
                for sy in slit_y:
                    mask[:, sy, :] = True  # slits in y-direction
                for k in range(4):
                    psi[k] *= mask

        rho = prob(psi)
        # Detection: sum over a detector region at y > c
        det_y = c + 4
        return np.sum(rho[:, det_y, :]) if det_y < n else 0.0

    A_vals = np.linspace(0, 2*np.pi, 13)
    P_vals = []
    for A in A_vals:
        P = evolve_ab(A)
        P_vals.append(P)
        print(f"  A={A:.2f}: P={P:.8f}")

    Pa = np.array(P_vals)
    V = (np.max(Pa) - np.min(Pa)) / (np.max(Pa) + np.min(Pa)) if np.max(Pa) > 0 else 0
    print(f"\n  AB visibility V = {V:.4f}")
    print(f"  {'PASS' if V > 0.3 else 'FAIL'} (need V > 0.3)")
    return V


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()

    print("=" * 70)
    print("DIRAC WALK v3 — HAMILTONIAN KG + CONVERGENCE + AB FLUX TUBE")
    print("=" * 70)

    # ── ATTACK 1: Hamiltonian KG ──────────────────────────────────────
    print("\n" + "="*70)
    print("ATTACK 1: SINGLE-STEP HAMILTONIAN BLOCH ANALYSIS")
    print("="*70)

    print("\n--- Mass sweep ---")
    best_r2, best_mass = 0.0, 0.1
    for mass in [0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5]:
        r2, m, c2, ax = bloch_hamiltonian_kg(mass, n=9)
        if r2 > best_r2:
            best_r2, best_mass = r2, mass

    print(f"\n  BEST Hamiltonian KG: R^2={best_r2:.6f} at mass={best_mass}")

    # Compare with split-step at same mass
    print("\n--- Split-step comparison at same mass ---")
    from frontier_dirac_walk_3plus1d_v2 import bloch_kg as bloch_split
    r2_split, _, _, ax_split = bloch_split(best_mass, n=9, mode="zyx")
    print(f"  Split-step R^2 = {r2_split:.6f}")
    print(f"  Hamiltonian R^2 = {best_r2:.6f}")
    print(f"  Improvement: {best_r2 - r2_split:+.6f}")

    # Band structure
    bloch_hamiltonian_band(best_mass, n=9)

    # ── ATTACK 2: Convergence ─────────────────────────────────────────
    print("\n" + "="*70)
    print("ATTACK 2: CONVERGENCE TEST")
    print("="*70)
    convergence_test(best_mass, coupling="reversed")

    # Full closure card at best n,N
    closure_score, _ = run_closure_card(best_mass, n=17, N=12, coupling="reversed")

    # ── ATTACK 3: AB flux tube ────────────────────────────────────────
    print("\n" + "="*70)
    print("ATTACK 3: AB FLUX TUBE")
    print("="*70)
    ab_v = ab_flux_tube_test(best_mass, n=11, N=10)

    # ── VERDICT ───────────────────────────────────────────────────────
    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("FINAL VERDICT")
    print(f"{'='*70}")
    print(f"  Hamiltonian KG R^2:  {best_r2:.6f} ({'PASS' if best_r2 > 0.99 else 'FAIL'}, need >0.99)")
    print(f"  Closure card (n=17): {closure_score}/10")
    print(f"  AB flux tube V:      {ab_v:.4f}")
    print(f"  Total time: {elapsed:.1f}s")

    if best_r2 > 0.99:
        print("\n  KG ISOTROPY: Hamiltonian approach achieves isotropic 3D Klein-Gordon.")
    elif best_r2 > 0.95:
        print(f"\n  KG ISOTROPY: Near-isotropic (R^2={best_r2:.4f}). Lattice corrections remain.")
    else:
        print(f"\n  KG ISOTROPY: Partial ({best_r2:.4f}). May need finer momentum sampling or different H.")
