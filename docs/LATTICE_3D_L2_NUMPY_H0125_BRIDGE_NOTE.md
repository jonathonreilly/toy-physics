# 3D 1/L^2 Numpy h=0.125 Bridge Note

**Date:** 2026-04-05  
**Status:** bounded continuum-bridge attempt; `h = 0.125` still unresolved on the
current frozen log

## Artifact chain

- [`scripts/lattice_3d_l2_numpy_h0125_bridge.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_numpy_h0125_bridge.py)
- [`scripts/lattice_3d_l2_numpy_h0125_only.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_numpy_h0125_only.py)
- [`logs/2026-04-05-lattice-3d-l2-numpy-h0125-bridge.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-lattice-3d-l2-numpy-h0125-bridge.txt)
- [`logs/2026-04-05-lattice-3d-l2-numpy-h0125-only.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-lattice-3d-l2-numpy-h0125-only.txt)

## Question

Can the retained 3D dense `1/L^2` plus `h^2`-measure lane complete one more
same-family refinement step to `h = 0.125` on a smaller but fixed physical
box, and if so what is the narrowest safe continuum claim?

This wrapper stays deliberately narrow:

- fixed physical family: `phys_l = 6`, `phys_w = 3`, `max_d_phys = 3`
- existing numpy dense-lattice card as the engine
- retained observables only:
  - Born if measured
  - gravity sign
  - `F~M` if the row has enough `TOWARD` points

## Frozen result

The original bridge wrapper still contains completed rows only through `h = 0.25`,
but the focused single-row decision harness now completes the decisive
`h = 0.125` row on the same fixed family:

| `h` | Born | gravity sign | `F~M` | note |
| --- | ---: | --- | ---: | --- |
| `1.0` | `6.65e-16` | `AWAY` | n/a | too few `TOWARD` points |
| `0.5` | `1.66e-15` | `TOWARD` | `0.50` | completed |
| `0.25` | `3.48e-15` | `TOWARD` | `0.50` | completed |
| `0.125` | `6.59e-15` | `TOWARD` | `0.50` | completed via focused single-row harness |

The current fixed-family artifact chain therefore supports:

- Born stays machine-clean on all completed rows
- the sign flips from `AWAY` at `h = 1.0` to `TOWARD` at `h = 0.5`,
  `h = 0.25`, and `h = 0.125`
- `k = 0` stays zero on the focused `h = 0.125` decision harness
- the completed same-family `F~M` readout remains `0.50`, not a clean
  Newtonian `1.00`

## Safe read

The strongest safe statement on current `main` is:

- the numpy wrapper is a useful continuation attempt for the 3D dense
  `1/L^2` lane
- it now gives a clean completed `h = 0.125` row on the fixed smaller
  physical family
- but the weak-field `F~M` readout on this family remains `0.50`, so this is
  still not a Newtonian bridge closure

## Honest limitation

This note is intentionally conservative.

It does **not** promote:

- an `h = 0.125` Newtonian-bridge success claim
- a continuum-limit theorem
- a clean Newtonian mass-law closure on this fixed small family

If a stronger `h = 0.125` continuation exists elsewhere, it still needs its
own tracked script/log/note chain before it should influence the retained
claim surface on `main`.

## Branch verdict

Treat this as a bounded bridge attempt:

- useful as a credibility lane
- still unresolved at `h = 0.125`
- not yet strong enough to change the current moonshot ranking
