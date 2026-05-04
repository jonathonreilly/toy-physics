#!/usr/bin/env python3
"""
PR #230 full positive closure assembly gate.

This runner answers the practical integration question for the current
campaign: when the chunk work finishes, what else must be true before PR #230
can honestly claim positive retained top-Yukawa closure?

It does not claim closure and it does not consume or package chunk outputs as
evidence.  It checks the non-chunk bridge surface: scalar LSZ/model-class
control plus one canonical-Higgs/source-overlap route.  Chunk evidence alone is
explicitly rejected.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"

PARENTS = {
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "fh_lsz_common_window_response": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "fh_lsz_finite_source_linearity": "outputs/yt_fh_lsz_finite_source_linearity_gate_2026-05-02.json",
    "fh_lsz_response_window_acceptance": "outputs/yt_fh_lsz_response_window_acceptance_gate_2026-05-03.json",
    "fh_lsz_target_ess": "outputs/yt_fh_lsz_target_observable_ess_certificate_2026-05-03.json",
    "fh_lsz_autocorrelation_ess": "outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json",
    "fh_lsz_polefit8x8_combiner": "outputs/yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json",
    "fh_lsz_polefit8x8_postprocessor": "outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json",
    "fh_lsz_model_class": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "fh_lsz_model_class_semantic_firewall": "outputs/yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json",
    "fh_lsz_pole_saturation": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "fh_lsz_finite_volume": "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json",
    "fh_lsz_soft_continuum": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_postprocess": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "wz_same_source_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_certificate_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "wz_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "canonical_higgs_operator": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "canonical_higgs_semantic_firewall": "outputs/yt_canonical_higgs_operator_semantic_firewall_2026-05-04.json",
    "source_pole_mixing": "outputs/yt_source_pole_canonical_higgs_mixing_obstruction_2026-05-02.json",
    "source_pole_purity": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
    "neutral_scalar_irreducibility": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
    "schur_kprime_rows": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
    "schur_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
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


def truth(cert: dict[str, Any], key: str) -> bool:
    return cert.get(key) is True


def closure_conditions() -> list[dict[str, Any]]:
    return [
        {
            "id": "production_physical_response",
            "required": (
                "strict direct correlator evidence or joint FH/LSZ same-source "
                "production evidence with homogeneous run-control, target ESS, "
                "finite-source derivative control, and no chunk/provenance collisions"
            ),
            "why_needed": "Supplies the physical response data; pilots and partial chunks are not y_t evidence.",
            "current_surface": "bounded production support only",
        },
        {
            "id": "scalar_lsz_model_class_fv_ir",
            "required": (
                "isolated scalar-pole derivative/residue with model-class or "
                "analytic-continuation authority plus FV/IR/zero-mode/threshold control"
            ),
            "why_needed": "Converts finite-shell same-source C_ss rows into a pole LSZ normalization.",
            "current_surface": "finite-shell/postprocessor gates remain support-only or exact negative boundaries",
        },
        {
            "id": "source_overlap_or_physical_response_bridge",
            "required": (
                "one accepted bridge among O_sp/O_H Gram purity with C_sH/C_HH "
                "rows, same-source W/Z response with sector-overlap identity, "
                "same-surface Schur/K-prime rows plus canonical bridge, or a "
                "neutral-scalar rank-one/irreducibility theorem"
            ),
            "why_needed": "Identifies the source-pole readout with physical canonical-Higgs y_t.",
            "current_surface": "all current bridge routes are absent, blocked, or conditional support",
        },
        {
            "id": "matching_running_bridge",
            "required": (
                "explicit lattice-to-physical matching and SM running bridge whose "
                "inputs are measured/certified, not observed-target selectors"
            ),
            "why_needed": "Turns the lattice-scale readout into the PR230 y_t(v)/m_t comparison.",
            "current_surface": "not authorized until production, LSZ, and overlap gates pass",
        },
        {
            "id": "retained_proposal_firewall",
            "required": (
                "retained-route and campaign status certificates allow proposed_retained, "
                "with no forbidden imports or open load-bearing assumptions"
            ),
            "why_needed": "Prevents local support artifacts from becoming branch-local retained claims.",
            "current_surface": "proposal_allowed is false",
        },
    ]


def route_statuses(certs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        "source_higgs_gram_purity": {
            "passes_current_surface": truth(certs["source_higgs_gram"], "source_higgs_gram_purity_gate_passed")
            or truth(certs["source_higgs_postprocess"], "osp_higgs_gram_purity_gate_passed"),
            "blocked_by": [
                "same-surface O_H certificate absent",
                "production C_sH/C_HH pole residues absent",
                "Gram-purity postprocessor awaiting production certificate",
            ],
            "parents": [
                PARENTS["source_higgs_readiness"],
                PARENTS["source_higgs_gram"],
                PARENTS["source_higgs_postprocess"],
                PARENTS["canonical_higgs_semantic_firewall"],
            ],
        },
        "same_source_wz_response": {
            "passes_current_surface": truth(certs["wz_same_source_action"], "same_source_ew_action_ready")
            and truth(certs["wz_certificate_gate"], "same_source_wz_response_certificate_gate_passed"),
            "blocked_by": [
                "same-source EW action certificate absent",
                "W/Z correlator mass-fit path absent",
                "sector-overlap identity not derived",
                "canonical-Higgs identity not derived",
            ],
            "parents": [
                PARENTS["wz_same_source_action"],
                PARENTS["wz_certificate_gate"],
                PARENTS["wz_mass_fit_path"],
                PARENTS["same_source_sector_overlap"],
            ],
        },
        "schur_kprime_kernel_rows": {
            "passes_current_surface": truth(certs["schur_kprime_rows"], "schur_kprime_row_gate_passed"),
            "blocked_by": [
                "same-surface Schur A/B/C rows absent",
                "finite FH/LSZ source rows explicitly rejected as kernel rows",
                "canonical bridge still required after K-prime sufficiency",
            ],
            "parents": [
                PARENTS["schur_kprime_rows"],
                PARENTS["schur_kprime_sufficiency"],
            ],
        },
        "neutral_scalar_rank_one": {
            "passes_current_surface": truth(certs["neutral_scalar_irreducibility"], "neutral_scalar_irreducibility_authority_present"),
            "blocked_by": [
                "no current primitive-cone/positivity-improving neutral-sector certificate",
                "rank-two neutral scalar counterfamilies remain allowed",
            ],
            "parents": [PARENTS["neutral_scalar_irreducibility"]],
        },
    }


def evaluate(state: dict[str, bool]) -> dict[str, Any]:
    required = [
        "production_physical_response",
        "scalar_lsz_model_class_fv_ir",
        "source_overlap_or_physical_response_bridge",
        "matching_running_bridge",
        "retained_proposal_firewall",
        "forbidden_import_firewall",
    ]
    missing = [name for name in required if not state.get(name, False)]
    return {
        "assembly_passed": not missing,
        "missing": missing,
        "proposal_allowed": not missing,
    }


def main() -> int:
    print("PR #230 full positive closure assembly gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: status(cert) for name, cert in certs.items()}
    routes = route_statuses(certs)
    any_bridge_passes = any(row["passes_current_surface"] for row in routes.values())

    response_side_support = (
        certs["fh_lsz_common_window_response"].get("common_window_response_gate_passed") is True
        or "support" in statuses["fh_lsz_common_window_response"]
    )
    finite_source_support = (
        certs["fh_lsz_finite_source_linearity"].get("finite_source_linearity_gate_passed") is True
        or "support" in statuses["fh_lsz_finite_source_linearity"]
    )
    ess_support = (
        certs["fh_lsz_target_ess"].get("target_observable_ess_gate_passed") is True
        or "ESS" in statuses["fh_lsz_target_ess"]
    )
    polefit_support_only = (
        certs["fh_lsz_polefit8x8_combiner"].get("proposal_allowed") is False
        and certs["fh_lsz_polefit8x8_postprocessor"].get("proposal_allowed") is False
        and "eight-mode" in statuses["fh_lsz_polefit8x8_postprocessor"]
    )
    scalar_lsz_blocks = (
        certs["fh_lsz_model_class"].get("proposal_allowed") is False
        and certs["fh_lsz_model_class_semantic_firewall"].get("proposal_allowed") is False
        and certs["fh_lsz_pole_saturation"].get("proposal_allowed") is False
        and certs["fh_lsz_finite_volume"].get("proposal_allowed") is False
        and certs["fh_lsz_soft_continuum"].get("proposal_allowed") is False
    )
    source_overlap_blocks = (
        any_bridge_passes is False
        and certs["canonical_higgs_semantic_firewall"].get("proposal_allowed") is False
        and certs["source_pole_mixing"].get("proposal_allowed") is False
        and certs["source_pole_purity"].get("proposal_allowed") is False
        and certs["canonical_higgs_operator"].get("proposal_allowed") is False
    )
    retained_route_open = (
        "retained closure not yet reached" in statuses["retained_route"]
        and certs["retained_route"].get("proposal_allowed") is False
    )
    campaign_open = (
        "active campaign" in statuses["campaign_status"]
        and certs["campaign_status"].get("proposal_allowed") is False
    )

    current_state = {
        "production_physical_response": False,
        "scalar_lsz_model_class_fv_ir": False,
        "source_overlap_or_physical_response_bridge": any_bridge_passes,
        "matching_running_bridge": False,
        "retained_proposal_firewall": False,
        "forbidden_import_firewall": True,
    }
    current_eval = evaluate(current_state)
    chunk_only_state = {
        **current_state,
        "production_physical_response": True,
    }
    chunk_only_eval = evaluate(chunk_only_state)
    synthetic_positive_state = {
        "production_physical_response": True,
        "scalar_lsz_model_class_fv_ir": True,
        "source_overlap_or_physical_response_bridge": True,
        "matching_running_bridge": True,
        "retained_proposal_firewall": True,
        "forbidden_import_firewall": True,
    }
    synthetic_eval = evaluate(synthetic_positive_state)

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("response-side-support-present", response_side_support, statuses["fh_lsz_common_window_response"])
    report("finite-source-support-present", finite_source_support, statuses["fh_lsz_finite_source_linearity"])
    report("target-ess-support-present", ess_support, statuses["fh_lsz_target_ess"])
    report("polefit8x8-support-only", polefit_support_only, statuses["fh_lsz_polefit8x8_postprocessor"])
    report(
        "canonical-higgs-semantic-firewall-support-only",
        "semantic firewall passed" in statuses["canonical_higgs_semantic_firewall"]
        and certs["canonical_higgs_semantic_firewall"].get("proposal_allowed") is False,
        statuses["canonical_higgs_semantic_firewall"],
    )
    report(
        "model-class-semantic-firewall-support-only",
        "model-class semantic firewall passed" in statuses["fh_lsz_model_class_semantic_firewall"]
        and certs["fh_lsz_model_class_semantic_firewall"].get("proposal_allowed") is False,
        statuses["fh_lsz_model_class_semantic_firewall"],
    )
    report("scalar-lsz-model-fv-ir-blocked", scalar_lsz_blocks, "model-class/FV/IR/threshold controls still block retained use")
    report("source-overlap-bridge-absent", source_overlap_blocks, f"route_passes={any_bridge_passes}")
    report("retained-route-still-open", retained_route_open, statuses["retained_route"])
    report("campaign-status-still-open", campaign_open, statuses["campaign_status"])
    report("current-surface-assembly-rejected", not current_eval["assembly_passed"], f"missing={current_eval['missing']}")
    report("chunk-only-assembly-rejected", not chunk_only_eval["assembly_passed"], f"missing={chunk_only_eval['missing']}")
    report("synthetic-positive-witness-passes-schema", synthetic_eval["assembly_passed"], f"missing={synthetic_eval['missing']}")

    result = {
        "actual_current_surface_status": "open / full positive PR230 closure assembly gate not passed",
        "verdict": (
            "The non-chunk closure assembly is now explicit.  Chunk completion "
            "can supply only the production-response leg; it cannot by itself "
            "supply scalar LSZ model-class/FV/IR control, the O_sp-to-O_H or "
            "same-source physical-response bridge, matching/running authority, "
            "or retained-proposal authorization.  On the current PR230 surface "
            "all allowed bridge routes are absent, blocked, or support-only, so "
            "full positive closure remains open."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The assembly gate rejects the current surface and also rejects a "
            "hypothetical chunk-only completion.  A positive proposal first "
            "needs scalar-LSZ pole/FV/IR/model-class closure plus one accepted "
            "source-overlap/physical-response bridge and retained-route approval."
        ),
        "bare_retained_allowed": False,
        "closure_conditions": closure_conditions(),
        "route_statuses": routes,
        "current_state": current_state,
        "current_evaluation": current_eval,
        "chunk_only_state": chunk_only_state,
        "chunk_only_evaluation": chunk_only_eval,
        "synthetic_positive_witness": {
            "state": synthetic_positive_state,
            "evaluation": synthetic_eval,
            "purpose": "schema sanity check only; not evidence and not a PR230 claim",
        },
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not package or certify chunk outputs",
            "does not define y_t through a matrix element or y_t_bare",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, observed targets, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not treat static EW algebra, W/Z absent guards, source-only C_ss rows, or finite-shell fits as physical y_t readouts",
        ],
        "exact_next_action": (
            "Keep the chunk worker on homogeneous production chunks.  In parallel, "
            "pursue one non-chunk bridge that can satisfy this gate: a real "
            "same-surface O_H certificate plus C_sH/C_HH pole rows, a same-source "
            "EW action plus W/Z mass-response rows and sector-overlap identity, "
            "same-surface Schur A/B/C kernel rows with scalar denominator closure, "
            "or a neutral-sector irreducibility theorem.  Rerun this assembly "
            "gate before any retained-route proposal."
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
