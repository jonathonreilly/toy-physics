# Audit Queue

**Generated:** 2026-05-03T11:04:10.695343+00:00
**Total pending:** 490
**Ready (all deps already at retained-grade or metadata tiers):** 18

By criticality:
- `critical`: 25
- `high`: 215
- `medium`: 155
- `leaf`: 95

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 244 | 16.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 2 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 238 | 28.90 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 3 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 131 | 15.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 4 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 130 | 15.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 5 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 126 | 14.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 6 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 124 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 7 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 118 | 28.89 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 8 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 117 | 28.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 9 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 116 | 20.87 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 10 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 110 | 22.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 11 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 104 | 23.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 12 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 96 | 19.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 13 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 87 | 14.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 14 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 86 | 14.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 15 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 85 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 16 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 85 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 17 | `ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 84 | 14.41 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `ckm_atlas_axiom_closure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 77 | 17.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 19 | `down_type_mass_ratio_ckm_dual_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 61 | 13.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 20 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 57 | 14.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 21 | `cosmological_constant_spectral_gap_identity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 15.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmological_constant_spectral_gap_identity.py` |
| 22 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 14.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 23 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 43 | 12.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 24 | `n_eff_from_three_generations_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 42 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_n_eff_from_three_generations.py` |
| 25 | `matter_radiation_equality_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 42 | 12.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_matter_radiation_equality_structural_identity.py` |
| 26 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 27 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 28 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 29 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 30 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | high | 174 | 8.95 | Y | fresh_context_or_stronger | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 31 | `pmns_selector_unique_amplitude_slot_note` | decoration | claim_type_backfill_reaudit | high | 112 | 9.32 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_selector_unique_amplitude_slot.py` |
| 32 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | high | 112 | 8.82 | Y | fresh_context_or_stronger | `scripts/frontier_g_bare_derivation.py` |
| 33 | `ew_current_matching_rule_open_gate_note_2026-05-03` | open_gate | unaudited | high | 111 | 7.31 | Y | fresh_context_or_stronger | - |
| 34 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 63 | 12.00 | Y | fresh_context_or_stronger | - |
| 35 | `universal_theta_induced_edm_vanishing_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 54 | 11.28 | Y | fresh_context_or_stronger | `scripts/frontier_universal_theta_induced_edm_vanishing.py` |
| 36 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | high | 53 | 8.76 | Y | fresh_context_or_stronger | `scripts/frontier_yt_qfp_insensitivity.py` |
| 37 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | high | 44 | 11.49 | Y | fresh_context_or_stronger | `scripts/frontier_taste_scalar_isotropy.py` |
| 38 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 37 | 7.75 | Y | fresh_context_or_stronger | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 39 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | high | 247 | 10.95 |  | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 40 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | high | 246 | 8.95 |  | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 41 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | high | 245 | 10.44 |  | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 42 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | high | 239 | 8.41 |  | fresh_context_or_stronger | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 43 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | high | 184 | 10.03 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 44 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | high | 183 | 10.52 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 45 | `neutrino_majorana_pfaffian_extension_note` | positive_theorem | unaudited | high | 182 | 10.02 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |
| 46 | `neutrino_majorana_pfaffian_axiom_boundary_note` | no_go | unaudited | high | 181 | 8.01 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py` |
| 47 | `neutrino_majorana_pfaffian_no_forcing_theorem_note` | positive_theorem | unaudited | high | 180 | 10.50 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py` |
| 48 | `neutrino_majorana_current_atlas_nonrealization_note` | positive_theorem | unaudited | high | 180 | 9.00 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py` |
| 49 | `neutrino_majorana_charge_two_primitive_reduction_note` | positive_theorem | unaudited | high | 179 | 8.99 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` |
| 50 | `neutrino_majorana_unique_source_slot_note` | positive_theorem | unaudited | high | 178 | 10.98 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_unique_source_slot.py` |

Full queue lives in `data/audit_queue.json`.
