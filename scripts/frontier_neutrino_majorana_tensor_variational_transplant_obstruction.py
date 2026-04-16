#!/usr/bin/env python3
"""
Majorana tensor-variational transplant obstruction on the current atlas stack.

Question:
  Can the exact direct-universal tensor variational / positive-background local
  closure family supply the missing absolute Majorana staircase anchor once the
  local Majorana lane has already selected the self-dual source ray?

Answer on the current exact stack:
  No. If the current Majorana local-to-generation data still enter that family
  only through a homogeneous source ray J_lambda = lambda J_0, then the exact
  stationary solution and stationary action stay homogeneous:

      F_*(lambda) = lambda K(D)^-1 J_0
      I_*(lambda) = -1/2 lambda^2 <J_0, K(D)^-1 J_0>.

  Normalized profiles are identical across lambda and the stationary value has
  no finite intrinsic selector on lambda > 0. So the universal tensor/local-
  closure family is not, by itself, the missing non-homogeneous bridge.
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


def stationary_family(
    k_op: np.ndarray,
    j0: np.ndarray,
    scales: list[float],
) -> tuple[list[np.ndarray], list[float]]:
    k_inv = np.linalg.inv(k_op)
    fields = []
    values = []
    for scale in scales:
        j = scale * j0
        fields.append(np.linalg.solve(k_op, j))
        values.append(-0.5 * float(j @ (k_inv @ j)))
    return fields, values


def normalize(vec: np.ndarray) -> np.ndarray:
    return vec / np.linalg.norm(vec)


def test_authority_stack_is_present() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ATLAS ALREADY CONTAINS THE TENSOR / LOCAL-CLOSURE FAMILY")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    cand = read("docs/UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md")
    local = read("docs/UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md")
    blocker = read("docs/NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md")

    has_tensor_row = "Universal tensor variational candidate" in atlas
    has_local_row = "Universal positive-background local closure" in atlas
    cand_has_hessian = "metric-source hessian" in cand.lower()
    local_has_stationary = "unique exact stationary boundary field" in local.lower()
    blocker_has_self_dual = (
        "selected local self-dual family is one positive ray" in blocker.lower()
        or "selected local family is the positive ray" in blocker.lower()
        or ("positive ray" in blocker.lower() and "projective" in blocker.lower())
    )

    check("Atlas retains the universal tensor-variational row", has_tensor_row)
    check("Atlas retains the universal positive-background local-closure row", has_local_row)
    check("The tensor-variational note defines the metric-source Hessian candidate", cand_has_hessian)
    check("The local-closure note gives a unique stationary solution family", local_has_stationary)
    check("The current Majorana blocker note already fixes the self-dual source family to one positive ray", blocker_has_self_dual)


def test_transplanted_stationary_family_stays_homogeneous() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE TRANSPLANTED TENSOR STATIONARY FAMILY STAYS HOMOGENEOUS")
    print("=" * 88)

    k_op = build_positive_background_operator()
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    j0 = np.linspace(1.0, float(k_op.shape[0]), k_op.shape[0], dtype=float)
    fields, values = stationary_family(k_op, j0, scales)

    max_profile_diff = 0.0
    value_ratios = []
    field_ratios = []

    base_profile = normalize(fields[0])
    for scale, field, value in zip(scales, fields, values):
        max_profile_diff = max(max_profile_diff, float(np.linalg.norm(normalize(field) - base_profile)))
        value_ratios.append(value / (scale * scale))
        field_ratios.append(float(np.linalg.norm(field) / scale))

    max_value_ratio_spread = max(value_ratios) - min(value_ratios)
    max_field_ratio_spread = max(field_ratios) - min(field_ratios)

    check(
        "Normalized stationary tensor profiles are identical across Majorana staircase rescalings",
        max_profile_diff < 1e-12,
        f"max normalized profile difference={max_profile_diff:.2e}",
    )
    check(
        "The stationary action scales exactly as lambda^2 on that family",
        max_value_ratio_spread < 1e-9,
        f"spread in I_*/lambda^2={max_value_ratio_spread:.2e}",
    )
    check(
        "The stationary field norm scales exactly as lambda on that family",
        max_field_ratio_spread < 1e-9,
        f"spread in ||F_*||/lambda={max_field_ratio_spread:.2e}",
    )


def test_no_finite_selector_emerges_from_stationary_value() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE STATIONARY TENSOR ACTION STILL HAS NO FINITE SCALE SELECTOR")
    print("=" * 88)

    k_op = build_positive_background_operator()
    k_inv = np.linalg.inv(k_op)
    j0 = np.linspace(1.0, float(k_op.shape[0]), k_op.shape[0], dtype=float)
    coeff = float(j0 @ (k_inv @ j0))
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    derivatives = [-scale * coeff for scale in scales]

    check(
        "The exact stationary action coefficient is positive",
        coeff > 0.0,
        f"<J_0,K^-1 J_0>={coeff:.6e}",
    )
    check(
        "d I_*(lambda) / d lambda = -lambda <J_0,K^-1 J_0> stays strictly negative on lambda > 0",
        all(derivative < 0.0 for derivative in derivatives),
        f"derivatives={derivatives}",
    )
    check(
        "So the tensor/local-closure family has no intrinsic finite positive stationary selector",
        coeff > 0.0 and all(derivative < 0.0 for derivative in derivatives),
        "only the trivial lambda=0 boundary is stationary on the homogeneous ray",
    )


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: TENSOR-VARIATIONAL TRANSPLANT OBSTRUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the exact direct-universal tensor-variational / positive-")
    print("  background local-closure family act as the missing absolute")
    print("  Majorana staircase selector on the current self-dual source ray?")

    test_authority_stack_is_present()
    test_transplanted_stationary_family_stays_homogeneous()
    test_no_finite_selector_emerges_from_stationary_value()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. The direct-universal tensor/local-closure family remains")
    print("  homogeneous when fed by the current self-dual Majorana source ray:")
    print("  the stationary field scales linearly, the stationary action scales")
    print("  quadratically, normalized profiles are unchanged, and no finite")
    print("  positive staircase selector emerges.")
    print()
    print("  So this gravity/atlas route is not the missing non-homogeneous")
    print("  local-to-generation bridge on the present stack.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
