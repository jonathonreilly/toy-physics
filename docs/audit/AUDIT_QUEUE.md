# Audit Queue

**Generated:** 2026-04-26T22:25:49.706874+00:00  
**Total pending:** 1601  
**Ready (all deps already at a stable tier):** 1204  

By criticality:
- `critical`: 91
- `high`: 569
- `medium`: 85
- `leaf`: 856

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent auditor before `audited_clean` lands.

## Top 50

| # | claim_id | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_scalar_temporal_completion_theorem_note` | critical | 279 | 15.13 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_completion_theorem.py` |
| 2 | `gauge_vacuum_plaquette_constant_lift_obstruction_note` | critical | 279 | 15.13 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py` |
| 3 | `gauge_vacuum_plaquette_mixed_cumulant_audit_note` | critical | 279 | 15.13 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py` |
| 4 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | critical | 279 | 15.13 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 5 | `scalar_3plus1_temporal_ratio_note` | critical | 279 | 15.13 | Y | cross_family_with_cross_confirmation | `scripts/frontier_scalar_3plus1_temporal_ratio.py` |
| 6 | `gauge_vacuum_plaquette_transfer_operator_character_recurrence_note` | critical | 278 | 15.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_transfer_operator_character_recurrence.py` |
| 7 | `gauge_vacuum_plaquette_perron_jacobi_underdetermination_note` | critical | 278 | 15.12 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py` |
| 8 | `gauge_vacuum_plaquette_source_sector_matrix_element_factorization_note` | critical | 278 | 15.12 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py` |
| 9 | `gauge_vacuum_plaquette_connected_hierarchy_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py` |
| 10 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 11 | `gauge_vacuum_plaquette_framework_point_underdetermination_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py` |
| 12 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 13 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 14 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 15 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 16 | `gauge_vacuum_plaquette_residual_environment_identification_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py` |
| 17 | `gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_character_measure.py` |
| 18 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 19 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 20 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | critical | 278 | 14.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 21 | `taste_scalar_isotropy_theorem_note` | critical | 277 | 17.62 | Y | cross_family_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 22 | `observable_principle_from_axiom_note` | critical | 276 | 28.61 | Y | cross_family_with_cross_confirmation | `scripts/frontier_hierarchy_observable_principle_from_axiom.py` |
| 23 | `yt_ew_color_projection_theorem` | critical | 276 | 22.61 | Y | cross_family_with_cross_confirmation | - |
| 24 | `graph_first_su3_integration_note` | critical | 275 | 23.11 | Y | cross_family_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 25 | `rconn_derived_note` | critical | 275 | 18.11 | Y | cross_family_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 26 | `yt_color_projection_correction_note` | critical | 275 | 16.11 | Y | cross_family_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 27 | `g_bare_derivation_note` | critical | 275 | 13.61 | Y | cross_family_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 28 | `native_gauge_closure_note` | critical | 274 | 19.60 | Y | cross_family_with_cross_confirmation | - |
| 29 | `s3_mass_matrix_no_go_note` | critical | 274 | 16.10 | Y | cross_family_with_cross_confirmation | `scripts/frontier_s3_mass_matrix_no_go.py` |
| 30 | `s3_taste_cube_decomposition_note` | critical | 274 | 16.10 | Y | cross_family_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 31 | `z2_hw1_mass_matrix_parametrization_note` | critical | 274 | 16.10 | Y | cross_family_with_cross_confirmation | `scripts/frontier_z2_hw1_mass_matrix_parametrization.py` |
| 32 | `g_bare_rigidity_theorem_note` | critical | 274 | 15.60 | Y | cross_family_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 33 | `yt_qfp_insensitivity_support_note` | critical | 274 | 14.60 | Y | cross_family_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 34 | `yt_explicit_systematic_budget_note` | critical | 274 | 14.10 | Y | cross_family_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 35 | `graph_first_selector_derivation_note` | critical | 274 | 13.60 | Y | cross_family_with_cross_confirmation | `scripts/frontier_graph_first_selector_derivation.py` |
| 36 | `higgs_mass_from_axiom_note` | critical | 274 | 13.10 | Y | cross_family_with_cross_confirmation | - |
| 37 | `confinement_string_tension_note` | critical | 118 | 14.39 | Y | cross_family_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 38 | `gauge_vacuum_plaquette_bridge_support_note` | critical | 278 | 14.62 |  | cross_family_with_cross_confirmation | - |
| 39 | `plaquette_self_consistency_note` | critical | 277 | 15.62 |  | cross_family_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 40 | `higgs_mass_derived_note` | critical | 276 | 20.11 |  | cross_family_with_cross_confirmation | - |
| 41 | `higgs_mechanism_note` | critical | 276 | 13.11 |  | cross_family_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 42 | `higgs_from_lattice_note` | critical | 276 | 12.61 |  | cross_family_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 43 | `alpha_s_derived_note` | critical | 275 | 32.61 |  | cross_family_with_cross_confirmation | - |
| 44 | `g_bare_dynamical_fixation_obstruction_note_2026-04-18` | critical | 274 | 14.10 |  | cross_family_with_cross_confirmation | `scripts/frontier_g_bare_critical_feature_scan.py` |
| 45 | `three_generation_structure_note` | critical | 273 | 25.10 |  | cross_family_with_cross_confirmation | - |
| 46 | `one_generation_matter_closure_note` | critical | 273 | 24.60 |  | cross_family_with_cross_confirmation | - |
| 47 | `three_generation_observable_theorem_note` | critical | 273 | 24.60 |  | cross_family_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 48 | `yt_ward_identity_derivation_theorem` | critical | 273 | 23.10 |  | cross_family_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 49 | `anomaly_forces_time_theorem` | critical | 273 | 22.60 |  | cross_family_with_cross_confirmation | - |
| 50 | `minimal_axioms_2026-04-11` | critical | 273 | 21.60 |  | cross_family_with_cross_confirmation | - |

Full queue lives in `data/audit_queue.json`.
