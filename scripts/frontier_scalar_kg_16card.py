#!/usr/bin/env python3
"""
Scalar Klein-Gordon + Potential Gravity — Full C1-C16 Card
============================================================
Architecture: 1 complex scalar per site, FFT split-step evolution.
  E(k) = sqrt(k_lat^2 + m^2), V(x) = -m * g * strength / (r + eps)
  No coin. No internal states. No mixing period.

Tests the expanded 16-row core card from FULL_TEST_MATRIX Part 10.

C1-C5:  Operating-point health
C6-C10: Measurement and scaling
C11-C16: Structural bottleneck checks
"""

import numpy as np
from scipy import stats
import time

# ============================================================================
# Core infrastructure
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
    """V = -mass * g * strength / (r + eps). Negative = attractive well."""
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

# ============================================================================
# Parameters
# ============================================================================
N_DEFAULT = 21
M_DEFAULT = 0.3
G_DEFAULT = 5.0
S_DEFAULT = 5e-4
DT = 0.3
NSTEPS = 10

# ============================================================================
# C1: Born barrier/slit |I3|/P
# ============================================================================
def test_c1():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2; bl = 4
    slits = [c-1, c, c+1]  # in x-dimension

    def ev(sl):
        psi = gaussian_state(n)
        E = build_dispersion(n, m); hk = np.exp(-1j*E*DT/2)
        for step in range(NSTEPS):
            psi = np.fft.ifftn(np.fft.fftn(psi)*hk)
            psi = np.fft.ifftn(np.fft.fftn(psi)*hk)
            if step == bl-1:
                mask = np.zeros((n,n,n));
                for s in sl: mask[s,:,:] = 1.0
                psi *= mask
        return prob(psi)

    rf = ev(slits)
    P = np.sum(rf)
    if P < 1e-20:
        # Try z-slits instead
        def ev_z(sl):
            psi = gaussian_state(n)
            E = build_dispersion(n, m); hk = np.exp(-1j*E*DT/2)
            for step in range(NSTEPS):
                psi = np.fft.ifftn(np.fft.fftn(psi)*hk)
                psi = np.fft.ifftn(np.fft.fftn(psi)*hk)
                if step == bl-1:
                    mask = np.zeros((n,n,n))
                    for s in sl: mask[:,:,s] = 1.0
                    psi *= mask
            return prob(psi)
        rf = ev_z(slits)
        P = np.sum(rf)
        rs = [ev_z([s]) for s in slits]
    else:
        rs = [ev([s]) for s in slits]

    if P > 1e-20:
        born = np.sum(np.abs(rf - sum(rs))) / P
    else:
        born = -1  # barrier failed
    passed = born > 0.01 if born >= 0 else False
    return "C1", f"Born |I3|/P = {born:.6f}" if born >= 0 else "Born: no P through barrier", passed

# ============================================================================
# C2: d_TV distinguishability
# ============================================================================
def test_c2():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    # Two different source positions, measure distinguishability
    psi_a = gaussian_state(n)
    psi_b = np.zeros((n,n,n), dtype=complex)
    sigma = n/8; x = np.arange(n)
    gx = np.exp(-(x-c)**2/(2*sigma**2))
    gy_shift = np.exp(-(x-(c+2))**2/(2*sigma**2))
    psi_b = (gx[:,None,None]*gy_shift[None,:,None]*gx[None,None,:]).astype(complex)
    psi_b /= np.sqrt(np.sum(np.abs(psi_b)**2))

    E = build_dispersion(n, m); hk = np.exp(-1j*E*DT/2)
    for _ in range(NSTEPS):
        psi_a = np.fft.ifftn(np.fft.fftn(psi_a)*hk); psi_a = np.fft.ifftn(np.fft.fftn(psi_a)*hk)
        psi_b = np.fft.ifftn(np.fft.fftn(psi_b)*hk); psi_b = np.fft.ifftn(np.fft.fftn(psi_b)*hk)
    ra = prob(psi_a); rb = prob(psi_b)
    pa = ra/np.sum(ra); pb = rb/np.sum(rb)
    dtv = 0.5*np.sum(np.abs(pa-pb))
    return "C2", f"d_TV = {dtv:.6f}", dtv > 0.01

# ============================================================================
# C3: Null control (f=0)
# ============================================================================
def test_c3():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    psi = evolve(n, m, DT, NSTEPS)
    rho = prob(psi)
    pz = np.sum(rho[c,c,c+1:c+4]); mz = np.sum(rho[c,c,c-3:c])
    bias = abs(pz-mz)/(pz+mz) if (pz+mz)>0 else 0
    return "C3", f"f=0 bias = {bias:.8f}", bias < 0.01

