# Audit Queue

**Total pending:** 1188
**Ready (all deps already at retained-grade or metadata tiers):** 2

By criticality:
- `critical`: 735
- `high`: 34
- `medium`: 152
- `leaf`: 267

Auditor (current best Codex GPT model at maximum reasoning by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---|---|---:|---:|:---:|---|---|
| 1 | `dark_energy_eos_note` | decoration | unaudited | critical | 782 | 11.11 | Y | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_dark_energy_eos.py` |
| 2 | `gauge_vacuum_plaquette_spatial_environment_transfer_theorem_note` | positive_theorem | unaudited | critical | 921 | 14.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py` |
| 3 | `gauge_vacuum_plaquette_tensor_transfer_perron_solve_note` | positive_theorem | unaudited | critical | 920 | 13.35 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py` |
| 4 | `gauge_vacuum_plaquette_bridge_support_note` | positive_theorem | unaudited | critical | 915 | 13.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py` |
| 5 | `gauge_vacuum_plaquette_susceptibility_flow_theorem_note` | bounded_theorem | unaudited | critical | 915 | 12.34 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py` |
| 6 | `plaquette_self_consistency_note` | bounded_theorem | unaudited | critical | 914 | 29.84 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_plaquette_self_consistency.py` |
| 7 | `qcd_low_energy_running_bridge_note_2026-05-01` | bounded_theorem | unaudited | critical | 868 | 13.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_qcd_low_energy_running_bridge.py` |
| 8 | `alpha_s_derived_note` | bounded_theorem | unaudited | critical | 867 | 37.76 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_zero_import_chain.py` |
| 9 | `yt_vertex_power_derivation` | open_gate | unaudited | critical | 862 | 11.25 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_vertex_power.py` |
| 10 | `yt_ward_identity_derivation_theorem` | bounded_theorem | unaudited | critical | 861 | 34.75 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 11 | `yt_color_projection_correction_note` | bounded_theorem | unaudited | critical | 839 | 14.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_color_projection_correction.py` |
| 12 | `yt_qfp_insensitivity_support_note` | bounded_theorem | unaudited | critical | 838 | 17.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_qfp_insensitivity.py` |
| 13 | `yt_exact_schur_normal_form_uniqueness_note` | bounded_theorem | unaudited | critical | 838 | 16.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_schur_normal_form_uniqueness.py` |
| 14 | `yt_boundary_theorem` | open_gate | unaudited | critical | 838 | 16.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_boundary_consistency.py` |
| 15 | `yt_constructive_uv_bridge_note` | bounded_theorem | unaudited | critical | 838 | 16.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_constructive_uv_bridge.py` |
| 16 | `yt_interacting_bridge_locality_note` | bounded_theorem | unaudited | critical | 838 | 15.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_interacting_bridge_locality.py` |
| 17 | `yt_bridge_hessian_selector_note` | bounded_theorem | unaudited | critical | 838 | 14.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_hessian_selector.py` |
| 18 | `yt_bridge_rearrangement_principle_note` | bounded_theorem | unaudited | critical | 838 | 13.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_rearrangement_principle.py` |
| 19 | `yt_zero_import_authority_note` | positive_theorem | unaudited | critical | 838 | 13.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ward_identity_derivation.py` |
| 20 | `yt_bridge_higher_order_corrections_note` | bounded_theorem | unaudited | critical | 838 | 13.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_higher_order_corrections.py` |
| 21 | `yt_bridge_nonlocal_corrections_note` | bounded_theorem | unaudited | critical | 838 | 13.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_nonlocal_corrections.py` |
| 22 | `yt_bridge_action_invariant_note` | bounded_theorem | unaudited | critical | 838 | 12.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_action_invariant.py` |
| 23 | `yt_bridge_moment_closure_note` | bounded_theorem | unaudited | critical | 838 | 12.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_moment_closure.py` |
| 24 | `yt_bridge_operator_closure_note` | bounded_theorem | unaudited | critical | 838 | 12.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_operator_closure.py` |
| 25 | `yt_explicit_systematic_budget_note` | positive_theorem | unaudited | critical | 838 | 12.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_explicit_systematic_budget.py` |
| 26 | `yt_exact_coarse_grained_bridge_operator_note` | bounded_theorem | unaudited | critical | 838 | 11.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_coarse_grained_bridge_operator.py` |
| 27 | `yt_exact_interacting_bridge_transport_note` | bounded_theorem | unaudited | critical | 838 | 11.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_exact_interacting_bridge_transport.py` |
| 28 | `yt_bridge_endpoint_shift_bound_note` | bounded_theorem | unaudited | critical | 838 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_endpoint_shift_bound.py` |
| 29 | `yt_bridge_uv_class_uniqueness_note` | bounded_theorem | unaudited | critical | 838 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_bridge_uv_class_uniqueness.py` |
| 30 | `yt_ew_coupling_bridge_note` | positive_theorem | unaudited | critical | 838 | 11.21 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_ew_coupling_derivation.py` |
| 31 | `yt_eft_bridge_theorem` | open_gate | unaudited | critical | 838 | 10.71 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_yt_eft_bridge.py` |
| 32 | `gate_b_grown_joint_package_note` | bounded_theorem | unaudited | critical | 830 | 13.70 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_grown_joint_package.py` |
| 33 | `three_generation_observable_theorem_note` | bounded_theorem | unaudited | critical | 816 | 46.17 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_three_generation_observable_theorem.py` |
| 34 | `gate_b_weak_connectivity_note` | bounded_theorem | unaudited | critical | 814 | 12.67 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_weak_connectivity_harness.py` |
| 35 | `three_generation_structure_note` | bounded_theorem | unaudited | critical | 811 | 30.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_generation_fermi_point.py` |
| 36 | `g_bare_rigidity_theorem_note` | positive_theorem | unaudited | critical | 811 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_rigidity_theorem.py` |
| 37 | `g_bare_structural_normalization_theorem_note_2026-04-18` | positive_theorem | unaudited | critical | 810 | 18.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/frontier_g_bare_structural_normalization.py` |
| 38 | `gate_b_nonlabel_connectivity_v1_note` | bounded_theorem | unaudited | critical | 810 | 13.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1.py` |
| 39 | `source_resolved_exact_green_pocket_note` | bounded_theorem | unaudited | critical | 807 | 12.66 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_pocket.py` |
| 40 | `source_resolved_exact_green_scaling_note` | bounded_theorem | unaudited | critical | 807 | 11.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_scaling.py` |
| 41 | `source_resolved_propagating_green_pocket_note` | positive_theorem | unaudited | critical | 807 | 11.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_propagating_green_pocket.py` |
| 42 | `source_resolved_exact_green_h025_pocket_note` | bounded_theorem | unaudited | critical | 807 | 10.16 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_exact_green_h025_pocket.py` |
| 43 | `gate_b_nonlabel_connectivity_v1_distance_note` | bounded_theorem | unaudited | critical | 803 | 10.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1_distance.py` |
| 44 | `gate_b_nonlabel_connectivity_v1_joint_note` | bounded_theorem | unaudited | critical | 803 | 10.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/gate_b_nonlabel_connectivity_v1_joint.py` |
| 45 | `minimal_absorbing_horizon_probe_note` | bounded_theorem | unaudited | critical | 802 | 11.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_absorbing_horizon_probe.py` |
| 46 | `source_resolved_wavefield_green_pocket_note` | positive_theorem | unaudited | critical | 802 | 10.65 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_green_pocket.py` |
| 47 | `source_resolved_wavefield_escalation_note` | bounded_theorem | unaudited | critical | 801 | 13.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/source_resolved_wavefield_escalation.py` |
| 48 | `minimal_bidirectional_trapping_probe_note` | bounded_theorem | unaudited | critical | 800 | 10.15 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/minimal_bidirectional_trapping_probe.py` |
| 49 | `retarded_field_delay_proxy_note` | bounded_theorem | unaudited | critical | 799 | 11.14 |  | fresh_context_or_stronger_with_cross_confirmation | `scripts/retarded_field_delay_proxy_probe.py` |
| 50 | `g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19` | positive_theorem | unaudited | critical | 798 | 12.64 |  | fresh_context_or_stronger_with_cross_confirmation | - |

## Citation cycle break targets

242 citation cycles in the graph. Each cycle permanently blocks every member from `retained` until one node is re-audited with explicit cycle-break instructions or a 'see also' edge is stripped. Top 25 below; full list in `data/audit_queue.json` under `cycle_break_targets`.

| # | cycle_id | length | max_desc | primary break target | criticality | audit_status |
|---:|---|---:|---:|---|---|---|
| 1 | `cycle-0001` | 2 | 838 | `yt_bridge_action_invariant_note` | critical | unaudited |
| 2 | `cycle-0002` | 2 | 838 | `yt_bridge_rearrangement_principle_note` | critical | unaudited |
| 3 | `cycle-0003` | 2 | 838 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 4 | `cycle-0004` | 2 | 838 | `yt_ew_coupling_bridge_note` | critical | unaudited |
| 5 | `cycle-0005` | 3 | 838 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 6 | `cycle-0006` | 3 | 838 | `yt_bridge_moment_closure_note` | critical | unaudited |
| 7 | `cycle-0007` | 3 | 838 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 8 | `cycle-0008` | 4 | 838 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 9 | `cycle-0009` | 4 | 838 | `yt_bridge_hessian_selector_note` | critical | unaudited |
| 10 | `cycle-0010` | 4 | 838 | `yt_bridge_operator_closure_note` | critical | unaudited |
| 11 | `cycle-0011` | 8 | 838 | `yt_boundary_theorem` | critical | unaudited |
| 12 | `cycle-0012` | 2 | 807 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 13 | `cycle-0013` | 2 | 807 | `source_resolved_exact_green_pocket_note` | critical | unaudited |
| 14 | `cycle-0014` | 3 | 807 | `source_resolved_exact_green_h025_pocket_note` | critical | unaudited |
| 15 | `cycle-0015` | 2 | 798 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 16 | `cycle-0016` | 4 | 798 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 17 | `cycle-0017` | 6 | 798 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 18 | `cycle-0018` | 7 | 798 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 19 | `cycle-0019` | 8 | 798 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 20 | `cycle-0020` | 9 | 798 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 21 | `cycle-0021` | 9 | 798 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 22 | `cycle-0022` | 10 | 798 | `gauge_vacuum_plaquette_beta6_evaluation_seam_reduction_science_only_note_2026-04-17` | critical | unaudited |
| 23 | `cycle-0023` | 2 | 793 | `axiom_first_reflection_positivity_theorem_note_2026-04-29` | critical | audited_conditional |
| 24 | `cycle-0024` | 2 | 788 | `pmns_active_four_real_source_from_transport_note` | critical | unaudited |
| 25 | `cycle-0025` | 2 | 784 | `lensing_finite_path_explanation_note` | critical | unaudited |

Full queue lives in `data/audit_queue.json`.
