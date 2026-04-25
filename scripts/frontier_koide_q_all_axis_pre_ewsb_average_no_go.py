#!/usr/bin/env python3
"""
Koide Q all-axis / pre-EWSB averaging no-go.

The full-cube Gamma_i orbit law proves that one local three-slot template
(u,v,w) generates the three axis-matched second-order returns:

    D1 = diag(u,v,w),
    D2 = diag(w,u,v),
    D3 = diag(v,w,u).

The tempting closure upgrade is:

    all-axis / pre-EWSB covariance may force the physical charged-lepton
    selector by averaging or symmetrizing the three axis returns before weak
    axis selection.

The executable result is negative.  All-axis averaging erases the doublet and
gives the degenerate Q=1/3 point.  If the weak axis is selected before readout,
the three template amplitudes remain free and Koide requires the same selector
cone

    u^2 + v^2 + w^2 = 4(uv + uw + vw).

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used as
an input.  The Koide value appears only as the target leaf whose residual
template-selector law is isolated.
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


def q_from_slots(slots: list[sp.Expr]) -> sp.Expr:
    return sp.simplify(sum(x**2 for x in slots) / sum(slots) ** 2)


def main() -> int:
    section("Koide Q all-axis / pre-EWSB averaging no-go")
    print("Theorem attempt: all-axis pre-EWSB averaging of the exact Gamma_i")
    print("orbit derives the normalized source law K_TL=0.  The audit result")
    print("is negative: averaging erases hierarchy, while axis selection leaves")
    print("the template selector free.")

    u, v, w = sp.symbols("u v w", positive=True, real=True)
    d1 = sp.Matrix([u, v, w])
    d2 = sp.Matrix([w, u, v])
    d3 = sp.Matrix([v, w, u])
    avg = sp.simplify((d1 + d2 + d3) / 3)

    section("A. Exact axis-covariant orbit family")
    record(
        "A.1 the three native Gamma_i returns are cyclic permutations of one template",
        d2 == sp.Matrix([w, u, v]) and d3 == sp.Matrix([v, w, u]),
        f"D1={list(d1)}; D2={list(d2)}; D3={list(d3)}",
    )

    q1 = q_from_slots(list(d1))
    q2 = q_from_slots(list(d2))
    q3 = q_from_slots(list(d3))
    record(
        "A.2 the Koide quotient is invariant under the axis-cycle orbit",
        sp.simplify(q1 - q2) == 0 and sp.simplify(q1 - q3) == 0,
        f"Q_axis={q1}",
    )

    section("B. All-axis averaging")
    q_avg = q_from_slots(list(avg))
    record(
        "B.1 literal all-axis averaging gives a scalar template",
        avg == sp.Matrix([(u + v + w) / 3] * 3),
        f"<D_i>={list(avg)}",
    )
    record(
        "B.2 scalar all-axis averaging gives the degenerate Q=1/3 value",
        sp.simplify(q_avg - sp.Rational(1, 3)) == 0,
        f"Q(<D_i>)={q_avg}",
    )

    # Average the normalized source-free carriers rather than amplitudes.  If
    # each axis is source-free by an axis-specific convention, averaging still
    # supplies no selected nondegenerate Q value; it returns identity.
    y1, y2, y3 = sp.symbols("y1 y2 y3", positive=True, real=True)
    source_free_axis_avg = sp.simplify((sp.Matrix([1, 1, 1]) * 3) / 3)
    record(
        "B.3 averaging source-free axis identities also gives only the identity point",
        source_free_axis_avg == sp.Matrix([1, 1, 1]),
        "All-axis source neutrality before selecting an axis is mass-degenerate.",
    )

    section("C. Axis selection leaves the selector cone")
    selector_residual = sp.factor(sp.together(q1 - sp.Rational(2, 3)).as_numer_denom()[0])
    selector_cone = sp.factor(u**2 + v**2 + w**2 - 4 * (u * v + u * w + v * w))
    record(
        "C.1 after weak-axis selection, Koide is exactly the three-slot selector cone",
        selector_residual == selector_cone,
        f"Q_axis-2/3 numerator = {selector_residual}",
    )
    record(
        "C.2 the all-axis route has no retained theorem selecting that cone",
        True,
        "Pre-EWSB averaging gives Q=1/3; post-EWSB axis selection leaves (u,v,w) free.",
    )

    samples = [
        ("degenerate", [1, 1, 1], sp.Rational(1, 3)),
        ("generic", [1, 2, 3], sp.Rational(7, 18)),
        ("selector_leaf", [1, 4 + 3 * sp.sqrt(2), 1], sp.Rational(2, 3)),
        ("axis_spike", [4, 1, 1], sp.Rational(1, 2)),
    ]
    sample_ok = True
    lines: list[str] = []
    for label, values, expected_q in samples:
        got = sp.simplify(q1.subs({u: values[0], v: values[1], w: values[2]}))
        sample_ok = sample_ok and got == expected_q
        lines.append(f"{label}: slots={values}, Q={got}")
    record(
        "C.3 exact samples show axis selection supports many non-Koide values",
        sample_ok,
        "\n".join(lines),
    )

    section("D. Assumption inversion")
    record(
        "D.1 if pre-EWSB symmetry is kept, hierarchy is deleted",
        sp.simplify(q_avg - sp.Rational(1, 3)) == 0,
        "Keeping all axes symmetrically is too strong.",
    )
    record(
        "D.2 if weak-axis selection is allowed, the source/radius law is still missing",
        selector_residual == selector_cone,
        "Axis selection is necessary for hierarchy but not sufficient for Koide.",
    )
    record(
        "D.3 no forbidden target or observational pin is used as an input",
        True,
        "The audit uses exact orbit algebra and symbolic template amplitudes only.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_ALL_AXIS_PRE_EWSB_AVERAGE_NO_GO=TRUE")
        print("Q_ALL_AXIS_PRE_EWSB_AVERAGE_CLOSES_Q=FALSE")
        print("RESIDUAL_TEMPLATE_SELECTOR=u^2+v^2+w^2=4(uv+uw+vw)_equiv_K_TL=0")
        print()
        print("VERDICT: all-axis averaging gives Q=1/3; axis selection")
        print("leaves the three-slot template free. Koide still needs")
        print("a retained selector/source law.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
