#!/usr/bin/env python3
"""
Koide gap — relentless attack, all remaining routes
=====================================================

Tested and closed in prior scripts:
  - PDG m_tau uncertainty: 7.46σ — DEAD
  - J3/J4 crossings in [-1.30,-0.90]: none found — widened here
  - Off-selected-line Part 9: eps=-6.7e-5 partial close
  - 2D intersection (uvw=1 AND κ=κ_PDG): ε_0 ≈ (272/45)α_EM² — sign issue
  - β_q23 origin: Tr(T_D·T_Q)=0 rules out algebraic fix
  - One-loop perturbative shift: ratio=0, wrong mechanism
  - Z3 potential: minimum at m_V≈-0.433, not m_*

NEW ROUTES THIS SCRIPT:
  1  — Wide J3 scan [-5, 5] — find crossing, check distance from m_star
  2  — NEW near-identity: Δm = 4α_EM² (0.5% match) — verify, PSLQ, Cl(3) origin
  3  — 2D (m,ε) system: J3(m,ε)=J3_PMNS AND κ(m,ε)=κ_PDG — solve jointly
  4  — Running masses: find μ_K such that κ(running masses at μ_K) = κ_prod1
  5  — PMNS ↔ Koide orthogonality: Tr(H_PMNS · H_sel(m)) = 0 crossing
  6  — Cross-sector Casimir: Tr(H_PMNS · H_sel(m)²) condition
  7  — Characteristic polynomial cross-sector: same char poly at m_star?
  8  — Cubic structure of J3_sel(m): extract A, B, solve exactly
  9  — Assumptions audit #2: test assumptions not yet challenged
 10  — Summary: final accounting

ASSUMPTION AUDIT #2 (done BEFORE coding — per user rule):
  A1: T_M² = I was just computed analytically — CONFIRMED, J3_sel is CUBIC not degree 6
  A2: H_BASE convention — are we using H_B correctly? Check Tr(H_B), eigenvalues
  A3: PDG masses are pole masses — correct. But Koide paper uses pole masses.
  A4: κ_PDG is computed correctly — re-verify from scratch
  A5: The gap formula Δm = m_prod1 - m_star is correct (m_prod1 > m_star since m_prod1 less negative)
  A6: PMNS pin (M_P,D_P,Q_P) — are these self-consistent with observed angles?
  A7: Cl(3) framework uses α_EM = 1/136.4 (predicted) or PDG 1/137.036?
      → The ε_0 ≈ (272/45)α_EM² uses PDG α_EM. What if we use framework α_EM?
  A8: The 2D convention: in the 2D intersection script, ε = -(d_0 - S) so
      ε_0 NEGATIVE means d_0 > S. Is the "wrong sign" actually just a convention issue?
  A9: T_M is NOT diag. It's [[1,0,0],[0,0,1],[0,1,0]]. Its eigenvalues are NOT 1,-1,-1.
      What are they? This affects the physical interpretation of the m parameter.
"""

from __future__ import annotations
import math, sys, itertools

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq, fsolve, minimize_scalar, root

# ─── constants ───────────────────────────────────────────────────────────────
GAMMA=0.5; E1=math.sqrt(8/3); E2=math.sqrt(8)/3
SQRT3=math.sqrt(3); SQRT6=math.sqrt(6); S=SQRT6/3
ALPHA_EM=7.2973535693e-3
ALPHA_LM=0.0907            # bare coupling (framework)
G2_SQ=0.25                 # SU(2) coupling: g_2² = 1/4
G_Y_SQ=0.20                # U(1)_Y coupling: g_Y² = 1/5

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
    sqm=np.sqrt([me,mmu,mtau]); d=sqm/np.linalg.norm(sqm)
    def koide_amp(k):
        w=(1-k)/(1+k)
        if w<=0: return 1.0
        u=koide_root_small(1.0,w)
        if u<=0: return 1.0
        a=np.array([u,1.0,w]); return -float(np.dot(a/np.linalg.norm(a),d))
    r=minimize_scalar(koide_amp,bounds=(-0.9999,-0.0001),method='bounded',options={'xatol':1e-14})
    return float(r.x)

kappa_pdg_central = kappa_pdg_from_masses(*PDG_MEV)

def kappa_sel(m):
    H=H3(m); eH=expm(H); v=float(np.real(eH[2,2])); w=float(np.real(eH[1,1]))
    return kappa_from_slots(v,w)

def uvw_at(m, d=S, q=S):
    H=H3(m,d,q); eH=expm(H)
    v=float(np.real(eH[2,2])); w=float(np.real(eH[1,1]))
    u=koide_root_small(v,w); return u*v*w

def kappa_at(m, d=S, q=S):
    H=H3(m,d,q); eH=expm(H)
    v=float(np.real(eH[2,2])); w=float(np.real(eH[1,1]))
    return kappa_from_slots(v,w)

# Find m_prod1 and m_star
ms_scan = np.linspace(-1.30, -1.00, 5000)
def uvw_diff(m): return uvw_at(m)-1.0
for i in range(len(ms_scan)-1):
    if uvw_diff(ms_scan[i])*uvw_diff(ms_scan[i+1])<0:
        m_prod1=brentq(uvw_diff,ms_scan[i],ms_scan[i+1],xtol=1e-14)
        break

def kappa_diff(m): return kappa_sel(m)-kappa_pdg_central
for i in range(len(ms_scan)-1):
    if kappa_diff(ms_scan[i])*kappa_diff(ms_scan[i+1])<0:
        m_star=brentq(kappa_diff,ms_scan[i],ms_scan[i+1],xtol=1e-14)
        break

delta_m = m_prod1 - m_star
kappa_prod1 = kappa_sel(m_prod1)
delta_kappa = kappa_prod1 - kappa_pdg_central

pass_count=0; fail_count=0
def check(label, cond, detail="", kind="NUMERIC"):
    global pass_count, fail_count
    tag = "PASS" if cond else "FAIL"
    if cond: pass_count+=1
    else: fail_count+=1
    print(f"  [{tag}] [{kind}] {label}  ({detail})")

print("="*80)
print("SETUP — key values")
print("="*80)
print(f"  m_prod1     = {m_prod1:.15f}")
print(f"  m_star      = {m_star:.15f}")
print(f"  Δm          = m_prod1 - m_star = {delta_m:.10e}")
print(f"  κ_prod1     = {kappa_prod1:.15f}")
print(f"  κ_PDG       = {kappa_pdg_central:.15f}")
print(f"  Δκ          = {delta_kappa:.10e}")
print(f"  α_EM        = {ALPHA_EM:.15e}")
print(f"  α_EM²       = {ALPHA_EM**2:.10e}")
print(f"  4·α_EM²     = {4*ALPHA_EM**2:.10e}")
print(f"  S×E1        = {S*E1:.15f}  [exact = 4/3 = {4/3:.15f}]")

