# Audit Queue

**Total pending:** 1173
**Ready (all deps already at retained-grade or metadata tiers):** 314

By criticality:
- `critical`: 818
- `high`: 24
- `medium`: 130
- `leaf`: 201

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `gate_b_grown_distance_law_note` | bounded_theorem | unaudited | critical | 328 | 12.36 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_grown_distance_law.py` |
| 2 | `ew_current_matching_rule_open_gate_note_2026-05-03` | no_go | audit_in_progress | critical | 326 | 13.85 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_current_matching_rule_no_go.py` |
| 3 | `claude_complex_action_grown_companion_note` | positive_theorem | unaudited | critical | 306 | 11.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_grown_companion.py` |
| 4 | `source_resolved_wavefield_escalation_note` | positive_theorem | unaudited | critical | 304 | 10.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_escalation.py` |
| 5 | `retarded_field_causality_probe_note` | bounded_theorem | unaudited | critical | 304 | 10.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/retarded_field_causality_probe.py` |
| 6 | `cl3_taste_generation_theorem` | positive_theorem | unaudited | critical | 303 | 13.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 7 | `s3_time_bilinear_tensor_primitive_note` | positive_theorem | unaudited | critical | 303 | 11.75 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 8 | `alt_connectivity_family_sign_note` | bounded_theorem | unaudited | critical | 303 | 10.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP.py` |
| 9 | `causal_field_portability_note` | positive_theorem | unaudited | critical | 302 | 11.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/causal_field_portability_probe.py` |
| 10 | `moving_source_retarded_portability_note` | bounded_theorem | unaudited | critical | 301 | 10.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/moving_source_retarded_portability_probe.py` |
| 11 | `source_resolved_wavefield_mechanism_note` | positive_theorem | unaudited | critical | 301 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_mechanism.py` |
| 12 | `claude_complex_action_carryover_note` | positive_theorem | unaudited | critical | 301 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/exact_lattice_complex_action_carryover.py` |
| 13 | `electrostatics_card_note` | positive_theorem | unaudited | critical | 301 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/electrostatics_card.py` |
| 14 | `second_grown_family_sign_note` | bounded_theorem | unaudited | critical | 301 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 15 | `third_grown_family_boundary_note` | positive_theorem | unaudited | critical | 301 | 9.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py` |
| 16 | `electrostatics_superposition_proxy_note` | positive_theorem | unaudited | critical | 301 | 8.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/electrostatics_superposition_proxy.py` |
| 17 | `diamond_sensor_protocol_note` | bounded_theorem | unaudited | critical | 300 | 9.73 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 18 | `fourth_family_quadrant_note` | positive_theorem | unaudited | critical | 297 | 9.22 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FOURTH_FAMILY_QUADRANT_SWEEP.py` |
| 19 | `s3_time_bilinear_tensor_action_note` | open_gate | unaudited | critical | 297 | 9.22 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 20 | `fifth_family_radial_boundary_note` | bounded_theorem | unaudited | critical | 296 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/FIFTH_FAMILY_RADIAL_FAILURE_AUDIT.py` |
| 21 | `source_resolved_wavefield_v2_note` | positive_theorem | unaudited | critical | 295 | 8.71 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_v2.py` |
| 22 | `gravity_sign_audit_2026-04-10` | positive_theorem | unaudited | critical | 293 | 12.20 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_correct_coupling.py` |
| 23 | `tensor_source_map_eta_note` | bounded_theorem | unaudited | critical | 293 | 9.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_tensor_source_map_eta.py` |
| 24 | `universal_gr_discrete_global_closure_note` | positive_theorem | unaudited | critical | 292 | 18.70 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 25 | `cl3_sm_embedding_theorem` | positive_theorem | unaudited | critical | 292 | 14.70 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/verify_cl3_sm_embedding.py` |
| 26 | `shapiro_static_discriminator_note` | positive_theorem | unaudited | critical | 291 | 10.19 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/shapiro_static_discriminator.py` |
| 27 | `signed_gravity_response_lane_status_note_2026-04-26` | no_go | unaudited | critical | 289 | 12.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_signed_gravity_response_lane_status.py` |
| 28 | `complex_action_note` | bounded_theorem | unaudited | critical | 289 | 11.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/complex_action_harness.py` |
| 29 | `gravitomagnetic_note` | positive_theorem | unaudited | critical | 289 | 9.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/gravitomagnetic_portable.py` |
| 30 | `causal_escape_window_note` | bounded_theorem | unaudited | critical | 289 | 8.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/causal_escape_window.py` |
| 31 | `single_axiom_hilbert_note` | positive_theorem | unaudited | critical | 288 | 12.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_single_axiom_hilbert.py` |
| 32 | `bell_inequality_derived_note` | bounded_theorem | unaudited | critical | 288 | 11.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bell_inequality.py` |
| 33 | `lensing_k_sweep_note` | bounded_theorem | unaudited | critical | 288 | 10.68 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/lensing_k_sweep.py` |
| 34 | `electrostatics_grown_sign_law_note` | bounded_theorem | unaudited | critical | 288 | 9.18 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py` |
| 35 | `quark_cp_carrier_completion_note_2026-04-18` | bounded_theorem | unaudited | critical | 287 | 13.17 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_quark_cp_carrier_completion.py` |
| 36 | `universal_gr_polarization_frame_bundle_blocker_note` | bounded_theorem | unaudited | critical | 285 | 10.16 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_polarization_frame_bundle.py` |
| 37 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 283 | 16.65 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 38 | `scalar_trace_tensor_no_go_note` | bounded_theorem | unaudited | critical | 283 | 9.15 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_scalar_trace_tensor_nogo.py` |
| 39 | `yukawa_color_projection_theorem` | positive_theorem | unaudited | critical | 282 | 13.14 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_ew_current_fierz_channel_decomposition.py` |
| 40 | `taste_scalar_isotropy_theorem_note` | bounded_theorem | claim_type_backfill_reaudit | critical | 280 | 14.13 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_taste_scalar_isotropy.py` |
| 41 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 280 | 10.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |
| 42 | `yt_bridge_uv_class_uniqueness_note` | bounded_theorem | unaudited | critical | 279 | 9.63 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_uv_class_uniqueness.py` |
| 43 | `oh_schur_boundary_action_note` | positive_theorem | unaudited | critical | 278 | 12.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_oh_schur_boundary_action.py` |
| 44 | `cosmology_scale_identification_and_reduction_note` | bounded_theorem | unaudited | critical | 277 | 14.62 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `charged_lepton_two_higgs_canonical_reduction_note` | positive_theorem | unaudited | critical | 277 | 13.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_charged_lepton_two_higgs_canonical_reduction.py` |
| 46 | `neutrino_dirac_two_higgs_canonical_reduction_note` | positive_theorem | unaudited | critical | 277 | 12.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_neutrino_dirac_two_higgs_canonical_reduction.py` |
| 47 | `graviton_mass_derived_note` | bounded_theorem | unaudited | critical | 277 | 12.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graviton_mass_derived.py` |
| 48 | `dark_energy_eos_note` | bounded_theorem | unaudited | critical | 277 | 9.62 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dark_energy_eos.py` |
| 49 | `strong_cp_theta_zero_note` | bounded_theorem | unaudited | critical | 276 | 15.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_strong_cp_theta_zero.py` |
| 50 | `universal_theta_induced_edm_vanishing_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 276 | 13.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_theta_induced_edm_vanishing.py` |

