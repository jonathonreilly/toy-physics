# Ordered-Lattice Packet Re-Identification Note

**Date:** 2026-04-04  
**Status:** bounded control for the persistent/quasi-persistent inertial-response lane

## Artifact chain

- Script: [`scripts/ordered_lattice_packet_reidentification.py`](/Users/jonreilly/Projects/Physics/scripts/ordered_lattice_packet_reidentification.py)
- Log: [`logs/2026-04-04-ordered-lattice-packet-reidentification.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-ordered-lattice-packet-reidentification.txt)

This is the smallest honest control I could build on the retained ordered-
lattice family:

- a localized Gaussian packet is launched on the source layer
- the packet is propagated with and without a weak external field
- the final packets are compared by centroid shift, width ratio, and best-shift
  similarity

Frozen result on the retained `h = 0.5`, `W = 8`, `L = 12` family:

- `valley-linear`
  - mean best-shift score: `1.000`
  - mean width ratio: `1.000` for the weakest field and `1.000` to `0.994`
    across the tested field strengths
- `spent-delay`
  - mean best-shift score: `1.000`
  - mean width ratio: `0.997` to `0.994` across the tested field strengths

Interpretation:

- the packet remains easily re-identifiable after propagation
- `valley-linear` keeps the packet shape almost exactly fixed on this control
- `spent-delay` broadens only slightly, but still does not destroy packet
  identity

The probe is intentionally narrow:

- 3D ordered lattice
- `h = 0.5`, `W = 8`, `L = 12`
- weak field sourced at the retained interior mass layer
- comparison of `valley-linear` and `spent-delay`

## What it tests

The question is not “does the packet move?”

The question is:

- can the packet be re-identified well enough after propagation that one could
  even begin talking about an inertial-response measurement?

That requires at minimum:

1. a recognizable packet shape
2. a stable centroid relation to the free baseline
3. a similarity score high enough that the packet is not just diffusing into a
   new object

## Safe read

This control is only useful if it keeps the packet shape recognizable.

The strongest possible outcomes are:

- high best-shift similarity
- modest width change
- a clean centroid displacement relative to the free baseline

On the retained family, the control is strong enough to say:

- a localized packet can be re-identified after propagation
- that makes a future inertial-response probe plausible
- but it still does **not** produce a persistent-pattern inertial-response
  experiment

If a future variant loses the packet shape or the best-shift score drops, then
the ordered-lattice family still does not have a usable inertial-response
object.

## Relation to the readiness note

This note is the natural follow-on to
[PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md](/Users/jonreilly/Projects/Physics/docs/PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md):

- readiness note: why the codebase was not yet ready
- this note: the smallest actual control to check whether re-identification is
  good enough to proceed

The relaunch companion is:

- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md)

## Best next move

If the control is strong enough, the next step is a real persistent or
quasi-persistent inertial-response probe.

If it is not, the honest next step is to keep the readiness note and stop
promising a persistent-mass test that the codebase cannot yet support.
