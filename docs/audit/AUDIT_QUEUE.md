# Audit Queue

**Total pending:** 1247
**Ready (all deps already at retained-grade or metadata tiers):** 100

By criticality:
- `critical`: 698
- `high`: 38
- `medium`: 177
- `leaf`: 334

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `minimal_source_driven_field_probe_note` | bounded_theorem | unaudited | critical | 455 | 10.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_source_driven_field_probe.py` |
| 2 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 448 | 19.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 3 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 444 | 13.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 4 | `sign_portability_invariant_family_second_grown_derivation_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 431 | 9.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` |
| 5 | `plaquette_v1_picard_fuchs_ode_note_2026-05-05` | bounded_theorem | unaudited | critical | 411 | 12.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py` |
| 6 | `hierarchy_effective_potential_endpoint_note` | bounded_theorem | unaudited | critical | 403 | 13.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_effective_potential_endpoint.py` |
| 7 | `newton_law_derived_note` | bounded_theorem | unaudited | critical | 400 | 14.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 8 | `koide_cl3_selector_gap_note_2026-04-19` | bounded_theorem | unaudited | critical | 400 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 400 | 9.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 10 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 400 | 9.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 11 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | unaudited | critical | 399 | 14.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 12 | `koide_circulant_wilson_target_note_2026-04-18` | positive_theorem | unaudited | critical | 399 | 10.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 13 | `bound_state_selection_note` | bounded_theorem | unaudited | critical | 399 | 10.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bound_state_selection.py` |
| 14 | `wave_static_boundary_sensitivity_note` | bounded_theorem | unaudited | critical | 399 | 9.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 15 | `wave_static_matrixfree_fixed_beam_boundary_note` | bounded_theorem | unaudited | critical | 399 | 9.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 16 | `cpt_exact_note` | positive_theorem | unaudited | critical | 739 | 23.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 17 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 739 | 18.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 18 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 731 | 10.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 19 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 730 | 18.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 20 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 728 | 15.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 21 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 721 | 11.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 22 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 721 | 10.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 23 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 720 | 11.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 24 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 719 | 9.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 25 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 718 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 26 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 717 | 14.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 27 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 717 | 14.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 28 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 716 | 15.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 29 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 715 | 18.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 30 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 713 | 16.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 31 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 701 | 30.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 32 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 641 | 13.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 33 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 640 | 12.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 34 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 637 | 12.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 35 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 636 | 9.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 36 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 635 | 13.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 37 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 635 | 11.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 38 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 635 | 11.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 39 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 635 | 11.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 40 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 634 | 26.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 41 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 629 | 11.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 42 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 627 | 27.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 43 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 606 | 15.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 44 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 596 | 18.22 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 45 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 593 | 10.21 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 592 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 47 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 584 | 12.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 48 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 583 | 36.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 49 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 576 | 17.67 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 50 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 574 | 28.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |

## Citation cycle break targets

225 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 402 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 400 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 398 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 398 | `higher_order_structural_theorems_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 398 | `higher_order_structural_theorems_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 398 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 398 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 398 | `koide_a1_derivation_status_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 398 | `koide_a1_derivation_status_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 398 | `koide_a1_derivation_status_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 398 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |
| 12 | `cycle-0012` | 2 | 398 | `c3_symmetry_preserved_interpretation_note_2026-05-08` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 398 | `a3_option_c_brannen_rivero_physical_lattice_bounded_obstruction_note_2026-05-08_optc` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 398 | `cosmology_from_mass_spectrum_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 398 | `dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 398 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 398 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 398 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 398 | `higher_order_structural_theorems_note` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 398 | `koide_a1_derivation_status_note` | critical | unaudited |
| 21 | `cycle-0021` | 3 | 398 | `neutrino_dirac_z3_support_trichotomy_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 398 | `a3_route2_single_clock_c3_obstruction_note_2026-05-08_r2` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 398 | `a3_route4_spin6_chain_bounded_obstruction_note_2026-05-08_r4` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 398 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 398 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
