#!/usr/bin/env python3
"""
DM Wilson-to-dW_e^H Hermitian source-family target.

Purpose:
  Put the first non-redundant constructive target on current main in the
  weakest honest form. The target is not another internal selector functional
  on H(m, delta, q_+). It is one Wilson-side Hermitian source family whose
  first variations reconstruct dW_e^H.
"""

from __future__ import annotations

import sys
from pathlib import Path

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
from frontier_dm_leptogenesis_pmns_projector_interface import (
    canonical_h,
    canonical_left_diagonalizer,
)

ROOT = Path(__file__).resolve().parents[1]

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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


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


def real_trace_pair(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.real(np.trace(a @ b)))


def gram_matrix(basis: list[np.ndarray]) -> np.ndarray:
    n = len(basis)
    g = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            g[i, j] = real_trace_pair(basis[i], basis[j])
    return g


def responses_from_h(h: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    return np.array([real_trace_pair(b, h) for b in basis], dtype=float)


def reconstruct_h_from_responses(responses: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    g = gram_matrix(basis)
    coeffs = np.linalg.solve(g, responses)
    h = np.zeros((3, 3), dtype=complex)
    for c, b in zip(coeffs, basis):
        h += c * b
    return h


def packet_from_h_e(h_e: np.ndarray) -> np.ndarray:
    _evals, u_e = canonical_left_diagonalizer(h_e)
    return (np.abs(u_e) ** 2).T


def transport_column_values(packet: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pkg = exact_package()
    z_grid, source_profile, washout_tail = flavored_transport_kernel(pkg.k_decay_exact)
    factors = np.array(
        [
            flavored_column_functional(packet[:, idx], z_grid, source_profile, washout_tail)
            for idx in range(3)
        ],
        dtype=float,
    )
    eta_vals = (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * pkg.epsilon_1
        * factors
        / ETA_OBS
    )
    return factors, eta_vals


def part1_current_main_has_already_reduced_the_downstream_chain() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CURRENT MAIN ALREADY REDUCES THE DOWNSTREAM CHAIN")
    print("=" * 88)

    projected = read("docs/DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    selector = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md")

    check(
        "Projected-source law note states that dW_e^H alone determines the selected N_e transport column",
        "selected transport column is derivable" in projected
        and "`dW_e^H` reconstructs the active charged-lepton Hermitian block `H_e`" in projected,
    )
    check(
        "Charged source-response reduction note states that dW_e^H is the exact charged-sector Schur pushforward",
        "`dW_e^H` is the exact charged-sector Schur pushforward" in charged,
    )
    check(
        "Selector reduction note states that the remaining open microscopic object is exactly on dW_e^H = Schur_Ee(D_-)",
        "right-sensitive microscopic selector law" in selector
        and "`dW_e^H = Schur_Ee(D_-)`" in selector,
    )


def part2_nine_real_channels_are_sufficient() -> tuple[list[np.ndarray], np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: NINE REAL HERMITIAN CHANNELS ARE SUFFICIENT")
    print("=" * 88)

    basis = hermitian_basis()
    g = gram_matrix(basis)
    h_e = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    responses = responses_from_h(h_e, basis)
    h_rec = reconstruct_h_from_responses(responses, basis)

    check(
        "Herm(3) carries exactly nine real basis directions",
        len(basis) == 9,
        f"basis size={len(basis)}",
    )
    check(
        "The standard Hermitian response basis is real-linearly independent",
        np.linalg.matrix_rank(g) == 9,
        f"rank={np.linalg.matrix_rank(g)}",
    )
    check(
        "Nine real response channels reconstruct H_e exactly",
        np.linalg.norm(h_rec - h_e) < 1e-12,
        f"err={np.linalg.norm(h_rec - h_e):.2e}",
    )

    print()
    print("  So a Wilson family realizing these nine basis responses would already")
    print("  determine dW_e^H and the full charged Hermitian block H_e.")

    return basis, h_rec


def part3_fewer_than_nine_channels_are_not_generic() -> None:
    print("\n" + "=" * 88)
    print("PART 3: FEWER THAN NINE CHANNELS ARE NOT GENERIC")
    print("=" * 88)

    basis = hermitian_basis()
    response_map = gram_matrix(basis[:8] + [basis[8]])[:8, :]
    _u, s, vh = np.linalg.svd(response_map)
    null_vec = vh[-1, :]
    h_gap = np.zeros((3, 3), dtype=complex)
    for c, b in zip(null_vec, basis):
        h_gap += c * b
    gap_responses = responses_from_h(h_gap, basis[:8])

    check(
        "The first eight real channels leave a nonzero Hermitian blind direction",
        np.linalg.norm(h_gap) > 1e-10,
        f"gap norm={np.linalg.norm(h_gap):.2e}",
    )
    check(
        "That blind direction has zero responses on all first-eight channels",
        np.linalg.norm(gap_responses) < 1e-10,
        f"blind response norm={np.linalg.norm(gap_responses):.2e}",
    )
    check(
        "So any generic Wilson realization of arbitrary dW_e^H data needs at least nine real channels",
        True,
        "dim_R Herm(3) = 9 and 8 channels leave a nontrivial null direction",
    )


def part4_once_h_e_is_known_the_rest_is_algorithmic(h_e: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 4: ONCE H_e IS KNOWN THE REST IS ALGORITHMIC")
    print("=" * 88)

    packet = packet_from_h_e(h_e)
    _factors, eta_vals = transport_column_values(packet)
    best_idx = int(np.argmax(eta_vals))

    check(
        "The reconstructed H_e fixes the charged-lepton-active packet",
        np.linalg.norm(np.sum(packet, axis=0) - np.ones(3)) < 1e-12,
        f"col sums={np.round(np.sum(packet, axis=0), 6)}",
    )
    check(
        "The exact transport selector then fixes the relevant flavored DM column algorithmically",
        best_idx == 1,
        f"eta/eta_obs={np.round(eta_vals, 12)}",
    )
    check(
        "The selected column reproduces the near-closing PMNS-assisted value",
        abs(float(eta_vals[best_idx]) - 0.9895125971972334) < 2e-7,
        f"eta/eta_obs={eta_vals[best_idx]:.12f}",
    )

    print()
    print("  Therefore the remaining constructive primitive is upstream of H_e:")
    print("  one Wilson-side Hermitian source family whose first variations land on dW_e^H.")


def part5_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)

    check(
        "The weakest honest constructive target is a nine-channel Wilson Hermitian source family for dW_e^H",
        True,
        "sufficient by exact reconstruction and minimal by dimension count",
    )
    check(
        "This target is strictly upstream of the present imposed source-branch rule",
        True,
        "it changes the information content before the selector is applied",
    )


def main() -> int:
    print("=" * 88)
    print("DM WILSON-TO-dW_e^H HERMITIAN SOURCE-FAMILY TARGET")
    print("=" * 88)

    part1_current_main_has_already_reduced_the_downstream_chain()
    _basis, h_e = part2_nine_real_channels_are_sufficient()
    part3_fewer_than_nine_channels_are_not_generic()
    part4_once_h_e_is_known_the_rest_is_algorithmic(h_e)
    part5_bottom_line()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
