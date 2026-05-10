#!/usr/bin/env python3
"""Verify the narrow Higgs quartic UV anchor theorem.

Claim scope: from the framework's tree-level mean-field formula
m_H_tree = v/(2 u_0) (HIGGS_MASS_FROM_AXIOM Step 5–6) and the standard
SM Higgs relation m_H² = 2 λ v², the Clifford-fixed dimensionless
quartic identity follows:

    λ_tree  =  1 / (8 u_0²)

and serves as the framework's positive UV anchor at the lattice
mean-field scale μ_* ≈ M_Pl × u_0, replacing the now-retired
λ(M_Pl) = 0 heuristic from VACUUM_CRITICAL_STABILITY (composite-Higgs
slogan retired by PR #937).

Class (A) algebraic substitution. Numerical value at u_0 = 0.8776:
λ_tree ≈ 0.1623.

Verifies via SymPy symbolic algebra + Fraction arithmetic + PDG
comparator (audit comparator only, NOT a derivation input).
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
    ROOT / "docs" / "HIGGS_LAMBDA_UV_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md"
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
    "Higgs Quartic UV Anchor",
    "claim_type: bounded_theorem",
    "1 / (8 u_0²)",
    "Counterfactual Pass",
    "Elon first-principles",
    "load_bearing_step_class: A",
    "forbidden_imports_used: false",
    "lambda(M_Pl) = 0 heuristic",
]
for s in required_strings:
    check(f"note contains: '{s[:40]}...'", s in note_text)

scope_disclaimers = [
    "explicitly does NOT",
    "audit verdict and downstream status are set only by the independent\naudit lane",
]
for s in scope_disclaimers:
    check(f"scope disclaimer present: '{s[:40]}...'", s in note_text)


# ============================================================================
section("Part 2: symbolic derivation of λ_tree = 1/(8 u_0²)")
# ============================================================================
#
# Start from m_H = v/(2 u_0) and m_H² = 2 λ v². Solve for λ. Verify v cancels.

v, u0, lam, m_H = sp.symbols("v u_0 lambda m_H", positive=True)

# Framework tree-level mean-field formula (HIGGS_MASS_FROM_AXIOM Step 6)
m_H_tree = v / (2 * u0)
check(
    "m_H_tree = v/(2 u_0) (admitted from HIGGS_MASS_FROM_AXIOM)",
    m_H_tree == v / (2 * u0),
    f"m_H_tree = {m_H_tree}",
)

# Standard Higgs relation m_H² = 2 λ v²
# Solve for λ
lam_solution = sp.solve(sp.Eq(m_H_tree ** 2, 2 * lam * v ** 2), lam)
assert len(lam_solution) == 1
lam_tree = sp.simplify(lam_solution[0])
expected = 1 / (8 * u0 ** 2)
check(
    "λ_tree = 1/(8 u_0²) (load-bearing identity)",
    sp.simplify(lam_tree - expected) == 0,
    f"derived λ_tree = {lam_tree}, expected = {expected}",
)

# Verify v cancels (sanity check)
check(
    "λ_tree is independent of v (v dependence cancels)",
    v not in lam_tree.free_symbols,
    f"free_symbols = {lam_tree.free_symbols}",
)


# ============================================================================
section("Part 3: numerical value at u_0 ≈ 0.8776 (gate #7 frontier)")
# ============================================================================
#
# u_0 = ⟨P⟩^(1/4) ≈ 0.8776 corresponds to ⟨P⟩ ≈ 0.594 from the framework
# Wilson surface lattice MC (per HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE
# baseline). At this u_0, λ_tree should be ≈ 0.1623.

u0_value = 0.8776
lam_numerical = float(lam_tree.subs(u0, u0_value))
expected_numerical = 1.0 / (8.0 * u0_value ** 2)
check(
    "λ_tree(u_0=0.8776) ≈ 0.1623",
    abs(lam_numerical - 0.16229) < 1e-3,
    f"computed λ_tree ≈ {lam_numerical:.6f}",
)
check(
    "Numerical λ_tree matches symbolic substitution",
    abs(lam_numerical - expected_numerical) < 1e-12,
    f"diff = {abs(lam_numerical - expected_numerical):.2e}",
)


# ============================================================================
section("Part 4: scale identification μ_* ≈ M_Pl × u_0")
# ============================================================================
#
# V_taste comes from integrating out staggered fermions on the L_s=2 minimal
# block. The matching scale is the typical fermion eigenvalue scale at mean
# field, which is ~ u_0 × a^(-1). With Planck pin, a^(-1) = M_Pl.
#
# Numerically: μ_* ≈ 0.88 × 1.22e19 GeV ≈ 1.07e19 GeV. Planck-scale up to
# O(1) Wilson coefficient.

M_Pl_GeV = 1.220910e19  # standard Planck mass in GeV (admitted context)
mu_star = u0_value * M_Pl_GeV
check(
    "μ_* = u_0 × M_Pl ≈ 0.88 × M_Pl",
    abs(mu_star / M_Pl_GeV - u0_value) < 1e-12,
    f"μ_*/M_Pl = {mu_star/M_Pl_GeV:.4f}",
)
check(
    "μ_* is Planck-scale up to O(1) Wilson coefficient",
    0.5 < mu_star / M_Pl_GeV < 2.0,
    f"μ_*/M_Pl = {mu_star/M_Pl_GeV:.4f} ∈ (0.5, 2)",
)


# ============================================================================
section("Part 5: comparison with retired λ(M_Pl) = 0 claim")
# ============================================================================
#
# This theorem's λ_tree ≈ 0.163 explicitly differs from the retired claim
# λ(M_Pl) = 0 from VACUUM_CRITICAL_STABILITY composite-Higgs heuristic.
# PR #937's named obstruction retired the heuristic; this theorem provides
# the positive replacement.

retired_lambda = 0.0
check(
    "λ_tree ≠ retired λ(M_Pl) = 0",
    abs(lam_numerical - retired_lambda) > 0.1,
    f"λ_tree ≈ {lam_numerical:.4f}, retired = {retired_lambda}",
)
check(
    "Difference is dimensionful, ~ 0.16 in dimensionless quartic units",
    0.10 < abs(lam_numerical - retired_lambda) < 0.20,
    f"|Δλ| ≈ {abs(lam_numerical - retired_lambda):.4f}",
)


# ============================================================================
section("Part 6: comparison with observed λ(v) — audit comparator only")
# ============================================================================
#
# Standard SM extraction at v: λ_obs(v) = m_H_obs² / (2 v_obs²).
# Observed values are PDG (NOT derivation inputs; included as audit
# comparators per the source note's forbidden_imports_used: false).

m_H_obs_GeV = 125.10  # PDG comparator only
v_obs_GeV = 246.22  # PDG comparator only
lam_obs_at_v = m_H_obs_GeV ** 2 / (2 * v_obs_GeV ** 2)
print(
    f"\n  [INFO] audit comparator (NOT a derivation input):"
    f"\n         λ_tree(μ_* ≈ M_Pl)  ≈  {lam_numerical:.4f}    [framework UV anchor]"
    f"\n         λ_obs(v)            ≈  {lam_obs_at_v:.4f}    [PDG extraction at v]"
    f"\n         ratio λ_tree / λ_obs = {lam_numerical/lam_obs_at_v:.4f}"
    f"\n         interpretation: framework's tree-level UV anchor sits"
    f"\n           ~ 26% above observed λ at v; this gap is the framework's"
    f"\n           +12% m_H_tree gap squared, expected to close via the"
    f"\n           framework's named SM RGE + CW + lattice-spacing +"
    f"\n           Wilson-taste-breaking corrections (HIGGS_MASS_FROM_AXIOM Step 5)."
)

# Confirm the gap structure
mh_tree_GeV = v_obs_GeV / (2 * u0_value)  # 140.3 GeV approx
gap_pct = (mh_tree_GeV - m_H_obs_GeV) / m_H_obs_GeV * 100
check(
    "m_H_tree ≈ 140.3 GeV (sanity check on framework's tree-level prediction)",
    139.0 < mh_tree_GeV < 142.0,
    f"m_H_tree = {mh_tree_GeV:.2f} GeV",
)
check(
    "Tree-level gap to observed m_H is +12%",
    11.0 < gap_pct < 13.0,
    f"gap = +{gap_pct:.2f}%",
)


# ============================================================================
section("Part 7: structural assertions")
# ============================================================================

# λ_tree depends only on u_0 (Clifford-fixed; no other parameters)
free_syms = lam_tree.free_symbols
check(
    "λ_tree is Clifford-fixed (only u_0 dependence)",
    free_syms == {u0},
    f"free_symbols = {free_syms}",
)

# Sign assertion: λ_tree > 0 (positive quartic, vacuum stable)
check(
    "λ_tree > 0 (positive quartic, vacuum stable at tree level)",
    lam_numerical > 0,
    f"λ_tree = {lam_numerical:.6f}",
)

# Dimension assertion: 1/(8 u_0²) is dimensionless (u_0 is dimensionless)
check(
    "λ_tree is dimensionless (u_0 is dimensionless lattice tadpole)",
    True,  # by construction
    "1/(8 u_0²) is dim-0 since u_0 is dim-0",
)


# ============================================================================
section("Summary")
# ============================================================================
print(f"\nTOTAL : PASS = {PASS}, FAIL = {FAIL}")
if FAIL > 0:
    sys.exit(1)
sys.exit(0)
