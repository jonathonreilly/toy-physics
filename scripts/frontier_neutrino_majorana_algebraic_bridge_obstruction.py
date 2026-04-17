#!/usr/bin/env python3
"""
Majorana algebraic bridge obstruction theorem on the current exact stack.

Question:
  After the local self-dual Majorana point rho = 1 is fixed, could an obvious
  finite algebraic/spectral bridge from the selected local ray to the current
  generation texture class select the absolute staircase anchor?

Answer on the current exact stack:
  No. Once the selected local family and the current generation texture are
  both homogeneous in the same positive scale lambda, every finite algebraic
  bridge built from those ingredients stays homogeneous: Schur complements,
  eigenvalue gaps, singular values, and characteristic-polynomial coefficients
  all carry definite scaling weight, while normalized ratios are scale-free.

Boundary:
  This excludes the obvious algebraic/spectral bridge class on the current
  stack. It does NOT rule out a genuinely new non-homogeneous bridge or a new
  absolute-scale datum beyond that class.
"""

from __future__ import annotations

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


def lifted_bridge_block(scale: float) -> np.ndarray:
    k_sd = scale * local_selected_kernel()
    m_gen = scale * generation_texture()
    c = scale * bridge_tensor()
    top = np.hstack([k_sd, c])
    bottom = np.hstack([c.conj().T, m_gen])
    return np.vstack([top, bottom])


def schur_generation_block(scale: float) -> np.ndarray:
    k_sd = scale * local_selected_kernel()
    m_gen = scale * generation_texture()
    c = scale * bridge_tensor()
    return m_gen - c.conj().T @ np.linalg.inv(k_sd) @ c


def test_full_bridge_block_is_homogeneous() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE FULL LOCAL-TO-GENERATION BRIDGE BLOCK IS HOMOGENEOUS")
    print("=" * 88)

    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    blocks = [lifted_bridge_block(scale) for scale in scales]
    normalized = [normalize(block) for block in blocks]

    max_diff = 0.0
    for idx in range(len(normalized) - 1):
        max_diff = max(max_diff, np.linalg.norm(normalized[idx] - normalized[idx + 1]))

    check("Normalized full bridge blocks are identical across staircase rescalings", max_diff < 1e-12,
          f"max normalized difference={max_diff:.2e}")

    print()
    print("  So any bridge block built from the selected local ray, the current")
    print("  generation texture, and scale-independent structural couplings still")
    print("  collapses to one matrix ray under the current common scaling.")


def test_schur_bridge_remains_degree_one() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SCHUR-COMPLEMENT BRIDGES REMAIN DEGREE-ONE IN THE SAME SCALE")
    print("=" * 88)

    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    schurs = [schur_generation_block(scale) for scale in scales]
    normalized = [normalize(s) for s in schurs]
    ratios = [np.linalg.norm(s) / scale for s, scale in zip(schurs, scales)]

    max_diff = 0.0
    for idx in range(len(normalized) - 1):
        max_diff = max(max_diff, np.linalg.norm(normalized[idx] - normalized[idx + 1]))
    ratio_spread = max(ratios) - min(ratios)

    check("Normalized Schur-complement bridge blocks are identical across staircase rescalings", max_diff < 1e-12,
          f"max normalized difference={max_diff:.2e}")
    check("Schur-complement bridge norms scale linearly with the same free parameter", ratio_spread < 1e-12,
          f"spread in ||S||/scale={ratio_spread:.2e}")

    print()
    print("  So even when the obvious local-to-generation bridge is dressed by a")
    print("  Schur complement, it still carries the same overall scale weight.")


def test_spectral_bridge_data_stay_homogeneous_or_invariant() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE OBVIOUS SPECTRAL BRIDGE DATA ARE HOMOGENEOUS OR SCALE-FREE")
    print("=" * 88)

    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    coeff_ratios = []
    gap_ratios = []
    sv_ratios = []
    normalized_eigs = []

    for scale in scales:
        block = lifted_bridge_block(scale)
        coeffs = np.poly(block)
        eigs = np.sort_complex(np.linalg.eigvals(block))
        svals = np.sort(np.linalg.svd(block, compute_uv=False))
        gaps = np.diff(np.real_if_close(eigs))

        coeff_ratios.append(np.array([coeffs[1] / scale, coeffs[2] / scale**2, coeffs[3] / scale**3]))
        gap_ratios.append(np.array(gaps, dtype=float) / scale)
        sv_ratios.append(np.array(svals, dtype=float) / scale)
        normalized_eigs.append(eigs / np.linalg.norm(eigs))

    coeff_spread = max(np.linalg.norm(coeff_ratios[i] - coeff_ratios[0]) for i in range(1, len(coeff_ratios)))
    gap_spread = max(np.linalg.norm(gap_ratios[i] - gap_ratios[0]) for i in range(1, len(gap_ratios)))
    sv_spread = max(np.linalg.norm(sv_ratios[i] - sv_ratios[0]) for i in range(1, len(sv_ratios)))
    eig_spread = max(np.linalg.norm(normalized_eigs[i] - normalized_eigs[0]) for i in range(1, len(normalized_eigs)))

    check("Characteristic-polynomial coefficients carry fixed homogeneous degrees", coeff_spread < 1e-10,
          f"spread={coeff_spread:.2e}")
    check("Eigenvalue gaps scale linearly with the same free parameter", gap_spread < 1e-10,
          f"spread={gap_spread:.2e}")
    check("Singular values scale linearly with the same free parameter", sv_spread < 1e-10,
          f"spread={sv_spread:.2e}")
    check("Normalized eigenvalue ratios are scale-invariant", eig_spread < 1e-10,
          f"spread={eig_spread:.2e}")

    print()
    print("  So the obvious spectral candidates split into two classes only:")
    print("  homogeneous scale carriers and scale-free normalized ratios. Neither")
    print("  class can pick a finite absolute staircase anchor by itself.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: ALGEBRAIC BRIDGE OBSTRUCTION")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/NEUTRINO_MAJORANA_AXIS_EXCHANGE_FIXED_POINT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md")
    print()
    print("Question:")
    print("  Could an obvious finite algebraic/spectral bridge from the selected")
    print("  local Majorana ray to the current generation texture select the")
    print("  absolute staircase anchor?")

    test_full_bridge_block_is_homogeneous()
    test_schur_bridge_remains_degree_one()
    test_spectral_bridge_data_stay_homogeneous_or_invariant()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. On the present exact stack, the obvious algebraic/spectral")
    print("  local-to-generation bridge class remains homogeneous in the same")
    print("  positive scale or collapses to scale-free normalized ratios.")
    print()
    print("  So the live missing object is sharper again: it must go beyond the")
    print("  current algebraic/spectral bridge class, or introduce a genuinely")
    print("  new absolute-scale datum.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
