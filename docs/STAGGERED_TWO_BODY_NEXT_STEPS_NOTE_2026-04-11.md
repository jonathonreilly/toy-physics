# Staggered Two-Body Next Steps Note

**Date:** 2026-04-11  
**Status:** bounded backlog / next-step note  
**Scope:** non-retainable staggered two-body pieces from the late 2026-04-11 batch

## What this note is for

This note freezes the actionable lesson from the new staggered open-cubic
frontier work:

- [STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md](STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md)
- [STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md](STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md)
- [STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md](STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md)
- [STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md](STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md)

The external-source staggered Newton reproduction is a real bounded positive.
The non-retainable part of this batch is narrower:

- the blocked-centroid **both-masses** lane does not close
- the blocked-centroid **self-consistent two-body trajectory** lane does not
  close

This note states exactly why, so the next iteration does not repeat the same
observable failure.

## What survived

Two useful positives are now established on the primary staggered architecture:

1. The open-cubic external-source trajectory lane is real.
   - with sensible blocking, the staggered envelope gives a Newton-compatible
     `d^-2` law
   - the result survives `(1,1,2)` and `(2,2,2)` blocking and fails only under
     obvious over-coarsening

2. The open-cubic self-consistent two-body **force** lane is real.
   - exact partner-only force is clean on all audited rows
   - the global fit is near-Newton on the calibrated open-cubic surface

So the architecture itself is not the blocker.

## What did not survive

### 1. Blocked both-masses packet split

The blocked `2x2x2` packet-level split does not support a retained both-masses
law.

From [STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md](STAGGERED_BOTH_MASSES_NOTE_2026-04-11.md):

- anchor slices are perfectly linear
- but `a_A^mut` and `a_B^mut` carry opposite signs across the full grid
- normalized responses drift by about `26%`
- force-balance proxy fails at `100%` on every row

That means the readout can see a weak pair-relative closing channel, but it
cannot decompose that closing into two honest packet-level forces.

### 2. Blocked self-consistent trajectory split

The self-consistent two-body lane confirms the same failure in a stronger
setting.

From [STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md](STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md):

- exact partner-only force is attractive on `15/15`
- blocked trajectory inward sign survives only `10/15`
- blocked mutual shift is tiny, around `1e-4`
- `dxA_mut` and `dxB_mut` often disagree in sign on the same row

So the force channel is real, but the blocked trajectory split is still not a
retainable observable.

## Why the blocked-centroid split fails

The failure mode is now clear enough to treat as a design constraint.

### A. The blocked centroid is an envelope readout, not a packet-force readout

Blocking suppresses parity beating well enough to recover a single-packet
envelope response under an external source. That does **not** mean the same
readout can be split into two packet-level mutual forces.

What the blocked centroid measures well:

- coarse envelope drift
- relative closing of the pair as a whole

What it does **not** measure well:

- equal-and-opposite packet forces
- local partner-to-partner momentum transfer

### B. The mutual channel is a small residual on top of larger self and parity structure

The two-body readout is built from `shared - self-only` differences. On the
staggered surface, that residual is small compared with:

- self-induced envelope reshaping
- parity-scale density redistribution inside each blocked window
- boundary-sensitive block occupancy changes

That is why the exact force can be clean while the blocked trajectory split
stays tiny and sign-fragile.

### C. Block boundaries alias internal density reshuffling as apparent drift

The blocked observable depends on how probability moves between cells inside a
coarse window, not just on where the packet center is physically accelerating.
In the two-body setting, that creates a failure mode:

- the pair-relative channel can remain inward
- while the packet-resolved blocked centroids report opposite or unstable signs

This is exactly what the both-masses and self-consistent two-body notes show.

### D. The observable is better at a relative-coordinate signal than at a force decomposition

The strongest honest read from the current batch is:

- the blocked readout can expose a small relative-closing channel
- it is not trustworthy for packet-by-packet force closure

That is why another blocked-centroid mass sweep is the wrong next step.

## What to try next

The next staggered two-body batch should move to observables that are closer to
the transport law and farther from block-boundary aliasing.

### 1. Local momentum flux

Measure a packet-local momentum-flux or force-flux quantity near each orbital,
using the same `shared` versus `self-only` subtraction.

Why this is first:

- it stays local to the packet
- it is naturally force-led
- it should respond to partner-driven transport before a centroid visibly moves

Acceptance gate:

- inward sign on both packets on the same row
- stable partner-mass normalization across the full grid
- materially better force-balance than the current blocked split

### 2. Mid-plane current

Measure the net probability current crossing the plane between the two packets.

Why:

- it is the most direct graph-native two-body transport observable
- it tests whether the shared field creates extra inward flow between the
  packets, rather than relying on post hoc centroid summaries

Acceptance gate:

- shared current exceeds self-only current with the correct sign on all audited
  rows
- current magnitude follows the same distance law as the exact partner-force
  channel on the same surface

### 3. Relative-coordinate density observable

Construct a relative-coordinate observable directly from the blocked density,
instead of subtracting two packet centroids.

Examples:

- left-right density imbalance around the mid-plane
- separation-weighted density moment
- inward shell transfer between packet-centered windows

Why:

- the current positive is genuinely pair-relative, not packet-resolved
- this keeps the observable aligned with what actually survives

Acceptance gate:

- monotone inward response under `shared - self-only`
- no sign disagreement between the two packet views
- better scaling stability than `dxA_mut` / `dxB_mut`

### 4. Only then revisit trajectory closure

Do **not** reopen another blocked-centroid both-masses sweep until one of the
three observables above has a clean sign and normalization surface.

The current batch already established that the blocked-centroid packet split is
not the right closure instrument.

## Recommended order

1. exact local momentum flux around each packet
2. mid-plane current on the same surface
3. pair-relative density observable if the first two remain mixed
4. only then a new mass-grid or distance sweep

## Bottom line

The current non-retainable staggered pieces do not mean the primary
architecture lacks a two-body channel.

They mean something narrower and more actionable:

> the open-cubic staggered lane now has a real external-source trajectory
> `d^-2` result and a real self-consistent two-body **force** result, but the
> blocked-centroid packet split is not a retainable two-body closure
> observable.

The next wins will come from force- or current-led readouts, not from another
centroid split.
