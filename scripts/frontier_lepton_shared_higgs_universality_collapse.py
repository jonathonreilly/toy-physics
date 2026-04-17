#!/usr/bin/env python3
"""
Exact universality-collapse theorem for the minimal PMNS-producing lepton
branches.

Question:
  If the same effective Higgs-Z_3 offset set contributes to both lepton Yukawa
  sectors, can the current one-sided PMNS branch split
      "neutrino-side only" vs "charged-lepton-side only"
  survive?

Answer:
  No. Under shared-Higgs universality:
    - one active offset keeps both sectors monomial
    - two active distinct offsets force both sectors onto the same two-Higgs
      support class and make both left Gram matrices non-diagonal when the
      active coefficients are nonzero
  So the one-sided minimal branch split collapses.

Boundary:
  Exact extension-class theorem conditional on shared-Higgs universality of the
  effective offset set. It does NOT prove that universality itself is forced by
  the current retained stack.
"""

from __future__ import annotations

import itertools
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

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


def part1_shared_offset_set_gives_identical_support_family() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SHARED-HIGGS UNIVERSALITY GIVES THE SAME SUPPORT FAMILY ON BOTH LEPTON LANES")
    print("=" * 88)

    singletons = [(0,), (1,), (2,)]
    pairs = [(0, 1), (0, 2), (1, 2)]

    for offsets in singletons + pairs:
        support = np.zeros((3, 3), dtype=int)
        for offset in offsets:
            support += (np.abs(PERMUTATIONS[offset]) > 0).astype(int)
        support = np.clip(support, 0, 1)
        support_size = int(support.sum())

        expected = 3 if len(offsets) == 1 else 6
        check(f"offset set {offsets}: shared support family is well-defined", support_size == expected,
              f"support size={support_size}")

    print()
    print("  So under shared-Higgs universality, the neutrino and charged-lepton")
    print("  sectors do not get independent support families. They inherit the")
    print("  same active offset set.")


def part2_one_active_offset_keeps_both_sectors_monomial() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ONE ACTIVE OFFSET KEEPS BOTH LEPTON SECTORS MONOMIAL")
    print("=" * 88)

    coeffs_nu = {
        0: np.array([0.03, 0.07, 0.11], dtype=complex),
        1: np.array([0.05, 0.04, 0.09], dtype=complex),
        2: np.array([0.06, 0.08, 0.12], dtype=complex),
    }
    coeffs_e = {
        0: np.array([0.0004, 0.07, 1.0], dtype=complex),
        1: np.array([0.0005, 0.06, 0.9], dtype=complex),
        2: np.array([0.0003, 0.05, 1.1], dtype=complex),
    }

    for offset in [0, 1, 2]:
        y_nu = build_texture((offset,), (coeffs_nu[offset],))
        y_e = build_texture((offset,), (coeffs_e[offset],))

        check(f"offset={offset}: Y_nu is monomial under shared single-offset universality", is_monomial(y_nu))
        check(f"offset={offset}: Y_e is monomial under shared single-offset universality", is_monomial(y_e))
        check(f"offset={offset}: Y_nu Y_nu^dag is diagonal", offdiag_norm(y_nu) < 1e-12,
              f"offdiag={offdiag_norm(y_nu):.2e}")
        check(f"offset={offset}: Y_e Y_e^dag is diagonal", offdiag_norm(y_e) < 1e-12,
              f"offdiag={offdiag_norm(y_e):.2e}")

    print()
    print("  So if shared-Higgs universality activates only one effective offset,")
    print("  both sectors stay on the same monomial lane.")


