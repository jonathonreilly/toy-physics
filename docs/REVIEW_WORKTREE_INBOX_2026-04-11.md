# Review Worktree Inbox

**Date:** 2026-04-11  
**Purpose:** consolidate the non-`main` science surface into one review branch so
promotion decisions happen in one place instead of across many frontier tips.

This inbox is intentionally strict:

- if something is already on `main`, it should not be finalized here
- if something is here, it is either:
  - a bounded promotion candidate that still needs one last review pass, or
  - a hold item with a specific missing control / redesign step
- bounded candidates are lane-specific evidence only; do not read them as
  full Newton or Einstein closure unless the note explicitly says the missing
  controls are closed

## Already On `main`

These are not review items anymore:

- `STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md`
- `scripts/frontier_staggered_test_mass_companion.py`
- `DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`
- `scripts/distance_law_3d_64_closure.py`
- `WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md`
- `scripts/frontier_test_mass_limit.py`
- `scripts/frontier_perturbative_mass_law.py`
- `scripts/frontier_continuum_limit.py`
- `scripts/frontier_newton_systematic.py`
- `docs/ACTION_UNIQUENESS_AUDIT_2026-04-11.md`
- `scripts/action_uniqueness_investigation.py`
- `docs/NEWTON_DERIVATION_NOTE.md`
- `docs/NEWTON_PERSISTENT_PATTERN_CONTROL_NOTE_2026-04-11.md`
- `docs/IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md`
- `scripts/frontier_irregular_sign_core_packet_gate.py`
- `docs/EMERGENT_PRODUCT_LAW_NOTE.md`
- `docs/EMERGENT_PRODUCT_LAW_AUDIT_2026-04-11.md`
- `scripts/frontier_emergent_product_law.py`
- `docs/ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`
- `docs/ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md`
- `scripts/frontier_architecture_portability_sweep.py`

Status:

- bounded-retained primary-architecture weak-field source-mass companion
- safe reading: source-only static-source companion
- not both-masses closure
- not self-consistent two-body closure
- not standalone distance-law closure
- bounded-retained `64^3` path-sum distance continuation
- safe reading: single-family continuation note for the path-sum distance story
- not full Newton closure
- not both-masses closure
- not architecture portability
- bounded-retained Wilson test-mass / continuum companion
- safe reading: exact source-mass scaling plus same-convention continuum fit
- not both-masses closure
- not action-reaction closure
- not architecture-independent Newton closure
- bounded-family action-uniqueness note
- safe reading: weak-field-linear phase valleys are Newtonian on the tested
  ordered-lattice family
- not a theorem
- not architecture-independent uniqueness
- bounded-retained emergent cross-field product-law companion
- safe reading: field-linearity product scaling on one audited open 3D
  staggered surface
- not full Newton closure
- not architecture-independent product-law closure
- bounded-retained architecture portability companion
- safe reading: source-mass scaling and attractive-sign portability across the
  audited ordered, staggered, Wilson, and 2D irregular control rows
- not architecture-independent full Newton closure

## Bounded Review Candidates

These are on `codex/review-active`, not on `main` yet. They need one more
review pass and claim-boundary check before any promotion.

### Overnight additions captured from `origin/claude/youthful-neumann`

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
- `docs/INDEPENDENT_SPATIAL_METRIC_NOTE.md`
- `scripts/frontier_independent_spatial_metric.py`

Current read:

- gravity+EM 2x2: bounded kinematic coexistence pass on the ray-sum surface;
  mixed residual is zero by linearity of accumulated action
- dispersion running-exponent: bounded classification improvement over the old
  global `R^2` fit; cubic/Wilson read as Schrodinger-type at the tested `h`
- Hawking Bogoliubov quench: bounded Gaussian-state in/out step with clean
  null and thermal-fit regime; not a Hawking claim
- distance law 64 frozen control: bounded diagnostic companion; brackets the
  continuum exponent but does not close the strict frozen/static-source gate
- distance law definitive: strong ordered-cubic/Dirichlet closure candidate,
  but still bounded to that surface until separately retained
