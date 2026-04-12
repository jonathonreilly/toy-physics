# Remaining Non-Main Holds

**Date:** 2026-04-11  
**Scope:** review-worktree items that are still not safe for `main`

This is the consolidated inventory for follow-through. It names the missing
control for each held lane.

## Already on `main`

These are not part of the hold list:

- `ACTION_UNIQUENESS_AUDIT_2026-04-11.md`
- `scripts/action_uniqueness_investigation.py`
- `IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md`
- `scripts/frontier_irregular_sign_core_packet_gate.py`
- `STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md`
- `DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`
- `WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md`
- `NEWTON_DERIVATION_NOTE.md`
- `NEWTON_PERSISTENT_PATTERN_CONTROL_NOTE_2026-04-11.md`
- `EMERGENT_PRODUCT_LAW_NOTE.md`
- `EMERGENT_PRODUCT_LAW_AUDIT_2026-04-11.md`
- `scripts/frontier_emergent_product_law.py`
- `ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`
- `ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md`
- `scripts/frontier_architecture_portability_sweep.py`

## On Review, Not Yet Held Or Retained

These artifacts have been captured onto `codex/review-active` as bounded review
candidates. They are not on `main`, but they are no longer part of the generic
overnight hold bundle.

- `docs/EM_GRAVITY_COEXISTENCE_2X2_NOTE.md`
- `scripts/em_gravity_coexistence_2x2.py`
- `docs/DISPERSION_RUNNING_EXPONENT_NOTE.md`
- `scripts/frontier_dispersion_running_exponent.py`
- `docs/HAWKING_BOGOLIUBOV_QUENCH_NOTE.md`
- `scripts/frontier_hawking_bogoliubov_quench.py`
- `docs/DISTANCE_LAW_64_FROZEN_CONTROL_NOTE.md`
- `scripts/frontier_distance_law_64_frozen_control.py`
- `docs/DISTANCE_LAW_DEFINITIVE_NOTE.md`
- `scripts/frontier_distance_law_definitive.py`
- `docs/ACTION_NORMALIZATION_NOTE.md`
- `scripts/frontier_action_normalization.py`
- `docs/BEYOND_LATTICE_QCD_NOTE.md`
- `scripts/frontier_beyond_lattice_qcd.py`
- `docs/DIAMOND_NV_EXPERIMENT_CARD.md`
- `docs/DIAMOND_NV_LATTICE_CORRECTION_NOTE.md`
- `scripts/frontier_diamond_nv_lattice_correction.py`
- `docs/POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md`
- `scripts/frontier_poisson_exhaustive_uniqueness.py`

### 2026-04-12 migration additions (bounded promotion candidates)

- `docs/NONLINEAR_BORN_GRAVITY_NOTE.md`
- `scripts/frontier_nonlinear_born_gravity.py`
- `docs/GRAVITATIONAL_ENTANGLEMENT_NOTE.md`
- `scripts/frontier_gravitational_entanglement.py`
- `docs/WAVE_EQUATION_GRAVITY_NOTE.md`
- `scripts/frontier_wave_equation_gravity.py`
- `docs/DISTANCE_LAW_64_BOUNDED_CONTINUATION_NOTE.md`
- `scripts/continuum_convergence_h0625.py`
- `docs/IRREGULAR_SIGN_LOW_SCREENING_GATE_NOTE.md`
- `scripts/frontier_irregular_sign_low_screening_gate.py`

### 2026-04-12 migration additions (archive-ready, not for promotion)

- `docs/WILSON_FROZEN_SOURCE_DISCRIMINATOR_NOTE.md`
- `scripts/frontier_wilson_frozen_source_discriminator.py`
- `docs/EXPERIMENTAL_PREDICTIONS_NOTE.md`
- `scripts/frontier_experimental_predictions.py`
- `docs/DIAMOND_NV_LATTICE_CORRECTION_NOTE.md` (reclassified: archive-ready)
- `docs/DIAMOND_NV_EXPERIMENT_CARD.md` (reviewer memo, not science)
- `docs/LATTICE_GAUGE_DISTINCTION_NOTE.md` (reviewer memo, not science)

