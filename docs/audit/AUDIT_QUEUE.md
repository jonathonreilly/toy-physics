# Audit Queue

**Generated:** 2026-05-02T14:46:44.302928+00:00
**Total pending:** 463
**Ready (all deps already at retained-grade or metadata tiers):** 45

By criticality:
- `critical`: 88
- `high`: 184
- `medium`: 122
- `leaf`: 69

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `native_gauge_closure_note` | bounded_theorem | unaudited | critical | 308 | 18.27 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_non_abelian_gauge.py` |
| 2 | `site_phase_cube_shift_intertwiner_note` | positive_theorem | claim_type_backfill_reaudit | critical | 305 | 15.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_site_phase_cube_shift_intertwiner.py` |
| 3 | `z2_hw1_mass_matrix_parametrization_note` | positive_theorem | claim_type_backfill_reaudit | critical | 303 | 13.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_z2_hw1_mass_matrix_parametrization.py` |
| 4 | `s3_taste_cube_decomposition_note` | positive_theorem | claim_type_backfill_reaudit | critical | 303 | 13.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 5 | `s3_mass_matrix_no_go_note` | positive_theorem | claim_type_backfill_reaudit | critical | 303 | 12.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_mass_matrix_no_go.py` |
| 6 | `generation_axiom_boundary_note` | positive_theorem | claim_type_backfill_reaudit | critical | 303 | 10.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 7 | `physical_lattice_necessity_note` | positive_theorem | claim_type_backfill_reaudit | critical | 301 | 15.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_lattice_necessity.py` |
| 8 | `observable_principle_from_axiom_note` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 26.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_observable_principle_from_axiom.py` |
| 9 | `hypercharge_identification_note` | positive_theorem | claim_type_backfill_reaudit | critical | 272 | 11.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 10 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 268 | 11.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 11 | `left_handed_charge_matching_note` | positive_theorem | unaudited | critical | 267 | 17.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 12 | `gauge_vacuum_plaquette_constant_lift_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 267 | 11.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py` |
| 13 | `gauge_vacuum_plaquette_source_sector_matrix_element_factorization_note` | positive_theorem | claim_type_backfill_reaudit | critical | 267 | 11.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py` |
| 14 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | open_gate | claim_type_backfill_reaudit | critical | 267 | 11.07 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 15 | `gauge_vacuum_plaquette_residual_environment_identification_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 267 | 11.07 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py` |
| 16 | `gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 267 | 11.07 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_character_measure.py` |
| 17 | `gauge_scalar_temporal_completion_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 266 | 11.06 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_completion_theorem.py` |
| 18 | `gauge_vacuum_plaquette_mixed_cumulant_audit_note` | positive_theorem | claim_type_backfill_reaudit | critical | 266 | 11.06 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py` |
| 19 | `scalar_3plus1_temporal_ratio_note` | positive_theorem | claim_type_backfill_reaudit | critical | 266 | 11.06 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_scalar_3plus1_temporal_ratio.py` |
| 20 | `yukawa_color_projection_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 12.05 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 21 | `gauge_vacuum_plaquette_transfer_operator_character_recurrence_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 11.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_transfer_operator_character_recurrence.py` |
| 22 | `gauge_vacuum_plaquette_perron_jacobi_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 11.05 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py` |
| 23 | `gauge_vacuum_plaquette_connected_hierarchy_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py` |
| 24 | `gauge_vacuum_plaquette_framework_point_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py` |
| 25 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 26 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 27 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 28 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 29 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 30 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 264 | 27.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 31 | `higgs_mass_from_axiom_note` | positive_theorem | claim_type_backfill_reaudit | critical | 264 | 10.05 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_corrected_yt.py` |
| 32 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | critical | 263 | 9.54 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 33 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 262 | 11.04 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 34 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 261 | 14.03 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 35 | `yt_color_projection_correction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 261 | 12.53 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 36 | `higgs_mechanism_note` | positive_theorem | claim_type_backfill_reaudit | critical | 261 | 9.03 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 37 | `higgs_from_lattice_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 261 | 8.53 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 38 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 260 | 11.53 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 39 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | critical | 260 | 10.03 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 40 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 53 | 13.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 41 | `three_generation_observable_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 302 | 21.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 42 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 267 | 11.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 43 | `three_generation_structure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 266 | 21.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 44 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | claim_type_backfill_reaudit | critical | 266 | 9.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 45 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 265 | 15.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 265 | 14.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 48 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 49 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 264 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 50 | `rconn_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 264 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |

Full queue lives in `data/audit_queue.json`.
