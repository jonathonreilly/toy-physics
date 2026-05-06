# Audit Queue

**Total pending:** 795
**Ready (all deps already at retained-grade or metadata tiers):** 5

By criticality:
- `critical`: 508
- `high`: 15
- `medium`: 93
- `leaf`: 179

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block1_theorem_note_2026-05-03` | positive_theorem | audit_in_progress | critical | 546 | 10.60 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_intertwiner_engine.py` |
| 2 | `second_grown_family_complex_note` | positive_theorem | audit_in_progress | critical | 459 | 10.85 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/SECOND_GROWN_FAMILY_COMPLEX.py` |
| 3 | `fourth_family_complex_boundary_note` | positive_theorem | unaudited | critical | 455 | 9.33 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FOURTH_FAMILY_COMPLEX.py` |
| 4 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 5 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 6 | `su3_wigner_intertwiner_block2_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 545 | 10.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_4fold_haar_projector.py` |
| 7 | `su3_wigner_intertwiner_block3_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 544 | 9.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_geometry.py` |
| 8 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 543 | 10.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 9 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 469 | 16.38 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 469 | 14.88 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 465 | 13.36 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 464 | 13.36 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 464 | 12.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 14 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 463 | 13.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 15 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 463 | 12.86 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 16 | `signed_gravity_tensor_source_transport_retention_note` | positive_theorem | unaudited | critical | 463 | 10.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_tensor_source_transport_retention.py` |
| 17 | `signed_gravity_continuum_graded_einstein_localization_note` | positive_theorem | unaudited | critical | 462 | 10.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_continuum_graded_einstein_localization.py` |
| 18 | `signed_gravity_cl3z3_source_character_derivation_note` | positive_theorem | unaudited | critical | 461 | 11.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_cl3z3_source_character_derivation.py` |
| 19 | `signed_gravity_native_boundary_complex_containment_note` | no_go | unaudited | critical | 461 | 11.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_native_boundary_complex_containment.py` |
| 20 | `signed_gravity_naturally_hosted_orientation_line_note` | positive_theorem | unaudited | critical | 461 | 11.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_naturally_hosted_orientation_line.py` |
| 21 | `signed_gravity_source_character_uniqueness_theorem_note` | positive_theorem | unaudited | critical | 461 | 11.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_source_character_uniqueness_theorem.py` |
| 22 | `signed_gravity_nature_grade_closure_blocker_audit_note` | positive_theorem | unaudited | critical | 461 | 10.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_nature_grade_closure_blockers.py` |
| 23 | `signed_gravity_staggered_dirac_aps_boundary_realization_note` | positive_theorem | unaudited | critical | 461 | 10.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py` |
| 24 | `signed_gravity_remaining_closure_gates_note` | positive_theorem | unaudited | critical | 461 | 10.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_remaining_closure_gates.py` |
| 25 | `diamond_absolute_unit_bridge_note` | positive_theorem | unaudited | critical | 461 | 9.35 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `diamond_phase_ramp_bridge_card_note` | positive_theorem | unaudited | critical | 460 | 9.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/diamond_phase_ramp_bridge_card.py` |
| 27 | `shapiro_delay_note` | positive_theorem | unaudited | critical | 459 | 11.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_phase_lag_probe.py` |
| 28 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 455 | 15.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 29 | `complex_selectivity_compare_note` | positive_theorem | unaudited | critical | 455 | 10.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_COMPARE.py` |
| 30 | `causal_field_canonical_chain_note` | positive_theorem | unaudited | critical | 454 | 9.83 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `complex_selectivity_predictor_note` | positive_theorem | unaudited | critical | 454 | 9.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py` |
| 32 | `signed_gravity_oriented_tensor_source_lift_note` | positive_theorem | unaudited | critical | 454 | 9.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_oriented_tensor_source_lift.py` |
| 33 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 453 | 25.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 34 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 453 | 16.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 35 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 453 | 15.83 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 453 | 14.83 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 453 | 14.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 38 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 453 | 13.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 39 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 453 | 13.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 40 | `newton_law_derived_note` | positive_theorem | unaudited | critical | 453 | 13.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 41 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 453 | 13.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 42 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 453 | 13.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 43 | `broad_gravity_derivation_note` | bounded_theorem | unaudited | critical | 453 | 12.83 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `gravity_signed_source_density_boundary_note` | positive_theorem | unaudited | critical | 453 | 12.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_signed_gravity_source_variational_audit.py` |
| 45 | `frontier_extension_lane_opening_note_2026-04-25` | open_gate | unaudited | critical | 453 | 11.83 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `signed_gravity_chi_selector_theorem_or_nogo_note` | no_go | unaudited | critical | 453 | 11.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_signed_gravity_chi_selector_algebra.py` |
| 47 | `signed_gravity_nonlocal_boundary_chi_target_note` | positive_theorem | unaudited | critical | 453 | 11.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `signed_gravity_source_action_escape_hatch_note` | positive_theorem | unaudited | critical | 453 | 11.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `signed_gravity_aps_locked_axiom_extension_note` | positive_theorem | unaudited | critical | 453 | 10.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_aps_locked_axiom_extension_audit.py` |
| 50 | `signed_gravity_aps_locked_source_action_proposal_note` | positive_theorem | unaudited | critical | 453 | 10.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_aps_locked_source_action_proposal.py` |

## Citation cycle break targets

177 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 469 | `universal_qg_projective_schur_closure_note` | critical | audited_conditional |
| 2 | `cycle-0002` | 3 | 469 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 464 | `yt_explicit_systematic_budget_note` | critical | audited_conditional |
| 4 | `cycle-0004` | 3 | 461 | `signed_gravity_native_boundary_complex_containment_note` | critical | unaudited |
| 5 | `cycle-0005` | 6 | 461 | `signed_gravity_cl3z3_source_character_derivation_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 453 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 453 | `broad_gravity_derivation_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 453 | `gravity_clean_derivation_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 453 | `gravity_clean_derivation_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 453 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 453 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 453 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 453 | `signed_gravity_aps_locked_axiom_extension_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 453 | `signed_gravity_aps_boundary_index_chi_probe_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 453 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 453 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 453 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 453 | `signed_gravity_aps_locked_source_action_proposal_note` | critical | unaudited |
| 19 | `cycle-0019` | 4 | 453 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 453 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 453 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 453 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 453 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 453 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 453 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