### 2026-04-12 batch 2 migration additions (bounded promotion candidates)

- `docs/DIMENSION_SELECTION_NOTE.md`
- `scripts/frontier_dimension_selection.py`
- `docs/BACKGROUND_INDEPENDENCE_NOTE.md`
- `scripts/frontier_background_independence.py`
- `docs/TENSOR_NETWORK_CONNECTION_NOTE.md`
- `scripts/frontier_tensor_network_connection.py`
- `docs/AXIOM_REDUCTION_NOTE.md`
- `docs/GRAVITATIONAL_WAVE_PROBE_NOTE.md`
- `scripts/frontier_grav_wave_post_newtonian.py`

### 2026-04-12 batch 2 migration additions (archive-ready, not for promotion)

- `docs/HIERARCHY_RATIO_NOTE.md`
- `scripts/frontier_hierarchy_ratio.py`
- `docs/LITERATURE_ANOMALY_SEARCH_NOTE.md`

### 2026-04-12 batch 2 migration additions (reviewer memos / planning)

- `docs/NATURE_SCIENCE_BACKLOG.md`

## Holds

### 0. Overnight Claude audit bundle

Files:

- `docs/OVERNIGHT_CLAUDE_AUDIT_2026-04-12.md`
- `docs/EMERGENT_GR_SIGNATURES_NOTE.md`
- `scripts/frontier_emergent_gr_signatures.py`
- `docs/ELECTROMAGNETISM_PROBE_NOTE.md`
- `scripts/frontier_electromagnetism_probe.py`
- `docs/EM_GRAVITY_COEXISTENCE_CONTROL_NOTE_2026-04-12.md`
- `docs/SPATIAL_METRIC_DERIVATION_NOTE.md`
- `scripts/frontier_spatial_metric_derivation.py`
- `docs/INDEPENDENT_SPATIAL_METRIC_NOTE.md`
- `scripts/frontier_independent_spatial_metric.py`
- `docs/SECOND_QUANTIZED_PROTOTYPE_NOTE.md`
- `scripts/frontier_second_quantized_prototype.py`
- `docs/HOLOGRAPHIC_ENTROPY_NOTE.md`
- `scripts/frontier_holographic_entropy.py`
- `docs/HAWKING_ANALOG_NOTE.md`
- `scripts/frontier_hawking_analog.py`
- `docs/DIMENSION_EMERGENCE_NOTE.md`
- `scripts/frontier_dimension_emergence.py`
- `docs/COSMOLOGICAL_EXPANSION_NOTE.md`
- `scripts/frontier_cosmological_expansion.py`
- `scripts/frontier_dispersion_relation.py`
- `docs/LATTICE_GAUGE_DISTINCTION_NOTE.md`
- `docs/SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
- `scripts/frontier_self_consistent_field_equation.py`

Why held:

- the overnight branch contains useful new artifacts, but none of them crosses
  the current `main` retention bar without substantial narrowing
- four bounded candidates from that branch have been split out above onto the
  active review surface; what remains here is hold-only
- GR-signatures and electromagnetism remain consistency checks rather than
  GR/Maxwell derivations
- the spatial-metric step remains a weak-field consistency argument rather than
  an unconditional derivation
- the gravity+EM coexistence claim is still blocked pending a factorial control
- second-quantized, holographic, and Hawking results remain prototype-scale
  field-theory probes
- dimension and cosmology remain bounded proxy studies
- the new dispersion runner is still an honest negative with anomalous scaling
- the old Poisson-preference note remains a hold artifact; the newer exhaustive
  audit is now tracked above as a separate bounded review candidate
- the independent-spatial-metric note improves the old circularity problem but
  still does not independently force the `(1-f)` amplitude prefactor

Next control:

- use the lane-specific blockers in `OVERNIGHT_CLAUDE_AUDIT_2026-04-12.md`
- do not promote any of these files to `main` without a new bounded audit note

### 0a. Historical resonance-controls slice

Files:

- `docs/LENSING_H025_EXACT_EDGE_REFERENCE_NOTE.md`
- `scripts/lensing_adjoint_kernel_reduced_model.py`
- `scripts/infinite_lattice_green_kernel.py`
- `docs/SPECTRAL_DIMENSION_CDT_AUDIT_2026-04-11.md`
- `scripts/frontier_spectral_on_lattice_fluxnorm.py`
- `scripts/frontier_geometric_baseline_control.py`
- `scripts/frontier_phase_strip_control.py`
- `docs/WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_THREE_FAMILY_TRANSFER_NOTE.md`
- `docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`
- `docs/WAVE_STATIC_MATRIXFREE_MOVING_SOURCE_FIXED_BEAM_BOUNDARY_NOTE.md`
- `scripts/wave_static_direct_probe.py`

Why held:

- this is historical bounded lane material imported from
  `origin/codex/resonance-controls`
- the notes are useful as control/reference freezes and negative diagnostics
- none of them currently clears the `main` retention bar
- the honest value is preserving the lane state in the single review branch,
  not promoting the historical artifacts themselves

Next control:

- no direct promotion
- if the lensing, spectral/CDT, or wave direct-`dM` lanes are reopened, write a
  fresh bounded audit note on the exact reopened surface instead of promoting
  these historical notes as-is

### 0b. Lensing / local-unitary / chiral exploratory side artifacts

Files:

- `docs/K_OSCILLATION_PREDICTION_NOTE.md`
- `scripts/k_oscillation_prediction.py`
- `scripts/lensing_beta_sweep_fine.py`
- `scripts/frontier_local_unitary_lorentzian.py`
- `scripts/frontier_chiral_two_body_superposition.py`
- `scripts/frontier_lorentzian_k8_card.py`

Why held:

- these are useful analytical or exploratory side-lane artifacts preserved from
  `origin/codex/archive-claude-distracted-napier-20260411`,
  `origin/codex/local-lorentzian-beamsplitter`, and
  `origin/codex/chiral-harness-tests`
- the `k`-oscillation note is a bounded lensing interpretation, not a retained
  gravity closure result
- the local-unitary Lorentzian and chiral two-body scripts are reopening
  harnesses / diagnostics only, with no audited bounded note establishing a
  `main` candidate
- the `k=8` Lorentzian card is a historical adjacent-window script, not a
  bounded note+runner pair and not a retained closure artifact

Next control:

- do not promote directly
- if any of these side lanes are reopened, write a fresh bounded audit note on
  the exact reopened surface before considering promotion

### 0c. Historical emergence / continuum / overnight Claude scaffolding

Files:

- `docs/ASSUMPTION_DERIVATION_LEDGER.md`
- `docs/LITERATURE_POSITIONING_NOTE.md`
- `scripts/four_d_continuum_gap_sweep.py`
- `scripts/adaptive_quantile_emergence.py`
- `scripts/birth_death_emergence.py`
- `scripts/cross_family_robustness.py`
- `scripts/emergence_sustain_and_4d.py`
- `scripts/fixed_position_alpha.py`
- `scripts/geometric_growth_emergence.py`
- `scripts/overnight_batch.py`
- `scripts/overnight_batch_2.py`
- `scripts/overnight_batch_3.py`
- `scripts/overnight_batch_4.py`
- `scripts/overnight_deep_batch.py`
- `scripts/overnight_verification.py`
- `scripts/slit_guided_3d_growth.py`

Why held:

- this batch preserves historical DAG-growth, emergence, and continuum search
  harnesses from small `claude/*` branches
- the two docs are framing/context notes, not retained physics results
- the scripts are reopening scaffolds and verification probes, not audited
  bounded results on the current retained science surface

Next control:

- no direct promotion
- if any emergence/continuum lane is reopened, promote only from a fresh
  bounded audit note written on the exact rerun surface

### 0d. Historical reviewer / prediction / nonlinear-rescue Claude batch

Files:

- `docs/CONTINUUM_BRIDGE_NOTE.md`
- `docs/REVIEWER_SUMMARY.md`
- `docs/PREDICTION_CARD.md`
- `scripts/preferential_gravity_diagnosis.py`
- `scripts/self_regulating_gap_3d.py`
- `scripts/self_regulating_large_n.py`
- `scripts/dynamical_reweight_distance_law.py`
- `scripts/nonlinear_phase_distance.py`

Why held:

- this batch preserves reviewer-facing summaries and historical diagnostics from
  the earlier DAG program
- the docs are framing/control-plane artifacts, not retained results on the
  current mainline science surface
- the scripts are useful reopening harnesses for preferential-attachment,
  self-regulating-gap, and nonlinear-rescue questions, but they are not bounded
  promotion candidates as-is

Next control:

- no direct promotion
- if any of these lanes are reopened, require a fresh bounded audit note on the
  exact rerun surface before considering `main`

### 0e. Historical Claude medium-branch notebooks

Files:

- `.claude/science/analyses/*`
- `.claude/science/derivations/*`
- `.claude/science/write-ups/*`
- `docs/SESSION_SUMMARY_2026-04-01_DIMENSIONAL.md`
- `docs/SYNTHESIS_NOTE_3D.md`
- `docs/MOONSHOT_HONEST_REVIEW_2026-04-09.md`
- `docs/MOONSHOT_TOP20_FRONTIERS.md`
- `docs/LENSING_K_SWEEP_NOTE.md`
- `docs/FINE_H_FAMILY_UNIVERSALITY_NOTE.md`
- historical script suites from `origin/claude/gracious-pasteur` and
  `origin/claude/distracted-napier`

Why held:

- these branches are historical notebook / frontier collections already
  preserved on review for provenance
- the docs and scripts contain useful lane history, theorem sketches, and old
  probe harnesses, but they are not bounded promotion artifacts on their
  historical wording

Next control:

- no direct promotion
- if a lane from these collections is reopened, write a fresh bounded audit
  note on the exact rerun surface before considering `main`

### 0f. Historical Claude backreaction / source-aware batch

Files:

- `docs/SOURCE_AWARE_MECHANISM_NOTE.md`
- `scripts/backreaction_cross_family.py`
- `scripts/backreaction_stability_map.py`
- `scripts/dense_prune_gravity_repair.py`
- `scripts/directional_b_overlap_onset_continuum_crowding_bridge.py`
- `scripts/directional_b_overlap_onset_midlayer_sampling_holdout.py`
- `scripts/directional_b_overlap_onset_occupancy_load_bridge.py`

Why held:

- this batch preserves historical source-aware / backreaction / directional-`b`
  diagnostics from `origin/claude/backreaction-frontier`
- the mechanism note is historically useful but still written as a bounded
  family-sensitive explanation, not a retained mainline result
- the scripts are reopening harnesses and diagnostic cards, not direct bounded
  promotion candidates on the current retained science surface

Next control:

- no direct promotion
- if the backreaction or source-aware lane is reopened, require a fresh bounded
  audit note on the exact rerun surface before considering `main`

### 1. Wilson mutual-attraction side lane

Files:

- `docs/TWO_BODY_ATTRACTION_RETAINED_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_FROZEN_SOURCE_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_TEMPORAL_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/WILSON_SIDE_LANE_PROMOTION_REVIEW_2026-04-11.md`
- `docs/WILSON_BOTH_MASSES_ACCEL_NOTE_2026-04-11.md`
- `docs/WILSON_CAUSAL_DISCRIMINATOR_NOTE_2026-04-11.md`
- `scripts/frontier_two_body_attraction.py`
- `scripts/frontier_two_body_attraction_frozen_source.py`
- `scripts/frontier_two_body_attraction_robustness.py`
- `scripts/frontier_two_body_attraction_temporal_robustness.py`
- `scripts/frontier_wilson_both_masses_accel.py`
- `scripts/frontier_wilson_both_masses_local_balance.py`
- `scripts/frontier_wilson_causal_discriminator.py`

Why held:

- the open-Wilson mutual channel is real
- the early/mid-window near-inverse-square law is real
- the frozen/static-source control has now been run and still does not
  separate dynamic shared backreaction cleanly from a static explanation
- the lagged source-refresh discriminator has now been run and the response is
  still too adiabatic to isolate causal timing cleanly on this surface
- full Newton closure is still open

Next control:

- same open 3D Wilson surface
- if reopened, move to an intervention-style observable rather than another
  source-refresh lag
- do not promote until the causal discriminator is clean

### 2. Exact two-particle product law

Files:

- `docs/EXACT_TWO_PARTICLE_PRODUCT_LAW_FRONTIER_NOTE_2026-04-11.md`
- `scripts/exact_two_particle_product_law.py`

Why held:

- the bilinear factor is built into the Hamiltonian ansatz
- exact diagonalization confirms the imposed kernel, not emergent product law
- the model is a 1D open-boundary toy, not the primary staggered surface

Next control:

- move the bilinear factor out of the ansatz
- add a frozen/static-source control
- replay on the primary staggered/open-cubic surface

### 3. Irregular transport / portability beyond the bounded core-packet gate

Files:

- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NOTE_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_closure.py`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NEXT_STEPS_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_REINFORCEMENT_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_SIZE_PORTABILITY_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_OBSERVABLE_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_THIRD_FAMILY_NOTE_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_reinforcement.py`
- `scripts/frontier_irregular_endogenous_sign_observable.py`
- `scripts/frontier_irregular_endogenous_sign_size_portability.py`
- `scripts/frontier_irregular_endogenous_sign_third_family.py`

Why held:

- the shell-packet same-surface separator is a real strong frontier result and
  is now preserved on review
- the bounded core-packet same-surface separator is now retained on `main`
- what remains open is portability beyond that surface
- the third packet family still does not close the lane
- the size-portability sweep still fails to make the sign separator portable
  across graph growth
- the new transport observable improves the readout, but `cut2` still fails on
  most of the audited rows, so the lane is not yet portable or transport-closed

Next control:

- if reopened, do not rerun the retained core-packet gate
- use a portability-grade transport or invariant observable on the same
  irregular surface, not another packet-family sweep

### 4. Staggered two-body closure family

Files:

- `docs/STAGGERED_DIRECT_COM_CLOSURE_NOTE_2026-04-11.md`
- `docs/STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_PORTABILITY_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_TRANSPORT_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_LINK_CURRENT_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_MOMENTUM_FLUX_NOTE_2026-04-11.md`
- `docs/STAGGERED_X_FLUX_REFINEMENT_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_NEXT_STEPS_NOTE_2026-04-11.md`
- `scripts/frontier_staggered_direct_com_closure.py`
- `scripts/frontier_staggered_both_masses.py`
- `scripts/frontier_staggered_two_body_portability.py`
- `scripts/frontier_staggered_two_body_transport.py`
- `scripts/frontier_staggered_two_body_link_current.py`
- `scripts/frontier_staggered_two_body_momentum_flux.py`

Why held:

- partner-force is real
- direct-CoM closure still fails
- both-masses closure is still negative / force-led
- detector-side transfer is still negative on the audited open-cubic surface
- the true link-current readout is still negative on the audited open-cubic
  surface
- the packet-local momentum-flux / impulse readout is also still negative on
  the audited open-cubic surface
- the x-directed shell-flux refinement fixes the sign gate, but the impulse
  remains non-convergent and the lane still lacks a retained trajectory law

Next control:

- stop centroid and shell-flux variants
- the current lane has now been tried; only a genuinely different conserved
  current or a different graph geometry would be credible if this family is
  revisited

## 2026-04-12 Migration Update

The following reclassifications were applied during the migration from
`claude/youthful-neumann`:

- Items #12-20 from the task list (emergent_gr_signatures through
  cosmological_expansion) remain in hold #0 with their existing blockers
- Items #7-9 (nonlinear_born_gravity, gravitational_entanglement,
  wave_equation_gravity) were migrated as new bounded promotion candidates
- Items #21-24 (wilson_frozen_source_discriminator, dispersion_relation,
  experimental_predictions, diamond_nv_lattice_correction) were classified
  as archive-ready
- Items #25-26 (LATTICE_GAUGE_DISTINCTION_NOTE, DIAMOND_NV_EXPERIMENT_CARD)
  are reviewer memos, not science artifacts

### 2026-04-12 batch 2 reclassifications

- `INDEPENDENT_SPATIAL_METRIC_NOTE.md` and `frontier_independent_spatial_metric.py`:
  updated versions copied; remains in hold #0 (user says not independent enough;
  (1-f) prefactor prescribed)
- `DIAMOND_NV_EXPERIMENT_CARD.md`: updated version copied; remains reviewer memo
- `POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md` and `frontier_poisson_exhaustive_uniqueness.py`:
  updated versions copied; remains bounded promotion candidate (21 operators)
- Files already on review-active that received updates from youthful-neumann:
  ACTION_NORMALIZATION, BEYOND_LATTICE_QCD, NONLINEAR_BORN_GRAVITY,
  GRAVITATIONAL_ENTANGLEMENT, WAVE_EQUATION_GRAVITY (all latest versions copied)

Full classification: `docs/MIGRATION_AUDIT_2026-04-12.md`

## 2026-04-12 Promotions Completed

The following items were promoted to `main` as bounded note+runner pairs.
They are no longer review candidates here:

- `frontier_distance_law_definitive.py` + `DISTANCE_LAW_DEFINITIVE_NOTE.md`
- `frontier_self_consistent_field_equation.py` + `SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
- `frontier_action_normalization.py` + `ACTION_NORMALIZATION_NOTE.md`
- `frontier_nonlinear_born_gravity.py` + `NONLINEAR_BORN_GRAVITY_NOTE.md`
- `frontier_gravitational_entanglement.py` + `GRAVITATIONAL_ENTANGLEMENT_NOTE.md`
- `frontier_wave_equation_gravity.py` + `WAVE_EQUATION_GRAVITY_NOTE.md`
- `frontier_beyond_lattice_qcd.py` + `BEYOND_LATTICE_QCD_NOTE.md`
- `em_gravity_coexistence_2x2.py` + `EM_GRAVITY_COEXISTENCE_2X2_NOTE.md`
- `frontier_poisson_exhaustive_uniqueness.py` + `POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md`
- `frontier_dimension_selection.py` + `DIMENSION_SELECTION_NOTE.md`
- `frontier_bound_state_selection.py` + `BOUND_STATE_SELECTION_NOTE.md`
- `frontier_background_independence.py` + `BACKGROUND_INDEPENDENCE_NOTE.md`
- `frontier_tensor_network_connection.py` + `TENSOR_NETWORK_CONNECTION_NOTE.md`
- `AXIOM_REDUCTION_NOTE.md` (memo only)
- `frontier_grav_wave_post_newtonian.py` + `GRAVITATIONAL_WAVE_PROBE_NOTE.md`

## Bottom Line

The review worktree now contains explicit holds only. The 15 bounded
promotion candidates have been moved to `main`. Nothing else should be
promoted without the missing control named in its section.
