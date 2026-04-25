#!/usr/bin/env python3
"""
Koide Q reduced-observable component-anonymity no-go.

Theorem attempt:
  Use the exact reduced observable theorem W_red=log(1+k_plus)+log(1+k_perp)
  to derive quotient-center component anonymity and therefore K_TL=0.

Result:
  Negative, but sharpened.  The reduced observable generator is symmetric in
  the two reduced source variables, and its source-free derivative gives equal
  components.  But that only closes Q after imposing the source-free point

      k_plus = k_perp = 0.

  The same symmetric reduced observable admits nonzero reduced sources
  compatible with trace normalization.  Those sources reparameterize the one
  remaining selector and give non-closing Q.  Thus reduced-observable symmetry
  plus pure-block normalization does not derive the source-free/component
  anonymity law; it restates the already-reviewed source-free conditional
  closure.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
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


def q_from_y(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(y_perp / y_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_y(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(y_perp / y_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Reduced observable symmetry")

    kp, kq = sp.symbols("k_plus k_perp", real=True)
    w_red = sp.log(1 + kp) + sp.log(1 + kq)
    w_swapped = w_red.subs({kp: kq, kq: kp}, simultaneous=True)
    record(
        "A.1 W_red is symmetric on the abstract two-slot reduced carrier",
        sp.simplify(w_red - w_swapped) == 0,
        f"W_red={w_red}",
    )
    y_plus = sp.simplify(sp.diff(w_red, kp))
    y_perp = sp.simplify(sp.diff(w_red, kq))
    record(
        "A.2 source-free derivative gives equal components",
        y_plus.subs({kp: 0}) == 1 and y_perp.subs({kq: 0}) == 1,
        f"dW/dk=({y_plus},{y_perp}) at K=0 -> (1,1)",
    )
    record(
        "A.3 source-free reduced point conditionally gives Q=2/3",
        q_from_y(sp.Integer(1), sp.Integer(1)) == sp.Rational(2, 3)
        and ktl_from_y(sp.Integer(1), sp.Integer(1)) == 0,
        "Y=(1,1) -> Q=2/3, K_TL=0.",
    )

    section("B. Symmetric observable still admits nonzero reduced sources")

    y = sp.symbols("y", positive=True, real=True)
    # Trace-normalized positive carrier: Y=(y,2-y).
    kp_y = sp.simplify(1 / y - 1)
    kq_y = sp.simplify(1 / (2 - y) - 1)
    trace_norm = sp.simplify(y + (2 - y))
    record(
        "B.1 trace normalization leaves a one-parameter source family",
        trace_norm == 2,
        f"K(y)=({kp_y},{kq_y}), Y=(y,2-y)",
    )

    sample_y = sp.Rational(2, 3)
    sample_kp = sp.simplify(kp_y.subs(y, sample_y))
    sample_kq = sp.simplify(kq_y.subs(y, sample_y))
    sample_q = q_from_y(sample_y, 2 - sample_y)
    sample_ktl = ktl_from_y(sample_y, 2 - sample_y)
    record(
        "B.2 nonzero reduced source is symmetric-form admissible but non-closing",
        sample_kp != 0
        and sample_kq != 0
        and sample_q == sp.Rational(1, 1)
        and sample_ktl == sp.Rational(3, 8),
        f"y={sample_y}, K=({sample_kp},{sample_kq}), Q={sample_q}, K_TL={sample_ktl}",
    )
    record(
        "B.3 K_TL=0 over the normalized family is exactly y=1",
        sp.solve(sp.Eq(ktl_from_y(y, 2 - y), 0), y) == [1],
        f"K_TL(y)={sp.factor(ktl_from_y(y, 2-y))}",
    )

    section("C. Verdict")

    record(
        "C.1 reduced-observable symmetry does not derive component anonymity",
        True,
        "It supports the source-free conditional theorem but does not force the source-free point.",
    )
    record(
        "C.2 Q remains open after reduced-observable component-anonymity audit",
        True,
        "Residual primitive: physical law setting the reduced source K to zero or equivalently Y=(1,1).",
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
        print("VERDICT: reduced-observable symmetry does not close Q.")
        print("KOIDE_Q_REDUCED_OBSERVABLE_COMPONENT_ANONYMITY_NO_GO=TRUE")
        print("Q_REDUCED_OBSERVABLE_COMPONENT_ANONYMITY_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=reduced_source_K_zero_equiv_component_anonymity")
        print("RESIDUAL_SOURCE=source_free_reduced_point_not_derived_by_W_red_symmetry")
        return 0

    print("VERDICT: reduced-observable component-anonymity audit has FAILs.")
    print("KOIDE_Q_REDUCED_OBSERVABLE_COMPONENT_ANONYMITY_NO_GO=FALSE")
    print("Q_REDUCED_OBSERVABLE_COMPONENT_ANONYMITY_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=reduced_source_K_zero_equiv_component_anonymity")
    print("RESIDUAL_SOURCE=source_free_reduced_point_not_derived_by_W_red_symmetry")
    return 1


if __name__ == "__main__":
    sys.exit(main())
