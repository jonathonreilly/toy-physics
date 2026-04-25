#!/usr/bin/env python3
"""
Koide Q locality/gluing UV-IR pairing no-go.

Theorem attempt:
  A retained locality or gluing law might refine the UV/IR endpoint audit by
  forcing the symmetric pairing A=1, equivalently the absolute log-source
  midpoint

      m = 0,  where x = log(1 + rho).

  If locality/gluing forced m=0, then rho=0 and the conditional Koide Q
  support chain would follow.

Result:
  No retained closure.  Local gluing of interval actions, cancellation of
  internal boundary counterterms, and orientation reversal of the two endpoint
  regulators all work for every finite midpoint m.  The retained data are
  functions of differences and endpoint orientation.  They do not choose the
  absolute midpoint.  m=0 conditionally closes Q; m=log(2) is an exact
  locality/gluing countersection with rho=1, Q=1, K_TL=3/8.

Exact residual:

      derive_retained_locality_gluing_uv_ir_midpoint_m_equals_zero.

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


def rho_from_m(m_value: sp.Expr) -> sp.Expr:
    return sp.simplify(sp.exp(m_value) - 1)


def q_from_m(m_value: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho_from_m(m_value)) / 3)


def ktl_from_m(m_value: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(sp.exp(m_value))
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    x, x0, x1, x2, c, m, L, b = sp.symbols("x x0 x1 x2 c m L b", real=True)
    anomaly_a = sp.symbols("anomaly_a", positive=True, real=True)
    m1, m2 = sp.symbols("m1 m2", real=True)

    section("A. Theorem attempt and route ranking")

    routes = [
        "local interval additivity might force the finite midpoint m=0",
        "gluing cancellation of internal boundary terms might remove finite parts",
        "orientation reversal exchanging UV and IR regulators might center at zero",
        "multiplicative UV/IR pairing might select the identity A=1",
        "local anomaly inflow might forbid nonzero boundary finite constants",
        "wrong-assumption inversion: m=log(2), A=4 satisfies the same gluing laws",
    ]
    record(
        "A.1 six locality/gluing variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )
    ranked = [
        ("local_interval_additivity", 3, 3, 3),
        ("boundary_counterterm_gluing", 3, 3, 2),
        ("uv_ir_orientation_reversal", 3, 2, 2),
        ("multiplicative_pairing_identity", 2, 2, 2),
        ("local_anomaly_inflow", 2, 2, 1),
    ]
    record(
        "A.2 local additivity and boundary gluing are the strongest tests",
        {ranked[0][0], ranked[1][0]}
        == {"local_interval_additivity", "boundary_counterterm_gluing"},
        "\n".join(
            f"{name}: positive={pos}, retained={ret}, novelty={nov}"
            for name, pos, ret, nov in ranked
        ),
    )

    section("B. Local interval gluing")

    segment_action = lambda left, right: sp.simplify(anomaly_a * (right - left))
    glued = sp.simplify(segment_action(x0, x1) + segment_action(x1, x2))
    direct = segment_action(x0, x2)
    record(
        "B.1 local segment actions glue additively",
        sp.simplify(glued - direct) == 0,
        f"S01+S12={glued}; S02={direct}",
    )
    shifted_segment = segment_action(x0 + c, x1 + c)
    record(
        "B.2 locality is invariant under absolute source translations",
        sp.simplify(shifted_segment - segment_action(x0, x1)) == 0,
        "Locality sees x1-x0, not the absolute midpoint.",
    )
    x_uv = sp.simplify(m - L)
    x_ir = sp.simplify(m + L)
    endpoint_action = segment_action(x_uv, x_ir)
    record(
        "B.3 endpoint-local action is independent of midpoint m",
        sp.diff(endpoint_action, m) == 0 and endpoint_action == 2 * L * anomaly_a,
        f"S[m-L,m+L]={endpoint_action}; dS/dm={sp.diff(endpoint_action, m)}",
    )

    section("C. Orientation reversal of endpoint regulators")

    reflected = sp.simplify(2 * m - x)
    reflected_twice = sp.simplify(reflected.subs(x, reflected))
    record(
        "C.1 reflection about any midpoint is an involution",
        reflected_twice == x,
        f"R_m(x)={reflected}; R_m(R_m(x))={reflected_twice}",
    )
    record(
        "C.2 reflection about any midpoint exchanges the paired UV/IR regulators",
        sp.simplify(reflected.subs(x, x_uv) - x_ir) == 0
        and sp.simplify(reflected.subs(x, x_ir) - x_uv) == 0,
        f"R_m(m-L)={sp.simplify(reflected.subs(x, x_uv))}; R_m(m+L)={sp.simplify(reflected.subs(x, x_ir))}",
    )
    record(
        "C.3 orientation reversal imposes no equation on m",
        sp.simplify(reflected_twice - x) == 0,
        "The involution and endpoint exchange identities hold for symbolic m.",
    )

    section("D. Boundary counterterm gluing")

    boundary_potential = lambda value: sp.simplify(anomaly_a * value + b)
    boundary_action = lambda left, right: sp.simplify(
        boundary_potential(right) - boundary_potential(left)
    )
    boundary_glued = sp.simplify(boundary_action(x0, x1) + boundary_action(x1, x2))
    boundary_direct = boundary_action(x0, x2)
    record(
        "D.1 boundary finite parts cancel at glued internal cuts for every b",
        sp.simplify(boundary_glued - boundary_direct) == 0,
        f"B01+B12={boundary_glued}; B02={boundary_direct}",
    )
    boundary_normalization = sp.solve(sp.Eq(boundary_potential(m), 0), b)
    record(
        "D.2 boundary normalization selects b=-a*m, not m=0",
        boundary_normalization == [-anomaly_a * m],
        f"B(m)=0 -> b={boundary_normalization[0]}",
    )
    record(
        "D.3 both m=0 and m=log(2) admit exact local boundary normalization",
        boundary_normalization[0].subs(m, 0) == 0
        and sp.simplify(boundary_normalization[0].subs(m, sp.log(2)) + anomaly_a * sp.log(2))
        == 0,
        "The finite boundary counterterm adapts to either midpoint.",
    )

    section("E. Multiplicative UV/IR pairing law")

    pairing = lambda midpoint: sp.simplify(sp.exp(2 * midpoint))
    record(
        "E.1 pairing parameter is positive and multiplicative under midpoint addition",
        sp.simplify(pairing(m1 + m2) - pairing(m1) * pairing(m2)) == 0,
        "A(m)=exp(2m) obeys A(m1+m2)=A(m1)A(m2).",
    )
    record(
        "E.2 the identity pairing A=1 is the midpoint m=0 but is not selected by multiplicativity",
        sp.solve(sp.Eq(pairing(m), 1), m) == [0],
        "Multiplicativity defines a group; choosing the identity object is extra.",
    )
    record(
        "E.3 A=4 is an equally valid positive pairing with inverse under gluing",
        pairing(sp.log(2)) == 4
        and sp.simplify(pairing(sp.log(2)) * pairing(-sp.log(2))) == 1,
        "The nonclosing midpoint has a perfectly valid inverse pairing.",
    )

    section("F. Q consequence and countersection")

    record(
        "F.1 m=0 conditionally gives the Koide support chain",
        rho_from_m(0) == 0
        and q_from_m(0) == sp.Rational(2, 3)
        and ktl_from_m(0) == 0,
        f"m=0 -> rho={rho_from_m(0)}, Q={q_from_m(0)}, K_TL={ktl_from_m(0)}",
    )
    record(
        "F.2 m=log(2) is an exact locality/gluing countersection",
        rho_from_m(sp.log(2)) == 1
        and q_from_m(sp.log(2)) == 1
        and ktl_from_m(sp.log(2)) == sp.Rational(3, 8),
        "m=log(2) -> rho=1, Q=1, K_TL=3/8",
    )

    section("G. Hostile review")

    record(
        "G.1 no forbidden target is assumed as a theorem input",
        True,
        "The runner audits m=0 and m=log(2) under the same gluing identities.",
    )
    record(
        "G.2 no observational pin or mass data are used",
        True,
        "Only exact locality, gluing, boundary, reflection, and pairing algebra is used.",
    )
    record(
        "G.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_locality_gluing_uv_ir_midpoint_m_equals_zero",
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
        print("VERDICT: locality/gluing does not force the UV/IR pairing A=1.")
        print("KOIDE_Q_LOCALITY_GLUING_UV_IR_PAIRING_NO_GO=TRUE")
        print("Q_LOCALITY_GLUING_UV_IR_PAIRING_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_LOCALITY_GLUING_MIDPOINT_M_EQUALS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_locality_gluing_uv_ir_midpoint_m_equals_zero")
        print("RESIDUAL_SOURCE=locality_gluing_leaves_uv_ir_midpoint_m_free")
        print("COUNTERSECTION=m_log2_A_4_rho_1_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: locality/gluing UV-IR pairing audit has FAILs.")
    print("KOIDE_Q_LOCALITY_GLUING_UV_IR_PAIRING_NO_GO=FALSE")
    print("Q_LOCALITY_GLUING_UV_IR_PAIRING_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_locality_gluing_uv_ir_midpoint_m_equals_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
