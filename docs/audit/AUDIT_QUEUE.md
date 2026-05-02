# Audit Queue

**Generated:** 2026-05-02T17:21:06.302511+00:00
**Total pending:** 572
**Ready (all deps already at retained-grade or metadata tiers):** 90

By criticality:
- `critical`: 72
- `high`: 203
- `medium`: 162
- `leaf`: 135

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `higgs_mass_from_axiom_note` | positive_theorem | claim_type_backfill_reaudit | critical | 296 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_corrected_yt.py` |
| 2 | `gauge_vacuum_plaquette_transfer_operator_character_recurrence_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 11.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_transfer_operator_character_recurrence.py` |
| 3 | `gauge_vacuum_plaquette_perron_jacobi_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 11.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py` |
| 4 | `gauge_vacuum_plaquette_connected_hierarchy_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py` |
| 5 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 6 | `gauge_vacuum_plaquette_framework_point_underdetermination_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py` |
| 7 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 8 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 9 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 10 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 11 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 12 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 27.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 13 | `g_bare_derivation_note` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 10.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 14 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 15 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 291 | 14.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 16 | `yt_color_projection_correction_note` | positive_theorem | claim_type_backfill_reaudit | critical | 291 | 12.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 17 | `higgs_mechanism_note` | positive_theorem | claim_type_backfill_reaudit | critical | 291 | 9.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 18 | `higgs_from_lattice_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 291 | 8.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 19 | `yt_qfp_insensitivity_support_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 290 | 11.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 20 | `yt_explicit_systematic_budget_note` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 10.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 21 | `universal_gr_discrete_global_closure_note` | positive_theorem | unaudited | critical | 60 | 14.43 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 22 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 60 | 13.93 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 23 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 24 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 46 | 14.05 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 25 | `three_generation_observable_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 346 | 22.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 26 | `three_generation_structure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 302 | 21.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 27 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 301 | 15.74 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 301 | 15.24 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 300 | 14.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 30 | `anomaly_forces_time_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 299 | 19.23 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 297 | 11.22 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 32 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 296 | 16.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 33 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 296 | 9.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 34 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | claim_type_backfill_reaudit | critical | 295 | 10.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 35 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 294 | 16.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 36 | `ew_current_matching_ozi_suppression_theorem_note_2026-04-27` | bounded_theorem | unaudited | critical | 294 | 9.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 37 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 293 | 24.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 38 | `g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.70 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 39 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 291 | 11.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |
| 40 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | positive_theorem | claim_type_backfill_reaudit | critical | 291 | 11.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 42 | `g_bare_two_ward_closure_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 290 | 10.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_two_ward_closure.py` |
| 43 | `g_bare_dynamical_fixation_obstruction_note_2026-04-18` | bounded_theorem | unaudited | critical | 290 | 10.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_critical_feature_scan.py` |
| 44 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 290 | 8.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 45 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 289 | 29.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 46 | `minimal_axioms_2026-04-11` | positive_theorem | claim_type_backfill_reaudit | critical | 289 | 26.18 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `higgs_vacuum_explicit_systematic_note` | positive_theorem | claim_type_backfill_reaudit | critical | 289 | 15.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 48 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 289 | 11.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 49 | `alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 289 | 10.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_s_direct_wilson_loop.py` |
| 50 | `yt_flagship_boundary_note` | positive_theorem | unaudited | critical | 289 | 8.68 |  | fresh_context_or_stronger_with_cross_confirmation | - |

Full queue lives in `data/audit_queue.json`.
