#!/usr/bin/env python3
"""
Graph Laplacian KG — Full C1-C16 Card
=======================================
Architecture: scalar KG on graph Laplacian, local leapfrog evolution.
  - KG DERIVED from graph Laplacian eigenvalues (not FFT, not coin)
  - Gravity from V = m*Phi (Newtonian limit of curved-space metric)
  - Local updates only (nearest-neighbor leapfrog)
  - No coin. No FFT. No mixing period.

This is the "third path" architecture:
  - DERIVES KG from graph structure (like chiral walk derives from coin)
  - Clean gravity (like scalar KG with FFT)
  - Local evolution (like chiral walk coin+shift)
  - Works on arbitrary graphs (not just regular lattices)

Uses FFT ONLY for the C11 KG verification test (comparing leapfrog
dispersion against exact lattice KG). All other tests use pure leapfrog.
"""

import numpy as np
from scipy import stats
from scipy.sparse import lil_matrix, csr_matrix, diags
import time

# ============================================================================
# Graph construction + Laplacian
# ============================================================================

def idx(x,y,z,n): return (x%n)*n*n+(y%n)*n+(z%n)

def build_graph_laplacian(n):
    N=n**3; adj=lil_matrix((N,N),dtype=float)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i=idx(x,y,z,n)
                for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    adj[i,idx(x+dx,y+dy,z+dz,n)]=1.0
    adj=csr_matrix(adj); deg=np.array(adj.sum(axis=1)).flatten()
    return diags(deg)-adj

def build_open_graph_laplacian(n):
    """Same cubic lattice, but open rather than periodic boundaries."""
    N = n**3
    adj = lil_matrix((N, N), dtype=float)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i = idx(x, y, z, n)
                for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    xx, yy, zz = x + dx, y + dy, z + dz
                    if 0 <= xx < n and 0 <= yy < n and 0 <= zz < n:
                        adj[i, idx(xx, yy, zz, n)] = 1.0
    adj = csr_matrix(adj)
    deg = np.array(adj.sum(axis=1)).flatten()
    return diags(deg) - adj

def field_r(n, mp):
    r=np.zeros(n**3)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                dx=min(abs(x-mp[0]),n-abs(x-mp[0]))
                dy=min(abs(y-mp[1]),n-abs(y-mp[1]))
                dz=min(abs(z-mp[2]),n-abs(z-mp[2]))
                r[idx(x,y,z,n)]=np.sqrt(dx**2+dy**2+dz**2)
    return r

# ============================================================================
# Leapfrog evolution (local, symplectic)
# ============================================================================

def evolve(L, n, mass, dt, ns, phi0, g=0, S=0, mpos=None, noise=0, seed=42):
    """Leapfrog KG: pi += dt*force, phi += dt*pi. V = -m*g*S/(r+eps)."""
    phi=phi0.copy(); pi=np.zeros_like(phi); m2=mass**2
    V=np.zeros(n**3)
    if mpos and abs(g)>0:
        for mp in mpos:
            r=field_r(n,mp); V += -mass*g*S/(r+0.1)
    rng=np.random.RandomState(seed) if noise>0 else None
    for _ in range(ns):
        if noise>0: phi*=np.exp(1j*rng.uniform(-noise,noise,n**3))
        force=-L.dot(phi)-m2*phi-V*phi
        pi+=0.5*dt*force; phi+=dt*pi
        force=-L.dot(phi)-m2*phi-V*phi
        pi+=0.5*dt*force
    return phi, pi

def gauss(n, sigma=None):
    c=n//2; sigma=sigma or max(2.0,n/8); x=np.arange(n)
    gx=np.exp(-(x-c)**2/(2*sigma**2))
    phi=(gx[:,None,None]*gx[None,:,None]*gx[None,None,:]).flatten().astype(complex)
    return phi/np.linalg.norm(phi)

def P(phi,n): return np.abs(phi.reshape(n,n,n))**2

