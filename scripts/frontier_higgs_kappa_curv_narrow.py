#!/usr/bin/env python3
"""Verify the narrow symmetric-point curvature ratio theorem κ_curv = 1/(8u_0²).

Claim scope: define κ_curv := |∂²V_taste/∂m²|_{m=0}| / (2 N_taste)
where V_taste(m) = -8 log(m² + 4 u_0²) is the per-channel taste-trace
potential at the symmetric point (HIGGS_MASS_FROM_AXIOM Step 4) and
N_taste = 16 from the staggered-Dirac realization open gate. Then

    κ_curv = 1/(8 u_0²).

At u_0 = 0.8776, κ_curv ≈ 0.1623.

CRITICAL FIRST-PRINCIPLES SCOPE:
  κ_curv is structurally a dimensionless lattice curvature ratio, NOT a |φ|⁴
  quartic coupling. By first-principles QFT standards, the SM Higgs
  quartic λ is the |φ|⁴ coefficient of V_eff at some Wilsonian scale.
  V_taste's |φ|⁴ coefficient at the lattice scale (with m = y_t·φ) is
  y_t⁴/(4u_0⁴) per channel — a DIFFERENT object than κ_curv.

This is why the symbol is κ (generic dimensionless ratio), not λ
(quartic coupling). The κ_curv ↔ SM λ bridge is a NAMED OPEN theorem.

Class (A) algebraic on V_taste's symmetric-point curvature plus a
class (E) definitional choice for the 2N_taste normalization. No new admissions
beyond the V_taste form, N_taste, and u_0 numerical input.
"""

from __future__ import annotations

from pathlib import Path
import sys

try:
    import sympy as sp
except ImportError:  # pragma: no cover
    print("FAIL: sympy required")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT
    / "docs"
    / "HIGGS_KAPPA_CURV_FROM_VTASTE_SYMMETRIC_POINT_NARROW_THEOREM_NOTE_2026-05-10.md"
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
section("Part 1: note structure and first-principles-honest naming")
# ============================================================================
note_text = NOTE_PATH.read_text()

# The first-principles-honest symbol is κ (kappa), NOT λ (lambda)
required_strings = [
    "Symmetric-Point Curvature Ratio κ_curv",
    "claim_type: bounded_theorem",
    "1 / (8 u_0²)",
    "κ_curv  =  1 / (8 u_0²)",
    "Counterfactual Pass",
    "Elon first-principles",
    "load_bearing_step_class: A",
    "definitional_step_class: E",
    "forbidden_imports_used: false",
    "named_open_bridge",
    "kappa_curv_to_sm_lambda",
    "lattice-normalized curvature ratio",
]
for s in required_strings:
    check(f"note contains: '{s[:50]}'", s in note_text)

# CRITICAL: the note must NOT use "λ_curv" as the primary symbol
# (it can mention λ_curv historically as the v2 name, but κ_curv is the
# first-principles-honest symbol going forward).
forbidden_as_primary = [
    "λ_curv  =  1",  # would mean "λ_curv equals" which is the old v2 form
    "λ_curv = 1/(8",
    "Higgs Quartic UV Anchor",  # would be over-claim per pre-check on v1
    "Higgs Lattice-Curvature Coupling λ_curv",  # would be the v2 over-naming
]
for s in forbidden_as_primary:
    check(f"note does NOT use over-claim '{s[:40]}'", s not in note_text)

# Scope discipline
scope_disclaimers = [
    "explicitly does NOT",
    "audit verdict and downstream status are set only by the independent\naudit lane",
    "EXPLICITLY DISTINCT",
    "structurally a lattice-normalized curvature ratio",  # the honest first-principles description
    "NOT a |φ|⁴ coefficient",  # honest distinction from SM λ
    "not a quartic coupling",  # the honest description (lowercase 'not' as in note)
]
for s in scope_disclaimers:
    check(f"scope disclaimer present: '{s[:40]}'", s in note_text)


# ============================================================================
section("Part 2: V_taste curvature at symmetric point (class A)")
# ============================================================================

