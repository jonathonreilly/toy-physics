# Gate B h=0.25 Joint Package Note

**Date:** 2026-04-05  
**Status:** bounded compact h=0.25 Born / interference / decoherence replay on
the retained grown-geometry family

## Artifact chain

- [`scripts/gate_b_h025_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_h025_joint_package.py)
- [`logs/2026-04-05-gate-b-h025-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-h025-joint-package.txt)

## Question

On the retained 3D `h = 0.25` family, does the grown-geometry package still
track the exact-grid Born / `d_TV` / `MI` / decoherence observables?

This note is intentionally narrow:

- one exact-grid row
- one retained grown row
- single-seed bounded replay

The first attempt at the canonical h=0.25 geometry was too heavy for the
session, so the frozen replay is a smaller compact refinement probe rather
than the full retained-width family.

## Safe read

The purpose here is not to replace the `h = 0.5` grown-geometry package.
It is to ask whether the same generated-geometry family remains admissible at a
finer retained resolution.

The frozen compact replay is:

| geometry | Born | d_TV | MI | decoherence |
| --- | ---: | ---: | ---: | ---: |
| exact grid | `2.62e-15` | `0.850` | `0.655` | `49.8%` |
| grown `drift = 0.2` | `2.94e-15` | `0.916` | `0.770` | `48.8%` |

The bounded read should be interpreted as:

- if the grown `h = 0.25` row stays close to the exact grid, that is evidence
  that the generated-geometry package survives refinement
- if it degrades sharply, that gives a clean bounded negative for the refined
  lane
- the joint-package observables are only being used as a bounded transfer
  check, not as a canonical-family theorem
- on this compact probe, the grown row remains in the same qualitative
  interference/decoherence regime as the exact grid, but it is not a full
  same-family closure proof

## Relation to Gate B

Read this together with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)

The h=`0.25` joint replay is the refinement check for the already retained
`h = 0.5` generated-geometry package. It is not a new architecture, and this
compact probe should not be promoted beyond a bounded refinement check.
