# Gate B No-Restore Joint Package Note

**Date:** 2026-04-05  
**Status:** bounded single-seed no-restore Born / interference / decoherence
replay on the same grown-geometry family

## Artifact chain

- [`scripts/gate_b_no_restore_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_no_restore_joint_package.py)
- [`logs/2026-04-05-gate-b-no-restore-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-no-restore-joint-package.txt)

## Question

What survives on the same grown-geometry family if the restoring force is
removed entirely?

This note freezes a single-seed bounded replay of:

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

The bounded read answers a single question:

- how much of the non-gravity joint package survives when `restore = 0`?

## Frozen result

The one-seed replay reports:

- exact grid: Born `2.12e-15`, `d_TV = 0.787`, `MI = 0.568`,
  decoherence `49.4%`
- no restore drift `0.0`: Born `2.12e-15`, `d_TV = 0.787`, `MI = 0.568`,
  decoherence `49.4%`
- no restore drift `0.2`: Born `2.01e-15`, `d_TV = 0.596`, `MI = 0.314`,
  decoherence `1.0%`
- no restore drift `0.5`: Born `1.31e-15`, `d_TV = 0.971`, `MI = 0.811`,
  decoherence `4.3%`

## Safe read

- `restore = 0` with zero drift reproduces the exact-grid package on this seed.
- once drift is turned on, the joint package becomes highly drift-sensitive.
- the no-restore lane is therefore a bounded probe, not a stability claim.

This is the cleanest honest read from the frozen replay.
