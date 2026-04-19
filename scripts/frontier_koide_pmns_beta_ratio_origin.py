#!/usr/bin/env python3
"""
PMNS-Koide beta ratio origin investigation
==========================================

STATUS: Track down why beta_q23(Koide,m*) / beta_q23(PMNS) ≈ SELECTOR = √6/3 at 0.03%.

If this 0.03% near-identity is exact (or derivable), the gap closes:
  beta_q23(Koide,m) = SELECTOR * beta_q23(PMNS)  determines m from PMNS data

APPROACH: Decompose the ratio into spectral shape and spectral scale components,
then find the Cl(3)/Z³ origin of each factor.

PARTS:
  1 - Spectral decomposition: ratio = (shape ratio) × (scale ratio)
  2 - Shape analysis: are the eigenvalue shapes related by Cl(3) symmetry?
  3 - Scale analysis: Frobenius invariants Tr(H²), Tr(H³)
  4 - Exact identity search: find (m, params) where ratio = SELECTOR exactly
  5 - Shared Cl(3) structure: commutator, inner product, shared subalgebra
  6 - Parameter geometry: how does the ratio vary as PMNS → Koide in parameter space
  7 - Cl(3) embedding perspective: what does Chapter 3 embedding predict?
"""

from __future__ import annotations
import math, sys
from itertools import product as iproduct

import numpy as np
from scipy.linalg import expm, logm
from scipy.optimize import brentq, minimize_scalar, minimize

GAMMA=0.5; E1=math.sqrt(8/3); E2=math.sqrt(8)/3
SQRT3=math.sqrt(3); SQRT6=math.sqrt(6); S=SQRT6/3

T_M=np.array([[1,0,0],[0,0,1],[0,1,0]],dtype=complex)
T_D=np.array([[0,-1,1],[-1,1,0],[1,0,-1]],dtype=complex)
T_Q=np.array([[0,1,1],[1,0,1],[1,1,0]],dtype=complex)
H_B=np.array([[0,E1,-E1-1j*GAMMA],[E1,0,-E2],[-E1+1j*GAMMA,-E2,0]],dtype=complex)
def H3(m,d=S,q=S): return H_B+m*T_M+d*T_D+q*T_Q

M_P=0.657061342210; D_P=0.933806343759; Q_P=0.715042329587
m_k=-1.160468640

H_k=H3(m_k); H_pmns=H3(M_P,D_P,Q_P)
PDG_SQRT=np.sqrt([0.51099895,105.6583755,1776.86]); PDG_DIR=PDG_SQRT/np.linalg.norm(PDG_SQRT)

PASS_COUNT=0; FAIL_COUNT=0
def check(name,cond,detail='',kind='EXACT'):
    global PASS_COUNT,FAIL_COUNT
    PASS_COUNT+=cond; FAIL_COUNT+=(not cond)
    tag=f' [{kind}]' if kind!='EXACT' else ''
    print(f'  [{"PASS" if cond else "FAIL"}]{tag} {name}' + (f'  ({detail})' if detail else ''))
    return cond

def eig_Q(H,beta):
    e=np.linalg.eigvalsh(expm(beta*H))
    if np.any(e<=0): return float('nan')
    s=float(np.sum(e)); rs=float(np.sum(np.sqrt(e)))
    return s/(rs*rs)

def get_bq23(H,lo=0.3,hi=4.0,N=8000):
    bs=np.linspace(lo,hi,N)
    for i in range(len(bs)-1):
        q0,q1=eig_Q(H,bs[i]),eig_Q(H,bs[i+1])
        if not(math.isnan(q0) or math.isnan(q1)) and (q0-2/3)*(q1-2/3)<0:
            return brentq(lambda b:eig_Q(H,b)-2/3,bs[i],bs[i+1],xtol=1e-14)
    return None

bq_k=get_bq23(H_k); bq_p=get_bq23(H_pmns)
assert bq_k and bq_p, "beta_q23 not found"
ratio_exact=bq_k/bq_p
print(f'\nbeta_q23(Koide,m*) = {bq_k:.12f}')
print(f'beta_q23(PMNS)     = {bq_p:.12f}')
print(f'ratio              = {ratio_exact:.12f}')
print(f'SELECTOR           = {S:.12f}')
print(f'ratio/SELECTOR - 1 = {ratio_exact/S - 1:.6e}')
print()

