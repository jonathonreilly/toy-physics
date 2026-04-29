# Broad Surrogate Point Source Compare Note

**Date:** 2026-04-04 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded interpretive diagnostic comparing broad-source and point-source representations on the upstream 3D ordered-lattice surrogate lane; not a tier-ratifiable persistent-mass, inertial-response, or geometry-generic theorem.

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

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, leaf criticality):

> Issue: the runner cleanly verifies the five-probe broad-source
> versus point-source diagnostic, but the source row is only a
> bounded interpretive diagnostic on an upstream proposed/bounded
> ordered-lattice surrogate lane and has no registered dependencies
> for those carrier and relaunch controls. Why this blocks: a
> hostile physicist can accept max TV distance 0.000051 for the
> scripted probes without accepting a retained persistent-mass,
> inertial-response, or geometry-generic theorem, because the source
> itself says it compares two source representations rather than
> producing a self-maintaining object.

The Status line removes the parser-tripping `proposed_retained` token
and explicitly disclaims the persistent-mass / inertial-response /
geometry-generic interpretation.

## What this note does NOT claim

- A persistent-mass theorem.
- An inertial-response theorem.
- A geometry-generic theorem on broad-source / point-source
  equivalence.
- Audit-clean upstream registration of the carrier and relaunch
  controls.

## What would close this lane (Path A future work)

A retained persistent-mass / inertial-response result would require
a separate registered runner that produces a self-maintaining object,
not a comparison of two source representations.
