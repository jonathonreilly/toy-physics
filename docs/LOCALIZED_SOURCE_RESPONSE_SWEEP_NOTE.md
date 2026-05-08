# Localized Source-Response Sweep Note

**Date:** 2026-04-05  
**Status:** bounded source-response sweep on the 3D `h=0.25` family

## Artifact chain

- Script: [`scripts/localized_source_response_sweep.py`](../scripts/localized_source_response_sweep.py)
- Log: [`logs/2026-04-05-localized-source-response-sweep.txt`](../logs/2026-04-05-localized-source-response-sweep.txt)

This sweep asks a narrow question:

- can any source object materially smaller than the broad mesoscopic control
  still source a field and preserve downstream sourced-response quality well
  enough to matter for the inertial-response lane?

The setup is intentionally the same retained ordered-lattice family used by the
other mesoscopic surrogate controls:

- family: retained 3D ordered lattice
- spacing: `h = 0.25`
- geometry: `W = 10`, `segment L = 12`
- broad control: `topN = 196`
- source location: `z = 3.0`
- field strength: `5e-5`
- explicit floors:
  - support `>= 9` bins in both stages
  - capture `>= 0.25` in both stages

## Frozen result

The log shows:

- broad `topN 196`
  - support2: `196`
  - capture2: `1.000`
  - score: `1.0000`
  - width ratio: `1.0000`
- best smaller admissible row: `topN 169`
  - support2: `169`
  - capture2: `1.000`
  - score: `1.0000`
  - width ratio: `1.0000`

The important comparison is simple:

- no smaller family beats the broad `topN 196` control on this sweep
- the smaller admissible rows can remain source-like and self-similar
- but they do **not** improve on the broad control frontier

## Safe read

The honest conclusion is:

- a materially smaller source object can still remain admissible on the
  retained family
- however, it does not outperform the broad mesoscopic control
- so the localization-to-source-response lane freezes as a bounded negative
  for “smaller beats broad”

This is slightly stronger than the earlier localization closure:

- the smaller source objects are not rejected outright
- they just do not beat the broad `topN` frontier under the same floors

So the best retained read is:

- broad mesoscopic source objects are still the least-bad source-response
  controls on this family
- a smaller object remains possible, but it does not change the frontier

## Relation to the other mesoscopic notes

Read this with:

- [`MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md`](MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md)
- [`MESOSCOPIC_SURROGATE_MULTISTAGE_NOTE.md`](MESOSCOPIC_SURROGATE_MULTISTAGE_NOTE.md)
- [`MESOSCOPIC_SURROGATE_H025_CONSTRAINED_LOCALIZATION_NOTE.md`](MESOSCOPIC_SURROGATE_H025_CONSTRAINED_LOCALIZATION_NOTE.md)
- `PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*)

Together they now say:

- the broad surrogate can source a weak additive field
- it can survive a second sourced-response stage
- smaller source objects can remain admissible on the retained `h=0.25`
  family
- but the broad control still owns the admissible frontier
- the localized persistent-inertial response is still not in hand

## Best next move

The next honest step is **not** more localization on this retained family.

The source-response lane is now frozen as a bounded result:

- smaller source objects exist
- broad control still wins
- the inertial-response gap remains open
