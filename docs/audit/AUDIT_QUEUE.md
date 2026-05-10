# Audit Queue

**Total pending:** 1117
**Ready (all deps already at retained-grade or metadata tiers):** 120

By criticality:
- `critical`: 681
- `high`: 22
- `medium`: 149
- `leaf`: 265

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `poisson_self_gravity_loop_note` | bounded_theorem | unaudited | critical | 641 | 12.33 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 2 | `universal_gr_isotropic_glue_operator_note` | bounded_theorem | unaudited | critical | 639 | 11.82 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 3 | `gate_b_poisson_self_gravity_note` | no_go | unaudited | critical | 639 | 11.32 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_poisson_self_gravity_probe.py` |
| 4 | `gravity_full_self_consistency_note` | bounded_theorem | unaudited | critical | 637 | 11.82 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 5 | `universal_gr_lorentzian_global_atlas_closure_note` | bounded_theorem | unaudited | critical | 636 | 19.82 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 6 | `staggered_fermion_card_2026-04-11` | bounded_theorem | unaudited | critical | 636 | 11.31 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_17card.py` |
| 7 | `quark_route2_source_domain_bridge_no_go_note_2026-04-28` | no_go | unaudited | critical | 634 | 9.81 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_route2_source_domain_bridge_no_go.py` |
| 8 | `universal_gr_tensor_action_blocker_note` | bounded_theorem | unaudited | critical | 633 | 10.81 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `complex_action_note` | bounded_theorem | unaudited | critical | 304 | 11.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_harness.py` |
| 10 | `gravitomagnetic_note` | positive_theorem | unaudited | critical | 304 | 9.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravitomagnetic_portable.py` |
| 11 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 303 | 11.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 12 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 294 | 16.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 13 | `dm_neutrino_bosonic_normalization_theorem_note_2026-04-15` | bounded_theorem | unaudited | critical | 288 | 8.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_bosonic_normalization_theorem.py` |
| 14 | `axiom_first_cpt_theorem_stretch_note_2026-04-29` | bounded_theorem | unaudited | critical | 284 | 8.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cpt_check.py` |
| 15 | `koide_cl3_selector_gap_note_2026-04-19` | bounded_theorem | unaudited | critical | 283 | 10.15 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 16 | `poisson_self_gravity_born_audit_note` | bounded_theorem | unaudited | critical | 283 | 10.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_born_audit.py` |
| 17 | `lensing_deflection_note` | bounded_theorem | unaudited | critical | 283 | 9.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_deflection_h025_slope_fit_certificate.py` |
| 18 | `poisson_self_gravity_loop_v3_note` | bounded_theorem | unaudited | critical | 283 | 9.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop_v3.py` |
| 19 | `koide_gamma_orbit_selector_bridge_note_2026-04-18` | positive_theorem | unaudited | critical | 282 | 11.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_orbit_selector_bridge.py` |
| 20 | `pmns_commutant_eigenoperator_selector_note` | bounded_theorem | unaudited | critical | 280 | 10.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_commutant_eigenoperator_selector.py` |
| 21 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | critical | 280 | 9.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 22 | `dm_abcc_pmns_nonsingularity_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_pmns_nonsingularity_theorem.py` |
| 23 | `gravity_law_cleanup_note` | bounded_theorem | unaudited | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravity_distance_fixed_geometry.py` |
| 24 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 25 | `pmns_three_flux_holonomy_closure_note` | bounded_theorem | unaudited | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_three_flux_holonomy_closure.py` |
| 26 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 27 | `cl3_quark_antiquark_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_quark_antiquark_color_singlet_check.py` |
| 28 | `dm_pmns_asymptotic_source_no_go_note_2026-04-20` | no_go | unaudited | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py` |
| 29 | `staggered_3d_self_gravity_sign_note_2026-04-11` | bounded_theorem | unaudited | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_3d_self_gravity_sign.py` |
| 30 | `charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26` | no_go | unaudited | critical | 279 | 12.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py` |
| 31 | `koide_circulant_character_bridge_narrow_theorem_note_2026-05-09` | positive_theorem | unaudited | critical | 279 | 10.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_character_bridge_narrow.py` |
| 32 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 279 | 10.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 33 | `koide_delta_lattice_wilson_selected_eigenline_no_go_note_2026-04-24` | no_go | unaudited | critical | 279 | 9.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py` |
| 34 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | bounded_theorem | unaudited | critical | 279 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py` |
| 35 | `circulant_parity_cp_tensor_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_parity_cp_tensor_narrow.py` |
| 36 | `koide_a1_loop_final_status_2026-04-22` | bounded_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_quartic_potential_derivation.py` |
| 37 | `wave_static_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 38 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 39 | `wave_static_fixed_beam_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_fixed_beam_boundary_sensitivity.py` |
| 40 | `wave_static_matrixfree_fixed_beam_boundary_note` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 41 | `wave_static_single_source_compare_note` | bounded_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_single_source_compare.py` |
| 42 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 278 | 14.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 43 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 670 | 16.39 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 44 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 643 | 21.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 45 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 643 | 10.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 46 | `cpt_exact_note` | positive_theorem | unaudited | critical | 641 | 20.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 47 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 639 | 11.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 48 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 638 | 13.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 49 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 638 | 10.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 50 | `lensing_combined_invariant_note` | positive_theorem | unaudited | critical | 638 | 10.32 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

237 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 643 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 638 | `3d_correction_master_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 634 | `bh_entropy_derived_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 632 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 632 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 632 | `discrete_einstein_regge_lift_note` | critical | unaudited |
| 7 | `cycle-0007` | 3 | 632 | `area_law_coefficient_gap_note` | critical | unaudited |
| 8 | `cycle-0008` | 4 | 632 | `area_law_coefficient_gap_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 632 | `area_law_coefficient_gap_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 632 | `area_law_coefficient_gap_note` | critical | unaudited |
| 11 | `cycle-0011` | 5 | 632 | `area_law_coefficient_gap_note` | critical | unaudited |
| 12 | `cycle-0012` | 5 | 632 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 13 | `cycle-0013` | 11 | 632 | `anomaly_forces_time_theorem` | critical | unaudited |
| 14 | `cycle-0014` | 12 | 632 | `anomaly_forces_time_theorem` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 565 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 565 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 17 | `cycle-0017` | 3 | 565 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 18 | `cycle-0018` | 6 | 565 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 19 | `cycle-0019` | 7 | 565 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 20 | `cycle-0020` | 8 | 565 | `alpha_s_derived_note` | critical | audited_conditional |
| 21 | `cycle-0021` | 8 | 565 | `alpha_s_derived_note` | critical | audited_conditional |
| 22 | `cycle-0022` | 8 | 565 | `alpha_s_derived_note` | critical | audited_conditional |
| 23 | `cycle-0023` | 8 | 565 | `alpha_s_derived_note` | critical | audited_conditional |
| 24 | `cycle-0024` | 2 | 376 | `hypercharge_identification_note` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 318 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
