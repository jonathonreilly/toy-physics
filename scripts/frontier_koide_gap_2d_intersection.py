#!/usr/bin/env python3
"""
Koide gap 2D intersection and epsilon-precision analysis
=========================================================

KEY INSIGHT from exhaustive script:
  Two conditions on the selected line give different m values:
    (A) u*v*w = 1  → m_prod1 = -1.160257
    (B) κ = κ_PDG  → m_star  = -1.160469
  They CANNOT be simultaneously satisfied on the 1D selected line d=q=S.

  But: if we allow d = q = S - ε (still symmetric, off selected line), we have
  a 2D space parameterized by (m, ε). The two conditions A and B each cut a 1D
  curve, and they INTERSECT at some (m_0, ε_0).

  From the exhaustive script Part 9: at m = m_prod1 and ε ≈ 6.7e-5, κ ≈ κ_PDG.
  But u*v*w ≠ 1 there. The EXACT 2D intersection point (m_0, ε_0) satisfies both.

HYPOTHESIS from exhaustive script (rough): ε_0 ≈ α_EM²/S = 6.52e-5 (2.7% match)

THIS SCRIPT:
  1  — Solve the 2D intersection precisely (Newton/brentq): find (m_0, ε_0)
  2  — High-precision test: ε_0 vs α_EM²/S and other candidates
  3  — PSLQ-style search: rational/algebraic combination matching ε_0
  4  — Characterise d_0 = S - ε_0 algebraically
  5  — Check: does (m_0, d_0, d_0) still satisfy eigenvalue Q = 2/3?
  6  — Check: is κ at (m_0, d_0) consistent with D*Q = 2/3 at PMNS pin?
  7  — NEW ROUTE: eigenvalue-based Koide Q at the selected line
  8  — NEW ROUTE: PMNS feedback coupling — does (D_P - Q_P) × α_EM → ε_0?
  9  — Systematic scan: ε_0 / (known constants) — find clean ratio
 10  — Assumptions audit: what new routes are revealed?
"""

from __future__ import annotations
import math, sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, fsolve, minimize_scalar

GAMMA=0.5; E1=math.sqrt(8/3); E2=math.sqrt(8)/3
SQRT3=math.sqrt(3); SQRT6=math.sqrt(6); S=SQRT6/3
ALPHA_EM=7.2973535693e-3

T_M=np.array([[1,0,0],[0,0,1],[0,1,0]],dtype=complex)
T_D=np.array([[0,-1,1],[-1,1,0],[1,0,-1]],dtype=complex)
T_Q=np.array([[0,1,1],[1,0,1],[1,1,0]],dtype=complex)
H_B=np.array([[0,E1,-E1-1j*GAMMA],[E1,0,-E2],[-E1+1j*GAMMA,-E2,0]],dtype=complex)

def H3(m, d=S, q=S):
    return H_B + m*T_M + d*T_D + q*T_Q

M_P=0.657061342210; D_P=0.933806343759; Q_P=0.715042329587
H_pmns=H3(M_P, D_P, Q_P)

PDG_MEV=np.array([0.51099895, 105.6583755, 1776.86])
PDG_SQRT=np.sqrt(PDG_MEV); PDG_DIR=PDG_SQRT/np.linalg.norm(PDG_SQRT)

def koide_root_small(v, w):
    rad=math.sqrt(3*(v*v+4*v*w+w*w)); return 2*(v+w)-rad

def kappa_from_slots(v, w):
    return (v-w)/(v+w)

def kappa_pdg_from_masses(me, mmu, mtau):
    from scipy.optimize import minimize_scalar as ms_
    sqm=np.sqrt([me,mmu,mtau]); d=sqm/np.linalg.norm(sqm)
    def koide_amp(k):
        w=(1-k)/(1+k)
        if w<=0: return 1.0
        u=koide_root_small(1.0,w)
        if u<=0: return 1.0
        a=np.array([u,1.0,w]); return -float(np.dot(a/np.linalg.norm(a),d))
    r=ms_(koide_amp,bounds=(-0.9999,-0.0001),method='bounded',options={'xatol':1e-14})
    return float(r.x)

kappa_pdg = kappa_pdg_from_masses(*PDG_MEV)

