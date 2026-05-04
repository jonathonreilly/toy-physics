# Audit Queue

**Total pending:** 920
**Ready (all deps already at retained-grade or metadata tiers):** 74

By criticality:
- `critical`: 105
- `high`: 337
- `medium`: 282
- `leaf`: 196

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 263 | 10.54 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |
| 2 | `yt_bridge_uv_class_uniqueness_note` | bounded_theorem | unaudited | critical | 262 | 9.54 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_uv_class_uniqueness.py` |
| 3 | `yt_color_projection_correction_note` | positive_theorem | unaudited | critical | 258 | 12.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 4 | `dm_leptogenesis_transport_status_note_2026-04-16` | positive_theorem | unaudited | critical | 202 | 15.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_transport_status.py` |
| 5 | `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24` | no_go | unaudited | critical | 155 | 15.29 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py` |
| 6 | `universal_gr_lorentzian_global_atlas_closure_note` | positive_theorem | unaudited | critical | 111 | 14.81 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 413 | 13.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 8 | `cpt_exact_note` | positive_theorem | unaudited | critical | 409 | 17.68 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 409 | 11.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 10 | `born_scattering_comparison_note` | positive_theorem | unaudited | critical | 408 | 10.68 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gaussian_beam_eikonal.py` |
| 11 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 404 | 14.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 12 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 404 | 14.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 13 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 404 | 13.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 14 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 404 | 12.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 15 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 403 | 24.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 16 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 403 | 16.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 17 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 403 | 15.66 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 403 | 14.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 19 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 403 | 14.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 20 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 403 | 13.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 21 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 403 | 13.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 22 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 403 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 23 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 403 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 24 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 403 | 12.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 25 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 403 | 12.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 26 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 403 | 11.66 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `architecture_note_directional_measure` | bounded_theorem | unaudited | critical | 403 | 10.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/architecture_directional_measure_table_runner_2026_05_03.py` |
| 28 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 403 | 9.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 29 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 403 | 9.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 30 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 395 | 9.63 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 31 | `left_handed_charge_matching_note` | positive_theorem | unaudited | critical | 394 | 23.63 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 32 | `g_bare_rescaling_freedom_removal_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 367 | 9.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 33 | `g_bare_constraint_vs_convention_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 366 | 9.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 34 | `g_bare_derivation_note` | positive_theorem | unaudited | critical | 365 | 15.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 35 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 361 | 11.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 36 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 360 | 12.00 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 37 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 355 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 38 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 355 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 39 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 355 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 40 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 355 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 41 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 355 | 10.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 42 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 354 | 19.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 43 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 344 | 8.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 44 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 343 | 30.93 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 45 | `one_generation_matter_closure_note` | positive_theorem | unaudited | critical | 338 | 22.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 46 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 288 | 22.18 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 47 | `neutrino_majorana_operator_axiom_first_note` | positive_theorem | unaudited | critical | 283 | 14.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_operator.py` |
| 48 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | critical | 281 | 11.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 49 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | critical | 279 | 12.13 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 50 | `neutrino_majorana_pfaffian_extension_note` | positive_theorem | unaudited | critical | 278 | 11.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |

Full queue lives in `data/audit_queue.json`.
