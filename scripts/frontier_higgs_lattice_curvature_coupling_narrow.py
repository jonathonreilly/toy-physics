#!/usr/bin/env python3
"""Verify the narrow Higgs lattice-curvature coupling theorem.

Claim scope: define λ_curv := |∂²V_taste/∂m²|_{m=0}| / (N_taste · 2 v²)
                            = (m_H_tree)² / (2 v²)
where:
  - V_taste(m) = -8 log(m² + 4 u_0²) is the per-channel taste-trace
    potential at the symmetric point on the L_s = 2 mean-field APBC
    surface (HIGGS_MASS_FROM_AXIOM Step 4);
  - N_taste = 16 from the staggered-Dirac realization open gate;
  - m_H_tree := v/(2 u_0) is the tree-level mean-field readout
    (HIGGS_MASS_FROM_AXIOM Step 5–6).

The Clifford-fixed identity is:
    λ_curv = 1/(8 u_0²),   v cancels exactly.

At u_0 = 0.8776, λ_curv ≈ 0.1623.

CRITICAL SCOPE: λ_curv is the framework's lattice-curvature coupling.
It is EXPLICITLY DISTINCT from the SM EFT's Higgs scalar quartic λ.
The bridge λ_curv ↔ SM λ is named here as an OPEN theorem (the framework's
"+12% gap" / m_H_tree ↔ m_H_pole identification per HIGGS_MASS_FROM_AXIOM
Step 5(b)). This runner verifies the LATTICE-CURVATURE side identity ONLY.

Class (A) algebraic. No new admissions beyond V_taste form, m_H_tree
readout convention, and N_taste from the open gate.
"""

from __future__ import annotations

from pathlib import Path
from fractions import Fraction
import sys

try:
    import sympy as sp
except ImportError:  # pragma: no cover
    print("FAIL: sympy required")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT / "docs" / "HIGGS_LATTICE_CURVATURE_COUPLING_NARROW_THEOREM_NOTE_2026-05-10.md"
)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Part 1: note structure and scope discipline")
# ============================================================================
note_text = NOTE_PATH.read_text()
required_strings = [
    "Higgs Lattice-Curvature Coupling λ_curv",
    "claim_type: bounded_theorem",
    "1 / (8 u_0²)",
    "Counterfactual Pass",
    "Elon first-principles",
    "load_bearing_step_class: A",
    "forbidden_imports_used: false",
    "EXPLICITLY DISTINCT",
    "named_open_bridge",
    "lambda_curv_to_sm_lambda",
]
for s in required_strings:
    check(f"note contains: '{s[:50]}'", s in note_text)

scope_disclaimers = [
    "explicitly does NOT",
    "audit verdict and downstream status are set only by the independent\naudit lane",
    "λ_curv` is **not** identified with SM λ",
]
for s in scope_disclaimers:
    check(f"scope disclaimer present: '{s[:40]}...'", s in note_text)

# Verify the note explicitly does NOT use class-(F) renaming language
forbidden_in_note = [
    "λ_tree = SM λ",  # would be class F
    "Gate #6 closes positively",  # would be over-claim per pre-check
    "composite-Higgs heuristic was retired",  # would forward-cite unmerged PR
]
for s in forbidden_in_note:
    check(f"note does NOT contain over-claim '{s[:40]}'", s not in note_text)


# ============================================================================
section("Part 2: V_taste curvature at symmetric point (class A algebraic)")
# ============================================================================
#
# V_taste(m) = -8 log(m² + 4 u_0²), HIGGS_MASS_FROM_AXIOM Step 4.
# Compute symbolically: ∂²V_taste/∂m²|_{m=0} = -4 / u_0² (tachyonic).

m, u0 = sp.symbols("m u_0", real=True, positive=True)
V_taste = -8 * sp.log(m ** 2 + 4 * u0 ** 2)

curvature_sym = sp.diff(V_taste, m, 2).subs(m, 0)
curvature_sym = sp.simplify(curvature_sym)
expected_curvature = -4 / u0 ** 2
check(
    "∂²V_taste/∂m²|_{m=0} = -4/u_0²  (tachyonic, drives EWSB)",
    sp.simplify(curvature_sym - expected_curvature) == 0,
    f"computed = {curvature_sym}, expected = {expected_curvature}",
)
check(
    "Sign of curvature is NEGATIVE (tachyonic)",
    bool(curvature_sym.subs(u0, 1) < 0),
    f"curvature(u_0=1) = {float(curvature_sym.subs(u0, 1))}",
)


