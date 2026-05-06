#!/usr/bin/env python3
"""
PR #230 W/Z same-source response route completion gate.

The W/Z route is the cleanest physical-observable bypass of direct O_H: if the
same scalar source moves the top and W/Z sectors, then matched FH slopes plus a
strict non-observed g2 certificate can compute y_t without defining O_H.

This runner works that route to the current-surface boundary.  It verifies that
the required same-source EW action, W/Z mass-response rows, matched covariance,
strict g2, and orthogonal-scalar correction authority are absent.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_wz_response_route_completion_2026-05-06.json"

PARENTS = {
    "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "one_higgs_orthogonal_null": "outputs/yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json",
    "delta_perp_builder": "outputs/yt_delta_perp_tomography_correction_builder_2026-05-04.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "same_source_top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
    "same_source_w_row_builder": "outputs/yt_same_source_w_response_row_builder_2026-05-04.json",
    "wz_response_certificate_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "wz_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "wz_same_source_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_same_source_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "wz_source_coordinate_transport_no_go": "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json",
    "wz_goldstone_no_go": "outputs/yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "top_wz_covariance_marginal_no_go": "outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json",
    "top_wz_factorization_gate": "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json",
    "top_wz_deterministic_covariance_gate": "outputs/yt_top_wz_deterministic_response_covariance_gate_2026-05-05.json",
    "top_wz_covariance_import_audit": "outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json",
    "electroweak_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_g2_self_normalization_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "wz_g2_casimir_no_go": "outputs/yt_wz_g2_generator_casimir_normalization_no_go_2026-05-05.json",
    "wz_g2_bare_running_attempt": "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json",
    "candidate_portfolio": "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json",
}

FUTURE_ARTIFACTS = {
    "same_source_ew_action_certificate": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "wz_mass_fit_response_rows": "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
    "same_source_top_response_certificate": "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
    "top_wz_matched_covariance_certificate": "outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json",
    "electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
    "delta_perp_tomography_rows": "outputs/yt_delta_perp_tomography_rows_2026-05-04.json",
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


def load_rel(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in FUTURE_ARTIFACTS.items()}


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_static_ew_algebra_as_source_response": False,
        "used_observed_g2_or_w_mass": False,
        "used_hunit_matrix_element_readout": False,
        "used_yt_ward_identity": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "set_delta_perp_equal_zero_by_fiat": False,
        "assumed_top_w_covariance_or_factorization": False,
        "claimed_retained_or_proposed_retained": False,
    }


def main() -> int:
    print("PR #230 W/Z same-source response route completion gate")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    futures = future_presence()

    ratio_support_present = (
        "FH gauge-normalized response route" in statuses["fh_gauge_normalized_response"]
        and parents["fh_gauge_normalized_response"].get("proposal_allowed") is False
        and parents["fh_gauge_normalized_response"].get(
            "gauge_normalized_response_gate_passed"
        )
        is False
    )
    w_decomposition_support_only = (
        "same-source W-response decomposition theorem"
        in statuses["same_source_w_response_decomposition"]
        and parents["same_source_w_response_decomposition"].get("proposal_allowed")
        is False
    )
    orthogonal_control_absent = (
        "orthogonal-correction gate not passed"
        in statuses["same_source_w_orthogonal_correction"]
        and parents["same_source_w_orthogonal_correction"].get(
            "orthogonal_correction_gate_passed"
        )
        is False
        and "one-Higgs completeness orthogonal-null theorem"
        in statuses["one_higgs_orthogonal_null"]
        and parents["one_higgs_orthogonal_null"].get("proposal_allowed") is False
        and "delta_perp tomography correction production rows absent"
        in statuses["delta_perp_builder"]
        and parents["delta_perp_builder"].get("proposal_allowed") is False
        and not futures["delta_perp_tomography_rows"]
    )
    top_response_absent = (
        "same-source top-response identity or covariance inputs absent"
        in statuses["same_source_top_response_builder"]
        and parents["same_source_top_response_builder"].get(
            "strict_same_source_top_response_certificate_builder_passed"
        )
        is False
        and "same-source top-response identity blockers remain"
        in statuses["same_source_top_response_identity_builder"]
        and parents["same_source_top_response_identity_builder"].get("proposal_allowed")
        is False
        and not futures["same_source_top_response_certificate"]
    )
    w_rows_absent = (
        "same-source W-response row builder inputs absent"
        in statuses["same_source_w_row_builder"]
        and parents["same_source_w_row_builder"].get(
            "strict_same_source_w_response_row_builder_passed"
        )
        is False
        and "same-source WZ response certificate gate not passed"
        in statuses["wz_response_certificate_gate"]
        and parents["wz_response_certificate_gate"].get(
            "same_source_wz_response_certificate_gate_passed"
        )
        is False
        and not futures["wz_mass_fit_response_rows"]
    )
    wz_mass_fit_absent = (
        "WZ correlator mass-fit path absent" in statuses["wz_mass_fit_path"]
        and parents["wz_mass_fit_path"].get("wz_correlator_mass_fit_path_ready")
        is False
        and "WZ mass-fit response-row builder" in statuses["wz_mass_fit_response_row_builder"]
        and parents["wz_mass_fit_response_row_builder"].get(
            "strict_wz_mass_fit_response_row_builder_passed"
        )
        is False
    )
    same_source_action_absent = (
        "same-source EW action not defined" in statuses["wz_same_source_action_gate"]
        and parents["wz_same_source_action_gate"].get("same_source_ew_action_ready")
        is False
        and "same-source EW action certificate absent"
        in statuses["wz_same_source_action_builder"]
        and parents["wz_same_source_action_builder"].get(
            "same_source_ew_action_certificate_valid"
        )
        is False
        and not futures["same_source_ew_action_certificate"]
    )
    source_transport_shortcuts_closed = (
        parents["wz_source_coordinate_transport_no_go"].get(
            "wz_source_coordinate_transport_no_go_passed"
        )
        is True
        and parents["wz_goldstone_no_go"].get(
            "goldstone_equivalence_source_identity_no_go_passed"
        )
        is True
    )
    covariance_absent = (
        "matched top-W response rows absent" in statuses["top_wz_matched_covariance_builder"]
        and parents["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
        and parents["top_wz_covariance_marginal_no_go"].get(
            "marginal_derivation_no_go_passed"
        )
        is True
        and "same-source top-W factorization not derived"
        in statuses["top_wz_factorization_gate"]
        and parents["top_wz_factorization_gate"].get(
            "strict_factorization_independence_gate_passed"
        )
        is False
        and "deterministic W response covariance shortcut not derived"
        in statuses["top_wz_deterministic_covariance_gate"]
        and parents["top_wz_deterministic_covariance_gate"].get(
            "strict_deterministic_response_covariance_gate_passed"
        )
        is False
        and parents["top_wz_covariance_import_audit"].get(
            "covariance_theorem_import_audit_passed"
        )
        is True
        and parents["top_wz_covariance_import_audit"].get(
            "future_closed_covariance_theorem_present"
        )
        is False
        and not futures["top_wz_matched_covariance_certificate"]
    )
    strict_g2_absent = (
        "electroweak g2 certificate builder inputs absent"
        in statuses["electroweak_g2_builder"]
        and parents["electroweak_g2_builder"].get(
            "strict_electroweak_g2_certificate_passed"
        )
        is False
        and "WZ response g2 authority absent" in statuses["wz_g2_authority_firewall"]
        and parents["wz_g2_authority_firewall"].get("proposal_allowed") is False
        and parents["wz_g2_self_normalization_no_go"].get(
            "g2_response_self_normalization_no_go_passed"
        )
        is True
        and parents["wz_g2_casimir_no_go"].get(
            "g2_generator_casimir_no_go_passed"
        )
        is True
        and parents["wz_g2_bare_running_attempt"].get(
            "wz_g2_bare_running_bridge_passed"
        )
        is False
        and not futures["electroweak_g2_certificate"]
    )
    clean_firewall = all(value is False for value in forbidden_firewall().values())

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("ratio-support-present-but-not-closure", ratio_support_present, statuses["fh_gauge_normalized_response"])
    report("w-decomposition-support-only", w_decomposition_support_only, statuses["same_source_w_response_decomposition"])
    report("orthogonal-control-absent", orthogonal_control_absent, statuses["same_source_w_orthogonal_correction"])
    report("same-source-top-response-absent", top_response_absent, statuses["same_source_top_response_builder"])
    report("same-source-wz-rows-absent", w_rows_absent, statuses["wz_response_certificate_gate"])
    report("wz-mass-fit-rows-absent", wz_mass_fit_absent, statuses["wz_mass_fit_response_row_builder"])
    report("same-source-ew-action-absent", same_source_action_absent, statuses["wz_same_source_action_gate"])
    report("source-transport-shortcuts-closed", source_transport_shortcuts_closed, statuses["wz_source_coordinate_transport_no_go"])
    report("matched-top-w-covariance-absent", covariance_absent, statuses["top_wz_matched_covariance_builder"])
    report("strict-nonobserved-g2-absent", strict_g2_absent, statuses["electroweak_g2_builder"])
    report("forbidden-firewall-clean", clean_firewall, str(forbidden_firewall()))

    exact_negative_boundary_passed = (
        not missing
        and not proposal_allowed
        and ratio_support_present
        and w_decomposition_support_only
        and orthogonal_control_absent
        and top_response_absent
        and w_rows_absent
        and wz_mass_fit_absent
        and same_source_action_absent
        and source_transport_shortcuts_closed
        and covariance_absent
        and strict_g2_absent
        and clean_firewall
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / WZ same-source response route not complete on current PR230 surface"
        ),
        "conditional_surface_status": (
            "The W/Z physical-response bypass can reopen only with a same-source "
            "EW action, production W/Z mass-response rows, matched top/W "
            "covariance or identity, strict non-observed g2, and delta_perp/"
            "orthogonal-scalar control."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Current W/Z artifacts are support, manifests, and no-go boundaries. "
            "No strict W/Z physical response packet exists."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "wz_response_route_completion_passed": exact_negative_boundary_passed,
        "exact_negative_boundary_passed": exact_negative_boundary_passed,
        "future_artifact_presence": futures,
        "blocked_requirements": {
            "same_source_ew_action": same_source_action_absent,
            "wz_mass_fit_response_rows": w_rows_absent or wz_mass_fit_absent,
            "same_source_top_response": top_response_absent,
            "matched_top_w_covariance": covariance_absent,
            "strict_nonobserved_g2": strict_g2_absent,
            "delta_perp_or_orthogonal_control": orthogonal_control_absent,
        },
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": forbidden_firewall(),
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use static EW algebra as a source-response measurement",
            "does not use observed g2, W/Z masses, H_unit, yt_ward_identity, alpha_LM, plaquette, or u0",
            "does not set delta_perp=0 or assume top/W covariance by convention",
        ],
        "exact_next_action": (
            "Treat W/Z same-source response as closed on the current surface. "
            "Move next to Schur A/B/C rows or the neutral primitive/rank-one "
            "theorem unless a real W/Z response packet appears."
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
