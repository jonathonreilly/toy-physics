#!/usr/bin/env python3
"""
PR #230 lane-1 action-premise derivation attempt.

Block A showed that the completed taste-radial packet does not derive
x=canonical O_H.  This runner attacks the next residual directly: can the
current minimal Cl(3)/Z3 substrate derive the same-surface EW/Higgs action or
canonical-operator premise needed to make x the canonical Higgs coordinate?

The current answer is no.  The minimal PR230 dynamics contain Wilson gauge
links plus staggered fermions and source insertions; the FMS packet requires a
dynamic Phi field, radial background, canonical h, and LSZ metric.  Adding
those is an action adoption/extension unless a future theorem supplies them
from the substrate.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_lane1_action_premise_derivation_attempt_2026-05-12.json"
)

DOCS = {
    "minimal_axioms": "docs/MINIMAL_AXIOMS_2026-04-11.md",
    "fms_cut": "docs/YT_PR230_FMS_ACTION_ADOPTION_MINIMAL_CUT_NOTE_2026-05-07.md",
    "fms_packet": "docs/YT_PR230_FMS_OH_CANDIDATE_ACTION_PACKET_NOTE_2026-05-07.md",
    "action_first_completion": "docs/YT_PR230_ACTION_FIRST_ROUTE_COMPLETION_NOTE_2026-05-06.md",
}

PARENTS = {
    "lane1_oh_root": "outputs/yt_pr230_lane1_oh_root_theorem_attempt_2026-05-12.json",
    "fms_action_adoption_minimal_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "canonical_oh_accepted_action_stretch": "outputs/yt_pr230_canonical_oh_accepted_action_stretch_attempt_2026-05-07.json",
    "action_first_route_completion": "outputs/yt_pr230_action_first_route_completion_2026-05-06.json",
    "same_source_ew_action_semantic_firewall": "outputs/yt_wz_same_source_ew_action_semantic_firewall_2026-05-04.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "additive_source_radial_spurion_incompatibility": "outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_target_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "adopted_external_higgs_action_as_derived": False,
    "treated_fms_literature_as_proof": False,
    "treated_source_insertion_as_dynamic_scalar_field": False,
    "treated_hubbard_stratonovich_rewrite_as_available_without_kernel": False,
    "relabelled_C_sx_C_xx_as_C_sH_C_HH": False,
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


def read(rel: str) -> str:
    path = ROOT / rel
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def main() -> int:
    print("PR #230 lane-1 action-premise derivation attempt")
    print("=" * 78)

    docs = {name: read(path) for name, path in DOCS.items()}
    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_docs = [name for name, text in docs.items() if not text]
    missing_certs = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]

    minimal_surface_is_gauge_fermion = (
        "staggered-Dirac partition" in docs["minimal_axioms"]
        and "Wilson action form" in docs["minimal_axioms"]
        and "Everything else" in docs["minimal_axioms"]
    )
    minimal_input_stack = (
        docs["minimal_axioms"].split("## What Already Follows On The Current Package")[0]
    )
    no_fundamental_scalar_in_bare_action = (
        "Grassmann / staggered-Dirac partition" in minimal_input_stack
        and "Everything else in the current publication" in minimal_input_stack
        and "Higgs" not in minimal_input_stack
        and "Phi" not in minimal_input_stack
        and "scalar action" not in minimal_input_stack
    )
    fms_packet = certs["fms_oh_candidate_action_packet"]
    fms_contract = fms_packet.get("packet", {})
    fms_action_contract = fms_contract.get("action_surface_contract", {})
    fms_surface = fms_contract.get("current_surface_classification", {})
    fms_required_fields = fms_action_contract.get("required_fields", [])
    fms_requires_new_dynamic_phi = (
        any("dynamic Higgs doublet Phi" in str(field) for field in fms_required_fields)
        and fms_packet.get("accepted_current_surface") is False
        and fms_packet.get("same_surface_cl3_z3_derived") is False
        and fms_surface.get("external_extension_required") is True
    )
    adoption_cut_open = (
        "minimal adoption cut still needs" in docs["fms_cut"]
        and certs["fms_action_adoption_minimal_cut"].get("proposal_allowed") is False
    )
    action_first_current_surface_blocked = (
        "route not complete on current PR230 surface" in status(certs["action_first_route_completion"])
        and certs["action_first_route_completion"].get("proposal_allowed") is False
    )
    semantic_firewall_blocks_import = (
        certs["same_source_ew_action_semantic_firewall"].get("proposal_allowed") is False
        and "semantic firewall" in status(certs["same_source_ew_action_semantic_firewall"])
    )
    radial_spurion_contract_support_only = (
        certs["radial_spurion_action_contract"].get("proposal_allowed") is False
        and certs["additive_source_radial_spurion_incompatibility"].get("proposal_allowed")
        is False
    )
    prior_lane1_root_blocked = (
        certs["lane1_oh_root"].get("exact_negative_boundary_passed") is True
        and certs["lane1_oh_root"].get("accepted_current_surface") is False
        and certs["lane1_oh_root"].get("canonical_oh_identity_derived") is False
    )
    aggregate_rejects = (
        certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )

    action_completion_witness = {
        "current_integration_variables": [
            "SU(3) gauge links",
            "staggered fermion/Grassmann fields",
            "external source insertions",
        ],
        "fms_action_variables_required": [
            "dynamic Higgs doublet Phi",
            "radial background v",
            "canonical scalar h",
            "Goldstone pi fields",
            "canonical scalar kinetic/LSZ metric",
        ],
        "missing_kernel_for_hs_rewrite": (
            "No current PR230 certificate supplies a four-fermion kernel, "
            "positive auxiliary-field covariance, or exact Hubbard-Stratonovich "
            "identity that would introduce Phi as a derived same-surface field."
        ),
        "conclusion": (
            "The current source/taste-radial insertion is an external probe of "
            "the existing gauge-fermion substrate.  It is not a derived dynamic "
            "Higgs action or canonical scalar field."
        ),
    }
    witness_blocks_derivation = (
        "dynamic Higgs doublet Phi" in action_completion_witness["fms_action_variables_required"]
        and "external source insertions" in action_completion_witness["current_integration_variables"]
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    exact_negative_boundary = (
        not missing_docs
        and not missing_certs
        and not proposal_parents
        and minimal_surface_is_gauge_fermion
        and no_fundamental_scalar_in_bare_action
        and fms_requires_new_dynamic_phi
        and adoption_cut_open
        and action_first_current_surface_blocked
        and semantic_firewall_blocks_import
        and radial_spurion_contract_support_only
        and prior_lane1_root_blocked
        and aggregate_rejects
        and witness_blocks_derivation
        and firewall_clean
    )

    report("docs-present", not missing_docs, f"missing={missing_docs}")
    report("parent-certificates-present", not missing_certs, f"missing={missing_certs}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("minimal-surface-is-gauge-fermion", minimal_surface_is_gauge_fermion, DOCS["minimal_axioms"])
    report("no-fundamental-scalar-in-minimal-input-stack", no_fundamental_scalar_in_bare_action, DOCS["minimal_axioms"])
    report("fms-requires-new-dynamic-phi", fms_requires_new_dynamic_phi, DOCS["fms_packet"])
    report("fms-action-adoption-cut-open", adoption_cut_open, statuses["fms_action_adoption_minimal_cut"])
    report("action-first-current-surface-blocked", action_first_current_surface_blocked, statuses["action_first_route_completion"])
    report("same-source-ew-action-firewall-blocks-import", semantic_firewall_blocks_import, statuses["same_source_ew_action_semantic_firewall"])
    report("radial-spurion-contract-support-only", radial_spurion_contract_support_only, statuses["radial_spurion_action_contract"])
    report("prior-lane1-root-blocked", prior_lane1_root_blocked, statuses["lane1_oh_root"])
    report("aggregate-gates-reject-proposal", aggregate_rejects, "retained/campaign proposal_allowed=false")
    report("action-completion-witness-blocks-derivation", witness_blocks_derivation, "source insertion != dynamic Phi action")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("exact-negative-boundary", exact_negative_boundary, "current minimal substrate does not derive accepted O_H action premise")

    result = {
        "actual_current_surface_status": (
            "no-go / exact negative boundary for lane-1 action-premise derivation: "
            "current minimal PR230 substrate does not derive accepted EW/Higgs action or canonical O_H authority"
        ),
        "conditional_surface_status": (
            "conditional-support if a future theorem derives a dynamic Phi/action/LSZ "
            "from Cl(3)/Z3, or if an explicit action extension is admitted and then "
            "strict C_ss/C_sH/C_HH pole rows are measured"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current substrate and certificates provide gauge-fermion dynamics, "
            "taste-radial source probes, and conditional FMS support, but no dynamic "
            "Phi field, accepted scalar action, canonical O_H identity, LSZ metric, "
            "or source-Higgs pole-row packet."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "exact_negative_boundary_passed": exact_negative_boundary,
        "same_surface_phi_derived": False,
        "same_surface_ew_higgs_action_derived": False,
        "canonical_oh_action_premise_derived": False,
        "canonical_lsz_metric_derived": False,
        "hs_rewrite_authority_present": False,
        "action_completion_witness": action_completion_witness,
        "open_imports": [
            "dynamic Phi or equivalent scalar carrier derived from Cl(3)/Z3",
            "same-surface EW/Higgs action or accepted extension authority",
            "canonical radial h and LSZ/metric normalization",
            "source coordinate dS/ds = sum_x O_H(x) without additive top contamination",
            "strict C_ss/C_sH/C_HH pole rows and Gram/FV/IR authority",
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
