# Audit Queue

**Total pending:** 1121
**Ready (all deps already at retained-grade or metadata tiers):** 19

By criticality:
- `critical`: 678
- `high`: 27
- `medium`: 162
- `leaf`: 254

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 425 | 19.23 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 420 | 12.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `sign_portability_invariant_family_second_grown_derivation_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 410 | 9.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` |
| 4 | `plaquette_v1_picard_fuchs_ode_note_2026-05-05` | bounded_theorem | unaudited | critical | 390 | 12.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py` |
| 5 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 379 | 9.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 6 | `cpt_exact_note` | positive_theorem | unaudited | critical | 711 | 22.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 7 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 709 | 17.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 8 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 703 | 9.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 9 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 702 | 18.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 10 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 700 | 15.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 11 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 692 | 10.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 12 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 692 | 10.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 13 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 691 | 11.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 14 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 690 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 15 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 689 | 10.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 16 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 688 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 17 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 688 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 18 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 687 | 15.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 19 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 686 | 18.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 20 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 684 | 16.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 21 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 673 | 30.40 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 22 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 609 | 13.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 23 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 608 | 12.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 24 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 605 | 12.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 25 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 604 | 9.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 26 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 603 | 12.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 27 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 603 | 11.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 28 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 603 | 11.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 29 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 603 | 11.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 30 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 602 | 25.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 31 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 599 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 32 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 597 | 27.22 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 33 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 581 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 34 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 569 | 18.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 35 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 566 | 10.15 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 565 | 11.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 37 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 556 | 11.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 38 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 555 | 35.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 39 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 550 | 17.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 40 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 548 | 27.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 41 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 526 | 24.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 42 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 508 | 10.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 43 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 507 | 17.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 44 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 498 | 10.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 45 | `s3_time_bilinear_tensor_primitive_note` | open_gate | unaudited | critical | 496 | 12.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_primitive.py` |
| 46 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 491 | 17.44 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 491 | 15.94 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `yt_constructive_uv_bridge_note` | bounded_theorem | unaudited | critical | 491 | 13.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_constructive_uv_bridge.py` |
| 49 | `s3_time_bilinear_tensor_action_note` | open_gate | unaudited | critical | 491 | 9.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_action.py` |
| 50 | `ckm_atlas_axiom_closure_note` | positive_theorem | unaudited | critical | 490 | 25.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |

## Citation cycle break targets

253 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 381 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 377 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 377 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 377 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 377 | `koide_a1_derivation_status_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 377 | `koide_a1_derivation_status_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 377 | `koide_a1_derivation_status_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 377 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |
| 9 | `cycle-0009` | 2 | 377 | `c3_symmetry_preserved_interpretation_note_2026-05-08` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 377 | `a3_option_c_brannen_rivero_physical_lattice_bounded_obstruction_note_2026-05-08_optc` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 377 | `cosmology_from_mass_spectrum_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 377 | `dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 377 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 377 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 377 | `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 377 | `koide_a1_derivation_status_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 377 | `neutrino_dirac_z3_support_trichotomy_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 377 | `a3_route2_single_clock_c3_obstruction_note_2026-05-08_r2` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 377 | `a3_route4_spin6_chain_bounded_obstruction_note_2026-05-08_r4` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 377 | `dm_neutrino_source_surface_carrier_side_conclusion_note_2026-04-18` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 377 | `dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_note_2026-04-19` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 377 | `publication.ci3_z3.claims_table` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 377 | `publication.ci3_z3.claims_table` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 377 | `dm_pmns_cp_orientation_parity_reduction_note_2026-04-20` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 377 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
