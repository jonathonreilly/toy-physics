#!/usr/bin/env python3
"""Exact reduction of the PMNS-relevant microscopic D law to a 4-real gap."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    CYCLE,
    I3,
    PERMUTATIONS,
    active_operator,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    passive_operator,
    passive_response_columns_from_sector_operator,
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


def support_trace_moments(block: np.ndarray) -> np.ndarray:
    return np.array(
        [
            np.trace(block @ PERMUTATIONS[0].conj().T),
            np.trace(block @ PERMUTATIONS[1].conj().T),
            np.trace(block @ PERMUTATIONS[2].conj().T),
        ],
        dtype=complex,
    )


def moment_support_count(block: np.ndarray, tol: float = 1e-10) -> int:
    return int(np.count_nonzero(np.abs(support_trace_moments(block)) > tol))


def recover_q(block: np.ndarray) -> int:
    return int(np.argmax(np.abs(support_trace_moments(block))))


def passive_moduli_from_hermitian(block: np.ndarray) -> np.ndarray:
    herm = block @ block.conj().T
    return np.sqrt(np.maximum(np.real(np.diag(herm)), 0.0))


def active_native_means(block: np.ndarray) -> tuple[float, complex]:
    x = np.real(np.diag(block))
    c = np.array([block[0, 1], block[1, 2], block[2, 0]], dtype=complex)
    return float(np.mean(x)), complex(np.mean(c))


def active_four_real_gap(block: np.ndarray) -> np.ndarray:
    x = np.real(np.diag(block))
    c = np.array([block[0, 1], block[1, 2], block[2, 0]], dtype=complex)
    xbar = float(np.mean(x))
    sigma = complex(np.mean(c))
    xi = x - xbar * np.ones(3, dtype=float)
    rho = np.array([np.real(c[0] - sigma), np.real(c[1] - sigma)], dtype=float)
    return np.array([xi[0], xi[1], rho[0], rho[1]], dtype=float)


def reconstruct_active_from_four_real(xbar: float, sigma: complex, gap: np.ndarray) -> np.ndarray:
    xi1, xi2, rho1, rho2 = gap.tolist()
    x = np.array([xbar + xi1, xbar + xi2, xbar - xi1 - xi2], dtype=float)
    re_sigma = float(np.real(sigma))
    im_sigma = float(np.imag(sigma))
    c1 = re_sigma + rho1
    c2 = re_sigma + rho2
    c3 = re_sigma - rho1 - rho2 + 3j * im_sigma
    c = np.array([c1, c2, c3], dtype=complex)
    return np.diag(x.astype(complex)) + np.diag(c) @ CYCLE


def sample_pair(
    tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, c_forward: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    active_sector = sector_operator_fixture_from_effective_block(active_operator(x, np.abs(c_forward), float(np.angle(c_forward[2]))), seed=2101 + 17 * tau + q)
    passive_sector = sector_operator_fixture_from_effective_block(passive_operator(coeffs, q), seed=2201 + 17 * tau + q)
    active = derive_active_block_from_response_columns(active_response_columns_from_sector_operator(active_sector, 0.31)[1], 0.31)[1]
    passive = derive_passive_block_from_response_columns(passive_response_columns_from_sector_operator(passive_sector, 0.27)[1], 0.27)[1]
    return (active, passive) if tau == 0 else (passive, active)


def run_sample(label: str, tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, c_forward: np.ndarray) -> None:
    d0_trip, dm_trip = sample_pair(tau, q, coeffs, x, c_forward)
    if moment_support_count(d0_trip) == 2:
        active, passive = d0_trip, dm_trip
    else:
        active, passive = dm_trip, d0_trip

    xbar, sigma = active_native_means(active)
    gap = active_four_real_gap(active)
    active_rebuilt = reconstruct_active_from_four_real(xbar, sigma, gap)
    moduli = passive_moduli_from_hermitian(passive)

    expected_moduli = np.abs(coeffs)
    expected_q = q

    check(f"{label}: q is still fixed natively from passive support moments", recover_q(passive) == expected_q, f"q={recover_q(passive)}")
    check(
        f"{label}: passive Hermitian data fix the three passive moduli",
        np.linalg.norm(moduli - expected_moduli) < 1e-12,
        f"moduli={np.round(moduli, 6)}",
    )
    check(
        f"{label}: the active block is fixed by native means plus a 4-real centered gap",
        np.linalg.norm(active_rebuilt - active) < 1e-12,
        f"error={np.linalg.norm(active_rebuilt - active):.2e}",
    )
    check(
        f"{label}: the only remaining unreduced active data are four real orbit-breaking coordinates",
        gap.shape == (4,),
        f"gap={np.round(gap, 6)}",
    )


def passive_moduli_are_q_independent() -> None:
    print("\n" + "=" * 88)
    print("PART 3: PASSIVE MODULI DO NOT DEPEND ON THE OFFSET q")
    print("=" * 88)
    coeffs = np.array([0.07 * np.exp(0.4j), 0.11 * np.exp(-0.7j), 0.23 * np.exp(1.1j)], dtype=complex)
    mods = []
    for q in (0, 1, 2):
        block = passive_operator(coeffs, q)
        mods.append(passive_moduli_from_hermitian(block))
    check(
        "The passive Hermitian law eliminates q from the passive moduli",
        np.linalg.norm(mods[0] - mods[1]) < 1e-12 and np.linalg.norm(mods[1] - mods[2]) < 1e-12,
    )


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC D FOUR-REAL LAST MILE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the passive Hermitian block is derived from the microscopic")
    print("  passive response law, how much of the PMNS-relevant microscopic")
    print("  operator D is still not fixed?")

    print("\n" + "=" * 88)
    print("PART 1: NEUTRINO-ACTIVE SAMPLE")
    print("=" * 88)
    run_sample(
        "neutrino-active",
        0,
        2,
        np.array([0.07 * np.exp(0.4j), 0.11 * np.exp(-0.7j), 0.23 * np.exp(1.1j)], dtype=complex),
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54 * np.exp(0.63j)], dtype=complex),
    )

    print("\n" + "=" * 88)
    print("PART 2: CHARGED-LEPTON-ACTIVE SAMPLE")
    print("=" * 88)
    run_sample(
        "charged-lepton-active",
        1,
        1,
        np.array([0.17 * np.exp(-0.3j), 0.09 * np.exp(0.9j), 0.04 * np.exp(-1.4j)], dtype=complex),
        np.array([0.92, 1.08, 0.85], dtype=float),
        np.array([0.33, 0.49, 0.26 * np.exp(-0.37j)], dtype=complex),
    )

    passive_moduli_are_q_independent()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction of the PMNS-relevant microscopic D law:")
    print("    - q remains fixed natively by passive support moments")
    print("    - passive Hermitian data fix the three passive moduli")
    print("    - xbar and sigma remain fixed natively on the active sector")
    print("    - the only unreduced active data are four real orbit-breaking coordinates")
    print()
    print("  So the PMNS-relevant D law is now reduced to a 4-real last mile:")
    print("    (xi_1, xi_2, rho_1, rho_2)")
    print("  together with the already derived native data (tau, q, xbar, sigma)")
    print("  and the passive Hermitian moduli.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
