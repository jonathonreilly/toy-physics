# Audit Queue

**Total pending:** 818
**Ready (all deps already at retained-grade or metadata tiers):** 6

By criticality:
- `critical`: 535
- `high`: 14
- `medium`: 95
- `leaf`: 174

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03` | no_go | unaudited | critical | 598 | 11.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_observable_bridge_no_go.py` |
| 2 | `su3_fusion_engine_pr1_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 588 | 10.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_fusion_engine.py` |
| 3 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 532 | 11.56 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 4 | `dm_leptogenesis_pmns_active_projector_reduction_note_2026-04-16` | bounded_theorem | unaudited | critical | 303 | 8.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_pmns_active_projector_reduction.py` |
| 5 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | unaudited | critical | 292 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 6 | `dm_abcc_closure_via_chamber_bound_and_dple_f4_note_2026-04-19` | bounded_theorem | unaudited | critical | 290 | 8.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_chamber_dple_closure.py` |
| 7 | `gauge_scalar_temporal_observable_bridge_stretch_note_2026-05-02` | open_gate | unaudited | critical | 589 | 10.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_observable_bridge_stretch.py` |
| 8 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 587 | 12.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 9 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 587 | 10.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 10 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | open_gate | unaudited | critical | 587 | 9.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py` |
| 11 | `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` | open_gate | unaudited | critical | 587 | 9.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py` |
| 12 | `su3_cube_perron_solve_combined_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 587 | 9.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_perron_solve.py` |
| 13 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 542 | 12.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 14 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 539 | 18.08 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 15 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 539 | 16.08 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 16 | `diamond_absolute_unit_bridge_note` | positive_theorem | unaudited | critical | 539 | 9.58 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 538 | 14.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 18 | `diamond_phase_ramp_bridge_card_note` | positive_theorem | unaudited | critical | 538 | 10.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/diamond_phase_ramp_bridge_card.py` |
| 19 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 538 | 10.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 20 | `shapiro_delay_note` | positive_theorem | unaudited | critical | 537 | 12.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_phase_lag_probe.py` |
| 21 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 535 | 15.57 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 22 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 534 | 15.06 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 533 | 16.06 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 24 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 533 | 15.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 25 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 533 | 12.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 26 | `complex_selectivity_compare_note` | positive_theorem | unaudited | critical | 533 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_COMPARE.py` |
| 27 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 532 | 17.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 28 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 532 | 15.56 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `signed_gravity_tensor_source_transport_retention_note` | positive_theorem | unaudited | critical | 532 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_tensor_source_transport_retention.py` |
| 30 | `universal_gr_curvature_localization_blocker_note` | positive_theorem | unaudited | critical | 532 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 532 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 32 | `causal_field_canonical_chain_note` | positive_theorem | unaudited | critical | 532 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `complex_selectivity_predictor_note` | positive_theorem | unaudited | critical | 532 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py` |
| 34 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 531 | 25.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 35 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 531 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 36 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 531 | 16.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 531 | 16.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `universal_qg_canonical_textbook_continuum_gr_closure_note` | positive_theorem | unaudited | critical | 531 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 39 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | positive_theorem | unaudited | critical | 531 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `universal_qg_smooth_gravitational_local_identification_note` | positive_theorem | unaudited | critical | 531 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 531 | 15.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 531 | 15.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 43 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | positive_theorem | unaudited | critical | 531 | 15.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `universal_qg_smooth_gravitational_global_atlas_note` | positive_theorem | unaudited | critical | 531 | 14.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 531 | 14.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 46 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 531 | 14.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 47 | `newton_law_derived_note` | positive_theorem | unaudited | critical | 531 | 14.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 48 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 531 | 14.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `universal_qg_canonical_smooth_gravitational_weak_measure_note` | positive_theorem | unaudited | critical | 531 | 14.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 531 | 13.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |

## Citation cycle break targets

257 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 3 | 587 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 2 | `cycle-0002` | 4 | 587 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 3 | `cycle-0003` | 5 | 587 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 4 | `cycle-0004` | 6 | 587 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 542 | `yt_explicit_systematic_budget_note` | critical | audited_conditional |
| 6 | `cycle-0006` | 2 | 539 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 539 | `universal_qg_projective_schur_closure_note` | critical | audited_conditional |
| 8 | `cycle-0008` | 3 | 539 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 538 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 531 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 531 | `universal_gr_tensor_quotient_uniqueness_note` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 531 | `universal_qg_canonical_textbook_continuum_gr_closure_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 531 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 531 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 531 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 531 | `signed_gravity_aps_locked_axiom_extension_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 531 | `signed_gravity_aps_boundary_index_chi_probe_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 531 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 531 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 531 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 21 | `cycle-0021` | 3 | 531 | `signed_gravity_native_boundary_complex_containment_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 531 | `signed_gravity_aps_locked_source_action_proposal_note` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 531 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | critical | unaudited |
| 24 | `cycle-0024` | 3 | 531 | `universal_qg_continuum_bridge_reduction_note` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 531 | `antigravity_sign_selector_boundary_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
