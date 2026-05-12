#!/usr/bin/env python3
"""
PR #230 Block55 canonical-neutral primitive cut gate.

Block54 reduced physical readout authorization to two roots.  This gate
attacks the canonical-Higgs / same-surface neutral-transfer root directly.
It checks whether the current degree-one, FMS, neutral-multiplicity, primitive
transfer, and Perron support artifacts close that root.  They do not: the
current surface still admits a two-neutral-singlet counterfamily, and the
finite C_sx rows are correlator support rather than transfer/primitive-cone
authority.

The positive value is a stricter cut for the next route: canonical-Higgs
closure must supply either accepted same-surface O_H/action plus strict rows,
or a same-surface primitive neutral transfer/cone certificate that fixes the
source-to-canonical-Higgs direction.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block55_canonical_neutral_primitive_cut_gate_2026-05-12.json"
)

PARENTS = {
    "block54_response_readout_reduction": "outputs/yt_pr230_block54_response_readout_reduction_gate_2026-05-12.json",
    "degree_one_radial_tangent_oh": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "same_surface_neutral_multiplicity_one": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "two_source_primitive_transfer_candidate": "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json",
    "positivity_improving_rank_one_support": "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json",
    "neutral_primitive_cone_certificate_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_hunit_as_operator": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_or_yukawa_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "treated_degree_one_support_as_current_oh_proof": False,
    "treated_fms_candidate_as_adopted_action": False,
    "treated_finite_c_sx_as_transfer_generator": False,
    "treated_positivity_support_as_primitive_cone_certificate": False,
    "treated_source_higgs_contract_as_rows": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "claimed_effective_or_proposed_retained": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 Block55 canonical-neutral primitive cut gate")
    print("=" * 76)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    block54_surviving_root = (
        certs["block54_response_readout_reduction"].get(
            "response_readout_root_reduction_passed"
        )
        is True
        and certs["block54_response_readout_reduction"].get("proposal_allowed")
        is False
        and "canonical-Higgs pole identity or same-surface neutral-transfer bridge"
        in certs["block54_response_readout_reduction"].get(
            "remaining_roots_after_reduction", []
        )
    )
    degree_one_support_not_authority = (
        certs["degree_one_radial_tangent_oh"].get(
            "degree_one_radial_tangent_oh_theorem_passed"
        )
        is True
        and certs["degree_one_radial_tangent_oh"].get("degree_one_tangent_unique")
        is True
        and certs["degree_one_radial_tangent_oh"].get(
            "canonical_oh_identity_derived"
        )
        is False
        and certs["degree_one_radial_tangent_oh"].get("source_higgs_pole_rows_present")
        is False
        and certs["degree_one_radial_tangent_oh"].get("proposal_allowed") is False
    )
    fms_candidate_not_adopted = (
        certs["fms_oh_candidate_action_packet"].get(
            "fms_oh_candidate_action_packet_passed"
        )
        is True
        and certs["fms_oh_candidate_action_packet"].get("same_surface_cl3_z3_derived")
        is False
        and certs["fms_oh_candidate_action_packet"].get("accepted_current_surface")
        is False
        and certs["fms_oh_candidate_action_packet"].get("closure_authorized")
        is False
        and certs["fms_oh_candidate_action_packet"].get("proposal_allowed") is False
    )

    counterfamily = certs["same_surface_neutral_multiplicity_one"].get(
        "current_two_singlet_counterfamily", []
    )
    overlaps = [
        row.get("source_to_candidate_overlap")
        for row in counterfamily
        if isinstance(row, dict)
    ]
    source_only_fixed = all(
        row.get("source_only_observables_change") is False
        for row in counterfamily
        if isinstance(row, dict)
    )
    neutral_counterfamily_blocks = (
        certs["same_surface_neutral_multiplicity_one"].get("candidate_accepted")
        is False
        and len(counterfamily) >= 4
        and source_only_fixed
        and min(overlaps) < 0.01
        and max(overlaps) > 0.99
        and any(
            row.get("id") == "multiplicity_one_or_primitive_generator"
            and row.get("current_satisfied") is False
            for row in certs["same_surface_neutral_multiplicity_one"].get(
                "required_artifact_contract", []
            )
            if isinstance(row, dict)
        )
    )
    finite_csx_not_transfer = (
        certs["two_source_primitive_transfer_candidate"].get(
            "finite_offdiagonal_correlation_support"
        )
        is True
        and certs["two_source_primitive_transfer_candidate"].get(
            "finite_correlator_blocks_positive"
        )
        is True
        and certs["two_source_primitive_transfer_candidate"].get(
            "physical_transfer_candidate_accepted"
        )
        is False
        and all(
            row.get("current_satisfied") is False
            for row in certs["two_source_primitive_transfer_candidate"].get(
                "primitive_transfer_obligations", []
            )
            if isinstance(row, dict)
        )
    )
    perron_support_premise_absent = (
        certs["positivity_improving_rank_one_support"].get(
            "positivity_improving_rank_one_theorem_passed"
        )
        is True
        and certs["positivity_improving_rank_one_support"].get(
            "positivity_improving_certificate_present"
        )
        is False
        and certs["positivity_improving_rank_one_support"].get(
            "current_closure_gate_passed"
        )
        is False
        and certs["positivity_improving_rank_one_support"].get("proposal_allowed")
        is False
    )
    primitive_cone_certificate_absent = (
        certs["neutral_primitive_cone_certificate_gate"].get(
            "primitive_cone_certificate_gate_passed"
        )
        is False
        and certs["neutral_primitive_cone_certificate_gate"].get("proposal_allowed")
        is False
        and "strict irreducibility certificate absent"
        in statuses["neutral_primitive_cone_certificate_gate"]
    )
    source_higgs_contract_not_rows = (
        certs["source_higgs_pole_row_contract"].get(
            "source_higgs_pole_row_acceptance_contract_passed"
        )
        is True
        and certs["source_higgs_pole_row_contract"].get("proposal_allowed") is False
        and "strict rows absent" in statuses["source_higgs_pole_row_contract"]
    )
    aggregate_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    canonical_neutral_primitive_cut_passed = (
        not missing
        and not proposal_parents
        and block54_surviving_root
        and degree_one_support_not_authority
        and fms_candidate_not_adopted
        and neutral_counterfamily_blocks
        and finite_csx_not_transfer
        and perron_support_premise_absent
        and primitive_cone_certificate_absent
        and source_higgs_contract_not_rows
        and aggregate_still_open
        and firewall_clean
    )

    remaining_canonical_neutral_obligations = [
        "accepted same-surface canonical O_H/action/LSZ certificate",
        "or same-surface primitive neutral transfer / irreducible cone certificate",
        "strict physical C_ss/C_sH/C_HH(tau) rows or equivalent source-overlap theorem",
    ]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report(
        "no-parent-authorizes-proposal",
        not proposal_parents,
        f"proposal_allowed={proposal_parents}",
    )
    report("block54-canonical-root-survives", block54_surviving_root, statuses["block54_response_readout_reduction"])
    report("degree-one-support-not-authority", degree_one_support_not_authority, statuses["degree_one_radial_tangent_oh"])
    report("fms-candidate-not-adopted", fms_candidate_not_adopted, statuses["fms_oh_candidate_action_packet"])
    report("neutral-counterfamily-blocks-current-surface", neutral_counterfamily_blocks, f"overlaps={overlaps}")
    report("finite-csx-not-transfer", finite_csx_not_transfer, statuses["two_source_primitive_transfer_candidate"])
    report("perron-support-premise-absent", perron_support_premise_absent, statuses["positivity_improving_rank_one_support"])
    report("primitive-cone-certificate-absent", primitive_cone_certificate_absent, statuses["neutral_primitive_cone_certificate_gate"])
    report("source-higgs-contract-not-rows", source_higgs_contract_not_rows, statuses["source_higgs_pole_row_contract"])
    report("aggregate-gates-still-open", aggregate_still_open, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report(
        "canonical-neutral-primitive-cut-passed",
        canonical_neutral_primitive_cut_passed,
        "current support narrows but does not close the canonical/neutral root",
    )

    result = {
        "actual_current_surface_status": "exact-support / Block55 canonical-neutral primitive cut; canonical-Higgs/neutral-transfer root still open",
        "conditional_surface_status": (
            "conditional-support if a future accepted same-surface O_H/action/LSZ "
            "certificate or primitive neutral transfer/cone certificate supplies "
            "strict source-Higgs rows or equivalent source-overlap authority"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Degree-one and FMS support narrow the operator shape, and conditional "
            "Perron support identifies the right route, but the current surface "
            "still admits a two-neutral-singlet counterfamily and lacks primitive "
            "neutral transfer, canonical O_H/action/LSZ, and strict C_sH/C_HH rows."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block55_canonical_neutral_primitive_cut_passed": canonical_neutral_primitive_cut_passed,
        "canonical_neutral_root_closed": False,
        "remaining_canonical_neutral_obligations": remaining_canonical_neutral_obligations,
        "counterfamily_overlap_range": {
            "min": min(overlaps) if overlaps else None,
            "max": max(overlaps) if overlaps else None,
        },
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim effective or proposed_retained y_t closure",
            "does not treat degree-one uniqueness as canonical O_H authority",
            "does not treat FMS candidate support as adopted action",
            "does not treat finite C_sx rows as a transfer generator or primitive cone",
            "does not treat conditional Perron support as a current primitive certificate",
            "does not treat the source-Higgs pole-row contract as row evidence",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Attack the canonical-neutral root only with a new same-surface "
            "primitive transfer/cone certificate or accepted O_H/action/LSZ "
            "certificate plus strict physical C_ss/C_sH/C_HH rows; otherwise "
            "pivot to scalar pole/model-class/FV/IR authority."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
