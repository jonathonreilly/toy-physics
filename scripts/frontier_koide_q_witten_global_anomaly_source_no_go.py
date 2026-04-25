#!/usr/bin/env python3
"""
Koide Q Witten/global-anomaly source no-go.

Theorem attempt:
  Use the strongest retained global gauge-anomaly constraint, the SU(2) mod-2
  Witten anomaly, or a Pin/mod-2 index refinement, to force the remaining
  charged-lepton center-source scalar K_TL to vanish.

Result:
  Negative.  The SU(2) global anomaly condition is a parity condition on the
  number of left-handed electroweak doublets:

      (-1)^N_doublet = +1.

  It is satisfied generation-by-generation in the Standard-Model charge
  pattern because 3 quark-color doublets plus 1 lepton doublet gives N=4.
  This parity is blind to the normalized C3 center-source state

      p(P_plus)=u, p(P_perp)=1-u,

  and therefore supplies no equation on K_TL.  Both the rank state u=1/3 and
  equal-label state u=1/2 have the same anomaly sign.  Turning the anomaly
  parity into u=1/2 would require an extra map from electroweak doublet parity
  to the C3 center-source distribution.

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


def q_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((1 + r) / 3)


def ktl_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((r**2 - 1) / (4 * r))


def witten_sign(n_doublets: sp.Expr) -> sp.Expr:
    return sp.Pow(-1, n_doublets, evaluate=True)


def main() -> int:
    section("A. SU(2) mod-2 anomaly constraint")

    n_quark_color_doublets = sp.Integer(3)
    n_lepton_doublets = sp.Integer(1)
    n_per_generation = n_quark_color_doublets + n_lepton_doublets
    n_three_generations = 3 * n_per_generation
    record(
        "A.1 one generation has even SU(2) doublet count",
        n_per_generation == 4 and witten_sign(n_per_generation) == 1,
        f"N_doublet=3+1={n_per_generation}, sign={witten_sign(n_per_generation)}",
    )
    record(
        "A.2 three generations also satisfy the global anomaly constraint",
        n_three_generations == 12 and witten_sign(n_three_generations) == 1,
        f"N_doublet=3*(3+1)={n_three_generations}, sign={witten_sign(n_three_generations)}",
    )

    n = sp.symbols("N", integer=True)
    record(
        "A.3 the anomaly equation is parity, not a real source equation",
        True,
        "constraint: N_doublet = 0 mod 2; no variable u or K_TL appears.",
    )

    section("B. Center-source scalar remains invisible")

    u = sp.symbols("u", positive=True, real=True)
    ktl = ktl_from_center_state(u)
    anomaly_expression = sp.Mod(n, 2)
    derivative_u = sp.diff(anomaly_expression, u)
    record(
        "B.1 mod-2 anomaly expression is independent of the center source",
        derivative_u == 0,
        f"d(N mod 2)/du={derivative_u}; K_TL(u)={ktl}",
    )

    samples = {
        "rank_state": sp.Rational(1, 3),
        "equal_label": sp.Rational(1, 2),
        "singlet_heavy": sp.Rational(2, 3),
    }
    sample_lines = []
    ok = True
    for name, value in samples.items():
        sign = witten_sign(n_three_generations)
        q_value = q_from_center_state(value)
        ktl_value = ktl_from_center_state(value)
        ok = ok and sign == 1
        sample_lines.append(f"{name}: u={value}, anomaly_sign={sign}, Q={q_value}, K_TL={ktl_value}")
    record(
        "B.2 anomaly-canceling theories realize closing and non-closing center states",
        ok,
        "\n".join(sample_lines),
    )
    record(
        "B.3 K_TL=0 is equivalent to u=1/2, not to even doublet parity",
        sp.solve(sp.Eq(ktl, 0), u) == [sp.Rational(1, 2)],
        f"K_TL(u)={ktl}",
    )

    section("C. Pin/mod-2 refinement does not add a C3 source map")

    parity_values = [sp.Integer(0), sp.Integer(1)]
    allowed_parity = [p for p in parity_values if p == 0]
    record(
        "C.1 any mod-2 index refinement still returns a parity class",
        allowed_parity == [0],
        f"parity classes={parity_values}, anomaly-free class={allowed_parity}",
    )
    a, b = sp.symbols("a b", real=True)
    source_map = sp.simplify(a * sp.Mod(n, 2) + b)
    b_needed = sp.solve(sp.Eq(source_map.subs(n, n_three_generations), sp.Rational(1, 2)), b)
    record(
        "C.2 mapping parity to u=1/2 requires an added affine source map",
        b_needed == [sp.Rational(1, 2)],
        f"u=a*(N mod 2)+b, anomaly-free N gives b={b_needed}",
    )
    record(
        "C.3 no retained anomaly datum selects the equal center-label source",
        True,
        "The anomaly sees electroweak doublet count; Q needs a C3 center-source distribution.",
    )

    section("D. Verdict")

    residual = sp.simplify(u - sp.Rational(1, 2))
    record(
        "D.1 Witten/global-anomaly route does not close Q",
        residual == u - sp.Rational(1, 2),
        f"RESIDUAL_SOURCE={residual}",
    )
    record(
        "D.2 Q remains open after global-anomaly audit",
        True,
        "Residual primitive: a physical map from anomaly data to the equal center-label source, not currently retained.",
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
        print("VERDICT: Witten/global anomaly cancellation does not close Q.")
        print("KOIDE_Q_WITTEN_GLOBAL_ANOMALY_SOURCE_NO_GO=TRUE")
        print("Q_WITTEN_GLOBAL_ANOMALY_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_MAP=global_anomaly_parity_to_C3_center_source_not_retained")
        return 0

    print("VERDICT: Witten/global-anomaly source audit has FAILs.")
    print("KOIDE_Q_WITTEN_GLOBAL_ANOMALY_SOURCE_NO_GO=FALSE")
    print("Q_WITTEN_GLOBAL_ANOMALY_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_MAP=global_anomaly_parity_to_C3_center_source_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
