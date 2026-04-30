# Audit Queue

**Generated:** 2026-04-30T11:41:13.605349+00:00
**Total pending:** 1180
**Ready (all deps already at a stable tier):** 746

By criticality:
- `critical`: 33
- `high`: 234
- `medium`: 342
- `leaf`: 571

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---:|---:|:---:|---|---|
| 1 | `site_phase_cube_shift_intertwiner_note` | critical | 281 | 15.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_site_phase_cube_shift_intertwiner.py` |
| 2 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | critical | 276 | 11.61 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 3 | `g_bare_two_ward_closure_note_2026-04-18` | critical | 275 | 11.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_two_ward_closure.py` |
| 4 | `physical_lattice_necessity_note` | critical | 274 | 15.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_lattice_necessity.py` |
| 5 | `left_handed_charge_matching_note` | critical | 248 | 17.46 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 6 | `three_generation_structure_note` | critical | 247 | 20.95 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `anomaly_forces_time_theorem` | critical | 244 | 17.44 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `one_generation_matter_closure_note` | critical | 241 | 20.42 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16` | critical | 125 | 15.48 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py` |
| 10 | `dm_neutrino_source_surface_active_affine_point_selection_boundary_note_2026-04-16` | critical | 124 | 14.97 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py` |
| 11 | `dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem_note_2026-04-16` | critical | 120 | 14.92 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem.py` |
| 12 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | critical | 116 | 15.87 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 13 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | critical | 113 | 28.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_wolfenstein_lambda_a_structural_identities.py` |
| 14 | `rconn_derived_note` | critical | 113 | 14.33 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 15 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | 112 | 28.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_cp_phase_structural_identity.py` |
| 16 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | critical | 111 | 20.81 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 17 | `higgs_mass_derived_note` | critical | 106 | 14.24 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `higgs_vacuum_explicit_systematic_note` | critical | 105 | 14.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 19 | `minimal_axioms_2026-04-11` | critical | 103 | 17.70 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 20 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | critical | 99 | 23.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 21 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | critical | 91 | 19.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 22 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | critical | 82 | 14.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 23 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | critical | 81 | 14.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 24 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | critical | 80 | 14.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 25 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | critical | 80 | 14.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 26 | `ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` | critical | 79 | 14.32 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 27 | `ckm_atlas_axiom_closure_note` | critical | 72 | 17.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 28 | `down_type_mass_ratio_ckm_dual_note` | critical | 57 | 13.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 29 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | critical | 48 | 14.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 30 | `cosmological_constant_spectral_gap_identity_theorem_note` | critical | 46 | 14.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmological_constant_spectral_gap_identity.py` |
| 31 | `n_eff_from_three_generations_theorem_note_2026-04-24` | critical | 38 | 13.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_n_eff_from_three_generations.py` |
| 32 | `matter_radiation_equality_structural_identity_theorem_note_2026-04-24` | critical | 38 | 12.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_matter_radiation_equality_structural_identity.py` |
| 33 | `publication.ci3_z3.publication_matrix` | critical | 31 | 12.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25` | high | 41 | 11.89 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_background_zero_z_erasure_criterion.py` |
| 35 | `koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25` | high | 41 | 10.89 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py` |
| 36 | `area_law_algebraic_spectrum_entropy_no_go_note_2026-04-25` | high | 39 | 9.82 | Y | fresh_context_or_stronger | `scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py` |
| 37 | `koide_q_delta_closure_package_readme_2026-04-21` | high | 38 | 11.29 | Y | fresh_context_or_stronger | - |
| 38 | `pmns_selector_current_stack_zero_law_note` | high | 37 | 8.75 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_selector_current_stack_zero_law.py` |
| 39 | `cl3_color_automorphism_theorem` | high | 36 | 10.21 | Y | fresh_context_or_stronger | `scripts/verify_cl3_sm_embedding.py` |
| 40 | `koide_q_source_domain_canonical_descent_theorem_note_2026-04-25` | high | 36 | 10.21 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_source_domain_canonical_descent.py` |
| 41 | `cpt_exact_note` | high | 36 | 9.21 | Y | fresh_context_or_stronger | - |
| 42 | `neutrino_two_amplitude_last_mile_reduction_note` | high | 36 | 9.21 | Y | fresh_context_or_stronger | `scripts/frontier_neutrino_two_amplitude_last_mile.py` |
| 43 | `pmns_right_conjugacy_invariant_no_go_note` | high | 36 | 8.71 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_right_conjugacy_invariant_nogo.py` |
| 44 | `pmns_sigma_zero_nogo_note` | high | 36 | 8.71 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_sigma_zero_no_go.py` |
| 45 | `ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26` | high | 35 | 10.67 | Y | fresh_context_or_stronger | `scripts/frontier_ew_higgs_gauge_mass_diagonalization.py` |
| 46 | `signed_gravity_response_lane_status_note_2026-04-26` | high | 35 | 9.17 | Y | fresh_context_or_stronger | `scripts/frontier_signed_gravity_response_lane_status.py` |
| 47 | `single_axiom_hilbert_note` | high | 34 | 9.63 | Y | fresh_context_or_stronger | `scripts/frontier_single_axiom_hilbert.py` |
| 48 | `universal_qg_canonical_refinement_net_note` | high | 34 | 9.13 | Y | fresh_context_or_stronger | - |
| 49 | `universal_qg_uv_finite_partition_note` | high | 34 | 8.63 | Y | fresh_context_or_stronger | - |
| 50 | `bell_inequality_derived_note` | high | 34 | 8.13 | Y | fresh_context_or_stronger | `scripts/frontier_bell_inequality.py` |

Full queue lives in `data/audit_queue.json`.
