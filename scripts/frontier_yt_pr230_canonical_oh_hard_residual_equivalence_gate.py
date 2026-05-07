#!/usr/bin/env python3
"""
PR #230 canonical O_H hard-residual equivalence gate.

The parallel hard-residual probes all converge on the same target.  The current
surface does not prove O_sp = O_H, but the missing bridge is now mathematically
sharp: either a same-surface certified O_H plus source-Higgs pole rows gives a
flat/Gram-pure extension, or a neutral scalar primitive-cone theorem forces
rank one, or a physical-response row packet removes the same overlap by W/Z
sector authority.

This runner records that equivalence as an exact negative boundary on the
current surface.  It does not close PR230 and does not authorize retained or
proposed_retained wording.
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
    / "yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json"
)

PARENTS = {
    "source_higgs_direct_pole_row_contract": "outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json",
    "osp_oh_identity_stretch": "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_gram_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "positivity_improving_rank_one_support": "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json",
    "primitive_cone_certificate_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "irreducibility_authority_audit": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
    "wz_response_ratio_contract": "outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json",
    "same_source_sector_overlap_obstruction": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "negative_route_applicability_review": "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_ARTIFACTS = {
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_measurement_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
    "source_higgs_production_certificate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "neutral_scalar_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "same_source_ew_action_certificate": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "wz_response_ratio_rows": "outputs/yt_pr230_wz_response_ratio_rows_2026-05-07.json",
    "electroweak_g2_certificate": "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
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


def psd_2x2(a: float, b: float) -> bool:
    return b >= -1.0e-12 and b - a * a >= -1.0e-12


def flat_extension_witness() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for a, b in ((0.40, 0.16), (0.40, 0.45), (-0.75, 0.5625), (-0.75, 0.90)):
        determinant = b - a * a
        rows.append(
            {
                "Res_C_sp_sp": 1.0,
                "Res_C_spH": a,
                "Res_C_HH": b,
                "psd": psd_2x2(a, b),
                "flat_extension": abs(determinant) <= 1.0e-12,
                "Delta_spH": determinant,
                "abs_rho_spH": abs(a) / math.sqrt(b) if b > 0.0 else float("nan"),
            }
        )
    return {
        "statement": (
            "With normalized O_sp, positivity gives b >= |a|^2 for "
            "M=[[1,a],[a,b]]. The O_sp=O_H bridge requires the flat equality "
            "b=|a|^2, equivalently Delta_spH=0 and |rho_spH|=1."
        ),
        "rows": rows,
    }


def closure_disjunction() -> list[dict[str, Any]]:
    return [
        {
            "id": "source_higgs_gram_purity",
            "required_future_artifacts": [
                "canonical_higgs_operator_certificate",
                "source_higgs_measurement_rows",
                "source_higgs_production_certificate",
            ],
            "mathematical_condition": "Delta_spH=0 and |rho_spH|=1 at the same nondegenerate isolated pole",
            "status_now": "absent",
        },
        {
            "id": "neutral_scalar_primitive_cone",
            "required_future_artifacts": [
                "neutral_scalar_primitive_cone_certificate",
                "canonical_higgs_operator_certificate or theorem bypassing explicit O_H rows",
            ],
            "mathematical_condition": "positivity-improving neutral transfer sector with unique lowest isolated scalar pole",
            "status_now": "premise absent",
        },
        {
            "id": "same_source_wz_physical_response",
            "required_future_artifacts": [
                "same_source_ew_action_certificate",
                "wz_response_ratio_rows",
                "electroweak_g2_certificate",
            ],
            "mathematical_condition": "sector-overlap and orthogonal-neutral correction controlled, with matched covariance",
            "status_now": "action/rows/g2 absent",
        },
    ]


def forbidden_firewall() -> dict[str, bool]:
    return {
        "used_hunit_matrix_element_readout": False,
        "used_hunit_as_operator": False,
        "used_yt_ward_identity": False,
        "used_observed_top_or_yukawa_targets": False,
        "used_observed_wz_or_g2_targets": False,
        "used_alpha_lm_plaquette_or_u0": False,
        "set_kappa_s_equal_one": False,
        "set_cos_theta_equal_one": False,
        "treated_psd_as_flat_extension": False,
        "treated_reflection_positivity_as_primitive_cone": False,
        "treated_c_sx_c_xx_as_c_sh_c_hh": False,
        "claimed_retained_or_proposed_retained": False,
        "touched_live_chunk_worker": False,
    }


def main() -> int:
    print("PR #230 canonical O_H hard-residual equivalence gate")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parents.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    futures = future_presence()
    witness = flat_extension_witness()
    firewall = forbidden_firewall()

    direct_contract_loaded = (
        parents["source_higgs_direct_pole_row_contract"].get(
            "source_higgs_direct_pole_row_contract_passed"
        )
        is True
        and parents["source_higgs_direct_pole_row_contract"].get("proposal_allowed")
        is False
    )
    source_only_identity_blocked = (
        "not derived" in statuses["osp_oh_identity_stretch"]
        and parents["osp_oh_identity_stretch"].get("proposal_allowed") is False
    )
    source_lsz_identifies_not_derives = (
        "source-functional LSZ identifiability" in statuses["source_functional_lsz_identifiability"]
        and parents["source_functional_lsz_identifiability"].get("proposal_allowed")
        is False
    )
    canonical_oh_absent = (
        parents["canonical_higgs_operator_gate"].get("candidate_present") is False
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
        and not futures["canonical_higgs_operator_certificate"]
    )
    source_higgs_rows_absent = (
        parents["source_higgs_gram_postprocessor"].get("candidate_present") is False
        and parents["source_higgs_gram_postprocessor"].get(
            "source_higgs_gram_purity_gate_passed"
        )
        is False
        and not futures["source_higgs_measurement_rows"]
        and not futures["source_higgs_production_certificate"]
    )
    primitive_theorem_conditional_only = (
        parents["positivity_improving_rank_one_support"].get(
            "positivity_improving_rank_one_theorem_passed"
        )
        is True
        and parents["positivity_improving_rank_one_support"].get(
            "positivity_improving_certificate_present"
        )
        is False
    )
    primitive_certificate_absent = (
        parents["primitive_cone_certificate_gate"].get(
            "primitive_cone_certificate_gate_passed"
        )
        is False
        and not futures["neutral_scalar_primitive_cone_certificate"]
    )
    irreducibility_authority_absent = (
        parents["irreducibility_authority_audit"].get(
            "neutral_scalar_irreducibility_certificate_present"
        )
        is False
    )
    wz_route_infrastructure_only = (
        parents["wz_response_ratio_contract"].get(
            "wz_response_ratio_identifiability_contract_passed"
        )
        is True
        and parents["wz_response_ratio_contract"].get("current_surface_contract_satisfied")
        is False
        and not futures["same_source_ew_action_certificate"]
        and not futures["wz_response_ratio_rows"]
    )
    sector_overlap_blocked = (
        parents["same_source_sector_overlap_obstruction"].get(
            "sector_overlap_identity_gate_passed"
        )
        is False
    )
    same_source_ew_action_absent = (
        parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready")
        is False
    )
    negative_review_preserves_reopen = (
        "negative-route applicability review passed"
        in statuses["negative_route_applicability_review"]
        and parents["negative_route_applicability_review"].get(
            "negative_results_are_current_surface_blockers_only"
        )
        is True
        and parents["negative_route_applicability_review"].get(
            "future_reopen_paths_preserved"
        )
        is True
        and parents["negative_route_applicability_review"].get("proposal_allowed")
        is not True
    )
    aggregate_rejects_proposal = (
        parents["full_positive_assembly"].get("proposal_allowed") is False
        and parents["retained_route"].get("proposal_allowed") is False
        and parents["campaign_status"].get("proposal_allowed") is False
    )
    flat_rows_ok = all(row["psd"] for row in witness["rows"])
    psd_not_enough = any(row["psd"] and not row["flat_extension"] for row in witness["rows"])
    flat_rows_close_math = all(
        (not row["flat_extension"]) or abs(row["abs_rho_spH"] - 1.0) <= 1.0e-12
        for row in witness["rows"]
    )
    disjunction_satisfied = any(futures[name] for name in FUTURE_ARTIFACTS)

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_parents, f"proposal_allowed={proposal_parents}")
    report("source-Higgs-direct-contract-loaded", direct_contract_loaded, statuses["source_higgs_direct_pole_row_contract"])
    report("source-only-Osp-OH-identity-blocked", source_only_identity_blocked, statuses["osp_oh_identity_stretch"])
    report("source-LSZ-identifies-not-derives-overlap", source_lsz_identifies_not_derives, statuses["source_functional_lsz_identifiability"])
    report("canonical-OH-certificate-absent", canonical_oh_absent, FUTURE_ARTIFACTS["canonical_higgs_operator_certificate"])
    report("source-Higgs-pole-rows-absent", source_higgs_rows_absent, FUTURE_ARTIFACTS["source_higgs_measurement_rows"])
    report("primitive-rank-one-theorem-conditional-only", primitive_theorem_conditional_only, statuses["positivity_improving_rank_one_support"])
    report("primitive-cone-certificate-absent", primitive_certificate_absent, FUTURE_ARTIFACTS["neutral_scalar_primitive_cone_certificate"])
    report("irreducibility-authority-absent", irreducibility_authority_absent, statuses["irreducibility_authority_audit"])
    report("WZ-route-infrastructure-only", wz_route_infrastructure_only, statuses["wz_response_ratio_contract"])
    report("WZ-sector-overlap-blocked", sector_overlap_blocked, statuses["same_source_sector_overlap_obstruction"])
    report("same-source-EW-action-absent", same_source_ew_action_absent, statuses["wz_same_source_ew_action_gate"])
    report("PSD-extension-witness-valid", flat_rows_ok, "b >= |a|^2 rows")
    report("PSD-alone-not-flat-extension", psd_not_enough, "strict b>|a|^2 rows exist")
    report("flat-extension-equals-Gram-purity", flat_rows_close_math, "flat rows have |rho_spH|=1")
    report("negative-route-review-preserves-reopen", negative_review_preserves_reopen, statuses["negative_route_applicability_review"])
    report("aggregate-gates-deny-proposal", aggregate_rejects_proposal, "proposal_allowed=false")
    report("future-disjunction-not-satisfied", not disjunction_satisfied, f"future_presence={futures}")
    report("forbidden-firewall-clean", not any(firewall.values()), str(firewall))
    report("does-not-authorize-proposed-retained", True, "proposal_allowed=false")

    passed = FAIL_COUNT == 0
    result = {
        "actual_current_surface_status": (
            "exact negative boundary / canonical O_H hard residual not closed on current PR230 surface"
        ),
        "conditional_surface_status": (
            "exact-support equivalence: O_sp/O_H closure may proceed only through "
            "source-Higgs Gram flatness with certified O_H rows, neutral scalar "
            "primitive-cone rank-one authority, or W/Z physical-response rows "
            "with sector-overlap/covariance/strict-g2 authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The gate sharpens the hard residual but supplies none of the "
            "future disjunctive artifacts.  Current PR230 still lacks canonical "
            "O_H, source-Higgs pole rows, primitive-cone authority, and W/Z "
            "physical-response authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "canonical_oh_hard_residual_equivalence_gate_passed": passed,
        "current_surface_closure_satisfied": False,
        "future_artifact_presence": futures,
        "closure_disjunction": closure_disjunction(),
        "flat_extension_witness": witness,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "forbidden_firewall": firewall,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not construct O_H or identify O_sp with O_H",
            "does not set kappa_s=1, cos(theta)=1, or a flat extension by convention",
            "does not treat positivity/PSD/reflection positivity as primitive-cone irreducibility",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
            "does not treat C_sx/C_xx aliases as C_sH/C_HH pole rows",
            "does not touch the live chunk worker",
        ],
        "exact_next_action": (
            "Stop cycling source-only or representation-theory shortcuts.  The "
            "next positive science artifact must be one of: a certified O_H "
            "with production C_sH/C_HH pole rows, a same-surface neutral scalar "
            "primitive-cone theorem, or a W/Z response row packet with accepted "
            "action, sector-overlap, covariance, and strict g2."
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
