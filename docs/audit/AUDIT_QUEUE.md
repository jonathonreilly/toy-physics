# Audit Queue

**Total pending:** 819
**Ready (all deps already at retained-grade or metadata tiers):** 14

By criticality:
- `critical`: 536
- `high`: 14
- `medium`: 95
- `leaf`: 174

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03` | no_go | unaudited | critical | 598 | 11.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_observable_bridge_no_go.py` |
| 2 | `su3_fusion_engine_pr1_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 588 | 10.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_fusion_engine.py` |
| 3 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 538 | 14.07 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 4 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 532 | 11.56 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 5 | `higgs_mass_derived_note` | positive_theorem | unaudited | critical | 308 | 17.77 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 6 | `dm_leptogenesis_pmns_active_projector_reduction_note_2026-04-16` | bounded_theorem | unaudited | critical | 303 | 8.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_pmns_active_projector_reduction.py` |
| 7 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | positive_theorem | unaudited | critical | 293 | 12.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_axis_covariant_full_cube_orbit_law.py` |
| 8 | `lensing_finite_path_explanation_note` | open_gate | unaudited | critical | 293 | 8.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_analytical_finite_path.py` |
| 9 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | unaudited | critical | 292 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 10 | `dm_abcc_closure_via_chamber_bound_and_dple_f4_note_2026-04-19` | bounded_theorem | unaudited | critical | 290 | 8.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_chamber_dple_closure.py` |
| 11 | `abcc_cp_phase_no_go_theorem_note_2026-04-19` | open_gate | unaudited | critical | 289 | 10.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_abcc_cp_phase_no_go_theorem.py` |
| 12 | `gauge_scalar_temporal_observable_bridge_stretch_note_2026-05-02` | open_gate | unaudited | critical | 589 | 10.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_observable_bridge_stretch.py` |
| 13 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 587 | 12.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 14 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 587 | 10.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 15 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | open_gate | unaudited | critical | 587 | 9.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py` |
| 16 | `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` | open_gate | unaudited | critical | 587 | 9.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py` |
| 17 | `su3_cube_perron_solve_combined_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 587 | 9.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_perron_solve.py` |
| 18 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 542 | 12.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 19 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 539 | 18.08 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 20 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 539 | 16.08 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 539 | 14.08 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 22 | `diamond_absolute_unit_bridge_note` | positive_theorem | unaudited | critical | 539 | 9.58 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `diamond_phase_ramp_bridge_card_note` | positive_theorem | unaudited | critical | 538 | 10.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/diamond_phase_ramp_bridge_card.py` |
| 24 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 538 | 10.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 25 | `shapiro_delay_note` | positive_theorem | unaudited | critical | 537 | 12.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_phase_lag_probe.py` |
| 26 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 535 | 15.57 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 534 | 15.06 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 533 | 16.06 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 533 | 15.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 30 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 533 | 12.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 31 | `complex_selectivity_compare_note` | positive_theorem | unaudited | critical | 533 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_COMPARE.py` |
| 32 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 532 | 17.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 33 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 532 | 15.56 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `signed_gravity_tensor_source_transport_retention_note` | positive_theorem | unaudited | critical | 532 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_tensor_source_transport_retention.py` |
| 35 | `universal_gr_curvature_localization_blocker_note` | positive_theorem | unaudited | critical | 532 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 532 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 37 | `causal_field_canonical_chain_note` | positive_theorem | unaudited | critical | 532 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `complex_selectivity_predictor_note` | positive_theorem | unaudited | critical | 532 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py` |
| 39 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 531 | 25.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 40 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 531 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 41 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 531 | 16.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 531 | 16.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `universal_qg_canonical_textbook_continuum_gr_closure_note` | positive_theorem | unaudited | critical | 531 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | positive_theorem | unaudited | critical | 531 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `universal_qg_smooth_gravitational_local_identification_note` | positive_theorem | unaudited | critical | 531 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 531 | 15.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 531 | 15.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 48 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | positive_theorem | unaudited | critical | 531 | 15.05 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `universal_qg_smooth_gravitational_global_atlas_note` | positive_theorem | unaudited | critical | 531 | 14.55 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 531 | 14.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |

## Citation cycle break targets

96 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 3 | 587 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 2 | `cycle-0002` | 4 | 587 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 3 | `cycle-0003` | 5 | 587 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 4 | `cycle-0004` | 6 | 587 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 531 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 531 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 7 | `cycle-0007` | 3 | 531 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 8 | `cycle-0008` | 3 | 531 | `signed_gravity_aps_locked_axiom_extension_note` | critical | unaudited |
| 9 | `cycle-0009` | 3 | 531 | `signed_gravity_aps_boundary_index_chi_probe_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 531 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 531 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 531 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 531 | `signed_gravity_native_boundary_complex_containment_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 531 | `signed_gravity_aps_locked_source_action_proposal_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 531 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | critical | unaudited |
| 16 | `cycle-0016` | 4 | 531 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 17 | `cycle-0017` | 4 | 531 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 18 | `cycle-0018` | 4 | 531 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 19 | `cycle-0019` | 4 | 531 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 531 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 531 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 531 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 531 | `universal_qg_canonical_smooth_gravitational_weak_measure_note` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 531 | `universal_qg_canonical_textbook_continuum_gr_closure_note` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 531 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
