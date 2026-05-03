# Audit Queue

**Generated:** 2026-05-03T11:31:07.135388+00:00
**Total pending:** 700
**Ready (all deps already at retained-grade or metadata tiers):** 89

By criticality:
- `critical`: 38
- `high`: 234
- `medium`: 269
- `leaf`: 159

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | - | unaudited | critical | 255 | 15.50 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 2 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | - | unaudited | critical | 254 | 14.99 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 3 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | - | unaudited | critical | 252 | 14.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 4 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 252 | 14.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 5 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 252 | 14.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 6 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 252 | 14.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 7 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 252 | 14.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 8 | `s3_general_r_derivation_note` | - | unaudited | critical | 64 | 18.02 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 61 | 17.45 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 10 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 254 | 14.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 11 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 253 | 12.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 12 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 252 | 14.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 13 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 251 | 20.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 14 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 245 | 32.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 15 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 139 | 20.63 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 16 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 138 | 19.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 17 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 137 | 19.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 18 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 133 | 19.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 19 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 131 | 20.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 20 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 125 | 32.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 21 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 124 | 32.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 22 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 123 | 24.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 23 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 117 | 26.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 24 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 111 | 27.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 25 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 103 | 23.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 26 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 94 | 19.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 27 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 93 | 18.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 28 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 92 | 18.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 29 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 92 | 18.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 30 | `ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 91 | 18.52 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `ckm_atlas_axiom_closure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 84 | 21.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 32 | `gate_b_farfield_note` | - | unaudited | critical | 81 | 18.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_farfield_harness.py` |
| 33 | `down_type_mass_ratio_ckm_dual_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 68 | 17.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 34 | `cosmological_constant_spectral_gap_identity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 58 | 19.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmological_constant_spectral_gap_identity.py` |
| 35 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 58 | 18.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 36 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 50 | 17.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 37 | `n_eff_from_three_generations_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 49 | 18.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_n_eff_from_three_generations.py` |
| 38 | `matter_radiation_equality_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 49 | 17.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_matter_radiation_equality_structural_identity.py` |
| 39 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | high | 181 | 13.01 | Y | fresh_context_or_stronger | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 40 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 126 | 17.49 | Y | fresh_context_or_stronger | - |
| 41 | `pmns_selector_unique_amplitude_slot_note` | decoration | claim_type_backfill_reaudit | high | 119 | 13.41 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_selector_unique_amplitude_slot.py` |
| 42 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | high | 119 | 12.91 | Y | fresh_context_or_stronger | `scripts/frontier_g_bare_derivation.py` |
| 43 | `alt_connectivity_family_sign_note` | - | unaudited | high | 78 | 12.80 | Y | fresh_context_or_stronger | `scripts/ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP.py` |
| 44 | `universal_theta_induced_edm_vanishing_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 61 | 15.45 | Y | fresh_context_or_stronger | `scripts/frontier_universal_theta_induced_edm_vanishing.py` |
| 45 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | high | 60 | 12.93 | Y | fresh_context_or_stronger | `scripts/frontier_yt_qfp_insensitivity.py` |
| 46 | `claude_complex_action_grown_companion_note` | - | unaudited | high | 57 | 12.86 | Y | fresh_context_or_stronger | `scripts/complex_action_grown_companion.py` |
| 47 | `source_resolved_wavefield_escalation_note` | - | unaudited | high | 55 | 12.31 | Y | fresh_context_or_stronger | `scripts/source_resolved_wavefield_escalation.py` |
| 48 | `causal_field_portability_note` | - | unaudited | high | 53 | 13.26 | Y | fresh_context_or_stronger | `scripts/causal_field_portability_probe.py` |
| 49 | `moving_source_retarded_portability_note` | - | unaudited | high | 52 | 12.23 | Y | fresh_context_or_stronger | `scripts/moving_source_retarded_portability_probe.py` |
| 50 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | high | 51 | 15.70 | Y | fresh_context_or_stronger | `scripts/frontier_taste_scalar_isotropy.py` |

Full queue lives in `data/audit_queue.json`.
