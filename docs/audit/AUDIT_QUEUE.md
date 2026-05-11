# Audit Queue

**Total pending:** 1122
**Ready (all deps already at retained-grade or metadata tiers):** 25

By criticality:
- `critical`: 684
- `high`: 27
- `medium`: 157
- `leaf`: 254

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 417 | 18.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 414 | 12.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 373 | 9.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 4 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 724 | 11.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 5 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 722 | 27.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 6 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 714 | 17.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 7 | `cpt_exact_note` | positive_theorem | unaudited | critical | 703 | 21.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 8 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 697 | 9.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 9 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 696 | 18.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 10 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 694 | 15.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 11 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 686 | 10.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 12 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 686 | 10.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 13 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 685 | 11.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 14 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 684 | 9.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 15 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 683 | 10.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 16 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 682 | 14.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 17 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 682 | 14.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 18 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 681 | 15.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 19 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 680 | 18.91 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 20 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 678 | 16.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 21 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 667 | 30.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 22 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 657 | 13.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 23 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 656 | 12.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 24 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 653 | 12.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 25 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 652 | 9.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 26 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 651 | 12.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 27 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 651 | 11.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 28 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 651 | 11.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 29 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 651 | 11.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 30 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 650 | 35.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 31 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 650 | 31.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 32 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 650 | 24.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 33 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | positive_theorem | unaudited | critical | 650 | 12.85 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 650 | 11.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 35 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 650 | 10.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 36 | `g_bare_constraint_vs_convention_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 650 | 10.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 37 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 572 | 15.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 38 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 563 | 18.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 39 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 560 | 10.13 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 559 | 11.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 41 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 542 | 15.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 42 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 540 | 27.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 43 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 520 | 24.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 44 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 502 | 18.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 45 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 502 | 10.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 46 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 492 | 10.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 47 | `s3_time_bilinear_tensor_primitive_note` | open_gate | unaudited | critical | 490 | 12.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_primitive.py` |
| 48 | `s3_time_bilinear_tensor_action_note` | open_gate | unaudited | critical | 490 | 10.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_action.py` |
| 49 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 485 | 17.43 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 485 | 15.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

270 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 8 | 650 | `alpha_s_derived_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 502 | `hypercharge_identification_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 490 | `s3_time_bilinear_tensor_action_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 481 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 481 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 6 | `cycle-0006` | 5 | 481 | `yt_boundary_theorem` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 416 | `minimal_absorbing_horizon_probe_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 404 | `sign_portability_invariant_family_second_grown_derivation_theorem_note_2026-05-09` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 400 | `yt_p2_taste_staircase_beta_functions_note_2026-04-17` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 397 | `wilson_bz_corner_hamming_staircase_bounded_note_2026-05-08` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 13 | `cycle-0013` | 4 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 14 | `cycle-0014` | 4 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 15 | `cycle-0015` | 4 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 16 | `cycle-0016` | 5 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 17 | `cycle-0017` | 5 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 375 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 371 | `dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem_note_2026-04-17` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 371 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 371 | `koide_a1_11_probe_campaign_bounded_admission_meta_note_2026-05-08` | critical | unaudited |
| 22 | `cycle-0022` | 2 | 371 | `koide_a1_derivation_status_note` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 371 | `koide_a1_derivation_status_note` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 371 | `koide_a1_derivation_status_note` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 371 | `neutrino_mass_reduction_to_dirac_note` | critical | audited_conditional |

Full queue lives in `data/audit_queue.json`.
