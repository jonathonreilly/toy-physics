# Audit Queue

**Generated:** 2026-05-03T11:52:49.526358+00:00
**Total pending:** 776
**Ready (all deps already at retained-grade or metadata tiers):** 121

By criticality:
- `critical`: 80
- `high`: 222
- `medium`: 271
- `leaf`: 203

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30` | positive_theorem | unaudited | critical | 290 | 8.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_hermitian_hamiltonian_and_sme_bridge.py` |
| 2 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 289 | 14.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 3 | `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 289 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cluster_decomposition_check.py` |
| 4 | `physical_lattice_necessity_note` | no_go | unaudited | critical | 288 | 15.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_lattice_necessity.py` |
| 5 | `architecture_note_directional_measure` | bounded_theorem | unaudited | critical | 288 | 10.18 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 6 | `planck_parent_source_hidden_character_no_go_note_2026-04-24` | no_go | unaudited | critical | 286 | 13.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_parent_source_hidden_character_nogo.py` |
| 7 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 286 | 12.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 8 | `holographic_probe_note_2026-04-11` | bounded_theorem | unaudited | critical | 286 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_holographic_probe.py` |
| 9 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 285 | 13.16 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `area_law_algebraic_spectrum_entropy_no_go_note_2026-04-25` | bounded_theorem | unaudited | critical | 284 | 12.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py` |
| 11 | `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 284 | 12.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_edge_entropy_selector_no_go.py` |
| 12 | `i3_zero_exact_theorem_note` | positive_theorem | unaudited | critical | 284 | 12.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_born_rule_derived.py` |
| 13 | `action_normalization_note` | bounded_theorem | unaudited | critical | 284 | 10.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_action_normalization.py` |
| 14 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 284 | 9.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 15 | `first_order_coframe_unconditionality_no_go_theorem_note_2026-04-30` | no_go | unaudited | critical | 284 | 8.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_first_order_coframe_unconditionality_no_go.py` |
| 16 | `substrate_to_p_a_forcing_theorem_note_2026-04-30` | no_go | unaudited | critical | 284 | 8.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_substrate_to_p_a_forcing.py` |
| 17 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | positive_theorem | unaudited | critical | 268 | 11.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 18 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | bounded_theorem | unaudited | critical | 267 | 11.07 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 19 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 20 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | unaudited | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 21 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 22 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 23 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 265 | 10.55 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 24 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 71 | 13.67 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 64 | 14.02 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `cl3_color_automorphism_theorem` | positive_theorem | unaudited | critical | 52 | 13.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 27 | `cpt_exact_note` | positive_theorem | unaudited | critical | 289 | 17.18 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 289 | 11.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 29 | `planck_finite_response_no_go_note_2026-04-24` | no_go | unaudited | critical | 285 | 12.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_finite_response_nogo.py` |
| 30 | `boundary_law_robustness_note_2026-04-11` | bounded_theorem | unaudited | critical | 285 | 9.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_boundary_law_robustness.py` |
| 31 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 284 | 13.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 32 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 284 | 12.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 33 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 284 | 11.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 34 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 283 | 22.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 35 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 283 | 14.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 36 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 283 | 14.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 37 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 283 | 14.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 38 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 283 | 14.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 39 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 283 | 14.15 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 283 | 13.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 41 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 283 | 12.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 42 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 283 | 12.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 43 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 283 | 12.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 44 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 283 | 12.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 45 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 283 | 11.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 46 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 283 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 47 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 283 | 9.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 48 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 283 | 8.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 49 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 267 | 11.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 50 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 266 | 9.56 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |

Full queue lives in `data/audit_queue.json`.
