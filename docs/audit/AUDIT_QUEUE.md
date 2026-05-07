# Audit Queue

**Total pending:** 829
**Ready (all deps already at retained-grade or metadata tiers):** 7

By criticality:
- `critical`: 503
- `high`: 24
- `medium`: 126
- `leaf`: 176

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 313 | 10.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 2 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 309 | 16.78 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 3 | `dm_leptogenesis_pmns_active_projector_reduction_note_2026-04-16` | bounded_theorem | unaudited | critical | 303 | 8.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_pmns_active_projector_reduction.py` |
| 4 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | unaudited | critical | 292 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 5 | `dm_abcc_closure_via_chamber_bound_and_dple_f4_note_2026-04-19` | bounded_theorem | unaudited | critical | 290 | 8.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_chamber_dple_closure.py` |
| 6 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 546 | 14.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 7 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 546 | 10.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 8 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 541 | 14.08 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 541 | 12.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 10 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 539 | 25.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 11 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 539 | 16.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 12 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 539 | 16.08 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 539 | 15.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 14 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 539 | 14.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 15 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 539 | 14.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 16 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 539 | 13.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 17 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 539 | 13.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 18 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 437 | 17.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 19 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 433 | 10.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 20 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 424 | 12.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 21 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 424 | 10.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 22 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | open_gate | unaudited | critical | 424 | 9.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py` |
| 23 | `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` | open_gate | unaudited | critical | 424 | 9.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py` |
| 24 | `su3_cube_perron_solve_combined_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 424 | 9.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_perron_solve.py` |
| 25 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 401 | 16.15 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 401 | 15.65 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 400 | 21.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 28 | `bminusl_anomaly_freedom_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 400 | 15.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bminusl_anomaly_freedom.py` |
| 29 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 400 | 15.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 30 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 400 | 14.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 31 | `hypercharge_squared_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 400 | 13.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_squared_trace_catalog.py` |
| 32 | `rh_sector_anomaly_cancellation_identities_note_2026-05-02` | positive_theorem | unaudited | critical | 400 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_rh_sector_anomaly_cancellation_identities.py` |
| 33 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 400 | 10.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 34 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 364 | 31.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 35 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 364 | 30.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 36 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 364 | 25.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 37 | `ckm_atlas_axiom_closure_note` | positive_theorem | unaudited | critical | 364 | 24.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 38 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 364 | 22.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 39 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 364 | 21.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 40 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 364 | 16.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 41 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 364 | 16.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 42 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 364 | 16.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 43 | `ckm_second_row_magnitudes_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 364 | 15.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_second_row_magnitudes.py` |
| 44 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 364 | 10.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 45 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 363 | 22.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 46 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 363 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `universal_gr_tensor_variational_candidate_note` | bounded_theorem | unaudited | critical | 363 | 12.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `universal_gr_tensor_quotient_uniqueness_note` | bounded_theorem | unaudited | critical | 363 | 12.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_tensor_quotient_uniqueness.py` |
| 49 | `universal_gr_a1_invariant_section_note` | positive_theorem | unaudited | critical | 363 | 11.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_a1_invariant_section.py` |
| 50 | `universal_gr_curvature_localization_blocker_note` | positive_theorem | unaudited | critical | 363 | 10.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

253 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 546 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 539 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 3 | `cycle-0003` | 7 | 539 | `anomaly_forces_time_theorem` | critical | unaudited |
| 4 | `cycle-0004` | 3 | 424 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 5 | `cycle-0005` | 4 | 424 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 6 | `cycle-0006` | 5 | 424 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 7 | `cycle-0007` | 6 | 424 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 400 | `hypercharge_identification_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 400 | `hypercharge_identification_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 400 | `hypercharge_identification_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 400 | `hypercharge_identification_note` | critical | unaudited |
| 12 | `cycle-0012` | 4 | 400 | `hypercharge_identification_note` | critical | unaudited |
| 13 | `cycle-0013` | 4 | 400 | `bminusl_anomaly_freedom_theorem_note_2026-04-24` | critical | unaudited |
| 14 | `cycle-0014` | 4 | 400 | `hypercharge_identification_note` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 364 | `ckm_atlas_axiom_closure_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 364 | `ckm_atlas_axiom_closure_note` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 364 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 364 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 364 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 364 | `ckm_atlas_axiom_closure_note` | critical | unaudited |
| 21 | `cycle-0021` | 3 | 364 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 364 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 364 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 363 | `universal_gr_discrete_global_closure_note` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 363 | `universal_gr_tensor_quotient_uniqueness_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
