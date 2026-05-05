# Audit Queue

**Total pending:** 862
**Ready (all deps already at retained-grade or metadata tiers):** 5

By criticality:
- `critical`: 549
- `high`: 23
- `medium`: 115
- `leaf`: 175

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block1_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 434 | 10.27 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_intertwiner_engine.py` |
| 2 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 308 | 10.77 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 3 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 4 | `persistent_object_top4_multistage_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 288 | 9.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_top4_multistage_transfer_sweep.py` |
| 5 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 6 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 447 | 13.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 7 | `cpt_exact_note` | positive_theorem | unaudited | critical | 443 | 17.79 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 443 | 11.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 9 | `born_scattering_comparison_note` | positive_theorem | unaudited | critical | 442 | 10.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gaussian_beam_eikonal.py` |
| 10 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 438 | 14.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 11 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 438 | 14.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 12 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 438 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 13 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 438 | 12.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 14 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 437 | 25.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 15 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 437 | 16.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 16 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 437 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 437 | 14.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 18 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 437 | 14.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 19 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 437 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 20 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 437 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 21 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 437 | 13.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 22 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 437 | 13.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 23 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 437 | 12.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 24 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 437 | 12.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 25 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 437 | 11.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `architecture_note_directional_measure` | bounded_theorem | unaudited | critical | 437 | 10.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/architecture_directional_measure_table_runner_2026_05_03.py` |
| 27 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 437 | 9.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 28 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 437 | 9.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 29 | `g_bare_derivation_note` | positive_theorem | unaudited | critical | 435 | 15.77 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 30 | `su3_wigner_intertwiner_block2_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 433 | 9.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_4fold_haar_projector.py` |
| 31 | `su3_wigner_intertwiner_block3_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 432 | 9.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_geometry.py` |
| 32 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 431 | 12.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 33 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 431 | 9.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 34 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 430 | 12.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 35 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 425 | 12.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 36 | `gauge_vacuum_plaquette_distinct_shell_theorem_note` | bounded_theorem | unaudited | critical | 425 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py` |
| 37 | `gauge_vacuum_plaquette_reduction_existence_theorem_note` | bounded_theorem | unaudited | critical | 425 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py` |
| 38 | `gauge_vacuum_plaquette_spectral_measure_theorem_note` | bounded_theorem | unaudited | critical | 425 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py` |
| 39 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 425 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 40 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 424 | 21.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 41 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 417 | 9.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 42 | `left_handed_charge_matching_note` | positive_theorem | unaudited | critical | 416 | 23.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 43 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 400 | 9.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 44 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 399 | 31.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 45 | `one_generation_matter_closure_note` | positive_theorem | unaudited | critical | 365 | 22.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 46 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 358 | 30.49 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 47 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 357 | 30.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 48 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 357 | 22.98 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 49 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 354 | 22.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 50 | `gate_b_grown_joint_package_note` | bounded_theorem | unaudited | critical | 346 | 12.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_grown_joint_package.py` |

## Citation cycle break targets

168 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 437 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 2 | `cycle-0002` | 7 | 437 | `anomaly_forces_time_theorem` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 321 | `yt_explicit_systematic_budget_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 319 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 319 | `universal_qg_projective_schur_closure_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 319 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 302 | `higgs_from_lattice_note` | critical | unaudited |
| 8 | `cycle-0008` | 2 | 302 | `higgs_mass_derived_note` | critical | audited_conditional |
| 9 | `cycle-0009` | 2 | 298 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 289 | `universal_gr_tensor_quotient_uniqueness_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 288 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 288 | `koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18` | critical | unaudited |
| 13 | `cycle-0013` | 2 | 288 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 288 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 287 | `charged_lepton_ue_identity_via_z3_trichotomy_note_2026-04-17` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 287 | `quark_issr1_bicac_forcing_theorem_note_2026-04-19` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 286 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 284 | `abcc_cp_phase_no_go_theorem_note_2026-04-19` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 284 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 284 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 284 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 22 | `cycle-0022` | 2 | 284 | `dm_pmns_graph_first_ordered_chain_nonzero_current_activation_theorem_note_2026-04-21` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 284 | `hadron_mass_lane1_theorem_plan_support_note_2026-04-27` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 284 | `koide_a1_fractional_topology_no_go_synthesis_note_2026-04-24` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 284 | `koide_eigenvalue_q23_surface_theorem_note_2026-04-20` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
