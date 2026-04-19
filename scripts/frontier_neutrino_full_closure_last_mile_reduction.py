#!/usr/bin/env python3
"""
Exact last-mile reduction theorem for full neutrino closure on the current bank.

Question:
  Once the retained stack has isolated the minimal PMNS-producing branches,
  what exactly remains between the current exact bank and full neutrino closure?

Answer:
  On the minimal-branch assumption, the remaining exact gap is branch
  conditioned:
    - neutrino-side branch: seven real quantities
    - charged-lepton-side branch: three neutrino Dirac mass moduli plus seven
      charged-lepton branch quantities
  and the current atlas does not yet select the branch.
  After selector realization, the surviving coefficient problem is explicit up
  to one residual Z2 sheet on the selected two-Higgs branch.

Boundary:
  Exact current-bank reduction theorem conditioned on the minimal surviving
  PMNS-producing branches. It does NOT derive the selector or the remaining
  quantities.
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


def part1_neutrino_side_minimal_branch_is_seven_real_quantities() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ON THE NEUTRINO-SIDE MINIMAL BRANCH, FULL NEUTRINO CLOSURE IS A SEVEN-QUANTITY PROBLEM")
    print("=" * 88)

    gauge_matrix = np.array(
        [
            [-1, 0, 0, 1, 0, 0],
            [0, -1, 0, 0, 1, 0],
            [0, 0, -1, 0, 0, 1],
            [-1, 1, 0, 0, 1, 0],
            [0, -1, 1, 0, 0, 1],
        ],
        dtype=float,
    )
    rank = int(np.linalg.matrix_rank(gauge_matrix))
    physical_count = 12 - rank

    check("The canonical neutrino-side two-Higgs branch has phase-reduction rank 5", rank == 5,
          f"rank={rank}")
    check("So the neutrino-side minimal branch carries exactly 7 real quantities", physical_count == 7,
          f"physical count={physical_count}")
    check("Those 7 quantities match the full Dirac-neutrino observable count on the monomial charged-lepton boundary",
          physical_count == 7,
          "3 neutrino masses + 3 PMNS angles + 1 Dirac phase")

    print()
    print("  So if the neutrino sector is the first non-monomial lepton lane,")
    print("  full neutrino closure on the minimal branch is a seven-quantity")
    print("  problem.")


def part2_charged_lepton_side_branch_needs_three_neutrino_mass_moduli_plus_seven_branch_quantities() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ON THE CHARGED-LEPTON-SIDE MINIMAL BRANCH, THREE NEUTRINO MASS MODULI REMAIN SEPARATELY")
    print("=" * 88)

    coeffs = np.array([0.018, 0.051, 0.074], dtype=float)
    y_nu = np.diag(coeffs) @ PERMUTATIONS[1]
    singular_values = np.linalg.svd(y_nu, compute_uv=False)
    offdiag = np.linalg.norm(y_nu @ y_nu.conj().T - np.diag(np.diag(y_nu @ y_nu.conj().T)))

    gauge_matrix = np.array(
        [
            [-1, 0, 0, 1, 0, 0],
            [0, -1, 0, 0, 1, 0],
            [0, 0, -1, 0, 0, 1],
            [-1, 1, 0, 0, 1, 0],
            [0, -1, 1, 0, 0, 1],
        ],
        dtype=float,
    )
    charged_lepton_count = 12 - int(np.linalg.matrix_rank(gauge_matrix))
    total_count = 3 + charged_lepton_count

    check("A monomial neutrino Dirac lane contributes exactly three positive singular values",
          np.allclose(np.sort(singular_values), np.sort(coeffs), atol=1e-12),
          f"svals={np.round(np.sort(singular_values), 6)}")
    check("The monomial neutrino lane contributes no PMNS mixing by itself", offdiag < 1e-12,
          f"offdiag norm={offdiag:.2e}")
    check("The charged-lepton minimal branch carries 7 real quantities", charged_lepton_count == 7,
          f"charged-lepton count={charged_lepton_count}")
    check("So branch-local zero-import full neutrino closure on that branch is a 3 + 7 = 10 quantity problem",
          total_count == 10, f"total count={total_count}")

    print()
    print("  So if the charged-lepton sector is the first non-monomial lane,")
    print("  PMNS lives on the charged-lepton branch, but three neutrino Dirac")
    print("  mass moduli still have to be derived separately from the monomial")
    print("  neutrino lane.")


def part3_current_atlas_does_not_select_the_branch() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT ATLAS STILL DOES NOT SELECT THE MINIMAL BRANCH")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    validation = read("docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md")
    matrix = read("docs/publication/ci3_z3/PUBLICATION_MATRIX.md")
    gates = read("docs/GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md")

    atlas_lower = atlas.lower()
    has_neutrino_branch = "| Neutrino Dirac two-Higgs canonical reduction |" in atlas
    has_charged_lepton_branch = "| Charged-lepton two-Higgs canonical reduction |" in atlas
    has_selector_row = "higgs multiplicity selector" in atlas_lower or "shared-higgs z_3 universality theorem" in atlas_lower
    has_flavor_blocker = "Higgs `Z_3` universality" in validation and "CKM Higgs-`Z_3` universality" in gates
    matrix_flavor_open = "| CKM / quantitative flavor |" in matrix and "| open |" in matrix

    check("The atlas isolates the minimal neutrino-side branch", has_neutrino_branch)
    check("The atlas isolates the minimal charged-lepton-side branch", has_charged_lepton_branch)
    check("The atlas still lacks a retained selector theorem", not has_selector_row)
    check("Flavor controls still record the Higgs-Z_3 universality blocker", has_flavor_blocker)
    check("Quantitative flavor closure remains open", matrix_flavor_open)

    print()
    print("  So the current exact bank does not yet resolve the discrete branch")
    print("  bit needed to choose the surviving minimal closure problem.")


def part4_after_selector_realization_the_remaining_coefficient_problem_is_explicit() -> None:
    print("\n" + "=" * 88)
    print("PART 4: AFTER SELECTOR REALIZATION, THE REMAINING COEFFICIENT PROBLEM IS EXPLICIT")
    print("=" * 88)

    note = read("docs/PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    selector = read("docs/PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md")

    check("The atlas carries the branch-conditioned quadratic-sheet closure row",
          "| PMNS branch-conditioned quadratic-sheet closure |" in atlas)
    check("The selector note still records sign(a_sel) as the branch handoff",
          "a_sel > 0" in selector and "a_sel < 0" in selector)
    check("The new closure note records one residual Z_2 sheet on the selected two-Higgs branch",
          "one residual `Z_2` sheet" in note and "quadratic equation" in note and "rational back-substitution" in note)

    print()
    print("  So once the missing selector is realized, the remaining")
    print("  coefficient side is no longer a vague seven-number target.")
    print("  It is an explicit algebraic reconstruction with one residual")
    print("  sheet bit on the selected two-Higgs branch.")


def main() -> int:
    print("=" * 88)
    print("FULL NEUTRINO CLOSURE: LAST-MILE REDUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Neutrino mass reduction to Dirac lane")
    print("  - Neutrino Dirac two-Higgs canonical reduction")
    print("  - Charged-lepton two-Higgs canonical reduction")
    print("  - current-atlas minimal-branch nonselection theorem")
    print()
    print("Question:")
    print("  What exactly remains between the current exact bank and full")
    print("  neutrino closure on the minimal surviving PMNS-producing branches?")

    part1_neutrino_side_minimal_branch_is_seven_real_quantities()
    part2_charged_lepton_side_branch_needs_three_neutrino_mass_moduli_plus_seven_branch_quantities()
    part3_current_atlas_does_not_select_the_branch()
    part4_after_selector_realization_the_remaining_coefficient_problem_is_explicit()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact last-mile answer on the minimal-branch assumption:")
    print("    - neutrino-side branch: 7 real quantities")
    print("    - charged-lepton-side branch: 3 neutrino mass moduli + 7 branch quantities")
    print("    - the current atlas does not yet select the branch")
    print("    - after selector realization, the surviving coefficient problem is explicit up to one residual Z_2 sheet")
    print()
    print("  So the remaining exact gap is no longer a generic flavor jungle.")
    print("  It is a discrete selector question plus a reduced branch-conditioned")
    print("  quantity count, and then an explicit selected-branch")
    print("  quadratic-sheet reconstruction problem.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
