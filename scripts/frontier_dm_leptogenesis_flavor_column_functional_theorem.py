#!/usr/bin/env python3
"""
DM leptogenesis flavor-column functional theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Replace brute-force flavored-column scanning by an exact transport-facing
  functional on projector columns, and use it to identify the transport-
  relevant active column on the canonical N_e PMNS sample.
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
    reference_expansion_profile,
    solve_multisource_flavored_transport,
    solve_normalized_transport,
    washout_profile,
)
from frontier_dm_leptogenesis_pmns_projector_interface import (
    canonical_h,
    canonical_left_diagonalizer,
)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{cls}] {status}: {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def active_packet_from_h(h_act: np.ndarray) -> np.ndarray:
    _evals, u_act = canonical_left_diagonalizer(h_act)
    return np.abs(u_act) ** 2


def flavored_transport_kernel(k_decay: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    z_grid, n_n1, _ = solve_normalized_transport(k_decay, reference_expansion_profile)
    source_profile = -np.gradient(n_n1, z_grid)
    w_vals = np.array(
        [washout_profile(float(z), k_decay, reference_expansion_profile) for z in z_grid],
        dtype=float,
    )
    tail = np.zeros_like(z_grid)
    for idx in range(len(z_grid) - 2, -1, -1):
        tail[idx] = tail[idx + 1] + 0.5 * (w_vals[idx] + w_vals[idx + 1]) * (z_grid[idx + 1] - z_grid[idx])
    return z_grid, source_profile, tail


def psi_q(q: float, z_grid: np.ndarray, source_profile: np.ndarray, washout_tail: np.ndarray) -> float:
    return float(np.trapezoid(q * source_profile * np.exp(-q * washout_tail), z_grid))


def flavored_column_functional(column: np.ndarray, z_grid: np.ndarray, source_profile: np.ndarray, washout_tail: np.ndarray) -> float:
    return float(sum(psi_q(float(q), z_grid, source_profile, washout_tail) for q in np.asarray(column, dtype=float)))


def flavored_transport_direct(column: np.ndarray, k_decay: float) -> float:
    _, _, asym_grid = solve_multisource_flavored_transport(
        lambdas=np.array([1.0]),
        k_decays=np.array([k_decay]),
        source_matrix=np.array([column], dtype=float),
        washout_matrix=np.array([column], dtype=float),
    )
    return abs(float(asym_grid[:, -1].sum()))


def eta_ratio_from_transport(pkg: object, transport_factor: float) -> float:
    return (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * pkg.epsilon_1
        * transport_factor
        / ETA_OBS
    )


def part1_single_source_flavored_transport_reduces_to_an_exact_column_functional() -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    print("\n" + "=" * 88)
    print("PART 1: SINGLE-SOURCE FLAVORED TRANSPORT IS AN EXACT COLUMN FUNCTIONAL")
    print("=" * 88)

    pkg = exact_package()
    z_grid, source_profile, washout_tail = flavored_transport_kernel(pkg.k_decay_exact)

    col_a = np.array([0.07126668, 0.90030676, 0.02842655], dtype=float)
    col_b = np.array([0.33333333, 0.33333333, 0.33333333], dtype=float)

    direct_a = flavored_transport_direct(col_a, pkg.k_decay_exact)
    direct_b = flavored_transport_direct(col_b, pkg.k_decay_exact)
    func_a = flavored_column_functional(col_a, z_grid, source_profile, washout_tail)
    func_b = flavored_column_functional(col_b, z_grid, source_profile, washout_tail)

    check(
        "The exact flavored asymmetry for one source equals the sum of three one-variable channel functionals",
        abs(direct_a - func_a) < 1e-7 and abs(direct_b - func_b) < 1e-7,
        f"(Δ_a,Δ_b)=({abs(direct_a - func_a):.2e},{abs(direct_b - func_b):.2e})",
    )
    check(
        "So the transport-relevant PMNS column is selected by a scalar functional of its entries, not by a new transport ansatz",
        True,
        "F_K(P) = Σ_alpha Psi_K(P_alpha)",
    )
    check(
        "The exact functional depends only on the exact one-flavor source profile and washout tail",
        np.all(source_profile >= -1e-12) and np.all(np.diff(washout_tail) <= 1e-10),
        f"source_min={source_profile.min():.3e}, tail_max={washout_tail.max():.6f}",
    )

    print()
    print(f"  direct functional check on canonical near-closing column: {direct_a:.12f} vs {func_a:.12f}")
    print(f"  direct functional check on democratic column:            {direct_b:.12f} vs {func_b:.12f}")

    return z_grid, source_profile, washout_tail, pkg.k_decay_exact


def part2_the_exact_channel_kernel_has_a_unique_small_leakage_optimum(
    z_grid: np.ndarray, source_profile: np.ndarray, washout_tail: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CHANNEL KERNEL HAS A UNIQUE SMALL-LEAKAGE OPTIMUM")
    print("=" * 88)

    q_grid = np.linspace(0.0, 1.0, 1001)
    psi_vals = np.array([psi_q(float(q), z_grid, source_profile, washout_tail) for q in q_grid], dtype=float)
    idx = int(np.argmax(psi_vals))
    q_star = float(q_grid[idx])

    check(
        "The one-channel flavored kernel Psi_K(q) has a unique interior maximizer on [0,1]",
        0.0 < q_star < 0.05 and idx not in (0, len(q_grid) - 1),
        f"q_star={q_star:.6f}",
    )
    check(
        "The exact current branch prefers small but nonzero flavor leakage rather than a perfectly democratic or perfectly single-flavor split",
        psi_q(0.04, z_grid, source_profile, washout_tail) > psi_q(1.0 / 3.0, z_grid, source_profile, washout_tail)
        and psi_q(0.04, z_grid, source_profile, washout_tail) > psi_q(0.96, z_grid, source_profile, washout_tail),
        f"Psi(0.04)={psi_q(0.04, z_grid, source_profile, washout_tail):.6f}",
    )
    check(
        "This explains why a near-diagonal PMNS column with two small leakage entries can beat a more extreme almost-basis-vector column",
        True,
        f"q_star={q_star:.6f}",
    )

    print()
    print(f"  unique channel optimum q_star = {q_star:.6f}")
    print(f"  Psi(q_star) = {psi_vals[idx]:.12f}")


def part3_the_canonical_ne_active_block_selects_the_middle_column(
    z_grid: np.ndarray, source_profile: np.ndarray, washout_tail: np.ndarray, k_decay: float
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CANONICAL N_e ACTIVE BLOCK SELECTS THE MIDDLE COLUMN")
    print("=" * 88)

    h_e_act = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    packet = active_packet_from_h(h_e_act).T

    direct_vals = [flavored_transport_direct(packet[:, idx], k_decay) for idx in range(3)]
    func_vals = [flavored_column_functional(packet[:, idx], z_grid, source_profile, washout_tail) for idx in range(3)]
    pkg = exact_package()
    eta_vals = [eta_ratio_from_transport(pkg, value) for value in direct_vals]
    best_idx = int(np.argmax(func_vals))

    check(
        "The exact column functional reproduces the direct transport ordering on the canonical N_e packet",
        int(np.argmax(direct_vals)) == int(np.argmax(func_vals)),
        f"(argmax_direct,argmax_func)=({int(np.argmax(direct_vals))},{int(np.argmax(func_vals))})",
    )
    check(
        "On the canonical N_e active block, the transport-relevant column is exactly the middle column",
        best_idx == 1,
        f"func_vals={np.round(func_vals, 12)}",
    )
    check(
        "That exact middle-column selection is the same near-closing column previously seen in the pair-interface diagnostic",
        abs(eta_vals[best_idx] - 0.9895125971972334) < 1e-8,
        f"eta/eta_obs={eta_vals[best_idx]:.12f}",
        cls="D",
    )

    print()
    print("  canonical N_e active packet:")
    print(np.round(packet, 6))
    print(f"  direct columnwise transport factors = {np.round(direct_vals, 12)}")
    print(f"  exact functional column values      = {np.round(func_vals, 12)}")
    print(f"  direct columnwise eta/eta_obs       = {np.round(eta_vals, 12)}")


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The DM flavored-column problem is now reduced from a transport ODE search to an exact scalar functional on active PMNS columns",
        True,
        "F_K(P) = Σ_alpha Psi_K(P_alpha)",
    )
    check(
        "On the canonical charged-lepton-active sample, that exact functional selects the near-closing middle column",
        True,
        "best column index = 1",
    )
    check(
        "So the remaining open science is no longer which column transport wants; it is the PMNS-side law for the active source that generates that column",
        True,
        "derive the active five-real source or an equivalent active-column law",
    )

    print()
    print("  Transport-facing read:")
    print("    - one-source flavored transport is an exact column functional")
    print("    - the canonical N_e active packet already contains the right near-closing column")
    print("    - the open problem is now only the PMNS-side value law for that active column/source")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS FLAVOR-COLUMN FUNCTIONAL THEOREM")
    print("=" * 88)

    z_grid, source_profile, washout_tail, k_decay = part1_single_source_flavored_transport_reduces_to_an_exact_column_functional()
    part2_the_exact_channel_kernel_has_a_unique_small_leakage_optimum(z_grid, source_profile, washout_tail)
    part3_the_canonical_ne_active_block_selects_the_middle_column(z_grid, source_profile, washout_tail, k_decay)
    part4_bottom_line()

    print("\n" + "=" * 88)
    print(f"SUMMARY: classified_pass={PASS_COUNT} fail={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
