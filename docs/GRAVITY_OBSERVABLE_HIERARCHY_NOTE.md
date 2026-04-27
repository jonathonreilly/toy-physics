# Gravity Observable Hierarchy

**Date:** 2026-04-04  
**Status:** canonical sign-interpretation note for proposed_retained lattice branches

## Purpose

This note answers one bounded interpretive question:

> If a gravity observable points "away" from mass, can that sign be re-read as
> attraction under a better detector metric?

The answer is:

- **not by convention**
- but **yes, in principle**, if a local mass-side detector observable and a
  global centroid observable disagree

So the right fix is not to flip signs by fiat. The right fix is to use a small
hierarchy of gravity observables.

## The hierarchy

### 1. Signed centroid shift

This is the current standard read:

- compare the detector centroid with and without the mass field
- positive = detector profile shifts toward the mass side
- negative = detector profile shifts away

This is the cleanest single-number summary, but it is global and can hide local
redistribution.

### 2. Mass-side window gain `P_near`

This is the detector-normalized probability gain in a fixed window centered on
the mass-side detector region.

- positive = the detector gets brighter near the mass
- negative = the detector gets dimmer near the mass

This checks whether "toward mass" is actually visible where the mass-side
signal lives.

### 3. Signed channel bias

This is a detector-normalized signed response:

- compare detector probability change on the mass side vs the opposite side
- normalize by total absolute detector change

Interpretation:

- positive = detector change is biased toward the mass side
- negative = detector change is biased away from the mass side

This is the cleanest companion to centroid because it measures **where the
detector reweighting happens**, not just where the overall center lands.

## Interpretation rule

| centroid | `P_near` | channel bias | read |
|---|---|---|---|
| `+` | `+` | `+` or mild `+` | **genuine attraction** |
| `-` | `+` | `+` | **mass-side enhancement with opposite centroid drift** |
| `-` | `-` | `-` | **away / depletion** |
| mixed | mixed | mixed | **mixed / ambiguous** |

The second row is the only case where a negative centroid should be treated as
something other than ordinary "away" behavior.

## Canonical examples

### 2D dense spent-delay, ultra-weak retained pocket

- family: ordered dense lattice, `max_dy = 5`
- slit family: `wide_center`
- strength: `0.0005`

Measured on the same retained barrier card:

- centroid shift: `+0.162694`
- `P_near`: `+0.006099`
- channel bias: `+0.888297`

Interpretation:

- **genuine attraction**

So the retained 2D ultra-weak dense-lattice reopening does **not** need a sign
reinterpretation. The detector moves the right way on all three observables.

### 2D dense spent-delay, strong-field depletion

- same family
- strength: `0.1`

Measured on the same card:

- centroid shift: `-6.538915`
- `P_near`: `-0.102645`
- channel bias: `-0.796165`

Interpretation:

- **away / depletion**

This is the beam-depletion regime. Again, there is no sign ambiguity: all three
observables point the same way.

### 3D power-action close-slit barrier card

- family: retained 3D action-power close-slit barrier card
- strength: `0.0001`

Measured on the retained barrier card:

- centroid shift: `-0.000076`
- `P_near`: `-5.57e-08`
- channel bias: `-0.918368`

Interpretation:

- **away / depletion**

So the retained 3D action-power barrier card also does **not** get rescued by
a better detector observable. Its sign is genuinely away on the current
observable hierarchy.

### 3D dense spent-delay ultra-weak branch

- family: retained 3D dense spent-delay ordered lattice
- strength: `5e-5`
- fixed geometry: `L = 12`, `W = 6`, `h = 1.0`, `max_d = 3`

Measured on the retained barrier card:

- `z = 2`: centroid `+0.003101`, `P_near` `+0.001469`, bias `+0.107097`
- `z = 3`: centroid `+0.001941`, `P_near` `+0.000374`, bias `+0.176381`
- `z = 4`: centroid `+0.001157`, `P_near` `+0.000626`, bias `+0.113676`
- `z = 5`: centroid `+0.000693`, `P_near` `+0.000715`, bias `+0.048601`
- `z = 6`: centroid `+0.000572`, `P_near` `+0.000536`, bias `+0.000112`
- `z = 7`: centroid `+0.000000`, `P_near` `+0.000000`, bias `nan`

Interpretation:

- **genuine attraction** on the retained tested `z = 2, 3, 4, 5, 6` window

So this branch is stronger than the earlier 3D ordered-lattice negative read.
The key point is that the hierarchy, not centroid alone, is what confirms it.

## What this means

1. We should **not** invert gravity sign by convention.
2. We should report at least:
   - centroid shift
   - `P_near`
   - channel bias
3. On the current retained examples:
   - 2D ultra-weak dense spent-delay is **genuinely attractive**
   - 3D action-power close-slit barrier is **genuinely away**
   - 3D dense spent-delay is **genuinely attractive on the retained tested
     `z = 2..6` window**

So the hierarchy sharpens sign interpretation, but it does **not** currently
rescue the retained 3D barrier failure.

## Artifact chain

- [`scripts/gravity_observable_hierarchy.py`](/Users/jonreilly/Projects/Physics/scripts/gravity_observable_hierarchy.py)
- [`logs/2026-04-04-gravity-observable-hierarchy.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-gravity-observable-hierarchy.txt)
- [`docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md)
