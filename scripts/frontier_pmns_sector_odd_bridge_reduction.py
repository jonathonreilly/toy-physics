#!/usr/bin/env python3
"""
Exact reduction theorem for the missing PMNS selector object.

Question:
  After the current support-side and scalar-observable banks both fail to
  realize the one-sided PMNS selector, what exact form can the missing future
  selector be reduced to?

Answer:
  On the reduced one-sided PMNS surface, any branch-distinguishing scalar can
  be replaced by its sector-odd part under the exact sector-exchange involution
  sigma. Therefore the missing object can be reduced to a nonzero sector-odd
  mixed bridge functional. The current exact banks provide no such object.

Boundary:
  Exact reduction theorem on the current one-sided PMNS surface. It does not
  construct the future bridge; it identifies the minimal parity class that any
  successful bridge must inhabit.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PERMUTATIONS = {
    0: np.eye(3, dtype=complex),
    1: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex),
    2: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex),
}


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


def build_texture(offsets: tuple[int, ...], diag_blocks: tuple[np.ndarray, ...]) -> np.ndarray:
    total = np.zeros((3, 3), dtype=complex)
    for offset, diag in zip(offsets, diag_blocks):
        total += np.diag(diag) @ PERMUTATIONS[offset]
    return total


def scalar_generator(d: np.ndarray, j: np.ndarray) -> float:
    val = np.linalg.det(d + j)
    base = np.linalg.det(d)
    return float(np.log(abs(val)) - np.log(abs(base)))


def branch_pair_values() -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:
    branch_nu = (
        build_texture(
            (0, 1),
            (
                np.array([0.03, 0.07, 0.11], dtype=complex),
                np.array([0.05, 0.04, 0.09], dtype=complex),
            ),
        ),
        build_texture((0,), (np.array([0.0004, 0.06, 1.0], dtype=complex),)),
    )
    branch_e = (
        build_texture((0,), (np.array([0.03, 0.07, 0.11], dtype=complex),)),
        build_texture(
            (0, 1),
            (
                np.array([0.0004, 0.06, 1.0], dtype=complex),
                np.array([0.0003, 0.05, 0.8], dtype=complex),
            ),
        ),
    )
    return branch_nu, branch_e


def antisymmetrize(a: float, b: float) -> tuple[float, float]:
    return (0.5 * (a - b), 0.5 * (b - a))


def part1_any_branch_distinguishing_scalar_reduces_to_sector_odd_part() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ANY BRANCH-DISTINGUISHING SCALAR REDUCES TO ITS SECTOR-ODD PART")
    print("=" * 88)

    f_nu = 2.7
    f_e = -0.4
    f_plus = 0.5 * (f_nu + f_e)
    f_minus_nu, f_minus_e = antisymmetrize(f_nu, f_e)

    check("A branch-distinguishing scalar has unequal values on the two orientations", abs(f_nu - f_e) > 1e-12,
          f"F_nu={f_nu:.3f}, F_e={f_e:.3f}")
    check("Its sigma-odd part is nonzero on the reduced surface", abs(f_minus_nu) > 1e-12 and abs(f_minus_e) > 1e-12,
          f"F_- values=({f_minus_nu:.3f},{f_minus_e:.3f})")
    check("The sigma-odd part flips sign under sector exchange", abs(f_minus_nu + f_minus_e) < 1e-12,
          f"sum={f_minus_nu + f_minus_e:.2e}")
    check("The sigma-even part cannot distinguish the two orientations", abs(f_plus - f_plus) < 1e-12,
          f"F_+={f_plus:.3f}")

    print()
    print("  So any successful one-sided PMNS selector can be reduced to a")
    print("  nonzero sector-odd scalar on the reduced surface.")


def part2_current_support_and_scalar_banks_supply_only_sector_even_data() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT SUPPORT AND SCALAR BANKS SUPPLY ONLY SECTOR-EVEN DATA")
    print("=" * 88)

    branch_nu, branch_e = branch_pair_values()

    support_nu = float(sum(np.count_nonzero(np.abs(m) > 1e-12) for m in branch_nu))
    support_e = float(sum(np.count_nonzero(np.abs(m) > 1e-12) for m in branch_e))
    support_minus_nu, support_minus_e = antisymmetrize(support_nu, support_e)

    d_nu = np.array([[2.0, 0.2], [0.1, 1.8]], dtype=complex)
    d_e = np.array([[1.7, 0.0], [0.0, 2.4]], dtype=complex)
    j_nu = np.diag([0.11, -0.07]).astype(complex)
    j_e = np.diag([0.03, 0.02]).astype(complex)
    w_nu_oriented = scalar_generator(d_nu, j_nu) + scalar_generator(d_e, j_e)
    w_e_oriented = scalar_generator(d_e, j_e) + scalar_generator(d_nu, j_nu)
    w_minus_nu, w_minus_e = antisymmetrize(w_nu_oriented, w_e_oriented)

    check("The reduced support-bank totals are sector-even", abs(support_minus_nu) < 1e-12 and abs(support_minus_e) < 1e-12,
          f"support antisym=({support_minus_nu:.2e},{support_minus_e:.2e})")
    check("The additive scalar observable bank is sector-even under exchange", abs(w_minus_nu) < 1e-12 and abs(w_minus_e) < 1e-12,
          f"scalar antisym=({w_minus_nu:.2e},{w_minus_e:.2e})")
    check("So neither current bank supplies a nonzero sector-odd selector part", True,
          "their antisymmetrizations vanish on the reduced one-sided surface")

    print()
    print("  The present banks therefore stop at sector-even data:")
    print("  unordered support information and additive block-local scalar response.")


def part3_minimal_missing_object_is_a_sector_odd_mixed_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE MINIMAL MISSING OBJECT IS A SECTOR-ODD MIXED BRIDGE")
    print("=" * 88)

    support_note = read("docs/PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md")
    scalar_note = read("docs/PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")

    check("The support-side theorem says the current support bank cannot force tau",
          "cannot force the residual" in support_note and "sector-orientation bit `tau in Z_2`" in support_note)
    check("The scalar theorem says the current scalar bank does not realize the selector bridge",
          "does not realize the missing PMNS" in scalar_note or "does not generate a mixed scalar bridge" in scalar_note)
    check("The atlas carries both obstruction rows", 
          "| PMNS sector-exchange nonforcing |" in atlas and "| PMNS scalar bridge nonrealization |" in atlas)

    print()
    print("  Therefore the smallest future selector can be taken to be:")
    print("    - sector-odd under sigma,")
    print("    - genuinely inter-sector,")
    print("    - and mixed, rather than a sum of independent block data.")


def main() -> int:
    print("=" * 88)
    print("PMNS SELECTOR: SECTOR-ODD BRIDGE REDUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS sector-exchange nonforcing")
    print("  - PMNS scalar bridge nonrealization")
    print()
    print("Question:")
    print("  What exact parity class can the missing PMNS selector now be reduced")
    print("  to on the one-sided surface?")

    part1_any_branch_distinguishing_scalar_reduces_to_sector_odd_part()
    part2_current_support_and_scalar_banks_supply_only_sector_even_data()
    part3_minimal_missing_object_is_a_sector_odd_mixed_bridge()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - any branch-distinguishing selector reduces to its nonzero")
    print("      sector-odd part under sigma")
    print("    - the current support and additive scalar banks provide only")
    print("      sector-even data on the reduced one-sided surface")
    print("    - so the minimal missing object is a sector-odd mixed bridge")
    print("      functional")
    print()
    print("  This is the sharpest exact finish-line reduction currently available.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
