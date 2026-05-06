#!/usr/bin/env python3
"""
PR #230 O_H / C_sH / C_HH first-principles candidate portfolio.

This runner does not try to close the top-Yukawa bridge.  It packages the
current physics-loop attack surface after the taste-condensate shortcut was
blocked: which routes remain genuinely candidate-positive, what each route
must still supply, and which exact negative boundaries are only shortcut
blockers rather than global route closures.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json"

CERTS = {
    "taste_condensate_oh_bridge": "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json",
    "canonical_higgs_repo_authority": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
    "canonical_higgs_certificate_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_higgs_production_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_cross_correlator_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_gram_purity_contract": "outputs/yt_source_higgs_gram_purity_contract_witness_2026-05-03.json",
    "fh_gauge_normalized_response": "outputs/yt_fh_gauge_normalized_response_route_2026-05-02.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "electroweak_g2_certificate_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_response_self_normalization_no_go": "outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json",
    "schur_kprime_sufficiency": "outputs/yt_schur_complement_kprime_sufficiency_2026-05-03.json",
    "schur_abc_definition_attempt": "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json",
    "neutral_primitive_cone_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "neutral_primitive_cone_stretch_no_go": "outputs/yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json",
    "positivity_improving_rank_one_support": "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json",
    "negative_route_applicability_review": "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json",
    "source_coordinate_transport_completion": "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json",
    "action_first_route_completion": "outputs/yt_pr230_action_first_route_completion_2026-05-06.json",
    "wz_response_route_completion": "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json",
    "schur_route_completion": "outputs/yt_pr230_schur_route_completion_2026-05-06.json",
    "neutral_primitive_route_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
    "assumption_import_stress": "outputs/yt_pr230_assumption_import_stress_2026-05-01.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def present(name: str, certs: dict[str, dict[str, Any]]) -> bool:
    return bool(certs.get(name))


def candidate(
    *,
    route_id: str,
    rank: int,
    title: str,
    route_class: str,
    first_principles_anchor: str,
    why_candidate_positive: list[str],
    exact_current_blockers: list[str],
    next_artifacts: list[str],
    current_boundaries: list[str],
    blocked_shortcuts_not_global_closure: list[str],
) -> dict[str, Any]:
    return {
        "route_id": route_id,
        "rank": rank,
        "title": title,
        "candidate_status": "positive_candidate_open",
        "route_class": route_class,
        "first_principles_anchor": first_principles_anchor,
        "why_candidate_positive": why_candidate_positive,
        "exact_current_blockers": exact_current_blockers,
        "next_artifacts": next_artifacts,
        "current_boundaries": current_boundaries,
        "blocked_shortcuts_not_global_closure": blocked_shortcuts_not_global_closure,
        "blocks_first_principles_derivation": False,
        "same_surface_required": True,
        "reopen_artifact_keys": next_artifacts,
    }


def main() -> int:
    print("PR #230 O_H / C_sH / C_HH first-principles candidate portfolio")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in CERTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    taste_blocks_shortcut = (
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in status(certs["taste_condensate_oh_bridge"])
        and certs["taste_condensate_oh_bridge"].get("proposal_allowed") is False
    )
    repo_oh_absent = (
        "repo-wide canonical-Higgs O_H authority audit" in status(certs["canonical_higgs_repo_authority"])
        and certs["canonical_higgs_repo_authority"].get("repo_authority_found") is False
    )
    source_higgs_launch_blocked = (
        "source-Higgs production launch blocked" in status(certs["source_higgs_production_readiness"])
        and certs["source_higgs_production_readiness"].get("proposal_allowed") is False
    )
    wz_ratio_support = (
        "FH gauge-normalized response route" in status(certs["fh_gauge_normalized_response"])
        and certs["fh_gauge_normalized_response"].get("gauge_normalized_response_gate_passed") is False
    )
    wz_inputs_absent = (
        "WZ mass-fit response-row builder inputs absent" in status(certs["wz_mass_fit_response_row_builder"])
        and certs["wz_mass_fit_response_row_builder"].get("strict_wz_mass_fit_response_row_builder_passed") is False
    )
    g2_absent = (
        "electroweak g2 certificate builder inputs absent"
        in status(certs["electroweak_g2_certificate_builder"])
        and certs["electroweak_g2_certificate_builder"].get("strict_electroweak_g2_certificate_passed") is False
    )
    schur_support = (
        "Schur-complement K-prime sufficiency theorem" in status(certs["schur_kprime_sufficiency"])
        and certs["schur_kprime_sufficiency"].get("schur_sufficiency_theorem_passed") is True
    )
    schur_rows_absent = (
        "Schur A/B/C definition not derivable" in status(certs["schur_abc_definition_attempt"])
        and certs["schur_abc_definition_attempt"].get("proposal_allowed") is False
    )
    neutral_contract = (
        "neutral-scalar primitive-cone certificate gate" in status(certs["neutral_primitive_cone_gate"])
        and certs["neutral_primitive_cone_gate"].get("primitive_cone_certificate_gate_passed") is False
    )
    rank_one_support = (
        "positivity-improving neutral-scalar rank-one theorem"
        in status(certs["positivity_improving_rank_one_support"])
        and certs["positivity_improving_rank_one_support"].get(
            "positivity_improving_rank_one_theorem_passed"
        )
        is True
    )
    negative_boundaries_scoped = (
        present("negative_route_applicability_review", certs)
        and certs["negative_route_applicability_review"].get("proposal_allowed") is False
    )
    source_transport_current_surface_closed = (
        "source-coordinate transport not derivable from current PR230 surface"
        in status(certs["source_coordinate_transport_completion"])
        and certs["source_coordinate_transport_completion"].get("proposal_allowed") is False
        and certs["source_coordinate_transport_completion"].get(
            "source_coordinate_transport_completion_passed"
        )
        is True
        and certs["source_coordinate_transport_completion"].get("algebra", {}).get(
            "source_relative_projection_onto_taste_axis_span"
        )
        == 0.0
    )
    action_first_current_surface_closed = (
        "action-first O_H/C_sH/C_HH route not complete on current PR230 surface"
        in status(certs["action_first_route_completion"])
        and certs["action_first_route_completion"].get("proposal_allowed") is False
        and certs["action_first_route_completion"].get(
            "action_first_route_completion_passed"
        )
        is True
    )
    wz_response_current_surface_closed = (
        "WZ same-source response route not complete on current PR230 surface"
        in status(certs["wz_response_route_completion"])
        and certs["wz_response_route_completion"].get("proposal_allowed") is False
        and certs["wz_response_route_completion"].get(
            "wz_response_route_completion_passed"
        )
        is True
    )
    schur_current_surface_closed = (
        "Schur A/B/C route not complete on current PR230 surface"
        in status(certs["schur_route_completion"])
        and certs["schur_route_completion"].get("proposal_allowed") is False
        and certs["schur_route_completion"].get("schur_route_completion_passed")
        is True
    )
    neutral_current_surface_closed = (
        "neutral primitive-rank-one route not complete on current PR230 surface"
        in status(certs["neutral_primitive_route_completion"])
        and certs["neutral_primitive_route_completion"].get("proposal_allowed") is False
        and certs["neutral_primitive_route_completion"].get(
            "neutral_primitive_route_completion_passed"
        )
        is True
    )
    assembly_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )

    routes = [
        candidate(
            route_id="A_source_coordinate_transport",
            rank=1,
            title="derive source-coordinate transport from uniform mass source to Higgs/taste source",
            route_class="derivation-first",
            first_principles_anchor="Cl(3)/Z^3 staggered source algebra and taste-shift operator representation",
            why_candidate_positive=[
                "the blocker is exact and low-dimensional: I_8 is orthogonal to the trace-zero taste axes",
                "a successful theorem would directly supply the missing source-to-Higgs coordinate map",
                "it avoids observed targets, H_unit, and old Ward matrix-element authority",
            ],
            exact_current_blockers=[
                "no theorem transports the uniform additive mass source into the taste-axis Higgs source",
                "taste isotropy gives scalar/taste support but not the PR230 source coordinate",
                "unit-preserving, trace-preserving, and taste-equivariant maps cannot send I_8 to trace-zero S_i on the current surface",
            ],
            next_artifacts=[
                "source-coordinate transport theorem with explicit linear/nonlinear map",
                "runner checking trace, norm, Jacobian, LSZ normalization, and forbidden-import firewall",
                "if transport is nonlinear, a proof that the pole residue uses the transported radial tangent",
            ],
            current_boundaries=[
                "taste_condensate_oh_bridge",
                "source_coordinate_transport_completion",
            ],
            blocked_shortcuts_not_global_closure=[
                "existing Higgs/taste theorem names alone",
                "setting the uniform-source projection onto taste axes to one",
            ],
        ),
        candidate(
            route_id="B_action_first_canonical_OH_rows",
            rank=2,
            title="construct canonical O_H on the same PR230 source surface and measure C_sH/C_HH",
            route_class="action-plus-measurement",
            first_principles_anchor="same-surface Cl(3)/Z^3 EW/Higgs action, FMS radial operator, and FH/LSZ source functional",
            why_candidate_positive=[
                "the source-Higgs harness and Gram-purity acceptance contracts already exist",
                "C_sH/C_HH rows directly measure the missing overlap instead of defining it",
                "this is the cleanest observable bridge if a canonical O_H certificate can be supplied",
            ],
            exact_current_blockers=[
                "canonical O_H identity/normalization certificate is absent",
                "source-Higgs production rows are guarded off in current chunks",
                "finite rows still need isolated-pole residue, FV/IR, and contact control",
                "same-source EW/Higgs action and Gram-purity certificates are absent on the current PR230 surface",
            ],
            next_artifacts=[
                "canonical O_H certificate with same_surface_cl3_z3=true and LSZ normalization",
                "production source-Higgs rows: C_ss, C_sH, C_HH on the same ensembles",
                "Gram-purity postprocessor proving |rho_sH|=1 at the isolated pole",
            ],
            current_boundaries=[
                "canonical_higgs_repo_authority",
                "source_higgs_production_readiness",
                "action_first_route_completion",
            ],
            blocked_shortcuts_not_global_closure=[
                "unratified source-Higgs smoke operator",
                "semantic O_H labels without source coordinate and normalization",
            ],
        ),
        candidate(
            route_id="C_wz_same_source_response_with_strict_g2",
            rank=3,
            title="bypass O_H with matched top/W/Z same-source response and strict non-observed g2",
            route_class="physical-response",
            first_principles_anchor="Feynman-Hellmann slopes under one source coordinate plus EW gauge-mass response",
            why_candidate_positive=[
                "the ratio dE_top/ds divided by dM_W/ds cancels the unknown scalar source scale",
                "the route is a physical observable route, not an operator-renaming route",
                "it avoids canonical O_H if strict W/Z rows and g2 authority are supplied",
            ],
            exact_current_blockers=[
                "W/Z correlator mass-fit rows are absent",
                "same-source top response certificate required by the W/Z builder is absent",
                "strict non-observed g2 certificate is absent",
                "response-only self-normalization cannot determine absolute g2",
                "matched top/W covariance and delta_perp/orthogonal control are absent",
            ],
            next_artifacts=[
                "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
                "outputs/yt_same_source_top_response_certificate_2026-05-04.json",
                "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
                "rerun W/Z row builder and same-source W/Z certificate gate",
            ],
            current_boundaries=[
                "fh_gauge_normalized_response",
                "wz_mass_fit_response_row_builder",
                "electroweak_g2_certificate_builder",
                "wz_g2_response_self_normalization_no_go",
                "wz_response_route_completion",
            ],
            blocked_shortcuts_not_global_closure=[
                "using observed g2 or package g2",
                "using W/Z response ratios alone as absolute y_t",
            ],
        ),
        candidate(
            route_id="D_schur_abc_neutral_kernel_rows",
            rank=4,
            title="derive same-surface Schur A/B/C rows for the neutral scalar kernel",
            route_class="representation/kernel",
            first_principles_anchor="neutral scalar kernel partition K=[[A,B^T],[B,C]] and Schur complement pole derivative",
            why_candidate_positive=[
                "the Schur K-prime sufficiency theorem is already exact support",
                "A/B/C rows would compute the source-pole normalization without guessing overlap",
                "this route can be theorem-first or row-production-first",
            ],
            exact_current_blockers=[
                "compressed source denominator does not determine A/B/C rows",
                "neutral scalar kernel basis and source/orthogonal projector are absent",
                "pole-derivative and FV/IR/contact authority are still needed",
                "same-surface Schur A/B/C row artifacts are absent",
            ],
            next_artifacts=[
                "same-surface neutral scalar kernel basis certificate",
                "A(pole), B(pole), C(pole), and derivative rows",
                "Schur row certificate with pole isolation and forbidden-import firewall",
            ],
            current_boundaries=[
                "schur_kprime_sufficiency",
                "schur_abc_definition_attempt",
                "schur_route_completion",
            ],
            blocked_shortcuts_not_global_closure=[
                "inferring block rows from the compressed denominator",
                "finite ladder scout rows without the neutral partition",
            ],
        ),
        candidate(
            route_id="E_neutral_primitive_rank_one",
            rank=5,
            title="prove neutral primitive/rank-one transfer so source pole and Higgs pole coincide",
            route_class="operator-theorem",
            first_principles_anchor="Perron-Frobenius/Krein-Rutman uniqueness for same-surface neutral scalar transfer",
            why_candidate_positive=[
                "a positivity-improving theorem would remove the orthogonal neutral ambiguity at the pole",
                "the primitive-cone gate already defines an executable acceptance contract",
                "this is the most derivation-native route if the neutral transfer operator can be constructed",
            ],
            exact_current_blockers=[
                "same-surface neutral transfer matrix/operator is not certified",
                "current source-only data admit reducible completions",
                "off-diagonal neutral generator and primitive positive power are absent",
                "strict neutral primitive-cone/rank-one certificate is absent",
            ],
            next_artifacts=[
                "neutral scalar basis and transfer matrix/operator certificate",
                "strong-connectivity and finite positive-power checks",
                "isolated lowest neutral pole plus positive source and canonical-Higgs overlaps",
                "orthogonal-neutral null certificate and firewall",
            ],
            current_boundaries=[
                "neutral_primitive_cone_gate",
                "neutral_primitive_cone_stretch_no_go",
                "positivity_improving_rank_one_support",
                "neutral_primitive_route_completion",
            ],
            blocked_shortcuts_not_global_closure=[
                "reflection positivity alone",
                "gauge Perron import",
                "symmetry labels or D17 support without dynamics",
            ],
        ),
    ]

    route_ids = [route["route_id"] for route in routes]
    unique_routes = len(route_ids) == len(set(route_ids))
    all_open_positive = all(route["candidate_status"] == "positive_candidate_open" for route in routes)

    report("required-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("taste-shortcut-blocked-not-global-closure", taste_blocks_shortcut, status(certs["taste_condensate_oh_bridge"]))
    report("repo-canonical-oh-absent", repo_oh_absent, status(certs["canonical_higgs_repo_authority"]))
    report("source-higgs-launch-blocked-but-contract-present", source_higgs_launch_blocked, status(certs["source_higgs_production_readiness"]))
    report("wz-ratio-support-present", wz_ratio_support, status(certs["fh_gauge_normalized_response"]))
    report("wz-production-inputs-absent", wz_inputs_absent, status(certs["wz_mass_fit_response_row_builder"]))
    report("strict-g2-certificate-absent", g2_absent, status(certs["electroweak_g2_certificate_builder"]))
    report("schur-support-present", schur_support, status(certs["schur_kprime_sufficiency"]))
    report("schur-abc-rows-absent", schur_rows_absent, status(certs["schur_abc_definition_attempt"]))
    report("neutral-primitive-contract-present", neutral_contract, status(certs["neutral_primitive_cone_gate"]))
    report("rank-one-conditional-support-present", rank_one_support, status(certs["positivity_improving_rank_one_support"]))
    report("negative-boundaries-scoped", negative_boundaries_scoped, status(certs["negative_route_applicability_review"]))
    report("source-coordinate-current-surface-closed", source_transport_current_surface_closed, status(certs["source_coordinate_transport_completion"]))
    report("action-first-current-surface-closed", action_first_current_surface_closed, status(certs["action_first_route_completion"]))
    report("wz-response-current-surface-closed", wz_response_current_surface_closed, status(certs["wz_response_route_completion"]))
    report("schur-current-surface-closed", schur_current_surface_closed, status(certs["schur_route_completion"]))
    report("neutral-primitive-current-surface-closed", neutral_current_surface_closed, status(certs["neutral_primitive_route_completion"]))
    report("assembly-still-open", assembly_still_open, "proposal_allowed=false across assembly/retained/campaign gates")
    report("candidate-routes-unique", unique_routes, f"routes={route_ids}")
    report("candidate-routes-open-not-closure", all_open_positive, "all routes are positive_candidate_open")

    result = {
        "actual_current_surface_status": "open / first-principles O_H bridge positive-candidate portfolio",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This is a route-selection and artifact-planning certificate.  It "
            "identifies positive candidates to pursue, but no route currently "
            "supplies O_H, C_sH/C_HH rows, W/Z rows with strict g2, Schur A/B/C "
            "rows, or a neutral primitive-cone theorem."
        ),
        "bare_retained_allowed": False,
        "candidate_portfolio_passed": FAIL_COUNT == 0,
        "candidate_count": len(routes),
        "ranked_positive_candidates": routes,
        "current_global_status": {
            "assembly_still_open": assembly_still_open,
            "full_positive_assembly_pass_count": certs["full_positive_assembly"].get("pass_count"),
            "full_positive_assembly_fail_count": certs["full_positive_assembly"].get("fail_count"),
            "retained_route_pass_count": certs["retained_route"].get("pass_count"),
            "retained_route_fail_count": certs["retained_route"].get("fail_count"),
            "campaign_status_pass_count": certs["campaign_status"].get("pass_count"),
            "campaign_status_fail_count": certs["campaign_status"].get("fail_count"),
        },
        "synthesis": [
            "Action-first O_H plus C_sH/C_HH rows remains a future physical route, but the current surface lacks the same-source EW/Higgs action, canonical O_H, rows, and Gram-purity certificates.",
            "The W/Z physical-observable bypass remains a future route, but the current surface lacks same-source EW action, W/Z rows, matched covariance, strict g2, and delta_perp control.",
            "The derivation-native neutral primitive/rank-one lane remains future-open but needs an actual same-surface primitive transfer or off-diagonal generator certificate.",
            "Schur is a good algebraic row-compression route after a neutral kernel basis exists; current source-only rows cannot define A/B/C.",
            "Source-coordinate transport now has an exact current-surface boundary: I_8 cannot be transported to trace-zero S_i by current algebraic/symmetry maps, but a future non-shortcut transport certificate could reopen it.",
        ],
        "negative_boundary_interpretation": {
            "blocks_only": ["shortcut", "current_surface"],
            "blocks_first_principles_derivation": False,
            "same_surface_required": True,
            "does_not_block": [
                "future same-surface source-coordinate transport theorem",
                "future canonical O_H plus C_sH/C_HH pole rows",
                "future W/Z response rows with strict g2/covariance/delta_perp",
                "future Schur A/B/C rows from a real neutral kernel",
                "future neutral primitive-cone or off-diagonal-generator theorem",
            ],
            "reopen_artifact_keys": [
                "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
                "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
                "outputs/yt_electroweak_g2_certificate_2026-05-04.json",
                "outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json",
                "outputs/yt_schur_scalar_kernel_rows_2026-05-03.json",
                "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
            ],
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not certify O_H, C_sH/C_HH, W/Z rows, Schur rows, or primitive-cone rows",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, u0, kappa_s=1, cos(theta)=1, c2=1, or Z_match=1",
            "does not treat exact negative boundaries as global investigation closure",
        ],
        "certificates": CERTS,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