## Citation cycle break targets

192 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 404 | `angular_kernel_underdetermination_no_go_note` | critical | unaudited |
| 2 | `cycle-0002` | 7 | 404 | `anomaly_forces_time_theorem` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 299 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 299 | `universal_qg_projective_schur_closure_note` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 299 | `universal_qg_canonical_refinement_net_note` | critical | unaudited |
| 6 | `cycle-0006` | 2 | 279 | `higgs_from_lattice_note` | critical | unaudited |
| 7 | `cycle-0007` | 2 | 279 | `higgs_mass_derived_note` | critical | audited_conditional |
| 8 | `cycle-0008` | 2 | 276 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 273 | `yt_explicit_systematic_budget_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 269 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 269 | `koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 269 | `universal_gr_tensor_quotient_uniqueness_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 269 | `koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18` | critical | unaudited |
| 14 | `cycle-0014` | 2 | 268 | `lensing_finite_path_explanation_note` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 267 | `quark_issr1_bicac_forcing_theorem_note_2026-04-19` | critical | unaudited |
| 16 | `cycle-0016` | 2 | 266 | `pmns_c3_character_holonomy_closure_note` | critical | unaudited |
| 17 | `cycle-0017` | 2 | 264 | `abcc_cp_phase_no_go_theorem_note_2026-04-19` | critical | unaudited |
| 18 | `cycle-0018` | 2 | 264 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 19 | `cycle-0019` | 2 | 264 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 264 | `charged_lepton_koide_review_packet_2026-04-18` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 264 | `dm_pmns_graph_first_ordered_chain_nonzero_current_activation_theorem_note_2026-04-21` | critical | unaudited |
| 22 | `cycle-0022` | 2 | 264 | `hadron_mass_lane1_theorem_plan_support_note_2026-04-27` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 264 | `koide_a1_fractional_topology_no_go_synthesis_note_2026-04-24` | critical | unaudited |
| 24 | `cycle-0024` | 2 | 264 | `koide_eigenvalue_q23_surface_theorem_note_2026-04-20` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 264 | `koide_berry_phase_theorem_note_2026-04-19` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
