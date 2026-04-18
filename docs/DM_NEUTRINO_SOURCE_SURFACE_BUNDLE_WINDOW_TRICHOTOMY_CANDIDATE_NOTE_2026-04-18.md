# DM Neutrino Source-Surface Bundle-Window Trichotomy Candidate

**Date:** 2026-04-18  
**Status:** broad exact-bundle trichotomy on endpoint / split-1 / split-2; not flagship closure  
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_bundle_window_trichotomy_candidate.py`

## Question

What is the sharpest shared statement about the three rival `m` windows when
they are viewed directly on the broad exact shift-quotient bundle of the
compact branch?

## Bottom line

The three windows do not behave the same on that bundle.

On the broad tested exact bundle box

- `delta in [-2.5, 2.5]`
- `r31 in [0.5, 4.0]`

their refined minima are:

- endpoint: `3.027555919409`
- split-1: `2.308603400914`
- split-2: `1.500442491658`

against the preferred recovered floor

- `Lambda_+(x_*) = 1.586874714730`

So:

- endpoint is safely above the preferred floor
- split-1 is safely above the preferred floor
- split-2 is below the preferred floor on that same broad bundle domain

## Why this matters

This changes the carrier-side interpretation.

It means broad exact-bundle dominance is not the right carrier-side theorem target. If we
tried to prove “every point in the three rival windows is above the preferred
floor” directly on the broad shift-quotient bundle, that statement would
already fail on split-2.

So the useful remaining theorem has to use the finer exact carrier restriction,
not the broad bundle alone.

## Local control

All three broad-box minima are still locally boundary-controlled in the same
basic sense:

- they sit at the upper-`m`, lower-`r31` corner of their tested boxes
- moving inward in `m` or `r31` raises repair
- the delta direction has positive local second variation

So the difference between endpoint/split-1 and split-2 is not missing local
control on the tested bundle box. It is the floor level itself.

## Carrier-side read after this note

The compact-branch picture is now:

- endpoint: strong tested local exact-bundle dominance candidate
- split-1: strong tested local exact-bundle dominance candidate
- split-2: broad exact-bundle counterexample to naive local dominance, even
  though the finer anchored split-2 carrier picture remains coherent on the
  tested stencils

That is why the remaining useful theorem target is not broad bundle dominance.
It is the finer exact-carrier dominance/completeness theorem.

## Honest boundary

This is not an interval-certified theorem, not exact carrier completeness, and
not flagship closure.

It is a broad exact-bundle trichotomy candidate whose main value is to show
that the exact carrier restriction is doing real mathematical work on the
carrier side.
