# Wave Direct-dM Portability Batch

**Date:** 2026-04-08
**Status:** proposed_retained bounded portability batch

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

The first follow-on is now recorded in
[`WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md):
the two-band split is best read as a seed-dependent late-branch
amplification split, not as sign loss and not as early-branch failure.

That first `H = 0.25` high-band replay has now landed as a diagnosed
boundary in
[`WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md):
the `Fam1`, seed `0` point keeps the sign but drops from the old
`-42%..-44%` band to `R_hist = -20.12%`.

The complementary lower-band replay has now also landed in
[`WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md`](./WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md):
the `Fam1`, seed `1` point stays at `R_hist = -29.47%` while the `H = 0.25`
seed-`0` replay had already fallen to `-20.12%`.

That narrow synthesis is now frozen in
[`WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md):
on the current `Fam1`, `S = 0.004` fine-`H` pair, both seeds keep the sign,
but the old seed ordering is not refinement-stable because seed `0` loses most
of its extra late gain while seed `1` retains the lower band.

The first extra-family reserve point has now also landed in
[`WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md):
`Fam2`, seed `0`, `S = 0.004`, `H = 0.25` keeps the sign but still falls from
the old coarse high band (`-42.33%`, `-37.73%`) to `R_hist = -22.61%`.
So the first family-widening replay is another boundary, not an
`H = 0.25` portability rescue.

The complementary second-family seed-`1` follow-up has now also landed in
[`WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md):
its late gain stays on the old seed-`1` scale
(`+0.001937`, `+0.002061`, `+0.002037`) while the same family's seed-`0`
replay had already compressed to `+0.001576`.
So the second family reproduces the cross-seed late-gain asymmetry, but the
normalized magnitude still shifts to `R_hist = -35.03%`, so the fine-`H`
story is still not a stable amplitude-band portability law.

Both second-family `H = 0.25` rows now also have same-resolution control
ladders:

- [`WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md):
  exact `S = 0` null, sign pattern `- - -`, `|delta_hist / s|` spread
  `6.67%`
- [`WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md):
  exact `S = 0` null, sign pattern `- - -`, `|delta_hist / s|` spread
  `4.25%`

So the second family is no longer a one-strength fine-`H` sidecar. It is
now a controlled pair, and the pair keeps the same qualitative asymmetry:
seed `0` remains in the lower boundary regime (`-22%` to `-24%`) while
seed `1` stays materially stronger (`-35%` to `-36%`) without restoring the
old coarse amplitude band.

That pair-level read is now frozen explicitly in
[`WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md).

So the next honest hardening step is now:

- keep the `H = 0.25` read promoted only as a narrow
  `Fam1`/`Fam2` family-pair asymmetry result
- if the lane continues next, spend it on a compression / synthesis pass
  comparing the retained `Fam1` and `Fam2` pair syntheses before any
  `Fam3`, third-seed, or weaker-strength replay
- do not widen to a broader `H = 0.25` portability batch yet

## Artifact chain

- [`scripts/wave_direct_dm_portability_batch.py`](../scripts/wave_direct_dm_portability_batch.py)
- [`logs/2026-04-08-wave-direct-dm-portability-batch.txt`](../logs/2026-04-08-wave-direct-dm-portability-batch.txt)
- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md`](./WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md)
