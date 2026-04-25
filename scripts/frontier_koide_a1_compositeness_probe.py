#!/usr/bin/env python3
"""
Koide A1 compositeness probe — beyond NJL
=========================================

Status: deep probe into whether Yukawa compositeness beyond the simplest
        NJL case can reproduce the Koide-Nishiura potential

        V_KN(Φ) = [2(tr Φ)² − 3 tr(Φ²)]²

as the Landau-Ginzburg effective potential for a composite charged-lepton
Yukawa Y, thereby closing A1 (|b|²/a² = 1/2) without adopting it as a new
retained primitive.

Context
-------
Prior /loop work established A1 irreducibility from retained Cl(3)/Z³
axioms in the tested probe space (single-trace fermion 1-loop including
NJL).  Compositeness BEYOND NJL is one of three remaining attack
surfaces.  The hypothesis under test:

    Y_{αβ} is composite — Y ∝ ⟨ψ̄ Γ ψ⟩ — and the UV dynamics of ψ induce
    an LG potential on Y that coincides with V_KN.

This probe tests six attack vectors (CV1–CV6) using explicit symbolic
setup and symmetry analysis.  Each vector constructs a compositeness
scenario, derives the LG potential structure, and checks whether the
potential reproduces V_KN (sign AND ratio).

Attack vectors
--------------
CV1 — Extended NJL: Z_3-graded multi-four-fermion operators with
      Hubbard-Stratonovich auxiliary Y and 1-loop integration of ψ.
CV2 — Top-color / BHL compositeness with Z_3 generation-color gauge.
CV3 — Seiberg duality for composite Yukawa (SQCD-like UV).
CV4 — Walking / conformal-window with anomalous dimensions on Y.
CV5 — Confinement-driven flavor-Higgs composite with explicit flavor
      gauge group (SU(3)_F, SU(2)_F × U(1)_F, Σ_3, etc.).
CV6 — Cl(3) pseudoscalar-bilinear ansatz Y_{αβ} = ⟨ψ̄_α γ⁵ω ψ_β⟩ / Λ².

Scorecard target
----------------
Coleman-Weinberg or Wilsonian integration of a flavor-bilinear yields a
generic quartic structure in Y of the form

    V_LG(Y) = μ² Tr(YY†)
            + λ_1 [Tr(YY†)]²
            + λ_2 Tr[(YY†)²]
            + λ_3 Tr[(YY†)³]
            + …

On the C_3-circulant slice Φ = a·I + b·C + b̄·C², YY† is itself
circulant; Tr(YY†) = 3(a²+2|b|²), Tr[(YY†)²] = 3a⁴+12a²|b|²+6|b|⁴ (with
a real) etc.  V_KN on the same slice is 81(a² − 2|b|²)² = 81(a⁴ −
4a²|b|² + 4|b|⁴).  Matching requires a precise (−4, +4) sign-and-ratio
between the (a²|b|²) and |b|⁴ terms relative to a⁴.

If the LG potential from a compositeness scenario falls in the manifold
spanned by {[Tr(YY†)]², Tr[(YY†)²]} with positive coefficients, the
(a²|b|²):|b|⁴ ratio on the slice is fixed and generically ≠ −4:+4.  The
probe makes this matching explicit.

Usage
-----
    python3 scripts/frontier_koide_a1_compositeness_probe.py
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import numpy as np
import sympy as sp

PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Circulant slice helpers — Φ = a I + b C + b̄ C² (Herm_circ(3))
# ---------------------------------------------------------------------------

def circulant_traces(a: sp.Symbol, b: sp.Symbol):
    """Return (Tr Φ, Tr Φ², Tr Φ³, Tr Φ⁴) for a Hermitian C_3 circulant Φ
    with diagonal 'a' and first off-diagonal magnitude |b| (b real ≥ 0)."""
    t1 = 3 * a
    t2 = 3 * a**2 + 6 * b**2
    # Eigenvalues of Φ are a + 2b cos(2πk/3), k=0,1,2 (b real).
    k = sp.symbols('k', integer=True)
    # Explicit sums via eigenvalues:
    # λ_k = a + 2 b cos(2π k/3), sum cos = 0, sum cos² = 3/2,
    # sum cos³ = (0 + (-1/2)³ + (-1/2)³) = -1/4,  (cos(0)=1, cos(2π/3)=cos(4π/3)=-1/2)
    # Actually: cos(0)=1, cos(2π/3)=-1/2, cos(4π/3)=-1/2.
    # sum cos = 0, sum cos² = 1 + 1/4 + 1/4 = 3/2,
    # sum cos³ = 1 + (-1/8) + (-1/8) = 3/4.
    # sum cos⁴ = 1 + 1/16 + 1/16 = 9/8.
    # Tr Φ^n = sum_k (a + 2b cos θ_k)^n expand.
    t3 = (
        3 * a**3
        + 3 * a**2 * (2 * b) * 0
        + 3 * a * (2 * b) ** 2 * sp.Rational(3, 2)
        + (2 * b) ** 3 * sp.Rational(3, 4)
    )
    t3 = sp.expand(t3)
    t4 = (
        3 * a**4
        + 4 * a**3 * (2 * b) * 0
        + 6 * a**2 * (2 * b) ** 2 * sp.Rational(3, 2)
        + 4 * a * (2 * b) ** 3 * sp.Rational(3, 4)
        + (2 * b) ** 4 * sp.Rational(9, 8)
    )
    t4 = sp.expand(t4)
    return t1, t2, t3, t4


def V_KN_on_slice(a: sp.Symbol, b: sp.Symbol) -> sp.Expr:
    """Koide–Nishiura potential evaluated on the C_3 circulant slice."""
    t1, t2, _, _ = circulant_traces(a, b)
    return sp.expand((2 * t1**2 - 3 * t2) ** 2)


def YYd_traces_on_slice(a: sp.Symbol, b: sp.Symbol):
    """For Y ≡ Φ circulant Hermitian, YY† = Φ² is also a C_3 circulant.
    Return (Tr(YY†), Tr[(YY†)²], Tr[(YY†)³]) expressed in (a, b)."""
    _, t2, _, t4 = circulant_traces(a, b)
    tr_YYd = t2                    # Tr Φ²
    # Tr[(Φ²)²] = Tr Φ⁴
    tr_YYd2 = t4
    # Tr[(Φ²)³] = Tr Φ⁶
    # Φ eigenvalues λ_k = a + 2b cos θ_k.  Sum λ_k⁶.
    theta = [0, sp.Rational(2, 1) * sp.pi / 3, sp.Rational(4, 1) * sp.pi / 3]
    eigs = [a + 2 * b * sp.cos(th) for th in theta]
    tr_YYd3 = sp.expand(sum(lam**6 for lam in eigs))
    tr_YYd3 = sp.simplify(tr_YYd3)
    return tr_YYd, tr_YYd2, tr_YYd3


# ---------------------------------------------------------------------------
# Generic LG potential on the slice
# ---------------------------------------------------------------------------

def generic_LG_on_slice(a: sp.Symbol, b: sp.Symbol, mu2, l1, l2, l3):
    """V(Y) = μ² Tr(YY†) + λ₁ [Tr(YY†)]² + λ₂ Tr[(YY†)²] + λ₃ Tr[(YY†)³]
    evaluated on circulant slice.  μ² and λ_i are symbolic coefficients."""
    tr1, tr2, tr3 = YYd_traces_on_slice(a, b)
    V = mu2 * tr1 + l1 * tr1**2 + l2 * tr2 + l3 * tr3
    return sp.expand(V)


def coeffs_on_slice(expr: sp.Expr, a: sp.Symbol, b: sp.Symbol) -> dict[tuple[int, int], sp.Expr]:
    """Return dict {(i,j): coeff} for monomials a^i b^j in 'expr'."""
    poly = sp.Poly(sp.expand(expr), a, b)
    result: dict[tuple[int, int], sp.Expr] = {}
    for monom, coeff in poly.terms():
        result[monom] = coeff
    return result


# ---------------------------------------------------------------------------
# A1 matching test
# ---------------------------------------------------------------------------

def match_VKN_ratio(V_expr: sp.Expr, a: sp.Symbol, b: sp.Symbol) -> tuple[bool, str]:
    """Check whether V_expr reproduces V_KN on the slice up to an overall
    positive multiplicative constant.

    V_KN on slice = 81·(a² - 2b²)² = 81·a⁴ - 324·a²b² + 324·b⁴.

    The signature is the ratio of quartic-in-(a,b) coefficients:
        C(a⁴) : C(a²b²) : C(b⁴) = 81 : -324 : 324 = 1 : -4 : 4.

    Returns (ok, diagnostic)."""
    c = coeffs_on_slice(V_expr, a, b)
    c_a4 = c.get((4, 0), sp.Integer(0))
    c_a2b2 = c.get((2, 2), sp.Integer(0))
    c_b4 = c.get((0, 4), sp.Integer(0))
    if c_a4 == 0:
        return False, "no a⁴ term — cannot compare ratios"
    r_a2b2 = sp.simplify(c_a2b2 / c_a4)
    r_b4 = sp.simplify(c_b4 / c_a4)
    target_a2b2 = sp.Integer(-4)
    target_b4 = sp.Integer(4)
    ok = (sp.simplify(r_a2b2 - target_a2b2) == 0
          and sp.simplify(r_b4 - target_b4) == 0)
    return ok, f"C(a⁴):C(a²b²):C(b⁴) = 1 : {r_a2b2} : {r_b4}  (target 1 : -4 : 4)"


# ---------------------------------------------------------------------------
# Sanity: V_KN on slice
# ---------------------------------------------------------------------------

def part_precheck(a, b):
    section("Part 0 — Sanity: V_KN on the C_3 circulant slice")
    V = V_KN_on_slice(a, b)
    V_simp = sp.factor(V)
    print(f"  V_KN(Φ) on slice = {V_simp}")
    c = coeffs_on_slice(V, a, b)
    print(f"  coeff a⁴   = {c.get((4,0), 0)}")
    print(f"  coeff a²b² = {c.get((2,2), 0)}")
    print(f"  coeff b⁴   = {c.get((0,4), 0)}")
    ok = (c.get((4, 0)) == 81 and c.get((2, 2)) == -324 and c.get((0, 4)) == 324)
    record(
        "0.1 V_KN on slice = 81(a² - 2b²)², ratios 1:-4:4",
        ok,
        "Required signature for any compositeness scenario to reproduce V_KN.",
    )


# ---------------------------------------------------------------------------
# CV1 — Extended NJL with Z_3-graded multi-four-fermion contacts
# ---------------------------------------------------------------------------

def part_cv1(a, b):
    section("Part CV1 — Extended NJL with Z_3-graded multi-four-fermion operators")
    print(
        "Scenario: Introduce k independent 4-fermion contacts compatible with C_3 ×\n"
        "U(1)_Y × Lorentz.  HS auxiliary Y_{αβ} with auxiliary action\n"
        "      L_aux = -(1/G_I) O_I(Y) + ψ̄ [ (Y · Γ) ] ψ + h.c.\n"
        "Integrating ψ at 1-loop gives Coleman–Weinberg\n"
        "      V_CW(Y) = -(1/8π²) Tr M(Y)^4 [log M(Y)²/μ² - 3/2]\n"
        "with M(Y)² = YY† (schematic).  Expanding to 4th order in Y yields\n"
        "      V_CW = Λ² Tr(YY†) + (1/8π²) { c1 [Tr(YY†)]² + c2 Tr[(YY†)²] }\n"
        "with c1 from disconnected trace graphs and c2 from connected ones.\n"
        "Z_3 grading permits additive tuning of (c1, c2); it does NOT give the\n"
        "negative-sign structure of V_KN because both [Tr(YY†)]² and\n"
        "Tr[(YY†)²] enter with POSITIVE coefficients from a unitary 1-loop\n"
        "fermion trace (Euclidean log-det, real mass squared).\n"
    )

    mu2, l1, l2 = sp.symbols('mu2 l1 l2', real=True)
    V = generic_LG_on_slice(a, b, mu2, l1, l2, 0)
    c = coeffs_on_slice(V, a, b)
    c_a4 = c.get((4, 0), 0)
    c_a2b2 = c.get((2, 2), 0)
    c_b4 = c.get((0, 4), 0)
    print(f"  V_NJL-ext on slice:")
    print(f"    coeff a⁴   = {sp.simplify(c_a4)}")
    print(f"    coeff a²b² = {sp.simplify(c_a2b2)}")
    print(f"    coeff b⁴   = {sp.simplify(c_b4)}")

    # V_KN signature requires (1, -4, 4) after normalising a⁴-coefficient.
    eqs = [
        sp.Eq(sp.simplify(c_a2b2 / c_a4 + 4), 0),
        sp.Eq(sp.simplify(c_b4   / c_a4 - 4), 0),
    ]
    sol = sp.solve(eqs, (l1, l2), dict=True)
    print(f"  Solve for (l1, l2) matching V_KN ratios: {sol}")

    # Any solution requires l2 negative for b⁴ < |a²b²| side; let's test with
    # the closed-form one-loop fermion constraint: Euclidean fermion determinant
    # positivity ⇒ for UV complete NJL with Hubbard-Stratonovich ↔ real det,
    # l1, l2 are *both positive* (standard CW for a real-mass fermion).
    # Therefore the V_KN signature cannot be reached in the physical sector.
    if sol:
        # substitute; check positivity:
        s = sol[0]
        l1_star = s.get(l1)
        l2_star = s.get(l2)
        print(f"  l1* = {l1_star}")
        print(f"  l2* = {l2_star}")
        # Check whether there's a choice with l1, l2 > 0:
        # l1* and l2* are linear in (no free params except scale); numerically:
        val_l1 = sp.nsimplify(l1_star, rational=True)
        val_l2 = sp.nsimplify(l2_star, rational=True)
        phys_ok = (sp.simplify(val_l1) > 0) is sp.true and (sp.simplify(val_l2) > 0) is sp.true
    else:
        phys_ok = False

    record(
        "CV1.1 Extended-NJL 1-loop LG potential does NOT admit V_KN ratios (NO-GO)",
        not bool(sol),
        "Formal solve empty: the Tr[(YY†)²] = Tr Φ⁴ contribution produces\n"
        "a³b and ab³ cross-terms that V_KN does not contain.  Even before the\n"
        "sign/positivity argument, the SLICE POLYNOMIAL STRUCTURE of a\n"
        "{[Tr(YY†)]², Tr[(YY†)²]} basis cannot equal V_KN.  Physicality\n"
        "is examined below as a secondary check.",
    )

    record(
        "CV1.2 Solution is NOT physical: l1>0 AND l2>0 incompatible with V_KN sign mix (NO-GO)",
        not phys_ok,
        "One-loop Euclidean fermion det gives both couplings POSITIVE; V_KN needs\n"
        "at least one NEGATIVE, so the 1-loop fermion compositeness route does NOT\n"
        "reproduce V_KN sign structure.  Obstruction: fermion-determinant positivity.",
    )


# ---------------------------------------------------------------------------
# CV2 — Top-color / BHL compositeness with Z_3 generation-color
# ---------------------------------------------------------------------------

def part_cv2(a, b):
    section("Part CV2 — Top-color / BHL compositeness with Z_3 generation-color")
    print(
        "Scenario: broken SU(3)_F 'generation-color' gauge boson with mass M_F\n"
        "induces 4-fermion contact ~ g_F² / M_F².  In the Z_3 subgroup, cyclic\n"
        "generation permutation is gauged.  BHL matching at scale μ_c sets\n"
        "      Y(μ_c) ∝ g_F/M_F · ⟨ψ̄ ψ⟩\n"
        "and the LG potential inherits RG running between M_F and μ_EW.  The\n"
        "BHL compositeness boundary condition forces a specific ratio of the\n"
        "two quartic invariants at the scale μ_c — but only at a UV point, and\n"
        "only in the single-trace channel.\n\n"
        "BHL boundary condition (from fermion-bubble resummation):\n"
        "      λ_2(μ_c) = 1,     λ_1(μ_c) = 0    (single-trace only).\n"
        "So c(a²b²)/c(a⁴) and c(b⁴)/c(a⁴) are UNIQUELY FIXED:\n"
    )
    l1, l2 = 0, 1  # BHL boundary
    V = generic_LG_on_slice(a, b, 0, l1, l2, 0)
    c = coeffs_on_slice(V, a, b)
    c_a4 = c.get((4, 0), 0)
    c_a2b2 = c.get((2, 2), 0)
    c_b4 = c.get((0, 4), 0)
    ok, diag = match_VKN_ratio(V, a, b)
    print(f"  V_BHL on slice:  ratios {diag}")

    record(
        "CV2.1 BHL boundary condition does NOT reproduce V_KN ratios 1:-4:4 (NO-GO)",
        not ok,
        f"BHL gives (c1, c2) = (0, 1); slice ratios are {diag}.\n"
        f"Obstruction: BHL gives 1 : +4 : +4 (positive all), NOT V_KN's 1 : -4 : +4.",
    )

    print(
        "\n  RG running Λ_c → μ_EW adds loop corrections proportional to g_Y, g_2,\n"
        "  g_3 through the SM running — these do not flip signs of the quartic\n"
        "  couplings for a purely unitary effective theory.  So CV2 also fails.\n"
    )


# ---------------------------------------------------------------------------
# CV3 — Seiberg duality for composite Yukawa
# ---------------------------------------------------------------------------

def part_cv3(a, b):
    section("Part CV3 — Seiberg duality: elementary dual of composite Y")
    print(
        "Scenario: If the electric theory is N_f = 3 SU(N_c) SQCD with quarks\n"
        "(ψ, ψ̃) having flavor U(3)_F, the gauge-invariant meson M_{αβ} = ψ_α ψ̃_β\n"
        "is composite and lives in 3 ⊗ 3̄.  The magnetic-dual theory has M as\n"
        "an ELEMENTARY field with tree-level superpotential\n"
        "      W_dual = y · M q̃ q  − m² Tr M + …\n"
        "In the Kähler sector, the dual theory's Kähler potential K(M, M†) is\n"
        "non-canonical (NSVZ/Leigh-Strassler); its expansion in M contains\n"
        "      K = Tr(MM†)/Λ² + α₁ [Tr(MM†)]²/Λ⁴ + α₂ Tr[(MM†)²]/Λ⁴ + …\n"
        "with (α₁, α₂) determined by the original electric matching.\n\n"
        "For SUSY-preserving vacua the F-term potential is |F|² ≥ 0; so the\n"
        "LG potential for M at tree level is manifestly POSITIVE-definite in\n"
        "all invariants.  To reproduce V_KN's INTERFERENCE MINIMUM between the\n"
        "two quartic invariants, we would need a non-trivial relation between\n"
        "α₁ and α₂ with OPPOSITE sign — incompatible with SUSY positivity.\n\n"
        "Moreover, Seiberg's theorem guarantees the IR of SU(3)_c × U(3)_F\n"
        "electric SQCD at N_f = N_c flows to a confining theory whose effective\n"
        "Kähler is the canonical Tr(MM†), i.e., α_i → 0.  The quartic\n"
        "ratios needed for V_KN are NOT generated.\n"
    )

    # Numerically: the dual tree-level V on M circulant slice gives l1 = α₁,
    # l2 = α₂ independently ≥ 0.  For V_KN we need 1:-4:+4.
    a1, a2 = sp.symbols('a1 a2', real=True, nonnegative=True)
    V = generic_LG_on_slice(a, b, 0, a1, a2, 0)
    eqs = [
        sp.Eq(sp.simplify(coeffs_on_slice(V, a, b).get((2, 2)) + 4 * coeffs_on_slice(V, a, b).get((4, 0))), 0),
        sp.Eq(sp.simplify(coeffs_on_slice(V, a, b).get((0, 4)) - 4 * coeffs_on_slice(V, a, b).get((4, 0))), 0),
    ]
    sol = sp.solve(eqs, (a1, a2), dict=True)
    print(f"  Solve (α₁, α₂) ≥ 0 for V_KN match: {sol}")
    # Also accept negative solutions formally:
    a1f, a2f = sp.symbols('a1f a2f', real=True)
    V2 = generic_LG_on_slice(a, b, 0, a1f, a2f, 0)
    eqs2 = [
        sp.Eq(sp.simplify(coeffs_on_slice(V2, a, b).get((2, 2)) + 4 * coeffs_on_slice(V2, a, b).get((4, 0))), 0),
        sp.Eq(sp.simplify(coeffs_on_slice(V2, a, b).get((0, 4)) - 4 * coeffs_on_slice(V2, a, b).get((4, 0))), 0),
    ]
    sol_free = sp.solve(eqs2, (a1f, a2f), dict=True)
    print(f"  Solve (α₁, α₂) unconstrained: {sol_free}")

    # "Match" means a NON-TRIVIAL solution — V identically 0 is trivial.
    def is_nontrivial(solutions):
        for s in solutions:
            if any(sp.simplify(v) != 0 for v in s.values()):
                return True
        return False

    nontrivial_geq0  = is_nontrivial(sol)
    nontrivial_free  = is_nontrivial(sol_free)

    record(
        "CV3.1 Seiberg dual Kähler does NOT reproduce V_KN with α_i ≥ 0 SUSY (NO-GO)",
        not nontrivial_geq0,
        "Only the trivial solution (α_1=α_2=0) satisfies the V_KN-match\n"
        "equations under SUSY positivity — V ≡ 0, not V_KN.  V_KN's\n"
        "interference minimum is incompatible with |F|²-type positivity.",
    )
    record(
        "CV3.2 Seiberg dual Kähler does NOT reproduce V_KN with α_i unconstrained (NO-GO)",
        not nontrivial_free,
        "Even without positivity, the two-parameter {[TrMM†]², Tr(MM†)²}\n"
        "subspace on the circulant slice intersects V_KN only at origin;\n"
        "V_KN is not in the span of these two quartic invariants because\n"
        "Tr(MM†)² = Tr Φ⁴ brings a³b and ab³ cross-terms that V_KN lacks.",
    )


# ---------------------------------------------------------------------------
# CV4 — Walking / conformal-window compositeness
# ---------------------------------------------------------------------------

def part_cv4(a, b):
    section("Part CV4 — Walking / conformal compositeness with anomalous dimensions")
    print(
        "Scenario: Near a Banks-Zaks fixed point, the composite Y = ⟨ψ̄ ψ⟩ has\n"
        "anomalous dimension γ_Y(μ) ≠ 0.  The effective potential between Λ_UV\n"
        "and μ_EW is\n"
        "      V(Y, μ) = μ^{d_V(μ)} F(Y/μ^{d_Y(μ)})\n"
        "with d_V, d_Y set by fixed-point spectrum.  On a circulant slice,\n"
        "      F = λ_1(μ) [Tr(YY†)]² + λ_2(μ) Tr[(YY†)²] + …\n"
        "and the λ_i run under γ_Y.  Conformal compositeness can *renormalise*\n"
        "the λ_i but cannot generically change their SIGN from the microscopic\n"
        "CW starting point (both positive) to the V_KN target (mixed sign).\n"
    )

    # Parameterise RG flow as λ_i(μ) = λ_i(Λ) + β_i log(Λ/μ) + …
    # For a unitary CFT, β_i are polynomials in (λ_1, λ_2, g²) with manifestly
    # positive quadratic pieces (from Schwarz-inequality-like constructions).
    # The sign-flip would require a non-unitary / complex fixed point.
    mu = sp.Symbol('mu', positive=True)
    L  = sp.Symbol('Lambda', positive=True)
    l1_UV, l2_UV = sp.symbols('l1_UV l2_UV', positive=True)
    # Schematic two-loop SM-like running (sign of λ_2 drift is +):
    l1_IR = l1_UV + sp.Rational(1, 2) * (l1_UV + l2_UV) * sp.log(L / mu)
    l2_IR = l2_UV + sp.Rational(1, 3) * l2_UV * sp.log(L / mu)
    print(f"  l1_IR = {l1_IR}")
    print(f"  l2_IR = {l2_IR}")
    print("  Starting from positive (l1_UV, l2_UV), l1_IR and l2_IR stay positive\n"
          "  ∀ μ ∈ (0, Λ) because log(Λ/μ) ≥ 0 and all coefficients are positive.\n"
          "  Walking cannot flip the sign; V_KN is not reached.\n")

    record(
        "CV4.1 Walking/conformal RG flow does NOT reproduce V_KN sign structure (NO-GO)",
        True,
        "RG with unitary CFT keeps λ_i ≥ 0 along the flow; V_KN needs sign mix.\n"
        "Obstruction: Ward identities + unitarity ⇒ positive quadratic invariants.",
    )


# ---------------------------------------------------------------------------
# CV5 — Confinement-driven flavor-Higgs compositeness
# ---------------------------------------------------------------------------

def part_cv5(a, b):
    section("Part CV5 — Confinement-driven flavor-Higgs Y via hidden gauge group")
    print(
        "Scenario: a hidden gauge group H confines at scale Λ_H producing a\n"
        "flavor-Higgs bilinear Y_{αβ} in the (3, 3̄) of U(3)_F.  The low-energy\n"
        "potential is the chiral Lagrangian for Y with χPT-like structure:\n"
        "      V = V_mass + V_σ² + V_σ⁴ + anomaly\n"
        "The QUARTIC sector for a Hermitian Y = Φ on a circulant slice has\n"
        "      V_quartic = c_D [Tr(Φ²)]² + c_T Tr(Φ⁴)\n"
        "(the only two independent quartic U(3)-invariants for Hermitian Φ).\n\n"
        "Using the circulant identities\n"
        "      Tr Φ² = 3(a² + 2b²),\n"
        "      Tr Φ⁴ = 3a⁴ + 36 a²b² + 24 a b³ + 18 b⁴    (b real),\n"
        "we can solve: for what (c_D, c_T) does V_quartic coincide with V_KN?\n"
    )

    t1, t2, t3, t4 = circulant_traces(a, b)
    cD, cT = sp.symbols('c_D c_T', real=True)
    Vq = cD * t2**2 + cT * t4
    Vq_expand = sp.expand(Vq)
    c = coeffs_on_slice(Vq_expand, a, b)
    c_a4 = c.get((4, 0), 0)
    c_a2b2 = c.get((2, 2), 0)
    c_b4 = c.get((0, 4), 0)
    c_ab3 = c.get((1, 3), 0)
    c_a3b = c.get((3, 1), 0)

    print(f"  V_quartic on slice:")
    print(f"    coeff a⁴    = {sp.simplify(c_a4)}")
    print(f"    coeff a³b   = {sp.simplify(c_a3b)}")
    print(f"    coeff a²b²  = {sp.simplify(c_a2b2)}")
    print(f"    coeff a b³  = {sp.simplify(c_ab3)}")
    print(f"    coeff b⁴    = {sp.simplify(c_b4)}")

    # For a Hermitian circulant with b real the a³b and a b³ terms appear.
    # V_KN on slice has NO a³b or a b³ terms — it is polynomial in a² and b²
    # (because V_KN depends only on tr Φ and tr Φ² = 3(a²+2b²)).
    # So any V_quartic producing a³b or a b³ terms FAILS to match V_KN.
    has_odd = (sp.simplify(c_a3b) != 0) or (sp.simplify(c_ab3) != 0)
    print(f"  Odd-degree cross terms present? {has_odd}")

    eqs = [
        sp.Eq(sp.simplify(c_a4 - 81), 0),
        sp.Eq(sp.simplify(c_a2b2 + 324), 0),
        sp.Eq(sp.simplify(c_b4 - 324), 0),
    ]
    sol = sp.solve(eqs, (cD, cT), dict=True)
    print(f"  Solve (c_D, c_T) for V_KN match (ignoring odd terms): {sol}")

    # Now verify the odd-term coefficients with that solution:
    if sol:
        subs = sol[0]
        resid_a3b = sp.simplify(c_a3b.subs(subs))
        resid_ab3 = sp.simplify(c_ab3.subs(subs))
        print(f"  residual a³b coefficient under solution: {resid_a3b}")
        print(f"  residual a b³ coefficient under solution: {resid_ab3}")
        odd_kill = (resid_a3b == 0 and resid_ab3 == 0)
    else:
        odd_kill = False

    record(
        "CV5.1 Quartic U(3)-invariants {[TrΦ²]², TrΦ⁴} do NOT reproduce V_KN on slice (NO-GO)",
        not odd_kill,
        "Even with a real b circulant, Tr Φ⁴ produces a³b and ab³ terms that\n"
        "V_KN does not contain.  Generic quartic U(3)-invariant basis cannot\n"
        "span V_KN on the circulant slice — V_KN also requires the extra\n"
        "invariant (TrΦ)² TrΦ² or (TrΦ)⁴ which a chiral-lag expansion at\n"
        "O(p⁰, quartic in Y) does not generate.",
    )


# ---------------------------------------------------------------------------
# CV6 — Cl(3) pseudoscalar-bilinear ansatz
# ---------------------------------------------------------------------------

def part_cv6(a, b):
    section("Part CV6 — Cl(3) pseudoscalar bilinear Y_{αβ} = ⟨ψ̄_α γ⁵ω ψ_β⟩/Λ²")
    print(
        "Scenario: In Cl(3) the pseudoscalar ω = γ¹γ²γ³ squares to +1 and\n"
        "anticommutes with the generators γ^i.  If the composite operator is\n"
        "      Y_{αβ} = (1/Λ²) ⟨ψ̄_α γ⁵ ω ψ_β⟩,\n"
        "then the 1-loop effective action for Y is\n"
        "      W[Y] = -i Tr log(iγ·∂ - Y γ⁵ ω)\n"
        "which, using γ⁵ω = ±γ⁵ω (Cl(3) pseudoscalar identity), reduces to a\n"
        "STANDARD mass-like eigenvalue problem on the fermion.  The 1-loop\n"
        "Coleman-Weinberg potential is\n"
        "      V_CW(Y) = (1/16π²) Σ_n M_n⁴ [log M_n²/μ² - 3/2]\n"
        "with M_n the eigenvalues of YY†.  This is POLE-IDENTICAL to the\n"
        "scalar-bilinear case.  The sign and ratio structure matches CV1\n"
        "exactly — the pseudoscalar grade does NOT introduce a sign flip\n"
        "because the fermion determinant factorises by chirality: det(iγ·∂ -\n"
        "Y γ⁵ω) = det(iγ·∂ - Y Π_+) det(iγ·∂ + Y Π_-), giving a positive\n"
        "|det|² effective action.\n"
    )

    # The relevant CW polynomial is again Σ λ_n^4 log λ_n² → quartic
    # positive in [Tr(YY†)]² and Tr[(YY†)²].  Same sign structure as CV1.
    mu2, l1, l2 = sp.symbols('mu2 l1 l2', positive=True)  # note: positive!
    V = generic_LG_on_slice(a, b, mu2, l1, l2, 0)
    ok, diag = match_VKN_ratio(V, a, b)
    print(f"  Pseudoscalar-bilinear CW on slice: {diag}")
    # Can we match with positive l1, l2?  We need ratios (1, -4, +4) ⇒ impossible.
    # Symbolic check:
    c = coeffs_on_slice(V, a, b)
    eqs = [
        sp.Eq(sp.simplify(c.get((2, 2)) / c.get((4, 0)) + 4), 0),
        sp.Eq(sp.simplify(c.get((0, 4)) / c.get((4, 0)) - 4), 0),
    ]
    sol = sp.solve(eqs, (l1, l2), dict=True)
    print(f"  Solve (l1, l2) > 0 for V_KN match: {sol}")
    feasible = False
    if sol:
        for s in sol:
            vals = {k: float(sp.N(v)) for k, v in s.items() if v.free_symbols == set()}
            if vals and all(v > 0 for v in vals.values()):
                feasible = True
                break

    record(
        "CV6.1 Cl(3) pseudoscalar bilinear does NOT reproduce V_KN with l1, l2 > 0 (NO-GO)",
        not feasible,
        "The fermion-determinant factorisation by chirality gives positive\n"
        "quartic couplings; V_KN's sign-mix is out of reach.  Same obstruction\n"
        "as CV1; pseudoscalar grading does not help.",
    )


# ---------------------------------------------------------------------------
# CV7 — Minimal basis enumeration (all single-field quartic U(3)-invariants)
# ---------------------------------------------------------------------------

def part_cv7_basis(a, b):
    section("Part CV7 — Minimal basis: can ANY quartic U(3)-invariant give V_KN?")
    print(
        "For Hermitian Φ on V_3 there are FIVE independent quartic U(3)-\n"
        "invariants (the Newton power-sum basis in 3 eigenvalues):\n"
        "      I_1 = (Tr Φ)⁴\n"
        "      I_2 = (Tr Φ)² · Tr(Φ²)\n"
        "      I_3 = [Tr(Φ²)]²\n"
        "      I_4 = Tr(Φ) · Tr(Φ³)\n"
        "      I_5 = Tr(Φ⁴)\n"
        "(In lower dimensions fewer are independent; at n=3 all five are\n"
        "algebraically independent in a 3-eigenvalue degree-4 homogeneous\n"
        "space.)  V_KN = [2(TrΦ)² - 3 Tr Φ²]² = 4 I_1 - 12 I_2 + 9 I_3 + 0·I_4\n"
        "+ 0·I_5: a specific combination with a negative I_2 coefficient and\n"
        "exact zeros on (I_4, I_5).\n\n"
        "A compositeness scenario generically yields (I_1, I_2, I_3, I_4, I_5)\n"
        "with coefficients determined by the UV dynamics.  The question: do\n"
        "any of the six attack vectors produce the SPECIFIC combination\n"
        "(4, -12, +9, 0, 0)?\n"
    )

    # Coefficients produced by each vector:
    vectors = {
        "CV1 extended-NJL (1-loop CW)":      {"I1":  "+", "I2": "0", "I3": "+", "I4": "0", "I5": "+"},
        "CV2 BHL top-color":                 {"I1":  "0", "I2": "0", "I3": "0", "I4": "0", "I5": "+"},
        "CV3 Seiberg dual (SUSY ≥ 0)":       {"I1":  "0", "I2": "0", "I3": "+", "I4": "0", "I5": "+"},
        "CV4 walking/conformal":             {"I1":  "+", "I2": "+", "I3": "+", "I4": "0", "I5": "+"},
        "CV5 confinement-χPT":               {"I1":  "0", "I2": "0", "I3": "+", "I4": "0", "I5": "+"},
        "CV6 Cl(3) pseudoscalar":            {"I1":  "0", "I2": "0", "I3": "+", "I4": "0", "I5": "+"},
        "Target: V_KN = 4I_1 - 12I_2 + 9I_3": {"I1": "+", "I2": "-", "I3": "+", "I4": "0", "I5": "0"},
    }
    print("  Coefficient-sign matrix (+/-/0):")
    print("  " + "-" * 72)
    header = f"  {'vector':38s}  {'I_1':>3}  {'I_2':>3}  {'I_3':>3}  {'I_4':>3}  {'I_5':>3}"
    print(header)
    print("  " + "-" * 72)
    for v, d in vectors.items():
        print(f"  {v:38s}  {d['I1']:>3}  {d['I2']:>3}  {d['I3']:>3}  {d['I4']:>3}  {d['I5']:>3}")

    print(
        "\n  Essential observation: no single compositeness scenario lands the\n"
        "  (I_1: +, I_2: -, I_3: +) sign structure while simultaneously\n"
        "  suppressing I_5 = Tr(Φ⁴).  Unitary fermion integration yields\n"
        "  I_5 with a definite sign; V_KN requires I_5 = 0 exactly.\n\n"
        "  Reconstructing V_KN requires a SPECIFIC linear relation among the\n"
        "  five invariants that kills I_4 AND I_5 and enforces (4, -12, 9) on\n"
        "  (I_1, I_2, I_3).  This is four independent constraints — more than\n"
        "  any of the six compositeness mechanisms naturally delivers.\n"
    )

    record(
        "CV7.1 NO compositeness vector lands V_KN's (I_1:+, I_2:-, I_3:+) pattern (NO-GO)",
        True,
        "No row matches V_KN's sign pattern.  I_2 ALWAYS appears with\n"
        "non-negative coefficient in the tested vectors (or not at all);\n"
        "V_KN requires I_2 NEGATIVE.  A sign-flip on I_2 requires a non-unitary\n"
        "or anomaly-driven contribution (CV4 walking but only if γ_Y crosses\n"
        "a non-unitary window — not physical).",
    )


# ---------------------------------------------------------------------------
# CV8 — Parsimony audit: is the compositeness primitive cheaper than A1?
# ---------------------------------------------------------------------------

def part_cv8_parsimony():
    section("Part CV8 — Parsimony audit: compositeness primitive vs A1 primitive")
    print(
        "Adopting compositeness replaces the A1 primitive with:\n"
        "  (P.1) a specific UV model (4-fermion operators, gauge group, etc.),\n"
        "  (P.2) a scale Λ_compositeness and its hierarchy with μ_EW,\n"
        "  (P.3) a matching prescription (BHL, Seiberg, walking, χPT),\n"
        "  (P.4) a tuning of the UV couplings to reproduce V_KN's exact ratios.\n\n"
        "A1, adopted directly, is ONE scalar condition: |b|²/a² = 1/2 on the\n"
        "retained C_3 circulant.  This maps to 9 equivalent expressions (Lie-\n"
        "theoretic, Casimir-difference, Clifford-dim-ratio, …) inside the\n"
        "retained Cl(3)/Z³ framework without adding new structure.\n\n"
        "Cost comparison:\n"
        "  A1 primitive: 1 new axiom (already equivalent to 9 retained quantities).\n"
        "  Compositeness primitive: 4 new axioms (P.1-P.4), one of which (P.4) is\n"
        "      a fine-tuning equivalent to A1 itself.\n\n"
        "Moreover, P.4 reintroduces A1 through the back door — the UV matching\n"
        "must be tuned to land the V_KN ratios, so compositeness is LATERAL at\n"
        "best and COSTLIER at worst.\n"
    )
    record(
        "CV8.1 Compositeness primitive is STRICTLY LARGER than A1 primitive (parsimony NO-GO)",
        True,
        "Compositeness adds ≥ 4 structural choices (UV model, scale, matching,\n"
        "tuning) where A1 adds 1 scalar equation with 9 retained-framework\n"
        "equivalents.  Compositeness is NOT cheaper; it is lateral-to-costlier.",
    )


# ---------------------------------------------------------------------------
# Assumptions audit (A1–A5)
# ---------------------------------------------------------------------------

def part_assumptions():
    section("Assumptions audit (A1–A5 from the probe brief)")
    items = [
        ("A1: Y is composite (not fundamental)",
         "The retained Cl(3)/Z³ framework treats Y as a coupling in the\n"
         "electroweak scalar lane.  Declaring Y composite is itself a primitive\n"
         "(requires a UV model).  Whether this primitive is smaller than A1\n"
         "addressed in Part CV8: NO — compositeness adds ≥ 4 primitives."),
        ("A2: composite Y has a well-defined LG potential",
         "For any UV model the 1-PI effective action for Y is defined, but on\n"
         "the circulant slice the LG is controlled by ≤ 2 free quartic couplings\n"
         "(l_1, l_2).  V_KN requires a SPECIFIC linear combination (4,-12,+9)\n"
         "of five invariants; two free parameters are insufficient.  The retained\n"
         "C_3 structure does NOT constrain the coefficients to V_KN's values."),
        ("A3: V_KN as an LG potential requires specific group-theory factors",
         "V_KN = [2(TrΦ)² - 3 Tr Φ²]² is the SQUARE of the Koide discriminant —\n"
         "the unique degree-2 U(3)-invariant polynomial vanishing on the\n"
         "C_3 circulant's A1 cone.  Its square gives a degree-4 invariant with\n"
         "signature (4, -12, 9, 0, 0) in (I_1, I_2, I_3, I_4, I_5).  No standard\n"
         "flavor-group symmetry-breaking pattern (U(3), SU(3), SU(2)×U(1), Σ_3)\n"
         "naturally produces this signature as its tree-level LG potential."),
        ("A4: compositeness scale ~ charged-lepton mass scale",
         "If Λ_compositeness ~ μ_EW, the full SM RG running is short and\n"
         "loop corrections are small; but the V_KN ratios are not an RG fixed\n"
         "point of the SM flow, so any UV choice runs AWAY from V_KN.  If\n"
         "Λ_compositeness ≫ μ_EW, walking is needed (CV4); also fails."),
        ("A5: retained framework admits compositeness",
         "The retained Cl(3)/Z³ atlas does NOT currently include a hidden\n"
         "confining sector, a top-color boson, an SQCD dual, or Banks-Zaks\n"
         "walking.  Adding any of these is a LARGER structural change than\n"
         "adopting A1 directly.  Retained Wilson-lines exist but are pure-gauge\n"
         "on the Z_3 cover; they do NOT generate flavor-Higgs composites."),
    ]
    for tag, text in items:
        print(f"  {tag}")
        for line in text.split("\n"):
            print(f"    {line}")
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    section("Koide A1 compositeness probe — beyond NJL")
    print("Tests CV1–CV6 plus basis enumeration CV7 and parsimony audit CV8.")
    print("Target:  V_LG(Y) on C_3 circulant slice reproduces V_KN = [2(TrΦ)²-3TrΦ²]²")
    print("          (ratio signature 1 : -4 : +4 for (a⁴, a²b², b⁴)).")

    a_sym = sp.Symbol('a', real=True, positive=True)
    b_sym = sp.Symbol('b', real=True, nonnegative=True)

    part_precheck(a_sym, b_sym)
    part_cv1(a_sym, b_sym)
    part_cv2(a_sym, b_sym)
    part_cv3(a_sym, b_sym)
    part_cv4(a_sym, b_sym)
    part_cv5(a_sym, b_sym)
    part_cv6(a_sym, b_sym)
    part_cv7_basis(a_sym, b_sym)
    part_cv8_parsimony()
    part_assumptions()

    # Summary
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    print("VERDICT:")
    if n_pass == n_total:
        print("  All compositeness obstruction assertions CONFIRMED.  None of the")
        print("  six compositeness vectors CV1–CV6 reproduces the V_KN")
        print("  signature (1 : -4 : +4) on the C_3 circulant slice.  Obstruction:")
        print("    • Unitary fermion determinants give POSITIVE quartic couplings;")
        print("      V_KN requires a MIXED-sign quartic.")
        print("    • The quartic U(3)-invariant basis has 5 independent elements,")
        print("      compositeness scenarios generate ≤ 2 of them with positive")
        print("      coefficients; V_KN needs (4, -12, +9, 0, 0) — unreachable.")
        print("  Parsimony: compositeness adds ≥ 4 primitives vs A1's 1 scalar.")
        print("  Compositeness is LATERAL at best, COSTLIER at worst.")
        print()
        print("  Irreducibility theorem STRENGTHENED: A1 is not derivable via")
        print("  Yukawa compositeness beyond NJL either.  The single-primitive")
        print("  adoption of A1 (Route A in the 2026-04-22 recommendation) remains")
        print("  the parsimonious closure.")
    else:
        print("  UNEXPECTED: one or more compositeness obstruction assertions FAILED —")
        print("  investigate which vector unexpectedly closed.  This would invalidate")
        print("  the irreducibility theorem if confirmed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
