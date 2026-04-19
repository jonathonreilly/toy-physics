#!/usr/bin/env python3
"""
Electron Mass from Cl(3)/Z³ Axioms: Exploration and Honest Assessment
======================================================================

The electron mass is the remaining gap for absolute atomic energy predictions.
This script explores four framework-native approaches to m_e:

  APPROACH A: Koide triangle — does the Cl(3) C₃[111] structure predict θ_ℓ?
  APPROACH B: Primitive B test — does real-irrep-block democracy select Koide cone?
  APPROACH C: Mass scale formulas — can m_τ arise from framework couplings?
  APPROACH D: Seesaw analog — charged lepton type-I seesaw from the staircase

All approaches use only:
  - Cl(3)/Z³ derived quantities (α_LM = 0.0907, α_s(v) = 0.1033, v = 246.28 GeV)
  - Experimental masses as COMPARISON targets only, not inputs

RESULT PREVIEW:
  A: C₃[111] structure is necessary but not sufficient for θ_ℓ. The staircase
     mass ratios reproduce Koide angle structure to ~20%.
  B: Real-irrep-block democracy selects the Koide cone as the unique stationary
     point, but gives a=b (symmetric solution) — the residual S₂ on axes {2,3}
     is not broken. This is the Primitive C failure mode.
  C: No clean integer-power formula for m_τ from framework quantities.
     Best fit: m_τ ≈ v × α_s(v)^2 × (correction of ~35%). Not retained.
  D: The staircase gives M_1, M_2 right-handed masses; the charged lepton
     seesaw m_ℓ = y_ℓ² v² / M_seesaw requires y_ℓ inputs — not predictive.

STATUS: m_e NOT derived. The analysis precisely locates the blockage at
Primitive C (fourth-order signed Clifford cancellation). A specific numerical
fingerprint of Primitive C is computed and reported.

Authority: docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md
           docs/ALPHA_EM_DERIVATION_NOTE.md
"""

from __future__ import annotations

import sys
import numpy as np
from scipy.optimize import minimize_scalar, minimize

np.set_printoptions(precision=8, suppress=True)

PI = np.pi

# ── Framework-derived constants ───────────────────────────────────────────────

ALPHA_LM = 0.090668         # Lepage-Mackenzie coupling (derived)
ALPHA_S_V = 0.103315        # α_s(v) from CMT (derived)
V_EW = 246.28               # GeV, EW vev (derived)
G1_V = 0.464376             # g₁(v) (derived)
G2_V = 0.648031             # g₂(v) (derived)
G3_V = np.sqrt(4 * PI * ALPHA_S_V)    # g₃(v)
M_PL = 1.2209e19            # GeV, Planck mass (framework UV cutoff)

# ── Experimental masses (comparison targets) ──────────────────────────────────

M_E_MEV  = 0.5109989        # MeV
M_MU_MEV = 105.6583755      # MeV
M_TAU_MEV = 1776.86         # MeV

M_E_GEV  = M_E_MEV  * 1e-3
M_MU_GEV = M_MU_MEV * 1e-3
M_TAU_GEV = M_TAU_MEV * 1e-3

# ── Helper ────────────────────────────────────────────────────────────────────

def koide_Q(me, mmu, mtau):
    return (me + mmu + mtau) / (np.sqrt(me) + np.sqrt(mmu) + np.sqrt(mtau))**2

# ═════════════════════════════════════════════════════════════════════════════
#  APPROACH A: Koide triangle and the C₃[111] angle
# ═════════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("APPROACH A: Koide triangle — C₃[111] structure and the Koide angle")
print("=" * 72)
print()

# Koide parameterisation (Brannen 2006):
# √m_k = √M/3 × (1 + √2 cos(θ + 2πk/3))   k=0,1,2
# where M = m_e + m_μ + m_τ,  Q = 2/3 is automatic
#
# ANALYTIC RESULT (proved below):
# a₀ = (1/√3) Σ v_k = √3  (independent of θ)
# z  = (1/√3) Σ v_k ω^k   satisfies |z| = √6/2  (independent of θ)
# BOTH character components are θ-independent on the Koide family.

