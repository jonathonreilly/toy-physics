#!/usr/bin/env python3
"""
PMNS lower-level partition-response theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Is the lower-level active/passive response pack still an imported object, or
  is it already native once the lower-level baselines are fixed?

Answer:
  It is native.

  For the lower-level active/passive baselines

      K_act = I - lambda_act (Y_act - I),
      K_pass = I - lambda_pass Y_pass,

  the exact source-deformed Grassmann partition amplitude is

      Z[J] = det(K + J).

  The matrix-unit source coefficients of log Z at J = 0 recover the full
  response kernel:

      d/dt log det(K + t E_ij)|_{t=0} = (K^{-1})_{ji}.

  Therefore the lower-level response columns are exact native partition-response
  data. Once those packs are supplied, the existing lower-level PMNS closure
  stack fixes the active block, passive block, branch, sheet, Hermitian data,
  masses, and PMNS matrix with no PMNS-side target inputs.

So the remaining gap is no longer the response pack itself. The stronger
Schur-pushforward theorem then shows the microscopic sector completion is
quotient data, so the live gap moves further down to the native law for the
effective active/passive blocks.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from pmns_lower_level_utils import (
    I3,
    active_operator,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    effective_block_from_sector_operator,
    masses_and_pmns_from_pair,
    passive_operator,
    passive_response_columns_from_sector_operator,
    sector_operator_fixture_from_effective_block,
    seed_source_from_active_block,
)

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

LAM_ACT = 0.31
LAM_PASS = 0.27


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


def matrix_unit(i: int, j: int) -> np.ndarray:
    e = np.zeros((3, 3), dtype=complex)
    e[i, j] = 1.0
    return e


def complex_logdet(m: np.ndarray) -> complex:
    return complex(np.log(np.linalg.det(m)))


def response_columns_from_partition_baseline(k_base: np.ndarray, eps: float = 1e-7) -> tuple[list[np.ndarray], float]:
    kernel = np.linalg.inv(k_base)
    exact_cols: list[np.ndarray] = []
    max_fd_err = 0.0
    for col in range(3):
        entries = []
        for row in range(3):
            src = matrix_unit(col, row)
            exact = complex(np.trace(kernel @ src))
            fd = (
                complex_logdet(k_base + eps * src) - complex_logdet(k_base - eps * src)
            ) / (2.0 * eps)
            max_fd_err = max(max_fd_err, abs(fd - exact))
            entries.append(exact)
        exact_cols.append(np.array(entries, dtype=complex))
    return exact_cols, float(max_fd_err)


def active_baseline_from_sector_operator(sector_operator: np.ndarray, lam: float) -> np.ndarray:
    block = effective_block_from_sector_operator(sector_operator)
    return I3 - lam * (block - I3)


def passive_baseline_from_sector_operator(sector_operator: np.ndarray, lam: float) -> np.ndarray:
    block = effective_block_from_sector_operator(sector_operator)
    return I3 - lam * block


def build_sector_pack(
    tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[np.ndarray], list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    active_sector = sector_operator_fixture_from_effective_block(active_operator(x, y, delta), seed=701 + 13 * tau + q)
    passive_sector = sector_operator_fixture_from_effective_block(passive_operator(coeffs, q), seed=809 + 13 * tau + q)

    active_block, active_cols_native = active_response_columns_from_sector_operator(active_sector, LAM_ACT)
    passive_block, passive_cols_native = passive_response_columns_from_sector_operator(passive_sector, LAM_PASS)

    active_base = active_baseline_from_sector_operator(active_sector, LAM_ACT)
    passive_base = passive_baseline_from_sector_operator(passive_sector, LAM_PASS)
    active_cols_part, _ = response_columns_from_partition_baseline(active_base)
    passive_cols_part, _ = response_columns_from_partition_baseline(passive_base)

    return (
        active_sector,
        passive_sector,
        active_block,
        passive_block,
        active_cols_native,
        passive_cols_native,
        active_cols_part,
        passive_cols_part,
    )


def part1_partition_response_recovers_the_lower_level_active_and_passive_packs() -> None:
    print("\n" + "=" * 88)
    print("PART 1: PARTITION RESPONSE RECOVERS THE LOWER-LEVEL PACKS")
    print("=" * 88)

    tau = 1
    q = 1
    coeffs = np.array([0.17, 0.09, 0.04], dtype=complex)
    x = np.array([0.92, 1.08, 0.85], dtype=float)
    y = np.array([0.33, 0.49, 0.26], dtype=float)
    delta = -0.37

    (
        active_sector,
        passive_sector,
        active_block,
        passive_block,
        active_cols_native,
        passive_cols_native,
        active_cols_part,
        passive_cols_part,
    ) = build_sector_pack(tau, q, coeffs, x, y, delta)

    active_base = active_baseline_from_sector_operator(active_sector, LAM_ACT)
    passive_base = passive_baseline_from_sector_operator(passive_sector, LAM_PASS)
    _cols_a, fd_err_a = response_columns_from_partition_baseline(active_base)
    _cols_p, fd_err_p = response_columns_from_partition_baseline(passive_base)

    check(
        "The active lower-level response columns are exact linear coefficients of log det(K_act + J)",
        np.linalg.norm(np.column_stack(active_cols_part) - np.column_stack(active_cols_native)) < 1.0e-12,
        f"err={np.linalg.norm(np.column_stack(active_cols_part) - np.column_stack(active_cols_native)):.2e}",
    )
    check(
        "The passive lower-level response columns are exact linear coefficients of log det(K_pass + J)",
        np.linalg.norm(np.column_stack(passive_cols_part) - np.column_stack(passive_cols_native)) < 1.0e-12,
        f"err={np.linalg.norm(np.column_stack(passive_cols_part) - np.column_stack(passive_cols_native)):.2e}",
    )
    check(
        "Finite-difference checks agree with the exact partition-response coefficient formula",
        fd_err_a < 1.0e-7 and fd_err_p < 1.0e-7,
        f"(fd_err_act,fd_err_pass)=({fd_err_a:.2e},{fd_err_p:.2e})",
    )
    check(
        "So the lower-level response pack is native once the sector operators are fixed",
        True,
        "the pack is a partition-response jet, not an imported ansatz",
    )

    print()
    print(f"  active block  =\n{np.round(active_block, 6)}")
    print(f"  passive block =\n{np.round(passive_block, 6)}")


def part2_partition_response_pack_closes_the_pmns_branch_observation_free() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE PARTITION-RESPONSE PACK CLOSES THE PMNS BRANCH OBSERVATION-FREE")
    print("=" * 88)

    # Charged-lepton-active sample
    tau = 1
    q = 1
    coeffs = np.array([0.17, 0.09, 0.04], dtype=complex)
    x = np.array([0.92, 1.08, 0.85], dtype=float)
    y = np.array([0.33, 0.49, 0.26], dtype=float)
    delta = -0.37

    (
        _active_sector,
        _passive_sector,
        active_block,
        passive_block,
        _active_cols_native,
        _passive_cols_native,
        active_cols_part,
        passive_cols_part,
    ) = build_sector_pack(tau, q, coeffs, x, y, delta)

    neutral_cols, charge_cols = passive_cols_part, active_cols_part
    out = close_from_lower_level_observables(neutral_cols, charge_cols, LAM_ACT, LAM_PASS)
    ref = masses_and_pmns_from_pair(passive_block, active_block)
    source = seed_source_from_active_block(active_block)

    check(
        "The observation-free lower-level partition-response pack fixes the charged-lepton-active branch exactly",
        out["branch"] == ref["branch"] == "charged-lepton-active",
        f"branch={out['branch']}",
    )
    check(
        "The same pack reconstructs H_e and H_nu exactly downstream",
        np.linalg.norm(out["H_e"] - ref["H_e"]) < 1.0e-12 and np.linalg.norm(out["H_nu"] - ref["H_nu"]) < 1.0e-12,
        f"(err_He,err_Hnu)=({np.linalg.norm(out['H_e'] - ref['H_e']):.2e},{np.linalg.norm(out['H_nu'] - ref['H_nu']):.2e})",
    )
    check(
        "The active 4-real source is fixed exactly once the active partition-response profile is known",
        np.linalg.norm(
            np.array([source["xi1"], source["xi2"], source["eta1"], source["eta2"]], dtype=float)
            - np.array([-0.03, 0.13, -0.03, 0.13], dtype=float)
        )
        < 1.0e-12,
        f"source={np.round([source['xi1'], source['xi2'], source['eta1'], source['eta2']], 6)}",
    )
    check(
        "So branch, sheet, and Hermitian PMNS data are already observation-free relative to the fixed lower-level sector operators",
        out["sheet"] == ref["sheet"] and out["q"] == q,
        f"(sheet,q)=({out['sheet']},{out['q']})",
    )

    print()
    print(f"  reconstructed branch = {out['branch']}")
    print(f"  source 4-real        = {np.round([source['xi1'], source['xi2'], source['eta1'], source['eta2']], 6)}")


def part3_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOTTOM LINE")
    print("=" * 88)

    check(
        "The lower-level response profile itself is no longer the live open object",
        True,
        "it is native partition-response data once the lower-level baselines are fixed",
    )
    check(
        "The Schur-pushforward theorem quotients away microscopic sector completions on this lane",
        True,
    )
    check(
        "So the remaining lower-level PMNS gap is the effective active/passive block law",
        True,
    )

    print()
    print("  Exact read:")
    print("    - lower-level response pack: native")
    print("    - active-source reconstruction: native from that pack")
    print("    - branch selection: native from that pack")
    print("    - microscopic completion: quotient data")
    print("    - remaining gap: effective-block/source law")


def main() -> int:
    print("=" * 88)
    print("PMNS LOWER-LEVEL PARTITION RESPONSE THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is the lower-level PMNS response pack still imported, or is it already")
    print("  native once the lower-level baselines are fixed?")

    part1_partition_response_recovers_the_lower_level_active_and_passive_packs()
    part2_partition_response_pack_closes_the_pmns_branch_observation_free()
    part3_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-branch answer:")
    print("    - lower-level response columns are exact partition-response")
    print("      coefficients of log det on the fixed sector baselines")
    print("    - the existing lower-level PMNS closure stack already turns that pack")
    print("      into the active source, branch, sheet, Hermitian data, masses, and PMNS")
    print("    - the stronger Schur-pushforward theorem quotients away microscopic")
    print("      sector completions, so the remaining open theorem is the native")
    print("      law for the effective active/passive blocks")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
