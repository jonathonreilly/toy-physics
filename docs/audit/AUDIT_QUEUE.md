# Audit Queue

**Total pending:** 1075
**Ready (all deps already at retained-grade or metadata tiers):** 98

By criticality:
- `critical`: 215
- `high`: 319
- `medium`: 279
- `leaf`: 262

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `cluster_decomposition_mass_gap_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 626 | 9.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cluster_decomposition_mass_gap_bridge_check.py` |
| 2 | `boundary_law_robustness_note_2026-04-11` | bounded_theorem | unaudited | critical | 624 | 10.29 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_boundary_law_robustness.py` |
| 3 | `gauge_vacuum_plaquette_rho_pq6_wilson_environment_bounded_note_2026-05-09` | bounded_theorem | unaudited | critical | 539 | 10.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py` |
| 4 | `dm_neutrino_weak_triplet_transfer_class_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 271 | 8.59 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_weak_triplet_transfer_class_theorem.py` |
| 5 | `dm_neutrino_source_surface_bundle_window_trichotomy_candidate_note_2026-04-18` | bounded_theorem | unaudited | critical | 269 | 9.08 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_bundle_window_trichotomy_candidate.py` |
| 6 | `dm_neutrino_source_surface_endpoint_window_bundle_dominance_candidate_note_2026-04-17` | bounded_theorem | unaudited | critical | 269 | 8.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_endpoint_window_bundle_dominance_candidate.py` |
| 7 | `dm_neutrino_source_surface_split1_window_bundle_dominance_candidate_note_2026-04-17` | bounded_theorem | unaudited | critical | 269 | 8.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_split1_window_bundle_dominance_candidate.py` |
| 8 | `dm_neutrino_source_surface_split2_upper_m_slack_floor_endpoint_candidate_note_2026-04-18` | bounded_theorem | unaudited | critical | 269 | 8.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_split2_upper_m_slack_floor_endpoint_candidate.py` |
| 9 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 190 | 15.58 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 10 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 660 | 16.37 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 11 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 633 | 21.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 12 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 633 | 10.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 13 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 631 | 27.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 14 | `cpt_exact_note` | positive_theorem | unaudited | critical | 631 | 20.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 15 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 628 | 10.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 16 | `lensing_combined_invariant_note` | positive_theorem | unaudited | critical | 628 | 10.30 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `3d_correction_master_note` | positive_theorem | unaudited | critical | 628 | 9.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/dispersion_3d_lattice.py` |
| 18 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 626 | 14.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 19 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 626 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 20 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 626 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 21 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 625 | 18.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 22 | `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 625 | 16.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cluster_decomposition_check.py` |
| 23 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 625 | 15.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 24 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 625 | 13.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 25 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 625 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 26 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 624 | 17.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 624 | 14.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 624 | 13.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 29 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 624 | 9.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 30 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 623 | 18.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 31 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 623 | 15.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 32 | `universal_qg_inverse_limit_closure_note` | bounded_theorem | unaudited | critical | 623 | 14.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 623 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 34 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 623 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 35 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 622 | 28.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 36 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 622 | 22.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 37 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 622 | 18.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 38 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 622 | 17.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 39 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 622 | 16.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 40 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 622 | 16.28 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 622 | 16.28 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 622 | 16.28 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 622 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 44 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 622 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | positive_theorem | unaudited | critical | 622 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 622 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `universal_qg_smooth_gravitational_local_identification_note` | positive_theorem | unaudited | critical | 622 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 622 | 15.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 49 | `planck_boundary_density_extension_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 622 | 15.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 50 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | positive_theorem | unaudited | critical | 622 | 15.28 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

173 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 633 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 628 | `3d_correction_master_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 625 | `bh_entropy_derived_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 622 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 622 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 622 | `area_law_coefficient_gap_note` | critical | audited_conditional |
| 7 | `cycle-0007` | 5 | 622 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 8 | `cycle-0008` | 11 | 622 | `anomaly_forces_time_theorem` | critical | unaudited |
| 9 | `cycle-0009` | 12 | 622 | `anomaly_forces_time_theorem` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 528 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 528 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 528 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 13 | `cycle-0013` | 6 | 528 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 14 | `cycle-0014` | 7 | 528 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 15 | `cycle-0015` | 8 | 528 | `alpha_s_derived_note` | critical | audited_conditional |
| 16 | `cycle-0016` | 8 | 528 | `alpha_s_derived_note` | critical | audited_conditional |
| 17 | `cycle-0017` | 8 | 528 | `alpha_s_derived_note` | critical | audited_conditional |
| 18 | `cycle-0018` | 8 | 528 | `alpha_s_derived_note` | critical | audited_conditional |
| 19 | `cycle-0019` | 2 | 308 | `hypercharge_identification_note` | critical | unaudited |
| 20 | `cycle-0020` | 5 | 268 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 21 | `cycle-0021` | 5 | 268 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 22 | `cycle-0022` | 5 | 268 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 23 | `cycle-0023` | 5 | 268 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 24 | `cycle-0024` | 5 | 268 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 25 | `cycle-0025` | 5 | 268 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
