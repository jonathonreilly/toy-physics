# DM Neutrino Source-Surface Carrier-Side Conclusion

**Date:** 2026-04-18  
**Status:** bounded - bounded or caveated result note
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_carrier_side_conclusion.py`

## Verdict

Carrier-side verdict: `obstruction`.

## Bottom line

The carrier side is not flagship-closed.

But it is no longer open-ended either. On the present science branch, the
carrier-side pressure is exhausted to two explicit split-2 upper-face
neighborhoods:

- the cap neighborhood near
  `(-0.14, 1.188513342509166, 0.0195041737783)`,
- the endpoint neighborhood near
  `(-0.14, 1.188955544069478, 0)`.

Endpoint and split-1 are not the live carrier pressure anymore. On the tested
broad bundle they stay above the preferred recovered floor from the start, and
the broad-window edge hierarchy already collapses the live broad pressure to
split-2.

Split-2 is not diffuse anymore either. The tested broad lower-repair pressure
first collapses to the low-slack edge interval, then to the upper-`m` face,
and then to the two explicit extremals above. The local tested neighborhoods
around those extremals are still transport-incompatible.

So the remaining carrier-side theorem gap is now minimal:

- interval-certified exclusion or dominance on the exact carrier inside those
  two explicit split-2 upper-face neighborhoods.

That is the honest carrier-side stopping point on the current branch.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_neutrino_source_surface_global_dominance_completeness_obstruction_note_2026-04-17](DM_NEUTRINO_SOURCE_SURFACE_GLOBAL_DOMINANCE_COMPLETENESS_OBSTRUCTION_NOTE_2026-04-17.md)
- [dm_neutrino_source_surface_split2_upper_face_local_neighborhoods_candidate_note_2026-04-18](DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_UPPER_FACE_LOCAL_NEIGHBORHOODS_CANDIDATE_NOTE_2026-04-18.md)
