# Gate B Weak-Connectivity Note

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded weak-connectivity numerical replay comparing exact grid,
no-restore label-NN connectivity, and no-restore KNN+floor connectivity at
`h = 0.5`, four seeds, `z = {3, 4, 5}`. Frozen on disk.
**Status authority:** independent audit lane only.
**Script:** [`scripts/gate_b_weak_connectivity_harness.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_weak_connectivity_harness.py) (PASS=3, all C-class)

## Audit boundary (2026-05-10)

The independent audit verdict on this row is `audited_conditional`. The
runner is non-print-only — it builds the lattice families, swaps connectivity
variants, propagates amplitudes, and computes the centroid readout and `F~M`
fit directly — and the bounded weak-connectivity comparison itself is
supported by that runner output.

The conditional grade comes from non-retained one-hop dependencies:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — cited as the upstream far-field
  Gate B reference. Conditional.
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
  (`effective_status: retained_bounded`) — cited for the bounded distance-law
  companion. Retained-bounded, cross-confirmed.
- [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)
  (`audit_status: audited_conditional`) — cited for the joint Born / `d_TV`
  / MI / decoherence bounded comparison. Conditional.

This note's load-bearing claim is therefore narrowed to the bounded
weak-connectivity comparison on the declared scope. The broader "Gate B
package survives weak connectivity" reading is recorded only as a
cross-reference, conditional on the upstream rows.

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

## Relation to Gate B (cross-references)

Read this together with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — far-field Gate B reference; one-hop dep.
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
  (`effective_status: retained_bounded`) — bounded distance-law companion; one-hop dep.
- [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)
  (`audit_status: audited_conditional`) — joint-package bounded comparison; one-hop dep.

The bounded weak-connectivity boundary map this note frozen-replays:

- the bounded harness signature on the no-restore label-NN control matches
  the exact grid (`12/12` TOWARD, `F~M = 1.00`)
- the no-restore KNN+floor candidate fails the harness signature (`0/12`
  TOWARD, `F~M = 0.00`)
- the full "Gate B" reading on either branch remains conditional on the
  upstream `gate_b_farfield_note` row's primitive-to-physical-gravity bridge

That is enough to call the connectivity bottleneck sharp on this comparison;
it is not enough to close full Gate B.
