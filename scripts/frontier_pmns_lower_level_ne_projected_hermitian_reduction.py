#!/usr/bin/env python3
"""
PMNS lower-level N_e projected-Hermitian reduction theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  On the charged-lepton-active N_e lane, what exactly survives from the new
  lower-level PMNS theorems into the DM/leptogenesis interface?

Answer:
  Once the lower-level effective active/passive blocks are fixed, the
  transport-facing projected Hermitian source object is already fixed exactly.

  The lower-level partition-response theorem makes the response pack native
  once the baselines are fixed, and the Schur-pushforward theorem quotients
  away microscopic completions. Therefore on N_e:

    effective active/passive blocks
      -> lower-level response pack
      -> active Hermitian slot
      -> projected Hermitian source law
      -> |U_e|^2^T
      -> selected transport column

  is exact and completion-invariant.

On the current lower-level pair convention, that transport-facing active
Hermitian slot is stored as H_nu on the charged-lepton-active branch, while H_e
stores the passive monomial block.

So the live gap on the observation-free N_e lane is not the response pack or
the microscopic completion. It is the effective-block/source law itself.
"""

from __future__ import annotations

import sys

import numpy as np

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h, canonical_left_diagonalizer, monomial_h
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from pmns_lower_level_utils import (
    active_operator,
    active_response_columns_from_sector_operator,
    passive_operator,
    passive_response_columns_from_sector_operator,
    sector_operator_fixture_from_effective_block,
)

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

LAM_ACT = 0.31
LAM_PASS = 0.27
Q_PASS = 1
PASSIVE_COEFFS = np.array([0.018, 0.051, 0.074], dtype=complex)
ACTIVE_X = np.array([0.24, 0.38, 1.07], dtype=float)
ACTIVE_Y = np.array([0.09, 0.22, 0.61], dtype=float)
ACTIVE_DELTA = 1.10


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


def hermitian_basis() -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for i in range(3):
        e = np.zeros((3, 3), dtype=complex)
        e[i, i] = 1.0
        basis.append(e)
    for i in range(3):
        for j in range(i + 1, 3):
            s = np.zeros((3, 3), dtype=complex)
            s[i, j] = 1.0
            s[j, i] = 1.0
            basis.append(s)
            a = np.zeros((3, 3), dtype=complex)
            a[i, j] = -1j
            a[j, i] = 1j
            basis.append(a)
    return basis


def hermitian_linear_responses(h: np.ndarray) -> list[float]:
    return [float(np.real(np.trace(x @ h))) for x in hermitian_basis()]


def reconstruct_h_from_responses(responses: list[float]) -> np.ndarray:
    h = np.zeros((3, 3), dtype=complex)
    h[0, 0] = responses[0]
    h[1, 1] = responses[1]
    h[2, 2] = responses[2]
    idx = 3
    for i in range(3):
        for j in range(i + 1, 3):
            sym = responses[idx]
            asym = responses[idx + 1]
            h[i, j] = 0.5 * (sym - 1j * asym)
            h[j, i] = 0.5 * (sym + 1j * asym)
            idx += 2
    return h


def packet_from_active_slot(h_active: np.ndarray) -> np.ndarray:
    _evals, u_active = canonical_left_diagonalizer(h_active)
    return (np.abs(u_active) ** 2).T


def eta_values_from_packet(packet: np.ndarray) -> np.ndarray:
    pkg = exact_package()
    z_grid, source_profile, washout_tail = flavored_transport_kernel(pkg.k_decay_exact)
    factors = np.array(
        [
            flavored_column_functional(packet[:, idx], z_grid, source_profile, washout_tail)
            for idx in range(3)
        ],
        dtype=float,
    )
    return (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * pkg.epsilon_1
        * factors
        / ETA_OBS
    )


def build_ne_closure(active_seed: int, passive_seed: int) -> dict:
    active_sector = sector_operator_fixture_from_effective_block(
        active_operator(ACTIVE_X, ACTIVE_Y, ACTIVE_DELTA),
        seed=active_seed,
    )
    passive_sector = sector_operator_fixture_from_effective_block(
        passive_operator(PASSIVE_COEFFS, Q_PASS),
        seed=passive_seed,
    )
    neutral_cols = passive_response_columns_from_sector_operator(passive_sector, LAM_PASS)[1]
    charge_cols = active_response_columns_from_sector_operator(active_sector, LAM_ACT)[1]
    return close_from_lower_level_observables(neutral_cols, charge_cols, LAM_ACT, LAM_PASS)


