# Audit Queue

**Total pending:** 1095
**Ready (all deps already at retained-grade or metadata tiers):** 114

By criticality:
- `critical`: 663
- `high`: 22
- `medium`: 146
- `leaf`: 264

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `shapiro_static_discriminator_note` | positive_theorem | unaudited | critical | 306 | 10.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_static_discriminator.py` |
| 2 | `complex_action_note` | bounded_theorem | unaudited | critical | 304 | 11.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_harness.py` |
| 3 | `gravitomagnetic_note` | positive_theorem | unaudited | critical | 304 | 9.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravitomagnetic_portable.py` |
| 4 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 303 | 11.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 5 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | decoration | unaudited | critical | 294 | 16.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_alpha_lm_geometric_mean_identity.py` |
| 6 | `dm_neutrino_bosonic_normalization_theorem_note_2026-04-15` | bounded_theorem | unaudited | critical | 288 | 8.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_bosonic_normalization_theorem.py` |
| 7 | `poisson_self_gravity_loop_note` | bounded_theorem | unaudited | critical | 285 | 10.66 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop.py` |
| 8 | `axiom_first_cpt_theorem_stretch_note_2026-04-29` | bounded_theorem | unaudited | critical | 284 | 8.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cpt_check.py` |
| 9 | `koide_cl3_selector_gap_note_2026-04-19` | bounded_theorem | unaudited | critical | 283 | 10.15 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `poisson_self_gravity_born_audit_note` | bounded_theorem | unaudited | critical | 283 | 10.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_born_audit.py` |
| 11 | `lensing_deflection_note` | bounded_theorem | unaudited | critical | 283 | 9.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_deflection_h025_slope_fit_certificate.py` |
| 12 | `poisson_self_gravity_loop_v3_note` | bounded_theorem | unaudited | critical | 283 | 9.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/poisson_self_gravity_loop_v3.py` |
| 13 | `koide_gamma_orbit_selector_bridge_note_2026-04-18` | positive_theorem | unaudited | critical | 282 | 11.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_gamma_orbit_selector_bridge.py` |
| 14 | `pmns_commutant_eigenoperator_selector_note` | bounded_theorem | unaudited | critical | 280 | 10.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_commutant_eigenoperator_selector.py` |
| 15 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | critical | 280 | 9.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 16 | `dm_abcc_pmns_nonsingularity_theorem_note_2026-04-19` | bounded_theorem | unaudited | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_abcc_pmns_nonsingularity_theorem.py` |
| 17 | `gravity_law_cleanup_note` | bounded_theorem | unaudited | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravity_distance_fixed_geometry.py` |
| 18 | `persistent_object_blended_readout_transfer_sweep_note_2026-04-16` | bounded_theorem | unaudited | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/persistent_object_blended_readout_boundary_probe.py` |
| 19 | `pmns_three_flux_holonomy_closure_note` | bounded_theorem | unaudited | critical | 280 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_three_flux_holonomy_closure.py` |
| 20 | `cl3_baryon_qqq_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_baryon_qqq_color_singlet_check.py` |
| 21 | `cl3_quark_antiquark_color_singlet_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/cl3_quark_antiquark_color_singlet_check.py` |
| 22 | `dm_pmns_asymptotic_source_no_go_note_2026-04-20` | no_go | unaudited | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py` |
| 23 | `staggered_3d_self_gravity_sign_note_2026-04-11` | bounded_theorem | unaudited | critical | 280 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_3d_self_gravity_sign.py` |
| 24 | `charged_lepton_direct_ward_free_yukawa_no_go_note_2026-04-26` | no_go | unaudited | critical | 279 | 12.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py` |
| 25 | `koide_circulant_character_bridge_narrow_theorem_note_2026-05-09` | positive_theorem | unaudited | critical | 279 | 10.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_circulant_character_bridge_narrow.py` |
| 26 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 279 | 10.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 27 | `koide_delta_lattice_wilson_selected_eigenline_no_go_note_2026-04-24` | no_go | unaudited | critical | 279 | 9.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py` |
| 28 | `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_3plus1_line_exact_solve_doublet_theorem_note_2026-04-20` | bounded_theorem | unaudited | critical | 279 | 9.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gauge_vacuum_plaquette_doublet_dense_root_count_certificate_2026_05_03.py` |
| 29 | `circulant_parity_cp_tensor_narrow_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_circulant_parity_cp_tensor_narrow.py` |
| 30 | `koide_a1_loop_final_status_2026-04-22` | bounded_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_quartic_potential_derivation.py` |
| 31 | `wave_static_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_boundary_sensitivity.py` |
| 32 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 33 | `wave_static_fixed_beam_boundary_sensitivity_note` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_fixed_beam_boundary_sensitivity.py` |
| 34 | `wave_static_matrixfree_fixed_beam_boundary_note` | positive_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_matrixfree_fixed_beam_boundary.py` |
| 35 | `wave_static_single_source_compare_note` | bounded_theorem | unaudited | critical | 279 | 8.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_single_source_compare.py` |
| 36 | `neutrino_mass_reduction_to_dirac_note` | positive_theorem | unaudited | critical | 278 | 14.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_mass_reduction_to_dirac.py` |
| 37 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | bounded_theorem | unaudited | critical | 664 | 16.38 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 38 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 637 | 21.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 39 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 637 | 10.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 40 | `left_handed_charge_matching_note` | bounded_theorem | unaudited | critical | 636 | 27.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 41 | `cpt_exact_note` | positive_theorem | unaudited | critical | 635 | 20.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cpt_exact.py` |
| 42 | `dispersion_relation_note` | positive_theorem | unaudited | critical | 632 | 10.31 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/lattice_dispersion_relation.py` |
| 43 | `lensing_combined_invariant_note` | positive_theorem | unaudited | critical | 632 | 10.31 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `3d_correction_master_note` | positive_theorem | unaudited | critical | 632 | 9.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/dispersion_3d_lattice.py` |
| 45 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 630 | 14.30 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 46 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 630 | 10.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 47 | `parity_operator_basis_dimension5_lv_no_go_theorem_note_2026-05-02` | no_go | unaudited | critical | 630 | 9.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_parity_operator_basis_dimension5_lv_no_go.py` |
| 48 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 629 | 18.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 49 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 629 | 15.80 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 629 | 13.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |

## Citation cycle break targets

232 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 637 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 632 | `3d_correction_master_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 629 | `bh_entropy_derived_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 626 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 626 | `bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 626 | `area_law_coefficient_gap_note` | critical | audited_conditional |
| 7 | `cycle-0007` | 5 | 626 | `universal_gr_constraint_action_stationarity_note` | critical | unaudited |
| 8 | `cycle-0008` | 11 | 626 | `anomaly_forces_time_theorem` | critical | unaudited |
| 9 | `cycle-0009` | 12 | 626 | `anomaly_forces_time_theorem` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 564 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 564 | `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` | critical | unaudited |
| 12 | `cycle-0012` | 3 | 564 | `g_bare_canonical_convention_narrow_theorem_note_2026-05-02` | critical | unaudited |
| 13 | `cycle-0013` | 6 | 564 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 14 | `cycle-0014` | 7 | 564 | `g_bare_constraint_vs_convention_restatement_note_2026-05-07` | critical | unaudited |
| 15 | `cycle-0015` | 8 | 564 | `alpha_s_derived_note` | critical | audited_conditional |
| 16 | `cycle-0016` | 8 | 564 | `alpha_s_derived_note` | critical | audited_conditional |
| 17 | `cycle-0017` | 8 | 564 | `alpha_s_derived_note` | critical | audited_conditional |
| 18 | `cycle-0018` | 8 | 564 | `alpha_s_derived_note` | critical | audited_conditional |
| 19 | `cycle-0019` | 2 | 376 | `hypercharge_identification_note` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 318 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | unaudited |
| 21 | `cycle-0021` | 5 | 318 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 22 | `cycle-0022` | 5 | 318 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 23 | `cycle-0023` | 5 | 318 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 24 | `cycle-0024` | 5 | 318 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |
| 25 | `cycle-0025` | 5 | 318 | `dm_neutrino_hermitian_bridge_carrier_note_2026-04-15` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
