# Audit Queue

**Total pending:** 813
**Ready (all deps already at retained-grade or metadata tiers):** 14

By criticality:
- `critical`: 514
- `high`: 15
- `medium`: 97
- `leaf`: 187

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `fourth_family_complex_boundary_note` | no_go | unaudited | critical | 502 | 9.47 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FOURTH_FAMILY_COMPLEX.py` |
| 2 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 501 | 11.47 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 3 | `dm_neutrino_weak_vector_theorem_note_2026-04-15` | bounded_theorem | unaudited | critical | 299 | 8.73 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 4 | `su3_casimir_fundamental_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 295 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/su3_casimir_fundamental_check.py` |
| 5 | `dm_neutrino_source_surface_atomic_witness_volume_selector_nonrealization_note_2026-04-18` | positive_theorem | unaudited | critical | 292 | 9.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_atomic_witness_volume_selector_nonrealization.py` |
| 6 | `persistent_object_top4_multistage_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 290 | 9.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 7 | `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 287 | 13.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py` |
| 8 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 552 | 12.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 9 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 519 | 17.52 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 519 | 15.52 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 515 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 514 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 513 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 14 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 513 | 10.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 15 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 512 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 16 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 512 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 511 | 15.00 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 511 | 12.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 19 | `universal_qg_canonical_smooth_geometric_action_note` | positive_theorem | unaudited | critical | 511 | 12.00 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 20 | `universal_qg_canonical_textbook_continuum_gr_closure_note` | positive_theorem | unaudited | critical | 510 | 14.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 510 | 13.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 22 | `signed_gravity_tensor_source_transport_retention_note` | positive_theorem | unaudited | critical | 510 | 11.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_tensor_source_transport_retention.py` |
| 23 | `signed_gravity_continuum_graded_einstein_localization_note` | positive_theorem | unaudited | critical | 509 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_continuum_graded_einstein_localization.py` |
| 24 | `signed_gravity_cl3z3_source_character_derivation_note` | positive_theorem | unaudited | critical | 508 | 11.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_cl3z3_source_character_derivation.py` |
| 25 | `signed_gravity_native_boundary_complex_containment_note` | no_go | unaudited | critical | 508 | 11.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_native_boundary_complex_containment.py` |
| 26 | `signed_gravity_naturally_hosted_orientation_line_note` | positive_theorem | unaudited | critical | 508 | 11.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_naturally_hosted_orientation_line.py` |
| 27 | `signed_gravity_source_character_uniqueness_theorem_note` | positive_theorem | unaudited | critical | 508 | 11.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_source_character_uniqueness_theorem.py` |
| 28 | `signed_gravity_nature_grade_closure_blocker_audit_note` | positive_theorem | unaudited | critical | 508 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_nature_grade_closure_blockers.py` |
| 29 | `signed_gravity_staggered_dirac_aps_boundary_realization_note` | positive_theorem | unaudited | critical | 508 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py` |
| 30 | `signed_gravity_remaining_closure_gates_note` | positive_theorem | unaudited | critical | 508 | 10.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_remaining_closure_gates.py` |
| 31 | `diamond_absolute_unit_bridge_note` | positive_theorem | unaudited | critical | 508 | 9.49 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 32 | `diamond_phase_ramp_bridge_card_note` | positive_theorem | unaudited | critical | 507 | 9.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/diamond_phase_ramp_bridge_card.py` |
| 33 | `shapiro_delay_note` | positive_theorem | unaudited | critical | 506 | 11.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_phase_lag_probe.py` |
| 34 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 502 | 15.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 35 | `complex_selectivity_compare_note` | positive_theorem | unaudited | critical | 502 | 10.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_COMPARE.py` |
| 36 | `causal_field_canonical_chain_note` | positive_theorem | unaudited | critical | 501 | 9.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `complex_selectivity_predictor_note` | positive_theorem | unaudited | critical | 501 | 9.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/COMPLEX_SELECTIVITY_PREDICTOR_SCAN.py` |
| 38 | `signed_gravity_oriented_tensor_source_lift_note` | positive_theorem | unaudited | critical | 501 | 9.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/signed_gravity_oriented_tensor_source_lift.py` |
| 39 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 500 | 25.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 40 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 500 | 16.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 41 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 500 | 15.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 500 | 14.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 500 | 14.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 44 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 500 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 45 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 500 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 46 | `newton_law_derived_note` | positive_theorem | unaudited | critical | 500 | 13.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 47 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 500 | 13.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 48 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 500 | 13.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 49 | `broad_gravity_derivation_note` | bounded_theorem | unaudited | critical | 500 | 12.97 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `gravity_signed_source_density_boundary_note` | positive_theorem | unaudited | critical | 500 | 12.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_signed_gravity_source_variational_audit.py` |

## Citation cycle break targets

194 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 519 | `universal_qg_projective_schur_closure_note` | critical | audited_conditional |
| 2 | `cycle-0002` | 3 | 519 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 511 | `yt_explicit_systematic_budget_note` | critical | audited_conditional |
| 4 | `cycle-0004` | 3 | 508 | `signed_gravity_native_boundary_complex_containment_note` | critical | unaudited |
| 5 | `cycle-0005` | 6 | 508 | `signed_gravity_cl3z3_source_character_derivation_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 500 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 500 | `broad_gravity_derivation_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 500 | `gravity_clean_derivation_note` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 500 | `gravity_clean_derivation_note` | critical | unaudited |
| 10 | `cycle-0010` | 3 | 500 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 11 | `cycle-0011` | 3 | 500 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 500 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 500 | `signed_gravity_aps_locked_axiom_extension_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 500 | `signed_gravity_aps_boundary_index_chi_probe_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 500 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 16 | `cycle-0016` | 3 | 500 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 500 | `signed_gravity_chi_selector_theorem_or_nogo_note` | critical | unaudited |
| 18 | `cycle-0018` | 3 | 500 | `signed_gravity_aps_locked_source_action_proposal_note` | critical | unaudited |
| 19 | `cycle-0019` | 4 | 500 | `antigravity_sign_selector_boundary_note` | critical | unaudited |
| 20 | `cycle-0020` | 4 | 500 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 21 | `cycle-0021` | 4 | 500 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 22 | `cycle-0022` | 4 | 500 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 23 | `cycle-0023` | 4 | 500 | `gravity_signed_source_density_boundary_note` | critical | unaudited |
| 24 | `cycle-0024` | 4 | 500 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 500 | `signed_gravity_aps_action_origin_superselection_stability_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