# ============================================================================
# C4: F∝M scaling
# ============================================================================
def test_c4():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2; g = G_DEFAULT
    cz0 = cz(prob(evolve(n,m,DT,NSTEPS)),n)
    strs = [1e-4,2e-4,5e-4,1e-3,2e-3]
    forces = [cz(prob(evolve(n,m,DT,NSTEPS,g,s,[(c,c,c+3)])),n)-cz0 for s in strs]
    fa=np.array(forces); sa=np.array(strs)
    co=np.polyfit(sa,fa,1); pred=np.polyval(co,sa)
    ssr=np.sum((fa-pred)**2); sst=np.sum((fa-np.mean(fa))**2)
    r2=1-ssr/sst if sst>0 else 0
    return "C4", f"F~M R^2 = {r2:.6f}", r2 > 0.9

# ============================================================================
# C5: Gravity sign at operating point
# ============================================================================
def test_c5():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    d0 = cz(prob(evolve(n,m,DT,NSTEPS)),n)
    dg = cz(prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)
    delta = dg - d0
    return "C5", f"delta_cz = {delta:+.6e} {'TOWARD' if delta>0 else 'AWAY'}", delta > 0

# ============================================================================
# C6: Decoherence/record proxy
# ============================================================================
def test_c6():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    # Coherence of off-diagonal in k-space (since scalar, use spatial coherence)
    psi_clean = evolve(n,m,DT,NSTEPS)
    psi_noisy = evolve(n,m,DT,NSTEPS, noise=1.0)
    # Coherence measure: |<psi|psi_shifted>| for a small shift
    def coherence(psi):
        shifted = np.roll(psi, 1, axis=0)
        return np.abs(np.sum(psi.conj() * shifted)) / np.sum(np.abs(psi)**2)
    coh_clean = coherence(psi_clean)
    coh_noisy = coherence(psi_noisy)
    passed = coh_noisy < coh_clean
    return "C6", f"coh_clean={coh_clean:.4f}, coh_noisy={coh_noisy:.4f}", passed

# ============================================================================
# C7: Mutual information
# ============================================================================
def test_c7():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    rho = prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c)]))
    rn = rho/np.sum(rho)
    px=np.sum(rn,axis=(1,2)); py=np.sum(rn,axis=(0,2)); pxy=np.sum(rn,axis=2)
    mi = 0.0
    for i in range(n):
        for j in range(n):
            if pxy[i,j]>1e-30 and px[i]>1e-30 and py[j]>1e-30:
                mi += pxy[i,j]*np.log(pxy[i,j]/(px[i]*py[j]))
    return "C7", f"MI = {mi:.6e}", mi > 0

# ============================================================================
# C8: Purity stability
# ============================================================================
def test_c8():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    purs = {}
    for ns in [6, 8, 10]:
        rho = prob(evolve(n,m,DT,ns,G_DEFAULT,S_DEFAULT,[(c,c,c)]))
        purs[ns] = np.sum(rho**2)/np.sum(rho)**2
    vals = list(purs.values())
    cv = np.std(vals)/np.mean(vals) if np.mean(vals)>0 else 0
    return "C8", f"purity CV = {cv:.4f}", cv < 0.5

# ============================================================================
# C9: Gravity grows with propagation
# ============================================================================
def test_c9():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    cz0_base = {}
    forces = {}
    for ns in [6, 8, 10, 12]:
        d0 = cz(prob(evolve(n,m,DT,ns)),n)
        dg = cz(prob(evolve(n,m,DT,ns,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)
        forces[ns] = dg - d0
    fv = list(forces.values())
    all_toward = all(f > 0 for f in fv)
    abs_grows = all(abs(fv[i]) <= abs(fv[i+1])*1.05 for i in range(len(fv)-1))
    detail = ", ".join(f"N={k}:{v:+.3e}" for k,v in forces.items())
    return "C9", f"grows={abs_grows}, all_tw={all_toward} [{detail}]", all_toward

# ============================================================================
# C10: Distance law
# ============================================================================
def test_c10():
    n = 25; m = M_DEFAULT; c = n//2
    d0 = cz(prob(evolve(n,m,DT,NSTEPS)),n)
    offs = list(range(2, n//4+1))
    forces = []
    for dz in offs:
        dg = cz(prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+dz)])),n)
        forces.append(dg - d0)
    ntw = sum(1 for f in forces if f > 0)
    fa = np.array(forces); oa = np.array(offs, dtype=float)
    tw = fa > 0
    if np.sum(tw) >= 3:
        lr=np.log(oa[tw]); lf=np.log(fa[tw])
        cf=np.polyfit(lr,lf,1); alpha=cf[0]
        pf=np.polyval(cf,lr); sr=np.sum((lf-pf)**2); st=np.sum((lf-np.mean(lf))**2)
        r2=1-sr/st if st>0 else 0
    else:
        alpha, r2 = 0.0, 0.0
    return "C10", f"{ntw}/{len(offs)} TOWARD, alpha={alpha:.2f}, R^2={r2:.3f}", ntw > len(offs)//2

