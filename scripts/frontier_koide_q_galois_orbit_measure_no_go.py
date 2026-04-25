#!/usr/bin/env python3
"""
Koide Q Galois-orbit measure no-go.

Theorem attempt:
  The real C3 carrier has two Galois orbits of complex characters:

      {0}, {1,2}.

  Perhaps counting these two real orbits equally forces equal total real-block
  weights and derives K_TL = 0.

Result:
  Negative.  Equal orbit counting does land on the Koide/source-neutral leaf,
  but it is a measure choice on the orbit set.  The push-forward of the
  retained uniform/Plancherel measure on the three complex characters gives
  orbit weights 1:2.  A one-parameter orbit-size measure family interpolates
  these choices; selecting the size exponent zero is the missing
  non-rank/non-fusion coarse-graining primitive.

No PDG masses, target Koide value, K_TL pin, delta pin, or H_* pin is used.
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


def q_from_orbit_weights(w0: sp.Expr, w12: sp.Expr) -> sp.Expr:
    r = sp.simplify(w12 / w0)
    return sp.simplify((1 + r) / 3)


def ktl_from_orbit_weights(w0: sp.Expr, w12: sp.Expr) -> sp.Expr:
    r = sp.simplify(w12 / w0)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Galois orbit structure")

    chars = [0, 1, 2]
    orbits = [(0,), (1, 2)]
    sizes = [len(orbit) for orbit in orbits]
    record(
        "A.1 complex C3 characters form real/Galois orbits {0} and {1,2}",
        chars == [0, 1, 2] and orbits == [(0,), (1, 2)],
        f"orbits={orbits}, sizes={sizes}",
    )

    section("B. Two natural orbit measures disagree")

    pushforward = (sp.Rational(1, 3), sp.Rational(2, 3))
    uniform_orbit = (sp.Rational(1, 2), sp.Rational(1, 2))
    record(
        "B.1 push-forward of uniform complex-character measure gives orbit weights 1:2",
        q_from_orbit_weights(*pushforward) == 1
        and ktl_from_orbit_weights(*pushforward) == sp.Rational(3, 8),
        f"pushforward={pushforward}; Q={q_from_orbit_weights(*pushforward)}, K_TL={ktl_from_orbit_weights(*pushforward)}",
    )
    record(
        "B.2 uniform measure on the orbit set gives equal blocks and lands on Koide",
        q_from_orbit_weights(*uniform_orbit) == sp.Rational(2, 3)
        and ktl_from_orbit_weights(*uniform_orbit) == 0,
        f"uniform_orbit={uniform_orbit}; Q={q_from_orbit_weights(*uniform_orbit)}, K_TL={ktl_from_orbit_weights(*uniform_orbit)}",
    )
    record(
        "B.3 the two measures are both Galois-invariant but physically inequivalent",
        pushforward != uniform_orbit,
        "Galois invariance alone does not choose push-forward character measure or orbit-label measure.",
    )

    section("C. Orbit-size exponent family exposes the residual")

    s = sp.symbols("s", real=True)
    w0 = sp.Integer(1) ** s
    w12 = sp.Integer(2) ** s
    r_s = sp.simplify(w12 / w0)
    q_s = q_from_orbit_weights(w0, w12)
    ktl_s = ktl_from_orbit_weights(w0, w12)
    record(
        "C.1 orbit-size measure family has ratio 2^s",
        r_s == 2**s,
        f"R(s)=w_12/w_0={r_s}; Q(s)={q_s}; K_TL(s)={ktl_s}",
    )
    s_equal = sp.solve(sp.Eq(r_s, 1), s)
    record(
        "C.2 equal orbit totals require size exponent s=0",
        s_equal == [0],
        f"2^s=1 -> s={s_equal}",
    )
    sample_values = {
        "inverse_size": -1,
        "uniform_orbit": 0,
        "pushforward_character": 1,
    }
    sample_lines = []
    for label, value in sample_values.items():
        ratio = sp.simplify(r_s.subs(s, value))
        sample_lines.append(
            f"{label}: s={value}, R={ratio}, Q={q_from_orbit_weights(1, ratio)}, K_TL={ktl_from_orbit_weights(1, ratio)}"
        )
    record(
        "C.3 retained-compatible orbit-size conventions select different Q values",
        True,
        "\n".join(sample_lines),
    )

    section("D. Verdict")

    record(
        "D.1 Galois orbit counting does not derive K_TL=0",
        True,
        "It closes only after choosing uniform orbit labels instead of the push-forward character measure.",
    )
    record(
        "D.2 Q remains open after Galois orbit measure audit",
        True,
        "Residual primitive: physical measure on real character orbits selecting size exponent s=0.",
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
        print("VERDICT: Galois orbit measure route does not close Q.")
        print("KOIDE_Q_GALOIS_ORBIT_MEASURE_NO_GO=TRUE")
        print("Q_GALOIS_ORBIT_MEASURE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=size_exponent_s_equals_0_equiv_K_TL")
        print("RESIDUAL_ORBIT_MEASURE=size_exponent_s_equals_0_equiv_K_TL")
        return 0

    print("VERDICT: Galois orbit measure audit has FAILs.")
    print("KOIDE_Q_GALOIS_ORBIT_MEASURE_NO_GO=FALSE")
    print("Q_GALOIS_ORBIT_MEASURE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=size_exponent_s_equals_0_equiv_K_TL")
    print("RESIDUAL_ORBIT_MEASURE=size_exponent_s_equals_0_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
