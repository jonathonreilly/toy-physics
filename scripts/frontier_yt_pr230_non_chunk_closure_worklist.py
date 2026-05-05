#!/usr/bin/env python3
"""
PR #230 non-chunk closure worklist gate.

This runner is the integration checkpoint for the user's "do the non-chunk
work" request.  It does not package MC chunks and it does not claim closure.
It verifies that every live non-chunk route is either represented by a strict
gate/no-go/support artifact or requires a named future certificate/data surface.

The point is to prevent a hidden shortcut from being missed while the chunk
worker continues production.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_non_chunk_closure_worklist_2026-05-05.json"

PARENTS = {
    "assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "canonical_oh_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_oh_realization": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "canonical_oh_semantic_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
    "fms_oh_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "cross_lane_oh": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "source_higgs_contract": "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json",
    "source_higgs_unratified_gram_no_go": "outputs/yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json",
    "wz_same_source_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_same_source_action_firewall": "outputs/yt_wz_same_source_ew_action_semantic_firewall_2026-05-04.json",
    "wz_source_coordinate_transport_no_go": "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json",
    "wz_goldstone_equivalence_no_go": "outputs/yt_wz_goldstone_equivalence_source_identity_no_go_2026-05-05.json",
    "same_source_w_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_orthogonal": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "delta_perp_builder": "outputs/yt_delta_perp_tomography_correction_builder_2026-05-04.json",
    "top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
    "top_wz_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "top_wz_covariance_marginal_no_go": "outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json",
    "top_wz_factorization_gate": "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json",
    "top_wz_deterministic_response_covariance_gate": "outputs/yt_top_wz_deterministic_response_covariance_gate_2026-05-05.json",
    "wz_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_rows": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "same_source_w_rows": "outputs/yt_same_source_w_response_row_builder_2026-05-04.json",
    "same_source_w_readout": "outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json",
    "electroweak_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_casimir_no_go": "outputs/yt_wz_g2_generator_casimir_normalization_no_go_2026-05-05.json",
    "wz_g2_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "wz_g2_self_norm_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "lsz_model_class": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "lsz_model_class_firewall": "outputs/yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json",
    "lsz_stieltjes_obstruction": "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json",
    "lsz_stieltjes_moment_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "lsz_pade_stieltjes_bounds": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "lsz_polefit8x8_stieltjes_proxy_diagnostic": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "lsz_contact_subtraction_identifiability": "outputs/yt_fh_lsz_contact_subtraction_identifiability_2026-05-05.json",
    "lsz_affine_contact_complete_monotonicity": "outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json",
    "lsz_polynomial_contact_finite_shell": "outputs/yt_fh_lsz_polynomial_contact_finite_shell_no_go_2026-05-05.json",
    "lsz_polynomial_contact_repair": "outputs/yt_fh_lsz_polynomial_contact_repair_no_go_2026-05-05.json",
    "nonchunk_route_family_import_audit": "outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json",
    "lsz_pole_saturation": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "lsz_threshold_authority": "outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json",
    "lsz_fv_obstruction": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "lsz_soft_continuum": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "scalar_denominator_attempt": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "kprime_attempt": "outputs/yt_kprime_closure_attempt_2026-05-02.json",
    "schur_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_absence": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_contract": "outputs/yt_schur_kernel_row_contract_gate_2026-05-03.json",
    "schur_candidate_extraction": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
    "neutral_rank_one": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "neutral_commutant_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "neutral_dynamic_attempt": "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json",
    "neutral_irreducibility_audit": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
    "neutral_primitive_cone_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "neutral_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "matching_running": "outputs/yt_pr230_matching_running_bridge_gate_2026-05-04.json",
}

FUTURE_FILES = {
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "stieltjes_moment_certificate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json",
    "pade_stieltjes_bounds_certificate": "outputs/yt_fh_lsz_pade_stieltjes_bounds_certificate_2026-05-05.json",
    "contact_subtraction_certificate": "outputs/yt_fh_lsz_contact_subtraction_certificate_2026-05-05.json",
    "polynomial_contact_certificate": "outputs/yt_fh_lsz_polynomial_contact_certificate_2026-05-05.json",
    "matched_top_wz_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "deterministic_response_covariance_certificate": "outputs/yt_top_wz_deterministic_response_covariance_certificate_2026-05-05.json",
    "source_coordinate_transport_certificate": "outputs/yt_wz_source_coordinate_transport_certificate_2026-05-05.json",
    "wz_mass_response_rows": "outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json",
    "non_observed_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-05.json",
    "delta_perp_rows": "outputs/yt_delta_perp_tomography_rows_2026-05-04.json",
    "schur_kernel_rows": "outputs/yt_schur_kernel_rows_2026-05-03.json",
    "neutral_irreducibility_certificate": "outputs/yt_neutral_scalar_irreducibility_certificate_2026-05-04.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "certified_physical_readout": "outputs/yt_pr230_certified_physical_readout_2026-05-04.json",
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


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def all_false(certs: dict[str, dict[str, Any]]) -> bool:
    return not [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]


def work_units(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": "canonical_oh_source_higgs",
            "kind": "non_chunk_or_new_surface_then_rows",
            "current_state": "blocked",
            "remaining": [
                FUTURE_FILES["canonical_oh_certificate"],
                FUTURE_FILES["source_higgs_rows"],
            ],
            "current_blockers": [
                status(certs["canonical_oh_gate"]),
                status(certs["fms_oh_attempt"]),
                status(certs["cross_lane_oh"]),
                status(certs["canonical_oh_premise_stretch"]),
                status(certs["source_higgs_readiness"]),
                status(certs["source_higgs_unratified_gram_no_go"]),
            ],
            "next_action": (
                "derive a same-surface O_H certificate or introduce a reviewed EW "
                "gauge-Higgs production surface; then produce C_ss/C_sH/C_HH rows"
            ),
        },
        {
            "id": "same_source_wz_response",
            "kind": "new_measurement_rows_or_new_theorem",
            "current_state": "blocked",
            "remaining": [
                FUTURE_FILES["matched_top_wz_rows"],
                FUTURE_FILES["deterministic_response_covariance_certificate"],
                FUTURE_FILES["source_coordinate_transport_certificate"],
                FUTURE_FILES["wz_mass_response_rows"],
                FUTURE_FILES["non_observed_g2_certificate"],
                FUTURE_FILES["delta_perp_rows"],
            ],
            "current_blockers": [
                status(certs["wz_same_source_action"]),
                status(certs["top_wz_covariance_marginal_no_go"]),
                status(certs["top_wz_factorization_gate"]),
                status(certs["top_wz_deterministic_response_covariance_gate"]),
                status(certs["wz_source_coordinate_transport_no_go"]),
                status(certs["wz_goldstone_equivalence_no_go"]),
                status(certs["electroweak_g2_builder"]),
                status(certs["wz_g2_casimir_no_go"]),
                status(certs["wz_g2_firewall"]),
                status(certs["wz_g2_self_norm_no_go"]),
            ],
            "next_action": (
                "produce matched top/WZ response rows and non-observed g2 authority, "
                "or derive a strict product-measure/conditional-independence/closed-covariance "
                "theorem plus source-coordinate transport authority"
            ),
        },
        {
            "id": "scalar_lsz_model_fv_ir",
            "kind": "non_chunk_theorem_or_strict_certificate",
            "current_state": "blocked",
            "remaining": [
                FUTURE_FILES["stieltjes_moment_certificate"],
                FUTURE_FILES["pade_stieltjes_bounds_certificate"],
                FUTURE_FILES["contact_subtraction_certificate"],
                FUTURE_FILES["polynomial_contact_certificate"],
            ],
            "current_blockers": [
                status(certs["lsz_model_class"]),
                status(certs["lsz_stieltjes_obstruction"]),
                status(certs["lsz_stieltjes_moment_gate"]),
                status(certs["lsz_pade_stieltjes_bounds"]),
                status(certs["lsz_polefit8x8_stieltjes_proxy_diagnostic"]),
                status(certs["lsz_contact_subtraction_identifiability"]),
                status(certs["lsz_affine_contact_complete_monotonicity"]),
                status(certs["lsz_polynomial_contact_finite_shell"]),
                status(certs["lsz_polynomial_contact_repair"]),
                status(certs["lsz_pole_saturation"]),
                status(certs["lsz_fv_obstruction"]),
                status(certs["lsz_soft_continuum"]),
                status(certs["scalar_denominator_attempt"]),
            ],
            "next_action": (
                "produce a strict Stieltjes moment certificate, derive a scalar "
                "denominator/analytic-continuation theorem, or prove a uniform "
                "threshold/FV/IR pole-saturation bound"
            ),
        },
        {
            "id": "schur_scalar_denominator_rows",
            "kind": "same_surface_kernel_rows",
            "current_state": "blocked",
            "remaining": [FUTURE_FILES["schur_kernel_rows"]],
            "current_blockers": [
                status(certs["schur_sufficiency"]),
                status(certs["schur_absence"]),
                status(certs["schur_contract"]),
                status(certs["schur_candidate_extraction"]),
                status(certs["kprime_attempt"]),
            ],
            "next_action": "supply same-surface Schur A/B/C kernel rows; FH/LSZ source rows do not substitute",
        },
        {
            "id": "neutral_scalar_rank_one",
            "kind": "new_irreducibility_theorem",
            "current_state": "blocked",
            "remaining": [
                FUTURE_FILES["neutral_irreducibility_certificate"],
                FUTURE_FILES["neutral_primitive_cone_certificate"],
            ],
            "current_blockers": [
                status(certs["neutral_rank_one"]),
                status(certs["neutral_commutant_no_go"]),
                status(certs["neutral_dynamic_attempt"]),
                status(certs["neutral_irreducibility_audit"]),
                status(certs["neutral_primitive_cone_gate"]),
                status(certs["neutral_primitive_cone_stretch_no_go"]),
            ],
            "next_action": (
                "derive primitive-cone/positivity-improving irreducibility for the "
                "neutral top-coupled scalar sector"
            ),
        },
        {
            "id": "matching_running",
            "kind": "downstream_bridge_after_physical_readout",
            "current_state": "blocked",
            "remaining": [FUTURE_FILES["certified_physical_readout"]],
            "current_blockers": [status(certs["matching_running"])],
            "next_action": "rerun only after production + scalar-LSZ + physical overlap/readout are certified",
        },
    ]


def main() -> int:
    print("PR #230 non-chunk closure worklist gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    future_present = {name: exists(rel) for name, rel in FUTURE_FILES.items()}
    units = work_units(certs)
    closed_units = [unit["id"] for unit in units if unit["current_state"] == "closed"]
    blocked_units = [unit["id"] for unit in units if unit["current_state"] == "blocked"]
    future_files_absent = [name for name, present in future_present.items() if not present]
    future_files_present = [name for name, present in future_present.items() if present]

    assembly_missing = certs["assembly"].get("current_evaluation", {}).get("missing", [])
    chunk_only_missing = certs["assembly"].get("chunk_only_evaluation", {}).get("missing", [])
    all_parent_proposals_false = all_false(certs)
    no_future_strict_files = not future_files_present

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed and all_parent_proposals_false, f"proposal_allowed={proposal_allowed}")
    report("assembly-still-rejects-current-surface", "scalar_lsz_model_class_fv_ir" in assembly_missing, f"missing={assembly_missing}")
    report("assembly-still-rejects-chunk-only", "scalar_lsz_model_class_fv_ir" in chunk_only_missing, f"missing={chunk_only_missing}")
    report("canonical-oh-route-gated", "canonical-Higgs operator certificate absent" in status(certs["canonical_oh_gate"]), status(certs["canonical_oh_gate"]))
    report("canonical-oh-premise-stretch-gated", "same-surface O_H identity and normalization" in status(certs["canonical_oh_premise_stretch"]), status(certs["canonical_oh_premise_stretch"]))
    report("source-higgs-route-gated", "source-Higgs production launch blocked" in status(certs["source_higgs_readiness"]), status(certs["source_higgs_readiness"]))
    report("source-higgs-unratified-gram-shortcut-closed", "unratified source-Higgs Gram shortcut" in status(certs["source_higgs_unratified_gram_no_go"]), status(certs["source_higgs_unratified_gram_no_go"]))
    report("wz-route-gated", "same-source EW action not defined" in status(certs["wz_same_source_action"]), status(certs["wz_same_source_action"]))
    report(
        "wz-source-coordinate-transport-shortcut-closed",
        "WZ source-coordinate transport shortcut rejected"
        in status(certs["wz_source_coordinate_transport_no_go"])
        and certs["wz_source_coordinate_transport_no_go"].get("proposal_allowed") is False
        and certs["wz_source_coordinate_transport_no_go"].get(
            "wz_source_coordinate_transport_no_go_passed"
        )
        is True,
        status(certs["wz_source_coordinate_transport_no_go"]),
    )
    report(
        "wz-goldstone-equivalence-shortcut-closed",
        "Goldstone equivalence does not identify PR230 source coordinate"
        in status(certs["wz_goldstone_equivalence_no_go"])
        and certs["wz_goldstone_equivalence_no_go"].get("proposal_allowed") is False
        and certs["wz_goldstone_equivalence_no_go"].get(
            "goldstone_equivalence_source_identity_no_go_passed"
        )
        is True,
        status(certs["wz_goldstone_equivalence_no_go"]),
    )
    report("wz-deterministic-response-shortcut-gated", "deterministic W response covariance shortcut not derived" in status(certs["top_wz_deterministic_response_covariance_gate"]), status(certs["top_wz_deterministic_response_covariance_gate"]))
    report("wz-g2-shortcuts-closed", "does not certify PR230 g2" in status(certs["wz_g2_casimir_no_go"]) and "response-only" in status(certs["wz_g2_self_norm_no_go"]), "Casimir and response-only g2 shortcuts rejected")
    report("scalar-lsz-route-gated", "Stieltjes moment-certificate gate" in status(certs["lsz_stieltjes_moment_gate"]), status(certs["lsz_stieltjes_moment_gate"]))
    report("pade-stieltjes-route-gated", "Pade-Stieltjes bounds gate" in status(certs["lsz_pade_stieltjes_bounds"]), status(certs["lsz_pade_stieltjes_bounds"]))
    report("scalar-lsz-current-proxy-blocked", "Stieltjes monotonicity" in status(certs["lsz_polefit8x8_stieltjes_proxy_diagnostic"]), status(certs["lsz_polefit8x8_stieltjes_proxy_diagnostic"]))
    report("contact-subtraction-route-gated", "contact-subtraction identifiability obstruction" in status(certs["lsz_contact_subtraction_identifiability"]), status(certs["lsz_contact_subtraction_identifiability"]))
    report("affine-contact-complete-monotonicity-route-gated", "affine contact complete-monotonicity no-go" in status(certs["lsz_affine_contact_complete_monotonicity"]), status(certs["lsz_affine_contact_complete_monotonicity"]))
    report("polynomial-contact-finite-shell-route-gated", "finite-shell polynomial contact non-identifiability no-go" in status(certs["lsz_polynomial_contact_finite_shell"]), status(certs["lsz_polynomial_contact_finite_shell"]))
    report("polynomial-contact-repair-route-gated", "polynomial contact repair not scalar-LSZ authority" in status(certs["lsz_polynomial_contact_repair"]), status(certs["lsz_polynomial_contact_repair"]))
    report(
        "route-family-import-audit-refreshed",
        "non-chunk route-family import audit" in status(certs["nonchunk_route_family_import_audit"])
        and certs["nonchunk_route_family_import_audit"].get("proposal_allowed") is False,
        status(certs["nonchunk_route_family_import_audit"]),
    )
    report("schur-route-gated", "Schur K-prime row absence guard" in status(certs["schur_absence"]), status(certs["schur_absence"]))
    report("neutral-rank-one-route-gated", "irreducibility authority absent" in status(certs["neutral_irreducibility_audit"]), status(certs["neutral_irreducibility_audit"]))
    report("neutral-primitive-cone-route-gated", "primitive-cone certificate gate" in status(certs["neutral_primitive_cone_gate"]), status(certs["neutral_primitive_cone_gate"]))
    report(
        "neutral-primitive-cone-stretch-closed-negatively",
        "primitive-cone stretch no-go" in status(certs["neutral_primitive_cone_stretch_no_go"])
        and certs["neutral_primitive_cone_stretch_no_go"].get("primitive_cone_stretch_no_go_passed") is True,
        status(certs["neutral_primitive_cone_stretch_no_go"]),
    )
    report("matching-running-awaits-certified-input", "awaits certified physical input" in status(certs["matching_running"]), status(certs["matching_running"]))
    report("all-future-strict-files-currently-absent", no_future_strict_files, f"present={future_files_present}")
    report("all-non-chunk-work-units-blocked-not-hidden", len(blocked_units) == len(units) and not closed_units, f"blocked={blocked_units}")
    report("does-not-authorize-proposed-retained", True, "worklist is an open-state integration gate")

    result = {
        "actual_current_surface_status": "open / PR230 non-chunk closure worklist complete; positive closure still blocked",
        "verdict": (
            "All current non-chunk routes are now represented by explicit gates, "
            "support artifacts, or no-go certificates.  No loaded parent "
            "authorizes proposed_retained.  The remaining work is not another "
            "hidden branch-local shortcut; it requires one of the named future "
            "same-surface certificates, measurement-row files, or new theorems "
            "listed in this worklist."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Current and chunk-only assembly are rejected.  The strict future "
            "files for O_H/source-Higgs, scalar-LSZ, W/Z response, Schur rows, "
            "neutral irreducibility, and certified physical readout are absent."
        ),
        "bare_retained_allowed": False,
        "work_units": units,
        "future_file_presence": future_present,
        "blocked_work_unit_ids": blocked_units,
        "closed_work_unit_ids": closed_units,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not package or certify chunk outputs",
            "does not define y_t_bare",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, u0, observed targets, or unit shortcuts",
            "does not turn support/no-go gates into physical y_t evidence",
        ],
        "exact_next_action": (
            "After the W/Z source-coordinate transport no-go, the W/Z Goldstone-"
            "equivalence source-identity no-go, and the neutral primitive-cone "
            "stretch no-go, do not spend another block on source-only or "
            "static-label shortcuts.  The next positive route requires a new "
            "strict same-surface artifact: O_H/C_sH/C_HH pole rows, W/Z response "
            "rows with identities and covariance authority, scalar-LSZ moment/"
            "threshold/FV authority, Schur A/B/C kernel rows, or a neutral "
            "primitive-cone certificate."
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
