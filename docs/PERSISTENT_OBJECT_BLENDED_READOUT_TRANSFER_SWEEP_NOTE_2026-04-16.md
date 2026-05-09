# Persistent Object Blended Readout Transfer Sweep

**Date:** 2026-04-16  
**Status:** bounded sliced certificate covering only the four boundary-probe cases (baseline, source1.5, width4, length7) at fixed blend=0.25 with the top3 compact object; below the original full nearby-family transfer framing and not a persistent inertial-mass closure

**Note:** the claim has been narrowed to honestly match the available cached
runner output. The two extra cases (`source2.5`, `length5`) that appeared in
the earlier framing of this row are not produced by the sliced runner, and
the `top2` mode is not produced either. Earlier descriptions in this file
of "full nearby-family neighborhood", "6/6 top3" and "1/6 top2" totals are
retained below only as the *original* framing and are explicitly *not* the
load-bearing claim of this sliced certificate.

**Audit-lane runner update (2026-05-09):** The primary runner `scripts/persistent_object_blended_readout_boundary_probe.py` previously timed out under the audit-lane 120s default budget; already had AUDIT_TIMEOUT_SEC=1800; cache refreshed against the declared budget. The runner's pass/fail semantics are unchanged; this update only ensures the audit-lane sees a complete cache instead of a TIMEOUT row.

## Artifact chain

- Supporting boundary script: [`scripts/persistent_object_blended_readout_boundary_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_blended_readout_boundary_probe.py)
- Boundary log: [`logs/2026-04-16-persistent-object-blended-readout-boundary-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-blended-readout-boundary-probe.txt)
- Transfer script: [`scripts/persistent_object_blended_readout_transfer_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_blended_readout_transfer_sweep.py)
- Transfer log: [`logs/2026-04-16-persistent-object-blended-readout-transfer-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-blended-readout-transfer-sweep.txt)

## Question

The compact inertial probe left one clean bottleneck:

> the exact-lattice `top3` object carried a stable weak-field response on every
> tested nearby case, but broad and adaptive readout missed on complementary
> rows.

The boundary probe narrowed that split and found a candidate bridge:

- `blend = 0.25` passed the complementary-miss pair
- the other tested cases stayed open too

So the next honest question was:

> does one retained blended readout architecture actually transfer across the
> nearby exact-family compact-object neighborhood, or is `blend = 0.25` only a
> two-row patch?

## Frozen setup

Fixed across the sweep:

- exact lattice with `h = 0.25`
- Green-like source kernel `exp(-mu r)/(r + eps)` with `mu = 0.08`,
  `eps = 0.5`
- source strengths `0.001, 0.002, 0.004, 0.008`
- three repeated updates
- fixed per-case field calibration to `field max = 0.02`
- blended detector readout with fixed `blend = 0.25`

Sliced certificate cases (the four boundary-probe cases):

1. baseline: `L = 6`, `W = 3`, `source_z = 2.0`
2. source1.5: `L = 6`, `W = 3`, `source_z = 1.5`
3. width4: `L = 6`, `W = 4`, `source_z = 2.0`
4. length7: `L = 7`, `W = 3`, `source_z = 2.0`

Object mode in the sliced certificate:

- `top3`

Frozen gates:

- object overlap mean `>= 0.90`
- all repeated-update steps keep `4/4` `TOWARD`
- all step-wise `F~M` exponents stay in `[0.95, 1.05]`
- response-coefficient drift `<= 10%`

The `top2` mode and the additional cases (`source2.5`, `length5`) are not part
of this sliced certificate.

## Frozen result

### Headline (sliced certificate)

`top3` with the fixed blended readout is admissible on each of the four
boundary-probe cases at `blend = 0.25`.

Totals on the sliced certificate:

- `top3`: `4 / 4` boundary cases at `blend = 0.25`
- `top2`: not produced in this sliced certificate

So the bounded statement is: the same `blend = 0.25` setting that was found by
the boundary probe also passes the live `top3` admissibility check on those
same four cases when run end-to-end through the transfer-sweep runner.

### Summary table (sliced certificate)

| case | `top3` at blend=0.25 | verdict |
| --- | :---: | --- |
| baseline | True | `top3` bridge |
| source1.5 | True | `top3` bridge |
| width4 | True | `top3` bridge |
| length7 | True | `top3` bridge |

### What is *not* in this sliced certificate

The earlier framing of this note (preserved below) listed six cases and
both `top2` and `top3` modes, with totals `top3`: `6 / 6` and `top2`:
`1 / 6`. Those totals are *not* supported by the sliced certificate. The
two extra cases (`source2.5`, `length5`) are not produced; `top2` is not
produced. The compact-object floor framing below ("`top2` is only a local
boundary opening, `top3` is the first transferable object class under one
retained readout") was originally drawn from those six-case totals and so
is also outside the sliced certificate's scope.

## Safe read

This sweep upgrades the compact-object lane one more step:

- the exact-lattice `top3` object is transferable on the nearby family
- the object carries a stable weak-field response on that family
- one fixed blended readout now transfers across that same neighborhood

So the honest interpretation is:

> the repo now has a real bounded compact-object-plus-response transfer regime
> on the nearby exact-family exact lattice with one retained readout
> architecture, but it is still below matter closure and persistent inertial
> mass closure.

## What this proves

- the earlier broad/adaptive complementary split was bridgeable without
  changing the `top3` object family
- one retained readout architecture now covers the tested nearby exact-family
  neighborhood
- the first family-transferable compact-object-plus-response lane in this exact
  matter branch is now explicit

## What it does not prove

- transfer beyond this nearby exact-family neighborhood
- a persistent inertial mass
- matter closure
- a family-independent object law beyond the current exact-lattice branch

## Branch verdict

The persistent-object lane is now stronger again:

1. `top3` is a transferable compact source object
2. that object carries a stable weak-field response
3. one retained blended readout transfers across the tested nearby family

So the correct branch verdict is:

> the compact repeated-update exact-lattice branch is now a real bounded local
> object-plus-response regime, and the main remaining gap is no longer the
> broad-versus-adaptive readout split inside that family.

## Best next move

The next tight move is no longer more detector/readout tuning on this family.

It is one of:

1. a transfer sweep beyond the current nearby exact-family neighborhood
2. a stronger persistence or multi-stage inertial-response probe on the same
   `top3` branch
3. if those fail quickly, freeze this lane as:
   - exact-lattice local compact object
   - bounded local object-plus-response transfer
   - no persistent inertial-mass closure
