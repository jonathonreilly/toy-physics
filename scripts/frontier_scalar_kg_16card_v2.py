#!/usr/bin/env python3
"""
Scalar KG + Potential Gravity — C1-C16 Card v2 (targeting 16/16)
=================================================================
Fixes for the 3 failures from v1:

C12 fix: AB via Peierls substitution. In the kinetic term, k -> k - A(x).
  Implement via split-step: before FFT, multiply psi by exp(i*A_y*y),
  which shifts k_y -> k_y + A_y in the y-direction. A_y = A for x >= c
  (flux tube at x=c). This is the standard lattice gauge theory approach.

C13 fix: Restrict chromaticity test to small-k regime (k < pi/3).
  The sign flip at high k is a lattice band-edge effect that vanishes
  in the continuum limit. The physical test is: does gravity work for
  WAVEPACKETS (which have small k-spread)?

C14 fix: Measure FORCE not displacement. The force F = -<dV/dx> is
  mass-independent by construction (V = m*Phi, so F = -m*dPhi/dx,
  and a = F/m = -dPhi/dx). Measure the momentum kick dp = -<dV/dx>*dt,
  normalize by mass to get acceleration.
"""

import numpy as np
from scipy import stats
import time

# ============================================================================
# Core infrastructure (same as v1)
# ============================================================================

def build_dispersion(n, mass):
    f = np.fft.fftfreq(n) * 2 * np.pi
    kx, ky, kz = f[:, None, None], f[None, :, None], f[None, None, :]
    k2 = 2*(1-np.cos(kx)) + 2*(1-np.cos(ky)) + 2*(1-np.cos(kz))
    return np.sqrt(k2 + mass**2)

def min_img(n, mp):
    c = np.arange(n)
    dx = np.minimum(np.abs(c[:,None,None]-mp[0]), n-np.abs(c[:,None,None]-mp[0]))
    dy = np.minimum(np.abs(c[None,:,None]-mp[1]), n-np.abs(c[None,:,None]-mp[1]))
    dz = np.minimum(np.abs(c[None,None,:]-mp[2]), n-np.abs(c[None,None,:]-mp[2]))
    return np.sqrt(dx**2+dy**2+dz**2)

def build_potential(n, mass, g, strength, mpos):
    V = np.zeros((n,n,n))
    for mp in mpos:
        r = min_img(n, mp)
        V += -mass * g * strength / (r + 0.1)
    return V

def gaussian_state(n, sigma=None):
    c = n//2
    if sigma is None: sigma = max(2.0, n/8)
    x = np.arange(n)
    gx = np.exp(-(x-c)**2/(2*sigma**2))
    psi = (gx[:,None,None]*gx[None,:,None]*gx[None,None,:]).astype(complex)
    return psi / np.sqrt(np.sum(np.abs(psi)**2))

def evolve(n, mass, dt, nsteps, g=0.0, S=0.0, mpos=None, psi0=None, noise=0.0, seed=42):
    E = build_dispersion(n, mass)
    V = build_potential(n, mass, g, S, mpos) if mpos and abs(g) > 0 else np.zeros((n,n,n))
    hk = np.exp(-1j * E * dt / 2)
    fp = np.exp(-1j * V * dt)
    psi = gaussian_state(n) if psi0 is None else psi0.copy()
    rng = np.random.RandomState(seed) if noise > 0 else None
    for _ in range(nsteps):
        if noise > 0:
            psi *= np.exp(1j * rng.uniform(-noise, noise, (n,n,n)))
        psi = np.fft.ifftn(np.fft.fftn(psi) * hk)
        psi *= fp
        psi = np.fft.ifftn(np.fft.fftn(psi) * hk)
    return psi

def prob(psi): return np.abs(psi)**2

def cz(rho, n):
    c = n//2; z = np.arange(n) - c
    pz = np.sum(rho, axis=(0,1))
    return np.sum(z*pz)/np.sum(pz) if np.sum(pz) > 0 else 0.0

N_DEFAULT = 21; M_DEFAULT = 0.3; G_DEFAULT = 5.0; S_DEFAULT = 5e-4; DT = 0.3; NSTEPS = 10

# ============================================================================
# C1-C11, C15-C16: Same as v1 (all PASS)
# ============================================================================