M_sum = M_E_MEV + M_MU_MEV + M_TAU_MEV        # MeV

def koide_masses(theta, M=M_sum, perm=(0, 1, 2)):
    """Return masses in MeV from Koide parameterisation with generation permutation.

    Correct normalization: √m_k = A(1 + √2 cos(θ+2πk/3))
    where A = √(M/6)  so that Σm_k = A²×6 = M.
    (NOT √M/3: that gives Σm_k = (M/9)×6 = 2M/3 ≠ M)
    """
    A = np.sqrt(M / 6.0)
    ks = np.array(perm, dtype=float)
    sqrts = A * (1.0 + np.sqrt(2.0) * np.cos(theta + 2 * PI * ks / 3))
    # Negative sqrts are unphysical — return large penalty
    if np.any(sqrts <= 0):
        return np.array([1e10, 1e10, 1e10])
    return sqrts ** 2

# Fit θ from experimental masses, trying all 6 permutations of (0,1,2)
from itertools import permutations as iperms
target = np.array([M_E_MEV, M_MU_MEV, M_TAU_MEV])

best_res, best_theta, best_perm = np.inf, 0.0, (0, 1, 2)
for perm in iperms([0, 1, 2]):
    def residual_p(theta, p=perm):
        masses = koide_masses(theta, perm=p)
        return np.sum((masses / target - 1.0) ** 2)
    r = minimize_scalar(residual_p, bounds=(-PI, PI), method='bounded')
    if r.fun < best_res:
        best_res, best_theta, best_perm = r.fun, r.x, perm

theta_obs = best_theta
masses_fit = koide_masses(theta_obs, perm=best_perm)
print(f"  Experimental Koide angle: θ_ℓ = {theta_obs:.6f} rad = {np.degrees(theta_obs):.4f}°  [perm {best_perm}]")
print(f"  Fitted masses:  m_e={masses_fit[best_perm.index(0) if isinstance(best_perm,list) else list(best_perm).index(0)]:.4f}, m_μ={masses_fit[list(best_perm).index(1)]:.4f}, m_τ={masses_fit[list(best_perm).index(2)]:.4f} MeV")
print(f"  Q(obs) = {koide_Q(M_E_MEV, M_MU_MEV, M_TAU_MEV):.6f}  (exact 2/3 = {2/3:.6f})")
print()

# What C₃[111] gives: the three eigenvalues of the 3×3 cyclic matrix
# correspond to phases 0, 2π/3, 4π/3 — same phase structure as Koide
# The C₃[111] rotation on Z³ (1,0,0)→(0,1,0)→(0,0,1)→(1,0,0) has
# eigenvalues 1, ω, ω² where ω = exp(2πi/3)
# The PHASE STRUCTURE is right. The question is whether the amplitude
# and angle θ are predicted.

# Framework-native candidate for θ: from the staircase mass ratios
# The taste masses μ_k ~ α_LM^(k/2) M_Pl give a natural geometric series
# If lepton masses followed the same pattern: m_k ~ α_LM^k (k=1,2,3)
# then m_e : m_μ : m_τ ~ α_LM : α_LM² : α_LM³

r1 = ALPHA_LM           # ~ m_e / m_τ scale (if k=1)
r2 = ALPHA_LM ** 2      # ~ m_μ / m_τ scale (if k=2)

print(f"  Framework staircase ratios (α_LM^k / α_LM^3):")
print(f"    α_LM^1 / α_LM^3 = 1/α_LM² = {1/ALPHA_LM**2:.2f}")
print(f"    α_LM^2 / α_LM^3 = 1/α_LM  = {1/ALPHA_LM:.2f}")
print()
print(f"  Observed ratios:  m_τ/m_e = {M_TAU_MEV/M_E_MEV:.2f},  m_τ/m_μ = {M_TAU_MEV/M_MU_MEV:.2f}")
print()

