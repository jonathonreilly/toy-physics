#!/usr/bin/env python3
"""
PR #230 direct source-Higgs pole-row contract.

This runner packages the selected source-Higgs Gram-purity lane as a positive
future-row acceptance contract.  It does not construct O_H and does not write
production C_sH/C_HH rows.  It states exactly what a future same-surface
O_H_candidate plus C_ss/C_sH/C_HH pole-row packet must contain before the
existing builder and Gram-purity postprocessor may treat it as PR230 bridge
evidence.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json"
)

PARENTS = {
    "source_overlap_route_selection": "outputs/yt_pr230_source_overlap_route_selection_2026-05-03.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "genuine_source_pole_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
    "source_higgs_production_readiness_gate": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_pole_residue_extractor": "outputs/yt_source_higgs_pole_residue_extractor_2026-05-03.json",
    "source_higgs_certificate_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / path).exists() for name, path in FUTURE_ARTIFACTS.items()}


def gram(c_ss: float, c_sH: float, c_HH: float) -> dict[str, Any]:
    product = c_ss * c_HH
    delta = product - c_sH * c_sH
    rho = c_sH / math.sqrt(product) if product > 0.0 else float("nan")
    c_spH = c_sH / math.sqrt(c_ss) if c_ss > 0.0 else float("nan")
    delta_spH = c_HH - c_spH * c_spH if math.isfinite(c_spH) else float("nan")
    rho_spH = c_spH / math.sqrt(c_HH) if c_HH > 0.0 and math.isfinite(c_spH) else float("nan")
    pure = (
        c_ss > 0.0
        and c_HH > 0.0
        and abs(delta) <= 1.0e-12
        and math.isfinite(rho)
        and abs(abs(rho) - 1.0) <= 1.0e-12
    )
    return {
        "Res_C_ss": c_ss,
        "Res_C_sH": c_sH,
        "Res_C_HH": c_HH,
        "gram_determinant": delta,
        "normalized_overlap_rho_sH": rho,
        "Res_C_spH": c_spH,
        "osp_higgs_gram_determinant": delta_spH,
        "normalized_overlap_rho_spH": rho_spH,
        "pure_bridge_condition_passed": pure,
    }


def witness_rows() -> dict[str, Any]:
    pure = gram(2.25, 3.0, 4.0)
    pure["witness_kind"] = "pure_same_pole"
    pure["interpretation"] = "O_sp and O_H create the same isolated state up to sign/normalization"

    mixed = gram(2.25, 2.4, 4.0)
    mixed["witness_kind"] = "mixed_same_source_readout"
    mixed["interpretation"] = "nonzero orthogonal scalar admixture; source row alone cannot remove it"

    sign_flip = gram(2.25, -3.0, 4.0)
    sign_flip["witness_kind"] = "pure_same_pole_opposite_sign"
    sign_flip["interpretation"] = "pure bridge with opposite convention sign"

    return {
        "pure_row": pure,
        "mixed_row": mixed,
        "sign_flip_row": sign_flip,
        "source_side_normalization": "O_sp = sqrt(Dprime_ss_at_pole) O_s; Res(C_sp,sp)=1",
        "acceptance_condition": "Delta=0 and abs(rho_spH)=1 at a nondegenerate isolated pole, after O_H certification and FV/IR/model-class gates",
    }


def row_packet_schema() -> dict[str, Any]:
    return {
        "future_input": FUTURE_ARTIFACTS["source_higgs_measurement_rows"],
        "operator_block": {
            "operator_id": "nonempty O_H_candidate id",
            "canonical_higgs_operator_identity_passed": True,
            "identity_certificate": FUTURE_ARTIFACTS["canonical_higgs_operator_certificate"],
            "normalization_certificate": "same-surface O_H normalization certificate",
            "hunit_used_as_operator": False,
            "static_ew_algebra_used_as_operator": False,
        },
        "row_block": {
            "phase": "production",
            "same_ensemble": True,
            "same_source_coordinate": True,
            "source_coordinate": "same PR230 scalar source coordinate",
            "pole_residue_rows": [
                "Res_C_ss, Res_C_sH, Res_C_HH plus errors/covariance",
                "selected_pole_row or isolated_pole_fit_passed",
            ],
            "model_class_or_pole_saturation_certificate_passed": True,
            "fv_ir_zero_mode_control_passed": True,
        },
        "forbidden_firewall": {
            "used_observed_targets_as_selectors": False,
            "used_yt_ward_identity": False,
            "used_alpha_lm_or_plaquette": False,
            "used_hunit_matrix_element_readout": False,
            "used_static_ew_algebra_as_operator": False,
            "treated_C_sx_C_xx_as_C_sH_C_HH": False,
        },
        "pipeline": [
            "frontier_yt_source_higgs_pole_residue_extractor.py",
            "frontier_yt_source_higgs_cross_correlator_certificate_builder.py",
            "frontier_yt_source_higgs_gram_purity_postprocessor.py",
            "frontier_yt_pr230_full_positive_closure_assembly_gate.py",
            "frontier_yt_retained_closure_route_certificate.py",
            "frontier_yt_pr230_campaign_status_certificate.py",
        ],
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_hunit_as_operator": False,
        "used_yt_ward_identity": False,
        "used_observed_targets_as_selectors": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "used_reduced_pilot_as_production": False,
        "set_kappa_s_equal_one": False,
        "set_cos_theta_equal_one": False,
        "treated_static_ew_algebra_as_oh": False,
        "treated_c_sx_c_xx_as_c_sh_c_hh": False,
        "claimed_retained_or_proposed_retained": False,
        "touched_live_chunk_worker": False,
    }


def main() -> int:
    print("PR #230 direct source-Higgs pole-row contract")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    witness = witness_rows()
    schema = row_packet_schema()
    firewall = forbidden_firewall()

    source_higgs_primary_route_selected = (
        parents["source_overlap_route_selection"].get("selected_primary_route")
        == "same_surface_source_higgs_gram_purity"
        and parents["source_overlap_route_selection"].get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and not futures["canonical_higgs_operator_certificate"]
    )
    osp_constructed_not_oh = (
        parents["legendre_source_pole_operator"].get("source_pole_operator_constructed")
        is True
        and parents["legendre_source_pole_operator"].get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
    )
    genuine_osp_intake_loaded = (
        parents["genuine_source_pole_intake"].get(
            "artifact_is_genuine_current_surface_support"
        )
        is True
        and parents["genuine_source_pole_intake"].get("artifact_is_physics_closure")
        is False
    )
    production_readiness_blocked = (
        parents["source_higgs_production_readiness_gate"].get("source_higgs_launch_ready")
        is False
        and parents["source_higgs_production_readiness_gate"].get(
            "taste_radial_rows_are_c_sx_c_xx_not_c_sH_c_HH"
        )
        is True
    )
    pole_extractor_waits = (
        parents["source_higgs_pole_residue_extractor"].get("gate_passed") is False
        and parents["source_higgs_pole_residue_extractor"].get("rows_written") is False
    )
    builder_waits = (
        parents["source_higgs_certificate_builder"].get("input_present") is False
        and parents["source_higgs_certificate_builder"].get("candidate_written") is False
    )
    gram_postprocessor_waits = (
        parents["source_higgs_gram_postprocessor"].get("candidate_present") is False
        and parents["source_higgs_gram_postprocessor"].get(
            "osp_higgs_gram_purity_gate_passed"
        )
        is False
    )
    kappa_contract_loaded = (
        parents["source_higgs_overlap_kappa_contract"].get(
            "source_higgs_overlap_kappa_contract_passed"
        )
        is True
        and parents["source_higgs_overlap_kappa_contract"].get("proposal_allowed")
        is False
    )
    aggregate_still_open = (
        parents["full_positive_assembly"].get("proposal_allowed") is False
        and parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    pure_witness_passes = witness["pure_row"]["pure_bridge_condition_passed"] is True
    sign_flip_is_convention = (
        witness["sign_flip_row"]["pure_bridge_condition_passed"] is True
        and witness["pure_row"]["normalized_overlap_rho_spH"]
        == -witness["sign_flip_row"]["normalized_overlap_rho_spH"]
    )
    mixed_witness_fails = witness["mixed_row"]["pure_bridge_condition_passed"] is False
    current_rows_absent = (
        not futures["source_higgs_measurement_rows"]
        and not futures["source_higgs_production_certificate"]
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("source-higgs-primary-route-selected", source_higgs_primary_route_selected, statuses["source_overlap_route_selection"])
    report("canonical-OH-certificate-absent", canonical_oh_absent, FUTURE_ARTIFACTS["canonical_higgs_operator_certificate"])
    report("Osp-constructed-but-not-OH", osp_constructed_not_oh, statuses["legendre_source_pole_operator"])
    report("genuine-Osp-intake-loaded", genuine_osp_intake_loaded, statuses["genuine_source_pole_intake"])
    report("production-readiness-blocked-until-OH", production_readiness_blocked, statuses["source_higgs_production_readiness_gate"])
    report("pole-residue-extractor-awaits-valid-rows", pole_extractor_waits, statuses["source_higgs_pole_residue_extractor"])
    report("cross-correlator-builder-awaits-rows", builder_waits, statuses["source_higgs_certificate_builder"])
    report("gram-postprocessor-awaits-candidate", gram_postprocessor_waits, statuses["source_higgs_gram_postprocessor"])
    report("overlap-kappa-contract-loaded", kappa_contract_loaded, statuses["source_higgs_overlap_kappa_contract"])
    report("pure-witness-passes-Gram", pure_witness_passes, f"Delta={witness['pure_row']['gram_determinant']}")
    report("sign-flip-treated-as-convention", sign_flip_is_convention, "rho sign flips, abs(rho)=1")
    report("mixed-witness-fails-Gram", mixed_witness_fails, f"rho={witness['mixed_row']['normalized_overlap_rho_spH']}")
    report("current-source-Higgs-pole-rows-absent", current_rows_absent, str(futures))
    report("aggregate-gates-deny-proposal", aggregate_still_open, "proposal_allowed=false")
    report("forbidden-firewall-clean", not any(firewall.values()), str(firewall))
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact-support / direct source-Higgs pole-row contract; O_H and "
            "production C_sH/C_HH rows are absent"
        ),
        "conditional_surface_status": (
            "exact support for a future same-surface certified O_H_candidate "
            "plus C_ss/C_sH/C_HH pole-row packet that passes Gram purity, "
            "FV/IR/model-class, and retained-route gates"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The runner supplies an acceptance contract and pure/mixed witness "
            "only.  The current surface has no certified canonical O_H and no "
            "production source-Higgs pole rows."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "source_higgs_direct_pole_row_contract_passed": passed,
        "current_surface_contract_satisfied": False,
        "future_artifact_presence": futures,
        "row_packet_schema": schema,
        "witness": witness,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not construct O_H or define it by fiat",
            "does not use H_unit, static EW algebra, C_sx/C_xx aliases, or FMS context as O_H",
            "does not set kappa_s=1 or cos(theta)=1",
            "does not use observed y_t, observed masses, yt_ward_identity, alpha_LM, plaquette, or u0",
            "does not write production source-Higgs rows or touch the live chunk worker",
        ],
        "exact_next_action": (
            "Derive or supply the same-surface canonical O_H certificate, then "
            "run a separate source-Higgs production row packet through the "
            "pole-residue extractor, cross-correlator builder, Gram-purity "
            "postprocessor, full assembly, retained-route, and campaign gates."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
