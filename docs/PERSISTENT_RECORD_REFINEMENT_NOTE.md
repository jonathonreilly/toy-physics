# Persistent Record Refinement Note

**Date:** 2026-04-03  
**Status:** bounded refinement stack explored

## Purpose

Continue the persistent-record lane past the initial worldtube-count pilot and
determine whether a small stack of coarse persistent bits can overtake the
node-label baseline while preserving a genuine residual branch-overlap
parameter.

This note supersedes the earlier side-bit note in one important respect:

- the side / packet markers now obey the intended **first-hit family** rule
  instead of being able to accumulate both marker states across later hits

So the current bounded comparison is now based on the corrected semantics.

## Current refinement stack

The current persistent-record family now supports:

- base worldtube-count record
- side bit
- side bit + packet-placement bit
- side bit + packet-placement bit + entry-timing bit

Relevant scripts:

- [persistent_record_overlap_kernel.py](/Users/jonreilly/Projects/Physics/scripts/persistent_record_overlap_kernel.py)
- [persistent_record_matched_compare.py](/Users/jonreilly/Projects/Physics/scripts/persistent_record_matched_compare.py)

Relevant corrected matched log:

- [2026-04-03-persistent-record-side-packet-entry-matched-compare.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-03-persistent-record-side-packet-entry-matched-compare.txt)

## Corrected matched result (`2` seeds, `gamma = 1.0`)

| N | node | side+packet trace | side+packet soft | side+packet+entry trace | side+packet+entry soft |
|---|---:|---:|---:|---:|---:|
| 8  | 0.7971 | 0.8323 | 0.8643 | 0.8323 | 0.8645 |
| 12 | 0.5128 | 0.5284 | 0.5634 | 0.5284 | 0.5627 |
| 18 | 0.7121 | 0.7630 | 0.7217 | 0.7630 | 0.7213 |

Lower purity is better.

## What changed

### Side + packet

After the corrected first-hit semantics, side + packet remains a real
improvement over side alone on the soft-overlap lane.

### Entry timing

Adding the early/late entry bit does **not** move the exact-trace lane on the
bounded slice, but it gives a very small additional lift on the soft-overlap
lane:

- `N = 12`: `0.5634 -> 0.5627`
- `N = 18`: `0.7217 -> 0.7213`

So the refinement direction is real, but the gain is now clearly diminishing.

## Targeted gamma result on the best current architecture

The best current bounded architecture is:

- worldtube counts
- side bit
- packet-placement bit
- entry-timing bit

On the critical `N = 18`, `2`-seed slice:

- exact trace: `0.7630`
- `gamma = 1.0`: `0.7213`
- `gamma = 1.5`: `0.7386`
- `gamma = 2.0`: `0.7490`

So:

- the soft-overlap lane genuinely beats the exact-trace lane
- but tuning `gamma` above `1.0` makes the result **worse**, not better

The overlap law is therefore no longer the main bottleneck on this bounded
slice. The current best soft point already sits near the useful region.

## Safe read

The persistent-record program now has a sharper bounded conclusion:

- a small stack of coarse persistent markers **does** keep improving the
  residual-connection architecture
- the best current row is the side + packet + entry soft lane at
  `N = 18`, `gamma = 1.0`, with `pur = 0.7213`
- but it still does **not** beat the node-label baseline at the same row
  (`0.7121`)

So the honest current read is:

- this architecture family is scientifically alive
- it is getting closer
- but the remaining gap is no longer being closed efficiently by simply adding
  one more coarse bit or retuning `gamma`

## Most useful next move

The next good move is probably **not** another one-bit refinement.

The sharper next frontier is one of:

1. a different overlap kernel that weights marker families unequally rather
   than using one isotropic `exp(-gamma ||r-r'||^2)` distance, or
2. a different record-writing law where the first-hit markers influence later
   record updates instead of merely being carried passively

Those are now more justified than continuing the current one-bit ladder.
