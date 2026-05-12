#!/usr/bin/env python3
"""
PR #230 W/Z absolute-authority route exhaustion after Block41.

Block36 selected strict W/Z accepted-action response as the active fallback
after the source-Higgs O_H/action route remained blocked.  Block39 then showed
that top/W/Z mass-plus-response rows self-normalize only ratios, not absolute
y_t.  This runner consumes the current W/Z parent surface and records the
route-level consequence: the current PR230 branch has support contracts and
no-go boundaries, but no accepted same-source action, production W/Z response
rows, matched top/W/Z covariance, strict non-observed g2 or v authority, or
final W/Z physical-response packet.

It is not a permanent W/Z no-go.  It is a current-surface exhaustion boundary:
reopen W/Z only with a real strict packet or a genuinely new absolute
normalization theorem.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_wz_absolute_authority_route_exhaustion_after_block41_2026-05-12.json"
)

PARENTS = {
    "block36_source_higgs_wz_dispatch": "outputs/yt_pr230_block36_source_higgs_wz_dispatch_checkpoint_2026-05-12.json",
    "wz_response_route_completion": "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json",
    "canonical_oh_wz_common_action_cut": "outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json",
    "wz_physical_response_packet_intake": "outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json",
    "wz_accepted_action_response_root": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "wz_response_ratio_identifiability_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "wz_same_source_action_minimal_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "wz_mass_response_self_normalization_no_go": "outputs/yt_pr230_wz_mass_response_self_normalization_no_go_2026-05-12.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_g2_response_self_normalization_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "wz_g2_bare_running_bridge_attempt": "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json",
    "electroweak_g2_certificate_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_correlator_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "wz_response_measurement_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
    "wz_response_row_production_attempt": "outputs/yt_wz_response_row_production_attempt_2026-05-03.json",
    "wz_harness_smoke_schema": "outputs/yt_pr230_wz_harness_smoke_schema_gate_2026-05-05.json",
    "wz_smoke_to_production_no_go": "outputs/yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json",
    "wz_source_coordinate_transport_no_go": "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json",
    "wz_goldstone_equivalence_source_identity_no_go": "outputs/yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json",
    "same_source_sector_overlap_identity_obstruction": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "top_wz_matched_covariance_certificate_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "top_wz_covariance_theorem_import_audit": "outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json",
    "top_wz_factorization_independence_gate": "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json",
    "same_source_wz_response_certificate_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
}

STRICT_WZ_PACKET_ROOTS = {
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "wz_correlator_mass_fit_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "same_source_top_response_certificate": "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
    "strict_electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "fh_gauge_mass_response_rows": "outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json",
    "fh_gauge_mass_response_certificate": "outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json",
    "top_wz_matched_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "delta_perp_correction_certificate": "outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json",
    "same_source_w_response_rows": "outputs/yt_same_source_w_response_rows_2026-05-04.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_y_t_bare": False,
    "used_observed_top_w_z_or_yt_selector": False,
    "used_observed_g2_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "used_static_ew_algebra_as_response_rows": False,
    "treated_scout_or_smoke_rows_as_production": False,
    "set_v_g2_c2_zmatch_or_kappa_by_unit_convention": False,
    "assumed_top_wz_covariance_or_factorization": False,
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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def present(rel: str) -> bool:
    return (ROOT / rel).exists()


def route_table(statuses: dict[str, str], packet_presence: dict[str, bool]) -> list[dict[str, Any]]:
    return [
        {
            "route": "strict W/Z physical-response packet",
            "current_surface_result": statuses["wz_physical_response_packet_intake"],
            "closes_current_surface": False,
            "remaining_import": "every strict packet root is absent",
            "missing_packet_roots": sorted(k for k, v in packet_presence.items() if not v),
        },
        {
            "route": "accepted same-source EW/Higgs action",
            "current_surface_result": statuses["wz_accepted_action_response_root"],
            "closes_current_surface": False,
            "remaining_import": "same-source action, sector overlap, canonical Higgs identity, and production W/Z mass-fit roots are open",
        },
        {
            "route": "W/Z response-ratio algebra",
            "current_surface_result": statuses["wz_response_ratio_identifiability_contract"],
            "closes_current_surface": False,
            "remaining_import": "ratio support requires missing production rows, covariance, strict g2, and accepted action",
        },
        {
            "route": "top/W/Z mass-plus-response self-normalization",
            "current_surface_result": statuses["wz_mass_response_self_normalization_no_go"],
            "closes_current_surface": False,
            "remaining_import": "mass+response rows still leave an absolute scale orbit without strict g2/v authority",
        },
        {
            "route": "strict non-observed g2 authority",
            "current_surface_result": statuses["wz_g2_authority_firewall"],
            "closes_current_surface": False,
            "remaining_import": "g2 builder inputs absent; response-only and bare-running shortcuts are blocked",
        },
        {
            "route": "production W/Z mass-fit and response rows",
            "current_surface_result": statuses["wz_mass_fit_response_row_builder"],
            "closes_current_surface": False,
            "remaining_import": "W/Z correlator mass-fit path and production row packet are absent",
        },
        {
            "route": "top/WZ covariance or factorization theorem",
            "current_surface_result": statuses["top_wz_matched_covariance_certificate_builder"],
            "closes_current_surface": False,
            "remaining_import": "matched rows absent; covariance import and factorization shortcuts are blocked",
        },
        {
            "route": "smoke/scout W/Z rows",
            "current_surface_result": statuses["wz_smoke_to_production_no_go"],
            "closes_current_surface": False,
            "remaining_import": "smoke/schema rows cannot be promoted to production W/Z evidence",
        },
    ]


def main() -> int:
    print("PR #230 W/Z absolute-authority route exhaustion after Block41")
    print("=" * 82)

    certs = {name: load(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    failing = [
        name
        for name, cert in certs.items()
        if int(cert.get("fail_count", cert.get("fails", 0)) or 0) != 0
    ]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    packet_presence = {name: present(path) for name, path in STRICT_WZ_PACKET_ROOTS.items()}
    routes = route_table(statuses, packet_presence)
    route_closures = [row for row in routes if row["closes_current_surface"]]

    block36_dispatch_not_closure = (
        "block36 source-Higgs route checkpointed and W/Z accepted-action response pivot selected"
        in statuses["block36_source_higgs_wz_dispatch"]
        and certs["block36_source_higgs_wz_dispatch"].get("proposal_allowed") is False
        and certs["block36_source_higgs_wz_dispatch"].get(
            "block36_source_higgs_wz_dispatch_checkpoint_passed"
        )
        is True
        and certs["block36_source_higgs_wz_dispatch"].get("checks", {}).get(
            "wz-pivot-not-admitted"
        )
        is True
    )
    wz_route_completion_blocks = (
        "WZ same-source response route not complete"
        in statuses["wz_response_route_completion"]
        and certs["wz_response_route_completion"].get(
            "wz_response_route_completion_passed"
        )
        is True
        and certs["wz_response_route_completion"].get("proposal_allowed") is False
    )
    common_action_cut_open = (
        "canonical O_H and WZ accepted-action common-cut"
        in statuses["canonical_oh_wz_common_action_cut"]
        and certs["canonical_oh_wz_common_action_cut"].get("common_action_cut_passed")
        is True
        and certs["canonical_oh_wz_common_action_cut"].get("proposal_allowed") is False
    )
    physical_packet_absent = (
        "WZ physical-response packet not present"
        in statuses["wz_physical_response_packet_intake"]
        and certs["wz_physical_response_packet_intake"].get(
            "wz_physical_response_packet_intake_checkpoint_passed"
        )
        is True
        and certs["wz_physical_response_packet_intake"].get(
            "production_packet_present"
        )
        is False
    )
    strict_packet_roots_absent = not any(packet_presence.values())
    action_root_absent = (
        "WZ accepted-action response root not closed"
        in statuses["wz_accepted_action_response_root"]
        and certs["wz_accepted_action_response_root"].get(
            "wz_accepted_action_response_root_checkpoint_passed"
        )
        is True
        and not certs["wz_accepted_action_response_root"].get("root_closures_found")
    )
    ratio_support_only = (
        "WZ response-ratio identifiability contract"
        in statuses["wz_response_ratio_identifiability_contract"]
        and certs["wz_response_ratio_identifiability_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and certs["wz_response_ratio_identifiability_contract"].get(
            "production_wz_response_rows_present"
        )
        is False
        and certs["wz_response_ratio_identifiability_contract"].get(
            "strict_g2_authority_present"
        )
        is False
    )
    same_source_action_cut_open = (
        "WZ accepted same-source action minimal certificate cut remains open"
        in statuses["wz_same_source_action_minimal_cut"]
        and certs["wz_same_source_action_minimal_cut"].get(
            "current_surface_action_certificate_satisfied"
        )
        is False
        and certs["wz_same_source_action_minimal_cut"].get("proposal_allowed") is False
    )
    mass_response_self_normalization_blocks = (
        certs["wz_mass_response_self_normalization_no_go"].get(
            "wz_mass_response_self_normalization_no_go_passed"
        )
        is True
        and certs["wz_mass_response_self_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
    )
    g2_authority_absent = (
        "WZ response g2 authority absent" in statuses["wz_g2_authority_firewall"]
        and certs["wz_g2_authority_firewall"].get("g2_authority_gate_passed")
        is False
        and certs["wz_g2_authority_firewall"].get("proposal_allowed") is False
    )
    g2_response_self_normalization_blocks = (
        certs["wz_g2_response_self_normalization_no_go"].get(
            "g2_response_self_normalization_no_go_passed"
        )
        is True
        and certs["wz_g2_response_self_normalization_no_go"].get(
            "proposal_allowed"
        )
        is False
    )
    g2_bare_running_blocks = (
        certs["wz_g2_bare_running_bridge_attempt"].get(
            "wz_g2_bare_running_bridge_passed"
        )
        is False
        and certs["wz_g2_bare_running_bridge_attempt"].get(
            "strict_electroweak_g2_certificate_written"
        )
        is False
        and certs["wz_g2_bare_running_bridge_attempt"].get(
            "exact_negative_boundary_passed"
        )
        is True
    )
    g2_builder_absent = (
        "electroweak g2 certificate builder inputs absent"
        in statuses["electroweak_g2_certificate_builder"]
        and certs["electroweak_g2_certificate_builder"].get(
            "strict_electroweak_g2_certificate_passed"
        )
        is False
    )
    wz_mass_fit_absent = (
        "WZ correlator mass-fit path absent" in statuses["wz_correlator_mass_fit_path"]
        and certs["wz_correlator_mass_fit_path"].get(
            "wz_correlator_mass_fit_path_ready"
        )
        is False
        and "WZ mass-fit response-row builder"
        in statuses["wz_mass_fit_response_row_builder"]
        and certs["wz_mass_fit_response_row_builder"].get(
            "strict_wz_mass_fit_response_row_builder_passed"
        )
        is False
    )
    row_contract_support_only = (
        "WZ response measurement-row contract gate"
        in statuses["wz_response_measurement_row_contract"]
        and certs["wz_response_measurement_row_contract"].get(
            "current_measurement_rows_present"
        )
        is False
        and certs["wz_response_measurement_row_contract"].get("proposal_allowed")
        is False
    )
    row_production_attempt_blocks = (
        "WZ response row production attempt"
        in statuses["wz_response_row_production_attempt"]
        and certs["wz_response_row_production_attempt"].get(
            "production_attempt_closes_pr230"
        )
        is False
        and certs["wz_response_row_production_attempt"].get(
            "raw_wz_correlator_path_present"
        )
        is False
    )
    smoke_rows_not_production = (
        "WZ harness smoke schema path" in statuses["wz_harness_smoke_schema"]
        and certs["wz_harness_smoke_schema"].get("wz_harness_smoke_schema_gate_passed")
        is True
        and certs["wz_smoke_to_production_no_go"].get(
            "wz_smoke_to_production_promotion_no_go_passed"
        )
        is True
    )
    source_identity_shortcuts_block = (
        certs["wz_source_coordinate_transport_no_go"].get(
            "wz_source_coordinate_transport_no_go_passed"
        )
        is True
        and certs["wz_goldstone_equivalence_source_identity_no_go"].get(
            "goldstone_equivalence_source_identity_no_go_passed"
        )
        is True
        and "same-source sector-overlap identity obstruction"
        in statuses["same_source_sector_overlap_identity_obstruction"]
    )
    covariance_absent = (
        "matched top-W response rows absent"
        in statuses["top_wz_matched_covariance_certificate_builder"]
        and certs["top_wz_matched_covariance_certificate_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
        and certs["top_wz_covariance_theorem_import_audit"].get(
            "covariance_theorem_import_audit_passed"
        )
        is True
        and certs["top_wz_covariance_theorem_import_audit"].get(
            "future_closed_covariance_theorem_present"
        )
        is False
        and "same-source top-W factorization not derived"
        in statuses["top_wz_factorization_independence_gate"]
    )
    same_source_wz_gate_open = (
        "same-source WZ response certificate gate not passed"
        in statuses["same_source_wz_response_certificate_gate"]
        and certs["same_source_wz_response_certificate_gate"].get(
            "same_source_wz_response_certificate_gate_passed"
        )
        is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    route_exhaustion_passed = all(
        [
            not missing,
            not failing,
            not proposal_parents,
            not route_closures,
            block36_dispatch_not_closure,
            wz_route_completion_blocks,
            common_action_cut_open,
            physical_packet_absent,
            strict_packet_roots_absent,
            action_root_absent,
            ratio_support_only,
            same_source_action_cut_open,
            mass_response_self_normalization_blocks,
            g2_authority_absent,
            g2_response_self_normalization_blocks,
            g2_bare_running_blocks,
            g2_builder_absent,
            wz_mass_fit_absent,
            row_contract_support_only,
            row_production_attempt_blocks,
            smoke_rows_not_production,
            source_identity_shortcuts_block,
            covariance_absent,
            same_source_wz_gate_open,
            firewall_clean,
        ]
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("parent-certificates-have-no-fails", not failing, f"failing={failing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("no-route-closes-current-surface", not route_closures, f"closures={route_closures}")
    report("block36-dispatch-not-closure", block36_dispatch_not_closure, statuses["block36_source_higgs_wz_dispatch"])
    report("wz-route-completion-blocks", wz_route_completion_blocks, statuses["wz_response_route_completion"])
    report("common-action-cut-open", common_action_cut_open, statuses["canonical_oh_wz_common_action_cut"])
    report("physical-packet-absent", physical_packet_absent, statuses["wz_physical_response_packet_intake"])
    report("strict-packet-roots-absent", strict_packet_roots_absent, str(packet_presence))
    report("accepted-action-root-absent", action_root_absent, statuses["wz_accepted_action_response_root"])
    report("ratio-contract-support-only", ratio_support_only, statuses["wz_response_ratio_identifiability_contract"])
    report("same-source-action-cut-open", same_source_action_cut_open, statuses["wz_same_source_action_minimal_cut"])
    report("mass-response-self-normalization-blocks", mass_response_self_normalization_blocks, statuses["wz_mass_response_self_normalization_no_go"])
    report("g2-authority-absent", g2_authority_absent, statuses["wz_g2_authority_firewall"])
    report("g2-response-self-normalization-blocks", g2_response_self_normalization_blocks, statuses["wz_g2_response_self_normalization_no_go"])
    report("g2-bare-running-blocks", g2_bare_running_blocks, statuses["wz_g2_bare_running_bridge_attempt"])
    report("g2-builder-absent", g2_builder_absent, statuses["electroweak_g2_certificate_builder"])
    report("wz-mass-fit-and-row-path-absent", wz_mass_fit_absent, statuses["wz_mass_fit_response_row_builder"])
    report("row-contract-support-only", row_contract_support_only, statuses["wz_response_measurement_row_contract"])
    report("row-production-attempt-blocks", row_production_attempt_blocks, statuses["wz_response_row_production_attempt"])
    report("smoke-rows-not-production", smoke_rows_not_production, statuses["wz_smoke_to_production_no_go"])
    report("source-identity-shortcuts-block", source_identity_shortcuts_block, statuses["same_source_sector_overlap_identity_obstruction"])
    report("covariance-absent", covariance_absent, statuses["top_wz_matched_covariance_certificate_builder"])
    report("same-source-wz-gate-open", same_source_wz_gate_open, statuses["same_source_wz_response_certificate_gate"])
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("wz-absolute-authority-route-exhaustion", route_exhaustion_passed, "current W/Z absolute-authority route exhausted without strict packet")

    result = {
        "actual_current_surface_status": (
            "support / exact negative boundary: W/Z absolute-authority "
            "current-surface route exhausted after Block41 without production "
            "W/Z rows and strict g2/v authority"
        ),
        "conditional_surface_status": (
            "conditional-support if a future strict W/Z physical-response packet "
            "supplies accepted action, production W/Z rows, same-source top rows, "
            "matched covariance, strict non-observed g2 or explicit v authority, "
            "delta_perp control, and aggregate retained-route approval"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Current W/Z artifacts are dispatch checkpoints, contracts, scout/smoke "
            "schemas, and no-go boundaries.  They do not supply the strict physical "
            "packet or an absolute g2/v normalization theorem, and the mass-plus-"
            "response shortcut leaves a scale orbit."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "wz_absolute_authority_route_exhaustion_passed": route_exhaustion_passed,
        "strict_packet_roots_present": packet_presence,
        "missing_strict_packet_roots": sorted(k for k, v in packet_presence.items() if not v),
        "route_table": routes,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "checks": {
            "parent-certificates-present": not missing,
            "parent-certificates-have-no-fails": not failing,
            "no-parent-authorizes-proposal": not proposal_parents,
            "no-route-closes-current-surface": not route_closures,
            "block36-dispatch-not-closure": block36_dispatch_not_closure,
            "wz-route-completion-blocks": wz_route_completion_blocks,
            "common-action-cut-open": common_action_cut_open,
            "physical-packet-absent": physical_packet_absent,
            "strict-packet-roots-absent": strict_packet_roots_absent,
            "accepted-action-root-absent": action_root_absent,
            "ratio-contract-support-only": ratio_support_only,
            "same-source-action-cut-open": same_source_action_cut_open,
            "mass-response-self-normalization-blocks": mass_response_self_normalization_blocks,
            "g2-authority-absent": g2_authority_absent,
            "g2-response-self-normalization-blocks": g2_response_self_normalization_blocks,
            "g2-bare-running-blocks": g2_bare_running_blocks,
            "g2-builder-absent": g2_builder_absent,
            "wz-mass-fit-and-row-path-absent": wz_mass_fit_absent,
            "row-contract-support-only": row_contract_support_only,
            "row-production-attempt-blocks": row_production_attempt_blocks,
            "smoke-rows-not-production": smoke_rows_not_production,
            "source-identity-shortcuts-block": source_identity_shortcuts_block,
            "covariance-absent": covariance_absent,
            "same-source-wz-gate-open": same_source_wz_gate_open,
            "forbidden-firewall-clean": firewall_clean,
        },
        "strict_non_claims": FORBIDDEN_FIREWALL,
        "remaining_positive_routes": [
            "same-surface neutral transfer primitive with physical H3/H4 transfer and source-Higgs coupling authority",
            "genuinely new W/Z production packet plus strict absolute g2/v authority",
            "genuinely new scalar/action/LSZ primitive not covered by Block41",
            "strict source-Higgs time-kernel rows after an accepted O_H/action theorem",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 and route_exhaustion_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
