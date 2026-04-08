# Wave Direct-dM Portability Batch

**Date:** 2026-04-08
**Status:** retained bounded portability batch

This note records the first real portability batch on the direct-`dM`
matched-schedule lane:

> Keep the direct-`dM` setup fixed, sweep the three canonical grown
> families and two seeds, retain the exact `S = 0` null plus the weak
> source-strength sweep, and ask whether the matched-schedule effect
> survives as a bounded multi-family signal.

## Scope

- families: `Fam1`, `Fam2`, `Fam3`
- seeds: `0`, `1`
- resolutions: `H = 0.5`, `0.35`
- strengths: `0.000`, `0.002`, `0.004`, `0.008`
- schedule pair: same realized move trace, different timing within the
  active interval

That is `3 x 2 x 2 x 4 = 48` direct retarded-wave runs.

## Headline result

Three things survived cleanly across the entire batch:

- exact null: `max |delta_hist| = 0.000e+00` at `S = 0`
- sign stability: every nonzero run has `delta_hist < 0`
- weak-field linearity: within each family/seed/`H` bucket, the spread
  on `|delta_hist / s|` over `s = 0.002, 0.004, 0.008` stays between
  `1.97%` and `6.91%`

At the reference strength `s = 0.004`, all `12` family/seed/`H` points
remain material:

- overall `R_hist` band: `-19.98%` to `-44.29%`
- family/`H` means:
  - `Fam1`: `-34.46%` at `H = 0.5`, `-31.17%` at `H = 0.35`
  - `Fam2`: `-34.32%` at `H = 0.5`, `-30.03%` at `H = 0.35`
  - `Fam3`: `-36.78%` at `H = 0.5`, `-33.02%` at `H = 0.35`

## The important nuance

The effect is portable in sign, but not tight in magnitude.

The dominant widening is seed-driven:

- seed `0` sits in the larger band, about `-37%` to `-45%`
- seed `1` sits in the smaller band, about `-20%` to `-30%`

So the honest retained statement is not “one number repeats.” It is:

> Across three canonical families, two seeds, two retained `H` values,
> and the full weak-field sweep, the direct-`dM` matched-schedule effect
> keeps exact null, common negative sign, and low within-seed linearity
> spread, while the normalized magnitude splits into a wider seed-driven
> band of roughly `-20%` to `-45%`.

## What this now supports

This is stronger than the earlier single-family note and stronger than
the one-seed family scout:

- not a `Fam1`-only replay
- not a one-seed coincidence
- not just a sign-at-one-strength scout

It is fair to count this as a **bounded portability positive** for the
direct-`dM` lane.

## What it still does not support

- not a tight amplitude law
- not a full continuum-stability claim
- not an `H = 0.25` portability batch
- not a lab-facing magnitude claim

## Current read

The direct-`dM` lane is now in better shape than the comparator lane.

The strongest clean claim is:

> The direct retarded response has a bounded multi-family,
> multi-seed matched-schedule effect with exact null, stable sign, and
> approximately linear weak-field scaling. The main unresolved issue is
> amplitude spread, not effect existence.

That is a meaningful upgrade over the previous “single-family retained
probe” state.

## Best next move

The next honest hardening step is not more families first. It is:

- explain the two-band seed split

Concrete options:

- add one simple geometry diagnostic to each seed/family replay and ask
  what separates the `-20%` band from the `-40%` band
- add one `H = 0.25` validation point for a single seed from each band,
  not the whole 12-point portability surface

## Artifact chain

- [`scripts/wave_direct_dm_portability_batch.py`](../scripts/wave_direct_dm_portability_batch.py)
- [`logs/2026-04-08-wave-direct-dm-portability-batch.txt`](../logs/2026-04-08-wave-direct-dm-portability-batch.txt)
