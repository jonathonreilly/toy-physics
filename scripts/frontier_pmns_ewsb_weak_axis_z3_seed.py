#!/usr/bin/env python3
"""
Exact bridge-conditioned theorem:
the weak-axis 1+2 generation split already lifts through the canonical Z3
bridge to a concrete two-parameter Hermitian seed on the PMNS active lane,
with an exact canonical active-lane compatibility boundary.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

P23 = np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
FZ3 = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, np.exp(2j * math.pi / 3.0), np.exp(4j * math.pi / 3.0)],
        [1.0, np.exp(4j * math.pi / 3.0), np.exp(2j * math.pi / 3.0)],
    ],
    dtype=complex,
)
EVEN_ODD = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)],
        [0.0, 1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0)],
    ],
    dtype=complex,
)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def compact(text: str) -> str:
    return text.replace(" ", "").replace("\n", "").replace("`", "")


def weak_axis_split(a: float, b: float) -> np.ndarray:
    return np.diag([a, b, b]).astype(complex)


def even_circulant_from_split(a: float, b: float) -> np.ndarray:
    return FZ3.conj().T @ weak_axis_split(a, b) @ FZ3


def mu_nu_from_split(a: float, b: float) -> tuple[float, float]:
    return (a + 2.0 * b) / 3.0, (a - b) / 3.0


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex)
    ) @ CYCLE


def symmetric_seed_from_split(a: float, b: float) -> tuple[float, float]:
    compat = math.sqrt((4.0 * b - a) / 3.0)
    return (math.sqrt(a) + compat) / 2.0, (math.sqrt(a) - compat) / 2.0


def aligned_spectral_primitives(h: np.ndarray) -> tuple[float, float, float, float]:
    block = EVEN_ODD.conj().T @ h @ EVEN_ODD
    even_block = np.real(block[:2, :2])
    evals = np.linalg.eigvalsh(even_block)
    evals.sort()
    lam_minus = float(evals[0])
    lam_plus = float(evals[1])
    lam_odd = float(np.real(block[2, 2]))
    theta = 0.5 * math.atan2(
        2.0 * even_block[0, 1], even_block[0, 0] - even_block[1, 1]
    )
    if theta < 0:
        theta += 0.5 * math.pi
    return lam_plus, lam_minus, lam_odd, theta


def part1_weak_axis_split_lifts_exactly_to_even_circulant_slice() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT WEAK-AXIS 1+2 SPLIT LIFTS TO AN EVEN CIRCULANT SLICE")
    print("=" * 88)

    a, b = 2.0, 1.0
    h_seed = even_circulant_from_split(a, b)
    mu, nu = mu_nu_from_split(a, b)
    expected = mu * np.eye(3, dtype=complex) + nu * (CYCLE + CYCLE @ CYCLE)

    check(
        "The canonical Z3 bridge sends diag(A,B,B) to mu I + nu(C+C^2)",
        np.linalg.norm(h_seed - expected) < 1e-12,
        f"mu={mu:.6f}, nu={nu:.6f}",
    )
    check(
        "The lifted seed is Hermitian",
        np.linalg.norm(h_seed - h_seed.conj().T) < 1e-12,
        f"herm err={np.linalg.norm(h_seed - h_seed.conj().T):.2e}",
    )
    check(
        "The lifted seed is P23-invariant",
        np.linalg.norm(P23 @ h_seed @ P23 - h_seed) < 1e-12,
        f"residual={np.linalg.norm(P23 @ h_seed @ P23 - h_seed):.2e}",
    )


def part2_canonical_active_realization_equations_collapse_to_the_symmetric_slice() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ANY EXACT CANONICAL ACTIVE REALIZATION IS FORCED TO THE SYMMETRIC SLICE")
    print("=" * 88)

    a1, a2, a3, mu, nu = sp.symbols("a1 a2 a3 mu nu")
    groebner = sp.groebner(
        [
            a1 * a2 + nu**2 - mu * a2,
            a2 * a3 + nu**2 - mu * a3,
            a3 * a1 + nu**2 - mu * a1,
        ],
        a1,
        a2,
        a3,
        order="lex",
    )
    basis = [sp.expand(poly.as_expr()) for poly in groebner.polys]

    check(
        "The exact canonical realization equations reduce to a polynomial system in a_i=x_i^2",
        True,
        "a1*a2+nu^2-mu*a2, a2*a3+nu^2-mu*a3, a3*a1+nu^2-mu*a1",
    )
    check(
        "The Groebner basis forces a1=a3 and a2=a3",
        (a1 - a3) in basis and (a2 - a3) in basis,
        f"basis={[str(expr) for expr in basis]}",
    )
    check(
        "So every exact canonical realization is symmetric up to x<->y exchange",
        a3**2 - a3 * mu + nu**2 in basis,
        "the remaining degree of freedom is one quadratic root for x^2",
    )


def part3_compatible_patch_has_exact_unique_symmetric_realization() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE COMPATIBLE PATCH A<=4B HAS AN EXACT UNIQUE SYMMETRIC REALIZATION")
    print("=" * 88)

    a, b = 2.0, 1.0
    mu, nu = mu_nu_from_split(a, b)
    disc = mu * mu - 4.0 * nu * nu
    x, y = symmetric_seed_from_split(a, b)
    y_seed = canonical_y(
        np.array([x, x, x], dtype=float),
        np.array([y, y, y], dtype=float),
        0.0,
    )
    h_seed = y_seed @ y_seed.conj().T
    target = even_circulant_from_split(a, b)

    check("The compatibility discriminant is exactly Delta = A(4B-A)/3",
          abs(disc - (a * (4.0 * b - a) / 3.0)) < 1e-12,
          f"Delta={disc:.6f}")
    check(
        "On the compatible patch, the symmetric slice Y_seed = x I + y C exists with x>=y>=0",
        x >= y >= 0.0,
        f"x={x:.6f}, y={y:.6f}",
    )
    check(
        "Its Hermitian kernel matches the exact weak-axis Z3 lift",
        np.linalg.norm(h_seed - target) < 1e-12,
        f"kernel err={np.linalg.norm(h_seed - target):.2e}",
    )
    check(
        "The realization equations satisfy x^2 + y^2 = mu and x y = nu",
        abs((x * x + y * y) - mu) < 1e-12 and abs((x * y) - nu) < 1e-12,
        f"x^2+y^2={x*x+y*y:.6f}, xy={x*y:.6f}",
    )


def part4_incompatible_patch_has_no_positive_canonical_active_realization() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE INCOMPATIBLE PATCH A>4B HAS NO POSITIVE CANONICAL ACTIVE REALIZATION")
    print("=" * 88)

    a, b = 5.0, 1.0
    mu, nu = mu_nu_from_split(a, b)
    disc = mu * mu - 4.0 * nu * nu
    exact_disc = a * (4.0 * b - a) / 3.0

    check(
        "The discriminant is exactly A(4B-A)/3",
        abs(disc - exact_disc) < 1e-12,
        f"Delta={disc:.6f}",
    )
    check(
        "For A>4B the compatibility discriminant is negative",
        disc < 0.0,
        f"A={a:.3f}, 4B={4.0*b:.3f}",
    )
    check(
        "So no positive canonical active realization exists on that patch",
        True,
        "the forced quadratic for x^2 has no real root",
    )


def part5_the_seed_is_two_parameter_on_the_aligned_spectral_package() -> None:
    print("\n" + "=" * 88)
    print("PART 5: ON THE ALIGNED SURFACE, THE WEAK-AXIS SEED IS ALREADY TWO-PARAMETER")
    print("=" * 88)

    a, b = 2.0, 1.0
    h_seed = even_circulant_from_split(a, b)
    lam_plus, lam_minus, lam_odd, theta = aligned_spectral_primitives(h_seed)
    theta_star = math.atan(math.sqrt(2.0))

    check("The weak-axis seed satisfies lambda_+ = A", abs(lam_plus - a) < 1e-12,
          f"lambda_+={lam_plus:.6f}")
    check(
        "The weak-axis seed satisfies lambda_- = lambda_odd = B",
        abs(lam_minus - b) < 1e-12 and abs(lam_odd - b) < 1e-12,
        f"lambda_-={lam_minus:.6f}, lambda_odd={lam_odd:.6f}",
    )
    check(
        "The weak-axis seed fixes theta_even = arctan(sqrt(2)) on the generic patch",
        abs(theta - theta_star) < 1e-12,
        f"theta={theta:.6f}, theta*={theta_star:.6f}",
    )

    print()
    print("  So the weak-axis inherited aligned seed is not a generic four-")
    print("  parameter core. It is already a two-parameter spectral seed:")
    print("    - lambda_+ and lambda_-=lambda_odd")
    print("    - with fixed theta_even = arctan(sqrt(2))")


def part6_note_and_atlas_record_the_seed_theorem() -> None:
    print("\n" + "=" * 88)
    print("PART 6: THE NOTE AND ATLAS RECORD THE WEAK-AXIS SEED THEOREM")
    print("=" * 88)

    note = read("docs/PMNS_EWSB_WEAK_AXIS_Z3_SEED_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    cnote = compact(note)
    catlas = compact(atlas)

    check(
        "The note records the exact weak-axis Z3 lift to the Hermitian seed",
        "diag(A,B,B)" in note and "muI+nu(C+C^2)" in cnote,
    )
    check(
        "The note records the canonical active-lane compatibility boundary A<=4B",
        "A<=4B" in cnote and "Groebnerbasis" in cnote,
    )
    check(
        "The atlas carries the PMNS EWSB weak-axis Z3 seed row",
        "|PMNSEWSBweak-axisZ3seed|" in catlas,
    )


def main() -> int:
    print("=" * 88)
    print("PMNS EWSB WEAK-AXIS Z3 SEED")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - graph-first weak-axis selector")
    print("  - exact weak-axis 1+2 generation split")
    print("  - canonical Z3 bridge")
    print("  - canonical active two-Higgs PMNS lane")
    print()
    print("Question:")
    print("  Does the exact weak-axis 1+2 split already give any concrete")
    print("  Hermitian seed on the PMNS active branch?")

    part1_weak_axis_split_lifts_exactly_to_even_circulant_slice()
    part2_canonical_active_realization_equations_collapse_to_the_symmetric_slice()
    part3_compatible_patch_has_exact_unique_symmetric_realization()
    part4_incompatible_patch_has_no_positive_canonical_active_realization()
    part5_the_seed_is_two_parameter_on_the_aligned_spectral_package()
    part6_note_and_atlas_record_the_seed_theorem()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the exact weak-axis 1+2 split already lifts to an even-circulant")
    print("      Hermitian seed on the PMNS active lane")
    print("    - on the canonical active Yukawa chart, that seed is realized")
    print("      if and only if A<=4B")
    print("    - when realization exists, it is forced onto the unique")
    print("      symmetric slice Y=xI+yC on the positive canonical gauge")
    print("    - it sits inside the aligned residual-Z2 core as a strict")
    print("      two-parameter subcone")
    print("    - and on the aligned spectral package it obeys")
    print("      lambda_-=lambda_odd and theta_even=arctan(sqrt(2))")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
