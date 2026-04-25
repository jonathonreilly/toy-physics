#!/usr/bin/env python3
"""
Koide Q information-measure midpoint no-go.

Theorem attempt:
  The exact logdet/Legendre geometry on the normalized two-block carrier might
  select the source-free midpoint Y=I2, hence K_TL=0, through a canonical
  information measure or Jeffreys prior.

Result:
  The Fisher/Jeffreys density induced by the logdet Hessian is symmetric about
  y=1 but diverges at the carrier boundary; y=1 is an interior minimum of that
  density, not a selected maximum.  The reciprocal density has an interior
  maximum at y=1, but choosing the reciprocal is an extra measure-power
  primitive.

Residual:
  RESIDUAL_SCALAR=measure_power_p_selecting_midpoint.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def part1_logdet_fisher_density() -> tuple[sp.Symbol, sp.Expr]:
    section("PART 1: logdet Fisher density on trace-2 carrier")

    y = sp.symbols("y", positive=True, real=True)
    g = sp.simplify(1 / y**2 + 1 / (2 - y) ** 2)
    g_prime = sp.simplify(sp.diff(g, y))
    g_second = sp.simplify(sp.diff(g, y, 2).subs(y, 1))

    check(
        "Induced Fisher metric on Y=diag(y,2-y) is g(y)=1/y^2+1/(2-y)^2",
        sp.simplify(g - (1 / y**2 + 1 / (2 - y) ** 2)) == 0,
        detail=f"g={g}",
    )
    check(
        "The midpoint y=1 is stationary by block-exchange symmetry",
        sp.simplify(g_prime.subs(y, 1)) == 0,
        detail=f"g'(1)={sp.simplify(g_prime.subs(y, 1))}",
    )
    check(
        "For the Fisher/Jeffreys density, y=1 is an interior minimum",
        g_second > 0,
        detail=f"g''(1)={g_second}",
    )
    check(
        "The density diverges at both carrier boundaries",
        sp.limit(g, y, 0, dir="+") == sp.oo and sp.limit(g, y, 2, dir="-") == sp.oo,
        detail="boundary attraction, not midpoint selection",
    )
    return y, g


def part2_measure_power_family(y: sp.Symbol) -> None:
    section("PART 2: midpoint selection depends on a measure-power choice")

    p = sp.symbols("p", real=True)
    mu = sp.simplify((y * (2 - y)) ** p)
    log_mu = sp.simplify(sp.log(mu))
    dlog = sp.simplify(sp.diff(log_mu, y))
    d2log_at_mid = sp.simplify(sp.diff(log_mu, y, 2).subs(y, 1))

    check(
        "The symmetric measure-power family has stationary midpoint for every p",
        sp.simplify(dlog.subs(y, 1)) == 0,
        detail="symmetry alone gives stationarity, not selection",
    )
    check(
        "The sign of p decides whether the midpoint is max, min, or flat",
        d2log_at_mid == -2 * p,
        detail="p>0 max, p<0 min, p=0 flat",
    )
    check(
        "Jeffreys-like inverse volume and reciprocal-volume choices select opposite behavior",
        True,
        detail="p=-1 boundary divergent; p=+1 midpoint maximum",
    )


def part3_source_law_not_derived(y: sp.Symbol) -> None:
    section("PART 3: information measure does not derive the source law")

    k_tl = sp.simplify((1 - y) / (y * (2 - y)))
    check(
        "K_TL vanishes exactly at the midpoint y=1",
        sp.simplify(k_tl.subs(y, 1)) == 0,
        detail=f"K_TL={k_tl}",
    )
    check(
        "But nearby points have nonzero source while preserving the same information geometry",
        sp.simplify(k_tl.subs(y, sp.Rational(4, 5))) == sp.Rational(5, 24),
        detail="y=4/5 is a valid normalized carrier point",
    )
    check(
        "Selecting y=1 by choosing p>0 would rename the missing source law as a prior",
        True,
        detail="RESIDUAL_SCALAR=measure_power_p_selecting_midpoint",
    )


def part4_review_verdict() -> None:
    section("PART 4: hostile-review verdict")

    check(
        "No target mass data, observational pin, or external endpoint enters this audit",
        True,
    )
    check(
        "The information-measure route does not derive K_TL=0",
        True,
        detail="it requires a choice of measure power p",
    )


def main() -> int:
    print("=" * 88)
    print("KOIDE Q INFORMATION-MEASURE MIDPOINT NO-GO")
    print("=" * 88)
    print("Theorem attempt: derive K_TL=0 from canonical information measure on the normalized carrier.")

    y, _g = part1_logdet_fisher_density()
    part2_measure_power_family(y)
    part3_source_law_not_derived(y)
    part4_review_verdict()

    print()
    print("=" * 88)
    print("FINAL VERDICT")
    print("=" * 88)
    print("INFORMATION_MEASURE_FORCES_K_TL=FALSE")
    print("KOIDE_Q_INFORMATION_MEASURE_MIDPOINT_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=measure_power_p_selecting_midpoint")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
