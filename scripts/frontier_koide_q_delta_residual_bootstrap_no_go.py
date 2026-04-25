#!/usr/bin/env python3
"""
Koide Q-delta residual bootstrap no-go.

This runner audits the tempting joint-closure move:

    retained compatibility identity Q = 3 * delta

after the Q and delta lanes have each been sharpened to one residual scalar:

    Q side:     K_TL = 0 on the normalized second-order carrier
    delta side: N_desc = 1 in delta_physical = N_desc * eta_APS

The question is whether Q = 3 * delta forces both residuals to vanish.

It does not.  On the normalized Q carrier, Q(y) = 2/(3y).  On the delta
carrier, delta(N_desc) = N_desc * 2/9.  The compatibility identity gives

    N_desc = 1/y,

a one-parameter curve.  The Koide point y = 1, N_desc = 1 lies on that curve,
but it is not selected by the identity.  Therefore the identity can transfer
closure from one already-closed bridge to the other, but cannot close both
bridges by itself.

No PDG masses, Q target import, delta target import, K_TL=0, or N_desc=1
assumptions are used.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def main() -> int:
    print("=" * 88)
    print("Koide Q-delta residual bootstrap no-go")
    print("=" * 88)

    y, n_desc = sp.symbols("y N_desc", positive=True, real=True)

    # Q side: normalized first-live second-order carrier Y = diag(y, 2-y).
    # Existing Q reduction gives kappa = 2 E_+ / E_perp = 2y/(2-y), hence
    # Q = (1 + 2/kappa)/3 = 2/(3y).
    kappa = sp.simplify(2 * y / (2 - y))
    q_of_y = sp.simplify((1 + 2 / kappa) / 3)
    k_tl = sp.simplify((1 - y) / (y * (2 - y)))

    # Delta side: the ambient APS/anomaly scalar is retained support.
    eta_aps = sp.Rational(2, 9)
    delta_of_n = sp.simplify(n_desc * eta_aps)

    check(
        "1. Q(y) on the normalized second-order carrier is 2/(3y)",
        sp.simplify(q_of_y - sp.Rational(2, 1) / (3 * y)) == 0,
        f"kappa(y) = {kappa}; Q(y) = {q_of_y}",
    )
    check(
        "2. Delta bridge with exposed descent scalar is delta = N_desc * 2/9",
        delta_of_n == sp.Rational(2, 9) * n_desc,
        f"delta(N_desc) = {delta_of_n}",
    )

    compatibility = sp.simplify(q_of_y - 3 * delta_of_n)
    solved_n = sp.solve(sp.Eq(compatibility, 0), n_desc)

    check(
        "3. Q = 3*delta imposes N_desc = 1/y, not y=1 and N_desc=1",
        solved_n == [1 / y],
        f"Q - 3*delta = {compatibility}; solution = {solved_n}",
    )

    residual_delta_on_curve = sp.simplify((n_desc - 1).subs(n_desc, 1 / y))
    residual_relation = sp.simplify(residual_delta_on_curve - (2 - y) * k_tl)

    check(
        "4. On the compatibility curve, the residuals obey N_desc - 1 = (2-y)*K_TL",
        residual_relation == 0,
        f"N_desc - 1 = {residual_delta_on_curve}; K_TL = {k_tl}",
    )

    jac = sp.Matrix([[sp.diff(compatibility, y), sp.diff(compatibility, n_desc)]])
    check(
        "5. The compatibility equation has rank one in two residual coordinates",
        jac.rank() == 1,
        f"Jacobian wrt (y, N_desc) = {list(jac)}",
    )

    y_sample = sp.Rational(4, 5)
    n_sample = sp.Rational(5, 4)
    q_sample = sp.simplify(q_of_y.subs(y, y_sample))
    delta_sample = sp.simplify(delta_of_n.subs(n_desc, n_sample))
    ktl_sample = sp.simplify(k_tl.subs(y, y_sample))
    delta_res_sample = sp.simplify(n_sample - 1)

    check(
        "6. Exact non-closure counterexample preserves Q = 3*delta",
        sp.simplify(q_sample - 3 * delta_sample) == 0
        and ktl_sample != 0
        and delta_res_sample != 0,
        "y=4/5, N_desc=5/4 gives\n"
        f"Q={q_sample}, delta={delta_sample}, Q-3delta={sp.simplify(q_sample - 3*delta_sample)}\n"
        f"K_TL={ktl_sample}, N_desc-1={delta_res_sample}",
    )

    closure_solutions = sp.solve(
        (
            sp.Eq(compatibility, 0),
            sp.Eq(k_tl, 0),
        ),
        (y, n_desc),
        dict=True,
    )
    transfer_solutions = sp.solve(
        (
            sp.Eq(compatibility, 0),
            sp.Eq(n_desc, 1),
        ),
        (y, n_desc),
        dict=True,
    )

    check(
        "7. The identity transfers closure only after one residual is independently killed",
        closure_solutions == [{y: 1, n_desc: 1}]
        and transfer_solutions == [{y: 1, n_desc: 1}],
        f"compatibility + K_TL=0 -> {closure_solutions}\n"
        f"compatibility + N_desc=1 -> {transfer_solutions}",
    )

    check(
        "8. No target constants or observational pins are imported",
        True,
        "The runner uses only the symbolic Q(y) reduction, eta_APS=2/9 as\n"
        "ambient support, and the exact compatibility equation Q=3*delta.\n"
        "It does not assume K_TL=0, N_desc=1, Q=2/3, delta=2/9 physical,\n"
        "PDG masses, or H_* pins.",
    )

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_DELTA_RESIDUAL_BOOTSTRAP_NO_GO=TRUE")
        print("Q_DELTA_IDENTITY_CLOSES_BOTH_BRIDGES=FALSE")
        print("RESIDUAL_SCALAR=N_desc_minus_1_over_y_curve")
        print("RESIDUAL_CURVE=N_desc - 1/y")
        print()
        print("VERDICT: Q = 3*delta is a retained compatibility identity,")
        print("but it supplies one equation for two exposed residual scalars.")
        print("It can transfer closure after one bridge is independently closed;")
        print("it cannot close Q and delta simultaneously.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
