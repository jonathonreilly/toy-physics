# Audit Queue

**Total pending:** 1133
**Ready (all deps already at retained-grade or metadata tiers):** 29

By criticality:
- `critical`: 679
- `high`: 27
- `medium`: 162
- `leaf`: 265

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 426 | 19.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 421 | 12.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `sign_portability_invariant_family_second_grown_derivation_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 411 | 9.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` |
| 4 | `plaquette_v1_picard_fuchs_ode_note_2026-05-05` | bounded_theorem | unaudited | critical | 391 | 12.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py` |
| 5 | `newton_law_derived_note` | bounded_theorem | unaudited | critical | 380 | 14.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 6 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 380 | 9.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 7 | `cpt_exact_note` | positive_theorem | unaudited | critical | 713 | 22.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 8 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 711 | 17.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 9 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 705 | 9.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 10 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 704 | 18.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 11 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 702 | 15.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 12 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 694 | 10.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 13 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 694 | 10.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 14 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 693 | 11.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 15 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 692 | 9.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 16 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 691 | 10.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 17 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 690 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 18 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 690 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 19 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 689 | 15.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 20 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 688 | 18.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 21 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 686 | 16.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 22 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 675 | 30.40 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 23 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 610 | 13.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 24 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 609 | 12.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 25 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 606 | 12.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 26 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 605 | 9.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 27 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 604 | 12.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 28 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 604 | 11.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 29 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 604 | 11.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 30 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 604 | 11.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 31 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 603 | 25.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 32 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 600 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 33 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 598 | 27.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 34 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 582 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 35 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 571 | 18.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 36 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 568 | 10.15 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 567 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 38 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 557 | 11.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 39 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 556 | 35.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 40 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 551 | 17.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 41 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 549 | 27.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 42 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 527 | 24.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 43 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 509 | 10.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 44 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 508 | 17.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 45 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 499 | 10.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 46 | `s3_time_bilinear_tensor_primitive_note` | open_gate | unaudited | critical | 497 | 12.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_primitive.py` |
| 47 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 492 | 17.45 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 492 | 15.95 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `yt_constructive_uv_bridge_note` | bounded_theorem | unaudited | critical | 492 | 13.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_constructive_uv_bridge.py` |
| 50 | `s3_time_bilinear_tensor_action_note` | open_gate | unaudited | critical | 492 | 9.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_action.py` |

## Citation cycle break targets

253 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 382 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 378 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 378 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 378 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 378 | `koide_a1_derivation_status_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 378 | `koide_a1_derivation_status_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 378 | `koide_a1_derivation_status_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 378 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |
| 9 | `cycle-0009` | 2 | 378 | `c3_symmetry_preserved_interpretation_note_2026-05-08` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 378 | `a3_option_c_brannen_rivero_physical_lattice_bounded_obstruction_note_2026-05-08_optc` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 378 | `cosmology_from_mass_spectrum_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 378 | `dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 378 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 378 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 378 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 378 | `koide_a1_derivation_status_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 378 | `neutrino_dirac_z3_support_trichotomy_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 378 | `a3_route2_single_clock_c3_obstruction_note_2026-05-08_r2` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 378 | `a3_route4_spin6_chain_bounded_obstruction_note_2026-05-08_r4` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 378 | `dm_neutrino_source_surface_carrier_side_conclusion_note_2026-04-18` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 378 | `dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_note_2026-04-19` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 378 | `publication.ci3_z3.claims_table` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 378 | `publication.ci3_z3.claims_table` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 378 | `dm_pmns_cp_orientation_parity_reduction_note_2026-04-20` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 378 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
