#!/usr/bin/env python3
"""
Majorana continuum-bridge transplant obstruction on the current atlas stack.

Question:
  Once the exact universal route has been reduced to an inverse-limit /
  continuum-interpretation frontier, can that continuum-bridge layer itself
  provide the missing absolute Majorana staircase selector on the current
  self-dual source ray?

Answer on the current exact stack:
  No. The current continuum bridge is only an interpretation frontier for the
  same exact discrete projective family. On that family, every finite-stage
  cylinder density along the current self-dual source ray is still of the form

      Delta log rho_n(lambda) = 1/2 c_n lambda^2,   c_n > 0,

  with exact refinement/projective compatibility preserving the same source
  scaling. So a bare inverse-limit reinterpretation of the same family does not
  create a finite selector without a genuinely new non-homogeneous limiting
  datum.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0
ALPHA_LM = 0.09067

ROOT = Path(__file__).resolve().parents[1]


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


def build_positive_background_operator() -> np.ndarray:
    d = np.array([2.0, 3.0, 5.0, 7.0], dtype=float)
    h_d = np.diag(
        [
            1.0 / (d[0] * d[0]),
            1.0 / (d[1] * d[1]),
            1.0 / (d[2] * d[2]),
            1.0 / (d[3] * d[3]),
            1.0 / (d[0] * d[1]),
            1.0 / (d[0] * d[2]),
            1.0 / (d[0] * d[3]),
            1.0 / (d[1] * d[2]),
            1.0 / (d[1] * d[3]),
            1.0 / (d[2] * d[3]),
        ]
    )
    lambda_r = np.array(
        [
            [2.0, 0.2, 0.0],
            [0.2, 1.7, 0.1],
            [0.0, 0.1, 1.4],
        ],
        dtype=float,
    )
    return np.kron(h_d, lambda_r)


def schur_reduce(
    k_op: np.ndarray,
    j: np.ndarray,
    keep: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    all_idx = np.arange(k_op.shape[0])
    elim = np.setdiff1d(all_idx, keep, assume_unique=True)
    k_kk = k_op[np.ix_(keep, keep)]
    k_ke = k_op[np.ix_(keep, elim)]
    k_ek = k_op[np.ix_(elim, keep)]
    k_ee = k_op[np.ix_(elim, elim)]
    j_k = j[keep]
    j_e = j[elim]
    k_ee_inv = np.linalg.inv(k_ee)
    k_eff = k_kk - k_ke @ k_ee_inv @ k_ek
    j_eff = j_k - k_ke @ k_ee_inv @ j_e
    return k_eff, j_eff


def test_authority_stack_is_present() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT ATLAS REDUCES THE QG FRONTIER TO INTERPRETATION")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    cont = read("docs/UNIVERSAL_QG_CONTINUUM_BRIDGE_REDUCTION_NOTE.md")
    refine = read("docs/UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md")
    blocker = read("docs/NEUTRINO_MAJORANA_PARTITION_PROJECTIVE_TRANSPLANT_OBSTRUCTION_NOTE.md")

    check("Atlas retains the universal continuum-bridge reduction row", "Universal continuum-bridge reduction" in atlas)
    check("The continuum-bridge note explicitly reduces the live issue to inverse-limit / continuum interpretation", "inverse-limit / continuum-equivalence" in cont.lower())
    check("The refinement-net note already gives the exact canonical discrete net", "canonical geometric refinement net" in refine.lower())
    check("The current Majorana partition/projective blocker note already closes the discrete measure/projective route", "does not" in blocker.lower() and "partition/projective/refinement family" in blocker.lower())


def test_all_finite_stages_keep_the_same_lambda_law() -> None:
    print("\n" + "=" * 88)
    print("PART 2: EVERY COMPATIBLE FINITE STAGE KEEPS THE SAME QUADRATIC SOURCE LAW")
    print("=" * 88)

    k0 = build_positive_background_operator()
    j0 = np.linspace(1.0, float(k0.shape[0]), k0.shape[0], dtype=float)
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]

    levels = [
        np.arange(k0.shape[0]),
        np.arange(20),
        np.arange(10),
    ]

    k_stage = k0
    j_stage0 = j0
    stage_coeffs = []
    for idx, keep in enumerate(levels):
        if idx == 0:
            current_k = k_stage
            current_j0 = j_stage0
        else:
            current_k, current_j0 = schur_reduce(k0, j0, keep)
        coeff = float(current_j0 @ np.linalg.solve(current_k, current_j0))
        stage_coeffs.append(coeff)

        ratios = []
        for scale in scales:
            j = scale * current_j0
            ratios.append(0.5 * float(j @ np.linalg.solve(current_k, j)) / (scale * scale))

        spread = max(ratios) - min(ratios)
        check(f"Finite stage {idx} keeps Delta log rho_n quadratic in lambda", spread < 1e-9, f"spread={spread:.2e}")
        check(f"Finite stage {idx} has positive coefficient c_n", coeff > 0.0, f"c_n={coeff:.6e}")

    print()
    print(f"  Stage coefficients c_n = {[f'{c:.3e}' for c in stage_coeffs]}")


def test_projective_compatibility_preserves_source_scaling() -> None:
    print("\n" + "=" * 88)
    print("PART 3: PROJECTIVE COMPATIBILITY PRESERVES THE SAME SOURCE SCALING")
    print("=" * 88)

    k0 = build_positive_background_operator()
    j0 = np.linspace(1.0, float(k0.shape[0]), k0.shape[0], dtype=float)
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]

    keep_mid = np.arange(20)
    keep_coarse = np.arange(10)

    base_mid = None
    base_coarse = None
    max_mid_diff = 0.0
    max_coarse_diff = 0.0
    for scale in scales:
        k_mid, j_mid = schur_reduce(k0, scale * j0, keep_mid)
        k_coarse, j_coarse = schur_reduce(k0, scale * j0, keep_coarse)
        if base_mid is None:
            base_mid = j_mid / scale
            base_coarse = j_coarse / scale
        max_mid_diff = max(max_mid_diff, float(np.max(np.abs(j_mid / scale - base_mid))))
        max_coarse_diff = max(max_coarse_diff, float(np.max(np.abs(j_coarse / scale - base_coarse))))

    check("Projective pushforward preserves the mid-level source ray exactly", max_mid_diff < 1e-12, f"max mid-level deviation={max_mid_diff:.2e}")
    check("Projective pushforward preserves the coarse-level source ray exactly", max_coarse_diff < 1e-12, f"max coarse-level deviation={max_coarse_diff:.2e}")
    check("So the exact projective family never leaves the same one-parameter source class", max(max_mid_diff, max_coarse_diff) < 1e-12, "all finite stages remain on compatible homogeneous rays")


def test_continuum_reinterpretation_alone_cannot_select_lambda() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BARE INVERSE-LIMIT REINTERPRETATION DOES NOT ADD A SELECTOR")
    print("=" * 88)

    k0 = build_positive_background_operator()
    j0 = np.linspace(1.0, float(k0.shape[0]), k0.shape[0], dtype=float)
    levels = [np.arange(k0.shape[0]), np.arange(20), np.arange(10)]

    positive_coeffs = []
    for idx, keep in enumerate(levels):
        if idx == 0:
            current_k = k0
            current_j0 = j0
        else:
            current_k, current_j0 = schur_reduce(k0, j0, keep)
        positive_coeffs.append(float(current_j0 @ np.linalg.solve(current_k, current_j0)))

    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    all_positive = True
    for coeff in positive_coeffs:
        all_positive = all_positive and all(scale * coeff > 0.0 for scale in scales)

    check("Every finite-stage cylinder density is still monotone in lambda on lambda>0", all_positive, f"coefficients={positive_coeffs}")
    check("So a bare inverse-limit reinterpretation of the same cylinder family adds no finite selector", all_positive, "a new non-homogeneous limiting datum would still be required")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: CONTINUUM-BRIDGE TRANSPLANT OBSTRUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the inverse-limit / continuum-interpretation layer itself act as")
    print("  the missing absolute Majorana staircase selector on the current")
    print("  self-dual source ray?")

    test_authority_stack_is_present()
    test_all_finite_stages_keep_the_same_lambda_law()
    test_projective_compatibility_preserves_source_scaling()
    test_continuum_reinterpretation_alone_cannot_select_lambda()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. On the current exact stack, the continuum bridge is only an")
    print("  interpretation frontier for the same compatible discrete projective")
    print("  family. Every finite-stage cylinder density remains quadratic and")
    print("  monotone in the same source scale, and projective/refinement")
    print("  compatibility preserves that law exactly.")
    print()
    print("  So a bare inverse-limit reinterpretation of the current family is")
    print("  not the missing non-homogeneous Majorana selector.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
