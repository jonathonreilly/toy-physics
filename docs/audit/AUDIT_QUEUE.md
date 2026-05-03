# Audit Queue

**Generated:** 2026-05-03T19:39:28.122146+00:00
**Total pending:** 808
**Ready (all deps already at retained-grade or metadata tiers):** 121

By criticality:
- `critical`: 148
- `high`: 220
- `medium`: 239
- `leaf`: 201

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `ew_current_matching_rule_open_gate_note_2026-05-03` | no_go | unaudited | critical | 140 | 19.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_current_matching_rule_no_go.py` |
| 2 | `dm_leptogenesis_transport_status_note_2026-04-16` | - | unaudited | critical | 131 | 17.54 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_transport_status.py` |
| 3 | `strong_cp_theta_zero_note` | - | unaudited | critical | 119 | 16.91 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_strong_cp_theta_zero.py` |
| 4 | `cl3_taste_generation_theorem` | - | unaudited | critical | 103 | 14.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 5 | `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24` | - | unaudited | critical | 86 | 14.94 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_a1_radian_bridge_irreducibility_audit.py` |
| 6 | `koide_dimensionless_objection_closure_review_packet_2026-04-24` | - | unaudited | critical | 86 | 14.94 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_dimensionless_objection_closure_review.py` |
| 7 | `koide_a1_fractional_topology_no_go_synthesis_note_2026-04-24` | - | unaudited | critical | 86 | 14.44 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `koide_pointed_origin_exhaustion_theorem_note_2026-04-24` | - | unaudited | critical | 86 | 14.44 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_pointed_origin_exhaustion_theorem.py` |
| 9 | `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | - | unaudited | critical | 80 | 16.34 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `cl3_sm_embedding_theorem` | - | unaudited | critical | 70 | 14.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 11 | `s3_cap_uniqueness_note` | - | unaudited | critical | 69 | 15.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 12 | `cosmology_scale_identification_and_reduction_note` | - | unaudited | critical | 68 | 14.61 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `universal_theta_induced_edm_vanishing_theorem_note_2026-04-24` | - | unaudited | critical | 68 | 14.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_theta_induced_edm_vanishing.py` |
| 14 | `quark_cp_carrier_completion_note_2026-04-18` | - | unaudited | critical | 64 | 13.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_cp_carrier_completion.py` |
| 15 | `rconn_derived_note` | - | unaudited | critical | 63 | 13.50 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_color_projection_mc.py` |
| 16 | `koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25` | - | unaudited | critical | 62 | 15.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_background_zero_z_erasure_criterion.py` |
| 17 | `universal_gr_lorentzian_global_atlas_closure_note` | - | unaudited | critical | 62 | 15.48 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 62 | 14.98 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 19 | `koide_q_onsite_source_domain_no_go_synthesis_note_2026-04-25` | - | unaudited | critical | 62 | 14.48 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py` |
| 20 | `koide_q_delta_closure_package_readme_2026-04-21` | - | unaudited | critical | 58 | 14.38 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_Q_eq_3delta_identity.py` |
| 21 | `ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26` | - | unaudited | critical | 56 | 15.33 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_higgs_gauge_mass_diagonalization.py` |
| 22 | `sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26` | - | unaudited | critical | 54 | 14.78 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py` |
| 23 | `dm_pmns_ordered_chain_graded_current_delta_closure_theorem_note_2026-04-21` | - | unaudited | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py` |
| 24 | `cosmology_single_ratio_inverse_reconstruction_theorem_note_2026-04-25` | - | unaudited | critical | 53 | 15.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_cosmology_single_ratio_inverse_reconstruction.py` |
| 25 | `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25` | - | unaudited | critical | 51 | 13.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py` |
| 26 | `lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 319 | 9.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_doublet_traceless_abelian_ratio.py` |
| 27 | `left_handed_charge_matching_note` | positive_theorem | unaudited | critical | 318 | 25.32 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graph_first_su3_integration.py` |
| 28 | `cpt_exact_note` | positive_theorem | unaudited | critical | 301 | 20.24 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 301 | 11.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 30 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 296 | 17.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 31 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 296 | 16.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 32 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 296 | 14.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 33 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 296 | 13.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 34 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 295 | 24.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 35 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 295 | 17.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 36 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 295 | 17.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 37 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 295 | 16.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 38 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 295 | 16.71 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 39 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 295 | 16.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 40 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 295 | 15.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 41 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 295 | 14.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 42 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 295 | 14.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 43 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 295 | 14.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 44 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 295 | 13.21 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 295 | 12.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 46 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 295 | 9.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 47 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 295 | 8.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 48 | `g_bare_rescaling_freedom_removal_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 293 | 9.20 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 49 | `g_bare_constraint_vs_convention_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 292 | 8.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |
| 50 | `g_bare_derivation_note` | positive_theorem | unaudited | critical | 291 | 14.69 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_derivation.py` |

Full queue lives in `data/audit_queue.json`.