- action normalization: reviewer-facing normalization memo; not an axiomatic
  derivation of the coupling coefficient
- beyond lattice QCD: reviewer-facing bounded differentiation memo, not
  standalone retained physics
- diamond NV card: lab-facing proposal card, not an experimental result
- diamond lattice correction: distinct formula relative to smooth GR, but not
  an actionable discriminator at realistic microscopic lattice scales
- Poisson exhaustive uniqueness: strengthened operator-family audit; safe as a
  bounded family result, not a global uniqueness theorem
- independent spatial metric: stronger than the old circular argument, but
  still held because the amplitude prefactor `(1-f)` is prescribed rather than
  independently forced

Promotion rule:

- do not move any of these to `main` without an explicit bounded audit note or
  a hold note that freezes the claim boundary
- not a universal distance-law portability result

### Historical bounded slice captured from `origin/codex/resonance-controls`

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

Current read:

- lensing H=0.25 exact-edge note: bounded historical reference freeze for the
  adjoint-kernel lane, not a new mechanism claim
- spectral/CDT audit: bounded narrow-positive / bounded-negative audit; useful
  as control-plane context, not a strong retained discovery
- wave direct-`dM` Fam3 notes: bounded historical control closures for a narrow
  transfer/compression lane, not a current `main` candidate
- wave static matrix-free boundary note: bounded negative / diagnostic lane;
  useful historical hold, not a promotion candidate

Promotion rule:

- do not promote any of this historical slice directly to `main`
- if any of these lanes are reopened, write a fresh bounded audit note on top
  of the imported artifacts rather than promoting the historical note itself

### Narrow capture from `origin/codex/irregular-sign-closure`

- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NOTE_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_closure.py`

Current read:

- strong same-surface shell-packet irregular sign separator on the audited
  irregular families
- valuable predecessor artifact for the later core-packet retention and
  portability analysis
- not a current `main` candidate because the later low-screening and
  portability gates, not this shell-packet surface alone, now define the lane

### Narrow capture from `origin/codex/wilson-temporal-robustness`

- `docs/TWO_BODY_ATTRACTION_FROZEN_SOURCE_NOTE_2026-04-11.md`
- `scripts/frontier_two_body_attraction_frozen_source.py`

Current read:

- bounded frozen-source negative control for the Wilson mutual-attraction lane
- important for the Wilson hold section because it narrows, but does not close,
  the static-vs-dynamic explanation gap

### Narrow capture from `origin/codex/axiom-risk-ledger`

- `docs/AXIOM_RISK_LEDGER.md`

Current read:

- reviewer-facing synthesis note about which axioms are stable, vague, or under
  pressure from the audited results
- useful framing document for manuscript and review response work
- not a retained physics result and not a promotion target for `main`

### Narrow capture from `origin/codex/next-session-tests`

- `scripts/frontier_lorentzian_weakfield_geodesic_refine.py`
- `scripts/frontier_persistent_source_spectrum.py`

Current read:

- future-probe scaffolding for two explicitly open lanes:
  - weak-field Lorentzian geodesic refinement
  - source-consistency spectrum on the retained ordered lattice
- useful to preserve on review as reopening harnesses
- not retained science and not a direct promotion target

### Narrow capture from `origin/codex/archive-claude-distracted-napier-20260411`

- `docs/K_OSCILLATION_PREDICTION_NOTE.md`
- `scripts/k_oscillation_prediction.py`
- `scripts/lensing_beta_sweep_fine.py`

Current read:

- bounded analytical side-note for the lensing `k·H` oscillation story
- useful because it ties one measured oscillation period to an adjacent
  impact-parameter field-phase contrast with no free parameters
- still a lensing interpretation note, not a retained gravity closure result
- the companion `β` sweep is supporting lane diagnostics, not a promotion
  target on its own

### Narrow capture from `origin/codex/local-lorentzian-beamsplitter`

- `scripts/frontier_local_unitary_lorentzian.py`

Current read:

- exploratory local-unitary Lorentzian beam-splitter harness
- useful as a reopening script for local/causal/Born-sign tests on a sparse
  brick-wall unitary
- no retained bounded note currently depends on it
- preserve on review as future-probe scaffolding only

### Narrow capture from `origin/codex/chiral-harness-tests`

- `scripts/frontier_chiral_two_body_superposition.py`

Current read:

- narrow 1D theta-coupled chiral superposition diagnostic
- tests whether the combined two-mass field matches the sum of individual
  centroid shifts on that specific chiral lane
- useful as a bounded nonlinear-diagnostic harness, not a retained physics
  result

### Single-artifact Claude capture batch

Captured from:

- `origin/claude/4d-continuum`
- `origin/claude/adaptive-emergence`
- `origin/claude/assumption-ledger`
- `origin/claude/birth-death`
- `origin/claude/cross-family`
- `origin/claude/emergence-sustain`
- `origin/claude/fixed-position-alpha`
- `origin/claude/geometric-growth`
- `origin/claude/literature`
- `origin/claude/overnight-2`
- `origin/claude/overnight-3`
- `origin/claude/overnight-4`
- `origin/claude/overnight-deep`
- `origin/claude/overnight-science`
- `origin/claude/overnight-verify`
- `origin/claude/slit-growth`

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

Current read:

- this is historical emergence / continuum / overnight probe scaffolding from
  the earlier DAG-growth program
- `ASSUMPTION_DERIVATION_LEDGER` and `LITERATURE_POSITIONING_NOTE` are
  reviewer-facing framing documents, not retained results
- the scripts are valuable to preserve on review because they encode earlier
  search directions, verification harnesses, and stress tests
- none of this batch is a direct `main` promotion target without a fresh bounded
  audit note on the exact reopened surface

### Small overlapping Claude batch

Captured from:

- `origin/claude/continuum-bridge`
- `origin/claude/docs-update`
- `origin/claude/review-fixes`
- `origin/claude/reviewer-summary`
- `origin/claude/predictions`
- `origin/claude/evolving-network`
- `origin/claude/nonlinear-pathsum`

Files:

- `docs/CONTINUUM_BRIDGE_NOTE.md`
- `docs/REVIEWER_SUMMARY.md`
- `docs/PREDICTION_CARD.md`
- `scripts/preferential_gravity_diagnosis.py`
- `scripts/self_regulating_gap_3d.py`
- `scripts/self_regulating_large_n.py`
- `scripts/dynamical_reweight_distance_law.py`
- `scripts/nonlinear_phase_distance.py`

Current read:

- `CONTINUUM_BRIDGE_NOTE`, `REVIEWER_SUMMARY`, and `PREDICTION_CARD` are
  reviewer-facing framing/control-plane documents from the earlier DAG program
- the prediction and emergence scripts are historical diagnostic harnesses for
  preferential-attachment failure, self-regulating gap dynamics, and nonlinear
  distance-law rescue attempts
- preserve on review for provenance and possible reopening, but none of this is
  a direct `main` promotion target without a fresh bounded audit note

### 2026-04-12 migration from `claude/youthful-neumann`

New bounded promotion candidates:

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

Current read:

- nonlinear Born gravity: I3=0 iff attractive, perfect correlation; bounded
  Born-rule nonlinearity probe on the audited surface
- gravitational entanglement: MI=2.3, lattice gauge theory cannot reproduce;
  bounded entanglement discriminator
- wave equation gravity: box(f)=rho recovers grav waves at c=1.05; bounded
  wave-equation probe
- distance law 64 continuation: bounded note documenting the 96^3 continuation
  alongside the definitive runner
- irregular sign low-screening gate: companion to the core-packet gate;
  bounded same-surface low-screening check

New archive-ready items (negative results, retained for reference):

- `docs/WILSON_FROZEN_SOURCE_DISCRIMINATOR_NOTE.md`
- `scripts/frontier_wilson_frozen_source_discriminator.py`
- `docs/EXPERIMENTAL_PREDICTIONS_NOTE.md`
- `scripts/frontier_experimental_predictions.py`

Current read:

- Wilson frozen source discriminator: negative result, lane closed
- experimental predictions: Planck-scale undetectable, lane closed

Full migration audit: `docs/MIGRATION_AUDIT_2026-04-12.md`

### 2026-04-12 batch 2 migration from `claude/youthful-neumann`

New bounded promotion candidates:

- `docs/DIMENSION_SELECTION_NOTE.md`
- `scripts/frontier_dimension_selection.py`
- `docs/BACKGROUND_INDEPENDENCE_NOTE.md`
- `scripts/frontier_background_independence.py`
- `docs/TENSOR_NETWORK_CONNECTION_NOTE.md`
- `scripts/frontier_tensor_network_connection.py`
- `docs/AXIOM_REDUCTION_NOTE.md`
- `docs/GRAVITATIONAL_WAVE_PROBE_NOTE.md`
- `scripts/frontier_grav_wave_post_newtonian.py`
- `docs/POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md` (updated)
- `scripts/frontier_poisson_exhaustive_uniqueness.py` (updated)

Current read:

- dimension selection: d>=3 from self-consistency; bounded to the tested
  operator family
- background independence: 4/4 passes on randomized backgrounds; bounded to
  the audited surface
- tensor network connection: 4/4 passes including holographic entanglement
  scaling; bounded to the tested graph family
- axiom reduction: 2 axioms + 1 integer sufficient for the bounded claim chain;
  reviewer-facing reduction memo
- gravitational wave probe: 3 beyond-Newton effects (speed, quadrupole,
  dissipation); bounded wave-equation extension
- Poisson exhaustive uniqueness: 21 operators scanned, only Poisson gives
  attraction; strengthened operator-family audit (updated version)

New archive-ready items (negative results, retained for reference):

- `docs/HIERARCHY_RATIO_NOTE.md`
- `scripts/frontier_hierarchy_ratio.py`
- `docs/LITERATURE_ANOMALY_SEARCH_NOTE.md`

Current read:

- hierarchy ratio: honest null, no hierarchy emerges at tested scales
- literature anomaly search: no match found in surveyed literature

Explicit hold (not for promotion):

- `docs/INDEPENDENT_SPATIAL_METRIC_NOTE.md` (updated)
- `scripts/frontier_independent_spatial_metric.py` (updated)

Current read:

- independent spatial metric: user says not independent enough; (1-f) amplitude
  prefactor still prescribed rather than forced; remains in hold #0

Reviewer memos and planning docs:

- `docs/DIAMOND_NV_EXPERIMENT_CARD.md` (updated)
- `docs/NATURE_SCIENCE_BACKLOG.md`

Current read:

- diamond NV card: updated lab protocol, not science
- nature/science backlog: internal planning document, not science

## Review Inventory

Everything left in this review worktree is now on hold.

### 1. Everything Left Is On Hold

Everything else in this review worktree is held pending a specific missing
control or redesign step.

#### Overnight Claude bundle (remaining holds only)

Files:

- `docs/OVERNIGHT_CLAUDE_AUDIT_2026-04-12.md`
- `docs/EMERGENT_GR_SIGNATURES_NOTE.md`
- `docs/ELECTROMAGNETISM_PROBE_NOTE.md`
- `docs/EM_GRAVITY_COEXISTENCE_CONTROL_NOTE_2026-04-12.md`
- `docs/SPATIAL_METRIC_DERIVATION_NOTE.md`
- `docs/SECOND_QUANTIZED_PROTOTYPE_NOTE.md`
- `docs/HOLOGRAPHIC_ENTROPY_NOTE.md`
- `docs/HAWKING_ANALOG_NOTE.md`
- `docs/DIMENSION_EMERGENCE_NOTE.md`
- `docs/COSMOLOGICAL_EXPANSION_NOTE.md`
- `docs/LATTICE_GAUGE_DISTINCTION_NOTE.md`
- `docs/SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
- `scripts/frontier_emergent_gr_signatures.py`
- `scripts/frontier_electromagnetism_probe.py`
- `scripts/frontier_spatial_metric_derivation.py`
- `scripts/frontier_second_quantized_prototype.py`
- `scripts/frontier_holographic_entropy.py`
- `scripts/frontier_hawking_analog.py`
- `scripts/frontier_dimension_emergence.py`
- `scripts/frontier_cosmological_expansion.py`
- `scripts/frontier_dispersion_relation.py`
- `scripts/frontier_self_consistent_field_equation.py`