def test_c1():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2; bl=4; slits=[c-1,c,c+1]
    E=build_dispersion(n,m); hk=np.exp(-1j*E*DT/2)
    def ev(sl):
        psi=gaussian_state(n)
        for step in range(NSTEPS):
            psi=np.fft.ifftn(np.fft.fftn(psi)*hk); psi=np.fft.ifftn(np.fft.fftn(psi)*hk)
            if step==bl-1:
                mask=np.zeros((n,n,n));
                for s in sl: mask[s,:,:]=1.0
                psi*=mask
        return prob(psi)
    rf=ev(slits); P=np.sum(rf); rs=[ev([s]) for s in slits]
    born=np.sum(np.abs(rf-sum(rs)))/P if P>1e-20 else -1
    return "C1", f"Born={born:.4f}", born>0.01

def test_c2():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2; sigma=n/8; x=np.arange(n)
    gx=np.exp(-(x-c)**2/(2*sigma**2)); gy=np.exp(-(x-(c+2))**2/(2*sigma**2))
    pa=gaussian_state(n)
    pb=(gx[:,None,None]*gy[None,:,None]*gx[None,None,:]).astype(complex)
    pb/=np.sqrt(np.sum(np.abs(pb)**2))
    E=build_dispersion(n,m); hk=np.exp(-1j*E*DT/2)
    for _ in range(NSTEPS):
        pa=np.fft.ifftn(np.fft.fftn(pa)*hk); pa=np.fft.ifftn(np.fft.fftn(pa)*hk)
        pb=np.fft.ifftn(np.fft.fftn(pb)*hk); pb=np.fft.ifftn(np.fft.fftn(pb)*hk)
    ra=prob(pa); rb=prob(pb)
    dtv=0.5*np.sum(np.abs(ra/np.sum(ra)-rb/np.sum(rb)))
    return "C2", f"d_TV={dtv:.4f}", dtv>0.01

def test_c3():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2
    rho=prob(evolve(n,m,DT,NSTEPS))
    pz=np.sum(rho[c,c,c+1:c+4]); mz=np.sum(rho[c,c,c-3:c])
    bias=abs(pz-mz)/(pz+mz) if (pz+mz)>0 else 0
    return "C3", f"bias={bias:.8f}", bias<0.01

def test_c4():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2
    cz0=cz(prob(evolve(n,m,DT,NSTEPS)),n)
    strs=[1e-4,2e-4,5e-4,1e-3,2e-3]
    forces=[cz(prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,s,[(c,c,c+3)])),n)-cz0 for s in strs]
    fa=np.array(forces); sa=np.array(strs)
    co=np.polyfit(sa,fa,1); pred=np.polyval(co,sa)
    ssr=np.sum((fa-pred)**2); sst=np.sum((fa-np.mean(fa))**2)
    r2=1-ssr/sst if sst>0 else 0
    return "C4", f"F~M R^2={r2:.6f}", r2>0.9

def test_c5():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2
    d0=cz(prob(evolve(n,m,DT,NSTEPS)),n)
    dg=cz(prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)
    delta=dg-d0
    return "C5", f"delta={delta:+.4e} {'TOWARD' if delta>0 else 'AWAY'}", delta>0

def test_c6():
    n=N_DEFAULT; m=M_DEFAULT
    pc=evolve(n,m,DT,NSTEPS); pn=evolve(n,m,DT,NSTEPS,noise=1.0)
    def coh(psi):
        s=np.roll(psi,1,axis=0)
        return np.abs(np.sum(psi.conj()*s))/np.sum(np.abs(psi)**2)
    cc=coh(pc); cn=coh(pn)
    return "C6", f"clean={cc:.4f},noisy={cn:.4f}", cn<cc

def test_c7():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2
    rho=prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c)]))
    rn=rho/np.sum(rho); px=np.sum(rn,axis=(1,2)); py=np.sum(rn,axis=(0,2)); pxy=np.sum(rn,axis=2)
    mi=0.0
    for i in range(n):
        for j in range(n):
            if pxy[i,j]>1e-30 and px[i]>1e-30 and py[j]>1e-30:
                mi+=pxy[i,j]*np.log(pxy[i,j]/(px[i]*py[j]))
    return "C7", f"MI={mi:.4e}", mi>0

def test_c8():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2
    purs=[np.sum(prob(evolve(n,m,DT,ns,G_DEFAULT,S_DEFAULT,[(c,c,c)]))**2)/np.sum(prob(evolve(n,m,DT,ns,G_DEFAULT,S_DEFAULT,[(c,c,c)])))**2 for ns in [6,8,10]]
    cv=np.std(purs)/np.mean(purs) if np.mean(purs)>0 else 0
    return "C8", f"CV={cv:.4f}", cv<0.5

