# Mesoscopic Surrogate h=0.25 Constrained Localization Note

**Date:** 2026-04-05  
**Status:** bounded final constrained localization attempt on the 3D `h=0.25` family; broad `topN` remains the best admissible control

## Artifact chain

- Script: [`scripts/mesoscopic_surrogate_h025_constrained_localization.py`](../scripts/mesoscopic_surrogate_h025_constrained_localization.py)
- Log: [`logs/2026-04-05-mesoscopic-surrogate-h025-constrained-localization.txt`](../logs/2026-04-05-mesoscopic-surrogate-h025-constrained-localization.txt)

This is the last non-degenerate localization attempt on the retained `h=0.25`
ordered-lattice mesoscopic surrogate lane.

The question is intentionally narrow:

- build the frozen broad surrogate source from the retained `h=0.25` family
- enforce explicit support/capture floors from the start
- compare the broad `topN` control against a localized annular family

If the annular family still cannot beat the broad `topN` control under the same
floors, the localization lane should close cleanly as a bounded negative result.

## Frozen setup

- family: retained 3D ordered lattice
- spacing: `h = 0.25`
- geometry: `W = 10`, `segment L = 12`
- source: `topN = 196`
- field source: `z = 3.0`
- field strength: `5e-5`
- explicit floors:
  - support `>= 9` bins in both stages
  - capture `>= 0.25` in both stages

Families compared:

- broad `topN`
- annular shell localization

## Frozen result

The log shows:

- `topN 196`
  - stage-1 capture: `0.413`
  - stage-2 capture: `1.000`
  - score: `1.0000`
  - width ratio: `1.000`
- best admissible annulus: `1:6`
  - stage-1 capture: `0.310`
  - stage-2 capture: `0.916`
  - score: `0.9947`
  - width ratio: `0.978`

The final comparison is unambiguous:

- meaningful improvement over topN: `False`
- overall best admissible row: `topN 196`

## Safe read

The honest conclusion is:

- the annular localized family is admissible on the retained `h=0.25`
  family
- but it does **not** beat the broad `topN` control on the same floors
- so the last constrained localization attempt closes as a bounded negative
  result

This is the last clean boundary for the mesoscopic localization lane:

- non-degenerate localization was tried
- explicit floors were enforced from the start
- broad `topN` still owned the admissible frontier

## Relation to the earlier mesoscopic notes

Read this with:

- [`MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md`](MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md)
- [`BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md`](BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md)
- [`MESOSCOPIC_SURROGATE_MULTISTAGE_NOTE.md`](MESOSCOPIC_SURROGATE_MULTISTAGE_NOTE.md)
- [`MESOSCOPIC_SURROGATE_ANNULAR_TAPERED_SWEEP_NOTE.md`](MESOSCOPIC_SURROGATE_ANNULAR_TAPERED_SWEEP_NOTE.md)

Together they now say:

- broad mesoscopic surrogates are real
- they can source weak additive fields and survive multistage sourced-response
- explicit support/capture floors do not rescue a sharply localized source on
  the retained `h=0.25` family
- the localization lane closes at the broad-source control frontier

## Best next move

The next honest step is **not** more localization on this retained family.

The localization lane is now frozen as a bounded negative result.
