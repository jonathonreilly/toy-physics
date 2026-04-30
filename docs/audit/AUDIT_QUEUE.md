# Audit Queue

**Generated:** 2026-04-30T22:39:16.003274+00:00
**Total pending:** 782
**Ready (all deps already at a stable tier):** 399

By criticality:
- `critical`: 1
- `high`: 205
- `medium`: 289
- `leaf`: 287

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---:|---:|:---:|---|---|
| 1 | `publication.ci3_z3.publication_matrix` | critical | 32 | 12.54 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 2 | `universal_gr_lorentzian_signature_extension_note` | high | 34 | 8.63 | Y | fresh_context_or_stronger | - |
| 3 | `universal_qg_inverse_limit_closure_note` | high | 33 | 8.09 | Y | fresh_context_or_stronger | - |
| 4 | `universal_qg_pl_field_interface_note` | high | 33 | 8.09 | Y | fresh_context_or_stronger | - |
| 5 | `universal_qg_pl_sobolev_interface_note` | high | 33 | 8.09 | Y | fresh_context_or_stronger | - |
| 6 | `universal_qg_pl_weak_form_note` | high | 33 | 8.09 | Y | fresh_context_or_stronger | - |
| 7 | `koide_reviewer_stress_test_note_2026-04-21` | high | 33 | 7.59 | Y | fresh_context_or_stronger | `scripts/frontier_koide_reviewer_stress_test.py` |
| 8 | `primordial_spectrum_note` | high | 33 | 7.59 | Y | fresh_context_or_stronger | `scripts/frontier_primordial_spectrum.py` |
| 9 | `universal_qg_canonical_smooth_geometric_action_note` | high | 33 | 7.59 | Y | fresh_context_or_stronger | - |
| 10 | `hubble_lane5_two_gate_dependency_firewall_note_2026-04-27` | high | 16 | 6.59 | Y | fresh_context_or_stronger | `scripts/frontier_hubble_lane5_two_gate_dependency_firewall.py` |
| 11 | `atomic_rydberg_dependency_firewall_note_2026-04-27` | high | 15 | 6.50 | Y | fresh_context_or_stronger | `scripts/frontier_atomic_rydberg_dependency_firewall.py` |
| 12 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | high | 249 | 14.97 |  | fresh_context_or_stronger | - |
| 13 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | high | 249 | 14.47 |  | fresh_context_or_stronger | - |
| 14 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | high | 248 | 12.96 |  | fresh_context_or_stronger | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 15 | `yt_zero_import_authority_note` | high | 205 | 11.19 |  | fresh_context_or_stronger | `scripts/frontier_yt_ward_identity_derivation.py` |
| 16 | `neutrino_majorana_native_gaussian_no_go_note` | high | 180 | 10.00 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 17 | `neutrino_majorana_finite_normal_grammar_no_go_note` | high | 179 | 10.49 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 18 | `neutrino_majorana_pfaffian_extension_note` | high | 178 | 9.98 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |
| 19 | `neutrino_majorana_pfaffian_axiom_boundary_note` | high | 177 | 7.98 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py` |
| 20 | `neutrino_majorana_pfaffian_no_forcing_theorem_note` | high | 176 | 9.97 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py` |
| 21 | `neutrino_majorana_current_atlas_nonrealization_note` | high | 176 | 8.97 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py` |
| 22 | `neutrino_majorana_charge_two_primitive_reduction_note` | high | 175 | 8.96 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` |
| 23 | `neutrino_majorana_unique_source_slot_note` | high | 174 | 10.95 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_unique_source_slot.py` |
| 24 | `neutrino_majorana_phase_removal_note` | high | 173 | 9.94 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_phase_removal.py` |
| 25 | `neutrino_majorana_canonical_local_block_note` | high | 169 | 9.91 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_canonical_local_block.py` |
| 26 | `neutrino_majorana_local_pfaffian_uniqueness_note` | high | 166 | 9.38 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_local_pfaffian_uniqueness.py` |
| 27 | `neutrino_majorana_nambu_source_principle_note` | high | 165 | 10.38 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_nambu_source_principle.py` |
| 28 | `neutrino_majorana_source_ray_theorem_note` | high | 164 | 11.87 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_source_ray_theorem.py` |
| 29 | `neutrino_majorana_z3_nonactivation_theorem_note` | high | 162 | 10.85 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_z3_nonactivation_theorem.py` |
| 30 | `neutrino_majorana_nambu_radial_observable_note` | high | 161 | 8.84 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_nambu_radial_observable.py` |
| 31 | `neutrino_majorana_nambu_quadratic_comparator_note` | high | 160 | 8.33 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_nambu_quadratic_comparator.py` |
| 32 | `neutrino_majorana_background_normalization_theorem_note` | high | 159 | 9.82 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_background_normalization_theorem.py` |
| 33 | `neutrino_majorana_staircase_blindness_theorem_note` | high | 159 | 9.82 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_staircase_blindness_theorem.py` |
| 34 | `neutrino_majorana_axis_exchange_fixed_point_note` | high | 157 | 10.30 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_axis_exchange_fixed_point.py` |
| 35 | `neutrino_majorana_self_dual_staircase_lift_obstruction_note` | high | 156 | 9.79 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_self_dual_staircase_lift_obstruction.py` |
| 36 | `yt_boundary_theorem` | high | 153 | 9.77 |  | fresh_context_or_stronger | `scripts/frontier_yt_boundary_consistency.py` |
| 37 | `neutrino_majorana_endpoint_exchange_midpoint_theorem_note` | high | 149 | 9.23 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_endpoint_exchange_midpoint_theorem.py` |
| 38 | `neutrino_majorana_adjacent_singlet_placement_theorem_note` | high | 148 | 10.22 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_adjacent_singlet_placement_theorem.py` |
| 39 | `neutrino_majorana_residual_sharing_split_theorem_note` | high | 145 | 8.69 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_residual_sharing_split_theorem.py` |
| 40 | `dm_neutrino_atmospheric_scale_theorem_note_2026-04-15` | high | 144 | 9.68 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_atmospheric_scale_theorem.py` |
| 41 | `dm_z3_texture_factor_theorem_note_2026-04-15` | high | 144 | 7.68 |  | fresh_context_or_stronger | `scripts/frontier_dm_z3_texture_factor_theorem.py` |
| 42 | `dm_leptogenesis_universal_yukawa_no_go_note_2026-04-15` | high | 143 | 9.17 |  | fresh_context_or_stronger | `scripts/frontier_dm_leptogenesis_universal_yukawa_nogo.py` |
| 43 | `dm_neutrino_ckm_texture_transfer_no_go_note_2026-04-15` | high | 142 | 8.16 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_ckm_texture_transfer_nogo.py` |
| 44 | `dm_neutrino_cp_kernel_deformation_necessity_note_2026-04-15` | high | 141 | 8.15 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_cp_kernel_deformation_necessity.py` |
| 45 | `dm_neutrino_z3_circulant_cp_tool_note_2026-04-15` | high | 140 | 8.64 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_z3_circulant_cp_tool.py` |
| 46 | `dm_neutrino_singlet_doublet_cp_slot_tool_note_2026-04-15` | high | 138 | 11.62 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_singlet_doublet_cp_slot_tool.py` |
| 47 | `dm_neutrino_two_higgs_right_gram_bridge_note_2026-04-15` | high | 132 | 8.55 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_two_higgs_right_gram_bridge.py` |
| 48 | `dm_neutrino_two_higgs_23_symmetric_slot_no_go_note_2026-04-15` | high | 131 | 8.04 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_two_higgs_23_symmetric_slot_nogo.py` |
| 49 | `dm_neutrino_canonical_two_higgs_slot_no_go_note_2026-04-15` | high | 130 | 8.03 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_canonical_two_higgs_slot_nogo.py` |
| 50 | `dm_neutrino_source_surface_m_spectator_theorem_note_2026-04-16` | high | 129 | 10.02 |  | fresh_context_or_stronger | `scripts/frontier_dm_neutrino_source_surface_m_spectator_theorem.py` |

Full queue lives in `data/audit_queue.json`.
