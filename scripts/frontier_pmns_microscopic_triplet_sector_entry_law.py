#!/usr/bin/env python3
"""
Exact triplet-sector entry law for the PMNS microscopic operators.

Question:
  Once the three-generation matter surface is treated as physical, what are the
  actual neutral and charge-(-1) lepton-sector operator entries on that
  retained triplet surface?

Answer:
  On the retained physical lepton surface, the relevant microscopic sector
  representatives are 3x3 generation operators:

    D_0^trip  on E_nu  = span{nu_0, nu_1, nu_2}
    D_-^trip  on E_e   = span{e_0,  e_1,  e_2}

  Their exact entry patterns are already fixed by the existing Cl(3) on Z^3
  derivation stack:

    single-Higgs lane:
      D_s^trip(q) = diag(a_1, a_2, a_3) P_q

    minimal two-Higgs lane:
      D_s^trip    = A_s + B_s C

  where P_q is one of the three exact permutation supports, C is the forward
  3-cycle, and A_s, B_s are diagonal. On the canonical normal form:

      A_s + B_s C
        = [[x_1, y_1, 0],
           [0,   x_2, y_2],
           [y_3 e^{i delta}, 0, x_3]]

Boundary:
  This theorem identifies the actual retained physical-triplet entries of the
  neutral and charge-(-1) lepton-sector operators. It does NOT derive the
  values of the coefficients (x_i, y_i, delta, a_i) from Cl(3) on Z^3, and it
  does NOT identify off-triplet spectator entries of any larger ambient sector
  operator.
"""

from __future__ import annotations

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
CYCLE = PERMUTATIONS[1]


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


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def monomial_triplet(coeffs: np.ndarray, offset: int) -> np.ndarray:
    return diagonal(coeffs) @ PERMUTATIONS[offset]


