# Source-Resolved Generated New Family Note

**Date:** 2026-04-05  
**Status:** real but bounded bridge on a genuinely different generated-family geometry

## Artifact chain

- [`scripts/source_resolved_generated_new_family_probe.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_new_family_probe.py)
- [`logs/2026-04-05-source-resolved-generated-new-family-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-new-family-probe.txt)

## Question

Can a genuinely different generated-family geometry, built to widen support by
construction rather than by a local repair, make the retained exact-lattice
wavefield mechanism matter more than it does on the compact bridge family?

This probe stays narrow:

- compact generated bridge family as the baseline control
- new three-band split-shell family as the tested geometry family
- static Green vs wavefield on each family
- exact zero-source reduction check
- detector effective support `N_eff`
- centroid sign counts and weak-field `F~M` fit

## Frozen result

Exact zero-source reduction survives both families:

- `zero = 0.000e+00`

Aggregated over seeds `0..3`:

| family | mode | `TOWARD` | `F~M` | `N_eff` | support frac |
| --- | --- | ---: | ---: | ---: | ---: |
| bridge | static | `9/16` | `-0.316` | `5.31` | `0.443` |
| bridge | wavefield | `6/16` | `0.098` | `5.14` | `0.432` |
| split-shell | static | `9/16` | `0.304` | `8.38` | `0.510` |
| split-shell | wavefield | `8/16` | `0.381` | `8.30` | `0.512` |

Geometry delta relative to the retained compact bridge:

- static: `delta_TOWARD = +0`, `delta_N_eff = +3.07`, `delta_F~M = +0.620`
- wavefield: `delta_TOWARD = +2`, `delta_N_eff = +3.16`, `delta_F~M = +0.283`

## Safe read

The important result is that the new geometry family is not just another small
bridge tweak.

It does widen support by construction:

- the detector effective support rises from `~5.1` on the compact bridge to
  `~8.3` on the split-shell family
- the support fraction also rises
- the wavefield fit improves relative to the compact bridge

That means the wavefield rule is no longer fighting the same compact-family
bottleneck.

## Honest limitation

This is still not generated-family closure.

- the weak-field mass law is still not cleanly linear
- the split-shell family is broader, but not yet a fully retained closure
- the geometry now looks more promising, but the wavefield gain is still
  modest rather than decisive

## Branch verdict

Treat this as a **real but bounded bridge**:

- the compact generated-family bridge remains closed
- the split-shell family is a genuinely different geometry rule
- it widens support enough for the field rule to matter more
- it does not yet fully restore the weak-field class

So this is a reopening of the generated-family story, but only as a bridge,
not as a closure theorem.
