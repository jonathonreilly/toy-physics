#!/usr/bin/env python3
"""
PR #230 assumption/import stress certificate.

This runner makes the physics-loop assumption exercise executable.  It checks
that the current PR #230 positive-closure routes still separate allowed
substrate inputs from forbidden proof imports, and that no route is allowed to
claim retained top-Yukawa closure while the scalar-LSZ or heavy-matching imports
remain open.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / ".claude" / "science" / "physics-loops" / "yt-pr230-ward-physical-readout-20260501"
ACTIVE_PACK = (
    ROOT
    / ".claude"
    / "science"
    / "physics-loops"
    / "yt-pr230-osp-oh-retained-closure-20260503"
)
TASTE_BRIDGE_PACK = (
    ROOT
    / ".claude"
    / "science"
    / "physics-loops"
    / "pr230-oh-csh-chh-bridge-20260506"
)
ASSUMPTIONS = PACK / "ASSUMPTIONS_AND_IMPORTS.md"
ACTIVE_ASSUMPTIONS = ACTIVE_PACK / "ASSUMPTIONS_AND_IMPORTS.md"
TASTE_BRIDGE_ASSUMPTIONS = TASTE_BRIDGE_PACK / "ASSUMPTIONS_AND_IMPORTS.md"
OUTPUT = ROOT / "outputs" / "yt_pr230_assumption_import_stress_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main() -> int:
    print("PR #230 assumption/import stress certificate")
    print("=" * 72)

    text = ASSUMPTIONS.read_text(encoding="utf-8")
    active_text = ACTIVE_ASSUMPTIONS.read_text(encoding="utf-8")
    taste_bridge_text = TASTE_BRIDGE_ASSUMPTIONS.read_text(encoding="utf-8")
    combined_text = f"{text}\n\n{active_text}\n\n{taste_bridge_text}"
    certificates = {
        "campaign": load("outputs/yt_pr230_campaign_status_certificate_2026-05-01.json"),
        "clean_source_higgs_math_tool_selector": load(
            "outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json"
        ),
        "invariant_ring_oh_certificate_attempt": load(
            "outputs/yt_pr230_invariant_ring_oh_certificate_attempt_2026-05-05.json"
        ),
        "gns_source_higgs_flat_extension_attempt": load(
            "outputs/yt_pr230_gns_source_higgs_flat_extension_attempt_2026-05-05.json"
        ),
        "neutral_scalar_burnside_irreducibility_attempt": load(
            "outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json"
        ),
        "neutral_offdiagonal_generator_derivation_attempt": load(
            "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json"
        ),
        "logdet_hessian_neutral_mixing_attempt": load(
            "outputs/yt_pr230_logdet_hessian_neutral_mixing_attempt_2026-05-05.json"
        ),
        "schur_abc_definition_derivation_attempt": load(
            "outputs/yt_pr230_schur_abc_definition_derivation_attempt_2026-05-05.json"
        ),
        "wz_g2_bare_running_bridge_attempt": load(
            "outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json"
        ),
        "scalar_lsz_carleman_tauberian_determinacy_attempt": load(
            "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json"
        ),
        "fh_lsz_complete_bernstein_inverse_diagnostic": load(
            "outputs/yt_fh_lsz_complete_bernstein_inverse_diagnostic_2026-05-05.json"
        ),
        "fresh_artifact_literature_route_review": load(
            "outputs/yt_pr230_fresh_artifact_literature_route_review_2026-05-05.json"
        ),
        "action_first_oh_artifact_attempt": load(
            "outputs/yt_pr230_action_first_oh_artifact_attempt_2026-05-05.json"
        ),
        "holonomic_source_response_feasibility_gate": load(
            "outputs/yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json"
        ),
        "oh_source_higgs_authority_rescan_gate": load(
            "outputs/yt_pr230_oh_source_higgs_authority_rescan_gate_2026-05-05.json"
        ),
        "derived_bridge_rank_one_closure_attempt": load(
            "outputs/yt_pr230_derived_bridge_rank_one_closure_attempt_2026-05-05.json"
        ),
        "source_sector_pattern_transfer_gate": load(
            "outputs/yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json"
        ),
        "det_positivity_bridge_intake_gate": load(
            "outputs/yt_pr230_det_positivity_bridge_intake_gate_2026-05-05.json"
        ),
        "reflection_det_primitive_upgrade_gate": load(
            "outputs/yt_pr230_reflection_det_primitive_upgrade_gate_2026-05-05.json"
        ),
        "minimal_axioms_yukawa_summary_firewall": load(
            "outputs/yt_pr230_minimal_axioms_yukawa_summary_firewall_2026-05-05.json"
        ),
        "genuine_source_pole_artifact_intake": load(
            "outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json"
        ),
        "l12_chunk_compute_status": load(
            "outputs/yt_pr230_l12_chunk_compute_status_2026-05-06.json"
        ),
        "taste_condensate_oh_bridge_audit": load(
            "outputs/yt_pr230_taste_condensate_oh_bridge_audit_2026-05-06.json"
        ),
        "source_coordinate_transport_gate": load(
            "outputs/yt_pr230_source_coordinate_transport_gate_2026-05-06.json"
        ),
        "origin_main_composite_higgs_intake_guard": load(
            "outputs/yt_pr230_origin_main_composite_higgs_intake_guard_2026-05-06.json"
        ),
        "origin_main_ew_m_residual_intake_guard": load(
            "outputs/yt_pr230_origin_main_ew_m_residual_intake_guard_2026-05-06.json"
        ),
        "z3_triplet_conditional_primitive_cone_theorem": load(
            "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
        ),
        "z3_generation_action_lift_attempt": load(
            "outputs/yt_pr230_z3_generation_action_lift_attempt_2026-05-06.json"
        ),
        "z3_lazy_transfer_promotion_attempt": load(
            "outputs/yt_pr230_z3_lazy_transfer_promotion_attempt_2026-05-06.json"
        ),
        "source_coordinate_transport_completion_attempt": load(
            "outputs/yt_pr230_source_coordinate_transport_completion_attempt_2026-05-06.json"
        ),
        "two_source_taste_radial_chart_certificate": load(
            "outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json"
        ),
        "two_source_taste_radial_action_certificate": load(
            "outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json"
        ),
        "two_source_taste_radial_row_contract": load(
            "outputs/yt_pr230_two_source_taste_radial_row_contract_2026-05-06.json"
        ),
        "two_source_taste_radial_row_production_manifest": load(
            "outputs/yt_pr230_two_source_taste_radial_row_production_manifest_2026-05-06.json"
        ),
        "taste_radial_canonical_oh_selector_gate": load(
            "outputs/yt_pr230_taste_radial_canonical_oh_selector_gate_2026-05-06.json"
        ),
        "degree_one_higgs_action_premise_gate": load(
            "outputs/yt_pr230_degree_one_higgs_action_premise_gate_2026-05-06.json"
        ),
        "fms_post_degree_route_rescore": load(
            "outputs/yt_pr230_fms_post_degree_route_rescore_2026-05-06.json"
        ),
        "action_first_route_completion": load(
            "outputs/yt_pr230_action_first_route_completion_2026-05-06.json"
        ),
        "wz_response_route_completion": load(
            "outputs/yt_pr230_wz_response_route_completion_2026-05-06.json"
        ),
        "schur_route_completion": load(
            "outputs/yt_pr230_schur_route_completion_2026-05-06.json"
        ),
        "neutral_primitive_route_completion": load(
            "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json"
        ),
        "oh_bridge_candidate_portfolio": load(
            "outputs/yt_pr230_oh_bridge_first_principles_candidate_portfolio_2026-05-06.json"
        ),
        "negative_route_applicability_review": load(
            "outputs/yt_pr230_negative_route_applicability_review_2026-05-06.json"
        ),
        "kinetic_matching": load("outputs/yt_heavy_kinetic_matching_obstruction_2026-05-01.json"),
        "momentum_pilot": load("outputs/yt_momentum_pilot_scaling_certificate_2026-05-01.json"),
        "scalar_ir": load("outputs/yt_scalar_ladder_ir_zero_mode_obstruction_2026-05-01.json"),
        "projector_norm": load("outputs/yt_scalar_ladder_projector_normalization_obstruction_2026-05-01.json"),
        "scalar_renormalization_condition_overlap": load(
            "outputs/yt_scalar_renormalization_condition_overlap_no_go_2026-05-01.json"
        ),
        "source_contact_term_scheme": load(
            "outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json"
        ),
        "finite_source_shift_derivative_no_go": load(
            "outputs/yt_finite_source_shift_derivative_no_go_2026-05-02.json"
        ),
        "source_higgs_cross_correlator_import": load(
            "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json"
        ),
        "same_source_wz_response_certificate_gate": load(
            "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json"
        ),
        "canonical_higgs_operator_realization_gate": load(
            "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json"
        ),
        "hunit_canonical_higgs_operator_candidate_gate": load(
            "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json"
        ),
        "source_higgs_harness_absence_guard": load(
            "outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json"
        ),
        "source_pole_purity_cross_correlator_gate": load(
            "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json"
        ),
        "source_functional_lsz_identifiability": load(
            "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json"
        ),
    }

    required_terms = [
        "H_unit-to-top matrix-element definition",
        "H_unit matrix-element readout",
        "yt_ward_identity as y_t authority",
        "observed top mass / observed y_t as proof selectors",
        "alpha_LM / plaquette / u0 as load-bearing normalization",
        "alpha_LM / plaquette / u0 as load-bearing proof input",
        "c2 = 1 unless derived",
        "Z_match = 1 unless derived",
        "kappa_s = 1 unless derived",
        "source operator overlap",
        "Source contact counterterms",
        "Single finite source-shift radius as a zero-source derivative",
        "Source-Higgs cross-correlator `C_sH`",
        "Static EW W/Z algebra is not a source-response certificate",
        "Slope-only W/Z outputs",
        "same-surface PR #230 operator",
        "`O_H`",
        "`H_unit` matrix-element readout",
        "reduced cold pilots as production evidence",
        "`source_higgs_cross_correlator` guard is claim",
        "`wz_mass_response` guard is claim",
        "Reduced cold-gauge momentum pilots",
        "Outside-math algorithms",
        "not proof selectors",
        "PSLQ",
        "invariant-ring/commutant",
        "Invariant-ring/commutant/Schur multiplicity-one argument",
        "two-singlet completion",
        "GNS/source-Higgs flat extension",
        "not proof selectors until O_H/C_sH/C_HH rows exist",
        "Burnside/double-commutant neutral irreducibility",
        "not proof selectors until a same-surface off-diagonal neutral generator or primitive transfer exists",
        "Neutral off-diagonal generator derivation",
        "not proof selectors until the mixed generator is derived on the same PR230 surface",
        "Staggered logdet Hessian neutral-mixing attempt",
        "source-only logdet tower does not define h/O_H",
        "Schur A/B/C definition derivation",
        "not proof selectors until same-surface Schur A/B/C rows and projectors exist",
        "W/Z g2 bare-running bridge",
        "not proof selectors until same-source EW action, scale ratio, thresholds, and finite matching exist",
        "Carleman/Tauberian scalar-LSZ determinacy",
        "not proof selectors until an infinite same-surface moment/asymptotic certificate exists",
        "Complete-Bernstein inverse-propagator diagnostic",
        "not proof selectors until a certified scalar denominator object passes the inverse tests",
        "FMS/action-first source-Higgs artifact route",
        "action-first `O_H/C_sH/C_HH`",
        "PR541-style holonomic source-response route",
        "not proof selectors until a same-current-surface O_H/h-source artifact exists",
        "O_H/source-Higgs authority rescan",
        "not proof selectors until canonical O_H or C_sH/C_HH pole rows exist",
        "Reflection plus determinant positivity primitive-upgrade",
        "same-surface neutral primitive-cone certificate exists",
        "MINIMAL_AXIOMS y_t/m_t summary",
        "not proof authority until the summarized Ward/H_unit y_t lane is repaired",
        "Genuine source-pole O_sp artifact",
        "source-side support only until canonical O_H and C_spH/C_HH rows exist",
        "Completed L12 chunk compute status",
        "not physical y_t closure until scalar-LSZ, O_H/source-overlap, FV/IR, and matching/running gates pass",
        "Taste-condensate O_H bridge",
        "uniform mass source is orthogonal to taste-axis Higgs operators",
        "not proof selectors until source-coordinate transport or C_sH/C_HH rows exist",
        "Source-coordinate transport to O_H",
        "not proof selectors until a same-surface transport certificate exists",
        "Source-coordinate transport completion",
        "unit-preserving/trace-preserving/taste-equivariant maps cannot send I_8 to trace-zero S_i",
        "not proof selectors until source-to-taste-axis certificate, canonical O_H rows, or neutral rank-one theorem exists",
        "Action-first O_H/C_sH/C_HH route completion",
        "not proof selectors until same-source EW/Higgs action, canonical O_H, source-Higgs rows, and Gram-purity certificate exist",
        "W/Z same-source response route completion",
        "not proof selectors until same-source EW action, W/Z response rows, matched covariance, strict g2, and delta_perp control exist",
        "Schur A/B/C route completion",
        "not proof selectors until neutral kernel basis plus Schur A/B/C rows or equivalent row theorem exists",
        "Neutral primitive/rank-one route completion",
        "not proof selectors until same-surface primitive transfer, off-diagonal generator, or irreducibility certificate exists",
        "Z3 lazy-transfer promotion attempt",
        "same-surface neutral transfer/action or off-diagonal generator",
        "Origin-main EW M-residual CMT packet",
        "CMT/u0/Fierz channel bookkeeping is not proof selectors",
        "Two-source taste-radial action source vertex",
        "not proof selectors until measured C_sx/C_xx rows and canonical O_H/source-overlap or physical-response authority exist",
        "Two-source taste-radial row contract",
        "not proof selectors until production C_sx/C_xx rows, pole/FV/IR authority, and canonical O_H/source-overlap or physical-response authority exist",
        "Two-source taste-radial row production manifest",
        "not proof selectors until the planned chunks are actually run, combined, pole-tested, and bridged to canonical O_H or physical response",
        "Degree-one Higgs-action premise",
        "Degree-one Higgs-action premise is not proof selectors until a same-surface EW/Higgs action or canonical-operator theorem derives the degree-one premise",
        "FMS post-degree route rescore",
        "FMS/lattice literature is route guidance only, not PR230 proof authority",
    ]
    missing_terms = [term for term in required_terms if term not in combined_text]
    proposal_allowed = [
        name for name, cert in certificates.items() if cert.get("proposal_allowed") is True
    ]
    loaded_failures = [
        name
        for name, cert in certificates.items()
        if name != "campaign" and int(cert.get("fail_count", 0)) != 0
    ]

    report("assumption-ledger-present", ASSUMPTIONS.exists(), str(ASSUMPTIONS.relative_to(ROOT)))
    report(
        "active-assumption-ledger-present",
        ACTIVE_ASSUMPTIONS.exists(),
        str(ACTIVE_ASSUMPTIONS.relative_to(ROOT)),
    )
    report(
        "taste-bridge-assumption-ledger-present",
        TASTE_BRIDGE_ASSUMPTIONS.exists(),
        str(TASTE_BRIDGE_ASSUMPTIONS.relative_to(ROOT)),
    )
    report("refreshed-kinetic-imports-present", "Heavy kinetic-action coefficient `c2`" in text and "Z_match" in text, "c2 and Z_match imports named")
    report("forbidden-imports-explicit", not missing_terms, f"missing={missing_terms}")
    report(
        "loaded-support-certificates-no-fail",
        not loaded_failures,
        f"failures={loaded_failures} count={len(certificates)}",
    )
    negative_route_review = certificates["negative_route_applicability_review"]
    report(
        "negative-route-applicability-review-preserves-future-reopen",
        negative_route_review.get("no_retained_negative_overclaim") is True
        and negative_route_review.get("future_reopen_paths_preserved") is True
        and negative_route_review.get("selected_negative_results_apply_on_current_surface") is True,
        negative_route_review.get("actual_current_surface_status"),
    )
    report("no-route-authorizes-retained-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "kinetic-countermodel-load-bearing",
        "exact negative boundary" in str(certificates["kinetic_matching"].get("actual_current_surface_status")),
        certificates["kinetic_matching"].get("actual_current_surface_status"),
    )
    report(
        "reduced-pilot-not-strict-evidence",
        "bounded-support" in str(certificates["momentum_pilot"].get("actual_current_surface_status")),
        certificates["momentum_pilot"].get("actual_current_surface_status"),
    )
    report(
        "scalar-ladder-imports-remain-open",
        "zero-mode" in str(certificates["scalar_ir"].get("actual_current_surface_status"))
        and "projector" in str(certificates["projector_norm"].get("actual_current_surface_status")),
        "IR/zero-mode and projector normalization obstructions loaded",
    )
    report(
        "canonical-kinetic-normalization-not-source-overlap",
        "renormalization-condition source-overlap no-go"
        in str(certificates["scalar_renormalization_condition_overlap"].get("actual_current_surface_status")),
        certificates["scalar_renormalization_condition_overlap"].get("actual_current_surface_status"),
    )
    report(
        "source-contact-terms-not-pole-residue",
        "source contact-term scheme boundary"
        in str(certificates["source_contact_term_scheme"].get("actual_current_surface_status")),
        certificates["source_contact_term_scheme"].get("actual_current_surface_status"),
    )
    report(
        "single-finite-source-radius-not-zero-derivative",
        "finite source-shift slope not zero-source derivative certificate"
        in str(certificates["finite_source_shift_derivative_no_go"].get("actual_current_surface_status")),
        certificates["finite_source_shift_derivative_no_go"].get("actual_current_surface_status"),
    )
    report(
        "source-higgs-cross-correlator-not-hidden-authority",
        "source-Higgs cross-correlator import audit"
        in str(certificates["source_higgs_cross_correlator_import"].get("actual_current_surface_status"))
        and certificates["source_higgs_cross_correlator_import"].get(
            "source_higgs_cross_correlator_authority_found"
        )
        is False,
        certificates["source_higgs_cross_correlator_import"].get("actual_current_surface_status"),
    )
    report(
        "static-wz-algebra-not-source-response",
        "same-source WZ response certificate gate not passed"
        in str(certificates["same_source_wz_response_certificate_gate"].get("actual_current_surface_status"))
        and certificates["same_source_wz_response_certificate_gate"].get(
            "same_source_wz_response_certificate_gate_passed"
        )
        is False,
        certificates["same_source_wz_response_certificate_gate"].get("actual_current_surface_status"),
    )
    report(
        "canonical-higgs-operator-not-realized",
        "canonical-Higgs operator realization gate not passed"
        in str(certificates["canonical_higgs_operator_realization_gate"].get("actual_current_surface_status"))
        and certificates["canonical_higgs_operator_realization_gate"].get(
            "canonical_higgs_operator_realization_gate_passed"
        )
        is False,
        certificates["canonical_higgs_operator_realization_gate"].get("actual_current_surface_status"),
    )
    report(
        "hunit-not-canonical-higgs-operator",
        "H_unit not canonical-Higgs operator realization"
        in str(certificates["hunit_canonical_higgs_operator_candidate_gate"].get("actual_current_surface_status"))
        and certificates["hunit_canonical_higgs_operator_candidate_gate"].get(
            "hunit_canonical_higgs_operator_gate_passed"
        )
        is False,
        certificates["hunit_canonical_higgs_operator_candidate_gate"].get("actual_current_surface_status"),
    )
    source_higgs_guard = certificates["source_higgs_harness_absence_guard"]
    source_higgs_guard_fields = source_higgs_guard.get("guard_fields", {})
    report(
        "source-higgs-default-off-guard-not-evidence",
        "source-Higgs harness default-off guard"
        in str(source_higgs_guard.get("actual_current_surface_status"))
        and source_higgs_guard.get("proposal_allowed") is False
        and source_higgs_guard_fields.get("source_higgs_cross_correlator") is True
        and source_higgs_guard_fields.get("enabled_false") is True
        and source_higgs_guard_fields.get("canonical_higgs_operator_certificate_gated") is True
        and source_higgs_guard_fields.get("used_as_physical_yukawa_readout_false") is True,
        source_higgs_guard.get("actual_current_surface_status"),
    )
    report(
        "source-pole-purity-gate-rejects-guard-only-schema",
        "source-pole purity cross-correlator gate not passed"
        in str(certificates["source_pole_purity_cross_correlator_gate"].get("actual_current_surface_status"))
        and certificates["source_pole_purity_cross_correlator_gate"].get("source_pole_purity_gate_passed")
        is False
        and certificates["source_pole_purity_cross_correlator_gate"].get(
            "current_harness_source_higgs_status", {}
        ).get("guarded_absence")
        is True
        and certificates["source_pole_purity_cross_correlator_gate"].get(
            "current_harness_source_higgs_status", {}
        ).get("real_measurement_path")
        is False,
        certificates["source_pole_purity_cross_correlator_gate"].get("actual_current_surface_status"),
    )
    report(
        "source-functional-lsz-rejects-source-only-closure",
        "source-functional LSZ identifiability theorem"
        in str(certificates["source_functional_lsz_identifiability"].get("actual_current_surface_status"))
        and certificates["source_functional_lsz_identifiability"].get("proposal_allowed") is False
        and certificates["source_functional_lsz_identifiability"].get("theorem_closed") is False
        and "kappa_s = 1 unless derived by scalar LSZ/canonical normalization"
        in certificates["source_functional_lsz_identifiability"].get("forbidden_shortcuts_checked", []),
        certificates["source_functional_lsz_identifiability"].get("actual_current_surface_status"),
    )
    math_selector = certificates["clean_source_higgs_math_tool_selector"]
    report(
        "outside-math-tools-not-proof-selectors",
        "clean source-Higgs outside-math route selector"
        in str(math_selector.get("actual_current_surface_status"))
        and math_selector.get("proposal_allowed") is False
        and math_selector.get("clean_physics_priority") == "source_higgs"
        and math_selector.get("forbidden_firewall", {}).get(
            "used_pslq_or_value_recognition_as_proof_selector"
        )
        is False,
        math_selector.get("actual_current_surface_status"),
    )
    invariant_attempt = certificates["invariant_ring_oh_certificate_attempt"]
    report(
        "invariant-ring-attempt-does-not-certify-oh",
        "invariant-ring O_H certificate attempt blocked"
        in str(invariant_attempt.get("actual_current_surface_status"))
        and invariant_attempt.get("proposal_allowed") is False
        and invariant_attempt.get("invariant_ring_certificate_passed") is False
        and invariant_attempt.get("canonical_oh_certificate_written") is False
        and invariant_attempt.get("future_file_presence", {}).get("canonical_oh_certificate")
        is False,
        invariant_attempt.get("actual_current_surface_status"),
    )
    gns_attempt = certificates["gns_source_higgs_flat_extension_attempt"]
    report(
        "gns-flat-extension-attempt-does-not-certify-source-higgs-purity",
        "GNS source-Higgs flat-extension attempt"
        in str(gns_attempt.get("actual_current_surface_status"))
        and gns_attempt.get("proposal_allowed") is False
        and gns_attempt.get("gns_flat_extension_passed") is False
        and gns_attempt.get("gns_certificate_written") is False
        and gns_attempt.get("future_file_presence", {}).get(
            "source_higgs_measurement_rows"
        )
        is False,
        gns_attempt.get("actual_current_surface_status"),
    )
    burnside_attempt = certificates["neutral_scalar_burnside_irreducibility_attempt"]
    report(
        "burnside-double-commutant-attempt-does-not-certify-neutral-irreducibility",
        "Burnside neutral irreducibility attempt"
        in str(burnside_attempt.get("actual_current_surface_status"))
        and burnside_attempt.get("proposal_allowed") is False
        and burnside_attempt.get("burnside_irreducibility_certificate_passed") is False
        and burnside_attempt.get("burnside_certificate_written") is False
        and burnside_attempt.get("future_file_presence", {}).get(
            "burnside_irreducibility_certificate"
        )
        is False,
        burnside_attempt.get("actual_current_surface_status"),
    )
    offdiag_attempt = certificates["neutral_offdiagonal_generator_derivation_attempt"]
    report(
        "neutral-offdiagonal-generator-attempt-does-not-certify-primitive-cone",
        "neutral off-diagonal generator not derivable"
        in str(offdiag_attempt.get("actual_current_surface_status"))
        and offdiag_attempt.get("proposal_allowed") is False
        and offdiag_attempt.get("offdiagonal_generator_certificate_passed") is False
        and offdiag_attempt.get("offdiagonal_generator_written") is False
        and offdiag_attempt.get("future_file_presence", {}).get(
            "offdiagonal_generator_certificate"
        )
        is False,
        offdiag_attempt.get("actual_current_surface_status"),
    )
    carleman_attempt = certificates["scalar_lsz_carleman_tauberian_determinacy_attempt"]
    report(
        "carleman-tauberian-attempt-does-not-certify-scalar-lsz-determinacy",
        "Carleman/Tauberian scalar-LSZ determinacy not derivable"
        in str(carleman_attempt.get("actual_current_surface_status"))
        and carleman_attempt.get("proposal_allowed") is False
        and carleman_attempt.get("carleman_tauberian_determinacy_passed") is False
        and carleman_attempt.get("finite_prefix_stieltjes_counterfamily_passed")
        is True,
        carleman_attempt.get("actual_current_surface_status"),
    )
    complete_bernstein = certificates["fh_lsz_complete_bernstein_inverse_diagnostic"]
    report(
        "complete-bernstein-inverse-diagnostic-does-not-certify-current-denominator",
        "complete-Bernstein monotonicity"
        in str(complete_bernstein.get("actual_current_surface_status"))
        and complete_bernstein.get("proposal_allowed") is False
        and complete_bernstein.get("complete_bernstein_inverse_certificate_passed")
        is False
        and complete_bernstein.get("violation_summary", {}).get(
            "all_adjacent_intervals_violate_non_decrease"
        )
        is True,
        complete_bernstein.get("actual_current_surface_status"),
    )
    schur_abc_attempt = certificates["schur_abc_definition_derivation_attempt"]
    report(
        "schur-abc-definition-attempt-does-not-certify-kprime-rows",
        "Schur A/B/C definition not derivable"
        in str(schur_abc_attempt.get("actual_current_surface_status"))
        and schur_abc_attempt.get("proposal_allowed") is False
        and schur_abc_attempt.get("schur_abc_definition_derivation_passed") is False
        and schur_abc_attempt.get("schur_abc_rows_written") is False
        and schur_abc_attempt.get("exact_negative_boundary_passed") is True,
        schur_abc_attempt.get("actual_current_surface_status"),
    )
    wz_g2_running_attempt = certificates["wz_g2_bare_running_bridge_attempt"]
    report(
        "wz-g2-bare-running-attempt-does-not-certify-low-scale-g2",
        "WZ g2 bare-to-low-scale running bridge"
        in str(wz_g2_running_attempt.get("actual_current_surface_status"))
        and wz_g2_running_attempt.get("proposal_allowed") is False
        and wz_g2_running_attempt.get("wz_g2_bare_running_bridge_passed") is False
        and wz_g2_running_attempt.get("strict_electroweak_g2_certificate_written") is False
        and wz_g2_running_attempt.get("exact_negative_boundary_passed") is True,
        wz_g2_running_attempt.get("actual_current_surface_status"),
    )
    fresh_artifact_review = certificates["fresh_artifact_literature_route_review"]
    report(
        "fresh-artifact-literature-review-selects-target-not-closure",
        "fresh artifact literature route review"
        in str(fresh_artifact_review.get("actual_current_surface_status"))
        and fresh_artifact_review.get("proposal_allowed") is False
        and fresh_artifact_review.get("review_passed") is True
        and fresh_artifact_review.get("genuine_artifact_found_on_current_surface")
        is False
        and fresh_artifact_review.get("selected_genuine_artifact_contract", {}).get(
            "contract"
        )
        == "O_H/C_sH/C_HH source-Higgs pole rows",
        fresh_artifact_review.get("actual_current_surface_status"),
    )
    action_first_attempt = certificates["action_first_oh_artifact_attempt"]
    report(
        "action-first-oh-artifact-attempt-does-not-certify-current-surface-oh",
        "action-first O_H artifact not constructible"
        in str(action_first_attempt.get("actual_current_surface_status"))
        and action_first_attempt.get("proposal_allowed") is False
        and action_first_attempt.get("exact_negative_boundary_passed") is True
        and action_first_attempt.get("same_source_ew_action_certificate_written")
        is False
        and action_first_attempt.get("canonical_oh_certificate_written") is False
        and action_first_attempt.get("source_higgs_rows_written") is False,
        action_first_attempt.get("actual_current_surface_status"),
    )
    holonomic_source_response = certificates["holonomic_source_response_feasibility_gate"]
    report(
        "holonomic-source-response-gate-does-not-supply-oh-or-h-source",
        "PR541-style holonomic source-response route"
        in str(holonomic_source_response.get("actual_current_surface_status"))
        and holonomic_source_response.get("proposal_allowed") is False
        and holonomic_source_response.get("exact_negative_boundary_passed") is True
        and holonomic_source_response.get("two_source_functional_current_surface_defined")
        is False
        and holonomic_source_response.get("pr541_route_immediate_closure") is False,
        holonomic_source_response.get("actual_current_surface_status"),
    )
    oh_source_higgs_rescan = certificates["oh_source_higgs_authority_rescan_gate"]
    report(
        "oh-source-higgs-authority-rescan-finds-no-current-certificate",
        "O_H/source-Higgs authority rescan found no"
        in str(oh_source_higgs_rescan.get("actual_current_surface_status"))
        and oh_source_higgs_rescan.get("proposal_allowed") is False
        and oh_source_higgs_rescan.get("oh_source_higgs_authority_found") is False
        and oh_source_higgs_rescan.get("exact_negative_boundary_passed") is True
        and oh_source_higgs_rescan.get("canonical_oh_absent") is True
        and oh_source_higgs_rescan.get("source_higgs_rows_absent") is True,
        oh_source_higgs_rescan.get("actual_current_surface_status"),
    )
    derived_bridge = certificates["derived_bridge_rank_one_closure_attempt"]
    report(
        "derived-bridge-rank-one-attempt-does-not-certify-source-to-oh",
        "derived rank-one bridge not closed"
        in str(derived_bridge.get("actual_current_surface_status"))
        and derived_bridge.get("proposal_allowed") is False
        and derived_bridge.get("derived_bridge_closure_passed") is False
        and derived_bridge.get("exact_negative_boundary_passed") is True
        and derived_bridge.get("future_artifact_presence", {}).get("source_higgs_rows")
        is False,
        derived_bridge.get("actual_current_surface_status"),
    )
    source_sector_transfer = certificates["source_sector_pattern_transfer_gate"]
    report(
        "source-sector-pattern-transfer-does-not-import-yukawa",
        "source-sector pattern is relevant"
        in str(source_sector_transfer.get("actual_current_surface_status"))
        and source_sector_transfer.get("proposal_allowed") is False
        and source_sector_transfer.get("approach_relevant") is True
        and source_sector_transfer.get("direct_closure_available") is False
        and source_sector_transfer.get("bounded_support_passed") is True,
        source_sector_transfer.get("actual_current_surface_status"),
    )
    det_positivity_intake = certificates["det_positivity_bridge_intake_gate"]
    report(
        "det-positivity-bridge-intake-does-not-certify-rank-one",
        "determinant positivity is useful"
        in str(det_positivity_intake.get("actual_current_surface_status"))
        and det_positivity_intake.get("proposal_allowed") is False
        and det_positivity_intake.get("candidate_present") is True
        and det_positivity_intake.get("determinant_bridge_closes_pr230") is False
        and det_positivity_intake.get("intake_gate_passed") is True,
        det_positivity_intake.get("actual_current_surface_status"),
    )
    reflection_det_upgrade = certificates["reflection_det_primitive_upgrade_gate"]
    report(
        "reflection-det-primitive-upgrade-does-not-certify-rank-one",
        "reflection plus determinant positivity"
        in str(reflection_det_upgrade.get("actual_current_surface_status"))
        and reflection_det_upgrade.get("proposal_allowed") is False
        and reflection_det_upgrade.get("primitive_upgrade_passed") is False
        and reflection_det_upgrade.get("exact_negative_boundary_passed") is True
        and reflection_det_upgrade.get("reflection_det_reducible_witness", {}).get(
            "orthogonal_neutral_top_coupling_can_survive"
        )
        is True,
        reflection_det_upgrade.get("actual_current_surface_status"),
    )
    logdet_hessian_mixing = certificates["logdet_hessian_neutral_mixing_attempt"]
    report(
        "logdet-hessian-neutral-mixing-does-not-derive-oh",
        "source-only staggered logdet Hessian does not derive"
        in str(logdet_hessian_mixing.get("actual_current_surface_status"))
        and logdet_hessian_mixing.get("proposal_allowed") is False
        and logdet_hessian_mixing.get("exact_negative_boundary_passed") is True
        and logdet_hessian_mixing.get("logdet_hessian_bridge_closes_pr230") is False
        and logdet_hessian_mixing.get("forbidden_firewall", {}).get(
            "uses_minimal_axioms_yukawa_summary_as_proof"
        )
        is False,
        logdet_hessian_mixing.get("actual_current_surface_status"),
    )
    minimal_axioms_firewall = certificates["minimal_axioms_yukawa_summary_firewall"]
    report(
        "minimal-axioms-yukawa-summary-not-proof-authority",
        "minimal-axioms Yukawa summary is not PR230 proof authority"
        in str(minimal_axioms_firewall.get("actual_current_surface_status"))
        and minimal_axioms_firewall.get("proposal_allowed") is False
        and minimal_axioms_firewall.get("exact_negative_boundary_passed") is True
        and minimal_axioms_firewall.get("forbidden_firewall", {}).get(
            "uses_minimal_axioms_yukawa_summary_as_authority"
        )
        is False
        and minimal_axioms_firewall.get("yt_ward_audit_status", {}).get(
            "effective_status"
        )
        == "audited_renaming",
        minimal_axioms_firewall.get("actual_current_surface_status"),
    )
    source_pole_intake = certificates["genuine_source_pole_artifact_intake"]
    report(
        "genuine-source-pole-artifact-not-oh-closure",
        "genuine same-source O_sp source-pole artifact"
        in str(source_pole_intake.get("actual_current_surface_status"))
        and source_pole_intake.get("proposal_allowed") is False
        and source_pole_intake.get("artifact_is_genuine_current_surface_support")
        is True
        and source_pole_intake.get("artifact_is_physics_closure") is False
        and source_pole_intake.get("canonical_higgs_operator_identity_passed")
        is False,
        source_pole_intake.get("actual_current_surface_status"),
    )
    l12_compute_status = certificates["l12_chunk_compute_status"]
    report(
        "completed-l12-chunk-compute-status-not-physical-yt",
        "completed L12 same-source chunk compute status"
        in str(l12_compute_status.get("actual_current_surface_status"))
        and l12_compute_status.get("proposal_allowed") is False
        and l12_compute_status.get("strict_closure_blockers", {}).get(
            "scalar_lsz_denominator_certificate_absent"
        )
        is True
        and l12_compute_status.get("strict_closure_blockers", {}).get(
            "canonical_oh_or_source_higgs_overlap_absent"
        )
        is True,
        l12_compute_status.get("actual_current_surface_status"),
    )
    negative_route_review = certificates["negative_route_applicability_review"]
    report(
        "negative-route-applicability-review-preserves-future-reopen",
        "negative-route applicability review passed"
        in str(negative_route_review.get("actual_current_surface_status"))
        and negative_route_review.get("proposal_allowed") is False
        and negative_route_review.get("negative_results_are_current_surface_blockers_only")
        is True
        and negative_route_review.get("future_reopen_paths_preserved") is True
        and negative_route_review.get("no_retained_negative_overclaim") is True,
        negative_route_review.get("actual_current_surface_status"),
    )
    taste_bridge = certificates["taste_condensate_oh_bridge_audit"]
    report(
        "taste-condensate-oh-bridge-does-not-supply-current-oh",
        "taste-condensate Higgs stack does not supply PR230 O_H bridge"
        in str(taste_bridge.get("actual_current_surface_status"))
        and taste_bridge.get("proposal_allowed") is False
        and taste_bridge.get("taste_condensate_oh_bridge_audit_passed") is True
        and taste_bridge.get("algebra", {}).get(
            "uniform_source_relative_projection_onto_taste_axis_span"
        )
        == 0.0,
        taste_bridge.get("actual_current_surface_status"),
    )
    source_coordinate_transport = certificates["source_coordinate_transport_gate"]
    report(
        "source-coordinate-transport-does-not-supply-current-oh",
        "source-coordinate transport to canonical O_H not derivable"
        in str(source_coordinate_transport.get("actual_current_surface_status"))
        and source_coordinate_transport.get("proposal_allowed") is False
        and source_coordinate_transport.get("source_coordinate_transport_gate_passed")
        is True
        and source_coordinate_transport.get("future_transport_certificate_present")
        is False,
        source_coordinate_transport.get("actual_current_surface_status"),
    )
    composite_higgs_intake = certificates["origin_main_composite_higgs_intake_guard"]
    report(
        "origin-main-composite-higgs-packet-not-pr230-oh-authority",
        "origin/main composite-Higgs stretch"
        in str(composite_higgs_intake.get("actual_current_surface_status"))
        and composite_higgs_intake.get("proposal_allowed") is False
        and composite_higgs_intake.get("origin_main_composite_higgs_intake_guard_passed")
        is True
        and composite_higgs_intake.get("origin_main_composite_higgs_closes_pr230")
        is False,
        composite_higgs_intake.get("actual_current_surface_status"),
    )
    ew_m_residual_intake = certificates["origin_main_ew_m_residual_intake_guard"]
    report(
        "origin-main-ew-m-residual-packet-not-pr230-wz-authority",
        "origin/main EW M-residual CMT packet"
        in str(ew_m_residual_intake.get("actual_current_surface_status"))
        and ew_m_residual_intake.get("proposal_allowed") is False
        and ew_m_residual_intake.get(
            "origin_main_ew_m_residual_intake_guard_passed"
        )
        is True
        and ew_m_residual_intake.get("origin_main_ew_m_residual_closes_pr230")
        is False
        and ew_m_residual_intake.get("packet_classification", {}).get(
            "explicit_nonclosure"
        )
        is True,
        ew_m_residual_intake.get("actual_current_surface_status"),
    )
    z3_primitive = certificates["z3_triplet_conditional_primitive_cone_theorem"]
    report(
        "z3-triplet-primitive-theorem-conditional-not-pr230-closure",
        "Z3-triplet primitive-cone theorem"
        in str(z3_primitive.get("actual_current_surface_status"))
        and z3_primitive.get("proposal_allowed") is False
        and z3_primitive.get("z3_triplet_conditional_primitive_theorem_passed")
        is True
        and z3_primitive.get("pr230_closure_authorized") is False,
        z3_primitive.get("actual_current_surface_status"),
    )
    z3_generation_lift = certificates["z3_generation_action_lift_attempt"]
    report(
        "z3-generation-action-lift-not-derived",
        "Z3 generation-action lift"
        in str(z3_generation_lift.get("actual_current_surface_status"))
        and z3_generation_lift.get("proposal_allowed") is False
        and z3_generation_lift.get("h1_generation_action_lift_attempt_passed")
        is True
        and z3_generation_lift.get("same_surface_h1_derived") is False
        and z3_generation_lift.get("pr230_closure_authorized") is False,
        z3_generation_lift.get("actual_current_surface_status"),
    )
    z3_lazy_transfer = certificates["z3_lazy_transfer_promotion_attempt"]
    report(
        "z3-lazy-transfer-promotion-not-derived",
        "Z3 lazy-transfer promotion not derivable"
        in str(z3_lazy_transfer.get("actual_current_surface_status"))
        and z3_lazy_transfer.get("proposal_allowed") is False
        and z3_lazy_transfer.get("z3_lazy_transfer_promotion_attempt_passed")
        is True
        and z3_lazy_transfer.get("physical_lazy_transfer_instantiated") is False
        and z3_lazy_transfer.get("pr230_closure_authorized") is False,
        z3_lazy_transfer.get("actual_current_surface_status"),
    )
    source_transport_completion = certificates["source_coordinate_transport_completion_attempt"]
    report(
        "source-coordinate-transport-current-surface-closed",
        "source-coordinate transport not derivable from current PR230 surface"
        in str(source_transport_completion.get("actual_current_surface_status"))
        and source_transport_completion.get("proposal_allowed") is False
        and source_transport_completion.get("source_coordinate_transport_completion_passed")
        is True
        and source_transport_completion.get("algebra", {}).get(
            "source_relative_projection_onto_taste_axis_span"
        )
        == 0.0,
        source_transport_completion.get("actual_current_surface_status"),
    )
    two_source_chart = certificates["two_source_taste_radial_chart_certificate"]
    report(
        "two-source-taste-radial-chart-support-not-oh-closure",
        "two-source taste-radial chart"
        in str(two_source_chart.get("actual_current_surface_status"))
        and two_source_chart.get("proposal_allowed") is False
        and two_source_chart.get("two_source_taste_radial_chart_support_passed")
        is True
        and two_source_chart.get("new_second_source_axis", {}).get(
            "orthogonal_to_pr230_source"
        )
        is True
        and two_source_chart.get("forbidden_firewall", {}).get(
            "identified_taste_radial_axis_with_canonical_oh"
        )
        is False,
        two_source_chart.get("actual_current_surface_status"),
    )
    two_source_action = certificates["two_source_taste_radial_action_certificate"]
    report(
        "two-source-taste-radial-action-support-not-oh-closure",
        "two-source taste-radial action source vertex"
        in str(two_source_action.get("actual_current_surface_status"))
        and two_source_action.get("proposal_allowed") is False
        and two_source_action.get("two_source_taste_radial_action_passed") is True
        and two_source_action.get("operator_certificate_payload", {}).get(
            "canonical_higgs_operator_identity_passed"
        )
        is False
        and two_source_action.get("forbidden_firewall", {}).get(
            "used_taste_radial_axis_as_canonical_oh"
        )
        is False,
        two_source_action.get("actual_current_surface_status"),
    )
    two_source_row_contract = certificates["two_source_taste_radial_row_contract"]
    report(
        "two-source-taste-radial-row-contract-support-not-closure",
        "two-source taste-radial C_sx/C_xx row contract"
        in str(two_source_row_contract.get("actual_current_surface_status"))
        and two_source_row_contract.get("proposal_allowed") is False
        and two_source_row_contract.get("two_source_taste_radial_row_contract_passed")
        is True
        and two_source_row_contract.get("future_file_presence", {}).get(
            "taste_radial_production_rows"
        )
        is False,
        two_source_row_contract.get("actual_current_surface_status"),
    )
    two_source_row_manifest = certificates["two_source_taste_radial_row_production_manifest"]
    report(
        "two-source-taste-radial-row-production-manifest-not-evidence",
        "two-source taste-radial C_sx/C_xx production manifest"
        in str(two_source_row_manifest.get("actual_current_surface_status"))
        and two_source_row_manifest.get("proposal_allowed") is False
        and two_source_row_manifest.get("manifest_passed") is True
        and two_source_row_manifest.get("dry_run_only") is True
        and two_source_row_manifest.get("future_combined_rows_present") is False
        and two_source_row_manifest.get("production_policy", {}).get("resume_allowed")
        is False,
        two_source_row_manifest.get("actual_current_surface_status"),
    )
    taste_radial_selector = certificates["taste_radial_canonical_oh_selector_gate"]
    report(
        "taste-radial-canonical-oh-selector-blocks-symmetry-shortcut",
        "degree-one taste-radial uniqueness"
        in str(taste_radial_selector.get("actual_current_surface_status"))
        and taste_radial_selector.get("proposal_allowed") is False
        and taste_radial_selector.get("taste_radial_canonical_oh_selector_gate_passed")
        is True
        and taste_radial_selector.get("degree_one_radial_unique") is True
        and taste_radial_selector.get("full_invariant_selector_nonunique") is True
        and taste_radial_selector.get("canonical_oh_selector_absent") is True,
        taste_radial_selector.get("actual_current_surface_status"),
    )
    degree_one_premise = certificates["degree_one_higgs_action_premise_gate"]
    report(
        "degree-one-higgs-action-premise-not-derived",
        "degree-one Higgs-action premise not derived"
        in str(degree_one_premise.get("actual_current_surface_status"))
        and degree_one_premise.get("proposal_allowed") is False
        and degree_one_premise.get("degree_one_higgs_action_premise_gate_passed")
        is True
        and degree_one_premise.get("degree_one_filter_selects_e1") is True
        and degree_one_premise.get("degree_one_premise_authorized_on_current_surface")
        is False
        and degree_one_premise.get("odd_parity_filter_nonunique") is True
        and degree_one_premise.get("production_bridge_absent") is True,
        degree_one_premise.get("actual_current_surface_status"),
    )
    fms_post_degree = certificates["fms_post_degree_route_rescore"]
    report(
        "fms-post-degree-route-rescore-support-not-proof",
        "FMS post-degree route rescore"
        in str(fms_post_degree.get("actual_current_surface_status"))
        and fms_post_degree.get("proposal_allowed") is False
        and fms_post_degree.get("fms_post_degree_route_rescore_passed") is True
        and fms_post_degree.get("forbidden_firewall", {}).get(
            "used_literature_as_proof_authority"
        )
        is False
        and fms_post_degree.get("forbidden_firewall", {}).get(
            "used_degree_or_odd_parity_as_oh_authority"
        )
        is False,
        fms_post_degree.get("actual_current_surface_status"),
    )
    action_first_completion = certificates["action_first_route_completion"]
    report(
        "action-first-route-current-surface-closed",
        "action-first O_H/C_sH/C_HH route not complete on current PR230 surface"
        in str(action_first_completion.get("actual_current_surface_status"))
        and action_first_completion.get("proposal_allowed") is False
        and action_first_completion.get("action_first_route_completion_passed") is True,
        action_first_completion.get("actual_current_surface_status"),
    )
    wz_response_completion = certificates["wz_response_route_completion"]
    report(
        "wz-response-route-current-surface-closed",
        "WZ same-source response route not complete on current PR230 surface"
        in str(wz_response_completion.get("actual_current_surface_status"))
        and wz_response_completion.get("proposal_allowed") is False
        and wz_response_completion.get("wz_response_route_completion_passed") is True,
        wz_response_completion.get("actual_current_surface_status"),
    )
    schur_route_completion = certificates["schur_route_completion"]
    report(
        "schur-route-current-surface-closed",
        "Schur A/B/C route not complete on current PR230 surface"
        in str(schur_route_completion.get("actual_current_surface_status"))
        and schur_route_completion.get("proposal_allowed") is False
        and schur_route_completion.get("schur_route_completion_passed") is True,
        schur_route_completion.get("actual_current_surface_status"),
    )
    neutral_primitive_route_completion = certificates["neutral_primitive_route_completion"]
    report(
        "neutral-primitive-route-current-surface-closed",
        "neutral primitive-rank-one route not complete on current PR230 surface"
        in str(neutral_primitive_route_completion.get("actual_current_surface_status"))
        and neutral_primitive_route_completion.get("proposal_allowed") is False
        and neutral_primitive_route_completion.get("neutral_primitive_route_completion_passed")
        is True,
        neutral_primitive_route_completion.get("actual_current_surface_status"),
    )
    candidate_portfolio = certificates["oh_bridge_candidate_portfolio"]
    report(
        "oh-bridge-first-principles-candidate-portfolio-open",
        "first-principles O_H bridge positive-candidate portfolio"
        in str(candidate_portfolio.get("actual_current_surface_status"))
        and candidate_portfolio.get("proposal_allowed") is False
        and candidate_portfolio.get("candidate_portfolio_passed") is True
        and candidate_portfolio.get("candidate_count") == 5,
        candidate_portfolio.get("actual_current_surface_status"),
    )

    result = {
        "actual_current_surface_status": "open / assumption-import stress complete",
        "verdict": (
            "The refreshed PR #230 assumption exercise is explicit: H_unit, "
            "yt_ward_identity, observed top/y_t, alpha_LM/plaquette/u0, "
            "reduced cold pilots, undetermined c2, undetermined Z_match, and "
            "kappa_s = 1 are forbidden as proof shortcuts unless the relevant "
            "normalization or matching theorem is derived.  Canonical Z_h=1 "
            "does not derive the source operator overlap <0|O_s|h>, and source "
            "contact-term schemes do not derive the isolated pole residue.  A "
            "single finite source-shift radius also does not derive the zero-source "
            "Feynman-Hellmann derivative.  A C_sH source-Higgs cross-correlator "
            "is not hidden in the current harness or EW/Higgs notes; it remains "
            "an open observable/theorem.  Current EW gauge-mass algebra also "
            "does not realize a same-surface canonical-Higgs operator O_H or "
            "C_HH/C_sH pole residues.  H_unit likewise is not O_H without "
            "the same pole-purity and canonical-normalization certificates.  "
            "The source-Higgs default-off guard and finite-row instrumentation "
            "are not themselves C_sH/C_HH evidence.  "
            "The source-functional LSZ identifiability theorem keeps the same "
            "firewall active after granting an isolated source pole: source-only "
            "LSZ data do not identify the canonical-Higgs overlap or exclude "
            "orthogonal neutral top coupling.  "
            "Static EW W/Z algebra is not dM_W/ds, "
            "and slope-only W/Z outputs need production mass fits plus sector-"
            "overlap and canonical-Higgs identity certificates.  "
            "Outside-math tools are now included in the assumption firewall: "
            "they may be used only to emit future same-surface certificates, "
            "not as PSLQ, exact-value, or theorem-name proof selectors.  The "
            "invariant-ring O_H certificate attempt confirms this boundary: "
            "current neutral labels still admit a two-singlet completion and "
            "do not prove multiplicity one, write O_H, or fix kappa_s.  The "
            "GNS/source-Higgs flat-extension attempt confirms the same "
            "outside-math firewall at the moment-matrix level: source-only "
            "C_ss projections admit multiple PSD O_H extensions with different "
            "GNS ranks and overlaps until O_H/C_sH/C_HH rows exist.  The "
            "Burnside/double-commutant neutral irreducibility attempt confirms "
            "the same firewall at the neutral-generator level: the current "
            "source-only generator algebra is not full and has a non-scalar "
            "commutant until a same-surface off-diagonal neutral generator or "
            "primitive transfer exists.  The Schur A/B/C definition derivation "
            "attempt adds it for row-definition machinery: outside math can compute defined "
            "Schur rows but cannot supply the missing neutral kernel basis, "
            "source/orthogonal projector, or A/B/C labels from source-only "
            "denominator data.  The W/Z g2 bare-running bridge attempt adds "
            "the same firewall for electroweak running: structural bare g2 "
            "and beta-function formulas do not supply the same-source EW "
            "action, scale ratio, thresholds, finite matching, or strict g2 "
            "certificate.  The Carleman/Tauberian scalar-LSZ "
            "determinacy attempt adds the same firewall for moment theory: "
            "finite scalar shell/moment prefixes are not proof selectors until "
            "an infinite same-surface moment/asymptotic certificate exists.  The "
            "fresh artifact/literature review adds the same firewall for "
            "FMS/FH/finite-volume/operator-renormalization literature: it "
            "selects the O_H/C_sH/C_HH contract as the cleanest next target "
            "but does not write a current-surface O_H certificate or authorize "
            "closure.  The action-first O_H artifact attempt confirms the "
            "next premise: writing a standard EW/Higgs action is a hypothetical "
            "new surface unless the same-source action and canonical O_H are "
            "derived on PR230.  The PR541-style holonomic source-response "
            "gate adds the same boundary for creative-telescoping/tensor "
            "methods: they can compute defined Z(beta,s,h) rows only after "
            "a same-current-surface O_H/h-source artifact exists; they do "
            "not supply the missing operator/source by method name.  The "
            "derived rank-one bridge attempt adds the same boundary for the "
            "cleanest source-only theorem route: positivity preservation, "
            "reflection positivity, determinant positivity, labels, and "
            "conditional Perron support do not supply the missing same-surface "
            "primitive-cone/off-diagonal-generator certificate, canonical O_H, "
            "or C_sH/C_HH rows.  The source-sector pattern transfer gate adds "
            "the same boundary for the SU3-plaquette analogy: finite-source "
            "and SD/holonomic/tensor methods are relevant bridge-computation "
            "tools only after a same-surface O_H/h source, C_sH/C_HH rows, "
            "same-source W/Z rows, or a neutral rank-one theorem exists; "
            "the plaquette value or exponent shift is not a Yukawa input.  The "
            "determinant-positivity bridge intake adds the same boundary for "
            "the latest staggered-Wilson positivity theorem: positive fermion "
            "measure is useful support, but it is not a primitive neutral "
            "transfer, canonical O_H identity, source-Higgs row, or y_t value.  The "
            "reflection-plus-determinant primitive-upgrade gate makes the "
            "combined positivity shortcut explicit: OS/spectral positivity "
            "and positive fermion measure still admit a reducible neutral "
            "transfer with an orthogonal top-coupled scalar.  No current route "
            "certificate authorizes retained proposal wording.  The negative-route "
            "applicability review confirms these blockers apply only on their "
            "current surfaces and preserve future reopen paths through C_sH/C_HH, "
            "W/Z rows, Schur rows, neutral rank-one/irreducibility, scalar-LSZ "
            "pole control, or production evidence plus matching.  "
            "The taste-condensate O_H bridge audit adds the strongest existing "
            "Higgs/taste-stack shortcut to the firewall: the exact taste-axis "
            "Higgs operators are trace-zero shift directions, while the PR230 "
            "FH/LSZ source is the uniform additive mass source and has zero "
            "projection onto that taste-axis span.  That stack cannot be used "
            "as O_H authority until a source-coordinate transport certificate "
            "or C_sH/C_HH rows exist.  The origin/main composite-Higgs intake "
            "guard adds the same firewall for cross-lane stretch packets: a "
            "multi-channel Z3 composite-Higgs candidate with branch-local "
            "Z3/equal-condensate/strong-coupling premises is useful context, "
            "but it is not PR230 uniform-source transport, canonical O_H "
            "authority, or C_sH/C_HH pole-row evidence.  The Z3-triplet "
            "primitive-cone theorem adds exact conditional neutral-rank-one "
            "support for a lazy cyclic transfer, but the same-surface PR230 "
            "action/off-diagonal generator premise remains absent.  The H1 "
            "Z3 generation-action lift attempt shows that the current surface "
            "does not distinguish trivial from cyclic quark-bilinear Z3 action, "
            "so the origin/main H1 premise is still not derived.  The Z3 "
            "lazy-transfer promotion attempt makes the remaining neutral "
            "primitive gap explicit: the same-surface artifact supplies the "
            "cyclic symmetry P, and the lazy matrix L=(I+P)/2 is primitive as "
            "mathematics, but current PR230 artifacts do not instantiate L as "
            "physical dynamics.  The first-principles O_H bridge "
            "candidate portfolio keeps five positive candidates open while "
            "recording that no candidate currently supplies closure authority.  "
            "The source-coordinate, action-first, W/Z response, Schur, and "
            "neutral-primitive completion gates close only current shortcut "
            "surfaces: they require, respectively, a real source-axis "
            "transport certificate, a same-source EW/Higgs action plus O_H and "
            "C_sH/C_HH rows, production W/Z rows with strict g2/covariance/"
            "delta_perp, neutral-kernel A/B/C rows, or a primitive transfer/"
            "off-diagonal-generator theorem.  The two-source taste-radial chart "
            "certificate is the first positive source-chart support after the "
            "one-source no-go: it gives an exact orthonormal same-surface "
            "`I_8/sqrt(8), (S0+S1+S2)/sqrt(24)` chart, but it is a new second "
            "source axis and it does not identify that axis with canonical O_H.  "
            "The two-source taste-radial action certificate realizes that axis "
            "as a gauge-covariant blocked-hypercube harness source vertex, but "
            "it is still support only until measured C_sx/C_xx rows and a "
            "canonical O_H/source-overlap or physical-response bridge land.  "
            "The two-source taste-radial row-contract certificate removes the "
            "schema ambiguity by emitting explicit C_sx/C_xx aliases for that "
            "second source, but it is a finite smoke/schema contract only, not "
            "production rows or pole evidence.  The two-source taste-radial "
            "row-production manifest now gives exact no-resume chunk commands "
            "and a collision guard for those rows, but it is dry-run run control "
            "only until the chunks are actually run, combined, pole-tested, and "
            "bridged to canonical O_H or physical response.  "
            "The taste-radial canonical-O_H selector gate proves the degree-one "
            "radial axis is unique only after a degree-one Higgs-action premise "
            "is supplied; current Z3/trace/source filters leave a three-dimensional "
            "trace-zero invariant taste algebra.  The degree-one Higgs-action "
            "premise gate blocks the next shortcut too: degree-one filtering "
            "selects E1, but current PR230 artifacts do not authorize using "
            "degree as canonical O_H identity.  "
            "Positive closure still requires "
            "production evidence plus heavy matching, "
            "or an independent scalar pole/LSZ theorem."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Open scalar-LSZ and heavy-matching imports remain after assumption stress.",
        "checked_certificates": {
            name: cert.get("actual_current_surface_status") for name, cert in certificates.items()
        },
        "missing_forbidden_terms": missing_terms,
        "strict_non_claims": [
            "not a y_t derivation",
            "not a production measurement",
            "does not use observed top mass as calibration",
            "does not define y_t through H_unit matrix elements",
            "does not use yt_ward_identity as y_t authority",
            "does not set kappa_s to one without scalar LSZ/canonical normalization",
            "does not use source-only LSZ data as canonical-Higgs identity",
            "does not use outside-math value recognition as a proof selector",
            "does not use Burnside or double-commutant theorem names without same-surface neutral generators",
            "does not treat positivity preservation as a primitive neutral scalar rank-one bridge",
            "does not import SU3 source-sector constants or exponent shifts into y_t",
            "does not treat staggered-Wilson determinant positivity as source-Higgs overlap authority",
            "does not treat reflection plus determinant positivity as a primitive neutral bridge",
            "does not treat the Higgs/taste condensate stack as PR230 O_H authority",
            "does not treat cross-lane composite-Higgs stretch packets as PR230 O_H authority",
            "does not treat conditional Z3-triplet primitive-cone support as a PR230 primitive certificate",
            "does not treat Koide/lepton Z3 as a quark-bilinear generation-action certificate",
            "does not treat Z3 symmetry averaging or a mathematical lazy matrix as a PR230 physical transfer",
            "does not treat the two-source taste-radial chart as canonical O_H or as production source-Higgs rows",
            "does not treat the two-source taste-radial action source vertex as canonical O_H or measured C_sx/C_xx rows",
            "does not treat the two-source taste-radial row contract as production C_sx/C_xx rows or pole evidence",
            "does not treat the two-source taste-radial production manifest as row data or pole evidence",
            "does not treat degree-one taste-radial uniqueness as canonical O_H without a same-surface degree-one Higgs-action premise",
            "does not close future source-Higgs, W/Z, Schur, rank-one, scalar-LSZ, or production routes",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