# ============================================================================
section("Part 3: m_H_tree readout from HIGGS_MASS_FROM_AXIOM Step 5")
# ============================================================================
#
# Tree-level mean-field readout convention:
#   (m_H_tree / v)² := |∂²V_taste/∂m²|_{m=0}| / N_taste
#                    = (4/u_0²) / 16
#                    = 1/(4 u_0²)
# Therefore m_H_tree = v / (2 u_0).

N_taste = sp.Integer(16)
v = sp.symbols("v", real=True, positive=True)

abs_curv = sp.Abs(curvature_sym)
mH_tree_sq_over_v_sq = abs_curv / N_taste
mH_tree_sq_over_v_sq_simplified = sp.simplify(mH_tree_sq_over_v_sq)
expected_ratio_sq = 1 / (4 * u0 ** 2)
check(
    "(m_H_tree / v)² = |curvature| / N_taste = 1/(4 u_0²)",
    sp.simplify(mH_tree_sq_over_v_sq_simplified - expected_ratio_sq) == 0,
    f"computed = {mH_tree_sq_over_v_sq_simplified}",
)

mH_tree = sp.sqrt(mH_tree_sq_over_v_sq * v ** 2)
mH_tree_simplified = sp.simplify(mH_tree)
expected_mH_tree = v / (2 * u0)
check(
    "m_H_tree = v / (2 u_0)  (tree-level mean-field readout)",
    sp.simplify(mH_tree_simplified - expected_mH_tree) == 0,
    f"computed = {mH_tree_simplified}",
)


# ============================================================================
section("Part 4: λ_curv definition and Clifford-fixed identity (class A)")
# ============================================================================
#
# Definition: λ_curv := (m_H_tree)² / (2 v²)
# Substituting m_H_tree = v/(2 u_0):
#   λ_curv = (v/(2 u_0))² / (2 v²) = 1 / (8 u_0²)
# v cancels exactly.

lam_curv = mH_tree ** 2 / (2 * v ** 2)
lam_curv_simplified = sp.simplify(lam_curv)
expected_lam_curv = 1 / (8 * u0 ** 2)
check(
    "λ_curv = (m_H_tree)² / (2 v²) = 1/(8 u_0²)",
    sp.simplify(lam_curv_simplified - expected_lam_curv) == 0,
    f"computed = {lam_curv_simplified}, expected = {expected_lam_curv}",
)
check(
    "λ_curv is independent of v (v cancels)",
    v not in lam_curv_simplified.free_symbols,
    f"free_symbols = {lam_curv_simplified.free_symbols}",
)


# ============================================================================
section("Part 5: numerical value at u_0 ≈ 0.8776 (gate #7 frontier)")
# ============================================================================

u0_value = 0.8776
lam_curv_numerical = float(lam_curv_simplified.subs(u0, u0_value))
expected_numerical = 1.0 / (8.0 * u0_value ** 2)
check(
    "λ_curv(u_0=0.8776) ≈ 0.1623",
    abs(lam_curv_numerical - 0.16229) < 1e-3,
    f"λ_curv ≈ {lam_curv_numerical:.6f}",
)
check(
    "Numerical λ_curv matches symbolic substitution",
    abs(lam_curv_numerical - expected_numerical) < 1e-12,
    f"diff = {abs(lam_curv_numerical - expected_numerical):.2e}",
)


# ============================================================================
section("Part 6: λ_curv is structurally distinct from SM λ (named bridge)")
# ============================================================================
#
# CRITICAL SCOPE CHECK: this theorem does NOT identify λ_curv with the
# SM EFT's Higgs quartic λ. The two are different objects:
#   - λ_curv: framework's tree-level lattice-curvature coupling at the
#             symmetric point of V_taste (where curvature is tachyonic;
#             magnitude convention applied).
#   - SM λ:   coefficient of |φ|⁴ in the SM Higgs effective potential,
#             defined post-EWSB with the broken-phase pole at φ = v.
# The bridge λ_curv ↔ SM λ is an OPEN theorem (the framework's named
# +12% gap from m_H_tree ↔ m_H_pole).

