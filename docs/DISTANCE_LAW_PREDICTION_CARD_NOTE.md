# Distance Law Prediction Card Note

**Date:** 2026-04-05  
**Status:** bounded prediction card for the distance-law story on `main`

## Purpose

This note reconciles the distance-law claim surface into one review-safe card.

The goal is not to sell a continuum theorem.
The goal is to say exactly what the repo can safely claim today, what is only
finite-lattice retained, what is not yet asymptotic, and what remains
branch-side speculation.

## Retained on `main`

The repository now safely retains two distance-law companions:

- compact grown-geometry tail transfer at `h = 0.25`
- wide-lattice ordered `h^2+T` far-tail replay on the retained 3D family

### 1. Compact grown-geometry companion

Relevant note:

- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
- [`docs/GATE_B_H025_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_H025_DISTANCE_LAW_NOTE.md)

Frozen readout:

- exact grid at `h = 0.5`: `20/20` TOWARD, tail `b^(-0.90)`, `R^2 = 0.855`
- grown `drift = 0.2` at `h = 0.5`: `20/20` TOWARD, tail `b^(-0.83)`, `R^2 = 0.884`
- exact grid at `h = 0.25`: `10/10` TOWARD, tail `b^(-0.42)`, `R^2 = 0.855`
- grown `drift = 0.2` at `h = 0.25`: `10/10` TOWARD, tail `b^(-0.54)`, `R^2 = 0.948`

Safe read:

- the far-field tail transfers from the exact grid to the retained grown
  family
- the refined `h = 0.25` replay stays positive and declining
- this is a finite-lattice companion result, not a continuum theorem

### 2. Wide-lattice `h^2+T` companion

Relevant note:

- [`docs/WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md)

Frozen readout on the independent wide replay:

- Born: `4.82e-15`
- `k = 0`: `0.000000`
- distance support: `10/10` TOWARD
- peak-tail fit from `z >= 4`: `b^(-0.95)`, `R^2 = 0.980`
- far-tail fit from `z >= 5`: `b^(-1.05)`, `R^2 = 0.990`
- `F~M` exponent: `1.000`

Safe read:

- the wide-lattice replay is a retained frontier result on `main`
- it is a strong finite-lattice far-tail replay with near-Newtonian behavior
- it is not a continuum-limit proof

## What Is Not Yet Asymptotic

The repository cannot yet safely claim:

- that the far-tail exponent is exactly `-1.00`
- that the wide-lattice replay proves a continuum theorem
- that the distance-law exponent is universal across all windows, widths, or
  generated families
- that the current ordered 3D family has a finalized asymptotic `1/b` law

The safe wording is:

- the repo retains finite-lattice far-field decline on two companions
- one companion is a compact grown-geometry transfer
- one companion is an independent wide-lattice `h^2+T` replay
- neither companion is a universal asymptotic law

## Real Testable Predictions

These are the claims the repo can safely hand to future replays or to a lab
style discriminator:

1. On the retained ordered 3D `h^2+T` family, the far-field rows should stay
   cleanly TOWARD and keep `F~M` near `1` when the same construction is
   replayed with the same family and comparable windows.
2. On the retained grown family, the far-field tail should continue to remain
   positive and declining at `h = 0.25` under the retained moderate-drift row.
3. If the lattice is widened or refined again, any exponent shift should be
   reported as a finite-lattice effect unless a new retained note explicitly
   promotes it.

Those are genuine predictions because they can be rerun and falsified on the
same retained family.

## Branch-Side Speculative Claims

These should stay out of the mainline prediction card until they are retained
on `main` with their own artifact chain:

- any claim that the distance law has converged to a universal continuum
  exponent
- any claim that the far-tail slope is a final model law rather than a finite-
  lattice readout
- any branch-only steepening story that is not yet on `main`

In particular, the safe surface does **not** include a claim that the
distance-law exponent has already settled into a universal `-1.5` or any
other asymptotic constant.

## Final Claim Surface

The exact safe claim surface is:

- compact grown-geometry distance-law transfer is retained on `main`
- wide-lattice ordered `h^2+T` far-tail replay is retained on `main`
- both are finite-lattice far-field results
- neither is yet an asymptotic theorem
- any stronger exponent claim remains branch-side until independently retained

