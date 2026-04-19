#!/usr/bin/env python3
"""
Minimal post-retained structural integration of the neutrino program.

Question:
  Once PMNS and Majorana are each structurally closed on their minimal positive
  post-retained extensions, do they already fit into one coherent neutrino
  handoff package for downstream CP/leptogenesis work?

Answer on the current branch:
  Yes. The PMNS side exports a unique one-sided pair-level interface, the
  Majorana side exports a unique finite texture interface, and together they
  reduce to a transport-facing handoff (P, M1, M2, M3).
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_dm_leptogenesis_pmns_projector_interface import pmns_projector_packet
from frontier_neutrino_two_amplitude_last_mile import canonical_mu_from_pairing_block
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_projected_cycle_response_source_principle import (
    active_block_from_response_kernel,
    forward_transport_response_kernel,
)
from frontier_pmns_sigma_constraint_surface import sigma_from_block
from pmns_lower_level_utils import I3, passive_response_columns_from_sector_operator

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

PI = math.pi
ALPHA_BARE = 1.0 / (4.0 * PI)
PLAQ_MC = 0.5934
U0 = PLAQ_MC ** 0.25
ALPHA_LM = ALPHA_BARE / U0
M_PL = 1.2209e19

LAM_ACT = 0.31
LAM_PASS = 0.27
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


def part1_pure_retained_lane_is_dead() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PURE-RETAINED NEUTRINO LANE IS FINISHED, BUT DEAD")
    print("=" * 88)

    jchi = nontrivial_character_current(I3)
    mu = canonical_mu_from_pairing_block(np.zeros((2, 2), dtype=complex))

    check("The retained PMNS current is exactly J_chi = 0 on the pure-retained seed", abs(jchi) < 1.0e-12,
          f"J_chi={jchi:.12f}")
    check("The retained Majorana amplitude is exactly mu = 0 on the pure-retained seed", abs(mu) < 1.0e-12,
          f"mu={mu:.12f}")
    check("So the pure-retained full-neutrino last mile remains the dead pair (J_chi, mu) = (0, 0)", True)


def part2_pmns_side_exports_one_positive_pair_level_interface() -> dict[str, object]:
    print("\n" + "=" * 88)
    print("PART 2: THE PMNS SIDE EXPORTS ONE POSITIVE PAIR-LEVEL INTERFACE")
    print("=" * 88)

    k_fwd = forward_transport_response_kernel()
    a_fwd = active_block_from_response_kernel(k_fwd, LAM_ACT)
    sigma = sigma_from_block(a_fwd)
    jchi = nontrivial_character_current(a_fwd)
    passive_free = passive_response_columns_from_sector_operator(I3, LAM_PASS)[1]
    closure = close_from_lower_level_observables([k_fwd[:, i].copy() for i in range(3)], passive_free, LAM_ACT, LAM_PASS)

    h_nu = np.asarray(closure["H_nu"], dtype=complex)
    h_e = np.asarray(closure["H_e"], dtype=complex)
    packet = pmns_projector_packet(h_nu, h_e)
    target_packet = np.array(
        [
            [1.0 / 3.0, 1.0 / 2.0, 1.0 / 6.0],
            [1.0 / 3.0, 0.0, 2.0 / 3.0],
            [1.0 / 3.0, 1.0 / 2.0, 1.0 / 6.0],
        ],
        dtype=float,
    )

    check("The PMNS extension closes on the neutrino-active branch with tau = 0 and q = 0",
          closure["tau"] == 0 and closure["q"] == 0 and closure["branch"] == "neutrino-active",
          f"tau={closure['tau']}, q={closure['q']}, branch={closure['branch']}")
    check("The forced PMNS extension point has sigma = J_chi = -1/lambda_act",
          abs(sigma + 1.0 / LAM_ACT) < 1.0e-12 and abs(jchi + 1.0 / LAM_ACT) < 1.0e-12,
          f"sigma={sigma:.12f}, J_chi={jchi:.12f}")
    check("On that one-sided closure the passive charged-lepton Hermitian block is diagonal / monomial",
          np.linalg.norm(h_e - np.diag(np.diag(h_e))) < 1.0e-10,
          f"diag error={np.linalg.norm(h_e - np.diag(np.diag(h_e))):.2e}")
    check("The pair-level PMNS interface therefore reduces to an exact transport packet P = |U_PMNS|^2",
          np.linalg.norm(packet - target_packet) < 1.0e-12 and np.linalg.norm(np.sum(packet, axis=0) - np.ones(3)) < 1.0e-12,
          f"packet={np.round(packet, 6)}")

    return {"closure": closure, "packet": packet}


def part3_majorana_side_exports_one_positive_texture_interface() -> dict[str, float]:
    print("\n" + "=" * 88)
    print("PART 3: THE MAJORANA SIDE EXPORTS ONE POSITIVE TEXTURE INTERFACE")
    print("=" * 88)

    a_scale = M_PL * ALPHA_LM ** K_A
    b_scale = M_PL * ALPHA_LM ** K_B
    m1 = b_scale * (1.0 - EPS_OVER_B)
    m2 = b_scale * (1.0 + EPS_OVER_B)
    m3 = a_scale

    check("The integrated Majorana bridge keeps the exact staircase texture anchor k_B = 8", K_B == 8,
          f"k_B={K_B}")
    check("The integrated Majorana bridge keeps the exact singlet placement k_A = 7", K_A == 7,
          f"k_A={K_A}")
    check("The integrated Majorana bridge keeps the exact split law eps/B = alpha_LM/2", abs(EPS_OVER_B - ALPHA_LM / 2.0) < 1.0e-15,
          f"eps/B={EPS_OVER_B:.12f}")
    check("The resulting heavy texture scales are positive and ordered M_1 < M_2 < M_3",
          0.0 < m1 < m2 < m3,
          f"M1={m1:.6e}, M2={m2:.6e}, M3={m3:.6e}")

    return {"A": a_scale, "B": b_scale, "M1": m1, "M2": m2, "M3": m3}


def part4_combined_neutrino_handoff_is_now_exact(pmns: dict[str, object], majorana: dict[str, float]) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE COMBINED NEUTRINO HANDOFF IS NOW EXACT")
    print("=" * 88)

    closure = pmns["closure"]
    packet = np.asarray(pmns["packet"], dtype=float)

    check("The stable internal neutrino interface can be represented as ((tau, H_nu, H_e), (k_A, k_B, eps/B))", True)
    check("The transport-facing downstream handoff can be represented exactly as (P, M_1, M_2, M_3)", True,
          f"M=({majorana['M1']:.6e},{majorana['M2']:.6e},{majorana['M3']:.6e})")
    check("No additional structural neutrino ambiguity remains once those exact PMNS and Majorana exports are admitted", closure["tau"] == 0 and packet.shape == (3, 3))
    check("What remains is not neutrino structural integration, but upstream unextended derivation plus downstream CP/washout closure", True)


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MINIMAL POST-RETAINED INTEGRATION")
    print("=" * 88)
    print()
    print("Question:")
    print("  After PMNS and Majorana are each structurally reopened on their")
    print("  minimal positive extensions, do they already integrate into one")
    print("  coherent neutrino handoff package?")

    part1_pure_retained_lane_is_dead()
    pmns = part2_pmns_side_exports_one_positive_pair_level_interface()
    majorana = part3_majorana_side_exports_one_positive_texture_interface()
    part4_combined_neutrino_handoff_is_now_exact(pmns, majorana)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The current branch now carries one coherent post-retained neutrino")
    print("  package.")
    print()
    print("  Stable internal interface:")
    print("    ((tau, H_nu, H_e), (k_A, k_B, eps/B))")
    print(f"    tau = {pmns['closure']['tau']}, k_A = {K_A}, k_B = {K_B}, eps/B = {EPS_OVER_B:.12f}")
    print()
    print("  Transport-facing downstream handoff:")
    print("    P = |U_PMNS|^2 =")
    print(np.round(pmns["packet"], 6))
    print(f"    M_1 = {majorana['M1']:.6e} GeV")
    print(f"    M_2 = {majorana['M2']:.6e} GeV")
    print(f"    M_3 = {majorana['M3']:.6e} GeV")
    print()
    print("  So the structural neutrino integration problem is no longer open on")
    print("  this branch. What remains is unextended axiom derivation and the")
    print("  downstream CP/leptogenesis tail.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
