# Persistent Object Top4 Multistage Outer Transfer Sweep

**Date:** 2026-04-16  
**Status:** bounded beyond-pocket multistage positive; the proposed_retained exact-lattice
`top4` floor survives on `4/5` one-ring-farther cases, with only the deeper
inward-source row still closed

## Artifact chain

- Script: [`scripts/persistent_object_top4_multistage_outer_transfer_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_top4_multistage_outer_transfer_sweep.py)
- Log: [`logs/2026-04-16-persistent-object-top4-multistage-outer-transfer-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-top4-multistage-outer-transfer-sweep.txt)
- Prior widened-pocket note: [`docs/PERSISTENT_OBJECT_TOP4_MULTISTAGE_TRANSFER_SWEEP_NOTE_2026-04-16.md`](/Users/jonreilly/Projects/Physics/docs/PERSISTENT_OBJECT_TOP4_MULTISTAGE_TRANSFER_SWEEP_NOTE_2026-04-16.md)
- Prior inward-boundary note: [`docs/PERSISTENT_OBJECT_INWARD_BOUNDARY_FLOOR_DIAGNOSIS_NOTE_2026-04-16.md`](/Users/jonreilly/Projects/Physics/docs/PERSISTENT_OBJECT_INWARD_BOUNDARY_FLOOR_DIAGNOSIS_NOTE_2026-04-16.md)

## Question

After the widened-pocket sweep and the inward-boundary floor diagnosis, one
honest transfer question remained:

> does the exact-lattice `top4` multistage floor leave the widened pocket at
> all, or is the route really just a bounded local-family result with a mapped
> inward-source edge?

## Frozen setup

Held fixed:

- exact lattice with `h = 0.25`
- retained multistage floor `top4`
- retained blended readout `blend = 0.25`
- same multistage protocol: `3` updates per segment, `3` chained segments
- same overlap / carry / alpha / drift gates as the prior multistage sweeps

One-ring-farther cases:

- `source0.50`
- `source2.85`
- `width6`
- `length3`
- `length9`

Notes:

- `source2.85` is the farthest valid outward source row before the fixed
  five-node source cluster clips the lattice edge

## Frozen result

### Headline

The exact-lattice `top4` floor does leave the widened pocket.

Totals:

- admissible: `4 / 5`
- failed: `1 / 5`

The only miss is the deeper inward-source row:

- `source0.50`: closed

Everything else survives one ring farther out:

- `source2.85`: open
- `width6`: open
- `length3`: open
- `length9`: open

### Summary table

| case | verdict | retained read |
| --- | --- | --- |
| `source0.50` | closed | inward directional boundary persists one step farther in |
| `source2.85` | open | outward source side still transfers |
| `width6` | open | broader width side still transfers |
| `length3` | open | shorter length side still transfers |
| `length9` | open | longer length side still transfers |

### Why this matters

This is materially stronger than “widened-pocket only.”

The retained multistage floor now survives:

- the farther outward source side
- one farther broader width
- one farther shorter length
- one farther longer length

So the exact-lattice branch is not just a local-patch curiosity. It has a real
bounded transfer region beyond the first widened pocket.

But the failure pattern is also clean:

- `source0.50` stays closed
- the closer inward rows `0.75` and `1.00` were already closed
- the reopened inward rows still start only at `1.25`

So the surviving limit is no longer “does it transfer beyond the current
pocket?” It is now:

> a persistent inward-source directional boundary

## Safe read

This last sweep upgrades the exact-lattice route one more time, then cleanly
stops it.

The strongest honest statement is now:

> the exact-lattice branch has a bounded beyond-pocket transferable multistage
> compact-object floor at `top4`, but it still carries a persistent
> inward-source directional boundary and remains below persistent inertial-mass
> closure.

## What this proves

- the `top4` multistage floor is not confined to the widened local pocket
- the exact-lattice branch now survives `4/5` one-ring-farther transfer cases
- the remaining local/beyond-local limit is sharply concentrated on the inward
  source direction

## What it does not prove

- a direction-independent transfer law
- a self-maintaining inertial mass
- matter closure

## Branch verdict

The exact-lattice branch is now best read as:

> a bounded beyond-pocket compact-object-plus-response regime with a persistent
> inward-source directional boundary

not as:

> merely a widened-pocket positive waiting for one more trivial transfer check.

## Best next move

This is a natural park point.

If the branch is ever resumed, the next work should not be another small width
or readout tweak. It should be either:

1. a direct inward-source directional-law diagnosis
2. or a different self-maintaining object architecture
