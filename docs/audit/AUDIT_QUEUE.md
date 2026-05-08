# Audit Queue

**Total pending:** 841
**Ready (all deps already at retained-grade or metadata tiers):** 0

By criticality:
- `critical`: 504
- `high`: 25
- `medium`: 131
- `leaf`: 181

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 551 | 14.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 2 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 551 | 10.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 3 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 546 | 14.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 4 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 546 | 12.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 5 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 544 | 25.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 6 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 544 | 16.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 7 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 544 | 16.09 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 544 | 15.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 9 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 544 | 14.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 10 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 544 | 14.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 11 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 544 | 13.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 12 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 544 | 13.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 13 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 450 | 24.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 14 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 437 | 17.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 15 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 435 | 12.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 16 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 435 | 10.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 17 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | open_gate | unaudited | critical | 435 | 9.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py` |
| 18 | `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` | open_gate | unaudited | critical | 435 | 9.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py` |
| 19 | `su3_cube_perron_solve_combined_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 435 | 9.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_perron_solve.py` |
| 20 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 433 | 10.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 21 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 429 | 23.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 22 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 429 | 10.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 23 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 428 | 25.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 24 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 402 | 16.16 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 402 | 15.65 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 401 | 21.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 27 | `bminusl_anomaly_freedom_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 401 | 15.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bminusl_anomaly_freedom.py` |
| 28 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 401 | 15.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 29 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 401 | 14.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 30 | `hypercharge_squared_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 401 | 14.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_squared_trace_catalog.py` |
| 31 | `rh_sector_anomaly_cancellation_identities_note_2026-05-02` | positive_theorem | unaudited | critical | 401 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_rh_sector_anomaly_cancellation_identities.py` |
| 32 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 401 | 10.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 33 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 364 | 31.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 34 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 364 | 30.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 35 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 364 | 25.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 36 | `ckm_atlas_axiom_closure_note` | positive_theorem | unaudited | critical | 364 | 24.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 37 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 364 | 22.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 38 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 364 | 21.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 39 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 364 | 16.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 40 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 364 | 16.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 41 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 364 | 16.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 42 | `ckm_second_row_magnitudes_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 364 | 15.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_second_row_magnitudes.py` |
| 43 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 364 | 10.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 44 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 363 | 22.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 45 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 363 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `universal_gr_tensor_variational_candidate_note` | bounded_theorem | unaudited | critical | 363 | 12.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `universal_gr_tensor_quotient_uniqueness_note` | bounded_theorem | unaudited | critical | 363 | 12.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_tensor_quotient_uniqueness.py` |
| 48 | `universal_gr_a1_invariant_section_note` | positive_theorem | unaudited | critical | 363 | 11.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_a1_invariant_section.py` |
| 49 | `universal_gr_curvature_localization_blocker_note` | positive_theorem | unaudited | critical | 363 | 10.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `universal_gr_constraint_action_stationarity_note` | positive_theorem | unaudited | critical | 363 | 9.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

254 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 551 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 544 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 3 | `cycle-0003` | 7 | 544 | `anomaly_forces_time_theorem` | critical | unaudited |
| 4 | `cycle-0004` | 3 | 435 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 5 | `cycle-0005` | 4 | 435 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 6 | `cycle-0006` | 5 | 435 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 7 | `cycle-0007` | 6 | 435 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 401 | `hypercharge_identification_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 401 | `hypercharge_identification_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 401 | `hypercharge_identification_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 401 | `hypercharge_identification_note` | critical | unaudited |
| 12 | `cycle-0012` | 4 | 401 | `hypercharge_identification_note` | critical | unaudited |
| 13 | `cycle-0013` | 4 | 401 | `bminusl_anomaly_freedom_theorem_note_2026-04-24` | critical | unaudited |
| 14 | `cycle-0014` | 4 | 401 | `hypercharge_identification_note` | critical | unaudited |
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