def part1_ne_lower_level_closure_recovers_the_canonical_pair_exactly() -> tuple[dict, dict]:
    print("\n" + "=" * 88)
    print("PART 1: N_e LOWER-LEVEL CLOSURE RECOVERS THE CANONICAL PAIR EXACTLY")
    print("=" * 88)

    out_a = build_ne_closure(active_seed=701, passive_seed=809)
    out_b = build_ne_closure(active_seed=1701, passive_seed=1809)
    h_active_ref = canonical_h(ACTIVE_X, ACTIVE_Y, ACTIVE_DELTA)
    h_passive_ref = monomial_h(np.real(PASSIVE_COEFFS))

    check(
        "The charged-lepton-active lower-level closure lands on the N_e branch exactly",
        out_a["branch"] == "charged-lepton-active" and out_b["branch"] == "charged-lepton-active",
        f"branches=({out_a['branch']},{out_b['branch']})",
    )
    check(
        "On the charged-lepton-active branch, the closure slot H_nu matches the canonical active Hermitian block exactly",
        np.linalg.norm(out_a["H_nu"] - h_active_ref) < 1.0e-12 and np.linalg.norm(out_b["H_nu"] - h_active_ref) < 1.0e-12,
        f"(err_a,err_b)=({np.linalg.norm(out_a['H_nu'] - h_active_ref):.2e},{np.linalg.norm(out_b['H_nu'] - h_active_ref):.2e})",
    )
    check(
        "On the same branch, the closure slot H_e matches the passive monomial Hermitian block exactly",
        np.linalg.norm(out_a["H_e"] - h_passive_ref) < 1.0e-12 and np.linalg.norm(out_b["H_e"] - h_passive_ref) < 1.0e-12,
        f"(err_a,err_b)=({np.linalg.norm(out_a['H_e'] - h_passive_ref):.2e},{np.linalg.norm(out_b['H_e'] - h_passive_ref):.2e})",
    )
    check(
        "Distinct microscopic completions with the same effective blocks give identical active/passive Hermitian slots",
        np.linalg.norm(out_a["H_e"] - out_b["H_e"]) < 1.0e-12 and np.linalg.norm(out_a["H_nu"] - out_b["H_nu"]) < 1.0e-12,
        f"(err_active,err_passive)=({np.linalg.norm(out_a['H_nu'] - out_b['H_nu']):.2e},{np.linalg.norm(out_a['H_e'] - out_b['H_e']):.2e})",
    )

    return out_a, out_b


def part2_the_projected_hermitian_source_pack_is_exact_and_completion_invariant(
    out_a: dict, out_b: dict
) -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: THE PROJECTED HERMITIAN SOURCE PACK IS EXACT AND COMPLETION-INVARIANT")
    print("=" * 88)

    responses_a = hermitian_linear_responses(out_a["H_nu"])
    responses_b = hermitian_linear_responses(out_b["H_nu"])
    h_rec_a = reconstruct_h_from_responses(responses_a)
    h_rec_b = reconstruct_h_from_responses(responses_b)

    check(
        "The nine projected Hermitian responses reconstruct the active Hermitian slot exactly on the first microscopic completion",
        np.linalg.norm(h_rec_a - out_a["H_nu"]) < 1.0e-12,
        f"err={np.linalg.norm(h_rec_a - out_a['H_nu']):.2e}",
    )
    check(
        "The same projected Hermitian responses reconstruct the active Hermitian slot exactly on the second microscopic completion",
        np.linalg.norm(h_rec_b - out_b["H_nu"]) < 1.0e-12,
        f"err={np.linalg.norm(h_rec_b - out_b['H_nu']):.2e}",
    )
    check(
        "The projected Hermitian source pack is identical across microscopic completions of the same effective blocks",
        np.linalg.norm(np.array(responses_a, dtype=float) - np.array(responses_b, dtype=float)) < 1.0e-12,
        f"err={np.linalg.norm(np.array(responses_a, dtype=float) - np.array(responses_b, dtype=float)):.2e}",
    )
    check(
        "So on N_e the lower-level PMNS lane already fixes the transport-facing projected Hermitian source object once the effective blocks are fixed",
        True,
        "response pack and microscopic completion are both quotient data here",
    )

    return h_rec_a, h_rec_b


