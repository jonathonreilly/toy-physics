#!/usr/bin/env python3
"""End-to-end PMNS closure from microscopic-sector-derived observable packs only."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    active_operator,
    circularity_guard,
    classify_tau_and_q_from_response_columns,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    effective_block_from_sector_operator,
    masses_and_pmns_from_pair,
    passive_operator,
    active_response_columns_from_sector_operator,
    passive_response_columns_from_sector_operator,
    recover_passive_coeffs,
    sector_operator_fixture_from_effective_block,
)

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


def close_from_lower_level_observables(
    neutral_columns: list[np.ndarray], charge_columns: list[np.ndarray], lam_act: float, lam_pass: float
) -> dict:
    tau, q, neutral_block, charge_block = classify_tau_and_q_from_response_columns(
        neutral_columns, charge_columns, lam_act, lam_pass
    )
    if tau == 0:
        active_columns, passive_columns = neutral_columns, charge_columns
    else:
        active_columns, passive_columns = charge_columns, neutral_columns

    _act_kernel, active_block = derive_active_block_from_response_columns(active_columns, lam_act)
    _pass_kernel, passive_block = derive_passive_block_from_response_columns(passive_columns, lam_pass)
    coeffs = recover_passive_coeffs(passive_block, q)

    if tau == 0:
        d0_trip, dm_trip = active_block, passive_block
    else:
        d0_trip, dm_trip = passive_block, active_block

    closure = masses_and_pmns_from_pair(d0_trip, dm_trip)
    closure["tau"] = tau
    closure["q"] = q
    closure["a"] = coeffs
    closure["D_0^trip"] = d0_trip
    closure["D_-^trip"] = dm_trip
    return closure


def build_observable_pack(
    tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    active_sector = sector_operator_fixture_from_effective_block(active_operator(x, y, delta), seed=701 + 13 * tau + q)
    passive_sector = sector_operator_fixture_from_effective_block(passive_operator(coeffs, q), seed=809 + 13 * tau + q)
    active_cols = active_response_columns_from_sector_operator(active_sector, 0.31)[1]
    passive_cols = passive_response_columns_from_sector_operator(passive_sector, 0.27)[1]
    return (active_cols, passive_cols) if tau == 0 else (passive_cols, active_cols)


def reference_pair(
    tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float
) -> tuple[np.ndarray, np.ndarray]:
    active_sector = sector_operator_fixture_from_effective_block(active_operator(x, y, delta), seed=701 + 13 * tau + q)
    passive_sector = sector_operator_fixture_from_effective_block(passive_operator(coeffs, q), seed=809 + 13 * tau + q)
    active = effective_block_from_sector_operator(active_sector)
    passive = effective_block_from_sector_operator(passive_sector)
    return (active, passive) if tau == 0 else (passive, active)


def run_sample(label: str, tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float) -> None:
    neutral_cols, charge_cols = build_observable_pack(tau, q, coeffs, x, y, delta)
    out = close_from_lower_level_observables(neutral_cols, charge_cols, 0.31, 0.27)
    ref_d0, ref_dm = reference_pair(tau, q, coeffs, x, y, delta)
    ref = masses_and_pmns_from_pair(ref_d0, ref_dm)

    check(f"{label}: circularity guard passes", circularity_guard(close_from_lower_level_observables, {"tau", "q", "x", "y", "delta", "coeffs", "d0_trip", "dm_trip"})[0])
    check(f"{label}: derived pair matches the reference pair",
          np.linalg.norm(out["D_0^trip"] - ref_d0) < 1e-12 and np.linalg.norm(out["D_-^trip"] - ref_dm) < 1e-12)
    check(f"{label}: branch matches", out["branch"] == ref["branch"], f"{out['branch']}")
    check(f"{label}: passive offset/coefficient data match", out["q"] == q and np.linalg.norm(out["a"] - coeffs) < 1e-12,
          f"q={out['q']}, a={np.round(out['a'], 6)}")
    check(f"{label}: H_nu matches", np.linalg.norm(out["H_nu"] - ref["H_nu"]) < 1e-12)
    check(f"{label}: H_e matches", np.linalg.norm(out["H_e"] - ref["H_e"]) < 1e-12)
    check(f"{label}: masses match", np.linalg.norm(out["m_nu"] - ref["m_nu"]) < 1e-10 and np.linalg.norm(out["m_e"] - ref["m_e"]) < 1e-10)
    if label == "aligned-seed":
        print(f"  [INFO] {label}: PMNS is degenerate on the aligned seed patch, so H-level closure is the invariant target")
    else:
        check(f"{label}: PMNS matches", np.linalg.norm(np.abs(out["pmns"]) - np.abs(ref["pmns"])) < 1e-10)
    check(f"{label}: sheet matches", out["sheet"] == ref["sheet"], f"sheet={out['sheet']}")


def main() -> int:
    print("=" * 88)
    print("PMNS LOWER-LEVEL END-TO-END CLOSURE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Starting from observable packs canonically derived from microscopic")
    print("  sector operators, can we reconstruct the PMNS-relevant microscopic")
    print("  pair and all downstream closure data?")

    run_sample(
        "aligned-seed",
        0,
        2,
        np.array([0.07, 0.11, 0.23], dtype=complex),
        np.array([0.90, 0.90, 0.90], dtype=float),
        np.array([0.40, 0.40, 0.40], dtype=float),
        0.0,
    )
    run_sample(
        "neutrino-active-off-seed",
        0,
        2,
        np.array([0.07, 0.11, 0.23], dtype=complex),
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    run_sample(
        "charged-lepton-active-off-seed",
        1,
        1,
        np.array([0.17, 0.09, 0.04], dtype=complex),
        np.array([0.92, 1.08, 0.85], dtype=float),
        np.array([0.33, 0.49, 0.26], dtype=float),
        -0.37,
    )

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact lower-level end-to-end closure:")
    print("    - no PMNS-side value inputs")
    print("    - pair reconstructed from microscopic-sector-derived observable packs")
    print("    - branch, sheet, H_nu, H_e, masses, and PMNS recovered downstream")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
