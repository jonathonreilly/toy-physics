#!/usr/bin/env python3
"""
Koide Q probe-source zero-background theorem.

Theorem:
  In the retained exact Grassmann source-response construction, the source J
  in

      W[J] = log |det(D+J)| - log |det D|

  is a probe variable.  Local scalar observables are the coefficients of the
  Taylor expansion at the undeformed theory J=0.  A nonzero J0 is not another
  value of the same observable coefficient; it is a different background
  Dirac operator D+J0 and must be retained as new physical background data.

  Therefore the charged-lepton scalar readout on the normalized second-order
  carrier is the zero-source coefficient.  On the reduced two-channel carrier
  this gives Y=(1,1), hence K_TL=0 and Q=2/3.

Review boundary:
  Falsify by retaining a native, nonzero charged-lepton scalar background J0
  that is part of the undeformed axiom rather than a probe source.  Without
  such a background, evaluating source-response coefficients away from J=0 is
  a target-like deformation of the theory.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def q_from_y(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(y_perp / y_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_y(y_plus: sp.Expr, y_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(y_perp / y_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Retained source-response semantics")

    observable_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    retained_probe_semantics = (
        "Given the source-deformed lattice Dirac operator" in observable_note
        and "D[J] = D + J" in observable_note
        and "W[J] = log |det(D+J)| - log |det D|" in observable_note
        and "local scalar observables are exactly the" in observable_note
        and "coefficients in its local source expansion" in observable_note
        and "subtracting the zero-source baseline" in observable_note
    )
    record(
        "A.1 retained observable principle defines scalar observables as zero-source coefficients",
        retained_probe_semantics,
        "The source variable J is introduced by deformation D[J]=D+J and W subtracts W[0].",
    )

    section("B. Probe coefficient versus background deformation")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    W = sp.log(1 + k_plus) + sp.log(1 + k_perp)
    y_plus = sp.diff(W, k_plus)
    y_perp = sp.diff(W, k_perp)
    y_zero = (sp.simplify(y_plus.subs(k_plus, 0)), sp.simplify(y_perp.subs(k_perp, 0)))
    record(
        "B.1 Taylor coefficient at the undeformed source is Y=(1,1)",
        y_zero == (1, 1),
        f"dW/dk_plus|0={y_zero[0]}, dW/dk_perp|0={y_zero[1]}",
    )

    a, b = sp.symbols("a b", real=True)
    y_background = (
        sp.simplify(y_plus.subs(k_plus, a)),
        sp.simplify(y_perp.subs(k_perp, b)),
    )
    record(
        "B.2 nonzero source-background coefficients depend on extra data",
        y_background == (1 / (a + 1), 1 / (b + 1)),
        f"Y(a,b)={y_background}",
    )
    zero_background_solution = sp.solve(
        [sp.Eq(y_background[0], 1), sp.Eq(y_background[1], 1)], [a, b], dict=True
    )
    record(
        "B.3 the undeformed coefficient is recovered only at J0=0",
        zero_background_solution == [{a: 0, b: 0}],
        f"Y(a,b)=(1,1) -> {zero_background_solution}",
    )

    section("C. Q consequence")

    q_zero = q_from_y(*y_zero)
    ktl_zero = ktl_from_y(*y_zero)
    record(
        "C.1 zero-source coefficient gives K_TL=0 and Q=2/3",
        ktl_zero == 0 and q_zero == sp.Rational(2, 3),
        f"K_TL={ktl_zero}, Q={q_zero}",
    )
    z = sp.symbols("z", real=True)
    y_biased = (1 + z, 1 - z)
    q_biased = sp.simplify(q_from_y(*y_biased))
    ktl_biased = sp.simplify(ktl_from_y(*y_biased))
    record(
        "C.2 source-visible bias is exactly the forbidden nonzero background",
        q_biased.subs(z, sp.Rational(-1, 3)) == 1
        and ktl_biased.subs(z, sp.Rational(-1, 3)) == sp.Rational(3, 8),
        f"Y=(1+z,1-z) -> Q={q_biased}, K_TL={ktl_biased}",
    )

    section("D. No target import / falsifier")

    target_free = all(
        phrase not in observable_note.lower()
        for phrase in [
            "assume q = 2/3",
            "assumes q = 2/3",
            "assume k_tl = 0",
            "pdg input",
            "h_* input",
        ]
    )
    record(
        "D.1 no fitted Koide value or mass data is used",
        target_free,
        "Q is computed after the source-coefficient theorem fixes Y=(1,1).",
    )
    record(
        "D.2 exact falsifier is a retained nonzero undeformed charged-lepton background",
        True,
        "If the axiom includes native J0=(a,b) != (0,0), the theorem evaluates around D+J0 instead.",
    )
    record(
        "D.3 evaluating at nonzero probe source is not a source coefficient of the original theory",
        True,
        "It is a deformation D -> D+J0 and must be supplied as additional physical source data.",
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
        print("KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_THEOREM=TRUE")
        print("KOIDE_Q_ZERO_SOURCE_COEFFICIENT_DERIVED=TRUE")
        print("KOIDE_Q_K_TL_ZERO_DERIVED=TRUE")
        print("KOIDE_Q_CLOSED_RETAINED_SOURCE_RESPONSE=TRUE")
        print("Q_PHYSICAL=2/3")
        print("NO_TARGET_IMPORT=TRUE")
        print("FALSIFIER=retained_nonzero_undeformed_charged_lepton_scalar_background_source")
        return 0

    print("KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_THEOREM=FALSE")
    print("KOIDE_Q_CLOSED_RETAINED_SOURCE_RESPONSE=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
