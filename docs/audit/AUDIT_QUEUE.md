# Audit Queue

**Total pending:** 1148
**Ready (all deps already at retained-grade or metadata tiers):** 113

By criticality:
- `critical`: 707
- `high`: 25
- `medium`: 148
- `leaf`: 268

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 624 | 10.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 2 | `rconn_derived_note` | bounded_theorem | unaudited | critical | 468 | 15.87 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 3 | `gate_b_farfield_note` | bounded_theorem | unaudited | critical | 406 | 16.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_farfield_harness.py` |
| 4 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 376 | 17.06 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 5 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 365 | 11.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 6 | `poisson_self_gravity_born_audit_note` | bounded_theorem | unaudited | critical | 345 | 10.44 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_born_audit.py` |
| 7 | `lensing_deflection_note` | bounded_theorem | unaudited | critical | 345 | 9.94 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_deflection_h025_slope_fit_certificate.py` |
| 8 | `poisson_self_gravity_loop_v3_note` | bounded_theorem | unaudited | critical | 345 | 9.94 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop_v3.py` |
| 9 | `koide_gamma_orbit_selector_bridge_note_2026-04-18` | positive_theorem | unaudited | critical | 344 | 11.43 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_orbit_selector_bridge.py` |
| 10 | `newton_law_derived_note` | positive_theorem | unaudited | critical | 342 | 13.42 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_distance_law_definitive.py` |
| 11 | `pmns_commutant_eigenoperator_selector_note` | bounded_theorem | unaudited | critical | 342 | 10.42 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_commutant_eigenoperator_selector.py` |
| 12 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | critical | 342 | 9.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 13 | `gravity_law_cleanup_note` | bounded_theorem | unaudited | critical | 342 | 9.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravity_distance_fixed_geometry.py` |
| 14 | `dm_abcc_pmns_nonsingularity_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 342 | 9.42 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_pmns_nonsingularity_theorem.py` |
| 15 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 342 | 9.42 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 16 | `pmns_three_flux_holonomy_closure_note` | bounded_theorem | unaudited | critical | 342 | 9.42 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_three_flux_holonomy_closure.py` |
| 17 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 342 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 18 | `cl3_quark_antiquark_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 342 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_quark_antiquark_color_singlet_check.py` |
| 19 | `staggered_3d_self_gravity_sign_note_2026-04-11` | bounded_theorem | unaudited | critical | 342 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_3d_self_gravity_sign.py` |
| 20 | `charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26` | no_go | unaudited | critical | 341 | 12.42 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py` |
| 21 | `koide_circulant_character_bridge_narrow_theorem_note_2026-05-09` | positive_theorem | unaudited | critical | 341 | 10.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_character_bridge_narrow.py` |
| 22 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 341 | 10.42 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 23 | `koide_delta_lattice_wilson_selected_eigenline_no_go_note_2026-04-24` | no_go | unaudited | critical | 341 | 9.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py` |
| 24 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | bounded_theorem | unaudited | critical | 341 | 9.42 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py` |
| 25 | `circulant_parity_cp_tensor_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_parity_cp_tensor_narrow.py` |
| 26 | `dm_neutrino_triplet_even_response_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_triplet_even_response_theorem.py` |
| 27 | `dm_pmns_asymptotic_source_no_go_note_2026-04-20` | no_go | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py` |
| 28 | `dm_strong_cp_gamma_transfer_no_go_note_2026-04-15` | positive_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_strong_cp_gamma_transfer_nogo.py` |
| 29 | `koide_a1_loop_final_status_2026-04-22` | bounded_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_quartic_potential_derivation.py` |
| 30 | `wave_static_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 31 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 32 | `wave_static_fixed_beam_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_fixed_beam_boundary_sensitivity.py` |
| 33 | `wave_static_matrixfree_fixed_beam_boundary_note` | positive_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 34 | `wave_static_single_source_compare_note` | bounded_theorem | unaudited | critical | 341 | 8.92 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_single_source_compare.py` |
| 35 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 340 | 14.91 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 36 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 688 | 16.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 37 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 688 | 11.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 38 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 686 | 27.42 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 39 | `s3_taste_cube_decomposition_note` | bounded_theorem | unaudited | critical | 676 | 15.90 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_action_taste_cube_decomposition.py` |
| 40 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 661 | 22.37 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 41 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 661 | 10.87 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 42 | `cpt_exact_note` | positive_theorem | unaudited | critical | 659 | 20.87 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 43 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 656 | 13.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 44 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 654 | 14.36 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 654 | 10.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 46 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 654 | 9.86 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 47 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 653 | 18.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 48 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 653 | 15.85 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 49 | `poisson_exhaustive_uniqueness_note` | bounded_theorem | unaudited | critical | 653 | 13.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 50 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 653 | 10.85 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |

## Citation cycle break targets

272 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 661 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 652 | `bh_entropy_derived_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 650 | `3d_correction_master_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 650 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 650 | `architecture_note_directional_measure` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 650 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 650 | `discrete_einstein_regge_lift_note` | critical | unaudited |
| 8 | `cycle-0008` | 3 | 650 | `area_law_coefficient_gap_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 650 | `area_law_coefficient_gap_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 650 | `area_law_coefficient_gap_note` | critical | unaudited |
| 11 | `cycle-0011` | 5 | 650 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 12 | `cycle-0012` | 6 | 650 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 13 | `cycle-0013` | 7 | 650 | `area_law_native_car_semantics_tightening_note_2026-04-25` | critical | unaudited |
| 14 | `cycle-0014` | 13 | 650 | `anomaly_forces_time_theorem` | critical | unaudited |
| 15 | `cycle-0015` | 14 | 650 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 617 | `su3_casimir_fundamental_algebraic_k1_k3_narrow_proof_walk_bounded_note_2026-05-10` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 614 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 614 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 614 | `gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10` | critical | unaudited |
| 20 | `cycle-0020` | 3 | 614 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 21 | `cycle-0021` | 6 | 614 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 22 | `cycle-0022` | 7 | 614 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 23 | `cycle-0023` | 8 | 614 | `alpha_s_derived_note` | critical | unaudited |
| 24 | `cycle-0024` | 8 | 614 | `alpha_s_derived_note` | critical | unaudited |
| 25 | `cycle-0025` | 8 | 614 | `alpha_s_derived_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