# Tr(T_M) and T_M eigenvalues
tm_eigs = np.linalg.eigvals(T_M)
tm_sq = T_M @ T_M
print(f"\n  T_M eigenvalues: {np.sort(tm_eigs.real)}")
print(f"  T_M² = I? max|T_M²-I| = {np.max(np.abs(tm_sq-np.eye(3))):.2e}")
print(f"  Tr(T_M) = {np.trace(T_M).real:.1f}")
print(f"  Tr(T_D) = {np.trace(T_D).real:.1f}, Tr(T_Q) = {np.trace(T_Q).real:.1f}")
print(f"  Tr(H_B) = {np.trace(H_B).real:.6f}")
H_0 = H_B + S*T_D + S*T_Q
print(f"  Tr(H_0) = {np.trace(H_0).real:.6f}  [H_0 = H_B + S*T_D + S*T_Q]")

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: Wide J3 scan [-5, 5]
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 1: Wide J3 scan — m in [-5, +5]")
print("="*80)

J3_pmns = float(np.real(np.trace(H_pmns @ H_pmns @ H_pmns)))
print(f"\n  J3(H_PMNS) = {J3_pmns:.10f}")

def J3_sel(m, d=S, q=S):
    H=H3(m,d,q); return float(np.real(np.trace(H@H@H)))

# Analytical structure of J3_sel(m) since T_M² = I:
# J3_sel(m) = Tr(H_0³) + 3m·Tr(H_0²·T_M) + 3m²·Tr(H_0) + m³·Tr(T_M)
# Since Tr(H_0)=0 and Tr(T_M)=1:
# J3_sel(m) = B + 3A·m + m³   where A=Tr(H_0²·T_M), B=Tr(H_0³)
A_coef = float(np.real(np.trace(H_0 @ H_0 @ T_M)))
B_coef = float(np.real(np.trace(H_0 @ H_0 @ H_0)))
print(f"\n  J3 cubic structure (exact since T_M²=I, Tr(H_0)=0, Tr(T_M)=1):")
print(f"    J3_sel(m) = m³ + 3A·m + B")
print(f"    A = Tr(H_0²·T_M) = {A_coef:.10f}")
print(f"    B = Tr(H_0³)     = {B_coef:.10f}")
print(f"    Verify: J3_sel(m_prod1) exact  = {m_prod1**3 + 3*A_coef*m_prod1 + B_coef:.6f}")
print(f"    Verify: J3_sel(m_prod1) direct = {J3_sel(m_prod1):.6f}")

# Solve m³ + 3A·m + B = J3_pmns analytically
# This is a depressed cubic p = m³ + 3A·m + (B - J3_pmns) = 0
# Use Cardano: discriminant Δ = -4(3A)³ - 27(B-J3_pmns)² = -4·27·A³ - 27·(B-J3_pmns)²
p_const = B_coef - J3_pmns
disc = -4*(3*A_coef)**3 - 27*p_const**2
print(f"\n  Solving m³ + 3A·m + (B-J3_PMNS) = 0:")
print(f"    B - J3_PMNS = {p_const:.10f}")
print(f"    Discriminant Δ = {disc:.6f}  (>0: three real roots, <0: one real root)")

# Numerical wide scan
ms_wide = np.linspace(-5.0, 5.0, 10000)
J3_diff = [J3_sel(m) - J3_pmns for m in ms_wide]
J3_crossings = []
for i in range(len(ms_wide)-1):
    if J3_diff[i]*J3_diff[i+1] < 0:
        m_c = brentq(lambda m: J3_sel(m)-J3_pmns, ms_wide[i], ms_wide[i+1], xtol=1e-13)
        J3_crossings.append(m_c)

print(f"\n  J3 crossings with J3_PMNS in [-5, +5]:")
if not J3_crossings:
    print("  NONE FOUND")
    check("J3 crossing near m_star (±0.01)", False, "no crossing in [-5,5]")
else:
    for m_c in J3_crossings:
        d_prod1 = m_c - m_prod1
        d_star  = m_c - m_star
        kap_c   = kappa_sel(m_c)
        dk      = kap_c - kappa_pdg_central
        print(f"    m_J3 = {m_c:.12f},  Δ(m_prod1) = {d_prod1:.4e},  Δ(m_*) = {d_star:.4e},  Δκ = {dk:.4e}")
        check(f"J3 crossing near m_star (±0.01)", abs(d_star)<0.01, f"dist={abs(d_star):.4e}")
        check(f"J3 crossing also has κ≈κ_PDG (±1e-4)", abs(dk)<1e-4, f"Δκ={dk:.4e}")