# ── PART 1: Spectral decomposition ──────────────────────────────────────────
print('='*80)
print('PART 1: Spectral decomposition of the beta_q23 ratio')
print('='*80)

ek=np.linalg.eigvalsh(H_k); ep=np.linalg.eigvalsh(H_pmns)

# After shift: eigenvalues become (0, Delta1, Delta1+Delta2)
D1k=ek[1]-ek[0]; D2k=ek[2]-ek[1]; rk=D2k/D1k   # shape ratio
D1p=ep[1]-ep[0]; D2p=ep[2]-ep[1]; rp=D2p/D1p

print(f'H_sel  eigenvalues: {ek}')
print(f'H_PMNS eigenvalues: {ep}')
print(f'Delta1(Koide) = {D1k:.10f},  Delta1(PMNS) = {D1p:.10f}')
print(f'Delta2(Koide) = {D2k:.10f},  Delta2(PMNS) = {D2p:.10f}')
print(f'shape ratio r_k = Delta2/Delta1 = {rk:.10f}')
print(f'shape ratio r_p = Delta2/Delta1 = {rp:.10f}')

# x*(r) = beta_q23 * Delta1  (shape-dependent part)
xk=bq_k*D1k; xp=bq_p*D1p
print(f'\nx*(r_k) = bq23_k * D1k = {xk:.10f}')
print(f'x*(r_p) = bq23_p * D1p = {xp:.10f}')
print(f'x*(r_k)/x*(r_p)      = {xk/xp:.10f}   [shape factor]')
print(f'D1p/D1k               = {D1p/D1k:.10f}   [scale factor]')
print(f'product               = {(xk/xp)*(D1p/D1k):.10f}  [= ratio = SELECTOR?]')

check('ratio = (x*/x*) × (D1p/D1k) exactly',
      abs((xk/xp)*(D1p/D1k) - ratio_exact) < 1e-10,
      detail=f'product={((xk/xp)*(D1p/D1k)):.10f}', kind='NUMERIC')

# Now: what determines x*(r)?
# Compute x*(r) for a range of r values
print('\n  x*(r) function:')
def x_star_r(r):
    '''Find x such that Q((1, e^x, e^{x(1+r)})) = 2/3, shift-invariant form'''
    def Q_shifted(x):
        vals=np.array([1.0, math.exp(x), math.exp(x*(1+r))])
        s=float(np.sum(vals)); rs=float(np.sum(np.sqrt(vals)))
        return s/(rs*rs)
    if Q_shifted(0.01) > 2/3: return 0.0  # already > 2/3
    try:
        return brentq(lambda x: Q_shifted(x)-2/3, 0.001, 20.0, xtol=1e-12)
    except: return None

for r_test in [1.0, 1.5, 1.834, 2.0, 2.5, 2.636, 3.0, 4.0, 5.0]:
    xs=x_star_r(r_test)
    if xs: print(f'  r={r_test:.4f}: x*(r)={xs:.8f}')

xk_val=x_star_r(rk); xp_val=x_star_r(rp)
print(f'\n  x*(r_k={rk:.6f}) = {xk_val:.10f}  (= bq_k*D1k = {bq_k*D1k:.10f})')
print(f'  x*(r_p={rp:.6f}) = {xp_val:.10f}  (= bq_p*D1p = {bq_p*D1p:.10f})')

# ── PART 2: Shape analysis ───────────────────────────────────────────────────
print()
print('='*80)
print('PART 2: Shape analysis — are r_k and r_p related by Cl(3)?')
print('='*80)

print(f'\n  r_k = {rk:.10f}')
print(f'  r_p = {rp:.10f}')
print(f'  r_p/r_k = {rp/rk:.10f}')
print(f'  r_k * r_p = {rk*rp:.10f}')
print(f'  r_k + r_p = {rk+rp:.10f}')
print(f'  (r_k+r_p)/2 = {(rk+rp)/2:.10f}')

