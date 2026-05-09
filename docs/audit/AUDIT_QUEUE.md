# Audit Queue

**Total pending:** 980
**Ready (all deps already at retained-grade or metadata tiers):** 37

By criticality:
- `critical`: 179
- `high`: 318
- `medium`: 259
- `leaf`: 224

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_vacuum_plaquette_rho_pq6_wilson_environment_bounded_note_2026-05-09` | bounded_theorem | unaudited | critical | 513 | 10.01 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py` |
| 2 | `dm_neutrino_source_surface_bundle_window_trichotomy_candidate_note_2026-04-18` | bounded_theorem | unaudited | critical | 264 | 9.05 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_bundle_window_trichotomy_candidate.py` |
| 3 | `dm_neutrino_source_surface_endpoint_window_bundle_dominance_candidate_note_2026-04-17` | bounded_theorem | unaudited | critical | 264 | 8.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_endpoint_window_bundle_dominance_candidate.py` |
| 4 | `dm_neutrino_source_surface_split1_window_bundle_dominance_candidate_note_2026-04-17` | bounded_theorem | unaudited | critical | 264 | 8.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_split1_window_bundle_dominance_candidate.py` |
| 5 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 601 | 27.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 6 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 592 | 20.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 7 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 592 | 10.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 8 | `cpt_exact_note` | positive_theorem | unaudited | critical | 590 | 20.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 9 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 590 | 10.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 10 | `lensing_combined_invariant_note` | positive_theorem | unaudited | critical | 590 | 10.21 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `3d_correction_master_note` | positive_theorem | unaudited | critical | 590 | 9.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/dispersion_3d_lattice.py` |
| 12 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 588 | 14.20 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 587 | 15.70 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 14 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 587 | 13.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 15 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 586 | 17.70 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 16 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 586 | 14.70 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 586 | 13.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 18 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 585 | 17.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 19 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 585 | 15.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 20 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 585 | 10.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 21 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 584 | 28.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 22 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 584 | 22.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 23 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 584 | 16.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 24 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 584 | 16.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 584 | 16.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 584 | 16.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 584 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 28 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 584 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | positive_theorem | unaudited | critical | 584 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 30 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 584 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `universal_qg_smooth_gravitational_local_identification_note` | positive_theorem | unaudited | critical | 584 | 15.69 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 32 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 584 | 15.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 33 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | positive_theorem | unaudited | critical | 584 | 15.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 584 | 15.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 35 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 584 | 14.69 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `universal_qg_smooth_gravitational_global_atlas_note` | positive_theorem | unaudited | critical | 584 | 14.69 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 584 | 14.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 38 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 584 | 14.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 39 | `universal_qg_canonical_smooth_gravitational_weak_measure_note` | positive_theorem | unaudited | critical | 584 | 14.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 584 | 13.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 41 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 584 | 13.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 42 | `universal_gr_tensor_variational_candidate_note` | bounded_theorem | unaudited | critical | 584 | 13.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `universal_qg_canonical_smooth_geometric_action_note` | positive_theorem | unaudited | critical | 584 | 13.19 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `universal_qg_external_fe_smooth_equivalence_note` | positive_theorem | unaudited | critical | 584 | 12.69 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `universal_gr_a1_invariant_section_note` | positive_theorem | unaudited | critical | 584 | 12.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_a1_invariant_section.py` |
| 46 | `universal_gr_tensor_quotient_uniqueness_note` | bounded_theorem | unaudited | critical | 584 | 12.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_tensor_quotient_uniqueness.py` |
| 47 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 584 | 11.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_quarter_wald_noether_framework_carrier.py` |
| 48 | `planck_link_local_first_variation_p_a_forcing_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 584 | 11.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_link_local_first_variation_p_a_forcing.py` |
| 49 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 584 | 11.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 50 | `universal_gr_curvature_localization_blocker_note` | positive_theorem | unaudited | critical | 584 | 10.69 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

182 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 592 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 590 | `3d_correction_master_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 587 | `bh_entropy_derived_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 584 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 584 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 6 | `cycle-0006` | 5 | 584 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 7 | `cycle-0007` | 7 | 584 | `anomaly_forces_time_theorem` | critical | unaudited |
| 8 | `cycle-0008` | 8 | 584 | `anomaly_forces_time_theorem` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 502 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 502 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 502 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 12 | `cycle-0012` | 6 | 502 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 13 | `cycle-0013` | 7 | 502 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 14 | `cycle-0014` | 8 | 502 | `alpha_s_derived_note` | critical | audited_conditional |
| 15 | `cycle-0015` | 8 | 502 | `alpha_s_derived_note` | critical | audited_conditional |
| 16 | `cycle-0016` | 8 | 502 | `alpha_s_derived_note` | critical | audited_conditional |
| 17 | `cycle-0017` | 8 | 502 | `alpha_s_derived_note` | critical | audited_conditional |
| 18 | `cycle-0018` | 2 | 303 | `hypercharge_identification_note` | critical | unaudited |
| 19 | `cycle-0019` | 5 | 263 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 20 | `cycle-0020` | 5 | 263 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 21 | `cycle-0021` | 5 | 263 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 22 | `cycle-0022` | 5 | 263 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 23 | `cycle-0023` | 5 | 263 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 24 | `cycle-0024` | 5 | 263 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 25 | `cycle-0025` | 5 | 263 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
