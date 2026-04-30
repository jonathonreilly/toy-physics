# Lattice NN RG Reconciliation Note

**Date:** 2026-04-03  
**Status:** bounded - bounded or caveated result note

This note reconciles the stronger branch-history story against the current
artifact chain for the nearest-neighbor lattice refinement work.

The goal is not to restate the most optimistic narrative. It is to pin down
what the existing scripts, logs, and retained notes actually support.

Artifacts in the current chain:

- [`docs/LATTICE_NN_CONTINUUM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_CONTINUUM_NOTE.md)
- [`docs/LATTICE_NN_RG_GRAVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_RG_GRAVITY_NOTE.md)
- [`docs/LATTICE_NN_RG_ALPHA_SWEEP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_RG_ALPHA_SWEEP_NOTE.md)
- [`docs/LATTICE_NN_HIGH_PRECISION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_HIGH_PRECISION_NOTE.md)
- [`scripts/lattice_nn_continuum.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_continuum.py)
- [`logs/2026-04-03-lattice-nn-continuum.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-nn-continuum.txt)
- [`logs/2026-04-03-lattice-nn-rg-gravity.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-nn-rg-gravity.txt)
- [`logs/2026-04-03-lattice-nn-rg-alpha-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-nn-rg-alpha-sweep.txt)

## What Is Canonical

The canonical, artifact-backed statement is narrow:

- the raw nearest-neighbor lattice is Born-clean through `h = 0.25`
- the raw kernel does not yet retain a successful `h = 0.125` continuation
- simple spacing-dependent strength laws are suggestive, but they do not yet
  establish a renormalization result
- the best measured alpha in the retained sweep is `1.5`, not `2.0`
- the current evidence supports a finite-resolution refinement trend, not a
  completed continuum theorem

The logs show the same picture:

- the raw refinement run reaches `h = 0.25` and then overflows at `h = 0.125`
- the RG-style gravity probe still fails at `h = 0.125` for all three tested
  schedules
- the alpha sweep only records `alpha = 0, 0.5, 1.0, 1.5`
- at `alpha = 1.5`, gravity is closest to h-independence in the measured pair,
  with `g(0.25) / g(0.5) = 0.858`

## What Is Narrative Only

The stronger branch-history claims should be treated as narrative unless and
until they are reproduced as artifacts:

- `alpha = 2.0` as the decisive renormalization exponent
- "continuum complete"
- "RG solved"
- "fixed point established"

Those phrases are stronger than the current evidence. In the retained chain, the
best-supported reading is still "promising but incomplete."

## What Would Be Needed To Promote RG Beyond Suggestive

To promote the RG story beyond "suggestive," we would need artifact-backed
evidence of all of the following:

- a successful continuation at `h = 0.125` under the chosen scaling law
- a repeatable run that keeps the Born audit clean on the retained window
- a scaling law whose gravity trend stays stable across more than one refinement
  step, not just a single `h = 0.5` to `h = 0.25` pair
- either a verified `alpha = 2.0` sweep or another law that beats it on a clear
  criterion, with the result frozen in logs
- practical runtime or exact-arithmetic continuation so the next spacing is not
  blocked by overflow or timeout

Until that exists, RG is best described as a narrow fixed-point-style probe, not
as a promoted renormalization result.

## Canonical Conclusion

Use this wording:

- the canonical NN result is a Born-clean finite-resolution refinement trend
  through `h = 0.25`
- the RG-style experiments are promising but still incomplete
- the stronger `alpha = 2.0` / "continuum complete" language is not yet
  supported by the current artifact chain
- promotion beyond "suggestive" requires a successful finer-spacing continuation
  plus a reproducible scaling law, not just a good narrative

Do **not** use:

- `alpha = 2.0` as if it were established by the current logs
- "continuum complete"
- "renormalization proven"
- "fixed point established"
