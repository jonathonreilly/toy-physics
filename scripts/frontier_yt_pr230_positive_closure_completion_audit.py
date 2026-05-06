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
    "z3_generation_action_lift_attempt": "outputs/yt_pr230_z3_generation_action_lift_attempt_2026-05-06.json",
    "z3_lazy_transfer_promotion_attempt": "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json",
    "two_source_taste_radial_chart": "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json",
    "two_source_taste_radial_action": "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json",
    "two_source_taste_radial_row_contract": "outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json",
    "two_source_taste_radial_row_production_manifest": "outputs/yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json",
    "taste_radial_canonical_oh_selector_gate": "outputs/yt_pr230_taste_radial_canonical_oh_selector_gate_2026-05-06.json",
    "degree_one_higgs_action_premise_gate": "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json",
    "fms_post_degree_route_rescore": "outputs/yt_pr230_fms_post_degree_route_rescore_2026-05-06.json",
    "fms_composite_oh_conditional_theorem": "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json",
    "higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "post_fms_source_overlap_necessity_gate": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
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
    no_unclosed_future_bridge_files_present = (
        all(
            present is False
            for name, present in future_bridge_presence.items()
            if name != "two_source_taste_radial_action"
        )
        and two_source_action_support_present
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
    wz_open = (
        certs["wz_same_source_action"].get("same_source_ew_action_ready") is not True
        and certs["wz_mass_fit_response_row_builder"].get("strict_wz_mass_fit_response_row_builder_passed")
        is not True
        and certs["top_wz_matched_covariance_builder"].get("strict_top_wz_matched_covariance_builder_passed")
        is not True
        and certs["electroweak_g2_builder"].get("strict_electroweak_g2_certificate_passed") is not True
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
    report("taste-radial-canonical-oh-selector-blocks-symmetry-shortcut", taste_radial_canonical_oh_selector_blocks_symmetry_shortcut, parent_statuses["taste_radial_canonical_oh_selector_gate"])
    report("degree-one-higgs-action-premise-not-derived", degree_one_higgs_action_premise_not_derived, parent_statuses["degree_one_higgs_action_premise_gate"])
    report("fms-post-degree-route-rescore-support-not-closure", fms_post_degree_route_support_not_closure, parent_statuses["fms_post_degree_route_rescore"])
    report("fms-composite-oh-conditional-support-not-closure", fms_composite_oh_conditional_support_not_closure, parent_statuses["fms_composite_oh_conditional_theorem"])
    report("higgs-mass-source-action-bridge-not-closure", higgs_mass_source_action_bridge_not_closure, parent_statuses["higgs_mass_source_action_bridge"])
    report("same-source-ew-higgs-action-ansatz-not-closure", same_source_ew_higgs_action_ansatz_not_closure, parent_statuses["same_source_ew_higgs_action_ansatz_gate"])
    report("same-source-ew-action-adoption-attempt-not-closure", same_source_ew_action_adoption_attempt_not_closure, parent_statuses["same_source_ew_action_adoption_attempt"])
    report("post-fms-source-overlap-necessity-blocks-current-inference", post_fms_source_overlap_necessity_blocks_current_inference, parent_statuses["post_fms_source_overlap_necessity_gate"])
    report("source-higgs-overlap-kappa-contract-not-closure", source_higgs_overlap_kappa_contract_not_closure, parent_statuses["source_higgs_overlap_kappa_contract"])
    report("origin-main-composite-higgs-intake-not-closure", origin_main_composite_higgs_not_closure, parent_statuses["origin_main_composite_higgs_intake_guard"])
    report("origin-main-ew-m-residual-intake-not-closure", origin_main_ew_m_residual_not_closure, parent_statuses["origin_main_ew_m_residual_intake_guard"])
    report("z3-triplet-conditional-primitive-support-not-closure", z3_triplet_conditional_primitive_not_closure, parent_statuses["z3_triplet_conditional_primitive_cone"])
    report("z3-generation-action-lift-not-derived", z3_generation_action_lift_not_derived, parent_statuses["z3_generation_action_lift_attempt"])
    report("z3-lazy-transfer-promotion-not-derived", z3_lazy_transfer_promotion_not_derived, parent_statuses["z3_lazy_transfer_promotion_attempt"])
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
            "taste_radial_canonical_oh_selector_blocks_symmetry_shortcut": taste_radial_canonical_oh_selector_blocks_symmetry_shortcut,
            "degree_one_higgs_action_premise_not_derived": degree_one_higgs_action_premise_not_derived,
            "fms_post_degree_route_support_not_closure": fms_post_degree_route_support_not_closure,
            "fms_composite_oh_conditional_support_not_closure": fms_composite_oh_conditional_support_not_closure,
            "higgs_mass_source_action_bridge_not_closure": higgs_mass_source_action_bridge_not_closure,
            "same_source_ew_higgs_action_ansatz_not_closure": same_source_ew_higgs_action_ansatz_not_closure,
            "same_source_ew_action_adoption_attempt_not_closure": same_source_ew_action_adoption_attempt_not_closure,
            "post_fms_source_overlap_necessity_blocks_current_inference": post_fms_source_overlap_necessity_blocks_current_inference,
            "origin_main_composite_higgs_not_closure": origin_main_composite_higgs_not_closure,
            "origin_main_ew_m_residual_not_closure": origin_main_ew_m_residual_not_closure,
            "z3_triplet_conditional_primitive_not_closure": z3_triplet_conditional_primitive_not_closure,
            "z3_generation_action_lift_not_derived": z3_generation_action_lift_not_derived,
            "z3_lazy_transfer_promotion_not_derived": z3_lazy_transfer_promotion_not_derived,
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
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not set c2=1, Z_match=1, or kappa_s=1",
        ],
        "exact_next_action": (
            "Supply one fresh parseable same-surface artifact beyond O_sp: "
            "O_sp-Higgs pole rows with canonical O_H identity/normalization "
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
