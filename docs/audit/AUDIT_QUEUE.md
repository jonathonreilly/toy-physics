# Audit Queue

**Generated:** 2026-05-02T15:43:13.603445+00:00
**Total pending:** 572
**Ready (all deps already at retained-grade or metadata tiers):** 112

By criticality:
- `critical`: 87
- `high`: 201
- `medium`: 146
- `leaf`: 138

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `s3_mass_matrix_no_go_note` | positive_theorem | claim_type_backfill_reaudit | critical | 329 | 12.87 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_mass_matrix_no_go.py` |
| 2 | `generation_axiom_boundary_note` | positive_theorem | claim_type_backfill_reaudit | critical | 329 | 10.87 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 3 | `physical_lattice_necessity_note` | positive_theorem | claim_type_backfill_reaudit | critical | 327 | 16.36 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_lattice_necessity.py` |
| 4 | `observable_principle_from_axiom_note` | positive_theorem | claim_type_backfill_reaudit | critical | 314 | 27.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_observable_principle_from_axiom.py` |
| 5 | `hypercharge_identification_note` | positive_theorem | claim_type_backfill_reaudit | critical | 296 | 12.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 6 | `left_handed_charge_matching_note` | positive_theorem | unaudited | critical | 291 | 19.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 7 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 287 | 11.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 8 | `gauge_scalar_temporal_completion_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_completion_theorem.py` |
| 9 | `gauge_vacuum_plaquette_constant_lift_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py` |
| 10 | `gauge_vacuum_plaquette_source_sector_matrix_element_factorization_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py` |
| 11 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | open_gate | claim_type_backfill_reaudit | critical | 286 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 12 | `gauge_vacuum_plaquette_residual_environment_identification_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py` |
| 13 | `gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_character_measure.py` |
| 14 | `yukawa_color_projection_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 285 | 12.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 15 | `gauge_vacuum_plaquette_mixed_cumulant_audit_note` | positive_theorem | claim_type_backfill_reaudit | critical | 285 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py` |
| 16 | `scalar_3plus1_temporal_ratio_note` | positive_theorem | claim_type_backfill_reaudit | critical | 285 | 11.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_scalar_3plus1_temporal_ratio.py` |
| 17 | `ew_current_fierz_channel_decomposition_note_2026-05-01` | positive_theorem | unaudited | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_current_fierz_channel_decomposition.py` |
| 18 | `gauge_vacuum_plaquette_transfer_operator_character_recurrence_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 11.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_transfer_operator_character_recurrence.py` |
| 19 | `gauge_vacuum_plaquette_perron_jacobi_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 11.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py` |
| 20 | `gauge_vacuum_plaquette_connected_hierarchy_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py` |
| 21 | `gauge_vacuum_plaquette_framework_point_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py` |
| 22 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 23 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 24 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 25 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 26 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 27 | `higgs_mass_from_axiom_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_corrected_yt.py` |
| 28 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 283 | 27.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 29 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | critical | 283 | 10.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 30 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 281 | 11.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 31 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 280 | 14.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 32 | `yt_color_projection_correction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 280 | 12.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 33 | `higgs_mechanism_note` | positive_theorem | claim_type_backfill_reaudit | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 34 | `higgs_from_lattice_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 35 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 279 | 11.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 36 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | critical | 279 | 10.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 37 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 55 | 13.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 38 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 53 | 13.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 39 | `three_generation_observable_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 328 | 22.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 40 | `three_generation_structure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 21.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 41 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 289 | 15.18 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 289 | 14.68 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 288 | 13.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 44 | `anomaly_forces_time_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 287 | 18.67 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 286 | 11.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 46 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | claim_type_backfill_reaudit | critical | 285 | 9.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 47 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 284 | 16.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 48 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 49 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 284 | 10.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 50 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 283 | 16.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |

Full queue lives in `data/audit_queue.json`.
