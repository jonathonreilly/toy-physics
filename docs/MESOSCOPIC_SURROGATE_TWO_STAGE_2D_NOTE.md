# Mesoscopic Surrogate Two-Stage 2D Note

**Date:** 2026-04-04  
**Status:** bounded 2D companion control for a two-stage mesoscopic-surrogate response

## Artifact chain

- Script: [`scripts/mesoscopic_surrogate_two_stage_2d.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_two_stage_2d.py)
- Log: [`logs/2026-04-04-mesoscopic-surrogate-two-stage-2d.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-two-stage-2d.txt)

This is the cheapest retained-family check I could build for the multi-stage
surrogate-source idea.

The question is deliberately narrow:

- if a broad surrogate source is used once to generate a sourced response,
  does the response remain stable enough to be compressed and used again as a
  second-stage source?

## Frozen replay

On the retained `h = 0.5`, `W = 12`, `L = 20` 2D ordered-lattice family:

- the stage-1 broad surrogate is built from the free packet profile
- the stage-2 broad surrogate is built from the stage-1 sourced response
- the printed stage-1 and stage-2 rows are identical to the shown precision
  across the tested `topN` values

For the frozen rows:

- `topN=9`
  - capture: `0.586`
  - source centroid: `+5.510`
  - source spread: `2.148`
  - stage-1 ratio: `0.655`
  - stage-2 ratio: `0.655`
  - carry: `1.000`

- `topN=25`
  - capture: `0.982`
  - source centroid: `+5.361`
  - source spread: `2.894`
  - stage-1 ratio: `0.372`
  - stage-2 ratio: `0.372`
  - carry: `1.000`

- `topN=49` and above
  - capture: `1.000`
  - source centroid: `+5.224`
  - source spread: `3.080`
  - stage-1 ratio: `0.117`
  - stage-2 ratio: `0.117`
  - carry: `1.000`

## Safe read

The strongest honest statement is:

- on this 2D companion family, the broad surrogate acts like a **stable
  mesoscopic fixed-point source control**
- the stage-2 surrogate remains identical to the stage-1 surrogate at printed
  precision for the frozen rows
- that means the surrogate can survive two sourced-response stages without an
  obvious collapse

But the important limit remains:

- the surrogate is still broad, not sharply localized
- the response ratios depend on the surrogate support size
- this is a control result, not a persistent-mass theorem

## Relation to the other surrogate controls

This note should be read together with:

- [`MESOSCOPIC_SURROGATE_SOURCE_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_SOURCE_2D_NOTE.md)
- [`ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md)
- [`QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md)
- [`MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MESOSCOPIC_SURROGATE_BACKREACTION_NOTE.md)

Together they now say:

- packets are re-identifiable
- compressed relaunch surrogates survive if they stay mesoscopic
- broad surrogate sources are stable, but still not point-like in 2D
- the broad surrogate can source a weak additive field and support bounded
  one-step backreaction in 3D
- the 2D two-stage control suggests the surrogate can survive a second sourced
  response stage without obvious collapse
- none of this yet produces a persistent-mass theorem

## Best next move

The next honest step is to ask whether the same two-stage stability can be
made less support-sensitive on a slightly different retained family, or
whether the broad mesoscopic source is already the strongest object this
lane can support.

If the latter, the right read stays bounded:

- stable mesoscopic surrogate source
- no localized inertial-object closure
