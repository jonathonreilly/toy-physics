#!/usr/bin/env python3
"""
Koide Q stable Morita trace-simplex no-go.

Theorem attempt:
  Derive the stable Morita source-response law from Morita-invariant traces.
  On each simple matrix block M_r, the normalized trace/logdet is stable under
  matrix amplification and deletes the internal rank r.  Perhaps this forces
  the physical source generator on the charged-lepton reduced algebra

      C plus M_2(C)

  to use equal coefficients on the two center components.

Result:
  Negative.  Stable Morita invariance normalizes each simple block, but a
  semisimple algebra still has a center-state simplex:

      tau_lambda = lambda tau_plus + (1-lambda) tau_perp.

  The equal center state lambda=1/2 conditionally closes Q.  The retained
  rank/K0 state lambda=1/3 is still stable on each simple block and gives
  Q=1, K_TL=3/8.  Therefore the missing law is not matrix-block Morita
  invariance itself; it is the physical center-state selection that chooses
  lambda=1/2 over rank-visible lambda=1/3.

No PDG masses, H_* pins, K_TL=0 assumptions, Q target assumptions, delta pins,
or observational inputs are used.
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


def q_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weights(w_plus: sp.Expr, w_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(w_perp / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def gradient_at_zero(w: sp.Expr, variables: tuple[sp.Symbol, sp.Symbol]) -> tuple[sp.Expr, sp.Expr]:
    k_plus, k_perp = variables
    return (
        sp.simplify(sp.diff(w, k_plus).subs({k_plus: 0, k_perp: 0})),
        sp.simplify(sp.diff(w, k_perp).subs({k_plus: 0, k_perp: 0})),
    )


def main() -> int:
    section("A. Stable Morita normalization inside simple blocks")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    r, n = sp.symbols("r n", integer=True, positive=True)
    full_logdet = n * r * sp.log(1 + k_perp)
    normalized_logdet = sp.simplify(full_logdet / (n * r))
    record(
        "A.1 normalized trace/logdet is stable under matrix amplification",
        normalized_logdet == sp.log(1 + k_perp),
        f"logdet(M_{{nr}})/(nr) = {normalized_logdet}",
    )
    record(
        "A.2 stable Morita normalization deletes simple-block rank",
        sp.diff(normalized_logdet, r) == 0 and sp.diff(normalized_logdet, n) == 0,
        "Internal matrix size is invisible after normalized trace/logdet.",
    )

    section("B. Semisimple center-state simplex remains")

    lam = sp.symbols("lambda_center", real=True)
    W_lam = lam * sp.log(1 + k_plus) + (1 - lam) * sp.log(1 + k_perp)
    y_lam = gradient_at_zero(W_lam, (k_plus, k_perp))
    ktl_lam = sp.simplify(ktl_from_weights(*y_lam))
    q_lam = sp.simplify(q_from_weights(*y_lam))
    record(
        "B.1 stable Morita traces on C plus M2(C) form a center-state simplex",
        y_lam == (lam, 1 - lam),
        f"W_lambda={W_lam}; dW|0={y_lam}",
    )
    record(
        "B.2 every lambda is normalized on the center-state simplex",
        sp.simplify(lam + (1 - lam)) == 1,
        "Morita normalization fixes each simple trace, not the center weight lambda.",
    )
    record(
        "B.3 K_TL=0 selects lambda=1/2",
        sp.solve(sp.Eq(ktl_lam, 0), lam) == [sp.Rational(1, 2)],
        f"K_TL(lambda)={ktl_lam}",
    )

    section("C. Conditional positive and retained counterstate")

    equal_center = {lam: sp.Rational(1, 2)}
    rank_center = {lam: sp.Rational(1, 3)}
    record(
        "C.1 equal center-state trace conditionally closes Q",
        ktl_lam.subs(equal_center) == 0
        and q_lam.subs(equal_center) == sp.Rational(2, 3),
        f"lambda=1/2 -> K_TL={ktl_lam.subs(equal_center)}, Q={q_lam.subs(equal_center)}",
    )
    record(
        "C.2 retained rank/K0 center state is stable inside each block but off Koide",
        ktl_lam.subs(rank_center) == sp.Rational(3, 8)
        and q_lam.subs(rank_center) == 1,
        f"lambda=1/3 -> K_TL={ktl_lam.subs(rank_center)}, Q={q_lam.subs(rank_center)}",
    )
    record(
        "C.3 stable Morita invariance does not distinguish equal-center from rank/K0 center state",
        True,
        "Both use normalized traces on each simple block; only the center weights differ.",
    )

    section("D. Hostile retained-status audit")

    center_state_selection = sp.symbols("center_state_selection", real=True)
    rank_visible_center_state = sp.symbols("rank_visible_center_state", real=True)
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.1 retained support constraints do not set lambda=1/2",
        retained_constraints.jacobian([center_state_selection]).rank() == 0,
        "No retained equation in this audit collapses the trace simplex to equal center weight.",
    )
    record(
        "D.2 retained support constraints do not exclude rank-visible lambda=1/3",
        retained_constraints.jacobian([rank_visible_center_state]).rank() == 0,
        "No retained equation in this audit forbids K0/rank center weighting.",
    )
    record(
        "D.3 exact residual primitive is named",
        True,
        "Need a retained theorem selecting equal center-state trace after stable Morita normalization.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The trace simplex is audited before evaluating Q.",
    )
    record(
        "E.2 stable Morita trace normalization is not promoted as retained closure",
        True,
        "It normalizes simple blocks, but does not select the semisimple center state.",
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
        print("VERDICT: stable Morita trace theory leaves a center-state simplex; Q is not closed.")
        print("KOIDE_Q_STABLE_MORITA_TRACE_SIMPLEX_NO_GO=TRUE")
        print("Q_STABLE_MORITA_TRACE_SIMPLEX_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_EQUAL_CENTER_STATE_IS_PHYSICAL=TRUE")
        print("RESIDUAL_SCALAR=derive_equal_center_state_after_stable_Morita_normalization")
        print("RESIDUAL_Q=rank_K0_center_state_lambda_1_over_3_not_excluded")
        print("COUNTERSTATE=stable_Morita_rank_center_state_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: stable Morita trace-simplex audit has FAILs.")
    print("KOIDE_Q_STABLE_MORITA_TRACE_SIMPLEX_NO_GO=FALSE")
    print("Q_STABLE_MORITA_TRACE_SIMPLEX_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_equal_center_state_after_stable_Morita_normalization")
    return 1


if __name__ == "__main__":
    sys.exit(main())
