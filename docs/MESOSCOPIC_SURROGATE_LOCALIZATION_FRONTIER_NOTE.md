# Mesoscopic Surrogate Localization Frontier Note

**Date:** 2026-04-04  
**Status:** bounded localization/strength tradeoff map for the 3D mesoscopic surrogate

## Artifact chain

- Script: [`scripts/mesoscopic_surrogate_localization_frontier.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_localization_frontier.py)
- Log: [`logs/2026-04-04-mesoscopic-surrogate-localization-frontier.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-localization-frontier.txt)

This probe follows the two-stage sourced-response result with a sharper question:

- how small can the 3D surrogate source get before the two-stage response stops
  looking like the same object family?

The answer is not a single collapse threshold. It is a **frontier**.

## Frozen result

Frozen on the retained `h = 0.5`, `W = 8`, `segment L = 6` 3D ordered-lattice
family with source at `z = 3.0` and strength `5e-5`.

### Compact but weak corner

- `topN = 9`
  - `capture1 = 0.188`
  - `capture2 = 0.189`
  - `delta1 = +0.00003623`
  - `delta2 = +0.00003570`
  - `delta ratio = 0.985`
  - `best-shift score = 1.0000`
  - `width ratio = 0.9963`

This is extremely stable, but the sourced response is weak.

### Stronger mesoscopic corner

- `topN = 196`
  - `capture1 = 0.691`
  - `capture2 = 0.825`
  - `delta1 = +0.00011066`
  - `delta2 = +0.00010015`
  - `delta ratio = 0.905`
  - `best-shift score = 0.9901`
  - `width ratio = 0.8756`

- `topN = 256`
  - `capture1 = 0.753`
  - `capture2 = 0.847`
  - `delta1 = +0.00010668`
  - `delta2 = +0.00010609`
  - `delta ratio = 0.994`
  - `best-shift score = 0.9901`
  - `width ratio = 0.9250`

This is less localized, but it carries much more source strength while
remaining clearly stable across two stages.

## Safe read

The strongest honest statement is:

- there is **no single sharp collapse threshold**
- smaller sources can remain extremely self-similar while becoming weak
- broader sources can carry stronger response while remaining mesoscopic and
  multistage-stable

So the correct next question is not:

- where is the collapse threshold?

It is:

- can any **more localized** source beat the current tradeoff frontier?

## Relation to the other mesoscopic notes

This note should be read with:

- [`MESOSCOPIC_SURROGATE_MULTISTAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_MULTISTAGE_NOTE.md)
- [`MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md)
- [`BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md)
- [`MESOSCOPIC_SURROGATE_TWO_STAGE_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_TWO_STAGE_2D_NOTE.md)

Together they now say:

- the broad source lane is real
- it composes across two stages in both 3D and 2D companion controls
- and the remaining open problem is no longer generic survival
- it is **beating the localization/strength frontier**

## Best next move

The next honest escalation is:

- search for an explicitly more localized source family that beats the current
  top-`N` frontier in 3D

If that fails, the strongest bounded conclusion becomes:

- mesoscopic source physics is real
- localized persistent-mass closure is likely not available on the retained
  family without changing the object class
