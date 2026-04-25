# Reproduce Guide

Run these from the repo root on the checked-out public package state.

This file is the quickest route to validating the active package. For claim
boundaries, pair it with [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md).
For domain routing, pair it with [SCIENCE_MAP.md](./SCIENCE_MAP.md). For the
exact validated runtime, use [RELEASE_ENVIRONMENT.md](./RELEASE_ENVIRONMENT.md).

## Pinned Environment

The public validation surface is pinned to:

- Python `3.13.5`
- `numpy==2.4.4`
- `scipy==1.17.1`

Install with:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-release.txt
```

## Fastest Validation Paths

Choose the slice that matches what you are trying to check.

### Manuscript-core retained backbone

```bash
python3 scripts/frontier_self_consistent_field_equation.py
python3 scripts/frontier_poisson_exhaustive_uniqueness.py
python3 scripts/frontier_newton_derived.py
python3 scripts/frontier_universal_gr_discrete_global_closure.py
python3 scripts/frontier_universal_qg_canonical_textbook_continuum_gr_closure.py
python3 scripts/frontier_non_abelian_gauge.py
python3 scripts/frontier_graph_first_su3_integration.py
python3 scripts/frontier_anomaly_forces_time.py
python3 scripts/frontier_chronology_operational_no_past_signaling.py
python3 scripts/frontier_sm_hypercharge_uniqueness.py
python3 scripts/frontier_fractional_charge_denominator_from_n_c.py
python3 scripts/frontier_su2_witten_z2_anomaly.py
python3 scripts/frontier_su3_cubic_anomaly_cancellation.py
python3 scripts/frontier_bminusl_anomaly_freedom.py
python3 scripts/frontier_three_generation_observable_theorem.py
python3 scripts/frontier_strong_cp_theta_zero.py
python3 scripts/frontier_universal_theta_induced_edm_vanishing.py
python3 scripts/frontier_lorentz_kernel_positive_closure.py
```

### Manuscript-core quantitative package

```bash
python3 scripts/frontier_hierarchy_observable_principle_from_axiom.py
python3 scripts/frontier_complete_prediction_chain.py
python3 scripts/frontier_alpha_lm_geometric_mean_identity.py
python3 scripts/frontier_yt_ward_identity_derivation.py
python3 scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py
python3 scripts/frontier_higgs_mass_full_3loop.py
python3 scripts/frontier_ckm_atlas_axiom_closure.py
python3 scripts/frontier_wolfenstein_lambda_a_structural_identities.py
python3 scripts/frontier_ckm_cp_phase_structural_identity.py
python3 scripts/frontier_ckm_atlas_triangle_right_angle.py
python3 scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py
python3 scripts/frontier_ckm_sin_2_beta_bar_nlo_n_quark_ratio.py
python3 scripts/frontier_ckm_barred_triangle_pythagorean_rho_lambda_sum_rule.py
python3 scripts/frontier_ckm_barred_apex_angle_exact_closed_form.py
python3 scripts/frontier_ckm_barred_circumradius_exact_closed_form.py
python3 scripts/frontier_ckm_jarlskog_exact_nlo_closed_form.py
python3 scripts/frontier_ckm_first_row_magnitudes.py
python3 scripts/frontier_ckm_second_row_magnitudes.py
python3 scripts/frontier_ckm_third_row_magnitudes.py
python3 scripts/frontier_ckm_bs_mixing_phase_derivation.py
python3 scripts/frontier_ckm_thales_cross_system_cp_ratio.py
python3 scripts/frontier_ckm_cp_product_alpha_s_cross_sector_extraction.py
python3 scripts/frontier_ckm_kaon_epsilon_k_jarlskog_decomposition.py
python3 scripts/frontier_ckm_neutron_edm_bound.py
```

### Manuscript-surface dark-matter package

```bash
python3 scripts/frontier_dm_leptogenesis_transport_status.py
python3 scripts/frontier_dm_abcc_retained_measurement_closure_2026_04_21.py
python3 scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py
```

### Open and support lanes

```bash
python3 scripts/frontier_koide_reviewer_stress_test.py
python3 scripts/frontier_koide_lane_regression.py
python3 scripts/frontier_koide_native_zero_section_nature_review.py
python3 scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py
python3 scripts/frontier_koide_q_delta_readout_retention_split_no_go.py
python3 scripts/frontier_koide_delta_marked_relative_cobordism_no_go.py
python3 scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py
python3 scripts/frontier_koide_pointed_origin_exhaustion_theorem.py
python3 scripts/frontier_koide_dimensionless_objection_closure_review.py
python3 scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py
python3 scripts/frontier_koide_q_background_zero_z_erasure_criterion.py
python3 scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py
python3 scripts/frontier_cross_sector_a_squared_koide_vcb_bridge.py
python3 scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py
python3 scripts/frontier_ckm_n9_structural_family_koide_bridge.py
python3 scripts/frontier_ckm_cubic_bernoulli_koide_bridge.py
python3 scripts/frontier_ckm_egyptian_bernoulli_closures_koide_bridge.py
python3 scripts/frontier_ckm_consecutive_primes_s3_koide_bridge.py
python3 scripts/frontier_framework_bare_alpha_3_alpha_em_dimension_fixed_ratio.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_planck_scale_program_audit.py
python3 scripts/frontier_planck_conditional_completion_audit.py
python3 scripts/frontier_planck_boundary_density_extension.py
python3 scripts/frontier_planck_finite_response_nogo.py
python3 scripts/frontier_planck_parent_source_hidden_character_nogo.py
python3 scripts/frontier_area_law_quarter_broader_no_go.py
python3 scripts/frontier_area_law_multipocket_selector_no_go.py
python3 scripts/frontier_area_law_primitive_edge_entropy_selector_no_go.py
python3 scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py
python3 scripts/frontier_area_law_primitive_parity_gate_carrier.py
python3 scripts/frontier_area_law_primitive_car_edge_identification.py
python3 scripts/frontier_area_law_native_car_semantics_tightening.py
python3 scripts/frontier_planck_target3_phase_unit_edge_statistics.py
python3 scripts/frontier_planck_target3_clifford_phase_bridge.py
python3 scripts/frontier_neutrino_retained_observable_bounds.py
python3 scripts/frontier_r_base_group_theory_derivation.py
python3 scripts/frontier_cosmology_frw_kinematic_reduction.py
python3 scripts/frontier_matter_radiation_equality_structural_identity.py
python3 scripts/frontier_n_eff_from_three_generations.py
python3 scripts/frontier_graviton_spectral_tower.py
python3 scripts/frontier_vector_gauge_field_kk_tower.py
python3 scripts/frontier_scalar_harmonic_tower.py
python3 scripts/frontier_gravity_cosmology_tower_lambda_spectral_bridge.py
```

## How To Read The Output

- use the note paired with each runner as the claim boundary
- use [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) to see
  which derivation note and release artifact each runner supports
- use [RESULTS_INDEX.md](./RESULTS_INDEX.md) when you want the canonical
  note/runner path for a specific lane
- do not elevate bounded or support lanes from raw stdout alone
- treat the first three validation blocks above as the release-grade public
  validation path; treat the open/support block as package context rather than
  manuscript-core validation

Historical runner-name caveats:

- `frontier_born_rule_derived.py` supports the retained `I_3 = 0` theorem, not
  a standalone full Born-rule derivation
- `frontier_cpt_exact.py` is an exact theorem runner on even periodic lattices
  only
- `frontier_newton_derived.py` supports the retained weak-field Newton/Poisson
  claim, not the full gravity/QG chain
- `frontier_anomaly_forces_time.py` mixes computed checks with labeled
  assertions; use the theorem note as the safe claim boundary

## Logs and Release Artifacts

- archive raw stdout logs per runner under `logs/` or `outputs/`
- archive retained logs under `logs/retained/`
- store figure-prep data under `outputs/figures/`
- keep the release status ledger aligned with the package labels:
  `retained`, `bounded`, or `open`

Before release:

- use the pinned environment above
- pin the exact commit hash
- confirm that the manuscript, claims table, inputs/qualifiers note, and
  non-claims note agree on the released package boundary

## Archival Freeze

The existing freeze note is an archival selective freeze, not the current
package authority surface:

- [REPRODUCIBILITY_FREEZE_2026-04-14.md](./REPRODUCIBILITY_FREEZE_2026-04-14.md)

Use it for provenance only.
