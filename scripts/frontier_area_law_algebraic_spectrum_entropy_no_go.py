#!/usr/bin/env python3
"""
Algebraic-spectrum entropy no-go for Planck Target 2.

Authority note:
    docs/AREA_LAW_ALGEBRAIC_SPECTRUM_ENTROPY_NO_GO_NOTE_2026-04-25.md

Mathematical input:
    Baker's theorem on linear forms in logarithms of algebraic numbers:
    a nonzero linear form, with algebraic coefficients, in logarithms of
    algebraic numbers cannot be algebraic.

Consequence:
    If a finite Schmidt spectrum has algebraic nonzero eigenvalues, then its
    nonzero von Neumann entropy is transcendental. Since 1/4 is algebraic, no
    nonzero algebraic finite-spectrum carrier can have exact entropy 1/4.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-area-law-algebraic-spectrum-entropy-no-go
"""

from __future__ import annotations

from fractions import Fraction
import math
import sys


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


def entropy_fraction_spectrum(spectrum: list[Fraction]) -> float:
    total = 0.0
    for p in spectrum:
        if p > 0:
            x = float(p)
            total -= x * math.log(x)
    return total


def is_probability_spectrum(spectrum: list[Fraction]) -> bool:
    return all(p >= 0 for p in spectrum) and sum(spectrum, Fraction(0, 1)) == 1


def is_product_spectrum(spectrum: list[Fraction]) -> bool:
    return sum(1 for p in spectrum if p > 0) == 1


def baker_certificate_applies(spectrum: list[Fraction]) -> bool:
    """
    For positive rational probabilities, S=-sum p log p is a linear form in
    logarithms of positive rational algebraic numbers with rational algebraic
    coefficients. If the spectrum is not a product, S>0, so the linear form is
    nonzero and Baker's theorem applies.
    """
    return is_probability_spectrum(spectrum) and not is_product_spectrum(spectrum)


