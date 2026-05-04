# Equivalence Principle Harness Note

**Date:** 2026-04-04  
**Status:** bounded test-particle probe on the proposed_retained 3D ordered-lattice family
**Primary runner:** [`scripts/equivalence_principle_harness.py`](../scripts/equivalence_principle_harness.py) (centroid-ratio amplitude-level EP, runner produces deflection table)

## Artifact chain

- Script: [`scripts/equivalence_principle_harness.py`](/Users/jonreilly/Projects/Physics/scripts/equivalence_principle_harness.py)
- Log: [`logs/2026-04-04-equivalence-principle-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-equivalence-principle-harness.txt)

This is a narrow probe on one fixed family:

- 3D ordered dense lattice
- `h = 0.5`, `W = 8`, `L = 12`
- external mass at `z = 5`
- action compared on the same family: `valley-linear` and `spent-delay`

## What was tested

The harness separates two different statements:

1. **Amplitude-scaling invariance**
   - scale the entire initial packet by a global factor `c`
   - ask whether the centroid shift changes

2. **Packet-shape dependence**
   - keep the packet centered at the same location
   - compare normalized packets with different internal width/shape
   - ask whether the centroid shift stays the same

## Frozen replay

### 1. Amplitude scaling

For both actions, the centroid shift is invariant under global amplitude
rescaling to machine precision:

- valley-linear: identical `delta = +0.00016872` for amplitudes `0.5, 1, 2, 5`
- spent-delay: identical `delta = +0.03481763` for amplitudes `0.5, 1, 2, 5`

This is an exact structural consequence of the linear propagator on this family.

### 2. Packet shape

For both actions, normalized packet shape matters strongly:

| Packet | Valley-linear `delta` | Spent-delay `delta` |
|---|---:|---:|
| point | `+0.00016872` | `+0.03481763` |
| gauss3 | `+0.00012421` | `+0.02579524` |
| flat3 | `+0.00008312` | `+0.01756582` |
| gauss5 | `+0.00008353` | `+0.01748646` |
| flat5 | `+0.00001697` | `+0.00390763` |

Relative spread across the tested packet shapes:

- valley-linear: `159.21%`
- spent-delay: `155.21%`

## Safe interpretation

The clean retained statement is:

- **linearity gives an amplitude-level equivalence statement**
  - global amplitude scaling cancels exactly in the centroid ratio
  - this is action-independent on the tested family

The harness also shows what linearity does **not** give:

- it does **not** make extended localized states composition-independent
- internal packet shape changes the response strongly on the tested family

So this result does **not** close the persistent-pattern / inertial-mass gap.

## What this means for the Newton derivation

This harness narrows Principle 3 sharply:

- trivial statement now supported:
  - global amplitude is not an independent inertial parameter in the test-particle regime
- still open:
  - whether a persistent localized pattern has an effective inertial mass
  - whether that inertial mass is the same parameter as its gravitational charge

## Best next experiment

The smallest viable next step is **not** another amplitude test.

It is:

- build the smallest persistent or quasi-persistent localized pattern the
  current lattice code can support
- measure its response to an external field under a controlled kick or drift
- compare that effective inertial response against the parameter that sets the
  field it sources

Until that exists, the equivalence-principle side is only closed at the
test-particle amplitude level, not at the persistent-pattern level.
