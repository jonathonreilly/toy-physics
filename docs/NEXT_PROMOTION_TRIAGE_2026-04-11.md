# Next Promotion Triage — 2026-04-11

**Purpose:** identify the next bounded promotion set from `frontier/spot-checks`
after the latest `main` promotion, and freeze the next items that should remain
frontier-only.

**Scope of this triage:** the current late-2026-04-11 frontier surface, with
special focus on:

- the staggered self-consistent two-body lane
- the unscreened Anderson recheck
- the staggered two-body / both-masses backlog

This note is intentionally narrow. It does **not** reopen already-promoted
open-cubic staggered notes, and it does **not** try to classify the whole
frontier branch. The later Wilson test-mass / continuum companion is a
separate bounded promotion candidate and is not part of this
staggered-focused triage.

## Current baseline

Already on `main`:

- open-cubic staggered external-source Newton reproduction
- blocking-sensitivity companion
- 3D staggered self-gravity contraction / sign note

Still only on frontier:

- unscreened Anderson torus companion
- staggered self-consistent two-body force-led note
- staggered both-masses negative
- staggered two-body next-steps backlog note

## Next 3 promotion candidates

These are the next items that are closest to `main` quality if promoted
carefully and with their bounds preserved.

### 1. Unscreened Anderson torus companion

Candidate:

- `docs/ANDERSON_PHASE_MU2_0001_NOTE_2026-04-11.md`
- `scripts/frontier_anderson_phase_unscreened_periodic.py`

Why it is promotable:

- it is already honestly framed as a bounded corrected-torus companion
- it does not overclaim architecture-wide closure
- the note states the real character change under unscreening:
  - `sigma_alpha > 3` on `28/28`
  - the distinction is carried by small, consistent boundary-law offsets
  - sign is weak as a disorder discriminator

Promotion gate:

- promote only as a **companion** to the corrected periodic Anderson lane
- update control-plane docs to say:
  - unscreening strengthens the numerical coefficient separation on the torus
  - it does **not** convert the torus lane into a generic disorder discriminator

### 2. Staggered self-consistent two-body note, but only as a bounded force-led positive

Candidate:

- `docs/STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md`
- `scripts/frontier_staggered_self_consistent_two_body.py`

Why it is close:

- it is a real primary-architecture advance beyond external-source
  reproduction
- the exact partner-force channel is clean on the audited open-cubic surface:
  - attractive `15/15`
  - global force law `~ d^-1.947` with `R^2 = 0.9992`
- the note already says the blocked trajectory readout does **not** close

Promotion gate:

- promote only if the note is carried to `main` exactly as a **force-led**
  bounded positive
- the control-plane text must explicitly preserve all three caveats:
  - no retained trajectory closure
  - no both-masses closure
  - no graph-family transfer beyond the calibrated open-cubic surface

If those caveats are not preserved, this stays frontier-only.

### 3. Staggered two-body next-steps backlog note

Candidate:

- `docs/STAGGERED_TWO_BODY_NEXT_STEPS_NOTE_2026-04-11.md`

Why it is promotable:

- it is not a science claim; it is a design-control note
- it freezes the actual observable failure mode cleanly:
  - blocked centroids are good enough for single-packet envelope drift
  - not good enough for packet-level two-body force decomposition
- it prevents repeating the same blocked-centroid mass sweep

Promotion gate:

- promote only as backlog / triage guidance
- do **not** cite it as evidence for or against a physical law
- keep the acceptance gates intact:
  - local momentum flux
  - mid-plane current
  - relative-coordinate density observable

## Next 3 items that should stay frontier-only

These are still useful, but should not move to `main` yet.

### 1. Staggered both-masses blocked-centroid lane

Keep on frontier:

- `docs/STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md`
- `scripts/frontier_staggered_both_masses.py`

Why:

- packet-level signs split across the grid
- normalization drift is about `26%`
- force-balance proxy fails at `100%` on every row

Concrete gate before promotion:

- one observable must simultaneously satisfy:
  - inward sign on both packet channels on the same row
  - stable partner-mass normalization across the full mass grid
  - materially nontrivial force-balance agreement

Another blocked-centroid mass sweep does not meet that bar.

### 2. Trajectory-closure claims inside the staggered self-consistent two-body lane

Keep on frontier:

- the trajectory side of
  `docs/STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md`

Why:

- blocked inward rows are only `10/15`
- `dxA_mut` and `dxB_mut` still disagree in sign on multiple rows
- the residual shift is tiny (`~1e-4`) and still aliased by parity-scale
  reshuffling inside coarse windows

Concrete gate before promotion:

- a force- or current-led trajectory companion must survive on the same surface
  with:
  - correct inward sign on every audited row
  - distance scaling consistent with the exact partner-force channel
  - better robustness than the current blocked-centroid residual

### 3. Any implied staggered Newton “full closure” summary

Keep on frontier:

- any control-plane summary that merges:
  - open-cubic external-source `d^-2`
  - self-consistent partner-force `d^-1.947`
  - blocked both-masses / trajectory failures
  into one headline Newton closure

Why:

- the staggered lane is now strong, but still split across bounded surfaces and
  observables
- the primary architecture does **not** yet have:
  - a retained both-masses law
  - a retained self-consistent trajectory observable

Concrete gate before promotion:

- at least one staggered two-body observable must close **both**:
  - self-consistent partner-force or mutual-transport sign
  - partner-mass / both-masses scaling
on the same retained surface

## Promotion order

If doing bounded promotions from this surface, the order should be:

1. `ANDERSON_PHASE_MU2_0001` companion note + runner
2. `STAGGERED_SELF_CONSISTENT_TWO_BODY` note + runner, only with explicit
   force-led caveats
3. `STAGGERED_TWO_BODY_NEXT_STEPS` backlog note

Everything else in this cluster should remain frontier-only until a new
observable closes the staggered two-body/both-masses gap cleanly.

## Bottom line

The next safe promotion set is not “full staggered Newton.”

It is:

- one bounded unscreened Anderson companion
- one bounded primary-architecture self-consistent force note
- one backlog note that prevents wasted reruns

The staggered both-masses and staggered trajectory-closure claims still need a
new observable, not a new summary.