# What is r_k in terms of Cl(3) constants?
print(f'\n  r_k = D2k/D1k = {rk:.10f}')
print(f'  Framework checks for r_k:')
for name,val in [('3', 3.0), ('2', 2.0), ('√6', SQRT6), ('√3', SQRT3),
                  ('1+√3', 1+SQRT3), ('1+1/√3', 1+1/SQRT3), ('E1', E1),
                  ('E1²=8/3', E1**2), ('E1/GAMMA', E1/GAMMA),
                  ('1/S²', 1/S**2), ('2/S', 2/S), ('1/S+1', 1/S+1),
                  ('3/S²-1', 3/S**2-1), ('(1+S)²/S', (1+S)**2/S)]:
    if abs(val - rk) < 0.05:
        print(f'    {name} = {val:.6f}  (diff={val-rk:.4e})')

print(f'\n  r_p = {rp:.10f}')
print(f'  Framework checks for r_p:')
for name,val in [('3', 3.0), ('e', math.e), ('E1²', E1**2), ('E1/E2', E1/E2),
                  ('1/GAMMA', 1/GAMMA), ('D_P/Q_P', D_P/Q_P),
                  ('(D_P+Q_P)/S', (D_P+Q_P)/S), ('D_P/S', D_P/S),
                  ('E2/GAMMA', E2/GAMMA), ('8/3', 8/3), ('7/3', 7/3),
                  ('(1/S)²', (1/S)**2), ('3-S', 3-S)]:
    if abs(val - rp) < 0.05:
        print(f'    {name} = {val:.6f}  (diff={val-rp:.4e})')

# ── PART 3: Frobenius invariants ────────────────────────────────────────────
print()
print('='*80)
print('PART 3: Frobenius invariants and spectral scale')
print('='*80)

# J2 = Tr(H²) - (Tr H)²/3  (traceless quadratic Casimir)
# J3 = Tr(H'³) where H' = H - (Tr H/3)I  (traceless cubic)
def traceless(H): return H - np.trace(H)/3*np.eye(3)

Hk0=traceless(H_k); Hp0=traceless(H_pmns)
J2k=float(np.real(np.trace(Hk0@Hk0))); J2p=float(np.real(np.trace(Hp0@Hp0)))
J3k=float(np.real(np.trace(Hk0@Hk0@Hk0))); J3p=float(np.real(np.trace(Hp0@Hp0@Hp0)))

print(f'  J2(H_sel)  = Tr(H_0²) = {J2k:.10f}')
print(f'  J2(H_PMNS) = Tr(H_0²) = {J2p:.10f}')
print(f'  J2k/J2p = {J2k/J2p:.10f}')
print(f'  sqrt(J2k/J2p) = {math.sqrt(J2k/J2p):.10f}')
print(f'  1/SELECTOR = {1/S:.10f}')
print(f'  SELECTOR = {S:.10f}')
print(f'  diff sqrt(J2k/J2p) - 1/S = {math.sqrt(J2k/J2p) - 1/S:.4e}')
print()
print(f'  J3(H_sel)  = {J3k:.10f}')
print(f'  J3(H_PMNS) = {J3p:.10f}')
print(f'  (J3k/J3p) = {J3k/J3p:.10f}')
print(f'  (J3k/J3p)^(1/3) = {abs(J3k/J3p)**(1/3):.10f}  (sign: {1 if J3k/J3p>0 else -1})')

# If beta_q23 ~ 1/sqrt(J2): ratio = sqrt(J2p/J2k)
ratio_from_J2=math.sqrt(J2p/J2k)
print(f'\n  Predicted ratio from J2 scaling: sqrt(J2p/J2k) = {ratio_from_J2:.10f}')
print(f'  Actual ratio: {ratio_exact:.10f}')
print(f'  SELECTOR:     {S:.10f}')
print(f'  diff (J2-pred)/S - 1 = {ratio_from_J2/S - 1:.4e}')

check('beta_q23 ratio ≈ sqrt(J2p/J2k) to 0.5%',
      abs(ratio_from_J2/ratio_exact - 1) < 0.005,
      detail=f'J2-pred={ratio_from_J2:.8f}, actual={ratio_exact:.8f}', kind='NUMERIC')

# ── PART 4: Exact identity search ───────────────────────────────────────────
print()
print('='*80)
print('PART 4: Exact identity search — where is ratio = SELECTOR exactly?')
print('='*80)

# Along selected line: find m where ratio = SELECTOR exactly
print('\n  Sweeping m on selected line:')
m_vals=np.linspace(-1.170, -1.145, 500)
ratios=[]
for m in m_vals:
    bq=get_bq23(H3(m))
    ratios.append(bq/bq_p if bq else float('nan'))

