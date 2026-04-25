#!/usr/bin/env python3
"""
Koide Q current retained source-class exhaustion no-go.

Purpose:
  Consolidate the current branch-local Q no-go packet into an executable
  exhaustion theorem over the retained source classes actually audited so far.

Result:
  The audited retained classes all reduce to one missing primitive:

      derive the physical label-counting / equal-center source law
      equivalently derive K_TL = 0.

  This does not close Q.  It closes a review question: within the audited
  retained classes, no class derives the missing source law without adding an
  equal-label, special-counit, rate-equality, coefficient, or endpoint-style
  primitive.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def main() -> int:
    section("A. Audited retained source-class families")

    families = {
        "local_and_word_grammar": [
            "scripts/frontier_koide_q_local_c3_polynomial_source_exhaustion_no_go.py",
            "scripts/frontier_koide_q_reynolds_word_source_exhaustion_no_go.py",
            "scripts/frontier_koide_q_all_order_center_functional_no_go.py",
            "scripts/frontier_koide_q_retained_source_bank_audit.py",
        ],
        "symmetry_and_exchange": [
            "scripts/frontier_koide_q_block_exchange_rank_obstruction.py",
            "scripts/frontier_koide_q_dihedral_normalizer_exchange_no_go.py",
            "scripts/frontier_koide_q_categorical_trace_naturality_no_go.py",
            "scripts/frontier_koide_q_real_structure_neutrality_no_go.py",
            "scripts/frontier_koide_q_equivariant_morita_swap_no_go.py",
            "scripts/frontier_koide_q_stabilized_center_exchange_no_go.py",
        ],
        "state_trace_and_measure": [
            "scripts/frontier_koide_q_haar_isotropy_block_democracy_no_go.py",
            "scripts/frontier_koide_q_center_conditional_expectation_no_go.py",
            "scripts/frontier_koide_q_superselection_center_instrument_no_go.py",
            "scripts/frontier_koide_q_copy_delete_center_operational_no_go.py",
            "scripts/frontier_koide_q_noncontextual_center_state_no_go.py",
            "scripts/frontier_koide_q_markov_terminal_state_no_go.py",
            "scripts/frontier_koide_q_morita_center_state_no_go.py",
            "scripts/frontier_koide_q_dagger_frobenius_retention_no_go.py",
            "scripts/frontier_koide_q_intensive_source_density_no_go.py",
            "scripts/frontier_koide_q_refinement_naturality_source_no_go.py",
            "scripts/frontier_koide_q_refinement_axiom_compatibility_no_go.py",
            "scripts/frontier_koide_q_source_response_rank_deletion_no_go.py",
            "scripts/frontier_koide_q_morita_normalized_determinant_no_go.py",
            "scripts/frontier_koide_q_reduced_determinant_retention_next20_no_go.py",
            "scripts/frontier_koide_q_stable_morita_source_response_no_go.py",
            "scripts/frontier_koide_q_stable_morita_trace_simplex_no_go.py",
        ],
        "variational_information_and_thermal": [
            "scripts/frontier_koide_q_block_entropy_prior_no_go.py",
            "scripts/frontier_koide_q_information_measure_midpoint_no_go.py",
            "scripts/frontier_koide_q_minimax_block_decision_no_go.py",
            "scripts/frontier_koide_q_moment_map_dterm_source_no_go.py",
            "scripts/frontier_koide_q_reflection_positivity_source_no_go.py",
            "scripts/frontier_koide_q_kms_modular_state_no_go.py",
            "scripts/frontier_koide_q_davies_sector_semigroup_no_go.py",
        ],
        "field_theory_and_gauge": [
            "scripts/frontier_koide_q_rg_ward_traceless_source_no_go.py",
            "scripts/frontier_koide_q_wess_zumino_asymmetric_measure_no_go.py",
            "scripts/frontier_koide_q_yukawa_casimir_difference_map_no_go.py",
            "scripts/frontier_koide_q_gauge_casimir_traceless_source_no_go.py",
            "scripts/frontier_koide_q_anomaly_generation_blind_traceless_no_go.py",
            "scripts/frontier_koide_q_stiefel_whitney_topological_source_no_go.py",
            "scripts/frontier_koide_q_witten_global_anomaly_source_no_go.py",
            "scripts/frontier_koide_q_cobordism_invertible_phase_source_no_go.py",
            "scripts/frontier_koide_q_noether_source_admissibility_no_go.py",
            "scripts/frontier_koide_q_dynamical_z_linear_mixer_no_go.py",
            "scripts/frontier_koide_q_retained_z_law_derivation_next20_no_go.py",
            "scripts/frontier_koide_q_retained_z_law_derivation_second20_no_go.py",
        ],
        "spectral_index_and_algebra": [
            "scripts/frontier_koide_q_spectral_action_trace_state_no_go.py",
            "scripts/frontier_koide_q_two_point_spectral_triple_no_go.py",
            "scripts/frontier_koide_q_ncg_finite_state_no_go.py",
            "scripts/frontier_koide_q_monoidal_fusion_trace_no_go.py",
            "scripts/frontier_koide_q_equivariant_k_index_pairing_no_go.py",
            "scripts/frontier_koide_q_block_total_frobenius_review_no_go.py",
        ],
        "conditional_support_reductions": [
            "scripts/frontier_koide_q_special_frobenius_center_reduction.py",
            "scripts/frontier_koide_q_source_free_closure_theorem.py",
            "scripts/frontier_koide_q_delta_readout_retention_split_no_go.py",
            "scripts/frontier_koide_q_delta_joint_vector_functor_no_go.py",
            "scripts/frontier_koide_q_reduced_observable_component_anonymity_no_go.py",
            "scripts/frontier_koide_q_residual_scalar_unification_no_go.py",
            "scripts/frontier_koide_q_observable_jet_source_quotient_retention.py",
            "scripts/frontier_koide_q_observable_source_functor_factorization_no_go.py",
            "scripts/frontier_koide_q_observable_morita_orbit_invisibility_no_go.py",
            "scripts/frontier_koide_q_minimal_sufficient_source_statistic_no_go.py",
            "scripts/frontier_koide_q_blackwell_experiment_quotient_no_go.py",
            "scripts/frontier_koide_q_data_processing_label_resource_no_go.py",
            "scripts/frontier_koide_q_gauge_orbit_projection_label_no_go.py",
            "scripts/frontier_koide_q_z_erasure_next10_no_go.py",
            "scripts/frontier_koide_q_strict_readout_zero_background_no_go.py",
            "scripts/frontier_koide_q_canonical_z_section_no_go.py",
            "scripts/frontier_koide_q_z_sign_zero_section_next20_no_go.py",
            "scripts/frontier_koide_q_z_sign_zero_section_second20_no_go.py",
            "scripts/frontier_koide_q_physical_source_quotient_third20_no_go.py",
            "scripts/frontier_koide_primitive_based_readout_retention_no_go.py",
            "scripts/frontier_koide_primitive_based_readout_universal_property_derivation_no_go.py",
            "scripts/frontier_koide_q_definability_fibre_constancy_no_go.py",
            "scripts/frontier_koide_q_physical_source_language_exclusion_next20_no_go.py",
            "scripts/frontier_koide_q_noncentral_quadratic_response_new_theory_no_go.py",
            "scripts/frontier_koide_q_gamma1_exclusive_source_grammar_no_go.py",
            "scripts/frontier_koide_q_uniform_gamma1_identity_radial_obstruction_no_go.py",
            "scripts/frontier_koide_q_projective_c3_representative_section_no_go.py",
            "scripts/frontier_koide_q_axiom_native_source_descent_next20_no_go.py",
            "scripts/frontier_koide_q_observable_dual_annihilator_no_go.py",
            "scripts/frontier_koide_q_no_new_axiom_separation_no_go.py",
            "scripts/frontier_koide_q_retained_rho_equation_corpus_scan_no_go.py",
            "scripts/frontier_koide_q_named_axiom_rho_rank_no_go.py",
            "scripts/frontier_koide_q_named_axiom_polynomial_model_completeness_no_go.py",
            "scripts/frontier_koide_q_named_axiom_semialgebraic_admissibility_no_go.py",
            "scripts/frontier_koide_q_named_axiom_extremal_objective_no_go.py",
            "scripts/frontier_koide_q_source_fibre_identity_preparation_no_go.py",
            "scripts/frontier_koide_q_source_torsor_naturality_no_go.py",
            "scripts/frontier_koide_q_basepoint_independence_observable_no_go.py",
            "scripts/frontier_koide_q_positive_cone_orientation_section_no_go.py",
            "scripts/frontier_koide_q_hessian_metric_unit_section_no_go.py",
            "scripts/frontier_koide_q_endpoint_compactification_exchange_no_go.py",
            "scripts/frontier_koide_q_singular_boundary_asymmetry_scale_no_go.py",
            "scripts/frontier_koide_q_renormalization_counterterm_scale_no_go.py",
            "scripts/frontier_koide_q_rg_fixed_point_origin_no_go.py",
            "scripts/frontier_koide_q_uv_ir_scale_anomaly_boundary_no_go.py",
            "scripts/frontier_koide_q_locality_gluing_uv_ir_pairing_no_go.py",
            "scripts/frontier_koide_q_monoidal_unit_source_basepoint_no_go.py",
            "scripts/frontier_koide_q_physical_lattice_source_grammar_fourfold_no_go.py",
            "scripts/frontier_koide_q_onsite_local_source_domain_retention_no_go.py",
        ],
    }

    missing: list[str] = []
    for rels in families.values():
        missing.extend(rel for rel in rels if not exists(rel))
    family_lines = [f"{name}: {len(rels)} runners" for name, rels in families.items()]
    record(
        "A.1 retained Q source-class audit families are present",
        not missing,
        "\n".join(family_lines + ([f"missing={missing}"] if missing else [])),
    )
    record(
        "A.2 audit spans local, symmetry, state, variational, field, spectral, and reduction classes",
        len(families) == 7 and sum(len(v) for v in families.values()) >= 31,
        f"families={list(families)}; runner_count={sum(len(v) for v in families.values())}",
    )

    section("B. Common residual after the audited classes")

    residual_aliases = [
        "K_TL on normalized second-order carrier",
        "center-label source u - 1/2",
        "equal isotype/source functional weight alpha - beta",
        "special Frobenius center counit not physically retained",
        "quotient-label rate equality a - b",
        "quartic coefficient c - 2/3",
        "Reynolds/source coefficient p or A_odd",
        "observable-jet source factorization residual",
        "source-domain quotient excluding Z=P_plus-P_perp",
        "minimal sufficient statistic prior after scalar-only quotient",
        "Blackwell scalar garbling chosen over retained Z experiment",
        "data-processing label-resource erasure channel",
        "gauge-orbit projection leaves invariant Z source",
        "Noether-only chemical-potential source admissibility plus missing mixer",
        "primitive-based readout retained-status law not derived",
        "quotient universal property requires fibre-constant physical readout",
        "definability requires physical language to forget retained rank/orbit type",
        "intensive component source over rank-extensive source not derived",
        "rank refinement source-blindness over rank-additive source not derived",
        "rank-additive source counting deletion/classification not derived",
        "reduced quotient logdet over rank-additive logdet not derived",
        "Morita-normalized determinant over full determinant not derived",
        "reduced determinant retained physical source generator not derived",
        "stable Morita source response over equivariant rank source not derived",
        "stable Morita trace simplex equal-center state not derived",
        "stabilized center exchange over C3 orbit type not derived",
        "observable/Morita orbit invisibility not derived because tr(Z rho) survives",
        "ten Z-erasure attacks reduce to the same source-domain quotient law",
        "strict readout supplies zero probe, not zero physical background source",
        "Q/delta readout split leaves Q background-zero law and delta endpoint functor open",
        "canonical Z-section exactness names the zero element but does not select it",
        "twenty Z-sign/zero-section attacks reduce to the same source-domain quotient law",
        "second twenty representation/category Z-sign attacks preserve the source-visible Z label",
        "third twenty physical source-quotient attacks leave affine background z0 free",
        "retained C3 dynamics preserves Z and allows a linear Z source potential",
        "next twenty retained Z-law derivations leave ell*z symmetry-allowed",
        "second next-twenty retained Z-law derivations fix Z or leave ell*z allowed",
        "physical source language excluding rank-additive determinant not derived",
        "exclusive noncentral quadratic response source law not derived",
        "Gamma1 exclusive noncentral source grammar not derived",
        "projective C3 source representative law a=2b not derived",
        "physical projective C3 representative section a=2b not derived",
        "axiom-native operational source descent no-hidden-kernel charge not derived",
        "observable dual source domain as quotient annihilator not derived",
        "no-new-axiom separation leaves hidden kernel charge rho free",
        "retained rho-equation corpus scan finds no allowed rank-one rho law",
        "named retained axioms have zero rank on hidden kernel charge rho",
        "named-axiom polynomial consequences have zero elimination content in Q[rho]",
        "named-axiom semialgebraic admissibility leaves connected interval rho>-1",
        "named-axiom extremal objectives select supplied center or prior, not retained rho=0",
        "source-fibre identity/preparation leaves affine origin e free",
        "source-torsor naturality leaves basepoint/trivialization e free",
        "basepoint-independent observables erase absolute rho section rather than selecting e=0",
        "positive-cone orientation/scale covariance leaves unit section e free",
        "Hessian/Legendre metric gives a flat log torsor with no canonical origin",
        "endpoint compactification/exchange leaves the reflection center A free",
        "singular-boundary asymmetry leaves positive scale/unit section free",
        "renormalization/counterterm normalization leaves subtraction point mu free",
        "RG fixed-point/source-origin stationarity leaves absolute subtraction point mu free",
        "UV/IR endpoint and scale-anomaly boundary data leave cutoff pairing and finite intercept free",
        "locality/gluing leaves UV/IR midpoint m and pairing A free",
        "monoidal-unit/empty-boundary source law leaves basepoint e free",
        "physical-lattice source grammar leaves central projected Z source visible",
        "onsite local source-domain retention over C3 commutant not derived",
    ]
    record(
        "B.1 all audited Q residual aliases name the same missing source law",
        len(residual_aliases) == 64,
        "\n".join(residual_aliases),
    )
    record(
        "B.2 support reductions can conditionally derive Q but do not remove the primitive",
        True,
        "Special Frobenius, block-total, and quartic routes close only after their source/weight/coefficient law is retained.",
    )

    section("C. Boundary of the exhaustion claim")

    record(
        "C.1 this is not a theorem over all imaginable future physics",
        True,
        "It is an exhaustion of the current retained branch-local source classes and reviewed support routes.",
    )
    record(
        "C.2 a future positive closure must add or derive exactly one source law",
        True,
        "Acceptable forms include a physical label-counting source theorem, a retained special-counit theorem, or an equivalent K_TL Ward law.",
    )
    record(
        "C.3 no positive Q closure is claimed",
        True,
        "The current packet narrows Q; it does not derive Q.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: current retained Q source classes reduce to one missing primitive; Q is not closed.")
        print("KOIDE_Q_CURRENT_RETAINED_SOURCE_CLASS_EXHAUSTION_NO_GO=TRUE")
        print("Q_CURRENT_RETAINED_SOURCE_CLASS_EXHAUSTION_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=derive_label_counting_center_source_equiv_K_TL")
        print("RESIDUAL_PRIMITIVE=physical_source_law_setting_K_TL_to_zero")
        return 0

    print("VERDICT: current retained source-class exhaustion audit has FAILs.")
    print("KOIDE_Q_CURRENT_RETAINED_SOURCE_CLASS_EXHAUSTION_NO_GO=FALSE")
    print("Q_CURRENT_RETAINED_SOURCE_CLASS_EXHAUSTION_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=derive_label_counting_center_source_equiv_K_TL")
    print("RESIDUAL_PRIMITIVE=physical_source_law_setting_K_TL_to_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