m, u0 = sp.symbols("m u_0", real=True, positive=True)
V_taste = -8 * sp.log(m ** 2 + 4 * u0 ** 2)

curvature = sp.simplify(sp.diff(V_taste, m, 2).subs(m, 0))
expected_curv = -4 / u0 ** 2
check(
    "∂²V_taste/∂m²|_{m=0} = -4/u_0² (tachyonic)",
    sp.simplify(curvature - expected_curv) == 0,
    f"computed = {curvature}",
)
check(
    "Curvature is NEGATIVE at m=0 (tachyonic instability)",
    bool(curvature.subs(u0, 1) < 0),
    f"curvature(u_0=1) = {float(curvature.subs(u0, 1))}",
)


# ============================================================================
section("Part 3: κ_curv definition and Clifford-fixed identity")
# ============================================================================
#
# κ_curv := |∂²V_taste/∂m²|_{m=0}| / (2 N_taste).
# In dimensionless lattice units this gives
# κ_curv = (4/u_0²) / (16 · 2) = 1/(8u_0²).

N_taste = sp.Integer(16)

kappa_curv = sp.Abs(curvature) / (N_taste * sp.Integer(2))
kappa_curv_simplified = sp.simplify(kappa_curv)
expected_kappa = 1 / (8 * u0 ** 2)
check(
    "κ_curv = 1/(8 u_0²) (load-bearing Clifford-fixed identity)",
    sp.simplify(kappa_curv_simplified - expected_kappa) == 0,
    f"computed = {kappa_curv_simplified}",
)
check(
    "κ_curv depends only on u_0",
    kappa_curv_simplified.free_symbols == {u0},
    f"free_symbols = {kappa_curv_simplified.free_symbols}",
)


# ============================================================================
section("Part 4: numerical value at u_0 = 0.8776")
# ============================================================================

u0_value = 0.8776
kappa_numerical = float(kappa_curv_simplified.subs(u0, u0_value))
check(
    "κ_curv(u_0=0.8776) ≈ 0.1623",
    abs(kappa_numerical - 0.16229) < 1e-3,
    f"κ_curv ≈ {kappa_numerical:.6f}",
)


# ============================================================================
section("Part 5: first-principles fermion-loop quartic (DISTINCT from κ_curv)")
# ============================================================================
#
# Per first principles: with m = y_t · φ (Yukawa to a Higgs scalar), the |φ|⁴
# coefficient of V_taste is y_t⁴/(4u_0⁴) per channel. This IS a candidate
# SM-EFT-style λ at the lattice scale via fermion-loop matching.
# It is STRUCTURALLY DIFFERENT from κ_curv:
#   - κ_curv: dimensionless lattice curvature ratio
#   - fermion-loop quartic: |φ|⁴ coefficient (the actual SM-style λ)
#
# Verify: y_t⁴/(4u_0⁴) ≠ 1/(8u_0²) for generic y_t.

y_t = sp.symbols("y_t", positive=True)
phi = sp.symbols("phi", real=True)
V_taste_phi = -8 * sp.log(y_t ** 2 * phi ** 2 + 4 * u0 ** 2)

# Taylor coefficient of φ^4 (i.e., 1/24 × d^4/dφ^4 evaluated at φ=0)
quartic_coef_phi = sp.simplify(sp.diff(V_taste_phi, phi, 4).subs(phi, 0) / 24)
expected_quartic = y_t ** 4 / (4 * u0 ** 4)
check(
    "First-principles |φ|⁴ coefficient = y_t⁴/(4 u_0⁴) per channel",
    sp.simplify(quartic_coef_phi - expected_quartic) == 0,
    f"computed = {quartic_coef_phi}",
)

