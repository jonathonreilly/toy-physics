# Audit Queue

**Total pending:** 1299
**Ready (all deps already at retained-grade or metadata tiers):** 123

By criticality:
- `critical`: 757
- `high`: 33
- `medium`: 167
- `leaf`: 342

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_lattice_noether_theorem_note_2026-04-29` | bounded_theorem | audit_in_progress | critical | 771 | 17.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_lattice_noether_check.py` |
| 2 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | audit_in_progress | critical | 726 | 13.01 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 3 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | audit_in_progress | critical | 726 | 11.51 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 4 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | audit_in_progress | critical | 724 | 12.00 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 5 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | audit_in_progress | critical | 724 | 12.00 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 6 | `s3_taste_cube_decomposition_note` | bounded_theorem | audit_in_progress | critical | 640 | 15.82 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 7 | `source_driven_field_recovery_sweep_note` | bounded_theorem | audit_in_progress | critical | 489 | 9.44 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_driven_field_recovery_sweep.py` |
| 8 | `source_resolved_exact_green_self_consistent_note` | bounded_theorem | audit_in_progress | critical | 473 | 9.39 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_self_consistent.py` |
| 9 | `claude_complex_action_grown_companion_note` | bounded_theorem | audit_in_progress | critical | 469 | 13.88 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 10 | `gravitomagnetic_note` | bounded_theorem | audit_in_progress | critical | 448 | 9.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravitomagnetic_portable.py` |
| 11 | `gauge_vacuum_plaquette_spatial_environment_transfer_underdetermination_note_2026-04-17` | no_go | audit_in_progress | critical | 439 | 9.78 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17.py` |
| 12 | `valley_linear_action_note` | bounded_theorem | audit_in_progress | critical | 432 | 11.76 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/valley_linear_same_harness_compare.py` |
| 13 | `dimensional_gravity_table` | bounded_theorem | audit_in_progress | critical | 430 | 11.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/dimensional_gravity_table_certificate_runner_2026_05_03.py` |
| 14 | `kubo_continuum_limit_note` | bounded_theorem | audit_in_progress | critical | 430 | 10.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/kubo_continuum_limit.py` |
| 15 | `action_crossover_note` | bounded_theorem | audit_in_progress | critical | 429 | 9.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/action_regularity_crossover.py` |
| 16 | `valley_linear_asymptotic_bridge_note` | bounded_theorem | audit_in_progress | critical | 428 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/valley_linear_asymptotic_bridge.py` |
| 17 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | audit_in_progress | critical | 425 | 9.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 18 | `koide_q_so2_phase_erasure_support_note_2026-04-25` | bounded_theorem | unaudited | critical | 424 | 13.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_so2_phase_erasure_support.py` |
| 19 | `hierarchy_matsubara_determinant_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 424 | 12.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_matsubara_determinant_narrow.py` |
| 20 | `koide_full_lattice_schur_inheritance_note_2026-04-18` | bounded_theorem | unaudited | critical | 424 | 12.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_full_lattice_schur_inheritance.py` |
| 21 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 424 | 9.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 22 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | audit_in_progress | critical | 423 | 14.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 23 | `koide_circulant_wilson_target_note_2026-04-18` | bounded_theorem | audit_in_progress | critical | 423 | 10.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 24 | `bound_state_selection_note` | bounded_theorem | audit_in_progress | critical | 423 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bound_state_selection.py` |
| 25 | `koide_selected_line_local_radian_bridge_no_go_note_2026-04-20` | no_go | audit_in_progress | critical | 423 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_selected_line_local_radian_bridge_no_go_2026_04_20.py` |
| 26 | `pmns_c3_character_mode_reduction_note` | bounded_theorem | unaudited | critical | 423 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_c3_character_mode_reduction.py` |
| 27 | `koide_taste_cube_cyclic_source_descent_note_2026-04-18` | bounded_theorem | unaudited | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_taste_cube_cyclic_source_descent.py` |
| 28 | `quark_bicac_endpoint_obstruction_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bicac_endpoint_obstruction_theorem.py` |
| 29 | `quark_bimodule_norm_naturality_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bimodule_norm_naturality_theorem.py` |
| 30 | `wave_static_boundary_sensitivity_note` | bounded_theorem | audit_in_progress | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 31 | `wave_static_matrixfree_fixed_beam_boundary_note` | bounded_theorem | audit_in_progress | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 32 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 776 | 19.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 33 | `cpt_exact_note` | positive_theorem | unaudited | critical | 774 | 23.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 34 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 766 | 10.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 35 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 765 | 18.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 36 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 763 | 15.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 37 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 756 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 38 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 756 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 39 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 755 | 11.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 40 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 754 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 41 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 753 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 42 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 752 | 14.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 43 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 752 | 14.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 44 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 751 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 45 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 750 | 19.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 46 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 748 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 47 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 736 | 30.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 48 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 730 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 49 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 729 | 13.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 50 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 725 | 10.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |

## Citation cycle break targets

257 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 550 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 550 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 550 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 550 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 550 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 550 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 7 | `cycle-0007` | 3 | 550 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 8 | `cycle-0008` | 4 | 550 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 550 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 550 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 11 | `cycle-0011` | 8 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 12 | `cycle-0012` | 9 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 13 | `cycle-0013` | 9 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 14 | `cycle-0014` | 9 | 550 | `yt_bridge_uv_class_uniqueness_note` | critical | unaudited |
| 15 | `cycle-0015` | 9 | 550 | `yt_bridge_uv_class_uniqueness_note` | critical | unaudited |
| 16 | `cycle-0016` | 10 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 17 | `cycle-0017` | 10 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 18 | `cycle-0018` | 10 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 19 | `cycle-0019` | 10 | 550 | `yt_boundary_theorem` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 472 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 472 | `source_resolved_exact_green_pocket_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 472 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 439 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 24 | `cycle-0024` | 9 | 438 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 429 | `pmns_active_four_real_source_from_transport_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
