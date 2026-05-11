# Audit Queue

**Total pending:** 1103
**Ready (all deps already at retained-grade or metadata tiers):** 7

By criticality:
- `critical`: 678
- `high`: 27
- `medium`: 158
- `leaf`: 240

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 420 | 19.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 415 | 12.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `sign_portability_invariant_family_second_grown_derivation_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 405 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` |
| 4 | `plaquette_v1_picard_fuchs_ode_note_2026-05-05` | bounded_theorem | unaudited | critical | 385 | 12.09 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py` |
| 5 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 374 | 9.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 6 | `cpt_exact_note` | positive_theorem | unaudited | critical | 704 | 21.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 7 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 702 | 17.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 8 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 698 | 9.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 9 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 697 | 18.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 10 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 695 | 15.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 11 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 687 | 10.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 12 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 687 | 10.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 13 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 686 | 11.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 14 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 685 | 9.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 15 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 684 | 10.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 16 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 683 | 14.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 17 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 683 | 14.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 18 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 682 | 15.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 19 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 681 | 18.91 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 20 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 679 | 16.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 21 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 668 | 30.39 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 22 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 602 | 13.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 23 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 601 | 12.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 24 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 598 | 12.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 25 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 597 | 9.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 26 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 596 | 12.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 27 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 596 | 11.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 28 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 596 | 11.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 29 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 596 | 11.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 30 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 595 | 25.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 31 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 592 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 32 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 590 | 27.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 33 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 574 | 15.67 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 34 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 564 | 18.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 35 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 561 | 10.13 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 560 | 11.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 37 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 549 | 11.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 38 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 548 | 35.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 39 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 543 | 15.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 40 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 541 | 27.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 41 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 521 | 24.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 42 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 503 | 10.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 43 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 502 | 17.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 44 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 493 | 10.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 45 | `s3_time_bilinear_tensor_primitive_note` | open_gate | unaudited | critical | 491 | 12.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_primitive.py` |
| 46 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 486 | 17.43 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 486 | 15.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `s3_time_bilinear_tensor_action_note` | open_gate | unaudited | critical | 486 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_action.py` |
| 49 | `ckm_atlas_axiom_closure_note` | positive_theorem | unaudited | critical | 485 | 25.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 50 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 485 | 16.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |

## Citation cycle break targets

253 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 376 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 372 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 372 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 372 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 372 | `koide_a1_derivation_status_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 372 | `koide_a1_derivation_status_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 372 | `koide_a1_derivation_status_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 372 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |
| 9 | `cycle-0009` | 2 | 372 | `c3_symmetry_preserved_interpretation_note_2026-05-08` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 372 | `a3_option_c_brannen_rivero_physical_lattice_bounded_obstruction_note_2026-05-08_optc` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 372 | `cosmology_from_mass_spectrum_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 372 | `dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 372 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 372 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 372 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 372 | `koide_a1_derivation_status_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 372 | `neutrino_dirac_z3_support_trichotomy_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 372 | `a3_route2_single_clock_c3_obstruction_note_2026-05-08_r2` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 372 | `a3_route4_spin6_chain_bounded_obstruction_note_2026-05-08_r4` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 372 | `dm_neutrino_source_surface_carrier_side_conclusion_note_2026-04-18` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 372 | `dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_note_2026-04-19` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 372 | `publication.ci3_z3.claims_table` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 372 | `publication.ci3_z3.claims_table` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 372 | `dm_pmns_cp_orientation_parity_reduction_note_2026-04-20` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 372 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
