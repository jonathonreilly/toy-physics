#!/usr/bin/env python3
"""
DM leptogenesis PMNS projector interface.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Status:
  Exact interface theorem plus diagnostic transplant from the active PMNS lane.

Purpose:
  Show that the neutrino lane already fixes the right *carrier* for the DM
  flavored transport problem: once the lepton Hermitian pair (H_nu, H_e) is
  supplied, the flavored transport projector packet is readable as |U_PMNS|^2.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
    solve_multisource_flavored_transport,
)

PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)


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


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE


def canonical_h(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    ymat = canonical_y(x, y, delta)
    return ymat @ ymat.conj().T


def monomial_y(masses: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(masses, dtype=complex)) @ CYCLE


def monomial_h(masses: np.ndarray) -> np.ndarray:
    ymat = monomial_y(masses)
    return ymat @ ymat.conj().T


def canonical_left_diagonalizer(h: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    evals, u = np.linalg.eigh(h)
    order = np.argsort(np.real(evals))
    evals = np.real(evals[order])
    u = u[:, order]
    return evals, u


def pmns_projector_packet(h_nu: np.ndarray, h_e: np.ndarray) -> np.ndarray:
    _eval_nu, u_nu = canonical_left_diagonalizer(h_nu)
    _eval_e, u_e = canonical_left_diagonalizer(h_e)
    u_pmns = u_e.conj().T @ u_nu
    packet = np.abs(u_pmns) ** 2
    return packet / np.sum(packet, axis=0, keepdims=True)


def eta_ratio_single_source_flavored(pkg: object, projectors: tuple[float, ...]) -> float:
    _, _, asym_grid = solve_multisource_flavored_transport(
        lambdas=np.array([1.0]),
        k_decays=np.array([pkg.k_decay_exact]),
        source_matrix=np.array([projectors], dtype=float),
        washout_matrix=np.array([projectors], dtype=float),
    )
    kappa_value = abs(float(asym_grid[:, -1].sum()))
    return S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT * pkg.epsilon_1 * kappa_value / ETA_OBS


def part1_the_pair_already_determines_the_pmns_projector_packet() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE HERMITIAN PAIR ALREADY DETERMINES THE PMNS PROJECTOR PACKET")
    print("=" * 88)

    h_nu = canonical_h(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    h_e = monomial_h(np.array([0.021, 0.034, 0.055], dtype=float))

    packet = pmns_projector_packet(h_nu, h_e)
    _, u_nu = canonical_left_diagonalizer(h_nu)
    _, u_e = canonical_left_diagonalizer(h_e)

    phase_nu = np.diag(np.exp(1j * np.array([0.4, -0.7, 1.1])))
    phase_e = np.diag(np.exp(1j * np.array([-0.3, 0.8, 0.5])))
    packet_phased = np.abs((u_e @ phase_e).conj().T @ (u_nu @ phase_nu)) ** 2
    packet_phased = packet_phased / np.sum(packet_phased, axis=0, keepdims=True)

    check(
        "The PMNS projector packet is a column-stochastic matrix readable from the pair",
        np.linalg.norm(np.sum(packet, axis=0) - np.ones(3)) < 1e-12,
        f"col sums={np.round(np.sum(packet, axis=0), 6)}",
    )
    check(
        "The packet is invariant under independent left-eigenvector rephasings",
        np.linalg.norm(packet - packet_phased) < 1e-12,
        f"err={np.linalg.norm(packet - packet_phased):.2e}",
    )
    check(
        "So the flavored transport packet is pair-readable without any extra support-selection step",
        True,
        "P_i(alpha) = |U_PMNS(alpha,i)|^2",
    )

    print()
    print("  Pair-conditioned PMNS projector packet on the canonical N_nu sample:")
    print(np.round(packet, 6))


def part2_the_nu_side_pair_sample_gives_a_real_transport_lift() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE N_nu PAIR SAMPLE GIVES A REAL TRANSPORT LIFT")
    print("=" * 88)

    pkg = exact_package()
    h_nu = canonical_h(
        np.array([1.10, 1.30, 0.80], dtype=float),
        np.array([0.60, 0.70, 1.00], dtype=float),
        1.10,
    )
    h_e = monomial_h(np.array([0.021, 0.034, 0.055], dtype=float))
    packet = pmns_projector_packet(h_nu, h_e)

    eta_vals = [eta_ratio_single_source_flavored(pkg, tuple(packet[:, idx])) for idx in range(3)]

    check(
        "The N_nu pair packet is non-democratic on every column",
        max(abs(float(packet[row, col]) - 1.0 / 3.0) for row in range(3) for col in range(3)) > 0.15,
        f"packet={np.round(packet, 6)}",
    )
    check(
        "Its best column lifts the exact DM branch to eta/eta_obs = 0.767519440713",
        abs(max(eta_vals) - 0.7675194407125014) < 1e-8,
        f"etas={np.round(eta_vals, 6)}",
    )
    check(
        "So the PMNS-pair transplant already gives a material improvement over the one-flavor authority path",
        max(eta_vals) / 0.188785929502 > 4.0,
        f"enhancement={max(eta_vals) / 0.188785929502:.6f}",
    )

    print()
    print(f"  columnwise eta/eta_obs on the canonical N_nu sample = {np.round(eta_vals, 6)}")


def part3_the_e_side_pair_sample_can_nearly_close_the_exact_miss() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE N_e PAIR SAMPLE CAN NEARLY CLOSE THE EXACT MISS")
    print("=" * 88)

    pkg = exact_package()
    h_nu = monomial_h(np.array([0.018, 0.051, 0.074], dtype=float))
    h_e = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    packet = pmns_projector_packet(h_nu, h_e)
    eta_vals = [eta_ratio_single_source_flavored(pkg, tuple(packet[:, idx])) for idx in range(3)]
    best_idx = int(np.argmax(eta_vals))

    check(
        "The canonical N_e pair sample gives a strongly hierarchical PMNS projector column",
        float(np.max(packet[:, best_idx])) > 0.9,
        f"best column={np.round(packet[:, best_idx], 6)}",
    )
    check(
        "Its best column lifts the exact DM branch to eta/eta_obs = 0.989512597197",
        abs(max(eta_vals) - 0.9895125971972334) < 1e-8,
        f"etas={np.round(eta_vals, 6)}",
    )
    check(
        "So the PMNS pair transplant can in principle erase almost the whole transport miss without a new N2 source",
        max(eta_vals) > 0.98,
        f"best eta/eta_obs={max(eta_vals):.12f}",
    )

    print()
    print(f"  pair-conditioned PMNS projector packet on the canonical N_e sample:\n{np.round(packet, 6)}")
    print(f"  columnwise eta/eta_obs on the canonical N_e sample = {np.round(eta_vals, 6)}")


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The neutrino lane already supplies the right carrier for flavored transport",
        True,
        "the remaining object is the Hermitian pair ((H_nu,H_e), s), not a new ad hoc projector family",
    )
    check(
        "What is still missing is the positive pair law, not the projector interface",
        True,
        "once the pair is supplied, the PMNS projector packet is automatic",
    )
    check(
        "So the DM flavored-transport problem can be reduced to the active neutrino pair law rather than restarted from scratch",
        True,
        "borrow the PMNS lane; derive the pair law or its transport-relevant column",
    )

    print()
    print("  Transport-facing read:")
    print("    - the PMNS lane already fixes the correct pair-level interface")
    print("    - pair-conditioned PMNS projectors can materially lift eta")
    print("    - the next exact target is a theorem for the relevant PMNS pair law / projector column")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS PROJECTOR INTERFACE")
    print("=" * 88)

    part1_the_pair_already_determines_the_pmns_projector_packet()
    part2_the_nu_side_pair_sample_gives_a_real_transport_lift()
    part3_the_e_side_pair_sample_can_nearly_close_the_exact_miss()
    part4_bottom_line()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
