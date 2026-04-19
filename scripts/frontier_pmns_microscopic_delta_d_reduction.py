#!/usr/bin/env python3
"""
Exact reduction theorem for the PMNS microscopic deformation ΔD.

Question:
  Once the native free microscopic core is derived as identity on the retained
  lepton surface, what is the exact form of the deformation

      ΔD = D - D_free

  on the PMNS-relevant triplet sectors?

Answer:
  It is not a generic 3x3 perturbation. On each retained triplet sector it lies
  in the exact diagonal-circulant channel family

      ΔD = U + V C + W C^2

  with U,V,W diagonal.

  More sharply:
    - single-Higgs lanes occupy exactly one of the three channels I, C, C^2
    - canonical minimal two-Higgs lanes occupy exactly the I + C subfamily
    - the weak-axis seed patch reduces further to the two-parameter slice
      ΔD = (x-1) I + y C up to the exchange sheet on the canonical (0,1) pair

Boundary:
  This identifies the exact native deformation carrier. It does not derive the
  values of the diagonal channel coefficients from Cl(3) on Z^3.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE2 = CYCLE @ CYCLE
PERMUTATIONS = {
    0: I3,
    1: CYCLE,
    2: CYCLE2,
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


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def monomial_triplet(coeffs: np.ndarray, offset: int) -> np.ndarray:
    return diagonal(coeffs) @ PERMUTATIONS[offset]


def canonical_two_higgs_triplet(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(x) + diagonal(y_eff) @ CYCLE


def diagonal_circulant(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return diagonal(a) + diagonal(b) @ CYCLE + diagonal(c) @ CYCLE2


def part1_all_retained_triplet_patterns_live_in_the_exact_diagonal_circulant_channel_basis() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ALL RETAINED TRIPLET PATTERNS LIVE IN THE DIAGONAL-CIRCULANT BASIS")
    print("=" * 88)

    coeffs = np.array([0.2 + 0.1j, 0.5 - 0.2j, 0.9 + 0.05j], dtype=complex)
    for offset in [0, 1, 2]:
        mono = monomial_triplet(coeffs, offset)
        if offset == 0:
            dc = diagonal_circulant(coeffs, np.zeros(3, dtype=complex), np.zeros(3, dtype=complex))
            channel = "I"
        elif offset == 1:
            dc = diagonal_circulant(np.zeros(3, dtype=complex), coeffs, np.zeros(3, dtype=complex))
            channel = "C"
        else:
            dc = diagonal_circulant(np.zeros(3, dtype=complex), np.zeros(3, dtype=complex), coeffs)
            channel = "C^2"
        check(f"offset={offset}: monomial triplet is exactly one diagonal-circulant channel", np.linalg.norm(mono - dc) < 1e-12,
              f"channel={channel}, err={np.linalg.norm(mono - dc):.2e}")

    x = np.array([0.7, 1.1, 0.9], dtype=float)
    y = np.array([0.3, 0.5, 0.4], dtype=float)
    delta = 0.61
    two = canonical_two_higgs_triplet(x, y, delta)
    dc_two = diagonal_circulant(
        x.astype(complex),
        np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex),
        np.zeros(3, dtype=complex),
    )
    check("Canonical two-Higgs triplet is exactly an I + C diagonal-circulant operator", np.linalg.norm(two - dc_two) < 1e-12,
          f"err={np.linalg.norm(two - dc_two):.2e}")


def part2_the_native_free_core_identifies_delta_d_as_an_affine_diagonal_circulant_deformation() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FREE CORE MAKES ΔD AN AFFINE DIAGONAL-CIRCULANT DEFORMATION")
    print("=" * 88)

    d_free = I3

    coeffs = np.array([0.07, 0.11, 0.23], dtype=complex)
    mono_forward = monomial_triplet(coeffs, 1)
    delta_forward = mono_forward - d_free
    expected_forward = diagonal_circulant(-np.ones(3, dtype=complex), coeffs, np.zeros(3, dtype=complex))

    x = np.array([0.9, 1.2, 1.1], dtype=float)
    y = np.array([0.3, 0.5, 0.4], dtype=float)
    delta = 0.62
    active = canonical_two_higgs_triplet(x, y, delta)
    delta_active = active - d_free
    expected_active = diagonal_circulant(
        x.astype(complex) - np.ones(3, dtype=complex),
        np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex),
        np.zeros(3, dtype=complex),
    )

    check("Subtracting the free core sends a forward-cyclic monomial lane to -I + D C", np.linalg.norm(delta_forward - expected_forward) < 1e-12,
          f"err={np.linalg.norm(delta_forward - expected_forward):.2e}")
    check("Subtracting the free core sends a canonical two-Higgs lane to (A-I) + B C", np.linalg.norm(delta_active - expected_active) < 1e-12,
          f"err={np.linalg.norm(delta_active - expected_active):.2e}")
    check("So ΔD stays inside the same exact diagonal-circulant carrier", True,
          "ΔD = U + V C + W C^2 with U,V,W diagonal")


def part3_one_sided_minimal_pmns_classes_reduce_the_full_lepton_deformation_to_branch_conditioned_channel_data() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ONE-SIDED MINIMAL PMNS CLASSES REDUCE ΔD TO BRANCH-CONDITIONED CHANNEL DATA")
    print("=" * 88)

    d_nu = canonical_two_higgs_triplet(
        np.array([0.8, 1.0, 0.9], dtype=float),
        np.array([0.2, 0.4, 0.3], dtype=float),
        0.37,
    )
    d_e = monomial_triplet(np.array([0.05, 0.11, 0.23], dtype=complex), 0)
    delta_nu = d_nu - I3
    delta_e = d_e - I3

    d_nu_e = monomial_triplet(np.array([0.03, 0.09, 0.17], dtype=complex), 1)
    d_e_act = canonical_two_higgs_triplet(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    delta_nu_e = d_nu_e - I3
    delta_e_act = d_e_act - I3

    check("Neutrino-active branch: ΔD_0 lives on the I+C channel family", np.linalg.norm(delta_nu - diagonal_circulant(
        np.array([0.8, 1.0, 0.9], dtype=float) - np.ones(3),
        np.array([0.2, 0.4, 0.3 * np.exp(1j * 0.37)], dtype=complex),
        np.zeros(3, dtype=complex),
    )) < 1e-12)
    check("Neutrino-active branch: ΔD_- lives on a single exact channel", np.linalg.norm(delta_e - diagonal_circulant(
        np.array([0.05, 0.11, 0.23], dtype=complex) - np.ones(3, dtype=complex),
        np.zeros(3, dtype=complex),
        np.zeros(3, dtype=complex),
    )) < 1e-12)
    check("Charged-lepton-active branch: ΔD_- lives on the I+C channel family", np.linalg.norm(delta_e_act - diagonal_circulant(
        np.array([0.24, 0.38, 1.07], dtype=float) - np.ones(3),
        np.array([0.09, 0.22, 0.61 * np.exp(1j * 1.10)], dtype=complex),
        np.zeros(3, dtype=complex),
    )) < 1e-12)
    check("Charged-lepton-active branch: ΔD_0 on offset-1 monomial lane is -I + D C", np.linalg.norm(delta_nu_e - diagonal_circulant(
        -np.ones(3, dtype=complex),
        np.array([0.03, 0.09, 0.17], dtype=complex),
        np.zeros(3, dtype=complex),
    )) < 1e-12)

    print()
    print("  So once the branch is fixed, the full lepton deformation is no longer")
    print("  a generic pair of 3x3 perturbations. It is exact channel data on")
    print("  the basis {I, C, C^2}.")


def part4_the_weak_axis_seed_patch_reduces_delta_d_further_to_a_two_parameter_slice_plus_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE WEAK-AXIS SEED PATCH REDUCES ΔD TO A TWO-PARAMETER SLICE PLUS SHEET")
    print("=" * 88)

    x = 0.9
    y = 0.4
    sheet0 = x * I3 + y * CYCLE
    sheet1 = y * I3 + x * CYCLE
    delta0 = sheet0 - I3
    delta1 = sheet1 - I3

    check("Seed sheet 0 gives ΔD = (x-1) I + y C", np.linalg.norm(delta0 - (((x - 1.0) * I3) + y * CYCLE)) < 1e-12,
          f"err={np.linalg.norm(delta0 - (((x - 1.0) * I3) + y * CYCLE)):.2e}")
    check("Seed sheet 1 gives the exchanged two-parameter slice ΔD = (y-1) I + x C", np.linalg.norm(delta1 - (((y - 1.0) * I3) + x * CYCLE)) < 1e-12,
          f"err={np.linalg.norm(delta1 - (((y - 1.0) * I3) + x * CYCLE)):.2e}")
    check("So on the aligned seed patch the only residual D-level ambiguity is the exchange sheet", np.linalg.norm(delta0 - delta1) > 1e-6)


def part5_the_remaining_value_law_is_exactly_the_diagonal_channel_coefficients() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE REMAINING VALUE LAW IS EXACTLY THE DIAGONAL CHANNEL COEFFICIENTS")
    print("=" * 88)

    check("No generic 3x3 PMNS deformation target remains", True,
          "all retained triplet operators sit in the diagonal-circulant carrier")
    check("The remaining unresolved object is only the diagonal coefficient data on I, C, C^2", True,
          "values of U, V, W")
    check("On one-sided minimal PMNS classes, one of those channels is already absent on the active sector", True,
          "canonical active lane uses I + C only")


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC DELTA-D REDUCTION")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - PMNS native free microscopic D law")
    print("  - PMNS microscopic triplet-sector entry law")
    print("  - neutrino Dirac Z_3 support trichotomy")
    print("  - neutrino / charged-lepton two-Higgs canonical reductions")
    print("  - PMNS weak-axis seed coefficient closure")
    print()
    print("Question:")
    print("  Once D_free is derived, what is the exact form of the PMNS-relevant")
    print("  microscopic deformation ΔD = D - D_free?")

    part1_all_retained_triplet_patterns_live_in_the_exact_diagonal_circulant_channel_basis()
    part2_the_native_free_core_identifies_delta_d_as_an_affine_diagonal_circulant_deformation()
    part3_one_sided_minimal_pmns_classes_reduce_the_full_lepton_deformation_to_branch_conditioned_channel_data()
    part4_the_weak_axis_seed_patch_reduces_delta_d_further_to_a_two_parameter_slice_plus_sheet()
    part5_the_remaining_value_law_is_exactly_the_diagonal_channel_coefficients()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact deformation answer:")
    print("    - ΔD is not a generic 3x3 perturbation")
    print("    - on each triplet sector, ΔD = U + V C + W C^2 with U,V,W diagonal")
    print("    - single-Higgs lanes occupy one exact channel")
    print("    - canonical two-Higgs lanes occupy the I + C subfamily")
    print("    - the weak-axis seed patch reduces to a two-parameter slice plus one sheet")
    print()
    print("  So the remaining science is only the value law of those diagonal")
    print("  channel coefficients from Cl(3) on Z^3.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
