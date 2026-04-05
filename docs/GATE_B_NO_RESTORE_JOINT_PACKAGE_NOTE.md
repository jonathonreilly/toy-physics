# Gate B No-Restore Joint Package Note

**Date:** 2026-04-05  
**Status:** bounded no-restore Born / interference / decoherence replay on the
same grown-geometry family

## Artifact chain

- [`scripts/gate_b_no_restore_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_no_restore_joint_package.py)
- [`logs/2026-04-05-gate-b-no-restore-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-no-restore-joint-package.txt)

## Question

What survives on the same grown-geometry family if the restoring force is
removed entirely?

This note freezes:

- Born
- `d_TV`
- `MI`
- CL-bath decoherence

on:

- exact grid
- no-restore grown rows at a few drift values

## Safe read

This note is intentionally narrow.

- It does not claim a full generated-geometry closure.
- It isolates the no-restore lane only.
- It should be read as a companion to the retained restore-based grown-geometry
  notes, not as a replacement.

Once the log lands, the bounded read should answer a single question:

- how much of the non-gravity joint package survives when `restore = 0`?

If the no-restore rows stay close to the exact grid, that supports the claim
that the geometry is not merely being hand-pulled back to the lattice.
If they degrade sharply, that gives a clean bounded negative for the no-restore
lane.
