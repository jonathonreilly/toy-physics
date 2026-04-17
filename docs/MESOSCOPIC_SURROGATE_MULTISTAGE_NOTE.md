# Mesoscopic Surrogate Multistage Note

**Date:** 2026-04-04  
**Status:** bounded two-stage sourced-response extension of the surrogate-source lane

## Artifact chain

- Script: [`scripts/mesoscopic_surrogate_multistage.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_multistage.py)
- Log: [`logs/2026-04-04-mesoscopic-surrogate-multistage.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-multistage.txt)

This note asks the next honest question after the one-step backreaction probe:

- can the broad mesoscopic surrogate survive **two** sourced-response stages
  on the retained 3D ordered-lattice family?

The setup is intentionally narrow:

1. start from the frozen broad `topN = 196` surrogate
2. propagate it through a weak broad-surrogate source field
3. re-identify the output as the next-stage surrogate
4. repeat one more sourced stage

## Frozen result

Frozen on the retained `h = 0.5`, `W = 8`, `segment L = 6` 3D ordered-lattice
family with source at `z = 3.0` and strength `5e-5`:

- stage-1 capture: `0.691`
- stage-2 capture: `0.825`
- stage-1 centroid shift: `+0.00011066`
- stage-2 centroid shift: `+0.00010015`
- delta ratio: `0.905`
- best-shift stage-2 vs stage-1: `0`
- best-shift score: `0.9901`
- width ratio stage-2 / stage-1: `0.8756`

## Safe read

This is the strongest bounded statement:

- the broad surrogate survives a **second sourced-response stage**
- the response stays in the same broad object family
- the centroid shift stays of the same order
- the shape similarity remains very high

The important limit is unchanged:

- this is still a **mesoscopic** surrogate
- it is still not sharply localized
- it is still not a self-maintaining persistent object
- it is still not a persistent-mass theorem

## Relation to the other surrogate notes

This note should be read together with:

- [`MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md)
- [`BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md)
- [`MESOSCOPIC_SURROGATE_SOURCE_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_SOURCE_2D_NOTE.md)
- [`QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md)

Together they now say:

- the surrogate is re-identifiable
- it can be relaunched if it stays broad enough
- it can act as a weak additive source on the retained 3D family
- it can survive a second sourced-response stage on that family
- it still remains a bounded mesoscopic control, not a localized inertial mass

## Best next move

The next honest escalation is:

- try to shrink the source object while keeping the multistage sourced-response
  score high

If that fails, the right conclusion remains:

- mesoscopic source lane: real
- localized persistent-mass lane: still open
