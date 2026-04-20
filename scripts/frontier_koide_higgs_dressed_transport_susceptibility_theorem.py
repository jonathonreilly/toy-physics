#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed transport susceptibility theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_TRANSPORT_SUSCEPTIBILITY_THEOREM_NOTE_2026-04-20.md`.
"""

from __future__ import annotations

import numpy as np

from frontier_koide_higgs_dressed_chamber_link_renormalization_theorem import (
    q_residual,
    transport_scalars,
)


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


LAMBDA_STAR = 0.01580870328539511


def P_x(x: float, t: float, d: float) -> float:
    return 4.0 * x**3 - 84.0 * t * x**2 + 2.0 * (198.0 * t * t - 1568.0 * d) * x - (28.0 * t**3 + 1088.0 * d * t)


def P_t(x: float, t: float, d: float) -> float:
    return -28.0 * x**3 + 396.0 * t * x**2 - (84.0 * t * t + 1088.0 * d) * x + 4.0 * t**3 - 64.0 * d * t


def P_d(x: float, t: float, d: float) -> float:
    return -1568.0 * x**2 - 1088.0 * t * x - 32.0 * t * t + 512.0 * d


def local_derivatives(lambda_value: float, eps: float = 1.0e-7) -> tuple[float, float, float, float]:
    _, tp, dp, _ = transport_scalars(lambda_value + eps, 0.0)
    _, tm, dm, _ = transport_scalars(lambda_value - eps, 0.0)
    t_prime = (tp - tm) / (2.0 * eps)
    d_prime = (dp - dm) / (2.0 * eps)
    fl = (q_residual(lambda_value + eps, 0.0) - q_residual(lambda_value - eps, 0.0)) / (2.0 * eps)
    fh = (q_residual(lambda_value, eps) - q_residual(lambda_value, -eps)) / (2.0 * eps)
    return t_prime, d_prime, fl, fh


def main() -> None:
    print("=" * 88)
    print("Koide Higgs-dressed transport susceptibility theorem")
    print("=" * 88)

    x_star, t_star, d_star, _ = transport_scalars(LAMBDA_STAR, 0.0)
    t_prime, d_prime, fl, fh = local_derivatives(LAMBDA_STAR)
    alpha = -fl / fh

    bare_tracking = 1.0
    backreaction = (LAMBDA_STAR**2) * (P_t(x_star, t_star, d_star) * t_prime + P_d(x_star, t_star, d_star) * d_prime) / P_x(x_star, t_star, d_star)
    alpha_from_balance = bare_tracking - backreaction

    check(
        "The local branch slope from direct Koide differentiation is positive and below bare O_0 tracking",
        0.9 < alpha < 1.0,
        detail=f"alpha={alpha:.12f}",
    )
    check(
        "The reached principal-block trace decreases with lambda at the physical root",
        t_prime < 0.0,
        detail=f"t'={t_prime:.12f}",
    )
    check(
        "The reached principal-block determinant also decreases with lambda at the physical root",
        d_prime < 0.0,
        detail=f"d'={d_prime:.12f}",
    )
    check(
        "The local O_0 susceptibility identity reproduces alpha from the principal-block balance law",
        abs(alpha - alpha_from_balance) < 1.0e-10,
        detail=f"alpha_balance={alpha_from_balance:.12f}",
    )
    check(
        "The deviation from bare chamber-link tracking is exactly a small reached-block backreaction",
        0.03 < backreaction < 0.05,
        detail=f"backreaction={backreaction:.12f}",
    )
    check(
        "That backreaction accounts for the full gap between alpha and 1 within numerical precision",
        abs((1.0 - alpha) - backreaction) < 1.0e-10,
        detail=f"1-alpha={1.0-alpha:.12f}",
    )

    # Finite-difference stability audit.
    eps_values = [1.0e-5, 1.0e-6, 1.0e-7]
    alphas = []
    for eps in eps_values:
        _, _, fl_eps, fh_eps = local_derivatives(LAMBDA_STAR, eps=eps)
        alphas.append(-fl_eps / fh_eps)
    check(
        "The susceptibility coefficient alpha is stable across finite-difference scales",
        max(alphas) - min(alphas) < 1.0e-8,
        detail=f"alphas={[round(a, 12) for a in alphas]}",
    )

    print()
    print("Interpretation:")
    print("  Alpha is not just a local fit coefficient. It is the exact local")
    print("  susceptibility ratio of the Koide transport equation, and it splits as")
    print("      alpha = 1 - reached-block backreaction.")
    print("  Numerically the backreaction is only about 4.08%, so the visible chamber")
    print("  link almost tracks exact Koide by itself. The live microscopic object is")
    print("  therefore even sharper: derive that reached-block backreaction term from")
    print("  the retained transport law.")
    print()
    print(f"  alpha        = {alpha:.12f}")
    print(f"  backreaction = {backreaction:.12f}")
    print(f"  t'           = {t_prime:.12f}")
    print(f"  d'           = {d_prime:.12f}")
    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
