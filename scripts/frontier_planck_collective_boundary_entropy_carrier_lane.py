#!/usr/bin/env python3
"""Audit the collective boundary entropy carrier lane honestly.

This is not a closure harness. It encodes a sharper reduction:
  - finite-state finite-memory collective boundary codes cannot give exact
    s_* = 1/4;
  - more generally, finite-dimensional algebraic transfer carriers cannot give
    exact s_* = 1/4;
  - the surviving class is a genuinely weighted gravitational Perron/pressure
    carrier with spectral radius exp(1/4).
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_COLLECTIVE_BOUNDARY_ENTROPY_CARRIER_LANE_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def perron_root(matrix: sp.Matrix) -> sp.Expr:
    vals = matrix.eigenvals()
    return max(vals, key=lambda expr: abs(complex(sp.N(expr, 30))))


def entropy_density_from_trace(matrix: sp.Matrix, n: int) -> float:
    z_n = sp.trace(matrix**n)
    return float(sp.log(sp.N(z_n)) / n)


def main() -> int:
    note = normalized(NOTE)
    target_root = sp.exp(sp.Rational(1, 4))
    n_pass = 0
    n_fail = 0

    print("Planck collective boundary entropy carrier lane audit")
    print("=" * 78)

    section("PART 1: TARGET COEFFICIENT CLASS")
    p = check(
        "exact conventional Planck on the boundary route means rho = exp(1/4)",
        sp.simplify(sp.log(target_root) - sp.Rational(1, 4)) == 0,
        "if s_* = log rho(T_grav) = 1/4, then rho(T_grav) must equal exp(1/4)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "exp(1/4) is transcendental, not algebraic",
        target_root.is_transcendental is True and target_root.is_algebraic is False,
        "SymPy confirms the Lindemann-Weierstrass consequence on this target root",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: FINITE-STATE COLLECTIVE CODE NO-GO")
    integer_examples = {
        "full shift": sp.Matrix([[1, 1], [1, 1]]),
        "Fibonacci code": sp.Matrix([[1, 1], [1, 0]]),
        "golden-mean with memory-2 presentation": sp.Matrix(
            [[1, 1, 0], [1, 0, 1], [1, 0, 0]]
        ),
    }
    misses_target = True
    algebraic_integer_like = True
    for name, matrix in integer_examples.items():
        rho = perron_root(matrix)
        algebraic_integer_like &= rho.is_algebraic is True
        misses_target &= sp.simplify(rho - target_root) != 0
        print(f"  sample {name:28s} rho = {sp.N(rho, 16)}")

    p = check(
        "representative integer adjacency Perron roots are algebraic and miss exp(1/4)",
        algebraic_integer_like and misses_target,
        (
            "finite-state exact counting lands Perron roots in the algebraic class, "
            "whereas the target root exp(1/4) is transcendental"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    phi = perron_root(integer_examples["Fibonacci code"])
    p = check(
        "a canonical collective finite-state code misses the target entropy density",
        abs(float(sp.N(sp.log(phi) - sp.Rational(1, 4)))) > 1e-6,
        f"log(phi) = {float(sp.N(sp.log(phi))):.12f}, target = 0.25",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: ALGEBRAIC FINITE-TRANSFER NO-GO")
    algebraic_examples = {
        "radical-weighted 2x2": sp.Matrix([[sp.sqrt(2), 1], [1, sp.sqrt(3)]]),
        "mixed algebraic 2x2": sp.Matrix(
            [[sp.Rational(1, 2), sp.sqrt(2)], [sp.sqrt(2), 1]]
        ),
    }
    algebraic_miss = True
    for name, matrix in algebraic_examples.items():
        rho = perron_root(matrix)
        algebraic_miss &= rho.is_algebraic is True and sp.simplify(rho - target_root) != 0
        print(f"  sample {name:28s} rho = {sp.N(rho, 16)}")

    p = check(
        "representative algebraic weighted transfer matrices still miss exp(1/4)",
        algebraic_miss,
        (
            "finite-dimensional transfer carriers with algebraic exact entries "
            "still live in the algebraic spectral-radius class"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: SURVIVING PERRON-CARRIER WITNESS")
    projector = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)],
                           [sp.Rational(1, 2), sp.Rational(1, 2)]])
    witness = target_root * projector
    rho_witness = perron_root(witness)
    p = check(
        "a positive weighted projector witness can realize the target root exactly",
        sp.simplify(rho_witness - target_root) == 0,
        "this is a witness for the surviving carrier class, not a derived closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    asymptotic_values = [entropy_density_from_trace(witness, n) for n in (1, 2, 4, 8, 16)]
    p = check(
        "the witness has exact asymptotic entropy density 1/4",
        max(abs(val - 0.25) for val in asymptotic_values) < 1e-12,
        (
            "for the rank-one positive witness, Tr(T^N) = exp(N/4), so "
            "(1/N) log Tr(T^N) = 1/4 exactly"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE HONESTY")
    p = check(
        "the note names the surviving class as a weighted gravitational Perron/pressure carrier",
        "weighted gravitational perron / pressure carrier" in note
        and "rho(t_grav) = e^(1/4)" in note,
        "the surviving class is explicit rather than implied",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly rules out both finite-state and algebraic finite-transfer closures",
        "no finite-state finite-memory collective boundary code" in note
        and "no finite-dimensional collective transfer carrier with purely algebraic" in note,
        "the second-wave narrowing is stated directly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The collective boundary route survives only in one very narrow form: "
        "an exact same-surface weighted gravitational Perron/pressure carrier "
        "whose spectral radius is exp(1/4). Finite-state collective counting "
        "and finite-dimensional algebraic transfer carriers are both ruled out."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
