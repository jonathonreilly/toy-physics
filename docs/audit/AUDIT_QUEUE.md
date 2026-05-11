# Audit Queue

**Total pending:** 1287
**Ready (all deps already at retained-grade or metadata tiers):** 130

By criticality:
- `critical`: 752
- `high`: 32
- `medium`: 169
- `leaf`: 334

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_lattice_noether_theorem_note_2026-04-29` | bounded_theorem | audit_in_progress | critical | 760 | 17.07 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_lattice_noether_check.py` |
| 2 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | audit_in_progress | critical | 710 | 12.97 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 3 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | audit_in_progress | critical | 710 | 11.47 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 4 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | audit_in_progress | critical | 708 | 11.97 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 5 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | audit_in_progress | critical | 708 | 11.97 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 6 | `s3_taste_cube_decomposition_note` | bounded_theorem | audit_in_progress | critical | 624 | 15.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 7 | `claude_complex_action_grown_companion_note` | bounded_theorem | audit_in_progress | critical | 459 | 13.35 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 8 | `poisson_self_gravity_loop_note` | bounded_theorem | audit_in_progress | critical | 450 | 12.32 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 9 | `finite_rank_source_to_metric_theorem_note` | bounded_theorem | unaudited | critical | 450 | 10.82 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_finite_rank_source_to_metric_theorem.py` |
| 10 | `yt_zero_import_chain_note` | positive_theorem | unaudited | critical | 442 | 12.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 11 | `scalar_trace_tensor_no_go_note` | bounded_theorem | unaudited | critical | 432 | 10.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_scalar_trace_tensor_nogo.py` |
| 12 | `one_parameter_reduced_shell_law_note` | bounded_theorem | unaudited | critical | 430 | 10.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_one_parameter_reduced_shell_law.py` |
| 13 | `gauge_vacuum_plaquette_spatial_environment_transfer_underdetermination_note_2026-04-17` | no_go | audit_in_progress | critical | 430 | 9.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17.py` |
| 14 | `kubo_continuum_limit_note` | positive_theorem | unaudited | critical | 421 | 10.72 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/kubo_continuum_limit.py` |
| 15 | `quark_lane3_bounded_companion_retention_firewall_note_2026-04-27` | bounded_theorem | unaudited | critical | 419 | 11.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py` |
| 16 | `star_supported_bridge_class_note` | positive_theorem | unaudited | critical | 419 | 11.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_star_supported_bridge_class.py` |
| 17 | `hadron_lane1_sqrt_sigma_b2_static_energy_bridge_scout_note_2026-04-30` | positive_theorem | unaudited | critical | 419 | 9.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py` |
| 18 | `koide_q_no_hidden_source_audit_2026-04-22` | positive_theorem | unaudited | critical | 418 | 10.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_no_hidden_source_audit.py` |
| 19 | `koide_q_normalized_second_order_effective_action_theorem_2026-04-22` | positive_theorem | unaudited | critical | 418 | 10.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_normalized_second_order_effective_action.py` |
| 20 | `koide_q_reduced_observable_restriction_theorem_2026-04-22` | positive_theorem | unaudited | critical | 418 | 10.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_reduced_observable_restriction_theorem.py` |
| 21 | `pmns_oriented_cycle_selection_structure_note` | positive_theorem | unaudited | critical | 418 | 10.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_selection_structure.py` |
| 22 | `koide_q_source_domain_canonical_descent_theorem_note_2026-04-25` | bounded_theorem | unaudited | critical | 417 | 14.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_source_domain_canonical_descent.py` |
| 23 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | audit_in_progress | critical | 416 | 9.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 24 | `pmns_twisted_flux_transfer_holonomy_boundary_note` | bounded_theorem | unaudited | critical | 416 | 9.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_twisted_flux_transfer_holonomy_boundary.py` |
| 25 | `koide_q_so2_phase_erasure_support_note_2026-04-25` | bounded_theorem | unaudited | critical | 415 | 13.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_so2_phase_erasure_support.py` |
| 26 | `koide_full_lattice_schur_inheritance_note_2026-04-18` | bounded_theorem | unaudited | critical | 415 | 12.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_full_lattice_schur_inheritance.py` |
| 27 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 415 | 9.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 28 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | audit_in_progress | critical | 414 | 14.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 29 | `koide_circulant_wilson_target_note_2026-04-18` | bounded_theorem | audit_in_progress | critical | 414 | 10.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 30 | `bound_state_selection_note` | bounded_theorem | audit_in_progress | critical | 414 | 10.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bound_state_selection.py` |
| 31 | `koide_selected_line_local_radian_bridge_no_go_note_2026-04-20` | no_go | audit_in_progress | critical | 414 | 10.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_selected_line_local_radian_bridge_no_go_2026_04_20.py` |
| 32 | `pmns_c3_character_mode_reduction_note` | bounded_theorem | unaudited | critical | 414 | 10.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_c3_character_mode_reduction.py` |
| 33 | `koide_taste_cube_cyclic_source_descent_note_2026-04-18` | bounded_theorem | unaudited | critical | 414 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_taste_cube_cyclic_source_descent.py` |
| 34 | `quark_bicac_endpoint_obstruction_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 414 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bicac_endpoint_obstruction_theorem.py` |
| 35 | `quark_bimodule_norm_naturality_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 414 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bimodule_norm_naturality_theorem.py` |
| 36 | `wave_static_boundary_sensitivity_note` | bounded_theorem | audit_in_progress | critical | 414 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 37 | `wave_static_matrixfree_fixed_beam_boundary_note` | bounded_theorem | audit_in_progress | critical | 414 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 38 | `cpt_exact_note` | positive_theorem | unaudited | critical | 763 | 23.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 39 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 763 | 19.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 40 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 755 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 41 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 754 | 18.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 42 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 752 | 15.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 43 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 745 | 11.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 44 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 745 | 10.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 45 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 744 | 11.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 46 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 743 | 10.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 47 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 742 | 11.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 48 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 741 | 14.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 49 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 741 | 14.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 50 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 740 | 15.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |

## Citation cycle break targets

253 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 541 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 541 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 541 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 541 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 541 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 541 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 7 | `cycle-0007` | 3 | 541 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 8 | `cycle-0008` | 4 | 541 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 541 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 541 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 11 | `cycle-0011` | 8 | 541 | `yt_boundary_theorem` | critical | unaudited |
| 12 | `cycle-0012` | 9 | 541 | `yt_boundary_theorem` | critical | unaudited |
| 13 | `cycle-0013` | 9 | 541 | `yt_boundary_theorem` | critical | unaudited |
| 14 | `cycle-0014` | 9 | 541 | `yt_bridge_uv_class_uniqueness_note` | critical | unaudited |
| 15 | `cycle-0015` | 9 | 541 | `yt_bridge_uv_class_uniqueness_note` | critical | unaudited |
| 16 | `cycle-0016` | 10 | 541 | `yt_boundary_theorem` | critical | unaudited |
| 17 | `cycle-0017` | 10 | 541 | `yt_boundary_theorem` | critical | unaudited |
| 18 | `cycle-0018` | 10 | 541 | `yt_boundary_theorem` | critical | unaudited |
| 19 | `cycle-0019` | 10 | 541 | `yt_boundary_theorem` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 430 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 21 | `cycle-0021` | 9 | 429 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 22 | `cycle-0022` | 2 | 420 | `pmns_active_four_real_source_from_transport_note` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 417 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 415 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 413 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
