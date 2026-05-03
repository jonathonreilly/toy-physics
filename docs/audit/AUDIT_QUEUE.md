# Audit Queue

**Generated:** 2026-05-03T11:33:25.416971+00:00
**Total pending:** 557
**Ready (all deps already at retained-grade or metadata tiers):** 50

By criticality:
- `critical`: 72
- `high`: 200
- `medium`: 154
- `leaf`: 131

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | - | unaudited | critical | 319 | 14.82 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 2 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 318 | 15.32 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 3 | `planck_boundary_density_extension_theorem_note_2026-04-24` | - | unaudited | critical | 317 | 17.31 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 4 | `physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30` | - | unaudited | critical | 317 | 12.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_hermitian_hamiltonian_and_sme_bridge.py` |
| 5 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | - | unaudited | critical | 316 | 17.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 6 | `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | - | unaudited | critical | 316 | 13.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cluster_decomposition_check.py` |
| 7 | `physical_lattice_necessity_note` | - | unaudited | critical | 314 | 18.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_lattice_necessity.py` |
| 8 | `planck_parent_source_hidden_character_no_go_note_2026-04-24` | - | unaudited | critical | 313 | 17.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_parent_source_hidden_character_nogo.py` |
| 9 | `bh_entropy_derived_note` | - | unaudited | critical | 313 | 15.29 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 10 | `holographic_probe_note_2026-04-11` | - | unaudited | critical | 313 | 12.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_holographic_probe.py` |
| 11 | `area_law_algebraic_spectrum_entropy_no_go_note_2026-04-25` | - | unaudited | critical | 311 | 15.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py` |
| 12 | `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25` | - | unaudited | critical | 311 | 15.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_edge_entropy_selector_no_go.py` |
| 13 | `gravity_clean_derivation_note` | - | unaudited | critical | 311 | 15.79 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 14 | `i3_zero_exact_theorem_note` | - | unaudited | critical | 311 | 15.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_born_rule_derived.py` |
| 15 | `action_normalization_note` | - | unaudited | critical | 311 | 13.29 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_action_normalization.py` |
| 16 | `light_cone_framing_note` | - | unaudited | critical | 311 | 12.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 17 | `architecture_note_directional_measure` | - | unaudited | critical | 311 | 11.79 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `first_order_coframe_unconditionality_no_go_theorem_note_2026-04-30` | - | unaudited | critical | 311 | 11.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_first_order_coframe_unconditionality_no_go.py` |
| 19 | `substrate_to_p_a_forcing_theorem_note_2026-04-30` | - | unaudited | critical | 311 | 11.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_substrate_to_p_a_forcing.py` |
| 20 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | - | unaudited | critical | 252 | 11.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 21 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | - | unaudited | critical | 251 | 10.98 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 22 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 141 | 14.65 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 23 | `cl3_color_automorphism_theorem` | positive_theorem | unaudited | critical | 45 | 13.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 24 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 316 | 14.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 25 | `planck_finite_response_no_go_note_2026-04-24` | - | unaudited | critical | 312 | 15.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_finite_response_nogo.py` |
| 26 | `boundary_law_robustness_note_2026-04-11` | bounded_theorem | unaudited | critical | 312 | 12.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_boundary_law_robustness.py` |
| 27 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 311 | 16.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 28 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 311 | 15.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 29 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 311 | 14.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 30 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 310 | 21.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 31 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 310 | 17.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 32 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 310 | 17.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 33 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 310 | 17.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 34 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 310 | 17.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 35 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 310 | 17.28 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 310 | 16.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 37 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 310 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 38 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 310 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 39 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 310 | 15.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 40 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 310 | 15.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 41 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | - | unaudited | critical | 310 | 14.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 42 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 310 | 14.28 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 310 | 12.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 44 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 310 | 11.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 45 | `one_generation_matter_closure_note` | - | unaudited | critical | 268 | 22.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 46 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 251 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 47 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 250 | 9.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 48 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 248 | 17.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 49 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 240 | 28.91 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 50 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 139 | 19.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |

Full queue lives in `data/audit_queue.json`.