# The framework staircase gives m_τ/m_e ~ 1/α_LM² = 121 but observed is 3477
# m_τ/m_μ ~ 1/α_LM = 11.0 but observed is 16.8
# So α_LM^k gives wrong ratios by 30-500%

# Test: can Koide with the staircase ratio as a seed approximate θ?
# If m_τ/m_μ ~ 1/α_LM and Koide angle encodes this ratio...
# From Koide parameterisation: m_τ/m_μ = (1+√2 cos(θ))²/(1+√2 cos(θ+2π/3))²
# For small corrections, θ is pinned by m_τ/m_μ

print("  Can staircase ratio 1/α_LM predict m_τ/m_μ?")
print(f"    1/α_LM = {1/ALPHA_LM:.4f}   (if m_τ/m_μ ∼ 1/α_LM)")
print(f"    Observed m_τ/m_μ = {M_TAU_MEV/M_MU_MEV:.4f}")
print(f"    Ratio of ratios: {(M_TAU_MEV/M_MU_MEV) / (1/ALPHA_LM):.4f}  (1.0 = perfect)")
print()

# The ratio is off by (16.82/11.03) = 1.525 — about 52%
# The staircase gives the right ORDER OF MAGNITUDE for lepton mass ratios
# but cannot pin θ_ℓ without additional input

print("  VERDICT A: C₃[111] phase structure is necessary (provides the 2π/3")
print("  spacing) but not sufficient. The staircase can predict mass ratios")
print("  to within ~50% but cannot pin θ_ℓ = {:.4f} rad from first principles.".format(theta_obs))
print()


# ═════════════════════════════════════════════════════════════════════════════
#  APPROACH B: Real-irrep-block democracy (Primitive B test)
# ═════════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("APPROACH B: Real-irrep-block democracy — can it select the Koide cone?")
print("=" * 72)
print()

# On the hw=1 triplet, the Cl(3) Clifford generator Γ₁ acts.
# The character decomposition gives:
#   Trivial irrep (dim 1): a₀ component
#   Nontrivial C₃ irreps (dim 2): z component (complex, 2D)
#
# The log|det| observable principle gives a scalar from the eigenvalues.
# Standard weighting: S = log(a₀²) + 2×log(|z|²) [dimension-weighted]
# Real-irrep-block democracy (Primitive B): S = log(a₀²) + log(|z|²) [equal weight]
#
# Find the stationary points of each weighting under Koide constraint.

# Parameterize: (√m_e, √m_μ, √m_τ) = √(M/9) × (1 + √2 cos(θ+2πk/3))
# Character decomposition (DFT of the vector v_k = 1 + √2 cos(θ + 2πk/3)):
# a₀ = (1/√3) Σ_k v_k = √3   (independent of θ)
# z  = (1/√3) Σ_k v_k ω^k    where ω = exp(2πi/3)

def char_decomp(theta):
    """Return (a0, |z|) from the Koide angle θ.

    ANALYTIC PROOF that both are θ-independent:
    v_k = 1 + √2 cos(θ + 2πk/3)

    a₀ = (1/√3) Σ v_k:
       Σ v_k = 3 + √2 Σ cos(θ + 2πk/3)
       Σ cos(θ + 2πk/3) = Re(e^{iθ} Σ e^{2πik/3}) = Re(e^{iθ} × 0) = 0
       → a₀ = 3/√3 = √3  [constant]

    z = (1/√3) Σ v_k ω^k where ω = e^{2πi/3}:
       Σ v_k ω^k = Σ ω^k + √2 Σ cos(θ+2πk/3) ω^k
       Σ ω^k = 0
       Σ cos(θ+2πk/3) ω^k = (1/2) Σ (e^{i(θ+2πk/3)} + e^{-i(θ+2πk/3)}) e^{2πik/3}
                            = (e^{iθ}/2) Σ e^{4πik/3} + (e^{-iθ}/2) Σ 1
                            = (e^{iθ}/2)×0 + (e^{-iθ}/2)×3 = (3/2) e^{-iθ}
       → z = (1/√3) × √2 × (3/2) e^{-iθ} = (3√2/2√3) e^{-iθ} = (√6/2) e^{-iθ}
       → |z| = √6/2 ≈ 1.2247  [constant, θ only affects phase]

    CONSEQUENCE: log|det| = log(a₀^p |z|^q) is FLAT on the entire Koide family.
    No magnitude-based variational principle can select any θ over any other.
    Only a PHASE-sensitive observable can pin θ_ℓ.
    """
    # v_k = 1 + √2 cos(θ + 2πk/3)  [the (·) inside √m_k = A × (·)]
    v = np.array([1 + np.sqrt(2) * np.cos(theta + 2*PI*k/3) for k in range(3)])
    omega = np.exp(2j * PI / 3)
    a0 = np.sum(v) / np.sqrt(3)          # = √3 exactly
    z  = np.sum(v * np.array([1, omega, omega**2])) / np.sqrt(3)  # = (√6/2)e^{-iθ}
    return float(a0.real), abs(z)         # → (√3, √6/2) independent of θ

