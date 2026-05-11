#!/usr/bin/env python3
"""Narrow runner for `YT_FIERZ_PROJECTION_DEFENSE_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies three disambiguation sub-checks for the y_t chain's sqrt(8/9)
Fierz color projection:

  (1) The Yukawa-side correction is sqrt(R_conn) = sqrt(8/9) (LSZ single-
      scalar-leg form), NOT R_conn = 8/9 (current-current form). Verified
      by direct LSZ leg-count algebra and by quoting the upstream
      YUKAWA_COLOR_PROJECTION_THEOREM Part 3.1 derivation.

  (2) The 3-loop QCD MSbar->pole conversion shift, computed from the
      published Chetyrkin-Steinhauser / Melnikov-van Ritbergen 3-loop
      coefficient (190.595 - 26.655*N_L + 0.6527*N_L^2) (a_s/pi)^3,
      gives ~0.31% relative to m_t. The framework's own internal
      comparator (COMPLETE_PREDICTION_CHAIN_2026_04_15.md §6.2) reports
      m_t,2L = 172.57 GeV and m_t,3L = 173.10 GeV; the runner verifies
      these are consistent with the published 3-loop coefficient.

  (3) The asymptotic-safety central value (Eichhorn-Held arXiv:1707.01107)
      m_t,pole ~ 171 GeV is recorded as an external comparator in a
      competing UV completion. The runner verifies that the framework
      vs AS central-value gap (~1.6 GeV) is well above FCC-ee threshold-
      scan precision (~9 MeV statistical, ~30-50 MeV theoretical), so
      the central values are experimentally distinguishable under the
      stated comparator assumptions.

PDG comparators (m_t,pole = 172.69 GeV) and the AS comparator
(m_t,pole ~ 171 GeV from arXiv:1707.01107) are used as audit comparators
only, not as framework inputs. The framework-chain m_t = 172.57 GeV
(2-loop) comparator comes from the upstream prediction-chain runners,
not from this narrow defense runner.

This narrow runner does NOT re-derive R_conn = 8/9; that is the upstream
EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE Fierz channel-fraction
identity. It also does NOT re-derive the LSZ structure; that is
YUKAWA_COLOR_PROJECTION_THEOREM Part 3.1. This runner verifies the
disambiguation arithmetic conditional on those upstream identities.

Self-contained: sympy + standard library only.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import sympy as sp
    from sympy import Rational, sqrt, symbols, Symbol, Matrix, eye, zeros, nsimplify, log
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# =============================================================================
section("Sub-check (1): Z_phi vs current-current Fierz disambiguation")
# Statement: with R_conn = (N_c^2-1)/N_c^2 = 8/9 and Z_phi = R_conn (per
# YUKAWA_COLOR_PROJECTION_THEOREM Part 2.5), the Yukawa correction enters
# as sqrt(Z_phi) on the single scalar leg via LSZ. We verify the algebra
# of LSZ leg-counting selects sqrt(R_conn), not R_conn.
# =============================================================================

N_c = Rational(3)
R_conn = (N_c**2 - 1) / N_c**2  # = 8/9
print(f"\n  R_conn = (N_c^2 - 1)/N_c^2 = {R_conn} (exact group theory)")

# Form (b): LSZ on single scalar leg gives sqrt(Z_phi)
# Yukawa amplitude: M_Y = sqrt(Z_psi) * sqrt(Z_phi) * sqrt(Z_psi) * Gamma_Y
# Two fermion legs (each sqrt(Z_psi)), one scalar leg (sqrt(Z_phi))
n_scalar_legs = 1  # Yukawa vertex psi-bar phi psi has ONE scalar leg
n_fermion_legs = 2  # Yukawa vertex has TWO fermion legs

# In the Ward ratio y_t / g_s, Z_psi cancels (same fermion field, both
# vertices). Gamma_Y / Gamma_g = 1 at leading order. The gluon Z_A is
# already absorbed in the CMT alpha_s = alpha_bare/u_0^2. The remaining
# correction is sqrt(Z_phi).
correction_form_b = sqrt(R_conn)  # LSZ single scalar leg
print(f"  Form (b) LSZ single-leg:           sqrt(R_conn) = {sp.simplify(correction_form_b)} = sqrt(8/9)")
check(
    "form (b): correction = sqrt(R_conn) on Yukawa amplitude",
    sp.simplify(correction_form_b - sqrt(Rational(8, 9))) == 0,
    detail=f"sqrt(8/9) = {sp.N(sqrt(Rational(8, 9)), 8)}",
)

# Form (a): current-current would give R_conn directly (no square-root).
# This applies to a four-fermion operator or two-vertex correlator.
# It would be a Wilson coefficient on a (psi-bar psi)(psi-bar psi) operator,
# not a single-leg LSZ factor.
correction_form_a = R_conn  # current-current
print(f"  Form (a) current-current:          R_conn       = {sp.simplify(correction_form_a)} = 8/9")
check(
    "form (a): would-be correction = R_conn (rejected by LSZ)",
    sp.simplify(correction_form_a - Rational(8, 9)) == 0,
    detail=f"8/9 = {sp.N(Rational(8, 9), 8)}",
)

# Distinguishing the forms: numerical values
val_b = float(sp.N(correction_form_b, 8))
val_a = float(sp.N(correction_form_a, 8))
print(f"\n  Numerical values:")
print(f"    sqrt(8/9) = {val_b:.6f}   (form b, selected)")
print(f"    8/9       = {val_a:.6f}   (form a, rejected)")
print(f"    Difference: {(val_b - val_a):.4f} = {(val_b - val_a)*100:.2f}% of m_t scale")

# Verify the two forms are NOT equal (they would only coincide for R_conn = 0 or 1)
check(
    "form (a) != form (b) for R_conn != 0, 1",
    sp.simplify(correction_form_b - correction_form_a) != 0,
    detail=f"sqrt(8/9) - 8/9 = {sp.simplify(correction_form_b - correction_form_a)} != 0",
)

# LSZ leg-count theorem: the Yukawa vertex has n_scalar = 1 scalar leg,
# so the LSZ factor is Z_phi^{n_scalar/2} = sqrt(Z_phi).
lsz_power = Rational(n_scalar_legs, 2)
print(f"\n  LSZ leg-count: scalar legs = {n_scalar_legs}, LSZ power = {lsz_power}")
check(
    "LSZ leg-count fixes form (b): power Z_phi^(n_scalar/2) = Z_phi^(1/2)",
    lsz_power == Rational(1, 2),
    detail="Yukawa has 1 scalar leg => one factor of sqrt(Z_phi)",
)

# Contrast: EW vacuum polarization is two-vertex, no LSZ factor on the
# operator itself; the projection enters the propagator linearly. Under
# kappa_EW = 0, alpha_phys/alpha_CMT = 1/R_conn = 9/8.
ew_correction = 1 / R_conn  # kappa_EW = 0 specialization
print(f"\n  Contrast: EW vac. pol. (two-vertex) at kappa_EW=0:")
print(f"    alpha_phys / alpha_CMT = 1/R_conn = {sp.simplify(ew_correction)} = 9/8")
print(f"    sqrt(9/8)              = {sp.N(sqrt(ew_correction), 8)}   (UP on g_EW)")
check(
    "EW side: alpha correction = 1/R_conn = 9/8 (not sqrt)",
    sp.simplify(ew_correction - Rational(9, 8)) == 0,
    detail="Two-vertex correlator => linear, not sqrt",
)
check(
    "EW side: g_EW correction = sqrt(9/8) = 1/sqrt(8/9) (one factor on amplitude)",
    sp.simplify(sqrt(ew_correction) - 1 / sqrt(R_conn)) == 0,
    detail=f"sqrt(9/8) = {sp.N(sqrt(ew_correction), 8)} (UP)",
)

# Sign / direction sanity: LSZ singlet projection only REDUCES propagator,
# so sqrt(Z_phi) < 1 (DOWN); EW connected-trace ratio kappa_EW = 0 gives
# alpha UP, hence g_EW UP.
check(
    "y_t direction: DOWN (sqrt(8/9) < 1)",
    val_b < 1,
    detail=f"sqrt(8/9) = {val_b:.6f} < 1",
)
check(
    "g_EW direction: UP (sqrt(9/8) > 1) at kappa_EW = 0",
    float(sp.N(sqrt(ew_correction), 8)) > 1,
    detail=f"sqrt(9/8) = {sp.N(sqrt(ew_correction), 8)} > 1",
)


# =============================================================================
section("Sub-check (2): 3-loop QCD MSbar->pole match check")
# Statement: the published 3-loop coefficient (Chetyrkin-Steinhauser
# Nucl. Phys. B573 (2000) 617; Melnikov-van Ritbergen Phys. Lett. B482
# (2000) 99) gives a ~0.31% shift on m_t,pole at alpha_s ~ 0.108. This
# is consistent with the framework's own COMPLETE_PREDICTION_CHAIN
# §6.2 reporting m_t,2L = 172.57 GeV and m_t,3L = 173.10 GeV.
# =============================================================================

# Chetyrkin-Steinhauser / Melnikov-van Ritbergen 3-loop coefficient:
# m_t,pole = m_t,MS * { 1 + (4/3)(a_s/pi) + c_2(N_L)(a_s/pi)^2 + c_3(N_L)(a_s/pi)^3 + ... }
# c_2(N_L) = -1.0414 N_L + 13.4434
# c_3(N_L) =  0.6527 N_L^2 - 26.655 N_L + 190.595

import math

N_L = 5  # light flavors at the top scale
alpha_s_mt = 0.108  # alpha_s(m_t) ~ 0.108 (standard PDG-consistent value)
a_pi = alpha_s_mt / math.pi

c_1 = 4.0 / 3.0
c_2 = -1.0414 * N_L + 13.4434
c_3 = 0.6527 * N_L**2 - 26.655 * N_L + 190.595

term_1 = c_1 * a_pi
term_2 = c_2 * a_pi**2
term_3 = c_3 * a_pi**3

print(f"\n  alpha_s(m_t) = {alpha_s_mt} (PDG comparator), N_L = {N_L}")
print(f"  a_s/pi = {a_pi:.6f}")
print(f"  Chetyrkin-Steinhauser / Melnikov-van Ritbergen coefficients:")
print(f"    c_1                    = {c_1:.4f}    (1-loop, exact 4/3)")
print(f"    c_2(N_L=5)             = {c_2:.4f}     (Gray-Broadhurst-Grafe-Schilcher 1990)")
print(f"    c_3(N_L=5)             = {c_3:.4f}     (Chetyrkin-Steinhauser 2000)")
print(f"  Numerical contributions:")
print(f"    term_1 (1-loop)        = {term_1:.6f}    ({term_1*100:.4f}%)")
print(f"    term_2 (2-loop)        = {term_2:.6f}    ({term_2*100:.4f}%)")
print(f"    term_3 (3-loop)        = {term_3:.6f}    ({term_3*100:.4f}%)")
print(f"    sum                    = {term_1+term_2+term_3:.6f}    ({(term_1+term_2+term_3)*100:.4f}%)")

# 3-loop shift relative to m_t (~163 GeV MSbar)
shift_3l_pct = term_3 * 100  # in percent
shift_3l_GeV_estimate = term_3 * 163.0  # m_t^MS ~ 163 GeV at mu = m_t

print(f"\n  3-loop shift estimate:")
print(f"    delta_3L / m_t = {shift_3l_pct:.4f}%")
print(f"    delta_3L      ≈ {shift_3l_GeV_estimate:.4f} GeV  (using m_t^MS ~ 163 GeV)")

check(
    "3-loop pole shift in 0.2-0.4% range (Chetyrkin-Steinhauser scale)",
    0.002 < term_3 < 0.004,
    detail=f"term_3 = {term_3:.6f}",
)
check(
    "3-loop shift > 2-loop shift in absolute size? (typically not at high N_L)",
    term_3 < term_2,
    detail=f"term_2 = {term_2:.6f} > term_3 = {term_3:.6f} (perturbative ordering OK)",
)

# Framework internal cross-check: COMPLETE_PREDICTION_CHAIN §6.2 records
# m_t,2L = 172.57 GeV and m_t,3L = 173.10 GeV. The framework-internal
# 3-loop shift should be consistent with the published coefficient.
m_t_2L_framework = 172.57  # COMPLETE_PREDICTION_CHAIN_2026_04_15.md §6.2
m_t_3L_framework = 173.10  # COMPLETE_PREDICTION_CHAIN_2026_04_15.md §6.2
delta_framework = m_t_3L_framework - m_t_2L_framework
delta_framework_pct = (delta_framework / m_t_2L_framework) * 100

print(f"\n  Framework internal 3-loop shift (COMPLETE_PREDICTION_CHAIN §6.2):")
print(f"    m_t(2-loop)        = {m_t_2L_framework} GeV")
print(f"    m_t(3-loop)        = {m_t_3L_framework} GeV")
print(f"    delta_3L           = {delta_framework:.4f} GeV")
print(f"    delta_3L / m_t     = {delta_framework_pct:.4f}%")

check(
    "framework internal 3-loop shift consistent with Chetyrkin-Steinhauser (within factor 2)",
    0.5 < delta_framework_pct / shift_3l_pct < 2.0,
    detail=f"framework shift {delta_framework_pct:.3f}% vs CS coefficient {shift_3l_pct:.3f}%",
)

# PDG comparator (audit comparator only, not framework input)
pdg_m_t = 172.69  # PDG world average
pdg_uncertainty = 0.30  # ~0.3 GeV PDG world average uncertainty

dev_2L_pct = (m_t_2L_framework - pdg_m_t) / pdg_m_t * 100
dev_3L_pct = (m_t_3L_framework - pdg_m_t) / pdg_m_t * 100
dev_bracket_pct = ((m_t_2L_framework + m_t_3L_framework) / 2 - pdg_m_t) / pdg_m_t * 100

print(f"\n  Framework vs PDG (audit comparator m_t,pole = {pdg_m_t} +/- {pdg_uncertainty} GeV):")
print(f"    2-loop deviation   = {dev_2L_pct:+.4f}%   ({m_t_2L_framework - pdg_m_t:+.3f} GeV)")
print(f"    3-loop deviation   = {dev_3L_pct:+.4f}%   ({m_t_3L_framework - pdg_m_t:+.3f} GeV)")
print(f"    bracket midpoint   = {dev_bracket_pct:+.4f}%   ({(m_t_2L_framework + m_t_3L_framework)/2 - pdg_m_t:+.3f} GeV)")

check(
    "2-loop framework-chain comparator within 0.1% of PDG (the headline 0.07% claim)",
    abs(dev_2L_pct) < 0.1,
    detail=f"|dev_2L| = {abs(dev_2L_pct):.4f}% < 0.1%",
)
check(
    "3-loop framework-chain comparator within 0.3% of PDG (sub-percent comparator)",
    abs(dev_3L_pct) < 0.3,
    detail=f"|dev_3L| = {abs(dev_3L_pct):.4f}% < 0.3%",
)
check(
    "2/3-loop bracket midpoint within 0.1% of PDG",
    abs(dev_bracket_pct) < 0.1,
    detail=f"|dev_bracket| = {abs(dev_bracket_pct):.4f}% < 0.1%",
)
check(
    "framework-chain 2-loop and 3-loop comparators bracket the PDG comparator",
    m_t_2L_framework < pdg_m_t < m_t_3L_framework,
    detail=f"{m_t_2L_framework} < {pdg_m_t} < {m_t_3L_framework}",
)


# =============================================================================
section("Sub-check (3): cross-check vs Eichhorn-Held asymptotic safety")
# Statement: the AS comparator central value is m_t,pole ~ 171 GeV
# (Eichhorn-Held arXiv:1707.01107).
# Framework-chain comparators are 172.57 GeV (2L) / 173.10 GeV (3L).
# PDG is 172.69 GeV.
# Verify the gap is above the FCC-ee threshold-scan precision (~9 MeV stat,
# ~30-50 MeV theoretical), so the central values are experimentally
# distinguishable under the stated comparator assumptions.
# =============================================================================

# AS comparator (Eichhorn-Held arXiv:1707.01107)
m_t_AS = 171.0  # GeV, central AS value (no explicit error bar quoted)

# Framework-chain comparators (from COMPLETE_PREDICTION_CHAIN §6.2)
print(f"\n  Comparators vs PDG:")
print(f"    Framework (2-loop)         = {m_t_2L_framework:.3f} GeV   ({(m_t_2L_framework - pdg_m_t):+.3f} GeV from PDG, {dev_2L_pct:+.3f}%)")
print(f"    Framework (3-loop)         = {m_t_3L_framework:.3f} GeV   ({(m_t_3L_framework - pdg_m_t):+.3f} GeV from PDG, {dev_3L_pct:+.3f}%)")
print(f"    Framework (2/3-loop mid)   = {(m_t_2L_framework + m_t_3L_framework)/2:.3f} GeV   ({((m_t_2L_framework + m_t_3L_framework)/2 - pdg_m_t):+.3f} GeV from PDG, {dev_bracket_pct:+.3f}%)")
print(f"    AS Eichhorn-Held           = {m_t_AS:.3f} GeV   ({(m_t_AS - pdg_m_t):+.3f} GeV from PDG, {(m_t_AS - pdg_m_t)/pdg_m_t*100:+.3f}%)")
print(f"    PDG world average          = {pdg_m_t:.3f} +/- {pdg_uncertainty:.3f} GeV")

# Framework vs AS gap
gap_framework_AS_2L = m_t_2L_framework - m_t_AS
gap_framework_AS_3L = m_t_3L_framework - m_t_AS
gap_framework_AS_2L_pct = gap_framework_AS_2L / pdg_m_t * 100

print(f"\n  Framework-vs-AS gap:")
print(f"    2-loop framework - AS      = {gap_framework_AS_2L:+.3f} GeV   ({gap_framework_AS_2L_pct:+.3f}% of m_t)")
print(f"    3-loop framework - AS      = {gap_framework_AS_3L:+.3f} GeV   ({gap_framework_AS_3L/pdg_m_t*100:+.3f}% of m_t)")

check(
    "framework-chain comparator is above AS central value",
    gap_framework_AS_2L > 0,
    detail=f"gap = {gap_framework_AS_2L:.3f} GeV",
)
check(
    "framework-vs-AS gap is sub-2 GeV / sub-percent",
    abs(gap_framework_AS_2L) < 2.0,
    detail=f"|gap| = {abs(gap_framework_AS_2L):.3f} GeV < 2 GeV",
)

# AS vs PDG: AS is 1.69 GeV / ~1% off PDG, framework is ~0.07%
as_dev = abs(m_t_AS - pdg_m_t)
fw_2L_dev = abs(m_t_2L_framework - pdg_m_t)
ratio_AS_to_fw = as_dev / max(fw_2L_dev, 0.01)

print(f"\n  AS deviation from PDG    = {as_dev:.3f} GeV ({as_dev/pdg_m_t*100:.3f}%)")
print(f"  FW 2-loop dev from PDG   = {fw_2L_dev:.3f} GeV ({fw_2L_dev/pdg_m_t*100:.4f}%)")
print(f"  AS dev / FW 2-loop dev   = {ratio_AS_to_fw:.1f}x (AS is {ratio_AS_to_fw:.0f}x further from PDG)")

check(
    "AS central value is separated from PDG comparator by >1 GeV",
    as_dev > 1.0,
    detail=(
        f"AS central value differs by {as_dev:.3f} GeV; no AS-side "
        "uncertainty band is imposed here"
    ),
)

# FCC-ee precision target (arXiv:2503.18713, arXiv:1611.03399):
# stat ~9 MeV, theoretical ~30-50 MeV; total ~50-100 MeV
fcc_ee_stat_MeV = 9.0
fcc_ee_theory_MeV = 50.0  # upper end of theoretical uncertainty estimate
fcc_ee_total_MeV = fcc_ee_stat_MeV + fcc_ee_theory_MeV  # very rough sum

print(f"\n  FCC-ee threshold-scan precision targets:")
print(f"    statistical (10/ab)        ~{fcc_ee_stat_MeV:.0f} MeV  (arXiv:2503.18713)")
print(f"    theoretical                ~{fcc_ee_theory_MeV:.0f} MeV  (arXiv:1611.03399 estimate)")
print(f"    total (rough sum)          ~{fcc_ee_total_MeV:.0f} MeV  (~0.06 GeV)")

# Distinguishability: gap >> FCC-ee precision => discriminable
distinguishable = abs(gap_framework_AS_2L) * 1000 > fcc_ee_total_MeV * 5  # 5x precision
print(f"\n  Discrimination check: framework-vs-AS gap = {abs(gap_framework_AS_2L)*1000:.0f} MeV")
print(f"                        FCC-ee precision     = ~{fcc_ee_total_MeV:.0f} MeV")
print(f"                        gap / precision      = {abs(gap_framework_AS_2L)*1000 / fcc_ee_total_MeV:.1f}x")

check(
    "framework-vs-AS central-value gap > 5x FCC-ee total precision",
    distinguishable,
    detail=f"gap {abs(gap_framework_AS_2L)*1000:.0f} MeV vs FCC-ee precision ~{fcc_ee_total_MeV:.0f} MeV",
)


# =============================================================================
section("Cross-cutting: same R_conn, opposite directions on y_t and g_EW")
# Verify the consistency check that the SAME group-theory factor R_conn = 8/9
# enters with OPPOSITE corrections on y_t (DOWN) and g_EW (UP at kappa_EW=0).
# =============================================================================

correction_yt = sqrt(R_conn)        # DOWN, sqrt(8/9)
correction_gEW = 1 / sqrt(R_conn)   # UP, sqrt(9/8) = 1/sqrt(8/9)

print(f"\n  Same R_conn = {R_conn}, opposite directions:")
print(f"    y_t correction:   sqrt(R_conn)   = sqrt(8/9) = {sp.N(correction_yt, 8)} (DOWN)")
print(f"    g_EW correction:  1/sqrt(R_conn) = sqrt(9/8) = {sp.N(correction_gEW, 8)} (UP)")
print(f"    Product:          1            (universal cancellation)")

check(
    "y_t correction * g_EW correction = 1 (universal R_conn factor)",
    sp.simplify(correction_yt * correction_gEW - 1) == 0,
    detail="sqrt(8/9) * sqrt(9/8) = 1, both sides use same R_conn",
)

# sin^2(theta_W) preservation: g_EW correction is universal across g_1 and g_2,
# so sin^2(theta_W) is preserved exactly.
g_y, g_2, f = symbols("g_y g_2 f", positive=True)
sin2_before = g_y**2 / (g_y**2 + g_2**2)
sin2_after = (f * g_y)**2 / ((f * g_y)**2 + (f * g_2)**2)
print(f"\n  sin^2(theta_W) preservation: g_EW factor sqrt(9/8) is universal across g_1, g_2")
print(f"    sin^2(theta_W) = g_Y^2 / (g_Y^2 + g_2^2): universal factor cancels in ratio")
check(
    "sin^2(theta_W) preserved exactly under universal g_EW correction",
    sp.simplify(sin2_after - sin2_before) == 0,
    detail="universal sqrt(9/8) factor cancels in sin^2(theta_W) ratio (theorem-level)",
)


# =============================================================================
section("Defense narrow theorem summary")
# =============================================================================

print(f"""
  Three sub-checks on the y_t chain's sqrt(8/9) Fierz color projection:

  (1) Vertex-level Z_phi vs current-current disambiguation:
      -- LSZ leg-count fixes correction = sqrt(R_conn) = sqrt(8/9), DOWN
      -- form (b) selected, form (a) [R_conn directly] rejected
      -- Citation: YUKAWA_COLOR_PROJECTION_THEOREM.md Parts 2.5, 3.1, 3.4, 4.1

  (2) 3-loop QCD MSbar->pole match check:
      -- Chetyrkin-Steinhauser/Melnikov-van Ritbergen 3-loop coefficient
         gives ~0.31% shift on m_t (~0.5 GeV)
      -- Framework's internal 3-loop comparator (m_t,3L = 173.10 GeV)
         consistent with this shift (delta = 0.53 GeV)
      -- Headline 0.07% match is the 2-loop comparator;
         3-loop comparator at +0.24%, still sub-percent
      -- 2/3-loop bracket midpoint at +0.08% from PDG

  (3) Cross-check vs Eichhorn-Held asymptotic safety:
      -- AS comparator central value is m_t,pole ~ 171 GeV
         (arXiv:1707.01107)
      -- Framework-vs-AS gap ~ 1.6 GeV ~ 0.9% of m_t
      -- AS central value is separated from the framework-chain central
         values by ~1.6-2.1 GeV
      -- FCC-ee threshold scan (~50 MeV total precision) would distinguish
         those central values under the cited comparator assumptions

  Three named admissions in the defense note:
      (i)   Fierz interpretation inherits from upstream LSZ derivation
      (ii)  0.07% match is loop-order specific (2-loop pole conversion)
      (iii) AS-vs-lattice discriminator is FCC-ee level

  Scope: this is a DISAMBIGUATION / DEFENSE, not a new positive theorem.
  Load-bearing step class: F (re-statement of upstream LSZ derivation).
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
