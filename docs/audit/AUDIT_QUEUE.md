# Audit Queue

**Total pending:** 790
**Ready (all deps already at retained-grade or metadata tiers):** 4

By criticality:
- `critical`: 471
- `high`: 23
- `medium`: 116
- `leaf`: 180

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `su3_wigner_intertwiner_block1_theorem_note_2026-05-03` | positive_theorem | audit_in_progress | critical | 437 | 10.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_intertwiner_engine.py` |
| 2 | `g_bare_rigidity_theorem_note` | positive_theorem | claim_type_backfill_reaudit | critical | 292 | 11.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 3 | `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | no_go | audit_in_progress | critical | 285 | 9.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hadron_lane1_sqrt_sigma_b5_framework_link_audit.py` |
| 4 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 438 | 25.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 5 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | - | unaudited | critical | 438 | 16.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 6 | `planck_scale_lane_status_note_2026-04-23` | - | unaudited | critical | 438 | 15.78 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `lorentz_kernel_positive_closure_note` | - | unaudited | critical | 438 | 14.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 8 | `angular_kernel_underdetermination_no_go_note` | - | unaudited | critical | 438 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 9 | `area_law_multipocket_selector_no_go_note_2026-04-25` | - | unaudited | critical | 438 | 13.78 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 10 | `area_law_native_car_semantics_tightening_note_2026-04-25` | - | unaudited | critical | 438 | 13.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 11 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | - | unaudited | critical | 438 | 13.28 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 12 | `su3_wigner_intertwiner_block2_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 436 | 9.77 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_4fold_haar_projector.py` |
| 13 | `su3_wigner_intertwiner_block3_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 435 | 9.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_geometry.py` |
| 14 | `su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03` | bounded_theorem | unaudited | critical | 434 | 10.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_su3_wigner_l3_cube_partition.py` |
| 15 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | positive_theorem | claim_type_backfill_reaudit | critical | 354 | 22.47 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_triangle_right_angle.py` |
| 16 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 344 | 25.43 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_magnitudes_structural_counts.py` |
| 17 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 336 | 21.40 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_nlo_barred_triangle_protected_gamma.py` |
| 18 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 325 | 16.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bernoulli_two_ninths_koide_bridge.py` |
| 19 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 324 | 16.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_bs_mixing_phase_derivation.py` |
| 20 | `ckm_thales_cross_system_cp_ratio_theorem_note_2026-04-25` | positive_theorem | claim_type_backfill_reaudit | critical | 323 | 16.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_thales_cross_system_cp_ratio.py` |
| 21 | `yt_zero_import_authority_note` | - | unaudited | critical | 321 | 11.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 22 | `ckm_atlas_axiom_closure_note` | positive_theorem | claim_type_backfill_reaudit | critical | 319 | 22.82 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ckm_atlas_axiom_closure.py` |
| 23 | `universal_qg_canonical_refinement_net_note` | - | unaudited | critical | 319 | 15.82 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 24 | `universal_qg_uv_finite_partition_note` | - | unaudited | critical | 319 | 14.32 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 315 | 12.80 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 26 | `sign_portability_invariant_note` | bounded_theorem | unaudited | critical | 315 | 10.80 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py` |
| 27 | `diamond_absolute_unit_bridge_note` | positive_theorem | unaudited | critical | 315 | 8.80 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 28 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 314 | 12.80 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 29 | `diamond_phase_ramp_bridge_card_note` | positive_theorem | unaudited | critical | 314 | 9.30 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/diamond_phase_ramp_bridge_card.py` |
| 30 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 313 | 12.29 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `shapiro_delay_note` | positive_theorem | unaudited | critical | 313 | 11.29 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_phase_lag_probe.py` |
| 32 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 312 | 14.79 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 33 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 308 | 15.77 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 308 | 15.27 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 35 | `causal_field_canonical_chain_note` | positive_theorem | unaudited | critical | 308 | 9.27 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 307 | 14.27 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 37 | `frontier_extension_lane_opening_note_2026-04-25` | open_gate | unaudited | critical | 307 | 11.27 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 38 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 306 | 20.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |
| 39 | `quark_projector_ray_phase_completion_note_2026-04-18` | bounded_theorem | unaudited | critical | 306 | 13.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_projector_ray_phase_completion.py` |
| 40 | `quark_projector_parameter_audit_note_2026-04-19` | bounded_theorem | unaudited | critical | 305 | 18.26 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_projector_parameter_audit.py` |
| 41 | `r_base_group_theory_derivation_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 304 | 18.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_r_base_group_theory_derivation.py` |
| 42 | `neutrino_majorana_operator_axiom_first_note` | positive_theorem | unaudited | critical | 304 | 14.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_operator.py` |
| 43 | `higgs_mass_derived_note` | positive_theorem | claim_type_backfill_reaudit | critical | 302 | 17.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_full_3loop.py` |
| 44 | `neutrino_majorana_native_gaussian_no_go_note` | positive_theorem | unaudited | critical | 302 | 11.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 45 | `higgs_mechanism_note` | positive_theorem | unaudited | critical | 302 | 10.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 46 | `higgs_from_lattice_note` | bounded_theorem | unaudited | critical | 302 | 8.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_higgs_mass_derived.py` |
| 47 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 300 | 23.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 48 | `neutrino_majorana_finite_normal_grammar_no_go_note` | positive_theorem | unaudited | critical | 300 | 12.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 49 | `omega_lambda_derivation_note` | positive_theorem | unaudited | critical | 299 | 13.73 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 50 | `neutrino_majorana_pfaffian_extension_note` | positive_theorem | unaudited | critical | 299 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |

## Citation cycle break targets

168 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 438 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 2 | `cycle-0002` | 7 | 438 | `anomaly_forces_time_theorem` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 321 | `yt_explicit_systematic_budget_note` | critical | audited_conditional |
| 4 | `cycle-0004` | 2 | 319 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 5 | `cycle-0005` | 2 | 319 | `universal_qg_projective_schur_closure_note` | critical | audited_conditional |
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
