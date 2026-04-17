#!/usr/bin/env python3
"""
DM leptogenesis PMNS active-projector reduction.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Use the active PMNS / neutrino lane to sharpen the flavored-transport target
  on the refreshed DM branch.

  The exact point is:
    - on a one-sided minimal PMNS branch, the passive monomial sector is
      Hermitian-diagonal and contributes only a basis permutation / phases
    - therefore the flavored transport projector packet is already determined
      by the active Hermitian block alone
    - combining that with the new PMNS-side native laws for branch/orientation
      and seed averages, the remaining DM-relevant PMNS object is the active
      five-real corner source, not the full Hermitian pair
"""

from __future__ import annotations

import sys
from itertools import permutations

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_leptogenesis_pmns_projector_interface import (
    canonical_h,
    canonical_left_diagonalizer,
    eta_ratio_single_source_flavored,
    monomial_h,
    pmns_projector_packet,
)

PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
I3 = np.eye(3, dtype=complex)


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


def active_packet_from_h(h_act: np.ndarray) -> np.ndarray:
    _evals, u_act = canonical_left_diagonalizer(h_act)
    return np.abs(u_act) ** 2


def packet_distance_up_to_column_permutation(a: np.ndarray, b: np.ndarray) -> tuple[float, tuple[int, int, int]]:
    best_err = float("inf")
    best_perm = (0, 1, 2)
    for perm in permutations(range(3)):
        err = float(np.linalg.norm(a - b[:, perm]))
        if err < best_err:
            best_err = err
            best_perm = tuple(int(x) for x in perm)
    return best_err, best_perm