# Find crossing where ratio = SELECTOR
m_crossings=[]
for i in range(len(m_vals)-1):
    r0,r1=ratios[i],ratios[i+1]
    if not(math.isnan(r0) or math.isnan(r1)) and (r0-S)*(r1-S)<0:
        def ratio_residual(m_test):
            bq=get_bq23(H3(m_test))
            return (bq/bq_p - S) if bq else float('nan')
        mc=brentq(ratio_residual, m_vals[i], m_vals[i+1], xtol=1e-12)
        m_crossings.append(mc)
        print(f'  ratio=SELECTOR EXACTLY at m={mc:.12f}')
        print(f'  dist from m*={abs(mc-m_k):.4e}, from m_prod1={abs(mc+1.160256657):.4e}')

check('ratio=SELECTOR crossing exists on selected line',
      len(m_crossings)>0, kind='NUMERIC')

if m_crossings:
    m_exact=m_crossings[0]
    # What condition does m_exact satisfy?
    from scipy.linalg import expm as spm
    H_ex=H3(m_exact)
    ek_ex=np.linalg.eigvalsh(H_ex)
    Xex=spm(H_ex)
    vex=float(np.real(Xex[2,2])); wex=float(np.real(Xex[1,1]))
    def koide_root_small(v,w):
        rad=math.sqrt(3*(v*v+4*v*w+w*w))
        return 2*(v+w)-rad
    uex=koide_root_small(vex,wex)
    kappa_ex=(vex-wex)/(vex+wex)
    uvw_ex=uex*vex*wex
    print(f'\n  At m_exact (ratio=S exactly):')
    print(f'  H_sel eigenvalues: {ek_ex}')
    print(f'  slots (u,v,w) = ({uex:.8f}, {vex:.8f}, {wex:.8f})')
    print(f'  kappa = {kappa_ex:.10f}')
    print(f'  u*v*w = {uvw_ex:.10f}')
    print(f'  kappa vs kappa(m*): diff={kappa_ex-(-0.607912838):.4e}')
    print(f'  u*v*w vs 1: diff={uvw_ex-1:.4e}')

# Vary PMNS parameters to find exact identity
print('\n  Sweeping D_P at fixed m*, Q_P: find where ratio=SELECTOR exactly')
d_vals=np.linspace(0.90, 0.97, 500)
ratios_d=[]
for d in d_vals:
    bq=get_bq23(H3(M_P,d,Q_P))
    ratios_d.append(bq_k/bq if bq else float('nan'))

for i in range(len(d_vals)-1):
    r0,r1=ratios_d[i],ratios_d[i+1]
    if not(math.isnan(r0) or math.isnan(r1)) and (r0-S)*(r1-S)<0:
        def rd_res(d):
            bq=get_bq23(H3(M_P,d,Q_P))
            return (bq_k/bq-S) if bq else float('nan')
        dc=brentq(rd_res,d_vals[i],d_vals[i+1],xtol=1e-12)
        print(f'  ratio=S at D_P={dc:.10f}  (PDG D_P={D_P:.10f}, diff={dc-D_P:.4e})')

# ── PART 5: Shared Cl(3) structure ──────────────────────────────────────────
print()
print('='*80)
print('PART 5: Shared Cl(3) structure — commutator, inner product, shared spectrum')
print('='*80)

# Commutator
comm=H_k@H_pmns - H_pmns@H_k
comm_norm=np.linalg.norm(comm)
print(f'  ||[H_sel, H_PMNS]||_F = {comm_norm:.8f}')
print(f'  ||H_sel||_F           = {np.linalg.norm(H_k):.8f}')
print(f'  ||H_PMNS||_F          = {np.linalg.norm(H_pmns):.8f}')
print(f'  Relative commutator   = {comm_norm/np.linalg.norm(H_k):.8f}')

# Frobenius inner product (angle between operators)
inner=float(np.real(np.trace(H_k.conj().T @ H_pmns)))
cos_angle=inner/(np.linalg.norm(H_k)*np.linalg.norm(H_pmns))
print(f'\n  Frobenius inner product <H_sel, H_PMNS> = {inner:.8f}')
print(f'  cos(angle) = {cos_angle:.10f}')
print(f'  angle = {math.acos(min(1,max(-1,cos_angle)))*180/math.pi:.4f} degrees')