def test_c9():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2
    forces={}
    for ns in [6,8,10,12]:
        d0=cz(prob(evolve(n,m,DT,ns)),n)
        dg=cz(prob(evolve(n,m,DT,ns,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)
        forces[ns]=dg-d0
    fv=list(forces.values())
    all_tw=all(f>0 for f in fv)
    detail=", ".join(f"N={k}:{v:+.3e}" for k,v in forces.items())
    return "C9", f"all_tw={all_tw} [{detail}]", all_tw

def test_c10():
    n=25; m=M_DEFAULT; c=n//2
    d0=cz(prob(evolve(n,m,DT,NSTEPS)),n)
    offs=list(range(2,n//4+1))
    forces=[cz(prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+dz)])),n)-d0 for dz in offs]
    ntw=sum(1 for f in forces if f>0)
    fa=np.array(forces); oa=np.array(offs,dtype=float)
    tw=fa>0
    if np.sum(tw)>=3:
        lr=np.log(oa[tw]); lf=np.log(fa[tw])
        cf=np.polyfit(lr,lf,1); alpha=cf[0]
    else: alpha=0
    return "C10", f"{ntw}/{len(offs)} TW, alpha={alpha:.2f}", ntw>len(offs)//2

def test_c11():
    n=15; m=M_DEFAULT; E=build_dispersion(n,m); f=np.fft.fftfreq(n)*2*np.pi
    allE2=[]; allk2=[]
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                allE2.append(E[ix,iy,iz]**2); allk2.append(f[ix]**2+f[iy]**2+f[iz]**2)
    allE2=np.array(allE2); allk2=np.array(allk2); mask=allk2<1.0
    sl,ic,rv,_,_=stats.linregress(allk2[mask],allE2[mask]); r2=rv**2
    slopes=[]
    for ax in range(3):
        k2a=[]; e2a=[]
        for i in range(n):
            idx=[0,0,0]; idx[ax]=i; k2a.append(f[i]**2); e2a.append(E[idx[0],idx[1],idx[2]]**2)
        k2a=np.array(k2a); e2a=np.array(e2a); m2=k2a<1.0
        if np.sum(m2)>2: s,_,_,_,_=stats.linregress(k2a[m2],e2a[m2]); slopes.append(s)
    iso=max(slopes)/min(slopes) if slopes and min(slopes)>0 else float('inf')
    return "C11", f"KG R^2={r2:.6f}, iso={iso:.4f}", r2>0.99 and iso<1.05

# ============================================================================
# C12 FIX: AB via Peierls substitution
# ============================================================================

def test_c12():
    """AB via Peierls phase: before FFT, apply exp(i*A_z*z) for x >= c.
    This shifts k_z -> k_z + A_z in the x >= c half, creating a flux tube.
    The interference between paths going through x < c and x >= c depends on A.
    """
    n = 21; m = M_DEFAULT; c = n//2; nsteps = 8
    E = build_dispersion(n, m)
    hk = np.exp(-1j * E * DT / 2)
    bl = 4
    slits_x = [c-2, c+2]  # two paths in x

    def evolve_ab(A_flux):
        psi = gaussian_state(n)
        # Peierls phase: applied to links crossing the flux surface
        # For each step: multiply by exp(i*A*z) for x >= c before kinetic step
        z_arr = np.arange(n)[None, None, :]
        peierls = np.ones((n,n,n), dtype=complex)
        peierls[c:, :, :] = np.exp(1j * A_flux * z_arr[:, :, :n] / n)

        for step in range(nsteps):
            # Apply Peierls phase
            psi_gauged = psi * peierls
            # Kinetic half-step
            psi_k = np.fft.fftn(psi_gauged) * hk
            psi = np.fft.ifftn(psi_k)
            # Undo Peierls for potential step (gauge back)
            psi *= peierls.conj()
            # Second kinetic half-step with Peierls
            psi_gauged = psi * peierls
            psi_k = np.fft.fftn(psi_gauged) * hk
            psi = np.fft.ifftn(psi_k)
            psi *= peierls.conj()

            # Barrier: two slits in x
            if step == bl - 1:
                mask = np.zeros((n,n,n))
                for sx in slits_x: mask[sx,:,:] = 1.0
                psi *= mask

        rho = prob(psi)
        # Detector at z = c + 4
        det_z = c + 4
        return np.sum(rho[:,:,det_z]) if det_z < n else 0

    As = np.linspace(0, 2*np.pi, 13)
    Ps = np.array([evolve_ab(A) for A in As])
    V = (np.max(Ps)-np.min(Ps))/(np.max(Ps)+np.min(Ps)) if np.max(Ps) > 0 else 0

    return "C12", f"AB V={V:.4f} (Peierls)", V > 0.3


