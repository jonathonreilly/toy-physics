# Gate B Weak-Connectivity Note

**Date:** 2026-04-05  
**Status:** bounded weak-connectivity replay on the no-restore grown family

## Artifact chain

- [`scripts/gate_b_weak_connectivity_harness.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_weak_connectivity_harness.py)
- [`logs/2026-04-05-gate-b-weak-connectivity-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-weak-connectivity-harness.txt)

## Question

Can the far-field generated-geometry result survive when we remove the restoring
force and weaken the connectivity rule?

This note freezes one bounded candidate only:

- exact grid control
- no-restore grown geometry with label connectivity
- no-restore grown geometry with weaker forward KNN+floor connectivity

## Safe read

This note is intentionally narrow.

It should be read as a yes/no check on one candidate, not as a broad search
over generated geometry.

The claim to keep if it survives is:

- far-field `TOWARD` gravity and `F~M = 1.00` still hold on the no-restore
  grown family with a weaker position-based forward connectivity rule

The claim to reject if it fails is:

- the far-field generated-geometry result requires the stronger imposed
  connectivity structure and does not carry through a weaker rule

## Frozen result

The bounded replay is clean:

- exact grid: `12/12` TOWARD, `F~M = 1.00`
- no-restore label-NN control: `12/12` TOWARD, `F~M = 1.00`
- no-restore KNN+floor candidate: `0/12` TOWARD, `F~M = 0.00`

So the no-restore part is not the limiting factor by itself. The weaker
connectivity rule is.

## Safe interpretation

- removing the restoring force still leaves the far-field package intact on
  the label-based control
- replacing the label-based connectivity with the weaker KNN+floor rule kills
  the far-field signal on this retained family
- that makes the connectivity bottleneck sharper, not looser

## Relation to Gate B

Read this together with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
- [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)

The generated-geometry story is now becoming a boundary map:

- strong retained far-field row
- companion distance / Born / decoherence support on the moderate-drift family
- one weaker-connectivity candidate that now closes as a bounded negative
