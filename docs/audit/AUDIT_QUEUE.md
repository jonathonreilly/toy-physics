# Audit Queue

**Total pending:** 1176
**Ready (all deps already at retained-grade or metadata tiers):** 0

By criticality:
- `critical`: 730
- `high`: 34
- `medium`: 152
- `leaf`: 260

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `staggered_wilson_det_positivity_bridge_theorem_note_2026-05-05` | positive_theorem | unaudited | critical | 786 | 11.12 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py` |
| 2 | `poisson_exhaustive_uniqueness_note` | bounded_theorem | unaudited | critical | 781 | 14.61 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 3 | `universal_gr_positive_background_local_closure_note` | bounded_theorem | unaudited | critical | 780 | 14.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 4 | `universal_qg_projective_schur_closure_note` | positive_theorem | unaudited | critical | 778 | 14.61 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 5 | `hopping_bilinear_hermiticity_theorem_note_2026-05-02` | positive_theorem | unaudited | critical | 778 | 11.11 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/hopping_bilinear_hermiticity_check.py` |
| 6 | `universal_qg_uv_finite_partition_note` | positive_theorem | unaudited | critical | 777 | 16.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 7 | `microcausality_finite_range_h_and_vlr_bridge_theorem_note_2026-05-09` | bounded_theorem | unaudited | critical | 777 | 11.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/microcausality_finite_range_h_bridge_2026_05_09.py` |
| 8 | `gravity_clean_derivation_note` | bounded_theorem | unaudited | critical | 776 | 18.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 9 | `universal_qg_canonical_refinement_net_note` | positive_theorem | unaudited | critical | 776 | 18.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 10 | `axiom_first_spectrum_condition_theorem_note_2026-04-29` | positive_theorem | unaudited | critical | 776 | 14.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_spectrum_condition_check.py` |
| 11 | `universal_gr_curvature_localization_blocker_note` | positive_theorem | unaudited | critical | 776 | 11.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 12 | `light_cone_crank_nicolson_lieb_robinson_bridge_note_2026-05-09` | bounded_theorem | unaudited | critical | 776 | 10.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_crank_nicolson_lr_2026_05_09.py` |
| 13 | `s3_general_r_derivation_note` | positive_theorem | unaudited | critical | 775 | 18.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_cap_uniqueness.py` |
| 14 | `universal_qg_inverse_limit_closure_note` | bounded_theorem | unaudited | critical | 775 | 15.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 15 | `bh_entropy_derived_note` | bounded_theorem | unaudited | critical | 775 | 13.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_bh_entropy_derived.py` |
| 16 | `universal_gr_tensor_variational_candidate_note` | bounded_theorem | unaudited | critical | 775 | 13.60 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 17 | `light_cone_framing_note` | positive_theorem | unaudited | critical | 775 | 11.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/light_cone_staggered_dispersion.py` |
| 18 | `universal_gr_positive_background_extension_note` | positive_theorem | unaudited | critical | 775 | 11.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/universal_gr_positive_background_local_closure.py` |
| 19 | `s3_time_theta_to_slice_coupling_note` | open_gate | unaudited | critical | 775 | 10.60 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 20 | `anomaly_forces_time_theorem` | bounded_theorem | unaudited | critical | 774 | 30.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_anomaly_forces_time.py` |
| 21 | `universal_gr_discrete_global_closure_note` | bounded_theorem | unaudited | critical | 774 | 22.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_universal_gr_discrete_global_closure.py` |
| 22 | `planck_primitive_coframe_boundary_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 774 | 20.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_primitive_coframe_boundary_carrier.py` |
| 23 | `planck_source_unit_normalization_support_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 774 | 19.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_source_unit_normalization_support_theorem.py` |
| 24 | `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01` | positive_theorem | unaudited | critical | 774 | 19.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_microcausality_check.py` |
| 25 | `emergent_lorentz_invariance_note` | bounded_theorem | unaudited | critical | 774 | 18.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_emergent_lorentz_invariance.py` |
| 26 | `planck_target3_clifford_phase_bridge_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 774 | 18.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_target3_clifford_phase_bridge.py` |
| 27 | `planck_boundary_density_extension_theorem_note_2026-04-24` | bounded_theorem | unaudited | critical | 774 | 17.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_boundary_density_extension.py` |
| 28 | `axiom_first_single_clock_codimension1_evolution_theorem_note_2026-05-03` | positive_theorem | unaudited | critical | 774 | 16.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/axiom_first_single_clock_codimension1_evolution_check.py` |
| 29 | `planck_scale_lane_status_note_2026-04-23` | positive_theorem | unaudited | critical | 774 | 16.60 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 30 | `universal_qg_pl_weak_form_note` | positive_theorem | unaudited | critical | 774 | 16.60 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 31 | `universal_qg_smooth_gravitational_global_solution_class_note` | positive_theorem | unaudited | critical | 774 | 16.60 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 32 | `universal_qg_abstract_gaussian_completion_note` | positive_theorem | unaudited | critical | 774 | 16.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 33 | `universal_qg_canonical_textbook_weak_measure_equivalence_note` | positive_theorem | unaudited | critical | 774 | 16.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 34 | `universal_qg_pl_sobolev_interface_note` | positive_theorem | unaudited | critical | 774 | 16.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 35 | `universal_qg_smooth_gravitational_local_identification_note` | positive_theorem | unaudited | critical | 774 | 16.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 36 | `area_law_quarter_broader_no_go_note_2026-04-25` | no_go | unaudited | critical | 774 | 15.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_quarter_broader_no_go.py` |
| 37 | `lorentz_boost_covariance_2d_theorem_note` | positive_theorem | unaudited | critical | 774 | 15.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_2d.py` |
| 38 | `lorentz_kernel_positive_closure_note` | positive_theorem | unaudited | critical | 774 | 15.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_kernel_positive_closure.py` |
| 39 | `universal_qg_canonical_textbook_geometric_action_equivalence_note` | positive_theorem | unaudited | critical | 774 | 15.60 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 40 | `universal_qg_pl_field_interface_note` | positive_theorem | unaudited | critical | 774 | 15.60 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 41 | `planck_scale_conditional_completion_note_2026-04-24` | positive_theorem | unaudited | critical | 774 | 15.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_conditional_completion_audit.py` |
| 42 | `universal_gr_lorentzian_signature_extension_note` | positive_theorem | unaudited | critical | 774 | 15.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 43 | `universal_qg_smooth_gravitational_global_atlas_note` | positive_theorem | unaudited | critical | 774 | 15.10 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 44 | `area_law_multipocket_selector_no_go_note_2026-04-25` | no_go | unaudited | critical | 774 | 14.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_multipocket_selector_no_go.py` |
| 45 | `area_law_primitive_car_edge_identification_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 774 | 14.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_car_edge_identification.py` |
| 46 | `lorentz_boost_covariance_3plus1d_theorem_note` | positive_theorem | unaudited | critical | 774 | 14.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_lorentz_boost_3plus1d.py` |
| 47 | `universal_qg_canonical_smooth_gravitational_weak_measure_note` | positive_theorem | unaudited | critical | 774 | 14.60 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 48 | `area_law_native_car_semantics_tightening_note_2026-04-25` | positive_theorem | unaudited | critical | 774 | 14.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_native_car_semantics_tightening.py` |
| 49 | `area_law_primitive_parity_gate_carrier_theorem_note_2026-04-25` | positive_theorem | unaudited | critical | 774 | 14.10 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_area_law_primitive_parity_gate_carrier.py` |
| 50 | `planck_link_local_first_variation_p_a_forcing_theorem_note_2026-04-30` | positive_theorem | unaudited | critical | 774 | 13.60 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_planck_link_local_first_variation_p_a_forcing.py` |