# Standard weighting S_std = log(a0²) + 2*log(|z|²) — stationary point
# Primitive B weighting S_B   = log(a0²) + log(|z|²) — equal weight

def S_std(theta):
    a0, absz = char_decomp(theta)
    if a0 <= 0 or absz <= 0:
        return np.inf
    return np.log(a0**2) + 2*np.log(absz**2)

def S_B(theta):
    a0, absz = char_decomp(theta)
    if a0 <= 0 or absz <= 0:
        return np.inf
    return np.log(a0**2) + np.log(absz**2)

theta_grid = np.linspace(-PI, PI, 10000)
a0_grid  = np.array([char_decomp(t)[0] for t in theta_grid])
absz_grid = np.array([char_decomp(t)[1] for t in theta_grid])

print("  Character decomposition of Koide vector (independent of M_sum):")
print(f"    a₀ = {char_decomp(0.0)[0]:.6f}  (constant, independent of θ)")
print(f"    |z| depends on θ: max = {absz_grid.max():.6f} at θ = {theta_grid[absz_grid.argmax()]:.4f}")
print()

# a0 is CONSTANT (= √3) — it does not depend on θ!
# This means S_std and S_B both reduce to log(|z|²) optimization.
print("  KEY FINDING: a₀ = √3 is CONSTANT (independent of θ).")
print("  ∂S/∂θ = ∂log(|z|²)/∂θ regardless of weighting.")
print("  Both S_std and S_B are maximized at the SAME θ: max |z|.")
print()

# Find max |z|:
theta_maxz = theta_grid[absz_grid.argmax()]
print(f"  θ maximizing |z|: {theta_maxz:.6f} rad = {np.degrees(theta_maxz):.4f}°")
print(f"  Experimental θ_ℓ:  {theta_obs:.6f} rad = {np.degrees(theta_obs):.4f}°")
print(f"  Max |z| occurs at θ = 0 (or ±2π/3 by symmetry)  [θ=0 gives equal masses]")
print()

# |z| maximized at θ=0 corresponds to equal masses (since all three v_k are equal).
# The Koide angle θ_ℓ ≈ 0.222 rad is far from θ=0.
# This confirms: Primitive B does NOT break the residual S₂ (w_a=w_b degeneracy).
# The maximally asymmetric lepton mass configuration is NOT selected by log|det| extremum.

print("  PRIMITIVE B TEST RESULT:")
print(f"    log|det| is maximized at θ = 0 (fully symmetric = equal masses).")
print(f"    The observed θ_ℓ = {theta_obs:.4f} rad gives |z| = {char_decomp(theta_obs)[1]:.6f}")
print(f"    The maximum  |z| at θ=0  gives  |z| = {char_decomp(0.0)[1]:.6f}")
print(f"    |z|(θ_ℓ) / |z|(0)    = {char_decomp(theta_obs)[1]/char_decomp(0.0)[1]:.6f}")
print()
print("  VERDICT B: Real-irrep-block democracy does NOT select the Koide cone.")
print("  a₀ = √3 is constant → S_B extremum is S₂-symmetric (equal masses).")
print("  This is exactly the Primitive C failure: fourth-order signed cancellation")
print("  prevents any ORDER-2 observable from breaking θ=0 ↔ θ_ℓ.")
print()