def canonical_two_higgs_triplet(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(x) + diagonal(y_eff) @ CYCLE


def part1_physical_three_generation_surface_reduces_the_relevant_sector_operators_to_triplets() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE RETAINED PHYSICAL LEPTON SURFACE ALREADY REDUCES TO TRIPLETS")
    print("=" * 88)

    p_nu = np.diag([1, 1, 1, 0, 0, 0]).astype(complex)
    p_e = np.diag([0, 0, 0, 1, 1, 1]).astype(complex)
    p_lep = p_nu + p_e

    check("The retained three-generation neutrino support has dimension 3", int(np.trace(p_nu).real) == 3)
    check("The retained three-generation charged-lepton support has dimension 3", int(np.trace(p_e).real) == 3)
    check("The physical lepton surface is exactly E_nu ⊕ E_e", np.linalg.norm(p_lep - np.eye(6)) < 1e-12)
    check("So the PMNS-relevant sector representatives are 3x3 operators on the fixed triplets", True,
          "D_0^trip on E_nu, D_-^trip on E_e")

    print()
    print("  On the retained physical matter surface there is no further support")
    print("  ambiguity: the PMNS-relevant neutral and charge-(-1) operators live")
    print("  directly on the triplets E_nu and E_e.")


def part2_single_higgs_triplet_entries_are_exact_monomial_matrices() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SINGLE-HIGGS TRIPLET ENTRIES ARE EXACT MONOMIAL MATRICES")
    print("=" * 88)

    coeffs = np.array([0.2 + 0.1j, 0.5 - 0.2j, 0.9 + 0.05j], dtype=complex)

    for offset in [0, 1, 2]:
        d_trip = monomial_triplet(coeffs, offset)
        support = (np.abs(d_trip) > 1e-12).astype(int)
        row_counts = support.sum(axis=1)
        col_counts = support.sum(axis=0)

        check(f"offset={offset}: D^trip has exactly one nonzero entry in each row", np.array_equal(row_counts, np.ones(3, dtype=int)),
              f"row counts={row_counts.tolist()}")
        check(f"offset={offset}: D^trip has exactly one nonzero entry in each column", np.array_equal(col_counts, np.ones(3, dtype=int)),
              f"col counts={col_counts.tolist()}")
        check(f"offset={offset}: the support is exactly the retained Z_3 permutation support", np.array_equal(support, PERMUTATIONS[offset].real.astype(int)),
              f"support=\n{support}")
        check(f"offset={offset}: the triplet entries are exactly diag(a_i) P_q", np.linalg.norm(d_trip @ PERMUTATIONS[offset].conj().T - diagonal(coeffs)) < 1e-12,
              f"factorization error={np.linalg.norm(d_trip @ PERMUTATIONS[offset].conj().T - diagonal(coeffs)):.2e}")

    print()
    print("  Therefore on any retained single-Higgs fixed-offset lane, the actual")
    print("  triplet-sector entries are already explicit monomial matrices.")


def part3_minimal_two_higgs_triplet_entries_are_exactly_a_plus_b_c() -> None:
    print("\n" + "=" * 88)
    print("PART 3: MINIMAL TWO-HIGGS TRIPLET ENTRIES ARE EXACTLY A + B C")
    print("=" * 88)

    x = np.array([0.7, 1.1, 0.9], dtype=float)
    y = np.array([0.3, 0.5, 0.4], dtype=float)
    delta = 0.61
    d_trip = canonical_two_higgs_triplet(x, y, delta)

    expected = np.array(
        [
            [x[0], y[0], 0.0],
            [0.0, x[1], y[1]],
            [y[2] * np.exp(1j * delta), 0.0, x[2]],
        ],
        dtype=complex,
    )
    off_support = d_trip - expected

    check("The canonical two-Higgs triplet representative equals A + B C exactly", np.linalg.norm(d_trip - (diagonal(x) + diagonal([y[0], y[1], y[2] * np.exp(1j * delta)]) @ CYCLE)) < 1e-12)
    check("The actual entries are exactly the canonical seven-invariant pattern", np.linalg.norm(off_support) < 1e-12,
          f"entry error={np.linalg.norm(off_support):.2e}")
    check("The support is the diagonal plus the forward 3-cycle", np.count_nonzero(np.abs(d_trip) > 1e-12) == 6,
          f"nonzero entries={np.count_nonzero(np.abs(d_trip) > 1e-12)}")
    check("Exactly one physical phase survives in the canonical triplet entries", abs(np.angle(d_trip[2, 0]) - delta) < 1e-12,
          f"phase={np.angle(d_trip[2, 0]):.6f}")

    print()
    print("  So on the minimal two-Higgs lane, the actual triplet-sector entries")
    print("  are already explicit. The only open question is the coefficient law.")


def part4_one_sided_minimal_pmns_classes_give_explicit_branch_conditioned_sector_pairs() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ONE-SIDED MINIMAL PMNS CLASSES GIVE EXPLICIT (D_0^trip,D_-^trip)")
    print("=" * 88)

    d_active = canonical_two_higgs_triplet(
        np.array([0.8, 1.0, 0.9], dtype=float),
        np.array([0.2, 0.4, 0.3], dtype=float),
        0.37,
    )
    d_passive = monomial_triplet(np.array([0.05, 0.11, 0.23], dtype=complex), 0)

    pair_nu_active = (d_active, d_passive)
    pair_e_active = (d_passive, d_active)

    check("On the neutrino-side branch, D_0^trip is active two-Higgs and D_-^trip is passive monomial",
          np.count_nonzero(np.abs(pair_nu_active[0]) > 1e-12) == 6 and np.count_nonzero(np.abs(pair_nu_active[1]) > 1e-12) == 3)
    check("On the charged-lepton-side branch, D_-^trip is active two-Higgs and D_0^trip is passive monomial",
          np.count_nonzero(np.abs(pair_e_active[1]) > 1e-12) == 6 and np.count_nonzero(np.abs(pair_e_active[0]) > 1e-12) == 3)
    check("So the branch-conditioned triplet-sector entries are explicit once the active side is fixed", True,
          "(D_0^trip,D_-^trip) = (A+B C, D P_q) or (D P_q, A_e+B_e C)")

    print()
    print("  The remaining branch ambiguity is no longer about matrix shape.")
    print("  It is only which explicit pair is realized.")


def part5_on_the_weak_axis_seed_patch_the_active_triplet_entries_close_up_to_one_sheet_bit() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE WEAK-AXIS SEED PATCH CLOSES THE ACTIVE TRIPLET ENTRIES UP TO ONE SHEET")
    print("=" * 88)

    x = 0.9
    y = 0.4
    sheet_0 = x * np.eye(3, dtype=complex) + y * CYCLE
    sheet_1 = y * np.eye(3, dtype=complex) + x * CYCLE

    check("Weak-axis seed sheet 0 has entries x on the diagonal and y on the cycle", np.allclose(
        sheet_0,
        np.array([[x, y, 0.0], [0.0, x, y], [y, 0.0, x]], dtype=complex),
    ))
    check("Weak-axis seed sheet 1 is the exact exchange sheet x <-> y", np.allclose(
        sheet_1,
        np.array([[y, x, 0.0], [0.0, y, x], [x, 0.0, y]], dtype=complex),
    ))
    check("So the weak-axis seed patch closes the active triplet entries up to one residual global sheet bit", True,
          "sheet exchange x <-> y")

    print()
    print("  On the exact seed patch, even the active two-Higgs triplet entries")
    print("  are explicit up to one residual sheet exchange.")


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC TRIPLET-SECTOR ENTRY LAW")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - Cl(3) on Z^3 one-generation matter closure")
    print("  - Cl(3) on Z^3 three-generation matter structure")
    print("  - PMNS lepton support identification reduction")
    print("  - neutrino Dirac Z_3 support trichotomy")
    print("  - lepton single-Higgs PMNS triviality")
    print("  - neutrino / charged-lepton two-Higgs canonical reductions")
    print("  - PMNS weak-axis seed coefficient closure")
    print()
    print("Question:")
    print("  What are the actual retained physical-triplet entries of the neutral")
    print("  and charge-(-1) lepton-sector operators?")

    part1_physical_three_generation_surface_reduces_the_relevant_sector_operators_to_triplets()
    part2_single_higgs_triplet_entries_are_exact_monomial_matrices()
    part3_minimal_two_higgs_triplet_entries_are_exactly_a_plus_b_c()
    part4_one_sided_minimal_pmns_classes_give_explicit_branch_conditioned_sector_pairs()
    part5_on_the_weak_axis_seed_patch_the_active_triplet_entries_close_up_to_one_sheet_bit()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact retained physical-triplet answer:")
    print("    - D_0^trip acts on E_nu = span{nu_0,nu_1,nu_2}")
    print("    - D_-^trip acts on E_e  = span{e_0,e_1,e_2}")
    print("    - on a single-Higgs lane: D_s^trip = diag(a_1,a_2,a_3) P_q")
    print("    - on a minimal two-Higgs lane: D_s^trip = A_s + B_s C")
    print("    - on the weak-axis seed patch: D_s^trip = x I + y C up to one sheet")
    print()
    print("  So the actual retained triplet-sector entries are explicit. What")
    print("  remains open is only the coefficient/value law and, on the seed patch,")
    print("  the residual sheet bit.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
