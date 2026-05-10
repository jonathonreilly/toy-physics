# Audit Queue

**Total pending:** 1102
**Ready (all deps already at retained-grade or metadata tiers):** 121

By criticality:
- `critical`: 670
- `high`: 22
- `medium`: 146
- `leaf`: 264

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 627 | 16.30 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cluster_decomposition_check.py` |
| 2 | `boundary_law_robustness_note_2026-04-11` | bounded_theorem | unaudited | critical | 626 | 10.29 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_boundary_law_robustness.py` |
| 3 | `discrete_einstein_regge_lift_note` | bounded_theorem | unaudited | critical | 626 | 9.79 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_isotropic_glue_operator.py` |
| 4 | `gauge_vacuum_plaquette_rho_pq6_wilson_environment_bounded_note_2026-05-09` | bounded_theorem | unaudited | critical | 573 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py` |
| 5 | `dm_neutrino_weak_triplet_transfer_class_theorem_note_2026-04-15` | positive_theorem | unaudited | critical | 319 | 8.82 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_weak_triplet_transfer_class_theorem.py` |
| 6 | `dm_neutrino_source_surface_bundle_window_trichotomy_candidate_note_2026-04-18` | bounded_theorem | unaudited | critical | 317 | 9.31 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_bundle_window_trichotomy_candidate.py` |
| 7 | `dm_neutrino_source_surface_endpoint_window_bundle_dominance_candidate_note_2026-04-17` | bounded_theorem | unaudited | critical | 317 | 8.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_endpoint_window_bundle_dominance_candidate.py` |
| 8 | `dm_neutrino_source_surface_split1_window_bundle_dominance_candidate_note_2026-04-17` | bounded_theorem | unaudited | critical | 317 | 8.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_split1_window_bundle_dominance_candidate.py` |
| 9 | `dm_neutrino_source_surface_split2_upper_m_slack_floor_endpoint_candidate_note_2026-04-18` | bounded_theorem | unaudited | critical | 317 | 8.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_split2_upper_m_slack_floor_endpoint_candidate.py` |
| 10 | `shapiro_static_discriminator_note` | positive_theorem | unaudited | critical | 304 | 10.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_static_discriminator.py` |
| 11 | `complex_action_note` | bounded_theorem | unaudited | critical | 302 | 11.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_harness.py` |
| 12 | `gravitomagnetic_note` | positive_theorem | unaudited | critical | 302 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravitomagnetic_portable.py` |
| 13 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 301 | 11.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 14 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 292 | 16.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 15 | `dm_neutrino_bosonic_normalization_theorem_note_2026-04-15` | bounded_theorem | unaudited | critical | 286 | 8.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_bosonic_normalization_theorem.py` |
| 16 | `poisson_self_gravity_loop_note` | bounded_theorem | unaudited | critical | 283 | 10.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 17 | `axiom_first_cpt_theorem_stretch_note_2026-04-29` | bounded_theorem | unaudited | critical | 282 | 8.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cpt_check.py` |
| 18 | `poisson_self_gravity_born_audit_note` | bounded_theorem | unaudited | critical | 281 | 10.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_born_audit.py` |
| 19 | `lensing_deflection_note` | bounded_theorem | unaudited | critical | 281 | 9.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_deflection_h025_slope_fit_certificate.py` |
| 20 | `poisson_self_gravity_loop_v3_note` | bounded_theorem | unaudited | critical | 281 | 9.64 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop_v3.py` |
| 21 | `koide_gamma_orbit_selector_bridge_note_2026-04-18` | positive_theorem | unaudited | critical | 280 | 11.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_orbit_selector_bridge.py` |
| 22 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | critical | 278 | 9.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 23 | `gravity_law_cleanup_note` | bounded_theorem | unaudited | critical | 278 | 9.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravity_distance_fixed_geometry.py` |
| 24 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 278 | 9.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 25 | `pmns_three_flux_holonomy_closure_note` | bounded_theorem | unaudited | critical | 278 | 9.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_three_flux_holonomy_closure.py` |
| 26 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 278 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 27 | `cl3_quark_antiquark_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 278 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_quark_antiquark_color_singlet_check.py` |
| 28 | `dm_pmns_asymptotic_source_no_go_note_2026-04-20` | no_go | unaudited | critical | 278 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py` |
| 29 | `staggered_3d_self_gravity_sign_note_2026-04-11` | bounded_theorem | unaudited | critical | 278 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_3d_self_gravity_sign.py` |
| 30 | `charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26` | no_go | unaudited | critical | 277 | 12.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py` |
| 31 | `koide_circulant_character_bridge_narrow_theorem_note_2026-05-09` | positive_theorem | unaudited | critical | 277 | 10.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_character_bridge_narrow.py` |
| 32 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 277 | 10.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 33 | `koide_cl3_selector_gap_note_2026-04-19` | bounded_theorem | unaudited | critical | 277 | 9.62 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `koide_delta_lattice_wilson_selected_eigenline_no_go_note_2026-04-24` | no_go | unaudited | critical | 277 | 9.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py` |
| 35 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | bounded_theorem | unaudited | critical | 277 | 9.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py` |
| 36 | `circulant_parity_cp_tensor_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 277 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_parity_cp_tensor_narrow.py` |
| 37 | `koide_a1_loop_final_status_2026-04-22` | bounded_theorem | unaudited | critical | 277 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_quartic_potential_derivation.py` |
| 38 | `wave_static_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 277 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 39 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 277 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 40 | `wave_static_fixed_beam_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 277 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_fixed_beam_boundary_sensitivity.py` |
| 41 | `wave_static_matrixfree_fixed_beam_boundary_note` | positive_theorem | unaudited | critical | 277 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 42 | `wave_static_single_source_compare_note` | bounded_theorem | unaudited | critical | 277 | 8.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_single_source_compare.py` |
| 43 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 276 | 14.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 44 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 662 | 16.37 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 45 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 635 | 21.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 46 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 635 | 10.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 47 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 634 | 27.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 48 | `cpt_exact_note` | positive_theorem | unaudited | critical | 633 | 20.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 49 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 630 | 10.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 50 | `lensing_combined_invariant_note` | positive_theorem | unaudited | critical | 630 | 10.30 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

232 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 635 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 630 | `3d_correction_master_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 627 | `bh_entropy_derived_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 624 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 624 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 624 | `area_law_coefficient_gap_note` | critical | audited_conditional |
| 7 | `cycle-0007` | 5 | 624 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 8 | `cycle-0008` | 11 | 624 | `anomaly_forces_time_theorem` | critical | unaudited |
| 9 | `cycle-0009` | 12 | 624 | `anomaly_forces_time_theorem` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 562 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 562 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 562 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 13 | `cycle-0013` | 6 | 562 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 14 | `cycle-0014` | 7 | 562 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 15 | `cycle-0015` | 8 | 562 | `alpha_s_derived_note` | critical | audited_conditional |
| 16 | `cycle-0016` | 8 | 562 | `alpha_s_derived_note` | critical | audited_conditional |
| 17 | `cycle-0017` | 8 | 562 | `alpha_s_derived_note` | critical | audited_conditional |
| 18 | `cycle-0018` | 8 | 562 | `alpha_s_derived_note` | critical | audited_conditional |
| 19 | `cycle-0019` | 2 | 374 | `hypercharge_identification_note` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 316 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 21 | `cycle-0021` | 5 | 316 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 22 | `cycle-0022` | 5 | 316 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 23 | `cycle-0023` | 5 | 316 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 24 | `cycle-0024` | 5 | 316 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 25 | `cycle-0025` | 5 | 316 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