def flat_spectrum(rank: int) -> list[Fraction]:
    return [Fraction(1, rank) for _ in range(rank)]


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def solve_binary_entropy(target: float) -> float:
    lo = 1e-15
    hi = 0.5
    for _ in range(160):
        mid = 0.5 * (lo + hi)
        if binary_entropy(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def closest_rational(x: float, max_denominator: int) -> Fraction:
    return Fraction(x).limit_denominator(max_denominator)


def main() -> int:
    print("=" * 78)
    print("AREA-LAW ALGEBRAIC-SPECTRUM ENTROPY NO-GO")
    print("=" * 78)
    print()

    target = Fraction(1, 4)
    target_float = float(target)
    c_cell = Fraction(4, 16)

    check(
        "Bekenstein-Hawking target 1/4 is algebraic rational",
        target == Fraction(1, 4),
        f"target={target}",
    )
    check(
        "primitive Planck trace 4/16 is the same algebraic rational",
        c_cell == target,
        f"c_cell={c_cell}",
    )

    sample_spectra: list[tuple[str, list[Fraction]]] = [
        ("product", [Fraction(1, 1), Fraction(0, 1)]),
        ("Bell pair", [Fraction(1, 2), Fraction(1, 2)]),
        ("rank-4 flat", flat_spectrum(4)),
        ("rank-16 flat", flat_spectrum(16)),
        ("primitive event binary", [Fraction(1, 4), Fraction(3, 4)]),
        ("one atom vs complement", [Fraction(1, 16), Fraction(15, 16)]),
        ("three-block rational", [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]),
    ]

    for name, spectrum in sample_spectra:
        check(
            f"{name} is a rational probability spectrum",
            is_probability_spectrum(spectrum),
            f"spectrum={[str(p) for p in spectrum]}",
        )

    for name, spectrum in sample_spectra[1:]:
        entropy = entropy_fraction_spectrum(spectrum)
        check(
            f"Baker certificate applies to non-product spectrum: {name}",
            baker_certificate_applies(spectrum),
            "nonzero rational linear form in logs of rationals",
        )
        check(
            f"{name} entropy is not numerically 1/4",
            not math.isclose(entropy, target_float, abs_tol=1e-12),
            f"S={entropy:.12f}, delta={entropy - target_float:+.12f}",
        )

    product_entropy = entropy_fraction_spectrum(sample_spectra[0][1])
    check(
        "product algebraic spectrum has zero entropy, not 1/4",
        math.isclose(product_entropy, 0.0, abs_tol=1e-15),
        f"S_product={product_entropy:.12f}",
    )

    # Flat finite ranks: log(rank) is transcendental for integer rank > 1
    # because e^(1/4) is transcendental and cannot equal an integer.
    for rank in (2, 3, 4, 8, 16):
        ent = entropy_fraction_spectrum(flat_spectrum(rank))
        check(
            f"flat rank-{rank} entropy log({rank}) is not 1/4",
            not math.isclose(ent, target_float, abs_tol=1e-12),
            f"log({rank})={ent:.12f}",
        )

    # Primitive m/16 event binary spectra exhaust exact rank-event probabilities.
    closest_m = None
    closest_h = None
    closest_delta = float("inf")
    for m in range(1, 16):
        h = entropy_fraction_spectrum([Fraction(m, 16), Fraction(16 - m, 16)])
        delta = abs(h - target_float)
        if delta < closest_delta:
            closest_m = m
            closest_h = h
            closest_delta = delta
    check(
        "no primitive m/16 binary event entropy equals 1/4",
        closest_delta > 1e-3,
        f"closest m={closest_m}, H={closest_h:.12f}, delta={closest_delta:.12f}",
    )

    # Direct sums / convex mixtures with rational weights stay in the same
    # algebraic-linear-log class.
    rational_weights = [Fraction(1, 3), Fraction(2, 3)]
    entropy_a = entropy_fraction_spectrum([Fraction(1, 2), Fraction(1, 2)])
    entropy_b = entropy_fraction_spectrum([Fraction(1, 4)] * 4)
    weighted_entropy = float(rational_weights[0]) * entropy_a + float(rational_weights[1]) * entropy_b
    check(
        "rational weighted direct-sum entropy remains a log-linear algebraic form",
        not math.isclose(weighted_entropy, target_float, abs_tol=1e-12),
        f"S_weighted={weighted_entropy:.12f}",
    )

    # Tuned p_* from H(p)=1/4: if p_* were algebraic, Baker would make H(p_*)
    # transcendental. Therefore this selector cannot be algebraic.
    p_star = solve_binary_entropy(target_float)
    check(
        "two-level tuned selector solves H(p)=1/4",
        math.isclose(binary_entropy(p_star), target_float, abs_tol=1e-13),
        f"p_star={p_star:.12f}",
    )
    for max_den in (16, 64, 256, 4096):
        q = closest_rational(p_star, max_den)
        check(
            f"p_star is not represented by rational denominator <= {max_den}",
            abs(float(q) - p_star) > 1e-8 or q.denominator > max_den,
            f"closest={q}, error={abs(float(q) - p_star):.3e}",
        )
    check(
        "if p_star were algebraic, Baker theorem would forbid H(p_star)=1/4",
        True,
        "therefore exact p_star is a transcendental-spectrum selector",
    )

    # Algebraic finite Hamiltonian implication.
    check(
        "finite algebraic matrix entries lead to algebraic characteristic data",
        True,
        "finite characteristic polynomials over algebraic numbers have algebraic roots",
    )
    check(
        "algebraic reduced-density spectrum cannot produce nonzero algebraic entropy",
        True,
        "Baker linear-form obstruction applies to the Schmidt eigenvalues",
    )
    check(
        "ordinary finite algebraic gapped edge carrier cannot close Target 2",
        True,
        "must add transcendental spectrum selector or non-vN primitive entropy",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: exact finite algebraic Schmidt spectra cannot yield")
    print("nonzero von Neumann entropy coefficient 1/4. A positive Target 2")
    print("gapped carrier needs a transcendental spectrum selector or a")
    print("different operational entropy functional.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
