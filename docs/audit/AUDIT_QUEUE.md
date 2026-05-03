# Audit Queue

**Generated:** 2026-05-03T11:40:34.290733+00:00
**Total pending:** 775
**Ready (all deps already at retained-grade or metadata tiers):** 121

By criticality:
- `critical`: 81
- `high`: 222
- `medium`: 270
- `leaf`: 202

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 329 | 11.87 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 2 | `planck_boundary_density_extension_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 327 | 14.36 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 3 | `physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30` | positive_theorem | unaudited | critical | 327 | 8.86 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_hermitian_hamiltonian_and_sme_bridge.py` |
| 4 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 326 | 14.85 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 5 | `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 326 | 10.85 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cluster_decomposition_check.py` |
| 6 | `architecture_note_directional_measure` | bounded_theorem | unaudited | critical | 325 | 10.35 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `physical_lattice_necessity_note` | no_go | unaudited | critical | 324 | 15.34 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_lattice_necessity.py` |
| 8 | `planck_parent_source_hidden_character_no_go_note_2026-04-24` | no_go | unaudited | critical | 323 | 13.34 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_parent_source_hidden_character_nogo.py` |
| 9 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 323 | 12.34 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 10 | `holographic_probe_note_2026-04-11` | bounded_theorem | unaudited | critical | 323 | 9.84 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_holographic_probe.py` |
| 11 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 322 | 13.34 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `area_law_algebraic_spectrum_entropy_no_go_note_2026-04-25` | bounded_theorem | unaudited | critical | 321 | 12.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py` |
| 13 | `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 321 | 12.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_edge_entropy_selector_no_go.py` |
| 14 | `i3_zero_exact_theorem_note` | positive_theorem | unaudited | critical | 321 | 12.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_born_rule_derived.py` |
| 15 | `action_normalization_note` | bounded_theorem | unaudited | critical | 321 | 10.33 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_action_normalization.py` |
| 16 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 321 | 9.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 17 | `first_order_coframe_unconditionality_no_go_theorem_note_2026-04-30` | no_go | unaudited | critical | 321 | 8.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_first_order_coframe_unconditionality_no_go.py` |
| 18 | `substrate_to_p_a_forcing_theorem_note_2026-04-30` | no_go | unaudited | critical | 321 | 8.83 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_substrate_to_p_a_forcing.py` |
| 19 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | positive_theorem | unaudited | critical | 261 | 11.53 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 20 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | bounded_theorem | unaudited | critical | 260 | 11.03 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 21 | `gauge_vacuum_plaquette_infinite_hierarchy_obstruction_note` | open_gate | unaudited | critical | 258 | 10.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py` |
| 22 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | unaudited | critical | 258 | 10.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 23 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 258 | 10.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 24 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 258 | 10.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 25 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 258 | 10.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 26 | `alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30` | bounded_theorem | unaudited | critical | 250 | 9.97 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_s_direct_wilson_loop.py` |
| 27 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 149 | 14.73 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 64 | 14.02 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `cl3_color_automorphism_theorem` | positive_theorem | unaudited | critical | 52 | 13.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 30 | `cpt_exact_note` | positive_theorem | unaudited | critical | 326 | 17.35 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 326 | 11.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 32 | `planck_finite_response_no_go_note_2026-04-24` | no_go | unaudited | critical | 322 | 12.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_finite_response_nogo.py` |
| 33 | `boundary_law_robustness_note_2026-04-11` | bounded_theorem | unaudited | critical | 322 | 9.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_boundary_law_robustness.py` |
| 34 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 321 | 13.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 35 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 321 | 12.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 36 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 321 | 11.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 37 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 320 | 22.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 38 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 320 | 14.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 39 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 320 | 14.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 40 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 320 | 14.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 41 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 320 | 14.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 42 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 320 | 14.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 320 | 13.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 44 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 320 | 12.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 45 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 320 | 12.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 46 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 320 | 12.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 47 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 320 | 12.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 48 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 320 | 11.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 49 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 320 | 11.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 320 | 9.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |

Full queue lives in `data/audit_queue.json`.
