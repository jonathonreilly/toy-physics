# Persistent Record Matched Compare Note

**Date:** 2026-04-03  
**Status:** bounded matched comparison completed

## Purpose

Compare the persistent-record overlap-kernel pilot against the main earlier
record architectures on the **same generated DAGs**, **same seeds**, **same `k`
band**, and **same post-barrier setup**.

The comparison question is narrower than asymptotic closure:

- does the persistent-record lane actually improve over the earlier record
  lanes on a matched bounded slice, or
- is it only interesting in isolation?

## Artifacts

- Harness:
  [persistent_record_matched_compare.py](/Users/jonreilly/Projects/Physics/scripts/persistent_record_matched_compare.py)
- Full-method matched log on `N = 8, 12`:
  [2026-04-03-persistent-record-matched-compare-full-n8-n12.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-03-persistent-record-matched-compare-full-n8-n12.txt)
- Fast matched log on `N = 8, 12, 18` without the expensive scar lane:
  [2026-04-03-persistent-record-matched-compare-fast-n8-n18.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-03-persistent-record-matched-compare-fast-n8-n18.txt)

## Matched results

### Full compare on `N = 8, 12` (`2` seeds)

| N | node | scar | entangling | persistent trace | persistent `gamma=0.25` | persistent `gamma=1.0` |
|---|---:|---:|---:|---:|---:|---:|
| 8  | 0.7971 | **0.6413** | 0.9383 | 0.8317 | 0.9556 | 0.8672 |
| 12 | **0.5128** | 0.6850 | 0.8050 | 0.5349 | 0.8117 | 0.6099 |

### Fast compare on `N = 8, 12, 18` (`2` seeds; no scar at `N = 18`)

| N | node | entangling | persistent trace | persistent `gamma=0.25` | persistent `gamma=1.0` |
|---|---:|---:|---:|---:|---:|
| 8  | 0.7971 | 0.9383 | 0.8317 | 0.9556 | 0.8672 |
| 12 | 0.5128 | 0.8050 | 0.5349 | 0.8117 | 0.6099 |
| 18 | **0.7121** | 0.8412 | 0.7511 | 0.8641 | 0.7314 |

Lower purity is better.

## What this says

The persistent-record lane is **not** the new raw purity champion.

On the matched bounded slice:

- at `N = 8`, graph-memory scars are strongest
- at `N = 12`, node-label is best and persistent trace is close behind
- at `N = 18`, node-label still beats the persistent lane on raw purity, but
  the persistent `gamma = 1.0` row stays close

So the new lane does **not** justify the strong claim:

- "persistent records plus residual inter-universe connection beat the old
  record models on raw decoherence"

But it does justify a narrower claim:

- the persistent-record overlap-kernel lane is a **competitive middle
  architecture**
- it stays materially better than the entangling-env lane on the matched slice
- and unlike node-label, it preserves an explicit nonzero residual
  branch-overlap structure

That last point matters. The lane is not merely "another environment label."
Its scientific value is:

- branch records are mesoscopic and persistent
- branches are neither fully merged nor forced instantly orthogonal
- residual branch connection is explicit and tunable through `gamma`

## Safe wording

The current safe read is:

- the persistent-record overlap kernel is **not** a raw bounded purity winner
  over node-label on the matched slice
- but it is the first bounded lane in this repo that keeps a genuine
  branch-connection parameter while remaining competitive with the older
  decoherence architectures instead of collapsing into the weak entangling-env
  regime

## Next useful step

The best next move is no longer "does this beat node-label on one small table?"
That answer is already no.

The sharper next question is:

- can one slightly richer persistent record geometry beat node-label **without**
  giving up the residual branch-overlap structure?

The most bounded version is:

1. keep the current worldtube-count record cells
2. add one extra persistent slit-side or packet-side bit
3. rerun the same matched `N = 8, 12, 18` comparison

That is now a more informative next test than broader resweeps of the current
record state alone.
