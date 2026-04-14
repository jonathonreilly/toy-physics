# GW Echo Null Result Note

**Date:** 2026-04-14  
**Script:** `scripts/frontier_echo_null_result.py`  
**Status:** BOUNDED COMPANION — accepted current framework reading is **no
detectable echoes**

## Summary

The current accepted framework result is **not** a positive gravitational-wave
echo prediction.

The older timing-only route correctly derived a characteristic round-trip time
for a would-be frozen-star surface, but later analysis closed the observable
question differently:

- the lattice hard floor still prevents a singularity
- the frozen-star surface still exists
- but the strong-field region between `R_min` and `R_S` creates an
  evanescent-barrier / absorption mechanism that suppresses coherent echo
  return to effectively zero

So the accepted companion claim is:

> frozen stars are observationally silent in ringdown; gravitational-wave echo
> amplitude is effectively zero, and the null-LIGO result is consistent with
> the framework rather than a failure of it.

This note replaces the older positive `67.66 ms / 14.8 Hz` echo-prediction
surface on the current authority path.

## Accepted Claim Boundary

Safe current statement:

- the frozen-star program remains bounded / companion-only
- the framework predicts **no detectable echoes**
- the strongest current explanation is the evanescent barrier in the `f > 1`
  region
- the catalog-level null result is consistent with that prediction

Not the accepted statement:

- that the framework predicts a detectable echo at `67.66 ms`
- that `GW echo timing` belongs on the current publication surface as a
  positive prediction row

## Derivation Chain

### 1. Frozen-star surface still exists

The lattice hard floor gives a minimum physical radius `R_min > 0`, so the
compact object does not collapse to a singularity.

### 2. Timing family still exists mathematically

If one computes the naive round-trip time from the light ring to the frozen
surface and back, one gets the old `58-68 ms` timing scale for GW150914-like
parameters.

That timing family by itself is **not** the accepted observable prediction.

### 3. The decisive later result is amplitude suppression

Later work analyzed four routes:

- absorption / mode conversion
- thermal reflectivity
- frequency-shift consistency
- evanescent tunneling through the `f > 1` region

The decisive lane is the evanescent barrier:

`T ~ exp[-(R_S/l_P) ln(R_S/R_min)]`

For stellar-mass systems the exponent is enormous, so the coherent return is
effectively zero.

### 4. Observation then matches the null prediction

The catalog-level searches do not show a confirmed echo signal. The accepted
summary numbers carried on this branch are:

- frozen-star stack significance: `0.41 sigma`
- Abedi-style stack significance: `1.29 sigma`

Both are null.

## Current Publication Use

This result is **not** part of the retained flagship gravity core.

It is companion-only material and should be carried, if at all, as:

- `GW echo null result`
- `no detectable echoes from frozen stars`
- `bounded / off-scope gravity companion`

It should **not** be carried as:

- `GW echo timing`
- `detectable echo prediction`

## Historical Relation To Older Route Work

The old positive timing-family note has been moved to
`docs/work_history/GW_ECHO_TIMING_ROUTE_NOTE.md`. It remains useful as route
history only.
