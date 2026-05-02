# Audit Queue

**Generated:** 2026-05-02T16:16:53.603576+00:00
**Total pending:** 575
**Ready (all deps already at retained-grade or metadata tiers):** 94

By criticality:
- `critical`: 85
- `high`: 202
- `medium`: 161
- `leaf`: 127

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `hypercharge_identification_note` | positive_theorem | claim_type_backfill_reaudit | critical | 308 | 13.77 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 2 | `left_handed_charge_matching_note` | positive_theorem | unaudited | critical | 304 | 20.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 3 | `gauge_scalar_temporal_completion_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 298 | 11.72 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_completion_theorem.py` |
| 4 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 298 | 11.72 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 5 | `yukawa_color_projection_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 297 | 12.72 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 6 | `gauge_vacuum_plaquette_constant_lift_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 297 | 11.72 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py` |
| 7 | `gauge_vacuum_plaquette_source_sector_matrix_element_factorization_note` | positive_theorem | claim_type_backfill_reaudit | critical | 297 | 11.72 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py` |
| 8 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | open_gate | claim_type_backfill_reaudit | critical | 297 | 11.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 9 | `gauge_vacuum_plaquette_residual_environment_identification_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 297 | 11.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py` |
| 10 | `gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 297 | 11.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_character_measure.py` |
| 11 | `ew_current_fierz_channel_decomposition_note_2026-05-01` | positive_theorem | unaudited | critical | 297 | 9.72 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_current_fierz_channel_decomposition.py` |
| 12 | `gauge_vacuum_plaquette_mixed_cumulant_audit_note` | positive_theorem | claim_type_backfill_reaudit | critical | 296 | 11.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py` |
| 13 | `scalar_3plus1_temporal_ratio_note` | positive_theorem | claim_type_backfill_reaudit | critical | 296 | 11.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_scalar_3plus1_temporal_ratio.py` |
| 14 | `higgs_mass_from_axiom_note` | positive_theorem | claim_type_backfill_reaudit | critical | 296 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_corrected_yt.py` |
| 15 | `gauge_vacuum_plaquette_transfer_operator_character_recurrence_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 11.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_transfer_operator_character_recurrence.py` |
| 16 | `gauge_vacuum_plaquette_perron_jacobi_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 11.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py` |
| 17 | `gauge_vacuum_plaquette_connected_hierarchy_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py` |
| 18 | `gauge_vacuum_plaquette_framework_point_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py` |
| 19 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 20 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 21 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 22 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 23 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 24 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 27.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 25 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 10.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 26 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 27 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 291 | 14.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 28 | `yt_color_projection_correction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 291 | 12.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 29 | `higgs_mechanism_note` | positive_theorem | claim_type_backfill_reaudit | critical | 291 | 9.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 30 | `higgs_from_lattice_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 291 | 8.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 31 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 290 | 11.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 32 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 10.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 33 | `universal_gr_discrete_global_closure_note` | positive_theorem | unaudited | critical | 60 | 14.43 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 60 | 13.93 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 35 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 36 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 46 | 14.05 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 37 | `three_generation_observable_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 346 | 22.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 38 | `three_generation_structure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 302 | 21.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 39 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 301 | 15.74 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 301 | 15.24 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 300 | 14.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 42 | `anomaly_forces_time_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 299 | 19.23 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 297 | 11.22 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 44 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 296 | 16.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 45 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | claim_type_backfill_reaudit | critical | 296 | 9.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 46 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 47 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 48 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 294 | 16.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 49 | `ew_current_matching_ozi_suppression_theorem_note_2026-04-27` | bounded_theorem | unaudited | critical | 294 | 9.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 50 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 293 | 24.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |

Full queue lives in `data/audit_queue.json`.
