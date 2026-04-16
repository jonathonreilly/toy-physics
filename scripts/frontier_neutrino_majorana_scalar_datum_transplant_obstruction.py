#!/usr/bin/env python3
"""
Majorana scalar-datum transplant obstruction on the current exact stack.

Question:
  Could one of the exact scalar atlas datums already derived on main
  (for example the hierarchy selector or endpoint constants) serve as the
  missing absolute-scale datum for the selected local Majorana lane?

Answer on the current exact stack:
  No. Any current exact scalar datum transplanted multiplicatively into the
  selected local-to-generation Majorana bridge only changes fixed dimensionless
  coefficients inside the block. The common positive staircase scale lambda
  still factors out exactly, so Schur complements and spectral bridge data
  remain homogeneous or scale-free.

Boundary:
  This rules out the current exact scalar-atlas data as the missing absolute
  Majorana staircase datum. It does NOT rule out a future non-homogeneous
  datum or bridge beyond that current scalar class.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
ALPHA_LM = 0.09067


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


def normalize(matrix: np.ndarray) -> np.ndarray:
    return matrix / np.linalg.norm(matrix)


def local_selected_kernel() -> np.ndarray:
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    return sigma_z + sigma_x


def generation_texture() -> np.ndarray:
    return np.array(
        [[2.0, 0.0, 0.0], [0.0, 0.25, 1.0], [0.0, 1.0, 0.25]],
        dtype=complex,
    )


def bridge_tensor() -> np.ndarray:
    return np.array(
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.5]],
        dtype=complex,
    )


def exact_scalar_datums() -> dict[str, float]:
    return {
        "selector_C4": (7.0 / 8.0) ** 0.25,
        "endpoint_Cinf4D": (3.0 / 4.0) ** 0.125,
        "A4_over_A2": 8.0 / 7.0,
        "Ainf_over_A2": 2.0 / math.sqrt(3.0),
    }


def lifted_bridge_block(scale: float, c_local: float, c_bridge: float, c_gen: float) -> np.ndarray:
    k_sd = scale * c_local * local_selected_kernel()
    m_gen = scale * c_gen * generation_texture()
    c = scale * c_bridge * bridge_tensor()
    top = np.hstack([k_sd, c])
    bottom = np.hstack([c.conj().T, m_gen])
    return np.vstack([top, bottom])


def schur_generation_block(scale: float, c_local: float, c_bridge: float, c_gen: float) -> np.ndarray:
    k_sd = scale * c_local * local_selected_kernel()
    m_gen = scale * c_gen * generation_texture()
    c = scale * c_bridge * bridge_tensor()
    return m_gen - c.conj().T @ np.linalg.inv(k_sd) @ c


def test_scalar_datums_are_fixed_positive_numbers() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CURRENT EXACT SCALAR ATLAS DATUMS ARE FIXED DIMENSIONLESS NUMBERS")
    print("=" * 88)

    datums = exact_scalar_datums()
    all_positive = all(value > 0.0 for value in datums.values())
    all_nontrivial = all(abs(value - 1.0) > 1e-6 for value in datums.values())

    check("Current hierarchy-side scalar datums are strictly positive", all_positive,
          f"values={datums}")
    check("The tested scalar datums are nontrivial fixed constants", all_nontrivial,
          f"values={datums}")

    print()
    print("  So the candidate imported atlas constants are real fixed numbers, not")
    print("  new scale variables on the Majorana lane.")


def test_transplanted_scalar_datums_preserve_global_scale_factorization() -> None:
    print("\n" + "=" * 88)
    print("PART 2: TRANSPLANTED SCALAR DATUMS STILL LEAVE THE GLOBAL SCALE FACTORIZED")
    print("=" * 88)

    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    datums = exact_scalar_datums()
    patterns = {
        "local-only": lambda c: (c, 1.0, 1.0),
        "bridge-only": lambda c: (1.0, c, 1.0),
        "generation-only": lambda c: (1.0, 1.0, c),
        "uniform": lambda c: (c, c, c),
    }

    worst_diff = 0.0
    for datum in datums.values():
        for choose_pattern in patterns.values():
            c_local, c_bridge, c_gen = choose_pattern(datum)
            blocks = [lifted_bridge_block(scale, c_local, c_bridge, c_gen) for scale in scales]
            normalized = [normalize(block) for block in blocks]
            for idx in range(len(normalized) - 1):
                worst_diff = max(worst_diff, np.linalg.norm(normalized[idx] - normalized[idx + 1]))

    check("Every tested scalar-datum transplant keeps the full bridge block on one normalized ray",
          worst_diff < 1e-12, f"max normalized difference={worst_diff:.2e}")

    print()
    print("  So a fixed scalar datum can change the shape constants inside the")
    print("  lifted block, but it still leaves the common staircase scale as one")
    print("  exact overall factor.")


def test_schur_and_spectral_data_stay_homogeneous() -> None:
    print("\n" + "=" * 88)
    print("PART 3: SCHUR AND SPECTRAL BRIDGE DATA STILL CARRY THE SAME SCALE WEIGHT")
    print("=" * 88)

    c_local = exact_scalar_datums()["selector_C4"]
    c_bridge = exact_scalar_datums()["endpoint_Cinf4D"]
    c_gen = exact_scalar_datums()["Ainf_over_A2"]
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]

    schurs = [schur_generation_block(scale, c_local, c_bridge, c_gen) for scale in scales]
    normalized_schurs = [normalize(s) for s in schurs]
    schur_ratios = [np.linalg.norm(s) / scale for s, scale in zip(schurs, scales)]

    blocks = [lifted_bridge_block(scale, c_local, c_bridge, c_gen) for scale in scales]
    eig_gap_ratios = []
    sv_ratios = []
    for scale, block in zip(scales, blocks):
        eigs = np.sort_complex(np.linalg.eigvals(block))
        gaps = np.diff(np.real_if_close(eigs))
        svals = np.sort(np.linalg.svd(block, compute_uv=False))
        eig_gap_ratios.append(np.array(gaps, dtype=float) / scale)
        sv_ratios.append(np.array(svals, dtype=float) / scale)

    schur_diff = max(
        np.linalg.norm(normalized_schurs[idx] - normalized_schurs[idx + 1])
        for idx in range(len(normalized_schurs) - 1)
    )
    schur_spread = max(schur_ratios) - min(schur_ratios)
    gap_spread = max(np.linalg.norm(eig_gap_ratios[i] - eig_gap_ratios[0]) for i in range(1, len(eig_gap_ratios)))
    sv_spread = max(np.linalg.norm(sv_ratios[i] - sv_ratios[0]) for i in range(1, len(sv_ratios)))

    check("Schur complements remain degree-one in the same staircase scale", schur_diff < 1e-12 and schur_spread < 1e-12,
          f"normalized diff={schur_diff:.2e}, spread in ||S||/scale={schur_spread:.2e}")
    check("Eigenvalue gaps remain degree-one after scalar-datum transplant", gap_spread < 1e-10,
          f"spread={gap_spread:.2e}")
    check("Singular values remain degree-one after scalar-datum transplant", sv_spread < 1e-10,
          f"spread={sv_spread:.2e}")

    print()
    print("  So the existing exact scalar atlas datums do not create the missing")
    print("  non-homogeneous scale law. They only change fixed coefficients inside")
    print("  the same homogeneous bridge class.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: SCALAR-DATUM TRANSPLANT OBSTRUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md")
    print("  - docs/HIERARCHY_EFFECTIVE_POTENTIAL_ENDPOINT_NOTE.md")
    print("  - docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_ALGEBRAIC_BRIDGE_OBSTRUCTION_NOTE.md")
    print()
    print("Question:")
    print("  Could one of the exact scalar atlas datums already derived on main")
    print("  serve as the missing absolute-scale datum for the selected local")
    print("  Majorana lane?")

    test_scalar_datums_are_fixed_positive_numbers()
    test_transplanted_scalar_datums_preserve_global_scale_factorization()
    test_schur_and_spectral_data_stay_homogeneous()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. On the current exact stack, transplanting the existing scalar")
    print("  atlas datums into the selected Majorana local-to-generation block")
    print("  only changes fixed dimensionless coefficients. The common positive")
    print("  staircase scale still factors out exactly.")
    print()
    print("  So the missing object is sharper again: it is not one of the current")
    print("  exact scalar atlas datums reused multiplicatively. It must be a")
    print("  genuinely new non-homogeneous bridge or a genuinely new absolute-scale")
    print("  datum beyond that current scalar class.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
