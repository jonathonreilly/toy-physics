# Wide-Lattice `h^2+T` Skeptic Audit Note

**Date:** 2026-04-06  
**Status:** bounded - finite-lattice distance-law replay; not universal distance-law closure

## Audited Target

Primary target:

- [`docs/WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md)

Evidence chain:

- [`scripts/wide_lattice_h2t_distance_replay.py`](/Users/jonreilly/Projects/Physics/scripts/wide_lattice_h2t_distance_replay.py)
- [`logs/2026-04-05-wide-lattice-h2t-distance-replay.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-wide-lattice-h2t-distance-replay.txt)

## What Survives

The replay is genuinely clean on the tested wide slice:

- Born sanity is machine-small: `4.82e-15`
- the `k = 0` null is exact: `0.000000`
- all tested distance rows are `TOWARD`: `10/10`
- the far-tail fit from `z >= 5` is close to Newtonian:
  - `b^(-1.05)`
  - `R^2 = 0.990`
  - `n = 7`
- the `F~M` sweep is linear on the tested source placement:
  - exponent `1.000`
  - all six strengths remain `TOWARD`

That is enough to keep the result as a retained finite-lattice replay.

## What Does Not Survive Promotion

The following claims are not justified by this replay alone:

- exact `1/b` asymptotics
- a continuum-limit theorem
- width independence across wider or narrower ordered families
- geometry-generic behavior outside the specific ordered 3D replay family
- a final-law claim for the distance tail rather than a finite-lattice readout

The fit is close to `-1`, but the evidence still comes from one widened family
and one detector window choice. That is not enough for a universal promotion.

## Missing Controls

The audit still lacks the controls that would make the claim harder to break:

- a second width or refinement check to show the tail does not drift with
  geometry size
- alternate detector windows to test whether the far-tail slope is window
  stable
- alternate source placements to show the `F~M = 1` readout is not a single
  placement artifact
- an independent replay of the same family with a different retained setup
  that preserves the exact nulls while changing the observational window

## Review-Safe Conclusion

The safest phrasing is:

- the wide-lattice replay is a real retained finite-lattice result
- it supports near-Newtonian far-tail behavior on the tested slice
- it does **not** yet justify a continuum theorem or final asymptotic law

## Final Verdict

**retain as finite-lattice frontier; do not promote as universal distance law**
