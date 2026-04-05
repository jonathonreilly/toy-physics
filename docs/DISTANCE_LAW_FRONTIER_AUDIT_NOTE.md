# Distance Law Frontier Audit

**Date:** 2026-04-05  
**Status:** retained frontier on the compact `h = 0.25` grown-geometry tail fit; wide-lattice `h^2+T` claim still exploratory on `main`

## Question

Is there one narrow distance-law claim that can be independently hardened onto
`main` without turning this into a full continuum theory?

This audit compares:

- the retained compact grown-geometry `h = 0.25` tail transfer already on
  `main`
- the branch-side wide-lattice `h^2+T` continuation as a reference only

## Mainline evidence

The retained mainline distance-law companions already say:

- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
- [`docs/GATE_B_H025_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_H025_DISTANCE_LAW_NOTE.md)

Frozen compact-family readout:

- exact grid: `20/20` TOWARD, tail `b^(-0.90)`, `R^2 = 0.855`
- grown `drift = 0.2`: `20/20` TOWARD, tail `b^(-0.83)`, `R^2 = 0.884`

Frozen finer-spacing replay:

- exact grid: `10/10` TOWARD, tail `b^(-0.42)`, `R^2 = 0.855`
- grown `drift = 0.2`: `10/10` TOWARD, tail `b^(-0.54)`, `R^2 = 0.948`

Safe read from the retained family:

- the distance-law tail transfers to the retained grown geometry
- the `h = 0.25` replay remains positive and declining
- this is a bounded refinement companion, not a full continuum theorem

## Branch-side reference

The `claude/distracted-napier` branch contains a wider `h^2+T` distance-law
claim with a far-field tail fit around `1/b^1.1` on a wider lattice window.

That is a useful reference point, but it is **not** yet a retained `main`
claim.

The reason is simple:

- `main` already has a retained compact `h = 0.25` grown-geometry tail fit
- the wide-lattice `h^2+T` result does not yet have a separate retained note /
  log chain on `main`
- without that, the wider claim should stay exploratory

## Final Verdict

The smallest serious distance-law claim that is already hardened on `main` is:

- compact grown-geometry far-field tail transfer at `h = 0.25`

That is a **retained frontier** result.

The broader wide-lattice `h^2+T` / continuum hardening claim is still:

- **exploratory**

It may become the next frontier if the wide-lattice replay is later frozen on
`main`, but it is not yet independently retained here.

## What This Means

The right near-term move is not to broaden into a full continuum theory.
It is to keep the compact retained tail transfer as the hard floor, and only
promote the wide-lattice `h^2+T` story if it earns its own script / log / note
chain on `main`.

