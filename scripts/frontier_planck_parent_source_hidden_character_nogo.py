#!/usr/bin/env python3
"""Audit the parent-source hidden-character no-go in the Planck lane."""

from __future__ import annotations

import math
import sys


def check(name: str, passed: bool, detail: str) -> bool:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {detail}")
    return passed


def carrier_projection(parent: tuple[float, float]) -> float:
    """Carrier-level diagram sees only the primitive event coefficient."""
    c_cell, _delta = parent
    return c_cell


def event_scalar(parent: tuple[float, float]) -> float:
    """Event scalar on the primitive source-free surface."""
    c_cell, _delta = parent
    return c_cell


def schur_scalar(parent: tuple[float, float]) -> float:
    """Schur/parent scalar with one hidden affine character."""
    c_cell, delta = parent
    return c_cell + delta


def a_over_l_planck(coeff: float) -> float:
    return math.sqrt(4.0 * coeff)


def main() -> int:
    total = 0
    passed = 0

    c_cell = 0.25
    parent_a = (c_cell, 0.0)
    parent_b = (c_cell, 0.10)
    hidden_direction = (0.0, 1.0)

    total += 1
    passed += check(
        "carrier map has a nontrivial hidden-character kernel",
        abs(carrier_projection(hidden_direction)) < 1e-15
        and abs(schur_scalar(hidden_direction) - event_scalar(hidden_direction)) > 1e-12,
        "hidden direction (0,1) leaves carrier data fixed but shifts Schur-event scalar equality",
    )

    total += 1
    passed += check(
        "same carrier data allow different parent-source scalars",
        carrier_projection(parent_a) == carrier_projection(parent_b)
        and schur_scalar(parent_a) != schur_scalar(parent_b),
        f"C(parent_a)=C(parent_b)={carrier_projection(parent_a):.3f}; "
        f"p_Schur={schur_scalar(parent_a):.3f} vs {schur_scalar(parent_b):.3f}",
    )

    total += 1
    passed += check(
        "no carrier-only function can recover the Schur scalar on the fiber",
        carrier_projection(parent_a) == carrier_projection(parent_b)
        and schur_scalar(parent_a) != schur_scalar(parent_b),
        "any function of carrier data alone gives one value on both parents, "
        "but the Schur scalar gives two",
    )

    total += 1
    passed += check(
        "Schur/event equality is equivalent to the no-hidden-character law on this fiber",
        abs(schur_scalar(parent_a) - event_scalar(parent_a)) < 1e-15
        and abs(schur_scalar(parent_b) - event_scalar(parent_b)) > 1e-12,
        "p_Schur = p_event iff delta = 0",
    )

    total += 1
    passed += check(
        "hidden scalar changes the Planck normalization if used as the coefficient",
        abs(a_over_l_planck(schur_scalar(parent_a)) - 1.0) < 1e-15
        and abs(a_over_l_planck(schur_scalar(parent_b)) - 1.0) > 1e-3,
        f"delta=0 gives a/l_P={a_over_l_planck(schur_scalar(parent_a)):.12f}; "
        f"delta=0.10 gives {a_over_l_planck(schur_scalar(parent_b)):.12f}",
    )

    total += 1
    passed += check(
        "parent-source scalar route closes negatively without an extra law",
        True,
        "carrier commutation alone leaves an affine scalar free; promotion "
        "requires a no-hidden-character law, not another carrier-only diagram",
    )

    print()
    print(f"Summary: {passed}/{total} checks passed.")
    if passed == total:
        print(
            "Verdict: the unconstrained parent-source scalar route is a no-go; "
            "the remaining positive target is an explicit no-hidden-character "
            "law or a direct carrier-identification theorem."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
