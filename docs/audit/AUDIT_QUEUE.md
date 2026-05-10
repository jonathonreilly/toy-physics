# Audit Queue

**Total pending:** 1100
**Ready (all deps already at retained-grade or metadata tiers):** 8

By criticality:
- `critical`: 695
- `high`: 26
- `medium`: 152
- `leaf`: 227

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 427 | 17.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 2 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 413 | 12.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 3 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 372 | 9.54 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 4 | `minimal_source_driven_field_probe_note` | bounded_theorem | unaudited | critical | 737 | 11.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_source_driven_field_probe.py` |
| 5 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 729 | 17.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 6 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 727 | 11.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 7 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 725 | 27.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 8 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 718 | 23.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 9 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 718 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 10 | `cpt_exact_note` | positive_theorem | unaudited | critical | 717 | 21.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 11 | `poisson_self_gravity_loop_note` | bounded_theorem | unaudited | critical | 716 | 12.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 12 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 715 | 15.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 13 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 713 | 13.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 14 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 711 | 14.48 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 15 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 711 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 16 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 711 | 9.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 17 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 710 | 18.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 18 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 710 | 15.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 19 | `poisson_exhaustive_uniqueness_note` | bounded_theorem | unaudited | critical | 710 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 20 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 710 | 11.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 21 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 709 | 17.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 22 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 709 | 17.47 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 709 | 14.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 24 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 709 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 25 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 709 | 13.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 26 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 709 | 9.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 27 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 708 | 18.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 28 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 708 | 15.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 29 | `universal_qg_inverse_limit_closure_note` | bounded_theorem | unaudited | critical | 708 | 14.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 30 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 708 | 10.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 31 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 708 | 10.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 32 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 708 | 10.47 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 707 | 30.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 34 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 707 | 22.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 35 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 707 | 19.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 36 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 707 | 18.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 37 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 707 | 18.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 38 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 707 | 17.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 39 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 707 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 40 | `planck_boundary_density_extension_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 707 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 41 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 707 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 707 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 707 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 707 | 15.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | positive_theorem | unaudited | critical | 707 | 15.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 707 | 15.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `universal_qg_smooth_gravitational_local_identification_note` | positive_theorem | unaudited | critical | 707 | 15.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 707 | 15.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 49 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 707 | 15.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 50 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | positive_theorem | unaudited | critical | 707 | 15.47 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

305 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 718 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 709 | `bh_entropy_derived_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 707 | `3d_correction_master_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 707 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 707 | `architecture_note_directional_measure` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 707 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 707 | `discrete_einstein_regge_lift_note` | critical | unaudited |
| 8 | `cycle-0008` | 3 | 707 | `area_law_coefficient_gap_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 707 | `area_law_coefficient_gap_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 707 | `area_law_coefficient_gap_note` | critical | unaudited |
| 11 | `cycle-0011` | 5 | 707 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 12 | `cycle-0012` | 6 | 707 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 13 | `cycle-0013` | 7 | 707 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 14 | `cycle-0014` | 13 | 707 | `anomaly_forces_time_theorem` | critical | unaudited |
| 15 | `cycle-0015` | 14 | 707 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 656 | `su3_casimir_fundamental_algebraic_k1_k3_narrow_proof_walk_bounded_note_2026-05-10` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 653 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 653 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 653 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 653 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 21 | `cycle-0021` | 6 | 653 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 22 | `cycle-0022` | 7 | 653 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 23 | `cycle-0023` | 8 | 653 | `alpha_s_derived_note` | critical | unaudited |
| 24 | `cycle-0024` | 8 | 653 | `alpha_s_derived_note` | critical | unaudited |
| 25 | `cycle-0025` | 8 | 653 | `alpha_s_derived_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