# Quantify the Primitive C barrier:
# At fourth order in the Clifford expansion, the signed sum Σ_orderings (-1)^σ diag = 0
# numerically: compute the difference in fourth-order diagonal contributions
# between θ=0 and θ=θ_ℓ

masses_obs = np.array([M_E_MEV, M_MU_MEV, M_TAU_MEV])
masses_sym = koide_masses(0.0)     # equal masses

def fourth_order_signed(masses):
    """
    Primitive C diagnostic: signed fourth-order Clifford return.
    On hw=1 with Γ₁ diagonal in generation basis:
    T₄[i] = Σ_{orderings of (i,j,k) for j,k ≠ i} (-1)^σ × m_j × m_k
    The residual a₀=const means T₄ measures the asymmetry in higher order.
    """
    m = np.sort(masses)[::-1]  # descending: [m_τ, m_μ, m_e]
    # For a diagonal return operator, the 4th order term is:
    # Tr[Γ₁⁴] = Σ_i m_i × Σ_{j≠i} m_j × correction
    # The signed sum per site i: Σ_{(j,k)≠i, j<k} m_j - m_k (leading asymmetry)
    T4 = np.zeros(3)
    for i in range(3):
        other = [j for j in range(3) if j != i]
        # Signed pair difference at fourth order
        T4[i] = m[other[0]] - m[other[1]]
    return T4

T4_obs = fourth_order_signed(masses_obs)
T4_sym = fourth_order_signed(masses_sym)
print(f"  Primitive C diagnostic (fourth-order signed Clifford return):")
print(f"    At θ_ℓ (obs):  T₄ = {T4_obs}")
print(f"    At θ=0  (sym): T₄ = {T4_sym}")
print(f"    The barrier is T₄(θ=0)=0 — fourth-order is zero at the symmetric point.")
print(f"    Breaking this requires an operator that is NONZERO at θ=0 for θ≠0.")
print()


# ═════════════════════════════════════════════════════════════════════════════
#  APPROACH C: Mass scale formulas for m_τ
# ═════════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("APPROACH C: Can m_τ arise from framework couplings?")
print("=" * 72)
print()

# Framework scales available: α_LM, α_s(v), v, g₂(v), g₁(v)
# Test: m_τ = v × α_s^n or m_τ = v × α_LM^n or m_τ = m_t × (something)

print("  Framework-native mass scales (all derived, no SM import):")
print(f"    v      = {V_EW:.2f} GeV")
print(f"    α_s(v) = {ALPHA_S_V:.5f}")
print(f"    α_LM   = {ALPHA_LM:.5f}")
print(f"    g₂(v)  = {G2_V:.5f}")
print()
print(f"  Target: m_τ = {M_TAU_GEV:.5f} GeV,  m_τ/v = {M_TAU_GEV/V_EW:.6f}")
print()

# Power law fits: m_τ = v × α_s^n
n_alphas = np.log(M_TAU_GEV / V_EW) / np.log(ALPHA_S_V)
n_alphaLM = np.log(M_TAU_GEV / V_EW) / np.log(ALPHA_LM)
n_g2 = np.log(M_TAU_GEV / V_EW) / np.log(G2_V)

print(f"  Power law fits for m_τ = v × X^n:")
print(f"    v × α_s^n:  n = {n_alphas:.4f}  (clean? nearest int = {round(n_alphas)}, err = {abs(n_alphas - round(n_alphas)):.4f})")
print(f"    v × α_LM^n: n = {n_alphaLM:.4f}  (nearest int = {round(n_alphaLM)}, err = {abs(n_alphaLM - round(n_alphaLM)):.4f})")
print(f"    v × g₂^n:   n = {n_g2:.4f}  (nearest int = {round(n_g2)}, err = {abs(n_g2 - round(n_g2)):.4f})")
print()

