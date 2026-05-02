# Audit Queue

**Generated:** 2026-05-02T16:14:53.986293+00:00
**Total pending:** 565
**Ready (all deps already at retained-grade or metadata tiers):** 105

By criticality:
- `critical`: 80
- `high`: 201
- `medium`: 146
- `leaf`: 138

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_scalar_temporal_completion_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_completion_theorem.py` |
| 2 | `gauge_vacuum_plaquette_constant_lift_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py` |
| 3 | `gauge_vacuum_plaquette_source_sector_matrix_element_factorization_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py` |
| 4 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | open_gate | claim_type_backfill_reaudit | critical | 286 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 5 | `gauge_vacuum_plaquette_residual_environment_identification_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py` |
| 6 | `gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_character_measure.py` |
| 7 | `yukawa_color_projection_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 285 | 12.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 8 | `gauge_vacuum_plaquette_mixed_cumulant_audit_note` | positive_theorem | claim_type_backfill_reaudit | critical | 285 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py` |
| 9 | `scalar_3plus1_temporal_ratio_note` | positive_theorem | claim_type_backfill_reaudit | critical | 285 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_scalar_3plus1_temporal_ratio.py` |
| 10 | `ew_current_fierz_channel_decomposition_note_2026-05-01` | positive_theorem | unaudited | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_current_fierz_channel_decomposition.py` |
| 11 | `gauge_vacuum_plaquette_transfer_operator_character_recurrence_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 11.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_transfer_operator_character_recurrence.py` |
| 12 | `gauge_vacuum_plaquette_perron_jacobi_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 11.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py` |
| 13 | `gauge_vacuum_plaquette_connected_hierarchy_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py` |
| 14 | `gauge_vacuum_plaquette_framework_point_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py` |
| 15 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 16 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 17 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 18 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 19 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 20 | `higgs_mass_from_axiom_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_corrected_yt.py` |
| 21 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 283 | 27.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 22 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | critical | 283 | 10.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 23 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 281 | 11.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 24 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 280 | 14.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 25 | `yt_color_projection_correction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 280 | 12.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 26 | `higgs_mechanism_note` | positive_theorem | claim_type_backfill_reaudit | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 27 | `higgs_from_lattice_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 28 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 279 | 11.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 29 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | critical | 279 | 10.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 30 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 55 | 13.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 31 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 53 | 13.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 32 | `three_generation_observable_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 328 | 22.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 33 | `three_generation_structure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 21.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 34 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 289 | 15.18 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 35 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 289 | 14.68 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 288 | 13.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 37 | `anomaly_forces_time_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 287 | 18.67 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 39 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | claim_type_backfill_reaudit | critical | 285 | 9.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 40 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 284 | 16.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 41 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 42 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 43 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 283 | 16.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 44 | `ew_current_matching_ozi_suppression_theorem_note_2026-04-27` | bounded_theorem | unaudited | critical | 282 | 9.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 45 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 281 | 24.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 46 | `g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19` | positive_theorem | claim_type_backfill_reaudit | critical | 281 | 11.64 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 280 | 11.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |
| 48 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | positive_theorem | claim_type_backfill_reaudit | critical | 280 | 11.13 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 279 | 15.63 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 50 | `g_bare_two_ward_closure_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 279 | 10.63 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_two_ward_closure.py` |

Full queue lives in `data/audit_queue.json`.
