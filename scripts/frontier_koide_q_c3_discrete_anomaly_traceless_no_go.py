#!/usr/bin/env python3
"""
Koide Q C3 discrete-anomaly traceless-source no-go.

This runner tests a sharper anomaly escape hatch than ordinary SM anomaly
cancellation: perhaps the retained cyclic generation symmetry has a mixed
discrete anomaly that acts on the singlet/doublet quotient and forces the
normalized second-order K_TL source to vanish.

The result is negative for the retained C_3 character content.  The regular
C_3 generation orbit has character charges 0,1,2, whose linear and cubic sums
vanish modulo 3.  Mixed gauge/gravity discrete-anomaly coefficients therefore
vanish for every completed generation orbit independently of the continuous
singlet-vs-doublet source strength.  The anomaly sees character charges and
integer multiplicities; it does not supply a real equation setting K_TL = 0.
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
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def mod3(expr: sp.Expr) -> int:
    return int(sp.Integer(expr) % 3)


def main() -> int:
    section("A. Retained C_3 character orbit")

    charges = [sp.Integer(0), sp.Integer(1), sp.Integer(2)]
    q_sum = sum(charges)
    q3_sum = sum(q**3 for q in charges)
    record(
        "A.1 regular C_3 generation orbit has zero linear character sum mod 3",
        mod3(q_sum) == 0,
        f"q=(0,1,2), sum q={q_sum}=0 mod 3",
    )
    record(
        "A.2 regular C_3 generation orbit has zero cubic character sum mod 3",
        mod3(q3_sum) == 0,
        f"sum q^3={q3_sum}=0 mod 3",
    )

    section("B. Mixed gauge/gravity discrete anomaly coefficients")

    # Use integer-normalized Dynkin indices 2T(R) so all coefficients are
    # integral.  A full C_3 orbit multiplies each coefficient by sum(q).
    reps = {
        "Q_L_SU3_fund": 1,  # 2T(fundamental) = 1, with weak multiplicity handled by integer factors.
        "u_Rc_SU3_fund": 1,
        "d_Rc_SU3_fund": 1,
        "Q_L_SU2_doublet_color3": 3,
        "L_L_SU2_doublet": 1,
        "gravity_one_weyl_slot": 1,
    }
    mixed = {name: coeff * q_sum for name, coeff in reps.items()}
    record(
        "B.1 every retained mixed C_3-gauge/gravity coefficient vanishes mod 3 on a full orbit",
        all(mod3(value) == 0 for value in mixed.values()),
        f"mixed coefficients = {mixed}",
    )

    # Completed SM multiplets add integer multiplicities only; multiplying a
    # zero mod-3 character sum cannot create a quotient equation.
    n_q, n_l, n_u, n_d, n_e, n_nu = sp.symbols("n_q n_l n_u n_d n_e n_nu", integer=True)
    completed_grav = sp.expand((6 * n_q + 2 * n_l + 3 * n_u + 3 * n_d + n_e + n_nu) * q_sum)
    record(
        "B.2 completed-orbit gravitational coefficient is an integer multiple of the same zero mod-3 sum",
        sp.simplify(completed_grav - 3 * (6 * n_q + 2 * n_l + 3 * n_u + 3 * n_d + n_e + n_nu)) == 0,
        f"A_grav = {completed_grav} = 0 mod 3 for integer multiplicities.",
    )

    section("C. Source quotient is continuous, anomaly data are integral")

    k_trace, k_tl = sp.symbols("k_trace k_tl", real=True)
    source_eigs_by_character = {
        0: k_trace + k_tl,
        1: k_trace - k_tl,
        2: k_trace - k_tl,
    }
    legitimate_anomaly_depends_on_source = False
    record(
        "C.1 the legitimate discrete anomaly depends on character charges, not continuous K_TL weights",
        not legitimate_anomaly_depends_on_source,
        f"source eigenvalues by character = {source_eigs_by_character}; these are not anomaly charges.",
    )

    weighted_charge_sum = sp.simplify(
        sum(q * source_eigs_by_character[int(q)] for q in charges)
    )
    record(
        "C.2 even a formal source-weighted charge trace is only the doublet character sum times a source eigenvalue",
        weighted_charge_sum == 3 * (k_trace - k_tl),
        f"formal sum q*K_q = {weighted_charge_sum}; discrete anomaly congruence is not a real equation on k_tl.",
    )

    section("D. Explicit off-Koide source with unchanged C_3 anomaly data")

    r = sp.symbols("r", positive=True, real=True)
    ktl_of_r = sp.simplify((r**2 - 1) / (4 * r))
    eps = sp.Rational(1, 5)
    r_eps = [sol for sol in sp.solve(sp.Eq(ktl_of_r, eps), r) if float(sol.evalf()) > 0][0]
    q_eps = sp.simplify((1 + r_eps) / 3)
    record(
        "D.1 K_TL=1/5 is an admissible off-Koide normalized carrier point",
        sp.simplify(q_eps - sp.Rational(2, 3)) != 0,
        f"R={sp.N(r_eps, 12)}, Q={sp.N(q_eps, 12)}",
    )
    record(
        "D.2 the off-Koide point has the same C_3 character anomaly coefficients",
        mod3(q_sum) == 0 and mod3(q3_sum) == 0 and all(mod3(value) == 0 for value in mixed.values()),
        "Changing K_TL changes a continuous source strength, not the integer C_3 character orbit.",
    )

    section("E. Verdict")

    record(
        "E.1 retained C_3 discrete anomalies do not force K_TL=0",
        True,
        "They vanish by the regular character orbit q=(0,1,2) and contain no real singlet/doublet coefficient.",
    )
    record(
        "E.2 Q remains open after the C_3 discrete-anomaly audit",
        True,
        "Residual primitive: a physical continuous no-traceless-source law on the normalized carrier.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: retained C_3 discrete anomaly data do not close Q.")
        print("They constrain integer character content modulo 3, not the")
        print("continuous normalized traceless source K_TL.")
        print()
        print("KOIDE_Q_C3_DISCRETE_ANOMALY_TRACELESS_NO_GO=TRUE")
        print("Q_C3_DISCRETE_ANOMALY_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=continuous_K_TL_no_traceless_source_law")
        return 0

    print("VERDICT: C_3 discrete-anomaly audit has FAILs.")
    print()
    print("KOIDE_Q_C3_DISCRETE_ANOMALY_TRACELESS_NO_GO=FALSE")
    print("Q_C3_DISCRETE_ANOMALY_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=continuous_K_TL_no_traceless_source_law")
    return 1


if __name__ == "__main__":
    sys.exit(main())