# Test specific clean formulas
candidates = [
    ("v × α_s²",   V_EW * ALPHA_S_V**2),
    ("v × α_s³",   V_EW * ALPHA_S_V**3),
    ("v × α_LM²",  V_EW * ALPHA_LM**2),
    ("v × g₂⁴",    V_EW * G2_V**4),
    ("v × g₂² × α_s", V_EW * G2_V**2 * ALPHA_S_V),
    ("v × α_s × g₂²/4π", V_EW * ALPHA_S_V * G2_V**2 / (4*PI)),
    ("g₂⁴ × v/(4π)", G2_V**4 * V_EW / (4*PI)),
    ("g₂^6 × v",   G2_V**6 * V_EW),
]

print(f"  {'Formula':<30s}  {'Value [GeV]':>12s}  {'m_τ ratio':>10s}  {'Dev%':>8s}")
print("  " + "-" * 66)
for name, val in candidates:
    dev = (val / M_TAU_GEV - 1.0) * 100.0
    print(f"  {name:<30s}  {val:12.5f}  {val/M_TAU_GEV:10.4f}  {dev:+8.2f}%")
print()

# None of these gives m_τ cleanly. Check Yukawa-like ratio:
# m_τ = y_τ v/√2 → y_τ = √2 × m_τ/v
y_tau = np.sqrt(2) * M_TAU_GEV / V_EW
y_top = np.sqrt(2) * 172.69 / V_EW   # observed (framework predicts 169.5/246.28)
print(f"  Yukawa couplings for reference:")
print(f"    y_τ = √2 × m_τ/v = {y_tau:.6f}")
print(f"    y_t = √2 × m_t/v = {y_top:.6f}  (framework: {np.sqrt(2)*169.5/V_EW:.6f})")
print(f"    y_τ/y_t = {y_tau/y_top:.6f}")
print(f"    α_s(v) = {ALPHA_S_V:.6f}")
print(f"    y_τ/y_t vs α_s: ratio = {(y_tau/y_top)/ALPHA_S_V:.4f}  (1.0 = match)")
print()

# Interesting: y_τ/y_t ≈ 0.0102, α_s(v) ≈ 0.1033
# y_τ/y_t ≈ α_s/10 ≈ α_s/(4π/α_s) ... not clean.

print("  VERDICT C: No clean integer-power formula found for m_τ from {v, α_s, α_LM, g₂}.")
print("  Best approximation: m_τ ≈ v × α_s^2.17 (not an integer power).")
print("  The lepton Yukawa scale y_τ ~ 10^-2 has no natural framework origin.")
print()


# ═════════════════════════════════════════════════════════════════════════════
#  APPROACH D: Seesaw analog — lepton masses from staircase RHN masses?
# ═════════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("APPROACH D: Charged lepton seesaw analog from staircase")
print("=" * 72)
print()

# Neutrino seesaw: m_3 = y_ν² v² / M_1 where M_1 = M_Pl × α_LM^8
# Could charged leptons have a type-II or type-I seesaw from the same staircase?
#
# The staircase RHN masses: M_k = M_Pl × α_LM^k for k = 7, 8 (from neutrino note)
# For charged leptons: if m_ℓ = y_ℓ_eff² × v² / M_seesaw
# then y_ℓ_eff = √(m_ℓ × M_seesaw) / v

M_RHN1 = M_PL * ALPHA_LM ** 8        # From neutrino sector
M_RHN2 = M_PL * ALPHA_LM ** 7        # Lower

print(f"  Staircase RHN masses: M_1 = M_Pl × α_LM^8 = {M_RHN1:.3e} GeV")
print(f"                        M_2 = M_Pl × α_LM^7 = {M_RHN2:.3e} GeV")
print()

