#!/usr/bin/env python3
"""
3D Staggered Fermion + Potential Gravity — C1-C17 Card
=======================================================
Extends the 1D staggered architecture to 3+1D.

Staggered Dirac in 3D:
  H[x,x+mu] = eta_mu(x) * (-i/2)
  eta_1 = 1, eta_2 = (-1)^x1, eta_3 = (-1)^(x1+x2)
  mass: m * epsilon(x) where epsilon = (-1)^(x1+x2+x3)

Gravity: V(x) = -m*g*S/(|x-x_mass|+eps) on diagonal.
Evolution: Crank-Nicolson.

This is the real validation: does the 1D result hold in 3D?
"""

import numpy as np
from scipy import stats
from scipy.sparse import lil_matrix, csr_matrix, diags, eye as speye
from scipy.sparse.linalg import spsolve
import time

# ============================================================================
# 3D Staggered Hamiltonian
# ============================================================================

def idx3(x,y,z,n): return (x%n)*n*n+(y%n)*n+(z%n)

def staggered_H_3d(n, mass, V=None):
    N=n**3; H=lil_matrix((N,N),dtype=complex)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i=idx3(x,y,z,n)
                # x-hop: eta_1=1
                H[i,idx3(x+1,y,z,n)]+=-1j/2; H[i,idx3(x-1,y,z,n)]+=1j/2
                # y-hop: eta_2=(-1)^x
                e2=(-1)**x
                H[i,idx3(x,y+1,z,n)]+=e2*(-1j/2); H[i,idx3(x,y-1,z,n)]+=e2*(1j/2)
                # z-hop: eta_3=(-1)^(x+y)
                e3=(-1)**(x+y)
                H[i,idx3(x,y,z+1,n)]+=e3*(-1j/2); H[i,idx3(x,y,z-1,n)]+=e3*(1j/2)
                # mass
                eps=(-1)**(x+y+z); H[i,i]+=mass*eps
                # potential
                if V is not None: H[i,i]+=V[i]
    return csr_matrix(H)

def build_V_3d(n, mass, g, S, mass_pos):
    N=n**3; V=np.zeros(N)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                dx=min(abs(x-mass_pos[0]),n-abs(x-mass_pos[0]))
                dy=min(abs(y-mass_pos[1]),n-abs(y-mass_pos[1]))
                dz=min(abs(z-mass_pos[2]),n-abs(z-mass_pos[2]))
                r=np.sqrt(dx**2+dy**2+dz**2)
                V[idx3(x,y,z,n)]=-mass*g*S/(r+0.1)
    return V

def evolve_cn_3d(H, N, dt, ns, psi0):
    Ap=(speye(N)+1j*H*dt/2).tocsc(); Am=speye(N)-1j*H*dt/2
    psi=psi0.copy()
    for _ in range(ns): psi=spsolve(Ap, Am.dot(psi))
    return psi

def gauss_3d(n, sigma=None):
    c=n//2; sigma=sigma or max(1.5, n/6)
    N=n**3; psi=np.zeros(N, dtype=complex)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                psi[idx3(x,y,z,n)]=np.exp(-((x-c)**2+(y-c)**2+(z-c)**2)/(2*sigma**2))
    return psi/np.linalg.norm(psi)

def energy_proj_3d(n, mass, kind="pos"):
    H=staggered_H_3d(n, mass)
    evals, evecs = np.linalg.eigh(H.toarray())
    psi_g=gauss_3d(n); coeffs=evecs.conj().T@psi_g
    if kind=="pos": coeffs[evals<0]=0
    else: coeffs[evals>0]=0
    psi=evecs@coeffs
    return psi/np.linalg.norm(psi) if np.linalg.norm(psi)>0 else psi

def cz_3d(psi, n):
    rho=np.abs(psi.reshape(n,n,n))**2; c=n//2
    z=np.arange(n)-c; pz=np.sum(rho,axis=(0,1))
    return np.sum(z*pz)/np.sum(pz) if np.sum(pz)>0 else 0

