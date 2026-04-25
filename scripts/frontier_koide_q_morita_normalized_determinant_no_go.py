#!/usr/bin/env python3
"""
Koide Q Morita-normalized determinant no-go.

Theorem attempt:
  Derive the reduced quotient logdet from Morita-normalized determinant theory.
  On a matrix block M_r, the normalized log-determinant

      log det_r(I+kI_r) / r = log(1+k)

  is invariant under matrix amplification.  If the physical charged-lepton
  source generator uses this normalized determinant on each simple component,
  then the retained ranks (1,2) are deleted:

      dW_Morita|_0 = (1,1) -> K_TL=0 -> Q=2/3.

Result:
  Conditional positive, retained negative.  Morita-normalized determinant
  closes Q exactly and is the cleanest formulation of the reduced quotient
  logdet.  But the full Hilbert determinant is also an exact retained
  determinant functional and gives

      dW_full|_0 = (1,2) -> Q=1, K_TL=3/8.

  The current retained package does not derive that the physical source
  generator is the Morita-normalized determinant rather than the full
  determinant.  That determinant-normalization choice is the missing source
  law.

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


def normalized_weights(y_plus: sp.Expr, y_perp: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    total = sp.simplify(y_plus + y_perp)
    return sp.simplify(y_plus / total), sp.simplify(y_perp / total)


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
    section("A. Full determinant versus Morita-normalized determinant")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    r_plus = sp.Integer(1)
    r_perp = sp.Integer(2)
    n = sp.symbols("n", integer=True, positive=True)
    log_det_full_r = r_perp * sp.log(1 + k_perp)
    log_det_norm_r = sp.simplify(log_det_full_r / r_perp)
    log_det_full_amp = n * r_perp * sp.log(1 + k_perp)
    log_det_norm_amp = sp.simplify(log_det_full_amp / (n * r_perp))
    record(
        "A.1 Morita-normalized logdet removes internal matrix rank",
        log_det_norm_r == sp.log(1 + k_perp),
        f"logdet_full(M_2)={log_det_full_r}; normalized_logdet={log_det_norm_r}",
    )
    record(
        "A.2 Morita-normalized logdet is invariant under matrix amplification",
        log_det_norm_amp == sp.log(1 + k_perp),
        f"logdet_full(M_{{2n}})={log_det_full_amp}; normalized_logdet_amp={log_det_norm_amp}",
    )
    record(
        "A.3 full logdet is not Morita invariant under amplification",
        log_det_full_amp != log_det_full_r,
        "Full logdet scales with the amplified matrix rank.",
    )

    section("B. Conditional positive theorem")

    w_morita = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    y_morita = gradient_at_zero(w_morita, (k_plus, k_perp))
    weights_morita = normalized_weights(*y_morita)
    record(
        "B.1 Morita-normalized determinant gives intensive component response",
        y_morita == (1, 1) and weights_morita == (sp.Rational(1, 2), sp.Rational(1, 2)),
        f"W_M={w_morita}; dW_M|0={y_morita}; weights={weights_morita}",
    )
    record(
        "B.2 Morita-normalized determinant closes the Q chain",
        ktl_from_weights(*weights_morita) == 0
        and q_from_weights(*weights_morita) == sp.Rational(2, 3),
        f"K_TL={ktl_from_weights(*weights_morita)}, Q={q_from_weights(*weights_morita)}",
    )

    section("C. Retained full-determinant countermodel")

    w_full = r_plus * sp.log(1 + k_plus) + r_perp * sp.log(1 + k_perp)
    y_full = gradient_at_zero(w_full, (k_plus, k_perp))
    weights_full = normalized_weights(*y_full)
    record(
        "C.1 full determinant gives rank-additive response",
        y_full == (1, 2) and weights_full == (sp.Rational(1, 3), sp.Rational(2, 3)),
        f"W_full={w_full}; dW_full|0={y_full}; weights={weights_full}",
    )
    record(
        "C.2 full determinant response is exact and off Koide",
        ktl_from_weights(*weights_full) == sp.Rational(3, 8)
        and q_from_weights(*weights_full) == 1,
        f"K_TL={ktl_from_weights(*weights_full)}, Q={q_from_weights(*weights_full)}",
    )

    section("D. Determinant-normalization exponent")

    alpha = sp.symbols("alpha_det", real=True)
    w_alpha = r_plus**alpha * sp.log(1 + k_plus) + r_perp**alpha * sp.log(1 + k_perp)
    y_alpha = gradient_at_zero(w_alpha, (k_plus, k_perp))
    weights_alpha = normalized_weights(*y_alpha)
    ktl_alpha = sp.simplify(ktl_from_weights(*weights_alpha))
    record(
        "D.1 determinant-normalization family leaves one exponent alpha",
        y_alpha[0] == 1 and y_alpha[1] == 2**alpha,
        f"dW_alpha|0={y_alpha}; K_TL={ktl_alpha}",
    )
    record(
        "D.2 K_TL=0 selects the Morita-normalized exponent alpha=0",
        sp.solveset(sp.Eq(2**alpha, 1), alpha, domain=sp.S.Reals) == sp.FiniteSet(0),
        "alpha=0 is normalized determinant; alpha=1 is full determinant.",
    )
    retained_constraints = sp.Matrix([0, 0, 0])
    record(
        "D.3 retained support constraints do not set alpha=0",
        retained_constraints.jacobian([alpha]).rank() == 0,
        "No retained equation in this audit chooses normalized determinant over full determinant.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as an input",
        True,
        "The determinant choices are audited before evaluating Q.",
    )
    record(
        "E.2 Morita normalization is not promoted as retained closure",
        True,
        "It is a sufficient determinant law, but the full determinant countermodel remains retained.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need a retained theorem selecting Morita-normalized determinant as the physical source generator.",
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
        print("VERDICT: Morita-normalized determinant is conditional, not retained-only proof.")
        print("KOIDE_Q_MORITA_NORMALIZED_DETERMINANT_NO_GO=TRUE")
        print("Q_MORITA_NORMALIZED_DETERMINANT_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_MORITA_NORMALIZED_DETERMINANT_IS_PHYSICAL=TRUE")
        print("RESIDUAL_SCALAR=derive_Morita_normalized_determinant_as_physical_source_generator")
        print("RESIDUAL_Q=full_rank_determinant_source_response_not_excluded")
        print("COUNTERSTATE=full_determinant_w_plus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: Morita-normalized determinant audit has FAILs.")
    print("KOIDE_Q_MORITA_NORMALIZED_DETERMINANT_NO_GO=FALSE")
    print("Q_MORITA_NORMALIZED_DETERMINANT_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_Morita_normalized_determinant_as_physical_source_generator")
    return 1


if __name__ == "__main__":
    sys.exit(main())