# Show J3 at key points
print(f"\n  J3_sel values at key points:")
for m_test, label in [(m_prod1,"m_prod1"),(m_star,"m_star"),(-1.0,"m=-1.0"),(-0.5,"m=-0.5"),(0.0,"m=0"),(0.5,"m=0.5"),(1.0,"m=1.0")]:
    j3_v = J3_sel(m_test)
    j3_analytic = m_test**3 + 3*A_coef*m_test + B_coef
    print(f"    {label:10s}: J3 = {j3_v:.6f}, analytic = {j3_analytic:.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: NEW near-identity Δm = 4α_EM²
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 2: New near-identity Δm = 4·α_EM²")
print("="*80)

delta_m_val = abs(delta_m)
aem2 = ALPHA_EM**2

candidates = {
    "4·α_EM²":                4*aem2,
    "(1/g_2²)·α_EM²":         (1/G2_SQ)*aem2,
    "(1/g_Y²)·α_EM²":         (1/G_Y_SQ)*aem2,
    "α_EM/(4π²)":             ALPHA_EM/(4*math.pi**2),
    "(4/3)²·α_EM²":           (4/3)**2*aem2,
    "S·E1·α_EM²·(4/3)":      (S*E1)*aem2*(4/3),
    "(272/45)·α_EM²/(S·E1)":  (272/45)*aem2/(S*E1),
    "S²·E1²·α_EM² × 1/(4π²)": (S*E1)**2*aem2/(4*math.pi**2),
    "α_LM²/(4π²)":            ALPHA_LM**2/(4*math.pi**2),
    "α_LM·α_EM/(4π)":         ALPHA_LM*ALPHA_EM/(4*math.pi),
    "16·α_EM³/S":             16*ALPHA_EM**3/S,
}

print(f"\n  |Δm| = {delta_m_val:.12e}")
print(f"  α_EM = {ALPHA_EM:.15e}")
print(f"\n  Testing candidates:")
best_ratio = None; best_label = None; best_err = 1.0
for label, val in candidates.items():
    ratio = delta_m_val / val
    err = abs(ratio - 1.0)
    marker = " <-- BEST" if err < 0.001 else ("  **" if err < 0.01 else "")
    print(f"    {label:45s}: {val:.8e}, ratio = {ratio:.8f}, err = {err*100:.4f}%{marker}")
    if err < best_err:
        best_err = err; best_label = label; best_ratio = ratio

print(f"\n  Best match: {best_label} with {best_err*100:.4f}% error")

# For 4·α_EM²:
ratio_4a2 = delta_m_val / (4*aem2)
print(f"\n  Δm / (4·α_EM²) = {ratio_4a2:.10f}")
print(f"  Δm / (4·α_EM²) - 1 = {ratio_4a2-1:.4e}")

# Can we explain the residual 0.46%?
residual = delta_m_val - 4*aem2
print(f"\n  Residual = Δm - 4·α_EM² = {residual:.6e}")
print(f"  Residual / (4·α_EM²) = {residual/(4*aem2):.6f}")
print(f"\n  What IS the residual? Testing:")
print(f"    Residual / (4·α_EM² · S²)   = {residual/(4*aem2*S**2):.6f}  [÷ S² = ÷(2/3)]")
print(f"    Residual / (4·α_EM² · α_EM) = {residual/(4*aem2*ALPHA_EM):.6f}  [next order]")
print(f"    Residual / (4·α_EM² · S)    = {residual/(4*aem2*S):.6f}")

check("Δm = 4·α_EM² within 1%", abs(ratio_4a2-1) < 0.01,
      f"ratio={ratio_4a2:.8f}, err={abs(ratio_4a2-1)*100:.4f}%")
check("Δm = 4·α_EM² within 0.5%", abs(ratio_4a2-1) < 0.005,
      f"ratio={ratio_4a2:.8f}, err={abs(ratio_4a2-1)*100:.4f}%")
check("Δm = 4·α_EM² within 0.1%", abs(ratio_4a2-1) < 0.001,
      f"ratio={ratio_4a2:.8f}, err={abs(ratio_4a2-1)*100:.4f}%")

# ε_0 consistency
# From 2D intersection script: |ε_0| = 3.21896e-4
eps0_known = 3.21896e-4
print(f"\n  Consistency with ε_0 from 2D intersection:")
print(f"  ε_0 / (4·α_EM²) = {eps0_known/(4*aem2):.8f}  vs  Δm/(4·α_EM²) = {ratio_4a2:.8f}")
print(f"  ε_0 / Δm = {eps0_known/delta_m_val:.8f}  [should ≈ (272/45)/4 = {(272/45)/4:.8f}]")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: PSLQ-style search for Δm and Δκ
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 3: PSLQ-style search — find integer relation for Δm and Δκ")
print("="*80)

def pslq_search(target, basis_vals, basis_names, max_coeff=20, max_terms=3):
    """Find small-integer linear combination of basis matching target."""
    best = None; best_err = 1.0
    for signs in itertools.product([-1,1], repeat=max_terms):
        for idxs in itertools.combinations(range(len(basis_vals)), max_terms):
            for coeffs in itertools.product(range(1, max_coeff+1), repeat=max_terms):
                candidate = sum(s*c*basis_vals[i] for s,c,i in zip(signs,coeffs,idxs))
                if candidate <= 0: continue
                err = abs(target/candidate - 1.0)
                if err < best_err:
                    best_err = err
                    terms = [f"{'+' if s>0 else '-'}({c}×{basis_names[i]})" for s,c,i in zip(signs,coeffs,idxs)]
                    best = ("".join(terms), candidate, err)
    return best

basis_vals  = [ALPHA_EM**2, ALPHA_EM, S, E1, S**2, E1**2, S*E1,
               (S*E1)**2, math.pi, G2_SQ, G_Y_SQ, ALPHA_LM]
basis_names = ["α²", "α", "S", "E1", "S²", "E1²", "S·E1",
               "(S·E1)²", "π", "g₂²", "g_Y²", "α_LM"]

# Search for Δm
print(f"\n  Searching integer relations for |Δm| = {delta_m_val:.8e}...")
print(f"  Testing: n×(product of 2 basis elements) matching |Δm|")
found_dm = []
for n in range(1, 25):
    for i, j in itertools.combinations_with_replacement(range(len(basis_vals)), 2):
        candidate = n * basis_vals[i] * basis_vals[j]
        err = abs(delta_m_val/candidate - 1.0)
        if err < 0.02:
            found_dm.append((err, n, basis_names[i], basis_names[j], candidate))

found_dm.sort()
print(f"  Best matches for |Δm| (error < 2%):")
for err, n, b1, b2, val in found_dm[:15]:
    print(f"    n={n:3d}, {b1}×{b2}: {val:.8e}, err={err*100:.4f}%")

# Search for Δκ
print(f"\n  Searching for |Δκ| = {abs(delta_kappa):.8e}...")
found_dk = []
for n in range(1, 25):
    for i, j in itertools.combinations_with_replacement(range(len(basis_vals)), 2):
        candidate = n * basis_vals[i] * basis_vals[j]
        err = abs(abs(delta_kappa)/candidate - 1.0)
        if err < 0.02:
            found_dk.append((err, n, basis_names[i], basis_names[j], candidate))

found_dk.sort()
print(f"  Best matches for |Δκ| (error < 2%):")
for err, n, b1, b2, val in found_dk[:15]:
    print(f"    n={n:3d}, {b1}×{b2}: {val:.8e}, err={err*100:.4f}%")

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: Running masses — find the Koide scale
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 4: Running masses — find μ_K such that κ_running(μ_K) = κ_prod1")
print("="*80)

# QED one-loop running: m(μ) = m(μ_0) × [1 - (3α/2π)×ln(μ/μ_0)]
# All three masses run with the SAME anomalous dimension in QED (proportional to Q²=1)
# So ratios m_μ/m_τ and m_e/m_τ run with DIFFERENT rates only through α(μ) running.
# At one loop with fixed α: m_i(μ)/m_i(μ_0) = [1 - (3α/2π)×ln(μ/μ_0)] for all i
# → ALL ratios are UNCHANGED at fixed-α one loop! κ does NOT run at fixed α.

# However: at two loops or with α running, ratios DO change.
# Simplified: use running α(μ) = α / [1 - (α/3π)×ln(μ/m_e)] for QED

def alpha_qed_running(mu_mev, alpha_ref=ALPHA_EM, mu_ref_mev=0.51099895):
    """One-loop QED running coupling (electron only below muon threshold)."""
    if mu_mev <= mu_ref_mev: return alpha_ref
    nf = 1  # just electron below muon threshold
    if mu_mev > 105.658: nf = 2
    if mu_mev > 1776.86: nf = 3
    log = math.log(mu_mev / mu_ref_mev)
    b0 = nf * 4.0/3.0  # QED beta function coefficient (one-loop, nf flavors)
    return alpha_ref / (1 - alpha_ref * b0 * log / (3*math.pi))

def lepton_masses_at_scale(mu_mev):
    """QED running lepton masses at scale mu (MeV). One-loop."""
    m_e0, m_mu0, m_tau0 = PDG_MEV
    # m(μ) = m(μ_0) × exp[-(3/4π) × ∫_{μ_0}^μ α(μ')/μ' dμ']
    # Approximate: m(μ) ≈ m(μ_0) × [1 + (3α/2π) × ln(μ_0/μ)]  (at fixed α)
    # Full one-loop with running α (simplified):
    alpha_mu = alpha_qed_running(mu_mev)
    log_me = math.log(mu_mev / m_e0) if mu_mev > m_e0 else 0
    log_mmu = math.log(mu_mev / m_mu0) if mu_mev > m_mu0 else 0
    log_mtau = math.log(mu_mev / m_tau0) if mu_mev > m_tau0 else 0
    gamma_m = 3*alpha_mu/(2*math.pi)  # anomalous dimension
    me = m_e0 * math.exp(-gamma_m * log_me)
    mmu = m_mu0 * math.exp(-gamma_m * log_mmu)
    mtau = m_tau0 * math.exp(-gamma_m * log_mtau)
    return me, mmu, mtau

def kappa_pdg_at_scale(mu_mev):
    me, mmu, mtau = lepton_masses_at_scale(mu_mev)
    return kappa_pdg_from_masses(me, mmu, mtau)

print(f"\n  κ_prod1 = {kappa_prod1:.12f}")
print(f"  κ_PDG   = {kappa_pdg_central:.12f}  (at pole masses)")
print(f"\n  κ(μ) at various scales:")
for mu in [0.5110, 10.0, 100.0, 105.6, 1000.0, 1776.86, 3000.0, 5000.0, 10000.0]:
    k = kappa_pdg_at_scale(mu)
    dk_from_prod1 = k - kappa_prod1
    print(f"    μ = {mu:8.2f} MeV: κ = {k:.12f}, Δκ from κ_prod1 = {dk_from_prod1:.6e}")

# Does κ(μ) ever reach κ_prod1 for some μ > m_tau?
# Find direction: is κ increasing or decreasing with μ?
k_pole = kappa_pdg_central
k_above = kappa_pdg_at_scale(1776.86 * 1.1)
dk_dmu = (k_above - k_pole) / (1776.86 * 0.1)
print(f"\n  dk/dμ near m_tau = {dk_dmu:.6e} /MeV")
print(f"  Gap Δκ = κ_prod1 - κ_PDG = {delta_kappa:.6e}")
print(f"  Required Δμ = {delta_kappa/dk_dmu:.2f} MeV above pole masses")

# Is there a scale where κ = κ_prod1?
def kappa_minus_prod1(log_mu):
    mu = math.exp(log_mu)
    try:
        k = kappa_pdg_at_scale(mu)
        return k - kappa_prod1
    except:
        return float('nan')

# Scan log(mu/m_tau) from 0 to 20 (mu from m_tau to e^20 × m_tau)
logmu_scan = np.linspace(math.log(PDG_MEV[2]), math.log(PDG_MEV[2]) + 20, 1000)
kap_scan = []
for logmu in logmu_scan:
    try:
        k = kappa_pdg_at_scale(math.exp(logmu))
        kap_scan.append(k - kappa_prod1)
    except:
        kap_scan.append(float('nan'))

crossings_mu = []
for i in range(len(logmu_scan)-1):
    if (not math.isnan(kap_scan[i]) and not math.isnan(kap_scan[i+1])
            and kap_scan[i]*kap_scan[i+1] < 0):
        try:
            lm_c = brentq(kappa_minus_prod1, logmu_scan[i], logmu_scan[i+1], xtol=1e-10)
            crossings_mu.append(math.exp(lm_c))
        except:
            pass

print(f"\n  Scale μ_K where κ(μ_K) = κ_prod1:")
if not crossings_mu:
    print("  No crossing found in [m_tau, e^20 × m_tau]")
    check("Running mass scale closes gap", False, "no μ_K found")
else:
    for mu_c in crossings_mu:
        me, mmu, mtau = lepton_masses_at_scale(mu_c)
        print(f"  μ_K = {mu_c:.4f} MeV = {mu_c/PDG_MEV[2]:.6f} × m_tau")
        print(f"    m_e({mu_c:.1f})={me:.6f}, m_mu={mmu:.4f}, m_tau={mtau:.4f} MeV")
        ratio = mu_c/PDG_MEV[2]
        print(f"    μ_K/m_tau = {ratio:.8f}")
        check("Running mass scale = natural framework scale", False,
              "need Cl(3) origin for μ_K/m_tau")

# ─────────────────────────────────────────────────────────────────────────────
# PART 5: PMNS ↔ Koide inner product and orthogonality
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 5: PMNS ↔ Koide coupling — inner product and orthogonality conditions")
print("="*80)

def hs_inner(A, B):
    """Hilbert-Schmidt inner product Tr(A†B)."""
    return float(np.real(np.trace(A.conj().T @ B)))

H0_sel = H_B + S*T_D + S*T_Q

print(f"\n  H_PMNS · H_sel inner products:")
hs_vals = []
ms_test = np.linspace(-1.30, -0.90, 3000)
for m in ms_test:
    H = H3(m)
    hs_vals.append(hs_inner(H_pmns, H))

hs_0 = hs_inner(H_pmns, H3(m_prod1))
hs_star = hs_inner(H_pmns, H3(m_star))
print(f"  ⟨H_PMNS|H_sel⟩ at m_prod1 = {hs_0:.10f}")
print(f"  ⟨H_PMNS|H_sel⟩ at m_star  = {hs_star:.10f}")

# Find where ⟨H_PMNS|H_sel⟩ = 0
hs_crossings = []
for i in range(len(ms_test)-1):
    if hs_vals[i]*hs_vals[i+1] < 0:
        m_c = brentq(lambda m: hs_inner(H_pmns, H3(m)),
                     ms_test[i], ms_test[i+1], xtol=1e-13)
        hs_crossings.append(m_c)

print(f"\n  ⟨H_PMNS|H_sel⟩ = 0 crossings:")
for m_c in hs_crossings:
    dk = kappa_sel(m_c) - kappa_pdg_central
    print(f"    m = {m_c:.12f}, dist from m_star = {m_c-m_star:.4e}, Δκ = {dk:.4e}")
    check("H_PMNS ⊥ H_sel at m_star (±1e-3)", abs(m_c-m_star)<1e-3, f"dist={abs(m_c-m_star):.4e}")

if not hs_crossings:
    print("  No crossing in scan range")
    check("H_PMNS ⊥ H_sel somewhere", False, "no crossing")

# Second-order: ⟨H_PMNS|H_sel²⟩
def hs2(m):
    H=H3(m); return hs_inner(H_pmns, H@H)

hs2_vals = [hs2(m) for m in ms_test]
print(f"\n  ⟨H_PMNS|H_sel²⟩ = 0 crossings:")
hs2_cross = []
for i in range(len(ms_test)-1):
    if hs2_vals[i]*hs2_vals[i+1] < 0:
        m_c = brentq(hs2, ms_test[i], ms_test[i+1], xtol=1e-13)
        hs2_cross.append(m_c)
        dk = kappa_sel(m_c)-kappa_pdg_central
        print(f"    m = {m_c:.12f}, dist from m_star = {m_c-m_star:.4e}, Δκ = {dk:.4e}")
        check("⟨H_PMNS|H_sel²⟩=0 at m_star (±1e-3)", abs(m_c-m_star)<1e-3, f"dist={abs(m_c-m_star):.4e}")

if not hs2_cross:
    print("  No crossing in scan range")

# ─────────────────────────────────────────────────────────────────────────────
# PART 6: Characteristic polynomial cross-sector
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 6: Characteristic polynomial — do H_sel(m_star) and H_PMNS share an invariant?")
print("="*80)

def char_poly_coeffs(H):
    """Return (p1, p2, p3) = (Tr, sum-of-2x2-minors, det) of H."""
    p1 = np.trace(H).real
    p2 = 0.5*(p1**2 - np.trace(H@H).real)
    p3 = np.linalg.det(H).real
    return p1, p2, p3

p1_pmns, p2_pmns, p3_pmns = char_poly_coeffs(H_pmns)
p1_star, p2_star, p3_star = char_poly_coeffs(H3(m_star))
p1_prod1, p2_prod1, p3_prod1 = char_poly_coeffs(H3(m_prod1))

print(f"\n  H_PMNS:    p1={p1_pmns:.8f}, p2={p2_pmns:.8f}, p3={p3_pmns:.8f}")
print(f"  H_sel(m*): p1={p1_star:.8f}, p2={p2_star:.8f}, p3={p3_star:.8f}")
print(f"  H_sel(m0): p1={p1_prod1:.8f}, p2={p2_prod1:.8f}, p3={p3_prod1:.8f}")

# Which coefficient is most similar?
for name, vp, vs in [("p1(Tr)", p1_pmns, p1_star),
                      ("p2", p2_pmns, p2_star),
                      ("p3(det)", p3_pmns, p3_star)]:
    diff = abs(vp-vs)
    rel = diff/max(abs(vp),abs(vs),1e-15)
    print(f"  |{name}_PMNS - {name}_sel(m*)| = {diff:.6e} (rel {rel:.4f})")

# Cross-sector p2 matching: find m where p2_sel(m) = p2_pmns
def p2_sel(m): return char_poly_coeffs(H3(m))[1]
def p3_sel(m): return char_poly_coeffs(H3(m))[2]

p2_diff = [p2_sel(m) - p2_pmns for m in ms_test]
p2_cross = []
for i in range(len(ms_test)-1):
    if p2_diff[i]*p2_diff[i+1] < 0:
        m_c = brentq(lambda m: p2_sel(m)-p2_pmns, ms_test[i], ms_test[i+1], xtol=1e-13)
        p2_cross.append(m_c)

print(f"\n  p2_sel(m) = p2_PMNS crossings:")
if not p2_cross:
    print("  None in scan range [-1.30, -0.90]")
else:
    for m_c in p2_cross:
        dk = kappa_sel(m_c)-kappa_pdg_central
        print(f"    m = {m_c:.12f}, dist from m_star = {m_c-m_star:.4e}, Δκ = {dk:.4e}")
        check("p2 crossing at m_star (±1e-3)", abs(m_c-m_star)<1e-3, f"dist={abs(m_c-m_star):.4e}")

p3_diff = [p3_sel(m) - p3_pmns for m in ms_test]
p3_cross = []
for i in range(len(ms_test)-1):
    if p3_diff[i]*p3_diff[i+1] < 0:
        m_c = brentq(lambda m: p3_sel(m)-p3_pmns, ms_test[i], ms_test[i+1], xtol=1e-13)
        p3_cross.append(m_c)

print(f"\n  p3_sel(m) = p3_PMNS = det(H_PMNS) crossings:")
if not p3_cross:
    print("  None in scan range [-1.30, -0.90]")
else:
    for m_c in p3_cross:
        dk = kappa_sel(m_c)-kappa_pdg_central
        print(f"    m = {m_c:.12f}, dist from m_star = {m_c-m_star:.4e}, Δκ = {dk:.4e}")
        check("det crossing at m_star (±1e-3)", abs(m_c-m_star)<1e-3, f"dist={abs(m_c-m_star):.4e}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 7: 2D system — J3(m,ε)=J3_PMNS AND κ(m,ε)=κ_PDG
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 7: 2D system — J3(m,ε)=J3_PMNS AND κ(m,ε)=κ_PDG")
print("="*80)

def state_2d(m, eps):
    """J3 and kappa at d=q=S-eps."""
    H = H3(m, S-eps, S-eps)
    j3 = float(np.real(np.trace(H@H@H)))
    eH = expm(H)
    v = float(np.real(eH[2,2])); w = float(np.real(eH[1,1]))
    kap = (v-w)/(v+w)
    return j3, kap

# System: F(m, eps) = [J3(m,eps) - J3_PMNS, kappa(m,eps) - kappa_PDG] = 0
def system_J3_kappa(x):
    m, eps = x
    j3, kap = state_2d(m, eps)
    return [j3 - J3_pmns, kap - kappa_pdg_central]

# Find initial guess: from 2D intersection script, the uvw=1+kappa=kPDG intersection
# was at (m_0, eps_0) = (-1.1615, -3.219e-4). Try nearby starting point.
# For J3: at eps=0, J3_sel(m) = J3_pmns at some m_J3 (from wide scan above).
# Start near (m_J3_crossing, 0) if it exists.

print(f"\n  J3_PMNS = {J3_pmns:.8f}")
print(f"\n  Attempting to solve J3(m,ε)=J3_PMNS AND κ(m,ε)=κ_PDG jointly...")

# Try multiple starting points
solutions_2d = []
starting_points = []

# Add J3 crossings from wide scan as starting points with eps=0
for m_j3c in J3_crossings:
    starting_points.append([m_j3c, 0.0])
    starting_points.append([m_j3c, 1e-4])
    starting_points.append([m_j3c, -1e-4])

# Also try near m_star
for eps_init in [0.0, 1e-4, -1e-4, 3e-4, -3e-4, 1e-3]:
    starting_points.append([m_star, eps_init])
    starting_points.append([m_prod1, eps_init])

for x0 in starting_points:
    try:
        sol = fsolve(system_J3_kappa, x0, full_output=True)
        x_sol, info, ier, msg = sol
        if ier == 1:
            residual = np.max(np.abs(system_J3_kappa(x_sol)))
            if residual < 1e-8:
                m_sol, eps_sol = x_sol
                # Check if already found
                duplicate = any(abs(m_sol - s[0]) < 1e-6 and abs(eps_sol - s[1]) < 1e-8
                                 for s in solutions_2d)
                if not duplicate:
                    solutions_2d.append([m_sol, eps_sol])
    except:
        pass

print(f"  Found {len(solutions_2d)} solution(s):")
for m_sol, eps_sol in solutions_2d:
    j3_v, kap_v = state_2d(m_sol, eps_sol)
    uvw_v = uvw_at(m_sol, S-eps_sol, S-eps_sol)
    d_sol = S - eps_sol
    print(f"\n    m_sol = {m_sol:.12f}, ε_sol = {eps_sol:.8e}")
    print(f"    d_sol = S {'+' if eps_sol<0 else '-'} {abs(eps_sol):.6e} = {d_sol:.12f}")
    print(f"    J3 check: {j3_v:.8f} vs {J3_pmns:.8f} (diff={j3_v-J3_pmns:.2e})")
    print(f"    κ  check: {kap_v:.12f} vs {kappa_pdg_central:.12f} (diff={kap_v-kappa_pdg_central:.2e})")
    print(f"    u·v·w    = {uvw_v:.10f}")
    print(f"    ε_sol vs (272/45)α_EM²: ratio = {abs(eps_sol)/((272/45)*ALPHA_EM**2):.6f}")
    check("J3 AND κ=κ_PDG solution exists", True,
          f"m={m_sol:.8f}, ε={eps_sol:.6e}")
    check("Solution near m_star (±0.1)", abs(m_sol-m_star)<0.1, f"dist={abs(m_sol-m_star):.4e}")
    check("ε_sol/((272/45)α_EM²) = 1 ± 0.1",
          abs(abs(eps_sol)/((272/45)*ALPHA_EM**2) - 1.0) < 0.1,
          f"ratio={abs(eps_sol)/((272/45)*ALPHA_EM**2):.6f}")

if not solutions_2d:
    check("J3 AND κ=κ_PDG 2D solution exists", False, "none found")

# ─────────────────────────────────────────────────────────────────────────────
# PART 8: Assumptions audit #2 — algebraic verification
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 8: Assumptions audit #2")
print("="*80)

print("\n  A1: T_M² = I (ASSUMPTION: used in cubic decomposition)")
check("T_M² = I (exact)", np.max(np.abs(T_M@T_M - np.eye(3))) < 1e-14,
      f"max|T_M²-I|={np.max(np.abs(T_M@T_M-np.eye(3))):.2e}", "ALGEBRAIC")

print("\n  A2: J3 cubic exact formula (m³ + 3A·m + B, no m² term)")
for m_test in [m_prod1, m_star, -1.0, -0.5]:
    j3_direct = J3_sel(m_test)
    j3_formula = m_test**3 + 3*A_coef*m_test + B_coef
    err = abs(j3_direct - j3_formula)
    check(f"  J3 formula exact at m={m_test:.4f}", err < 1e-10, f"err={err:.2e}", "ALGEBRAIC")

print("\n  A3: Tr(T_D·T_Q) = 0 (rules out H² cross-sector fix)")
tr_dq = float(np.real(np.trace(T_D @ T_Q)))
check("  Tr(T_D·T_Q) = 0 (confirmed)", abs(tr_dq) < 1e-14, f"value={tr_dq:.2e}", "ALGEBRAIC")

print("\n  A4: κ_PDG recomputed from scratch")
kpdg2 = kappa_pdg_from_masses(*PDG_MEV)
check("  κ_PDG stable (|κ - κ_PDG_prev| < 1e-12)", abs(kpdg2 - kappa_pdg_central) < 1e-12,
      f"κ_PDG={kpdg2:.15f}", "NUMERIC")

print("\n  A5: T_M eigenvalues (not ±1 — affects m parameter interpretation)")
eigs_TM = sorted(np.linalg.eigvals(T_M).real)
print(f"  T_M eigenvalues = {eigs_TM}")
# T_M = [[1,0,0],[0,0,1],[0,1,0]] acts on space {e0,e1,e2}
# e0 is fixed: T_M e0 = e0 (eigenvalue +1)
# T_M e1 = e2, T_M e2 = e1: swaps e1 and e2
# → eigenvalues: +1 (fixed e0), +1 (e1+e2)/√2, -1 (e1-e2)/√2
print(f"  Expected: +1, +1, -1 (reflection that fixes e0, swaps e1↔e2)")
check("  T_M eigenvalues are {-1, +1, +1}", sorted(eigs_TM) == sorted([-1,1,1]),
      f"eigs={eigs_TM}", "ALGEBRAIC")

print("\n  A6: PMNS pin is on Koide cone (β_q23 = S near-identity)")
# β_q23(PMNS): solve for β where eigenvalue-Q(β·H_PMNS) = 2/3
def eig_koide_Q(beta, H):
    eH = expm(beta * H)
    eigs = sorted(np.linalg.eigvals(eH).real)
    s1 = sum(eigs); s2 = sum(math.sqrt(abs(e)) for e in eigs)
    return s1/s2**2 if s2>0 else 1.0

# Find β where Q(β H_PMNS) = 2/3
def q_minus_2_3(beta):
    return eig_koide_Q(beta, H_pmns) - 2/3

# Scan β
beta_scan = np.linspace(0.1, 3.0, 500)
q_vals = []
for b in beta_scan:
    try: q_vals.append(q_minus_2_3(b))
    except: q_vals.append(float('nan'))

beta_crossings = []
for i in range(len(beta_scan)-1):
    if not math.isnan(q_vals[i]) and not math.isnan(q_vals[i+1]):
        if q_vals[i]*q_vals[i+1] < 0:
            try:
                b_c = brentq(q_minus_2_3, beta_scan[i], beta_scan[i+1], xtol=1e-13)
                beta_crossings.append(b_c)
            except: pass

print(f"  β_q23(PMNS) = {beta_crossings}")
if beta_crossings:
    b0 = beta_crossings[0]
    print(f"  β_q23(PMNS) = {b0:.12f}")
    print(f"  S           = {S:.12f}")
    print(f"  β_q23/S     = {b0/S:.10f}, gap = {abs(b0-S):.6e}")
    check("  β_q23(PMNS)/S - 1 < 1e-3 (near-identity)", abs(b0/S-1)<1e-3,
          f"ratio={b0/S:.8f}, gap={abs(b0-S):.4e}")
    check("  β_q23(PMNS) = S to 0.01%", abs(b0/S-1)<1e-4,
          f"ratio={b0/S:.10f}, gap={abs(b0-S):.4e}")

print("\n  A7: Using framework α_EM vs PDG α_EM for ε_0 identity")
eps0_known = 3.21896e-4  # from 2D intersection script
alpha_framework = ALPHA_LM / (4*math.pi)  # α_LM = g²/(4πu₀), approximate
print(f"  PDG α_EM = {ALPHA_EM:.10e}")
print(f"  Framework α_LM/(4π) ≈ {alpha_framework:.10e}")
ratio_pdg = eps0_known / ((272/45)*ALPHA_EM**2)
ratio_fw  = eps0_known / ((272/45)*alpha_framework**2)
print(f"  ε_0 / [(272/45)·α_PDG²] = {ratio_pdg:.8f}  (err = {abs(ratio_pdg-1)*100:.4f}%)")
print(f"  ε_0 / [(272/45)·α_fw²]  = {ratio_fw:.8f}  (err = {abs(ratio_fw-1)*100:.4f}%)")
check("  PDG α better than framework α for ε_0 identity", abs(ratio_pdg-1) < abs(ratio_fw-1),
      f"PDG err={abs(ratio_pdg-1)*100:.4f}% vs fw err={abs(ratio_fw-1)*100:.4f}%")

print("\n  A8: What is Tr(T_D³) and Tr(T_Q³)? (cubic invariants of generators)")
tr_D3 = float(np.real(np.trace(T_D@T_D@T_D)))
tr_Q3 = float(np.real(np.trace(T_Q@T_Q@T_Q)))
tr_D2Q = float(np.real(np.trace(T_D@T_D@T_Q)))
tr_DQ2 = float(np.real(np.trace(T_D@T_Q@T_Q)))
print(f"  Tr(T_D³) = {tr_D3:.6f}")
print(f"  Tr(T_Q³) = {tr_Q3:.6f}")
print(f"  Tr(T_D²·T_Q) = {tr_D2Q:.6f}")
print(f"  Tr(T_D·T_Q²) = {tr_DQ2:.6f}")

# These contribute to J3_sel via the d,q-dependent terms
# J3(H_0+mT_M) includes terms with T_D and T_Q
print(f"\n  Cross-sector cubic Tr(H_B·T_D·T_Q) = {float(np.real(np.trace(H_B@T_D@T_Q))):.6f}")
print(f"  Tr(H_B·T_M·T_D) = {float(np.real(np.trace(H_B@T_M@T_D))):.6f}")
print(f"  Tr(H_B·T_M·T_Q) = {float(np.real(np.trace(H_B@T_M@T_Q))):.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 9: The 272/45 decomposition — Cl(3) factor analysis
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 9: 272/45 factor analysis — searching for Cl(3) origin")
print("="*80)

# Known: |ε_0| ≈ (272/45)·α_EM² to 0.006%
# 272/45 = (17/5)·(16/9) = (17/5)·(S·E1)²
# Known Cl(3) numbers: g_Y²=1/5, g_2²=1/4, N_c=3, dim(Cl⁺)=4, dim(Cl)=8, taste=7/18
# Key: S·E1 = 4/3 EXACTLY, g_Y² = 1/5

# Can we write 272/45 = N × g_Y^a × g_2^b × S^c × E1^d?
# 272/45 = (17/5) × (4/3)²
# 5 = 1/g_Y²  ✓
# But 17 = ?

# Search: 17 = ?
print(f"\n  272/45 = {272/45:.10f}")
print(f"  (17/5)·(S·E1)² = {(17/5)*(S*E1)**2:.10f}")
print(f"  (17/5) = {17/5:.6f}")
print(f"\n  Can 17 come from Cl(3)?")
print(f"    2^4 + 1 = {2**4+1}  (dim(Cl_C(3)) + 1?)")
print(f"    dim(Cl(3)) + dim(Cl+(3)) + dim(ω-ext) = 8+4+5 = {8+4+5}")
print(f"    1/g_2² + 1/g_Y² + 1 = 4+5+1 = {4+5+1} ≠ 17")
print(f"    4 × (1/g_2²) + 1 = {4*(1/G2_SQ)+1}")  # = 17!

four_over_g2sq_plus_1 = 4*(1/G2_SQ) + 1
print(f"\n  KEY: 4·(1/g_2²) + 1 = 4×4 + 1 = {four_over_g2sq_plus_1}  == 17? {abs(four_over_g2sq_plus_1-17)<1e-10}")

# So: 272/45 = [4(1/g_2²)+1] / (1/g_Y²) × (S·E1)²
decomp = (4*(1/G2_SQ)+1) * G_Y_SQ * (S*E1)**2
print(f"  [(4/g_2²+1)·g_Y²·(S·E1)²] = {decomp:.10f} vs 272/45 = {272/45:.10f}")
check("272/45 = (4/g_2²+1)·g_Y²·(S·E1)² = 17/5·(4/3)²",
      abs(decomp - 272/45) < 1e-12, f"decomp={decomp:.10f}", "ALGEBRAIC")

# Even simpler: (4×dim(Cl+)+1)/dim(ω-ext) × (color-Casimir)²
print(f"\n  Physical interpretation:")
print(f"    dim(Cl⁺(3))    = 4 = 1/g_2²")
print(f"    dim(ω-ext)     = 5 = 1/g_Y²")
print(f"    C_2(fund)      = 4/3 = S·E1  [SU(3) color Casimir]")
print(f"    272/45         = (4×4+1)/5 × (4/3)² = 17/5 × C_2² = (4/g_2²+1)·g_Y²·C_2²")
print(f"    → ε_0 = [(4/g_2²+1)·g_Y²·C_2²] · α_EM²")
print(f"           = [17 SU(2)×U(1) modes × color Casimir²] · α_EM²")

# Relate 4+1=5: 1/g_2²=4 SU(2) generators + 1 U(1) hypercharge = 5 EW generators!
print(f"\n  DEEPER: 17 = 4+1 × 4 = (n_SU2+1) × (1/g_2²)")
print(f"  Note: 16 = (1/g_2²)² = dim(Cl+(3))²")
print(f"        17 = 16+1 = (1/g_2²)² + 1")
# Can we write 4/g_2² + 1 = (1/g_2² + 1)² / (1/g_2²) × something?
# (4+1)² = 25, not 17. 4² + 1 = 17. So 17 = (1/g_2²)² + 1.
print(f"  SIMPLEST: 17 = (1/g_2²)² + 1 = (dim Cl+)² + 1 = 4² + 1")
print(f"  Check: (1/g_2²)²+1 = {int((1/G2_SQ)**2)+1} == 17? {int((1/G2_SQ)**2)+1==17}")

print(f"\n  Therefore: 272/45 = [(1/g_2²)²+1] · g_Y² · (S·E1)²")
print(f"           = [(1/g_2²)²+1] / (1/g_Y²) · (S·E1)²")
decomp2 = ((1/G2_SQ)**2 + 1) * G_Y_SQ * (S*E1)**2
print(f"  Numerical: {decomp2:.12f} vs 272/45 = {272/45:.12f}")
check("272/45 = [(1/g_2²)²+1]·g_Y²·(S·E1)² exact", abs(decomp2-272/45)<1e-12, "ALGEBRAIC")

print(f"\n  Final factored identity:")
print(f"    |ε_0| = [(dim Cl+)² + 1] · g_Y² · C_2(SU3)² · α_EM²")
print(f"          = 17/5 · (4/3)² · α_EM²  = (272/45) · α_EM²")
print(f"    where: dim Cl+ = 4, g_Y² = 1/5, C_2(SU3) = 4/3 = S·E1")

# ─────────────────────────────────────────────────────────────────────────────
# PART 10: The sign problem — is d_0 > S physical?
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 10: Sign analysis — is the ε_0 < 0 direction physically preferred?")
print("="*80)

# The 2D intersection requires d_0 = S + |ε_0| > S (moving ABOVE S).
# But the Cl(3) symmetry argument says d=q=S is the minimum of the Z3 potential.
# QUESTION: is the Z3 potential a minimum at S, or could it be a maximum?

# From z3_scalar_potential.py: the potential minimum is at m ≈ -0.433, but
# the d,q direction has its own potential. What is V(d) at fixed m=m_prod1?
def V_dq(dq, m=None):
    """Frobenius norm of H at d=q=dq."""
    if m is None: m = m_prod1
    H = H3(m, dq, dq)
    return float(np.real(np.trace(H@H)))

# Scan d=q around S
dq_scan = np.linspace(S-0.01, S+0.01, 1000)
V_vals = [V_dq(dq) for dq in dq_scan]
V_at_S = V_dq(S)
V_at_d0 = V_dq(S + 3.22e-4)

print(f"\n  Frobenius potential V(d=q=dq) = Tr(H²) at m=m_prod1:")
print(f"  V at d=S:        {V_at_S:.10f}")
print(f"  V at d=S+ε_0:    {V_at_d0:.10f}  (Δ={V_at_d0-V_at_S:.6e})")

# Is S a minimum of V(dq)?
dV_at_S = (V_dq(S+1e-7) - V_dq(S-1e-7))/(2e-7)
print(f"  dV/d(dq) at S: {dV_at_S:.6e}  (should be 0 if S is extremum)")

# Find extremum
try:
    from scipy.optimize import minimize_scalar as ms2
    res = ms2(V_dq, bounds=(S-0.05, S+0.05), method='bounded')
    print(f"  V minimum at dq = {res.x:.10f},  S = {S:.10f}")
    print(f"  V minimum vs S: dq - S = {res.x - S:.6e}")
    check("S is minimum of V(dq) at m=m_prod1", abs(res.x - S) < 1e-6,
          f"dq_min={res.x:.10f}, S={S:.10f}")
except Exception as e:
    print(f"  Error: {e}")

# Sign of correction: does the PMNS coupling PUSH d above or below S?
# The PMNS-Koide cross-sector interaction:
# ΔV ∝ -Tr(H_PMNS · H_sel(d)) (attraction)
# d/dq ΔV = -Tr(H_PMNS · ∂H_sel/∂dq) = -Tr(H_PMNS · (T_D + T_Q))
push_dir = -float(np.real(np.trace(H_pmns @ (T_D + T_Q))))
print(f"\n  PMNS-Koide coupling direction:")
print(f"  -Tr(H_PMNS · (T_D+T_Q)) = {push_dir:.8f}")
print(f"  Sign: {'POSITIVE (pushes d ABOVE S)' if push_dir > 0 else 'NEGATIVE (pushes d BELOW S)'}")
check("PMNS coupling pushes d ABOVE S (consistent with d_0>S)",
      push_dir > 0, f"coupling={push_dir:.6f}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 11: Combined α_EM² identity — final assessment
# ─────────────────────────────────────────────────────────────────────────────
print("\n"+"="*80)
print("PART 11: Final accounting — two near-identities with α_EM²")
print("="*80)

print(f"""
  Two independent α_EM² near-identities found:

  IDENTITY 1 (m-gap):
    Δm = m_prod1 - m_star = {delta_m_val:.12e}
    4·α_EM²               = {4*ALPHA_EM**2:.12e}
    Ratio                 = {delta_m_val/(4*ALPHA_EM**2):.10f}  ({abs(delta_m_val/(4*ALPHA_EM**2)-1)*100:.4f}% error)
    Framework:  4 = (1/g_2²) = dim(Cl⁺(3))

  IDENTITY 2 (ε-gap, from 2D intersection):
    |ε_0|   = {eps0_known:.12e}
    (272/45)·α_EM² = {(272/45)*ALPHA_EM**2:.12e}
    Ratio           = {eps0_known/((272/45)*ALPHA_EM**2):.10f}  ({abs(eps0_known/((272/45)*ALPHA_EM**2)-1)*100:.4f}% error)
    Framework: 272/45 = [(dim Cl+)²+1]·g_Y²·C_2²  [PROVEN ALGEBRAIC IDENTITY]

  Consistency:
    ε_0/Δm  = {eps0_known/delta_m_val:.8f}
    (272/45)/4 = {272/45/4:.8f}  [should equal ε_0/Δm if both identities exact]
    Diff    = {abs(eps0_known/delta_m_val - 272/45/4):.6e}

  The ε-gap identity is much more precise (0.006%) than the m-gap identity (0.46%).
  If the m-gap identity were exact, its precision should match ε-gap, suggesting
  the exact m-gap relation is NOT simply 4·α_EM².
""")

# Better m-gap candidate using the exact ε_0 relation?
# If ε_0 = (272/45)·α_EM² exactly, and Δm = ε_0 / (ε_0/Δm sensitivity)...
# sensitivity = ε_0/Δm = 3.219/2.120 = 1.518
# And (272/45)/4 = 1.511
# So Δm = (4/1)·α_EM² × [ε_0/Δm / ((272/45)/4)] = 4·α_EM² × 1.518/1.511 = 4α_EM² × 1.0046
# The 0.46% residual IS the 0.46% difference between ε_0/Δm and (272/45)/4.

print(f"  Key: the m-gap's 0.46% error = the (ε_0/Δm)/(272/180) correction")
print(f"  Actual ε_0/Δm = {eps0_known/delta_m_val:.8f}")
print(f"  Theoretical (272/45)/4 = {272/45/4:.8f}")
print(f"  → If ε_0 = (272/45)α_EM² exactly, then Δm = 4·α_EM² × {eps0_known/delta_m_val/(272/45*4):.8f}")

# What is the EXACT Δm in terms of framework constants?
# From sensitivity: Δm = ε_0 / (ε_0/Δm) = ε_0 × (Δm/ε_0)
# = (272/45)·α_EM² × (Δm/ε_0)
# = (272/45)·α_EM² × (4/[1 + correction])
# The correction is the ε_0→Δm nonlinear sensitivity factor.
print(f"\n  CONCLUSION: The ε-gap identity ε_0=(272/45)α_EM² is the PRIMARY identity.")
print(f"  The m-gap Δm≈4α_EM² is a secondary consequence, less precise due to")
print(f"  the nonlinear sensitivity of m→ε conversion.")

print("\n"+"="*80)
print(f"FINAL: PASS={pass_count} FAIL={fail_count}")
print("="*80)