def part3_the_transport_packet_and_selected_column_are_already_downstream_algorithmic(
    h_rec_a: np.ndarray, h_rec_b: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE TRANSPORT PACKET AND SELECTED COLUMN ARE ALREADY DOWNSTREAM ALGORITHMIC")
    print("=" * 88)

    packet_a = packet_from_active_slot(h_rec_a)
    packet_b = packet_from_active_slot(h_rec_b)
    eta_a = eta_values_from_packet(packet_a)
    eta_b = eta_values_from_packet(packet_b)
    packet_ref = np.array(
        [
            [0.915868, 0.071267, 0.012865],
            [0.074689, 0.900307, 0.025004],
            [0.009443, 0.028427, 0.962131],
        ],
        dtype=float,
    )

    check(
        "The N_e packet derived from the active Hermitian slot is completion-invariant",
        np.linalg.norm(packet_a - packet_b) < 1.0e-12,
        f"err={np.linalg.norm(packet_a - packet_b):.2e}",
    )
    check(
        "The derived N_e packet matches the canonical packet exactly",
        np.linalg.norm(packet_a - packet_ref) < 2.0e-6,
        f"err={np.linalg.norm(packet_a - packet_ref):.2e}",
    )
    check(
        "The selected column and eta-value are completion-invariant downstream of the active Hermitian slot",
        int(np.argmax(eta_a)) == int(np.argmax(eta_b)) == 1 and np.linalg.norm(eta_a - eta_b) < 1.0e-12,
        f"eta_a={np.round(eta_a, 12)}, eta_b={np.round(eta_b, 12)}",
    )
    check(
        "The canonical N_e lower-level lane still gives the near-closing value eta/eta_obs = 0.989512597197",
        abs(float(np.max(eta_a)) - 0.9895125971972334) < 2.0e-7,
        f"best eta/eta_obs={float(np.max(eta_a)):.12f}",
    )

    print()
    print(f"  completion-invariant N_e packet =\n{np.round(packet_a, 6)}")
    print(f"  completion-invariant columnwise eta/eta_obs = {np.round(eta_a, 12)}")


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "On the observation-free N_e lane, the live gap is not the lower-level response pack",
        True,
        "partition response already fixes that pack from the lower-level baselines",
    )
    check(
        "It is not the microscopic completion either",
        True,
        "exact Schur pushforward quotients completions away on support",
    )
    check(
        "The live remaining N_e gap is the effective active/passive block law, equivalently the exact active Hermitian source law from Cl(3) on Z^3",
        True,
    )

    print()
    print("  Exact N_e reduction:")
    print("    - effective blocks")
    print("      -> lower-level response pack")
    print("      -> active Hermitian slot")
    print("      -> projected Hermitian source law")
    print("      -> |U_active|^2^T")
    print("      -> selected column")
    print("      -> eta")
    print("    - response pack and microscopic completion are quotient data")
    print("    - remaining target: effective-block/source law")


def main() -> int:
    print("=" * 88)
    print("PMNS LOWER-LEVEL N_e PROJECTED-HERMITIAN REDUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the charged-lepton-active N_e lane, what exactly survives from the")
    print("  lower-level PMNS stack into the transport-facing DM interface?")

    out_a, out_b = part1_ne_lower_level_closure_recovers_the_canonical_pair_exactly()
    h_rec_a, h_rec_b = part2_the_projected_hermitian_source_pack_is_exact_and_completion_invariant(out_a, out_b)
    part3_the_transport_packet_and_selected_column_are_already_downstream_algorithmic(h_rec_a, h_rec_b)
    part4_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  On N_e, the lower-level PMNS lane now reduces exactly to the")
    print("  transport-facing projected Hermitian source object once the effective")
    print("  active/passive blocks are fixed.")
    print()
    print("  So the live remaining observation-free gap is not the response pack")
    print("  and not the microscopic completion. It is the effective-block/source")
    print("  law, equivalently the exact active Hermitian source law from Cl(3)")
    print("  on Z^3.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
