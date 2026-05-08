# Audit Queue

**Total pending:** 846
**Ready (all deps already at retained-grade or metadata tiers):** 0

By criticality:
- `critical`: 71
- `high`: 302
- `medium`: 277
- `leaf`: 196

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 522 | 15.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 2 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 522 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 3 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 516 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 4 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 516 | 12.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 5 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 514 | 27.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 6 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 514 | 16.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 7 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 514 | 16.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 514 | 15.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 9 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 514 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 10 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 514 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 11 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 514 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 12 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 514 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 13 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 428 | 26.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 14 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 402 | 12.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 15 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 370 | 10.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 16 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 369 | 26.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 17 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 352 | 23.96 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 18 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 342 | 16.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 19 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 338 | 10.40 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 20 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 277 | 10.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 21 | `neutrino_majorana_operator_axiom_first_note` | positive_theorem | unaudited | critical | 267 | 14.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_operator.py` |
| 22 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | critical | 265 | 11.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 23 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | critical | 263 | 12.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 24 | `neutrino_majorana_pfaffian_extension_note` | positive_theorem | unaudited | critical | 262 | 11.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |
| 25 | `neutrino_majorana_pfaffian_axiom_boundary_note` | no_go | unaudited | critical | 261 | 8.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py` |
| 26 | `neutrino_majorana_pfaffian_no_forcing_theorem_note` | positive_theorem | unaudited | critical | 260 | 12.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py` |
| 27 | `neutrino_majorana_current_atlas_nonrealization_note` | positive_theorem | unaudited | critical | 260 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py` |
| 28 | `neutrino_majorana_charge_two_primitive_reduction_note` | positive_theorem | unaudited | critical | 259 | 10.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` |
| 29 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 258 | 17.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 30 | `neutrino_majorana_unique_source_slot_note` | positive_theorem | unaudited | critical | 258 | 12.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_unique_source_slot.py` |
| 31 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 258 | 9.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 32 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 258 | 9.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 33 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 257 | 21.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 34 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 257 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 35 | `universal_gr_tensor_variational_candidate_note` | bounded_theorem | unaudited | critical | 257 | 12.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `universal_gr_a1_invariant_section_note` | positive_theorem | unaudited | critical | 257 | 11.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_a1_invariant_section.py` |
| 37 | `universal_gr_tensor_quotient_uniqueness_note` | bounded_theorem | unaudited | critical | 257 | 11.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_tensor_quotient_uniqueness.py` |
| 38 | `universal_gr_curvature_localization_blocker_note` | positive_theorem | unaudited | critical | 257 | 9.51 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 39 | `universal_gr_constraint_action_stationarity_note` | positive_theorem | unaudited | critical | 257 | 9.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `neutrino_majorana_phase_removal_note` | positive_theorem | unaudited | critical | 250 | 10.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_phase_removal.py` |
| 41 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 234 | 25.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 42 | `ckm_atlas_axiom_closure_note` | positive_theorem | unaudited | critical | 213 | 23.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 43 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 195 | 18.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 44 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 193 | 20.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 45 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 183 | 18.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 46 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 183 | 17.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 47 | `dm_leptogenesis_transport_status_note_2026-04-16` | positive_theorem | unaudited | critical | 166 | 14.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_transport_status.py` |
| 48 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 155 | 28.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 49 | `quark_projector_parameter_audit_note_2026-04-19` | bounded_theorem | unaudited | critical | 137 | 17.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_projector_parameter_audit.py` |
| 50 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 133 | 14.57 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

45 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 522 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 514 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 3 | `cycle-0003` | 7 | 514 | `anomaly_forces_time_theorem` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 258 | `hypercharge_identification_note` | critical | unaudited |
| 5 | `cycle-0005` | 4 | 257 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 6 | `cycle-0006` | 5 | 257 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 7 | `cycle-0007` | 6 | 257 | `universal_gr_a1_invariant_section_note` | critical | unaudited |
| 8 | `cycle-0008` | 6 | 257 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 124 | `yt_p2_taste_staircase_beta_functions_note_2026-04-17` | high | unaudited |
| 10 | `cycle-0010` | 6 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 11 | `cycle-0011` | 7 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 12 | `cycle-0012` | 7 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 13 | `cycle-0013` | 8 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 14 | `cycle-0014` | 9 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 15 | `cycle-0015` | 12 | 107 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 16 | `cycle-0016` | 14 | 107 | `charged_lepton_koide_cone_algebraic_equivalence_note` | high | unaudited |
| 17 | `cycle-0017` | 2 | 89 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 18 | `cycle-0018` | 4 | 44 | `dm_pmns_cp_orientation_parity_reduction_note_2026-04-20` | medium | unaudited |
| 19 | `cycle-0019` | 2 | 42 | `lensing_finite_path_explanation_note` | medium | unaudited |
| 20 | `cycle-0020` | 4 | 38 | `publication.ci3_z3.claims_table` | high | unaudited |
| 21 | `cycle-0021` | 5 | 38 | `publication.ci3_z3.claims_table` | high | unaudited |
| 22 | `cycle-0022` | 4 | 35 | `localized_source_response_sweep_note` | medium | unaudited |
| 23 | `cycle-0023` | 5 | 35 | `mesoscopic_surrogate_backreaction_note` | high | unaudited |
| 24 | `cycle-0024` | 2 | 26 | `newton_derivation_note` | medium | unaudited |
| 25 | `cycle-0025` | 4 | 23 | `signed_gravity_cl3z3_source_character_derivation_note` | high | unaudited |

Full queue lives in `data/audit_queue.json`.
