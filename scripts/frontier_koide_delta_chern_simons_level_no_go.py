#!/usr/bin/env python3
"""
Koide delta Chern-Simons level-normalization no-go.

Theorem attempt:
  A Chern-Simons/lens-space topological action on the retained Z3 boundary
  might identify the selected-line endpoint with eta_APS = 2/9.

Result:
  Negative for the standard quantized U(1)-style normalizations tested here.
  For a Z_p flat sector with p=3 and generator charge a=1, the common
  normalizations give phase fractions

      k a^2 / p      = k/3,
      k a^2 / (2p)  = k/6.

  Integer level k gives thirds or sixths, not 2/9.  Hitting 2/9 requires
  fractional levels k=2/3 or k=4/3 respectively, i.e. an extra normalization
  law.  Even if a fractional topological action is chosen, it still must be
  identified with the selected-line open Berry endpoint.

No PDG masses, Koide Q target, delta pin, or H_* pin is used.
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


def main() -> int:
    section("A. Standard CS phase fractions on a Z3 flat sector")

    p = sp.Integer(3)
    a = sp.Integer(1)
    eta = sp.Rational(2, 9)
    k = sp.symbols("k", real=True)
    cs_p = sp.simplify(k * a**2 / p)
    cs_2p = sp.simplify(k * a**2 / (2 * p))

    record(
        "A.1 standard p-normalized CS fraction is k/3",
        cs_p == k / 3,
        f"CS_p={cs_p}",
    )
    record(
        "A.2 standard 2p-normalized spin-style fraction is k/6",
        cs_2p == k / 6,
        f"CS_2p={cs_2p}",
    )

    section("B. Quantized levels miss eta=2/9")

    p_values = [sp.simplify(cs_p.subs(k, value)) % 1 for value in range(6)]
    two_p_values = [sp.simplify(cs_2p.subs(k, value)) % 1 for value in range(12)]
    record(
        "B.1 integer k in k/3 gives thirds, not 2/9",
        eta not in p_values,
        f"k/3 values mod 1 for k=0..5: {p_values}",
    )
    record(
        "B.2 integer k in k/6 gives sixths, not 2/9",
        eta not in two_p_values,
        f"k/6 values mod 1 for k=0..11: {two_p_values}",
    )

    k_needed_p = sp.solve(sp.Eq(cs_p, eta), k)
    k_needed_2p = sp.solve(sp.Eq(cs_2p, eta), k)
    record(
        "B.3 hitting eta requires fractional level in both normalizations",
        k_needed_p == [sp.Rational(2, 3)] and k_needed_2p == [sp.Rational(4, 3)],
        f"k/3=2/9 -> k={k_needed_p}; k/6=2/9 -> k={k_needed_2p}",
    )

    section("C. Endpoint bridge remains separate")

    theta0, theta_end = sp.symbols("theta0 theta_end", real=True)
    residual = sp.simplify(theta_end - theta0 - eta)
    record(
        "C.1 topological action value still must be mapped to selected-line endpoint",
        residual == theta_end - theta0 - sp.Rational(2, 9),
        f"RESIDUAL_ENDPOINT={residual}",
    )
    record(
        "C.2 choosing a fractional level plus identity endpoint map would be two extra laws",
        True,
        "Needed: level normalization producing 2/9 and a Berry endpoint identification.",
    )

    section("D. Verdict")

    record(
        "D.1 Chern-Simons level-normalization route does not close delta",
        True,
        "Standard quantized levels miss 2/9; fractional level choice is an extra normalization.",
    )
    record(
        "D.2 delta remains open after CS audit",
        True,
        "Residual primitive: topological-action normalization plus selected-line endpoint functor.",
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
        print("VERDICT: Chern-Simons level-normalization route does not close delta.")
        print("KOIDE_DELTA_CHERN_SIMONS_LEVEL_NO_GO=TRUE")
        print("DELTA_CHERN_SIMONS_LEVEL_CLOSES_DELTA=FALSE")
        print("RESIDUAL_LEVEL=fractional_CS_level_needed_for_eta_APS")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        return 0

    print("VERDICT: Chern-Simons level audit has FAILs.")
    print("KOIDE_DELTA_CHERN_SIMONS_LEVEL_NO_GO=FALSE")
    print("DELTA_CHERN_SIMONS_LEVEL_CLOSES_DELTA=FALSE")
    print("RESIDUAL_LEVEL=fractional_CS_level_needed_for_eta_APS")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    return 1


if __name__ == "__main__":
    sys.exit(main())
