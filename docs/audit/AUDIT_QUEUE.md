# Audit Queue

**Total pending:** 811
**Ready (all deps already at retained-grade or metadata tiers):** 17

By criticality:
- `critical`: 520
- `high`: 15
- `medium`: 95
- `leaf`: 181

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block1_theorem_note_2026-05-03` | positive_theorem | audit_in_progress | critical | 556 | 10.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_intertwiner_engine.py` |
| 2 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | positive_theorem | unaudited | critical | 514 | 14.51 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 3 | `universal_gr_constraint_action_stationarity_note` | positive_theorem | unaudited | critical | 510 | 9.50 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 4 | `universal_qg_smooth_gravitational_global_atlas_note` | positive_theorem | unaudited | critical | 509 | 13.49 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 5 | `universal_qg_smooth_gravitational_local_identification_note` | positive_theorem | unaudited | critical | 509 | 13.49 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 6 | `universal_qg_canonical_smooth_gravitational_weak_measure_note` | positive_theorem | unaudited | critical | 509 | 12.99 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | positive_theorem | unaudited | critical | 508 | 12.99 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `second_grown_family_complex_note` | positive_theorem | audit_in_progress | critical | 503 | 10.98 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/SECOND_GROWN_FAMILY_COMPLEX.py` |
| 9 | `fourth_family_complex_boundary_note` | positive_theorem | unaudited | critical | 499 | 9.47 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FOURTH_FAMILY_COMPLEX.py` |
| 10 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 11 | `teleportation_acceptance_suite_note` | bounded_theorem | unaudited | critical | 285 | 10.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_teleportation_acceptance_suite.py` |
| 12 | `universal_qg_external_fe_smooth_equivalence_note` | positive_theorem | unaudited | critical | 285 | 10.66 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `universal_qg_continuum_bridge_reduction_note` | positive_theorem | unaudited | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 14 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 15 | `radial_scaling_protected_angle_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 285 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_radial_scaling_protected_angle_narrow.py` |
| 16 | `su3_wigner_intertwiner_block2_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 555 | 10.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_4fold_haar_projector.py` |
| 17 | `su3_wigner_intertwiner_block3_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 554 | 9.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_geometry.py` |
| 18 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 553 | 10.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 19 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 516 | 17.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 20 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 516 | 15.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 512 | 14.00 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 22 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 511 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 510 | 14.00 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 24 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 510 | 10.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 25 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 509 | 13.49 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 509 | 13.49 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 508 | 14.99 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 508 | 12.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 29 | `universal_qg_canonical_smooth_geometric_action_note` | positive_theorem | unaudited | critical | 508 | 11.99 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 30 | `universal_qg_canonical_textbook_continuum_gr_closure_note` | positive_theorem | unaudited | critical | 507 | 14.49 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 507 | 13.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 32 | `signed_gravity_tensor_source_transport_retention_note` | positive_theorem | unaudited | critical | 507 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_tensor_source_transport_retention.py` |
| 33 | `signed_gravity_continuum_graded_einstein_localization_note` | positive_theorem | unaudited | critical | 506 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_continuum_graded_einstein_localization.py` |
| 34 | `signed_gravity_cl3z3_source_character_derivation_note` | positive_theorem | unaudited | critical | 505 | 11.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_cl3z3_source_character_derivation.py` |
| 35 | `signed_gravity_native_boundary_complex_containment_note` | no_go | unaudited | critical | 505 | 11.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_native_boundary_complex_containment.py` |
| 36 | `signed_gravity_naturally_hosted_orientation_line_note` | positive_theorem | unaudited | critical | 505 | 11.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_naturally_hosted_orientation_line.py` |
| 37 | `signed_gravity_source_character_uniqueness_theorem_note` | positive_theorem | unaudited | critical | 505 | 11.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_source_character_uniqueness_theorem.py` |
| 38 | `signed_gravity_nature_grade_closure_blocker_audit_note` | positive_theorem | unaudited | critical | 505 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_nature_grade_closure_blockers.py` |
| 39 | `signed_gravity_staggered_dirac_aps_boundary_realization_note` | positive_theorem | unaudited | critical | 505 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py` |
| 40 | `signed_gravity_remaining_closure_gates_note` | positive_theorem | unaudited | critical | 505 | 10.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_remaining_closure_gates.py` |
| 41 | `diamond_absolute_unit_bridge_note` | positive_theorem | unaudited | critical | 505 | 9.48 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `diamond_phase_ramp_bridge_card_note` | positive_theorem | unaudited | critical | 504 | 9.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/diamond_phase_ramp_bridge_card.py` |
| 43 | `shapiro_delay_note` | positive_theorem | unaudited | critical | 503 | 11.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_phase_lag_probe.py` |
| 44 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 499 | 15.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 45 | `complex_selectivity_compare_note` | positive_theorem | unaudited | critical | 499 | 10.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_COMPARE.py` |
| 46 | `causal_field_canonical_chain_note` | positive_theorem | unaudited | critical | 498 | 9.96 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `complex_selectivity_predictor_note` | positive_theorem | unaudited | critical | 498 | 9.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py` |
| 48 | `signed_gravity_oriented_tensor_source_lift_note` | positive_theorem | unaudited | critical | 498 | 9.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_oriented_tensor_source_lift.py` |
| 49 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 497 | 25.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 50 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 497 | 16.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |

## Citation cycle break targets

192 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 516 | `universal_qg_projective_schur_closure_note` | critical | audited_conditional |
| 2 | `cycle-0002` | 3 | 516 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 508 | `yt_explicit_systematic_budget_note` | critical | audited_conditional |
| 4 | `cycle-0004` | 3 | 505 | `signed_gravity_native_boundary_complex_containment_note` | critical | unaudited |
| 5 | `cycle-0005` | 6 | 505 | `signed_gravity_cl3z3_source_character_derivation_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 497 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 497 | `broad_gravity_derivation_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 497 | `gravity_clean_derivation_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 497 | `gravity_clean_derivation_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 497 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 497 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 497 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 497 | `signed_gravity_aps_locked_axiom_extension_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 497 | `signed_gravity_aps_boundary_index_chi_probe_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 497 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 497 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 497 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 497 | `signed_gravity_aps_locked_source_action_proposal_note` | critical | unaudited |
| 19 | `cycle-0019` | 4 | 497 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 497 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 497 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 497 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 497 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 497 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 497 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
