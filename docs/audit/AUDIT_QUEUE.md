# Audit Queue

**Total pending:** 843
**Ready (all deps already at retained-grade or metadata tiers):** 17

By criticality:
- `critical`: 51
- `high`: 273
- `medium`: 301
- `leaf`: 218

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 453 | 12.33 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 2 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 446 | 14.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 3 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 388 | 10.10 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 4 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 451 | 16.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 5 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 449 | 13.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 6 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 448 | 13.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 7 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 447 | 13.81 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 445 | 13.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 9 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 444 | 15.80 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 441 | 13.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 11 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 440 | 11.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 12 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 435 | 14.77 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 13 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 426 | 24.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 14 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 406 | 24.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 15 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 384 | 12.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 16 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 348 | 9.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 17 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 347 | 24.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 18 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 333 | 23.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 19 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 267 | 10.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 20 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 265 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 21 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 261 | 10.03 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 22 | `neutrino_majorana_operator_axiom_first_note` | positive_theorem | unaudited | critical | 251 | 14.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_operator.py` |
| 23 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 224 | 24.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 24 | `ckm_atlas_axiom_closure_note` | positive_theorem | unaudited | critical | 202 | 23.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 25 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 184 | 18.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 26 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 182 | 20.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 27 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 172 | 18.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 28 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 144 | 17.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 29 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 129 | 20.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 30 | `dm_leptogenesis_transport_status_note_2026-04-16` | positive_theorem | unaudited | critical | 127 | 14.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_transport_status.py` |
| 31 | `quark_projector_parameter_audit_note_2026-04-19` | bounded_theorem | unaudited | critical | 126 | 16.99 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_projector_parameter_audit.py` |
| 32 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 124 | 14.47 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 122 | 19.94 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 34 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 113 | 27.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 35 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 103 | 15.20 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 88 | 28.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 37 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 83 | 27.39 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 38 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 83 | 19.89 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 39 | `down_type_mass_ratio_ckm_dual_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 80 | 14.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 40 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | positive_theorem | claim_type_backfill_reaudit | critical | 70 | 15.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 41 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 69 | 23.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 42 | `cosmological_constant_spectral_gap_identity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 63 | 17.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmological_constant_spectral_gap_identity.py` |
| 43 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 59 | 18.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 44 | `n_eff_from_three_generations_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 54 | 14.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_n_eff_from_three_generations.py` |
| 45 | `koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 51 | 13.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_background_zero_z_erasure_criterion.py` |
| 46 | `matter_radiation_equality_structural_identity_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 51 | 13.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_matter_radiation_equality_structural_identity.py` |
| 47 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 50 | 13.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 48 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 49 | 13.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 49 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 48 | 13.62 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 50 | `higgs_vacuum_explicit_systematic_note` | positive_theorem | unaudited | critical | 47 | 13.09 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |

## Citation cycle break targets

3 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 441 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 216 | `hypercharge_identification_note` | high | unaudited |
| 3 | `cycle-0003` | 2 | 0 | `repo.active_review_queue` | leaf | unaudited |

Full queue lives in `data/audit_queue.json`.
