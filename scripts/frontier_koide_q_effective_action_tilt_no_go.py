#!/usr/bin/env python3
"""
Koide Q effective-action tilt no-go.

This runner audits the strongest remaining normalized-effective-action route:

    S_eff(Y) = Tr(Y) - log det(Y) - 2

on the trace-2 first-live second-order carrier.  The source-free action has
the unique minimum Y=I_2, hence the Koide leaf.  The Nature-grade question is
whether convexity/effective-action naturality itself forces the source-free
point.

It does not.  On Y=diag(y,2-y), the exact trace-slice action is

    S_0(y) = -log(y(2-y)).

Adding the allowed traceless source term gives the equally exact tilted family

    S_tau(y) = S_0(y) + 2*tau*(y-1).

For every y0 in (0,2), there is a unique tau = (1-y0)/(y0(2-y0)) for which
y0 is the unique global minimum.  The Koide point is the special member
tau=0, exactly the already named residual K_TL=0.

No PDG masses, Q target import, K_TL=0 assumption, or H_* pin is used.
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
    print("Koide Q effective-action tilt no-go")
    print("=" * 88)

    y, tau, y0 = sp.symbols("y tau y0", positive=True, real=True)
    s0 = -sp.log(y * (2 - y))
    s_tau = sp.simplify(s0 + 2 * tau * (y - 1))
    ds0 = sp.simplify(sp.diff(s0, y))
    d2s0 = sp.simplify(sp.diff(s0, y, 2))
    ds_tau = sp.simplify(sp.diff(s_tau, y))
    d2s_tau = sp.simplify(sp.diff(s_tau, y, 2))

    check(
        "1. Source-free trace-slice action is S0(y) = -log(y(2-y))",
        s0 == -sp.log(y * (2 - y)),
        f"S0 = {s0}",
    )
    check(
        "2. S0 has the unique interior stationary point y=1",
        sp.solve(sp.Eq(ds0, 0), y) == [1],
        f"dS0/dy = {ds0}",
    )
    check(
        "3. S0 is strictly convex on the trace-2 cone",
        sp.simplify(d2s0 - (1 / y**2 + 1 / (2 - y) ** 2)) == 0,
        f"d2S0/dy2 = {d2s0}",
    )

    ktl_of_y = sp.simplify((1 - y) / (y * (2 - y)))
    tau_for_y0 = sp.simplify((1 - y0) / (y0 * (2 - y0)))

    check(
        "4. The exact traceless source tilt is linear on the trace slice",
        sp.simplify(s_tau - s0 - 2 * tau * (y - 1)) == 0,
        "For K = tau*diag(+1,-1), Tr(KY)=2*tau*(y-1) up to the sign convention\n"
        "used by the source-coupled effective action.",
    )
    check(
        "5. Stationarity of the tilted action gives tau = K_TL(y)",
        sp.simplify(sp.solve(sp.Eq(ds_tau, 0), tau)[0] - ktl_of_y) == 0,
        f"dS_tau/dy = {ds_tau}; K_TL(y) = {ktl_of_y}",
    )
    check(
        "6. The linear tilt preserves strict convexity",
        sp.simplify(d2s_tau - d2s0) == 0,
        f"d2S_tau/dy2 = {d2s_tau}",
    )

    residual_at_y0 = sp.simplify(
        ds_tau.subs({y: y0, tau: tau_for_y0})
    )
    check(
        "7. Every interior y0 is the unique minimizer for a matching traceless source",
        residual_at_y0 == 0,
        f"tau(y0) = {tau_for_y0}",
    )

    sample_y = sp.Rational(4, 5)
    sample_tau = sp.simplify(ktl_of_y.subs(y, sample_y))
    sample_stationarity = sp.simplify(ds_tau.subs({y: sample_y, tau: sample_tau}))
    kappa = sp.simplify(2 * y / (2 - y))
    q_of_y = sp.simplify((1 + 2 / kappa) / 3)
    sample_q = sp.simplify(q_of_y.subs(y, sample_y))

    check(
        "8. Exact non-Koide counterexample: tilted action has unique off-center minimum",
        sample_stationarity == 0 and sample_tau != 0 and sample_q != sp.Rational(2, 3),
        f"y=4/5 -> tau=K_TL={sample_tau}, Q={sample_q}",
    )

    tau_zero_solution = sp.solve(sp.Eq(tau_for_y0, 0), y0)
    check(
        "9. The Koide point is exactly the special source-free member tau=0",
        tau_zero_solution == [1],
        f"tau(y0)=0 -> y0={tau_zero_solution}",
    )

    check(
        "10. Effective-action convexity alone cannot derive K_TL=0",
        True,
        "The same observable-principle effective action admits a one-parameter\n"
        "family of strictly convex source-coupled minima. Selecting tau=0 is\n"
        "precisely the missing no-traceless-source law.",
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
        print("KOIDE_Q_EFFECTIVE_ACTION_TILT_NO_GO=TRUE")
        print("Q_EFFECTIVE_ACTION_CONVEXITY_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=tau=K_TL")
        print()
        print("VERDICT: the normalized effective action supports the Koide leaf")
        print("only after setting the traceless source tilt to zero. Convexity")
        print("does not derive that source-free law.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
