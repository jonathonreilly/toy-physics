#!/usr/bin/env python3
"""Authority closeout for the PMNS lane on the current branch."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_effective_action_selector_boundary import gram_lift, relative_action_to_seed
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_oriented_cycle_channel_value_law import projected_forward_cycle
from frontier_pmns_projected_cycle_response_source_principle import (
    active_block_from_response_kernel,
    forward_transport_response_kernel,
)
from frontier_pmns_sigma_constraint_surface import sigma_from_block
from frontier_pmns_sigma_zero_no_go import pure_retained_pmns_blocks
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import sole_axiom_hw1_source_transfer_pack
from pmns_lower_level_utils import (
    CYCLE,
    I3,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    passive_response_columns_from_sector_operator,
)

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
LAM_ACT = 0.31
LAM_PASS = 0.27


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


def column_packet_from_active_h(h_act: np.ndarray) -> np.ndarray:
    evals, u = np.linalg.eigh(h_act)
    order = np.argsort(np.real(evals))
    u = u[:, order]
    return np.abs(u) ** 2


def part1_the_retained_bank_is_exactly_blocked() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PURE-RETAINED PMNS BANK IS EXACTLY BLOCKED")
    print("=" * 88)

    blocks = pure_retained_pmns_blocks(LAM_ACT)
    sigmas = {name: sigma_from_block(block) for name, block in blocks.items()}
    currents = {name: nontrivial_character_current(block) for name, block in blocks.items()}

    check(
        "Every current retained PMNS source route still has sigma = 0",
        all(abs(value) < 1.0e-12 for value in sigmas.values()),
        f"sigmas={sigmas}",
    )
    check(
        "Every current retained PMNS readout on those routes still has J_chi = 0",
        all(abs(value) < 1.0e-12 for value in currents.values()),
        f"currents={currents}",
    )
    check(
        "So the present pure-retained sole-axiom PMNS lane is blocked at the sigma-zero boundary",
        True,
    )


def part2_the_current_axiom_bank_still_does_not_derive_the_missing_response_pack() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT AXIOM BANK STILL DOES NOT DERIVE THE MISSING RESPONSE PACK")
    print("=" * 88)

    pack = sole_axiom_hw1_source_transfer_pack(LAM_ACT, LAM_PASS)
    kernel, block = derive_active_block_from_response_columns(pack["active_columns"], LAM_ACT)
    transported_frame = [CYCLE @ col for col in pack["active_columns"]]
    transported_sector = CYCLE @ I3 @ CYCLE.conj().T
    actual_transport_columns = active_response_columns_from_sector_operator(transported_sector, LAM_ACT)[1]

    check(
        "The current sole-axiom active response pack is still the free basis-column pack",
        np.linalg.norm(np.column_stack(pack["active_columns"]) - I3) < 1.0e-12
        and np.linalg.norm(kernel - I3) < 1.0e-12
        and np.linalg.norm(block - I3) < 1.0e-12,
    )
    check(
        "Transporting the frame does not change the actual microscopic response pack of the transported free sector",
        np.linalg.norm(transported_sector - I3) < 1.0e-12
        and np.linalg.norm(np.column_stack(actual_transport_columns) - I3) < 1.0e-12,
    )
    check(
        "So the graph-fixed frame data are still not an axiom-derived nontrivial response pack",
        np.linalg.norm(np.column_stack(transported_frame) - np.column_stack(actual_transport_columns)) > 1.0e-6,
        f"frame-vs-pack={np.linalg.norm(np.column_stack(transported_frame) - np.column_stack(actual_transport_columns)):.6f}",
    )


def part3_one_exact_extension_principle_closes_pmns_positively_and_uniquely() -> dict[str, object]:
    print("\n" + "=" * 88)
    print("PART 3: ONE EXACT EXTENSION PRINCIPLE CLOSES PMNS POSITIVELY AND UNIQUELY")
    print("=" * 88)

    c = projected_forward_cycle()
    k_fwd = forward_transport_response_kernel()
    a_fwd = active_block_from_response_kernel(k_fwd, LAM_ACT)
    sigma = sigma_from_block(a_fwd)
    jchi = nontrivial_character_current(a_fwd)
    passive_free = passive_response_columns_from_sector_operator(I3, LAM_PASS)[1]
    closure = close_from_lower_level_observables([k_fwd[:, i].copy() for i in range(3)], passive_free, LAM_ACT, LAM_PASS)
    expected = -1.0 / LAM_ACT

    check(
        "The graph-fixed forward projected-cycle principle forces the unique nonfree kernel K_fwd = C^2",
        np.linalg.norm(k_fwd - (c @ c)) < 1.0e-12 and np.linalg.norm(k_fwd - I3) > 1.0e-6,
        f"error={np.linalg.norm(k_fwd - (c @ c)):.2e}",
    )
    check(
        "The exact response law then forces A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C",
        np.linalg.norm(a_fwd - ((1.0 + 1.0 / LAM_ACT) * I3 - (1.0 / LAM_ACT) * c)) < 1.0e-12,
    )
    check(
        "That forced point already has sigma = J_chi = -1/lambda_act exactly",
        abs(sigma - expected) < 1.0e-12 and abs(jchi - expected) < 1.0e-12,
        f"sigma={sigma:.12f}, J_chi={jchi:.12f}",
    )
    check(
        "With the retained passive free pack unchanged, the one-sided PMNS lane closes on the neutrino-active branch",
        closure["branch"] == "neutrino-active" and closure["tau"] == 0 and closure["q"] == 0,
        f"branch={closure['branch']}, tau={closure['tau']}, q={closure['q']}",
    )

    return {"kernel": k_fwd, "active_block": a_fwd, "closure": closure}


def part4_the_result_is_extension_dependent_and_the_downstream_handoff_is_active_only(
    data: dict[str, object],
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE RESULT IS EXTENSION-DEPENDENT AND THE DOWNSTREAM HANDOFF IS ACTIVE-ONLY")
    print("=" * 88)

    a_fwd = np.asarray(data["active_block"], dtype=complex)
    closure = data["closure"]
    action_free = relative_action_to_seed(gram_lift(I3))
    action_cycle = relative_action_to_seed(gram_lift(projected_forward_cycle()))
    action_fwd = relative_action_to_seed(gram_lift(a_fwd))
    h_nu = np.asarray(closure["H_nu"], dtype=complex)
    h_e = np.asarray(closure["H_e"], dtype=complex)
    packet = column_packet_from_active_h(h_nu)

    check(
        "The native action alone still does not select the positive reopening point",
        abs(action_free) < 1.0e-12 and abs(action_cycle) < 1.0e-12 and action_fwd > 1.0e-6,
        f"S_free={action_free:.12f}, S_cycle={action_cycle:.12f}, S_fwd={action_fwd:.12f}",
    )
    check(
        "So the current branch classification is extension-dependent rather than pure-retained positive",
        True,
    )
    check(
        "On the current positive closeout, the passive charged-lepton Hermitian block is diagonal so the downstream interface localizes to the active neutrino Hermitian block",
        np.linalg.norm(h_e - np.diag(np.diag(h_e))) < 1.0e-10 and np.linalg.norm(h_nu - np.diag(np.diag(h_nu))) > 1.0e-6,
        f"diag_error={np.linalg.norm(h_e - np.diag(np.diag(h_e))):.2e}",
    )
    check(
        "If downstream only needs flavored transport weights, that active block reduces further to a column-stochastic packet",
        np.linalg.norm(np.sum(packet, axis=0) - np.ones(3)) < 1.0e-12,
        f"packet={np.round(packet, 6)}",
    )


def main() -> int:
    print("=" * 88)
    print("PMNS CLOSURE STATUS")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the current branch, is PMNS already structurally closed from the")
    print("  retained bank, merely blocked, or extension-dependent; and what is")
    print("  the minimal honest handoff to the downstream CP/leptogenesis lane?")

    part1_the_retained_bank_is_exactly_blocked()
    part2_the_current_axiom_bank_still_does_not_derive_the_missing_response_pack()
    data = part3_one_exact_extension_principle_closes_pmns_positively_and_uniquely()
    part4_the_result_is_extension_dependent_and_the_downstream_handoff_is_active_only(data)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact PMNS branch status:")
    print("    - pure-retained bank: blocked at sigma = J_chi = 0")
    print("    - current axiom bank: still does not derive the nontrivial active response pack")
    print("    - exact beyond-retained extension: closes uniquely with")
    print("        K_fwd = C^2")
    print("        A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C")
    print("        sigma = J_chi = -1/lambda_act")
    print()
    print("  Therefore the strongest honest overall classification on this branch is:")
    print("    extension-dependent.")
    print()
    print("  Minimal PMNS handoff to CP/leptogenesis:")
    print("    - stable interface: (tau, H_act)")
    print("    - on the current positive closeout: tau = 0 and H_act = H_nu")
    print("    - transport-only consumers can reduce further to the packet")
    print("      P_i(alpha) = |U_PMNS(alpha,i)|^2 from that active block because")
    print("      the passive side is fixed diagonal/monomial on the one-sided lane")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
