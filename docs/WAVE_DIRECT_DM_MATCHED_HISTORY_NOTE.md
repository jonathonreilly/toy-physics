# Wave Direct-dM Matched-History

**Date:** 2026-04-08
**Status:** retained single-family direct-response probe

This probe is the smallest clean fallback if the exact static comparator
route does not stabilize:

> On the current `Fam1`, seed-0 replay, keep the source start position,
> end position, total `NL`, and final source geometry fixed, use two
> source schedules with the same realized moving trace but different
> timing, and compare the direct retarded-wave beam response `dM`.

The two schedules used here are:

- `early-move`: source moves to the final position in the first half of
  the active interval, then sits
- `late-move`: source sits first, then moves to the same final position
  in the second half of the active interval

This is a **single-family replay** only. It is not yet a portability
claim.

## Control stack

The probe now includes an exact `S = 0` null and a small-strength sweep
at both tested `H` values.

### `H = 0.5`

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.002710` | `+0.004777` | `-0.002067` | `-43.27%` | `-1.034` |
| `0.004` | `+0.005385` | `+0.009547` | `-0.004161` | `-43.59%` | `-1.040` |
| `0.008` | `+0.010627` | `+0.019059` | `-0.008432` | `-44.24%` | `-1.054` |

### `H = 0.35`

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.002423` | `+0.004164` | `-0.001741` | `-41.81%` | `-0.871` |
| `0.004` | `+0.004811` | `+0.008346` | `-0.003535` | `-42.36%` | `-0.884` |
| `0.008` | `+0.009483` | `+0.016764` | `-0.007281` | `-43.43%` | `-0.910` |

The exact null is exact to numerical precision at both tested `H`
values, and the nonzero points are approximately linear in `s` over the
tested weak-field band.

## Results

| quantity | `H = 0.5` | `H = 0.35` |
| --- | ---: | ---: |
| `dM(early)` | `+0.005385` | `+0.004811` |
| `dM(late)` | `+0.009547` | `+0.008346` |
| `delta_hist = dM(early) - dM(late)` | `-0.004161` | `-0.003535` |
| `R_hist` | `-43.59%` | `-42.36%` |

## Honest read

On the current `Fam1`, seed-0 replay, the direct finite-`c` response is
schedule-sensitive even when the realized move trace and final source
geometry are matched.

- the sign of `delta_hist` is the same at both tested `H`
- the normalized effect size is also similar: about `-42%` to `-44%` at
  both `H = 0.5` and `H = 0.35`
- the tested `H` values are only approximately matched in physical
  geometry because discretization shifts `PW` and `z_start` slightly
  (`PW=6.000` vs `5.950`, `z_start=3.000` vs `3.150`)

What this does **not** show yet:

- no three-family portability yet
- no multi-seed replay yet
- no full `H = 0.25` ladder yet
- no claim that this is a lab-ready observable

Related side notes:

- an exploratory one-seed family scout is recorded in
  [`WAVE_DIRECT_DM_FAMILY_SCOUT_NOTE.md`](./WAVE_DIRECT_DM_FAMILY_SCOUT_NOTE.md)
- a narrow `H = 0.25` runtime check is recorded in
  [`WAVE_DIRECT_DM_H025_FEASIBILITY_NOTE.md`](./WAVE_DIRECT_DM_H025_FEASIBILITY_NOTE.md)

So the current retained claim is narrow:

> On the current `Fam1`, seed-0 replay, two source schedules with the
> same realized move trace produce materially different direct retarded
> responses `dM`, with exact `S = 0` null, consistent sign across
> `H = 0.5` and `H = 0.35`, and approximately linear weak-field scaling
> over the tested `s` range.

## Artifact chain

- [`scripts/wave_direct_dm_matched_history_probe.py`](../scripts/wave_direct_dm_matched_history_probe.py)
- [`logs/2026-04-08-wave-direct-dm-matched-history.txt`](../logs/2026-04-08-wave-direct-dm-matched-history.txt)