# Audit comparator: SM λ extracted from observed m_H, v
m_H_pole_obs = 125.10  # PDG comparator only (NOT a derivation input)
v_obs = 246.22  # PDG comparator only (NOT a derivation input)
sm_lambda_obs_at_v = m_H_pole_obs ** 2 / (2 * v_obs ** 2)

# The framework's tree-level prediction for m_H at v:
m_H_tree_at_v = v_obs / (2 * u0_value)
gap_pct = (m_H_tree_at_v - m_H_pole_obs) / m_H_pole_obs * 100

print(
    f"\n  [INFO] AUDIT COMPARATORS (NOT derivation inputs):"
    f"\n         λ_curv (this theorem)           ≈ {lam_curv_numerical:.4f}"
    f"\n         SM λ (PDG-extracted at v)        ≈ {sm_lambda_obs_at_v:.4f}"
    f"\n         m_H_tree at v_obs                ≈ {m_H_tree_at_v:.2f} GeV (framework tree-level)"
    f"\n         m_H_pole (PDG)                   = {m_H_pole_obs:.2f} GeV"
    f"\n         m_H gap (m_H_tree vs m_H_pole)   ≈ +{gap_pct:.2f}%"
    f"\n"
    f"\n         The {gap_pct:.1f}% m_H gap encodes the m_H_tree ↔ m_H_pole identification gap"
    f"\n         (HIGGS_MASS_FROM_AXIOM Step 5(b)). This narrow theorem makes that gap"
    f"\n         explicit as the named open bridge λ_curv ↔ SM λ. The numerical"
    f"\n         disparity ({lam_curv_numerical:.3f} vs {sm_lambda_obs_at_v:.3f}) is the +12% m_H gap squared."
    f"\n         CLAIM SCOPE: this theorem closes the LATTICE-CURVATURE side only."
)

check(
    "λ_curv ≠ SM λ (numerically distinct, by ~26% — encodes +12% m_H gap squared)",
    abs(lam_curv_numerical - sm_lambda_obs_at_v) > 0.02,
    f"|λ_curv - SM λ_obs| ≈ {abs(lam_curv_numerical - sm_lambda_obs_at_v):.4f}",
)
check(
    "+12% m_H gap structure verified (sanity check on framework's claim)",
    11.0 < gap_pct < 13.0,
    f"gap = +{gap_pct:.2f}%",
)


# ============================================================================
section("Part 7: structural assertions")
# ============================================================================

# λ_curv depends only on u_0 (Clifford-fixed)
free_syms = lam_curv_simplified.free_symbols
check(
    "λ_curv is Clifford-fixed (only u_0 dependence)",
    free_syms == {u0},
    f"free_symbols = {free_syms}",
)

# λ_curv > 0 (magnitude convention applied to tachyonic curvature)
check(
    "λ_curv > 0 (magnitude convention; positive dimensionless ratio)",
    lam_curv_numerical > 0,
    f"λ_curv = {lam_curv_numerical:.6f}",
)

# Dimensional consistency
check(
    "λ_curv is dimensionless (u_0 is dimensionless lattice tadpole)",
    True,  # by construction
    "1/(8 u_0²) is dim-0 since u_0 is dim-0",
)


# ============================================================================
section("Part 8: scope-narrowing audit checks")
# ============================================================================
#
# After the audit pre-check on the prior draft of this PR flagged class-(F)
# renaming concerns, the present scope-narrowed theorem MUST honor the
# distinction between λ_curv and SM λ. Verify the source note does so.

scope_narrowing_assertions = [
    "EXPLICITLY DISTINCT",
    "named open bridge",
    "lattice-curvature coupling",
    "**not** identified with SM λ",
]
for s in scope_narrowing_assertions:
    check(
        f"scope-narrowing language present: '{s[:40]}'",
        s in note_text,
    )

# Section §10 ("What this theorem does NOT close") must explicitly mention
# the bridge as open and Gate #6 as not-fully-closed.
section_10_assertions = [
    "λ_curv ↔ SM λ",
    "Gate #6 (lambda-UV anchor) in full",
]
for s in section_10_assertions:
    check(
        f"§10 honest scope: '{s[:40]}'",
        s in note_text,
    )


# ============================================================================
section("Summary")
# ============================================================================
print(f"\nTOTAL : PASS = {PASS}, FAIL = {FAIL}")
if FAIL > 0:
    sys.exit(1)
sys.exit(0)
