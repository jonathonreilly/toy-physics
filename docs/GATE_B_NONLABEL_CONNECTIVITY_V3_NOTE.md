# Gate B Non-Label Connectivity V3 Note

**Date:** 2026-04-05
**Status:** bounded non-label forward-connectivity candidate on the no-restore
grown family

## Artifact chain

- [`scripts/gate_b_nonlabel_connectivity_v3.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v3.py)
- [`logs/2026-04-05-gate-b-nonlabel-connectivity-v3.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-nonlabel-connectivity-v3.txt)

## Question

Can a local degree-balancing forward-connectivity rule, with no direct
grid-label NN matching, preserve the far-field grown-geometry package on the
retained no-restore family?

This note is intentionally narrow:

- exact grid control
- no-restore label-NN control
- no-restore degree-balanced matching candidate

Only the far-field `TOWARD` fraction and `F~M` scaling are frozen here.

## Safe interpretation

This is a yes/no test of whether the far-field package survives once direct
label matching is removed.

The claim to keep if it survives is:

- local degree balancing can replace direct label-NN matching without losing
  the far-field grown-geometry package

The claim to reject if it fails is:

- the far-field package depends on the direct label-based connectivity rule and
  does not survive a purely local degree-balanced matching rule

## Frozen result

The bounded replay is not a far-field pass:

- exact grid: `12/12` TOWARD, `F~M = 1.00`
- no-restore label-NN control: `12/12` TOWARD, `F~M = 1.00`
- no-restore degree-balanced matching candidate: `10/12` TOWARD, `F~M = 0.75`

## Safe read

The local degree-balancing rule is not yet a viable replacement for direct
label-NN matching on this retained family.

It preserves most far-field sign rows, but it does not keep the `F~M = 1.00`
class cleanly enough to count as a retained Gate B positive.

So the bounded conclusion is:

- non-label degree balancing is promising as a weak forward-structure
  candidate
- it is **not** yet strong enough to replace the label-based far-field
  connectivity rule

## Relation to Gate B

Read this together with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_NO_RESTORE_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NO_RESTORE_FARFIELD_NOTE.md)
- [`docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md)

This note should be promoted only if the non-label candidate keeps the far-
field sign and `F~M` close to the exact-grid or label-control rows. Otherwise
it is a bounded negative for the non-label forward-connectivity idea.
