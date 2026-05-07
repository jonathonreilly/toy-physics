#!/usr/bin/env python3
"""
PR #230 FMS / gauge-invariant-field source-overlap literature intake.

This runner records a targeted literature bridge for the cleanest source-Higgs
route.  The bridge is deliberately non-authoritative: FMS and modern
gauge-invariant-field papers motivate a canonical composite Higgs operator
only after a same-surface EW/Higgs action, scalar doublet, radial background,
and canonical LSZ normalization are present.  They do not derive the PR230
Cl(3)/Z3 source-to-Higgs overlap or set kappa_s.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_fms_literature_source_overlap_intake_2026-05-07.json"
)

PARENTS = {
    "fms_conditional_theorem": "outputs/yt_pr230_fms_composite_oh_conditional_theorem_2026-05-06.json",
    "fms_post_degree_route_rescore": "outputs/yt_pr230_fms_post_degree_route_rescore_2026-05-06.json",
    "higgs_mass_source_action_bridge": "outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json",
    "same_source_ew_higgs_action_ansatz_gate": "outputs/yt_pr230_same_source_ew_higgs_action_ansatz_gate_2026-05-06.json",
    "same_source_ew_action_adoption_attempt": "outputs/yt_pr230_same_source_ew_action_adoption_attempt_2026-05-06.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_overlap_kappa_contract": "outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json",
    "post_fms_source_overlap_necessity": "outputs/yt_pr230_post_fms_source_overlap_necessity_gate_2026-05-06.json",
    "genuine_source_pole_intake": "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json",
    "taste_radial_promotion_contract": "outputs/yt_pr230_taste_radial_to_source_higgs_promotion_contract_2026-05-07.json",
    "time_kernel_harness": "outputs/yt_pr230_source_higgs_time_kernel_harness_extension_gate_2026-05-07.json",
    "time_kernel_gevp": "outputs/yt_pr230_source_higgs_time_kernel_gevp_contract_2026-05-07.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_FILES = {
    "accepted_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_pole_residue_packet": "outputs/yt_pr230_source_higgs_pole_residue_packet_2026-05-07.json",
    "time_kernel_production_rows": "outputs/yt_pr230_source_higgs_time_kernel_rows_2026-05-07.json",
}

LITERATURE_REFERENCES = [
    {
        "id": "fms_1980",
        "title": "Higgs phenomenon without a symmetry breaking order parameter",
        "authors": "Froehlich, Morchio, Strocchi",
        "doi": "10.1016/0370-2693(80)90594-8",
        "role": "non-derivation context for gauge-invariant composite fields",
    },
    {
        "id": "maas_2014_observables",
        "title": "Observables in Higgsed Theories",
        "url": "https://arxiv.org/abs/1410.2740",
        "role": "non-derivation context for FMS mass correspondence and lattice checks",
    },
    {
        "id": "maas_pedro_2016_2hdm",
        "title": "Gauge invariance and the physical spectrum in the two-Higgs-doublet model",
        "url": "https://arxiv.org/abs/1601.02006",
        "role": "non-derivation context for model-dependent composite spectra",
    },
    {
        "id": "gauge_invariant_quantum_fields_2024",
        "title": "Gauge-invariant quantum fields",
        "doi": "10.1140/epjc/s10052-024-13317-0",
        "role": "non-derivation context for dynamical gauge-invariant scalar fields and LSZ on mass eigenstates",
    },
]

FORBIDDEN_FIREWALL = {
    "used_fms_literature_as_same_surface_action_proof": False,
    "used_fms_literature_as_kappa_s_proof": False,
    "used_hunit_matrix_element_readout": False,
    "used_yt_ward_identity": False,
    "used_observed_top_or_yukawa_as_selector": False,
    "used_observed_wz_or_g2_as_selector": False,
    "used_alpha_lm_plaquette_or_u0": False,
    "used_reduced_pilots_as_production_evidence": False,
    "set_kappa_s_equal_one": False,
    "set_c2_equal_one": False,
    "set_z_match_equal_one": False,
    "set_g2_equal_one": False,
    "identified_taste_radial_x_with_canonical_O_H": False,
    "identified_O_sp_with_canonical_O_H": False,
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def future_presence() -> dict[str, bool]:
    return {name: (ROOT / path).exists() for name, path in FUTURE_FILES.items()}


def acceptance_contract() -> dict[str, Any]:
    return {
        "future_status": "exact-support if all rows pass; not retained until retained-route audit",
        "required_same_surface_inputs": [
            "accepted EW/Higgs action with scalar doublet Phi on the PR230 surface",
            "canonical kinetic normalization and radial background v from that action",
            "gauge-invariant scalar O_FMS = (Phi^dagger Phi - v^2/2) / v or equivalent canonical field",
            "source-coordinate theorem identifying O_sp or taste-radial x with O_FMS, or direct C_spH/C_HH pole rows",
            "isolated nondegenerate scalar pole with FV/IR/threshold authority",
            "residue packet containing Res_C_sp_sp, Res_C_spH, Res_C_HH and Gram-purity check",
        ],
        "blocked_shortcuts": [
            "FMS method name without same-surface action",
            "literature O_H formula without PR230 Phi/v/canonical kinetic term",
            "O_sp source-side normalization alone",
            "taste-radial C_sx/C_xx relabeling",
            "reduced time-kernel GEVP diagnostic",
            "kappa_s = 1 by convention",
        ],
        "immediate_next_artifact": (
            "Build an accepted same-surface EW/Higgs action/O_FMS certificate "
            "or produce production C_spH/C_HH pole rows that measure the "
            "source-Higgs overlap directly."
        ),
    }


def main() -> int:
    print("PR #230 FMS literature source-overlap intake")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    futures = future_presence()

    literature_bridge_scope_ok = all(
        "non-derivation context" in row["role"] for row in LITERATURE_REFERENCES
    )
    fms_conditional_support_only = (
        "FMS composite O_H theorem" in statuses["fms_conditional_theorem"]
        and certs["fms_conditional_theorem"].get("fms_composite_oh_conditional_theorem_passed") is True
        and certs["fms_conditional_theorem"].get("proposal_allowed") is False
    )
    action_formula_support_only = (
        "Higgs mass-source action bridge" in statuses["higgs_mass_source_action_bridge"]
        and certs["higgs_mass_source_action_bridge"].get("proposal_allowed") is False
        and "same-surface EW/Higgs action" in statuses["higgs_mass_source_action_bridge"]
    )
    action_adoption_blocked = (
        certs["same_source_ew_higgs_action_ansatz_gate"].get("current_surface_adoption_passed") is False
        and certs["same_source_ew_action_adoption_attempt"].get(
            "same_source_ew_action_adoption_attempt_passed"
        )
        is True
        and certs["same_source_ew_action_adoption_attempt"].get("proposal_allowed") is False
    )
    canonical_oh_absent = (
        certs["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and certs["canonical_higgs_operator_gate"].get("proposal_allowed") is False
        and not futures["canonical_higgs_operator_certificate"]
    )
    source_higgs_rows_absent = (
        certs["source_higgs_builder"].get("input_present") is False
        and certs["source_higgs_builder"].get("candidate_written") is False
        and certs["source_higgs_gram"].get("source_higgs_gram_purity_gate_passed") is False
        and not futures["source_higgs_measurement_rows"]
        and not futures["source_higgs_pole_residue_packet"]
    )
    source_overlap_still_open = (
        certs["source_higgs_overlap_kappa_contract"]
        .get("current_blockers", {})
        .get("source_higgs_row_packet_absent")
        is True
        and certs["post_fms_source_overlap_necessity"].get("proposal_allowed") is False
    )
    osp_support_not_oh = (
        "O_sp source-pole artifact" in statuses["genuine_source_pole_intake"]
        and certs["genuine_source_pole_intake"].get("proposal_allowed") is False
    )
    taste_radial_promotion_blocked = (
        certs["taste_radial_promotion_contract"].get(
            "current_promotion_allowed"
        )
        is False
        and certs["taste_radial_promotion_contract"].get("promotion_contract_passed")
        is True
        and certs["taste_radial_promotion_contract"].get("proposal_allowed") is False
    )
    time_kernel_support_not_pole = (
        certs["time_kernel_harness"].get("proposal_allowed") is False
        and certs["time_kernel_harness"].get("used_as_physical_yukawa_readout") is False
        and certs["time_kernel_gevp"].get("physical_pole_extraction_accepted") is False
        and not futures["time_kernel_production_rows"]
    )
    wz_status = statuses["wz_response_ratio_contract"]
    wz_fallback_not_this_bridge = (
        (
            "W/Z response-ratio identifiability contract" in wz_status
            or "WZ response-ratio identifiability contract" in wz_status
        )
        and certs["wz_response_ratio_contract"].get("proposal_allowed") is False
        and certs["wz_response_ratio_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and certs["wz_response_ratio_contract"].get(
            "current_surface_contract_satisfied"
        )
        is False
    )
    aggregate_denies_proposal = (
        certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    firewall_clean = all(value is False for value in FORBIDDEN_FIREWALL.values())
    closure_allowed_now = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("literature-bridge-marked-non-derivation-context", literature_bridge_scope_ok, str(LITERATURE_REFERENCES))
    report("fms-conditional-support-only", fms_conditional_support_only, statuses["fms_conditional_theorem"])
    report("action-form-support-only", action_formula_support_only, statuses["higgs_mass_source_action_bridge"])
    report("same-source-ew-action-adoption-blocked", action_adoption_blocked, statuses["same_source_ew_action_adoption_attempt"])
    report("canonical-oh-certificate-absent", canonical_oh_absent, statuses["canonical_higgs_operator_gate"])
    report("source-higgs-pole-rows-absent", source_higgs_rows_absent, statuses["source_higgs_builder"])
    report("source-overlap-kappa-still-open", source_overlap_still_open, statuses["source_higgs_overlap_kappa_contract"])
    report("osp-support-not-canonical-oh", osp_support_not_oh, statuses["genuine_source_pole_intake"])
    report("taste-radial-promotion-blocked", taste_radial_promotion_blocked, statuses["taste_radial_promotion_contract"])
    report("time-kernel-support-not-pole-authority", time_kernel_support_not_pole, statuses["time_kernel_gevp"])
    report("wz-remains-fallback-not-source-overlap-bridge", wz_fallback_not_this_bridge, statuses["wz_response_ratio_contract"])
    report("aggregate-denies-proposal", aggregate_denies_proposal, "retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", firewall_clean, str(FORBIDDEN_FIREWALL))
    report("closure-not-authorized-now", not closure_allowed_now, "same-surface action/O_H/rows absent")

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact negative boundary / FMS literature does not supply PR230 "
            "source-overlap or kappa_s on the current surface"
        ),
        "conditional_surface_status": (
            "exact-support if a future same-surface EW/Higgs action derives "
            "O_FMS with canonical LSZ and production C_spH/C_HH pole rows "
            "measure the source overlap"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The literature bridge is non-derivation context.  Current PR230 "
            "still lacks accepted EW/Higgs action, canonical O_H, source-Higgs "
            "pole rows, Gram purity, FV/IR/threshold authority, and retained-route approval."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "fms_literature_source_overlap_intake_passed": passed,
        "literature_references": LITERATURE_REFERENCES,
        "literature_bridge_scope": "non_derivation_context_only",
        "acceptance_contract": acceptance_contract(),
        "future_files": {name: rel(ROOT / path) for name, path in FUTURE_FILES.items()},
        "future_file_presence": futures,
        "current_blockers": {
            "same_source_ew_action_absent": action_adoption_blocked,
            "canonical_oh_absent": canonical_oh_absent,
            "source_higgs_rows_absent": source_higgs_rows_absent,
            "source_overlap_still_open": source_overlap_still_open,
            "osp_support_not_oh": osp_support_not_oh,
            "taste_radial_promotion_blocked": taste_radial_promotion_blocked,
            "time_kernel_support_not_pole": time_kernel_support_not_pole,
        },
        "parent_statuses": statuses,
        "forbidden_firewall": FORBIDDEN_FIREWALL,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not use FMS or gauge-invariant-field literature as same-surface proof authority",
            "does not identify O_sp or taste-radial x with canonical O_H",
            "does not set kappa_s, c2, Z_match, or g2 to one",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, reduced pilots, or value recognition",
            "does not treat reduced time-kernel GEVP or smoke rows as pole residue authority",
        ],
        "exact_next_action": (
            "Produce an accepted same-surface EW/Higgs action/O_FMS certificate "
            "or production C_spH/C_HH pole rows measuring O_sp-Higgs overlap; "
            "then rerun source-Higgs Gram purity, scalar-LSZ/FV/IR, assembly, "
            "retained-route, and campaign gates."
        ),
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
