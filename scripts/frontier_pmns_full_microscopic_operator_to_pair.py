#!/usr/bin/env python3
"""PMNS closure from the full microscopic charge-preserving operator."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    active_operator,
    active_response_columns_from_sector_operator,
    circularity_guard,
    effective_block_from_sector_operator,
    passive_operator,
    passive_response_columns_from_sector_operator,
    sector_operator_fixture_from_effective_block,
)
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


def build_full_charge_preserving_operator(
    neutral_sector: np.ndarray, charge_sector: np.ndarray, plus_shift: float = 3.4
) -> np.ndarray:
    plus_sector = plus_shift * np.eye(2, dtype=complex)
    return np.block(
        [
            [neutral_sector, np.zeros((neutral_sector.shape[0], charge_sector.shape[0]), dtype=complex), np.zeros((neutral_sector.shape[0], 2), dtype=complex)],
            [np.zeros((charge_sector.shape[0], neutral_sector.shape[0]), dtype=complex), charge_sector, np.zeros((charge_sector.shape[0], 2), dtype=complex)],
            [np.zeros((2, neutral_sector.shape[0]), dtype=complex), np.zeros((2, charge_sector.shape[0]), dtype=complex), plus_sector],
        ]
    )


def extract_sector_operators(d: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return d[:5, :5].copy(), d[5:10, 5:10].copy()


def sample_full_operator(
    tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    active_sector = sector_operator_fixture_from_effective_block(active_operator(x, y, delta), seed=1201 + 23 * tau + q)
    passive_sector = sector_operator_fixture_from_effective_block(passive_operator(coeffs, q), seed=1301 + 23 * tau + q)
    if tau == 0:
        neutral_sector, charge_sector = active_sector, passive_sector
    else:
        neutral_sector, charge_sector = passive_sector, active_sector
    return build_full_charge_preserving_operator(neutral_sector, charge_sector), neutral_sector, charge_sector


def close_from_full_microscopic_operator(d: np.ndarray, lam_act: float, lam_pass: float) -> dict:
    neutral_sector, charge_sector = extract_sector_operators(d)
    neutral_cols = active_response_columns_from_sector_operator(neutral_sector, lam_act)[1]
    charge_cols = passive_response_columns_from_sector_operator(charge_sector, lam_pass)[1]
    try:
        return close_from_lower_level_observables(neutral_cols, charge_cols, lam_act, lam_pass)
    except ValueError:
        neutral_cols = passive_response_columns_from_sector_operator(neutral_sector, lam_pass)[1]
        charge_cols = active_response_columns_from_sector_operator(charge_sector, lam_act)[1]
        return close_from_lower_level_observables(neutral_cols, charge_cols, lam_act, lam_pass)


def reference_pair_from_full_operator(d: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    neutral_sector, charge_sector = extract_sector_operators(d)
    return effective_block_from_sector_operator(neutral_sector), effective_block_from_sector_operator(charge_sector)


def run_sample(label: str, tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float) -> None:
    d, neutral_sector, charge_sector = sample_full_operator(tau, q, coeffs, x, y, delta)
    derived = close_from_full_microscopic_operator(d, 0.31, 0.27)
    ref_d0, ref_dm = reference_pair_from_full_operator(d)

    check(f"{label}: full microscopic operator preserves the charge-sector split", np.linalg.norm(d[:5, 5:]) < 1e-12 and np.linalg.norm(d[5:10, :5]) < 1e-12)
    check(f"{label}: sector extraction recovers the embedded neutral operator", np.linalg.norm(extract_sector_operators(d)[0] - neutral_sector) < 1e-12)
    check(f"{label}: sector extraction recovers the embedded charge operator", np.linalg.norm(extract_sector_operators(d)[1] - charge_sector) < 1e-12)
    check(f"{label}: full-D closure recovers D_0^trip exactly", np.linalg.norm(derived['D_0^trip'] - ref_d0) < 1e-12)
    check(f"{label}: full-D closure recovers D_-^trip exactly", np.linalg.norm(derived['D_-^trip'] - ref_dm) < 1e-12)
    expected_branch = "neutrino-active" if tau == 0 else "charged-lepton-active"
    check(f"{label}: branch is read correctly from full-D data", derived["branch"] == expected_branch, derived["branch"])


def part3_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CIRCULARITY GUARD")
    print("=" * 88)
    ok, bad = circularity_guard(close_from_full_microscopic_operator, {"tau", "q", "x", "y", "delta", "coeffs", "d0_trip", "dm_trip"})
    check("The full-D closure function takes no PMNS-side target values as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS FULL MICROSCOPIC OPERATOR TO PAIR")
    print("=" * 88)
    print()
    print("Question:")
    print("  Starting from the full charge-preserving microscopic operator D alone,")
    print("  can we extract the lepton charge sectors, derive the source-response")
    print("  packs, and recover the PMNS-relevant microscopic pair?")

    print("\n" + "=" * 88)
    print("PART 1: FULL-D TO PMNS PAIR ON THE NEUTRINO-ACTIVE CLASS")
    print("=" * 88)
    run_sample(
        "neutrino-active-off-seed",
        0,
        2,
        np.array([0.07, 0.11, 0.23], dtype=complex),
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )

    print("\n" + "=" * 88)
    print("PART 2: FULL-D TO PMNS PAIR ON THE CHARGED-LEPTON-ACTIVE CLASS")
    print("=" * 88)
    run_sample(
        "charged-lepton-active-off-seed",
        1,
        1,
        np.array([0.17, 0.09, 0.04], dtype=complex),
        np.array([0.92, 1.08, 0.85], dtype=float),
        np.array([0.33, 0.49, 0.26], dtype=float),
        -0.37,
    )

    part3_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact full-microscopic-to-pair reduction:")
    print("    - the theorem input is the full charge-preserving microscopic operator D")
    print("    - neutral and charge sectors are extracted from D")
    print("    - sector source-response packs are derived from those sectors")
    print("    - the PMNS-relevant microscopic pair is then recovered exactly")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
