# Audit Queue

**Generated:** 2026-04-30T11:42:05.283156+00:00
**Total pending:** 1165
**Ready (all deps already at a stable tier):** 746

By criticality:
- `critical`: 18
- `high`: 234
- `medium`: 342
- `leaf`: 571

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---:|---:|:---:|---|---|
| 1 | `site_phase_cube_shift_intertwiner_note` | critical | 281 | 15.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_site_phase_cube_shift_intertwiner.py` |
| 2 | `higgs_mass_derived_note` | critical | 106 | 14.24 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 3 | `higgs_vacuum_explicit_systematic_note` | critical | 105 | 14.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 4 | `minimal_axioms_2026-04-11` | critical | 103 | 17.70 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 5 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | critical | 99 | 23.64 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 6 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | critical | 91 | 19.52 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 7 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | critical | 82 | 14.88 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_third_row_magnitudes.py` |
| 8 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | critical | 81 | 14.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 9 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | critical | 80 | 14.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 10 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | critical | 80 | 14.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 11 | `ckm_n9_structural_family_koide_bridge_support_note_2026-04-25` | critical | 79 | 14.32 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `ckm_atlas_axiom_closure_note` | critical | 72 | 17.19 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 13 | `down_type_mass_ratio_ckm_dual_note` | critical | 57 | 13.36 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_mass_ratio_ckm_dual.py` |
| 14 | `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | critical | 48 | 14.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py` |
| 15 | `cosmological_constant_spectral_gap_identity_theorem_note` | critical | 46 | 14.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmological_constant_spectral_gap_identity.py` |
| 16 | `n_eff_from_three_generations_theorem_note_2026-04-24` | critical | 38 | 13.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_n_eff_from_three_generations.py` |
| 17 | `matter_radiation_equality_structural_identity_theorem_note_2026-04-24` | critical | 38 | 12.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_matter_radiation_equality_structural_identity.py` |
| 18 | `publication.ci3_z3.publication_matrix` | critical | 31 | 12.50 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 19 | `koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25` | high | 41 | 11.89 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_background_zero_z_erasure_criterion.py` |
| 20 | `koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25` | high | 41 | 10.89 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py` |
| 21 | `area_law_algebraic_spectrum_entropy_no_go_note_2026-04-25` | high | 39 | 9.82 | Y | fresh_context_or_stronger | `scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py` |
| 22 | `koide_q_delta_closure_package_readme_2026-04-21` | high | 38 | 11.29 | Y | fresh_context_or_stronger | - |
| 23 | `pmns_selector_current_stack_zero_law_note` | high | 37 | 8.75 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_selector_current_stack_zero_law.py` |
| 24 | `cl3_color_automorphism_theorem` | high | 36 | 10.21 | Y | fresh_context_or_stronger | `scripts/verify_cl3_sm_embedding.py` |
| 25 | `koide_q_source_domain_canonical_descent_theorem_note_2026-04-25` | high | 36 | 10.21 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_source_domain_canonical_descent.py` |
| 26 | `cpt_exact_note` | high | 36 | 9.21 | Y | fresh_context_or_stronger | - |
| 27 | `neutrino_two_amplitude_last_mile_reduction_note` | high | 36 | 9.21 | Y | fresh_context_or_stronger | `scripts/frontier_neutrino_two_amplitude_last_mile.py` |
| 28 | `pmns_right_conjugacy_invariant_no_go_note` | high | 36 | 8.71 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_right_conjugacy_invariant_nogo.py` |
| 29 | `pmns_sigma_zero_nogo_note` | high | 36 | 8.71 | Y | fresh_context_or_stronger | `scripts/frontier_pmns_sigma_zero_no_go.py` |
| 30 | `ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26` | high | 35 | 10.67 | Y | fresh_context_or_stronger | `scripts/frontier_ew_higgs_gauge_mass_diagonalization.py` |
| 31 | `signed_gravity_response_lane_status_note_2026-04-26` | high | 35 | 9.17 | Y | fresh_context_or_stronger | `scripts/frontier_signed_gravity_response_lane_status.py` |
| 32 | `single_axiom_hilbert_note` | high | 34 | 9.63 | Y | fresh_context_or_stronger | `scripts/frontier_single_axiom_hilbert.py` |
| 33 | `universal_qg_canonical_refinement_net_note` | high | 34 | 9.13 | Y | fresh_context_or_stronger | - |
| 34 | `universal_qg_uv_finite_partition_note` | high | 34 | 8.63 | Y | fresh_context_or_stronger | - |
| 35 | `bell_inequality_derived_note` | high | 34 | 8.13 | Y | fresh_context_or_stronger | `scripts/frontier_bell_inequality.py` |
| 36 | `broad_gravity_derivation_note` | high | 34 | 8.13 | Y | fresh_context_or_stronger | - |
| 37 | `ckm_moduli_only_unitarity_jarlskog_area_certificate_theorem_note_2026-04-26` | high | 33 | 10.09 | Y | fresh_context_or_stronger | `scripts/frontier_ckm_moduli_only_unitarity_jarlskog_area_certificate.py` |
| 38 | `koide_q_so2_phase_erasure_support_note_2026-04-25` | high | 33 | 9.59 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_so2_phase_erasure_support.py` |
| 39 | `sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26` | high | 33 | 9.59 | Y | fresh_context_or_stronger | `scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py` |
| 40 | `newton_law_derived_note` | high | 33 | 9.09 | Y | fresh_context_or_stronger | - |
| 41 | `poisson_exhaustive_uniqueness_note` | high | 33 | 9.09 | Y | fresh_context_or_stronger | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 42 | `self_consistency_forces_poisson_note` | high | 33 | 9.09 | Y | fresh_context_or_stronger | `scripts/frontier_self_consistent_field_equation.py` |
| 43 | `single_axiom_information_note` | high | 33 | 9.09 | Y | fresh_context_or_stronger | `scripts/frontier_single_axiom_information.py` |
| 44 | `dm_pmns_ordered_chain_graded_current_delta_closure_theorem_note_2026-04-21` | high | 33 | 8.59 | Y | fresh_context_or_stronger | `scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py` |
| 45 | `universal_gr_lorentzian_global_atlas_closure_note` | high | 33 | 8.59 | Y | fresh_context_or_stronger | - |
| 46 | `universal_gr_lorentzian_signature_extension_note` | high | 33 | 8.59 | Y | fresh_context_or_stronger | - |
| 47 | `dm_split2_interval_certified_dominance_closure_theorem_note_2026-04-21` | high | 33 | 8.09 | Y | fresh_context_or_stronger | `scripts/frontier_dm_split2_interval_certified_dominance_closure_2026_04_21.py` |
| 48 | `grav_decoherence_derived_note` | high | 33 | 7.59 | Y | fresh_context_or_stronger | `scripts/frontier_grav_decoherence_derived.py` |
| 49 | `monopole_derived_note` | high | 33 | 7.59 | Y | fresh_context_or_stronger | `scripts/frontier_monopole_derived.py` |
| 50 | `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25` | high | 32 | 9.54 | Y | fresh_context_or_stronger | `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py` |

Full queue lives in `data/audit_queue.json`.
