#!/usr/bin/env python3
"""
Koide gap exhaustive attack
============================
All remaining routes to close the gap between m_prod1 (u*v*w=1) and m* (PDG-optimal).

  kappa(m_prod1) = -0.607961050,  kappa_PDG = -0.607912839
  Delta_kappa = 4.82e-5,          Delta_m   = 2.19e-4

ASSUMPTION AUDIT governs this investigation. At each wall: list assumptions,
ask "what if wrong", follow new directions.

PARTS:
  1  — PDG m_tau measurement uncertainty: does Delta_kappa fall within error bars?
  2  — PMNS angle uncertainty: does the beta_q23 gap fall within NuFit errors?
  3  — J3 = Tr(H^3) cross-sector crossing
  4  — J4 = Tr(H^4) cross-sector crossing
  5  — det(H) cross-sector crossing
  6  — Frobenius distance argmin: ||H_PMNS - H_sel(m)||
  7  — Commutator minimization: argmin ||[H_PMNS, H_sel(m)]||
  8  — Cross-sector trace inner products
  9  — Off-selected-line: what (d,q) near (S,S) closes the gap at m_prod1?
 10  — Spectral crossing: H_sel(m) eigenvalue = H_PMNS eigenvalue
 11  — J3/J2 normalised ratio cross-sector
 12  — m_exact algebraic characterisation (where beta ratio = S exactly)
 13  — Scalar potential gradient: V'(m)=0 and second-order extrema
 14  — The kappa dispersion: sensitivity of kappa_PDG to each PDG mass
 15  — FINAL AUDIT: assumptions list, new routes revealed
"""

from __future__ import annotations
import math, sys

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, minimize_scalar, minimize

GAMMA=0.5; E1=math.sqrt(8/3); E2=math.sqrt(8)/3
SQRT3=math.sqrt(3); SQRT6=math.sqrt(6); S=SQRT6/3

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
PDG_M_TAU_ERR = 0.12   # MeV, 1-sigma

def koide_root_small(v, w):
    rad=math.sqrt(3*(v*v+4*v*w+w*w)); return 2*(v+w)-rad

def kappa_from_slots(v, w):
    return (v-w)/(v+w)

def selected_line_slots(m):
    x=expm(H3(m)); return float(x[2,2].real), float(x[1,1].real)

def kappa_sel(m):
    v,w=selected_line_slots(m); return kappa_from_slots(v,w)

def kappa_pdg_from_masses(me, mmu, mtau):
    """Koide-cone projection κ from given masses."""
    sqrt_masses = np.sqrt([me, mmu, mtau])
    dir_ = sqrt_masses / np.linalg.norm(sqrt_masses)
    def koide_amp(kappa):
        v0=1.0; w=v0*(1-kappa)/(1+kappa)
        if w<=0: return None
        u=koide_root_small(v0, w)
        if u<=0: return None
        return np.array([u,v0,w])
    def neg_cos(kappa):
        amp=koide_amp(kappa)
        if amp is None: return 1.0
        return -float(np.dot(amp/np.linalg.norm(amp), dir_))
    res=minimize_scalar(neg_cos, bounds=(-0.9999,-0.0001), method='bounded',
                        options={'xatol':1e-14})
    return float(res.x)

def eig_Q(H, beta):
    e=np.linalg.eigvalsh(expm(beta*H))
    if np.any(e<=0): return float('nan')
    s=float(np.sum(e)); rs=float(np.sum(np.sqrt(e)))
    return s/(rs*rs)

def get_bq23(H, lo=0.3, hi=4.0, N=8000):
    bs=np.linspace(lo,hi,N)
    for i in range(len(bs)-1):
        q0,q1=eig_Q(H,bs[i]),eig_Q(H,bs[i+1])
        if not(math.isnan(q0) or math.isnan(q1)) and (q0-2/3)*(q1-2/3)<0:
            return brentq(lambda b: eig_Q(H,b)-2/3, bs[i],bs[i+1], xtol=1e-14)
    return None

# Pre-compute key fixed quantities
m_prod1_approx = -1.160468640   # u*v*w=1 from prior scripts
kappa_prod1 = kappa_sel(m_prod1_approx)
kappa_pdg_central = kappa_pdg_from_masses(*PDG_MEV)

# Find m_star where kappa_sel(m) = kappa_pdg_central
m_star = brentq(lambda m: kappa_sel(m)-kappa_pdg_central, -1.165, -1.155, xtol=1e-14)

# Find precise m_prod1 by requiring u*v*w=1
def uvw_product(m):
    v,w=selected_line_slots(m)
    u=koide_root_small(v,w)
    return u*v*w-1.0

try:
    m_prod1 = brentq(uvw_product, -1.165, -1.155, xtol=1e-14)
except:
    m_prod1 = m_prod1_approx
kappa_prod1 = kappa_sel(m_prod1)

print(f"\nReference values:")
print(f"  m_prod1       = {m_prod1:.12f}  (u*v*w=1)")
print(f"  m_star        = {m_star:.12f}  (kappa=kappa_PDG)")
print(f"  Delta_m       = {m_star-m_prod1:.4e}")
print(f"  kappa_prod1   = {kappa_prod1:.15f}")
print(f"  kappa_PDG     = {kappa_pdg_central:.15f}")
print(f"  Delta_kappa   = {kappa_prod1-kappa_pdg_central:.4e}")

