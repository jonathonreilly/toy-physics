#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for the charged-lepton Koide-cone
narrow theorem note
`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-10.md`.

The parent narrow note's load-bearing content is the algebraic equivalence
that, on any positive 3-vector v = (v_1, v_2, v_3) decomposed under the
unitary C_3 = Z/3Z character Fourier transform, the Koide invariant

  Q(v) := (v_1^2 + v_2^2 + v_3^2) / (v_1 + v_2 + v_3)^2

satisfies

  Q(v) = 2/3   <=>   a_0^2 = 2 |z|^2                                  (P1)

where a_0 = (v_1 + v_2 + v_3)/sqrt(3) and z = (v_1 + omegabar v_2 +
omega v_3)/sqrt(3), omega = exp(2 pi i / 3).

This Pattern A narrow runner adds a sympy-based exact-symbolic
verification:

  (a) treats (v_1, v_2, v_3) as free positive real symbols;
  (b) constructs the C_3-character components (a_0, z) via the unitary
      discrete Fourier transform on Z/3Z;
  (c) verifies Plancherel/Parseval (E1), the linear-sum identity (E3),
      and the closed form (E4) for Q(v) parametrically;
  (d) verifies the forward and reverse directions of (P1) by direct
      symbolic substitution;
  (e) verifies the geometric corollary cos^2(angle(v, (1,1,1))) = 1/2
      reduces to the same condition;
  (f) numerical FP cross-check at three independent positive-vector
      samples;
  (g) counterfactual: at Q = 1/3 the equivalence fails (the cone
      equation no longer reads a_0^2 = 2 |z|^2).

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the parent's
load-bearing class-(A) algebra holds at exact symbolic precision over
abstract positive 3-vectors. The narrow theorem has zero ledger
dependencies; the discrete Fourier transform on C_3 = Z/3Z is a
universal property of finite abelian groups.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import (
        Rational,
        Symbol,
        exp,
        expand,
        I,
        pi,
        sqrt,
        simplify,
        symbols,
        conjugate,
        re,
        im,
        nsimplify,
        Abs,
    )
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-10")
    print("Goal: sympy-symbolic verification of Q = 2/3 <=> a_0^2 = 2|z|^2")
    print("under the C_3 character Fourier transform on positive 3-vectors")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------

    v1, v2, v3 = symbols("v1 v2 v3", positive=True, real=True)
    omega = exp(2 * pi * I / 3)  # primitive cube root of unity
    omegabar = exp(-2 * pi * I / 3)

    # Cited C_3 character basis (unitary discrete Fourier transform):
    e_plus = sympy.Matrix([1, 1, 1]) / sqrt(3)
    e_omega = sympy.Matrix([1, omega, omega**2]) / sqrt(3)
    e_omega2 = sympy.Matrix([1, omega**2, omega]) / sqrt(3)

    v = sympy.Matrix([v1, v2, v3])

    # (D2) a_0 = sum / sqrt(3)
    a_0 = (v1 + v2 + v3) / sqrt(3)

    # (D3) z = (v_1 + omegabar v_2 + omega v_3) / sqrt(3)
    z = (v1 + omegabar * v2 + omega * v3) / sqrt(3)

    # |z|^2 = z * conjugate(z) (since z is complex)
    z_abs_sq_raw = simplify(expand(z * conjugate(z)))
    # On real (v1, v2, v3), conjugate(z) = (v1 + omega v2 + omegabar v3)/sqrt(3) = zbar.
    # We can verify |z|^2 reduces to a real polynomial in (v1, v2, v3).
    z_abs_sq = simplify(sympy.re(z_abs_sq_raw) + 0)  # forced real

    print(f"  symbolic v = ({v1}, {v2}, {v3})")
    print(f"  a_0 = {a_0}")
    print(f"  z   = {z}")
    print(f"  |z|^2 (simplified) = {z_abs_sq}")

    # Expected expansion of |z|^2:
    # |z|^2 = (1/3) [v1^2 + v2^2 + v3^2 - (v1 v2 + v2 v3 + v3 v1)]
    z_abs_sq_target = (
        Rational(1, 3) * (v1**2 + v2**2 + v3**2 - (v1 * v2 + v2 * v3 + v3 * v1))
    )
    check(
        "|z|^2 reduces to (1/3)(v1^2+v2^2+v3^2 - (v1 v2 + v2 v3 + v3 v1))",
        simplify(z_abs_sq - z_abs_sq_target) == 0,
        detail=f"diff = {simplify(z_abs_sq - z_abs_sq_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 1: Plancherel/Parseval (E1): |v|^2 = a_0^2 + 2 |z|^2")
    # ---------------------------------------------------------------------
    v_norm_sq = v1**2 + v2**2 + v3**2
    E1_diff = simplify(v_norm_sq - (a_0**2 + 2 * z_abs_sq_target))
    check(
        "(E1) Plancherel: v1^2 + v2^2 + v3^2 - (a_0^2 + 2|z|^2) reduces to 0",
        E1_diff == 0,
        detail=f"diff = {E1_diff}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: linear-sum identity (E3): (v_1 + v_2 + v_3)^2 = 3 a_0^2")
    # ---------------------------------------------------------------------
    sum_sq = (v1 + v2 + v3) ** 2
    E3_diff = simplify(sum_sq - 3 * a_0**2)
    check(
        "(E3) (v_1 + v_2 + v_3)^2 - 3 a_0^2 reduces to 0",
        E3_diff == 0,
        detail=f"diff = {E3_diff}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: closed form (E4): Q(v) = (a_0^2 + 2|z|^2) / (3 a_0^2)")
    # ---------------------------------------------------------------------
    Q_v = v_norm_sq / sum_sq
    E4_target = (a_0**2 + 2 * z_abs_sq_target) / (3 * a_0**2)
    E4_diff = simplify(Q_v - E4_target)
    check(
        "(E4) Q(v) - (a_0^2 + 2|z|^2) / (3 a_0^2) reduces to 0 parametrically",
        E4_diff == 0,
        detail=f"diff = {E4_diff}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: forward direction of (P1): Q = 2/3 => a_0^2 = 2|z|^2")
    # ---------------------------------------------------------------------
    # Substitute Q = 2/3 into E4 form and solve.
    # (a_0^2 + 2|z|^2) / (3 a_0^2) = 2/3
    # => a_0^2 + 2|z|^2 = 2 a_0^2
    # => a_0^2 = 2|z|^2.
    A, B = symbols("A B", positive=True, real=True)  # A = a_0^2, B = |z|^2
    eq_forward = (A + 2 * B) / (3 * A) - Rational(2, 3)
    # Multiply through; expected reduction A = 2 B.
    sols_forward = sympy.solve(eq_forward, A)
    pos_forward_ok = len(sols_forward) == 1 and simplify(sols_forward[0] - 2 * B) == 0
    check(
        "forward (P1): solving (a_0^2 + 2|z|^2)/(3 a_0^2) = 2/3 gives a_0^2 = 2|z|^2",
        pos_forward_ok,
        detail=f"sympy.solve returned a_0^2 ∈ {sols_forward}, expected {{2*B}}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: reverse direction of (P1): a_0^2 = 2|z|^2 => Q = 2/3")
    # ---------------------------------------------------------------------
    Q_under_cone = simplify(((A + 2 * B) / (3 * A)).subs(A, 2 * B))
    expected_Q = Rational(2, 3)
    check(
        "reverse (P1): substituting a_0^2 = 2|z|^2 into Q gives Q = 2/3",
        simplify(Q_under_cone - expected_Q) == 0,
        detail=f"Q under a_0^2 = 2|z|^2 = {Q_under_cone}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: full parametric forward direction in (v1, v2, v3)")
    # ---------------------------------------------------------------------
    # Substitute Q(v) = v_norm_sq / sum_sq with C_3 character forms.
    # Q(v) = 2/3 algebraically equivalent to v_norm_sq * 3 = 2 sum_sq,
    # i.e. 3(v1^2+v2^2+v3^2) - 2(v1+v2+v3)^2 = 0.
    Koide_lhs = 3 * v_norm_sq - 2 * sum_sq
    # Expanded: 3 v1^2+3 v2^2+3 v3^2 - 2(v1^2+v2^2+v3^2+2 v1 v2+2 v2 v3+2 v3 v1)
    # = v1^2+v2^2+v3^2 - 4 v1 v2 - 4 v2 v3 - 4 v3 v1
    Koide_lhs_expanded = expand(Koide_lhs)
    print(f"  Koide condition (Q=2/3) in (v1,v2,v3): {Koide_lhs_expanded} = 0")

    # Substitute the character form: |v|^2 - 2 |z|^2 = a_0^2 - 0 means
    # a_0^2 = 2|z|^2 should rewrite Koide_lhs to 0.
    # We use (E1): v_norm_sq = a_0^2 + 2|z|^2; (E3): sum_sq = 3 a_0^2.
    # So Koide_lhs = 3 (a_0^2 + 2|z|^2) - 2 (3 a_0^2) = 3 a_0^2 + 6|z|^2 - 6 a_0^2
    #              = -3 a_0^2 + 6|z|^2 = 3 (2|z|^2 - a_0^2).
    # Hence Koide_lhs = 0 <=> a_0^2 = 2|z|^2.
    Koide_lhs_via_chars = simplify(
        3 * (a_0**2 + 2 * z_abs_sq_target) - 2 * (3 * a_0**2)
    )
    target_chars = 3 * (2 * z_abs_sq_target - a_0**2)
    check(
        "Koide LHS in C_3 chars: 3(a_0^2 + 2|z|^2) - 2(3 a_0^2) = 3 (2|z|^2 - a_0^2)",
        simplify(Koide_lhs_via_chars - target_chars) == 0,
        detail=f"diff = {simplify(Koide_lhs_via_chars - target_chars)}",
    )

    # The two-way equivalence:
    check(
        "parametric (P1): Koide LHS = 0 <=> 2|z|^2 - a_0^2 = 0 (zero iff char cone)",
        simplify(Koide_lhs_expanded - target_chars) == 0,
        detail=f"(Koide_lhs - target_chars) = {simplify(Koide_lhs_expanded - target_chars)}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: geometric corollary - 45-degree angle from diagonal")
    # ---------------------------------------------------------------------
    # cos^2(angle(v, (1,1,1))) = (v . (1,1,1))^2 / (|v|^2 * 3)
    #                         = (v_1+v_2+v_3)^2 / (3 |v|^2)
    # In terms of abstract Q := |v|^2 / sum_sq, cos^2 = sum_sq / (3 |v|^2) = 1/(3 Q).
    # Verify symbolically via the relation cos_sq * 3 Q = 1, then substitute Q = 2/3.
    Q_sym = Symbol("Q_sym", positive=True, real=True)
    # Algebraic relation: cos^2 = 1 / (3 Q).
    cos_sq_in_Q = 1 / (3 * Q_sym)
    cos_sq_at_Q_two_thirds = simplify(cos_sq_in_Q.subs(Q_sym, Rational(2, 3)))
    expected_cos_sq = Rational(1, 2)
    check(
        "geometric corollary: at Q = 2/3, cos^2(angle(v, (1,1,1))) = 1/2",
        simplify(cos_sq_at_Q_two_thirds - expected_cos_sq) == 0,
        detail=f"cos^2 at Q=2/3 = {cos_sq_at_Q_two_thirds}",
    )
    # Verify the underlying identity cos^2 * Q * 3 = 1 in (v1, v2, v3):
    cos_sq_vars = sum_sq / (3 * v_norm_sq)
    Q_vars = v_norm_sq / sum_sq
    relation = simplify(cos_sq_vars * Q_vars * 3 - 1)
    check(
        "underlying identity: cos^2(angle) * Q * 3 = 1 parametric in (v1, v2, v3)",
        relation == 0,
        detail=f"diff = {relation}",
    )

    # sigma(v) = a_0^2 / (a_0^2 + 2|z|^2) = a_0^2 / |v|^2 (E1)
    # = (sum/sqrt(3))^2 / sum_sq * (sum_sq / |v|^2) -- redo:
    # = a_0^2 / (a_0^2 + 2|z|^2). At a_0^2 = 2|z|^2, sigma = 2|z|^2/(2|z|^2+2|z|^2) = 1/2.
    sigma_at_cone = simplify(A / (A + 2 * B)).subs(A, 2 * B)
    expected_sigma = Rational(1, 2)
    check(
        "geometric corollary: at a_0^2 = 2|z|^2, sigma = 1/2",
        simplify(sigma_at_cone - expected_sigma) == 0,
        detail=f"sigma at cone = {sigma_at_cone}",
    )

    # cos^2 = sigma (since cos^2 = sum_sq/(3 |v|^2) = 3 a_0^2 / (3 |v|^2) = a_0^2/|v|^2)
    check(
        "identity: cos^2(angle(v, (1,1,1))) = sigma(v) = a_0^2 / |v|^2",
        simplify(cos_sq_vars - a_0**2 / v_norm_sq) == 0,
        detail="cos^2 equals trivial-character fraction",
    )

    # ---------------------------------------------------------------------
    section("Part 8: numerical FP cross-checks at three independent samples")
    # ---------------------------------------------------------------------
    # Sample 1: charged-lepton mass-square-roots (PDG approximate; not
    # consumed as authority — sanity-only verification).
    me, mmu, mtau = (
        Rational("510999", 1_000_000_000),  # m_e ~ 0.5109989 MeV in GeV
        Rational("105658", 1_000_000),  # m_mu ~ 0.1056583 GeV
        Rational("177686", 100_000),  # m_tau ~ 1.77686 GeV
    )
    # v_i = sqrt(m_i)
    v_sample_1 = (sqrt(me), sqrt(mmu), sqrt(mtau))
    Q_sample_1 = float(
        (v_sample_1[0] ** 2 + v_sample_1[1] ** 2 + v_sample_1[2] ** 2)
        / (v_sample_1[0] + v_sample_1[1] + v_sample_1[2]) ** 2
    )
    # PDG charged-lepton Koide value is ~0.6667 (very close to 2/3); sanity.
    fp_sample_1_ok = abs(Q_sample_1 - 2.0 / 3.0) < 1e-3
    check(
        "FP sanity: charged-lepton mass-square-roots give Q ~ 2/3 (PDG sanity)",
        fp_sample_1_ok,
        detail=f"Q (sample 1) = {Q_sample_1:.6f}, |Q - 2/3| = {abs(Q_sample_1 - 2/3):.3e}",
    )

    # Sample 2: explicitly on-cone vector chosen by setting v_1 = 1, v_2 = t,
    # v_3 = 1/t with t > 0 (geometric mean condition). Verify Q is the
    # closed-form (E4) value, NOT that it equals 2/3.
    t = Rational(5, 3)  # arbitrary positive rational
    v_sample_2 = (Rational(1), t, 1 / t)
    Q_sample_2 = (
        (v_sample_2[0] ** 2 + v_sample_2[1] ** 2 + v_sample_2[2] ** 2)
        / (v_sample_2[0] + v_sample_2[1] + v_sample_2[2]) ** 2
    )
    # Compute via E4 separately
    a0_s2 = (v_sample_2[0] + v_sample_2[1] + v_sample_2[2]) / sqrt(3)
    z_s2 = (
        v_sample_2[0] + omegabar * v_sample_2[1] + omega * v_sample_2[2]
    ) / sqrt(3)
    z_abs_sq_s2 = simplify(re(expand(z_s2 * conjugate(z_s2))))
    E4_s2 = simplify((a0_s2**2 + 2 * z_abs_sq_s2) / (3 * a0_s2**2))
    check(
        "(E4) at sample 2 (1, 5/3, 3/5): Q matches closed-form (a_0^2 + 2|z|^2)/(3 a_0^2)",
        simplify(Q_sample_2 - E4_s2) == 0,
        detail=f"Q = {Q_sample_2}, E4 form = {E4_s2}",
    )

    # Sample 3: off-cone vector
    v_sample_3 = (Rational(1), Rational(1), Rational(2))
    Q_sample_3 = (
        (v_sample_3[0] ** 2 + v_sample_3[1] ** 2 + v_sample_3[2] ** 2)
        / (v_sample_3[0] + v_sample_3[1] + v_sample_3[2]) ** 2
    )
    # Q = 6/16 = 3/8 = 0.375. Off the 2/3 cone.
    check(
        "off-cone sample 3 (1,1,2): Q = 3/8 != 2/3 (off the Koide cone)",
        simplify(Q_sample_3 - Rational(3, 8)) == 0 and Q_sample_3 != Rational(2, 3),
        detail=f"Q = {Q_sample_3}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: counterfactual probes")
    # ---------------------------------------------------------------------
    # At Q = 1/3 (not 2/3) the cone equation reads:
    # (A + 2B)/(3A) = 1/3 => A + 2B = A => B = 0, i.e. |z|^2 = 0.
    # That is a different cone (the diagonal itself), not the Koide cone.
    # Use a generic real symbol for the counterfactual solve (the positive
    # constraint on B would exclude the algebraic root B = 0).
    A_gen, B_gen = symbols("A_gen B_gen", real=True)
    sols_cf = sympy.solve(
        (A_gen + 2 * B_gen) / (3 * A_gen) - Rational(1, 3), B_gen
    )
    check(
        "counterfactual: at Q = 1/3 the equivalence cone reduces to |z|^2 = 0 (diagonal)",
        len(sols_cf) == 1 and simplify(sols_cf[0]) == 0,
        detail=f"sympy.solve returned |z|^2 ∈ {sols_cf} (confirms Q != 2/3 changes the cone)",
    )

    # At Q = 1 (degenerate vector), the cone equation reads:
    # (A + 2B)/(3A) = 1 => A + 2B = 3A => B = A, i.e. |z|^2 = a_0^2.
    sols_cf_2 = sympy.solve((A + 2 * B) / (3 * A) - 1, B)
    check(
        "counterfactual: at Q = 1 the equivalence cone reduces to |z|^2 = a_0^2",
        len(sols_cf_2) == 1 and simplify(sols_cf_2[0] - A) == 0,
        detail=f"sympy.solve returned |z|^2 ∈ {sols_cf_2}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (E1) Plancherel: |v|^2 = a_0^2 + 2|z|^2 parametric in (v1, v2, v3)")
    print("    (E3) (v_1+v_2+v_3)^2 = 3 a_0^2 parametric")
    print("    (E4) Q(v) = (a_0^2 + 2|z|^2)/(3 a_0^2) parametric")
    print("    Forward (P1): Q = 2/3 algebraically implies a_0^2 = 2|z|^2")
    print("    Reverse (P1): a_0^2 = 2|z|^2 algebraically implies Q = 2/3")
    print("    Parametric (P1): Koide LHS = 0 <=> 2|z|^2 - a_0^2 = 0")
    print("    Geometric corollary: Q = 2/3 <=> cos^2(angle(v,(1,1,1))) = 1/2")
    print("    cos^2(angle) = sigma(v) = a_0^2 / |v|^2")
    print("    FP sanity at three samples (charged-lepton, on-cone, off-cone)")
    print("    Counterfactual: Q = 1/3 and Q = 1 give different cones")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
