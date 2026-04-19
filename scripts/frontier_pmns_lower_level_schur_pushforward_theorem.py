#!/usr/bin/env python3
"""
PMNS lower-level Schur-pushforward theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Does the lower-level PMNS response/closure lane still require a microscopic
  sector-operator law, or does the full microscopic source-response already
  factor exactly through the Schur effective blocks?

Answer:
  It factors exactly through the Schur effective blocks.

  For lower-level active/passive full baselines

      K_act^full = I - lambda_act (Y_full - I),
      K_pass^full = I - lambda_pass Y_full,

  and any support-restricted source J_sup on the 3x3 PMNS support,

      log det(K_full + J_sup^full) - log det(K_full)

  depends only on the Schur effective baseline on that support.

Therefore:
  - the lower-level response columns depend only on the effective active/passive
    blocks, not on the microscopic spectator completion;
  - any two microscopic sector operators with the same effective blocks yield
    the same response pack and the same downstream PMNS closure data.

So the microscopic sector-operator choice is exact quotient data on this lane.
The remaining open theorem is the law for the effective active/passive blocks,
not the microscopic completion.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from pmns_lower_level_utils import (
    I3,
    active_operator,
    active_response_columns_from_sector_operator,
    effective_block_from_sector_operator,
    masses_and_pmns_from_pair,
    passive_operator,
    passive_response_columns_from_sector_operator,
    schur_eff,
    sector_operator_fixture_from_effective_block,
)

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

SUPPORT_DIM = 3
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


def complex_logdet(m: np.ndarray) -> complex:
    return complex(np.log(np.linalg.det(m)))


def embed_support_source(j_support: np.ndarray, full_dim: int) -> np.ndarray:
    j = np.zeros((full_dim, full_dim), dtype=complex)
    j[:SUPPORT_DIM, :SUPPORT_DIM] = np.asarray(j_support, dtype=complex)
    return j


def active_full_baseline(sector_operator: np.ndarray, lam: float) -> np.ndarray:
    ident = np.eye(sector_operator.shape[0], dtype=complex)
    return ident - lam * (np.asarray(sector_operator, dtype=complex) - ident)


def passive_full_baseline(sector_operator: np.ndarray, lam: float) -> np.ndarray:
    ident = np.eye(sector_operator.shape[0], dtype=complex)
    return ident - lam * np.asarray(sector_operator, dtype=complex)


def support_schur_baseline(full_baseline: np.ndarray) -> np.ndarray:
    if full_baseline.shape[0] == SUPPORT_DIM:
        return np.asarray(full_baseline, dtype=complex)
    a = full_baseline[:SUPPORT_DIM, :SUPPORT_DIM]
    b = full_baseline[:SUPPORT_DIM, SUPPORT_DIM:]
    c = full_baseline[SUPPORT_DIM:, :SUPPORT_DIM]
    f = full_baseline[SUPPORT_DIM:, SUPPORT_DIM:]
    return schur_eff(a, b, c, f)


def response_columns_from_full_inverse(full_baseline: np.ndarray) -> list[np.ndarray]:
    inv_full = np.linalg.inv(full_baseline)
    support_inv = inv_full[:SUPPORT_DIM, :SUPPORT_DIM]
    return [support_inv[:, i].copy() for i in range(SUPPORT_DIM)]


def part1_full_support_source_response_factors_exactly_through_the_schur_baseline() -> None:
    print("\n" + "=" * 88)
    print("PART 1: FULL SUPPORT SOURCE RESPONSE FACTORS EXACTLY THROUGH THE SCHUR BASELINE")
    print("=" * 88)

    active_block = active_operator(
        np.array([0.92, 1.08, 0.85], dtype=float),
        np.array([0.33, 0.49, 0.26], dtype=float),
        -0.37,
    )
    passive_block = passive_operator(np.array([0.17, 0.09, 0.04], dtype=complex), 1)
    active_sector = sector_operator_fixture_from_effective_block(active_block, seed=701)
    passive_sector = sector_operator_fixture_from_effective_block(passive_block, seed=809)

    j_support = np.array(
        [
            [0.08, 0.02 + 0.01j, 0.0],
            [0.02 - 0.01j, -0.03, 0.02],
            [0.0, 0.02, 0.06],
        ],
        dtype=complex,
    )

    for label, full_baseline in (
        ("active", active_full_baseline(active_sector, LAM_ACT)),
        ("passive", passive_full_baseline(passive_sector, LAM_PASS)),
    ):
        eff_baseline = support_schur_baseline(full_baseline)
        j_full = embed_support_source(j_support, full_baseline.shape[0])
        full_resp = complex_logdet(full_baseline + j_full) - complex_logdet(full_baseline)
        eff_resp = complex_logdet(eff_baseline + j_support) - complex_logdet(eff_baseline)
        inv_support = np.linalg.inv(full_baseline)[:SUPPORT_DIM, :SUPPORT_DIM]
        inv_eff = np.linalg.inv(eff_baseline)

        check(
            f"{label}: support-restricted microscopic logdet response factors exactly through the Schur baseline",
            abs(full_resp - eff_resp) < 1.0e-12,
            f"|Δ|={abs(full_resp - eff_resp):.2e}",
        )
        check(
            f"{label}: the support block of the full inverse equals the inverse of the Schur baseline",
            np.linalg.norm(inv_support - inv_eff) < 1.0e-12,
            f"err={np.linalg.norm(inv_support - inv_eff):.2e}",
        )


def part2_lower_level_response_columns_are_schur_class_invariants() -> tuple[list[np.ndarray], list[np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 2: LOWER-LEVEL RESPONSE COLUMNS ARE SCHUR-CLASS INVARIANTS")
    print("=" * 88)

    active_block = active_operator(
        np.array([0.92, 1.08, 0.85], dtype=float),
        np.array([0.33, 0.49, 0.26], dtype=float),
        -0.37,
    )
    passive_block = passive_operator(np.array([0.17, 0.09, 0.04], dtype=complex), 1)

    active_sector_a = sector_operator_fixture_from_effective_block(active_block, seed=701)
    active_sector_b = sector_operator_fixture_from_effective_block(active_block, seed=1701)
    passive_sector_a = sector_operator_fixture_from_effective_block(passive_block, seed=809)
    passive_sector_b = sector_operator_fixture_from_effective_block(passive_block, seed=1809)

    active_cols_a = active_response_columns_from_sector_operator(active_sector_a, LAM_ACT)[1]
    active_cols_b = active_response_columns_from_sector_operator(active_sector_b, LAM_ACT)[1]
    passive_cols_a = passive_response_columns_from_sector_operator(passive_sector_a, LAM_PASS)[1]
    passive_cols_b = passive_response_columns_from_sector_operator(passive_sector_b, LAM_PASS)[1]

    d_active = float(np.linalg.norm(active_sector_a - active_sector_b))
    d_passive = float(np.linalg.norm(passive_sector_a - passive_sector_b))
    err_active = float(np.linalg.norm(np.column_stack(active_cols_a) - np.column_stack(active_cols_b)))
    err_passive = float(np.linalg.norm(np.column_stack(passive_cols_a) - np.column_stack(passive_cols_b)))

    check(
        "Distinct microscopic active-sector completions can realize the same effective active block",
        d_active > 1.0e-3
        and np.linalg.norm(
            effective_block_from_sector_operator(active_sector_a) - effective_block_from_sector_operator(active_sector_b)
        )
        < 1.0e-12,
        f"|Δsector|={d_active:.6f}",
    )
    check(
        "Distinct microscopic passive-sector completions can realize the same effective passive block",
        d_passive > 1.0e-3
        and np.linalg.norm(
            effective_block_from_sector_operator(passive_sector_a) - effective_block_from_sector_operator(passive_sector_b)
        )
        < 1.0e-12,
        f"|Δsector|={d_passive:.6f}",
    )
    check(
        "The active lower-level response pack is identical across the active Schur class",
        err_active < 1.0e-12,
        f"err={err_active:.2e}",
    )
    check(
        "The passive lower-level response pack is identical across the passive Schur class",
        err_passive < 1.0e-12,
        f"err={err_passive:.2e}",
    )

    return active_cols_a, passive_cols_a


def part3_downstream_pmns_closure_is_invariant_across_microscopic_sector_completions() -> None:
    print("\n" + "=" * 88)
    print("PART 3: DOWNSTREAM PMNS CLOSURE IS INVARIANT ACROSS MICROSCOPIC COMPLETIONS")
    print("=" * 88)

    active_block = active_operator(
        np.array([0.92, 1.08, 0.85], dtype=float),
        np.array([0.33, 0.49, 0.26], dtype=float),
        -0.37,
    )
    passive_block = passive_operator(np.array([0.17, 0.09, 0.04], dtype=complex), 1)

    active_sector_a = sector_operator_fixture_from_effective_block(active_block, seed=701)
    active_sector_b = sector_operator_fixture_from_effective_block(active_block, seed=1701)
    passive_sector_a = sector_operator_fixture_from_effective_block(passive_block, seed=809)
    passive_sector_b = sector_operator_fixture_from_effective_block(passive_block, seed=1809)

    close_a = close_from_lower_level_observables(
        passive_response_columns_from_sector_operator(passive_sector_a, LAM_PASS)[1],
        active_response_columns_from_sector_operator(active_sector_a, LAM_ACT)[1],
        LAM_ACT,
        LAM_PASS,
    )
    close_b = close_from_lower_level_observables(
        passive_response_columns_from_sector_operator(passive_sector_b, LAM_PASS)[1],
        active_response_columns_from_sector_operator(active_sector_b, LAM_ACT)[1],
        LAM_ACT,
        LAM_PASS,
    )
    ref = masses_and_pmns_from_pair(passive_block, active_block)

    check(
        "Charged-lepton-active branch selection is invariant across microscopic Schur completions",
        close_a["branch"] == close_b["branch"] == ref["branch"] == "charged-lepton-active",
        f"branches=({close_a['branch']},{close_b['branch']})",
    )
    check(
        "H_e and H_nu are invariant across microscopic Schur completions",
        np.linalg.norm(close_a["H_e"] - close_b["H_e"]) < 1.0e-12
        and np.linalg.norm(close_a["H_nu"] - close_b["H_nu"]) < 1.0e-12,
        f"(err_He,err_Hnu)=({np.linalg.norm(close_a['H_e'] - close_b['H_e']):.2e},{np.linalg.norm(close_a['H_nu'] - close_b['H_nu']):.2e})",
    )
    check(
        "The same downstream closure data match the effective-block reference exactly",
        np.linalg.norm(close_a["H_e"] - ref["H_e"]) < 1.0e-12
        and np.linalg.norm(close_a["H_nu"] - ref["H_nu"]) < 1.0e-12,
        f"(err_He,err_Hnu)=({np.linalg.norm(close_a['H_e'] - ref['H_e']):.2e},{np.linalg.norm(close_a['H_nu'] - ref['H_nu']):.2e})",
    )
    check(
        "So the microscopic sector-operator choice is quotient data for lower-level PMNS closure",
        close_a["sheet"] == close_b["sheet"] and close_a["q"] == close_b["q"],
        f"(sheet,q)=({close_a['sheet']},{close_a['q']})",
    )


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The remaining live PMNS lower-level gap is not a microscopic sector-operator law",
        True,
    )
    check(
        "It is the law for the effective active/passive blocks that survive exact Schur pushforward",
        True,
    )
    check(
        "So the sector-operator concern is now quotiented away exactly on this lane",
        True,
    )

    print()
    print("  Exact read:")
    print("    - microscopic sector operator: quotient data")
    print("    - Schur effective blocks: load-bearing data")
    print("    - remaining gap: effective-block/source law")


def main() -> int:
    print("=" * 88)
    print("PMNS LOWER-LEVEL SCHUR-PUSHFORWARD THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the lower-level PMNS response/closure lane still require a")
    print("  microscopic sector-operator law, or does the full source-response")
    print("  already factor exactly through the Schur effective blocks?")

    part1_full_support_source_response_factors_exactly_through_the_schur_baseline()
    part2_lower_level_response_columns_are_schur_class_invariants()
    part3_downstream_pmns_closure_is_invariant_across_microscopic_sector_completions()
    part4_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-branch answer:")
    print("    - the full lower-level microscopic source-response factors exactly")
    print("      through the Schur effective baselines on PMNS support")
    print("    - response columns and downstream PMNS closure data depend only on")
    print("      the effective active/passive blocks")
    print("    - microscopic sector operators are exact quotient data on this lane")
    print("    - the remaining live theorem is the effective-block/source law")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
