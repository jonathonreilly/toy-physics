#!/usr/bin/env python3
"""
PR #230 FMS action-adoption minimal cut.

The FMS route is the cleanest current physics target only if the candidate
O_H packet becomes an accepted same-surface action/operator artifact.  This
runner records the exact root cut for that adoption, distinguishes real
support already present from the still-missing roots, and keeps the current
surface open with proposal_allowed=false.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json"
)

PARENTS = {
    "fms_oh_candidate_action_packet": "outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json",
    "fms_source_overlap_readout_gate": "outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json",
    "degree_one_radial_tangent_oh_theorem": "outputs/yt_pr230_degree_one_radial_tangent_oh_theorem_2026-05-07.json",
    "genuine_source_pole_artifact_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
    "source_higgs_direct_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "source_higgs_pole_row_acceptance_contract": "outputs/yt_pr230_source_higgs_pole_row_acceptance_contract_2026-05-06.json",
    "source_higgs_time_kernel_manifest": "outputs/yt_pr230_source_higgs_time_kernel_production_manifest_2026-05-07.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "radial_spurion_action_contract": "outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "accepted_same_surface_ew_higgs_action": "outputs/yt_pr230_same_surface_ew_higgs_action_certificate_2026-05-07.json",
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_pr230_canonical_oh_certificate_2026-05-07.json",
    "source_higgs_pole_rows": "outputs/yt_pr230_source_higgs_pole_rows_2026-05-06.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
}

FORBIDDEN_FIREWALL = {
    "used_hunit_matrix_element_readout": False,
    "used_hunit_as_operator": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yt": False,
    "used_observed_wz_or_g2": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "used_reduced_pilots_as_production": False,
    "used_fms_literature_as_proof_authority": False,
    "used_taste_radial_axis_as_canonical_oh": False,
    "identified_osp_with_oh_without_rows": False,
    "aliased_c_sx_to_c_sh": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "set_g2_equal_one": False,
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def present_map(paths: dict[str, str]) -> dict[str, bool]:
    return {name: (ROOT / rel).exists() for name, rel in paths.items()}


def support_vertices(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": "O_sp_source_pole",
            "satisfied": certs["genuine_source_pole_artifact_intake"].get(
                "artifact_is_genuine_current_surface_support"
            )
            is True
            and certs["genuine_source_pole_artifact_intake"].get(
                "artifact_is_physics_closure"
            )
            is False,
            "role": "same-source LSZ source-side normalization",
            "proof_limit": "does not identify O_sp with canonical O_H",
        },
        {
            "id": "degree_one_radial_axis",
            "satisfied": certs["degree_one_radial_tangent_oh_theorem"].get(
                "degree_one_radial_tangent_oh_theorem_passed"
            )
            is True
            and certs["degree_one_radial_tangent_oh_theorem"].get(
                "same_surface_linear_tangent_premise_derived"
            )
            is False,
            "role": "unique taste-radial axis under a future degree-one action premise",
            "proof_limit": "the degree-one premise and canonical LSZ metric are not derived",
        },
        {
            "id": "fms_candidate_packet",
            "satisfied": certs["fms_oh_candidate_action_packet"].get(
                "fms_oh_candidate_action_packet_passed"
            )
            is True
            and certs["fms_oh_candidate_action_packet"].get("accepted_current_surface")
            is False,
            "role": "candidate O_H and action-shape packet",
            "proof_limit": "candidate packet is not an accepted Cl(3)/Z3 same-surface action",
        },
        {
            "id": "source_overlap_readout_formula",
            "satisfied": certs["fms_source_overlap_readout_gate"].get(
                "fms_source_overlap_readout_gate_passed"
            )
            is True
            and certs["fms_source_overlap_readout_gate"].get("readout_executable_now")
            is False,
            "role": "future kappa_sH residue formula",
            "proof_limit": "strict C_ss/C_sH/C_HH pole rows are absent",
        },
        {
            "id": "time_kernel_manifest",
            "satisfied": certs["source_higgs_time_kernel_manifest"].get(
                "time_kernel_schema_version"
            )
            == "source_higgs_time_kernel_v1"
            and certs["source_higgs_time_kernel_manifest"].get("chunk_count")
            == 63
            and certs["source_higgs_time_kernel_manifest"].get(
                "closure_launch_authorized_now"
            )
            is False,
            "role": "future non-colliding row campaign commands",
            "proof_limit": "manifest is not evidence and is blocked until O_H is accepted",
        },
    ]


def root_cut(
    certs: dict[str, dict[str, Any]], futures: dict[str, bool]
) -> list[dict[str, Any]]:
    canonical_gate = certs["canonical_higgs_operator_gate"]
    action_gate = certs["same_source_ew_action_gate"]
    adoption = certs["same_source_ew_action_adoption_attempt"]
    pole_contract = certs["source_higgs_pole_row_acceptance_contract"]
    manifest = certs["source_higgs_time_kernel_manifest"]
    direct_contract = certs["source_higgs_direct_pole_row_contract"]

    return [
        {
            "id": "same_surface_action_derivation_or_accepted_extension",
            "current_satisfied": (
                futures["accepted_same_surface_ew_higgs_action"]
                or futures["accepted_same_source_ew_action"]
                or action_gate.get("same_source_ew_action_ready") is True
            ),
            "current_evidence": status(action_gate),
            "required_artifact": [
                FUTURE_FILES["accepted_same_surface_ew_higgs_action"],
                FUTURE_FILES["accepted_same_source_ew_action"],
            ],
        },
        {
            "id": "dynamic_phi_and_gauge_covariant_higgs_kinetic_term",
            "current_satisfied": adoption.get("adoption_allowed_now") is True,
            "current_evidence": status(adoption),
            "required_artifact": "accepted action certificate with Phi, gauge kinetic semantics, and update/ensemble authority",
        },
        {
            "id": "canonical_radial_h_lsz_metric_and_v",
            "current_satisfied": canonical_gate.get("candidate_valid") is True,
            "current_evidence": status(canonical_gate),
            "required_artifact": FUTURE_FILES["canonical_oh_certificate"],
        },
        {
            "id": "fms_OH_identity_and_normalization",
            "current_satisfied": canonical_gate.get("candidate_present") is True
            and canonical_gate.get("candidate_valid") is True,
            "current_evidence": status(canonical_gate),
            "required_artifact": "O_H = Phi^dagger Phi - <Phi^dagger Phi> with canonical normalization and same-surface provenance",
        },
        {
            "id": "same_source_derivative_no_independent_top_source",
            "current_satisfied": certs["radial_spurion_action_contract"].get(
                "current_surface_contract_satisfied"
            )
            is True,
            "current_evidence": status(certs["radial_spurion_action_contract"]),
            "required_artifact": "dS/ds = sum_x O_H(x), with no independent additive top bare-mass source",
        },
        {
            "id": "production_C_ss_C_sH_C_HH_pole_rows",
            "current_satisfied": pole_contract.get("closure_contract_satisfied") is True
            and (
                futures["source_higgs_pole_rows"]
                or futures["source_higgs_measurement_rows"]
            ),
            "current_evidence": status(pole_contract),
            "required_artifact": [
                FUTURE_FILES["source_higgs_pole_rows"],
                FUTURE_FILES["source_higgs_measurement_rows"],
            ],
        },
        {
            "id": "pole_covariance_fv_ir_model_class_authority",
            "current_satisfied": direct_contract.get("current_surface_contract_satisfied")
            is True
            and manifest.get("closure_launch_authorized_now") is True,
            "current_evidence": status(direct_contract),
            "required_artifact": "isolated-pole residue, covariance, FV/IR, zero-mode, and model-class certificate",
        },
        {
            "id": "aggregate_retained_route_gates",
            "current_satisfied": certs["full_positive_assembly"].get(
                "proposal_allowed"
            )
            is True
            and certs["retained_route"].get("proposal_allowed") is True
            and certs["campaign_status"].get("proposal_allowed") is True,
            "current_evidence": (
                f"{status(certs['full_positive_assembly'])}; "
                f"{status(certs['retained_route'])}; "
                f"{status(certs['campaign_status'])}"
            ),
            "required_artifact": "assembly, retained-route, and campaign proposal certificates",
        },
    ]


def main() -> int:
    print("PR #230 FMS action-adoption minimal cut")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    futures = present_map(FUTURE_FILES)
    support = support_vertices(certs)
    roots = root_cut(certs, futures)
    missing_roots = [row["id"] for row in roots if row["current_satisfied"] is not True]
    support_clean = all(row["satisfied"] is True for row in support)
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())

    fms_packet_support_only = (
        certs["fms_oh_candidate_action_packet"].get("fms_oh_candidate_action_packet_passed")
        is True
        and certs["fms_oh_candidate_action_packet"].get("proposal_allowed") is False
        and certs["fms_oh_candidate_action_packet"].get("accepted_current_surface")
        is False
        and certs["fms_oh_candidate_action_packet"].get("same_surface_cl3_z3_derived")
        is False
        and certs["fms_oh_candidate_action_packet"].get("closure_authorized")
        is False
    )
    adoption_attempt_blocked = (
        certs["same_source_ew_action_adoption_attempt"].get(
            "same_source_ew_action_adoption_attempt_passed"
        )
        is True
        and certs["same_source_ew_action_adoption_attempt"].get(
            "adoption_allowed_now"
        )
        is False
    )
    canonical_oh_absent = (
        certs["canonical_higgs_operator_gate"].get("candidate_present") is False
        and certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    strict_rows_absent = (
        certs["source_higgs_pole_row_acceptance_contract"].get("rows_present")
        is False
        and certs["source_higgs_pole_row_acceptance_contract"].get(
            "closure_contract_satisfied"
        )
        is False
    )
    aggregate_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    current_adoption_allowed = not missing_roots

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("support-vertices-loaded", support_clean, str(support))
    report("fms-packet-support-only", fms_packet_support_only, statuses["fms_oh_candidate_action_packet"])
    report("same-source-action-adoption-attempt-blocked", adoption_attempt_blocked, statuses["same_source_ew_action_adoption_attempt"])
    report("canonical-oh-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("strict-source-higgs-pole-rows-absent", strict_rows_absent, statuses["source_higgs_pole_row_acceptance_contract"])
    report("root-cut-not-satisfied-now", bool(missing_roots), f"missing={missing_roots}")
    report("aggregate-gates-open", aggregate_open, "assembly/retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("adoption-not-allowed-now", not current_adoption_allowed, f"adoption_allowed_now={current_adoption_allowed}")

    cut_passed = (
        not missing
        and not proposal_parents
        and support_clean
        and fms_packet_support_only
        and adoption_attempt_blocked
        and canonical_oh_absent
        and strict_rows_absent
        and bool(missing_roots)
        and aggregate_open
        and firewall_clean
        and not current_adoption_allowed
    )

    result = {
        "actual_current_surface_status": (
            "exact-support / FMS action-adoption minimal cut; current PR230 "
            "surface has candidate support but no adopted same-surface action, "
            "canonical O_H, or strict pole rows"
        ),
        "conditional_surface_status": (
            "exact-support for the FMS source-Higgs route only after every root "
            "in adoption_root_cut is satisfied and aggregate route gates pass"
        ),
        "hypothetical_axiom_status": (
            "external gauge-Higgs extension remains hypothetical until accepted "
            "or derived from the Cl(3)/Z3 substrate"
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The FMS packet is a candidate/action shape only.  The current "
            "surface lacks an accepted action derivation, dynamic Phi/canonical "
            "radial LSZ metric, O_H identity, same-source derivative theorem, "
            "and production C_ss/C_sH/C_HH pole rows."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "fms_action_adoption_minimal_cut_passed": cut_passed,
        "adoption_allowed_now": current_adoption_allowed,
        "current_surface_action_adopted": False,
        "accepted_current_surface": False,
        "same_surface_cl3_z3_derived": False,
        "closure_authorized": False,
        "support_vertices": support,
        "adoption_root_cut": roots,
        "missing_root_vertices": missing_roots,
        "future_files": FUTURE_FILES,
        "future_file_presence": futures,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not identify taste-radial x or O_sp with O_H",
            "does not set kappa_s, c2, Z_match, or g2 to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat FMS literature or the action ansatz as same-surface proof authority",
        ],
        "next_exact_action": (
            "Derive or supply the same-surface action/canonical O_H root "
            "certificate; after it passes, launch the existing source-Higgs "
            "time-kernel rows and run pole/covariance/FV/IR/source-overlap gates."
        ),
        "parent_statuses": statuses,
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