def state_at(m, eps):
    """Return (uvw, kappa) at d=q=S-eps."""
    H=H3(m, S-eps, S-eps)
    x=expm(H)
    v=float(x[2,2].real); w=float(x[1,1].real)
    u=koide_root_small(v,w)
    return u*v*w, kappa_from_slots(v,w)

def eig_Q(H, beta=1.0):
    e=np.linalg.eigvalsh(expm(beta*H))
    if np.any(e<=0): return float('nan')
    return float(np.sum(e))/(float(np.sum(np.sqrt(e)))**2)

PASS_COUNT=0; FAIL_COUNT=0
def check(name, cond, detail='', kind='EXACT'):
    global PASS_COUNT, FAIL_COUNT
    PASS_COUNT+=cond; FAIL_COUNT+=(not cond)
    tag=f' [{kind}]' if kind!='EXACT' else ''
    print(f'  [{"PASS" if cond else "FAIL"}]{tag} {name}'+(f'  ({detail})' if detail else ''))
    return cond

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: Solve 2D intersection precisely
# Find (m_0, eps_0) such that uvw(m,eps)=1 AND kappa(m,eps)=kappa_PDG
# ─────────────────────────────────────────────────────────────────────────────
print("="*80)
print("PART 1: Solve 2D intersection (uvw=1 AND kappa=kappa_PDG)")
print("="*80)

print(f"\n  kappa_PDG = {kappa_pdg:.15f}")

# Strategy: for each eps, find m such that uvw(m,eps)=1 (using brentq on m)
# Then check if kappa = kappa_PDG

def m_at_uvw1(eps, lo=-1.17, hi=-1.15):
    """Find m where uvw=1 at d=q=S-eps."""
    f = lambda m: state_at(m, eps)[0] - 1.0
    try:
        return brentq(f, lo, hi, xtol=1e-15)
    except ValueError:
        return float('nan')

def kappa_at_uvw1(eps):
    """kappa at the uvw=1 point for given eps."""
    m0 = m_at_uvw1(eps)
    if math.isnan(m0): return float('nan')
    return state_at(m0, eps)[1]

# Scan eps to find crossing kappa = kappa_PDG
eps_scan = np.linspace(-1e-3, 1e-3, 2000)
kappa_scan = []
for eps in eps_scan:
    kappa_scan.append(kappa_at_uvw1(eps) - kappa_pdg)

# Find crossings
eps_crossings = []
for i in range(len(eps_scan)-1):
    if not math.isnan(kappa_scan[i]) and not math.isnan(kappa_scan[i+1]):
        if kappa_scan[i]*kappa_scan[i+1] < 0:
            eps_c = brentq(lambda e: kappa_at_uvw1(e)-kappa_pdg,
                           eps_scan[i], eps_scan[i+1], xtol=1e-15)
            eps_crossings.append(eps_c)

print(f"\n  Scanning eps in [-1e-3, 1e-3]...")
print(f"  Found {len(eps_crossings)} crossing(s):")

for eps_c in eps_crossings:
    m_c = m_at_uvw1(eps_c)
    uvw_c, kappa_c = state_at(m_c, eps_c)
    d_c = S - eps_c
    print(f"\n  eps_0  = {eps_c:.15e}")
    print(f"  m_0    = {m_c:.15f}")
    print(f"  d_0=q_0= {d_c:.15f} (vs S = {S:.15f})")
    print(f"  uvw    = {uvw_c:.12f}  (should be 1)")
    print(f"  kappa  = {kappa_c:.15f}")
    print(f"  kappa_PDG = {kappa_pdg:.15f}")
    print(f"  kappa diff = {kappa_c - kappa_pdg:.4e}")
    check("uvw = 1 at 2D solution (1e-12)", abs(uvw_c-1)<1e-12, f"uvw-1={uvw_c-1:.2e}")
    check("kappa = kappa_PDG at 2D solution (1e-10)", abs(kappa_c-kappa_pdg)<1e-10,
          f"diff={kappa_c-kappa_pdg:.2e}")

# Pick the physical solution (eps > 0 or nearest)
if eps_crossings:
    eps_0 = eps_crossings[0]
    m_0 = m_at_uvw1(eps_0)
    d_0 = S - eps_0
else:
    print("  ERROR: no crossing found!")
    sys.exit(1)

