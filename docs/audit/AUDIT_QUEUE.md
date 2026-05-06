# Audit Queue

**Total pending:** 804
**Ready (all deps already at retained-grade or metadata tiers):** 10

By criticality:
- `critical`: 513
- `high`: 15
- `medium`: 95
- `leaf`: 181

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `dm_leptogenesis_flavor_column_functional_theorem_note_2026-04-16` | bounded_theorem | audit_in_progress | critical | 299 | 8.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_flavor_column_functional_theorem.py` |
| 2 | `dm_leptogenesis_ne_active_column_axiom_boundary_note_2026-04-16` | bounded_theorem | unaudited | critical | 299 | 8.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_ne_active_column_axiom_boundary.py` |
| 3 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 294 | 11.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 4 | `teleportation_acceptance_suite_note` | bounded_theorem | unaudited | critical | 287 | 10.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_teleportation_acceptance_suite.py` |
| 5 | `universal_qg_external_fe_smooth_equivalence_note` | positive_theorem | unaudited | critical | 287 | 10.67 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 6 | `universal_qg_continuum_bridge_reduction_note` | positive_theorem | unaudited | critical | 287 | 9.67 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 287 | 9.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 8 | `radial_scaling_protected_angle_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 287 | 8.67 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_radial_scaling_protected_angle_narrow.py` |
| 9 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 551 | 12.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 10 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 518 | 17.52 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 518 | 15.52 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 514 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 513 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 14 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 512 | 14.00 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 15 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 512 | 10.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 16 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 511 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 511 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 510 | 15.00 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 19 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 510 | 12.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 20 | `universal_qg_canonical_smooth_geometric_action_note` | positive_theorem | unaudited | critical | 510 | 12.00 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `universal_qg_canonical_textbook_continuum_gr_closure_note` | positive_theorem | unaudited | critical | 509 | 14.49 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 22 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 509 | 13.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 23 | `signed_gravity_tensor_source_transport_retention_note` | positive_theorem | unaudited | critical | 509 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_tensor_source_transport_retention.py` |
| 24 | `signed_gravity_continuum_graded_einstein_localization_note` | positive_theorem | unaudited | critical | 508 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_continuum_graded_einstein_localization.py` |
| 25 | `signed_gravity_cl3z3_source_character_derivation_note` | positive_theorem | unaudited | critical | 507 | 11.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_cl3z3_source_character_derivation.py` |
| 26 | `signed_gravity_native_boundary_complex_containment_note` | no_go | unaudited | critical | 507 | 11.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_native_boundary_complex_containment.py` |
| 27 | `signed_gravity_naturally_hosted_orientation_line_note` | positive_theorem | unaudited | critical | 507 | 11.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_naturally_hosted_orientation_line.py` |
| 28 | `signed_gravity_source_character_uniqueness_theorem_note` | positive_theorem | unaudited | critical | 507 | 11.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_source_character_uniqueness_theorem.py` |
| 29 | `signed_gravity_nature_grade_closure_blocker_audit_note` | positive_theorem | unaudited | critical | 507 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_nature_grade_closure_blockers.py` |
| 30 | `signed_gravity_staggered_dirac_aps_boundary_realization_note` | positive_theorem | unaudited | critical | 507 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py` |
| 31 | `signed_gravity_remaining_closure_gates_note` | positive_theorem | unaudited | critical | 507 | 10.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_remaining_closure_gates.py` |
| 32 | `diamond_absolute_unit_bridge_note` | positive_theorem | unaudited | critical | 507 | 9.49 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `diamond_phase_ramp_bridge_card_note` | positive_theorem | unaudited | critical | 506 | 9.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/diamond_phase_ramp_bridge_card.py` |
| 34 | `shapiro_delay_note` | positive_theorem | unaudited | critical | 505 | 11.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_phase_lag_probe.py` |
| 35 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 501 | 15.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 36 | `complex_selectivity_compare_note` | positive_theorem | unaudited | critical | 501 | 10.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_COMPARE.py` |
| 37 | `causal_field_canonical_chain_note` | positive_theorem | unaudited | critical | 500 | 9.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `complex_selectivity_predictor_note` | positive_theorem | unaudited | critical | 500 | 9.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py` |
| 39 | `signed_gravity_oriented_tensor_source_lift_note` | positive_theorem | unaudited | critical | 500 | 9.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_oriented_tensor_source_lift.py` |
| 40 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 499 | 25.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 41 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 499 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 42 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 499 | 15.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 499 | 14.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 499 | 14.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 45 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 499 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 46 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 499 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 47 | `newton_law_derived_note` | positive_theorem | unaudited | critical | 499 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 48 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 499 | 13.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 49 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 499 | 13.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 50 | `broad_gravity_derivation_note` | bounded_theorem | unaudited | critical | 499 | 12.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

192 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 518 | `universal_qg_projective_schur_closure_note` | critical | audited_conditional |
| 2 | `cycle-0002` | 3 | 518 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 510 | `yt_explicit_systematic_budget_note` | critical | audited_conditional |
| 4 | `cycle-0004` | 3 | 507 | `signed_gravity_native_boundary_complex_containment_note` | critical | unaudited |
| 5 | `cycle-0005` | 6 | 507 | `signed_gravity_cl3z3_source_character_derivation_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 499 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 499 | `broad_gravity_derivation_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 499 | `gravity_clean_derivation_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 499 | `gravity_clean_derivation_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 499 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 499 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 499 | `signed_gravity_aps_locked_axiom_extension_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 499 | `signed_gravity_aps_boundary_index_chi_probe_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 499 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 499 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 499 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 499 | `signed_gravity_aps_locked_source_action_proposal_note` | critical | unaudited |
| 19 | `cycle-0019` | 4 | 499 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 499 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 499 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 499 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
