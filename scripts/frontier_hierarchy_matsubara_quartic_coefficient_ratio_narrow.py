#!/usr/bin/env python3
"""Verify the narrow Matsubara quartic coefficient ratio theorem.

Claim scope: at L_s = 2 minimal APBC block with mean-field gauge
factorization, the small-m expansion of the staggered free-energy density

    Δf(L_t, m) = (1/(2L_t)) Σ_ω log(1 + m²/(u_0²(3+sin²ω)))

has the exact m⁴ coefficient

    B(L_t) = -(1/(4 L_t u_0⁴)) Σ_ω 1/(3+sin²ω)²

with B_2 = -1/(64 u_0⁴), B_4 = -1/(49 u_0⁴), and the structural ratio

    |B_4| / |B_2| = 64/49 = (8/7)² = (A_2/A_4)²    (exact rational).

Class (A) algebraic on parent narrow theorem + standard log Taylor
expansion. Verified two ways: (i) Fraction arithmetic on the explicit
coefficient formula; (ii) symbolic differentiation of Δf via SymPy.
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
    ROOT
    / "docs"
    / "HIERARCHY_MATSUBARA_QUARTIC_COEFFICIENT_RATIO_NARROW_THEOREM_NOTE_2026-05-10.md"
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
    "Hierarchy Matsubara Quartic Coefficient Ratio",
    "**Claim type:** bounded_theorem",
    "B(L_t)",
    "(8/7)²",
    "Composite-Higgs slogan retired",
    "This is a bounded_theorem source row.",
    "does not close a Higgs EFT",
]
for s in required_strings:
    check(f"note contains: '{s[:50]}'", s in note_text)


# ============================================================================
section("Part 2: exact rational B(L_t) via explicit formula (Fraction)")
# ============================================================================


def matsubara_modes_sin_squared(L_t: int) -> list[Fraction]:
    """Return the L_t APBC Matsubara mode sin² values as rationals
    when L_t is in {2, 4}.

    L_t = 2: omega in {pi/2, 3pi/2}, sin^2 = {1, 1}
    L_t = 4: omega in {pi/4, 3pi/4, 5pi/4, 7pi/4}, sin^2 = 1/2 (all)
    """
    if L_t == 2:
        return [Fraction(1), Fraction(1)]
    if L_t == 4:
        return [Fraction(1, 2)] * 4
    raise NotImplementedError(f"rational mode list not tabulated for L_t = {L_t}")


def A_lattice(L_t: int) -> Fraction:
    """A(L_t) * u_0² (dimensionless rational)."""
    s2_list = matsubara_modes_sin_squared(L_t)
    return sum(Fraction(1) / (Fraction(3) + s2) for s2 in s2_list) / (2 * L_t)


def B_lattice_magnitude(L_t: int) -> Fraction:
    """|B(L_t)| * u_0⁴ (positive rational; B itself is negative)."""
    s2_list = matsubara_modes_sin_squared(L_t)
    return sum(Fraction(1) / (Fraction(3) + s2) ** 2 for s2 in s2_list) / (4 * L_t)


# Verify A_2, A_4 (from parent narrow theorem; cross-check)
A2 = A_lattice(2)
A4 = A_lattice(4)
check(
    "A_2 · u_0² = 1/8 (parent cross-check)",
    A2 == Fraction(1, 8),
    f"A_2 = {A2}",
)
check(
    "A_4 · u_0² = 1/7 (parent cross-check)",
    A4 == Fraction(1, 7),
    f"A_4 = {A4}",
)

# Verify B_2, B_4 (this note's load-bearing computation)
B2_mag = B_lattice_magnitude(2)
B4_mag = B_lattice_magnitude(4)
check(
    "|B_2| · u_0⁴ = 1/64 (new identity)",
    B2_mag == Fraction(1, 64),
    f"|B_2| = {B2_mag}",
)
check(
    "|B_4| · u_0⁴ = 1/49 (new identity)",
    B4_mag == Fraction(1, 49),
    f"|B_4| = {B4_mag}",
)

# The cross-endpoint ratio
ratio_B = B4_mag / B2_mag
expected_ratio = Fraction(64, 49)
check(
    "|B_4|/|B_2| = 64/49 = (8/7)² (the new structural identity)",
    ratio_B == expected_ratio,
    f"ratio = {ratio_B}",
)

# Verify it equals (A_4/A_2)² — the squared inverse m² coefficient ratio.
# This is the right direction: |B| Sigma uses 1/(3+s²)² (squared), so the
# A ratio appears squared; and A(L_t=4) > A(L_t=2), so we need A_4/A_2 here.
A_ratio_sq_inv = (A4 / A2) ** 2
check(
    "|B_4|/|B_2| = (A_4/A_2)² (squared inverse m² coef ratio)",
    ratio_B == A_ratio_sq_inv,
    f"(A_4/A_2)² = {A_ratio_sq_inv}",
)
check(
    "(8/7)² = 64/49 numerical sanity",
    Fraction(8, 7) ** 2 == Fraction(64, 49),
)


# ============================================================================
section("Part 3: symbolic differentiation cross-check (SymPy)")
# ============================================================================
#
# Independently re-derive A(L_t) and B(L_t) by symbolic differentiation of
# Δf(L_t, m) at m = 0. This verifies the explicit formula in Part 2 against
# a fully different computational path.

m = sp.symbols("m", real=True)
u0 = sp.symbols("u0", positive=True)


def df_symbolic(L_t: int) -> sp.Expr:
    """Δf(L_t, m) symbolic for L_t ∈ {2, 4}."""
    s2_list = (
        [sp.Rational(1)] * 2
        if L_t == 2
        else [sp.Rational(1, 2)] * 4
    )
    return (
        sum(sp.log(1 + m ** 2 / (u0 ** 2 * (sp.Rational(3) + s2))) for s2 in s2_list)
        / (2 * L_t)
    )


for L_t in (2, 4):
    df = df_symbolic(L_t)
    # m² coefficient = (1/2) d²Δf/dm²|₀
    A_sym = sp.simplify(sp.diff(df, m, 2).subs(m, 0) / 2)
    # m⁴ coefficient = (1/24) d⁴Δf/dm⁴|₀
    B_sym = sp.simplify(sp.diff(df, m, 4).subs(m, 0) / 24)

    A_expected = sp.Rational(1, 8 if L_t == 2 else 7) / u0 ** 2
    B_expected = sp.Rational(-1, 64 if L_t == 2 else 49) / u0 ** 4

    check(
        f"L_t={L_t}: A symbolic matches explicit formula",
        sp.simplify(A_sym - A_expected) == 0,
        f"sym = {A_sym}, expected = {A_expected}",
    )
    check(
        f"L_t={L_t}: B symbolic matches explicit formula",
        sp.simplify(B_sym - B_expected) == 0,
        f"sym = {B_sym}, expected = {B_expected}",
    )


# ============================================================================
section("Part 4: sign assertion (B(L_t) < 0 — opposite from V_taste)")
# ============================================================================
#
# The framework has TWO related quantities with opposite m² and m⁴ signs:
#
#   Δf  (HIERARCHY notes):  +A m² + B m⁴ with A > 0, B < 0  [stabilizing m²,
#                                                            destabilizing m⁴]
#   V_taste (HIGGS notes):  -2/u_0² m² + 1/(4u_0⁴) m⁴      [tachyonic m²,
#                                                          stabilizing m⁴]
#
# These are NOT the same effective potential — they differ by an overall
# sign convention (Δf is the free-energy density change due to fermion mass
# m; V_taste is the Higgs-EFT effective potential with EWSB sign convention).

check("B(L_t=2) is negative", float(-B2_mag) < 0, f"B_2 = {-B2_mag}")
check("B(L_t=4) is negative", float(-B4_mag) < 0, f"B_4 = {-B4_mag}")


# ============================================================================
section("Part 5: standard Higgs minimum readout vs framework's per-mode")
# ============================================================================
#
# If one APPLIED the standard Higgs minimum extraction
#   v² = A(L_t) / (2 |B(L_t)|)
# then v(L_t=4)/v(L_t=2) = √[(A_4/A_2) × (|B_2|/|B_4|)]
#                       = √[(8/7) × (49/64)]
#                       = √(7/8)  =  (7/8)^(1/2)  ≈  0.9354.
#
# This is NOT the framework's claimed (7/8)^(1/4) compression, which is the
# per-mode geometric-mean readout from the determinant identity (separate
# narrow theorem). This part of the runner verifies the distinction
# explicitly.

v_sq_2 = A2 / (2 * B2_mag)  # = 4 u_0² (drops u_0² because A and B have opposite u_0 powers)
v_sq_4 = A4 / (2 * B4_mag)  # = 7 u_0² / 2

# These are dimensionless lattice-units values (u_0² already cancels in ratio)
# The ratio v²(L_t=4) / v²(L_t=2) gives u_0-independent rational
v_sq_ratio = v_sq_4 / v_sq_2
expected_v_sq_ratio = Fraction(7, 8)
check(
    "Standard Higgs minimum v²(L_t=4)/v²(L_t=2) = 7/8",
    v_sq_ratio == expected_v_sq_ratio,
    f"ratio = {v_sq_ratio}",
)

# So under standard Higgs minimum, v compression = (7/8)^(1/2)
import math as _math
v_compression_higgs = float(expected_v_sq_ratio) ** 0.5
v_compression_per_mode = (7 / 8) ** 0.25
check(
    "Standard Higgs compression = (7/8)^(1/2) ≈ 0.9354",
    abs(v_compression_higgs - 0.9354143467422) < 1e-10,
    f"computed = {v_compression_higgs:.10f}",
)
check(
    "Framework per-mode compression = (7/8)^(1/4) ≈ 0.9672 (DIFFERENT)",
    abs(v_compression_per_mode - 0.9671682101343) < 1e-10,
    f"per-mode = {v_compression_per_mode:.10f}, "
    f"difference = {abs(v_compression_higgs - v_compression_per_mode):.4f}",
)
check(
    "(7/8)^(1/2) ≠ (7/8)^(1/4) — standard Higgs and per-mode readouts disagree",
    abs(v_compression_higgs - v_compression_per_mode) > 0.01,
    f"differ by {abs(v_compression_higgs - v_compression_per_mode) * 100:.2f}%",
)


# ============================================================================
section("Part 6: composite-Higgs slogan retirement (named obstruction)")
# ============================================================================
#
# The slogan "composite Higgs (no elementary scalar) ⟹ λ(M_Pl) = 0" in
# VACUUM_CRITICAL_STABILITY_NOTE assumes that the absence of a bare quartic
# in the lattice action implies a vanishing UV quartic. The honest
# computation here gives finite, nonzero induced quartic on both endpoints:

check(
    "B(L_t=2) ≠ 0 (induced quartic is finite on L_t=2)",
    B2_mag != 0,
    f"|B_2| = {B2_mag}",
)
check(
    "B(L_t=4) ≠ 0 (induced quartic is finite on L_t=4)",
    B4_mag != 0,
    f"|B_4| = {B4_mag}",
)
print(
    "\n  [INFO] composite-Higgs ⟹ λ(M_Pl)=0 slogan is structurally retired:"
    "\n         the induced quartic from integrating out staggered fermions"
    "\n         is finite and nonzero on both endpoints. NJL-type counterexample"
    "\n         (Bardeen-Hill-Lindner 1990) confirmed on framework's own surface."
)


# ============================================================================
section("Summary")
# ============================================================================
print(f"\nTOTAL : PASS = {PASS}, FAIL = {FAIL}")
if FAIL > 0:
    sys.exit(1)
sys.exit(0)
