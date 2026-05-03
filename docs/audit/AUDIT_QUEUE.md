# Audit Queue

**Generated:** 2026-05-03T13:31:50.817855+00:00
**Total pending:** 769
**Ready (all deps already at retained-grade or metadata tiers):** 107

By criticality:
- `critical`: 60
- `high`: 223
- `medium`: 277
- `leaf`: 209

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gauge_vacuum_plaquette_perron_reduction_theorem_note` | positive_theorem | unaudited | critical | 268 | 10.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py` |
| 2 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 268 | 10.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 3 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 268 | 10.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 4 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 268 | 10.57 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 5 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 71 | 13.67 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 6 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 64 | 14.02 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `cl3_color_automorphism_theorem` | positive_theorem | unaudited | critical | 52 | 13.73 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 8 | `cpt_exact_note` | positive_theorem | unaudited | critical | 292 | 17.20 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 291 | 11.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 10 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 286 | 13.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 11 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 286 | 12.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 12 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 286 | 11.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 13 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 285 | 22.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 14 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 285 | 14.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 15 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 285 | 14.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 16 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 285 | 14.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 17 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 285 | 14.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 18 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 285 | 14.16 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 19 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 285 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 20 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 285 | 12.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 21 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 285 | 12.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 22 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 285 | 12.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 23 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 285 | 12.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 24 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 285 | 11.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 25 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 285 | 11.16 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 285 | 9.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 27 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 285 | 8.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 28 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 270 | 11.08 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 29 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 269 | 9.58 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 30 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 268 | 10.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 31 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 267 | 18.57 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 32 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 260 | 8.53 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 33 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 259 | 29.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 34 | `one_generation_matter_closure_note` | positive_theorem | unaudited | critical | 241 | 21.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 35 | `yt_ew_color_projection_theorem` | positive_theorem | unaudited | critical | 224 | 24.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 36 | `yt_ward_identity_derivation_theorem` | open_gate | unaudited | critical | 193 | 26.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 37 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 140 | 15.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 38 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 139 | 15.63 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 39 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | positive_theorem | claim_type_backfill_reaudit | critical | 135 | 15.59 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 40 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 131 | 16.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 41 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 128 | 29.01 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 42 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 127 | 29.50 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 43 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 124 | 20.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 44 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 112 | 23.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 45 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 103 | 19.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 46 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 94 | 15.07 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 47 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 93 | 14.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 48 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 93 | 14.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 49 | `ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 92 | 14.54 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 92 | 14.54 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |

Full queue lives in `data/audit_queue.json`.
