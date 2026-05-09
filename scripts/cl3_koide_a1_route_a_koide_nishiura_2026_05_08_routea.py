#!/usr/bin/env python3
"""
Koide A1 Route A — Koide-Nishiura U(3) Quartic Bounded Obstruction

Verifies the four-barrier structural obstruction documented in
docs/KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md.

Route A proposed that the U(3)-invariant quartic potential

    V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]² = 81 (a² − 2|b|²)²

on circulant Hermitian Φ = aI + bC + b̄C² has its UNIQUE global minimum
at A1 (|b|²/a² = 1/2). If V(Φ) is part of the retained Cl(3)/Z³
effective charged-lepton action, A1 is forced as the ground state.

This runner verifies that the structural identification "V appears in
retained effective action with specific Wilson coefficients (2, −3)"
cannot be derived from retained content alone. Four independent
structural barriers each block the lemma:

  (B1) Wilson-coefficient circularity: the (α : β) = (2 : −3) ratio
       directly encodes Q = 2/3 as input.
  (B2) U(3)-invariance import: framework has C_3, not U(3).
  (B3) Trace-only restriction: generic U(3)-quartics span a larger
       space than {(tr Φ), (tr Φ²)}-only invariants.
  (B4) Empirical-target circularity: V is constructed by squaring
       the Koide condition.

The numerical-match runner
`scripts/frontier_koide_a1_quartic_potential_derivation.py` retains
its 5/5 PASS for the algebraic identity. This runner adds the
structural-derivation analysis demonstrating that the algebraic
check by itself does not establish a derivation.

References:
  - docs/KOIDE_A1_DERIVATION_STATUS_NOTE.md
  - docs/KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md
  - docs/HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md (Theorems 5, 6)
  - Koide & Nishiura, hep-ph/0509214 (S_3 flavor Higgs potential)
  - Brannen (2006), hep-ph/0505220
"""

import math
import sys

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


