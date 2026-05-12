#!/usr/bin/env python3
"""
PR #230 lane-1 canonical O_H root theorem attempt.

This runner is the first block of the lane-1 physics-loop campaign:
action-first canonical O_H plus strict source-Higgs pole rows.  It tests the
strongest current claim after the completed 63/63 taste-radial packet:

    current PR230 surface => x = canonical O_H and accepted action authority.

The result is an exact negative boundary for the current surface, not a global
no-go.  The completed rows remain useful bounded support, but the present
certificates still allow distinct same-surface completions with identical
current taste-radial evidence and different source-Higgs overlap.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_lane1_oh_root_theorem_attempt_2026-05-12.json"

PARENTS = {
    "degree_one_radial_tangent": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "taste_radial_promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "row_combiner": "outputs/yt_pr230_two_source_taste_radial_row_combiner_gate_2026-05-06.json",
    "source_higgs_direct_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "canonical_oh_hard_residual": "outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json",
    "source_higgs_time_kernel_gevp": "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json",
    "os_transfer_kernel_artifact": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "additive_top_rows": "outputs/yt_pr230_additive_top_jacobian_rows_2026-05-07.json",
    "additive_top_subtraction_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yukawa_selector": False,
    "used_observed_wz_mass_or_g2_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "used_reduced_pilot_as_production": False,
    "renamed_C_sx_C_xx_as_C_sH_C_HH": False,
    "identified_taste_radial_x_as_canonical_O_H": False,
    "treated_conditional_fms_packet_as_accepted_action": False,
    "treated_equal_time_rows_as_transfer_kernel": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "claimed_retained_or_proposed_retained": False,
    "touched_live_chunk_worker": False,
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load(relpath: str) -> dict[str, Any]:
    path = ROOT / relpath
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def int_value(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, list):
        return len(value)
    return None


def overlap_witness(theta: float) -> dict[str, Any]:
    """Two completions with the same current x-data and different O_H overlap."""
    source_axis = [1.0, 0.0]
    orthogonal_axis = [0.0, 1.0]
    oh_identity = [1.0, 0.0]
    oh_mixed = [math.cos(theta), math.sin(theta)]
    current_observed_rows = {
        "operator_measured": "x_taste_radial",
        "C_ss": "fixed",
        "C_sx": "fixed",
        "C_xx": "fixed",
        "C_sH": "absent",
        "C_HH": "absent",
    }
    return {
        "same_current_observed_rows": current_observed_rows,
        "source_axis_x": source_axis,
        "orthogonal_neutral_axis": orthogonal_axis,
        "completion_A": {
            "canonical_O_H": oh_identity,
            "x_dot_O_H": 1.0,
            "source_higgs_overlap": 1.0,
            "promotion_allowed_if_action_LSZ_also_certified": True,
        },
        "completion_B": {
            "canonical_O_H": oh_mixed,
            "x_dot_O_H": math.cos(theta),
            "source_higgs_overlap": math.cos(theta),
            "promotion_allowed_on_current_surface": False,
        },
        "theta_radians": theta,
        "overlap_difference": 1.0 - math.cos(theta),
        "interpretation": (
            "Current PR230 rows measure x, not canonical O_H.  Until the "
            "action/LSZ/canonical-operator premise fixes O_H, both completions "
            "preserve the current measured x-packet while giving different "
            "source-Higgs overlap."
        ),
    }


def main() -> int:
    print("PR #230 lane-1 canonical O_H root theorem attempt")
    print("=" * 78)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    row_combiner = certs["row_combiner"]
    ready_chunks = int_value(row_combiner.get("ready_chunks"))
    expected_chunks = int_value(row_combiner.get("expected_chunks"))
    complete_taste_packet = (
        ready_chunks == 63
        and expected_chunks == 63
        and row_combiner.get("combined_rows_written") is True
        and "C_sx/C_xx" in statuses["row_combiner"]
    )

    degree_support_only = (
        certs["degree_one_radial_tangent"].get("degree_one_radial_tangent_oh_theorem_passed")
        is True
        and certs["degree_one_radial_tangent"].get("degree_one_tangent_unique") is True
        and certs["degree_one_radial_tangent"].get("same_surface_linear_tangent_premise_derived")
        is False
        and certs["degree_one_radial_tangent"].get("canonical_oh_identity_derived")
        is False
    )
    fms_conditional_only = (
        certs["fms_oh_candidate_action_packet"].get("proposal_allowed") is False
        and certs["fms_oh_candidate_action_packet"].get("accepted_current_surface") is False
        and certs["fms_oh_candidate_action_packet"].get("same_surface_cl3_z3_derived") is False
    )
    promotion_blocked = (
        certs["taste_radial_promotion_contract"].get("promotion_contract_passed") is True
        and certs["taste_radial_promotion_contract"].get("current_promotion_allowed") is False
    )
    pole_rows_absent = (
        certs["source_higgs_direct_pole_row_contract"].get("proposal_allowed") is False
        and not certs["source_higgs_direct_pole_row_contract"].get(
            "current_source_higgs_pole_rows_present", False
        )
    )
    hard_residual_open = (
        certs["canonical_oh_hard_residual"].get("proposal_allowed") is False
        and "hard residual not closed" in statuses["canonical_oh_hard_residual"]
    )
    no_scalar_time_kernel = (
        certs["os_transfer_kernel_artifact"].get("same_surface_transfer_or_gevp_present")
        is False
        and certs["os_transfer_kernel_artifact"].get(
            "chunks_with_scalar_time_kernel", 0
        )
        == 0
    )
    additive_rows_not_lane1_closure = (
        certs["additive_top_rows"].get("proposal_allowed") is False
        and certs["additive_top_rows"].get("bounded_additive_top_jacobian_rows_passed")
        is True
        and certs["additive_top_rows"].get("row_source", {}).get("complete_chunk_packet")
        is True
        and certs["additive_top_rows"].get("strict_additive_top_jacobian_rows_passed")
        is False
        and certs["additive_top_subtraction_contract"].get("proposal_allowed") is False
    )
    aggregate_rejects = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    witness = overlap_witness(math.pi / 4.0)
    witness_nonidentifying = (
        witness["completion_A"]["source_higgs_overlap"]
        != witness["completion_B"]["source_higgs_overlap"]
        and witness["same_current_observed_rows"]["C_sH"] == "absent"
        and witness["same_current_observed_rows"]["C_HH"] == "absent"
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    exact_negative_boundary = (
        not missing
        and not proposal_parents
        and complete_taste_packet
        and degree_support_only
        and fms_conditional_only
        and promotion_blocked
        and pole_rows_absent
        and hard_residual_open
        and no_scalar_time_kernel
        and additive_rows_not_lane1_closure
        and aggregate_rejects
        and witness_nonidentifying
        and firewall_clean
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("complete-taste-radial-packet", complete_taste_packet, f"ready={ready_chunks}/{expected_chunks}")
    report("degree-one-theorem-support-only", degree_support_only, statuses["degree_one_radial_tangent"])
    report("fms-packet-conditional-only", fms_conditional_only, statuses["fms_oh_candidate_action_packet"])
    report("taste-radial-promotion-blocked", promotion_blocked, statuses["taste_radial_promotion_contract"])
    report("source-higgs-pole-rows-absent", pole_rows_absent, statuses["source_higgs_direct_pole_row_contract"])
    report("canonical-oh-hard-residual-open", hard_residual_open, statuses["canonical_oh_hard_residual"])
    report("scalar-time-kernel-absent", no_scalar_time_kernel, statuses["os_transfer_kernel_artifact"])
    report("additive-rows-not-lane1-closure", additive_rows_not_lane1_closure, statuses["additive_top_rows"])
    report("aggregate-gates-reject-proposal", aggregate_rejects, "assembly/retained/campaign deny proposal")
    report("overlap-witness-nonidentifying", witness_nonidentifying, f"delta={witness['overlap_difference']:.12f}")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("exact-negative-boundary", exact_negative_boundary, "current support stack does not derive x=canonical O_H")

    result = {
        "actual_current_surface_status": (
            "no-go / exact negative boundary for lane-1 Block A: current PR230 "
            "support stack does not derive x=canonical O_H or accepted action authority"
        ),
        "conditional_surface_status": (
            "exact support if a future same-surface action/canonical-operator "
            "certificate proves x=canonical O_H with LSZ/metric normalization "
            "and strict C_ss/C_sH/C_HH pole rows"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current surface has complete taste-radial C_sx/C_xx support and "
            "degree-one axis support, but accepted action authority, canonical O_H, "
            "C_sH/C_HH pole rows, scalar time-kernel authority, and Gram flatness "
            "remain absent."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "lane1_block": "A",
        "lane1_block_result": "exact_negative_boundary_current_surface_only",
        "exact_negative_boundary_passed": exact_negative_boundary,
        "same_surface_cl3_z3_derived": False,
        "accepted_current_surface": False,
        "canonical_oh_identity_derived": False,
        "canonical_lsz_metric_derived": False,
        "source_higgs_pole_rows_present": False,
        "scalar_time_kernel_present": False,
        "current_promotion_allowed": False,
        "complete_taste_radial_packet": complete_taste_packet,
        "ready_chunks": ready_chunks,
        "expected_chunks": expected_chunks,
        "witness": witness,
        "open_imports": [
            "same-surface EW/Higgs action or canonical-operator theorem",
            "x=canonical O_H identity and normalization certificate",
            "canonical LSZ/metric and limiting-order authority",
            "production C_ss/C_sH/C_HH pole rows",
            "source-Higgs Gram flatness or equivalent rank-one theorem",
            "FV/IR/model-class scalar-pole authority",
        ],
        "retirement_paths": [
            "derive/adopt same-surface action and canonical O_H, then rerun promotion and pole-row gates",
            "measure strict C_ss/C_sH/C_HH time-kernel rows for certified O_H",
            "prove a neutral rank-one theorem that forces x=O_H or kappa=1 without relabeling",
            "bypass through strict same-source W/Z physical-response packet",
        ],
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "summary": {
            "pass": PASS_COUNT,
            "fail": FAIL_COUNT,
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