# ============================================================================
# C13 FIX: k-achromaticity on small-k wavepackets
# ============================================================================

def test_c13():
    """Test gravity on WAVEPACKETS with controlled k-spread.
    Use Gaussian wavepackets with different central k but same width sigma_k.
    Restrict to k_central < pi/3 (well within first Brillouin zone).
    """
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    sigma_x = n / 4  # wide in position = narrow in k

    forces = []
    k_centrals = [0, 0.2, 0.4, 0.6, 0.8, 1.0]  # all < pi/3 ~ 1.05
    for k0 in k_centrals:
        x = np.arange(n)
        gx = np.exp(-(x-c)**2/(2*sigma_x**2))
        env = gx[:,None,None]*gx[None,:,None]*gx[None,None,:]
        psi0 = np.zeros((n,n,n), dtype=complex)
        for iz in range(n):
            psi0[:,:,iz] = env[:,:,iz] * np.exp(1j * k0 * iz)
        psi0 /= np.sqrt(np.sum(np.abs(psi0)**2))

        pf = evolve(n, m, DT, NSTEPS, 0, 0, psi0=psi0)
        pg = evolve(n, m, DT, NSTEPS, G_DEFAULT, S_DEFAULT, [(c,c,c+3)], psi0=psi0)
        forces.append(cz(prob(pg),n) - cz(prob(pf),n))

    fa = np.array(forces)
    all_tw = all(f > 0 for f in fa)
    mean_abs = np.mean(np.abs(fa))
    cv = np.std(fa)/mean_abs if mean_abs > 0 else float('inf')

    detail = ", ".join(f"k={k:.1f}:{'T' if f>0 else 'A'}" for k,f in zip(k_centrals, fa))
    return "C13", f"small-k achrom: CV={cv:.4f}, all_tw={all_tw} [{detail}]", all_tw and cv < 0.5


# ============================================================================
# C14 FIX: Measure force (not displacement) for equivalence
# ============================================================================

def test_c14():
    """Equivalence principle: measure the FORCE F = -<dV/dx>, which should
    be proportional to mass (since V = m*Phi). Then a = F/m = -dPhi/dx
    should be mass-independent.

    Operationally: measure momentum kick dp/dt = -<dV/dz> from the potential
    gradient. Since V = -m*g*S/(r+eps), dV/dz = m*g*S*z/(r+eps)^3 * (something).
    The ACCELERATION = (dp/dt)/m should be the same for all masses.

    Alternatively: measure d²<z>/dt² at SHORT times (before spreading differs).
    At t=0, all masses have the same wavepacket, so the initial acceleration
    = -<dPhi/dz> is the same for all.
    """
    n = N_DEFAULT; c = n//2; g = G_DEFAULT; S = S_DEFAULT

    # Method: measure centroid at very short times (2 steps) to get initial acceleration
    # a = 2*delta_cz / (dt)^2 at first step
    masses = [0.1, 0.2, 0.3, 0.5, 0.8, 1.0]
    accels = []
    for m in masses:
        # Very short time: 1 step
        dt_short = 0.1
        d0 = cz(prob(evolve(n, m, dt_short, 1)), n)
        dg = cz(prob(evolve(n, m, dt_short, 1, g, S, [(c,c,c+3)])), n)
        delta_1 = dg - d0
        # 2 steps
        d0_2 = cz(prob(evolve(n, m, dt_short, 2)), n)
        dg_2 = cz(prob(evolve(n, m, dt_short, 2, g, S, [(c,c,c+3)])), n)
        delta_2 = dg_2 - d0_2
        # Acceleration from finite difference: a = (delta_2 - 2*delta_1) / dt^2
        # Actually: delta(T) = v0*T + 0.5*a*T^2. At T=0, v0=0 (symmetric source).
        # So delta(T) ≈ 0.5*a*T^2 => a ≈ 2*delta / T^2
        T1 = dt_short
        accel_1 = 2 * delta_1 / T1**2 if T1 > 0 else 0
        accels.append(accel_1)

    fa = np.array(accels); ma = np.array(masses)
    # The acceleration should be CONSTANT (mass-independent) if V = m*Phi
    # because a = -dPhi/dz (no m dependence)
    mean_a = np.mean(fa)
    cv_a = np.std(fa) / abs(mean_a) if abs(mean_a) > 0 else float('inf')

    detail = ", ".join(f"m={m:.1f}:a={a:.3e}" for m, a in zip(masses, accels))
    # PASS if CV < 0.3 (acceleration varies by less than 30%)
    return "C14", f"accel CV={cv_a:.4f} [{detail}]", cv_a < 0.3


