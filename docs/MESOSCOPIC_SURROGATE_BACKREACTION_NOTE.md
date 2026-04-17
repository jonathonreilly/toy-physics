# Mesoscopic Surrogate Backreaction Note

**Date:** 2026-04-04  
**Status:** bounded source/backreaction extension of the quasi-persistent surrogate lane

## Artifact chain

- Script: [`scripts/mesoscopic_surrogate_backreaction_harness.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_backreaction_harness.py)
- Log: [`logs/2026-04-04-mesoscopic-surrogate-backreaction.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-backreaction.txt)

This is the next honest step after the relaunch/compression controls:

- treat the frozen broad relaunch surrogate as a **distributed source**
- test whether its weak-field response remains additive
- test whether two such surrogates satisfy a bounded one-step two-body symmetry

The goal is not to prove persistent mass. The goal is to check whether the
surrogate is coherent enough to act like a mesoscopic source object at all.

## Frozen result

Frozen on the retained `h = 0.5`, `W = 8`, `segment L = 6` 3D ordered-lattice
family, using the frozen `topN = 196` broad surrogate:

### Same-shape source additivity

- mean relative error: `0.0003%`
- max relative error: `0.0005%`

### Disjoint broad-source additivity

- mean relative error: `0.0068%`
- max relative error: `0.0145%`

### One-step two-body symmetry

- mean violation: `0.2942%`
- max violation: `0.3240%`

The individual frozen rows show the same pattern:

- additive source response stays at the `10^-5` to `10^-4` relative level
- one-step two-body symmetry stays at the few-`10^-3` level

## Safe read

The strongest honest statement is:

- the broad relaunch surrogate can source a **weak additive field**
- the same broad surrogate supports **bounded one-step two-body symmetry**
- so the surrogate is acting like a real **mesoscopic source object**

But the limit remains just as important:

- the surrogate is still broad, not sharply localized
- the experiment is still only one-step and weak-field
- this is **not** a self-maintaining localized inertial object
- this is **not** persistent-mass closure

## Relation to the other surrogate controls

This note should be read with:

- [`ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md)
- [`QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md)

Together they now say:

- packets are re-identifiable
- compressed relaunch surrogates survive if they stay mesoscopic
- the same surrogate idea survives a 2D sanity check
- the broad surrogate can source a weak additive field and participate in
  bounded one-step backreaction
- but the fully persistent inertial-object gap is still open

## Best next move

The next honest step is:

- read this note together with
  [`BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md)
  and
  [`MESOSCOPIC_SURROGATE_SOURCE_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_SOURCE_2D_NOTE.md)
  to bound how point-like the surrogate-source picture really is
- then ask whether the surrogate can survive *another* sourced response stage
  without collapsing into an ordinary broad packet

If those fail, the right read stays bounded:

- useful mesoscopic surrogate
- no persistent-mass theorem
