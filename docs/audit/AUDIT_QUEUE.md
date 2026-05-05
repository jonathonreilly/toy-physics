# Audit Queue

**Total pending:** 875
**Ready (all deps already at retained-grade or metadata tiers):** 11

By criticality:
- `critical`: 587
- `high`: 15
- `medium`: 93
- `leaf`: 180

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block1_theorem_note_2026-05-03` | positive_theorem | audit_in_progress | critical | 537 | 10.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_intertwiner_engine.py` |
| 2 | `staggered_fermion_card_2026-04-11` | - | unaudited | critical | 446 | 10.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_17card.py` |
| 3 | `staggered_newton_reproduction_note_2026-04-11` | - | unaudited | critical | 446 | 9.80 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_newton_reproduction.py` |
| 4 | `alt_connectivity_family_complex_failure_note` | - | unaudited | critical | 446 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/ALT_CONNECTIVITY_FAMILY_COMPLEX_SWEEP.py` |
| 5 | `fifth_family_complex_boundary_note` | - | unaudited | critical | 446 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FIFTH_FAMILY_COMPLEX_TARGETED.py` |
| 6 | `fourth_family_complex_boundary_note` | - | unaudited | critical | 446 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FOURTH_FAMILY_COMPLEX.py` |
| 7 | `third_grown_family_complex_boundary_note` | - | unaudited | critical | 446 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/THIRD_GROWN_FAMILY_COMPLEX.py` |
| 8 | `staggered_self_consistent_two_body_note_2026-04-11` | - | unaudited | critical | 445 | 9.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_self_consistent_two_body.py` |
| 9 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 10 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 11 | `su3_wigner_intertwiner_block2_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 536 | 10.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_4fold_haar_projector.py` |
| 12 | `g_bare_derivation_note` | positive_theorem | unaudited | critical | 535 | 16.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 13 | `su3_wigner_intertwiner_block3_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 535 | 9.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_geometry.py` |
| 14 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 534 | 10.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 15 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 531 | 13.05 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 16 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 530 | 12.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 17 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 525 | 12.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 18 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 525 | 11.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 19 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 525 | 11.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 20 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 525 | 11.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 21 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 525 | 11.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 22 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 524 | 22.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 23 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 502 | 9.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 24 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 501 | 31.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 25 | `gate_b_grown_joint_package_note` | bounded_theorem | unaudited | critical | 483 | 12.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_grown_joint_package.py` |
| 26 | `gate_b_weak_connectivity_note` | bounded_theorem | unaudited | critical | 475 | 11.89 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_weak_connectivity_harness.py` |
| 27 | `gate_b_nonlabel_connectivity_v1_note` | bounded_theorem | unaudited | critical | 471 | 12.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1.py` |
| 28 | `gate_b_nonlabel_connectivity_v1_distance_note` | bounded_theorem | unaudited | critical | 465 | 9.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1_distance.py` |
| 29 | `gate_b_nonlabel_connectivity_v1_joint_note` | bounded_theorem | unaudited | critical | 465 | 9.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1_joint.py` |
| 30 | `universal_gr_positive_background_local_closure_note` | positive_theorem | unaudited | critical | 463 | 11.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 31 | `minimal_absorbing_horizon_probe_note` | bounded_theorem | unaudited | critical | 463 | 9.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_absorbing_horizon_probe.py` |
| 32 | `minimal_bidirectional_trapping_probe_note` | bounded_theorem | unaudited | critical | 462 | 9.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_bidirectional_trapping_probe.py` |
| 33 | `yt_bridge_endpoint_shift_bound_note` | bounded_theorem | unaudited | critical | 461 | 10.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_endpoint_shift_bound.py` |
| 34 | `retarded_field_delay_proxy_note` | bounded_theorem | unaudited | critical | 461 | 9.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/retarded_field_delay_proxy_probe.py` |
| 35 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 460 | 16.35 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 460 | 14.85 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 460 | 12.85 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `yt_exact_coarse_grained_bridge_operator_note` | bounded_theorem | unaudited | critical | 460 | 10.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_coarse_grained_bridge_operator.py` |
| 39 | `yt_exact_schur_normal_form_uniqueness_note` | bounded_theorem | unaudited | critical | 459 | 14.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py` |
| 40 | `diamond_sensor_prediction_note` | bounded_theorem | unaudited | critical | 459 | 11.35 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 457 | 13.84 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `universal_qg_inverse_limit_closure_note` | bounded_theorem | unaudited | critical | 457 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `propagator_family_unification_note` | positive_theorem | unaudited | critical | 457 | 9.34 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 456 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `diamond_nv_phase_ramp_signal_budget_note` | positive_theorem | unaudited | critical | 456 | 10.34 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 455 | 13.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 455 | 12.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 48 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 455 | 10.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 49 | `universal_qg_canonical_textbook_continuum_gr_closure_note` | positive_theorem | unaudited | critical | 454 | 14.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 454 | 14.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

174 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 460 | `universal_qg_projective_schur_closure_note` | critical | unaudited |
| 2 | `cycle-0002` | 3 | 460 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 455 | `yt_explicit_systematic_budget_note` | critical | unaudited |
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
