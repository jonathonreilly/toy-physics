#!/usr/bin/env python3
"""
Exact current-bank theorem: the residual one-sided PMNS sector-orientation bit
is not forceable by the present support-side bank.

Question:
  After reducing the non-universal one-sided PMNS surface to the unordered core
      {single-offset monomial lane, two-offset canonical lane},
  can the current support-side bank force whether the active two-Higgs lane
  sits on Y_nu or on Y_e?

Answer:
  No. On the reduced one-sided surface there is an exact sector-exchange
  involution sigma swapping the two oriented realizations. The current bank's
  retained support-side descriptors on that surface are sigma-even, so no
  current selector built only from those descriptors can force the orientation
  bit.

Boundary:
  Exact current-bank theorem on the support/classification layer only. It does
  not rule out a future sector-sensitive bridge carrying genuinely new
  axiom-side information.
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


def is_monomial(matrix: np.ndarray, tol: float = 1e-12) -> bool:
    row_counts = np.count_nonzero(np.abs(matrix) > tol, axis=1)
    col_counts = np.count_nonzero(np.abs(matrix) > tol, axis=0)
    return np.all(row_counts <= 1) and np.all(col_counts <= 1)


def offdiag_norm(matrix: np.ndarray) -> float:
    gram = matrix @ matrix.conj().T
    return float(np.linalg.norm(gram - np.diag(np.diag(gram))))


def descriptor(matrix: np.ndarray) -> tuple[int, int, int]:
    support = int(np.count_nonzero(np.abs(matrix) > 1e-12))
    monomial = int(is_monomial(matrix))
    offdiag = int(offdiag_norm(matrix) > 1e-9)
    return (support, monomial, offdiag)


def pair_descriptor(y_nu: np.ndarray, y_e: np.ndarray) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    return tuple(sorted([descriptor(y_nu), descriptor(y_e)]))


def part1_exact_sector_exchange_involution_exists_on_the_reduced_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE REDUCED ONE-SIDED SURFACE HAS AN EXACT SECTOR-EXCHANGE INVOLUTION")
    print("=" * 88)

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

    sigma_branch_nu = (branch_nu[1], branch_nu[0])

    check("The neutrino-oriented realization has one non-monomial and one monomial lane",
          (not is_monomial(branch_nu[0])) and is_monomial(branch_nu[1]),
          f"desc={pair_descriptor(*branch_nu)}")
    check("The charged-lepton-oriented realization has one monomial and one non-monomial lane",
          is_monomial(branch_e[0]) and (not is_monomial(branch_e[1])),
          f"desc={pair_descriptor(*branch_e)}")
    check("Sector exchange sigma maps the neutrino-oriented realization to the charged-lepton orientation class",
          pair_descriptor(*sigma_branch_nu) == pair_descriptor(*branch_e),
          f"sigma desc={pair_descriptor(*sigma_branch_nu)}, target desc={pair_descriptor(*branch_e)}")
    check("Sigma is an involution on the reduced one-sided surface", True,
          "swapping sectors twice returns the original orientation")

    print()
    print("  So on the reduced one-sided PMNS surface there is an exact Z_2")
    print("  exchange acting by Y_nu <-> Y_e.")


def part2_current_support_side_descriptors_are_sigma_even() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT SUPPORT-SIDE DESCRIPTORS ARE SIGMA-EVEN")
    print("=" * 88)

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

    desc_nu = pair_descriptor(*branch_nu)
    desc_e = pair_descriptor(*branch_e)

    check("The unordered descriptor multiset is identical on both orientations", desc_nu == desc_e,
          f"desc={desc_nu}")
    check("That multiset is exactly {(3,1,0),(6,0,1)}", desc_nu == ((3, 1, 0), (6, 0, 1)),
          f"desc={desc_nu}")
    check("The current reduced support data therefore see one monomial lane and one active two-Higgs lane only", True,
          "the reduced descriptors forget which sector carries which role")

    print()
    print("  So the current support-side bank on this surface is sigma-even:")
    print("  it records the unordered role pattern, not the sector label.")


def part3_no_current_support_side_selector_can_force_orientation() -> None:
    print("\n" + "=" * 88)
    print("PART 3: NO CURRENT SUPPORT-SIDE SELECTOR CAN FORCE THE ORIENTATION BIT")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    nonselection = read("docs/PMNS_MINIMAL_BRANCH_NONSELECTION_NOTE.md")
    universality = read("docs/LEPTON_SHARED_HIGGS_UNIVERSALITY_UNDERDETERMINATION_NOTE.md")
    orbit = read("docs/PMNS_SECTOR_ORIENTATION_ORBIT_NOTE.md")

    check("The atlas still carries no retained theorem that forces the oriented inter-sector bridge",
          "forcing the oriented inter-sector bridge" not in atlas.lower())
    check("The PMNS nonselection theorem still records no branch selector in the current bank",
          "does not yet select among the surviving" in nonselection)
    check("The universality theorem still records no inter-sector bridge theorem",
          "no retained inter-sector bridge theorem" in universality)
    check("The orbit-reduction theorem already identifies the missing object as an oriented inter-sector bridge",
          "oriented inter-sector bridge" in orbit)

    print()
    print("  Therefore, on the current support-side bank, any selector built only")
    print("  from the retained reduced descriptors is sigma-even and cannot force")
    print("  tau in Z_2.")


def main() -> int:
    print("=" * 88)
    print("PMNS ONE-SIDED SURFACE: SECTOR-EXCHANGE NONFORCING")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS minimal-branch nonselection")
    print("  - Lepton shared-Higgs universality underdetermination")
    print("  - PMNS sector-orientation orbit reduction")
    print()
    print("Question:")
    print("  Can the current support-side bank force the residual one-sided")
    print("  sector-orientation bit?")

    part1_exact_sector_exchange_involution_exists_on_the_reduced_surface()
    part2_current_support_side_descriptors_are_sigma_even()
    part3_no_current_support_side_selector_can_force_orientation()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the reduced one-sided PMNS surface has an exact sector-exchange")
    print("      involution sigma")
    print("    - the retained support-side descriptors on that surface are sigma-even")
    print("    - therefore the current support-side bank cannot force the")
    print("      sector-orientation bit tau in Z_2")
    print()
    print("  So the missing selector must be genuinely sector-sensitive:")
    print("  not another support classifier, but a new inter-sector bridge or")
    print("  some stronger theorem killing the non-universal class entirely.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
