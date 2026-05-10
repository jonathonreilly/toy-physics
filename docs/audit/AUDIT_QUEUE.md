# Audit Queue

**Total pending:** 1093
**Ready (all deps already at retained-grade or metadata tiers):** 8

By criticality:
- `critical`: 694
- `high`: 26
- `medium`: 150
- `leaf`: 223

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_casimir_fundamental_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 651 | 15.85 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/su3_casimir_fundamental_check.py` |
| 2 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 423 | 17.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 3 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 409 | 12.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 4 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 368 | 9.53 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 5 | `minimal_source_driven_field_probe_note` | bounded_theorem | unaudited | critical | 733 | 11.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_source_driven_field_probe.py` |
| 6 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 725 | 17.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 7 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 723 | 11.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 8 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 721 | 27.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 9 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 714 | 23.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 10 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 714 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 11 | `cpt_exact_note` | positive_theorem | unaudited | critical | 713 | 21.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 12 | `poisson_self_gravity_loop_note` | bounded_theorem | unaudited | critical | 712 | 12.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 13 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 711 | 15.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 14 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 709 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 15 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 707 | 14.47 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 16 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 707 | 10.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 17 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 707 | 9.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 18 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 706 | 18.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 19 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 706 | 15.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 20 | `poisson_exhaustive_uniqueness_note` | bounded_theorem | unaudited | critical | 706 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 21 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 706 | 11.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 22 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 705 | 17.96 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 705 | 16.96 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 24 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 705 | 14.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 25 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 705 | 13.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 26 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 705 | 13.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 27 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 705 | 9.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 28 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 704 | 18.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 29 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 704 | 15.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 30 | `universal_qg_inverse_limit_closure_note` | bounded_theorem | unaudited | critical | 704 | 14.96 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 704 | 10.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 32 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 704 | 10.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 33 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 704 | 10.46 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 703 | 30.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 35 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 703 | 22.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 36 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 703 | 19.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 37 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 703 | 18.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 38 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 703 | 18.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 39 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 703 | 17.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 40 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 703 | 16.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 41 | `planck_boundary_density_extension_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 703 | 16.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 42 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 703 | 16.46 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 703 | 16.46 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 703 | 16.46 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 703 | 15.96 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | positive_theorem | unaudited | critical | 703 | 15.96 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 703 | 15.96 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `universal_qg_smooth_gravitational_local_identification_note` | positive_theorem | unaudited | critical | 703 | 15.96 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 703 | 15.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 50 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 703 | 15.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |

## Citation cycle break targets

304 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 714 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 705 | `bh_entropy_derived_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 703 | `3d_correction_master_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 703 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 703 | `architecture_note_directional_measure` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 703 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 703 | `discrete_einstein_regge_lift_note` | critical | unaudited |
| 8 | `cycle-0008` | 3 | 703 | `area_law_coefficient_gap_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 703 | `area_law_coefficient_gap_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 703 | `area_law_coefficient_gap_note` | critical | unaudited |
| 11 | `cycle-0011` | 5 | 703 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 12 | `cycle-0012` | 6 | 703 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 13 | `cycle-0013` | 7 | 703 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 14 | `cycle-0014` | 13 | 703 | `anomaly_forces_time_theorem` | critical | unaudited |
| 15 | `cycle-0015` | 14 | 703 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 649 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 649 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 649 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | critical | unaudited |
| 19 | `cycle-0019` | 3 | 649 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 20 | `cycle-0020` | 6 | 649 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 21 | `cycle-0021` | 7 | 649 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 22 | `cycle-0022` | 8 | 649 | `alpha_s_derived_note` | critical | unaudited |
| 23 | `cycle-0023` | 8 | 649 | `alpha_s_derived_note` | critical | unaudited |
| 24 | `cycle-0024` | 8 | 649 | `alpha_s_derived_note` | critical | unaudited |
| 25 | `cycle-0025` | 8 | 649 | `alpha_s_derived_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
