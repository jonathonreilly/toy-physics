# Audit Queue

**Total pending:** 1169
**Ready (all deps already at retained-grade or metadata tiers):** 106

By criticality:
- `critical`: 712
- `high`: 27
- `medium`: 152
- `leaf`: 278

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 407 | 17.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 393 | 11.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 375 | 11.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 4 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 352 | 9.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 5 | `koide_circulant_character_bridge_narrow_theorem_note_2026-05-09` | positive_theorem | audit_in_progress | critical | 351 | 10.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_character_bridge_narrow.py` |
| 6 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 351 | 10.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 7 | `koide_delta_lattice_wilson_selected_eigenline_no_go_note_2026-04-24` | no_go | unaudited | critical | 351 | 9.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py` |
| 8 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | bounded_theorem | unaudited | critical | 351 | 9.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py` |
| 9 | `circulant_parity_cp_tensor_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_parity_cp_tensor_narrow.py` |
| 10 | `dm_abcc_signature_forcing_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_signature_forcing_theorem.py` |
| 11 | `dm_neutrino_triplet_even_response_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_triplet_even_response_theorem.py` |
| 12 | `dm_pmns_asymptotic_source_no_go_note_2026-04-20` | no_go | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py` |
| 13 | `dm_strong_cp_gamma_transfer_no_go_note_2026-04-15` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_strong_cp_gamma_transfer_nogo.py` |
| 14 | `koide_a1_loop_final_status_2026-04-22` | bounded_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_quartic_potential_derivation.py` |
| 15 | `koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_orbit_cyclic_return_candidate.py` |
| 16 | `wave_static_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 17 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 18 | `wave_static_fixed_beam_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_fixed_beam_boundary_sensitivity.py` |
| 19 | `wave_static_matrixfree_fixed_beam_boundary_note` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 20 | `wave_static_single_source_compare_note` | bounded_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_single_source_compare.py` |
| 21 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 350 | 14.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 22 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 706 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 23 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 702 | 11.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 24 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 700 | 27.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 25 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 697 | 23.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 26 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 697 | 10.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 27 | `cpt_exact_note` | positive_theorem | unaudited | critical | 695 | 21.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 28 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 692 | 13.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 29 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 690 | 15.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 30 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 690 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 690 | 10.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 32 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 690 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 33 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 689 | 18.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 34 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 689 | 15.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 35 | `poisson_exhaustive_uniqueness_note` | bounded_theorem | unaudited | critical | 689 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 36 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 689 | 11.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 37 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 688 | 17.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 688 | 16.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 39 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 688 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 40 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 688 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 41 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 688 | 13.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 42 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 688 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 43 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 687 | 18.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 44 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 687 | 15.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 45 | `universal_qg_inverse_limit_closure_note` | bounded_theorem | unaudited | critical | 687 | 14.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 687 | 10.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 47 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 687 | 10.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 48 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 687 | 10.43 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 686 | 30.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 50 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 686 | 22.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |

## Citation cycle break targets

304 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 697 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 688 | `bh_entropy_derived_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 686 | `3d_correction_master_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 686 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 686 | `architecture_note_directional_measure` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 686 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 686 | `discrete_einstein_regge_lift_note` | critical | unaudited |
| 8 | `cycle-0008` | 3 | 686 | `area_law_coefficient_gap_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 686 | `area_law_coefficient_gap_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 686 | `area_law_coefficient_gap_note` | critical | unaudited |
| 11 | `cycle-0011` | 5 | 686 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 12 | `cycle-0012` | 6 | 686 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 13 | `cycle-0013` | 7 | 686 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 14 | `cycle-0014` | 13 | 686 | `anomaly_forces_time_theorem` | critical | unaudited |
| 15 | `cycle-0015` | 14 | 686 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 631 | `su3_casimir_fundamental_algebraic_k1_k3_narrow_proof_walk_bounded_note_2026-05-10` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 628 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 628 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 628 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 628 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 21 | `cycle-0021` | 6 | 628 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 22 | `cycle-0022` | 7 | 628 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 23 | `cycle-0023` | 8 | 628 | `alpha_s_derived_note` | critical | unaudited |
| 24 | `cycle-0024` | 8 | 628 | `alpha_s_derived_note` | critical | unaudited |
| 25 | `cycle-0025` | 8 | 628 | `alpha_s_derived_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