PASS_COUNT=0; FAIL_COUNT=0
def check(name, cond, detail='', kind='EXACT'):
    global PASS_COUNT, FAIL_COUNT
    PASS_COUNT+=cond; FAIL_COUNT+=(not cond)
    tag=f' [{kind}]' if kind!='EXACT' else ''
    print(f'  [{"PASS" if cond else "FAIL"}]{tag} {name}'+(f'  ({detail})' if detail else ''))
    return cond

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: PDG m_tau measurement uncertainty
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 1: PDG m_tau measurement uncertainty")
print("="*80)

me,mmu,mtau = PDG_MEV
dk_dm_tau_fwd = (kappa_pdg_from_masses(me,mmu,mtau+0.001) - kappa_pdg_central)/0.001
dk_dm_tau_bwd = (kappa_pdg_central - kappa_pdg_from_masses(me,mmu,mtau-0.001))/0.001
dk_dm_tau = (dk_dm_tau_fwd + dk_dm_tau_bwd)/2

delta_kappa_gap = kappa_prod1 - kappa_pdg_central
delta_mtau_needed = delta_kappa_gap / dk_dm_tau
sigma_equiv = abs(delta_mtau_needed) / PDG_M_TAU_ERR

print(f"\n  kappa_PDG sensitivity: d(kappa)/d(m_tau) = {dk_dm_tau:.6e} /MeV")
print(f"  Delta_kappa gap       = {delta_kappa_gap:.4e}")
print(f"  m_tau shift to close  = {delta_mtau_needed:.4f} MeV")
print(f"  PDG m_tau uncertainty = ±{PDG_M_TAU_ERR:.3f} MeV (1sigma)")
print(f"  Equivalent sigma      = {sigma_equiv:.2f}σ")
print()

# Compute kappa_PDG at +/- 1,2 sigma
for nsigma in [0.5, 1.0, 1.5, 2.0, 2.5]:
    for sign, label in [(+1, '+'), (-1, '-')]:
        mtau_shifted = mtau + sign*nsigma*PDG_M_TAU_ERR
        kappa_shifted = kappa_pdg_from_masses(me, mmu, mtau_shifted)
        dk = kappa_shifted - kappa_pdg_central
        relative_closure = dk / delta_kappa_gap
        if sign == -1:
            print(f"  m_tau {label}{nsigma}σ: kappa_PDG = {kappa_shifted:.9f}, "
                  f"d(kappa)={dk:+.3e}, closes {relative_closure*100:.1f}% of gap")

print()
check("Gap closed by m_tau at 1-sigma",
      abs(sigma_equiv) <= 1.0, f"sigma={sigma_equiv:.2f}", "NUMERIC")
check("Gap closed by m_tau at 2-sigma",
      abs(sigma_equiv) <= 2.0, f"sigma={sigma_equiv:.2f}", "NUMERIC")
check("Gap closed by m_tau at 3-sigma",
      abs(sigma_equiv) <= 3.0, f"sigma={sigma_equiv:.2f}", "NUMERIC")

# Also check sensitivity to m_mu
dk_dm_mu = (kappa_pdg_from_masses(me,mmu+0.001,mtau) - kappa_pdg_central)/0.001
dm_mu_needed = delta_kappa_gap / dk_dm_mu
print(f"\n  For comparison, mu shift to close: {dm_mu_needed:.4f} MeV "
      f"(PDG error ±0.0023 MeV → {abs(dm_mu_needed)/0.0023:.0f}σ)")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: PMNS angle uncertainty and beta_q23 gap
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 2: PMNS parameter uncertainty and beta_q23 gap")
print("="*80)

bq_k = get_bq23(H3(m_prod1))
bq_p = get_bq23(H_pmns)
beta_ratio = bq_k / bq_p
gap_beta = beta_ratio/S - 1

print(f"\n  beta_q23(Koide,m_prod1) = {bq_k:.12f}")
print(f"  beta_q23(PMNS)          = {bq_p:.12f}")
print(f"  ratio/SELECTOR - 1      = {gap_beta:.4e}  ({gap_beta*100:.4f}%)")

# Find D_P shift that closes the ratio gap
def beta_ratio_from_D(D_shift):
    H_p_shifted = H3(M_P, D_P + D_shift, Q_P)
    bq = get_bq23(H_p_shifted)
    if bq is None: return float('nan')
    return bq_k / bq / S - 1

# Find D_P shift that gives ratio = S
try:
    D_shift_close = brentq(beta_ratio_from_D, -0.005, 0.005, xtol=1e-10)
    D_frac_shift = D_shift_close/D_P
except:
    D_shift_close = float('nan')
    D_frac_shift = float('nan')

print(f"\n  D_P shift to close beta ratio: {D_shift_close:.5f} ({D_frac_shift*100:.3f}%)")
print(f"  PDG m_tau uncertainty maps to D_P uncertainty...")

