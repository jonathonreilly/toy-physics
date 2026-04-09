# Gate B Non-Label Connectivity V1 Joint Note

**Date:** 2026-04-05  
**Status:** bounded joint-package companion for the geometry-sector stencil on
the no-restore grown family

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

## Relation to Gate B

Read this together with:

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)

The safe combined picture is now:

- the geometry-sector stencil preserves the far-field package on the no-restore
  grown family
- this joint-package companion says it also keeps the Born / interference /
  decoherence observables in the same qualitative regime on the same cheap
  replay
- that is review-relevant, but still not full Gate B closure
