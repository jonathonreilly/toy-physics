# 3D Valley-Linear Action Note

**Date:** 2026-04-04  
**Status:** bounded action-fork note for the ordered-lattice `1/L^2` family

## One-line read

On the fixed 3D ordered-lattice `1/L^2` family at `h = 0.25`, the
valley-linear action `S = L(1-f)` improves the tested mass-law exponent and
distance-tail slope relative to spent-delay while preserving Born and the
TOWARD gravity sign on the retained window.

That makes it a real action fork on `main`, but not a promoted flagship claim
or a finished convergence theorem.

## Primary comparison artifact

Script:

- [`scripts/valley_linear_same_harness_compare.py`](/Users/jonreilly/Projects/Physics/scripts/valley_linear_same_harness_compare.py)

Log:

- [`logs/2026-04-04-valley-linear-same-harness-compare.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-valley-linear-same-harness-compare.txt)

The comparison keeps fixed:

- the 3D ordered dense lattice family
- the `1/L^2` kernel with `h^2` measure
- the slit geometry
- the detector readout
- the field shape

It changes only the action law:

- spent-delay
- valley-linear `S = L(1-f)`

## Heavier companion script

- [`scripts/lattice_3d_valley_linear_card.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_valley_linear_card.py)

This heavier script audits the valley-linear lane more broadly, but it should
be read carefully:

- the fixed-resolution core card is at `h = 0.25`
- the multi-`L` purity / gravity-growth checks are companion checks run at
  `h = 0.5` for speed

So it is a same-family ten-property audit, not a pure “all 10 at one fixed
resolution” theorem card.

## Same-harness comparison result

| action | Born | `k=0` | `F~M` alpha | gravity at `z=3` | TOWARD count | tail |
|---|---:|---:|---:|---:|---:|---|
| spent-delay | `4.20e-15` | `+0.00e+00` | `0.50` | `+0.045346` | `8/8` | `z>=4: -0.52`, `R^2 = 0.951` |
| valley-linear | `4.20e-15` | `+0.00e+00` | `1.00` | `+0.000224` | `8/8` | `z>=4: -0.93`, `R^2 = 0.983` |

## Safe interpretation

- Born remains machine-clean for both actions on the retained family.
- `k=0` remains exactly zero for both actions on the retained family.
- Valley-linear improves the tested mass-law exponent from `0.50` to `1.00`.
- Valley-linear steepens the tested post-peak tail from `-0.52` to `-0.93`.
- Both actions remain TOWARD on the retained `z = 2..9` window.
- Valley-linear also has a much smaller gravity magnitude on the tested
  `z=3` slice, so it is not a simple across-the-board numerical win.

## What is not retained from this note

- “Newtonian gravity is now established”
- “the action is derived from the axioms”
- “convergence under refinement is closed”
- “the valley-linear action replaces the flagship mirror lane”

This note freezes a bounded same-family comparison only.

## Why this matters

The action fork is now on firmer footing because it is no longer only
commit-message narrative. A skeptical reader can now inspect:

1. the same-family comparison
2. the on-disk log
3. the heavier companion script

without having to trust branch prose.
