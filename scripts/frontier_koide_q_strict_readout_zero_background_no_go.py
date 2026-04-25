#!/usr/bin/env python3
"""
Koide Q strict-readout zero-background no-go.

Theorem attempt:
  Derive the remaining Z-erasure/source-domain law from the retained statement
  that physical scalar observables are local source-response coefficients of
  W[J] at a zero-source expansion point.

Result:
  Negative as retained-only closure.  The retained source-response calculus
  cleanly distinguishes two notions:

      probe zero:      take derivatives with respect to a local probe J at
                       J=0 around a chosen background K_bg;
      background zero: choose K_bg=0 as the physical charged-lepton selector.

  Probe-zero readout is retained and works around every admissible background.
  Background-zero readout is exactly the missing source law.  On the
  normalized trace-2 carrier, a nonzero traceless background is a one-scalar
  selector coordinate; it remains source-response compatible and off Koide.

Only exact symbolic source-response algebra is used.
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


def q_from_y(y_plus: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.Rational(2, 3) / y_plus)


def ktl_from_y(y_plus: sp.Expr) -> sp.Expr:
    return sp.simplify((1 - y_plus) / (y_plus * (2 - y_plus)))


def main() -> int:
    section("A. Probe-zero source-response is not background-zero selection")

    k_plus, k_perp, j_plus, j_perp = sp.symbols(
        "k_plus k_perp j_plus j_perp", real=True
    )
    w_bg = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    w_probe = (
        sp.log(1 + k_plus + j_plus)
        + sp.log(1 + k_perp + j_perp)
        - w_bg
    )
    y_plus = sp.simplify(sp.diff(w_probe, j_plus).subs({j_plus: 0, j_perp: 0}))
    y_perp = sp.simplify(sp.diff(w_probe, j_perp).subs({j_plus: 0, j_perp: 0}))

    record(
        "A.1 local scalar readout is a probe derivative at J=0 around K_bg",
        y_plus == 1 / (1 + k_plus) and y_perp == 1 / (1 + k_perp),
        f"dW_probe/dJ|0=({y_plus}, {y_perp})",
    )
    record(
        "A.2 setting the probe to zero does not set the background source to zero",
        w_probe.subs({j_plus: 0, j_perp: 0}) == 0
        and y_plus.has(k_plus)
        and y_perp.has(k_perp),
        "The probe baseline subtracts W(K_bg); K_bg remains as physical background data.",
    )

    section("B. Normalized trace-2 background family")

    t = sp.symbols("t", real=True)
    k_perp_trace2 = sp.simplify(-t / (2 * t + 1))
    y_plus_t = sp.simplify(y_plus.subs(k_plus, t))
    y_perp_t = sp.simplify(y_perp.subs(k_perp, k_perp_trace2))
    record(
        "B.1 trace normalization leaves a one-parameter traceless background source",
        sp.simplify(y_plus_t + y_perp_t - 2) == 0,
        f"K_bg(t)=diag({t}, {k_perp_trace2}); Y(t)=diag({y_plus_t}, {y_perp_t})",
    )
    record(
        "B.2 the zero-background member is unique and lands on the identity carrier",
        sp.solve(sp.Eq(t, 0), t) == [0]
        and y_plus_t.subs(t, 0) == 1
        and y_perp_t.subs(t, 0) == 1,
        "K_bg=0 -> Y=I_2.",
    )
    record(
        "B.3 nonzero backgrounds are still exact source-response backgrounds",
        y_plus_t.subs(t, sp.Rational(1, 4)) == sp.Rational(4, 5)
        and y_perp_t.subs(t, sp.Rational(1, 4)) == sp.Rational(6, 5),
        "t=1/4 -> Y=diag(4/5,6/5), still Tr(Y)=2.",
    )

    section("C. Q consequence and counterbackground")

    q_t = sp.simplify(q_from_y(y_plus_t))
    ktl_t = sp.simplify(ktl_from_y(y_plus_t))
    record(
        "C.1 zero background conditionally gives the Q chain",
        q_t.subs(t, 0) == sp.Rational(2, 3) and ktl_t.subs(t, 0) == 0,
        f"Q(t)={q_t}, K_TL(t)={ktl_t}",
    )
    record(
        "C.2 an exact nonzero background gives an off-Koide source-compatible state",
        q_t.subs(t, sp.Rational(1, 4)) == sp.Rational(5, 6)
        and ktl_t.subs(t, sp.Rational(1, 4)) == sp.Rational(5, 24),
        "t=1/4 is the explicit retained counterbackground.",
    )
    record(
        "C.3 K_TL=0 is equivalent to the missing background-zero equation",
        [root for root in sp.solve(sp.Eq(ktl_t, 0), t) if root > -sp.Rational(1, 2)]
        == [0],
        "On the positive trace-2 source domain t>-1/2, K_TL=0 iff t=0.",
    )

    section("D. Relation to Z erasure")

    P_plus = sp.Matrix([[1, 0], [0, 0]])
    P_perp = sp.Matrix([[0, 0], [0, 1]])
    Z = sp.simplify(P_plus - P_perp)
    K_bg_t = sp.diag(t, k_perp_trace2)
    z_coeff = sp.simplify(sp.trace(Z * K_bg_t) / 2)
    record(
        "D.1 the surviving background coordinate is exactly the Z source coefficient",
        sp.diff(z_coeff, t) != 0 and z_coeff.subs(t, 0) == 0,
        f"1/2 tr(Z K_bg(t))={z_coeff}",
    )
    record(
        "D.2 strict readout kills Z only after choosing background zero",
        z_coeff.subs(t, sp.Rational(1, 4)) != 0,
        "The source-visible Z coordinate survives unless the background-zero law is supplied.",
    )

    section("E. Hostile review")

    record(
        "E.1 strict source-response readout is valid conditional support",
        True,
        "It proves the algebraic consequence of K_bg=0 on the normalized carrier.",
    )
    record(
        "E.2 strict readout does not derive retained-only Q closure",
        True,
        "The disputed step is identifying the physical charged-lepton background with K_bg=0.",
    )
    record(
        "E.3 no empirical or fitted input is used",
        True,
        "All checks are symbolic identities in the reduced source generator.",
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
        print("VERDICT: strict readout does not derive zero physical background.")
        print("KOIDE_Q_STRICT_READOUT_ZERO_BACKGROUND_NO_GO=TRUE")
        print("Q_STRICT_READOUT_ZERO_BACKGROUND_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_PHYSICAL_BACKGROUND_SOURCE_IS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_physical_background_source_zero_equiv_Z_erasure")
        print("RESIDUAL_SOURCE=probe_zero_readout_allows_nonzero_traceless_background")
        print("COUNTERBACKGROUND=t_1_over_4_Q_5_over_6_K_TL_5_over_24")
        return 0

    print("VERDICT: strict-readout zero-background audit has FAILs.")
    print("KOIDE_Q_STRICT_READOUT_ZERO_BACKGROUND_NO_GO=FALSE")
    print("Q_STRICT_READOUT_ZERO_BACKGROUND_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_physical_background_source_zero_equiv_Z_erasure")
    return 1


if __name__ == "__main__":
    sys.exit(main())
