#!/usr/bin/env python3
"""Chronology lane probe: multi-time support constraints are nonlocal imports.

Toy equation on one selected clock t1:

    d_t1^2 phi + d_t2^2 phi - d_x^2 phi = 0.

After Fourier transform along the codimension-1 slice coordinates (t2, x),
each mode obeys

    a''(t1) + (k^2 - omega2^2) a(t1) = 0.

A retained single-clock Cauchy surface would allow arbitrary local data on the
slice.  A constrained multi-time reading instead keeps only modes satisfying
k^2 >= omega2^2.  This script shows that delta-local slice data have full
Fourier support, including forbidden modes, and therefore require a nonlocal
projection/filter before they are admissible.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


PASS = 0
FAIL = 0


@dataclass(frozen=True)
class Mode:
    omega2: int
    k: int


@dataclass(frozen=True)
class Z2Point:
    tau: int
    x: int


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")


def fmt_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def mode_grid(radius: int) -> list[Mode]:
    return [
        Mode(omega2, k)
        for omega2 in range(-radius, radius + 1)
        for k in range(-radius, radius + 1)
    ]


def is_allowed(mode: Mode) -> bool:
    return mode.k * mode.k >= mode.omega2 * mode.omega2


def mode_type(mode: Mode) -> str:
    if is_allowed(mode):
        return "oscillatory/admissible"
    return "exponential/forbidden"


def frequency_square(mode: Mode) -> int:
    return mode.k * mode.k - mode.omega2 * mode.omega2


def delta_fourier_coefficients(modes: list[Mode]) -> dict[Mode, Fraction]:
    """Fourier transform of a delta at the slice origin.

    The normalization is irrelevant for support.  The important exact fact is
    that every mode has a nonzero coefficient.
    """

    return {mode: Fraction(1) for mode in modes}


def support_counts(modes: list[Mode]) -> tuple[int, int]:
    allowed = sum(1 for mode in modes if is_allowed(mode))
    forbidden = len(modes) - allowed
    return allowed, forbidden


def project_to_allowed(coefficients: dict[Mode, Fraction]) -> dict[Mode, Fraction]:
    return {
        mode: coefficient if is_allowed(mode) else Fraction(0)
        for mode, coefficient in coefficients.items()
    }


def z2_character(mode: Mode, point: Z2Point) -> int:
    phase = (mode.omega2 * point.tau + mode.k * point.x) % 2
    return -1 if phase else 1


def inverse_z2_transform(coefficients: dict[Mode, Fraction]) -> dict[Z2Point, Fraction]:
    points = [Z2Point(tau, x) for tau in (0, 1) for x in (0, 1)]
    scale = Fraction(1, 4)
    return {
        point: scale
        * sum(
            coefficient * z2_character(mode, point)
            for mode, coefficient in coefficients.items()
        )
        for point in points
    }


def fmt_mode(mode: Mode) -> str:
    return f"(omega2={mode.omega2:+d}, k={mode.k:+d})"


def print_mode_samples(modes: list[Mode]) -> None:
    samples = [
        Mode(0, 2),
        Mode(1, 2),
        Mode(2, 1),
        Mode(3, 0),
    ]
    print("SAMPLE t1 MODE EQUATIONS")
    for mode in samples:
        if mode not in modes:
            continue
        q = frequency_square(mode)
        if q >= 0:
            equation = f"a'' + {q} a = 0"
        else:
            equation = f"a'' - {-q} a = 0"
        print(f"  {fmt_mode(mode):18s} -> {equation:14s}  {mode_type(mode)}")
    print()


def main() -> int:
    print("=" * 88)
    print("MULTI-TIME SUPPORT CONSTRAINT PROBE")
    print("  Test: arbitrary local slice data activate forbidden ultrahyperbolic modes.")
    print("=" * 88)
    print()

    radius = 4
    modes = mode_grid(radius)
    allowed_count, forbidden_count = support_counts(modes)
    total_count = len(modes)
    forbidden_fraction = Fraction(forbidden_count, total_count)

    print("FINITE FOURIER LATTICE")
    print(f"  modes: omega2,k in [-{radius}, {radius}]")
    print("  admissibility constraint: k^2 >= omega2^2")
    print(f"  total modes      = {total_count}")
    print(f"  allowed modes    = {allowed_count}")
    print(f"  forbidden modes  = {forbidden_count}")
    print(f"  forbidden share  = {fmt_fraction(forbidden_fraction)}")
    print()
    print_mode_samples(modes)

    field_delta_hat = delta_fourier_coefficients(modes)
    velocity_delta_hat = delta_fourier_coefficients(modes)
    projected_hat = project_to_allowed(field_delta_hat)

    forbidden_field_slots = [
        mode
        for mode, coefficient in field_delta_hat.items()
        if not is_allowed(mode) and coefficient != 0
    ]
    forbidden_velocity_slots = [
        mode
        for mode, coefficient in velocity_delta_hat.items()
        if not is_allowed(mode) and coefficient != 0
    ]
    removed_slots = [
        mode
        for mode, coefficient in field_delta_hat.items()
        if coefficient != projected_hat[mode]
    ]

    arbitrary_cauchy_slots = 2 * total_count
    constrained_cauchy_slots = 2 * allowed_count

    print("LOCAL SLICE DATA")
    print("  data: delta-local field perturbation at (t2,x)=(0,0)")
    print("  exact Fourier support: coefficient 1 on every lattice mode")
    print("  data: delta-local normal-velocity perturbation at the same point")
    print("  exact Fourier support: coefficient 1 on every lattice mode")
    print()

    check(
        "finite lattice has a nonempty forbidden region",
        forbidden_count > 0,
        f"{forbidden_count}/{total_count} modes have omega2^2 > k^2",
    )
    check(
        "delta-local field data activate forbidden modes",
        len(forbidden_field_slots) == forbidden_count,
        f"{len(forbidden_field_slots)} forbidden coefficients are nonzero",
    )
    check(
        "delta-local velocity data activate forbidden modes",
        len(forbidden_velocity_slots) == forbidden_count,
        f"{len(forbidden_velocity_slots)} forbidden coefficients are nonzero",
    )
    check(
        "support projection removes exactly the forbidden field modes",
        len(removed_slots) == forbidden_count
        and all(projected_hat[mode] == 0 for mode in forbidden_field_slots),
        f"removed={len(removed_slots)}",
    )
    check(
        "constrained multi-time Cauchy slots are fewer than arbitrary local slots",
        constrained_cauchy_slots < arbitrary_cauchy_slots,
        f"{constrained_cauchy_slots} constrained vs {arbitrary_cauchy_slots} arbitrary",
    )
    print()

    z2_modes = [Mode(omega2, k) for omega2 in (0, 1) for k in (0, 1)]
    z2_delta_hat = delta_fourier_coefficients(z2_modes)
    z2_projected_hat = project_to_allowed(z2_delta_hat)
    z2_projected_data = inverse_z2_transform(z2_projected_hat)
    z2_origin = Z2Point(0, 0)
    z2_off_origin = [
        value for point, value in z2_projected_data.items() if point != z2_origin
    ]
    z2_off_origin_l1 = sum(abs(value) for value in z2_off_origin)

    print("EXACT NONLOCAL PROJECTION WITNESS ON Z2 x Z2")
    print("  modes: (omega2,k) in {0,1}^2")
    print("  forbidden mode under k^2 >= omega2^2: (omega2=1,k=0)")
    print("  inverse transform of the projected delta:")
    for point, value in sorted(
        z2_projected_data.items(), key=lambda item: (item[0].tau, item[0].x)
    ):
        label = "origin" if point == z2_origin else "off-origin"
        print(
            f"    (t2={point.tau}, x={point.x}) -> "
            f"{fmt_fraction(value):>4s}  {label}"
        )
    print()

    check(
        "projected point data are no longer point-local",
        any(value != 0 for value in z2_off_origin),
        f"off-origin L1 mass={fmt_fraction(z2_off_origin_l1)}",
    )
    check(
        "the projection kernel is an exact global slice filter",
        z2_projected_data[Z2Point(0, 1)] == Fraction(-1, 4)
        and z2_projected_data[Z2Point(1, 0)] == Fraction(1, 4)
        and z2_projected_data[Z2Point(1, 1)] == Fraction(1, 4),
        "removing one forbidden Fourier character changes every slice point",
    )
    print()

    print("CLASSIFICATION")
    print("  retained single-clock arbitrary local Cauchy surface: NO")
    print("  constrained multi-time support surface: YES")
    print("  imported structure: nonlocal Fourier support projection/filter")
    print("  chronology reading: boundary classifier, not operational past signaling")
    print()

    total = PASS + FAIL
    print("=" * 88)
    print(f"RESULT: {PASS}/{total} checks passed")
    if FAIL:
        print("STATUS: FAIL")
        return 1
    print("STATUS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
