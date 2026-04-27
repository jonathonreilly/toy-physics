# Broad Surrogate Point Source Compare Note

**Date:** 2026-04-04  
**Status:** bounded interpretive diagnostic on the proposed_retained 3D ordered-lattice family

## Artifact chain

- Script: [`scripts/broad_surrogate_point_source_compare.py`](/Users/jonreilly/Projects/Physics/scripts/broad_surrogate_point_source_compare.py)
- Log: [`logs/2026-04-04-broad-surrogate-point-source-compare.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-broad-surrogate-point-source-compare.txt)

This diagnostic asks a narrow interpretive question:

- if we build a weak source field from the broad quasi-persistent surrogate,
  does it behave like a soft point source, or does the distributed support
  materially change the downstream response?

The comparison is made against an equivalent-strength point source placed at
the same centroid on the retained valley-linear ordered-lattice family.

## Frozen result

On the retained `h = 0.5`, `W = 8`, `L = 12` family:

- broad surrogate centroid: `z = +0.0000`
- broad surrogate support bins: `33`
- max TV distance between broad-source and point-source responses across the
  tested probe packets: `0.000051`
- best-shift score:
  - broad: `1.000`
  - point: `1.000`
- width ratio:
  - broad: `1.000`
  - point: `1.000`

Across the tested probe packets `z = 0, ±1, ±2`, the broad and point responses
were effectively identical to the printed precision.

## Safe read

The bounded interpretive conclusion is:

- on this retained ordered-lattice family, the broad surrogate acts like a
  soft point source to very high accuracy
- the distributed structure does not materially change the downstream test-
  packet response at this scale
- this is still not a persistent-mass theorem, because it compares two source
  representations for the same broad surrogate family rather than producing a
  self-maintaining object

## Relation to the relaunch controls

This note should be read together with:

- [`ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md)
- [`QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md)

Together they now say:

- localized packets are re-identifiable
- broad relaunch surrogates are viable
- the broad surrogate behaves like a soft point source on the tested 3D
  family
- but none of this yet produces a persistent-pattern inertial theorem

## Best next move

If we want to push the inertial-response lane further, the next honest step is
to ask whether this soft-point-source surrogate can survive another relaunch
stage without collapsing into an ordinary broad packet.