# NuFit theta_13 uncertainty: sin^2(theta_13) = 0.0222 ± 0.0007 (~3.2%)
# theta_13 maps to D_P via the PMNS eigenvalue structure
# Rough estimate: delta(theta_13)/theta_13 ~ 10% => delta(D_P) ~ few %
# The 0.19% shift is well within this
theta13_frac_err = 0.032   # 3.2% uncertainty in sin^2(theta_13)
print(f"  NuFit sin²theta_13 uncertainty ≈ {theta13_frac_err*100:.1f}%")
print(f"  Required D_P fractional shift   = {D_frac_shift*100:.3f}%")
if not math.isnan(D_frac_shift):
    D_sigma_equiv = abs(D_frac_shift)/theta13_frac_err
    print(f"  Equivalent sigma (theta_13)     = {D_sigma_equiv:.2f}σ")
    check("Beta ratio gap within NuFit theta_13 uncertainties (2-sigma)",
          D_sigma_equiv <= 2.0, f"equiv={D_sigma_equiv:.2f}sigma", "NUMERIC")
    check("Beta ratio gap within NuFit theta_13 uncertainties (1-sigma)",
          D_sigma_equiv <= 1.0, f"equiv={D_sigma_equiv:.2f}sigma", "NUMERIC")

# Also check Q_P sensitivity
def beta_ratio_from_Q(Q_shift):
    H_p_shifted = H3(M_P, D_P, Q_P + Q_shift)
    bq = get_bq23(H_p_shifted)
    if bq is None: return float('nan')
    return bq_k / bq / S - 1

try:
    Q_shift_close = brentq(beta_ratio_from_Q, -0.005, 0.005, xtol=1e-10)
    Q_frac_shift = Q_shift_close/Q_P
    print(f"\n  Alternatively: Q_P shift = {Q_shift_close:.5f} ({Q_frac_shift*100:.3f}%)")
except:
    pass

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: J3 = Tr(H^3) cross-sector crossing
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 3: J3 = Tr(H^3) cross-sector crossing")
print("="*80)

J3_pmns = float(np.real(np.trace(np.linalg.matrix_power(H_pmns, 3))))
print(f"\n  J3(H_PMNS) = {J3_pmns:.10f}")

def J3_sel(m):
    H=H3(m); return float(np.real(np.trace(H @ H @ H)))

# Scan
ms = np.linspace(-1.30, -0.90, 2000)
J3_vals = [J3_sel(m) - J3_pmns for m in ms]
J3_crossings = []
for i in range(len(ms)-1):
    if J3_vals[i]*J3_vals[i+1] < 0:
        m_c = brentq(lambda m: J3_sel(m)-J3_pmns, ms[i], ms[i+1], xtol=1e-12)
        J3_crossings.append(m_c)

print(f"  J3_sel crossing(s) with J3_PMNS:")
for m_c in J3_crossings:
    dist_prod1 = m_c - m_prod1
    dist_star  = m_c - m_star
    kappa_c = kappa_sel(m_c)
    dk = kappa_c - kappa_pdg_central
    print(f"    m_J3 = {m_c:.10f}, dist_from_m_prod1={dist_prod1:.4e}, "
          f"dist_from_m*={dist_star:.4e}, kappa_diff={dk:.4e}")
    check("J3 crossing at m_prod1 (within 1e-3)",
          abs(dist_prod1) < 1e-3, f"dist={abs(dist_prod1):.4e}", "NUMERIC")
    check("J3 crossing at m_star (within 1e-3)",
          abs(dist_star) < 1e-3, f"dist={abs(dist_star):.4e}", "NUMERIC")

