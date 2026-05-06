# Persistent Object Top4 Multistage Transfer Sweep

**Date:** 2026-04-16  
**Status:** bounded widened-pocket multistage positive; the first self-maintaining floor `top4` transfers on `11/13` tested local-pocket rows with only a residual inward-source boundary

## Artifact chain

- Script: [`scripts/persistent_object_top4_multistage_transfer_sweep.py`](../scripts/persistent_object_top4_multistage_transfer_sweep.py)
  (thin wrapper; the load-bearing `Case` / `_run_case` admissibility computation lives in
  [`scripts/persistent_object_top3_multistage_probe.py`](../scripts/persistent_object_top3_multistage_probe.py),
  which this script imports and re-runs at `top_keep=4`)
- SHA-pinned audit-lane cache: [`logs/runner-cache/persistent_object_top4_multistage_transfer_sweep.txt`](../logs/runner-cache/persistent_object_top4_multistage_transfer_sweep.txt)
  (see `docs/audit/RUNNER_CACHE_POLICY.md`)

## Question

The multistage floor sweep identified the first honest self-maintaining floor:

> `top4`, not `top3`

That left the next honest bar:

> does that `top4` multistage floor transfer across the widened exact-lattice
> local pocket, or is it only a stable-anchor subset result?

## Frozen setup

Fixed across the sweep:

- exact lattice with `h = 0.25`
- retained blended readout `blend = 0.25`
- retained multistage floor `top4`
- three updates per segment
- three chained segments
- same multistage gates as the floor sweep

Tested widened-pocket rows:

- `baseline`
- inward-source side: `source0.75`, `source1.00`, `source1.25`, `source1.50`
- outward-source side: `source2.50`, `source2.75`
- width side: `width4`, `width5`
- length side: `length4`, `length5`, `length7`, `length8`

## Frozen result

### Headline

`top4` transfers as a multistage floor on **most of the widened local pocket**.

Totals:

- admissible: `11 / 13`
- failed: `2 / 13`

The full width/length side is open:

- width side: `2 / 2`
- length side: `4 / 4`

The outward-source side is also fully open:

- `source2.50`: open
- `source2.75`: open

The only remaining misses are the two deepest inward-source rows:

- `source0.75`: closed
- `source1.00`: closed

while:

- `source1.25`: open
- `source1.50`: open

So the multistage floor boundary has moved inward relative to the earlier
single-segment `top3` read. On the current exact lattice, the residual
inward-source boundary is now between `source_z = 1.00` and `1.25`.

### Summary table

| family slice | rows | `top4` multistage result |
| --- | --- | --- |
| baseline control | `baseline` | `1 / 1` |
| inward source side | `0.75, 1.00, 1.25, 1.50` | `2 / 4` |
| outward source side | `2.50, 2.75` | `2 / 2` |
| width side | `width4, width5` | `2 / 2` |
| length side | `length4, length5, length7, length8` | `4 / 4` |

### Why this is a real upgrade

This is no longer just a stable-anchor positive.

The first self-maintaining floor now survives:

- both tested outer-source rows
- both tested width rows
- all four tested length rows
- one inward-source reopening step earlier than before (`1.25` instead of only
  `1.50`)

So the branch has upgraded from:

> stable-branch multistage positive

to:

> widened-pocket multistage positive with a residual inward-source boundary

### What still limits the route

The route is not yet local-pocket universal.

Two rows still fail:

- `source0.75`
- `source1.00`

The `source1.00` miss is visibly an exponent miss:

- stage alpha: `[1.11, 1.11, 1.11]`

The `source0.75` row also remains inadmissible despite strong overlap/carry.

So the remaining local limit is now narrow and directional:

> deep inward source placement

rather than a generic failure of the `top4` multistage floor.

## Safe read

This sweep strengthens the exact-lattice object route again.

The strongest honest statement is now:

> the exact-lattice branch has a real self-maintaining multistage `top4` floor
> that transfers across most of the widened local pocket, with only a residual
> inward-source boundary between `1.00` and `1.25`.

That is still below persistent inertial-mass closure, but it is materially
stronger than the earlier “stable subset only” read.

## What this proves

- `top4` is not just the first multistage floor on the stable anchor rows
- the `top4` floor transfers across `11 / 13` tested widened-pocket rows
- the remaining local boundary is now narrow and mapped

## What it does not prove

- full local-pocket universality
- transfer beyond the current widened local pocket
- persistent inertial-mass closure
- matter closure

## Branch verdict

The persistent-object branch is stronger again:

1. `top3` found the local transfer-positive branch
2. `top4` became the first self-maintaining multistage floor
3. that `top4` floor now transfers across most of the widened local pocket

So the correct branch verdict is:

> the exact-lattice route now has a bounded transferable multistage compact
> object floor, not just a stable-anchor multistage object.

## Best next move

The next tight move is now one of:

1. one farther transfer sweep beyond the current widened local pocket
2. one focused diagnosis of the residual inward-source boundary at `0.75` and
   `1.00`
3. if those fail quickly, freeze the route as:
   - transferable widened-pocket multistage floor
   - inward-source-bounded local regime
   - no closure-grade persistent inertial mass yet