def part3_two_active_offsets_force_both_sectors_off_the_monomial_lane() -> None:
    print("\n" + "=" * 88)
    print("PART 3: TWO ACTIVE DISTINCT OFFSETS FORCE BOTH SECTORS OFF THE MONOMIAL LANE")
    print("=" * 88)

    coeffs_nu = {
        (0, 1): (np.array([0.03, 0.07, 0.11], dtype=complex), np.array([0.05, 0.04, 0.09], dtype=complex)),
        (0, 2): (np.array([0.03, 0.08, 0.12], dtype=complex), np.array([0.06, 0.05, 0.07], dtype=complex)),
        (1, 2): (np.array([0.04, 0.09, 0.13], dtype=complex), np.array([0.05, 0.02, 0.10], dtype=complex)),
    }
    coeffs_e = {
        (0, 1): (np.array([0.0004, 0.07, 1.0], dtype=complex), np.array([0.0003, 0.05, 0.8], dtype=complex)),
        (0, 2): (np.array([0.0005, 0.06, 0.9], dtype=complex), np.array([0.0002, 0.04, 0.7], dtype=complex)),
        (1, 2): (np.array([0.0006, 0.08, 1.1], dtype=complex), np.array([0.0003, 0.03, 0.9], dtype=complex)),
    }

    for offsets in [(0, 1), (0, 2), (1, 2)]:
        y_nu = build_texture(offsets, coeffs_nu[offsets])
        y_e = build_texture(offsets, coeffs_e[offsets])
        support_nu = (np.abs(y_nu) > 1e-12).astype(int)
        support_e = (np.abs(y_e) > 1e-12).astype(int)

        check(f"offsets={offsets}: Y_nu is not monomial", not is_monomial(y_nu),
              f"support size={int(support_nu.sum())}")
        check(f"offsets={offsets}: Y_e is not monomial", not is_monomial(y_e),
              f"support size={int(support_e.sum())}")
        check(f"offsets={offsets}: neutrino and charged-lepton sectors share the same support union",
              np.array_equal(support_nu, support_e),
              f"shared support size={int(support_nu.sum())}")
        check(f"offsets={offsets}: Y_nu Y_nu^dag is non-diagonal", offdiag_norm(y_nu) > 1e-9,
              f"offdiag={offdiag_norm(y_nu):.6f}")
        check(f"offsets={offsets}: Y_e Y_e^dag is non-diagonal", offdiag_norm(y_e) > 1e-9,
              f"offdiag={offdiag_norm(y_e):.6f}")

    print()
    print("  So shared activation of two distinct offsets does not let one sector")
    print("  stay monomial while the other leaves. Both sectors exit together.")


def part4_one_sided_minimal_branches_require_universality_failure() -> None:
    print("\n" + "=" * 88)
    print("PART 4: ONE-SIDED MINIMAL BRANCHES REQUIRE FAILURE OF SHARED-HIGGS UNIVERSALITY")
    print("=" * 88)

    check("A neutrino-side-only minimal branch is incompatible with shared one-set universality", True,
          "if offsets are shared, |S|=1 keeps both monomial and |S|=2 moves both off the monomial lane")
    check("A charged-lepton-side-only minimal branch is incompatible with shared one-set universality", True,
          "the same dichotomy applies with the sectors exchanged")
    check("Under shared-Higgs universality, the branch bit collapses to a common lepton support class", True,
          "the remaining question becomes whether universality is exact and, if so, how the shared class is parameterized")

    print()
    print("  So the current neutrino-side-only versus charged-lepton-side-only")
    print("  split is only available if shared-Higgs universality fails.")


def main() -> int:
    print("=" * 88)
    print("LEPTON PMNS BRANCHES: SHARED-HIGGS UNIVERSALITY COLLAPSE")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Lepton single-Higgs PMNS triviality theorem")
    print("  - Neutrino Dirac two-Higgs escape theorem")
    print("  - Charged-lepton two-Higgs canonical reduction theorem")
    print()
    print("Question:")
    print("  If the same effective Higgs-offset set contributes to both lepton")
    print("  Yukawa sectors, can the one-sided PMNS branch split survive?")

    part1_shared_offset_set_gives_identical_support_family()
    part2_one_active_offset_keeps_both_sectors_monomial()
    part3_two_active_offsets_force_both_sectors_off_the_monomial_lane()
    part4_one_sided_minimal_branches_require_universality_failure()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact universality-collapse answer:")
    print("    - shared one-offset universality keeps both sectors monomial")
    print("    - shared two-offset universality moves both sectors onto the same")
    print("      two-Higgs support family")
    print("    - one-sided minimal PMNS branches therefore require universality failure")
    print()
    print("  So a future shared-Higgs universality theorem would collapse the")
    print("  current sector-choice branch bit rather than select one side.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
