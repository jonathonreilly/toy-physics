# Audit Queue

**Total pending:** 802
**Ready (all deps already at retained-grade or metadata tiers):** 13

By criticality:
- `critical`: 514
- `high`: 15
- `medium`: 93
- `leaf`: 180

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block1_theorem_note_2026-05-03` | positive_theorem | audit_in_progress | critical | 537 | 10.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_intertwiner_engine.py` |
| 2 | `second_grown_family_sign_note` | bounded_theorem | unaudited | critical | 458 | 9.84 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/SECOND_GROWN_FAMILY_SIGN_SWEEP.py` |
| 3 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 455 | 9.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 4 | `staggered_fermion_card_2026-04-11` | bounded_theorem | unaudited | critical | 446 | 10.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_17card.py` |
| 5 | `staggered_newton_reproduction_note_2026-04-11` | bounded_theorem | unaudited | critical | 446 | 9.80 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_newton_reproduction.py` |
| 6 | `alt_connectivity_family_complex_failure_note` | positive_theorem | unaudited | critical | 446 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/ALT_CONNECTIVITY_FAMILY_COMPLEX_SWEEP.py` |
| 7 | `fifth_family_complex_boundary_note` | positive_theorem | unaudited | critical | 446 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py` |
| 8 | `fourth_family_complex_boundary_note` | positive_theorem | unaudited | critical | 446 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FOURTH_FAMILY_COMPLEX.py` |
| 9 | `third_grown_family_complex_boundary_note` | positive_theorem | unaudited | critical | 446 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/THIRD_GROWN_FAMILY_COMPLEX.py` |
| 10 | `staggered_self_consistent_two_body_note_2026-04-11` | bounded_theorem | unaudited | critical | 445 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_self_consistent_two_body.py` |
| 11 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 12 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 13 | `su3_wigner_intertwiner_block2_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 536 | 10.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_4fold_haar_projector.py` |
| 14 | `su3_wigner_intertwiner_block3_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 535 | 9.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_geometry.py` |
| 15 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 534 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 16 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 460 | 16.35 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 460 | 14.85 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 456 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 19 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 455 | 13.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 20 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 455 | 12.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 21 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 454 | 13.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 22 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 454 | 12.83 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `signed_gravity_tensor_source_transport_retention_note` | positive_theorem | unaudited | critical | 454 | 10.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_tensor_source_transport_retention.py` |
| 24 | `signed_gravity_continuum_graded_einstein_localization_note` | positive_theorem | unaudited | critical | 453 | 10.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_continuum_graded_einstein_localization.py` |
| 25 | `signed_gravity_cl3z3_source_character_derivation_note` | positive_theorem | unaudited | critical | 452 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_cl3z3_source_character_derivation.py` |
| 26 | `sign_portability_invariant_note` | bounded_theorem | unaudited | critical | 452 | 11.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` |
| 27 | `signed_gravity_native_boundary_complex_containment_note` | no_go | unaudited | critical | 452 | 11.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_native_boundary_complex_containment.py` |
| 28 | `signed_gravity_naturally_hosted_orientation_line_note` | positive_theorem | unaudited | critical | 452 | 11.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_naturally_hosted_orientation_line.py` |
| 29 | `signed_gravity_source_character_uniqueness_theorem_note` | positive_theorem | unaudited | critical | 452 | 11.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_source_character_uniqueness_theorem.py` |
| 30 | `signed_gravity_nature_grade_closure_blocker_audit_note` | positive_theorem | unaudited | critical | 452 | 10.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_nature_grade_closure_blockers.py` |
| 31 | `signed_gravity_staggered_dirac_aps_boundary_realization_note` | positive_theorem | unaudited | critical | 452 | 10.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py` |
| 32 | `signed_gravity_remaining_closure_gates_note` | positive_theorem | unaudited | critical | 452 | 10.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_remaining_closure_gates.py` |
| 33 | `diamond_absolute_unit_bridge_note` | positive_theorem | unaudited | critical | 452 | 9.32 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `diamond_phase_ramp_bridge_card_note` | positive_theorem | unaudited | critical | 451 | 9.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/diamond_phase_ramp_bridge_card.py` |
| 35 | `shapiro_delay_note` | positive_theorem | unaudited | critical | 450 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_phase_lag_probe.py` |
| 36 | `second_grown_family_complex_note` | positive_theorem | unaudited | critical | 450 | 10.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/SECOND_GROWN_FAMILY_COMPLEX.py` |
| 37 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 446 | 15.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 38 | `complex_selectivity_compare_note` | positive_theorem | unaudited | critical | 446 | 10.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_COMPARE.py` |
| 39 | `causal_field_canonical_chain_note` | positive_theorem | unaudited | critical | 445 | 9.80 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `complex_selectivity_predictor_note` | positive_theorem | unaudited | critical | 445 | 9.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py` |
| 41 | `signed_gravity_oriented_tensor_source_lift_note` | positive_theorem | unaudited | critical | 445 | 9.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_oriented_tensor_source_lift.py` |
| 42 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 444 | 25.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 43 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 444 | 16.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 44 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 444 | 15.80 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 444 | 14.80 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 444 | 14.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 47 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 444 | 13.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 48 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 444 | 13.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 49 | `newton_law_derived_note` | positive_theorem | unaudited | critical | 444 | 13.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 50 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 444 | 13.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |

## Citation cycle break targets

174 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 460 | `universal_qg_projective_schur_closure_note` | critical | audited_conditional |
| 2 | `cycle-0002` | 3 | 460 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 455 | `yt_explicit_systematic_budget_note` | critical | audited_conditional |
| 4 | `cycle-0004` | 3 | 452 | `signed_gravity_native_boundary_complex_containment_note` | critical | unaudited |
| 5 | `cycle-0005` | 6 | 452 | `signed_gravity_cl3z3_source_character_derivation_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 444 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 444 | `broad_gravity_derivation_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 444 | `gravity_clean_derivation_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 444 | `gravity_clean_derivation_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 444 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 444 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 444 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 444 | `signed_gravity_aps_locked_axiom_extension_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 444 | `signed_gravity_aps_boundary_index_chi_probe_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 444 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 444 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 444 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 444 | `signed_gravity_aps_locked_source_action_proposal_note` | critical | unaudited |
| 19 | `cycle-0019` | 4 | 444 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 444 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 444 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 444 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 444 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 444 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 444 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
