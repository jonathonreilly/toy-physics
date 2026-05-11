# Audit Queue

**Total pending:** 1255
**Ready (all deps already at retained-grade or metadata tiers):** 96

By criticality:
- `critical`: 713
- `high`: 37
- `medium`: 169
- `leaf`: 336

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `claude_complex_action_grown_companion_note` | bounded_theorem | audit_in_progress | critical | 450 | 13.32 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 2 | `poisson_self_gravity_loop_note` | bounded_theorem | audit_in_progress | critical | 440 | 11.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 3 | `gauge_vacuum_plaquette_spatial_environment_transfer_underdetermination_note_2026-04-17` | no_go | audit_in_progress | critical | 421 | 9.72 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_first_three_sample_environment_evaluator_route_2026_04_17.py` |
| 4 | `persistent_object_inward_boundary_floor_diagnosis_note_2026-04-16` | bounded_theorem | unaudited | critical | 407 | 9.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 5 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 406 | 9.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 6 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | unaudited | critical | 405 | 14.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 7 | `koide_circulant_wilson_target_note_2026-04-18` | positive_theorem | unaudited | critical | 405 | 10.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 8 | `bound_state_selection_note` | bounded_theorem | unaudited | critical | 405 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bound_state_selection.py` |
| 9 | `wave_static_boundary_sensitivity_note` | bounded_theorem | unaudited | critical | 405 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 10 | `wave_static_matrixfree_fixed_beam_boundary_note` | bounded_theorem | unaudited | critical | 405 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 11 | `cpt_exact_note` | positive_theorem | unaudited | critical | 750 | 23.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 12 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 750 | 19.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 13 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 742 | 10.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 14 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 741 | 18.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 15 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 739 | 15.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 16 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 732 | 11.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 17 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 732 | 10.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 18 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 731 | 11.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 19 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 730 | 10.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 20 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 729 | 11.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 21 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 728 | 14.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 22 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 728 | 14.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 23 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 727 | 15.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 24 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 726 | 19.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 25 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 724 | 16.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 26 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 712 | 30.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 27 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 653 | 13.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 28 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 652 | 12.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 29 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 649 | 12.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 30 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 648 | 9.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 31 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 647 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 32 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 647 | 11.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 33 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 647 | 11.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 34 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 647 | 11.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 35 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 646 | 27.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 36 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 640 | 11.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 37 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 638 | 27.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 38 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 612 | 15.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 39 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 602 | 18.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 40 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 599 | 10.23 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 598 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 42 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 590 | 12.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 43 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 589 | 36.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 44 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 582 | 17.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 45 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 580 | 28.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 46 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 563 | 24.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 47 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 543 | 11.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 48 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 541 | 18.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 49 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 530 | 11.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 50 | `s3_time_bilinear_tensor_primitive_note` | open_gate | unaudited | critical | 528 | 13.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_primitive.py` |

## Citation cycle break targets

224 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 9 | 420 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 408 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 406 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 404 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 404 | `higher_order_structural_theorems_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 404 | `higher_order_structural_theorems_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 404 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 404 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 404 | `koide_a1_derivation_status_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 404 | `koide_a1_derivation_status_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 404 | `koide_a1_derivation_status_note` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 404 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |
| 13 | `cycle-0013` | 2 | 404 | `c3_symmetry_preserved_interpretation_note_2026-05-08` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 404 | `a3_option_c_brannen_rivero_physical_lattice_bounded_obstruction_note_2026-05-08_optc` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 404 | `cosmology_from_mass_spectrum_note` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 404 | `dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 404 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 404 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 404 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 404 | `higher_order_structural_theorems_note` | critical | unaudited |
| 21 | `cycle-0021` | 3 | 404 | `koide_a1_derivation_status_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 404 | `neutrino_dirac_z3_support_trichotomy_note` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 404 | `a3_route2_single_clock_c3_obstruction_note_2026-05-08_r2` | critical | unaudited |
| 24 | `cycle-0024` | 3 | 404 | `a3_route4_spin6_chain_bounded_obstruction_note_2026-05-08_r4` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 404 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
