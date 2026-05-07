#!/usr/bin/env python3
"""
PR #230 canonical O_H / WZ common accepted-action cut.

This runner resumes the neutral-transfer/eigenoperator campaign after the
block01 source-mixing no-go.  It does not try to promote the blocked neutral
primitive shortcut.  Instead it audits the two requested pivots:

1. canonical O_H / source-Higgs pole rows;
2. W/Z same-source physical response.

The useful science move is to expose the shared root certificate vertex that
would reopen both routes, while keeping their route-specific data obligations
separate.  Current support artifacts are accepted as support, not closure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json"
)

PARENTS = {
    "neutral_source_mixing_no_go": "outputs/yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go_2026-05-07.json",
    "degree_one_radial_tangent_oh": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "source_higgs_pole_row_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "source_higgs_time_kernel_gevp": "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json",
    "source_higgs_time_kernel_production_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
    "os_transfer_kernel_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "wz_same_source_action_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_observed_wz_masses_or_g2": False,
    "used_alpha_lm_or_plaquette_u0": False,
    "renamed_C_sx_C_xx_as_C_sH_C_HH": False,
    "used_C_sx_alias_before_canonical_OH": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "set_g2_equal_one": False,
    "treated_support_contract_as_current_action_authority": False,
    "touched_live_chunk_worker": False,
    "claimed_retained_or_proposed_retained": False,
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: str) -> dict[str, Any]:
    full = ROOT / path
    if not full.exists():
        return {}
    data = json.loads(full.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def proposal_parents(certs: dict[str, dict[str, Any]]) -> list[str]:
    return [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]


def source_higgs_contract() -> dict[str, Any]:
    return {
        "route": "canonical O_H / source-Higgs pole rows",
        "shared_root_vertices": [
            "same_surface_ew_higgs_action_or_canonical_O_H_identity",
            "canonical_scalar_kinetic_lsz_normalization",
        ],
        "route_specific_vertices": [
            "same_ensemble_C_ss_C_sH_C_HH_time_kernel_or_pole_rows",
            "no_C_sx_C_xx_aliasing_before_x_is_certified_as_O_H",
            "source_Higgs_Gram_purity_or_orthogonal_neutral_exclusion",
            "isolated_pole_FV_IR_threshold_model_class_authority",
        ],
        "support_already_present": [
            "degree_one_radial_tangent_axis_unique_under_future_action_premise",
            "default_off_time_kernel_harness_and_formal_GEVP_contract",
            "non-colliding source-Higgs time-kernel production manifest",
            "strict_source_Higgs_pole_row_acceptance_schema",
        ],
        "current_surface_status": "open_support_only",
    }


def wz_contract() -> dict[str, Any]:
    return {
        "route": "W/Z accepted-action physical response",
        "shared_root_vertices": [
            "same_surface_ew_higgs_action_or_canonical_O_H_identity",
            "single_same_source_radial_spurion_with_no_independent_top_source",
        ],
        "route_specific_vertices": [
            "accepted_same_source_EW_action_certificate",
            "production_W_or_Z_mass_fit_response_rows",
            "same_source_top_response_rows",
            "matched_top_W_or_top_Z_covariance_rows",
            "strict_non_observed_g2_or_sqrt_g2_gY_authority",
        ],
        "support_already_present": [
            "radial_spurion_response_ratio_algebra_contract",
            "minimal_WZ_accepted_action_certificate_cut",
        ],
        "current_surface_status": "open_support_only",
    }


def common_cut(certs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    wz_cut = certs["wz_same_source_action_cut"]
    source_contract = certs["source_higgs_pole_row_contract"]
    degree = certs["degree_one_radial_tangent_oh"]
    return {
        "strict_intersection_vertex": "same_surface_canonical_higgs_operator_certificate",
        "why_common": (
            "The source-Higgs route needs canonical O_H before C_sH/C_HH row "
            "labels are physical.  The W/Z accepted-action cut also lists a "
            "non-shortcut canonical-Higgs certificate as a root action vertex."
        ),
        "source_higgs_current_pass": (
            source_contract.get("source_higgs_pole_row_acceptance_contract_passed")
            is True
        ),
        "wz_current_pass": (
            wz_cut.get("wz_same_source_action_minimal_certificate_cut_passed")
            is True
        ),
        "degree_one_axis_support": (
            degree.get("degree_one_radial_tangent_oh_theorem_passed") is True
        ),
        "open_root_vertices": [
            "same_surface_canonical_higgs_operator_certificate",
            "same_surface_EW_Higgs_action_or_current_sector_overlap_identity",
            "production_source_Higgs_or_WZ_rows_on_the_accepted_action",
        ],
        "fork_after_common_vertex": {
            "source_higgs": [
                "C_ss/C_sH/C_HH pole rows",
                "Gram purity",
                "OS/GEVP/FV/IR/scalar-LSZ authority",
            ],
            "wz": [
                "W/Z mass-fit response rows",
                "matched top/W or top/Z covariance",
                "strict non-observed g2 authority",
            ],
        },
    }


def next_actions() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "action": "derive or supply a non-shortcut same-surface canonical O_H / accepted EW-Higgs action certificate",
            "why": "This is the common root vertex for the canonical source-Higgs route and the W/Z accepted-action route.",
            "must_not_use": [
                "C_sx/C_xx aliasing",
                "H_unit or yt_ward_identity",
                "observed targets",
                "plaquette/u0/alpha_LM",
                "unit kappa_s/c2/Z_match/g2 conventions",
            ],
        },
        {
            "rank": 2,
            "action": "if canonical O_H lands, run production C_ss/C_sH/C_HH time-kernel rows and OS/GEVP pole/overlap gates",
            "why": "The degree-one radial theorem and time-kernel harness are support only until physical rows exist.",
            "must_not_use": ["live chunk worker", "current C_sx labels as C_sH"],
        },
        {
            "rank": 3,
            "action": "if W/Z action lands first, build W/Z mass-fit response rows, same-source top response, matched covariance, and strict g2",
            "why": "The response-ratio algebra cancels source normalization only after these route-specific vertices exist.",
            "must_not_use": ["observed g2", "static EW algebra as response rows", "assumed covariance"],
        },
    ]


def main() -> int:
    print("PR #230 canonical O_H / WZ common accepted-action cut")
    print("=" * 76)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposals = proposal_parents(certs)

    neutral_blocked = (
        certs["neutral_source_mixing_no_go"].get("proposal_allowed") is False
        and "physical_transfer_or_offdiagonal_generator_absent"
        in certs["neutral_source_mixing_no_go"].get("current_missing_artifacts", {})
        and certs["neutral_source_mixing_no_go"]["current_missing_artifacts"][
            "physical_transfer_or_offdiagonal_generator_absent"
        ]
        is True
    )
    oh_support = (
        certs["degree_one_radial_tangent_oh"].get(
            "degree_one_radial_tangent_oh_theorem_passed"
        )
        is True
        and certs["source_higgs_pole_row_contract"].get(
            "source_higgs_pole_row_acceptance_contract_passed"
        )
        is True
        and certs["source_higgs_pole_row_contract"].get("closure_contract_satisfied")
        is False
    )
    time_kernel_support_only = (
        certs["source_higgs_time_kernel_gevp"].get("used_as_physical_yukawa_readout")
        is False
        and certs["source_higgs_time_kernel_gevp"].get(
            "physical_pole_extraction_accepted"
        )
        is False
    )
    time_kernel_manifest_not_evidence = (
        certs["source_higgs_time_kernel_production_manifest"].get(
            "proposal_allowed"
        )
        is False
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "closure_launch_authorized_now"
        )
        is False
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "operator_certificate_is_canonical_oh"
        )
        is False
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "chunk_count"
        )
        == 63
    )
    os_transfer_absent = (
        certs["os_transfer_kernel_gate"].get("os_transfer_kernel_artifact_present")
        is False
    )
    wz_support = (
        certs["wz_response_ratio_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and certs["wz_response_ratio_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certs["wz_same_source_action_cut"].get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and certs["wz_same_source_action_cut"].get(
            "current_surface_action_certificate_satisfied"
        )
        is False
    )
    common = common_cut(certs)
    common_vertex_open = (
        "same_surface_canonical_higgs_operator_certificate"
        in certs["wz_same_source_action_cut"].get("root_certificate_cut_open", [])
        and certs["source_higgs_pole_row_contract"].get("canonical_oh_passed")
        is False
    )
    aggregate_denies_proposal = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = not any(FORBIDDEN_FIREWALL.values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposals, f"proposal_allowed={proposals}")
    report("neutral-transfer-current-route-blocked", neutral_blocked, statuses["neutral_source_mixing_no_go"])
    report("source-higgs-support-artifacts-present", oh_support, statuses["degree_one_radial_tangent_oh"])
    report("time-kernel-remains-support-only", time_kernel_support_only, statuses["source_higgs_time_kernel_gevp"])
    report("time-kernel-manifest-not-evidence", time_kernel_manifest_not_evidence, statuses["source_higgs_time_kernel_production_manifest"])
    report("os-transfer-kernel-physical-artifact-absent", os_transfer_absent, statuses["os_transfer_kernel_gate"])
    report("wz-support-contracts-present", wz_support, statuses["wz_response_ratio_contract"])
    report("common-canonical-oh-vertex-open", common_vertex_open, str(common["open_root_vertices"]))
    report("aggregate-gates-deny-proposal", aggregate_denies_proposal, "proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact support/boundary / canonical O_H and WZ accepted-action "
            "common-cut certificate; current surface remains open"
        ),
        "claim_type": "open_gate",
        "audit_status_authority": "independent audit lane only",
        "conditional_surface_status": (
            "exact-support if a future same-surface canonical O_H / accepted "
            "EW-Higgs action certificate lands; source-Higgs and WZ still need "
            "their separate production rows and authority gates"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This block only exposes the shared root vertex and route-specific "
            "data cuts.  The current surface still lacks canonical O_H, an "
            "accepted same-source EW/Higgs action, source-Higgs pole rows, "
            "W/Z response rows, matched covariance, strict g2, and aggregate "
            "retained-route approval."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "common_action_cut_passed": passed,
        "time_kernel_manifest_not_evidence": time_kernel_manifest_not_evidence,
        "neutral_current_route_blocked": neutral_blocked,
        "source_higgs_route_support": source_higgs_contract(),
        "wz_route_support": wz_contract(),
        "common_cut": common,
        "common_canonical_oh_vertex_open": common_vertex_open,
        "aggregate_denies_proposal": aggregate_denies_proposal,
        "ranked_next_actions": next_actions(),
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained closure",
            "does not write or validate the accepted same-source EW action certificate",
            "does not identify C_sx/C_xx with C_sH/C_HH before canonical O_H is certified",
            "does not treat the formal GEVP smoke as physical pole authority",
            "does not treat the time-kernel production manifest as launched rows or pole authority",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, or unit normalization conventions",
            "does not touch or relaunch the live chunk worker",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
