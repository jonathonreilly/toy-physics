# Exact Same-Boundary `4`-Cube Complement Theorem on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact local same-boundary theorem  
**Script:** `scripts/frontier_same_boundary_hypercube_complement.py`

## Question

Once the one-shell local face-state closure is dead, what is the next exact
hidden sector in the rooted `3`-chain problem itself?

## Exact answer

The rooted `3`-chain already has a local same-boundary ambiguity:

> a rooted `3`-cell can be replaced by the `7`-facet complement of any incident
> unit `4`-cube boundary while preserving exactly the same plaquette boundary.

So the next missing object is not just a richer boundary-face transfer. The
rooted volume itself already carries a `4`-dimensional same-boundary completion
sector.

## Theorem 1: exact same-boundary fillings on one incident `4`-cube

Fix one rooted `3`-cell

`c = ((0,0,0,0),(0,1,2))`.

Inside one incident unit `4`-cube, enumerate all subsets of the `8` boundary
`3`-cells and compare their plaquette boundaries to `d c`.

Then the only same-boundary subsets are:

1. the facet `c` itself
2. the `7`-facet complement `∂H \ c`

So on one `4`-cube the exact same-boundary subset-size classes are exactly:

- size `1`: multiplicity `1`
- size `7`: multiplicity `1`

The `7`-facet complement is connected and satisfies

`d(∂H \ c) = d c`.

## Theorem 2: exact rooted multiplicity at the tagged plaquette face

Fix the tagged root face `q`.

Then:

1. `q` is incident to exactly `4` rooted `3`-cells
2. each rooted `3`-cell is incident to exactly `2` unit `4`-cubes

Therefore the exact number of minimal rooted same-boundary hidden completions is

`4 * 2 = 8`.

Each such completion:

- has size `7`
- is connected
- keeps `q` in the boundary
- has exactly the same plaquette boundary as the corresponding rooted `3`-cell

So the exact rooted hidden-completion histogram is:

`{7: 8}`.

## Why this matters

This sharpens the remaining obstruction beyond the one-shell face-state no-go.

That no-go said:

> one-shell local boundary-face data is not enough.

This theorem says something stronger:

> the rooted `3`-chain itself already has a local same-boundary `4`-dimensional
> completion sector.

So any honest closure has to retain more than boundary-face correlations. It
also has to control same-boundary `4`-cube complement replacements in the
rooted volume.

## Relation to the rooted coefficient engine

The corrected rooted engine through `|V| = 5` did not yet reach this sector.

That is why the exact rooted counts through `n = 5` could still be organized by
boundary size and root-launch data without confronting same-boundary volume
ambiguity directly.

This theorem identifies the next exact structural gate after that finite engine:

1. rooted counts through `n = 5`
2. one-shell face-state multiset no-go
3. first hidden same-boundary volume completion: the `7`-facet `4`-cube
   complement

## Honest status

This note does **not** derive analytic `P(6)`.

What it closes exactly is the next missing local sector:

1. the rooted volume has a minimal same-boundary hidden completion
2. that sector is `4`-dimensional and local
3. it appears with exact rooted multiplicity `8`

That is the cleanest exact statement yet of what a real correlated
frontier-state closure still has to sum.

That local hidden sector is now integrated into the exact physical quotient by
`docs/CUBICAL_QUOTIENT_THEOREM_NOTE.md`, which shows the root/complement pair
differs by exactly one unit `4`-cube boundary.

## Commands run

```bash
python3 scripts/frontier_same_boundary_hypercube_complement.py
```

Output summary:

- exact same-boundary subset-size classes on one incident `4`-cube: `1` and `7`
- exact rooted minimal hidden-completion count: `8`
- every rooted hidden completion is connected and preserves `q`
