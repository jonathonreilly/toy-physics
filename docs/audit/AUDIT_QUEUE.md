# Audit Queue

**Generated:** 2026-05-02T20:49:27.531694+00:00
**Total pending:** 615
**Ready (all deps already at retained-grade or metadata tiers):** 133

By criticality:
- `critical`: 72
- `high`: 209
- `medium`: 168
- `leaf`: 166

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `planck_boundary_density_extension_theorem_note_2026-04-24` | - | unaudited | critical | 307 | 14.27 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 2 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 307 | 11.27 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_reflection_positivity_check.py` |
| 3 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | - | unaudited | critical | 306 | 14.76 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 4 | `axiom_first_cluster_decomposition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 306 | 10.26 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cluster_decomposition_check.py` |
| 5 | `physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30` | - | unaudited | critical | 305 | 12.76 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_hermitian_hamiltonian_and_sme_bridge.py` |
| 6 | `physical_lattice_necessity_note` | no_go | unaudited | critical | 304 | 15.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_physical_lattice_necessity.py` |
| 7 | `planck_parent_source_hidden_character_no_go_note_2026-04-24` | - | unaudited | critical | 303 | 17.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_parent_source_hidden_character_nogo.py` |
| 8 | `bh_entropy_derived_note` | - | unaudited | critical | 303 | 12.25 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 9 | `holographic_probe_note_2026-04-11` | - | unaudited | critical | 303 | 9.75 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_holographic_probe.py` |
| 10 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | - | unaudited | critical | 302 | 15.24 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 11 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | - | unaudited | critical | 302 | 14.74 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` | - | unaudited | critical | 302 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_cl3_per_site_uniqueness_check.py` |
| 13 | `staggered_fermion_card_2026-04-10` | - | unaudited | critical | 302 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_17card.py` |
| 14 | `area_law_algebraic_spectrum_entropy_no_go_note_2026-04-25` | - | unaudited | critical | 301 | 12.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py` |
| 15 | `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25` | - | unaudited | critical | 301 | 12.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_edge_entropy_selector_no_go.py` |
| 16 | `gravity_clean_derivation_note` | - | unaudited | critical | 301 | 12.74 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `i3_zero_exact_theorem_note` | - | unaudited | critical | 301 | 12.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_born_rule_derived.py` |
| 18 | `action_normalization_note` | bounded_theorem | unaudited | critical | 301 | 10.24 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_action_normalization.py` |
| 19 | `light_cone_framing_note` | - | unaudited | critical | 301 | 9.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 20 | `architecture_note_directional_measure` | - | unaudited | critical | 301 | 8.74 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 21 | `first_order_coframe_unconditionality_no_go_theorem_note_2026-04-30` | - | unaudited | critical | 301 | 8.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_first_order_coframe_unconditionality_no_go.py` |
| 22 | `substrate_to_p_a_forcing_theorem_note_2026-04-30` | - | unaudited | critical | 301 | 8.74 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_substrate_to_p_a_forcing.py` |
| 23 | `yt_ward_identity_derivation_theorem` | positive_theorem | claim_type_backfill_reaudit | critical | 183 | 26.52 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 24 | `confinement_string_tension_note` | positive_theorem | claim_type_backfill_reaudit | critical | 54 | 13.28 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_confinement_string_tension.py` |
| 25 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 306 | 10.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 26 | `planck_finite_response_no_go_note_2026-04-24` | - | unaudited | critical | 302 | 12.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_finite_response_nogo.py` |
| 27 | `boundary_law_robustness_note_2026-04-11` | bounded_theorem | unaudited | critical | 302 | 9.24 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_boundary_law_robustness.py` |
| 28 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 301 | 14.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 29 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 301 | 13.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 30 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 301 | 12.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 31 | `bh_entropy_rt_ratio_widom_no_go_note` | no_go | unaudited | critical | 301 | 11.74 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_rt_ratio_widom.py` |
| 32 | `anomaly_forces_time_theorem` | positive_theorem | unaudited | critical | 300 | 19.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 33 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 300 | 14.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 34 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 300 | 14.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 35 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 300 | 14.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 36 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 300 | 14.23 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 37 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 300 | 13.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 38 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 300 | 13.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 39 | `angular_kernel_underdetermination_no_go_note` | no_go | unaudited | critical | 300 | 12.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_angular_kernel_underdetermination_nogo.py` |
| 40 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 300 | 12.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 41 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 300 | 12.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 42 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 300 | 12.23 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 43 | `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 300 | 11.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` |
| 44 | `area_law_coefficient_gap_note` | positive_theorem | unaudited | critical | 300 | 11.23 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 45 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 300 | 9.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 46 | `axiom_first_lattice_wess_zumino_fujikawa_theorem_note_2026-05-02` | bounded_theorem | unaudited | critical | 300 | 8.73 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_lattice_wess_zumino_check.py` |
| 47 | `one_generation_matter_closure_note` | positive_theorem | unaudited | critical | 259 | 21.02 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_right_handed_sector.py` |
| 48 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 244 | 16.44 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 49 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 238 | 28.90 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 50 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | positive_theorem | unaudited | critical | 132 | 16.55 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_sm_hypercharge_uniqueness.py` |

Full queue lives in `data/audit_queue.json`.
