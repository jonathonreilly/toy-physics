# Audit Queue

**Total pending:** 867
**Ready (all deps already at retained-grade or metadata tiers):** 31

By criticality:
- `critical`: 72
- `high`: 312
- `medium`: 288
- `leaf`: 195

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 406 | 10.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 2 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 522 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 3 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 520 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 4 | `lensing_combined_invariant_note` | positive_theorem | unaudited | critical | 520 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 5 | `3d_correction_master_note` | positive_theorem | unaudited | critical | 520 | 9.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/dispersion_3d_lattice.py` |
| 6 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 516 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 516 | 12.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 8 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 514 | 16.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 9 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 514 | 16.01 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 514 | 15.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 11 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 514 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 12 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 514 | 14.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 13 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 514 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 14 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 514 | 13.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 15 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 514 | 11.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 16 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 514 | 10.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 17 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 402 | 12.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 18 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 371 | 10.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 19 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 370 | 25.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 20 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 356 | 23.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 21 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 343 | 16.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 22 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 339 | 10.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 23 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 291 | 10.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 24 | `neutrino_majorana_operator_axiom_first_note` | positive_theorem | unaudited | critical | 277 | 14.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_operator.py` |
| 25 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | critical | 275 | 11.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 26 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | critical | 273 | 12.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 27 | `neutrino_majorana_pfaffian_extension_note` | positive_theorem | unaudited | critical | 272 | 11.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |
| 28 | `neutrino_majorana_pfaffian_axiom_boundary_note` | no_go | unaudited | critical | 271 | 8.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py` |
| 29 | `neutrino_majorana_pfaffian_no_forcing_theorem_note` | positive_theorem | unaudited | critical | 270 | 12.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py` |
| 30 | `neutrino_majorana_current_atlas_nonrealization_note` | positive_theorem | unaudited | critical | 270 | 10.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py` |
| 31 | `neutrino_majorana_charge_two_primitive_reduction_note` | positive_theorem | unaudited | critical | 269 | 10.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` |
| 32 | `neutrino_majorana_unique_source_slot_note` | positive_theorem | unaudited | critical | 268 | 12.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_unique_source_slot.py` |
| 33 | `s3_time_transfer_matrix_bridge_note` | bounded_theorem | unaudited | critical | 266 | 10.06 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_transfer_matrix_bridge.py` |
| 34 | `neutrino_majorana_phase_removal_note` | positive_theorem | unaudited | critical | 265 | 10.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_phase_removal.py` |
| 35 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 262 | 11.04 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 36 | `neutrino_majorana_canonical_local_block_note` | positive_theorem | unaudited | critical | 261 | 10.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_canonical_local_block.py` |
| 37 | `neutrino_majorana_z3_nonactivation_theorem_note` | positive_theorem | unaudited | critical | 258 | 12.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_z3_nonactivation_theorem.py` |
| 38 | `yt_boundary_theorem` | open_gate | unaudited | critical | 257 | 12.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_boundary_consistency.py` |
| 39 | `neutrino_majorana_local_pfaffian_uniqueness_note` | positive_theorem | unaudited | critical | 256 | 10.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_local_pfaffian_uniqueness.py` |
| 40 | `neutrino_majorana_observable_principle_obstruction_note` | positive_theorem | unaudited | critical | 256 | 8.51 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_observable_principle_obstruction.py` |
| 41 | `neutrino_majorana_current_stack_exhaustion_note` | positive_theorem | unaudited | critical | 255 | 8.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_current_stack_exhaustion.py` |
| 42 | `neutrino_majorana_nambu_source_principle_note` | positive_theorem | unaudited | critical | 254 | 10.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_nambu_source_principle.py` |
| 43 | `neutrino_majorana_source_ray_theorem_note` | positive_theorem | unaudited | critical | 253 | 12.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_source_ray_theorem.py` |
| 44 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 250 | 14.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 45 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 250 | 9.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 46 | `neutrino_majorana_nambu_radial_observable_note` | positive_theorem | unaudited | critical | 250 | 9.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_nambu_radial_observable.py` |
| 47 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 231 | 24.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 48 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 202 | 19.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 49 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 200 | 21.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 50 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 190 | 19.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |

## Citation cycle break targets

37 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 522 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | audited_conditional |
| 2 | `cycle-0002` | 2 | 520 | `3d_correction_master_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 514 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 4 | `cycle-0004` | 7 | 514 | `anomaly_forces_time_theorem` | critical | audited_conditional |
| 5 | `cycle-0005` | 2 | 250 | `hypercharge_identification_note` | critical | unaudited |
| 6 | `cycle-0006` | 4 | 149 | `universal_gr_constraint_action_stationarity_note` | high | unaudited |
| 7 | `cycle-0007` | 5 | 149 | `universal_gr_constraint_action_stationarity_note` | high | unaudited |
| 8 | `cycle-0008` | 6 | 149 | `universal_gr_a1_invariant_section_note` | high | unaudited |
| 9 | `cycle-0009` | 6 | 149 | `universal_gr_constraint_action_stationarity_note` | high | unaudited |
| 10 | `cycle-0010` | 4 | 124 | `yt_p2_taste_staircase_beta_functions_note_2026-04-17` | high | unaudited |
| 11 | `cycle-0011` | 6 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 12 | `cycle-0012` | 7 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 13 | `cycle-0013` | 7 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 14 | `cycle-0014` | 8 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 15 | `cycle-0015` | 9 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 16 | `cycle-0016` | 12 | 107 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 17 | `cycle-0017` | 14 | 107 | `charged_lepton_koide_cone_algebraic_equivalence_note` | high | unaudited |
| 18 | `cycle-0018` | 2 | 89 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | audited_conditional |
| 19 | `cycle-0019` | 4 | 44 | `dm_pmns_cp_orientation_parity_reduction_note_2026-04-20` | medium | unaudited |
| 20 | `cycle-0020` | 4 | 38 | `publication.ci3_z3.claims_table` | high | unaudited |
| 21 | `cycle-0021` | 5 | 38 | `publication.ci3_z3.claims_table` | high | unaudited |
| 22 | `cycle-0022` | 4 | 35 | `localized_source_response_sweep_note` | medium | unaudited |
| 23 | `cycle-0023` | 5 | 35 | `mesoscopic_surrogate_backreaction_note` | high | unaudited |
| 24 | `cycle-0024` | 2 | 26 | `newton_derivation_note` | medium | unaudited |
| 25 | `cycle-0025` | 4 | 23 | `signed_gravity_cl3z3_source_character_derivation_note` | high | unaudited |

Full queue lives in `data/audit_queue.json`.
