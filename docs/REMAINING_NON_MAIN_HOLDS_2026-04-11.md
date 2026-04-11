# Remaining Non-Main Holds

**Date:** 2026-04-11  
**Scope:** review-worktree items that are still not safe for `main`

This is the consolidated inventory for follow-through. It separates the one
remaining bounded candidate from the held items and names the missing control
for each held lane.

## Already on `main`

These are not part of the hold list:

- `STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md`
- `DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`
- `WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md`

## Remaining Bounded Candidate

- `docs/NEWTON_DERIVATION_NOTE.md`

Why it is still only a candidate:

- it is a bounded ordered-lattice family law
- the open step is persistent-pattern inertia / one-parameter mass realization
- it is not yet architecture-independent

## Holds

### 1. Wilson mutual-attraction side lane

Files:

- `docs/TWO_BODY_ATTRACTION_RETAINED_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/TWO_BODY_ATTRACTION_TEMPORAL_ROBUSTNESS_NOTE_2026-04-11.md`
- `docs/WILSON_SIDE_LANE_PROMOTION_REVIEW_2026-04-11.md`
- `docs/WILSON_BOTH_MASSES_ACCEL_NOTE_2026-04-11.md`
- `scripts/frontier_two_body_attraction.py`
- `scripts/frontier_two_body_attraction_robustness.py`
- `scripts/frontier_two_body_attraction_temporal_robustness.py`
- `scripts/frontier_wilson_both_masses_accel.py`
- `scripts/frontier_wilson_both_masses_local_balance.py`

Why held:

- the open-Wilson mutual channel is real
- the early/mid-window near-inverse-square law is real
- the frozen/static-source control has now been run and still does not
  separate dynamic shared backreaction cleanly from a static explanation
- full Newton closure is still open

Next control:

- same open 3D Wilson surface
- `SHARED`, `SELF_ONLY`, `FROZEN_SOURCE`
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

### 3. Action uniqueness

Files:

- `docs/ACTION_UNIQUENESS_AUDIT_2026-04-11.md`
- `scripts/action_uniqueness_investigation.py`

Why held:

- the evidence supports a weak-field family law on one ordered-lattice setup
- it does not justify architecture-independent uniqueness

Next control:

- rewrite to the family level, or
- prove portability across the retained architectures

### 4. Irregular endogenous sign closure

Files:

- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NEXT_STEPS_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_REINFORCEMENT_NOTE_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_closure.py`
- `scripts/frontier_irregular_endogenous_sign_reinforcement.py`

Why held:

- strong on one screened shell-packet surface
- low-screening confirmation failed
- the second packet family still does not close the lane

Next control:

- a third genuinely independent packet family, or
- a size-portability sweep on the same observable

### 5. Staggered two-body closure family

Files:

- `docs/STAGGERED_DIRECT_COM_CLOSURE_NOTE_2026-04-11.md`
- `docs/STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_PORTABILITY_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_TRANSPORT_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_NEXT_STEPS_NOTE_2026-04-11.md`
- `scripts/frontier_staggered_direct_com_closure.py`
- `scripts/frontier_staggered_both_masses.py`
- `scripts/frontier_staggered_two_body_portability.py`
- `scripts/frontier_staggered_two_body_transport.py`

Why held:

- partner-force is real
- direct-CoM closure still fails
- both-masses closure is still negative / force-led
- detector-side transfer is still negative on the audited open-cubic surface

Next control:

- stop centroid variants
- move to a true current, flux, or impulse observable on the same staggered
  surface

## Bottom Line

The review worktree now contains one bounded candidate and a set of explicit
holds. Nothing else should be promoted without the missing control named in
its section.
