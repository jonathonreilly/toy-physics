# Audit Queue

**Total pending:** 1253
**Ready (all deps already at retained-grade or metadata tiers):** 97

By criticality:
- `critical`: 703
- `high`: 38
- `medium`: 178
- `leaf`: 334

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `claude_complex_action_grown_companion_note` | bounded_theorem | audit_in_progress | critical | 449 | 13.31 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 2 | `poisson_self_gravity_loop_note` | bounded_theorem | unaudited | critical | 439 | 11.78 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 3 | `hierarchy_effective_potential_endpoint_note` | bounded_theorem | unaudited | critical | 408 | 13.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_effective_potential_endpoint.py` |
| 4 | `newton_law_derived_note` | bounded_theorem | unaudited | critical | 405 | 14.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 5 | `koide_cl3_selector_gap_note_2026-04-19` | bounded_theorem | unaudited | critical | 405 | 10.66 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 6 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 405 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 7 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 405 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 8 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | unaudited | critical | 404 | 14.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 9 | `koide_circulant_wilson_target_note_2026-04-18` | positive_theorem | unaudited | critical | 404 | 10.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 10 | `bound_state_selection_note` | bounded_theorem | unaudited | critical | 404 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bound_state_selection.py` |
| 11 | `wave_static_boundary_sensitivity_note` | bounded_theorem | unaudited | critical | 404 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 12 | `wave_static_matrixfree_fixed_beam_boundary_note` | bounded_theorem | unaudited | critical | 404 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 13 | `cpt_exact_note` | positive_theorem | unaudited | critical | 749 | 23.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 14 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 749 | 19.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 15 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 741 | 10.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 16 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 740 | 18.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 17 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 738 | 15.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 18 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 731 | 11.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 19 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 731 | 10.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 20 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 730 | 11.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 21 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 729 | 10.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 22 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 728 | 11.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 23 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 727 | 14.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 24 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 727 | 14.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 25 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 726 | 15.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 26 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 725 | 19.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 27 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 723 | 16.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 28 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 711 | 30.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 29 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 646 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 30 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 645 | 12.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 31 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 642 | 12.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 32 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 641 | 9.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 33 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 640 | 13.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 34 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 640 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 35 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 640 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 36 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 640 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 37 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 639 | 26.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 38 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 639 | 11.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 39 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 637 | 27.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 40 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 611 | 15.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 41 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 601 | 18.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 42 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 598 | 10.23 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 597 | 11.22 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 44 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 589 | 12.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 45 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 588 | 36.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 46 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 581 | 17.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 47 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 579 | 28.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 48 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 562 | 24.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 49 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 542 | 11.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 50 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 540 | 18.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |

## Citation cycle break targets

225 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 407 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 405 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 403 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 403 | `higher_order_structural_theorems_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 403 | `higher_order_structural_theorems_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 403 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 403 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 403 | `koide_a1_derivation_status_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 403 | `koide_a1_derivation_status_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 403 | `koide_a1_derivation_status_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 403 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |
| 12 | `cycle-0012` | 2 | 403 | `c3_symmetry_preserved_interpretation_note_2026-05-08` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 403 | `a3_option_c_brannen_rivero_physical_lattice_bounded_obstruction_note_2026-05-08_optc` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 403 | `cosmology_from_mass_spectrum_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 403 | `dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 403 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 403 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 403 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 403 | `higher_order_structural_theorems_note` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 403 | `koide_a1_derivation_status_note` | critical | unaudited |
| 21 | `cycle-0021` | 3 | 403 | `neutrino_dirac_z3_support_trichotomy_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 403 | `a3_route2_single_clock_c3_obstruction_note_2026-05-08_r2` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 403 | `a3_route4_spin6_chain_bounded_obstruction_note_2026-05-08_r4` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 403 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 403 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
