# Audit Queue

**Total pending:** 1265
**Ready (all deps already at retained-grade or metadata tiers):** 97

By criticality:
- `critical`: 725
- `high`: 37
- `medium`: 169
- `leaf`: 334

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `claude_complex_action_grown_companion_note` | bounded_theorem | audit_in_progress | critical | 459 | 13.35 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 2 | `poisson_self_gravity_loop_note` | bounded_theorem | audit_in_progress | critical | 449 | 11.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 3 | `gauge_vacuum_plaquette_spatial_environment_transfer_underdetermination_note_2026-04-17` | no_go | audit_in_progress | critical | 430 | 9.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17.py` |
| 4 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | audit_in_progress | critical | 416 | 9.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 5 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 415 | 9.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 6 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | audit_in_progress | critical | 414 | 14.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 7 | `koide_circulant_wilson_target_note_2026-04-18` | bounded_theorem | audit_in_progress | critical | 414 | 10.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 8 | `bound_state_selection_note` | bounded_theorem | audit_in_progress | critical | 414 | 10.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bound_state_selection.py` |
| 9 | `koide_selected_line_local_radian_bridge_no_go_note_2026-04-20` | no_go | audit_in_progress | critical | 414 | 10.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_selected_line_local_radian_bridge_no_go_2026_04_20.py` |
| 10 | `wave_static_boundary_sensitivity_note` | bounded_theorem | audit_in_progress | critical | 414 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 11 | `wave_static_matrixfree_fixed_beam_boundary_note` | bounded_theorem | unaudited | critical | 414 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 12 | `cpt_exact_note` | positive_theorem | unaudited | critical | 758 | 23.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 13 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 758 | 19.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 14 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 750 | 10.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 15 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 749 | 18.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 16 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 747 | 15.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 17 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 740 | 11.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 18 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 740 | 10.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 19 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 739 | 11.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 20 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 738 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 21 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 737 | 11.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 22 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 736 | 14.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 23 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 736 | 14.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 24 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 735 | 15.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 25 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 734 | 19.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 26 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 732 | 16.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 27 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 720 | 30.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 28 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 662 | 13.37 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 29 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 661 | 12.87 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 30 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 658 | 12.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 31 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 657 | 9.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 32 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 656 | 13.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 33 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 656 | 11.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 34 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 656 | 11.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 35 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 656 | 11.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 36 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 655 | 27.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 37 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 648 | 11.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 38 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 646 | 27.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 39 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 621 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 40 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 611 | 18.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 41 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 608 | 10.25 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 607 | 11.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 43 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 599 | 12.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 44 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 598 | 36.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 45 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 591 | 17.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 46 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 589 | 28.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 47 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 571 | 24.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 48 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 552 | 11.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 49 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 550 | 18.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 50 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 539 | 11.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |

## Citation cycle break targets

232 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 9 | 429 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 417 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 415 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 413 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 413 | `higher_order_structural_theorems_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 413 | `higher_order_structural_theorems_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 413 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 413 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 413 | `koide_a1_derivation_status_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 413 | `koide_a1_derivation_status_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 413 | `koide_a1_derivation_status_note` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 413 | `koide_higgs_dressed_resolvent_root_theorem_note_2026-04-20` | critical | unaudited |
| 13 | `cycle-0013` | 2 | 413 | `koide_higgs_dressed_resolvent_root_theorem_note_2026-04-20` | critical | unaudited |
| 14 | `cycle-0014` | 2 | 413 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |
| 15 | `cycle-0015` | 2 | 413 | `pmns_selector_three_identity_support_note_2026-04-21` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 413 | `pmns_selector_three_identity_support_note_2026-04-21` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 413 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 413 | `c3_symmetry_preserved_interpretation_note_2026-05-08` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 413 | `a3_option_c_brannen_rivero_physical_lattice_bounded_obstruction_note_2026-05-08_optc` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 413 | `cosmology_from_mass_spectrum_note` | critical | unaudited |
| 21 | `cycle-0021` | 3 | 413 | `dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 413 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 413 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 24 | `cycle-0024` | 3 | 413 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 25 | `cycle-0025` | 3 | 413 | `higher_order_structural_theorems_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
