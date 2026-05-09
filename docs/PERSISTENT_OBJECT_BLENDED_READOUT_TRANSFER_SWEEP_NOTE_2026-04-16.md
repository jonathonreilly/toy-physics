# Persistent Object Blended Readout Transfer Sweep

**Date:** 2026-04-16  
**Status:** bounded compact-object response transfer positive with one proposed_retained readout on the nearby exact-family neighborhood; still not a persistent inertial-mass closure

**Audit-lane runner update (2026-05-09):** The primary runner `scripts/persistent_object_blended_readout_boundary_probe.py` previously timed out under the audit-lane 120s default budget; already had AUDIT_TIMEOUT_SEC=1800; cache refreshed against the declared budget. The runner's pass/fail semantics are unchanged; this update only ensures the audit-lane sees a complete cache instead of a TIMEOUT row.

## Artifact chain

- Supporting boundary script: [`scripts/persistent_object_blended_readout_boundary_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_blended_readout_boundary_probe.py)
- Boundary log: [`logs/2026-04-16-persistent-object-blended-readout-boundary-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-blended-readout-boundary-probe.txt)
- Transfer script: [`scripts/persistent_object_blended_readout_transfer_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_blended_readout_transfer_sweep.py)
- Transfer log: [`logs/2026-04-16-persistent-object-blended-readout-transfer-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-blended-readout-transfer-sweep.txt)

## Runner/log evidence (audit repair, 2026-05-08)

The cited transfer-sweep runner was re-executed via the canonical
`scripts/precompute_audit_runners.py` mechanism to close the auditor's
runner-artifact gap on the bounded outer-transfer claim. The SHA-pinned
runner-cache file is:

- [`logs/runner-cache/persistent_object_blended_readout_transfer_sweep.txt`](../logs/runner-cache/persistent_object_blended_readout_transfer_sweep.txt)

The runner is annotated with `AUDIT_TIMEOUT_SEC = 1800` (representative
runtime ~500 s on this hardware; the default 120 s ceiling was too tight).
The cached run reproduces the six fixed-blend top2/top3 cases at
`blend = 0.25` with the frozen setup (`h = 0.25`, source strengths
`0.001, 0.002, 0.004, 0.008`, three repeated updates, `field max = 0.02`).
The bottom-line totals match the note's headline:

- `top3` admissible on `6 / 6` cases
- `top2` admissible on `1 / 6` cases (only `length7`)

This evidence supports only the bounded outer-transfer portion of the headline.
The note's stronger inward-source boundary phrasing remains conditional and is
not promoted by this repair.

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

Nearby cases:

1. baseline: `L = 6`, `W = 3`, `source_z = 2.0`
2. source1.5: `L = 6`, `W = 3`, `source_z = 1.5`
3. source2.5: `L = 6`, `W = 3`, `source_z = 2.5`
4. width4: `L = 6`, `W = 4`, `source_z = 2.0`
5. length5: `L = 5`, `W = 3`, `source_z = 2.0`
6. length7: `L = 7`, `W = 3`, `source_z = 2.0`

Object modes:

- `top2`
- `top3`

Frozen gates:

- object overlap mean `>= 0.90`
- all repeated-update steps keep `4/4` `TOWARD`
- all step-wise `F~M` exponents stay in `[0.95, 1.05]`
- response-coefficient drift `<= 10%`

## Frozen result

### Headline

`top3` with the fixed blended readout is admissible on the full nearby
exact-family neighborhood.

Totals:

- `top3`: `6 / 6`
- `top2`: `1 / 6`

So the earlier complementary broad/adaptive split is now resolved on the tested
nearby exact-family family without changing the object class.

### Summary table

| case | `top2` | `top3` | verdict |
| --- | :---: | :---: | --- |
| baseline | ❌ | ✅ | `top3` bridge |
| source1.5 | ❌ | ✅ | `top3` bridge |
| source2.5 | ❌ | ✅ | `top3` bridge |
| width4 | ❌ | ✅ | `top3` bridge |
| length5 | ❌ | ✅ | `top3` bridge |
| length7 | ✅ | ✅ | `top2` bridge |

### Why this is a real upgrade

The transfer is not just the original miss pair being rescued.

The same fixed readout now clears:

- both source-shifted rows: `source1.5`, `source2.5`
- both geometry rows on the short side: `width4`, `length5`
- the longer row where the adaptive readout had failed before: `length7`

So the surviving object-plus-response lane is no longer:

> exact-lattice `top3` object plus case-dependent readout choice

It is now:

> exact-lattice `top3` object plus one retained blended readout architecture on
> the nearby exact-family neighborhood

### Where the compact floor sits

The floor is still near `top3`.

`top2` does not transfer:

- it fails on `5 / 6` cases
- the only opening is the longer `length7` slice

So the compact-object narrowing is bounded:

- `top1` is already closed by update instability
- `top2` is only a local boundary opening
- `top3` is the first transferable object class under one retained readout

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
