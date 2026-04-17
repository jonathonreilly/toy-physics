# Persistent Object Blended Readout Outer Transfer Sweep

**Date:** 2026-04-16  
**Status:** bounded widened local compact-object response positive with a mapped inward-source boundary; still not a persistent inertial-mass closure

## Artifact chain

- Outer sweep script: [`scripts/persistent_object_blended_readout_outer_transfer_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_blended_readout_outer_transfer_sweep.py)
- Outer sweep log: [`logs/2026-04-16-persistent-object-blended-readout-outer-transfer-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-blended-readout-outer-transfer-sweep.txt)
- Boundary script: [`scripts/persistent_object_blended_readout_inner_source_boundary_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_object_blended_readout_inner_source_boundary_probe.py)
- Boundary log: [`logs/2026-04-16-persistent-object-blended-readout-inner-source-boundary-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-16-persistent-object-blended-readout-inner-source-boundary-probe.txt)

## Question

The first blended-readout transfer sweep established one real local positive:

> the exact-lattice `top3` object plus fixed `blend = 0.25` passes on the full
> nearby `6 / 6` family.

That still left the next honest bar open:

> does the same branch survive one ring farther out, or does the current
> positive stop at the immediate neighborhood?

## Frozen setup

Fixed across the outer sweep:

- exact lattice with `h = 0.25`
- compact object class `top3`, with `top2` retained as a boundary check
- fixed blended detector readout `blend = 0.25`
- source strengths `0.001, 0.002, 0.004, 0.008`
- three repeated updates
- same overlap / `TOWARD` / `F~M` / drift gates as the local transfer sweep

Second-ring cases:

1. `source1.0`: `L = 6`, `W = 3`, `source_z = 1.0`
2. `source2.75`: `L = 6`, `W = 3`, `source_z = 2.75`
3. `width5`: `L = 6`, `W = 5`, `source_z = 2.0`
4. `length4`: `L = 4`, `W = 3`, `source_z = 2.0`
5. `length8`: `L = 8`, `W = 3`, `source_z = 2.0`

Follow-up boundary cases on the failing inward-source side:

- `source0.75`
- `source1.00`
- `source1.25`
- `source1.50`

## Frozen result

### Headline

The exact-lattice `top3` branch does widen beyond the immediate neighborhood,
but not uniformly.

Outer second-ring totals:

- `top3`: `4 / 5`
- `top2`: `1 / 5`

The only outer miss is the inward source shift `source_z = 1.0`.

The boundary probe then shows that this is not a one-row fluke:

- `source0.75`: closed
- `source1.00`: closed
- `source1.25`: closed
- `source1.50`: open

So the widened regime has a real inward-source boundary between `1.25` and
`1.50` on the baseline `L = 6`, `W = 3` family.

### Summary table

| case | `top2` | `top3` | verdict |
| --- | :---: | :---: | --- |
| `source1.0` | ❌ | ❌ | closed |
| `source2.75` | ❌ | ✅ | `top3` outer bridge |
| `width5` | ❌ | ✅ | `top3` outer bridge |
| `length4` | ❌ | ✅ | `top3` outer bridge |
| `length8` | ✅ | ✅ | `top2` outer bridge |

### Why the inward miss matters

This is not a generic collapse of the whole branch.

The widened branch survives:

- one farther outward source placement
- one broader width slice
- one shorter length slice
- one longer length slice

So the local exact-lattice object-plus-response regime is genuinely larger than
the first-shell note showed.

But the failure is also not a harmless isolated row.

The inward-source boundary probe says the branch stays closed across three
consecutive inward rows and only reopens at `source_z = 1.50`.

That means the surviving branch is now best read as:

> a widened but source-placement-bounded exact-lattice compact-object response
> regime

rather than:

> an already robust all-direction local transfer law

### Where the compact floor sits

The floor still sits near `top3`.

`top2` remains bounded:

- only `length8` opens
- all other second-ring cases stay closed

So there is still no evidence that the widened regime is narrowing below
`top3` in any general way.

## Safe read

This sweep upgrades the compact-object lane, but only in a bounded way:

- the exact-lattice `top3` branch survives most of the second ring
- the surviving regime is visibly larger than the immediate nearby family
- the first strong outer boundary is now mapped on the inward-source side

So the honest interpretation is:

> the repo now has a widened local exact-lattice compact-object-plus-response
> regime, but it remains source-placement bounded and is still below
> persistent inertial-mass closure.

## What this proves

- the `top3 + blend = 0.25` branch is not confined to the first-shell nearby
  family
- the current positive survives on `4 / 5` second-ring cases
- the first clear outer boundary is a real inward-source boundary, not a vague
  “sometimes it fails” story

## What it does not prove

- a direction-independent local transfer law
- a persistent inertial mass
- matter closure
- transfer beyond the now-mapped widened exact-lattice local regime

## Branch verdict

The persistent-object lane is stronger again:

1. `top3` is a transferable compact source object
2. that object carries a stable weak-field response
3. one retained blended readout transfers on the full nearby family
4. the same branch survives most of the second ring, but has a mapped inward
   boundary

So the correct branch verdict is:

> the compact repeated-update exact-lattice branch is now a widened local
> object-plus-response regime with a known inward-source boundary, not yet a
> closure-grade persistent inertial object law.

## Best next move

The next tight move is now one of:

1. a stronger multi-stage persistence / inertial-response probe on the stable
   `top3` rows that survive the widened regime
2. one farther transfer test beyond the current widened local pocket
3. if those fail quickly, freeze this branch as:
   - widened local exact-lattice compact object
   - bounded widened local object-plus-response transfer
   - no persistent inertial-mass closure