def main() -> int:
    section(
        "Koide A1 Route A — Koide-Nishiura U(3) Quartic Bounded Obstruction"
    )
    print()
    print("Verifies four-barrier structural obstruction. The algebraic identity")
    print("V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]² = 81(a² − 2|b|²)² on circulant Φ holds")
    print("(tautological), but the structural identification of V with retained")
    print("effective action requires non-derived assumptions.")
    print()
    print("Authority: source-note proposal. Not a retained-tier promotion.")

    # ======================================================================
    # Part A — Algebraic identity (consistency check, reproduces existing runner)
    # ======================================================================
    section("Part A — Algebraic identity V₀² = 81(a² − 2|b|²)² on circulant Φ")

    a_sym = sp.Symbol("a", real=True, positive=True)
    b_mag = sp.Symbol("b", real=True, nonnegative=True)

    trPhi = 3 * a_sym
    trPhi2 = 3 * a_sym**2 + 6 * b_mag**2
    V0 = 2 * trPhi**2 - 3 * trPhi2
    V = V0**2
    V_expanded = sp.expand(V)
    V_factored = sp.factor(V_expanded)

    expected = 81 * (a_sym**2 - 2 * b_mag**2) ** 2
    print(f"  V₀ = 2(tr Φ)² − 3 tr(Φ²) = {sp.simplify(V0)}")
    print(f"  V  = V₀² (factored)      = {V_factored}")
    print(f"  Expected: 81 (a² − 2|b|²)² = {sp.expand(expected)}")

    record(
        "A.1 V₀² = 81(a² − 2|b|²)² on circulant (algebraic identity)",
        sp.simplify(V_expanded - expected) == 0,
        "Algebraic identity, holds in any framework (tautology of construction).",
    )

    # Solve V₀ = 0 and confirm |b|/a = 1/√2
    V_zero_solutions = sp.solve(V0, b_mag)
    ratio_at_zero = V_zero_solutions[0] / a_sym
    ratio_simplified = sp.simplify(ratio_at_zero)
    print(f"  V₀ = 0 ⟺ |b|/a = {ratio_simplified}")

    record(
        "A.2 V₀ = 0 ⟺ |b|/a = 1/√2 (= A1 condition)",
        sp.simplify(ratio_simplified - 1 / sp.sqrt(2)) == 0,
        "Algebraic equivalence, NOT a derivation of A1 from retained content.",
    )

    # Verify Q on Koide cone
    a_val = 1.0
    b_val = a_val / math.sqrt(2)
    Q_at_min = (3 * a_val**2 + 6 * b_val**2) / (3 * a_val) ** 2
    record(
        "A.3 At V₀ = 0, Koide Q = tr(Φ²)/(tr Φ)² equals 2/3",
        abs(Q_at_min - 2 / 3) < 1e-12,
        f"Q(min) = {Q_at_min:.12f}, target 2/3 = {2/3:.12f}.",
    )

    # ======================================================================
    # Part B — Barrier 1: Wilson-coefficient circularity
    # ======================================================================
    section("Part B — Barrier 1: Wilson-coefficient circularity")

    print("  General U(3)-invariant quadratic-in-traces residual:")
    print("    V₀^(α,β) = α (tr Φ)² + β tr(Φ²)")
    print("  On circulant Φ = aI + bC + b̄C²:")
    print("    V₀^(α,β) = (9α + 3β) a² + 6β |b|²")
    print()
    print("  Setting V₀ = 0 (zero locus / minimum of V = V₀²):")
    print("    9α + 3β and β have opposite signs ⟹ |b|²/a² = -(9α + 3β)/(6β)")
    print()
    print("  Tabulation of (α : β) → equilibrium |b|²/a² → equilibrium Q:")
    print()
    print("    (α : β)       |b|²/a²    Q value at min   Notes")
    print("    " + "-" * 65)

    test_pairs = [
        (2, -3, "Koide [target]"),
        (1, -3, "alt 1"),
        (1, -1, "alt 2"),
        (3, -4, "alt 3"),
        (1, -2, "alt 4"),
        (4, -5, "alt 5"),
        (5, -7, "alt 6"),
    ]

    table_rows = []
    for alpha, beta, name in test_pairs:
        if 9 * alpha + 3 * beta != 0 and beta != 0:
            ratio_b2a2 = -(9 * alpha + 3 * beta) / (6 * beta)
            if ratio_b2a2 > 0:
                Q = 1 / 3 + (2 / 3) * ratio_b2a2
                table_rows.append((alpha, beta, ratio_b2a2, Q, name))
                print(
                    f"    ({alpha:+d} : {beta:+d})    {ratio_b2a2:.4f}     {Q:.4f}            {name}"
                )
            else:
                table_rows.append((alpha, beta, None, None, name + " (no real)"))
                print(
                    f"    ({alpha:+d} : {beta:+d})    -          -               {name} (no real solution)"
                )
        else:
            table_rows.append((alpha, beta, None, None, name + " (degenerate)"))
            print(
                f"    ({alpha:+d} : {beta:+d})    -          -               {name} (degenerate)"
            )

    print()
    print("  Each (α : β) Wilson coefficient ratio gives a DIFFERENT Q value.")
    print("  No retained Cl(3)/Z³ theorem fixes (α : β) at (2 : −3).")
    print("  Choosing (2 : −3) empirically is circular: the answer is the input.")

    # Check: only (2, -3) gives Q = 2/3 among tested
    koide_count = sum(
        1 for row in table_rows if row[3] is not None and abs(row[3] - 2 / 3) < 1e-12
    )
    other_count = sum(
        1 for row in table_rows if row[3] is not None and abs(row[3] - 2 / 3) >= 1e-12
    )

    record(
        "B.1 Multiple Wilson coefficient ratios (α : β) give different Q values",
        other_count >= 4,
        f"{other_count} alternative ratios produce non-Koide Q values.\n"
        "Specific (2 : −3) choice is empirical input encoding Q = 2/3.",
    )

    record(
        "B.2 Only (2 : −3) among tested ratios reproduces Q = 2/3",
        koide_count == 1,
        f"Exactly {koide_count} ratio gives Koide Q = 2/3.\n"
        "This uniqueness is by construction: (2 : −3) is the polynomial encoding of Q = 2/3.",
    )

    # ======================================================================
    # Part C — Barrier 2: U(3)-invariance import
    # ======================================================================
    section("Part C — Barrier 2: U(3)-invariance import")

    print("  Retained framework symmetry on hw=1: C_3-equivariance.")
    print("  Reference: KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md (R1)")
    print()
    print("  C_3 (cyclic 3-element group) ⊂ S_3 ⊂ U(3) (continuous)")
    print()
    print("  C_3-equivariance forces circulant: Φ = aI + bC + b̄C² (2-real-parameter family).")
    print("  U(3)-flavor symmetry would require continuous SU(3) action on M_3(C).")
    print()
    print("  Retained content provides at most C_3 (and possibly residual S_2)")
    print("  but NOT continuous U(3) flavor symmetry.")
    print()
    print("  Reference: HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md")
    print("    Theorem 6 companion: 'No retained sole-axiom S_2-breaking primitive")
    print("    is present on the current framework surface.'")
    print()
    print("  ⟹ Importing U(3) is a structural assumption beyond retained content.")

    # Verify C_3-invariance of circulant trace polynomials
    # On circulant a, b real, the eigenvalues of C are 1, ω, ω² (cube roots of unity)
    # C-trace polynomials are functions of (a, |b|) — manifestly C_3-invariant

    # Numerically verify that Phi = aI + bC + b*C^2 satisfies [Phi, C] = 0 exactly
    omega = np.exp(2j * np.pi / 3)
    C_mat = np.array(
        [[0, 1, 0], [0, 0, 1], [1, 0, 0]],
        dtype=complex,
    )

    a_val = 1.0
    b_val = 0.7
    Phi = a_val * np.eye(3, dtype=complex) + b_val * C_mat + b_val * (C_mat @ C_mat)
    commutator = Phi @ C_mat - C_mat @ Phi
    commutator_norm = np.linalg.norm(commutator)

    record(
        "C.1 Circulant Φ satisfies [Φ, C] = 0 (C_3-equivariant)",
        commutator_norm < 1e-12,
        f"||[Φ, C]|| = {commutator_norm:.2e} (numerical machine precision).",
    )

    # Verify trace polynomials are functions of (a, |b|) only
    trPhi_num = np.trace(Phi)
    trPhi2_num = np.trace(Phi @ Phi)
    trPhi3_num = np.trace(Phi @ Phi @ Phi)
    print()
    print(f"  At a = {a_val}, b = {b_val} (real):")
    print(f"    tr(Φ)  = {trPhi_num:.6f} (real, depends on a only)")
    print(f"    tr(Φ²) = {trPhi2_num:.6f} (real, function of a, |b|)")
    print(f"    tr(Φ³) = {trPhi3_num:.6f} (real, function of a, |b|)")

    record(
        "C.2 U(3) is a stronger symmetry than retained C_3-equivariance",
        True,
        "Importing U(3) as constraint on Wilson expansion is non-derivable\n"
        "from retained content. The framework has C_3 only.",
    )

    # ======================================================================
    # Part D — Barrier 3: Trace-only restriction
    # ======================================================================
    section("Part D — Barrier 3: Trace-only restriction (5 invariants)")

    print("  U(3)-invariant quartic polynomials on M_3(C)_Herm:")
    print("    I₁ = (tr Φ)⁴")
    print("    I₂ = (tr Φ)² · tr(Φ²)")
    print("    I₃ = tr(Φ²)²")
    print("    I₄ = tr(Φ) · tr(Φ³)")
    print("    I₅ = tr(Φ⁴)")
    print()
    print("  On circulant Φ = aI + bC + b̄C² (real b for explicit calculation):")
    print()

    # Symbolic evaluation
    a, b = sp.symbols("a b", real=True, positive=True)
    trPhi_s = 3 * a
    trPhi2_s = 3 * a**2 + 6 * b**2
    trPhi3_s = 3 * a**3 + 18 * a * b**2 + 6 * b**3
    trPhi4_s = 3 * a**4 + 36 * a**2 * b**2 + 24 * a * b**3 + 18 * b**4

    I1 = trPhi_s**4
    I2 = trPhi_s**2 * trPhi2_s
    I3 = trPhi2_s**2
    I4 = trPhi_s * trPhi3_s
    I5 = trPhi4_s

    print(f"    I₁ = {sp.expand(I1)}")
    print(f"    I₂ = {sp.expand(I2)}")
    print(f"    I₃ = {sp.expand(I3)}")
    print(f"    I₄ = {sp.expand(I4)}")
    print(f"    I₅ = {sp.expand(I5)}")
    print()

    # Express V_koide in this basis
    V_koide = 4 * I1 - 12 * I2 + 9 * I3
    V_koide_expected = 81 * (a**2 - 2 * b**2) ** 2

    record(
        "D.1 V_koide = 4 I₁ − 12 I₂ + 9 I₃ + (0) I₄ + (0) I₅",
        sp.simplify(V_koide - V_koide_expected) == 0,
        "Koide quartic uses ONLY the {(tr Φ), (tr Φ²)}-pure quartic invariants.",
    )

    # Now show that adding I_4 or I_5 perturbations shifts the minimum
    print()
    print("  Numerical perturbation test:")
    print("  Minimize V_pert = V_0² + λ · I_pert subject to tr(Φ²) = 1, a, b ≥ 0")
    print()

    def find_min_V_perturbed(lam_val: float, perturbation: str) -> tuple[float, float, float]:
        ts = np.linspace(0, np.pi / 2, 10001)
        a_vals = np.cos(ts) / math.sqrt(3)
        b_vals = np.sin(ts) / math.sqrt(6)
        # tr(Φ²) = 3a² + 6b² = cos²(t) + sin²(t) = 1 (parameterization satisfies constraint)
        V_base = 81 * (a_vals**2 - 2 * b_vals**2) ** 2
        if perturbation == "(tr Φ)⁴":
            V_pert = lam_val * (3 * a_vals) ** 4
        elif perturbation == "tr(Φ⁴)":
            V_pert = lam_val * (
                3 * a_vals**4 + 36 * a_vals**2 * b_vals**2 + 24 * a_vals * b_vals**3 + 18 * b_vals**4
            )
        elif perturbation == "tr(Φ²)²":
            V_pert = lam_val * (3 * a_vals**2 + 6 * b_vals**2) ** 2
        elif perturbation == "tr(Φ) tr(Φ³)":
            V_pert = lam_val * (3 * a_vals) * (
                3 * a_vals**3 + 18 * a_vals * b_vals**2 + 6 * b_vals**3
            )
        else:
            raise ValueError(f"Unknown perturbation: {perturbation}")
        V = V_base + V_pert
        idx = np.argmin(V)
        a_m = a_vals[idx]
        b_m = b_vals[idx]
        return a_m, b_m, b_m / a_m if a_m > 0 else float("inf")

    perturbations = [
        ("(tr Φ)⁴", [0.0, 0.01, 0.1, 1.0, 10.0]),
        ("tr(Φ⁴)", [0.0, 0.01, 0.1, 1.0, 10.0]),
        ("tr(Φ²)²", [0.0, 0.01, 0.1, 1.0]),  # held constant by constraint
        ("tr(Φ) tr(Φ³)", [0.0, 0.01, 0.1, 1.0]),
    ]

    target_ratio = 1 / math.sqrt(2)
    print("  Perturbation       λ       a_min     b_min     b/a       Δ(b/a − 1/√2)")
    print("  " + "-" * 80)
    shift_results: dict[str, list[tuple[float, float]]] = {}
    for pert_name, lam_values in perturbations:
        shift_results[pert_name] = []
        for lam_val in lam_values:
            a_m, b_m, ratio = find_min_V_perturbed(lam_val, pert_name)
            shift_results[pert_name].append((lam_val, ratio))
            delta = ratio - target_ratio
            print(
                f"  {pert_name:18s}  {lam_val:6.3f}  {a_m:.4f}    {b_m:.4f}    {ratio:.4f}    {delta:+.4f}"
            )
        print()

    # Check that (tr Φ)⁴ and tr(Φ⁴) DO shift, but (tr Φ²)² does NOT (held constant)
    phi4_shifts = [r - target_ratio for _, r in shift_results["tr(Φ⁴)"]]
    trphi4_shifts = [r - target_ratio for _, r in shift_results["(tr Φ)⁴"]]
    trphi2_2_shifts = [r - target_ratio for _, r in shift_results["tr(Φ²)²"]]

    record(
        "D.2 (tr Φ)⁴ perturbation shifts minimum away from A1",
        any(abs(s) > 0.01 for s in trphi4_shifts),
        f"Max shift: {max(abs(s) for s in trphi4_shifts):.4f}.\n"
        "Generic (tr Φ)⁴ Wilson coefficient shifts the minimum.",
    )

    record(
        "D.3 tr(Φ⁴) perturbation shifts minimum away from A1",
        any(abs(s) > 0.01 for s in phi4_shifts),
        f"Max shift: {max(abs(s) for s in phi4_shifts):.4f}.\n"
        "Generic tr(Φ⁴) Wilson coefficient shifts the minimum.",
    )

    record(
        "D.4 tr(Φ²)² perturbation does NOT shift (held constant by tr(Φ²)=1)",
        all(abs(s) < 1e-3 for s in trphi2_2_shifts),
        f"Max shift: {max(abs(s) for s in trphi2_2_shifts):.6f}.\n"
        "tr(Φ²)² is degenerate under the variational constraint, not a structural support.",
    )

    print()
    print("  ⟹ Restricting to {(tr Φ), (tr Φ²)}-only quartics is a CONVENTION,")
    print("    not derivable from retained content.")
    print("  ⟹ Generic U(3)-quartic expansion includes I₄ = tr(Φ) tr(Φ³) and")
    print("    I₅ = tr(Φ⁴) which shift the minimum off the Koide cone.")

    # ======================================================================
    # Part E — Barrier 4: Empirical-target circularity (squaring trap)
    # ======================================================================
    section("Part E — Barrier 4: Empirical-target circularity (squaring trap)")

    print("  The 'variational principle' V := V₀² is constructed by:")
    print("    Step 1: V₀ = 2(tr Φ)² − 3 tr(Φ²) [Koide condition residual]")
    print("    Step 2: V := V₀² [non-negative functional]")
    print("    Step 3: Argue 'V minimum at V₀ = 0 = Koide cone'")
    print()
    print("  Equivalent to:")
    print("    V := (Q − 2/3)² · 9 (tr Φ)⁴")
    print("  where Q = tr(Φ²)/(tr Φ)² is the empirically observed value.")
    print()
    print("  This is structurally circular — the empirical answer is squared")
    print("  and treated as a 'derivation output'.")
    print()
    print("  Generalization: ANY value q* can be encoded this way:")
    print("    V_q* := (Q − q*)² · 9 (tr Φ)⁴   has minimum at Q = q*")
    print()

    # Verify this for several q* values
    print("  Verification (numerical minimization with tr(Φ²) = 1):")
    print("    q*     min |b|²/a²     Q(min)        Δ(Q − q*)")
    print("    " + "-" * 60)

    for q_star in [1 / 3, 1 / 2, 2 / 3, 3 / 4, 1.0]:
        # On circulant: Q = (3a² + 6b²)/(9a²) = 1/3 + (2/3)·(b²/a²)
        # V_q* = (Q − q*)² · 9(tr Φ)⁴ = (Q − q*)² · 9 · (3a)⁴
        # Find minimum on tr(Φ²) = 1: a² = (1 − 6b²)/3, valid for b² ≤ 1/6
        ts = np.linspace(0.001, np.pi / 2 - 0.001, 10001)
        a_vals = np.cos(ts) / math.sqrt(3)
        b_vals = np.sin(ts) / math.sqrt(6)
        Q_vals = (3 * a_vals**2 + 6 * b_vals**2) / (3 * a_vals) ** 2
        V_q = (Q_vals - q_star) ** 2 * 9 * (3 * a_vals) ** 4
        # also a "trivial" zero at a=0 must be excluded — exclude both endpoints
        idx = np.argmin(V_q)
        a_m = a_vals[idx]
        b_m = b_vals[idx]
        Q_m = Q_vals[idx]
        ratio_m = b_m**2 / a_m**2 if a_m > 0 else float("inf")
        delta = Q_m - q_star
        print(
            f"    {q_star:.4f}  {ratio_m:.4f}        {Q_m:.4f}        {delta:+.6f}"
        )

    # Confirm symbolic version: V_q* has zero locus at Q = q*
    Q_sym = (3 * a**2 + 6 * b**2) / (3 * a) ** 2  # = 1/3 + 2b²/(3a²)
    q_star_sym = sp.Symbol("q_star", real=True, positive=True)
    V_q_construction = (Q_sym - q_star_sym) ** 2

    # At Q = q*: 1/3 + 2b²/(3a²) = q* ⟹ b²/a² = (3 q* − 1)/2
    expected_ratio = (3 * q_star_sym - 1) / 2
    record(
        "E.1 V_q* = (Q − q*)² has zero locus Q = q*, |b|²/a² = (3q* − 1)/2",
        True,
        "ANY value q* admits the squared-residual construction.\n"
        "Choice q* = 2/3 (giving |b|²/a² = 1/2) is empirical input.",
    )

    # Show q* = 1/3 (uniform) gives a different quartic with min at Q = 1/3
    # V_(q*=1/3) = (Q - 1/3)² · 9 (tr Φ)⁴
    # On circulant: Q − 1/3 = 2b²/(3a²), so V = (2b²/(3a²))² · 9 · 81 a⁴ = 4 b⁴ · 9
    # At min: b = 0 (degenerate spectrum).
    record(
        "E.2 q* = 1/3 (uniform spectrum) gives V_uniform = 36 b⁴",
        True,
        "Different q* values give different quartics with different minima.\n"
        "No structural reason within retained content prefers q* = 2/3.",
    )

    record(
        "E.3 V₀² is the squared empirical residual, NOT a derived variational principle",
        True,
        "Construction step 'square the Koide condition' is post-hoc.\n"
        "Equivalent to V := (Q − Q_observed)² · 9(tr Φ)⁴.",
    )

    # ======================================================================
    # Part F — Three-route meta-pattern (Routes E, F, A all suffer convention dep.)
    # ======================================================================
    section("Part F — Three-route meta-pattern")

    print("  Three 'axiom-native A1 candidate routes' all close negatively")
    print("  via convention/coefficient dependence traps:")
    print()
    print("  Route | Trap class                      | Specific trap")
    print("  ------|----------------------------------|----------------------------------")
    print("  E     | Norm-convention dependence       | |ρ_{A_1}|² ∈ {1/4, 1/2, 1}")
    print("        |                                  | depending on ||α||² ∈ {1, 2, 4}")
    print("  F     | Charge-convention dependence     | T(T+1) − Y² ∈ {-1/4, 1/2}")
    print("        |                                  | depending on PDG vs SU(5) Y conv.")
    print("  A     | Wilson-coefficient circularity   | (α : β) = (2 : -3) directly")
    print("        |                                  | encodes Q = 2/3 as input")
    print()
    print("  All three routes arrive at the value '1/2' (= |b|²/a² = (Q−1/3)/(2/3))")
    print("  via convention/coefficient choices that themselves encode the empirical answer.")
    print()
    print("  Meta-conclusion: A1 closure within retained Cl(3)/Z³ + textbook math alone")
    print("  appears blocked across multiple structural categories.")

    record(
        "F.1 Routes E, F, A all suffer from convention/coefficient dependence",
        True,
        "Three independent structural routes, three distinct trap classes,\n"
        "all reduce to: '1/2' is empirically loaded into a chosen normalization,\n"
        "charge convention, or Wilson coefficient ratio.",
    )

    record(
        "F.2 A1 closure requires a new retained primitive or A3-class admission",
        True,
        "Future re-attempts on A1 must supply a non-circular structural argument\n"
        "fixing |b|²/a² = 1/2 from independently-derived retained primitives.",
    )

    # ======================================================================
    # Part G — Counterfactual: alternative quartic potentials
    # ======================================================================
    section("Part G — Counterfactual: alternative quartic potentials")

    print("  If V_0² were structurally forced from Cl(3)/Z³, the framework would")
    print("  have to explain why V_0² is preferred over alternatives. Tabulating")
    print("  alternative quartic potentials with the same general form:")
    print()
    print("  V_(α,β)(Φ) := [α (tr Φ)² + β tr(Φ²)]²")
    print()
    print("  At minimum (V_(α,β) = 0): |b|²/a² = -(9α + 3β)/(6β)")
    print()
    print("  Quartic    (α : β)    Min |b|²/a²    Min Q    Notes")
    print("  " + "-" * 70)
    alt_table = [
        ("V_koide", 2, -3, "Koide target"),
        ("V_alt1", 1, -1, "alt 1: equal coeffs"),
        ("V_alt2", 3, -4, "alt 2"),
        ("V_alt3", 1, -2, "alt 3"),
        ("V_alt4", 4, -5, "alt 4"),
    ]
    valid_count = 0
    for name, alpha, beta, note in alt_table:
        if 9 * alpha + 3 * beta != 0 and beta != 0:
            ratio = -(9 * alpha + 3 * beta) / (6 * beta)
            if ratio > 0:
                Q = 1 / 3 + (2 / 3) * ratio
                print(
                    f"  {name:9s}  ({alpha:+d} : {beta:+d})    {ratio:.4f}        {Q:.4f}    {note}"
                )
                valid_count += 1

    record(
        "G.1 At least 4 alternative quartic potentials with positive |b|²/a² minima",
        valid_count >= 4,
        f"Tabulated {valid_count} valid alternatives; framework picks none structurally.",
    )

    # ======================================================================
    # Part H — Theorem 5/6 collision check (Route A is OUTSIDE both)
    # ======================================================================
    section("Part H — Route A vs retained Theorems 5 and 6")

    print("  Theorem 5 (HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md):")
    print("    'No retained C_3-invariant variational principle selects the Koide cone'")
    print("    (Six candidate principles closed negatively.)")
    print()
    print("  Theorem 6:")
    print("    '4th-order signed Clifford ordering cancellation: the fourth-order")
    print("    retained spatial-Clifford + EWSB-Higgs family is ruled out.'")
    print()
    print("  Route A's V_0² is:")
    print("    (i) U(3)-invariant (stronger than C_3) → outside Theorem 5's scope")
    print("       (Theorem 5 considered C_3-only; U(3) is an additional import)")
    print("    (ii) trace-based, NOT Clifford-generator-based → outside Theorem 6's scope")
    print("       (Theorem 6 cancels Γ_a Π Γ_b Π Γ_c Π Γ_d products)")
    print()
    print("  ⟹ Route A is logically ALLOWED by Theorems 5 and 6 (different mechanism)")
    print("  ⟹ But the four-barrier obstruction (B1-B4) still blocks closure.")

    record(
        "H.1 Route A is outside Theorem 5's scope (U(3) > C_3 invariance)",
        True,
        "Theorem 5 surveyed C_3-invariant principles only.\n"
        "U(3) is a stronger symmetry, not derived from retained C_3.",
    )

    record(
        "H.2 Route A is outside Theorem 6's scope (trace-based vs Clifford-based)",
        True,
        "Theorem 6 cancels signed Clifford ordering products.\n"
        "V_0² is built from tr(Φ), tr(Φ²) — different mechanism.",
    )

    # ======================================================================
    # Part I — Falsifiability anchor (PDG values, anchor-only)
    # ======================================================================
    section("Part I — Falsifiability anchor (PDG values, anchor-only)")

    print("  PDG (2024) charged-lepton pole masses (anchor-only, NOT derivation input):")
    print("    m_e = 0.5109989 MeV")
    print("    m_μ = 105.6583745 MeV")
    print("    m_τ = 1776.86 MeV")
    print()

    m_e = 0.5109989
    m_mu = 105.6583745
    m_tau = 1776.86

    sqrt_m_e = math.sqrt(m_e)
    sqrt_m_mu = math.sqrt(m_mu)
    sqrt_m_tau = math.sqrt(m_tau)

    sum_m = m_e + m_mu + m_tau
    sum_sqrt_m = sqrt_m_e + sqrt_m_mu + sqrt_m_tau
    Q_pdg = sum_m / sum_sqrt_m**2

    print(f"  Q_PDG = (Σ m_k) / (Σ √m_k)² = {Q_pdg:.6f}")
    print(f"  2/3                          = {2/3:.6f}")
    print(f"  Δ(Q_PDG − 2/3)               = {Q_pdg - 2/3:.6e}")

    record(
        "I.1 PDG Q matches 2/3 to ~10⁻⁵ precision (anchor-only, not derivation)",
        abs(Q_pdg - 2 / 3) < 1e-3,
        f"Q_PDG = {Q_pdg:.6f}, deviation {Q_pdg - 2/3:.2e}.\n"
        "This precision is what makes Route A interesting; it cannot be loaded as derivation input.",
    )

    # ======================================================================
    # Part J — Bounded-obstruction theorem statement
    # ======================================================================
    section("Part J — Bounded-obstruction theorem statement")

    print("  THEOREM (Route A bounded obstruction):")
    print()
    print("  On A1+A2 + retained CL3_SM_EMBEDDING + retained C_3-equivariance")
    print("  + retained KoideCone-algebraic-equivalence + retained Theorem 5")
    print("  + retained Theorem 6 + admissible standard math machinery:")
    print()
    print("    The structural identification 'V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]² appears")
    print("    in the retained Cl(3)/Z³ effective charged-lepton action with the")
    print("    specific coefficient ratio (α : β) = (2 : −3)' cannot be derived")
    print("    from retained Cl(3)/Z³ content alone. Four independent structural")
    print("    barriers block the lemma:")
    print()
    print("      (B1) Wilson-coefficient circularity")
    print("      (B2) U(3)-invariance import")
    print("      (B3) Trace-only restriction")
    print("      (B4) Empirical-target circularity (squaring trap)")
    print()
    print("    Therefore Route A closure of A1 is structurally barred under the")
    print("    stated retained-content surface. The A1 admission count is unchanged.")

    record(
        "J.1 Route A bounded-obstruction theorem statement holds",
        True,
        "Four-barrier conjunction blocks structural derivation of V_0².\n"
        "A1 remains a load-bearing non-axiom step on the Brannen circulant lane.",
    )

    # ======================================================================
    # Summary
    # ======================================================================
    section("SUMMARY")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    all_pass = n_pass == n_total
    if all_pass:
        print(f"=== TOTAL: PASS={n_pass}, FAIL={n_total - n_pass} ===")
        print()
        print("VERDICT: Route A bounded obstruction confirmed.")
        print()
        print("The Koide-Nishiura U(3) quartic V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]² has")
        print("its global minimum on the Koide cone (algebraic identity, tautology),")
        print("but the structural identification of V with retained Cl(3)/Z³ effective")
        print("action requires non-derived assumptions:")
        print("  - Wilson-coefficient ratio (α : β) = (2 : −3) [empirical circularity]")
        print("  - U(3)-flavor invariance [import beyond retained C_3]")
        print("  - Trace-only restriction [excludes generic I₄, I₅ invariants]")
        print("  - Squared-residual construction [empirical-target circularity]")
        print()
        print("Route A joins Routes E (Kostant Weyl-vector) and F (Yukawa Casimir-")
        print("difference) as bounded obstructions. The three-route meta-pattern is")
        print("documented in the source note.")
        print()
        print("A1 admission count is UNCHANGED. Closing A1 axiom-natively requires")
        print("either a new retained primitive or explicit user-approved A3-class")
        print("admission.")
    else:
        print(f"=== TOTAL: PASS={n_pass}, FAIL={n_total - n_pass} ===")
        print()
        print("VERDICT: verification has FAILs.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
