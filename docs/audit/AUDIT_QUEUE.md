# Audit Queue

**Generated:** 2026-05-03T10:45:17.886489+00:00
**Total pending:** 494
**Ready (all deps already at retained-grade or metadata tiers):** 20

By criticality:
- `critical`: 37
- `high`: 209
- `medium`: 153
- `leaf`: 95

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | positive_theorem | unaudited | critical | 255 | 11.50 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 2 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | bounded_theorem | unaudited | critical | 254 | 10.99 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 3 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 252 | 10.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 4 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 252 | 10.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 5 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 252 | 10.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 6 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 252 | 10.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 7 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 252 | 10.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 8 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 9 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 254 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 10 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 253 | 8.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 11 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 252 | 10.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 12 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 251 | 16.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 13 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 247 | 28.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 14 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 214 | 24.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 15 | `yt_ward_identity_derivation_theorem` | open_gate | unaudited | critical | 183 | 26.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 16 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 132 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 17 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 131 | 15.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 18 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 130 | 15.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 19 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 126 | 14.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 20 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 124 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 21 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 118 | 28.89 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 22 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 117 | 28.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 23 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 116 | 20.87 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 24 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 104 | 23.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 25 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 96 | 19.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 26 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 87 | 14.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 27 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 86 | 14.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 28 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 85 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 29 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 85 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 30 | `ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 84 | 14.41 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `ckm_atlas_axiom_closure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 77 | 17.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 32 | `down_type_mass_ratio_ckm_dual_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 61 | 13.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 33 | `cosmological_constant_spectral_gap_identity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 15.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmological_constant_spectral_gap_identity.py` |
| 34 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 14.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 35 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 43 | 12.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 36 | `n_eff_from_three_generations_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 42 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_n_eff_from_three_generations.py` |
| 37 | `matter_radiation_equality_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 42 | 12.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_matter_radiation_equality_structural_identity.py` |
| 38 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | high | 184 | 9.03 | Y | fresh_context_or_stronger | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 39 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 119 | 13.41 | Y | fresh_context_or_stronger | - |
| 40 | `pmns_selector_unique_amplitude_slot_note` | decoration | claim_type_backfill_reaudit | high | 112 | 9.32 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_selector_unique_amplitude_slot.py` |
| 41 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | high | 112 | 8.82 | Y | fresh_context_or_stronger | `scripts/frontier_g_bare_derivation.py` |
| 42 | `universal_theta_induced_edm_vanishing_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 54 | 11.28 | Y | fresh_context_or_stronger | `scripts/frontier_universal_theta_induced_edm_vanishing.py` |
| 43 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | high | 53 | 8.76 | Y | fresh_context_or_stronger | `scripts/frontier_yt_qfp_insensitivity.py` |
| 44 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | high | 44 | 11.49 | Y | fresh_context_or_stronger | `scripts/frontier_taste_scalar_isotropy.py` |
| 45 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 37 | 7.75 | Y | fresh_context_or_stronger | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 46 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | high | 248 | 8.46 |  | fresh_context_or_stronger | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 47 | `ew_current_matching_ozi_suppression_theorem_note_2026-04-27` | bounded_theorem | unaudited | high | 215 | 8.76 |  | fresh_context_or_stronger | `scripts/frontier_color_projection_mc.py` |
| 48 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | high | 184 | 10.03 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 49 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | high | 183 | 10.52 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 50 | `yt_zero_import_authority_note` | positive_theorem | unaudited | high | 183 | 10.52 |  | fresh_context_or_stronger | `scripts/frontier_yt_ward_identity_derivation.py` |

Full queue lives in `data/audit_queue.json`.
