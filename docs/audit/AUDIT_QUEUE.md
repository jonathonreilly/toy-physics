# Audit Queue

**Total pending:** 837
**Ready (all deps already at retained-grade or metadata tiers):** 4

By criticality:
- `critical`: 60
- `high`: 302
- `medium`: 281
- `leaf`: 194

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 506 | 13.99 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 2 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 506 | 11.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 3 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 504 | 25.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 4 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 504 | 16.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 5 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 504 | 15.98 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 6 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 504 | 14.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 7 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 504 | 13.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 8 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 504 | 13.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 9 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 504 | 13.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 10 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 504 | 13.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 11 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 417 | 24.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 12 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 398 | 12.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 13 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 360 | 10.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 14 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 359 | 24.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 15 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 344 | 23.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 16 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 335 | 16.89 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 17 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 331 | 10.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 18 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 276 | 10.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 19 | `neutrino_majorana_operator_axiom_first_note` | positive_theorem | unaudited | critical | 261 | 14.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_operator.py` |
| 20 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | critical | 259 | 11.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 21 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | critical | 257 | 12.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 22 | `neutrino_majorana_pfaffian_extension_note` | positive_theorem | unaudited | critical | 256 | 11.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |
| 23 | `neutrino_majorana_pfaffian_axiom_boundary_note` | no_go | unaudited | critical | 255 | 8.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py` |
| 24 | `neutrino_majorana_pfaffian_no_forcing_theorem_note` | positive_theorem | unaudited | critical | 254 | 11.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py` |
| 25 | `neutrino_majorana_current_atlas_nonrealization_note` | positive_theorem | unaudited | critical | 254 | 9.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py` |
| 26 | `neutrino_majorana_charge_two_primitive_reduction_note` | positive_theorem | unaudited | critical | 253 | 9.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` |
| 27 | `neutrino_majorana_unique_source_slot_note` | positive_theorem | unaudited | critical | 252 | 12.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_unique_source_slot.py` |
| 28 | `hypercharge_identification_note` | bounded_theorem | unaudited | critical | 251 | 15.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hypercharge_identification.py` |
| 29 | `lhcm_matter_assignment_from_su3_representation_note_2026-05-02` | positive_theorem | unaudited | critical | 251 | 9.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lhcm_matter_assignment.py` |
| 30 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 230 | 24.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 31 | `ckm_atlas_axiom_closure_note` | positive_theorem | unaudited | critical | 213 | 23.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 32 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 194 | 18.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 33 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 192 | 20.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 34 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 183 | 17.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 35 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 182 | 18.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 36 | `dm_leptogenesis_transport_status_note_2026-04-16` | positive_theorem | unaudited | critical | 166 | 14.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_transport_status.py` |
| 37 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 152 | 28.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 38 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 149 | 20.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 39 | `quark_projector_parameter_audit_note_2026-04-19` | bounded_theorem | unaudited | critical | 137 | 17.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_projector_parameter_audit.py` |
| 40 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 126 | 14.49 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 124 | 20.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 42 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 117 | 15.38 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 109 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 44 | `charged_lepton_mass_hierarchy_review_note_2026-04-17` | bounded_theorem | unaudited | critical | 107 | 14.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_observable_curvature.py` |
| 45 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 89 | 28.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 46 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 89 | 27.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 47 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 84 | 19.91 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 48 | `down_type_mass_ratio_ckm_dual_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 81 | 14.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 49 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 70 | 23.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 50 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 67 | 13.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |

## Citation cycle break targets

35 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 504 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 2 | `cycle-0002` | 7 | 504 | `anomaly_forces_time_theorem` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 251 | `hypercharge_identification_note` | critical | unaudited |
| 4 | `cycle-0004` | 4 | 149 | `universal_gr_constraint_action_stationarity_note` | high | unaudited |
| 5 | `cycle-0005` | 5 | 149 | `universal_gr_constraint_action_stationarity_note` | high | unaudited |
| 6 | `cycle-0006` | 6 | 149 | `universal_gr_a1_invariant_section_note` | high | unaudited |
| 7 | `cycle-0007` | 6 | 149 | `universal_gr_constraint_action_stationarity_note` | high | unaudited |
| 8 | `cycle-0008` | 4 | 124 | `yt_p2_taste_staircase_beta_functions_note_2026-04-17` | high | unaudited |
| 9 | `cycle-0009` | 6 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 10 | `cycle-0010` | 7 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 11 | `cycle-0011` | 7 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 12 | `cycle-0012` | 8 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 13 | `cycle-0013` | 9 | 107 | `koide_brannen_phase_reduction_theorem_note_2026-04-20` | high | unaudited |
| 14 | `cycle-0014` | 12 | 107 | `charged_lepton_koide_review_packet_2026-04-18` | high | unaudited |
| 15 | `cycle-0015` | 14 | 107 | `charged_lepton_koide_cone_algebraic_equivalence_note` | high | unaudited |
| 16 | `cycle-0016` | 2 | 89 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 17 | `cycle-0017` | 4 | 44 | `dm_pmns_cp_orientation_parity_reduction_note_2026-04-20` | medium | unaudited |
| 18 | `cycle-0018` | 4 | 38 | `publication.ci3_z3.claims_table` | high | unaudited |
| 19 | `cycle-0019` | 5 | 38 | `publication.ci3_z3.claims_table` | high | unaudited |
| 20 | `cycle-0020` | 4 | 35 | `localized_source_response_sweep_note` | medium | unaudited |
| 21 | `cycle-0021` | 5 | 35 | `mesoscopic_surrogate_backreaction_note` | high | unaudited |
| 22 | `cycle-0022` | 2 | 26 | `newton_derivation_note` | medium | unaudited |
| 23 | `cycle-0023` | 4 | 23 | `signed_gravity_cl3z3_source_character_derivation_note` | high | unaudited |
| 24 | `cycle-0024` | 4 | 16 | `signed_gravity_boundary_coframe_chi_probe_note` | medium | unaudited |
| 25 | `cycle-0025` | 4 | 16 | `signed_gravity_chi_selector_theorem_or_nogo_note` | high | unaudited |

Full queue lives in `data/audit_queue.json`.
