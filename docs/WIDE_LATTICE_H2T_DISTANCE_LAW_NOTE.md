# Wide-Lattice h^2+T Distance-Law Note

**Date:** 2026-04-05  
**Status:** proposed_retained frontier on an independent wide-lattice replay of the
ordered 3D `1/L^2` family

## Artifact chain

- [`scripts/wide_lattice_h2t_distance_replay.py`](/Users/jonreilly/Projects/Physics/scripts/wide_lattice_h2t_distance_replay.py)
- [`logs/2026-04-05-wide-lattice-h2t-distance-replay.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-wide-lattice-h2t-distance-replay.txt)

## Question

Does the branch-side wide-lattice `h^2+T` distance-law claim survive an
independent replay on `main` when we keep the same ordered 3D `1/L^2`
geometry family but freeze the wider `W = 12`, `h = 0.25` slice?

This note is intentionally narrow:

- one wide-lattice ordered 3D family
- valley-linear action
- `1/L^2` kernel with `h^2` measure
- distance tail plus the minimal sanity checks needed to promote it

## Frozen result

Independent wide replay at `h = 0.25`, `W = 12`, `L = 12`:

- Born: `4.82e-15`
- `k=0`: `0.000000`
- distance support: `10/10` TOWARD
- peak-tail fit from `z >= 4`: `b^(-0.95)`, `R^2 = 0.980`, `n = 8`
- far-tail fit from `z >= 5`: `b^(-1.05)`, `R^2 = 0.990`, `n = 7`
- `F~M` exponent: `1.000`

The important qualitative read is:

- the wide-lattice replay is cleanly attractive on all tested distance rows
- the far tail stays close to Newtonian
- the mass scaling remains linear
- the result is independently reproduced on `main`, not just borrowed from the
  branch summary

## Safe read

The strongest honest statement is:

- the wide-lattice `h^2+T` replay is now a **retained frontier** result on
  `main`
- it is a strong finite-lattice replay with near-Newtonian far-tail behavior
- it is **not** yet a universal theorem or continuum-limit proof

## What this is not

- It is not a proof that the far-tail exponent is exactly `-1.00`.
- It is not a continuum theorem.
- It is not a replacement for the already-retained compact grown-geometry
  frontier.

The review-safe wording is:

- the wide-lattice replay strengthens the 3D `h^2+T` distance-law story
- the far tail is now independently reproducible on `main`
- the branch-side wide-lattice claim is no longer just exploratory

## Final Verdict

**retained frontier**

