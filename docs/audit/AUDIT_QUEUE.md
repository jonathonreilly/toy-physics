# Audit Queue

**Generated:** 2026-05-02T17:42:23.363966+00:00
**Total pending:** 589
**Ready (all deps already at retained-grade or metadata tiers):** 106

By criticality:
- `critical`: 66
- `high`: 205
- `medium`: 165
- `leaf`: 153

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 2 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 3 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 4 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 5 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 6 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 27.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 7 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 10.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 8 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 9 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 291 | 14.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 10 | `yt_color_projection_correction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 291 | 12.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 11 | `higgs_mechanism_note` | positive_theorem | claim_type_backfill_reaudit | critical | 291 | 9.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 12 | `higgs_from_lattice_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 291 | 8.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 13 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 290 | 11.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 14 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 10.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 15 | `universal_gr_discrete_global_closure_note` | positive_theorem | unaudited | critical | 60 | 14.43 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 16 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 60 | 13.93 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 17 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 18 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 46 | 14.05 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 19 | `three_generation_observable_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 346 | 22.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 20 | `three_generation_structure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 302 | 21.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 21 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 301 | 15.74 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 22 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 301 | 15.24 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 300 | 14.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 24 | `anomaly_forces_time_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 299 | 19.23 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 297 | 11.22 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 26 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 296 | 16.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 27 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 296 | 9.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 28 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 29 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 294 | 16.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 30 | `ew_current_matching_ozi_suppression_theorem_note_2026-04-27` | bounded_theorem | unaudited | critical | 294 | 9.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 31 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 293 | 24.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 32 | `g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.70 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 291 | 11.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |
| 34 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | positive_theorem | claim_type_backfill_reaudit | critical | 291 | 11.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 35 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 36 | `g_bare_two_ward_closure_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 10.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_two_ward_closure.py` |
| 37 | `g_bare_dynamical_fixation_obstruction_note_2026-04-18` | bounded_theorem | unaudited | critical | 290 | 10.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_critical_feature_scan.py` |
| 38 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 290 | 8.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 39 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 289 | 29.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 40 | `minimal_axioms_2026-04-11` | positive_theorem | claim_type_backfill_reaudit | critical | 289 | 26.18 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `higgs_vacuum_explicit_systematic_note` | positive_theorem | unaudited | critical | 289 | 15.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 42 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 289 | 11.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 43 | `alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 289 | 10.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_s_direct_wilson_loop.py` |
| 44 | `yt_flagship_boundary_note` | positive_theorem | unaudited | critical | 289 | 8.68 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `one_generation_matter_closure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 259 | 21.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 46 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 132 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 47 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 131 | 15.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 48 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 130 | 15.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 49 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 126 | 14.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 50 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 124 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |

Full queue lives in `data/audit_queue.json`.
