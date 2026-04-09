# Electric Sign-Law Note

**Date:** 2026-04-04  
**Status:** bounded electric-like sign-law probe on the retained 3D ordered-lattice family

## Artifact chain

- Script: [`scripts/electric_sign_law_harness.py`](/Users/jonreilly/Projects/Physics/scripts/electric_sign_law_harness.py)
- Log: [`logs/2026-04-04-electric-sign-law-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-electric-sign-law-harness.txt)

This is a minimal sign-law test on the same retained ordered-lattice family
used by the derivation lane:

- 3D ordered dense lattice
- `h = 0.5`, `W = 8`, `L = 12`
- source position fixed at `z = 5`
- weak-field charged test packet

## What was tested

The probe asks whether a sign-flipped phase-valley law can represent a
clean electric-like interaction:

- like charges should repel
- unlike charges should attract
- neutral charge should do nothing

The test is intentionally narrow and does not attempt Maxwell theory,
vector fields, gauge symmetry, or radiation.

## Frozen replay

On the retained 3D ordered family:

- source `+1`, test `+1`: repulsion, negative centroid shift
- source `+1`, test `-1`: attraction, positive centroid shift
- source `+1`, test `0`: no measurable shift to printed precision
- source `-1`, test `-1`: repulsion, negative centroid shift
- source `-1`, test `+1`: attraction, positive centroid shift
- source `-1`, test `0`: no measurable shift to printed precision

## Safe read

The strongest retained statement is:

- the same ordered-lattice machinery can represent an electric-like sign law
  if the phase coupling is sign-flipped
- like signs repel and unlike signs attract on the tested weak-field family
- neutral charge is inert to printed precision

What this does **not** establish:

- a full electromagnetic field theory
- Maxwell equations
- gauge structure
- radiation or magnetic effects

## Relation to the existing gravity lane

This is best read as a sign-law companion to the gravity lane:

- gravity: positive phase valley, always attractive
- electric-like sign law: phase hill for like charge, phase valley for unlike charge

The result is interesting because it shows the retained ordered-lattice
machinery can encode signed source coupling, but it does not yet elevate the
project to a full EM theory.
