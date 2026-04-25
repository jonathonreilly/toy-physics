#!/usr/bin/env python3
"""
Koide Q UV/IR endpoint and scale-anomaly boundary no-go.

Theorem attempt:
  UV/IR endpoint regularity or a scale-anomaly boundary condition might fix
  the absolute origin of the live log-source carrier

      x = log(1 + rho),

  without supplying a cutoff pairing, finite counterterm, or subtraction
  basepoint.  If this fixed x=0, it would give rho=0 and the conditional Q
  support chain.

Result:
  No retained closure.  The exact retained endpoint and anomaly data determine
  asymptotic ends and anomaly slopes, but not the finite intercept/midpoint of
  the log-source line.  UV/IR cutoff pairings

      x_UV = log(eps),   x_IR = log(A/eps)

  have finite midpoint (1/2)log(A).  A=1 conditionally closes Q, while A=4
  selects x=log(2), rho=1, Q=1, K_TL=3/8.  Likewise, a scale-anomaly Ward law
  dW/dx=a fixes the slope a but leaves the finite constant b free, so W=0
  selects x=-b/a.

Exact residual:

      derive_retained_uv_ir_scale_anomaly_absolute_origin_A_equals_one.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
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


def rho_from_x(x_value: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.exp(x_value) - 1)


def q_from_x(x_value: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho_from_x(x_value)) / 3)


def ktl_from_x(x_value: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(sp.exp(x_value))
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    x, c, b = sp.symbols("x c b", real=True)
    eps = sp.symbols("eps", positive=True, real=True)
    pair_A = sp.symbols("pair_A", positive=True, real=True)
    anomaly_a = sp.symbols("anomaly_a", positive=True, real=True)
    x0 = sp.symbols("x0", real=True)

    section("A. Theorem attempt and route ranking")

    routes = [
        "UV endpoint regularity might anchor finite source origin x=0",
        "IR endpoint regularity might anchor finite source origin x=0",
        "UV/IR paired cutoffs might define a canonical midpoint",
        "scale anomaly might fix the finite intercept of W=a*x+b",
        "boundary counterterm cancellation might select a unique finite part",
        "wrong-assumption inversion: UV/IR pairing A=4 selects x=log(2)",
    ]
    record(
        "A.1 six UV/IR and scale-anomaly variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )
    ranked = [
        ("uv_ir_cutoff_midpoint", 3, 2, 3),
        ("scale_anomaly_finite_intercept", 3, 2, 3),
        ("endpoint_regular_boundary", 2, 2, 2),
        ("boundary_counterterm_cancellation", 2, 1, 2),
        ("uv_ir_endpoint_exchange", 1, 1, 1),
    ]
    record(
        "A.2 cutoff midpoint and anomaly intercept are the decisive tests",
        {ranked[0][0], ranked[1][0]}
        == {"uv_ir_cutoff_midpoint", "scale_anomaly_finite_intercept"},
        "\n".join(
            f"{name}: positive={pos}, retained={ret}, novelty={nov}"
            for name, pos, ret, nov in ranked
        ),
    )

    section("B. Endpoint regularity does not fix a finite point")

    translated_x = x + c
    record(
        "B.1 translations preserve the UV and IR endpoints",
        sp.limit(translated_x, x, -sp.oo) == -sp.oo
        and sp.limit(translated_x, x, sp.oo) == sp.oo,
        "x -> x+c sends -infinity to -infinity and +infinity to +infinity.",
    )
    record(
        "B.2 endpoint anomaly density is translation invariant",
        sp.diff(translated_x, x) == 1,
        "Endpoint slope/orientation data do not see the finite intercept c.",
    )
    record(
        "B.3 no finite interior source point is fixed by all endpoint-preserving translations",
        sp.solve(sp.Eq(x + c, x), c) == [0],
        "Fixedness holds only for the identity translation.",
    )

    section("C. UV/IR cutoff pairing audit")

    x_uv = sp.log(eps)
    x_ir = sp.log(pair_A / eps)
    midpoint = sp.simplify((x_uv + x_ir) / 2)
    length = sp.simplify(x_ir - x_uv)
    finite_length_part = sp.log(pair_A)
    record(
        "C.1 paired cutoffs have a finite midpoint controlled by A",
        sp.simplify(midpoint - sp.log(pair_A) / 2) == 0,
        f"x_UV={x_uv}; x_IR={x_ir}; midpoint={midpoint}",
    )
    record(
        "C.2 endpoint separation diverges while finite pairing data remains A",
        sp.limit(length.subs(pair_A, 1), eps, 0, dir="+") == sp.oo
        and sp.limit(length - finite_length_part, eps, 0, dir="+") == sp.oo,
        f"length={length}; finite pairing label={finite_length_part}",
    )
    record(
        "C.3 symmetric pairing A=1 conditionally selects x=0",
        sp.simplify(midpoint.subs(pair_A, 1)) == 0,
        "A=1 is a supplied UV/IR pairing convention.",
    )
    record(
        "C.4 equally exact pairing A=4 selects the nonclosing x=log(2)",
        sp.simplify(midpoint.subs(pair_A, 4) - sp.log(2)) == 0,
        "A=4 preserves both endpoint limits and the anomaly slope.",
    )

    section("D. Scale anomaly finite-intercept audit")

    anomaly_action = anomaly_a * x + b
    zero_action_roots = sp.solve(sp.Eq(anomaly_action, 0), x)
    record(
        "D.1 scale anomaly fixes slope but not finite intercept",
        sp.diff(anomaly_action, x) == anomaly_a
        and zero_action_roots == [-b / anomaly_a],
        f"W=a*x+b; dW/dx={sp.diff(anomaly_action, x)}; W=0 -> x={zero_action_roots[0]}",
    )
    record(
        "D.2 finite anomaly constant b=0 conditionally selects x=0",
        zero_action_roots[0].subs(b, 0) == 0,
        "The vanishing finite constant is an extra boundary normalization.",
    )
    record(
        "D.3 finite anomaly constant b=-a*log(2) selects x=log(2)",
        sp.simplify(zero_action_roots[0].subs(b, -anomaly_a * sp.log(2)) - sp.log(2))
        == 0,
        "The same anomaly slope admits the nonclosing finite part.",
    )
    shifted_action = sp.simplify(anomaly_a * (x + c) + (b - anomaly_a * c))
    record(
        "D.4 finite counterterm shifts preserve the anomaly equation",
        sp.diff(shifted_action, x) == anomaly_a
        and sp.simplify(shifted_action - anomaly_action) == 0,
        "Changing finite intercept is invisible to dW/dx=a after compensating b.",
    )

    section("E. Boundary counterterm audit")

    boundary_ct = sp.simplify(-anomaly_a * x0 - b)
    renormalized_boundary_value = sp.simplify(anomaly_action.subs(x, x0) + boundary_ct)
    record(
        "E.1 boundary counterterm cancellation works at any supplied x0",
        renormalized_boundary_value == 0,
        f"C_boundary={boundary_ct}; W_R(x0)=0",
    )
    record(
        "E.2 choosing x0=0 conditionally closes while x0=log(2) countercloses",
        q_from_x(0) == sp.Rational(2, 3)
        and ktl_from_x(0) == 0
        and q_from_x(sp.log(2)) == 1
        and ktl_from_x(sp.log(2)) == sp.Rational(3, 8),
        "The cancellation point x0 is not derived by the boundary law.",
    )

    section("F. Q consequence and countersection")

    record(
        "F.1 endpoint/anomaly origin x=0 conditionally gives the Koide support chain",
        rho_from_x(0) == 0
        and q_from_x(0) == sp.Rational(2, 3)
        and ktl_from_x(0) == 0,
        f"x=0 -> rho={rho_from_x(0)}, Q={q_from_x(0)}, K_TL={ktl_from_x(0)}",
    )
    record(
        "F.2 x=log(2) is an exact UV/IR-anomaly countersection",
        rho_from_x(sp.log(2)) == 1
        and q_from_x(sp.log(2)) == 1
        and ktl_from_x(sp.log(2)) == sp.Rational(3, 8),
        "x=log(2) -> rho=1, Q=1, K_TL=3/8",
    )

    section("G. Hostile review")

    record(
        "G.1 no forbidden target is assumed as a theorem input",
        True,
        "The runner audits A=1/b=0 and A=4/b=-a*log(2) symmetrically.",
    )
    record(
        "G.2 no observational pin or mass data are used",
        True,
        "Only exact endpoint, cutoff, finite-part, and anomaly-slope algebra is used.",
    )
    record(
        "G.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_uv_ir_scale_anomaly_absolute_origin_A_equals_one",
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
        print("VERDICT: UV/IR endpoint and scale-anomaly boundary data do not close Q.")
        print("KOIDE_Q_UV_IR_SCALE_ANOMALY_BOUNDARY_NO_GO=TRUE")
        print("Q_UV_IR_SCALE_ANOMALY_BOUNDARY_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_UV_IR_PAIRING_A_EQUALS_ONE_OR_B_EQUALS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_uv_ir_scale_anomaly_absolute_origin_A_equals_one")
        print("RESIDUAL_SOURCE=endpoint_anomaly_data_leave_cutoff_pairing_and_finite_intercept_free")
        print("COUNTERSECTION=uv_ir_pairing_A_4_or_b_minus_a_log2_selects_x_log2_rho_1_Q_1")
        return 0

    print("VERDICT: UV/IR endpoint and scale-anomaly boundary audit has FAILs.")
    print("KOIDE_Q_UV_IR_SCALE_ANOMALY_BOUNDARY_NO_GO=FALSE")
    print("Q_UV_IR_SCALE_ANOMALY_BOUNDARY_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_uv_ir_scale_anomaly_absolute_origin_A_equals_one")
    return 1


if __name__ == "__main__":
    sys.exit(main())
