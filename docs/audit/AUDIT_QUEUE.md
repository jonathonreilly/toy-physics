# Audit Queue

**Total pending:** 1134
**Ready (all deps already at retained-grade or metadata tiers):** 118

By criticality:
- `critical`: 695
- `high`: 23
- `medium`: 150
- `leaf`: 266

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `universal_gr_tensor_action_blocker_note` | bounded_theorem | unaudited | critical | 641 | 10.83 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 2 | `gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note` | positive_theorem | unaudited | critical | 612 | 13.76 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_tensor_transfer.py` |
| 3 | `gauge_vacuum_plaquette_local_environment_factorization_theorem_note` | bounded_theorem | unaudited | critical | 611 | 12.76 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py` |
| 4 | `complex_action_note` | bounded_theorem | unaudited | critical | 306 | 11.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_harness.py` |
| 5 | `gravitomagnetic_note` | positive_theorem | unaudited | critical | 306 | 9.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravitomagnetic_portable.py` |
| 6 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 305 | 11.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 7 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 296 | 16.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 8 | `dm_neutrino_bosonic_normalization_theorem_note_2026-04-15` | bounded_theorem | unaudited | critical | 290 | 8.69 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_bosonic_normalization_theorem.py` |
| 9 | `axiom_first_cpt_theorem_stretch_note_2026-04-29` | bounded_theorem | unaudited | critical | 286 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cpt_check.py` |
| 10 | `koide_cl3_selector_gap_note_2026-04-19` | bounded_theorem | unaudited | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `poisson_self_gravity_born_audit_note` | bounded_theorem | unaudited | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_born_audit.py` |
| 12 | `lensing_deflection_note` | bounded_theorem | unaudited | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_deflection_h025_slope_fit_certificate.py` |
| 13 | `poisson_self_gravity_loop_v3_note` | bounded_theorem | unaudited | critical | 285 | 9.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop_v3.py` |
| 14 | `koide_gamma_orbit_selector_bridge_note_2026-04-18` | positive_theorem | unaudited | critical | 284 | 11.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_orbit_selector_bridge.py` |
| 15 | `newton_law_derived_note` | positive_theorem | unaudited | critical | 282 | 12.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 16 | `pmns_commutant_eigenoperator_selector_note` | bounded_theorem | unaudited | critical | 282 | 10.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_commutant_eigenoperator_selector.py` |
| 17 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | critical | 282 | 9.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 18 | `dm_abcc_pmns_nonsingularity_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 282 | 9.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_pmns_nonsingularity_theorem.py` |
| 19 | `gravity_law_cleanup_note` | bounded_theorem | unaudited | critical | 282 | 9.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravity_distance_fixed_geometry.py` |
| 20 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 282 | 9.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 21 | `pmns_three_flux_holonomy_closure_note` | bounded_theorem | unaudited | critical | 282 | 9.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_three_flux_holonomy_closure.py` |
| 22 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 282 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 23 | `cl3_quark_antiquark_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 282 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_quark_antiquark_color_singlet_check.py` |
| 24 | `dm_pmns_asymptotic_source_no_go_note_2026-04-20` | no_go | unaudited | critical | 282 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py` |
| 25 | `staggered_3d_self_gravity_sign_note_2026-04-11` | bounded_theorem | unaudited | critical | 282 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_3d_self_gravity_sign.py` |
| 26 | `charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26` | no_go | unaudited | critical | 281 | 12.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py` |
| 27 | `koide_circulant_character_bridge_narrow_theorem_note_2026-05-09` | positive_theorem | unaudited | critical | 281 | 10.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_character_bridge_narrow.py` |
| 28 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 281 | 10.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 29 | `koide_delta_lattice_wilson_selected_eigenline_no_go_note_2026-04-24` | no_go | unaudited | critical | 281 | 9.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py` |
| 30 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | bounded_theorem | unaudited | critical | 281 | 9.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py` |
| 31 | `circulant_parity_cp_tensor_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 281 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_parity_cp_tensor_narrow.py` |
| 32 | `koide_a1_loop_final_status_2026-04-22` | bounded_theorem | unaudited | critical | 281 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_quartic_potential_derivation.py` |
| 33 | `wave_static_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 281 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 34 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 281 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 35 | `wave_static_fixed_beam_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 281 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_fixed_beam_boundary_sensitivity.py` |
| 36 | `wave_static_matrixfree_fixed_beam_boundary_note` | positive_theorem | unaudited | critical | 281 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 37 | `wave_static_single_source_compare_note` | bounded_theorem | unaudited | critical | 281 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_single_source_compare.py` |
| 38 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 280 | 14.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 39 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 678 | 16.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 40 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 678 | 11.41 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 41 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 676 | 27.40 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 42 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 666 | 15.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 43 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 651 | 21.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 44 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 651 | 10.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 45 | `cpt_exact_note` | positive_theorem | unaudited | critical | 649 | 20.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 46 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 646 | 13.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 47 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 644 | 14.33 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 644 | 10.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 49 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 644 | 9.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 50 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 643 | 18.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |

## Citation cycle break targets

243 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 651 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 642 | `bh_entropy_derived_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 640 | `3d_correction_master_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 640 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 640 | `architecture_note_directional_measure` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 640 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 640 | `discrete_einstein_regge_lift_note` | critical | unaudited |
| 8 | `cycle-0008` | 3 | 640 | `area_law_coefficient_gap_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 640 | `area_law_coefficient_gap_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 640 | `area_law_coefficient_gap_note` | critical | unaudited |
| 11 | `cycle-0011` | 5 | 640 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 12 | `cycle-0012` | 6 | 640 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 13 | `cycle-0013` | 7 | 640 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 14 | `cycle-0014` | 13 | 640 | `anomaly_forces_time_theorem` | critical | unaudited |
| 15 | `cycle-0015` | 14 | 640 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 607 | `su3_casimir_fundamental_algebraic_k1_k3_narrow_proof_walk_bounded_note_2026-05-10` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 604 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 604 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 604 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 604 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 21 | `cycle-0021` | 6 | 604 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 22 | `cycle-0022` | 7 | 604 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 23 | `cycle-0023` | 8 | 604 | `alpha_s_derived_note` | critical | unaudited |
| 24 | `cycle-0024` | 8 | 604 | `alpha_s_derived_note` | critical | unaudited |
| 25 | `cycle-0025` | 8 | 604 | `alpha_s_derived_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
