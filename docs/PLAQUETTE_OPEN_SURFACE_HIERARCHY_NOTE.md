# Plaquette Open-Surface Hierarchy on the Exact `3+1` Lattice

**Date:** 2026-04-15  
**Status:** exact combinatorial theorem and next derivation program after the constant-lift no-go  
**Script:** `scripts/frontier_plaquette_open_surface_hierarchy.py`

## Question

After the constant-lift closure fails, what exact geometric structure must any
analytic derivation of the plaquette respect?

## Answer

The plaquette is not a one-cell problem. It is an open-surface problem.

The exact local `SU(3)` block still gives the minimal area-`1` surface. But on
the cubic `3 spatial + 1 time` lattice, the very first nonlocal completions of
the same boundary already occur at area `5`, and there are exactly `4` of them.

So any real analytic derivation of `P` has to close an open-surface hierarchy.
It cannot be exact on a single plaquette block alone.

## Theorem 1: same-boundary surfaces differ by a closed `2`-cycle

Fix a plaquette `q`. Let `S` be any `Z_2` plaquette surface with the same
boundary as `q`:

`partial S = partial q`.

Then

`partial (S + q) = partial S + partial q = 0`

mod `2`.

So `S + q` is a closed `2`-cycle.

This is the exact topological statement behind the failure of the local-block
closure: every alternative completion of the plaquette boundary is obtained by
adding a closed surface to the single face.

## Theorem 2: the minimal nontrivial closed `2`-cycle on the cubic lattice has area `6`

On the hypercubic lattice, the smallest nonempty closed plaquette surface is
the boundary of an elementary `3`-cube. It contains exactly `6` plaquettes.

There is no nontrivial closed `2`-cycle with area `< 6`.

So if `S != q` but `partial S = partial q`, then `S + q` must contain at least
`6` plaquettes.

## Corollary: the first nonlocal completion has area `5`

If `S` has the same boundary as `q`, then

`area(S) = area(q) + area(S + q) - 2 area(S cap q)`.

For the minimal nontrivial case, `S + q` is the boundary of an elementary cube
and `q` is one face of that cube. Then:

- `area(q) = 1`
- `area(S + q) = 6`
- `area(S cap q) = 1`

Therefore

`area(S) = 1 + 6 - 2 = 5`.

So the first nonlocal completion of a plaquette boundary is not area `2`, `3`,
or `4`. It is area `5`.

## Theorem 3: on the exact `3+1` lattice there are exactly `4` minimal area-`5` completions

Take a plaquette in plane `(mu, nu)`.

On a `3 spatial + 1 time` lattice there are `4 - 2 = 2` directions orthogonal
to that plane.

For each orthogonal direction `rho`, there are exactly `2` elementary `3`-cubes
having `q` as a face: one on the `+rho` side and one on the `-rho` side.

So the number of distinct elementary cubes containing `q` is

`2 * (4 - 2) = 4`.

Each such cube gives one complementary `5`-face surface with the same boundary
as `q`.

Therefore the first nonlocal layer of the plaquette hierarchy is:

- `1` minimal area-`1` surface
- `4` distinct minimal area-`5` completions

before any larger open surfaces appear.

## Why this matters for analytic `P`

The exact local one-plaquette block captures the area-`1` surface exactly.

But the full gauge theory does not stop there. The same plaquette boundary
already admits `4` distinct multi-plaquette completions at the next geometric
step.

So the constant-lift failure was not accidental. It was structural.

The correct analytic program is:

1. start from the exact gauge source identity  
   `P = (1/N_plaq) d log Z / d beta`
2. rewrite the observable on the pure-gauge Wilson-loop / open-surface side
3. close the resulting hierarchy of same-boundary surfaces

That is the right next theorem stack if `P` is ever to become analytic.

## Honest status

This note does **not** derive `P(beta = 6)`.

It closes something narrower but important:

> the first nonlocal geometry after the local plaquette is exact, minimal, and
> unavoidable. Therefore any real derivation of `P` must be an open-surface
> hierarchy derivation, not a dressed one-plaquette ansatz.

Together with
`docs/GAUGE_PLAQUETTE_SOURCE_NO_GO_NOTE.md`, this gives a clean failure record
for the constant-lift route and a clean statement of the next viable route.

The first constructive theorem on that route is now
`docs/PLAQUETTE_FIRST_NONLOCAL_CONNECTED_CORRECTION_NOTE.md`, which computes
the exact area-`5` cube-complement coefficient `1/472392`.

The next exact rooted layer is now
`docs/ROOTED_3CHAIN_COEFFICIENT_ENGINE_NOTE.md`, which pushes the rooted
same-boundary counts through five `3`-cells, corrects the earlier
boundary-shellable undercount, and shows that a directed-cell face-factorized
closure already fails at `n = 3`.

The exact local closure surface beyond that is now split across:

- `docs/DIRECTED_CELL_BOUNDARY_CLUSTER_THEOREM_NOTE.md`
- `docs/ROOT_FACE_LAUNCH_THEOREM_NOTE.md`
- `docs/DIRECTED_CELL_BOUNDARY_STATE_TRANSFER_NOTE.md`

The hidden-filling sector beyond those local no-gos is now carried by:

- `docs/SAME_BOUNDARY_HYPERCUBE_COMPLEMENT_NOTE.md`
- `docs/CUBICAL_QUOTIENT_THEOREM_NOTE.md`
- `docs/QUOTIENT_SURFACE_ENGINE_NOTE.md`

So the current canonical next route is the quotient-distinct anchored surface
gas, summarized in `docs/ANCHORED_SURFACE_GAS_ROUTE_NOTE.md`.

## Commands run

```bash
python3 scripts/frontier_plaquette_open_surface_hierarchy.py
```

Output summary:

- exact checks: `6 pass / 0 fail`
- elementary same-boundary solutions on one cube: areas `1` and `5`
- exact `3+1` minimal-completion count: `4`
