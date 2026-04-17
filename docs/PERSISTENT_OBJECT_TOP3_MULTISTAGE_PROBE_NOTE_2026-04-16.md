# Persistent Object Top3 Multistage Probe

**Date:** 2026-04-16  
**Status:** bounded multistage negative; the widened exact-lattice `top3` branch keeps perfect compressed carry and stable response, but still fails the honest persistence bar

## Artifact chain

- Script: [`scripts/persistent_object_top3_multistage_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_top3_multistage_probe.py)
- Log: [`logs/2026-04-16-persistent-object-top3-multistage-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-top3-multistage-probe.txt)

## Question

The widened blended-readout transfer sweep left one stronger test:

> if the exact-lattice `top3` branch is really moving toward a persistent
> inertial object, it should survive more than a single sourced-response
> segment and keep both its object identity and its weak-field response.

So this probe keeps the branch fixed and asks the harder version:

> can the widened exact-lattice `top3` branch survive **three full
> sourced-response segments in sequence** as the same compact object family?

## Frozen setup

Fixed across the probe:

- exact lattice with `h = 0.25`
- retained compact object rule `top3`
- retained blended readout `blend = 0.25`
- source strengths `0.001, 0.002, 0.004, 0.008`
- three updates per segment
- three chained segments

Stable widened-regime rows:

1. baseline: `L = 6`, `W = 3`, `source_z = 2.0`
2. source1.5: `L = 6`, `W = 3`, `source_z = 1.5`
3. source2.75: `L = 6`, `W = 3`, `source_z = 2.75`
4. width5: `L = 6`, `W = 5`, `source_z = 2.0`
5. length8: `L = 8`, `W = 3`, `source_z = 2.0`

Each segment does the same thing:

1. start from the current source-weight object
2. run the full three-update sourced-response cycle
3. compress back to the final `top3` source object
4. use that final object as the next segment seed

Frozen gates:

- every segment keeps mean update overlap `>= 0.90`
- every stage-to-stage carry mean `>= 0.90`
- every stage-to-stage carry minimum `>= 0.85`
- every segment keeps `4/4` `TOWARD`
- every segment keeps `F~M` in `[0.95, 1.05]`
- stage-to-stage `kappa` drift `<= 10%`

## Frozen result

### Headline

The widened `top3` branch fails the multistage persistence bar on **all**
tested stable rows:

- multistage-admissible: `0 / 5`

But the failure is not a generic collapse.

Two parts stay almost perfectly stable:

- stage-to-stage compressed carry: `1.000` on every tested row
- stage-to-stage `kappa` drift: `0.000%` on every tested row

The actual failure is narrower and more informative:

- stage-2 and stage-3 mean update overlap falls below the retained `0.90` bar
- the later-segment overlap sits in the range `0.835 - 0.884`

So the branch keeps coming back to the same compressed `top3` object, but it
does not remain honest as a self-maintaining `top3` object while each segment
is actually propagating.

### Summary table

| case | stage mean overlap | carry mean | max `kappa` drift | verdict |
| --- | --- | --- | --- | --- |
| baseline | `[0.929, 0.876, 0.876]` | `[1.000, 1.000]` | `0.000%` | fail |
| source1.5 | `[0.929, 0.884, 0.884]` | `[1.000, 1.000]` | `0.000%` | fail |
| source2.75 | `[0.931, 0.835, 0.835]` | `[1.000, 1.000]` | `0.000%` | fail |
| width5 | `[0.928, 0.884, 0.884]` | `[1.000, 1.000]` | `0.000%` | fail |
| length8 | `[0.935, 0.856, 0.856]` | `[1.000, 1.000]` | `0.000%` | fail |

### Why this is the right negative

This is not the same as saying the branch disappears.

It does **not** disappear:

- the compressed object family is re-identifiable stage after stage
- the response law is extremely stable once that compression is imposed

What fails is the stronger persistence claim:

> during each segment, the propagated source distribution repopulates enough
> weight outside the compressed `top3` support that the honest within-segment
> object overlap falls below the retained persistence bar

So the widened exact-lattice branch is best read as:

> a compression-stabilized transfer object

not:

> a self-maintaining multistage persistent object

## Safe read

This probe closes the stronger escalation on the current exact-lattice branch.

The widened `top3` lane now has all of the following:

- nearby-family transfer
- second-ring partial transfer
- mapped outer boundary
- perfect compressed carry across chained segments
- perfectly stable stage-wise weak-field response across those segments

But it still does **not** have:

- honest self-maintaining multistage persistence at the retained overlap bar

So the correct interpretation is:

> the exact-lattice `top3` branch is a widened local transfer-positive compact
> object with compression-stabilized multistage response, not a closure-grade
> persistent inertial object.

## What this proves

- the widened `top3` branch is more structured than a one-step artifact
- the branch has a real compressed fixed-point character across segments
- the remaining failure is specifically the self-maintaining persistence bar,
  not the weak-field response law

## What it does not prove

- a self-maintaining persistent inertial mass
- matter closure
- a multistage object law that survives without repeated compression back to
  `top3`

## Branch verdict

The persistent-object branch is now better diagnosed:

1. `top3` is a widened local exact-lattice transfer object
2. the response law survives chained segments
3. the compressed object is re-identifiable stage after stage
4. the self-maintaining persistence claim still fails

So the correct branch verdict is:

> this exact-lattice `top3` route should now be read as a widened local
> transfer-positive object lane, not as the missing persistent inertial object
> closure.

## Best next move

The next honest move is no longer another small tuning pass on this branch.

It is one of:

1. a different object architecture that can stay honest without per-segment
   recompression
2. one last explicit diagnostic showing whether a slightly broader retained
   source object, rather than `top3`, is the real self-maintaining floor
3. if that does not open quickly, freeze this exact-lattice route as:
   - widened local transfer-positive compact object
   - compression-stabilized multistage response
   - no persistent inertial-mass closure
