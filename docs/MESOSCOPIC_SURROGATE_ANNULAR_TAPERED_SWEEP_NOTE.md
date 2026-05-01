# Mesoscopic Surrogate Annular / Tapered Sweep Note

**Date:** 2026-04-04  
**Status:** bounded localization sweep on the 3D mesoscopic surrogate family

## Artifact chain

- Script:
  [`scripts/mesoscopic_surrogate_annular_tapered_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_annular_tapered_sweep.py)
- Log:
  [`logs/2026-04-04-mesoscopic-surrogate-annular-tapered-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-annular-tapered-sweep.txt)

This sweep asks a narrow question:

- can a non-degenerate localized source family beat the broad `topN`
  surrogate on the retained 3D ordered-lattice family if we forbid collapse
  to point-like behavior by construction?

## Frozen setup

- retained 3D ordered-lattice valley-linear family
- base surrogate: `topN = 196`
- source: `z = 3.0`, strength `5e-5`
- explicit floors:
  - support `>= 9` at stage 1 and stage 2
  - capture `>= 0.25` at stage 1 and stage 2

Families compared:

- `topN`
- annular Euclidean shells
- hollow square shells
- tapered ellipsoidal shells

## Frozen result

The admissible frontier is still owned by the broad `topN` control.

### Best admissible rows

- `topN 225`
  - score `1.0000`
  - capture2 `1.000`
  - support2 `225`
  - width ratio `1.0000`

- `annulus 1:5`
  - score `0.9857`
  - capture2 `0.830`
  - support2 `80`
  - width ratio `0.8977`

- `square 1:4`
  - score `0.9733`
  - capture2 `0.806`
  - support2 `80`
  - width ratio `0.8813`

- `tapered`
  - no row met the floors

### Safe comparison

Among the non-degenerate localized families:

- annular shells come closest to the `topN` frontier
- hollow square shells are slightly weaker still
- tapered ellipsoids do not clear the explicit floors at all

But none of the localized families beat the admissible `topN` control on the
score/capture tradeoff.

## Safe read

The honest interpretation is:

- explicit floors successfully block point-like collapse
- the retained 3D family still prefers a broad source surrogate
- localized annular / hollow / tapered families can remain stable, but they do
  not surpass `topN` when the floors are enforced

So this is a bounded negative result, not a new localization breakthrough.

## Relation to the other mesoscopic notes

This note should be read with:

- [`MESOSCOPIC_SURROGATE_LOCALIZATION_SWEEP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_LOCALIZATION_SWEEP_NOTE.md)
- [`MESOSCOPIC_SURROGATE_LOCALIZATION_FRONTIER_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_LOCALIZATION_FRONTIER_NOTE.md)
- [`MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md)
- [`PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/PERSISTENT_INERTIAL_RESPONSE_READINESS_NOTE.md)

Together, these notes say:

- broad mesoscopic source surrogates are real
- support shrinkage alone does not produce a sharp threshold on the retained 2D
  or 3D families
- more structured localized shapes still do not beat the broad `topN` control
  when point-like collapse is excluded

## Best next move

The next honest escalation is no longer another point-source-adjacent
localization search.

The remaining options are:

- try a genuinely different retained family if one is available
- or accept that the mesoscopic surrogate lane closes at a broad-source
  mesoscopic object rather than a sharply localized inertial particle
