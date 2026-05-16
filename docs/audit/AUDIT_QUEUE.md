# Audit Queue

**Total pending:** 1206
**Ready (all deps already at retained-grade or metadata tiers):** 22

By criticality:
- `critical`: 748
- `high`: 34
- `medium`: 151
- `leaf`: 273

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `pmns_graph_axis_to_active_lane_bridge_note` | bounded_theorem | audit_in_progress | critical | 784 | 10.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_graph_axis_to_active_lane_bridge.py` |
| 2 | `hierarchy_matsubara_free_energy_density_narrow_theorem_note_2026-05-16` | positive_theorem | unaudited | critical | 783 | 10.12 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_hierarchy_matsubara_free_energy_density_narrow.py` |
| 3 | `koide_q_readout_factorization_theorem_2026-04-22` | bounded_theorem | unaudited | critical | 782 | 12.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_q_readout_factorization_theorem.py` |
| 4 | `s3_boundary_link_theorem_note` | bounded_theorem | unaudited | critical | 782 | 12.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_s3_boundary_link_theorem.py` |
| 5 | `pmns_commutant_eigenoperator_selector_note` | bounded_theorem | unaudited | critical | 782 | 11.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_commutant_eigenoperator_selector.py` |
| 6 | `koide_frobenius_isotype_split_uniqueness_note_2026-04-21` | bounded_theorem | unaudited | critical | 781 | 15.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` |
| 7 | `dm_leptogenesis_pmns_projector_interface_note_2026-04-16` | bounded_theorem | unaudited | critical | 781 | 14.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dm_leptogenesis_pmns_projector_interface.py` |
| 8 | `graviton_mass_derived_note` | bounded_theorem | unaudited | critical | 781 | 13.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_graviton_mass_derived.py` |
| 9 | `pmns_hw1_source_transfer_boundary_note` | bounded_theorem | unaudited | critical | 781 | 11.61 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_pmns_hw1_source_transfer_boundary.py` |
| 10 | `dark_energy_eos_note` | decoration | unaudited | critical | 781 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dark_energy_eos.py` |
| 11 | `generation_axiom_boundary_note` | bounded_theorem | unaudited | critical | 781 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_axiom_boundary.py` |
| 12 | `koide_cl3_selector_gap_note_2026-04-19` | open_gate | unaudited | critical | 781 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 13 | `koide_a1_physical_bridge_attempt_2026-04-22` | no_go | unaudited | critical | 781 | 10.11 | Y | fresh_context_or_stronger_with_cross_confirmation | - |
| 14 | `wave_static_direct_probe_fine_note` | positive_theorem | unaudited | critical | 781 | 10.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/wave_static_direct_probe.py` |
| 15 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 919 | 14.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 16 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 918 | 13.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 17 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 913 | 13.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 18 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 913 | 12.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 19 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 912 | 28.83 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 20 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 866 | 13.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 21 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 865 | 37.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 22 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 860 | 11.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 23 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 859 | 34.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 24 | `yt_color_projection_correction_note` | bounded_theorem | unaudited | critical | 837 | 14.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 25 | `yt_qfp_insensitivity_support_note` | bounded_theorem | unaudited | critical | 836 | 17.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 26 | `yt_exact_schur_normal_form_uniqueness_note` | bounded_theorem | unaudited | critical | 836 | 16.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py` |
| 27 | `yt_boundary_theorem` | open_gate | unaudited | critical | 836 | 16.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_boundary_consistency.py` |
| 28 | `yt_constructive_uv_bridge_note` | bounded_theorem | unaudited | critical | 836 | 16.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_constructive_uv_bridge.py` |
| 29 | `yt_interacting_bridge_locality_note` | bounded_theorem | unaudited | critical | 836 | 15.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_interacting_bridge_locality.py` |
| 30 | `yt_bridge_hessian_selector_note` | bounded_theorem | unaudited | critical | 836 | 14.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_hessian_selector.py` |
| 31 | `yt_bridge_rearrangement_principle_note` | bounded_theorem | unaudited | critical | 836 | 13.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_rearrangement_principle.py` |
| 32 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 836 | 13.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 33 | `yt_bridge_higher_order_corrections_note` | bounded_theorem | unaudited | critical | 836 | 13.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_higher_order_corrections.py` |
| 34 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 836 | 13.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |
| 35 | `yt_bridge_action_invariant_note` | bounded_theorem | unaudited | critical | 836 | 12.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_action_invariant.py` |
| 36 | `yt_bridge_moment_closure_note` | bounded_theorem | unaudited | critical | 836 | 12.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_moment_closure.py` |
| 37 | `yt_bridge_operator_closure_note` | bounded_theorem | unaudited | critical | 836 | 12.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_operator_closure.py` |
| 38 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 836 | 12.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 39 | `yt_exact_coarse_grained_bridge_operator_note` | bounded_theorem | unaudited | critical | 836 | 11.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_coarse_grained_bridge_operator.py` |
| 40 | `yt_exact_interacting_bridge_transport_note` | bounded_theorem | unaudited | critical | 836 | 11.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_interacting_bridge_transport.py` |
| 41 | `yt_bridge_endpoint_shift_bound_note` | bounded_theorem | unaudited | critical | 836 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_endpoint_shift_bound.py` |
| 42 | `yt_bridge_uv_class_uniqueness_note` | bounded_theorem | unaudited | critical | 836 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_uv_class_uniqueness.py` |
| 43 | `yt_ew_coupling_bridge_note` | positive_theorem | unaudited | critical | 836 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ew_coupling_derivation.py` |
| 44 | `yt_eft_bridge_theorem` | open_gate | unaudited | critical | 836 | 10.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_eft_bridge.py` |
| 45 | `gate_b_grown_joint_package_note` | bounded_theorem | unaudited | critical | 829 | 13.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_grown_joint_package.py` |
| 46 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 814 | 46.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 47 | `gate_b_weak_connectivity_note` | bounded_theorem | unaudited | critical | 813 | 12.67 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_weak_connectivity_harness.py` |
| 48 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 809 | 30.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 49 | `g_bare_rigidity_theorem_note` | positive_theorem | unaudited | critical | 809 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 50 | `gate_b_nonlabel_connectivity_v1_note` | bounded_theorem | unaudited | critical | 809 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1.py` |

## Citation cycle break targets

242 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 836 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 836 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 836 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 836 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 836 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 836 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 7 | `cycle-0007` | 3 | 836 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 8 | `cycle-0008` | 4 | 836 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 836 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 836 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 11 | `cycle-0011` | 8 | 836 | `yt_boundary_theorem` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 806 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 13 | `cycle-0013` | 2 | 806 | `source_resolved_exact_green_pocket_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 806 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 797 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 16 | `cycle-0016` | 4 | 797 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 17 | `cycle-0017` | 6 | 797 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 18 | `cycle-0018` | 7 | 797 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 19 | `cycle-0019` | 8 | 797 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 20 | `cycle-0020` | 9 | 797 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 21 | `cycle-0021` | 9 | 797 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 22 | `cycle-0022` | 10 | 797 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 792 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | audited_conditional |
| 24 | `cycle-0024` | 2 | 787 | `pmns_active_four_real_source_from_transport_note` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 783 | `lensing_finite_path_explanation_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
