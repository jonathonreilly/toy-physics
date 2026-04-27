# Persistent Inertial Object Probe Note

**Date:** 2026-04-06  
**Status:** diagnosed closure; the proposed_retained ordered family still reduces to broad-surrogate steering, not a persistent-mass object

## Artifact chain

- Script: [`scripts/persistent_inertial_object_probe.py`](/Users/jonreilly/Projects/Physics/scripts/persistent_inertial_object_probe.py)
- Log: [`logs/2026-04-06-persistent-inertial-object-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-persistent-inertial-object-probe.txt)

## Question

Can the retained ordered-lattice family support one object class whose persistence and inertial response are both measurable on the same family?

This note keeps the answer narrow:

- amplitude-level equivalence is already frozen by the earlier equivalence-principle harness
- this probe only asks whether a relaunchable object class can stay identifiable and keep its weak-field response
- the test family is the retained 3D ordered lattice at `h = 0.5`, `W = 8`, `L = 12`

## Frozen result

The probe launches a point packet, reads out the detector-layer profile, and then relaunches compressed `topN` surrogates on the same family.

The sweep is keyed to the same retained family used by the earlier quasi-persistent relaunch control.

The logged conclusion is:

- the narrow `topN` classes are too thin to be honest persistent objects
- no row clears the combined capture/carry/shift thresholds
- the leading broad surrogate row is `topN=361`

That row is the strongest retained surrogate, but it is still broad enough to behave like a surrogate packet, not a persistent inertial mass.

## Safe read

The clean separation is:

1. **Amplitude-level equivalence**
   - already frozen elsewhere on this family
   - global amplitude rescaling is not the issue here

2. **Persistent-mass claim**
   - not closed by this probe
   - the same family does not yield a sharply localized object whose own persistence and inertial response are both measurable

3. **Practical outcome**
   - the retained ordered family supports broad-surrogate steering
   - the strongest row is still a broad mesoscopic relaunch profile

So the lane does **not** yet identify a true persistent inertial object class.

It diagnoses the weaker but real statement instead:

- a broad surrogate can be relaunched
- the broad surrogate can carry the weak-field response
- but the object class remains too mesoscopic to deserve persistent-mass language

## Branch verdict

The persistent/quasi-persistent inertial-object lane is therefore closed as follows:

- amplitude-level equivalence is separate and already frozen
- same-family relaunchability is real
- persistent-mass closure is still absent
- the honest interpretation is broad-surrogate steering on the retained ordered family

## Fastest falsifier

If a future version of this probe finds a much narrower class that still meets the same capture, carry, and response thresholds, then the lane should be reopened.

Until then, the retained family only supports the broad surrogate read.
