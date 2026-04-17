#!/usr/bin/env python3
"""
Current-stack underdetermination theorem for shared-Higgs universality on the
lepton Yukawa lanes.

Question:
  Does the present retained stack force shared-Higgs universality between the
  neutrino and charged-lepton Yukawa sectors, or force its failure?

Answer:
  No. The current exact support grammar admits:
    - universal one-offset lepton assignments
    - universal two-offset lepton assignments
    - non-universal neutrino-side-only PMNS-producing assignments
    - non-universal charged-lepton-side-only PMNS-producing assignments
  and the current atlas contains no retained bridge theorem selecting among
  them.

Boundary:
  Current-stack theorem only. It does not claim universality or non-universality
  are impossible to derive in future work.
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


def part1_universal_and_nonuniversal_assignments_are_both_exactly_admissible() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT SUPPORT GRAMMAR ADMITS BOTH UNIVERSAL AND NON-UNIVERSAL ASSIGNMENTS")
    print("=" * 88)

    coeffs_single_nu = (np.array([0.03, 0.07, 0.11], dtype=complex),)
    coeffs_single_e = (np.array([0.0004, 0.06, 1.0], dtype=complex),)
    coeffs_pair_nu = (
        np.array([0.03, 0.07, 0.11], dtype=complex),
        np.array([0.05, 0.04, 0.09], dtype=complex),
    )
    coeffs_pair_e = (
        np.array([0.0004, 0.06, 1.0], dtype=complex),
        np.array([0.0003, 0.05, 0.8], dtype=complex),
    )

    cases = {
        "universal_single": ((0,), coeffs_single_nu, (0,), coeffs_single_e),
        "universal_pair": ((0, 1), coeffs_pair_nu, (0, 1), coeffs_pair_e),
        "nonuniversal_nu_side": ((0, 1), coeffs_pair_nu, (0,), coeffs_single_e),
        "nonuniversal_e_side": ((0,), coeffs_single_nu, (0, 1), coeffs_pair_e),
    }

    for name, (offsets_nu, coeffs_nu, offsets_e, coeffs_e) in cases.items():
        y_nu = build_texture(offsets_nu, coeffs_nu)
        y_e = build_texture(offsets_e, coeffs_e)
        support_nu = int(np.count_nonzero(np.abs(y_nu) > 1e-12))
        support_e = int(np.count_nonzero(np.abs(y_e) > 1e-12))

        check(f"{name}: neutrino-side support is exact and admissible", support_nu in {3, 6},
              f"support size={support_nu}")
        check(f"{name}: charged-lepton-side support is exact and admissible", support_e in {3, 6},
              f"support size={support_e}")

    print()
    print("  So the current support grammar itself does not force universality or")
    print("  force its failure. Both kinds of assignment exist exactly.")


def part2_current_stack_allows_both_universal_and_nonuniversal_pmns_patterns() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT STACK ALLOWS BOTH UNIVERSAL AND NON-UNIVERSAL PMNS PATTERNS")
    print("=" * 88)

    y_nu_univ_single = build_texture((0,), (np.array([0.03, 0.07, 0.11], dtype=complex),))
    y_e_univ_single = build_texture((0,), (np.array([0.0004, 0.06, 1.0], dtype=complex),))

    y_nu_univ_pair = build_texture(
        (0, 1),
        (np.array([0.03, 0.07, 0.11], dtype=complex), np.array([0.05, 0.04, 0.09], dtype=complex)),
    )
    y_e_univ_pair = build_texture(
        (0, 1),
        (np.array([0.0004, 0.06, 1.0], dtype=complex), np.array([0.0003, 0.05, 0.8], dtype=complex)),
    )

    y_nu_nonuniv = y_nu_univ_pair
    y_e_nonuniv = y_e_univ_single

    check("Universal single-offset assignment keeps both sectors monomial",
          is_monomial(y_nu_univ_single) and is_monomial(y_e_univ_single))
    check("Universal single-offset assignment gives diagonal left Gram matrices",
          offdiag_norm(y_nu_univ_single) < 1e-12 and offdiag_norm(y_e_univ_single) < 1e-12,
          f"offdiag_nu={offdiag_norm(y_nu_univ_single):.2e}, offdiag_e={offdiag_norm(y_e_univ_single):.2e}")

    check("Universal two-offset assignment moves both sectors off the monomial lane",
          (not is_monomial(y_nu_univ_pair)) and (not is_monomial(y_e_univ_pair)))
    check("Universal two-offset assignment gives non-diagonal left Gram matrices on both sectors",
          offdiag_norm(y_nu_univ_pair) > 1e-9 and offdiag_norm(y_e_univ_pair) > 1e-9,
          f"offdiag_nu={offdiag_norm(y_nu_univ_pair):.6f}, offdiag_e={offdiag_norm(y_e_univ_pair):.6f}")

    check("A non-universal neutrino-side-only assignment is also exactly admissible",
          (not is_monomial(y_nu_nonuniv)) and is_monomial(y_e_nonuniv))
    check("That non-universal assignment reproduces the one-sided branch pattern",
          offdiag_norm(y_nu_nonuniv) > 1e-9 and offdiag_norm(y_e_nonuniv) < 1e-12,
          f"offdiag_nu={offdiag_norm(y_nu_nonuniv):.6f}, offdiag_e={offdiag_norm(y_e_nonuniv):.2e}")

    print()
    print("  So the current exact stack does not even force the qualitative")
    print("  universality pattern of the lepton PMNS-producing assignment.")


def part3_current_atlas_has_no_universality_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT ATLAS CARRIES NO SHARED-HIGGS UNIVERSALITY BRIDGE")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    validation = read("docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP.md")
    packet = read("docs/publication/ci3_z3/NEUTRINO_DIRAC_PMNS_BOUNDARY_PACKET_2026-04-15.md")
    atlas_lower = atlas.lower()

    has_qh_under = "| Neutrino Higgs `Z_3` underdetermination |" in atlas
    has_nonselection = "| PMNS minimal-branch nonselection |" in atlas
    has_univ_collapse = "| Lepton shared-Higgs universality collapse |" in atlas
    has_univ_bridge = "shared-higgs `z_3` universality theorem" in atlas_lower
    validation_open = "Higgs `Z_3` universality" in validation
    packet_mentions_future_universality = "future shared-Higgs universality theorem" in packet

    check("Atlas carries the Higgs-Z_3 underdetermination row", has_qh_under)
    check("Atlas carries the PMNS nonselection row", has_nonselection)
    check("Atlas carries the universality-collapse conditional row", has_univ_collapse)
    check("Atlas still does not carry a retained universality bridge theorem", not has_univ_bridge)
    check("Publication controls still record Higgs-Z_3 universality as open", validation_open)
    check("The PMNS packet treats universality as future work, not as closed", packet_mentions_future_universality)

    print()
    print("  So the current atlas state matches the constructive examples:")
    print("    - universality can be discussed conditionally,")
    print("    - but it is not forced or rejected by any retained bridge theorem.")


def main() -> int:
    print("=" * 88)
    print("LEPTON SHARED-HIGGS UNIVERSALITY: CURRENT-STACK UNDERDETERMINATION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Neutrino Higgs Z_3 underdetermination")
    print("  - Lepton single-Higgs PMNS triviality theorem")
    print("  - Neutrino Dirac two-Higgs escape theorem")
    print("  - Lepton shared-Higgs universality collapse theorem")
    print()
    print("Question:")
    print("  Does the present retained stack force shared-Higgs universality, or")
    print("  force its failure, on the lepton Yukawa lanes?")

    part1_universal_and_nonuniversal_assignments_are_both_exactly_admissible()
    part2_current_stack_allows_both_universal_and_nonuniversal_pmns_patterns()
    part3_current_atlas_has_no_universality_bridge()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-stack answer:")
    print("    - shared-Higgs universality is not forced")
    print("    - universality failure is not forced")
    print("    - both universal and non-universal lepton assignments remain")
    print("      exact admissible extension classes")
    print()
    print("  So the remaining selector science is now explicit: derive an")
    print("  inter-sector universality bridge theorem, or derive a theorem of")
    print("  universality failure. The current stack does neither.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
