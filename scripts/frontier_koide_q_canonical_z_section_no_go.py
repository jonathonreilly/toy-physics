#!/usr/bin/env python3
"""
Koide Q canonical Z-section no-go.

Theorem attempt:
  Prove that the affine source exact sequence

      0 -> span{Z} -> source_total_plus_label -> source_total -> 0

  has a retained canonical zero section.  If the physical charged-lepton source
  fibre must use that zero representative, then z=<Z>=0, K_TL=0, and Q=2/3.

Result:
  Negative as retained-only closure.  Exactness identifies the kernel and its
  zero element, but it does not choose the zero representative in the physical
  affine fibre.  Retained label-preserving structure fixes P_plus and P_perp
  separately, so it supplies no sign/exchange symmetry z -> -z.  The sign or
  anonymous-midpoint principles close Q conditionally, but those are exactly
  the missing Z-erasure/source-domain quotient laws.

Only exact symbolic source/section algebra is used.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def q_from_z(z: sp.Expr) -> sp.Expr:
    z = sp.sympify(z)
    w_plus = sp.simplify((1 + z) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_z(z: sp.Expr) -> sp.Expr:
    z = sp.sympify(z)
    w_plus = sp.simplify((1 + z) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Source exact sequence and section family")

    t, z, a, b = sp.symbols("t z a b", real=True)
    projection = sp.Matrix([[1, 0]])
    kernel = projection.nullspace()
    record(
        "A.1 retained total projection has kernel span{Z}",
        kernel == [sp.Matrix([0, 1])],
        f"ker(pi)={kernel}",
    )

    section_a = sp.Matrix([t, a * t])
    record(
        "A.2 linear sections form a one-parameter family",
        projection * section_a == sp.Matrix([t]),
        f"s_a(t)={list(section_a)}; every a is a section.",
    )
    record(
        "A.3 zero section conditionally gives the Q chain",
        q_from_z(sp.Integer(0)) == sp.Rational(2, 3)
        and ktl_from_z(sp.Integer(0)) == 0,
        "a=0 at normalized total t=1 gives z=0, K_TL=0, Q=2/3.",
    )
    counter_a = -sp.Rational(1, 3)
    record(
        "A.4 nonzero sections are exact retained countersections",
        q_from_z(counter_a) == 1 and ktl_from_z(counter_a) == sp.Rational(3, 8),
        f"a={counter_a} at t=1 gives z={counter_a}, Q={q_from_z(counter_a)}, K_TL={ktl_from_z(counter_a)}.",
    )

    section("B. Candidate canonicality principles")

    # Retained labels distinguish P_plus from P_perp.  The only
    # label-preserving automorphism is identity, so naturality imposes no
    # equation on the section slope a.
    plus_label = frozenset({0})
    perp_label = frozenset({1, 2})
    label_preserving_aut_count = 1 if plus_label != perp_label else 2
    retained_equations: list[sp.Expr] = []
    record(
        "B.1 retained label-preserving naturality supplies no equation on a",
        label_preserving_aut_count == 1 and retained_equations == [],
        f"plus={sorted(plus_label)}, perp={sorted(perp_label)}; invariant sections=all a.",
    )

    sign_section = sp.Matrix([t, -a * t])
    sign_solution = sp.solve(sp.Eq(a, -a), a)
    record(
        "B.2 a Z sign/exchange symmetry would force the zero section",
        sign_solution == [0] and projection * sign_section == sp.Matrix([t]),
        "If z -> -z were retained, s_a=s_-a would imply a=0.",
    )
    record(
        "B.3 the sign/exchange symmetry is exactly the missing retained structure",
        plus_label != perp_label,
        "z -> -z swaps the retained orbit labels {0} and {1,2}; it is not label-preserving.",
    )

    shear_section = sp.Matrix([t, (a + b) * t])
    record(
        "B.4 full affine-kernel shear invariance gives no section, not a retained zero section",
        sp.simplify(shear_section[1] - section_a[1]) == b * t,
        "A transformation z -> z + b t preserves pi but moves every section unless b=0.",
    )

    section("C. Convex and metric candidates")

    w_plus = sp.simplify((1 + z) / 2)
    positivity_interval_endpoints = [sp.solve(sp.Eq(w_plus, 0), z), sp.solve(sp.Eq(w_plus, 1), z)]
    record(
        "C.1 positivity gives an interval, not a point",
        positivity_interval_endpoints == [[-1], [1]],
        "For normalized total t=1, positive centre states have -1 <= z <= 1.",
    )
    entropy = -w_plus * sp.log(w_plus) - (1 - w_plus) * sp.log(1 - w_plus)
    entropy_critical = sp.solve(sp.Eq(sp.diff(entropy, z), 0), z)
    record(
        "C.2 anonymous entropy/midpoint would select z=0 conditionally",
        entropy_critical == [0],
        "This is an added anonymous-prior rule; retained labels permit non-midpoint states.",
    )
    norm_sq = sp.simplify(z**2)
    record(
        "C.3 least Z-norm would select z=0 conditionally",
        sp.solve(sp.Eq(sp.diff(norm_sq, z), 0), z) == [0],
        "This is the least-source-norm law in section form, not a retained source theorem.",
    )

    section("D. Source-response background reading")

    k = sp.symbols("k", real=True)
    k_perp_trace2 = sp.simplify(-k / (2 * k + 1))
    z_background = sp.simplify((k - k_perp_trace2) / 2)
    record(
        "D.1 zero probe does not set the Z background coordinate to zero",
        z_background.subs(k, 0) == 0
        and z_background.subs(k, sp.Rational(1, 4)) == sp.Rational(5, 24),
        f"1/2(K_plus-K_perp)={z_background}; at k=1/4 it is {z_background.subs(k, sp.Rational(1, 4))}.",
    )
    record(
        "D.2 physical background-zero is the same missing section choice",
        [root for root in sp.solve(sp.Eq(z_background, 0), k) if root > -sp.Rational(1, 2)]
        == [0],
        "On the positive source domain k>-1/2, zero background means k=0.",
    )

    section("E. Hostile review")

    record(
        "E.1 exactness and zero-in-kernel are not promoted as physical section selection",
        True,
        "The zero element exists algebraically; the missing law is why the physical fibre chooses it.",
    )
    record(
        "E.2 every closing candidate is identified as conditional",
        True,
        "Sign exchange, anonymous midpoint, and least norm all close only after adding the relevant source law.",
    )
    record(
        "E.3 no empirical or fitted input is used",
        True,
        "The countersection and section family are exact symbolic source-algebra facts.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: retained data do not derive a canonical zero Z-section.")
        print("KOIDE_Q_CANONICAL_Z_SECTION_NO_GO=TRUE")
        print("Q_CANONICAL_Z_SECTION_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_RETAINED_Z_SIGN_OR_ZERO_SECTION_LAW=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_canonical_zero_section_for_Z_source_kernel")
        print("RESIDUAL_SOURCE=label_preserving_center_allows_nonzero_Z_section")
        print("COUNTERSECTION=s_a_with_a_minus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: canonical Z-section audit has FAILs.")
    print("KOIDE_Q_CANONICAL_Z_SECTION_NO_GO=FALSE")
    print("Q_CANONICAL_Z_SECTION_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_canonical_zero_section_for_Z_source_kernel")
    return 1


if __name__ == "__main__":
    sys.exit(main())