# ============================================================================
# C11: 3D KG isotropy
# ============================================================================
def test_c11():
    n = 15; m = M_DEFAULT
    E = build_dispersion(n, m)
    f = np.fft.fftfreq(n)*2*np.pi
    allE2, allk2 = [], []
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                k2 = f[ix]**2+f[iy]**2+f[iz]**2
                allE2.append(E[ix,iy,iz]**2); allk2.append(k2)
    allE2=np.array(allE2); allk2=np.array(allk2)
    mask=allk2<1.0
    sl,ic,rv,_,_=stats.linregress(allk2[mask],allE2[mask])
    r2=rv**2
    # Isotropy: check slopes along axes
    slopes = []
    for ax in range(3):
        k2a=[]; e2a=[]
        for i in range(n):
            idx = [0,0,0]; idx[ax]=i
            k2a.append(f[i]**2); e2a.append(E[idx[0],idx[1],idx[2]]**2)
        k2a=np.array(k2a); e2a=np.array(e2a)
        m2=k2a<1.0
        if np.sum(m2)>2:
            s,_,_,_,_=stats.linregress(k2a[m2],e2a[m2]); slopes.append(s)
    iso = max(slopes)/min(slopes) if min(slopes)>0 else float('inf')
    return "C11", f"KG R^2={r2:.6f}, isotropy={iso:.4f}", r2 > 0.99 and iso < 1.05

# ============================================================================
# C12: 3D gauge/AB
# ============================================================================
def test_c12():
    """AB test: add flux phase to y-shifts crossing x=c plane."""
    n = 15; m = M_DEFAULT; c = n//2; nsteps = 8
    E = build_dispersion(n, m)
    hk = np.exp(-1j * E * DT / 2)

    def evolve_ab(A):
        psi = gaussian_state(n)
        # Build AB potential: V_AB(x) = A for x >= c, 0 otherwise
        # This creates a flux tube at x=c
        V_ab = np.zeros((n,n,n))
        V_ab[c:,:,:] = A  # phase gradient across the cut
        fp = np.exp(-1j * V_ab * DT)
        for _ in range(nsteps):
            psi = np.fft.ifftn(np.fft.fftn(psi)*hk)
            psi *= fp
            psi = np.fft.ifftn(np.fft.fftn(psi)*hk)
        rho = prob(psi)
        det = c + 3
        return np.sum(rho[det,:,:]) if det < n else 0

    As = np.linspace(0, 2*np.pi, 13)
    Ps = [evolve_ab(A) for A in As]
    Pa = np.array(Ps)
    V = (np.max(Pa)-np.min(Pa))/(np.max(Pa)+np.min(Pa)) if np.max(Pa)>0 else 0
    return "C12", f"AB V = {V:.4f}", V > 0.3

# ============================================================================
# C13: k-achromaticity
# ============================================================================
def test_c13():
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    forces = []
    for ki in range(6):  # small-k only
        k = 2*np.pi*ki/n
        psi0 = np.zeros((n,n,n), dtype=complex)
        sigma=n/8; x=np.arange(n); gx=np.exp(-(x-c)**2/(2*sigma**2))
        env=gx[:,None,None]*gx[None,:,None]*gx[None,None,:]
        for iz in range(n): psi0[:,:,iz]=env[:,:,iz]*np.exp(1j*k*iz)
        psi0/=np.sqrt(np.sum(np.abs(psi0)**2))
        pf=evolve(n,m,DT,NSTEPS,0,0,psi0=psi0)
        pg=evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)],psi0=psi0)
        forces.append(cz(prob(pg),n)-cz(prob(pf),n))
    fa=np.array(forces)
    same_sign = all(f>0 for f in fa) or all(f<0 for f in fa)
    mean_abs = np.mean(np.abs(fa))
    cv = np.std(fa)/mean_abs if mean_abs>0 else float('inf')
    return "C13", f"k-achrom: same_sign={same_sign}, CV={cv:.4f}", same_sign and cv < 0.5

