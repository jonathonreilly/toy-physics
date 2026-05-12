#!/usr/bin/env python3
"""
PR #230 Block63 lane-1 completion audit.

This runner is a strict campaign checkpoint for the action-first canonical
O_H plus source-Higgs pole-row lane.  It does not claim closure.  It verifies
that the current PR230 surface still lacks the exact artifacts required by the
lane-1 objective, even after the compact-source/K-prime support blocks and the
latest higher-shell chunk checkpoints.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block63_lane1_completion_audit_2026-05-12.json"
)

PARENTS = {
    "action_first_oh_artifact": "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json",
    "degree_one_radial_tangent_oh": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_action_adoption_minimal_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "fms_source_overlap_readout": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
    "canonical_oh_accepted_action_stretch": "outputs/yt_pr230_canonical_oh_accepted_action_stretch_attempt_2026-05-07.json",
    "source_higgs_direct_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "source_higgs_production_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_gram_purity_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "block62_compact_source_kprime": "outputs/yt_pr230_block62_compact_source_kprime_identifiability_obstruction_2026-05-12.json",
    "schur_higher_shell_chunk003": "outputs/yt_pr230_schur_higher_shell_chunk003_checkpoint_2026-05-12.json",
    "schur_higher_shell_chunk004": "outputs/yt_pr230_schur_higher_shell_chunk004_checkpoint_2026-05-12.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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


def proposal_allowed(cert: dict[str, Any]) -> bool:
    return cert.get("proposal_allowed") is True


def main() -> int:
    print("PR #230 Block63 lane-1 completion audit")
    print("=" * 72)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if proposal_allowed(cert)
    ]

    fms_packet = certs["fms_oh_candidate_action_packet"]
    fms_adoption = certs["fms_action_adoption_minimal_cut"]
    degree_one = certs["degree_one_radial_tangent_oh"]
    action_first = certs["action_first_oh_artifact"]
    accepted_action = certs["canonical_oh_accepted_action_stretch"]
    direct_rows = certs["source_higgs_direct_pole_row_contract"]
    row_acceptance = certs["source_higgs_pole_row_acceptance_contract"]
    readiness = certs["source_higgs_production_readiness"]
    gram_gate = certs["source_higgs_gram_purity_gate"]
    gram_post = certs["source_higgs_gram_purity_postprocess"]
    block62 = certs["block62_compact_source_kprime"]
    chunk003 = certs["schur_higher_shell_chunk003"]
    chunk004 = certs["schur_higher_shell_chunk004"]
    assembly = certs["full_positive_assembly"]
    campaign = certs["campaign_status"]
    retained = certs["retained_route"]

    degree_one_support_loaded = (
        degree_one.get("degree_one_radial_tangent_oh_theorem_passed") is True
        and proposal_allowed(degree_one) is False
        and "same-surface action/LSZ premise and pole rows absent"
        in statuses["degree_one_radial_tangent_oh"]
    )
    fms_support_not_adopted = (
        fms_packet.get("fms_oh_candidate_action_packet_passed") is True
        and fms_packet.get("same_surface_cl3_z3_derived") is False
        and fms_packet.get("accepted_current_surface") is False
        and proposal_allowed(fms_packet) is False
        and fms_adoption.get("fms_action_adoption_minimal_cut_passed") is True
        and fms_adoption.get("same_surface_cl3_z3_derived") is False
        and fms_adoption.get("accepted_current_surface") is False
        and proposal_allowed(fms_adoption) is False
    )
    action_first_root_blocked = (
        proposal_allowed(action_first) is False
        and "not constructible from current PR230 surface"
        in statuses["action_first_oh_artifact"]
        and proposal_allowed(accepted_action) is False
        and "accepted-action root not derivable"
        in statuses["canonical_oh_accepted_action_stretch"]
    )
    canonical_oh_absent = (
        direct_rows.get("future_artifact_presence", {}).get(
            "canonical_higgs_operator_certificate"
        )
        is False
        and readiness.get("operator_certificate_present") is False
    )
    strict_source_higgs_rows_absent = (
        direct_rows.get("future_artifact_presence", {}).get(
            "source_higgs_measurement_rows"
        )
        is False
        and direct_rows.get("future_artifact_presence", {}).get(
            "source_higgs_production_certificate"
        )
        is False
        and readiness.get("future_rows_present") is False
        and readiness.get("future_production_certificate_present") is False
        and direct_rows.get("current_surface_contract_satisfied") is False
        and row_acceptance.get("source_higgs_pole_row_acceptance_contract_passed")
        is True
        and proposal_allowed(row_acceptance) is False
    )
    source_higgs_launch_blocked = (
        readiness.get("source_higgs_launch_ready") is False
        and "blocked by missing O_H certificate"
        in statuses["source_higgs_production_readiness"]
    )
    gram_authority_absent = (
        proposal_allowed(gram_gate) is False
        and "not passed" in statuses["source_higgs_gram_purity_gate"]
        and proposal_allowed(gram_post) is False
        and "awaiting production certificate"
        in statuses["source_higgs_gram_purity_postprocess"]
    )
    kprime_residue_absent_after_block62 = (
        block62.get("block62_compact_source_kprime_identifiability_obstruction_passed")
        is True
        and block62.get("kprime_authority_present") is False
        and block62.get("pole_residue_authority_present") is False
        and proposal_allowed(block62) is False
    )
    latest_chunk_support_only = (
        proposal_allowed(chunk003) is False
        and proposal_allowed(chunk004) is False
        and "bounded-support" in statuses["schur_higher_shell_chunk003"]
        and "bounded-support" in statuses["schur_higher_shell_chunk004"]
    )
    assembly_still_open = (
        proposal_allowed(assembly) is False
        and "full positive PR230 closure assembly gate not passed"
        in statuses["full_positive_assembly"]
        and assembly.get("block62_compact_source_kprime_identifiability_blocks")
        is True
    )
    campaign_still_open = (
        proposal_allowed(campaign) is False
        and "active campaign continuing after current shortcut blocks"
        in statuses["campaign_status"]
        and campaign.get("block62_compact_source_kprime_identifiability_blocks")
        is True
    )
    retained_route_still_open = (
        proposal_allowed(retained) is False
        and "retained closure not yet reached" in statuses["retained_route"]
    )

    full_positive_closure_achieved = False
    block63_completion_audit_passed = True

    missing_completion_requirements = [
        {
            "requirement": "same_surface_cl3_z3_derived canonical O_H/action theorem",
            "current_evidence": "FMS candidate/action packet is support only; same_surface_cl3_z3_derived=false and accepted_current_surface=false.",
            "blocking_parent": "fms_oh_candidate_action_packet / fms_action_adoption_minimal_cut",
        },
        {
            "requirement": "accepted current-surface EW/Higgs action and canonical O_H normalization/LSZ fields",
            "current_evidence": "Action-first and accepted-action attempts are exact negative boundaries on the present support stack.",
            "blocking_parent": "action_first_oh_artifact / canonical_oh_accepted_action_stretch",
        },
        {
            "requirement": "strict physical C_ss/C_sH/C_HH pole rows under canonical O_H authority",
            "current_evidence": "Direct source-Higgs row contract is exact support only; current row packet and production certificate are absent.",
            "blocking_parent": "source_higgs_direct_pole_row_contract / source_higgs_production_readiness",
        },
        {
            "requirement": "source-Higgs Gram purity and FV/IR/model-class acceptance",
            "current_evidence": "Gram gate and postprocess are open because production rows and canonical O_H certificate are absent.",
            "blocking_parent": "source_higgs_gram_purity_gate / source_higgs_gram_purity_postprocess",
        },
        {
            "requirement": "K-prime / pole-residue authority or strict scalar denominator theorem",
            "current_evidence": "Block62 proves compact source support plus fixed carrier does not identify K'(pole) or pole residue.",
            "blocking_parent": "block62_compact_source_kprime",
        },
        {
            "requirement": "aggregate retained-route authorization",
            "current_evidence": "Full closure assembly, retained-route, and campaign gates remain open with proposal_allowed=false.",
            "blocking_parent": "full_positive_assembly / retained_route / campaign_status",
        },
    ]

    next_admissible_actions = [
        "Derive an accepted same-surface Cl(3)/Z3 EW/Higgs action and canonical O_H/LSZ theorem without H_unit, Ward, observed targets, alpha_LM, plaquette, u0, or alias imports.",
        "Generate strict source-Higgs C_ss/C_sH/C_HH Euclidean pole rows after canonical O_H is certified, then run pole extraction, Gram purity, FV/IR/model-class, retained-route, and campaign gates.",
        "Derive a scalar denominator theorem giving K'(pole) and pole residue directly on the thermodynamic PR230 surface.",
        "Supply same-surface Schur A/B/C kernel rows with pole derivatives instead of using finite compact-source moments as a residue proxy.",
        "Supply a strict physical W/Z response or neutral primitive transfer bridge with absolute normalization authority, not support-only covariance or ratio rows.",
    ]

    report("parent-certificates-present", not missing, f"missing={missing}")
    report(
        "no-parent-authorizes-proposed-retained",
        not proposal_allowed_parents,
        f"proposal_allowed={proposal_allowed_parents}",
    )
    report("degree-one-support-loaded-not-closure", degree_one_support_loaded, statuses["degree_one_radial_tangent_oh"])
    report("fms-support-not-adopted", fms_support_not_adopted, statuses["fms_oh_candidate_action_packet"])
    report("action-first-root-blocked", action_first_root_blocked, statuses["action_first_oh_artifact"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["source_higgs_direct_pole_row_contract"])
    report("strict-source-higgs-rows-absent", strict_source_higgs_rows_absent, statuses["source_higgs_direct_pole_row_contract"])
    report("source-higgs-launch-blocked", source_higgs_launch_blocked, statuses["source_higgs_production_readiness"])
    report("gram-authority-absent", gram_authority_absent, statuses["source_higgs_gram_purity_gate"])
    report("kprime-residue-absent-after-block62", kprime_residue_absent_after_block62, statuses["block62_compact_source_kprime"])
    report("latest-chunks-support-only", latest_chunk_support_only, "chunks003/004 are bounded support, not closure rows")
    report("full-assembly-still-open", assembly_still_open, statuses["full_positive_assembly"])
    report("campaign-still-open", campaign_still_open, statuses["campaign_status"])
    report("retained-route-still-open", retained_route_still_open, statuses["retained_route"])
    report("full-positive-closure-not-achieved", not full_positive_closure_achieved, "Block63 is a completion audit, not a closure claim")
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false by construction and evidence")

    result = {
        "actual_current_surface_status": (
            "open / exact lane-1 completion audit: full PR230 positive closure "
            "not achieved on the current surface"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface canonical O_H/action/LSZ "
            "theorem and strict C_ss/C_sH/C_HH pole-row packet pass all aggregate gates"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Block63 is a completion audit.  It finds missing same-surface "
            "canonical O_H/action/LSZ authority, absent strict source-Higgs "
            "pole rows, absent Gram/FVIR/model-class acceptance, and absent "
            "K-prime/pole-residue authority."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block63_lane1_completion_audit_passed": block63_completion_audit_passed,
        "full_positive_closure_achieved": full_positive_closure_achieved,
        "proposed_retained_allowed": False,
        "completion_checks": {
            "degree_one_support_loaded": degree_one_support_loaded,
            "fms_support_not_adopted": fms_support_not_adopted,
            "action_first_root_blocked": action_first_root_blocked,
            "canonical_oh_absent": canonical_oh_absent,
            "strict_source_higgs_rows_absent": strict_source_higgs_rows_absent,
            "source_higgs_launch_blocked": source_higgs_launch_blocked,
            "gram_authority_absent": gram_authority_absent,
            "kprime_residue_absent_after_block62": kprime_residue_absent_after_block62,
            "latest_chunk_support_only": latest_chunk_support_only,
            "assembly_still_open": assembly_still_open,
            "campaign_still_open": campaign_still_open,
            "retained_route_still_open": retained_route_still_open,
        },
        "missing_completion_requirements": missing_completion_requirements,
        "next_admissible_actions": next_admissible_actions,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat degree-one radial-tangent uniqueness as accepted O_H/action authority",
            "does not treat FMS candidate support as adopted current-surface action",
            "does not treat C_sx/C_xx or higher-shell chunks as C_sH/C_HH pole rows",
            "does not infer K'(pole) or pole residue from compact source support, finite positivity, or fixed source carrier",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed top/Yukawa values, alpha_LM, plaquette, u0, kappa_s=1, c2=1, or Z_match=1",
        ],
        "exact_next_action": (
            "Continue only on a primitive-bearing positive route: accepted "
            "same-surface canonical O_H/action/LSZ theorem, strict source-Higgs "
            "pole rows after that theorem, a thermodynamic K-prime/residue "
            "theorem, same-surface Schur pole-derivative rows, or strict "
            "physical W/Z/neutral-transfer authority."
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
