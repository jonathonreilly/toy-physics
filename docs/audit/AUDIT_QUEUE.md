# Audit Queue

**Total pending:** 1122
**Ready (all deps already at retained-grade or metadata tiers):** 25

By criticality:
- `critical`: 689
- `high`: 26
- `medium`: 156
- `leaf`: 251

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 429 | 18.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 414 | 12.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 401 | 11.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_canonical_convention_narrow.py` |
| 4 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 382 | 13.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 5 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 373 | 9.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 6 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 723 | 11.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 7 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 721 | 27.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 8 | `cpt_exact_note` | positive_theorem | unaudited | critical | 715 | 21.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 9 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 713 | 17.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 10 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 709 | 9.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 11 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 708 | 18.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 12 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 706 | 15.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 13 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 698 | 10.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 14 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 698 | 10.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 15 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 697 | 11.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 16 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 696 | 9.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 17 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 695 | 10.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 18 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 694 | 14.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 19 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 694 | 14.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 20 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 693 | 15.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 21 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 692 | 18.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 22 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 690 | 16.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 23 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 679 | 30.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 24 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 656 | 13.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 25 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 655 | 12.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 26 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 652 | 12.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 27 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | bounded_theorem | unaudited | critical | 651 | 9.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_hierarchy_obstruction_lemmas.py` |
| 28 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 650 | 12.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 29 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 650 | 11.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 30 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 650 | 11.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 31 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 650 | 11.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 32 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 649 | 35.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 33 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 649 | 31.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 34 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 649 | 24.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 35 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | positive_theorem | unaudited | critical | 649 | 12.84 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 649 | 11.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 37 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 649 | 10.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 38 | `g_bare_constraint_vs_convention_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 649 | 10.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 39 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 575 | 18.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 40 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 572 | 10.16 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 571 | 15.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 42 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 571 | 11.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 43 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 541 | 15.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 44 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 539 | 27.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 45 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 533 | 24.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 46 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 515 | 18.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 47 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 515 | 10.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 48 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 504 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 49 | `s3_time_bilinear_tensor_primitive_note` | open_gate | unaudited | critical | 502 | 12.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_primitive.py` |
| 50 | `s3_time_bilinear_tensor_action_note` | open_gate | unaudited | critical | 502 | 10.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_bilinear_tensor_action.py` |

## Citation cycle break targets

280 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 8 | 649 | `alpha_s_derived_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 515 | `hypercharge_identification_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 502 | `s3_time_bilinear_tensor_action_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 492 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 492 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 6 | `cycle-0006` | 5 | 492 | `yt_boundary_theorem` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 465 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 416 | `minimal_absorbing_horizon_probe_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 411 | `yt_p2_taste_staircase_beta_functions_note_2026-04-17` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 411 | `yt_p2_taste_staircase_beta_functions_note_2026-04-17` | critical | unaudited |
| 11 | `cycle-0011` | 4 | 411 | `yt_p2_taste_staircase_beta_functions_note_2026-04-17` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 404 | `sign_portability_invariant_family_second_grown_derivation_theorem_note_2026-05-09` | critical | unaudited |
| 13 | `cycle-0013` | 2 | 403 | `ckm_from_mass_hierarchy_note` | critical | unaudited |
| 14 | `cycle-0014` | 2 | 397 | `wilson_bz_corner_hamming_staircase_bounded_note_2026-05-08` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 395 | `higgs_mass_from_axiom_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 395 | `higgs_mass_from_axiom_note` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 395 | `higgs_mass_from_axiom_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 395 | `ew_coupling_derivation_note` | critical | unaudited |
| 19 | `cycle-0019` | 4 | 395 | `ew_coupling_derivation_note` | critical | unaudited |
| 20 | `cycle-0020` | 5 | 395 | `complete_prediction_chain_2026_04_15` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 384 | `plaquette_v1_picard_fuchs_ode_all_order_proof_note_2026-05-09` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
