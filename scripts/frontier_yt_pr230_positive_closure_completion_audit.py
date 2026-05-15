#!/usr/bin/env python3
"""
PR #230 positive-closure completion audit.

This runner maps the live objective, "resume positive closure on PR #230",
to concrete artifacts on the branch.  It is not a physics proof and it does
not claim closure.  Its purpose is to make the current completion status
executable: chunks may be complete, but retained/proposed-retained top-Yukawa
closure still requires scalar-LSZ authority, one physical source-overlap or
W/Z response bridge, matching/running authority, and retained-route approval.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_positive_closure_completion_audit_2026-05-05.json"

PARENTS = {
    "genuine_source_pole_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
    "taste_condensate_oh_bridge": "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json",
    "source_coordinate_transport_gate": "outputs/yt_pr230_source_coordinate_transport_gate_2026-05-06.json",
    "origin_main_composite_higgs_intake_guard": "outputs/yt_pr230_origin_main_composite_higgs_intake_guard_2026-05-06.json",
    "origin_main_ew_m_residual_intake_guard": "outputs/yt_pr230_origin_main_ew_m_residual_intake_guard_2026-05-06.json",
    "z3_triplet_conditional_primitive_cone": "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json",
    "z3_triplet_positive_cone_support": "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json",
    "z3_generation_action_lift_attempt": "outputs/yt_pr230_z3_generation_action_lift_attempt_2026-05-06.json",
    "z3_lazy_transfer_promotion_attempt": "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json",
    "z3_heat_kernel_neutral_transfer_attempt": "outputs/yt_pr230_z3_heat_kernel_neutral_transfer_attempt_2026-05-15.json",
    "two_source_taste_radial_chart": "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json",
    "two_source_taste_radial_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_taste_radial_row_contract": "outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json",
    "two_source_taste_radial_row_production_manifest": "outputs/yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json",
    "two_source_taste_radial_chunk_package": "outputs/yt_pr230_two_source_taste_radial_chunk_package_audit_2026-05-06.json",
    "source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "taste_radial_canonical_oh_selector_gate": "outputs/yt_pr230_taste_radial_canonical_oh_selector_gate_2026-05-06.json",
    "degree_one_higgs_action_premise_gate": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "degree_one_radial_tangent_oh_theorem": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "taste_radial_to_source_higgs_promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "fms_post_degree_route_rescore": "outputs/yt_pr230_fms_post_degree_route_rescore_2026-05-06.json",
    "fms_composite_oh_conditional_theorem": "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json",
    "fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_source_overlap_readout_gate": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
    "fms_action_adoption_minimal_cut": "outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json",
    "higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "additive_source_radial_spurion_incompatibility": "outputs/yt_pr230_additive_source_radial_spurion_incompatibility_2026-05-07.json",
    "additive_top_subtraction_row_contract": "outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json",
    "top_mass_scan_response_harness_gate": "outputs/yt_pr230_top_mass_scan_response_harness_gate_2026-05-12.json",
    "wz_response_ratio_identifiability_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "wz_same_source_action_minimal_certificate_cut": "outputs/yt_pr230_wz_same_source_action_minimal_certificate_cut_2026-05-07.json",
    "wz_accepted_action_response_root_checkpoint": "outputs/yt_pr230_wz_accepted_action_response_root_checkpoint_2026-05-07.json",
    "canonical_oh_wz_common_action_cut": "outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json",
    "canonical_oh_accepted_action_stretch_attempt": "outputs/yt_pr230_canonical_oh_accepted_action_stretch_attempt_2026-05-07.json",
    "post_fms_source_overlap_necessity_gate": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "same_surface_neutral_multiplicity_one_gate": "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json",
    "os_transfer_kernel_artifact_gate": "outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json",
    "source_higgs_time_kernel_harness_extension_gate": "outputs/yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json",
    "source_higgs_time_kernel_gevp_contract": "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json",
    "source_higgs_time_kernel_production_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
    "fms_literature_source_overlap_intake": "outputs/yt_pr230_fms_literature_source_overlap_intake_2026-05-07.json",
    "schur_higher_shell_production_contract": "outputs/yt_pr230_schur_higher_shell_production_contract_2026-05-07.json",
    "schur_higher_shell_complete_packet_monotonicity": "outputs/yt_pr230_schur_higher_shell_complete_packet_monotonicity_gate_2026-05-15.json",
    "two_source_taste_radial_primitive_transfer_candidate_gate": "outputs/yt_pr230_two_source_taste_radial_primitive_transfer_candidate_gate_2026-05-07.json",
    "orthogonal_top_coupling_exclusion_candidate_gate": "outputs/yt_pr230_orthogonal_top_coupling_exclusion_candidate_gate_2026-05-07.json",
    "strict_scalar_lsz_moment_fv_authority_gate": "outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json",
    "schur_complement_stieltjes_repair_gate": "outputs/yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json",
    "schur_complement_complete_monotonicity_gate": "outputs/yt_pr230_schur_complement_complete_monotonicity_gate_2026-05-07.json",
    "schur_x_given_source_one_pole_scout": "outputs/yt_pr230_schur_x_given_source_one_pole_scout_2026-05-07.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "matching_running": "outputs/yt_pr230_matching_running_bridge_gate_2026-05-04.json",
    "wz_smoke_promotion_no_go": "outputs/yt_pr230_wz_smoke_to_production_promotion_no_go_2026-05-05.json",
    "wz_same_source_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "electroweak_g2_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_v_authority_firewall": "outputs/yt_pr230_wz_v_authority_firewall_2026-05-15.json",
    "post_block100_completion_reopen_audit": "outputs/yt_pr230_post_block100_completion_reopen_audit_2026-05-15.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "schur_kprime_rows": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "neutral_primitive_cone": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "fh_lsz_stieltjes_moment": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "fh_lsz_pade_stieltjes": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
}

FUTURE_BRIDGE_FILES = {
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_coordinate_transport_certificate": "outputs/yt_pr230_source_coordinate_transport_certificate_2026-05-06.json",
    "source_higgs_cross_correlator_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "two_source_taste_radial_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_taste_radial_rows": "outputs/yt_pr230_two_source_taste_radial_measurement_rows_2026-05-06.json",
    "top_wz_matched_response_rows": "outputs/yt_top_wz_matched_response_rows_2026-05-04.json",
    "schur_abc_kernel_rows": "outputs/yt_schur_abc_kernel_rows_2026-05-05.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "carleman_tauberian_certificate": "outputs/yt_fh_lsz_carleman_tauberian_certificate_2026-05-05.json",
}

PRODUCTION_PATTERN = "outputs/yt_pr230_fh_lsz_production_L12_T24_chunk*_2026-05-01.json"
POLEFIT_PATTERN = "outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk*_2026-05-04.json"

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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def chunk_id(path: Path) -> str | None:
    match = re.search(r"_chunk(\d{3})_", path.name)
    return match.group(1) if match else None


def chunk_paths(pattern: str) -> list[Path]:
    return sorted(path for path in ROOT.glob(pattern) if "chunked_combined" not in path.name)


def mode_rows_have_timeseries(rows: Any) -> bool:
    if isinstance(rows, dict):
        iterable = rows.values()
    elif isinstance(rows, list):
        iterable = rows
    else:
        return False
    row_list = [row for row in iterable if isinstance(row, dict)]
    return bool(row_list) and all("C_ss_timeseries" in row for row in row_list)


def chunk_schema_summary(paths: list[Path]) -> dict[str, Any]:
    missing_source_energy = []
    missing_source_slopes = []
    missing_lsz_timeseries = []
    bad_seed = []
    unreadable = []
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - defensive certificate path
            unreadable.append({"path": str(path.relative_to(ROOT)), "error": str(exc)})
            continue
        ensembles = data.get("ensembles", [])
        ensemble = ensembles[0] if isinstance(ensembles, list) and ensembles else {}
        source = ensemble.get("scalar_source_response_analysis", {}) if isinstance(ensemble, dict) else {}
        lsz = ensemble.get("scalar_two_point_lsz_analysis", {}) if isinstance(ensemble, dict) else {}
        seed = ensemble.get("rng_seed_control", {}) if isinstance(ensemble, dict) else {}
        rel = str(path.relative_to(ROOT))
        if "per_configuration_effective_energies" not in source:
            missing_source_energy.append(rel)
        if "per_configuration_slopes" not in source:
            missing_source_slopes.append(rel)
        if not mode_rows_have_timeseries(lsz.get("mode_rows")):
            missing_lsz_timeseries.append(rel)
        if seed.get("seed_control_version") != "numba_gauge_seed_v1":
            bad_seed.append(rel)
    return {
        "unreadable": unreadable,
        "missing_source_effective_energies": missing_source_energy,
        "missing_source_slopes": missing_source_slopes,
        "missing_lsz_C_ss_timeseries": missing_lsz_timeseries,
        "bad_seed_control": bad_seed,
        "schema_ok": not (
            unreadable
            or missing_source_energy
            or missing_source_slopes
            or missing_lsz_timeseries
            or bad_seed
        ),
    }


def chunk_family_summary(pattern: str) -> dict[str, Any]:
    paths = chunk_paths(pattern)
    ids = sorted(chunk_id(path) for path in paths if chunk_id(path))
    expected = [f"{index:03d}" for index in range(1, 64)]
    missing = [cid for cid in expected if cid not in ids]
    extra = [cid for cid in ids if cid not in expected]
    schema = chunk_schema_summary(paths)
    return {
        "count": len(ids),
        "expected_count": 63,
        "missing_ids": missing,
        "extra_ids": extra,
        "complete_id_set": len(ids) == 63 and not missing and not extra,
        "schema": schema,
        "complete_with_schema": len(ids) == 63 and not missing and not extra and schema["schema_ok"],
    }


def main() -> int:
    print("PR #230 positive-closure completion audit")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    parent_statuses = {name: status(cert) for name, cert in certs.items()}
    future_bridge_presence = {
        name: (ROOT / path).exists() for name, path in FUTURE_BRIDGE_FILES.items()
    }

    production = chunk_family_summary(PRODUCTION_PATTERN)
    polefit = chunk_family_summary(POLEFIT_PATTERN)
    assembly = certs["full_positive_assembly"]
    current_eval = assembly.get("current_evaluation", {})
    chunk_eval = assembly.get("chunk_only_evaluation", {})
    route_statuses = assembly.get("route_statuses", {})
    genuine_source_pole = certs["genuine_source_pole_intake"]

    source_pole_intaken = (
        genuine_source_pole.get("artifact_is_genuine_current_surface_support") is True
        and genuine_source_pole.get("artifact_is_physics_closure") is False
        and genuine_source_pole.get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and not future_bridge_presence["canonical_higgs_operator_certificate"]
    )
    osp_higgs_rows_absent = (
        certs["source_higgs_builder"].get("input_present") is False
        and certs["source_higgs_builder"].get("candidate_written") is False
        and certs["source_higgs_postprocess"].get("candidate_present") is False
        and certs["source_higgs_postprocess"].get("osp_higgs_gram_purity_gate_passed")
        is False
        and not future_bridge_presence["source_higgs_cross_correlator_rows"]
        and not future_bridge_presence["source_higgs_production_certificate"]
    )
    two_source_action_support_present = (
        future_bridge_presence["two_source_taste_radial_action"] is True
        and certs["two_source_taste_radial_action"].get("proposal_allowed") is False
        and certs["two_source_taste_radial_action"].get(
            "two_source_taste_radial_action_passed"
        )
        is True
        and certs["two_source_taste_radial_action"].get(
            "operator_certificate_payload", {}
        ).get("canonical_higgs_operator_identity_passed")
        is False
    )
    two_source_rows_payload = load_json(FUTURE_BRIDGE_FILES["two_source_taste_radial_rows"])
    two_source_rows_support_present = (
        future_bridge_presence["two_source_taste_radial_rows"] is True
        and two_source_rows_payload.get("proposal_allowed") is False
        and two_source_rows_payload.get("bare_retained_allowed") is False
        and len(two_source_rows_payload.get("completed_chunk_indices", [])) == 63
        and "canonical O_H and pole/FV/IR authority still absent"
        in two_source_rows_payload.get("actual_current_surface_status", "")
    )
    no_unclosed_future_bridge_files_present = (
        all(
            present is False
            for name, present in future_bridge_presence.items()
            if name
            not in {"two_source_taste_radial_action", "two_source_taste_radial_rows"}
        )
        and two_source_action_support_present
        and two_source_rows_support_present
    )
    taste_condensate_bridge_blocked = (
        certs["taste_condensate_oh_bridge"].get("taste_condensate_oh_bridge_audit_passed")
        is True
        and certs["taste_condensate_oh_bridge"].get("proposal_allowed") is False
        and "does not supply PR230 O_H bridge"
        in parent_statuses["taste_condensate_oh_bridge"]
    )
    source_coordinate_transport_blocked = (
        certs["source_coordinate_transport_gate"].get("source_coordinate_transport_gate_passed")
        is True
        and certs["source_coordinate_transport_gate"].get("proposal_allowed") is False
        and certs["source_coordinate_transport_gate"].get("future_transport_certificate_present")
        is False
        and "source-coordinate transport to canonical O_H not derivable"
        in parent_statuses["source_coordinate_transport_gate"]
    )
    two_source_taste_radial_support_not_closure = (
        certs["two_source_taste_radial_chart"].get(
            "two_source_taste_radial_chart_support_passed"
        )
        is True
        and certs["two_source_taste_radial_chart"].get("proposal_allowed") is False
        and certs["two_source_taste_radial_chart"].get("forbidden_firewall", {}).get(
            "identified_taste_radial_axis_with_canonical_oh"
        )
        is False
        and "two-source taste-radial chart"
        in parent_statuses["two_source_taste_radial_chart"]
    )
    two_source_taste_radial_action_not_closure = (
        "two-source taste-radial action source vertex"
        in parent_statuses["two_source_taste_radial_action"]
        and two_source_action_support_present
        and certs["two_source_taste_radial_action"].get("forbidden_firewall", {}).get(
            "used_taste_radial_axis_as_canonical_oh"
        )
        is False
    )
    two_source_taste_radial_row_contract_not_closure = (
        "two-source taste-radial C_sx/C_xx row contract"
        in parent_statuses["two_source_taste_radial_row_contract"]
        and certs["two_source_taste_radial_row_contract"].get("proposal_allowed") is False
        and certs["two_source_taste_radial_row_contract"].get(
            "two_source_taste_radial_row_contract_passed"
        )
        is True
        and certs["two_source_taste_radial_row_contract"].get(
            "future_file_presence", {}
        ).get("taste_radial_production_rows")
        is False
    )
    two_source_taste_radial_row_manifest_not_closure = (
        "two-source taste-radial C_sx/C_xx production manifest"
        in parent_statuses["two_source_taste_radial_row_production_manifest"]
        and certs["two_source_taste_radial_row_production_manifest"].get(
            "proposal_allowed"
        )
        is False
        and certs["two_source_taste_radial_row_production_manifest"].get(
            "manifest_passed"
        )
        is True
        and certs["two_source_taste_radial_row_production_manifest"].get(
            "dry_run_only"
        )
        is True
        and certs["two_source_taste_radial_row_production_manifest"].get(
            "future_combined_rows_present"
        )
        is False
    )
    two_source_taste_radial_chunk_package_not_closure = (
        "two-source taste-radial chunks001-"
        in parent_statuses["two_source_taste_radial_chunk_package"]
        and certs["two_source_taste_radial_chunk_package"].get(
            "chunk_package_audit_passed"
        )
        is True
        and certs["two_source_taste_radial_chunk_package"].get("proposal_allowed")
        is False
        and certs["two_source_taste_radial_chunk_package"].get(
            "completed_chunk_count", 0
        )
        >= 20
        and certs["two_source_taste_radial_chunk_package"].get(
            "active_chunks_counted_as_evidence"
        )
        is False
    )
    source_higgs_pole_row_contract_open = (
        "source-Higgs C_ss/C_sH/C_HH pole-row acceptance contract"
        in parent_statuses["source_higgs_pole_row_acceptance_contract"]
        and certs["source_higgs_pole_row_acceptance_contract"].get(
            "source_higgs_pole_row_acceptance_contract_passed"
        )
        is True
        and certs["source_higgs_pole_row_acceptance_contract"].get(
            "closure_contract_satisfied"
        )
        is False
        and certs["source_higgs_pole_row_acceptance_contract"].get(
            "proposal_allowed"
        )
        is False
    )
    taste_radial_canonical_oh_selector_blocks_symmetry_shortcut = (
        "degree-one taste-radial uniqueness"
        in parent_statuses["taste_radial_canonical_oh_selector_gate"]
        and certs["taste_radial_canonical_oh_selector_gate"].get("proposal_allowed")
        is False
        and certs["taste_radial_canonical_oh_selector_gate"].get(
            "taste_radial_canonical_oh_selector_gate_passed"
        )
        is True
        and certs["taste_radial_canonical_oh_selector_gate"].get(
            "degree_one_radial_unique"
        )
        is True
        and certs["taste_radial_canonical_oh_selector_gate"].get(
            "full_invariant_selector_nonunique"
        )
        is True
        and certs["taste_radial_canonical_oh_selector_gate"].get(
            "canonical_oh_selector_absent"
        )
        is True
    )
    degree_one_higgs_action_premise_not_derived = (
        "degree-one Higgs-action premise not derived"
        in parent_statuses["degree_one_higgs_action_premise_gate"]
        and certs["degree_one_higgs_action_premise_gate"].get("proposal_allowed")
        is False
        and certs["degree_one_higgs_action_premise_gate"].get(
            "degree_one_higgs_action_premise_gate_passed"
        )
        is True
        and certs["degree_one_higgs_action_premise_gate"].get(
            "degree_one_premise_authorized_on_current_surface"
        )
        is False
        and certs["degree_one_higgs_action_premise_gate"].get(
            "degree_one_filter_selects_e1"
        )
        is True
    )
    degree_one_radial_tangent_oh_theorem_support_not_closure = (
        "degree-one radial-tangent O_H uniqueness theorem"
        in parent_statuses["degree_one_radial_tangent_oh_theorem"]
        and certs["degree_one_radial_tangent_oh_theorem"].get("proposal_allowed")
        is False
        and certs["degree_one_radial_tangent_oh_theorem"].get(
            "degree_one_radial_tangent_oh_theorem_passed"
        )
        is True
        and certs["degree_one_radial_tangent_oh_theorem"].get(
            "degree_one_tangent_unique"
        )
        is True
        and certs["degree_one_radial_tangent_oh_theorem"].get(
            "same_surface_linear_tangent_premise_derived"
        )
        is False
        and certs["degree_one_radial_tangent_oh_theorem"].get(
            "canonical_oh_identity_derived"
        )
        is False
        and certs["degree_one_radial_tangent_oh_theorem"].get(
            "source_higgs_pole_rows_present"
        )
        is False
    )
    taste_radial_to_source_higgs_promotion_contract_support_not_closure = (
        "taste-radial-to-source-Higgs promotion contract"
        in parent_statuses["taste_radial_to_source_higgs_promotion_contract"]
        and certs["taste_radial_to_source_higgs_promotion_contract"].get(
            "promotion_contract_passed"
        )
        is True
        and certs["taste_radial_to_source_higgs_promotion_contract"].get(
            "current_promotion_allowed"
        )
        is False
        and certs["taste_radial_to_source_higgs_promotion_contract"].get(
            "proposal_allowed"
        )
        is False
        and "same_surface_canonical_O_H_identity_absent"
        in certs["taste_radial_to_source_higgs_promotion_contract"].get(
            "current_promotion_blockers", []
        )
        and certs["taste_radial_to_source_higgs_promotion_contract"].get(
            "row_packet_status", {}
        ).get("canonical_source_higgs_rows_present")
        is False
    )
    fms_post_degree_route_support_not_closure = (
        "FMS post-degree route rescore"
        in parent_statuses["fms_post_degree_route_rescore"]
        and certs["fms_post_degree_route_rescore"].get("proposal_allowed") is False
        and certs["fms_post_degree_route_rescore"].get(
            "fms_post_degree_route_rescore_passed"
        )
        is True
        and certs["fms_post_degree_route_rescore"].get(
            "forbidden_firewall", {}
        ).get("used_literature_as_proof_authority")
        is False
    )
    fms_composite_oh_conditional_support_not_closure = (
        "FMS composite O_H theorem"
        in parent_statuses["fms_composite_oh_conditional_theorem"]
        and certs["fms_composite_oh_conditional_theorem"].get("proposal_allowed")
        is False
        and certs["fms_composite_oh_conditional_theorem"].get(
            "fms_composite_oh_conditional_theorem_passed"
        )
        is True
        and certs["fms_composite_oh_conditional_theorem"].get(
            "current_closure_authority_present"
        )
        is False
        and certs["fms_composite_oh_conditional_theorem"].get(
            "same_surface_action_absent"
        )
        is True
        and certs["fms_composite_oh_conditional_theorem"].get(
            "source_higgs_rows_absent"
        )
        is True
    )
    fms_oh_candidate_action_packet_support_not_closure = (
        "FMS O_H candidate/action packet"
        in parent_statuses["fms_oh_candidate_action_packet"]
        and certs["fms_oh_candidate_action_packet"].get("proposal_allowed")
        is False
        and certs["fms_oh_candidate_action_packet"].get(
            "fms_oh_candidate_action_packet_passed"
        )
        is True
        and certs["fms_oh_candidate_action_packet"].get("accepted_current_surface")
        is False
        and certs["fms_oh_candidate_action_packet"].get(
            "same_surface_cl3_z3_derived"
        )
        is False
        and certs["fms_oh_candidate_action_packet"].get(
            "external_extension_required"
        )
        is True
        and certs["fms_oh_candidate_action_packet"].get("closure_authorized")
        is False
    )
    fms_source_overlap_readout_gate_support_not_closure = (
        "FMS source-overlap readout gate"
        in parent_statuses["fms_source_overlap_readout_gate"]
        and certs["fms_source_overlap_readout_gate"].get("proposal_allowed")
        is False
        and certs["fms_source_overlap_readout_gate"].get(
            "fms_source_overlap_readout_gate_passed"
        )
        is True
        and certs["fms_source_overlap_readout_gate"].get(
            "readout_executable_now"
        )
        is False
        and certs["fms_source_overlap_readout_gate"].get("strict_rows_present")
        is False
        and certs["fms_source_overlap_readout_gate"].get("closure_authorized")
        is False
    )
    fms_action_adoption_minimal_cut_support_not_closure = (
        "FMS action-adoption minimal cut"
        in parent_statuses["fms_action_adoption_minimal_cut"]
        and certs["fms_action_adoption_minimal_cut"].get("proposal_allowed")
        is False
        and certs["fms_action_adoption_minimal_cut"].get(
            "fms_action_adoption_minimal_cut_passed"
        )
        is True
        and certs["fms_action_adoption_minimal_cut"].get("adoption_allowed_now")
        is False
        and certs["fms_action_adoption_minimal_cut"].get(
            "accepted_current_surface"
        )
        is False
        and certs["fms_action_adoption_minimal_cut"].get(
            "same_surface_cl3_z3_derived"
        )
        is False
        and certs["fms_action_adoption_minimal_cut"].get("closure_authorized")
        is False
        and bool(certs["fms_action_adoption_minimal_cut"].get("missing_root_vertices"))
    )
    higgs_mass_source_action_bridge_not_closure = (
        "Higgs mass-source action bridge"
        in parent_statuses["higgs_mass_source_action_bridge"]
        and certs["higgs_mass_source_action_bridge"].get("proposal_allowed") is False
        and certs["higgs_mass_source_action_bridge"].get(
            "higgs_mass_source_action_bridge_passed"
        )
        is True
        and certs["higgs_mass_source_action_bridge"].get(
            "same_surface_ew_action_certificate_absent"
        )
        is True
        and certs["higgs_mass_source_action_bridge"].get("canonical_oh_absent")
        is True
        and certs["higgs_mass_source_action_bridge"].get("source_higgs_rows_absent")
        is True
    )
    same_source_ew_higgs_action_ansatz_not_closure = (
        "same-source EW/Higgs action-extension ansatz"
        in parent_statuses["same_source_ew_higgs_action_ansatz_gate"]
        and certs["same_source_ew_higgs_action_ansatz_gate"].get("proposal_allowed")
        is False
        and certs["same_source_ew_higgs_action_ansatz_gate"].get(
            "same_source_ew_higgs_action_ansatz_gate_passed"
        )
        is True
        and certs["same_source_ew_higgs_action_ansatz_gate"].get(
            "current_surface_adoption_passed"
        )
        is False
        and certs["same_source_ew_higgs_action_ansatz_gate"].get(
            "future_default_certificates_written"
        )
        is False
    )
    same_source_ew_action_adoption_attempt_not_closure = (
        "ansatz-only same-source EW action adoption shortcut blocked"
        in parent_statuses["same_source_ew_action_adoption_attempt"]
        and certs["same_source_ew_action_adoption_attempt"].get("proposal_allowed")
        is False
        and certs["same_source_ew_action_adoption_attempt"].get(
            "same_source_ew_action_adoption_attempt_passed"
        )
        is True
        and certs["same_source_ew_action_adoption_attempt"].get(
            "adoption_allowed_now"
        )
        is False
        and certs["same_source_ew_action_adoption_attempt"].get(
            "accepted_action_certificate_written_by_this_attempt"
        )
        is False
    )
    radial_spurion_action_contract_not_closure = (
        "no-independent-top-source radial-spurion action contract"
        in parent_statuses["radial_spurion_action_contract"]
        and certs["radial_spurion_action_contract"].get("proposal_allowed") is False
        and certs["radial_spurion_action_contract"].get(
            "radial_spurion_action_contract_passed"
        )
        is True
        and certs["radial_spurion_action_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certs["radial_spurion_action_contract"].get(
            "accepted_action_certificate_written"
        )
        is False
    )
    additive_source_radial_spurion_incompatibility_not_closure = (
        "current additive source is incompatible"
        in parent_statuses["additive_source_radial_spurion_incompatibility"]
        and certs["additive_source_radial_spurion_incompatibility"].get(
            "proposal_allowed"
        )
        is False
        and certs["additive_source_radial_spurion_incompatibility"].get(
            "additive_source_radial_spurion_incompatibility_passed"
        )
        is True
        and certs["additive_source_radial_spurion_incompatibility"].get(
            "forbidden_firewall", {}
        ).get("set_kappa_s_equal_one")
        is False
        and certs["additive_source_radial_spurion_incompatibility"].get(
            "forbidden_firewall", {}
        ).get("used_observed_wz_masses_or_g2")
        is False
    )
    additive_top_subtraction_row_contract_not_closure = (
        "additive-top subtraction row contract"
        in parent_statuses["additive_top_subtraction_row_contract"]
        and certs["additive_top_subtraction_row_contract"].get("proposal_allowed")
        is False
        and certs["additive_top_subtraction_row_contract"].get(
            "additive_top_subtraction_row_contract_passed"
        )
        is True
        and certs["additive_top_subtraction_row_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certs["additive_top_subtraction_row_contract"].get(
            "subtraction_identity_exact"
        )
        is True
        and certs["additive_top_subtraction_row_contract"].get(
            "matched_covariance_delta_method_valid"
        )
        is True
        and (
            certs["additive_top_subtraction_row_contract"].get(
                "future_artifact_presence", {}
            ).get("additive_top_jacobian_rows")
            is False
            or certs["additive_top_subtraction_row_contract"].get(
                "additive_top_jacobian_row_status", {}
            ).get("strict")
            is False
        )
        and certs["additive_top_subtraction_row_contract"].get(
            "future_artifact_presence", {}
        ).get("wz_response_ratio_rows")
        is False
        and certs["additive_top_subtraction_row_contract"].get(
            "future_artifact_presence", {}
        ).get("strict_electroweak_g2_certificate")
        is False
    )
    top_mass_scan_response_harness_not_closure = (
        "top mass-scan response harness schema gate"
        in parent_statuses["top_mass_scan_response_harness_gate"]
        and certs["top_mass_scan_response_harness_gate"].get("proposal_allowed")
        is False
        and certs["top_mass_scan_response_harness_gate"].get(
            "top_mass_scan_response_harness_gate_passed"
        )
        is True
        and certs["top_mass_scan_response_harness_gate"].get("row_schema_version")
        == "top_mass_scan_response_v1"
    )
    post_fms_source_overlap_necessity_blocks_current_inference = (
        "post-FMS source-overlap not derivable"
        in parent_statuses["post_fms_source_overlap_necessity_gate"]
        and certs["post_fms_source_overlap_necessity_gate"].get("proposal_allowed")
        is False
        and certs["post_fms_source_overlap_necessity_gate"].get(
            "post_fms_source_overlap_necessity_gate_passed"
        )
        is True
        and certs["post_fms_source_overlap_necessity_gate"].get(
            "current_source_overlap_authority_present"
        )
        is False
        and certs["post_fms_source_overlap_necessity_gate"].get(
            "two_source_rows_are_c_sx_not_c_sH"
        )
        is True
    )
    source_higgs_overlap_kappa_contract_not_closure = (
        "source-Higgs overlap-kappa row contract"
        in parent_statuses["source_higgs_overlap_kappa_contract"]
        and certs["source_higgs_overlap_kappa_contract"].get("proposal_allowed")
        is False
        and certs["source_higgs_overlap_kappa_contract"].get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
        and certs["source_higgs_overlap_kappa_contract"].get(
            "current_blockers", {}
        ).get("source_higgs_row_packet_absent")
        is True
        and certs["source_higgs_overlap_kappa_contract"].get(
            "forbidden_firewall", {}
        ).get("set_kappa_s_equal_one")
        is False
    )
    origin_main_composite_higgs_not_closure = (
        certs["origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_intake_guard_passed"
        )
        is True
        and certs["origin_main_composite_higgs_intake_guard"].get("proposal_allowed")
        is False
        and certs["origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_closes_pr230"
        )
        is False
        and "not PR230 same-surface"
        in parent_statuses["origin_main_composite_higgs_intake_guard"]
    )
    origin_main_ew_m_residual_not_closure = (
        certs["origin_main_ew_m_residual_intake_guard"].get(
            "origin_main_ew_m_residual_intake_guard_passed"
        )
        is True
        and certs["origin_main_ew_m_residual_intake_guard"].get("proposal_allowed")
        is False
        and certs["origin_main_ew_m_residual_intake_guard"].get(
            "origin_main_ew_m_residual_closes_pr230"
        )
        is False
        and "context-only channel bookkeeping"
        in parent_statuses["origin_main_ew_m_residual_intake_guard"]
    )
    z3_triplet_conditional_primitive_not_closure = (
        certs["z3_triplet_conditional_primitive_cone"].get(
            "z3_triplet_conditional_primitive_theorem_passed"
        )
        is True
        and certs["z3_triplet_conditional_primitive_cone"].get("proposal_allowed")
        is False
        and certs["z3_triplet_conditional_primitive_cone"].get(
            "pr230_closure_authorized"
        )
        is False
        and "same-surface PR230 primitive premise absent"
        in parent_statuses["z3_triplet_conditional_primitive_cone"]
    )
    z3_triplet_positive_cone_h2_support_not_transfer = (
        certs["z3_triplet_positive_cone_support"].get(
            "z3_triplet_positive_cone_h2_support_passed"
        )
        is True
        and certs["z3_triplet_positive_cone_support"].get("proposal_allowed")
        is False
        and certs["z3_triplet_positive_cone_support"].get(
            "pr230_closure_authorized"
        )
        is False
        and certs["z3_triplet_positive_cone_support"].get(
            "supplies_conditional_premises", {}
        ).get("H2_positive_cone_equal_magnitude_support")
        is True
        and certs["z3_triplet_positive_cone_support"].get(
            "supplies_conditional_premises", {}
        ).get("H3_lazy_positive_physical_transfer")
        is False
        and "Z3-triplet positive-cone H2 support"
        in parent_statuses["z3_triplet_positive_cone_support"]
    )
    z3_generation_action_lift_not_derived = (
        certs["z3_generation_action_lift_attempt"].get(
            "h1_generation_action_lift_attempt_passed"
        )
        is True
        and certs["z3_generation_action_lift_attempt"].get("proposal_allowed")
        is False
        and certs["z3_generation_action_lift_attempt"].get(
            "same_surface_h1_derived"
        )
        is False
        and "Z3 generation-action lift"
        in parent_statuses["z3_generation_action_lift_attempt"]
    )
    z3_lazy_transfer_promotion_not_derived = (
        certs["z3_lazy_transfer_promotion_attempt"].get(
            "z3_lazy_transfer_promotion_attempt_passed"
        )
        is True
        and certs["z3_lazy_transfer_promotion_attempt"].get("proposal_allowed")
        is False
        and certs["z3_lazy_transfer_promotion_attempt"].get(
            "physical_lazy_transfer_instantiated"
        )
        is False
        and "Z3 lazy-transfer promotion not derivable"
        in parent_statuses["z3_lazy_transfer_promotion_attempt"]
    )
    z3_heat_kernel_support_not_h3h4 = (
        certs["z3_heat_kernel_neutral_transfer_attempt"].get(
            "z3_heat_kernel_neutral_transfer_attempt_passed"
        )
        is True
        and certs["z3_heat_kernel_neutral_transfer_attempt"].get("proposal_allowed")
        is False
        and certs["z3_heat_kernel_neutral_transfer_attempt"].get(
            "mathematical_heat_kernel_primitive_support"
        )
        is True
        and certs["z3_heat_kernel_neutral_transfer_attempt"].get(
            "same_surface_physical_action_selects_heat_time"
        )
        is False
        and certs["z3_heat_kernel_neutral_transfer_attempt"].get(
            "strict_neutral_h3_authority_passed"
        )
        is False
        and certs["z3_heat_kernel_neutral_transfer_attempt"].get(
            "strict_h4_source_canonical_higgs_coupling_passed"
        )
        is False
        and "Z3 heat-kernel primitive transfer is mathematical support only"
        in parent_statuses["z3_heat_kernel_neutral_transfer_attempt"]
    )
    same_surface_neutral_multiplicity_gate_rejects_current_surface = (
        "same-surface neutral multiplicity-one artifact intake gate"
        in parent_statuses["same_surface_neutral_multiplicity_one_gate"]
        and certs["same_surface_neutral_multiplicity_one_gate"].get("proposal_allowed")
        is False
        and certs["same_surface_neutral_multiplicity_one_gate"].get(
            "candidate_accepted"
        )
        is False
    )
    os_transfer_kernel_artifact_absent = (
        "OS transfer-kernel artifact absent"
        in parent_statuses["os_transfer_kernel_artifact_gate"]
        and certs["os_transfer_kernel_artifact_gate"].get("proposal_allowed") is False
        and certs["os_transfer_kernel_artifact_gate"].get(
            "os_transfer_kernel_artifact_present"
        )
        is False
        and certs["os_transfer_kernel_artifact_gate"].get(
            "same_surface_transfer_or_gevp_present"
        )
        is False
    )
    source_higgs_time_kernel_harness_support_only = (
        "source-Higgs time-kernel harness"
        in parent_statuses["source_higgs_time_kernel_harness_extension_gate"]
        and certs["source_higgs_time_kernel_harness_extension_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["source_higgs_time_kernel_harness_extension_gate"].get(
            "contract", {}
        ).get("adds_default_off_time_kernel_rows")
        is True
        and certs["source_higgs_time_kernel_harness_extension_gate"].get(
            "contract", {}
        ).get("selected_mass_only")
        is True
        and certs["source_higgs_time_kernel_harness_extension_gate"].get(
            "used_as_physical_yukawa_readout"
        )
        is False
    )
    source_higgs_time_kernel_gevp_contract_support_only = (
        "source-Higgs time-kernel GEVP contract"
        in parent_statuses["source_higgs_time_kernel_gevp_contract"]
        and certs["source_higgs_time_kernel_gevp_contract"].get("proposal_allowed")
        is False
        and certs["source_higgs_time_kernel_gevp_contract"].get(
            "formal_gevp_diagnostic", {}
        ).get("available")
        is True
        and certs["source_higgs_time_kernel_gevp_contract"].get(
            "physical_pole_extraction_accepted"
        )
        is False
    )
    source_higgs_time_kernel_production_manifest_not_evidence = (
        "source-Higgs time-kernel production manifest"
        in parent_statuses["source_higgs_time_kernel_production_manifest"]
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "proposal_allowed"
        )
        is False
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "closure_launch_authorized_now"
        )
        is False
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "support_launch_authorized_now"
        )
        is False
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "operator_certificate_is_canonical_oh"
        )
        is False
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "time_kernel_schema_version"
        )
        == "source_higgs_time_kernel_v1"
        and certs["source_higgs_time_kernel_production_manifest"].get(
            "chunk_count"
        )
        == 63
    )
    fms_literature_source_overlap_intake_non_authority = (
        "FMS literature does not supply PR230 source-overlap"
        in parent_statuses["fms_literature_source_overlap_intake"]
        and certs["fms_literature_source_overlap_intake"].get("proposal_allowed")
        is False
        and certs["fms_literature_source_overlap_intake"].get(
            "literature_bridge_scope"
        )
        == "non_derivation_context_only"
        and certs["fms_literature_source_overlap_intake"].get(
            "current_blockers", {}
        ).get("canonical_oh_absent")
        is True
        and certs["fms_literature_source_overlap_intake"].get(
            "current_blockers", {}
        ).get("source_higgs_rows_absent")
        is True
    )
    schur_higher_shell_production_contract_not_evidence = (
        "higher-shell Schur scalar-LSZ production contract"
        in parent_statuses["schur_higher_shell_production_contract"]
        and certs["schur_higher_shell_production_contract"].get("proposal_allowed")
        is False
        and certs["schur_higher_shell_production_contract"].get(
            "higher_shell_schur_production_contract_passed"
        )
        is True
        and certs["schur_higher_shell_production_contract"].get(
            "rows_written_by_contract"
        )
        is False
        and certs["schur_higher_shell_production_contract"].get(
            "current_four_mode_campaign_must_remain_unmixed"
        )
        is True
    )
    schur_higher_shell_complete_packet_monotonicity_blocks = (
        "complete 63/63 higher-shell finite rows fail"
        in parent_statuses["schur_higher_shell_complete_packet_monotonicity"]
        and certs["schur_higher_shell_complete_packet_monotonicity"].get(
            "proposal_allowed"
        )
        is False
        and certs["schur_higher_shell_complete_packet_monotonicity"].get(
            "higher_shell_complete_packet_monotonicity_gate_passed"
        )
        is True
        and certs["schur_higher_shell_complete_packet_monotonicity"].get(
            "complete_packet_chunk_count"
        )
        == 63
        and certs["schur_higher_shell_complete_packet_monotonicity"].get(
            "strict_schur_or_scalar_lsz_authority_passed"
        )
        is False
        and bool(
            certs["schur_higher_shell_complete_packet_monotonicity"].get(
                "failing_complete_monotonicity_fields"
            )
        )
    )
    two_source_taste_radial_primitive_transfer_candidate_not_h3 = (
        "finite C_sx rows do not certify a physical primitive neutral transfer"
        in parent_statuses["two_source_taste_radial_primitive_transfer_candidate_gate"]
        and certs["two_source_taste_radial_primitive_transfer_candidate_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["two_source_taste_radial_primitive_transfer_candidate_gate"].get(
            "physical_transfer_candidate_accepted"
        )
        is False
        and certs["two_source_taste_radial_primitive_transfer_candidate_gate"].get(
            "finite_offdiagonal_correlation_support"
        )
        is True
    )
    orthogonal_top_coupling_exclusion_candidate_rejected = (
        "orthogonal-neutral top-coupling exclusion candidate rejected"
        in parent_statuses["orthogonal_top_coupling_exclusion_candidate_gate"]
        and certs["orthogonal_top_coupling_exclusion_candidate_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["orthogonal_top_coupling_exclusion_candidate_gate"].get(
            "orthogonal_top_coupling_exclusion_candidate_accepted"
        )
        is False
        and certs["orthogonal_top_coupling_exclusion_candidate_gate"].get(
            "finite_c_sx_rows_are_top_coupling_tomography"
        )
        is False
    )
    strict_scalar_lsz_moment_fv_authority_absent = (
        "raw C_ss rows do not supply strict scalar-LSZ moment/FV authority"
        in parent_statuses["strict_scalar_lsz_moment_fv_authority_gate"]
        and certs["strict_scalar_lsz_moment_fv_authority_gate"].get(
            "proposal_allowed"
        )
        is False
        and certs["strict_scalar_lsz_moment_fv_authority_gate"].get(
            "strict_scalar_lsz_moment_fv_authority_gate_passed"
        )
        is True
        and certs["strict_scalar_lsz_moment_fv_authority_gate"].get(
            "strict_scalar_lsz_moment_fv_authority_present"
        )
        is False
        and certs["strict_scalar_lsz_moment_fv_authority_gate"].get(
            "current_raw_c_ss_proxy_fails_stieltjes_monotonicity"
        )
        is True
    )
    schur_complement_stieltjes_repair_not_closure = (
        "Schur-complement Stieltjes repair split"
        in parent_statuses["schur_complement_stieltjes_repair_gate"]
        and certs["schur_complement_stieltjes_repair_gate"].get("proposal_allowed")
        is False
        and certs["schur_complement_stieltjes_repair_gate"].get(
            "schur_complement_stieltjes_repair_gate_passed"
        )
        is True
        and certs["schur_complement_stieltjes_repair_gate"].get(
            "source_given_x_stieltjes_first_shell_failed"
        )
        is True
        and certs["schur_complement_stieltjes_repair_gate"].get(
            "x_given_source_stieltjes_first_shell_passed"
        )
        is True
        and certs["schur_complement_stieltjes_repair_gate"].get(
            "strict_scalar_lsz_authority_present"
        )
        is False
        and certs["schur_complement_stieltjes_repair_gate"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    schur_complement_complete_monotonicity_not_closure = (
        "C_x|s Schur residual passes"
        in parent_statuses["schur_complement_complete_monotonicity_gate"]
        and certs["schur_complement_complete_monotonicity_gate"].get("proposal_allowed")
        is False
        and certs["schur_complement_complete_monotonicity_gate"].get(
            "schur_complement_complete_monotonicity_gate_passed"
        )
        is True
        and certs["schur_complement_complete_monotonicity_gate"].get(
            "complete_monotonicity_authority_passed"
        )
        is False
        and certs["schur_complement_complete_monotonicity_gate"].get(
            "canonical_higgs_or_physical_response_bridge_present"
        )
        is False
    )
    schur_x_given_source_one_pole_scout_not_authority = (
        "one-pole finite-residue scout"
        in parent_statuses["schur_x_given_source_one_pole_scout"]
        and certs["schur_x_given_source_one_pole_scout"].get("proposal_allowed")
        is False
        and certs["schur_x_given_source_one_pole_scout"].get(
            "schur_x_given_source_one_pole_scout_passed"
        )
        is True
        and certs["schur_x_given_source_one_pole_scout"].get("one_pole_fit_valid")
        is True
        and certs["schur_x_given_source_one_pole_scout"].get(
            "one_pole_model_class_authority_passed"
        )
        is False
        and certs["schur_x_given_source_one_pole_scout"].get(
            "two_pole_counterfamily_present"
        )
        is True
        and certs["schur_x_given_source_one_pole_scout"].get(
            "physical_pole_residue_authority_present"
        )
        is False
    )
    wz_response_ratio_identifiability_contract_not_closure = (
        "WZ response-ratio identifiability contract"
        in parent_statuses["wz_response_ratio_identifiability_contract"]
        and certs["wz_response_ratio_identifiability_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and certs["wz_response_ratio_identifiability_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
        and certs["wz_response_ratio_identifiability_contract"].get(
            "future_response_ratio_row_packet_present"
        )
        is False
        and certs["wz_response_ratio_identifiability_contract"].get(
            "strict_g2_authority_present"
        )
        is False
        and certs["wz_response_ratio_identifiability_contract"].get(
            "matched_covariance_authority_present"
        )
        is False
        and certs["wz_response_ratio_identifiability_contract"].get(
            "proposal_allowed"
        )
        is False
    )
    wz_same_source_action_minimal_certificate_cut_open = (
        "WZ accepted same-source action minimal certificate cut"
        in parent_statuses["wz_same_source_action_minimal_certificate_cut"]
        and certs["wz_same_source_action_minimal_certificate_cut"].get(
            "wz_same_source_action_minimal_certificate_cut_passed"
        )
        is True
        and certs["wz_same_source_action_minimal_certificate_cut"].get(
            "proposal_allowed"
        )
        is False
        and certs["wz_same_source_action_minimal_certificate_cut"].get(
            "current_surface_action_certificate_satisfied"
        )
        is False
    )
    wz_accepted_action_response_root_checkpoint_blocks = (
        "WZ accepted-action response root not closed"
        in parent_statuses["wz_accepted_action_response_root_checkpoint"]
        and certs["wz_accepted_action_response_root_checkpoint"].get(
            "proposal_allowed"
        )
        is False
        and certs["wz_accepted_action_response_root_checkpoint"].get(
            "wz_accepted_action_response_root_checkpoint_passed"
        )
        is True
        and certs["wz_accepted_action_response_root_checkpoint"].get(
            "current_route_blocked"
        )
        is True
        and certs["wz_accepted_action_response_root_checkpoint"].get(
            "root_closures_found"
        )
        == []
        and not any(
            certs["wz_accepted_action_response_root_checkpoint"].get(
                "future_artifact_presence", {}
            ).values()
        )
    )
    canonical_oh_wz_common_action_cut_open = (
        "canonical O_H and WZ accepted-action common-cut"
        in parent_statuses["canonical_oh_wz_common_action_cut"]
        and certs["canonical_oh_wz_common_action_cut"].get("proposal_allowed")
        is False
        and certs["canonical_oh_wz_common_action_cut"].get(
            "common_action_cut_passed"
        )
        is True
        and certs["canonical_oh_wz_common_action_cut"].get(
            "common_canonical_oh_vertex_open"
        )
        is True
        and certs["canonical_oh_wz_common_action_cut"].get(
            "aggregate_denies_proposal"
        )
        is True
        and certs["canonical_oh_wz_common_action_cut"].get(
            "time_kernel_manifest_not_evidence"
        )
        is True
    )
    canonical_oh_accepted_action_stretch_blocks_current_stack = (
        "canonical O_H accepted-action root not derivable"
        in parent_statuses["canonical_oh_accepted_action_stretch_attempt"]
        and certs["canonical_oh_accepted_action_stretch_attempt"].get(
            "proposal_allowed"
        )
        is False
        and certs["canonical_oh_accepted_action_stretch_attempt"].get(
            "stretch_attempt_passed"
        )
        is True
        and certs["canonical_oh_accepted_action_stretch_attempt"].get(
            "current_route_blocked"
        )
        is True
        and certs["canonical_oh_accepted_action_stretch_attempt"].get(
            "root_closures_found"
        )
        == []
    )

    completion_criteria = {
        "genuine_source_pole_support_intaken": source_pole_intaken,
        "canonical_oh_certificate": not canonical_oh_absent,
        "osp_higgs_pole_rows": not osp_higgs_rows_absent,
        "production_chunks_complete_with_schema": production["complete_with_schema"],
        "polefit8x8_chunks_complete_with_schema": polefit["complete_with_schema"],
        "assembly_current_surface_passed": current_eval.get("assembly_passed") is True,
        "assembly_chunk_only_passed": chunk_eval.get("assembly_passed") is True,
        "scalar_lsz_model_class_fv_ir": "scalar_lsz_model_class_fv_ir"
        not in current_eval.get("missing", []),
        "source_overlap_or_physical_response_bridge": "source_overlap_or_physical_response_bridge"
        not in current_eval.get("missing", []),
        "matching_running_bridge": "matching_running_bridge" not in current_eval.get("missing", []),
        "retained_proposal_firewall": "retained_proposal_firewall" not in current_eval.get("missing", []),
        "retained_route_allows_proposal": certs["retained_route"].get("proposal_allowed") is True,
        "campaign_allows_proposal": certs["campaign_status"].get("proposal_allowed") is True,
    }
    closure_achieved = all(completion_criteria.values())
    missing_requirements = [key for key, ok in completion_criteria.items() if not ok]

    source_higgs_open = (
        certs["source_higgs_readiness"].get("source_higgs_launch_ready") is not True
        and "missing O_H certificate" in parent_statuses["source_higgs_readiness"]
    )
    wz_v_authority_firewall_blocks = (
        "PR230 W/Z explicit-v authority absent"
        in parent_statuses["wz_v_authority_firewall"]
        and certs["wz_v_authority_firewall"].get("proposal_allowed") is False
        and certs["wz_v_authority_firewall"].get("wz_v_authority_firewall_passed")
        is True
        and certs["wz_v_authority_firewall"].get("v_authority_gate_passed")
        is False
        and certs["wz_v_authority_firewall"].get("package_v_surface", {}).get(
            "rejected_as_pr230_load_bearing_input"
        )
        is True
    )
    post_block100_completion_reopen_blocks = (
        "positive closure not achieved"
        in parent_statuses["post_block100_completion_reopen_audit"]
        and certs["post_block100_completion_reopen_audit"].get("proposal_allowed")
        is False
        and certs["post_block100_completion_reopen_audit"].get(
            "completion_reopen_audit_passed"
        )
        is True
        and certs["post_block100_completion_reopen_audit"].get("closure_achieved")
        is False
        and certs["post_block100_completion_reopen_audit"].get(
            "fresh_artifact_admitted"
        )
        is False
    )
    wz_open = (
        certs["wz_same_source_action"].get("same_source_ew_action_ready") is not True
        and certs["wz_mass_fit_response_row_builder"].get("strict_wz_mass_fit_response_row_builder_passed")
        is not True
        and certs["top_wz_matched_covariance_builder"].get("strict_top_wz_matched_covariance_builder_passed")
        is not True
        and certs["electroweak_g2_builder"].get("strict_electroweak_g2_certificate_passed") is not True
        and wz_v_authority_firewall_blocks
    )
    schur_open = certs["schur_kprime_rows"].get("current_schur_kernel_rows_present") is not True
    neutral_open = certs["neutral_primitive_cone"].get("primitive_cone_certificate_gate_passed") is not True
    lsz_open = (
        certs["fh_lsz_stieltjes_moment"].get("strict_stieltjes_moment_certificate_present") is not True
        and certs["fh_lsz_pade_stieltjes"].get("strict_pade_stieltjes_bounds_certificate_present") is not True
    )
    matching_open = certs["matching_running"].get("matching_running_bridge_passed") is not True
    smoke_promotion_blocked = (
        certs["wz_smoke_promotion_no_go"].get("wz_smoke_to_production_promotion_no_go_passed")
        is True
        and certs["wz_smoke_promotion_no_go"].get("proposal_allowed") is False
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("genuine-source-pole-support-intaken", source_pole_intaken, parent_statuses["genuine_source_pole_intake"])
    report("source-pole-support-not-closure", source_pole_intaken and genuine_source_pole.get("artifact_is_physics_closure") is False, genuine_source_pole.get("proposal_allowed_reason", ""))
    report("canonical-oh-certificate-still-absent", canonical_oh_absent, parent_statuses["canonical_higgs_operator_gate"])
    report("osp-higgs-pole-rows-still-absent", osp_higgs_rows_absent, parent_statuses["source_higgs_builder"])
    report("taste-condensate-oh-bridge-blocked", taste_condensate_bridge_blocked, parent_statuses["taste_condensate_oh_bridge"])
    report("source-coordinate-transport-blocked", source_coordinate_transport_blocked, parent_statuses["source_coordinate_transport_gate"])
    report("two-source-taste-radial-chart-support-not-closure", two_source_taste_radial_support_not_closure, parent_statuses["two_source_taste_radial_chart"])
    report("two-source-taste-radial-action-support-not-closure", two_source_taste_radial_action_not_closure, parent_statuses["two_source_taste_radial_action"])
    report("two-source-taste-radial-row-contract-support-not-closure", two_source_taste_radial_row_contract_not_closure, parent_statuses["two_source_taste_radial_row_contract"])
    report("two-source-taste-radial-row-production-manifest-support-not-closure", two_source_taste_radial_row_manifest_not_closure, parent_statuses["two_source_taste_radial_row_production_manifest"])
    report("two-source-taste-radial-chunk-package-support-not-closure", two_source_taste_radial_chunk_package_not_closure, parent_statuses["two_source_taste_radial_chunk_package"])
    report("source-higgs-pole-row-contract-open", source_higgs_pole_row_contract_open, parent_statuses["source_higgs_pole_row_acceptance_contract"])
    report("taste-radial-canonical-oh-selector-blocks-symmetry-shortcut", taste_radial_canonical_oh_selector_blocks_symmetry_shortcut, parent_statuses["taste_radial_canonical_oh_selector_gate"])
    report("degree-one-higgs-action-premise-not-derived", degree_one_higgs_action_premise_not_derived, parent_statuses["degree_one_higgs_action_premise_gate"])
    report("degree-one-radial-tangent-oh-theorem-support-not-closure", degree_one_radial_tangent_oh_theorem_support_not_closure, parent_statuses["degree_one_radial_tangent_oh_theorem"])
    report("taste-radial-to-source-higgs-promotion-contract-support-not-closure", taste_radial_to_source_higgs_promotion_contract_support_not_closure, parent_statuses["taste_radial_to_source_higgs_promotion_contract"])
    report("fms-post-degree-route-rescore-support-not-closure", fms_post_degree_route_support_not_closure, parent_statuses["fms_post_degree_route_rescore"])
    report("fms-composite-oh-conditional-support-not-closure", fms_composite_oh_conditional_support_not_closure, parent_statuses["fms_composite_oh_conditional_theorem"])
    report("fms-oh-candidate-action-packet-support-not-closure", fms_oh_candidate_action_packet_support_not_closure, parent_statuses["fms_oh_candidate_action_packet"])
    report("fms-source-overlap-readout-gate-support-not-closure", fms_source_overlap_readout_gate_support_not_closure, parent_statuses["fms_source_overlap_readout_gate"])
    report("fms-action-adoption-minimal-cut-support-not-closure", fms_action_adoption_minimal_cut_support_not_closure, parent_statuses["fms_action_adoption_minimal_cut"])
    report("higgs-mass-source-action-bridge-not-closure", higgs_mass_source_action_bridge_not_closure, parent_statuses["higgs_mass_source_action_bridge"])
    report("same-source-ew-higgs-action-ansatz-not-closure", same_source_ew_higgs_action_ansatz_not_closure, parent_statuses["same_source_ew_higgs_action_ansatz_gate"])
    report("same-source-ew-action-adoption-attempt-not-closure", same_source_ew_action_adoption_attempt_not_closure, parent_statuses["same_source_ew_action_adoption_attempt"])
    report("radial-spurion-action-contract-not-closure", radial_spurion_action_contract_not_closure, parent_statuses["radial_spurion_action_contract"])
    report("additive-source-radial-spurion-incompatibility-not-closure", additive_source_radial_spurion_incompatibility_not_closure, parent_statuses["additive_source_radial_spurion_incompatibility"])
    report("additive-top-subtraction-row-contract-not-closure", additive_top_subtraction_row_contract_not_closure, parent_statuses["additive_top_subtraction_row_contract"])
    report("top-mass-scan-response-harness-not-closure", top_mass_scan_response_harness_not_closure, parent_statuses["top_mass_scan_response_harness_gate"])
    report("wz-response-ratio-identifiability-contract-not-closure", wz_response_ratio_identifiability_contract_not_closure, parent_statuses["wz_response_ratio_identifiability_contract"])
    report("wz-same-source-action-minimal-certificate-cut-open", wz_same_source_action_minimal_certificate_cut_open, parent_statuses["wz_same_source_action_minimal_certificate_cut"])
    report("wz-accepted-action-response-root-checkpoint-blocks", wz_accepted_action_response_root_checkpoint_blocks, parent_statuses["wz_accepted_action_response_root_checkpoint"])
    report("canonical-oh-wz-common-action-cut-open", canonical_oh_wz_common_action_cut_open, parent_statuses["canonical_oh_wz_common_action_cut"])
    report("canonical-oh-accepted-action-stretch-blocks-current-stack", canonical_oh_accepted_action_stretch_blocks_current_stack, parent_statuses["canonical_oh_accepted_action_stretch_attempt"])
    report("post-fms-source-overlap-necessity-blocks-current-inference", post_fms_source_overlap_necessity_blocks_current_inference, parent_statuses["post_fms_source_overlap_necessity_gate"])
    report("source-higgs-overlap-kappa-contract-not-closure", source_higgs_overlap_kappa_contract_not_closure, parent_statuses["source_higgs_overlap_kappa_contract"])
    report("origin-main-composite-higgs-intake-not-closure", origin_main_composite_higgs_not_closure, parent_statuses["origin_main_composite_higgs_intake_guard"])
    report("origin-main-ew-m-residual-intake-not-closure", origin_main_ew_m_residual_not_closure, parent_statuses["origin_main_ew_m_residual_intake_guard"])
    report("z3-triplet-conditional-primitive-support-not-closure", z3_triplet_conditional_primitive_not_closure, parent_statuses["z3_triplet_conditional_primitive_cone"])
    report("z3-triplet-positive-cone-h2-support-not-transfer", z3_triplet_positive_cone_h2_support_not_transfer, parent_statuses["z3_triplet_positive_cone_support"])
    report("z3-generation-action-lift-not-derived", z3_generation_action_lift_not_derived, parent_statuses["z3_generation_action_lift_attempt"])
    report("z3-lazy-transfer-promotion-not-derived", z3_lazy_transfer_promotion_not_derived, parent_statuses["z3_lazy_transfer_promotion_attempt"])
    report("z3-heat-kernel-neutral-transfer-support-not-h3h4", z3_heat_kernel_support_not_h3h4, parent_statuses["z3_heat_kernel_neutral_transfer_attempt"])
    report("same-surface-neutral-multiplicity-one-gate-rejects-current-surface", same_surface_neutral_multiplicity_gate_rejects_current_surface, parent_statuses["same_surface_neutral_multiplicity_one_gate"])
    report("os-transfer-kernel-artifact-absent", os_transfer_kernel_artifact_absent, parent_statuses["os_transfer_kernel_artifact_gate"])
    report("source-higgs-time-kernel-harness-support-only", source_higgs_time_kernel_harness_support_only, parent_statuses["source_higgs_time_kernel_harness_extension_gate"])
    report("source-higgs-time-kernel-gevp-contract-support-only", source_higgs_time_kernel_gevp_contract_support_only, parent_statuses["source_higgs_time_kernel_gevp_contract"])
    report("source-higgs-time-kernel-production-manifest-not-evidence", source_higgs_time_kernel_production_manifest_not_evidence, parent_statuses["source_higgs_time_kernel_production_manifest"])
    report("fms-literature-source-overlap-intake-non-authority", fms_literature_source_overlap_intake_non_authority, parent_statuses["fms_literature_source_overlap_intake"])
    report("schur-higher-shell-production-contract-not-evidence", schur_higher_shell_production_contract_not_evidence, parent_statuses["schur_higher_shell_production_contract"])
    report("schur-higher-shell-complete-packet-monotonicity-blocks-shortcut", schur_higher_shell_complete_packet_monotonicity_blocks, parent_statuses["schur_higher_shell_complete_packet_monotonicity"])
    report("two-source-taste-radial-primitive-transfer-candidate-not-h3", two_source_taste_radial_primitive_transfer_candidate_not_h3, parent_statuses["two_source_taste_radial_primitive_transfer_candidate_gate"])
    report("orthogonal-top-coupling-exclusion-candidate-rejected", orthogonal_top_coupling_exclusion_candidate_rejected, parent_statuses["orthogonal_top_coupling_exclusion_candidate_gate"])
    report("strict-scalar-lsz-moment-fv-authority-absent", strict_scalar_lsz_moment_fv_authority_absent, parent_statuses["strict_scalar_lsz_moment_fv_authority_gate"])
    report("schur-complement-stieltjes-repair-not-closure", schur_complement_stieltjes_repair_not_closure, parent_statuses["schur_complement_stieltjes_repair_gate"])
    report("schur-complement-complete-monotonicity-not-closure", schur_complement_complete_monotonicity_not_closure, parent_statuses["schur_complement_complete_monotonicity_gate"])
    report("schur-x-given-source-one-pole-scout-not-authority", schur_x_given_source_one_pole_scout_not_authority, parent_statuses["schur_x_given_source_one_pole_scout"])
    report("future-bridge-artifact-files-support-only-or-absent", no_unclosed_future_bridge_files_present, str(future_bridge_presence))
    report("production-chunks-complete", production["complete_id_set"], f"count={production['count']} missing={production['missing_ids']}")
    report("production-chunk-schema-complete", production["schema"]["schema_ok"], str(production["schema"]))
    report("polefit8x8-chunks-complete", polefit["complete_id_set"], f"count={polefit['count']} missing={polefit['missing_ids']}")
    report("polefit8x8-chunk-schema-complete", polefit["schema"]["schema_ok"], str(polefit["schema"]))
    report("assembly-current-surface-rejects-closure", current_eval.get("assembly_passed") is False, str(current_eval.get("missing", [])))
    report("assembly-chunk-only-rejects-closure", chunk_eval.get("assembly_passed") is False, str(chunk_eval.get("missing", [])))
    report("retained-route-denies-proposal", certs["retained_route"].get("proposal_allowed") is False, parent_statuses["retained_route"])
    report("campaign-denies-proposal", certs["campaign_status"].get("proposal_allowed") is False, parent_statuses["campaign_status"])
    report("scalar-lsz-route-open", lsz_open, "strict Stieltjes/Pade moment-threshold certificate absent")
    report("source-higgs-route-open", source_higgs_open, parent_statuses["source_higgs_readiness"])
    report("same-source-wz-route-open", wz_open, "same-source EW action/WZ rows/covariance/g2 inputs absent")
    report("wz-v-authority-firewall-blocks", wz_v_authority_firewall_blocks, parent_statuses["wz_v_authority_firewall"])
    report(
        "post-block100-completion-reopen-audit-blocks",
        post_block100_completion_reopen_blocks,
        parent_statuses["post_block100_completion_reopen_audit"],
    )
    report("wz-smoke-promotion-blocked", smoke_promotion_blocked, parent_statuses["wz_smoke_promotion_no_go"])
    report("schur-route-open", schur_open, parent_statuses["schur_kprime_rows"])
    report("neutral-rank-route-open", neutral_open, parent_statuses["neutral_primitive_cone"])
    report("matching-running-route-open", matching_open, parent_statuses["matching_running"])
    report("closure-not-achieved-recorded", closure_achieved is False, f"missing={missing_requirements}")

    checklist = [
        {
            "requirement": "identify the strongest genuine current artifact in the clean source-Higgs contract",
            "evidence": PARENTS["genuine_source_pole_intake"],
            "status": "satisfied / support-only" if source_pole_intaken else "missing",
            "details": {
                "artifact": "O_sp source-pole operator",
                "artifact_is_physics_closure": genuine_source_pole.get(
                    "artifact_is_physics_closure"
                ),
                "proposal_allowed": genuine_source_pole.get("proposal_allowed"),
                "current_blocker": genuine_source_pole.get(
                    "proposal_allowed_reason"
                ),
            },
        },
        {
            "requirement": "upgrade O_sp source-side support to source-Higgs bridge evidence",
            "evidence": [
                PARENTS["canonical_higgs_operator_gate"],
                PARENTS["source_higgs_builder"],
                PARENTS["source_higgs_postprocess"],
            ],
            "status": "missing",
            "details": {
                "canonical_oh_absent": canonical_oh_absent,
                "osp_higgs_rows_absent": osp_higgs_rows_absent,
                "taste_condensate_oh_bridge_blocked": taste_condensate_bridge_blocked,
                "origin_main_composite_higgs_not_closure": origin_main_composite_higgs_not_closure,
                "origin_main_ew_m_residual_not_closure": origin_main_ew_m_residual_not_closure,
                "source_higgs_overlap_kappa_contract_not_closure": source_higgs_overlap_kappa_contract_not_closure,
                "radial_spurion_action_contract_not_closure": radial_spurion_action_contract_not_closure,
                "future_bridge_file_presence": future_bridge_presence,
                "needed": [
                    "same-surface canonical O_H identity/normalization certificate",
                    "Res_C_sp_sp=1",
                    "Res_C_spH",
                    "Res_C_HH",
                    "O_sp-Higgs Gram purity plus FV/IR/model-class authority",
                ],
            },
        },
        {
            "requirement": "complete target production chunks with FH/LSZ target schema",
            "evidence": "production chunk root JSON files 001-063",
            "status": "satisfied" if production["complete_with_schema"] else "missing",
            "details": production,
        },
        {
            "requirement": "complete polefit8x8 chunks with LSZ C_ss timeseries schema",
            "evidence": "polefit8x8 chunk root JSON files 001-063",
            "status": "satisfied" if polefit["complete_with_schema"] else "missing",
            "details": polefit,
        },
        {
            "requirement": "scalar-LSZ model-class/FV/IR/pole authority",
            "evidence": [
                PARENTS["fh_lsz_stieltjes_moment"],
                PARENTS["fh_lsz_pade_stieltjes"],
                "full assembly current_evaluation",
            ],
            "status": "missing",
            "details": "strict moment-threshold/Stieltjes/Pade/FV certificate absent on current surface",
        },
        {
            "requirement": "one accepted source-overlap or physical-response bridge",
            "evidence": [
                "source-Higgs route",
                "same-source W/Z route",
                "Schur/K-prime route",
                "neutral primitive-cone route",
            ],
            "status": "missing",
            "details": {
                "source_higgs_open": source_higgs_open,
                "same_source_wz_open": wz_open,
                "schur_open": schur_open,
                "neutral_open": neutral_open,
                "route_statuses": route_statuses,
            },
        },
        {
            "requirement": "matching/running bridge from certified physical readout",
            "evidence": PARENTS["matching_running"],
            "status": "missing",
            "details": parent_statuses["matching_running"],
        },
        {
            "requirement": "retained/proposed-retained proposal authorization",
            "evidence": [PARENTS["retained_route"], PARENTS["campaign_status"]],
            "status": "missing",
            "details": {
                "retained_route_proposal_allowed": certs["retained_route"].get("proposal_allowed"),
                "campaign_proposal_allowed": certs["campaign_status"].get("proposal_allowed"),
            },
        },
    ]

    result = {
        "actual_current_surface_status": "open / positive closure completion audit: retained closure not achieved",
        "objective": "resume positive closure on PR #230",
        "closure_achieved": closure_achieved,
        "completion_audit_passed": FAIL_COUNT == 0,
        "completion_criteria": completion_criteria,
        "missing_requirements": missing_requirements,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Chunk production is complete and O_sp supplies exact same-source "
            "source-side support, but canonical O_H/O_sp-Higgs overlap rows, "
            "taste-radial production rows, "
            "scalar-LSZ authority, an accepted source-overlap or same-source "
            "physical-response bridge, matching/running authority, and retained-"
            "route/campaign proposal authorization remain absent."
        ),
        "post_osp_support_evidence": {
            "source_pole_intaken": source_pole_intaken,
            "canonical_oh_absent": canonical_oh_absent,
            "osp_higgs_rows_absent": osp_higgs_rows_absent,
            "taste_condensate_oh_bridge_blocked": taste_condensate_bridge_blocked,
            "source_coordinate_transport_blocked": source_coordinate_transport_blocked,
            "two_source_taste_radial_support_not_closure": two_source_taste_radial_support_not_closure,
            "two_source_taste_radial_action_not_closure": two_source_taste_radial_action_not_closure,
            "two_source_taste_radial_row_contract_not_closure": two_source_taste_radial_row_contract_not_closure,
            "two_source_taste_radial_row_manifest_not_closure": two_source_taste_radial_row_manifest_not_closure,
            "two_source_taste_radial_chunk_package_not_closure": two_source_taste_radial_chunk_package_not_closure,
            "source_higgs_pole_row_contract_open": source_higgs_pole_row_contract_open,
            "taste_radial_canonical_oh_selector_blocks_symmetry_shortcut": taste_radial_canonical_oh_selector_blocks_symmetry_shortcut,
            "degree_one_higgs_action_premise_not_derived": degree_one_higgs_action_premise_not_derived,
            "degree_one_radial_tangent_oh_theorem_support_not_closure": degree_one_radial_tangent_oh_theorem_support_not_closure,
            "taste_radial_to_source_higgs_promotion_contract_support_not_closure": taste_radial_to_source_higgs_promotion_contract_support_not_closure,
            "fms_post_degree_route_support_not_closure": fms_post_degree_route_support_not_closure,
            "fms_composite_oh_conditional_support_not_closure": fms_composite_oh_conditional_support_not_closure,
            "fms_oh_candidate_action_packet_support_not_closure": fms_oh_candidate_action_packet_support_not_closure,
            "fms_source_overlap_readout_gate_support_not_closure": fms_source_overlap_readout_gate_support_not_closure,
            "fms_action_adoption_minimal_cut_support_not_closure": fms_action_adoption_minimal_cut_support_not_closure,
            "higgs_mass_source_action_bridge_not_closure": higgs_mass_source_action_bridge_not_closure,
            "same_source_ew_higgs_action_ansatz_not_closure": same_source_ew_higgs_action_ansatz_not_closure,
            "same_source_ew_action_adoption_attempt_not_closure": same_source_ew_action_adoption_attempt_not_closure,
            "radial_spurion_action_contract_not_closure": radial_spurion_action_contract_not_closure,
            "additive_source_radial_spurion_incompatibility_not_closure": additive_source_radial_spurion_incompatibility_not_closure,
            "additive_top_subtraction_row_contract_not_closure": additive_top_subtraction_row_contract_not_closure,
            "top_mass_scan_response_harness_not_closure": top_mass_scan_response_harness_not_closure,
            "wz_response_ratio_identifiability_contract_not_closure": wz_response_ratio_identifiability_contract_not_closure,
            "wz_same_source_action_minimal_certificate_cut_open": wz_same_source_action_minimal_certificate_cut_open,
            "wz_accepted_action_response_root_checkpoint_blocks": wz_accepted_action_response_root_checkpoint_blocks,
            "wz_v_authority_firewall_blocks": wz_v_authority_firewall_blocks,
            "post_block100_completion_reopen_audit_blocks": post_block100_completion_reopen_blocks,
            "canonical_oh_wz_common_action_cut_open": canonical_oh_wz_common_action_cut_open,
            "canonical_oh_accepted_action_stretch_blocks_current_stack": canonical_oh_accepted_action_stretch_blocks_current_stack,
            "post_fms_source_overlap_necessity_blocks_current_inference": post_fms_source_overlap_necessity_blocks_current_inference,
            "origin_main_composite_higgs_not_closure": origin_main_composite_higgs_not_closure,
            "origin_main_ew_m_residual_not_closure": origin_main_ew_m_residual_not_closure,
            "z3_triplet_conditional_primitive_not_closure": z3_triplet_conditional_primitive_not_closure,
            "z3_triplet_positive_cone_h2_support_not_transfer": z3_triplet_positive_cone_h2_support_not_transfer,
            "z3_generation_action_lift_not_derived": z3_generation_action_lift_not_derived,
            "z3_lazy_transfer_promotion_not_derived": z3_lazy_transfer_promotion_not_derived,
            "z3_heat_kernel_neutral_transfer_support_not_h3h4": z3_heat_kernel_support_not_h3h4,
            "same_surface_neutral_multiplicity_one_gate_rejects_current_surface": same_surface_neutral_multiplicity_gate_rejects_current_surface,
            "os_transfer_kernel_artifact_absent": os_transfer_kernel_artifact_absent,
            "source_higgs_time_kernel_harness_support_only": source_higgs_time_kernel_harness_support_only,
            "source_higgs_time_kernel_gevp_contract_support_only": source_higgs_time_kernel_gevp_contract_support_only,
            "source_higgs_time_kernel_production_manifest_not_evidence": source_higgs_time_kernel_production_manifest_not_evidence,
            "fms_literature_source_overlap_intake_non_authority": fms_literature_source_overlap_intake_non_authority,
            "schur_higher_shell_production_contract_not_evidence": schur_higher_shell_production_contract_not_evidence,
            "schur_higher_shell_complete_packet_monotonicity_blocks_shortcut": schur_higher_shell_complete_packet_monotonicity_blocks,
            "two_source_taste_radial_primitive_transfer_candidate_not_h3": two_source_taste_radial_primitive_transfer_candidate_not_h3,
            "orthogonal_top_coupling_exclusion_candidate_rejected": orthogonal_top_coupling_exclusion_candidate_rejected,
            "strict_scalar_lsz_moment_fv_authority_absent": strict_scalar_lsz_moment_fv_authority_absent,
            "schur_complement_stieltjes_repair_not_closure": schur_complement_stieltjes_repair_not_closure,
            "schur_complement_complete_monotonicity_not_closure": schur_complement_complete_monotonicity_not_closure,
            "schur_x_given_source_one_pole_scout_not_authority": schur_x_given_source_one_pole_scout_not_authority,
            "future_bridge_file_presence": future_bridge_presence,
        },
        "bare_retained_allowed": False,
        "prompt_to_artifact_checklist": checklist,
        "parent_certificates": PARENTS,
        "parent_statuses": parent_statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not treat completed chunks as scalar-LSZ or source-overlap authority",
            "does not treat W/Z smoke rows as production response rows",
            "does not treat package hierarchy v as PR230 W/Z absolute-normalization authority",
            "does not treat Z3 H2 positive-cone support as physical neutral transfer or primitive irreducibility",
            "does not treat a finite-group Z3 heat kernel as PR230 physical transfer without a same-surface action selecting its heat time and H4 source/canonical-Higgs coupling",
            "does not treat the same-surface neutral multiplicity-one intake gate as accepted O_H authority",
            "does not treat the current additive top source as a no-independent-top radial spurion",
            "does not treat the additive-top subtraction formula as closure before additive Jacobian rows, W/Z rows, matched covariance, strict g2, and accepted action exist",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Supply one fresh parseable same-surface artifact beyond O_sp: "
            "a same-surface neutral multiplicity-one certificate accepted by "
            "outputs/yt_pr230_same_surface_neutral_multiplicity_one_gate_2026-05-07.json, "
            "then O_sp-Higgs pole rows with canonical O_H identity/normalization "
            "(Res_C_sp_sp=1, Res_C_spH, Res_C_HH), a real source-coordinate "
            "transport certificate from the uniform PR230 source to canonical "
            "O_H, a genuine same-source EW action plus production W/Z mass-fit "
            "rows, matched covariance and non-observed g2 certificate, "
            "same-surface Schur A/B/C kernel rows with scalar denominator "
            "closure, or a neutral-sector primitive-cone/irreducibility "
            "certificate.  Then rerun assembly, retained-"
            "route, and campaign gates before any proposal wording."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