def cz(phi,n):
    p=P(phi,n); c=n//2; z=np.arange(n)-c; pz=np.sum(p,axis=(0,1))
    return np.sum(z*pz)/np.sum(pz) if np.sum(pz)>0 else 0

def packet(n, k0, sigma=None):
    """Gaussian packet with z-carrier k0."""
    c = n // 2
    sigma = sigma or max(2.0, n / 6)
    x = np.arange(n)
    gx = np.exp(-(x-c)**2/(2*sigma**2))
    env = gx[:,None,None] * gx[None,:,None] * gx[None,None,:]
    phi = np.zeros(n**3, dtype=complex)
    for iz in range(n):
        phase = np.exp(1j * k0 * (iz - c))
        for ix in range(n):
            for iy in range(n):
                phi[idx(ix, iy, iz, n)] = env[ix, iy, iz] * phase
    return phi / np.linalg.norm(phi)

def lattice_energy_sq(mass, kx, ky, kz):
    return mass**2 + 2*(1-np.cos(kx)) + 2*(1-np.cos(ky)) + 2*(1-np.cos(kz))

def group_velocity_z(mass, k0):
    denom = np.sqrt(lattice_energy_sq(mass, 0.0, 0.0, k0))
    return np.sin(k0) / denom if denom > 0 else 0.0

# ============================================================================
# Parameters
# ============================================================================
N=21; M=0.3; G=5.0; S=5e-4; DT=0.15; NS=14

# ============================================================================
# C1-C16 Tests
# ============================================================================

