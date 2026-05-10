# Gate B Non-Label Connectivity V1 Joint Note

**Date:** 2026-04-05 (audit-narrowing refresh: 2026-05-10)
**Type:** bounded_theorem
**Status:** bounded numerical Born / `d_TV` / MI / decoherence comparison
between exact grid and no-restore geometry-sector stencil at `h = 0.5`,
`W = 10`, `NL = 25`, `seeds = 4`, `drift = 0.2`. Frozen on disk.
**Status authority:** independent audit lane only.
**Script:** [`scripts/gate_b_nonlabel_connectivity_v1_joint.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v1_joint.py) (PASS=1, C-class)

## Audit boundary (2026-05-10)

The independent audit verdict on this row is `audited_conditional`. The
runner is non-print-only — it constructs the geometries, propagates
amplitudes, and computes Born / `d_TV` / MI / decoherence directly — and
the bounded numerical comparison itself is supported by that runner output.

The conditional grade comes from non-retained one-hop dependencies:

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
  (`audit_status: audited_conditional`) — base geometry-sector candidate
  this row companions. Conditional.
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — far-field Gate B reference;
  conditional.

This note's load-bearing claim is therefore narrowed to the bounded
numerical Born / `d_TV` / MI / decoherence comparison on the declared
scope. The broader "non-label joint package transfers" reading is recorded
only as a cross-reference, conditional on the upstream rows.

## Artifact chain

- [`scripts/gate_b_nonlabel_connectivity_v1_joint.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v1_joint.py)
- [`logs/2026-04-05-gate-b-nonlabel-connectivity-v1-joint.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-nonlabel-connectivity-v1-joint.txt)

## Question

Starting from the positive geometry-sector stencil candidate, does the
Born / `d_TV` / `MI` / decoherence package stay in the same qualitative regime
as the exact grid on a cheap bounded replay?

This note is intentionally narrow:

- exact grid control
- geometry-sector stencil on the no-restore grown family
- joint-package observables only

## Frozen result

The frozen log is:

- `h = 0.5`
- `W = 10`
- `NL = 25`
- `seeds = 4`
- `drift = 0.2`

Frozen readout:

| geometry | Born | d_TV | MI | decoh |
| --- | ---: | ---: | ---: | ---: |
| exact grid | `0.00e+00` | `0.458` | `0.178` | `17.2%` |
| geometry-sector stencil | `7.23e-16` | `0.453` | `0.204` | `17.5%` |

## Safe read

The bounded statement is:

- the geometry-sector stencil stays Born-clean to machine precision on this
  cheap replay
- the `d_TV` / `MI` / decoherence observables remain in the same qualitative
  regime as the exact grid on this retained family
- this is a bounded companion, not a universal non-label connectivity theorem

## Relation to Gate B (cross-references)

Read this together with:

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
  (`audit_status: audited_conditional`) — base geometry-sector candidate; one-hop dep.
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
  (`audit_status: audited_conditional`) — far-field Gate B reference; one-hop dep.

The bounded numerical observation: on the tested no-restore family, the
geometry-sector stencil stays Born-clean to machine precision and keeps
`d_TV` / MI / decoherence in the same qualitative regime as the exact-grid
control. That is a bounded numerical companion read on the declared scope,
not a "non-label joint package transfers" closure. Promotion past
`audited_conditional` waits on the upstream
`gate_b_nonlabel_connectivity_v1_note` and `gate_b_farfield_note` rows.