## Citation cycle break targets

186 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 786 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | audited_conditional |
| 2 | `cycle-0002` | 11 | 774 | `anomaly_forces_time_theorem` | critical | unaudited |
| 3 | `cycle-0003` | 12 | 774 | `anomaly_forces_time_theorem` | critical | unaudited |
| 4 | `cycle-0004` | 13 | 774 | `anomaly_forces_time_theorem` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 739 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 6 | `cycle-0006` | 4 | 739 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 7 | `cycle-0007` | 5 | 739 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | critical | unaudited |
| 8 | `cycle-0008` | 6 | 739 | `gauge_scalar_bridge_3plus1_native_tube_staging_gate_2026-05-03` | critical | unaudited |
| 9 | `cycle-0009` | 2 | 552 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 10 | `cycle-0010` | 2 | 552 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 11 | `cycle-0011` | 2 | 552 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 552 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 13 | `cycle-0013` | 3 | 552 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 552 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 15 | `cycle-0015` | 3 | 552 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 16 | `cycle-0016` | 4 | 552 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 17 | `cycle-0017` | 4 | 552 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 18 | `cycle-0018` | 4 | 552 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 19 | `cycle-0019` | 8 | 552 | `yt_boundary_theorem` | critical | unaudited |
| 20 | `cycle-0020` | 2 | 470 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 21 | `cycle-0021` | 2 | 470 | `source_resolved_exact_green_pocket_note` | critical | unaudited |
| 22 | `cycle-0022` | 3 | 470 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 437 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 24 | `cycle-0024` | 3 | 437 | `cosmological_constant_result_2026-04-12` | critical | unaudited |
| 25 | `cycle-0025` | 4 | 437 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
