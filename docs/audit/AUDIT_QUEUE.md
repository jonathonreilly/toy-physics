# Audit Queue

**Generated:** 2026-05-02T20:35:10.197649+00:00
**Total pending:** 595
**Ready (all deps already at retained-grade or metadata tiers):** 121

By criticality:
- `critical`: 27
- `high`: 227
- `medium`: 173
- `leaf`: 168

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 183 | 26.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 2 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 3 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 244 | 16.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 4 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 238 | 28.90 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 5 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 132 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 6 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 131 | 15.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 7 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 130 | 15.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 8 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 126 | 14.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 9 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 124 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 10 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 118 | 28.89 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 11 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 117 | 28.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 12 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 116 | 20.87 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 13 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 110 | 22.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 14 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 104 | 23.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 15 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 96 | 19.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 16 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 87 | 14.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 17 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 86 | 14.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 18 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 85 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 19 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 85 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 20 | `ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 84 | 14.41 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `ckm_atlas_axiom_closure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 77 | 17.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 22 | `down_type_mass_ratio_ckm_dual_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 61 | 13.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 23 | `cosmological_constant_spectral_gap_identity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 15.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmological_constant_spectral_gap_identity.py` |
| 24 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 14.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 25 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 43 | 12.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 26 | `n_eff_from_three_generations_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 42 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_n_eff_from_three_generations.py` |
| 27 | `matter_radiation_equality_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 42 | 12.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_matter_radiation_equality_structural_identity.py` |
| 28 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 29 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 30 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 31 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 245 | 10.44 | Y | fresh_context_or_stronger | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 32 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | high | 174 | 8.95 | Y | fresh_context_or_stronger | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 33 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 119 | 13.41 | Y | fresh_context_or_stronger | - |
| 34 | `dm_neutrino_dirac_bridge_theorem_note_2026-04-15` | positive_theorem | unaudited | high | 115 | 10.86 | Y | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_dirac_bridge_theorem.py` |
| 35 | `pmns_selector_unique_amplitude_slot_note` | decoration | claim_type_backfill_reaudit | high | 112 | 9.32 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_selector_unique_amplitude_slot.py` |
| 36 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | high | 112 | 8.82 | Y | fresh_context_or_stronger | `scripts/frontier_g_bare_derivation.py` |
| 37 | `koide_dweh_cyclic_compression_note_2026-04-18` | positive_theorem | unaudited | high | 77 | 8.79 | Y | fresh_context_or_stronger | `scripts/frontier_koide_dweh_cyclic_compression.py` |
| 38 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | high | 71 | 9.67 | Y | fresh_context_or_stronger | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 39 | `koide_axiom_native_support_batch_note_2026-04-22` | bounded_theorem | unaudited | high | 69 | 8.63 | Y | fresh_context_or_stronger | - |
| 40 | `physical_lattice_necessity_note` | no_go | unaudited | high | 57 | 12.86 | Y | fresh_context_or_stronger | `scripts/frontier_physical_lattice_necessity.py` |
| 41 | `complex_action_note` | bounded_theorem | unaudited | high | 57 | 8.36 | Y | fresh_context_or_stronger | `scripts/complex_action_harness.py` |
| 42 | `lensing_k_sweep_note` | bounded_theorem | unaudited | high | 57 | 8.36 | Y | fresh_context_or_stronger | `scripts/lensing_k_sweep.py` |
| 43 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | high | 54 | 11.28 | Y | fresh_context_or_stronger | `scripts/verify_cl3_sm_embedding.py` |
| 44 | `universal_theta_induced_edm_vanishing_theorem_note_2026-04-24` | decoration | claim_type_backfill_reaudit | high | 54 | 11.28 | Y | fresh_context_or_stronger | `scripts/frontier_universal_theta_induced_edm_vanishing.py` |
| 45 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | high | 53 | 8.76 | Y | fresh_context_or_stronger | `scripts/frontier_yt_qfp_insensitivity.py` |
| 46 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | high | 44 | 11.49 | Y | fresh_context_or_stronger | `scripts/frontier_taste_scalar_isotropy.py` |
| 47 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | high | 37 | 7.75 | Y | fresh_context_or_stronger | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 48 | `teleportation_conclusion_boundary_note` | open_gate | unaudited | high | 36 | 8.71 | Y | fresh_context_or_stronger | `scripts/frontier_teleportation_conclusion_boundary.py` |
| 49 | `monopole_derived_note` | positive_theorem | unaudited | high | 36 | 7.71 | Y | fresh_context_or_stronger | `scripts/frontier_monopole_derived.py` |
| 50 | `teleportation_acceptance_suite_note` | bounded_theorem | unaudited | high | 36 | 7.71 | Y | fresh_context_or_stronger | `scripts/frontier_teleportation_acceptance_suite.py` |

Full queue lives in `data/audit_queue.json`.
