# Review Worktree Inbox

**Date:** 2026-04-11  
**Purpose:** consolidate the non-`main` science surface into one review branch so
promotion decisions happen in one place instead of across many frontier tips.

This inbox is intentionally strict:

- if something is already on `main`, it should not be finalized here
- if something is here, it is either:
  - a bounded promotion candidate that still needs one last review pass, or
  - a hold item with a specific missing control / redesign step

## Already On `main`

These are not review items anymore:

- `STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md`
- `scripts/frontier_staggered_test_mass_companion.py`

Status:

- bounded-retained primary-architecture weak-field source-mass companion
- safe reading: source-only static-source companion
- not both-masses closure
- not self-consistent two-body closure
- not standalone distance-law closure

## Review Inventory

### 1. Bounded promotion candidates

These are the strongest things in this review worktree. They still need one
final human pass before any `main` promotion.

#### A. 64^3 path-sum distance continuation

Source branches:

- `origin/claude/youthful-neumann`
- `origin/codex/resonance-controls`

Files:

- `docs/DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`
- `scripts/distance_law_3d_64_closure.py`

Current verdict:

- bounded continuation candidate

Why bounded:

- one 3D point-mass path-sum family
- Dirichlet boundary sensitivity still matters
- no architecture-portability result
- no both-masses closure

What decides promotion:

- final note wording must stay continuation-level only
- no `full Newton closure` language

#### B. Wilson mutual-attraction side lane

Source branches:

- `origin/frontier/spot-checks`
- `origin/claude/sleepy-cerf`
- `origin/codex/wilson-temporal-robustness`

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

Current verdict:

- hold for now

Blocker:

- missing `FROZEN_SOURCE` / static-source control on the same open 3D Wilson
  surface

Required next experiment:

- replay the same side / placement / separation / early-window surface with
  `SHARED`, `SELF_ONLY`, and `FROZEN_SOURCE`

Promotion rule:

- do not move this to `main` unless the new control shows dynamic shared
  backreaction matters beyond a frozen-field explanation

### 2. Explicit holds

These should stay out of `main` until the listed redesign or control is done.

#### A. Exact two-particle product law

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

#### B. Action uniqueness

Source branches:

- `origin/claude/youthful-neumann`
- `origin/codex/resonance-controls`

Files:

- `docs/ACTION_UNIQUENESS_AUDIT_2026-04-11.md`
- `scripts/action_uniqueness_investigation.py`

Why held:

- current evidence supports a weak-field family law on one ordered-lattice
  setup
- it does not justify architecture-independent uniqueness

Required next experiment:

- rewrite the claim to the family level, or
- prove portability across the retained architectures

#### C. Irregular endogenous sign closure

Source branches:

- `origin/codex/irregular-sign-closure`
- `origin/codex/resonance-controls`

Files:

- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NOTE_2026-04-11.md`
- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NEXT_STEPS_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_closure.py`

Why held:

- strong on one screened shell-packet surface
- low-screening confirmation fails
- packet-family generality is not closed

Required next experiment:

- second packet family
- low-screening confirmation on the same observable
- optional size portability if the above two pass

#### D. Staggered two-body closure family

Source branches:

- `origin/frontier/spot-checks`
- `origin/claude/sleepy-cerf`

Files:

- `docs/STAGGERED_DIRECT_COM_CLOSURE_NOTE_2026-04-11.md`
- `docs/STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_PORTABILITY_NOTE_2026-04-11.md`
- `docs/STAGGERED_TWO_BODY_NEXT_STEPS_NOTE_2026-04-11.md`
- `scripts/frontier_staggered_direct_com_closure.py`
- `scripts/frontier_staggered_both_masses.py`
- `scripts/frontier_staggered_two_body_portability.py`

Why held:

- partner-force is real
- direct-CoM closure still fails
- both-masses closure is still negative / force-led

Required next experiment:

- stop trying more centroid variants
- move to current / flux / impulse observables on the staggered surface

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
- this review worktree carries the outstanding non-`main` science surface
- no important current frontier item should exist only on a deleted local path
