# Mesoscopic Surrogate Compact Floor Sweep Note

**Date:** 2026-04-04  
**Status:** constrained compact-family control sweep for the retained 3D surrogate lane

## Artifact chain

- Script: [`scripts/mesoscopic_surrogate_compact_floor_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_compact_floor_sweep.py)
- Log: [`logs/2026-04-04-mesoscopic-surrogate-compact-floor-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-compact-floor-sweep.txt)

This sweep is the follow-up to the localization-family negative result.
It asks a tighter question:

- can any compact Gaussian or tapered compact source family beat the broad
  top-N control once we enforce explicit floors that exclude point-like winners?

## Frozen setup

The retained 3D ordered-lattice valley-linear family is unchanged:

- `h = 0.5`
- `W = 8`
- `segment L = 6`
- source at `z = 3.0`
- source strength `5e-5`

The compact families are tested against the same two-stage sourced-response
setup as the earlier surrogate notes.

The floors are:

- support `>= 5` bins in both stages
- capture `>= 0.25` in both stages

That is the key difference from the older localization sweeps:

- point-like or near-point-like winners are excluded by construction

## Result

Frozen result is recorded in the log file linked above.

The summary statement to fill from the frozen run is:

- whether any compact Gaussian family passed the floors
- whether any tapered compact family passed the floors
- whether any compact family improved on the broad top-N benchmark once the floors were enforced

## Safe read

This note is intentionally narrow.

Its job is to decide whether the localization story has a real compact-source
branch after the degenerate point-like cases are removed.

The expected outcomes are:

- if no compact family passes the floors, then the broad top-N control remains
  the least-bad mesoscopic object on the retained 3D family
- if a compact family passes the floors, it still has to beat top-N on the same
  support/capture constraint before we call it an improvement

## Relation to the other mesoscopic notes

Read this with:

- [`MESOSCOPIC_SURROGATE_LOCALIZATION_SWEEP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_LOCALIZATION_SWEEP_NOTE.md)
- [`MESOSCOPIC_SURROGATE_MULTISTAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_MULTISTAGE_NOTE.md)
- [`MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md)
- [`BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/BROAD_SURROGATE_POINT_SOURCE_COMPARE_NOTE.md)

## Best next move

The next honest escalation is one of:

- if the compact families fail the floors, freeze that as the end of the compact branch
- if a compact family passes, compare it directly against top-N under the same floors
