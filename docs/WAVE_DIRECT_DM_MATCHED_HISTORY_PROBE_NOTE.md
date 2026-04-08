# Wave Direct-dM Matched-History Probe

**Date:** 2026-04-08
**Status:** preliminary fallback probe

This is the smallest comparator-free fallback lane for the
wave-retardation program:

> hold the beam setup fixed, use two source histories with the same
> start position, end position, final geometry, total `NL`, and
> `src_layer`, and compare the direct retarded-wave response `dM`.

The two histories are:

- `early_move`: move to the final source position in the first half of
  the active interval, then sit
- `late_move`: sit first, then move to the same final source position in
  the second half of the active interval

The observable is:

- `dM = cz(retarded field) - cz(free beam)`
- `Δ_hist = dM(early_move) - dM(late_move)`
- `R_hist = Δ_hist / max(|dM_early|, |dM_late|, 1e-12)`

## Initial result

The first probe used the existing beam setup and tested two `H` values.

| quantity | `H = 0.5` | `H = 0.35` |
| --- | ---: | ---: |
| `dM(early)` | `+0.005840` | `+0.005215` |
| `dM(late)` | `+0.009541` | `+0.008328` |
| `Δ_hist` | `-0.003701` | `-0.003113` |
| `R_hist` | `-38.79%` | `-37.38%` |

## Honest read

This is **not** a retained lane yet. It is a promising fallback probe.

What is encouraging:

- `Δ_hist` has the same sign at both tested `H` values
- the normalized history observable `R_hist` is stable in sign and close
  in magnitude across the two tested steps
- the result does not depend on any `c = infinity` comparator

What is still missing before promotion:

- exact `S = 0` null
- small-`s` linearity check
- fine-step `H = 0.25`
- optional frozen-source and reversal controls

So the current read is narrow:

> matched source histories with the same final geometry already produce
> a stable-sign difference in the direct finite-`c` response `dM` at
> coarse and medium `H`.

That is enough to make the direct-`dM` lane the right fallback if the
static-comparator rescue fails, but not enough to replace the flagship
yet.

## Artifact chain

- [`scripts/wave_direct_dm_matched_history_probe.py`](../scripts/wave_direct_dm_matched_history_probe.py)
