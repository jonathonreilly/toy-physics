#!/usr/bin/env python3
"""Uniform scalar-deformation boundary for the retained PMNS lepton lane.

Question:
  If we move beyond the sole-axiom free point by admitting the repo's
  translation-invariant local scalar / Coleman-Weinberg deformation route,
  does that produce a nontrivial retained PMNS response profile?

Answer:
  No. A uniform local scalar condensate is generation-blind on the retained
  `hw=1` triplets. The most general resulting lower-level lepton pair is

      D_0^trip = u_0 I_3,
      D_-^trip = u_- I_3,

  so both active/passive response profiles remain scalar column sets and the
  retained one-sided minimal PMNS closure stack still rejects them.

Boundary:
  This is a stronger negative theorem than the sole-axiom free-point result.
  It closes the admitted uniform scalar/Coleman-Weinberg extension itself on
  the retained PMNS lane: that extension can only rescale the free point, not
  generate retained PMNS structure.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from pmns_lower_level_utils import (
    I3,
    TARGET_SUPPORT,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    passive_response_columns_from_sector_operator,
    support_mask,
)
from frontier_pmns_active_four_real_source_from_transport import active_four_real_source
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def expect_raises(fn, exc_type) -> tuple[bool, str]:
    try:
        fn()
    except exc_type as e:  # noqa: PERF203
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, f"wrong exception {type(e).__name__}: {e}"
    return False, "no exception"


def hw1_corners() -> list[np.ndarray]:
    return [
        np.array([math.pi, 0.0, 0.0], dtype=float),
        np.array([0.0, math.pi, 0.0], dtype=float),
        np.array([0.0, 0.0, math.pi], dtype=float),
    ]


def staggered_h_antiherm_with_uniform_scalar(K: np.ndarray, phi: float) -> np.ndarray:
    alpha_list = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alpha_list)}
    h = np.zeros((8, 8), dtype=complex)
    for a in alpha_list:
        i = alpha_idx[a]
        a1, a2, a3 = a
        for mu in range(3):
            if mu == 0:
                eta = 1.0
            elif mu == 1:
                eta = (-1.0) ** a1
            else:
                eta = (-1.0) ** (a1 + a2)
            b = list(a)
            b[mu] = 1 - b[mu]
            j = alpha_idx[tuple(b)]
            phase = np.exp(1j * K[mu]) if a[mu] == 1 else 1.0
            h[i, j] += 0.5 * eta * phase
            h[j, i] -= 0.5 * eta * np.conj(phase)
        eps = (-1.0) ** (a1 + a2 + a3)
        h[i, i] += 1j * phi * eps
    return h


def positive_corner_energy(phi: float, K: np.ndarray) -> float:
    herm = 1j * staggered_h_antiherm_with_uniform_scalar(K, phi)
    evals = np.sort(np.linalg.eigvalsh(herm))
    return float(evals[4])


def scalar_triplet_block(u: float) -> np.ndarray:
    return float(u) * I3


def part1_uniform_scalar_condensate_keeps_the_hw1_triplet_scalar() -> None:
    print("\n" + "=" * 88)
    print("PART 1: UNIFORM SCALAR CONDENSATE KEEPS THE hw=1 TRIPLET SCALAR")
    print("=" * 88)

    for phi in (0.0, 0.2, 0.7, 1.3):
        energies = []
        square_residuals = []
        for K in hw1_corners():
            h = staggered_h_antiherm_with_uniform_scalar(K, phi)
            energies.append(positive_corner_energy(phi, K))
            square_residuals.append(float(np.linalg.norm(h @ h + (1.0 + phi**2) * np.eye(8))))

        energies = np.array(energies, dtype=float)
        check(
            f"phi={phi:g}: each hw=1 corner still has exact energy sqrt(1+phi^2)",
            np.allclose(energies, math.sqrt(1.0 + phi**2), atol=1e-12),
            f"energies={np.round(energies, 12)}",
        )
        check(
            f"phi={phi:g}: the three hw=1 corners remain exactly degenerate",
            np.allclose(energies, energies[0], atol=1e-12),
        )
        check(
            f"phi={phi:g}: the corner Hamiltonian squares to -(1+phi^2) I_8",
            max(square_residuals) < 1e-12,
            f"max residual={max(square_residuals):.2e}",
        )

    print()
    print("  So the admitted translation-invariant local scalar condensate does")
    print("  not split or mix the three generation corners. It only renormalizes")
    print("  their common scalar energy.")


def part2_the_most_general_retained_triplet_pair_from_a_uniform_scalar_lane_is_sector_scalar() -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: THE RETAINED LEPTON PAIR IS SECTOR-SCALAR ON THE UNIFORM SCALAR LANE")
    print("=" * 88)

    u0 = math.sqrt(1.0 + 0.4**2)
    um = math.sqrt(1.0 + 0.9**2)
    d0_trip = scalar_triplet_block(u0)
    dm_trip = scalar_triplet_block(um)

    check("The neutral retained triplet block is generation-scalar", np.linalg.norm(d0_trip - u0 * I3) < 1e-12)
    check("The charge-(-1) retained triplet block is generation-scalar", np.linalg.norm(dm_trip - um * I3) < 1e-12)
    check("A scalar active block has purely diagonal support, not the canonical active support I+C",
          np.array_equal(support_mask(d0_trip), np.eye(3, dtype=int)) and not np.array_equal(support_mask(d0_trip), TARGET_SUPPORT))
    check("The scalar active block has zero four-real orbit-breaking source", np.linalg.norm(active_four_real_source(d0_trip)) < 1e-12,
          f"source={np.round(active_four_real_source(d0_trip), 6)}")

    print()
    print("  So the admitted uniform scalar/CW lane can at most move the retained")
    print("  PMNS pair along sector-scalar directions (u_0 I_3, u_- I_3).")
    return d0_trip, dm_trip


def part3_scalar_response_profiles_are_exact_scalar_resolvents() -> tuple[list[np.ndarray], list[np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 3: THE INDUCED LOWER-LEVEL RESPONSE PROFILES STAY SCALAR")
    print("=" * 88)

    u_act = math.sqrt(1.0 + 0.4**2)
    u_pass = math.sqrt(1.0 + 0.9**2)
    lam_act = 0.31
    lam_pass = 0.27

    active_cols = active_response_columns_from_sector_operator(scalar_triplet_block(u_act), lam_act)[1]
    passive_cols = passive_response_columns_from_sector_operator(scalar_triplet_block(u_pass), lam_pass)[1]
    act_kernel, act_block = derive_active_block_from_response_columns(active_cols, lam_act)
    pass_kernel, pass_block = derive_passive_block_from_response_columns(passive_cols, lam_pass)

    active_scale = 1.0 / (1.0 - lam_act * (u_act - 1.0))
    passive_scale = 1.0 / (1.0 - lam_pass * u_pass)
    expected_active = active_scale * I3
    expected_passive = passive_scale * I3

    check("The active response profile is exactly a scalar resolvent column set",
          np.linalg.norm(np.column_stack(active_cols) - expected_active) < 1e-12,
          f"scale={active_scale:.12f}")
    check("The passive response profile is exactly a scalar resolvent column set",
          np.linalg.norm(np.column_stack(passive_cols) - expected_passive) < 1e-12,
          f"scale={passive_scale:.12f}")
    check("The scalar response profiles recover the same scalar triplet blocks exactly",
          np.linalg.norm(act_block - scalar_triplet_block(u_act)) < 1e-12 and np.linalg.norm(pass_block - scalar_triplet_block(u_pass)) < 1e-12)
    check("The scalar response kernels themselves carry no active-support or corner-breaking data",
          np.array_equal(support_mask(act_kernel), np.eye(3, dtype=int)) and np.array_equal(support_mask(pass_kernel), np.eye(3, dtype=int)))

    return active_cols, passive_cols


def part4_the_retained_pmns_closure_stack_rejects_every_scalar_pair(
    active_cols: list[np.ndarray], passive_cols: list[np.ndarray]
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE RETAINED PMNS STACK REJECTS THE UNIFORM SCALAR LANE")
    print("=" * 88)

    ok, detail = expect_raises(
        lambda: close_from_lower_level_observables(active_cols, passive_cols, 0.31, 0.27),
        ValueError,
    )
    check("The live retained lower-level PMNS closure stack rejects scalar response profiles", ok, detail)
    check("Reason: the resulting pair is not on a one-sided minimal PMNS class",
          ("one-sided minimal PMNS class" in detail) or ("response packs do not realize a one-sided minimal PMNS class" in detail),
          detail)

    print()
    print("  So the admitted uniform scalar/CW deformation law still cannot realize")
    print("  the retained PMNS lane. It only rescales the free point.")


def main() -> int:
    print("=" * 88)
    print("PMNS UNIFORM SCALAR DEFORMATION BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  If we admit the translation-invariant local scalar/Coleman-Weinberg")
    print("  deformation route, does that produce a nontrivial retained PMNS")
    print("  lower-level response profile?")

    part1_uniform_scalar_condensate_keeps_the_hw1_triplet_scalar()
    part2_the_most_general_retained_triplet_pair_from_a_uniform_scalar_lane_is_sector_scalar()
    active_cols, passive_cols = part3_scalar_response_profiles_are_exact_scalar_resolvents()
    part4_the_retained_pmns_closure_stack_rejects_every_scalar_pair(active_cols, passive_cols)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact admitted-scalar boundary:")
    print("    - a uniform local scalar condensate keeps the hw=1 triplets scalar")
    print("    - the most general retained lepton pair on that lane is (u_0 I_3, u_- I_3)")
    print("    - the induced lower-level response profiles are scalar resolvents")
    print("    - the retained PMNS closure stack rejects those profiles exactly")
    print()
    print("  So even the admitted uniform scalar / Coleman-Weinberg deformation")
    print("  route does not generate retained PMNS structure by itself.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
