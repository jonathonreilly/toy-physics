# Audit Queue

**Total pending:** 874
**Ready (all deps already at retained-grade or metadata tiers):** 7

By criticality:
- `critical`: 566
- `high`: 23
- `medium`: 113
- `leaf`: 172

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03` | no_go | unaudited | critical | 453 | 10.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_observable_bridge_no_go.py` |
| 2 | `plaquette_closure_mathematical_probes_note_2026-05-05` | bounded_theorem | unaudited | critical | 443 | 10.29 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 3 | `su3_fusion_engine_pr1_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 443 | 9.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_fusion_engine.py` |
| 4 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 308 | 10.77 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 5 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 6 | `persistent_object_top4_multistage_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 288 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 7 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 8 | `g_bare_derivation_note` | positive_theorem | unaudited | critical | 453 | 15.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 9 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 447 | 13.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 10 | `gauge_scalar_temporal_observable_bridge_stretch_note_2026-05-02` | open_gate | unaudited | critical | 444 | 9.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_temporal_observable_bridge_stretch.py` |
| 11 | `cpt_exact_note` | positive_theorem | unaudited | critical | 443 | 17.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 443 | 12.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 13 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 443 | 11.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 14 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 443 | 11.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 15 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 443 | 11.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 16 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 443 | 11.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 17 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 443 | 11.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 18 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 442 | 21.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 19 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 442 | 13.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 20 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 442 | 12.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 21 | `born_scattering_comparison_note` | positive_theorem | unaudited | critical | 442 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gaussian_beam_eikonal.py` |
| 22 | `chain_refactoring_bare_to_pdg_note_2026-05-05` | bounded_theorem | unaudited | critical | 442 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `su3_low_rank_irrep_picard_fuchs_odes_note_2026-05-05` | positive_theorem | unaudited | critical | 442 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_low_rank_picard_fuchs_odes_2026_05_05.py` |
| 24 | `plaquette_minimal_block_closed_form_note_2026-05-05` | positive_theorem | unaudited | critical | 442 | 10.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `theorem3_deep_audit_loophole_note_2026-05-06` | no_go | unaudited | critical | 442 | 10.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `chain_closure_44ppm_brainstorm_note_2026-05-05` | positive_theorem | unaudited | critical | 442 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `chain_closure_derivation_blocked_note_2026-05-05` | bounded_theorem | unaudited | critical | 442 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `plaquette_4d_mc_fss_numerical_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 442 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_4d_plaquette_fss_verify_2026_05_05.py` |
| 29 | `plaquette_4d_mc_support_note_2026-05-04` | bounded_theorem | unaudited | critical | 442 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_4d_mc_support_2026_05_04.py` |
| 30 | `route1_v2_onset_reduced_note_2026-05-06` | bounded_theorem | unaudited | critical | 442 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `su3_bridge_pr525_flaw_fix_note_2026-05-05` | positive_theorem | unaudited | critical | 442 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 32 | `su3_cube_perron_solve_combined_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 442 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_perron_solve.py` |
| 33 | `chain_closure_9ppm_brainstorm_note_2026-05-05` | bounded_theorem | unaudited | critical | 442 | 9.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `chain_residual_2loop_lattice_artifact_note_2026-05-05` | positive_theorem | unaudited | critical | 442 | 9.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 35 | `chain_residual_precision_correction_note_2026-05-05` | positive_theorem | unaudited | critical | 442 | 9.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | open_gate | unaudited | critical | 442 | 9.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py` |
| 37 | `route2_lpt_deep_audit_note_2026-05-06` | positive_theorem | unaudited | critical | 442 | 9.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` | open_gate | unaudited | critical | 442 | 9.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py` |
| 39 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 438 | 14.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 40 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 438 | 14.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 41 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 438 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 42 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 438 | 12.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 43 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 437 | 25.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 44 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 437 | 16.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 45 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 437 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 437 | 14.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 47 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 437 | 14.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 48 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 437 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 49 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 437 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 50 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 437 | 13.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |

## Citation cycle break targets

176 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 442 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 2 | `cycle-0002` | 7 | 442 | `chain_closure_44ppm_brainstorm_note_2026-05-05` | critical | unaudited |
| 3 | `cycle-0003` | 8 | 442 | `chain_closure_44ppm_brainstorm_note_2026-05-05` | critical | unaudited |
| 4 | `cycle-0004` | 8 | 442 | `chain_closure_44ppm_brainstorm_note_2026-05-05` | critical | unaudited |
| 5 | `cycle-0005` | 9 | 442 | `chain_closure_44ppm_brainstorm_note_2026-05-05` | critical | unaudited |
| 6 | `cycle-0006` | 10 | 442 | `chain_closure_44ppm_brainstorm_note_2026-05-05` | critical | unaudited |
| 7 | `cycle-0007` | 10 | 442 | `chain_closure_44ppm_brainstorm_note_2026-05-05` | critical | unaudited |
| 8 | `cycle-0008` | 11 | 442 | `chain_closure_44ppm_brainstorm_note_2026-05-05` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 437 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 10 | `cycle-0010` | 7 | 437 | `anomaly_forces_time_theorem` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 321 | `yt_explicit_systematic_budget_note` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 319 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 13 | `cycle-0013` | 2 | 319 | `universal_qg_projective_schur_closure_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 319 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 302 | `higgs_from_lattice_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 302 | `higgs_mass_derived_note` | critical | audited_conditional |
| 17 | `cycle-0017` | 2 | 298 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 289 | `universal_gr_tensor_quotient_uniqueness_note` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 288 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 288 | `koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 288 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 288 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 287 | `charged_lepton_ue_identity_via_z3_trichotomy_note_2026-04-17` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 287 | `quark_issr1_bicac_forcing_theorem_note_2026-04-19` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 286 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