print(f"\n  2D SOLUTION: m_0={m_0:.12f}, eps_0={eps_0:.12e}, d_0={d_0:.12f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: High-precision test of eps_0 against algebraic candidates
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 2: Precision test of eps_0 against candidate expressions")
print("="*80)

print(f"\n  eps_0 = {eps_0:.15e}")
print(f"  S     = {S:.15f}")

candidates = {
    "alpha_EM^2 / S":       ALPHA_EM**2 / S,
    "alpha_EM^2 * S":       ALPHA_EM**2 * S,
    "alpha_EM^2":           ALPHA_EM**2,
    "alpha_EM^2 / E1":      ALPHA_EM**2 / E1,
    "alpha_EM^2 * E1":      ALPHA_EM**2 * E1,
    "alpha_EM^2 / (4*pi)":  ALPHA_EM**2 / (4*math.pi),
    "alpha_EM^2 * S / 2":   ALPHA_EM**2 * S / 2,
    "alpha_EM * S / (40*pi)":   ALPHA_EM * S / (40*math.pi),
    "alpha_EM * S^2 / (40*pi)": ALPHA_EM * S**2 / (40*math.pi),
    "alpha_EM / (4*pi) * S^2":  ALPHA_EM/(4*math.pi) * S**2,
    "alpha_EM / (4*pi) * S^3":  ALPHA_EM/(4*math.pi) * S**3,
    "alpha_EM^2 / (2*S)":   ALPHA_EM**2 / (2*S),
    "alpha_EM^2 / (S^2)":   ALPHA_EM**2 / S**2,
    "alpha_EM^2 / (2*pi*S)": ALPHA_EM**2/(2*math.pi*S),
    "alpha_EM^2 * (D_P - S)": ALPHA_EM**2 * (D_P - S),
    "alpha_EM^2 * (S - Q_P)": ALPHA_EM**2 * (S - Q_P),
    "(D_P - S) * (S - Q_P) * alpha_EM": (D_P-S)*(S-Q_P)*ALPHA_EM,
    "alpha_EM * (D_P - Q_P)^2 / (4*pi)": ALPHA_EM*(D_P-Q_P)**2/(4*math.pi),
    "alpha_EM * (D_P*Q_P - S^2) / (2*S)": ALPHA_EM*(D_P*Q_P-S**2)/(2*S),
    "S^3 / (4*pi)":         S**3/(4*math.pi),
    "S^4 / (4*pi)":         S**4/(4*math.pi),
    "S^5 / E1":             S**5/E1,
    "alpha_EM^2 * (4/3)":   ALPHA_EM**2 * (4/3),
    "alpha_EM^2 * (3/2)":   ALPHA_EM**2 * (3/2),
    "alpha_EM^2 * 2 / S":   ALPHA_EM**2 * 2 / S,
    "(alpha_EM / (2*pi))^2": (ALPHA_EM/(2*math.pi))**2,
    "(alpha_EM / pi)^2":    (ALPHA_EM/math.pi)**2,
    "alpha_EM / (2*pi) * S^2": ALPHA_EM/(2*math.pi) * S**2,
}

best_ratio = float('inf')
best_name = ''
print(f"\n  Candidate comparisons (ratio = candidate/eps_0):")
for name, val in sorted(candidates.items(), key=lambda x: abs(x[1]/eps_0-1)):
    ratio = val/eps_0
    pct_err = (ratio - 1)*100
    marker = " ****" if abs(pct_err) < 1.0 else (" ***" if abs(pct_err) < 5 else "")
    print(f"    {name:45s} = {val:.4e}, ratio={ratio:.6f} ({pct_err:+.2f}%){marker}")
    if abs(pct_err) < abs((best_ratio-1)*100):
        best_ratio = ratio
        best_name = name

print(f"\n  Best match: {best_name} (ratio={best_ratio:.8f})")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: PSLQ-style integer relation search on eps_0 / alpha_EM^n / S^m
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 3: PSLQ-style rational search for eps_0")
print("="*80)

# Test: eps_0 = p/q * alpha_EM^a * S^b * E1^c * pi^d for small integers
# In log space: log(eps_0) = log(p/q) + a*log(alpha_EM) + b*log(S) + c*log(E1) + d*log(pi)
log_eps = math.log(abs(eps_0))
log_aEM = math.log(ALPHA_EM)
log_S = math.log(S)
log_E1 = math.log(E1)
log_pi = math.log(math.pi)
log_e  = 1.0  # log(e) = 1

print(f"\n  log(eps_0) = {log_eps:.8f}")
print(f"  Searching for a*log(aEM) + b*log(S) + c*log(E1) + d*log(pi) + log(n/m):")

best_score = float('inf')
best_combo = None
for a in range(0, 4):
    for b in range(-3, 4):
        for c in range(-2, 3):
            for d in range(-2, 3):
                val = a*log_aEM + b*log_S + c*log_E1 + d*log_pi
                residual = log_eps - val
                # Check if residual = log(rational) = log(p/q) for small p,q
                exp_res = math.exp(residual)  # should be rational
                for numer in range(1, 30):
                    for denom in range(1, 30):
                        if abs(exp_res - numer/denom) < 5e-4:
                            score = abs(exp_res - numer/denom)/exp_res
                            if score < best_score:
                                best_score = score
                                best_combo = (a, b, c, d, numer, denom)

if best_combo:
    a,b,c,d,n,m = best_combo
    expr = f"({n}/{m}) * alpha_EM^{a} * S^{b} * E1^{c} * pi^{d}"
    val = (n/m) * ALPHA_EM**a * S**b * E1**c * math.pi**d
    print(f"  Best: eps_0 ≈ {expr}")
    print(f"        = {val:.6e} vs eps_0 = {eps_0:.6e}  (ratio = {val/eps_0:.8f})")
    check("PSLQ match to 0.1%", abs(val/eps_0-1)<1e-3, f"ratio={val/eps_0:.8f}", "NUMERIC")
else:
    print("  No clean rational combination found.")

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: Characterize d_0 = S - eps_0 algebraically
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 4: Algebraic characterization of d_0 = S - eps_0")
print("="*80)

print(f"\n  d_0 = S - eps_0 = {d_0:.15f}")
print(f"  S              = {S:.15f}")
print(f"  d_0^2          = {d_0**2:.15f}")
print(f"  S^2 = 2/3      = {S**2:.15f}")
print(f"  d_0^2 - S^2    = {d_0**2 - S**2:.4e}")
print(f"  d_0 / S        = {d_0/S:.15f}")
print(f"  1 - d_0/S      = {1-d_0/S:.4e}")

# Test algebraic relations for d_0
candidates_d0 = {
    "S - alpha_EM^2/S": S - ALPHA_EM**2/S,
    "S*(1 - alpha_EM^2/S^2)": S*(1-ALPHA_EM**2/S**2),
    "S*(1 - 3*alpha_EM^2/2)": S*(1-3*ALPHA_EM**2/2),
    "sqrt(S^2 - alpha_EM^2)": math.sqrt(S**2-ALPHA_EM**2),
    "sqrt(2/3 - alpha_EM^2)": math.sqrt(2/3-ALPHA_EM**2),
    "S - alpha_EM^2/E1": S - ALPHA_EM**2/E1,
    "S*(1 - alpha_EM^2/E1^2)": S*(1-ALPHA_EM**2/E1**2),
}

print(f"\n  Candidate d_0 values:")
for name, val in candidates_d0.items():
    diff = d_0 - val
    print(f"    {name:40s} = {val:.12f}, d_0-val = {diff:.4e}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 5: Does (m_0, d_0) still satisfy eigenvalue Q = 2/3?
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 5: Eigenvalue Q = 2/3 check at (m_0, d_0)")
print("="*80)

H_2d = H3(m_0, d_0, d_0)
Q_eig_2d = eig_Q(H_2d)
print(f"\n  Q(eigenvalue) at (m_0, d_0, d_0) = {Q_eig_2d:.10f} (vs 2/3={2/3:.10f})")
print(f"  Q - 2/3 = {Q_eig_2d - 2/3:.4e}")

# Also slot Q (from koide_root_small construction)
x = expm(H_2d)
v2d=float(x[2,2].real); w2d=float(x[1,1].real); u2d=koide_root_small(v2d,w2d)
Q_slot_2d = (u2d**2+v2d**2+w2d**2) / (u2d+v2d+w2d)**2
print(f"  Q(slot) at (m_0, d_0, d_0)       = {Q_slot_2d:.10f}")
check("Q_slot = 2/3 exactly at 2D solution", abs(Q_slot_2d-2/3)<1e-10,
      f"Q_slot-2/3={Q_slot_2d-2/3:.2e}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 6: Does the beta_q23 identity hold at (m_0, d_0)?
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 6: beta_q23 identity at (m_0, d_0)")
print("="*80)

def get_bq23(H, lo=0.3, hi=4.0, N=8000):
    bs=np.linspace(lo,hi,N)
    from scipy.optimize import brentq as bq_
    for i in range(len(bs)-1):
        q0,q1=eig_Q(H,bs[i]),eig_Q(H,bs[i+1])
        if not(math.isnan(q0) or math.isnan(q1)) and (q0-2/3)*(q1-2/3)<0:
            return bq_(lambda b: eig_Q(H,b)-2/3, bs[i],bs[i+1], xtol=1e-14)
    return None

bq_2d = get_bq23(H_2d)
bq_p  = get_bq23(H_pmns)

print(f"\n  beta_q23 at (m_0, d_0, d_0) = {bq_2d}")
print(f"  beta_q23 at PMNS            = {bq_p:.12f}")
if bq_2d:
    ratio_2d = bq_2d / bq_p
    print(f"  ratio = {ratio_2d:.12f}")
    print(f"  S     = {S:.12f}")
    print(f"  ratio/S - 1 = {ratio_2d/S - 1:.4e}")
    check("Beta ratio = S at 2D solution (0.03%)", abs(ratio_2d/S-1)<3e-4,
          f"miss={ratio_2d/S-1:.2e}", "NUMERIC")

# ─────────────────────────────────────────────────────────────────────────────
# PART 7: NEW ROUTE — eigenvalue-based Koide Q on selected line
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 7: Eigenvalue-based Koide Q on selected line")
print("="*80)

print(f"\n  The slot-based Koide formula uses diagonal entries of exp(H).")
print(f"  The eigenvalue-based formula uses eigenvalues of exp(H) directly.")
print()

# What is the eigenvalue-based Q at m_prod1 on the original selected line?
m_prod1_ref = -1.160256656687
H_prod1 = H3(m_prod1_ref)
eigs_prod1 = np.sort(np.linalg.eigvalsh(expm(H_prod1)))
Q_eig_prod1 = np.sum(eigs_prod1) / (np.sum(np.sqrt(eigs_prod1)))**2
print(f"  Eigenvalues of exp(H_sel(m_prod1)): {eigs_prod1}")
print(f"  Eigenvalue-based Q                : {Q_eig_prod1:.8f} (vs slot 2/3 = 0.66667)")
print(f"  Difference from 2/3               : {Q_eig_prod1-2/3:.4e}")

# Is there an m where the EIGENVALUE-based Q = 2/3?
ms = np.linspace(-1.30, -0.90, 4000)
Q_eig_vals = []
for m in ms:
    e=np.linalg.eigvalsh(expm(H3(m)))
    e=np.sort(e)
    if np.any(e<=0):
        Q_eig_vals.append(float('nan'))
        continue
    Q_eig_vals.append(float(np.sum(e)/(np.sum(np.sqrt(e)))**2))

eig_Koide_m = None
for i in range(len(ms)-1):
    if not math.isnan(Q_eig_vals[i]) and not math.isnan(Q_eig_vals[i+1]):
        if (Q_eig_vals[i]-2/3)*(Q_eig_vals[i+1]-2/3) < 0:
            m_c = brentq(lambda m: float(np.sum(np.sort(np.linalg.eigvalsh(expm(H3(m)))))
                         /np.sum(np.sqrt(np.abs(np.linalg.eigvalsh(expm(H3(m))))))**2-2/3),
                         ms[i], ms[i+1], xtol=1e-12)
            print(f"  Eigenvalue Q=2/3 at m = {m_c:.10f}")
            print(f"    kappa_sel = {(lambda v,w: (v-w)/(v+w))(*[float(expm(H3(m_c))[k,k].real) for k in [2,1]]):.10f}")
            print(f"    dist from m_prod1 = {m_c - m_prod1_ref:.4e}")
            print(f"    dist from m_star  = {m_c - (-1.160468686316):.4e}")
            eig_Koide_m = m_c
            break

if eig_Koide_m is None:
    print(f"  No eigenvalue Q=2/3 crossing found in [{ms[0]:.2f},{ms[-1]:.2f}]")
    print(f"  Q_eig at m_prod1 = {Q_eig_prod1:.6f}, at m={ms[0]:.2f}: {Q_eig_vals[0]:.6f}, m={ms[-1]:.2f}: {Q_eig_vals[-1]:.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 8: PMNS feedback coupling — does asymmetry (D_P-Q_P) induce eps_0?
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 8: PMNS feedback — does (D_P - Q_P) × coupling → eps_0?")
print("="*80)

dDQ = D_P - Q_P     # 0.2188 — asymmetry between D and Q at PMNS
sumDQ = D_P + Q_P   # 1.6488
avgDQ = (D_P + Q_P)/2  # 0.8244

print(f"\n  D_P - Q_P = {dDQ:.8f}")
print(f"  D_P + Q_P = {sumDQ:.8f}")
print(f"  D_P * Q_P = {D_P*Q_P:.8f} (vs S^2 = {S**2:.8f})")
print(f"  D_P*Q_P - S^2 = {D_P*Q_P - S**2:.4e}")
print(f"  eps_0     = {eps_0:.8e}")

# Candidates from PMNS asymmetry
candidates_pmns = {
    "alpha_EM * (D_P-Q_P)^2 / (4*pi)": ALPHA_EM*(D_P-Q_P)**2/(4*math.pi),
    "alpha_EM * (D_P-Q_P)^2 / (2*pi)": ALPHA_EM*(D_P-Q_P)**2/(2*math.pi),
    "alpha_EM * (D_P*Q_P - S^2) / (2*S)": ALPHA_EM*(D_P*Q_P-S**2)/(2*S),
    "(D_P*Q_P - S^2)^2 / (2*S)": (D_P*Q_P-S**2)**2/(2*S),
    "alpha_EM * (D_P*Q_P - S^2)": ALPHA_EM*(D_P*Q_P-S**2),
    "alpha_EM^2 * (D_P - S) / S": ALPHA_EM**2*(D_P-S)/S,
    "alpha_EM^2 * (S - Q_P) / S": ALPHA_EM**2*(S-Q_P)/S,
    "(D_P-S)*(S-Q_P)*S": (D_P-S)*(S-Q_P)*S,
    "alpha_EM * |D_P-S| * |S-Q_P| / S": ALPHA_EM*abs(D_P-S)*abs(S-Q_P)/S,
    "S * (D_P/Q_P - 1)^2 / (4*pi)": S*(D_P/Q_P-1)**2/(4*math.pi),
    "S * (1 - Q_P/D_P)^2 / (4*pi)": S*(1-Q_P/D_P)**2/(4*math.pi),
    "alpha_EM^2 / (1 + D_P*Q_P)": ALPHA_EM**2/(1+D_P*Q_P),
    "alpha_EM^2 * D_P*Q_P / S": ALPHA_EM**2*D_P*Q_P/S,
}

print(f"\n  PMNS-derived candidates:")
for name, val in sorted(candidates_pmns.items(), key=lambda x: abs(x[1]/eps_0-1)):
    ratio = val/eps_0
    pct_err = (ratio-1)*100
    marker = " ****" if abs(pct_err)<1 else (" ***" if abs(pct_err)<5 else "")
    print(f"    {name:50s} = {val:.4e}, ratio={ratio:.5f} ({pct_err:+.2f}%){marker}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 9: Systematic ratio scan — eps_0 / alpha_EM^a * S^b * E1^c * pi^d
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 9: Systematic ratio scan")
print("="*80)

print(f"\n  eps_0 = {eps_0:.12e}")
print(f"  Scanning all a in [0,3], b in [-4,4], c in [-2,2], d in [-2,2]:")

matches = []
for a in range(0, 4):
    for b in range(-4, 5):
        for c in range(-2, 3):
            for d in range(-2, 3):
                val = ALPHA_EM**a * S**b * E1**c * math.pi**d
                if val <= 0: continue
                ratio = eps_0 / val
                if 0.5 < ratio < 10:
                    # Check if ratio is close to a small rational
                    for n in range(1, 30):
                        for m_int in range(1, 30):
                            if abs(ratio - n/m_int) < 1e-3:
                                total_err = abs(ratio - n/m_int)/ratio
                                if total_err < 5e-3:
                                    matches.append((total_err, a, b, c, d, n, m_int,
                                                    val*(n/m_int)))

matches.sort()
print(f"\n  Top matches (eps_0 ≈ (n/m) * alpha_EM^a * S^b * E1^c * pi^d):")
shown = set()
for err, a, b, c, d, n, m_int, val in matches[:20]:
    key = (a,b,c,d,n,m_int)
    if key in shown: continue
    shown.add(key)
    expr_parts = []
    if n != m_int: expr_parts.append(f"{n}/{m_int}")
    if a: expr_parts.append(f"aEM^{a}")
    if b: expr_parts.append(f"S^{b}")
    if c: expr_parts.append(f"E1^{c}")
    if d: expr_parts.append(f"pi^{d}")
    expr = " * ".join(expr_parts) if expr_parts else "1"
    pct = (val/eps_0-1)*100
    print(f"    {expr:45s} = {val:.6e}, ratio={val/eps_0:.8f} ({pct:+.3f}%)")
    if abs(pct) < 0.1:
        check(f"eps_0 = {expr} to 0.1%", True, f"err={pct:+.3f}%", "NUMERIC")

# ─────────────────────────────────────────────────────────────────────────────
# PART 10: Assumptions audit — what new routes does this reveal?
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 10: Assumptions audit after 2D intersection")
print("="*80)

print(f"""
  NEW FACTS:
    eps_0 = {eps_0:.8e}  (the departure from S that closes both gaps simultaneously)
    m_0   = {m_0:.10f}  (the m value with uvw=1 AND kappa=kappa_PDG)
    d_0   = {d_0:.10f}  (the new d=q value, vs S = {S:.10f})
    eps_0/alpha_EM^2 = {eps_0/ALPHA_EM**2:.8f}
    eps_0*S/alpha_EM^2 = {eps_0*S/ALPHA_EM**2:.8f}
    eps_0/(alpha_EM^2/S) = {eps_0/(ALPHA_EM**2/S):.8f}

  ASSUMPTION A: d=q=S is the EXACT two-axiom prediction
    WHAT IF: d=q=S is the TREE-LEVEL prediction but there are loop corrections?
    DIRECTION: In a QFT context, the selected-line equilibrium d=q=S could
    receive radiative corrections from the charged-lepton sector. The leading
    correction would be of order alpha_EM^2 times a geometric factor.
    → IF eps_0 ≈ alpha_EM^2/S exactly, this is the "smoking gun" for radiative
       corrections from the U(1)_Y gauge sector.

  ASSUMPTION B: The 2D solution (m_0, d_0) is the physical point
    WHAT IF: Some additional condition selects (m_0, d_0) over (m_prod1, S)?
    DIRECTION: Is (m_0, d_0) the minimum of some effective potential in (m, d)?

  ASSUMPTION C: Cl(3)/Z^3 is the complete framework at tree level
    WHAT IF: There are alpha_EM^2 radiative corrections to the selected line?
    DIRECTION: Study the one-loop effective action for the (d,q) flat direction.
    The flat direction d=q is lifted at order alpha_EM (one loop) or alpha_EM^2
    (two loops) depending on the symmetry structure.

  ASSUMPTION D: The beta_q23 identity and kappa gap are separate problems
    WHAT IF: They're both manifestations of the SAME alpha_EM^2 correction?
    The beta ratio gap (3.05e-4) and the kappa gap (4.82e-5) might both be
    resolved by d=q = S - eps_0 with eps_0 = alpha_EM^2/S.
    → The ratio 3.05e-4 / 4.82e-5 ≈ 6.3. And 1/S ≈ 1.22. Hmm.

  KEY OPEN QUESTION: Is eps_0 = alpha_EM^2 / S exactly?
    Current precision: eps_0/(alpha_EM^2/S) = {eps_0/(ALPHA_EM**2/S):.8f}
    If this ratio = 1 exactly, we have found the mechanism.
""")

# ─────────────────────────────────────────────────────────────────────────────
# FINAL
# ─────────────────────────────────────────────────────────────────────────────
print("="*80)
print(f"FINAL: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
print("="*80)
print(f"\n  SUMMARY:")
print(f"    eps_0 = {eps_0:.15e}")
print(f"    alpha_EM^2/S = {ALPHA_EM**2/S:.15e}")
print(f"    ratio = {eps_0/(ALPHA_EM**2/S):.12f}")
print(f"    diff  = {eps_0 - ALPHA_EM**2/S:.4e}  ({(eps_0/(ALPHA_EM**2/S)-1)*100:.4f}%)")
