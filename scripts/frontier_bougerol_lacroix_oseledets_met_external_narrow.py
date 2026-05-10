#!/usr/bin/env python3
"""Runner for the Bougerol-Lacroix / Oseledets MET external theorem note."""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "BOUGEROL_LACROIX_OSELEDETS_MET_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md"

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        status = "PASS (A)"
    else:
        FAIL += 1
        status = "FAIL (A)"
    print(f"  [{status}] {label}")
    if detail:
        print(f"         {detail}")


def close(x: float, y: float, tol: float = 1e-12) -> bool:
    return math.isclose(x, y, rel_tol=tol, abs_tol=tol)


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def test_diagonal_product_exponents() -> None:
    section("T1: diagonal product exponents")
    a, b = 0.5, 0.25
    n = 64
    exponents = [math.log(abs(a**n)) / n, math.log(abs(b**n)) / n]
    ok = close(exponents[0], math.log(a)) and close(exponents[1], math.log(b))
    check("diagonal product recovers log singular-value exponents", ok, f"exponents={exponents}")


def test_singular_values_for_diagonal_product() -> None:
    section("T2: singular-value definition")
    a, b = 0.8, 0.3
    n = 32
    singular_values = [abs(a**n), abs(b**n)]
    vals = [math.log(singular_values[0]) / n, math.log(singular_values[1]) / n]
    ok = close(vals[0], math.log(a)) and close(vals[1], math.log(b))
    check("diagonal singular-value MET formula matches known rates", ok, f"vals={vals}")


def test_vector_growth() -> None:
    section("T3: vector growth in top Oseledets direction")
    a, b = 0.7, 0.2
    n = 40
    v_norm = 3.0
    product_v_norm = abs(a**n) * v_norm
    growth = math.log(product_v_norm / v_norm) / n
    check("top-direction vector growth tends to lambda_1 in exact diagonal case", close(growth, math.log(a)), f"growth={growth}")


def test_degenerate_no_gap_boundary() -> None:
    section("T4: degenerate no-gap boundary")
    a = 0.5
    n = 16
    vals = [math.log(abs(a**n)) / n, math.log(abs(a**n)) / n]
    check("equal diagonal rates give lambda_1 = lambda_2, so no spectral-gap claim is inferred", close(vals[0], vals[1]), f"vals={vals}")


def test_diagonal_operator_bound() -> None:
    section("T5: diagonal operator bound")
    a1, b1 = 0.8, 0.4
    a2, b2 = 0.5, 0.25
    v1, v2 = 3.0, -4.0
    lhs = math.hypot(a2 * a1 * v1, b2 * b1 * v2)
    rhs = max(abs(a2), abs(b2)) * max(abs(a1), abs(b1)) * math.hypot(v1, v2)
    check("diagonal operator products obey the operator-norm vector bound", lhs <= rhs + 1e-12, f"lhs={lhs}, rhs={rhs}")


def test_limit_not_finite_rate_claim() -> None:
    section("T6: limit theorem boundary")
    n1, n2 = 16, 64
    a = 0.6
    rate1 = math.log(abs(a**n1)) / n1
    rate2 = math.log(abs(a**n2)) / n2
    ok = close(rate1, rate2) and close(rate2, math.log(a))
    check("exact diagonal examples agree at multiple N without asserting a general finite-N rate", ok, f"rates={(rate1, rate2)}")


def test_note_boundary() -> None:
    section("T7: source-note boundary")
    text = NOTE.read_text(encoding="utf-8")
    lower = text.lower()
    forbidden = [
        "pathwise exponentially small remainder",
        "project-specific coupling equals exp(lambda_1); this theorem proves it",
        "framework substitution is closed",
        "hierarchy formula is closed",
        "pipeline-derived status: retained",
    ]
    check("note declares positive_theorem", "**Claim type:** positive_theorem" in text)
    check("note avoids spectral-rate and framework-bridge overclaims", not any(item in lower for item in forbidden))


def main() -> int:
    print("# Bougerol-Lacroix / Oseledets MET external theorem runner")
    print(f"# Source note: {NOTE.relative_to(ROOT)}")
    test_diagonal_product_exponents()
    test_singular_values_for_diagonal_product()
    test_vector_growth()
    test_degenerate_no_gap_boundary()
    test_diagonal_operator_bound()
    test_limit_not_finite_rate_claim()
    test_note_boundary()
    print(f"\n=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