if not J3_crossings:
    print("  No J3 crossing found in scan range.")
    # Show values at key points
    print(f"  J3_sel(m_prod1) = {J3_sel(m_prod1):.6f}, J3_PMNS = {J3_pmns:.6f}, "
          f"diff = {J3_sel(m_prod1)-J3_pmns:.4e}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: J4 = Tr(H^4) cross-sector crossing
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 4: J4 = Tr(H^4) cross-sector crossing")
print("="*80)

J4_pmns = float(np.real(np.trace(np.linalg.matrix_power(H_pmns, 4))))
print(f"\n  J4(H_PMNS) = {J4_pmns:.10f}")

def J4_sel(m):
    H=H3(m); H2=H@H; return float(np.real(np.trace(H2@H2)))

J4_vals = [J4_sel(m)-J4_pmns for m in ms]
J4_crossings = []
for i in range(len(ms)-1):
    if J4_vals[i]*J4_vals[i+1] < 0:
        m_c = brentq(lambda m: J4_sel(m)-J4_pmns, ms[i], ms[i+1], xtol=1e-12)
        J4_crossings.append(m_c)

print(f"  J4_sel crossing(s) with J4_PMNS:")
for m_c in J4_crossings:
    dist_prod1 = m_c - m_prod1
    dist_star  = m_c - m_star
    kappa_c = kappa_sel(m_c)
    dk = kappa_c - kappa_pdg_central
    print(f"    m_J4 = {m_c:.10f}, dist_from_m_prod1={dist_prod1:.4e}, "
          f"dist_from_m*={dist_star:.4e}, kappa_diff={dk:.4e}")

if not J4_crossings:
    print(f"  J4_sel(m_prod1) = {J4_sel(m_prod1):.6f}, J4_PMNS = {J4_pmns:.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 5: det(H) cross-sector crossing
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 5: det(H) cross-sector crossing")
print("="*80)

det_pmns = float(np.real(np.linalg.det(H_pmns)))
print(f"\n  det(H_PMNS) = {det_pmns:.10f}")

def det_sel(m):
    return float(np.real(np.linalg.det(H3(m))))

det_vals = [det_sel(m)-det_pmns for m in ms]
det_crossings = []
for i in range(len(ms)-1):
    if det_vals[i]*det_vals[i+1] < 0:
        m_c = brentq(lambda m: det_sel(m)-det_pmns, ms[i], ms[i+1], xtol=1e-12)
        det_crossings.append(m_c)

print(f"  det(H_sel) crossing(s) with det(H_PMNS):")
for m_c in det_crossings:
    dist_prod1 = m_c - m_prod1
    dist_star  = m_c - m_star
    kappa_c = kappa_sel(m_c)
    dk = kappa_c - kappa_pdg_central
    print(f"    m_det = {m_c:.10f}, dist_from_m_prod1={dist_prod1:.4e}, "
          f"dist_from_m*={dist_star:.4e}, kappa_diff={dk:.4e}")
    check("det crossing near m* (within 1e-3)",
          abs(dist_star) < 1e-3, f"dist={abs(dist_star):.4e}", "NUMERIC")

if not det_crossings:
    print(f"  det_sel(m_prod1) = {det_sel(m_prod1):.6f}, det_PMNS = {det_pmns:.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 6: Frobenius distance argmin: ||H_PMNS - H_sel(m)||_F
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 6: Frobenius distance argmin")
print("="*80)

def frob_dist(m):
    diff = H_pmns - H3(m)
    return float(np.real(np.trace(diff.conj().T @ diff)))

# Find minimum
res = minimize_scalar(frob_dist, bounds=(-2.0, 0.0), method='bounded',
                      options={'xatol':1e-12})
m_frob = float(res.x)
dist_frob = float(res.fun)

print(f"\n  argmin_m ||H_PMNS - H_sel(m)||_F = {m_frob:.10f}")
print(f"  Min Frobenius distance²           = {dist_frob:.6f}")
print(f"  Distance from m_prod1             = {m_frob - m_prod1:.4e}")
print(f"  Distance from m_star              = {m_frob - m_star:.4e}")
kappa_frob = kappa_sel(m_frob)
print(f"  kappa at m_frob                   = {kappa_frob:.9f}")
print(f"  kappa diff from PDG               = {kappa_frob - kappa_pdg_central:.4e}")
check("Frobenius min near m_star (within 1e-2)",
      abs(m_frob - m_star) < 1e-2, f"dist={abs(m_frob-m_star):.4e}", "NUMERIC")

# ─────────────────────────────────────────────────────────────────────────────
# PART 7: Commutator minimization: ||[H_PMNS, H_sel(m)]||_F
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 7: Commutator minimization")
print("="*80)

def commutator_norm(m):
    H=H3(m); C=H_pmns@H-H@H_pmns
    return float(np.real(np.trace(C.conj().T@C)))

# Dense scan first
comm_vals = [commutator_norm(m) for m in ms]
m_comm_min_scan = ms[int(np.argmin(comm_vals))]
res = minimize_scalar(commutator_norm, bounds=(m_comm_min_scan-0.1, m_comm_min_scan+0.1),
                      method='bounded', options={'xatol':1e-12})
m_comm = float(res.x)
comm_min = float(res.fun)

print(f"\n  argmin_m ||[H_PMNS, H_sel(m)]||_F = {m_comm:.10f}")
print(f"  Min ||commutator||_F²              = {comm_min:.6f}")
print(f"  Distance from m_prod1              = {m_comm - m_prod1:.4e}")
print(f"  Distance from m_star               = {m_comm - m_star:.4e}")
kappa_comm = kappa_sel(m_comm)
print(f"  kappa at m_comm                    = {kappa_comm:.9f}")
print(f"  kappa diff from PDG                = {kappa_comm - kappa_pdg_central:.4e}")
check("Commutator min near m_star (within 1e-2)",
      abs(m_comm - m_star) < 1e-2, f"dist={abs(m_comm-m_star):.4e}", "NUMERIC")

# ─────────────────────────────────────────────────────────────────────────────
# PART 8: Cross-sector trace inner products
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 8: Cross-sector trace inner products")
print("="*80)

def trace_ip(m):
    H=H3(m)
    return float(np.real(np.trace(H_pmns @ H)))

def trace_ip2(m):
    H=H3(m)
    return float(np.real(np.trace(H_pmns @ H @ H)))

def trace_ip3(m):
    H=H3(m)
    return float(np.real(np.trace(H_pmns @ H_pmns @ H)))

# Find extrema of each
res1 = minimize_scalar(lambda m: -trace_ip(m), bounds=(-2.0,0.0), method='bounded',
                       options={'xatol':1e-12})
m_ip1 = float(res1.x)
res2 = minimize_scalar(lambda m: -trace_ip2(m), bounds=(-2.0,0.0), method='bounded',
                       options={'xatol':1e-12})
m_ip2 = float(res2.x)
res3 = minimize_scalar(lambda m: -trace_ip3(m), bounds=(-2.0,0.0), method='bounded',
                       options={'xatol':1e-12})
m_ip3 = float(res3.x)

print(f"\n  argmax_m Tr(H_PMNS H_sel)    = {m_ip1:.10f}, dist_m*={m_ip1-m_star:.4e}")
print(f"  argmax_m Tr(H_PMNS H_sel^2)  = {m_ip2:.10f}, dist_m*={m_ip2-m_star:.4e}")
print(f"  argmax_m Tr(H_PMNS^2 H_sel)  = {m_ip3:.10f}, dist_m*={m_ip3-m_star:.4e}")

# Also find where Tr(H_PMNS H_sel) = 0 crossing
ip_vals = [trace_ip(m) for m in ms]
ip_crossings = []
for i in range(len(ms)-1):
    if ip_vals[i]*ip_vals[i+1] < 0:
        m_c = brentq(trace_ip, ms[i], ms[i+1], xtol=1e-12)
        ip_crossings.append(m_c)
if ip_crossings:
    print(f"  Tr(H_PMNS H_sel)=0 at m={ip_crossings}")

# Check if Tr(H_PMNS H_sel) has a clean value at m_prod1 or m_star
ip_prod1 = trace_ip(m_prod1)
ip_star  = trace_ip(m_star)
J2_pmns  = float(np.real(np.trace(H_pmns @ H_pmns)))
print(f"\n  Tr(H_PMNS H_sel(m_prod1)) = {ip_prod1:.8f}")
print(f"  Tr(H_PMNS H_sel(m_star))  = {ip_star:.8f}")
print(f"  Tr(H_PMNS^2)              = {J2_pmns:.8f}")
print(f"  Ratio ip/J2 at m_prod1    = {ip_prod1/J2_pmns:.8f} (vs S={S:.8f})")
print(f"  Ratio ip/J2 at m_star     = {ip_star/J2_pmns:.8f} (vs S={S:.8f})")

# ─────────────────────────────────────────────────────────────────────────────
# PART 9: Off-selected-line correction
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 9: Off-selected-line correction — what (d,q) closes gap at m_prod1?")
print("="*80)

print(f"\n  On the selected line: d=q=S={S:.8f} exactly (two-axiom symmetry)")
print(f"  Question: what departure from d=q=S closes kappa_gap at m=m_prod1?")
print()

def kappa_offsel(delta_d, delta_q, m=None):
    """kappa at (m, S+dd, S+dq) via slot formula."""
    if m is None: m = m_prod1
    x=expm(H3(m, S+delta_d, S+delta_q))
    v,w=float(x[2,2].real), float(x[1,1].real)
    return kappa_from_slots(v,w)

# Fix delta_d = 0, vary delta_q
dq_range = np.linspace(-0.01, 0.01, 500)
kappa_offs = [kappa_offsel(0, dq) for dq in dq_range]
dq_crossings = []
for i in range(len(dq_range)-1):
    if (kappa_offs[i]-kappa_pdg_central)*(kappa_offs[i+1]-kappa_pdg_central) < 0:
        dq_c = brentq(lambda dq: kappa_offsel(0,dq)-kappa_pdg_central,
                      dq_range[i], dq_range[i+1], xtol=1e-12)
        dq_crossings.append(dq_c)

if dq_crossings:
    for dq_c in dq_crossings:
        print(f"  delta_q (with delta_d=0) closing gap: dq={dq_c:.6f} ({dq_c/S*100:.4f}% of S)")
        check("Off-sel correction small (|dq/S| < 1%)",
              abs(dq_c/S) < 0.01, f"|dq/S|={abs(dq_c/S)*100:.4f}%", "NUMERIC")

# Symmetric departure: delta_d = delta_q = epsilon
eps_range = np.linspace(-0.005, 0.005, 500)
kappa_sym = [kappa_offsel(e,e) for e in eps_range]
sym_crossings = []
for i in range(len(eps_range)-1):
    if (kappa_sym[i]-kappa_pdg_central)*(kappa_sym[i+1]-kappa_pdg_central) < 0:
        e_c = brentq(lambda e: kappa_offsel(e,e)-kappa_pdg_central,
                     eps_range[i], eps_range[i+1], xtol=1e-12)
        sym_crossings.append(e_c)

if sym_crossings:
    for e_c in sym_crossings:
        print(f"  Symmetric departure (delta_d=delta_q) closing gap: eps={e_c:.6f} ({e_c/S*100:.4f}% of S)")
        print(f"  New d=q = {S+e_c:.8f} vs S={S:.8f}")

# What if d and q are not exactly equal? Antisymmetric departure: delta_d = -delta_q
antisym_crossings = []
kappa_antisym = [kappa_offsel(e,-e) for e in eps_range]
for i in range(len(eps_range)-1):
    if (kappa_antisym[i]-kappa_pdg_central)*(kappa_antisym[i+1]-kappa_pdg_central) < 0:
        e_c = brentq(lambda e: kappa_offsel(e,-e)-kappa_pdg_central,
                     eps_range[i], eps_range[i+1], xtol=1e-12)
        antisym_crossings.append(e_c)

if antisym_crossings:
    for e_c in antisym_crossings:
        print(f"  Antisymmetric departure (delta_d=-delta_q): eps={e_c:.6f} ({e_c/S*100:.4f}% of S)")

# ─────────────────────────────────────────────────────────────────────────────
# PART 10: Spectral crossing — H_sel eigenvalue = H_PMNS eigenvalue
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 10: Spectral crossing — when do H_sel(m) eigenvalues match H_PMNS?")
print("="*80)

eigs_pmns = np.sort(np.linalg.eigvalsh(H_pmns))
print(f"\n  H_PMNS eigenvalues: {eigs_pmns}")

for k, lam_target in enumerate(eigs_pmns):
    def eig_diff(m):
        return np.sort(np.linalg.eigvalsh(H3(m)))[k] - lam_target
    eig_cross = []
    eig_v = [eig_diff(m) for m in ms]
    for i in range(len(ms)-1):
        if eig_v[i]*eig_v[i+1] < 0:
            m_c = brentq(eig_diff, ms[i], ms[i+1], xtol=1e-12)
            eig_cross.append(m_c)
    print(f"  eig[{k}]={lam_target:.5f} crossing(s): ", end='')
    if eig_cross:
        for m_c in eig_cross:
            print(f"m={m_c:.6f}(dist_m*={m_c-m_star:.3e}) ", end='')
    print()

# ─────────────────────────────────────────────────────────────────────────────
# PART 11: J3/J2 normalised cross-sector
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 11: J3/J2 and J4/J2² normalised cross-sector conditions")
print("="*80)

J2_pmns = float(np.real(np.trace(H_pmns @ H_pmns)))
ratio_J3_pmns = J3_pmns / J2_pmns
ratio_J4_pmns = J4_pmns / (J2_pmns**2)
print(f"\n  J3/J2 at PMNS:     {ratio_J3_pmns:.8f}")
print(f"  J4/J2² at PMNS:    {ratio_J4_pmns:.8f}")

def J2_sel(m):
    H=H3(m); return float(np.real(np.trace(H@H)))

# Find where J3/J2 at Koide = J3/J2 at PMNS
def ratio_J3_diff(m):
    return J3_sel(m)/J2_sel(m) - ratio_J3_pmns

ratio_crossings = []
ratio_v = [ratio_J3_diff(m) for m in ms]
for i in range(len(ms)-1):
    if ratio_v[i]*ratio_v[i+1] < 0:
        m_c = brentq(ratio_J3_diff, ms[i], ms[i+1], xtol=1e-12)
        ratio_crossings.append(m_c)

print(f"  J3/J2 = J3_pmns/J2_pmns crossing(s):")
for m_c in ratio_crossings:
    print(f"    m={m_c:.8f}, dist_m*={m_c-m_star:.4e}, dist_prod1={m_c-m_prod1:.4e}")
    check("J3/J2 crossing near m_star (1e-3)",
          abs(m_c-m_star) < 1e-3, f"dist={abs(m_c-m_star):.4e}", "NUMERIC")

# ─────────────────────────────────────────────────────────────────────────────
# PART 12: m_exact algebraic characterisation
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 12: m_exact (where beta_q23 ratio = S exactly) algebraic properties")
print("="*80)

m_exact = -1.159438237033   # from previous script
print(f"\n  m_exact = {m_exact:.12f}  (ratio = SELECTOR exactly)")
print(f"  m_prod1 = {m_prod1:.12f}  (u*v*w=1)")
print(f"  m_star  = {m_star:.12f}  (kappa=kappa_PDG)")
print(f"  m_exact - m_prod1 = {m_exact-m_prod1:.4e}")
print(f"  m_exact - m_star  = {m_exact-m_star:.4e}")

# Invariants at each point
H_exact = H3(m_exact)
H_prod1 = H3(m_prod1)
H_mstar = H3(m_star)

for m_label, H_check in [("m_exact", H_exact), ("m_prod1", H_prod1), ("m_star",H_mstar)]:
    J2 = float(np.real(np.trace(H_check@H_check)))
    J3 = float(np.real(np.trace(H_check@H_check@H_check)))
    J4 = float(np.real(np.trace(np.linalg.matrix_power(H_check,4))))
    det = float(np.real(np.linalg.det(H_check)))
    x=expm(H_check); v=float(x[2,2].real); w=float(x[1,1].real); u=koide_root_small(v,w)
    uvw = u*v*w
    kappa_h = kappa_from_slots(v,w)
    print(f"\n  {m_label}:")
    print(f"    J2={J2:.8f}, J3={J3:.8f}, J4={J4:.8f}")
    print(f"    det={det:.8f}, uvw={uvw:.10f}, kappa={kappa_h:.12f}")
    print(f"    J3/J2={J3/J2:.8f}, J4/J2²={J4/J2**2:.8f}, det/J2^(3/2)={det/J2**1.5:.8f}")

# Does m_exact have a simpler invariant description?
J3_exact = float(np.real(np.trace(H_exact@H_exact@H_exact)))
J2_exact = float(np.real(np.trace(H_exact@H_exact)))
print(f"\n  At m_exact: J3/J2 = {J3_exact/J2_exact:.10f}")
print(f"  At PMNS:    J3/J2 = {J3_pmns/J2_pmns:.10f}")
print(f"  Match? diff = {abs(J3_exact/J2_exact - J3_pmns/J2_pmns):.4e}")

det_exact = float(np.real(np.linalg.det(H_exact)))
det_J2_exact = det_exact / J2_exact
print(f"  At m_exact: det/J2 = {det_J2_exact:.10f}")
det_J2_pmns  = det_pmns / J2_pmns
print(f"  At PMNS:    det/J2 = {det_J2_pmns:.10f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 13: Scalar potential V(m) and off-diagonal extrema
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 13: Z³ scalar potential V(m) and connection to m_star")
print("="*80)

# The scalar potential is V(m) = Tr(H_sel(m)^2) / 2 + higher order?
# Or the potential from the Z³ lattice?
# Try: V(m) = ||H_sel(m)||_F^2 / 2 as a starting guess
# The gradient V'(m) = d/dm Tr(H^2)/2 = Tr(H * T_M)

def V_frob(m):
    H=H3(m); return float(np.real(np.trace(H@H)))/2.0

def dV_dm(m):
    H=H3(m); return float(np.real(np.trace(H@T_M + T_M@H)))/2.0

# Find extremum of V_frob(m)
V_vals = [V_frob(m) for m in ms]
dV_vals = [dV_dm(m) for m in ms]
dV_crossings = []
for i in range(len(ms)-1):
    if dV_vals[i]*dV_vals[i+1] < 0:
        m_c = brentq(dV_dm, ms[i], ms[i+1], xtol=1e-12)
        dV_crossings.append(m_c)

print(f"\n  V(m) = Tr(H²)/2 extrema (dV/dm = Tr(H T_M) = 0):")
for m_c in dV_crossings:
    print(f"    m_V = {m_c:.8f}, dist_m*={m_c-m_star:.4e}, dist_prod1={m_c-m_prod1:.4e}")

# Try J3 extremum
def dJ3_dm(m):
    H=H3(m); return float(np.real(np.trace(3*T_M@H@H)))

dJ3_crossings = []
dJ3_vals = [dJ3_dm(m) for m in ms]
for i in range(len(ms)-1):
    if dJ3_vals[i]*dJ3_vals[i+1] < 0:
        m_c = brentq(dJ3_dm, ms[i], ms[i+1], xtol=1e-12)
        dJ3_crossings.append(m_c)

print(f"  J3(m) extrema (dJ3/dm = 0):")
for m_c in dJ3_crossings:
    print(f"    m_J3 = {m_c:.8f}, dist_m*={m_c-m_star:.4e}")

# The "Rayleigh quotient" R(m) = J3/J2^(3/2) — related to the skewness
def skewness(m):
    H=H3(m); J2=float(np.real(np.trace(H@H))); J3=float(np.real(np.trace(H@H@H)))
    return J3/J2**1.5

skew_pmns = J3_pmns / J2_pmns**1.5
print(f"\n  Skewness R = J3/J2^(3/2) at PMNS:  {skew_pmns:.8f}")
print(f"  Skewness at m_prod1: {skewness(m_prod1):.8f}")
print(f"  Skewness at m_star:  {skewness(m_star):.8f}")

skew_vals = [skewness(m)-skew_pmns for m in ms]
skew_crossings = []
for i in range(len(ms)-1):
    if skew_vals[i]*skew_vals[i+1] < 0:
        m_c = brentq(lambda m: skewness(m)-skew_pmns, ms[i], ms[i+1], xtol=1e-12)
        skew_crossings.append(m_c)

print(f"  Skewness crossing(s):")
for m_c in skew_crossings:
    print(f"    m_skew={m_c:.8f}, dist_m*={m_c-m_star:.4e}, dist_prod1={m_c-m_prod1:.4e}")
    check("Skewness crossing near m_star (5e-4)",
          abs(m_c-m_star) < 5e-4, f"dist={abs(m_c-m_star):.4e}", "NUMERIC")

# ─────────────────────────────────────────────────────────────────────────────
# PART 14: kappa sensitivity to each PDG mass
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 14: kappa sensitivity and mass uncertainty budget")
print("="*80)

dk_de   = (kappa_pdg_from_masses(me+1e-6,mmu,mtau)-kappa_pdg_central)/1e-6
dk_dmu  = (kappa_pdg_from_masses(me,mmu+1e-6,mtau)-kappa_pdg_central)/1e-6
dk_dtau = (kappa_pdg_from_masses(me,mmu,mtau+1e-6)-kappa_pdg_central)/1e-6

err_e   = 3e-9      # MeV, effectively zero
err_mu  = 0.0023    # MeV 1sigma
err_tau = 0.12      # MeV 1sigma

dkappa_e   = dk_de   * err_e
dkappa_mu  = dk_dmu  * err_mu
dkappa_tau = dk_dtau * err_tau

print(f"\n  Sensitivity dk/dm_i:          dk/de={dk_de:.4e}, dk/dmu={dk_dmu:.4e}, dk/dtau={dk_dtau:.4e}")
print(f"  Contribution to kappa error:   de={dkappa_e:.2e}, dmu={dkappa_mu:.2e}, dtau={dkappa_tau:.2e}")
print(f"  Total kappa uncertainty (sum): ±{abs(dkappa_e)+abs(dkappa_mu)+abs(dkappa_tau):.2e}")
print(f"  Total kappa uncertainty (quad):±{math.sqrt(dkappa_e**2+dkappa_mu**2+dkappa_tau**2):.2e}")
print(f"  Delta_kappa (gap):              {delta_kappa_gap:.2e}")
sigma_gap = abs(delta_kappa_gap) / math.sqrt(dkappa_e**2+dkappa_mu**2+dkappa_tau**2)
print(f"  Gap in sigma units:             {sigma_gap:.2f}σ")

check("Gap within 2sigma of PDG kappa uncertainty",
      sigma_gap <= 2.0, f"sigma={sigma_gap:.2f}", "NUMERIC")
check("Gap within 3sigma of PDG kappa uncertainty",
      sigma_gap <= 3.0, f"sigma={sigma_gap:.2f}", "NUMERIC")

# ─────────────────────────────────────────────────────────────────────────────
# PART 15: NEW ROUTE — simultaneous cross-sector condition
# Find m such that BOTH: beta_q23 ratio ≈ S AND kappa ≈ kappa_PDG
# How close can we get? Is there a single m that nearly satisfies both?
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 15: Simultaneous cross-sector condition (beta ratio + kappa)")
print("="*80)

print(f"\n  Two conditions:")
print(f"  (A) kappa(m) = kappa_PDG   solved by m = m_star = {m_star:.8f}")
print(f"  (B) beta_q23 ratio = S     solved by m = m_exact = {m_exact:.8f}")
print(f"  Residual: m_star - m_exact = {m_star - m_exact:.4e}")
print()

# Both conditions are close. What is the "combined" condition?
# Weighted least squares: find m minimising alpha*(kappa-kappa_PDG)^2 + (1-alpha)*(ratio-S)^2
# normalized by characteristic scales
kappa_scale = abs(kappa_pdg_central) * 1e-4   # relative precision 1e-4
ratio_scale = S * 1e-4

def combined_loss(m_arr):
    m = m_arr[0]
    kappa_diff = (kappa_sel(m) - kappa_pdg_central) / kappa_scale
    bq = get_bq23(H3(m))
    if bq is None: return 1e10
    ratio_diff = (bq/bq_p/S - 1) / 1e-4
    return kappa_diff**2 + ratio_diff**2

res_comb = minimize(combined_loss, [m_prod1], method='Nelder-Mead',
                    options={'xatol':1e-12, 'fatol':1e-12, 'maxiter':10000})
m_comb = float(res_comb.x[0])
kappa_at_comb = kappa_sel(m_comb)
bq_at_comb = get_bq23(H3(m_comb))
ratio_at_comb = bq_at_comb/bq_p if bq_at_comb else float('nan')

print(f"  Combined-loss minimum at m_comb = {m_comb:.10f}")
print(f"  kappa at m_comb = {kappa_at_comb:.10f}, diff_PDG = {kappa_at_comb-kappa_pdg_central:.4e}")
print(f"  ratio at m_comb = {ratio_at_comb:.10f} (S={S:.10f}), diff = {ratio_at_comb-S:.4e}")
print(f"  Residual gap: these two conditions are {m_star-m_exact:.4e} apart in m-space")

# The two conditions cannot be simultaneously satisfied on the selected line.
# What does this tell us?
print()
print(f"  KEY: The gap between the two m-predictions is {abs(m_star-m_exact):.4e}")
print(f"       i.e., the cross-sector beta identity and kappa_PDG disagree by {abs(m_star-m_exact):.4e} in m")

# ─────────────────────────────────────────────────────────────────────────────
# PART 16: ASSUMPTIONS AUDIT
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 16: ASSUMPTIONS AUDIT")
print("="*80)
print("""
  ASSUMPTION 1: The physical m is pinned by u*v*w=1
    → WHAT IF: m is pinned by some other Cl(3) condition?
    → TESTED: J3 crossing, J4 crossing, det crossing, J3/J2 skewness
    → RESULT: Report above; none coincide with m_star exactly

  ASSUMPTION 2: d = q = S exactly on the physical selected line
    → WHAT IF: There are small quantum corrections d = S+eps, q = S+eps?
    → TESTED (PART 9): Finds eps that closes gap. Reports scale of correction.
    → KEY QUESTION: What is the physical origin of such a correction?

  ASSUMPTION 3: The gap is a real physical discrepancy (not experimental noise)
    → WHAT IF: Delta_kappa = 4.82e-5 is within PDG m_tau experimental error?
    → TESTED (PARTS 1, 14): Reports sigma equivalence.
    → KEY RESULT: if sigma < 2, gap dissolves under experimental uncertainty

  ASSUMPTION 4: The PMNS pin (M_P, D_P, Q_P) is exact
    → WHAT IF: The theoretical PMNS pin satisfies D*Q = S^2 = 2/3 exactly,
               and the PDG-fitted values differ due to experimental errors?
    → TESTED (PART 2): D_P shift of ~0.19% closes beta ratio gap
    → KEY QUESTION: Is 0.19% within NuFit theta_13 uncertainty?

  ASSUMPTION 5: The Koide sector is independent of the PMNS sector
    → WHAT IF: A coupled (PMNS, Koide) variational condition pins m*?
    → TESTED (PARTS 6,7,8): Frobenius, commutator, inner product extrema
    → RESULT: These natural conditions report their m values above

  ASSUMPTION 6: kappa_PDG uses PDG central masses
    → WHAT IF: kappa_PDG should use some other reference (e.g., running masses)?
    → NOT TESTED: Would require QED running mass calculation
    → DIRECTION: m_e, m_mu, m_tau at mu = 2 GeV (MS-bar) vs pole masses

  ASSUMPTION 7: The gap is in the m direction only
    → WHAT IF: The gap is partially in (d, q) too?
    → TESTED (PART 9): What (d,q) near (S,S) closes gap at m_prod1
    → KEY RESULT: size of required correction reveals whether it's 'natural'
""")

# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print(f"FINAL: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
print("="*80)
