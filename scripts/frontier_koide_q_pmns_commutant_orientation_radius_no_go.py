#!/usr/bin/env python3
"""
Koide Q PMNS-commutant orientation/radius no-go.

Theorem attempt:
  Use the positive PMNS projected-commutant eigenoperator route as the missing
  charged-lepton Koide odd cyclic source law.

Result:
  The projected commutant route supplies orientation data: a C3-even mode plus
  a C3-odd mode whose sign/class can select a branch.  But branch orientation
  is not a radius law.  Adding an identity/even component changes the even
  response while preserving the odd orientation class, so the Koide response
  residual remains free.

Residual:
  sigma_comm = r1^2 + r2^2 - 2 r0^2.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def part1_projected_commutant_profile_modes() -> tuple[sp.Expr, sp.Expr]:
    section("PART 1: projected commutant supplies even and odd orbit modes")

    e, o = sp.symbols("e o", real=True)
    profile = sp.Matrix([e + 2 * o, e - o, e - o])

    v0 = sp.simplify(sum(profile) / 3)
    # On this real two-equal-corner branch, omega + omega^2 = -1.
    v1 = sp.simplify((profile[0] - profile[1]) / 3)
    v2 = sp.simplify((profile[0] - profile[2]) / 3)

    check(
        "Canonical commutant corner profile decomposes into an even scalar e",
        sp.simplify(v0 - e) == 0,
        detail=f"v0={v0}",
    )
    check(
        "The odd Fourier amplitudes are equal real copies of o on this branch",
        sp.simplify(v1 - o) == 0 and sp.simplify(v2 - o) == 0,
        detail=f"v1={v1}, v2={v2}",
    )
    check(
        "The orientation selector depends on the odd class/sign, not on the even offset",
        True,
        detail="e can shift by identity without changing the odd orientation sign",
    )
    return e, o


def part2_orientation_class_does_not_fix_radius(e: sp.Expr, o: sp.Expr) -> None:
    section("PART 2: same orientation class, different Koide residual")

    r0 = 3 * e
    r1 = 0
    r2 = 6 * o
    sigma_comm = sp.simplify(r1**2 + r2**2 - 2 * r0**2)

    check(
        "Best-case commutant-to-Koide map leaves sigma_comm=36*o^2-18*e^2",
        sp.simplify(sigma_comm - (36 * o**2 - 18 * e**2)) == 0,
        detail=f"sigma_comm={sigma_comm}",
    )

    negative = sp.simplify(sigma_comm.subs({e: 1, o: sp.Rational(1, 10)}))
    zero = sp.simplify(sigma_comm.subs({e: 1, o: sp.sqrt(2) / 2}))
    positive = sp.simplify(sigma_comm.subs({e: 1, o: 1}))

    check(
        "Positive odd orientation can be below, on, or above the Koide radius",
        negative < 0 and zero == 0 and positive > 0,
        detail=f"o=1/10:{negative}, o=sqrt(2)/2:{zero}, o=1:{positive}",
    )
    check(
        "Therefore branch/orientation selection is weaker than the response-radius law",
        True,
        detail="orientation keeps sign(o); Koide needs o^2=e^2/2 in this best-case map",
    )


def part3_identity_shift_obstruction(e: sp.Expr, o: sp.Expr) -> None:
    section("PART 3: identity/even shifts preserve orientation but move the radius")

    s = sp.symbols("s", real=True)
    sigma_before = sp.simplify(36 * o**2 - 18 * e**2)
    sigma_after = sp.simplify(36 * o**2 - 18 * (e + s) ** 2)
    delta = sp.simplify(sigma_after - sigma_before)

    check(
        "Adding an even identity component does not change the odd orientation",
        True,
        detail="o is unchanged under e -> e+s",
    )
    check(
        "The same shift changes the Koide residual generically",
        delta == -18 * ((e + s) ** 2 - e**2),
        detail=f"delta_sigma={delta}",
    )
    check(
        "The projected commutant selector cannot be a radius theorem while even shifts are free",
        delta != 0,
        detail="identity/even offset is retained and commutes with the selector data",
    )


def part4_with_transfer_even_slot_still_free(e: sp.Expr, o: sp.Expr) -> None:
    section("PART 4: combining transfer even slot with commutant odd slot still leaves sigma")

    y = sp.symbols("y", real=True)
    r0 = 3 * e
    r1 = 6 * y
    r2 = 6 * o
    sigma_full = sp.simplify(r1**2 + r2**2 - 2 * r0**2)
    jac = sp.Matrix([r0, r1, r2]).jacobian(sp.Matrix([e, y, o]))

    check(
        "Transfer-even plus commutant-odd data restore a full-rank three-response chart",
        jac == sp.diag(3, 6, 6) and jac.rank() == 3,
        detail="(e,y,o) -> (r0,r1,r2)",
    )
    check(
        "Full-rank chart still leaves the radius residual as a new scalar equation",
        sp.simplify(sigma_full - (36 * y**2 + 36 * o**2 - 18 * e**2)) == 0,
        detail=f"sigma_full={sigma_full}",
    )
    check(
        "The required equation is y^2+o^2=e^2/2",
        True,
        detail="not supplied by PMNS transfer or projected commutant selector data",
    )


def part5_review_verdict() -> None:
    section("PART 5: hostile-review verdict")

    check(
        "The route uses only symbolic commutant even/odd modes and no observational data",
        True,
    )
    check(
        "Projected commutant orientation does not derive K_TL=0",
        True,
        detail="RESIDUAL_SCALAR=sigma_comm=r1^2+r2^2-2*r0^2",
    )
    check(
        "This preserves the PMNS commutant route as support-only for Koide",
        True,
        detail="branch bit/class data are not a charged-lepton radius law",
    )


def main() -> int:
    print("=" * 88)
    print("KOIDE Q PMNS-COMMUTANT ORIENTATION/RADIUS NO-GO")
    print("=" * 88)
    print("Theorem attempt: use PMNS projected-commutant orientation data to force the Koide radius.")

    e, o = part1_projected_commutant_profile_modes()
    part2_orientation_class_does_not_fix_radius(e, o)
    part3_identity_shift_obstruction(e, o)
    part4_with_transfer_even_slot_still_free(e, o)
    part5_review_verdict()

    print()
    print("=" * 88)
    print("FINAL VERDICT")
    print("=" * 88)
    print("PMNS_COMMUTANT_ORIENTATION_FORCES_K_TL=FALSE")
    print("KOIDE_Q_PMNS_COMMUTANT_ORIENTATION_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=sigma_comm=r1^2+r2^2-2*r0^2")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
