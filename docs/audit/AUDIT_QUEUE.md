# Audit Queue

**Total pending:** 898
**Ready (all deps already at retained-grade or metadata tiers):** 6

By criticality:
- `critical`: 99
- `high`: 354
- `medium`: 251
- `leaf`: 194

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 559 | 18.63 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 2 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 559 | 10.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 3 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 557 | 10.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 4 | `lensing_combined_invariant_note` | positive_theorem | unaudited | critical | 557 | 10.12 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 5 | `3d_correction_master_note` | positive_theorem | unaudited | critical | 557 | 9.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/dispersion_3d_lattice.py` |
| 6 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 553 | 14.61 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 553 | 12.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 8 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 551 | 28.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 9 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 551 | 16.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 10 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 551 | 16.11 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 551 | 15.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 12 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 551 | 14.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 13 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 551 | 14.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 14 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 551 | 13.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 15 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 551 | 13.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 16 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 463 | 26.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 17 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 438 | 12.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 18 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 422 | 12.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 19 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 421 | 26.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 20 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 381 | 24.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 21 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 367 | 17.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 22 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 363 | 10.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 23 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 309 | 10.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 24 | `neutrino_majorana_operator_axiom_first_note` | positive_theorem | unaudited | critical | 299 | 14.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_operator.py` |
| 25 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | critical | 297 | 11.72 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 26 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | critical | 295 | 12.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 27 | `neutrino_majorana_pfaffian_extension_note` | positive_theorem | unaudited | critical | 294 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |
| 28 | `neutrino_majorana_pfaffian_axiom_boundary_note` | no_go | unaudited | critical | 293 | 8.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py` |
| 29 | `neutrino_majorana_pfaffian_no_forcing_theorem_note` | positive_theorem | unaudited | critical | 292 | 12.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py` |
| 30 | `neutrino_majorana_current_atlas_nonrealization_note` | positive_theorem | unaudited | critical | 292 | 10.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py` |
| 31 | `neutrino_majorana_charge_two_primitive_reduction_note` | positive_theorem | unaudited | critical | 291 | 10.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` |
| 32 | `neutrino_majorana_unique_source_slot_note` | positive_theorem | unaudited | critical | 290 | 12.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_unique_source_slot.py` |
| 33 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 283 | 9.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 34 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 282 | 21.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 35 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 282 | 13.64 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `universal_gr_tensor_variational_candidate_note` | bounded_theorem | unaudited | critical | 282 | 12.14 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `universal_gr_a1_invariant_section_note` | positive_theorem | unaudited | critical | 282 | 11.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_a1_invariant_section.py` |
| 38 | `universal_gr_tensor_quotient_uniqueness_note` | bounded_theorem | unaudited | critical | 282 | 11.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_tensor_quotient_uniqueness.py` |
| 39 | `neutrino_majorana_phase_removal_note` | positive_theorem | unaudited | critical | 282 | 10.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_phase_removal.py` |
| 40 | `universal_gr_curvature_localization_blocker_note` | positive_theorem | unaudited | critical | 282 | 9.64 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `universal_gr_constraint_action_stationarity_note` | positive_theorem | unaudited | critical | 282 | 9.14 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 42 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 279 | 11.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 43 | `neutrino_majorana_canonical_local_block_note` | positive_theorem | unaudited | critical | 278 | 10.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_canonical_local_block.py` |
| 44 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 275 | 17.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 45 | `neutrino_majorana_z3_nonactivation_theorem_note` | positive_theorem | unaudited | critical | 275 | 12.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_z3_nonactivation_theorem.py` |
| 46 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 275 | 9.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 47 | `yt_boundary_theorem` | open_gate | unaudited | critical | 274 | 12.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_boundary_consistency.py` |
| 48 | `neutrino_majorana_local_pfaffian_uniqueness_note` | positive_theorem | unaudited | critical | 273 | 10.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_local_pfaffian_uniqueness.py` |
| 49 | `neutrino_majorana_observable_principle_obstruction_note` | positive_theorem | unaudited | critical | 273 | 8.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_observable_principle_obstruction.py` |
| 50 | `neutrino_majorana_current_stack_exhaustion_note` | positive_theorem | unaudited | critical | 272 | 8.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_current_stack_exhaustion.py` |

## Citation cycle break targets

105 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 559 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 557 | `3d_correction_master_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 551 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 4 | `cycle-0004` | 6 | 551 | `anomaly_forces_time_theorem` | critical | unaudited |
| 5 | `cycle-0005` | 7 | 551 | `anomaly_forces_time_theorem` | critical | unaudited |
| 6 | `cycle-0006` | 4 | 282 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 7 | `cycle-0007` | 5 | 282 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 8 | `cycle-0008` | 6 | 282 | `universal_gr_a1_invariant_section_note` | critical | unaudited |
| 9 | `cycle-0009` | 6 | 282 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 275 | `hypercharge_identification_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 168 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 12 | `cycle-0012` | 4 | 141 | `yt_p2_taste_staircase_beta_functions_note_2026-04-17` | high | unaudited |
| 13 | `cycle-0013` | 2 | 124 | `koide_a1_derivation_status_note` | high | unaudited |
| 14 | `cycle-0014` | 2 | 124 | `koide_a1_derivation_status_note` | high | unaudited |
| 15 | `cycle-0015` | 3 | 124 | `koide_a1_derivation_status_note` | high | unaudited |
| 16 | `cycle-0016` | 4 | 124 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 17 | `cycle-0017` | 4 | 124 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 18 | `cycle-0018` | 4 | 124 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 19 | `cycle-0019` | 4 | 124 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 20 | `cycle-0020` | 4 | 124 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 21 | `cycle-0021` | 4 | 124 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 22 | `cycle-0022` | 4 | 124 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 23 | `cycle-0023` | 4 | 124 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 24 | `cycle-0024` | 5 | 124 | `charged_lepton_koide_cone_algebraic_equivalence_note` | critical | unaudited |
| 25 | `cycle-0025` | 5 | 124 | `charged_lepton_koide_cone_algebraic_equivalence_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
