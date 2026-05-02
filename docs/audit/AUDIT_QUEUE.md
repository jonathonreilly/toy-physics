# Audit Queue

**Generated:** 2026-05-02T18:41:52.337461+00:00
**Total pending:** 590
**Ready (all deps already at retained-grade or metadata tiers):** 113

By criticality:
- `critical`: 33
- `high`: 231
- `medium`: 170
- `leaf`: 156

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `three_generation_structure_note` | positive_theorem | unaudited | critical | 248 | 20.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 2 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 183 | 26.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 3 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 60 | 13.93 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 4 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 5 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 46 | 14.05 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 6 | `one_generation_matter_closure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 259 | 21.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 7 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 244 | 16.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 8 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 238 | 28.90 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 9 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 132 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 10 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 131 | 15.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 11 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 130 | 15.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 12 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 126 | 14.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 13 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 124 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 14 | `three_generation_observable_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 123 | 20.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 15 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 118 | 28.89 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 16 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 117 | 28.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 17 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 116 | 20.87 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 18 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 113 | 14.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 19 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 110 | 22.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 20 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 104 | 23.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 21 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 96 | 19.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 22 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 87 | 14.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 23 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 86 | 14.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 24 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 85 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 25 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 85 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 26 | `ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 84 | 14.41 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `ckm_atlas_axiom_closure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 77 | 17.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 28 | `down_type_mass_ratio_ckm_dual_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 61 | 13.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 29 | `cosmological_constant_spectral_gap_identity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 15.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmological_constant_spectral_gap_identity.py` |
| 30 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 14.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 31 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 43 | 12.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 32 | `n_eff_from_three_generations_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 42 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_n_eff_from_three_generations.py` |
| 33 | `matter_radiation_equality_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 42 | 12.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_matter_radiation_equality_structural_identity.py` |
| 34 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 35 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 36 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 37 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 38 | `alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | high | 240 | 9.91 | Y | fresh_context_or_stronger | `scripts/frontier_alpha_s_direct_wilson_loop.py` |
| 39 | `yt_color_projection_correction_note` | positive_theorem | unaudited | high | 175 | 11.46 | Y | fresh_context_or_stronger | `scripts/frontier_yt_color_projection_correction.py` |
| 40 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | high | 174 | 8.95 | Y | fresh_context_or_stronger | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 41 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | high | 134 | 13.58 | Y | fresh_context_or_stronger | - |
| 42 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | high | 124 | 8.97 | Y | fresh_context_or_stronger | `scripts/frontier_generation_axiom_boundary.py` |
| 43 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 119 | 13.41 | Y | fresh_context_or_stronger | - |
| 44 | `yukawa_color_projection_theorem` | positive_theorem | unaudited | high | 119 | 11.41 | Y | fresh_context_or_stronger | `scripts/frontier_ew_current_fierz_channel_decomposition.py` |
| 45 | `pmns_selector_unique_amplitude_slot_note` | decoration | claim_type_backfill_reaudit | high | 112 | 9.32 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_selector_unique_amplitude_slot.py` |
| 46 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | high | 112 | 8.82 | Y | fresh_context_or_stronger | `scripts/frontier_g_bare_derivation.py` |
| 47 | `koide_dweh_cyclic_compression_note_2026-04-18` | positive_theorem | unaudited | high | 77 | 8.79 | Y | fresh_context_or_stronger | `scripts/frontier_koide_dweh_cyclic_compression.py` |
| 48 | `koide_axiom_native_support_batch_note_2026-04-22` | bounded_theorem | unaudited | high | 69 | 8.63 | Y | fresh_context_or_stronger | - |
| 49 | `complex_action_note` | bounded_theorem | unaudited | high | 57 | 8.36 | Y | fresh_context_or_stronger | `scripts/complex_action_harness.py` |
| 50 | `lensing_k_sweep_note` | bounded_theorem | unaudited | high | 57 | 8.36 | Y | fresh_context_or_stronger | `scripts/lensing_k_sweep.py` |

Full queue lives in `data/audit_queue.json`.
