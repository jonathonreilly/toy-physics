# Audit Queue

**Total pending:** 1157
**Ready (all deps already at retained-grade or metadata tiers):** 95

By criticality:
- `critical`: 701
- `high`: 27
- `medium`: 151
- `leaf`: 278

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 406 | 17.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 392 | 11.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 351 | 9.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 4 | `koide_circulant_wilson_target_note_2026-04-18` | positive_theorem | unaudited | critical | 350 | 10.46 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_wilson_target.py` |
| 5 | `dm_pmns_asymptotic_source_no_go_note_2026-04-20` | no_go | unaudited | critical | 350 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py` |
| 6 | `dm_strong_cp_gamma_transfer_no_go_note_2026-04-15` | positive_theorem | unaudited | critical | 350 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_strong_cp_gamma_transfer_nogo.py` |
| 7 | `koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18` | positive_theorem | unaudited | critical | 350 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_orbit_cyclic_return_candidate.py` |
| 8 | `wave_static_fixed_beam_boundary_sensitivity_note` | bounded_theorem | audit_in_progress | critical | 350 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_fixed_beam_boundary_sensitivity.py` |
| 9 | `wave_static_matrixfree_fixed_beam_boundary_note` | positive_theorem | unaudited | critical | 350 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 10 | `wave_static_single_source_compare_note` | bounded_theorem | unaudited | critical | 350 | 8.96 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_single_source_compare.py` |
| 11 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 349 | 14.95 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 12 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 705 | 16.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 13 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 701 | 11.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 14 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 699 | 27.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 15 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 696 | 23.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 16 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 696 | 10.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 17 | `cpt_exact_note` | positive_theorem | unaudited | critical | 694 | 21.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 18 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 691 | 13.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 19 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 689 | 15.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 20 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 689 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 689 | 10.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 22 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 689 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 23 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 688 | 18.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 24 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 688 | 15.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `poisson_exhaustive_uniqueness_note` | bounded_theorem | unaudited | critical | 688 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 26 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 688 | 11.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 27 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 687 | 17.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 687 | 16.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 687 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 30 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 687 | 13.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 31 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 687 | 13.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 32 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 687 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 33 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 686 | 18.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 34 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 686 | 15.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 35 | `universal_qg_inverse_limit_closure_note` | bounded_theorem | unaudited | critical | 686 | 14.92 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 686 | 10.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 37 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 686 | 10.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 38 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 686 | 10.42 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 39 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 685 | 30.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 40 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 685 | 22.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 41 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 685 | 19.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 42 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 685 | 18.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 43 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 685 | 18.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 44 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 685 | 17.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 45 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 685 | 16.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 46 | `planck_boundary_density_extension_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 685 | 16.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 47 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 685 | 16.42 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 685 | 16.42 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 685 | 16.42 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 685 | 15.92 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

270 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

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