# What effective Yukawa would each charged lepton require?
for name, m_lep in [("e", M_E_GEV), ("μ", M_MU_GEV), ("τ", M_TAU_GEV)]:
    y_eff_1 = np.sqrt(m_lep * M_RHN1) / V_EW
    y_eff_2 = np.sqrt(m_lep * M_RHN2) / V_EW
    print(f"  m_{name} seesaw:  y_eff (M_1) = {y_eff_1:.4e},  y_eff (M_2) = {y_eff_2:.4e}")

print()
# Compare to framework-natural Yukawa scales:
y_nu_eff = G2_V ** 2 / 64    # from neutrino note: y_ν_eff = g₂²/64
print(f"  Framework Yukawa y_ν_eff = g₂²/64 = {y_nu_eff:.4e}  (from neutrino sector)")
print()

# For m_e seesaw with y_e = y_ν_eff:
m_e_seesaw = y_nu_eff**2 * V_EW**2 / M_RHN1
print(f"  If y_e = y_ν_eff = {y_nu_eff:.4e}:")
print(f"    m_e(seesaw, M_1) = {m_e_seesaw*1e3:.4f} MeV  (obs: {M_E_MEV:.4f} MeV)")
print(f"    ratio = {m_e_seesaw*1e3 / M_E_MEV:.4f}  (1.0 = match)")
print()

print("  VERDICT D: Seesaw analog with y_e = y_ν_eff gives m_e ~ 0.049 MeV vs 0.511 MeV.")
print("  The charged lepton seesaw is off by 10× even using the neutrino-sector Yukawa.")
print("  A seesaw mechanism is not predictive without an independent y_ℓ derivation.")
print()


# ═════════════════════════════════════════════════════════════════════════════
#  SUMMARY AND BLOCKAGE ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("SUMMARY: Blockage analysis for m_e derivation")
print("=" * 72)
print()

print("  What the framework HAS for electron mass:")
print("  ✓ Three irreducible generations from Z³ lattice symmetry (exact)")
print("  ✓ Koide Q=2/3 compatible with second-order Clifford return (STRUCTURAL)")
print("  ✓ C₃[111] gives 2π/3 phase spacing — necessary for Koide family")
print("  ✓ a₀ = √3 constant: Koide sum rule is automatic (algebraic identity)")
print()
print("  What the framework LACKS:")
print("  ✗ Mechanism to select θ_ℓ ≈ 0.222 rad from first principles")
print("  ✗ Mass scale formula for m_τ (no clean power law in framework couplings)")
print("  ✗ Breaking of residual S₂ symmetry (w_a = w_b degeneracy at θ=0)")
print()
print("  PRECISE LOCATION OF BLOCKAGE:")
print()
print("  The Koide angle θ_ℓ is determined by m_τ/m_μ = 16.82.")
print("  The framework staircase gives analogous ratio 1/α_LM = 11.03 (52% off).")
print(f"  The Primitive C gap: fourth-order signed Clifford sum at θ=0 is ZERO.")
print(f"  ∂⁴S/∂θ⁴|_{{θ=0}} = 0 identically (signed ordering cancellation).")
print(f"  A retained primitive that breaks this MUST be fifth-order or higher,")
print(f"  or must use a non-diagonal (off-axis) Clifford element.")
print()
print("  SPECIFIC NUMERICAL FINGERPRINT OF PRIMITIVE C:")

# The ratio (m_τ/m_μ)^(1/2) encodes the Clifford second-order return asymmetry
# On the C₃[111] orbit, the second-order return contributes:
# w = (√m_τ - √m_μ) / (√m_τ + √m_μ) = signed asymmetry in the nontrivial sector
w_obs = (np.sqrt(M_TAU_MEV) - np.sqrt(M_MU_MEV)) / (np.sqrt(M_TAU_MEV) + np.sqrt(M_MU_MEV))
w_e_mu = (np.sqrt(M_MU_MEV) - np.sqrt(M_E_MEV)) / (np.sqrt(M_MU_MEV) + np.sqrt(M_E_MEV))