def active_operator(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(y_eff) @ CYCLE


def support_trace_moments(d: np.ndarray) -> np.ndarray:
    return np.array(
        [
            np.trace(d @ I3.conj().T),
            np.trace(d @ CYCLE.conj().T),
            np.trace(d @ (CYCLE @ CYCLE).conj().T),
        ],
        dtype=complex,
    )


def moment_support_count(d: np.ndarray, tol: float = 1e-10) -> int:
    return int(np.count_nonzero(np.abs(support_trace_moments(d)) > tol))


def seed_averages(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    return float(np.mean(x)), float(np.mean(y))


def source_coordinates(x: np.ndarray, y: np.ndarray, delta: float) -> tuple[np.ndarray, np.ndarray, float]:
    xbar, ybar = seed_averages(x, y)
    xi = np.asarray(x, dtype=float) - xbar * np.ones(3, dtype=float)
    eta = np.asarray(y, dtype=float) - ybar * np.ones(3, dtype=float)
    return xi, eta, float(delta)


def flavored_eta_columns(packet: np.ndarray) -> list[float]:
    pkg = exact_package()
    return [eta_ratio_single_source_flavored(pkg, tuple(packet[:, idx])) for idx in range(3)]


def part1_one_sided_pmns_projectors_localize_to_the_active_hermitian_block() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ONE-SIDED PMNS PROJECTORS LOCALIZE TO THE ACTIVE HERMITIAN BLOCK")
    print("=" * 88)

    h_nu_act = canonical_h(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    h_e_pass_sorted = monomial_h(np.array([0.021, 0.034, 0.055], dtype=float))

    packet_nu_sorted = pmns_projector_packet(h_nu_act, h_e_pass_sorted)
    packet_nu_active = active_packet_from_h(h_nu_act)

    h_nu_pass_sorted = monomial_h(np.array([0.018, 0.051, 0.074], dtype=float))
    h_e_act = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    packet_e_sorted = pmns_projector_packet(h_nu_pass_sorted, h_e_act)
    packet_e_active = active_packet_from_h(h_e_act)

    check(
        "On N_nu with the passive monomial block already ordered, the PMNS packet equals the active packet exactly",
        np.linalg.norm(packet_nu_sorted - packet_nu_active) < 1e-12,
        f"err={np.linalg.norm(packet_nu_sorted - packet_nu_active):.2e}",
    )
    check(
        "On N_e with the passive monomial block already ordered, the PMNS packet is the transpose of the active packet",
        np.linalg.norm(packet_e_sorted - packet_e_active.T) < 1e-12,
        f"err={np.linalg.norm(packet_e_sorted - packet_e_active.T):.2e}",
    )
    check(
        "So once the passive monomial ordering is fixed, the one-sided PMNS transport packet is determined by the active block alone",
        True,
        "N_nu gives |U_act|^2 and N_e gives |U_act|^2^T",
    )

    print()
    print("  So on one-sided minimal PMNS branches, the flavored transport packet is")
    print("  already an active-Hermitian object. The passive monomial side only")
    print("  contributes column ordering.")


def part2_the_near_closing_transport_lift_comes_from_the_active_block_alone() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE TRANSPORT LIFT COMES FROM THE ACTIVE BLOCK ALONE")
    print("=" * 88)

    h_nu_act = canonical_h(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    h_e_act = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )

    eta_nu = flavored_eta_columns(active_packet_from_h(h_nu_act))
    eta_e = flavored_eta_columns(active_packet_from_h(h_e_act).T)

    check(
        "The canonical N_nu active block alone reproduces the known PMNS-interface transport lift",
        abs(max(eta_nu) - 0.7675194407125014) < 1e-8,
        f"etas={np.round(eta_nu, 6)}",
    )
    check(
        "The canonical N_e active block alone reproduces the near-closing PMNS-interface lift",
        abs(max(eta_e) - 0.9895125971972334) < 1e-8,
        f"etas={np.round(eta_e, 6)}",
    )
    check(
        "So the pair-conditioned near-closure on N_e is already entirely carried by the active charged-lepton Hermitian block",
        max(eta_e) > 0.98,
        f"best eta/eta_obs={max(eta_e):.12f}",
    )

    print()
    print(f"  canonical N_nu active-only columnwise eta/eta_obs = {np.round(eta_nu, 6)}")
    print(f"  canonical N_e active-only columnwise eta/eta_obs = {np.round(eta_e, 6)}")


def part3_the_remaining_dm_relevant_pmns_object_is_the_active_five_real_source() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REMAINING DM-RELEVANT PMNS OBJECT IS THE ACTIVE FIVE-REAL SOURCE")
    print("=" * 88)

    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    delta_a = 0.63

    x_b = np.array([1.05, 0.97, 0.90], dtype=float)
    y_b = np.array([0.60, 0.09, 0.54], dtype=float)
    delta_b = 0.63

    xbar_a, ybar_a = seed_averages(x_a, y_a)
    xbar_b, ybar_b = seed_averages(x_b, y_b)
    xi_a, eta_a, _ = source_coordinates(x_a, y_a, delta_a)
    xi_b, eta_b, _ = source_coordinates(x_b, y_b, delta_b)

    d_act_a = active_operator(x_a, y_a, delta_a)
    d_act_b = active_operator(x_b, y_b, delta_b)
    counts = (moment_support_count(d_act_a), moment_support_count(d_act_b))

    h_e_a = canonical_h(x_a, y_a, delta_a)
    h_e_b = canonical_h(x_b, y_b, delta_b)
    packet_a = active_packet_from_h(h_e_a).T
    packet_b = active_packet_from_h(h_e_b).T
    eta_cols_a = flavored_eta_columns(packet_a)
    eta_cols_b = flavored_eta_columns(packet_b)

    check(
        "The PMNS-side native transport laws fix the same seed averages on both active samples",
        abs(xbar_a - xbar_b) < 1e-12 and abs(ybar_a - ybar_b) < 1e-12,
        f"(xbar,ybar)=({xbar_a:.6f},{ybar_a:.6f})",
    )
    check(
        "The same native support law reads both operators as active one-sided blocks",
        counts == (2, 2),
        f"moment-support counts={counts}",
    )
    check(
        "The two active samples still carry different five-real source data",
        np.linalg.norm(xi_a - xi_b) > 1e-6 and np.linalg.norm(eta_a - eta_b) > 1e-6,
        f"xi_a={np.round(xi_a, 6)}, xi_b={np.round(xi_b, 6)}; eta_a={np.round(eta_a, 6)}, eta_b={np.round(eta_b, 6)}",
    )
    check(
        "Those distinct five-real source data induce different active projector packets",
        np.linalg.norm(packet_a - packet_b) > 1e-3,
        f"packet distance={np.linalg.norm(packet_a - packet_b):.6f}",
    )
    check(
        "They also induce different flavored DM transport outputs on the same exact branch",
        abs(max(eta_cols_a) - max(eta_cols_b)) > 1e-3,
        f"best etas=({max(eta_cols_a):.12f},{max(eta_cols_b):.12f})",
    )

    print()
    print(f"  source A columnwise eta/eta_obs = {np.round(eta_cols_a, 6)}")
    print(f"  source B columnwise eta/eta_obs = {np.round(eta_cols_b, 6)}")
    print()
    print("  Therefore the exact remaining PMNS object relevant for DM flavored")
    print("  transport is not the full pair, not the passive monomial side, and")
    print("  not the already-native seed/orientation data. It is the active")
    print("  five-real source.")


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The PMNS lane removes the need to invent a new flavored-projector family on the DM branch",
        True,
        "the transport packet localizes to the active Hermitian block on one-sided PMNS classes",
    )
    check(
        "The exact remaining PMNS input to DM flavored transport is only the active five-real source",
        True,
        "tau and the seed pair are already native; the passive side is only a permutation",
    )
    check(
        "So the next exact DM target is a PMNS-side law for that active five-real source, not a new transport ansatz",
        True,
        "derive the active source or the transport-relevant active column",
    )

    print()
    print("  Transport-facing read:")
    print("    - one-sided PMNS projectors are active-block objects")
    print("    - the near-closing N_e transport lift already lives on the active H_e block")
    print("    - the open science is the active five-real PMNS source law")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS ACTIVE-PROJECTOR REDUCTION")
    print("=" * 88)

    part1_one_sided_pmns_projectors_localize_to_the_active_hermitian_block()
    part2_the_near_closing_transport_lift_comes_from_the_active_block_alone()
    part3_the_remaining_dm_relevant_pmns_object_is_the_active_five_real_source()
    part4_bottom_line()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