Why held:

- the overnight branch contains real work, but the safe interpretation is
  narrower than the overnight storyline
- some bounded candidates have now been split out above; what remains in this
  bundle is still hold-only
- the latest Poisson/self-consistency, spatial-metric, and lattice-gauge notes
  also remain review-only after audit

#### A. Wilson mutual-attraction side lane

Source branches:

- `origin/frontier/spot-checks`
- `origin/claude/sleepy-cerf`
- `origin/codex/wilson-temporal-robustness`
- `origin/codex/wilson-temporal-window-lane`

Files:

- `docs/TWO_BODY_ATTRACTION_RETAINED_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_TEMPORAL_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/WILSON_SIDE_LANE_PROMOTION_REVIEW_2026-04-11.md`
- `docs/WILSON_BOTH_MASSES_ACCEL_NOTE_2026-04-11.md`
- `docs/WILSON_CAUSAL_DISCRIMINATOR_NOTE_2026-04-11.md`
- `scripts/frontier_two_body_attraction.py`
- `scripts/frontier_two_body_attraction_robustness.py`
- `scripts/frontier_two_body_attraction_temporal_robustness.py`
- `scripts/frontier_wilson_both_masses_accel.py`
- `scripts/frontier_wilson_both_masses_local_balance.py`
- `scripts/frontier_wilson_causal_discriminator.py`

