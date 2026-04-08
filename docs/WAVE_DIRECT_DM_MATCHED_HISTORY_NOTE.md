# Wave Direct-dM Matched-History

**Date:** 2026-04-08
**Status:** retained direct-response probe

This probe is the smallest clean fallback if the exact static comparator
route does not stabilize:

> Keep the beam setup fixed, keep the source start position, end
> position, total `NL`, and final source geometry fixed, and compare the
> direct retarded-wave beam response `dM` for two different source
> histories.

The two histories used here are:

- `early-move`: source moves to the final position in the first half of
  the active interval, then sits
- `late-move`: source sits first, then moves to the same final position
  in the second half of the active interval

## Results

| quantity | `H = 0.5` | `H = 0.35` |
| --- | ---: | ---: |
| `dM(early)` | `+0.005840` | `+0.005215` |
| `dM(late)` | `+0.009541` | `+0.008328` |
| `delta_hist = dM(early) - dM(late)` | `-0.003701` | `-0.003113` |
| `R_hist` | `-38.79%` | `-37.38%` |

## Honest read

The direct finite-`c` response is history-sensitive even when the final
source geometry is matched.

- the sign of `delta_hist` is the same at both tested `H`
- the normalized effect size is also similar: about `-38%` at both
  `H = 0.5` and `H = 0.35`

This is already a cleaner signal than the current comparator lane,
because it does not rely on defining a `c = infinity` baseline.

What this does **not** show yet:

- no null/control stack yet
- no three-family portability yet
- no full `H = 0.25` ladder yet
- no claim that this is a lab-ready observable

So the current retained claim is narrow:

> At fixed beam geometry and matched final source geometry, two
> different source histories give materially different direct retarded
> responses `dM`, with consistent sign and similar normalized magnitude
> on the tested `H = 0.5` and `H = 0.35` points.

## Artifact chain

- [`scripts/wave_direct_dm_matched_history_probe.py`](../scripts/wave_direct_dm_matched_history_probe.py)
