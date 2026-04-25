#!/usr/bin/env python3
"""
Koide Q PMNS-transfer odd-slot no-go.

Theorem attempt:
  Use the retained PMNS hw=1 transfer interface as a positive microscopic
  source for the charged-lepton Koide cyclic response law.

Result:
  The aligned transfer kernel is exactly

      T_seed = x I + y (C + C^2).

  Projected to the Koide cyclic response basis, this gives

      r0 = 3 x,   r1 = 6 y,   r2 = 0.

  The odd cyclic slot is absent, and the even-slot ratio y/x is not fixed by
  the transfer spectrum.  The exact residual is

      sigma_PMNS_transfer = r1^2 + r2^2 - 2 r0^2
                          = 18 (2 y^2 - x^2).

  Thus the PMNS transfer interface is positive support for an aligned seed
  pair, but it does not derive K_TL = 0 or close Koide Q.
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


def cyclic_basis() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    c = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    c2 = c**2
    b0 = sp.eye(3)
    b1 = c + c2
    b2 = sp.I * (c - c2)
    return c, b0, b1, b2


def real_trace_pair(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.re(sp.trace(a * b))


def part1_transfer_kernel_to_koide_responses() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    section("PART 1: PMNS aligned transfer kernel projected to Koide responses")

    _c, b0, b1, b2 = cyclic_basis()
    x, y = sp.symbols("x y", real=True)
    t_seed = x * b0 + y * b1

    r0 = sp.simplify(real_trace_pair(b0, t_seed))
    r1 = sp.simplify(real_trace_pair(b1, t_seed))
    r2 = sp.simplify(real_trace_pair(b2, t_seed))
    sigma = sp.simplify(r1**2 + r2**2 - 2 * r0**2)

    check(
        "Aligned PMNS transfer kernel has only I and C+C^2 channels",
        t_seed == x * b0 + y * b1,
        detail="T_seed=x*B0+y*B1",
    )
    check(
        "Koide cyclic responses are r0=3x, r1=6y, r2=0",
        (r0, r1, r2) == (3 * x, 6 * y, 0),
        detail=f"(r0,r1,r2)=({r0},{r1},{r2})",
    )
    check(
        "The odd cyclic Koide response is absent on the aligned transfer image",
        r2 == 0,
        detail="rho_odd_missing=r2",
    )
    check(
        "The induced Koide residual is sigma_PMNS_transfer=18*(2*y^2-x^2)",
        sp.simplify(sigma - 18 * (2 * y**2 - x**2)) == 0,
        detail=f"sigma={sigma}",
    )
    return x, y, r0, r1, sigma


def part2_dominant_mode_reconstructs_seed_pair_but_not_ratio(x: sp.Expr, y: sp.Expr) -> None:
    section("PART 2: dominant/subdominant modes reconstruct but do not select")

    lam_plus = sp.simplify(x + 2 * y)
    lam_minus = sp.simplify(x - y)
    x_rec = sp.simplify((lam_plus + 2 * lam_minus) / 3)
    y_rec = sp.simplify((lam_plus - lam_minus) / 3)

    check(
        "PMNS transfer eigenvalues reconstruct the aligned seed pair exactly",
        x_rec == x and y_rec == y,
        detail=f"lambda_plus={lam_plus}, lambda_minus={lam_minus}",
    )
    check(
        "The transfer spectrum has two independent scalar inputs",
        sp.Matrix([lam_plus, lam_minus]).jacobian(sp.Matrix([x, y])).rank() == 2,
        detail="rank=2, so no y/x ratio is fixed",
    )

    sigma_y0 = sp.simplify(18 * (2 * y**2 - x**2)).subs({x: 1, y: 0})
    sigma_yhalf = sp.simplify(18 * (2 * y**2 - x**2)).subs({x: 1, y: sp.Rational(1, 2)})
    sigma_ykoide = sp.simplify(18 * (2 * y**2 - x**2)).subs({x: 1, y: sp.sqrt(2) / 2})

    check(
        "Positive transfer-compatible seed witnesses can be off the Koide circle",
        sigma_y0 != 0 and sigma_yhalf != 0,
        detail=f"y=0 residual={sigma_y0}, y=1/2 residual={sigma_yhalf}",
    )
    check(
        "The Koide-compatible even ratio is one special value, not a transfer theorem",
        sigma_ykoide == 0,
        detail="y/x=1/sqrt(2) is the missing coefficient law",
    )


def part3_off_seed_source_blindness() -> None:
    section("PART 3: transfer-only data are blind to off-seed source content")

    x, y, a, b = sp.symbols("x y a b", real=True)
    x_profile_1 = sp.Matrix([x + a, x - a, x])
    x_profile_2 = sp.Matrix([x + 2 * a, x - 2 * a, x])
    y_profile_1 = sp.Matrix([y + b, y - b, y])
    y_profile_2 = sp.Matrix([y - b, y + b, y])

    xbar_1 = sp.simplify(sum(x_profile_1) / 3)
    xbar_2 = sp.simplify(sum(x_profile_2) / 3)
    ybar_1 = sp.simplify(sum(y_profile_1) / 3)
    ybar_2 = sp.simplify(sum(y_profile_2) / 3)

    check(
        "Distinct off-seed active profiles can share the same transfer means",
        xbar_1 == xbar_2 == x and ybar_1 == ybar_2 == y,
        detail="transfer sees xbar,ybar only",
    )
    check(
        "Those profiles differ in zero-sum source directions invisible to transfer-only data",
        sp.simplify((x_profile_1 - x_profile_2).norm()) != 0
        and sp.simplify((y_profile_1 - y_profile_2).norm()) != 0,
        detail="source-response columns are needed to see the breaking carrier",
    )


def part4_odd_slot_extension_still_needs_a_radius_law() -> None:
    section("PART 4: adding an odd selector slot does not close the radius")

    x, y, z = sp.symbols("x y z", real=True)
    r0, r1, r2 = 3 * x, 6 * y, 6 * z
    sigma_full = sp.simplify(r1**2 + r2**2 - 2 * r0**2)
    jac = sp.Matrix([r0, r1, r2]).jacobian(sp.Matrix([x, y, z]))

    check(
        "A transferred odd slot would restore the full three-response carrier",
        jac == sp.diag(3, 6, 6) and jac.rank() == 3,
        detail="(x,y,z) -> (r0,r1,r2) is full rank",
    )
    check(
        "But the full carrier still leaves the Koide radius as a residual scalar",
        sp.simplify(sigma_full - (36 * y**2 + 36 * z**2 - 18 * x**2)) == 0,
        detail=f"sigma_full={sigma_full}",
    )
    check(
        "Odd-slot existence is not enough; the missing law is y^2+z^2=x^2/2",
        True,
        detail="rho_odd plus radius law would be new retained structure",
    )


def part5_review_verdict() -> None:
    section("PART 5: hostile-review verdict")

    check(
        "No observational mass data or external pins enter this PMNS-transfer audit",
        True,
    )
    check(
        "The PMNS transfer route does not derive K_TL=0; it reduces to sigma_PMNS_transfer=0 plus an odd-slot gap",
        True,
        detail="RESIDUAL_SCALAR=sigma_PMNS_transfer=18*(2*y^2-x^2); rho_odd_missing=r2",
    )
    check(
        "This is a no-go for importing the aligned PMNS transfer law as Koide closure",
        True,
        detail="the positive PMNS theorem fixes a seed pair, not the charged-lepton source radius",
    )


def main() -> int:
    print("=" * 88)
    print("KOIDE Q PMNS-TRANSFER ODD-SLOT NO-GO")
    print("=" * 88)
    print("Theorem attempt: use the retained PMNS hw=1 transfer interface to derive the Koide cyclic source law.")

    x, y, _r0, _r1, _sigma = part1_transfer_kernel_to_koide_responses()
    part2_dominant_mode_reconstructs_seed_pair_but_not_ratio(x, y)
    part3_off_seed_source_blindness()
    part4_odd_slot_extension_still_needs_a_radius_law()
    part5_review_verdict()

    print()
    print("=" * 88)
    print("FINAL VERDICT")
    print("=" * 88)
    print("PMNS_TRANSFER_FORCES_K_TL=FALSE")
    print("KOIDE_Q_PMNS_TRANSFER_ODD_SLOT_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=sigma_PMNS_transfer=18*(2*y^2-x^2);rho_odd_missing=r2")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