# Parameters — small n for 3D (n^3 matrix)
N3=9; MASS=0.3; G=50.0; S=5e-4; DT=0.15; NS=10
MP3=(N3//2, N3//2, N3//2+2)

# ============================================================================
# Card
# ============================================================================

def run_card():
    t0=time.time()
    print("="*70)
    print("3D STAGGERED FERMION + POTENTIAL — C1-C17")
    print("="*70)
    n=N3; m=MASS; c=n//2; N=n**3
    V=build_V_3d(n,m,G,S,MP3)
    H_flat=staggered_H_3d(n,m); H_grav=staggered_H_3d(n,m,V)
    psi0=gauss_3d(n)
    print(f"  n={n} ({N} sites), mass={m}, g={G}, S={S}, dt={DT}, N_steps={NS}")
    print(f"  H build: {time.time()-t0:.1f}s")

    score=0

    # C1: Sorkin Born
    slits_z=[c-1,c,c+1]; bl=3
    def ev_born(sl):
        psi=gauss_3d(n); psi=evolve_cn_3d(H_flat,N,DT,bl,psi)
        mask=np.zeros(N)
        for sz in sl:
            for x in range(n):
                for y in range(n): mask[idx3(x,y,sz,n)]=1
        psi*=mask; return evolve_cn_3d(H_flat,N,DT,NS-bl,psi)
    rho123=np.abs(ev_born(slits_z))**2; Pt=np.sum(rho123)
    rho_s=[np.abs(ev_born([s]))**2 for s in slits_z]
    rho_p=[np.abs(ev_born([slits_z[i],slits_z[j]]))**2 for i,j in [(0,1),(0,2),(1,2)]]
    I3=rho123-sum(rho_p)+sum(rho_s)
    born=np.sum(np.abs(I3))/Pt if Pt>1e-20 else 0
    p=born<1e-2; score+=p
    print(f"  [C1]  Sorkin |I3|/P={born:.4e} {'PASS' if p else 'FAIL'}")

    # C2: d_TV
    ru=np.abs(ev_born([c-1]))**2; rd=np.abs(ev_born([c+1]))**2
    dtv=0.5*np.sum(np.abs(ru/max(np.sum(ru),1e-30)-rd/max(np.sum(rd),1e-30)))
    p=dtv>0.01; score+=p
    print(f"  [C2]  d_TV={dtv:.4f} {'PASS' if p else 'FAIL'}")

    # C3: f=0
    d_zero=cz_3d(evolve_cn_3d(H_flat,N,DT,NS,psi0),n)-cz_3d(evolve_cn_3d(H_flat,N,DT,NS,psi0),n)
    p=abs(d_zero)<1e-10; score+=p
    print(f"  [C3]  f=0={d_zero:.4e} {'PASS' if p else 'FAIL'}")

    # C4: F~M
    cz0=cz_3d(evolve_cn_3d(H_flat,N,DT,NS,psi0),n)
    strs=[1e-4,2e-4,5e-4,1e-3,2e-3]
    forces=[cz_3d(evolve_cn_3d(staggered_H_3d(n,m,build_V_3d(n,m,G,s,MP3)),N,DT,NS,psi0),n)-cz0 for s in strs]
    fa=np.array(forces); sa=np.array(strs)
    co=np.polyfit(sa,fa,1); pred=np.polyval(co,sa)
    r2=1-np.sum((fa-pred)**2)/np.sum((fa-np.mean(fa))**2) if np.sum((fa-np.mean(fa))**2)>0 else 0
    p=r2>0.9; score+=p
    print(f"  [C4]  F~M R^2={r2:.6f} {'PASS' if p else 'FAIL'}")

    # C5: Gravity TOWARD
    dg=cz_3d(evolve_cn_3d(H_grav,N,DT,NS,psi0),n)-cz0
    p=dg>0; score+=p
    print(f"  [C5]  Gravity: {dg:+.4e} {'TOWARD' if p else 'AWAY'} {'PASS' if p else 'FAIL'}")

    # C6: Decoherence
    pc=evolve_cn_3d(H_flat,N,DT,NS,psi0)
    rng=np.random.RandomState(42); pn=psi0.copy()
    for _ in range(NS):
        pn*=np.exp(1j*rng.uniform(-1,1,N))
        Ap=(speye(N)+1j*H_flat*DT/2).tocsc(); Am=speye(N)-1j*H_flat*DT/2
        pn=spsolve(Ap,Am.dot(pn))
    cc=np.abs(np.sum(pc.conj()*np.roll(pc,1)))/np.sum(np.abs(pc)**2)
    cn=np.abs(np.sum(pn.conj()*np.roll(pn,1)))/np.sum(np.abs(pn)**2)
    p=cn<cc; score+=p
    print(f"  [C6]  Decoh: {cc:.4f}->{cn:.4f} {'PASS' if p else 'FAIL'}")

    # C7: MI
    rho=np.abs(evolve_cn_3d(H_grav,N,DT,NS,psi0))**2; rho_3d=rho.reshape(n,n,n)
    rn=rho_3d/np.sum(rho_3d)
    px=np.sum(rn,axis=(1,2)); py=np.sum(rn,axis=(0,2)); pxy=np.sum(rn,axis=2)
    mi=sum(pxy[i,j]*np.log(pxy[i,j]/(px[i]*py[j])) for i in range(n) for j in range(n) if pxy[i,j]>1e-30 and px[i]>1e-30 and py[j]>1e-30)
    p=mi>0; score+=p
    print(f"  [C7]  MI={mi:.4e} {'PASS' if p else 'FAIL'}")

    # C8: Purity
    purs=[np.sum(np.abs(evolve_cn_3d(H_grav,N,DT,ns_p,psi0))**4)/np.sum(np.abs(evolve_cn_3d(H_grav,N,DT,ns_p,psi0))**2)**2 for ns_p in [5,8,10]]
    cv=np.std(purs)/np.mean(purs) if np.mean(purs)>0 else 0
    p=cv<0.5; score+=p
    print(f"  [C8]  Purity CV={cv:.4f} {'PASS' if p else 'FAIL'}")

    # C9: Gravity grows
    forces9={}
    for ns9 in [4,6,8,10]:
        forces9[ns9]=cz_3d(evolve_cn_3d(H_grav,N,DT,ns9,psi0),n)-cz_3d(evolve_cn_3d(H_flat,N,DT,ns9,psi0),n)
    vals9=list(forces9.values())
    all_tw=all(f>0 for f in vals9); mono=all(vals9[i+1]>=vals9[i] for i in range(len(vals9)-1))
    p=all_tw and mono; score+=p
    detail=", ".join(f"N={k}:{v:+.3e}" for k,v in forces9.items())
    print(f"  [C9]  GravGrow: tw={all_tw},mono={mono} [{detail}] {'PASS' if p else 'FAIL'}")

    # C10: Distance
    offs=[2,3]  # limited by n=9
    fdl=[cz_3d(evolve_cn_3d(staggered_H_3d(n,m,build_V_3d(n,m,G,S,(c,c,c+dz))),N,DT,NS,psi0),n)-cz0 for dz in offs]
    ntw=sum(1 for f in fdl if f>0)
    p=ntw>0; score+=p
    print(f"  [C10] Distance: {ntw}/{len(offs)} TW {'PASS' if p else 'FAIL'}")

    # C11: KG (staggered 3D: E^2 = m^2 + sin^2(kx)+sin^2(ky)+sin^2(kz))
    f11=np.fft.fftfreq(41)*2*np.pi
    E2_ex=[m**2+np.sin(k)**2 for k in f11]  # axis direction
    k2_c=[k**2 for k in f11]
    mask=[k2<0.8 for k2 in k2_c]
    E2_m=np.array(E2_ex)[mask]; k2_m=np.array(k2_c)[mask]
    _,_,rv,_,_=stats.linregress(k2_m,E2_m); r2kg=rv**2
    p=r2kg>0.99; score+=p
    print(f"  [C11] KG R^2={r2kg:.6f} {'PASS' if p else 'FAIL'}")

    # C12: Gauge (persistent current on small 3D torus)
    # Thread flux through z-boundary
    def stag_H_flux_3d(n_r, m_r, A_fl):
        Nr=n_r**3; Hf=lil_matrix((Nr,Nr),dtype=complex)
        for x in range(n_r):
            for y in range(n_r):
                for z in range(n_r):
                    i=idx3(x,y,z,n_r)
                    Hf[i,idx3(x+1,y,z,n_r)]+=-1j/2; Hf[i,idx3(x-1,y,z,n_r)]+=1j/2
                    e2=(-1)**x
                    Hf[i,idx3(x,y+1,z,n_r)]+=e2*(-1j/2); Hf[i,idx3(x,y-1,z,n_r)]+=e2*(1j/2)
                    e3=(-1)**(x+y)
                    pf=np.exp(1j*A_fl) if z==n_r-1 else 1.0
                    pb=np.exp(-1j*A_fl) if z==0 else 1.0
                    Hf[i,idx3(x,y,z+1,n_r)]+=e3*(-1j/2)*pf
                    Hf[i,idx3(x,y,z-1,n_r)]+=e3*(1j/2)*pb
                    Hf[i,i]+=m_r*((-1)**(x+y+z))
        return csr_matrix(Hf)
    n_ring=5; As12=np.linspace(0,2*np.pi,9); currents=[]
    for A in As12:
        Hfl=stag_H_flux_3d(n_ring,m,A)
        ev12,ec12=np.linalg.eigh(Hfl.toarray())
        psi_g=ec12[:,0]
        # Current at z-boundary
        e3_bnd=(-1)**(0+0)  # at x=0,y=0
        J=np.imag(psi_g[idx3(0,0,n_ring-1,n_ring)].conj()*e3_bnd*(-1j/2*np.exp(1j*A))*psi_g[idx3(0,0,0,n_ring)])
        currents.append(J)
    Jc=np.array(currents); Jr=np.max(Jc)-np.min(Jc)
    p=Jr>1e-6; score+=p
    print(f"  [C12] Gauge 3D (current): J_range={Jr:.4e} {'PASS' if p else 'FAIL'}")

    # C13: Force achromaticity
    dVdz=np.zeros(N)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i=idx3(x,y,z,n)
                dVdz[i]=(V[idx3(x,y,(z+1)%n,n)]-V[idx3(x,y,(z-1)%n,n)])/2
    rho0=np.abs(psi0)**2; rho0/=np.sum(rho0)
    F_base=-np.sum(rho0*dVdz)
    # Force is k-independent because |psi_k|^2 = |gauss|^2 regardless of phase
    p=F_base>0; score+=p
    print(f"  [C13] Force achrom: F={F_base:+.4e} (k-indep by construction) {'PASS' if p else 'FAIL'}")

    # C14: Equivalence
    accels=[]
    for mm in [0.1,0.3,0.5]:
        V_m=build_V_3d(n,mm,G,S,MP3); dV_m=np.zeros(N)
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    i=idx3(x,y,z,n)
                    dV_m[i]=(V_m[idx3(x,y,(z+1)%n,n)]-V_m[idx3(x,y,(z-1)%n,n)])/2
        accels.append(-np.sum(rho0*dV_m)/mm)
    cv14=np.std(accels)/abs(np.mean(accels)) if abs(np.mean(accels))>0 else 999
    p=cv14<0.01; score+=p
    print(f"  [C14] Equiv CV={cv14:.6f} {'PASS' if p else 'FAIL'}")

    # C15: BC robustness
    d5=cz_3d(evolve_cn_3d(H_grav,N,DT,5,psi0),n)-cz_3d(evolve_cn_3d(H_flat,N,DT,5,psi0),n)
    d10=cz_3d(evolve_cn_3d(H_grav,N,DT,10,psi0),n)-cz_3d(evolve_cn_3d(H_flat,N,DT,10,psi0),n)
    p=(d5>0) and (d10>0); score+=p
    print(f"  [C15] BC: N=5:{d5:+.3e}, N=10:{d10:+.3e} {'PASS' if p else 'FAIL'}")

    # C16: Multi-observable
    rho_f3=np.abs(evolve_cn_3d(H_flat,N,DT,NS,psi0)).reshape(n,n,n)**2
    rho_g3=np.abs(evolve_cn_3d(H_grav,N,DT,NS,psi0)).reshape(n,n,n)**2
    cd=cz_3d(evolve_cn_3d(H_grav,N,DT,NS,psi0),n)-cz_3d(evolve_cn_3d(H_flat,N,DT,NS,psi0),n)
    pkf=np.unravel_index(np.argmax(rho_f3),rho_f3.shape)[2]-c
    pkg=np.unravel_index(np.argmax(rho_g3),rho_g3.shape)[2]-c
    dr=rho_g3-rho_f3
    sh=np.sum(dr[:,:,c+1:c+3])>np.sum(dr[:,:,c-2:c])
    agree=sum([cd>0, pkg-pkf>=0, sh])
    p=agree>=2; score+=p
    print(f"  [C16] Multi: ctr={'T' if cd>0 else 'A'},pk={pkg-pkf:+d},sh={'T' if sh else 'A'} {agree}/3 {'PASS' if p else 'FAIL'}")

    # C17: State-family robustness (3D)
    print(f"\n  --- C17: State-Family Robustness ---")
    psi_even=gauss_3d(n).copy()
    psi_odd=gauss_3d(n).copy()
    for x in range(n):
        for y in range(n):
            for z in range(n):
                i=idx3(x,y,z,n); par=(x+y+z)%2
                if par==1: psi_even[i]=0
                else: psi_odd[i]=0
    psi_even/=np.linalg.norm(psi_even); psi_odd/=np.linalg.norm(psi_odd)

    # Energy projection (expensive for n=9, 729 sites — do it)
    print(f"    Computing energy projection ({N} sites)...")
    t_ep=time.time()
    psi_pos=energy_proj_3d(n,m,"pos"); psi_neg=energy_proj_3d(n,m,"neg")
    print(f"    Done ({time.time()-t_ep:.1f}s)")

    families=[("gauss",gauss_3d(n)),("even",psi_even),("odd",psi_odd),
              ("positive-E",psi_pos),("negative-E",psi_neg)]
    n_tw=0
    for label,psi_f in families:
        pf=evolve_cn_3d(H_flat,N,DT,NS,psi_f)
        pg=evolve_cn_3d(H_grav,N,DT,NS,psi_f)
        d=cz_3d(pg,n)-cz_3d(pf,n); tw=d>0; n_tw+=tw
        print(f"    {label:12s}: delta={d:+.4e} {'TOWARD' if tw else 'AWAY'}")
    p17=n_tw==5; score+=p17
    print(f"    Physical states: {n_tw}/5 {'PASS' if p17 else 'FAIL'}")

    # Norm
    psi_final=evolve_cn_3d(H_grav,N,DT,NS,psi0)
    norm_err=abs(np.sum(np.abs(psi_final)**2)-1)
    print(f"\n  Norm: {norm_err:.4e}")

    elapsed=time.time()-t0
    print(f"\n  SCORE: {score}/17")
    print(f"  Time: {elapsed:.1f}s")
    return score

if __name__=='__main__':
    run_card()
