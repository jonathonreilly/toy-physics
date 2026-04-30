# Audit Queue

**Generated:** 2026-04-30T22:06:22.283810+00:00
**Total pending:** 799
**Ready (all deps already at a stable tier):** 416

By criticality:
- `critical`: 1
- `high`: 222
- `medium`: 289
- `leaf`: 287

Auditor (Codex GPT-5.5 by default) should pull from the top of this list. Critical claims require cross-confirmation by a second independent clean-room auditor before `audited_clean` lands.

## Top 50

| # | claim_id | criticality | desc | score | ready | indep required | runner |
|---:|---|---|---:|---:|:---:|---|---|
| 1 | `publication.ci3_z3.publication_matrix` | critical | 32 | 12.54 |  | fresh_context_or_stronger_with_cross_confirmation | - |
| 2 | `universal_qg_canonical_refinement_net_note` | high | 35 | 9.17 | Y | fresh_context_or_stronger | - |
| 3 | `universal_qg_uv_finite_partition_note` | high | 35 | 8.67 | Y | fresh_context_or_stronger | - |
| 4 | `bell_inequality_derived_note` | high | 35 | 8.17 | Y | fresh_context_or_stronger | `scripts/frontier_bell_inequality.py` |
| 5 | `broad_gravity_derivation_note` | high | 35 | 8.17 | Y | fresh_context_or_stronger | - |
| 6 | `ckm_moduli_only_unitarity_jarlskog_area_certificate_theorem_note_2026-04-26` | high | 34 | 10.13 | Y | fresh_context_or_stronger | `scripts/frontier_ckm_moduli_only_unitarity_jarlskog_area_certificate.py` |
| 7 | `koide_q_so2_phase_erasure_support_note_2026-04-25` | high | 34 | 9.63 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_so2_phase_erasure_support.py` |
| 8 | `sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26` | high | 34 | 9.63 | Y | fresh_context_or_stronger | `scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py` |
| 9 | `newton_law_derived_note` | high | 34 | 9.13 | Y | fresh_context_or_stronger | `scripts/frontier_distance_law_definitive.py` |
| 10 | `poisson_exhaustive_uniqueness_note` | high | 34 | 9.13 | Y | fresh_context_or_stronger | `scripts/frontier_poisson_exhaustive_uniqueness.py` |
| 11 | `self_consistency_forces_poisson_note` | high | 34 | 9.13 | Y | fresh_context_or_stronger | `scripts/frontier_self_consistent_field_equation.py` |
| 12 | `single_axiom_information_note` | high | 34 | 9.13 | Y | fresh_context_or_stronger | `scripts/frontier_single_axiom_information.py` |
| 13 | `dm_pmns_ordered_chain_graded_current_delta_closure_theorem_note_2026-04-21` | high | 34 | 8.63 | Y | fresh_context_or_stronger | `scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py` |
| 14 | `universal_gr_lorentzian_signature_extension_note` | high | 34 | 8.63 | Y | fresh_context_or_stronger | - |
| 15 | `dm_split2_interval_certified_dominance_closure_theorem_note_2026-04-21` | high | 34 | 8.13 | Y | fresh_context_or_stronger | `scripts/frontier_dm_split2_interval_certified_dominance_closure_2026_04_21.py` |
| 16 | `grav_decoherence_derived_note` | high | 34 | 7.63 | Y | fresh_context_or_stronger | `scripts/frontier_grav_decoherence_derived.py` |
| 17 | `monopole_derived_note` | high | 34 | 7.63 | Y | fresh_context_or_stronger | `scripts/frontier_monopole_derived.py` |
| 18 | `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25` | high | 33 | 9.59 | Y | fresh_context_or_stronger | `scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py` |
| 19 | `universal_qg_inverse_limit_closure_note` | high | 33 | 8.09 | Y | fresh_context_or_stronger | - |
| 20 | `universal_qg_pl_field_interface_note` | high | 33 | 8.09 | Y | fresh_context_or_stronger | - |
| 21 | `universal_qg_pl_sobolev_interface_note` | high | 33 | 8.09 | Y | fresh_context_or_stronger | - |
| 22 | `universal_qg_pl_weak_form_note` | high | 33 | 8.09 | Y | fresh_context_or_stronger | - |
| 23 | `koide_q_second_order_support_batch_note_2026-04-22` | high | 33 | 7.59 | Y | fresh_context_or_stronger | `scripts/frontier_koide_q_bridge_single_primitive.py` |
| 24 | `koide_reviewer_stress_test_note_2026-04-21` | high | 33 | 7.59 | Y | fresh_context_or_stronger | `scripts/frontier_koide_reviewer_stress_test.py` |
| 25 | `primordial_spectrum_note` | high | 33 | 7.59 | Y | fresh_context_or_stronger | `scripts/frontier_primordial_spectrum.py` |
| 26 | `universal_qg_canonical_smooth_geometric_action_note` | high | 33 | 7.59 | Y | fresh_context_or_stronger | - |
| 27 | `hubble_lane5_two_gate_dependency_firewall_note_2026-04-27` | high | 16 | 6.59 | Y | fresh_context_or_stronger | `scripts/frontier_hubble_lane5_two_gate_dependency_firewall.py` |
| 28 | `atomic_rydberg_dependency_firewall_note_2026-04-27` | high | 15 | 6.50 | Y | fresh_context_or_stronger | `scripts/frontier_atomic_rydberg_dependency_firewall.py` |
| 29 | `su2_witten_z2_anomaly_theorem_note_2026-04-24` | high | 249 | 14.97 |  | fresh_context_or_stronger | - |
| 30 | `su3_cubic_anomaly_cancellation_theorem_note_2026-04-24` | high | 249 | 14.47 |  | fresh_context_or_stronger | - |
| 31 | `lh_anomaly_trace_catalog_theorem_note_2026-04-25` | high | 248 | 12.96 |  | fresh_context_or_stronger | `scripts/frontier_lh_anomaly_trace_catalog.py` |
| 32 | `yt_zero_import_authority_note` | high | 205 | 11.19 |  | fresh_context_or_stronger | `scripts/frontier_yt_ward_identity_derivation.py` |
| 33 | `neutrino_majorana_native_gaussian_no_go_note` | high | 180 | 10.00 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_native_gaussian_nogo.py` |
| 34 | `neutrino_majorana_finite_normal_grammar_no_go_note` | high | 179 | 10.49 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_finite_normal_grammar_nogo.py` |
| 35 | `neutrino_majorana_pfaffian_extension_note` | high | 178 | 9.98 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_extension.py` |
| 36 | `neutrino_majorana_pfaffian_axiom_boundary_note` | high | 177 | 7.98 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_axiom_boundary.py` |
| 37 | `neutrino_majorana_pfaffian_no_forcing_theorem_note` | high | 176 | 9.97 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_pfaffian_no_forcing_theorem.py` |
| 38 | `neutrino_majorana_current_atlas_nonrealization_note` | high | 176 | 8.97 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_current_atlas_nonrealization.py` |
| 39 | `neutrino_majorana_charge_two_primitive_reduction_note` | high | 175 | 8.96 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` |
| 40 | `neutrino_majorana_unique_source_slot_note` | high | 174 | 10.95 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_unique_source_slot.py` |
| 41 | `neutrino_majorana_phase_removal_note` | high | 173 | 9.94 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_phase_removal.py` |
| 42 | `neutrino_majorana_canonical_local_block_note` | high | 169 | 9.91 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_canonical_local_block.py` |
| 43 | `neutrino_majorana_local_pfaffian_uniqueness_note` | high | 166 | 9.38 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_local_pfaffian_uniqueness.py` |
| 44 | `neutrino_majorana_nambu_source_principle_note` | high | 165 | 10.38 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_nambu_source_principle.py` |
| 45 | `neutrino_majorana_source_ray_theorem_note` | high | 164 | 11.87 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_source_ray_theorem.py` |
| 46 | `neutrino_majorana_z3_nonactivation_theorem_note` | high | 162 | 10.85 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_z3_nonactivation_theorem.py` |
| 47 | `neutrino_majorana_nambu_radial_observable_note` | high | 161 | 8.84 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_nambu_radial_observable.py` |
| 48 | `neutrino_majorana_nambu_quadratic_comparator_note` | high | 160 | 8.33 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_nambu_quadratic_comparator.py` |
| 49 | `neutrino_majorana_background_normalization_theorem_note` | high | 159 | 9.82 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_background_normalization_theorem.py` |
| 50 | `neutrino_majorana_staircase_blindness_theorem_note` | high | 159 | 9.82 |  | fresh_context_or_stronger | `scripts/frontier_neutrino_majorana_staircase_blindness_theorem.py` |

Full queue lives in `data/audit_queue.json`.