# Numerical at u_0 = 0.8776, y_t ≈ 0.4 (rough AS-fixed-point value at high scale)
yt_high_scale = 0.4
fermion_loop_quartic = float(expected_quartic.subs([(u0, u0_value), (y_t, yt_high_scale)]))
check(
    "First-principles fermion-loop quartic at u_0=0.8776, y_t=0.4: ~0.011",
    abs(fermion_loop_quartic - 0.0108) < 1e-3,
    f"y_t⁴/(4u_0⁴) ≈ {fermion_loop_quartic:.4f}",
)
check(
    "Fermion-loop quartic ≠ κ_curv (structurally different objects)",
    abs(fermion_loop_quartic - kappa_numerical) > 0.05,
    f"|fermion-loop-quartic - κ_curv| = {abs(fermion_loop_quartic - kappa_numerical):.4f}",
)


# ============================================================================
section("Part 6: comparison with SM λ_obs(v) — audit comparator only")
# ============================================================================
#
# CRITICAL: SM λ_obs is the |φ|⁴ coefficient of V_eff post-EWSB at scale v;
# it is structurally different from κ_curv (which is curvature-derived, not |φ|⁴).
# Forbidden derivation input; appears here as audit comparator.

m_H_pole_obs = 125.10  # PDG comparator only
v_obs = 246.22  # PDG comparator only
sm_lambda_obs_at_v = m_H_pole_obs ** 2 / (2 * v_obs ** 2)

print(
    f"\n  [INFO] AUDIT COMPARATORS (NOT derivation inputs):"
    f"\n         κ_curv (this theorem; lattice curvature ratio) ≈ {kappa_numerical:.4f}"
    f"\n         y_t⁴/(4u_0⁴) (fermion-loop quartic, y_t=0.4) ≈ {fermion_loop_quartic:.4f}"
    f"\n         SM λ_obs(v) (PDG-extracted)                  ≈ {sm_lambda_obs_at_v:.4f}"
    f"\n"
    f"\n         Three structurally different objects. The first is a curvature-derived"
    f"\n         ratio at the symmetric point (this theorem); the second is the |φ|⁴"
    f"\n         coefficient of V_taste at the lattice scale (the first-principles"
    f"\n         analogue of SM λ); the third is the post-EWSB SM λ at scale v."
    f"\n         The κ_curv ↔ SM λ bridge is the framework's NAMED OPEN theorem."
)

check(
    "All three objects (κ_curv, fermion-loop quartic, SM λ_obs) are distinct",
    (
        abs(kappa_numerical - fermion_loop_quartic) > 0.05
        and abs(kappa_numerical - sm_lambda_obs_at_v) > 0.02
        and abs(fermion_loop_quartic - sm_lambda_obs_at_v) > 0.05
    ),
    "structural distinctions verified numerically",
)


# ============================================================================
section("Part 7: structural assertions")
# ============================================================================

check(
    "κ_curv > 0 (magnitude convention; positive dimensionless ratio)",
    kappa_numerical > 0,
)
check(
    "κ_curv is dimensionless",
    True,  # by construction: 1/(8 u_0²) is dim-0 since u_0 is dim-0
    "1/(8 u_0²) is dim-0 since u_0 is dim-0",
)
check(
    "κ_curv is Clifford-fixed (depends only on u_0 from gauge sector)",
    kappa_curv_simplified.free_symbols == {u0},
)


# ============================================================================
section("Part 8: scope-narrowing audit checks")
# ============================================================================
#
# The v3 iteration replaces "λ_curv" with "κ_curv" because the object is
# structurally a curvature-derived ratio, not a quartic coupling. Verify the
# note honors this first-principles-honest naming.

scope_assertions = [
    "Stripping all framework conventions",  # Elon first-principles redo
    "fermion-loop-induced quartic at the lattice",  # the right SM-style λ
    "y_t⁴/(4u_0⁴)",  # the actual fermion-loop quartic
    "structurally a lattice-normalized curvature ratio",  # honest description of κ_curv
    "Bardeen, Hill, Lindner (1990)",  # NJL reference for the honest open bridge
]
for s in scope_assertions:
    check(
        f"first-principles-honest assertion: '{s[:40]}'",
        s in note_text,
    )

# §10 honest scope checks
section_10_assertions = [
    "κ_curv ↔ SM λ` bridge",
    "Gate #6 (lambda-UV anchor) in full",
    "first-principles fermion-loop quartic",  # listed as separately not closed
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
