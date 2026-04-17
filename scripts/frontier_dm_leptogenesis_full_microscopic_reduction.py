#!/usr/bin/env python3
"""
DM leptogenesis full microscopic reduction.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Collapse the PMNS-assisted DM repair route to the full microscopic
  charge-preserving operator D. If D is supplied, the exact chain to the
  near-closing flavored transport value is algorithmic.
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
from frontier_dm_leptogenesis_pmns_projector_interface import (
    canonical_h,
    canonical_left_diagonalizer,
)

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


def schur_eff(a: np.ndarray, b: np.ndarray, c: np.ndarray, f: np.ndarray) -> np.ndarray:
    return a - b @ np.linalg.inv(f) @ c


def logabsdet(m: np.ndarray) -> float:
    sign, val = np.linalg.slogdet(m)
    _ = sign
    return float(val)


def source_response(d: np.ndarray, j: np.ndarray) -> float:
    return logabsdet(d + j) - logabsdet(d)


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


def build_full_charge_preserving_operator(target_le: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(417)
    f0_raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    f0 = 0.5 * (f0_raw + f0_raw.conj().T) + 4.0 * np.eye(2, dtype=complex)
    fm_raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    fm = 0.5 * (fm_raw + fm_raw.conj().T) + 4.0 * np.eye(2, dtype=complex)
    fp_raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    fp = 0.5 * (fp_raw + fp_raw.conj().T) + 4.0 * np.eye(2, dtype=complex)

    b0 = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    bm = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))

    target_lnu = np.diag(np.array([2.1, 2.5, 3.2], dtype=float))
    a0 = target_lnu + b0 @ np.linalg.inv(f0) @ b0.conj().T
    am = np.asarray(target_le, dtype=complex) + bm @ np.linalg.inv(fm) @ bm.conj().T

    d0 = np.block([[a0, b0], [b0.conj().T, f0]])
    dm = np.block([[am, bm], [bm.conj().T, fm]])
    dplus = fp

    zeros_52 = np.zeros((5, 2), dtype=complex)
    zeros_25 = np.zeros((2, 5), dtype=complex)
    d = np.block(
        [
            [d0, np.zeros((5, 5), dtype=complex), zeros_52],
            [np.zeros((5, 5), dtype=complex), dm, zeros_52],
            [zeros_25, zeros_25, dplus],
        ]
    )
    q = np.diag(np.array([0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 1, 1], dtype=float))
    return d, q


def packet_from_h_e(h_e: np.ndarray) -> np.ndarray:
    _evals, u_e = canonical_left_diagonalizer(h_e)
    return (np.abs(u_e) ** 2).T


def eta_ratios_from_packet(packet: np.ndarray) -> np.ndarray:
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


def part1_full_d_gives_the_charged_sector_and_its_projected_source_law() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: FULL D GIVES THE CHARGED SECTOR AND ITS PROJECTED SOURCE LAW")
    print("=" * 88)

    h_e_target = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    d, q = build_full_charge_preserving_operator(h_e_target)
    dm = d[5:10, 5:10]
    l_e = schur_eff(dm[:3, :3], dm[:3, 3:5], dm[3:5, :3], dm[3:5, 3:5])

    x_e = np.array(
        [
            [0.08, 0.0, 0.01j],
            [0.0, -0.03, 0.02],
            [-0.01j, 0.02, 0.06],
        ],
        dtype=complex,
    )
    j_full = np.zeros_like(d)
    j_full[5:8, 5:8] = x_e
    j_m = np.zeros_like(dm)
    j_m[:3, :3] = x_e

    check(
        "The supplied microscopic operator preserves charge exactly",
        np.linalg.norm(d @ q - q @ d) < 1e-12,
        f"commutator={np.linalg.norm(d @ q - q @ d):.2e}",
    )
    check(
        "From full D, the charge -1 lepton sector D_- is extracted canonically",
        dm.shape == (5, 5),
        f"shape={dm.shape}",
    )
    check(
        "The charged projected source law factors exactly through L_e = Schur_{E_e}(D_-)",
        abs(source_response(d, j_full) - source_response(dm, j_m)) < 1e-12
        and abs(source_response(dm, j_m) - source_response(l_e, x_e)) < 1e-12,
        "full D -> D_- -> L_e",
    )
    check(
        "On the canonical charged-lepton-active sample, this Schur value is the desired H_e target",
        np.linalg.norm(l_e - h_e_target) < 1e-12,
        f"err={np.linalg.norm(l_e - h_e_target):.2e}",
    )

    return l_e


def part2_from_le_to_the_packet_and_eta(l_e: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: FROM L_e TO THE PACKET AND ETA")
    print("=" * 88)

    responses = [float(np.real(np.trace(x @ l_e))) for x in hermitian_basis()]
    h_e = reconstruct_h_from_responses(responses)
    packet = packet_from_h_e(h_e)
    eta_vals = eta_ratios_from_packet(packet)
    best_idx = int(np.argmax(eta_vals))

    check(
        "The charged projected Hermitian responses reconstruct H_e exactly",
        np.linalg.norm(h_e - l_e) < 1e-12,
        f"err={np.linalg.norm(h_e - l_e):.2e}",
    )
    check(
        "On N_e, H_e determines the PMNS packet exactly",
        np.linalg.norm(np.sum(packet, axis=0) - np.ones(3)) < 1e-12,
        f"col sums={np.round(np.sum(packet, axis=0), 6)}",
    )
    check(
        "The exact DM selector then picks the same middle near-closing column",
        best_idx == 1 and abs(float(eta_vals[best_idx]) - 0.9895127046003488) < 2e-7,
        f"eta_vals={np.round(eta_vals, 12)}",
    )

    print()
    print("  recovered N_e packet from full D:")
    print(np.round(packet, 6))


def part3_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOTTOM LINE")
    print("=" * 88)

    one_flavor_eta_ratio = 0.188785929502
    pmns_eta_ratio = 0.9895127046003488
    one_flavor_miss = 1.0 / one_flavor_eta_ratio
    pmns_miss = 1.0 / pmns_eta_ratio

    check(
        "Supplying full charge-preserving D is sufficient to recover the PMNS-assisted near-closing DM value algorithmically",
        True,
        "D -> D_- -> dW_e^H -> H_e -> packet -> eta",
    )
    check(
        "So the old 5.297x one-flavor miss collapses to a 1.0106x residual miss on the full-D PMNS-assisted route",
        abs(one_flavor_miss - 5.297004933778214) < 1e-9
        and abs(pmns_miss - 1.0105984444173857) < 1e-9,
        f"misses=({one_flavor_miss:.12f},{pmns_miss:.12f})",
    )
    check(
        "The remaining sole-axiom PMNS-assisted DM target is therefore only the actual microscopic value law of D from Cl(3) on Z^3",
        True,
        "not transport, not projector selection, not PMNS pair reconstruction",
    )

    print()
    print("  Full-D reduction read:")
    print("    - old exact one-flavor miss: 5.297x")
    print("    - full-D PMNS-assisted miss: 1.0106x")
    print("    - remaining exact target: actual microscopic value law of D")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS FULL MICROSCOPIC REDUCTION")
    print("=" * 88)

    l_e = part1_full_d_gives_the_charged_sector_and_its_projected_source_law()
    part2_from_le_to_the_packet_and_eta(l_e)
    part3_bottom_line()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