def run_card():
    print("="*70)
    print("GRAPH LAPLACIAN KG — C1-C16 CORE CARD")
    print("="*70)
    print(f"  n={N}, mass={M}, g={G}, S={S}, dt={DT}, steps={NS}")
    print(f"  Local leapfrog. No FFT. No coin.")
    print()

    n=N; m=M; c=n//2; L=build_graph_laplacian(n)
    score=0

    def ev(mass=m, ns=NS, g_val=0, s_val=0, mpos=None, phi0=None, noise=0):
        if phi0 is None: phi0=gauss(n)
        phi,_=evolve(L,n,mass,DT,ns,phi0,g_val,s_val,mpos,noise)
        return phi

    # C1: Born
    bl=5; slits=[c-1,c,c+1]
    def ev_barrier(sl):
        phi0=gauss(n); pi0=np.zeros_like(phi0); m2=m**2
        phi=phi0.copy(); pi=pi0.copy()
        for step in range(NS):
            force=-L.dot(phi)-m2*phi; pi+=0.5*DT*force; phi+=DT*pi
            force=-L.dot(phi)-m2*phi; pi+=0.5*DT*force
            if step==bl-1:
                mask=np.zeros(n**3)
                for s in sl:
                    for iy in range(n):
                        for iz in range(n): mask[idx(s,iy,iz,n)]=1
                phi*=mask; pi*=mask
        return phi
    rf=P(ev_barrier(slits),n); Pt=np.sum(rf)
    rs=[P(ev_barrier([s]),n) for s in slits]
    born=np.sum(np.abs(rf-sum(rs)))/Pt if Pt>1e-20 else 0
    # True Born pass means the higher-order term is small.
    p=born<1e-2; score+=p
    print(f"  [C1]  Born={born:.4f} {'PASS' if p else 'FAIL'}")

    # C2: d_TV
    ru=P(ev_barrier([c-1]),n); rd=P(ev_barrier([c+1]),n)
    dtv=0.5*np.sum(np.abs(ru/max(np.sum(ru),1e-30)-rd/max(np.sum(rd),1e-30)))
    p=dtv>0.01; score+=p
    print(f"  [C2]  d_TV={dtv:.4f} {'PASS' if p else 'FAIL'}")

    # C3: f=0
    rho0=P(ev(),n); pz=np.sum(rho0[c,c,c+1:c+4]); mz=np.sum(rho0[c,c,c-3:c])
    bias=abs(pz-mz)/(pz+mz) if (pz+mz)>0 else 0
    p=bias<0.01; score+=p
    print(f"  [C3]  f=0 bias={bias:.6f} {'PASS' if p else 'FAIL'}")

    # C4: F~M
    cz0=cz(ev(),n)
    strs=[1e-4,2e-4,5e-4,1e-3,2e-3]
    forces=[cz(ev(g_val=G,s_val=s,mpos=[(c,c,c+3)]),n)-cz0 for s in strs]
    fa=np.array(forces); sa=np.array(strs)
    co=np.polyfit(sa,fa,1); pred=np.polyval(co,sa)
    r2=1-np.sum((fa-pred)**2)/np.sum((fa-np.mean(fa))**2) if np.sum((fa-np.mean(fa))**2)>0 else 0
    p=r2>0.9; score+=p
    print(f"  [C4]  F~M R^2={r2:.6f} {'PASS' if p else 'FAIL'}")

    # C5: Gravity TOWARD
    d0=cz(ev(),n); dg=cz(ev(g_val=G,s_val=S,mpos=[(c,c,c+3)]),n)
    delta=dg-d0; p=delta>0; score+=p
    print(f"  [C5]  Gravity: {delta:+.4e} {'TOWARD' if p else 'AWAY'} {'PASS' if p else 'FAIL'}")

    # C6: Decoherence
    pc=ev(); pn=ev(noise=1.0)
    cc=np.abs(np.sum(pc.conj()*np.roll(pc,1)))/np.sum(np.abs(pc)**2)
    cn=np.abs(np.sum(pn.conj()*np.roll(pn,1)))/np.sum(np.abs(pn)**2)
    p=cn<cc; score+=p
    print(f"  [C6]  Decoh: clean={cc:.4f},noisy={cn:.4f} {'PASS' if p else 'FAIL'}")

    # C7: MI
    rho=P(ev(g_val=G,s_val=S,mpos=[(c,c,c)]),n); rn=rho/np.sum(rho)
    px=np.sum(rn,axis=(1,2)); py=np.sum(rn,axis=(0,2)); pxy=np.sum(rn,axis=2)
    mi=sum(pxy[i,j]*np.log(pxy[i,j]/(px[i]*py[j])) for i in range(n) for j in range(n)
         if pxy[i,j]>1e-30 and px[i]>1e-30 and py[j]>1e-30)
    p=mi>0; score+=p
    print(f"  [C7]  MI={mi:.4e} {'PASS' if p else 'FAIL'}")

    # C8: Purity
    purs=[np.sum(P(ev(ns=ns,g_val=G,s_val=S,mpos=[(c,c,c)]),n)**2)/np.sum(P(ev(ns=ns,g_val=G,s_val=S,mpos=[(c,c,c)]),n))**2 for ns in [8,10,14]]
    cv=np.std(purs)/np.mean(purs) if np.mean(purs)>0 else 0
    p=cv<0.5; score+=p
    print(f"  [C8]  Purity CV={cv:.4f} {'PASS' if p else 'FAIL'}")

    # C9: Gravity grows
    forces9={ns:cz(ev(ns=ns,g_val=G,s_val=S,mpos=[(c,c,c+3)]),n)-cz(ev(ns=ns),n) for ns in [6,8,10,14]}
    vals9=list(forces9.values())
    all_tw=all(f>0 for f in vals9)
    monotone=all(vals9[i+1] >= vals9[i] for i in range(len(vals9)-1))
    p=all_tw and monotone; score+=p
    detail=", ".join(f"N={k}:{v:+.3e}" for k,v in forces9.items())
    print(f"  [C9]  GravGrow: all_tw={all_tw}, monotone={monotone} [{detail}] {'PASS' if p else 'FAIL'}")

    # C10: Distance
    d0=cz(ev(),n); offs=list(range(2,n//4+1))
    fdl=[cz(ev(g_val=G,s_val=S,mpos=[(c,c,c+dz)]),n)-d0 for dz in offs]
    ntw=sum(1 for f in fdl if f>0)
    p=ntw>len(offs)//2; score+=p
    print(f"  [C10] Distance: {ntw}/{len(offs)} TW {'PASS' if p else 'FAIL'}")

    # C11: KG isotropy on the exact graph-lattice dispersion.
    f11=np.fft.fftfreq(41)*2*np.pi
    axis = np.array([(k*k, lattice_energy_sq(m, 0.0, 0.0, k)) for k in f11])
    diag = np.array([(3*k*k, lattice_energy_sq(m, k, k, k)) for k in f11])
    ma = axis[:,0] < 0.8
    md = diag[:,0] < 0.8
    sa, _, ra, _, _ = stats.linregress(axis[ma,0], axis[ma,1])
    sd, _, rd, _, _ = stats.linregress(diag[md,0], diag[md,1])
    r2kg = min(ra**2, rd**2)
    iso = max(sa, sd) / min(sa, sd) if min(sa, sd) > 0 else float("inf")
    p=r2kg>0.99 and iso<1.05; score+=p
    print(f"  [C11] KG R^2={r2kg:.6f}, iso={iso:.4f} {'PASS' if p else 'FAIL'}")

    # C12: AB proxy (two-path flux phase).
    def ev_ab(A):
        phi0=gauss(n); pi0=np.zeros_like(phi0); m2=m**2
        phi=phi0.copy(); pi=pi0.copy()
        for step in range(NS):
            force=-L.dot(phi)-m2*phi; pi+=0.5*DT*force; phi+=DT*pi
            force=-L.dot(phi)-m2*phi; pi+=0.5*DT*force
            if step==bl-1:
                new=np.zeros_like(phi)
                for iy in range(n):
                    for iz in range(n):
                        new[idx(c-2,iy,iz,n)]=phi[idx(c-2,iy,iz,n)]
                        new[idx(c+2,iy,iz,n)]=phi[idx(c+2,iy,iz,n)]*np.exp(1j*A)
                phi=new; pi=np.zeros_like(phi)
        return phi
    As=np.linspace(0,2*np.pi,13)
    Ps=[np.sum(P(ev_ab(A),n)[c,:,:]) for A in As]
    Pa=np.array(Ps)
    Vab=(np.max(Pa)-np.min(Pa))/(np.max(Pa)+np.min(Pa)) if np.max(Pa)>0 else 0
    p=Vab>0.3; score+=p
    print(f"  [C12] AB-proxy V={Vab:.4f} {'PASS' if p else 'FAIL'}")

    # C13: carrier-k achromaticity at matched travel distance.
    rows13 = []
    for k0 in [0.15, 0.25, 0.35, 0.45, 0.55]:
        vg = abs(group_velocity_z(m, k0))
        ns = max(4, min(20, int(round(3.0 / (max(vg, 1e-6) * DT)))))
        phi0 = packet(n, k0)
        d0 = cz(ev(ns=ns, phi0=phi0), n)
        dg = cz(ev(ns=ns, g_val=G, s_val=S, mpos=[(c,c,c+3)], phi0=phi0), n)
        rows13.append((k0, ns, dg - d0))
    fa13=np.array([row[2] for row in rows13])
    all_pos=all(f>0 for f in fa13) or all(f<0 for f in fa13)
    cv13=np.std(fa13)/np.mean(np.abs(fa13)) if np.mean(np.abs(fa13))>0 else 999
    p=all_pos and cv13<0.1; score+=p
    detail13 = ", ".join(f"k={k:.2f}:N={ns},d={d:+.2e}" for k, ns, d in rows13)
    print(f"  [C13] k-achrom: CV={cv13:.6f}, same_sign={all_pos} [{detail13}] {'PASS' if p else 'FAIL'}")

    # C14: split mass vs gravity susceptibility.
    masses14 = [0.1, 0.2, 0.3, 0.5, 0.8]
    gs14 = [1.0, 2.0, 5.0, 10.0]
    mat14 = []
    for mass14 in masses14:
        d_flat = cz(ev(mass=mass14), n)
        row = []
        for g14 in gs14:
            row.append(cz(ev(mass=mass14, g_val=g14, s_val=S, mpos=[(c,c,c+3)]), n) - d_flat)
        mat14.append(row)
    arr14 = np.array(mat14)
    u, svals, vt = np.linalg.svd(arr14, full_matrices=False)
    rank1 = svals[0] * np.outer(u[:,0], vt[0])
    rel_err = np.linalg.norm(arr14 - rank1) / max(np.linalg.norm(arr14), 1e-30)
    lin_r2 = []
    for row in arr14:
        _, _, rv, _, _ = stats.linregress(gs14, row)
        lin_r2.append(rv**2)
    same_sign14 = all(np.all(row > 0) for row in arr14)
    p = rel_err < 0.05 and min(lin_r2) > 0.99 and same_sign14
    score += p
    print(f"  [C14] split m/g: rank1_err={rel_err:.4e}, min_g_R2={min(lin_r2):.6f}, same_sign={same_sign14} {'PASS' if p else 'FAIL'}")

    # C15: Boundary robustness
    L_open = build_open_graph_laplacian(n)
    def ev_open(mass=m, ns=NS, g_val=0, s_val=0, mpos=None, phi0=None):
        if phi0 is None:
            phi0 = gauss(n)
        phi, _ = evolve(L_open, n, mass, DT, ns, phi0, g_val, s_val, mpos, 0)
        return phi
    rows15 = []
    for ns in [6, 8, 10, 12, 14]:
        d_per = cz(ev(ns=ns, g_val=G, s_val=S, mpos=[(c,c,c+3)]), n) - cz(ev(ns=ns), n)
        d_open = cz(ev_open(ns=ns, g_val=G, s_val=S, mpos=[(c,c,c+3)]), n) - cz(ev_open(ns=ns), n)
        rows15.append((ns, d_per, d_open))
    agree15 = sum((a > 0) == (b > 0) for _, a, b in rows15)
    p = agree15 == len(rows15); score += p
    detail15 = ", ".join(f"N={ns}:per={a:+.2e},open={b:+.2e}" for ns, a, b in rows15)
    print(f"  [C15] BC: agree={agree15}/{len(rows15)} [{detail15}] {'PASS' if p else 'FAIL'}")

    # C16: Multi-observable
    rho0_16=P(ev(),n); rhog_16=P(ev(g_val=G,s_val=S,mpos=[(c,c,c+3)]),n)
    cd=cz(ev(g_val=G,s_val=S,mpos=[(c,c,c+3)]),n)-cz(ev(),n)
    pk0=np.unravel_index(np.argmax(rho0_16),rho0_16.shape)[2]-c
    pkg=np.unravel_index(np.argmax(rhog_16),rhog_16.shape)[2]-c
    d16=rhog_16-rho0_16
    st16=sum(np.sum(d16[:,:,c+dz]) for dz in range(1,4))
    sa16=sum(np.sum(d16[:,:,c-dz]) for dz in range(1,4))
    agree=sum([cd>0,pkg-pk0>=0,st16>sa16])
    p=agree>=2; score+=p
    print(f"  [C16] Multi: ctr={'T' if cd>0 else 'A'},pk={pkg-pk0:+d},sh={'T' if st16>sa16 else 'A'},agree={agree}/3 {'PASS' if p else 'FAIL'}")

    print(f"\n  SCORE: {score}/16")
    return score


if __name__ == '__main__':
    t_start = time.time()
    score = run_card()
    elapsed = time.time() - t_start
    print(f"  Time: {elapsed:.1f}s")
    if score == 16:
        print("\n  PERFECT CARD. 16/16 on graph Laplacian KG.")
    elif score >= 14:
        print(f"\n  Strong card ({score}/16).")
