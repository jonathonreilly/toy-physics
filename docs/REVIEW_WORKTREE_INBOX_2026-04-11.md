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

## Review Inventory

### 1. New Bounded Candidates Awaiting Audit

These are now consolidated here from Claude frontier, but are not yet on
`main` and are not yet approved. They need one last audit pass.

#### A. Emergent product-law candidate

Files:

- `docs/EMERGENT_PRODUCT_LAW_NOTE.md`
- `scripts/frontier_emergent_product_law.py`

Current claim:

- on the audited open 3D staggered cross-field Poisson surface, `F ~ M_A^alpha
  M_B^beta` with `alpha ~ 1.015`, `beta ~ 0.986`, `R^2 > 0.99999`
- the bilinear factor is not explicit in the Hamiltonian
- frozen-field control stays near-identical

Audit focus:

- confirm the bounded reading is correct
- keep the claim at “field-linearity emergence on this surface,” not full
  Newton closure
- decide whether it is safe for bounded promotion to `main`

#### B. Architecture portability candidate

Files:

- `docs/ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`
- `scripts/frontier_architecture_portability_sweep.py`

Current claim:

- source-mass exponent `beta ~ 1` and attractive sign survive on four
  architectures:
  - ordered 3D cubic
  - staggered 3D cubic
  - Wilson 3D cubic
  - random geometric

Audit focus:

- confirm the architectures are being compared honestly
- keep it bounded to mass-law/source-scaling portability
- do not let it drift into architecture-independent full Newton closure

### 2. Everything Else Left Is On Hold

Everything else in this review worktree is held pending a specific missing
control or redesign step.

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

## Bottom Line

After this consolidation:

- `main` carries the retained baseline
- this review worktree carries only explicit holds from the non-`main` science
  surface
- no important current frontier item should exist only on a deleted local path