Current verdict:

- hold for now

Blocker:

- frozen/static-source control has now been run and does **not** close the
  promotion bar on the same open 3D Wilson surface

Current bounded temporal read:

- early/mid windows survive on the audited `45`-configuration surface
- retained windows:
  - `w02_10`
  - `w05_13`
  - `w08_16`
- later windows lose cleanliness or sign stability and do not support a
  retained global fit
- the frozen/static-source control has now been run on the same Wilson surface
  and it still does **not** clear the promotion bar
- the lagged source-refresh discriminator is also too adiabatic to isolate
  causal timing on this surface

Required next experiment:

- no promotion yet; the missing discriminator remains causal, not temporal

Promotion rule:

- do not move this to `main` unless the new control shows dynamic shared
  backreaction matters beyond a frozen-field explanation or a lagged-refresh
  explanation

#### B. Exact two-particle product law

Source branches:

- `origin/claude/youthful-neumann`
- `origin/codex/resonance-controls`

Files:

- `docs/EXACT_TWO_PARTICLE_PRODUCT_LAW_FRONTIER_NOTE_2026-04-11.md`
- `scripts/exact_two_particle_product_law.py`

Why held:

- the Hamiltonian ansatz already bakes in the bilinear `s1*s2` factor
- exact diagonalization confirms response to that ansatz, not emergent product
  law
- toy 1D open-boundary model, not the retained primary architecture

Required next experiment:

- move the bilinear factor out of the ansatz
- add frozen/static-source control
- replay on the primary staggered/open-cubic surface

#### C. Irregular transport / portability beyond the bounded core-packet gate

Source branches:

- `origin/codex/irregular-sign-closure`
- `origin/codex/resonance-controls`

Files:

- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NEXT_STEPS_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_REINFORCEMENT_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_OBSERVABLE_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_SIZE_PORTABILITY_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_THIRD_FAMILY_NOTE_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_reinforcement.py`
- `scripts/frontier_irregular_endogenous_sign_observable.py`
- `scripts/frontier_irregular_endogenous_sign_size_portability.py`
- `scripts/frontier_irregular_endogenous_sign_third_family.py`

Why held:

- the bounded core-packet same-surface separator is now retained on `main`
- what remains open is portability beyond that surface
- the low-screening transport readout still fails on `cut2`
- the third packet family still does not close the lane
- the size-portability sweep still fails to make the sign separator portable
  across graph growth

Required next experiment:

- if reopened, do not rerun the retained core-packet gate
- switch to a portability-grade transport or invariant observable on the same
  irregular surface, not another packet-family sweep

#### D. Staggered two-body closure family

Source branches:

- `origin/frontier/spot-checks`
- `origin/claude/sleepy-cerf`

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
- detector-side transfer has now been tried and is still negative on the
  audited open-cubic surface
- the true mid-plane link-current readout has now been tried and is still
  negative on the audited open-cubic surface
- the packet-local momentum-flux / impulse readout has now been tried and is
  still negative on the audited open-cubic surface
- the x-directed shell-flux refinement fixes the sign gate, but the impulse
  remains non-convergent and does not produce a retained trajectory law

Required next experiment:

- stop trying more centroid variants
- if the lane is reopened, it needs a genuinely different conserved-current
  formulation or a different graph geometry, not another packet cut

## Claude Instructions

If Claude continues from this review worktree, give these instructions:

1. Treat this worktree as the only non-`main` consolidation point.
2. Do not create new frontier branches until each inbox item here is marked
   `promote` or `hold`.
3. Promote only bounded notes with explicit limits and runner pairings.
4. For hold items, add only the minimal next-step control note or runner needed
   to decide them.
5. Do not restate Newton closure, Einstein-equation, or both-masses closure
   unless the missing controls above are actually closed.

## 2026-04-12 Bounded Promotion to Main

The following 15 bounded note+runner pairs were promoted to `main` on
2026-04-12. They are no longer review candidates on this branch.

Promoted items:

1. `frontier_distance_law_definitive.py` + `DISTANCE_LAW_DEFINITIVE_NOTE.md`
2. `frontier_self_consistent_field_equation.py` + `SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
3. `frontier_action_normalization.py` + `ACTION_NORMALIZATION_NOTE.md`
4. `frontier_nonlinear_born_gravity.py` + `NONLINEAR_BORN_GRAVITY_NOTE.md`
5. `frontier_gravitational_entanglement.py` + `GRAVITATIONAL_ENTANGLEMENT_NOTE.md`
6. `frontier_wave_equation_gravity.py` + `WAVE_EQUATION_GRAVITY_NOTE.md`
7. `frontier_beyond_lattice_qcd.py` + `BEYOND_LATTICE_QCD_NOTE.md`
8. `em_gravity_coexistence_2x2.py` + `EM_GRAVITY_COEXISTENCE_2X2_NOTE.md`
9. `frontier_poisson_exhaustive_uniqueness.py` + `POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md`
10. `frontier_dimension_selection.py` + `DIMENSION_SELECTION_NOTE.md`
11. `frontier_bound_state_selection.py` + `BOUND_STATE_SELECTION_NOTE.md`
12. `frontier_background_independence.py` + `BACKGROUND_INDEPENDENCE_NOTE.md`
13. `frontier_tensor_network_connection.py` + `TENSOR_NETWORK_CONNECTION_NOTE.md`
14. `AXIOM_REDUCTION_NOTE.md` (memo only, no runner)
15. `frontier_grav_wave_post_newtonian.py` + `GRAVITATIONAL_WAVE_PROBE_NOTE.md`

All promoted as bounded claims. No full Newton closure, unconditional
spatial-metric derivation, or global Poisson uniqueness restated.

Items NOT promoted (remain on hold):
- spatial metric derivation (user hold)
- GR signatures (consistency check, spatial metric gate not closed)
- electromagnetism probe (staggered eps issue)
- second quantized / holographic / Hawking (Paper 2)
- dimension emergence / cosmology (bounded proxy)
- independent spatial metric (user hold)
- hierarchy ratio / literature search / dispersion (archive)

## Bottom Line

After this consolidation:

- `main` carries the retained baseline plus 15 newly promoted bounded probes
- this review worktree carries only explicit holds from the non-`main` science
  surface
- no important current frontier item should exist only on a deleted local path