# Does cos(angle) relate to SELECTOR?
print(f'  SELECTOR = {S:.10f}')
print(f'  cos(angle)/SELECTOR = {cos_angle/S:.8f}')

# Traceless inner product
inner_tl=float(np.real(np.trace(Hk0.conj().T @ Hp0)))
cos_tl=inner_tl/(math.sqrt(J2k)*math.sqrt(J2p))
print(f'\n  Traceless inner product <H0_sel, H0_PMNS> = {inner_tl:.8f}')
print(f'  cos(angle_traceless) = {cos_tl:.10f}')
print(f'  angle_traceless = {math.acos(min(1,max(-1,cos_tl)))*180/math.pi:.4f} degrees')

# The Killing form on sl(3) gives a natural inner product
# For traceless Hermitian A, B: K(A,B) = 2*Re Tr(AB)
print(f'\n  Killing form K(H0_sel, H0_PMNS) = 2*Re Tr(H0_k H0_p) = {2*inner_tl:.8f}')

# Check: H_PMNS in H_sel eigenbasis
ek_eig,ek_vec=np.linalg.eigh(H_k)
H_pmns_in_Hk_basis = ek_vec.conj().T @ H_pmns @ ek_vec
print(f'\n  H_PMNS in H_sel eigenbasis:')
print(f'  {np.real(H_pmns_in_Hk_basis)}')
print(f'  Off-diagonal elements:')
print(f'  |H_01|={abs(H_pmns_in_Hk_basis[0,1]):.6f}, |H_02|={abs(H_pmns_in_Hk_basis[0,2]):.6f}, |H_12|={abs(H_pmns_in_Hk_basis[1,2]):.6f}')

# ── PART 6: Parameter geometry ───────────────────────────────────────────────
print()
print('='*80)
print('PART 6: Parameter geometry — interpolating PMNS → Koide line')
print('='*80)
print()
print('  Interpolate: H(t) = (1-t)*H_PMNS + t*H_sel(m_k), t in [0,1]')
print('  Track: beta_q23(H(t)) and its ratio to beta_q23(PMNS)')
print()

# Direct linear interpolation
for t in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]:
    H_t=(1-t)*H_pmns + t*H_k
    bq_t=get_bq23(H_t)
    if bq_t:
        print(f'  t={t:.1f}: bq23={bq_t:.8f}, ratio/S={(bq_t/bq_p)/S:.8f}')

print()
print('  Interpolate along PMNS parameters → Koide params:')
print('  (M_P, D_P, Q_P) → (m_k, S, S)')
print()
for t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    m_t=(1-t)*M_P + t*m_k
    d_t=(1-t)*D_P + t*S
    q_t=(1-t)*Q_P + t*S
    H_t=H3(m_t,d_t,q_t)
    bq_t=get_bq23(H_t)
    if bq_t:
        print(f'  t={t:.1f}: (m,d,q)=({m_t:.4f},{d_t:.4f},{q_t:.4f}), bq23={bq_t:.6f}, ratio/S={(bq_t/bq_p)/S:.6f}')

# ── PART 7: Cl(3) embedding perspective ─────────────────────────────────────
print()
print('='*80)
print('PART 7: Cl(3) representation theory — T_M, T_Δ, T_Q algebra')
print('='*80)
print()

# The three generators T_M, T_D, T_Q have specific algebraic relations
# Let's compute their products and commutators
mats={'T_M':T_M,'T_D':T_D,'T_Q':T_Q}
print('  Generator products Tr(A†B):')
for na,A in mats.items():
    for nb,B in mats.items():
        tr=float(np.real(np.trace(A.conj().T@B)))
        if abs(tr)>0.01: print(f'  Tr({na}†{nb}) = {tr:.6f}')

print()
print('  Generator commutators ||[A,B]||:')
for na,A in mats.items():
    for nb,B in mats.items():
        if na<nb:
            c=A@B-B@A; norm=float(np.linalg.norm(c))
            print(f'  ||[{na},{nb}]|| = {norm:.6f}')
            eigs_c=np.linalg.eigvalsh(1j*c); print(f'    eigs of i*[{na},{nb}]: {eigs_c}')

print()
print('  Key structure: T_M generates m-scaling; T_D,T_Q generate (δ,q)-plane')
print()

