# Fixed Field Grown Transfer Scout Note

**Date:** 2026-04-06  
**Status:** proposed_retained narrow grown-geometry signed-source positive

## Artifact chain

- [`scripts/fixed_field_grown_transfer_scout.py`](/Users/jonreilly/Projects/Physics/scripts/fixed_field_grown_transfer_scout.py)
- [`logs/2026-04-06-fixed-field-grown-transfer-scout.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-fixed-field-grown-transfer-scout.txt)
- companion grown-geometry control:
  [`docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md)
  and
  [`logs/2026-04-06-grown-geometry-complex-action-companion-replay.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-grown-geometry-complex-action-companion-replay.txt)

## Question

Does the retained grown geometry row carry a bounded signed-source transfer
signal outside exact-lattice pockets, while still reducing exactly to the
zero-source baseline where applicable?

This scout is intentionally narrow:

- retained grown geometry row only: `drift = 0.2`, `restore = 0.7`
- fixed-field propagation, no graph update
- one interior source layer and one final-layer detector centroid
- exact zero-source and neutral same-point cancellation checks
- small superposition / linearity sanity pass

## Frozen Result

Single-seed retained run (`seed = 0`) on the grown row:

| case | source(s) | delta_z mean | sign | read |
| --- | ---: | ---: | ---: | --- |
| zero source field | `none` | `+0.000000e+00` | `ZERO` | `zero` |
| single `+1` | `+1@3.0` | `-1.594422e-04` | `AWAY` | `repel` |
| single `-1` | `-1@3.0` | `+1.594790e-04` | `TOWARD` | `attract` |
| neutral same-point `+1/-1` | `+1@3.0 + -1@3.0` | `+0.000000e+00` | `ZERO` | `null` |
| like pair `+1/+1` | `+1@2.0 + +1@4.0` | `-2.159862e-04` | `AWAY` | `repel` |
| dipole `+1/-1` | `+1@2.0 + -1@4.0` | `+1.810494e-05` | `TOWARD` | `partial-cancel` |
| double `+2` | `+2@3.0` | `-3.188474e-04` | `AWAY` | `linear` |

Reduction / linearity checks:

- zero-source field delta: `+0.000000e+00`
- neutral same-point `+1/-1` delta: `+0.000000e+00`
- single `+1` vs double `+2` charge exponent: `1.000`

Grown-geometry control cross-check from the companion replay:

- exact `gamma = 0` reduction delta: `+2.460475e-01`
- Born proxy on seed `0`: `|I3|/P = 1.456e-15`
- weak-field `F~M` on the checked grown-row sweep: `1.000`

## Safe Read

The narrow, honest statement is:

- the retained grown row preserves the scalar sign response in the fixed-field scout
- zero-source and neutral same-point controls reduce to printed zero
- the single-source response is approximately linear in source charge
- the companion grown-geometry control stays exact at `gamma = 0` and Born-clean
- this is a bounded grown-geometry transfer positive, not a geometry-generic theorem

## What This Is Not

- It is not full electromagnetism.
- It is not a Maxwell derivation.
- It is not a geometry-independent transfer claim.

## Final Verdict

**retained narrow grown-geometry signed-source positive**
