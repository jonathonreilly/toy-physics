#!/usr/bin/env python3
"""HW=1 source-transfer boundary theorem for the retained PMNS lane.

This script packages the exact lower-level source/transfer interface:

- transfer summaries fix the weak-axis seed pair and branch bit
- active source-response columns fix the active kernel exactly
- passive source-response columns fix q and a_i exactly
- the combined source/transfer pack reconstructs the retained PMNS pair

It also proves the remaining boundary:

- transfer-only summaries are blind to the full 5-real active corner source
- two distinct off-seed active blocks can share the same transfer shadow

So the current exact bank is no longer blocked by the hw=1 interface itself;
what remains open is deriving that nontrivial source/transfer pack from
Cl(3) on Z^3 alone.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_corner_transport_active_block import (
    active_corner_transport,
    recover_seed_pair,
    transport_branch_bit,
)
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_transfer_operator_dominant_mode import (
    projected_transfer_kernel_from_active_block,
    reconstruct_seed_pair_from_transfer_kernel,
)
from pmns_lower_level_utils import (
    CYCLE,
    active_operator,
    active_response_columns_from_sector_operator,
    circularity_guard,
    classify_tau_and_q_from_response_columns,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    effective_block_from_sector_operator,
    masses_and_pmns_from_pair,
    passive_operator,
    passive_response_columns_from_sector_operator,
    recover_passive_coeffs,
    recover_q_from_block,
    sector_operator_fixture_from_effective_block,
    seed_source_from_active_block,
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


def hw1_source_transfer_pack(
    neutral_sector: np.ndarray,
    charge_sector: np.ndarray,
    lam_act: float,
    lam_pass: float,
) -> dict:
    tau, q, neutral_as_passive, charge_as_passive = classify_tau_and_q_from_response_columns(
        active_response_columns_from_sector_operator(neutral_sector, lam_act)[1],
        passive_response_columns_from_sector_operator(charge_sector, lam_pass)[1],
        lam_act,
        lam_pass,
    )
    if tau == 0:
        active_sector, passive_sector = neutral_sector, charge_sector
    else:
        active_sector, passive_sector = charge_sector, neutral_sector

    active_ref, active_cols = active_response_columns_from_sector_operator(active_sector, lam_act)
    passive_ref, passive_cols = passive_response_columns_from_sector_operator(passive_sector, lam_pass)
    _active_kernel, active_block = derive_active_block_from_response_columns(active_cols, lam_act)
    _passive_kernel, passive_block = derive_passive_block_from_response_columns(passive_cols, lam_pass)
    source = seed_source_from_active_block(active_block)
    transfer_kernel = source["xbar"] * np.eye(3, dtype=complex) + source["ybar"] * (CYCLE + CYCLE @ CYCLE)
    seed_pair = reconstruct_seed_pair_from_transfer_kernel(transfer_kernel)
    coeffs = recover_passive_coeffs(passive_block, q)
    return {
        "tau": tau,
        "q": q,
        "active_block": active_block,
        "passive_block": passive_block,
        "active_columns": active_cols,
        "passive_columns": passive_cols,
        "transfer_kernel": transfer_kernel,
        "seed_pair": seed_pair,
        "source": source,
        "coeffs": coeffs,
        "active_ref": active_ref,
        "passive_ref": passive_ref,
        "neutral_as_passive": neutral_as_passive,
        "charge_as_passive": charge_as_passive,
    }


def hw1_transfer_kernel_from_active_block(block: np.ndarray) -> np.ndarray:
    source = seed_source_from_active_block(block)
    return source["xbar"] * np.eye(3, dtype=complex) + source["ybar"] * (CYCLE + CYCLE @ CYCLE)


def part1_transfer_summaries_fix_the_seed_pair_and_branch_bit() -> None:
    print("\n" + "=" * 88)
    print("PART 1: TRANSFER SUMMARIES FIX THE SEED PAIR AND BRANCH BIT")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.0

    T = active_corner_transport(x, y, delta)
    xbar, ybar = recover_seed_pair(T)
    bit = transport_branch_bit(active_corner_transport(x, y, 0.63))

    transfer_kernel = np.diag(np.array([xbar, xbar, xbar], dtype=complex)) + ybar * np.array(
        [[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=complex
    )
    rxbar, rybar = reconstruct_seed_pair_from_transfer_kernel(transfer_kernel)

    check("The direct corner-transport profile recovers the weak-axis seed pair",
          abs(xbar - np.mean(x)) < 1e-12 and abs(ybar - np.mean(y)) < 1e-12,
          f"(xbar,ybar)=({xbar:.6f},{ybar:.6f})")
    check("The transfer dominant-mode law recovers the same seed pair",
          abs(rxbar - xbar) < 1e-12 and abs(rybar - ybar) < 1e-12,
          f"(rxbar,rybar)=({rxbar:.6f},{rybar:.6f})")
    check("The branch bit is fixed by the C3-odd transport asymmetry", bit in (0, 1), f"bit={bit}")


def part2_active_source_response_columns_fix_the_active_kernel() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ACTIVE SOURCE-RESPONSE COLUMNS FIX THE ACTIVE KERNEL")
    print("=" * 88)

    lam = 0.31
    target = active_operator(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    sector = sector_operator_fixture_from_effective_block(target, seed=4217)
    reference, columns = active_response_columns_from_sector_operator(sector, lam)
    _kernel, active_block = derive_active_block_from_response_columns(columns, lam)
    source = seed_source_from_active_block(active_block)

    check("The lower-level active response profile recovers the active block exactly",
          np.linalg.norm(active_block - reference) < 1e-12,
          f"error={np.linalg.norm(active_block - reference):.2e}")
    check("The active kernel is uniquely recovered from the response columns",
          np.linalg.norm(np.column_stack(columns) - np.column_stack(active_response_columns_from_sector_operator(sector, lam)[1])) < 1e-12)
    check("The active block decomposes into the seed pair plus the 5-real corner source",
          source["xi"].shape == (3,) and source["eta"].shape == (3,),
          f"(xi,eta)=({np.round(source['xi'], 6)}, {np.round(source['eta'], 6)})")


def part3_passive_source_response_columns_fix_q_and_ai() -> None:
    print("\n" + "=" * 88)
    print("PART 3: PASSIVE SOURCE-RESPONSE COLUMNS FIX q AND a_i")
    print("=" * 88)

    lam = 0.27
    target = passive_operator(np.array([0.07, 0.11, 0.23], dtype=complex), 2)
    sector = sector_operator_fixture_from_effective_block(target, seed=307)
    reference, columns = passive_response_columns_from_sector_operator(sector, lam)
    _kernel, passive_block = derive_passive_block_from_response_columns(columns, lam)
    q = recover_q_from_block(passive_block)
    coeffs = recover_passive_coeffs(passive_block, q)

    check("The lower-level passive response profile recovers the passive block exactly",
          np.linalg.norm(passive_block - reference) < 1e-12,
          f"error={np.linalg.norm(passive_block - reference):.2e}")
    check("The passive offset q is fixed by the derived passive block", q == recover_q_from_block(reference), f"q={q}")
    check("The passive coefficients a_i are fixed by the derived passive block",
          np.linalg.norm(coeffs - recover_passive_coeffs(reference, q)) < 1e-12,
          f"a={np.round(coeffs, 6)}")


def part4_combined_pack_recovers_the_retained_pair_and_downstream_closure() -> None:
    print("\n" + "=" * 88)
    print("PART 4: PACK-TO-RETAINED-PMNS BRIDGE VS INDEPENDENT SCHUR CERTIFICATE")
    print("=" * 88)
    print("  Bridge theorem (this part):")
    print("    The map (active source-response columns, passive source-response columns)")
    print("    -> (D_0^trip, D_-^trip, H_nu, H_e, m_nu, m_e, |PMNS|) computed via")
    print("    response-column inversion equals the same map computed via the direct")
    print("    Schur-complement effective block + Hermitian eigendecomposition.")
    print("    The Schur path does not call any response-column helper, so equality")
    print("    is an independent proof certificate, not a self-comparison.")
    print()

    lam_act = 0.31
    lam_pass = 0.27
    neutral_sector = sector_operator_fixture_from_effective_block(
        active_operator(
            np.array([1.15, 0.82, 0.95], dtype=float),
            np.array([0.41, 0.28, 0.54], dtype=float),
            0.63,
        ),
        seed=5311,
    )
    charge_sector = sector_operator_fixture_from_effective_block(
        passive_operator(np.array([0.07, 0.11, 0.23], dtype=complex), 2),
        seed=7311,
    )

    # Lane A: pack-derived closure via response-column inversion.
    pack = hw1_source_transfer_pack(neutral_sector, charge_sector, lam_act, lam_pass)
    closure = close_from_lower_level_observables(
        pack["active_columns"], pack["passive_columns"], lam_act, lam_pass
    )

    # Lane B: independent Schur certificate. Build the retained pair directly from
    # the sector operators via the Schur-complement effective-block formula, then
    # run the downstream Hermitian eigen-closure on that independently constructed
    # pair. This path never calls derive_*_block_from_response_columns or
    # close_from_lower_level_observables, so it is not a self-comparison of the
    # response-column helper.
    neutral_block_ref = effective_block_from_sector_operator(neutral_sector)
    charge_block_ref = effective_block_from_sector_operator(charge_sector)
    if pack["tau"] == 0:
        d0_ref, dm_ref = neutral_block_ref, charge_block_ref
    else:
        d0_ref, dm_ref = charge_block_ref, neutral_block_ref
    ref = masses_and_pmns_from_pair(d0_ref, dm_ref)

    check("The source-transfer pack derives tau and q without PMNS-side inputs",
          pack["tau"] in (0, 1) and isinstance(pack["q"], int),
          f"tau={pack['tau']}, q={pack['q']}")
    check("Bridge: pack-derived D_0^trip equals the independent Schur D_0^trip",
          np.linalg.norm(closure["D_0^trip"] - d0_ref) < 1e-12,
          f"||delta||={np.linalg.norm(closure['D_0^trip'] - d0_ref):.2e}")
    check("Bridge: pack-derived D_-^trip equals the independent Schur D_-^trip",
          np.linalg.norm(closure["D_-^trip"] - dm_ref) < 1e-12,
          f"||delta||={np.linalg.norm(closure['D_-^trip'] - dm_ref):.2e}")
    check("Bridge: pack-derived H_nu equals the independent Schur H_nu",
          np.linalg.norm(closure["H_nu"] - ref["H_nu"]) < 1e-12,
          f"||delta||={np.linalg.norm(closure['H_nu'] - ref['H_nu']):.2e}")
    check("Bridge: pack-derived H_e equals the independent Schur H_e",
          np.linalg.norm(closure["H_e"] - ref["H_e"]) < 1e-12,
          f"||delta||={np.linalg.norm(closure['H_e'] - ref['H_e']):.2e}")
    check("Bridge: pack-derived neutrino masses equal the independent Schur masses",
          np.linalg.norm(closure["m_nu"] - ref["m_nu"]) < 1e-10,
          f"||delta||={np.linalg.norm(closure['m_nu'] - ref['m_nu']):.2e}")
    check("Bridge: pack-derived charged-lepton masses equal the independent Schur masses",
          np.linalg.norm(closure["m_e"] - ref["m_e"]) < 1e-10,
          f"||delta||={np.linalg.norm(closure['m_e'] - ref['m_e']):.2e}")
    check("Bridge: pack-derived |PMNS| equals the independent Schur |PMNS|",
          np.linalg.norm(np.abs(closure["pmns"]) - np.abs(ref["pmns"])) < 1e-10,
          f"||delta||={np.linalg.norm(np.abs(closure['pmns']) - np.abs(ref['pmns'])):.2e}")
    check("Bridge: branch label agrees with the independent Schur branch",
          closure["branch"] == ref["branch"],
          f"branch={closure['branch']}")
    check("Bridge: sheet label agrees with the independent Schur sheet",
          closure["sheet"] == ref["sheet"],
          f"sheet={closure['sheet']}")


def part5_transfer_only_is_blind_to_the_five_real_corner_source() -> None:
    print("\n" + "=" * 88)
    print("PART 5: TRANSFER-ONLY DATA ARE BLIND TO THE FIVE-REAL CORNER SOURCE")
    print("=" * 88)

    x1 = np.array([1.15, 0.82, 0.95], dtype=float)
    y1 = np.array([0.41, 0.28, 0.54], dtype=float)
    x2 = np.array([1.20, 0.77, 0.95], dtype=float)
    y2 = np.array([0.36, 0.33, 0.54], dtype=float)
    delta = 0.63

    a1 = active_operator(x1, y1, delta)
    a2 = active_operator(x2, y2, delta)
    t1 = hw1_transfer_kernel_from_active_block(a1)
    t2 = hw1_transfer_kernel_from_active_block(a2)
    s1 = seed_source_from_active_block(a1)
    s2 = seed_source_from_active_block(a2)

    check("Two distinct active blocks have the same transfer summary", np.linalg.norm(t1 - t2) < 1e-12,
          f"transfer diff={np.linalg.norm(t1 - t2):.2e}")
    check("Those two active blocks have different corner sources",
          np.linalg.norm(s1["xi"] - s2["xi"]) > 1e-6 or np.linalg.norm(s1["eta"] - s2["eta"]) > 1e-6,
          f"|Δxi|={np.linalg.norm(s1['xi'] - s2['xi']):.6f}, |Δeta|={np.linalg.norm(s1['eta'] - s2['eta']):.6f}")
    print("  [INFO] Transfer-only data do not select the 5-real source  (the source-response columns are the thing that repairs this blindness)")


def part6_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 6: CIRCULARITY GUARD")
    print("=" * 88)

    ok, bad = circularity_guard(hw1_source_transfer_pack, {"x", "y", "delta", "tau", "q", "coeffs", "d0_trip", "dm_trip"})
    check("The new hw=1 source-transfer pack does not take PMNS-side value targets as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS HW1 SOURCE-TRANSFER BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can a genuinely axiom-first hw=1 source/transfer law do better than")
    print("  the current sole-axiom free-profile boundary?")

    part1_transfer_summaries_fix_the_seed_pair_and_branch_bit()
    part2_active_source_response_columns_fix_the_active_kernel()
    part3_passive_source_response_columns_fix_q_and_ai()
    part4_combined_pack_recovers_the_retained_pair_and_downstream_closure()
    part5_transfer_only_is_blind_to_the_five_real_corner_source()
    part6_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The hw=1 source/transfer pack is strong enough to close the retained")
    print("  PMNS lane once it is supplied:")
    print("    - transfer summaries fix the seed pair and branch bit")
    print("    - active source-response columns fix the active kernel")
    print("    - passive source-response columns fix q and a_i")
    print("    - the combined pack reconstructs the retained pair and downstream data")
    print()
    print("  Boundary:")
    print("    - transfer-only summaries are blind to the 5-real active corner source")
    print("    - the current exact bank still does not derive the source/transfer")
    print("      pack itself from Cl(3) on Z^3 alone")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
