# Mesoscopic Surrogate Source 2D Note

**Date:** 2026-04-04  
**Status:** bounded 2D companion check for the surrogate-source idea

## Artifact chain

- Script: [`scripts/mesoscopic_surrogate_source_2d.py`](/Users/jonreilly/Projects/Physics/scripts/mesoscopic_surrogate_source_2d.py)
- Log: [`logs/2026-04-04-mesoscopic-surrogate-source-2d.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-mesoscopic-surrogate-source-2d.txt)

This note asks a narrower question than the relaunch controls:

- if a broad relaunch surrogate is promoted to a distributed source on the
  retained 2D ordered-lattice family, does it behave like a soft point source
  or does the breadth of the support materially change the response?

The test is intentionally bounded:

- family: retained 2D ordered lattice
- geometry: `h = 0.5`, `W = 12`, `L = 20`
- probe: off-center packet launched at `y = 5.0`
- comparison: distributed surrogate source vs equivalent-strength point source
  at the same surrogate centroid

## Frozen replay

The surrogate source was built from the free packet profile and compressed to a
top-`N` support on the detector-profile family.

### Source support and response

- `topN=9`
  - capture fraction: `0.586`
  - source centroid: `+5.510`
  - source spread: `2.148`
  - distributed-source response ratio vs point source:
    - `0.655`
    - `0.655`
    - `0.656`

- `topN=25`
  - capture fraction: `0.982`
  - source centroid: `+5.361`
  - source spread: `2.894`
  - distributed-source response ratio vs point source:
    - `0.372`
    - `0.372`
    - `0.372`

- `topN=49` and above
  - capture fraction: `1.000`
  - source centroid: `+5.224`
  - source spread: `3.080`
  - distributed-source response ratio vs point source:
    - `0.117`
    - `0.117`
    - `0.117`

The output spread stays essentially unchanged from the point-source control,
but the centroid shift amplitude drops as the source support broadens.

## Safe read

The bounded companion conclusion is:

- the broad surrogate does **not** behave like a true point source
- it does preserve the downstream response shape well enough to remain a
  meaningful control object
- but its distributed support matters materially for the response amplitude

So the surrogate-source idea is:

- stable as a mesoscopic source control
- not yet a mass-like source theorem

## Relation to the relaunch controls

This note should be read together with:

- [`ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_PACKET_REIDENTIFICATION_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_NOTE.md)
- [`ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ORDERED_LATTICE_QUASI_PERSISTENT_RELAUNCH_2D_NOTE.md)
- [`QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/QUASI_PERSISTENT_RELAUNCH_PROBE_NOTE.md)

Together they say:

- packets can be re-identified after propagation
- relaunch surrogates are viable if they stay broad
- surrogate sources are broad and stable, but their breadth still changes the
  response
- none of this yet yields a persistent-mass theorem

## Best next move

The next honest step is a 3D companion check that asks the same question:

- does the broad surrogate source act like a soft source on the retained 3D
  ordered-lattice family, or does its support also materially change the
  response there?

If the 3D version agrees, the surrogate-source picture is family-generic as a
control.
If it fails, then the 2D result is just a bounded companion, not a general
mesoscopic source law.
