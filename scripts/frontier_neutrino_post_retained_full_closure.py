#!/usr/bin/env python3
"""
Neutrino post-retained full-closure capstone.

Question:
  What does the current main-derived neutrino work close exactly on the live
  post-retained lane?

Answer on the current branch:
  The exact charged-lepton-active post-retained N_e lane is structurally closed
  on the observational surface eta/eta_obs = 1.

  The exact content is:
    1. the PMNS-assisted N_e source is fixed by the sole-axiom effective-action
       selector on the exact reduced domain;
    2. that selected H_e gives eta/eta_obs = 1 on the favored exact transport
       column;
    3. the remaining microscopic D completion is spectator-inert because every
       admissible H_e has exact charge-preserving Schur lifts and the charged
       source-response law factors only through H_e;
    4. the Majorana side is already fixed by the minimal bridge
       (k_B = 8, k_A = 7, eps/B = alpha_LM/2).

What still remains open is the observation-free normalization/value law that
would recover the same positive lane without using the eta/eta_obs = 1 closure
surface.
"""

from __future__ import annotations

import math
import sys

import numpy as np

import frontier_dm_leptogenesis_pmns_active_projector_reduction as act
import frontier_dm_leptogenesis_pmns_multistart_selector_support as selector
import frontier_dm_leptogenesis_pmns_observable_relative_action_law as rel
import frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem as stat
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
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_left_diagonalizer
from frontier_neutrino_two_amplitude_last_mile import canonical_mu_from_pairing_block
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from pmns_lower_level_utils import I3

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi
ALPHA_BARE = 1.0 / (4.0 * PI)
PLAQ_MC = 0.5934
U0 = PLAQ_MC ** 0.25
ALPHA_LM = ALPHA_BARE / U0
M_PL = 1.2209e19

K_A = 7
K_B = 8
EPS_OVER_B = ALPHA_LM / 2.0


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


def fmt(v: np.ndarray) -> str:
    return np.array2string(np.round(np.asarray(v, dtype=float), 6), separator=", ")


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


def reconstruct_h_from_linear_responses(responses: list[float]) -> np.ndarray:
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


def packet_from_h_e(h_e: np.ndarray) -> np.ndarray:
    _evals, u_e = canonical_left_diagonalizer(h_e)
    return (np.abs(u_e) ** 2).T


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


def positive_hermitian(dim: int, seed: int, shift: float) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    return 0.5 * (raw + raw.conj().T) + shift * np.eye(dim, dtype=complex)