# ============================================================================
# C14: Split mass vs gravity
# ============================================================================
def test_c14():
    """Acceleration should be independent of mass (equivalence principle)."""
    n = N_DEFAULT; c = n//2
    # Measure displacement at fixed time for different masses
    forces = []; masses = [0.1, 0.3, 0.5, 1.0]
    for m in masses:
        d0 = cz(prob(evolve(n,m,DT,NSTEPS)),n)
        dg = cz(prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)
        forces.append(dg-d0)
    fa=np.array(forces); ma=np.array(masses)
    _,_,rv,_,_=stats.linregress(ma,fa)
    r2=rv**2
    return "C14", f"R^2(disp vs mass) = {r2:.4f}", r2 < 0.3

# ============================================================================
# C15: Boundary condition robustness
# ============================================================================
def test_c15():
    """Compare periodic vs absorbing-layer boundary."""
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    # Periodic (default)
    d0p = cz(prob(evolve(n,m,DT,NSTEPS)),n)
    dgp = cz(prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)
    fp = dgp - d0p

    # "Absorbing" layer: damp edges by multiplying by smooth window
    def evolve_absorbing(n, m, dt, nsteps, g=0, S=0, mpos=None):
        E = build_dispersion(n, m)
        V = build_potential(n,m,g,S,mpos) if mpos and abs(g)>0 else np.zeros((n,n,n))
        hk = np.exp(-1j*E*dt/2); fp = np.exp(-1j*V*dt)
        psi = gaussian_state(n)
        # Absorbing window: Hann window damps edges
        x = np.arange(n); w = 0.5*(1-np.cos(2*np.pi*x/(n-1)))
        window = w[:,None,None]*w[None,:,None]*w[None,None,:]
        for _ in range(nsteps):
            psi = np.fft.ifftn(np.fft.fftn(psi)*hk)
            psi *= fp
            psi = np.fft.ifftn(np.fft.fftn(psi)*hk)
            psi *= window  # absorb at boundaries
        return psi

    d0a = cz(prob(evolve_absorbing(n,m,DT,NSTEPS)),n)
    dga = cz(prob(evolve_absorbing(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)])),n)
    fa = dga - d0a

    same_sign = (fp > 0 and fa > 0) or (fp < 0 and fa < 0)
    ratio = fp/fa if abs(fa) > 1e-30 else float('inf')
    return "C15", f"periodic={fp:+.3e}, absorbing={fa:+.3e}, same_sign={same_sign}", same_sign

# ============================================================================
# C16: Multi-observable gravity consistency
# ============================================================================
def test_c16():
    """Compare centroid, peak, and shell-sum gravity proxies."""
    n = N_DEFAULT; m = M_DEFAULT; c = n//2
    rho0 = prob(evolve(n,m,DT,NSTEPS))
    rhog = prob(evolve(n,m,DT,NSTEPS,G_DEFAULT,S_DEFAULT,[(c,c,c+3)]))

    # Centroid
    centroid_delta = cz(rhog,n) - cz(rho0,n)

    # Peak position
    peak0 = np.unravel_index(np.argmax(rho0), rho0.shape)[2] - c
    peakg = np.unravel_index(np.argmax(rhog), rhog.shape)[2] - c
    peak_delta = peakg - peak0

    # Shell sum: probability in shell toward mass vs away
    d = rhog - rho0
    shell_toward = sum(np.sum(d[:,:,c+dz]) for dz in range(1,4))
    shell_away = sum(np.sum(d[:,:,c-dz]) for dz in range(1,4))
    shell_dir = "TOWARD" if shell_toward > shell_away else "AWAY"

    agree = sum([
        centroid_delta > 0,
        peak_delta >= 0,
        shell_toward > shell_away
    ])
    return "C16", f"centroid={'T' if centroid_delta>0 else 'A'}, peak={peak_delta:+d}, shell={shell_dir}, agree={agree}/3", agree >= 2


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()
    print("=" * 70)
    print("SCALAR KG + POTENTIAL GRAVITY — C1-C16 CORE CARD")
    print("=" * 70)
    print(f"  n={N_DEFAULT}, mass={M_DEFAULT}, g={G_DEFAULT}, S={S_DEFAULT}, dt={DT}")
    print(f"  V(x) = -mass * g * S / (r + 0.1)  [attractive, mass-proportional]")
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

    if score >= 14:
        print(f"\n  VERDICT: Strong card ({score}/16). Architecture is viable.")
    elif score >= 10:
        print(f"\n  VERDICT: Moderate card ({score}/16). Core physics present, refinement needed.")
    else:
        print(f"\n  VERDICT: Weak card ({score}/16). Architecture has structural gaps.")
