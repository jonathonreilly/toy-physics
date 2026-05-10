# Audit Queue

**Total pending:** 1175
**Ready (all deps already at retained-grade or metadata tiers):** 112

By criticality:
- `critical`: 719
- `high`: 26
- `medium`: 153
- `leaf`: 277

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 407 | 17.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 393 | 11.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 375 | 11.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 4 | `gravity_law_cleanup_note` | bounded_theorem | unaudited | critical | 352 | 9.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravity_distance_fixed_geometry.py` |
| 5 | `dm_abcc_pmns_nonsingularity_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 352 | 9.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_pmns_nonsingularity_theorem.py` |
| 6 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 352 | 9.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 7 | `pmns_three_flux_holonomy_closure_note` | bounded_theorem | unaudited | critical | 352 | 9.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_three_flux_holonomy_closure.py` |
| 8 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 352 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 9 | `cl3_quark_antiquark_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 352 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_quark_antiquark_color_singlet_check.py` |
| 10 | `staggered_3d_self_gravity_sign_note_2026-04-11` | bounded_theorem | unaudited | critical | 352 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_3d_self_gravity_sign.py` |
| 11 | `charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26` | no_go | unaudited | critical | 351 | 12.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py` |
| 12 | `koide_circulant_character_bridge_narrow_theorem_note_2026-05-09` | positive_theorem | unaudited | critical | 351 | 10.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_character_bridge_narrow.py` |
| 13 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 351 | 10.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 14 | `koide_delta_lattice_wilson_selected_eigenline_no_go_note_2026-04-24` | no_go | unaudited | critical | 351 | 9.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py` |
| 15 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | bounded_theorem | unaudited | critical | 351 | 9.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py` |
| 16 | `circulant_parity_cp_tensor_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_parity_cp_tensor_narrow.py` |
| 17 | `dm_neutrino_triplet_even_response_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_triplet_even_response_theorem.py` |
| 18 | `dm_pmns_asymptotic_source_no_go_note_2026-04-20` | no_go | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py` |
| 19 | `dm_strong_cp_gamma_transfer_no_go_note_2026-04-15` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_strong_cp_gamma_transfer_nogo.py` |
| 20 | `koide_a1_loop_final_status_2026-04-22` | bounded_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_quartic_potential_derivation.py` |
| 21 | `koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_orbit_cyclic_return_candidate.py` |
| 22 | `wave_static_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 23 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 24 | `wave_static_fixed_beam_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_fixed_beam_boundary_sensitivity.py` |
| 25 | `wave_static_matrixfree_fixed_beam_boundary_note` | positive_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 26 | `wave_static_single_source_compare_note` | bounded_theorem | unaudited | critical | 351 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_single_source_compare.py` |
| 27 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 350 | 14.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 28 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 705 | 16.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 29 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 701 | 11.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 30 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 699 | 27.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 31 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 696 | 23.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 32 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 696 | 10.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 33 | `cpt_exact_note` | positive_theorem | unaudited | critical | 694 | 21.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 34 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 691 | 13.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 35 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 689 | 15.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 36 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 689 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 689 | 10.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 38 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 689 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 39 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 688 | 18.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 40 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 688 | 15.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `poisson_exhaustive_uniqueness_note` | bounded_theorem | unaudited | critical | 688 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 42 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 688 | 11.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 43 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 687 | 17.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 687 | 16.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 687 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 46 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 687 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 47 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 687 | 13.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 48 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 687 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 49 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 686 | 18.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 50 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 686 | 15.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |

## Citation cycle break targets

304 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 696 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 687 | `bh_entropy_derived_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 685 | `3d_correction_master_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 685 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 685 | `architecture_note_directional_measure` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 685 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 685 | `discrete_einstein_regge_lift_note` | critical | unaudited |
| 8 | `cycle-0008` | 3 | 685 | `area_law_coefficient_gap_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 685 | `area_law_coefficient_gap_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 685 | `area_law_coefficient_gap_note` | critical | unaudited |
| 11 | `cycle-0011` | 5 | 685 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 12 | `cycle-0012` | 6 | 685 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 13 | `cycle-0013` | 7 | 685 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 14 | `cycle-0014` | 13 | 685 | `anomaly_forces_time_theorem` | critical | unaudited |
| 15 | `cycle-0015` | 14 | 685 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 630 | `su3_casimir_fundamental_algebraic_k1_k3_narrow_proof_walk_bounded_note_2026-05-10` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 627 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 627 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 627 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 627 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 21 | `cycle-0021` | 6 | 627 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 22 | `cycle-0022` | 7 | 627 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 23 | `cycle-0023` | 8 | 627 | `alpha_s_derived_note` | critical | unaudited |
| 24 | `cycle-0024` | 8 | 627 | `alpha_s_derived_note` | critical | unaudited |
| 25 | `cycle-0025` | 8 | 627 | `alpha_s_derived_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