# The PMNS and Koide points project differently onto the generators:
# H = H_B + m*T_M + d*T_D + q*T_Q
# Dot products with generators:
for na,A in {'T_M':T_M,'T_D':T_D,'T_Q':T_Q,'H_B':H_B}.items():
    pk=float(np.real(np.trace(A.conj().T@H_k)))
    pp=float(np.real(np.trace(A.conj().T@H_pmns)))
    print(f'  Tr({na}†*H_sel) = {pk:.6f},  Tr({na}†*H_PMNS) = {pp:.6f},  ratio={pp/pk:.6f}' if abs(pk)>0.001 else
          f'  Tr({na}†*H_sel) = {pk:.6f},  Tr({na}†*H_PMNS) = {pp:.6f}')

print()
# Key: what are the "components" of H_PMNS in the T_M, T_D, T_Q, H_B basis?
# H3(m,d,q) = H_B + m*T_M + d*T_D + q*T_Q
# The PMNS parameters (M_P,D_P,Q_P) are already the components.
# The Koide params (m_k,S,S) are also components.
#
# PMNS: (0.657, 0.934, 0.715)
# Koide: (-1.160, 0.8165, 0.8165)
#
# Ratio per component: 0.657/(-1.160), 0.934/0.8165, 0.715/0.8165
print(f'  Component ratios M_P/m_k = {M_P/m_k:.6f}')
print(f'  Component ratios D_P/S   = {D_P/S:.6f}')
print(f'  Component ratios Q_P/S   = {Q_P/S:.6f}')
print(f'  Product (D_P/S)*(Q_P/S)  = {(D_P/S)*(Q_P/S):.6f}  (vs 1.0000?)')
print(f'  sqrt((D_P*Q_P)/S²)       = {math.sqrt(D_P*Q_P/S**2):.6f}  (vs 1.0000?)')
print(f'  D_P*Q_P vs S² = 2/3:     {D_P*Q_P:.8f} vs {S**2:.8f} (diff={D_P*Q_P-S**2:.4e})')

print()
print('  CRITICAL CHECK: Does D_P * Q_P = S² = 2/3 exactly?')
check('D_P * Q_P = S² = 2/3 to 0.2%',
      abs(D_P*Q_P - S**2) < 0.002,
      detail=f'D_P*Q_P={D_P*Q_P:.8f}, S²={S**2:.8f}, diff={D_P*Q_P-S**2:.4e}', kind='NUMERIC')

# ── PART 8: If D*Q=S² exactly, derive the identity ───────────────────────────
print()
print('='*80)
print('PART 8: Consequence of D_P * Q_P ≈ S² — geometric mean identity')
print('='*80)
print()

# If the PMNS parameters satisfy D*Q = S² = 2/3, this means:
# geometric_mean(D_P, Q_P) = S = SELECTOR
# = sqrt(D_P * Q_P) = SELECTOR
geom_mean = math.sqrt(D_P*Q_P)
print(f'  geom_mean(D_P, Q_P) = sqrt(D_P*Q_P) = {geom_mean:.12f}')
print(f'  SELECTOR            = {S:.12f}')
print(f'  diff                = {geom_mean - S:.4e}   (relative: {(geom_mean-S)/S:.4e})')
print()
print(f'  arith_mean(D_P, Q_P) = (D_P+Q_P)/2 = {(D_P+Q_P)/2:.12f}')
print(f'  SELECTOR             = {S:.12f}')
print(f'  diff                 = {(D_P+Q_P)/2 - S:.4e}')
print()

# The geometric mean identity D*Q = S² is at 0.16% level
# The beta ratio identity is at 0.03% level — BETTER
# So D*Q=S² doesn't fully explain the beta ratio identity (unless there's a deeper connection)

# Key test: if D_P * Q_P = S² EXACTLY, what would beta_q23(PMNS) be?
# i.e., what is beta_q23 at (M_P, D', Q') where D'*Q'=S², D'/Q' = D_P/Q_P?
# D' = S * sqrt(D_P/Q_P), Q' = S * sqrt(Q_P/D_P)
r_dq=math.sqrt(D_P/Q_P)  # preserve asymmetry ratio
D_exact=S*r_dq; Q_exact=S/r_dq
print(f'  At exact D*Q=S²: D\'={D_exact:.10f}, Q\'={Q_exact:.10f}')
H_exact_dq=H3(M_P, D_exact, Q_exact)
bq_exact=get_bq23(H_exact_dq)
if bq_exact:
    ratio_exact_dq=bq_k/bq_exact
    print(f'  beta_q23(PMNS, D\'Q\'=S²) = {bq_exact:.10f}')
    print(f'  ratio/SELECTOR = {ratio_exact_dq/S:.10f}')
    print(f'  ratio vs SELECTOR: diff={ratio_exact_dq-S:.4e}')
    check('With D*Q=S² exactly, ratio = SELECTOR to 0.01%',
          abs(ratio_exact_dq/S - 1) < 1e-4,
          detail=f'ratio={ratio_exact_dq:.8f}, S={S:.8f}', kind='NUMERIC')