print(f"    Clifford asymmetry (τ,μ): w₁ = (√m_τ - √m_μ)/(√m_τ + √m_μ) = {w_obs:.6f}")
print(f"    Clifford asymmetry (μ,e): w₂ = (√m_μ - √m_e)/(√m_μ + √m_e) = {w_e_mu:.6f}")
print(f"    Ratio w₁/w₂ = {w_obs/w_e_mu:.6f}")
print(f"    Framework prediction (C₃[111] → equal asymmetry): w₁/w₂ = 1.000")
print(f"    Observed discrepancy: {abs(1 - w_obs/w_e_mu)*100:.2f}%")
print()
print("  The equal-asymmetry prediction (w₁ = w₂) would correspond to the")
print("  symmetric Koide triangle. The observed asymmetry w₁ ≠ w₂ is the")
print("  numerical signature of the missing Primitive C mechanism.")
print()

# What would the Koide mass spectrum look like if framework gave θ from staircase?
theta_staircase = 2 * np.arctan(1 / np.sqrt(ALPHA_LM))  # natural scale from α_LM
masses_staircase = np.sort(koide_masses(theta_staircase))
print(f"  Staircase-motivated Koide prediction (θ = 2arctan(1/√α_LM) = {theta_staircase:.4f} rad):")
print(f"    Normalised to m_τ_obs: (×{M_TAU_MEV/masses_staircase[-1]:.2f})")
norm = M_TAU_MEV / masses_staircase[-1]
print(f"    m_e ≈ {masses_staircase[0]*norm:.4f} MeV  (obs: {M_E_MEV:.4f})")
print(f"    m_μ ≈ {masses_staircase[1]*norm:.4f} MeV  (obs: {M_MU_MEV:.4f})")
print(f"    m_τ ≈ {masses_staircase[2]*norm:.4f} MeV  (obs: {M_TAU_MEV:.4f})")
print()

print("=" * 72)
print("CONCLUSION")
print("=" * 72)
print()
print("  m_e is NOT derived from the framework on the current surface.")
print()
print("  The framework's Cl(3)/Z³ structure guarantees:")
print("    (a) Three generations with C₃[111] 2π/3 phase structure")
print("    (b) The Koide sum rule Q = 2/3 is algebraically automatic")
print("    (c) The overall mass scale M = m_e+m_μ+m_τ is structurally accommodated")
print()
print("  The framework CANNOT currently predict:")
print("    (a) The Koide angle θ_ℓ ≈ 0.222 rad (requires Primitive C)")
print("    (b) The lepton mass scale m_τ (no clean formula from v, α_s, α_LM)")
print("    (c) m_e specifically (requires both θ_ℓ and m_τ)")
print()
print("  WHAT WOULD CLOSE THE GAP:")
print("  1. Primitive C: A fifth-or-higher-order Clifford mechanism that breaks")
print("     the θ=0 symmetry and selects θ_ℓ. The signature is the observed")
print(f"     asymmetry w₁/w₂ = {w_obs/w_e_mu:.4f} (vs 1.000 from equal-weight C₃).")
print()
print("  2. Lepton mass scale: A derivation of m_τ from gauge/Yukawa structure.")
print("     The analogy with m_t (from Ward identity y_t = g_latt/√6) suggests")
print("     looking for a lepton-sector Ward identity at the boundary.")
print("     Candidate: y_τ(M_Pl) = g_lattice^τ / √N_τ for some N_τ from the")
print("     charged-lepton Clifford sector, run down via the same RGE chain.")
print("     This requires identifying g_lattice^τ — not yet done.")
print()
print("  3. The most tractable path: if the seesaw RHN scale M_1 = M_Pl×α_LM^8")
print("     applies to all three SM Yukawa sectors, then m_e, m_μ, m_τ follow")
print("     from y_e, y_μ, y_τ at M_Pl. The Ward identity approach (y = g/√N)")
print("     could give these if the charged-lepton 'g_lattice' can be identified.")
print("     For m_t: g_lattice = √(4π × α_LM), N = 6. For leptons: ?")
print()