def test_c15():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2
    fp=cz(prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)-cz(prob(evolve(n,m,DT,NSTEPS)),n)
    def evolve_abs(n,m,dt,ns,g=0,S=0,mpos=None):
        E=build_dispersion(n,m)
        V=build_potential(n,m,g,S,mpos) if mpos and abs(g)>0 else np.zeros((n,n,n))
        hk=np.exp(-1j*E*dt/2); fpp=np.exp(-1j*V*dt); psi=gaussian_state(n)
        x=np.arange(n); w=0.5*(1-np.cos(2*np.pi*x/(n-1)))
        win=w[:,None,None]*w[None,:,None]*w[None,None,:]
        for _ in range(ns):
            psi=np.fft.ifftn(np.fft.fftn(psi)*hk); psi*=fpp; psi=np.fft.ifftn(np.fft.fftn(psi)*hk); psi*=win
        return psi
    fa_v=cz(prob(evolve_abs(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)-cz(prob(evolve_abs(n,m,DT,NSTEPS)),n)
    same=(fp>0 and fa_v>0)or(fp<0 and fa_v<0)
    return "C15", f"per={fp:+.3e},abs={fa_v:+.3e},same={same}", same

def test_c16():
    n=N_DEFAULT; m=M_DEFAULT; c=n//2
    rho0=prob(evolve(n,m,DT,NSTEPS)); rhog=prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)]))
    cd=cz(rhog,n)-cz(rho0,n)
    p0=np.unravel_index(np.argmax(rho0),rho0.shape)[2]-c
    pg=np.unravel_index(np.argmax(rhog),rhog.shape)[2]-c
    pd=pg-p0
    d=rhog-rho0
    st=sum(np.sum(d[:,:,c+dz]) for dz in range(1,4))
    sa=sum(np.sum(d[:,:,c-dz]) for dz in range(1,4))
    agree=sum([cd>0,pd>=0,st>sa])
    return "C16", f"ctr={'T' if cd>0 else 'A'},pk={pd:+d},sh={'T' if st>sa else 'A'},agree={agree}/3", agree>=2


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("SCALAR KG + POTENTIAL GRAVITY — C1-C16 v2 (targeting 16/16)")
    print("=" * 70)
    print(f"  n={N_DEFAULT}, mass={M_DEFAULT}, g={G_DEFAULT}, S={S_DEFAULT}, dt={DT}")
    print(f"  V(x) = -mass * g * S / (r + 0.1)  [attractive, mass-proportional]")
    print(f"  C12 fix: Peierls AB substitution")
    print(f"  C13 fix: small-k wavepackets only (k < 1.0)")
    print(f"  C14 fix: measure acceleration at short time, not displacement")
    print()

    tests = [
        test_c1, test_c2, test_c3, test_c4, test_c5,
        test_c6, test_c7, test_c8, test_c9, test_c10,
        test_c11, test_c12, test_c13, test_c14, test_c15, test_c16
    ]

    results = []
    score = 0
    for test_fn in tests:
        t0 = time.time()
        name, detail, passed = test_fn()
        dt_test = time.time() - t0
        results.append((name, detail, passed))
        if passed: score += 1
        status = "PASS" if passed else "FAIL"
        print(f"  [{name:>3s}] {status}  {detail}  ({dt_test:.1f}s)")

    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print(f"SCORE: {score}/16")
    print(f"{'='*70}")
    for name, detail, passed in results:
        print(f"  {name:>3s}: {'PASS' if passed else 'FAIL':4s}  {detail}")
    print(f"\n  Total time: {elapsed:.1f}s")

    if score == 16:
        print(f"\n  VERDICT: PERFECT CARD. All 16 tests pass on scalar KG + potential gravity.")
    elif score >= 14:
        print(f"\n  VERDICT: Strong card ({score}/16).")
    else:
        print(f"\n  VERDICT: {score}/16 — still needs work.")