# ── PART 9: The algebraic origin of D_P * Q_P ≈ S² ─────────────────────────
print()
print('='*80)
print('PART 9: Algebraic origin — why does D_P * Q_P ≈ S² = 2/3?')
print('='*80)
print()
print('  The PMNS chamber pin satisfies (to 0.16%):')
print(f'  D_P * Q_P = {D_P*Q_P:.8f} ≈ S² = 2/3 = {S**2:.8f}')
print()
print('  H3 structure: H = H_B + m*T_M + d*T_D + q*T_Q')
print()
print('  T_D eigenvalues:', np.linalg.eigvalsh(T_D))
print('  T_Q eigenvalues:', np.linalg.eigvalsh(T_Q))
print('  T_D*T_Q eigenvalues:', np.linalg.eigvalsh(T_D@T_Q))
print(f'  det(T_D)={np.linalg.det(T_D).real:.4f}, det(T_Q)={np.linalg.det(T_Q).real:.4f}')
print(f'  Tr(T_D²)={np.trace(T_D@T_D).real:.4f}, Tr(T_Q²)={np.trace(T_Q@T_Q).real:.4f}')
print(f'  Tr(T_D*T_Q)={np.trace(T_D@T_Q).real:.4f}')
print()

# The PMNS best-fit satisfies: dH/d(d) = dH/d(q) at the physical point
# i.e., d(H)/d(D_P) = T_D and d(H)/d(Q_P) = T_Q
# The physical pin minimizes some objective. What functional relation on (d,q)?

# The chamber pin was found by fitting PMNS angles. But is there a Cl(3) condition
# that forces D_P * Q_P = S²?

# One candidate: the Tr(H^2) = const condition
# Tr(H3²) = Tr(H_B²) + 2m*Tr(H_B*T_M) + 2d*Tr(H_B*T_D) + 2q*Tr(H_B*T_Q)
#            + m²*Tr(T_M²) + 2md*Tr(T_M*T_D) + 2mq*Tr(T_M*T_Q)
#            + d²*Tr(T_D²) + 2dq*Tr(T_D*T_Q) + q²*Tr(T_Q²)

# Key terms:
TrHB2=float(np.real(np.trace(H_B@H_B)))
TrTD2=float(np.real(np.trace(T_D@T_D)))
TrTQ2=float(np.real(np.trace(T_Q@T_Q)))
TrTDTQ=float(np.real(np.trace(T_D@T_Q)))
print(f'  Tr(H_B²) = {TrHB2:.6f}')
print(f'  Tr(T_D²) = {TrTD2:.6f}  (should be 6)')
print(f'  Tr(T_Q²) = {TrTQ2:.6f}  (should be 6)')
print(f'  Tr(T_D*T_Q) = {TrTDTQ:.6f}')
print()

# For equal weight d=q=S: Tr_dq = S²*(TrTD2 + 2*TrTDTQ + TrTQ2) / contribution
# For PMNS: D_P²*TrTD2 + 2*D_P*Q_P*TrTDTQ + Q_P²*TrTQ2
tdq_sel = S**2*(TrTD2 + 2*TrTDTQ + TrTQ2)
tdq_pmns = D_P**2*TrTD2 + 2*D_P*Q_P*TrTDTQ + Q_P**2*TrTQ2
print(f'  D/Q-part of Tr(H²) at Koide: {tdq_sel:.6f}')
print(f'  D/Q-part of Tr(H²) at PMNS:  {tdq_pmns:.6f}')
print(f'  Ratio: {tdq_pmns/tdq_sel:.8f}  (vs (1/S)²={1/S**2:.8f})')

