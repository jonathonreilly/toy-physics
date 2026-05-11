# Audit Queue

**Total pending:** 1249
**Ready (all deps already at retained-grade or metadata tiers):** 99

By criticality:
- `critical`: 702
- `high`: 38
- `medium`: 177
- `leaf`: 332

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 446 | 13.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 2 | `poisson_self_gravity_loop_note` | bounded_theorem | unaudited | critical | 436 | 11.77 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 3 | `sign_portability_invariant_family_second_grown_derivation_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 433 | 9.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` |
| 4 | `plaquette_v1_picard_fuchs_ode_note_2026-05-05` | bounded_theorem | unaudited | critical | 413 | 12.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py` |
| 5 | `hierarchy_effective_potential_endpoint_note` | bounded_theorem | unaudited | critical | 405 | 13.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_effective_potential_endpoint.py` |
| 6 | `newton_law_derived_note` | bounded_theorem | unaudited | critical | 402 | 14.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 7 | `koide_cl3_selector_gap_note_2026-04-19` | bounded_theorem | unaudited | critical | 402 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 402 | 9.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 9 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 402 | 9.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 10 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | unaudited | critical | 401 | 14.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 11 | `koide_circulant_wilson_target_note_2026-04-18` | positive_theorem | unaudited | critical | 401 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 12 | `bound_state_selection_note` | bounded_theorem | unaudited | critical | 401 | 10.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bound_state_selection.py` |
| 13 | `wave_static_boundary_sensitivity_note` | bounded_theorem | unaudited | critical | 401 | 9.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 14 | `wave_static_matrixfree_fixed_beam_boundary_note` | bounded_theorem | unaudited | critical | 401 | 9.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 15 | `cpt_exact_note` | positive_theorem | unaudited | critical | 741 | 23.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 16 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 741 | 18.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 17 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 733 | 10.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 18 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 732 | 18.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 19 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 730 | 15.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 20 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 723 | 11.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 21 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 723 | 10.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 22 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 722 | 11.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 23 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 721 | 10.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 24 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 720 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 25 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 719 | 14.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 26 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 719 | 14.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 27 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 718 | 15.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 28 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 717 | 18.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 29 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 715 | 16.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 30 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 703 | 30.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 31 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 643 | 13.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 32 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 642 | 12.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 33 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 639 | 12.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 34 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 638 | 9.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 35 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 637 | 13.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 36 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 637 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 37 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 637 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 38 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 637 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 39 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 636 | 26.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 40 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 631 | 11.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 41 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 629 | 27.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 42 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 608 | 15.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 43 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 598 | 18.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 44 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 595 | 10.22 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 594 | 11.22 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 46 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 586 | 12.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 47 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 585 | 36.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 48 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 578 | 17.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 49 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 576 | 28.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 50 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 554 | 24.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |

## Citation cycle break targets

225 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 404 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 402 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 400 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 400 | `higher_order_structural_theorems_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 400 | `higher_order_structural_theorems_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 400 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 400 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 400 | `koide_a1_derivation_status_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 400 | `koide_a1_derivation_status_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 400 | `koide_a1_derivation_status_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 400 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |
| 12 | `cycle-0012` | 2 | 400 | `c3_symmetry_preserved_interpretation_note_2026-05-08` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 400 | `a3_option_c_brannen_rivero_physical_lattice_bounded_obstruction_note_2026-05-08_optc` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 400 | `cosmology_from_mass_spectrum_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 400 | `dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 400 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 400 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 400 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 400 | `higher_order_structural_theorems_note` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 400 | `koide_a1_derivation_status_note` | critical | unaudited |
| 21 | `cycle-0021` | 3 | 400 | `neutrino_dirac_z3_support_trichotomy_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 400 | `a3_route2_single_clock_c3_obstruction_note_2026-05-08_r2` | critical | unaudited |
| 23 | `cycle-0023` | 3 | 400 | `a3_route4_spin6_chain_bounded_obstruction_note_2026-05-08_r4` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 400 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 400 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
