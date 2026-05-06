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
            "or C_sH/C_HH rows exist.  The first-principles O_H bridge "
            "candidate portfolio keeps five positive candidates open while "
            "recording that no candidate currently supplies closure authority.  "
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