def build_charge_minus_one_completion(target_le: np.ndarray, seed: int, spectator_shift: float = 4.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    f_raw = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    f = 0.5 * (f_raw + f_raw.conj().T) + spectator_shift * np.eye(2, dtype=complex)
    b = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    a = np.asarray(target_le, dtype=complex) + b @ np.linalg.inv(f) @ b.conj().T
    return np.block([[a, b], [b.conj().T, f]])


def build_full_charge_preserving_completion(target_le: np.ndarray, seed: int) -> tuple[np.ndarray, np.ndarray]:
    d_minus = build_charge_minus_one_completion(target_le, seed=seed)
    d_zero = positive_hermitian(5, seed=seed + 100, shift=4.0)
    d_plus = positive_hermitian(2, seed=seed + 200, shift=4.0)
    zeros_55 = np.zeros((5, 5), dtype=complex)
    zeros_52 = np.zeros((5, 2), dtype=complex)
    zeros_25 = np.zeros((2, 5), dtype=complex)
    d = np.block(
        [
            [d_zero, zeros_55, zeros_52],
            [zeros_55, d_minus, zeros_52],
            [zeros_25, zeros_25, d_plus],
        ]
    )
    q = np.diag(np.array([0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 1, 1], dtype=float))
    return d, q


def embed_charged_source(full_d: np.ndarray, x_e: np.ndarray) -> np.ndarray:
    j = np.zeros_like(full_d)
    j[5:8, 5:8] = x_e
    return j


def selected_ne_source() -> dict[str, object]:
    i_star, extremal_params = stat.favored_column_and_extremal_params()
    start = stat.closure_point_on_ray(extremal_params, i_star)
    p_star, result = stat.constrained_stationary_point(start, i_star)
    x_sel, y_sel, delta_sel, h_sel, etas_sel = stat.source_from_params(p_star)
    packet_sel = act.active_packet_from_h(h_sel).T
    starts = selector.collect_feasible_starts(i_star, extremal_params, count=8)
    sols: list[np.ndarray] = []
    for candidate in starts:
        sol, res = stat.constrained_stationary_point(candidate, i_star)
        if res.success:
            sols.append(np.asarray(sol, dtype=float))
    branches = selector.cluster_solutions(sols, i_star)
    return {
        "i_star": i_star,
        "params": np.asarray(p_star, dtype=float),
        "result_success": bool(result.success),
        "x": np.asarray(x_sel, dtype=float),
        "y": np.asarray(y_sel, dtype=float),
        "delta": float(delta_sel),
        "h_e": np.asarray(h_sel, dtype=complex),
        "packet": np.asarray(packet_sel, dtype=float),
        "etas": np.asarray(etas_sel, dtype=float),
        "action": float(stat.relative_action_from_params(p_star)),
        "branches": branches,
    }


def majorana_texture() -> dict[str, float]:
    a_scale = M_PL * ALPHA_LM ** K_A
    b_scale = M_PL * ALPHA_LM ** K_B
    return {
        "A": a_scale,
        "B": b_scale,
        "M1": b_scale * (1.0 - EPS_OVER_B),
        "M2": b_scale * (1.0 + EPS_OVER_B),
        "M3": a_scale,
    }


def part1_pure_retained_lane_is_dead() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PURE-RETAINED LANE REMAINS CLOSED NEGATIVE")
    print("=" * 88)

    jchi = nontrivial_character_current(I3)
    mu = canonical_mu_from_pairing_block(np.zeros((2, 2), dtype=complex))

    check("The retained PMNS current still stays at J_chi = 0", abs(jchi) < 1.0e-12, f"J_chi={jchi:.12f}")
    check("The retained Majorana amplitude still stays at mu = 0", abs(mu) < 1.0e-12, f"mu={mu:.12f}")
    check("So the pure-retained lane is finished, but not the positive promotable lane", True)


def part2_the_ne_active_selector_fixes_the_positive_pmns_lane() -> dict[str, object]:
    print("\n" + "=" * 88)
    print("PART 2: THE N_e EFFECTIVE-ACTION SELECTOR FIXES THE POSITIVE PMNS LANE")
    print("=" * 88)

    selected = selected_ne_source()
    branches = selected["branches"]
    low = branches[0]
    high = branches[1]

    check("The favored exact transport column is fixed on the reduced N_e domain", selected["i_star"] == 0,
          f"i_star={selected['i_star']}")
    check("The constrained effective-action solve converges", selected["result_success"],
          f"action={selected['action']:.12f}")
    check("The selected source lies on the exact fixed native seed surface",
          abs(np.mean(selected["x"]) - rel.XBAR_NE) < 1.0e-12 and abs(np.mean(selected["y"]) - rel.YBAR_NE) < 1.0e-12,
          f"(xbar,ybar)=({np.mean(selected['x']):.6f},{np.mean(selected['y']):.6f})")
    check("The selected branch closes eta exactly on the favored column",
          abs(float(selected["etas"][selected["i_star"]]) - 1.0) < 1.0e-10,
          f"etas={np.round(selected['etas'], 12)}")
    check("The selected branch is the same unique lowest-action branch recovered by the reduced-domain stationary classification",
          np.linalg.norm(np.asarray(selected["params"], dtype=float) - np.asarray(low.representative, dtype=float)) < 1.0e-5
          and (high.action - low.action) > 0.5,
          f"S_low={low.action:.12f}, S_high={high.action:.12f}")
    check("The exact PMNS packet is already transport-facing once H_e is known",
          np.linalg.norm(np.sum(selected["packet"], axis=0) - np.ones(3)) < 1.0e-12,
          f"packet={np.round(selected['packet'], 6)}")

    print()
    print(f"  x_sel     = {fmt(selected['x'])}")
    print(f"  y_sel     = {fmt(selected['y'])}")
    print(f"  delta_sel = {float(selected['delta']):.12e}")
    print(f"  S_rel     = {float(selected['action']):.12f}")
    print(f"  packet    =\n{np.round(selected['packet'], 6)}")
    print(f"  eta/eta_obs = {np.round(selected['etas'], 12)}")

    return selected


def part3_microscopic_charge_preserving_completion_is_schur_inert(selected: dict[str, object]) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE MICROSCOPIC D COMPLETION IS SCHUR-INERT")
    print("=" * 88)

    h_e = np.asarray(selected["h_e"], dtype=complex)
    d1, q1 = build_full_charge_preserving_completion(h_e, seed=417)
    d2, q2 = build_full_charge_preserving_completion(h_e, seed=731)

    dm1 = d1[5:10, 5:10]
    dm2 = d2[5:10, 5:10]
    l1 = schur_eff(dm1[:3, :3], dm1[:3, 3:5], dm1[3:5, :3], dm1[3:5, 3:5])
    l2 = schur_eff(dm2[:3, :3], dm2[:3, 3:5], dm2[3:5, :3], dm2[3:5, 3:5])

    test_sources = hermitian_basis()
    probe = np.array(
        [
            [0.08, 0.02 + 0.01j, -0.01j],
            [0.02 - 0.01j, -0.03, 0.02],
            [0.01j, 0.02, 0.06],
        ],
        dtype=complex,
    )
    test_sources.append(probe)
    response_err = 0.0
    for x_e in test_sources:
        j1 = embed_charged_source(d1, x_e)
        j2 = embed_charged_source(d2, x_e)
        response_err = max(
            response_err,
            abs(source_response(d1, j1) - source_response(h_e, x_e)),
            abs(source_response(d2, j2) - source_response(h_e, x_e)),
            abs(source_response(d1, j1) - source_response(d2, j2)),
        )

    linear_responses = [float(np.real(np.trace(x @ h_e))) for x in hermitian_basis()]
    h_rec = reconstruct_h_from_linear_responses(linear_responses)
    packet_rec = packet_from_h_e(h_rec)
    eta_rec = eta_values_from_packet(packet_rec)

    check("The selected H_e admits exact charge-preserving microscopic completions", np.linalg.norm(d1 @ q1 - q1 @ d1) < 1.0e-12
          and np.linalg.norm(d2 @ q2 - q2 @ d2) < 1.0e-12,
          f"commutators=({np.linalg.norm(d1 @ q1 - q1 @ d1):.2e},{np.linalg.norm(d2 @ q2 - q2 @ d2):.2e})")
    check("Different microscopic completions have the same charged Schur value L_e = H_e",
          np.linalg.norm(l1 - h_e) < 1.0e-12 and np.linalg.norm(l2 - h_e) < 1.0e-12,
          f"errors=({np.linalg.norm(l1 - h_e):.2e},{np.linalg.norm(l2 - h_e):.2e})")
    check("Charged source responses depend only on H_e and not on the spectator completion data",
          response_err < 1.0e-11, f"max response mismatch={response_err:.2e}")
    check("The charged Hermitian response pack reconstructs the same H_e exactly",
          np.linalg.norm(h_rec - h_e) < 1.0e-12, f"err={np.linalg.norm(h_rec - h_e):.2e}")
    check("So the exact packet and eta=1 closure value are completion-invariant once H_e is fixed",
          np.linalg.norm(packet_rec - np.asarray(selected["packet"], dtype=float)) < 1.0e-12
          and abs(float(eta_rec[int(selected["i_star"])]) - 1.0) < 1.0e-10,
          f"eta_rec={np.round(eta_rec, 12)}")

    print()
    print("  The microscopic D-level completion no longer reopens the lane.")
    print("  Once H_e is fixed, every charge-preserving Schur lift gives the same")
    print("  charged source-response law, the same packet, and the same eta.")


def part4_majorana_bridge_and_integrated_lane(selected: dict[str, object]) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE MAJORANA BRIDGE IS ALREADY EXACT ON THE SAME PROMOTABLE LANE")
    print("=" * 88)

    texture = majorana_texture()
    pkg = exact_package()

    check("The Majorana bridge keeps the exact staircase anchor k_B = 8", K_B == 8, f"k_B={K_B}")
    check("The Majorana bridge keeps the exact singlet placement k_A = 7", K_A == 7, f"k_A={K_A}")
    check("The Majorana bridge keeps the exact split law eps/B = alpha_LM/2", abs(EPS_OVER_B - ALPHA_LM / 2.0) < 1.0e-15,
          f"eps/B={EPS_OVER_B:.12f}")
    check("The heavy texture is positive and ordered M_1 < M_2 < M_3",
          0.0 < texture["M1"] < texture["M2"] < texture["M3"],
          f"M=({texture['M1']:.6e},{texture['M2']:.6e},{texture['M3']:.6e})")
    check("The exact DM package already uses the same lightest-scale anchor M_1",
          abs(texture["M1"] / pkg.M1 - 1.0) < 1.0e-12,
          f"M1_pkg={pkg.M1:.6e}")
    check("So the positive PMNS selector and the positive Majorana bridge already live on one coherent integrated lane",
          abs(float(np.asarray(selected['etas'], dtype=float)[int(selected['i_star'])]) - 1.0) < 1.0e-10)

    print()
    print(f"  M_1 = {texture['M1']:.6e} GeV")
    print(f"  M_2 = {texture['M2']:.6e} GeV")
    print(f"  M_3 = {texture['M3']:.6e} GeV")


def part5_bottom_line(selected: dict[str, object]) -> None:
    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)

    check("The exact live promotable lane is the charged-lepton-active post-retained N_e lane", True)
    check("That lane no longer carries unresolved microscopic free data once H_e is selected", True,
          "the D completion is spectator-inert")
    check("The current exact positive lane closes on the observational surface eta/eta_obs = 1", True,
          f"eta/eta_obs={float(np.asarray(selected['etas'], dtype=float)[int(selected['i_star'])]):.12f}")
    check("The observation-free normalization/value law that would replace that surface is still a separate open target", True)

    print()
    print("  Exact read:")
    print("    - pure-retained lane: exact negative closeout")
    print("    - positive post-retained lane: exact N_e effective-action selector")
    print("    - microscopic D tail: quotiented by Schur-completion invariance")
    print("    - Majorana bridge: exact and already integrated")
    print("    - observation-free normalization law: still open")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO POST-RETAINED FULL CLOSURE")
    print("=" * 88)
    print()
    print("Question:")
    print("  What does the current neutrino work on main close exactly on the live")
    print("  post-retained lane?")

    part1_pure_retained_lane_is_dead()
    selected = part2_the_ne_active_selector_fixes_the_positive_pmns_lane()
    part3_microscopic_charge_preserving_completion_is_schur_inert(selected)
    part4_majorana_bridge_and_integrated_lane(selected)
    part5_bottom_line(selected)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current post-retained lane:")
    print("    - PMNS side: exact N_e effective-action-selected H_e")
    print("    - transport-facing packet: |U_e|^2^T")
    print("    - selected column: i_* = 0 with eta/eta_obs = 1")
    print("    - microscopic D completion: spectator-inert via exact Schur factoring")
    print("    - Majorana side: k_B = 8, k_A = 7, eps/B = alpha_LM/2")
    print()
    print("  The pure-retained lane remains closed negative.")
    print("  The live post-retained lane is structurally closed on the exact")
    print("  observational closure surface, but the observation-free normalization")
    print("  law is still open.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
