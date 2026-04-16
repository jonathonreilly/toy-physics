# Persistent Object Compact Inertial Probe

**Date:** 2026-04-16  
**Status:** bounded compact-object response positive with readout-dependent transfer; still not a persistent inertial-mass closure

## Artifact chain

- Script: [`scripts/persistent_object_compact_inertial_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_compact_inertial_probe.py)
- Log: [`logs/2026-04-16-persistent-object-compact-inertial-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-compact-inertial-probe.txt)

## Question

The compact transfer sweep established a real transferable `top3` exact-lattice
source object.

That moved the bottleneck from source portability to the response side:

> can the transferable compact object carry a stable weak-field response across
> repeated updates and nearby exact-family slices, or does the lane still stop
> at “portable source object” only?

This probe uses the same compact object family and couples it to the two
retained detector readouts:

- broad centroid
- adaptive contour

## Frozen setup

Fixed across the probe:

- exact lattice with `h = 0.25`
- Green-like source kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`,
  `eps = 0.5`
- source strengths `0.001, 0.002, 0.004, 0.008`
- three repeated updates
- fixed per-case field calibration to `field max = 0.02`

Nearby cases:

1. baseline: `L = 6`, `W = 3`, `source_z = 2.0`
2. source1.5: `L = 6`, `W = 3`, `source_z = 1.5`
3. width4: `L = 6`, `W = 4`, `source_z = 2.0`
4. length7: `L = 7`, `W = 3`, `source_z = 2.0`

Object modes:

- `broad`
- `top2`
- `top3`

Readouts:

- `broad`
- `adaptive`

Frozen gates:

- object overlap mean `>= 0.90`
- all repeated-update steps keep `4/4` `TOWARD`
- all step-wise `F~M` exponents stay in `[0.95, 1.05]`
- response-coefficient drift `<= 10%`

The response metrics reuse the ordered-lattice inertial lane directly:

- `kappa = delta / s`
- stage-wise `kappa_mean = mean_s(kappa)`
- drift between updates
  `= abs(curr_kappa_mean - prev_kappa_mean) / max(abs(prev_kappa_mean), 1e-30)`

## Frozen result

### Headline

The transferable compact object does carry a stable weak-field response, but the
transfer is readout-dependent.

For `top3`:

- broad readout is admissible on `3 / 4` nearby cases
- adaptive readout is admissible on `3 / 4` nearby cases
- the misses are complementary

So across the tested family:

- baseline: both broad and adaptive pass
- width4: both broad and adaptive pass
- source1.5: adaptive passes, broad fails
- length7: broad passes, adaptive fails

That means the compact object itself is real on all tested cases, but no single
retained readout is yet family-dominant.

### Summary table

| case | `top3 broad` | `top3 adaptive` | `top2 broad` | `top2 adaptive` |
| --- | :---: | :---: | :---: | :---: |
| baseline | ✅ | ✅ | ❌ | ❌ |
| source1.5 | ❌ | ✅ | ❌ | ❌ |
| width4 | ✅ | ✅ | ❌ | ❌ |
| length7 | ✅ | ❌ | ✅ | ❌ |

Totals:

- `top3 broad`: `3 / 4`
- `top3 adaptive`: `3 / 4`
- `top2 broad`: `1 / 4`
- `top2 adaptive`: `0 / 4`

### Why the misses matter

The failures are not generic collapses.

#### `source1.5`

`top3` broad fails only by response drift:

- broad `max drift = 12.137%`
- adaptive `max drift = 8.796%`
- both keep `F~M ≈ 1`
- both keep the object overlap gate

So this row says the adaptive contour can stabilize a nearby source-shifted
response that the broad centroid does not stabilize.

#### `length7`

`top3` adaptive fails, but broad passes cleanly:

- broad `max drift = 1.154%`, `F~M = 1.00`
- adaptive `max drift = 3.292%`, but `F~M = 1.06`

So the adaptive miss is not a drift problem. It is a mild exponent overshoot on
the longer slice.

### What survives strongly

Two points are now quite robust:

1. `top3` is a real transferable compact object family
2. the compact object can carry a stable weak-field response on every tested
   nearby case if one allows the best retained readout for that case

The narrower boundary remains bounded:

- `top2` only passes on `length7` with the broad readout
- `top1` was already closed by update instability in the transfer sweep

So the compact-object floor is still near `top3`, with `top2` only a local
narrowing on the longer slice.

## Safe read

This probe upgrades the compact-object lane one more step:

- the exact-lattice object is no longer just a portable source pattern
- it now carries a measurable, weak-field-stable response on a nearby family
- but the response is still readout-architecture dependent

So the honest interpretation is:

> the compact repeated-update exact-lattice object now supports a bounded
> compact-object-plus-response regime, but not yet a readout-invariant or
> closure-grade inertial object law.

## What this proves

- `top3` supports a stable weak-field response on the tested nearby family
- the response survives under both retained readout architectures on part of
  that family
- the current failures are complementary rather than universal
- the remaining bottleneck has narrowed to readout-dependent transfer

## What it does not prove

- a single readout architecture that transfers across the whole tested family
- a persistent inertial mass
- matter closure
- a fully readout-invariant compact object law

## Branch verdict

The persistent-object lane is now stronger again:

1. `top3` is a transferable compact source object
2. that object now also carries a stable weak-field response
3. the remaining boundary is a readout-dependent transfer split

So the correct branch verdict is:

> the repo now has a real bounded compact-object-plus-response lane on the
> exact lattice, but it is still below the closure bar because the retained
> readout is not yet family-invariant.

## Best next move

The next tight move is not more source shrinkage.

It is one of:

1. a blended broad/adaptive readout architecture tested specifically on the
   complementary-miss pair (`source1.5`, `length7`)
2. a small readout-boundary sweep around those two rows to see whether one
   retained readout can cover both
3. if that fails quickly, freeze this lane as:
   - transferable compact source object
   - bounded compact-object response
   - no readout-invariant inertial closure