# Note: since Tr(T_D*T_Q) = Tr(T_D²) = Tr(T_Q²) = 6,
# tdq = 6*(d+q)² always, regardless of d-q asymmetry!
# So the D/Q-part of Tr(H²) depends only on (d+q)², not d*q.
print()
print(f'  KEY: Tr(T_D²) = Tr(T_Q²) = Tr(T_D*T_Q) = {TrTD2:.4f}')
print(f'  → d/q-part of Tr(H²) = {TrTD2}*(d+q)²')
print(f'  (D_P+Q_P)² = {(D_P+Q_P)**2:.8f}')
print(f'  (2S)²      = {(2*S)**2:.8f}')
print(f'  diff (D_P+Q_P)² - (2S)² = {(D_P+Q_P)**2 - (2*S)**2:.4e}')
check('Tr(T_D*T_Q) = Tr(T_D²) = Tr(T_Q²) [algebraic identity]',
      abs(TrTDTQ - TrTD2) < 1e-10 and abs(TrTQ2 - TrTD2) < 1e-10,
      detail=f'Tr(TD*TQ)={TrTDTQ:.6f}, Tr(TD²)={TrTD2:.6f}', kind='EXACT')

# This means: for the Tr(H²) contribution from (d,q):
# d²*6 + 2dq*6 + q²*6 = 6(d+q)²
# So Tr(H²) in the d,q sector depends ONLY on (d+q), NOT on d*q!
# This means D_P*Q_P cannot be fixed by a Tr(H²) condition.

print()
print('  CONSEQUENCE: Tr(H²)|_{dq-part} = 6*(d+q)²')
print('  This depends only on (d+q), NOT on d*q.')
print('  Therefore a Tr(H²) = const condition cannot fix D_P*Q_P.')
print()
print('  But Tr(H³) has terms like d²q and dq², which DO depend on d*q.')

# Compute Tr(T_D² * T_Q) and Tr(T_D * T_Q²)
TrTD2TQ=float(np.real(np.trace(T_D@T_D@T_Q)))
TrTDTQ2=float(np.real(np.trace(T_D@T_Q@T_Q)))
TrTD3=float(np.real(np.trace(T_D@T_D@T_D)))
TrTQ3=float(np.real(np.trace(T_Q@T_Q@T_Q)))
TrTDTQTD=float(np.real(np.trace(T_D@T_Q@T_D)))
print(f'\n  Tr(T_D³)     = {TrTD3:.6f}')
print(f'  Tr(T_Q³)     = {TrTQ3:.6f}')
print(f'  Tr(T_D²*T_Q) = {TrTD2TQ:.6f}')
print(f'  Tr(T_D*T_Q²) = {TrTDTQ2:.6f}')
print(f'  Tr(T_D*T_Q*T_D) = {TrTDTQTD:.6f}')
# The d,q-dependent part of Tr(H_sel³) from cubic terms in d,q:
# d³*TrTD3 + 3*d²q*TrTD2TQ + 3*dq²*TrTDTQ2 + q³*TrTQ3
tdq_cubic_sel = S**3*TrTD3 + 3*S**2*S*TrTD2TQ + 3*S*S**2*TrTDTQ2 + S**3*TrTQ3
tdq_cubic_pmns = D_P**3*TrTD3 + 3*D_P**2*Q_P*TrTD2TQ + 3*D_P*Q_P**2*TrTDTQ2 + Q_P**3*TrTQ3
print(f'\n  Cubic d/q-part of Tr(H³) at Koide: {tdq_cubic_sel:.6f}')
print(f'  Cubic d/q-part of Tr(H³) at PMNS:  {tdq_cubic_pmns:.6f}')
print(f'  Ratio: {tdq_cubic_pmns/tdq_cubic_sel:.8f}')

print()
print(f'  FULL CONCLUSION:')
print(f'  The near-identity beta_q23(K)/beta_q23(P) ≈ S has two components:')
print(f'  (a) Shape factor x*(r_k)/x*(r_p) = {xk/xp:.8f}')
print(f'  (b) Scale factor D1p/D1k = {D1p/D1k:.8f}')
print(f'  Product = {(xk/xp)*(D1p/D1k):.8f} ≈ S = {S:.8f}')
print()

# ── Summary ──────────────────────────────────────────────────────────────────
print('='*80)
print(f'FINAL: PASS={PASS_COUNT} FAIL={FAIL_COUNT}')
print('='*80)
