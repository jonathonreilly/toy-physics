# Audit Queue

**Total pending:** 1307
**Ready (all deps already at retained-grade or metadata tiers):** 134

By criticality:
- `critical`: 763
- `high`: 33
- `medium`: 168
- `leaf`: 343

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
| 7 | `claude_complex_action_grown_companion_note` | bounded_theorem | audit_in_progress | critical | 469 | 13.88 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 8 | `poisson_self_gravity_loop_note` | bounded_theorem | audit_in_progress | critical | 463 | 12.36 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 9 | `gravitomagnetic_note` | bounded_theorem | audit_in_progress | critical | 448 | 9.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravitomagnetic_portable.py` |
| 10 | `dark_energy_eos_note` | bounded_theorem | unaudited | critical | 440 | 10.29 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dark_energy_eos.py` |
| 11 | `one_parameter_reduced_shell_law_note` | bounded_theorem | unaudited | critical | 439 | 10.78 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_one_parameter_reduced_shell_law.py` |
| 12 | `gauge_vacuum_plaquette_spatial_environment_transfer_underdetermination_note_2026-04-17` | no_go | audit_in_progress | critical | 439 | 9.78 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17.py` |
| 13 | `valley_linear_action_note` | bounded_theorem | unaudited | critical | 432 | 11.76 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/valley_linear_same_harness_compare.py` |
| 14 | `dimensional_gravity_table` | bounded_theorem | audit_in_progress | critical | 430 | 11.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/dimensional_gravity_table_certificate_runner_2026_05_03.py` |
| 15 | `kubo_continuum_limit_note` | positive_theorem | unaudited | critical | 430 | 10.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/kubo_continuum_limit.py` |
| 16 | `action_crossover_note` | bounded_theorem | audit_in_progress | critical | 429 | 9.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/action_regularity_crossover.py` |
| 17 | `decoherence_action_independence_note` | bounded_theorem | unaudited | critical | 429 | 9.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/decoherence_action_independence.py` |
| 18 | `quark_lane3_bounded_companion_retention_firewall_note_2026-04-27` | bounded_theorem | unaudited | critical | 428 | 11.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py` |
| 19 | `star_supported_bridge_class_note` | positive_theorem | unaudited | critical | 428 | 11.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_star_supported_bridge_class.py` |
| 20 | `valley_linear_asymptotic_bridge_note` | bounded_theorem | audit_in_progress | critical | 428 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/valley_linear_asymptotic_bridge.py` |
| 21 | `hadron_lane1_sqrt_sigma_b2_static_energy_bridge_scout_note_2026-04-30` | positive_theorem | unaudited | critical | 428 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py` |
| 22 | `koide_q_no_hidden_source_audit_2026-04-22` | positive_theorem | unaudited | critical | 427 | 10.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_no_hidden_source_audit.py` |
| 23 | `koide_q_normalized_second_order_effective_action_theorem_2026-04-22` | positive_theorem | unaudited | critical | 427 | 10.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_normalized_second_order_effective_action.py` |
| 24 | `koide_q_reduced_observable_restriction_theorem_2026-04-22` | positive_theorem | unaudited | critical | 427 | 10.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_reduced_observable_restriction_theorem.py` |
| 25 | `pmns_oriented_cycle_selection_structure_note` | positive_theorem | unaudited | critical | 427 | 10.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_oriented_cycle_selection_structure.py` |
| 26 | `koide_q_source_domain_canonical_descent_theorem_note_2026-04-25` | bounded_theorem | unaudited | critical | 426 | 14.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_source_domain_canonical_descent.py` |
| 27 | `axiom_first_coleman_mermin_wagner_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 425 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_coleman_mermin_wagner_check.py` |
| 28 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | audit_in_progress | critical | 425 | 9.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 29 | `pmns_twisted_flux_transfer_holonomy_boundary_note` | bounded_theorem | unaudited | critical | 425 | 9.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_twisted_flux_transfer_holonomy_boundary.py` |
| 30 | `koide_q_so2_phase_erasure_support_note_2026-04-25` | bounded_theorem | unaudited | critical | 424 | 13.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_so2_phase_erasure_support.py` |
| 31 | `koide_full_lattice_schur_inheritance_note_2026-04-18` | bounded_theorem | unaudited | critical | 424 | 12.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_full_lattice_schur_inheritance.py` |
| 32 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 424 | 9.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 33 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | audit_in_progress | critical | 423 | 14.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 34 | `koide_circulant_wilson_target_note_2026-04-18` | bounded_theorem | audit_in_progress | critical | 423 | 10.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 35 | `bound_state_selection_note` | bounded_theorem | audit_in_progress | critical | 423 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bound_state_selection.py` |
| 36 | `koide_selected_line_local_radian_bridge_no_go_note_2026-04-20` | no_go | audit_in_progress | critical | 423 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_selected_line_local_radian_bridge_no_go_2026_04_20.py` |
| 37 | `pmns_c3_character_mode_reduction_note` | bounded_theorem | unaudited | critical | 423 | 10.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_c3_character_mode_reduction.py` |
| 38 | `koide_taste_cube_cyclic_source_descent_note_2026-04-18` | bounded_theorem | unaudited | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_taste_cube_cyclic_source_descent.py` |
| 39 | `quark_bicac_endpoint_obstruction_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bicac_endpoint_obstruction_theorem.py` |
| 40 | `quark_bimodule_norm_naturality_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_bimodule_norm_naturality_theorem.py` |
| 41 | `wave_static_boundary_sensitivity_note` | bounded_theorem | audit_in_progress | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 42 | `wave_static_matrixfree_fixed_beam_boundary_note` | bounded_theorem | audit_in_progress | critical | 423 | 9.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 43 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 776 | 19.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 44 | `cpt_exact_note` | positive_theorem | unaudited | critical | 774 | 23.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 45 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 766 | 10.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 46 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 765 | 18.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 47 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 763 | 15.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 48 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 756 | 11.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 49 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 756 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 50 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 755 | 11.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |

## Citation cycle break targets

254 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

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
| 20 | `cycle-0020` | 3 | 439 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 21 | `cycle-0021` | 9 | 438 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 22 | `cycle-0022` | 2 | 429 | `pmns_active_four_real_source_from_transport_note` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 426 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 424 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 422 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
