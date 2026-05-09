# Audit Queue

**Total pending:** 986
**Ready (all deps already at retained-grade or metadata tiers):** 57

By criticality:
- `critical`: 136
- `high`: 360
- `medium`: 258
- `leaf`: 232

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_casimir_fundamental_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 488 | 13.43 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/su3_casimir_fundamental_check.py` |
| 2 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | unaudited | critical | 487 | 11.43 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 3 | `universal_gr_invariant_nonlinear_completion_note` | positive_theorem | unaudited | critical | 295 | 9.21 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_invariant_nonlinear_completion.py` |
| 4 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 585 | 27.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 5 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 575 | 19.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 6 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 575 | 10.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 7 | `cpt_exact_note` | positive_theorem | unaudited | critical | 573 | 20.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 8 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 573 | 10.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 9 | `lensing_combined_invariant_note` | positive_theorem | unaudited | critical | 573 | 10.16 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `3d_correction_master_note` | positive_theorem | unaudited | critical | 573 | 9.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/dispersion_3d_lattice.py` |
| 11 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 570 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 12 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 569 | 14.65 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 569 | 12.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 14 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 568 | 15.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 15 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 567 | 28.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 16 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 567 | 16.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 17 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 567 | 16.15 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 567 | 15.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 19 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 567 | 14.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 20 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 567 | 14.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 21 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 567 | 13.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 22 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 567 | 13.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 23 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 516 | 37.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 24 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 493 | 12.95 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 25 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 492 | 12.45 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 26 | `g_bare_rigidity_theorem_note` | positive_theorem | unaudited | critical | 487 | 12.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 27 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 486 | 29.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 28 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 486 | 16.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |
| 29 | `g_bare_hilbert_schmidt_rigidity_theorem_note_2026-05-07` | positive_theorem | unaudited | critical | 486 | 16.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_audit_residual_closure.py` |
| 30 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | positive_theorem | unaudited | critical | 486 | 14.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_audit_residual_closure.py` |
| 31 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | positive_theorem | unaudited | critical | 486 | 12.93 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 32 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 486 | 11.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 33 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 486 | 10.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_canonical_convention_narrow.py` |
| 34 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 486 | 10.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 35 | `g_bare_constraint_vs_convention_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 486 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 36 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 486 | 9.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_canonical_convention_narrow.py` |
| 37 | `three_generation_observable_no_proper_quotient_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 443 | 12.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` |
| 38 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 442 | 27.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 39 | `one_generation_matter_closure_note` | bounded_theorem | unaudited | critical | 403 | 24.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 40 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 379 | 17.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 41 | `s3_time_spacetime_tensor_primitive_note` | bounded_theorem | unaudited | critical | 375 | 10.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_time_spacetime_tensor_primitive.py` |
| 42 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 331 | 10.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 43 | `neutrino_majorana_operator_axiom_first_note` | positive_theorem | unaudited | critical | 321 | 14.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_operator.py` |
| 44 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | critical | 319 | 11.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 45 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | critical | 317 | 12.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 46 | `neutrino_majorana_pfaffian_extension_note` | positive_theorem | unaudited | critical | 316 | 11.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |
| 47 | `neutrino_majorana_pfaffian_axiom_boundary_note` | no_go | unaudited | critical | 315 | 8.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py` |
| 48 | `neutrino_majorana_pfaffian_no_forcing_theorem_note` | positive_theorem | unaudited | critical | 314 | 12.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py` |
| 49 | `neutrino_majorana_current_atlas_nonrealization_note` | positive_theorem | unaudited | critical | 314 | 10.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py` |
| 50 | `neutrino_majorana_charge_two_primitive_reduction_note` | positive_theorem | unaudited | critical | 313 | 10.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` |

## Citation cycle break targets

184 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 575 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 573 | `3d_correction_master_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 570 | `bh_entropy_derived_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 567 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 6 | 567 | `anomaly_forces_time_theorem` | critical | unaudited |
| 6 | `cycle-0006` | 7 | 567 | `anomaly_forces_time_theorem` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 486 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 486 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 9 | `cycle-0009` | 3 | 486 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 10 | `cycle-0010` | 6 | 486 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 11 | `cycle-0011` | 7 | 486 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 12 | `cycle-0012` | 8 | 486 | `alpha_s_derived_note` | critical | audited_conditional |
| 13 | `cycle-0013` | 8 | 486 | `alpha_s_derived_note` | critical | audited_conditional |
| 14 | `cycle-0014` | 8 | 486 | `alpha_s_derived_note` | critical | audited_conditional |
| 15 | `cycle-0015` | 8 | 486 | `alpha_s_derived_note` | critical | audited_conditional |
| 16 | `cycle-0016` | 4 | 294 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 17 | `cycle-0017` | 5 | 294 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 18 | `cycle-0018` | 6 | 294 | `universal_gr_a1_invariant_section_note` | critical | unaudited |
| 19 | `cycle-0019` | 6 | 294 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 287 | `hypercharge_identification_note` | critical | unaudited |
| 21 | `cycle-0021` | 5 | 247 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | high | unaudited |
| 22 | `cycle-0022` | 5 | 247 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | high | unaudited |
| 23 | `cycle-0023` | 5 | 247 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | high | unaudited |
| 24 | `cycle-0024` | 5 | 247 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | high | unaudited |
| 25 | `cycle-0025` | 5 | 247 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | high | unaudited |

Full queue lives in `data/audit_queue.json`.
