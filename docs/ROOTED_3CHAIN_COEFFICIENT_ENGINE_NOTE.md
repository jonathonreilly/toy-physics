# Exact Rooted `3`-Chain Coefficient Engine for the `3+1` Plaquette Program

**Date:** 2026-04-16  
**Status:** corrected exact rooted same-boundary engine through five `3`-cells;
exact no-go for boundary-shellable growth and directed-cell face-factorization;
exact root-launch sector data through five `3`-cells  
**Script:** `scripts/frontier_rooted_3chain_coefficient_engine.py`

## Question

After the first nonlocal connected coefficient, what is the next exact gauge-side
object needed to close analytic `P`?

## Answer

The right next object is the rooted `3`-chain engine.

Fix the tagged plaquette `q`. Any connected same-boundary surface can be written
as

`S = q + dV`

for a connected `3`-chain `V` with `q in dV`.

So the nonlocal dressing problem is equivalent to enumerating connected rooted
`3`-chains `V` on the exact `3 spatial + 1 time` lattice and organizing them by
their boundary size

`F = |dV|`.

This note does that exactly through `|V| = 5`.

## Important correction: exact rooted growth is not boundary-shellable

An earlier exploratory version of this lane grew `3`-chains by attaching a new
cell only across a **current boundary face**.

That rule is false.

A connected `3`-chain can require adding a cell across a plaquette face that is
temporarily internal and only later reappears in the boundary. So exact rooted
enumeration must grow by **any shared plaquette face of the current cluster**,
not just by the present boundary.

The counts below use that corrected exact connected-growth rule.

## Theorem 1: corrected exact rooted counts through five `3`-cells

Let `N(n, F)` be the number of connected rooted `3`-chains with:

- `|V| = n`
- `q in dV`
- `|dV| = F`

Then the exact counts are:

- `n = 1`:
  - `N(1, 6) = 4`
- `n = 2`:
  - `N(2, 10) = 60`
- `n = 3`:
  - `N(3, 12) = 64`
  - `N(3, 14) = 1036`
  - `N(3, 16) = 64`
- `n = 4`:
  - `N(4, 12) = 32`
  - `N(4, 14) = 112`
  - `N(4, 16) = 2224`
  - `N(4, 18) = 20292`
  - `N(4, 20) = 2340`
- `n = 5`:
  - `N(5, 12) = 64`
  - `N(5, 14) = 56`
  - `N(5, 16) = 1024`
  - `N(5, 18) = 6192`
  - `N(5, 20) = 68160`
  - `N(5, 22) = 421432`
  - `N(5, 24) = 68832`
  - `N(5, 26) = 884`

These are exact integer counts, not Monte Carlo estimates.

## Theorem 2: exact root-launch sector grading through five `3`-cells

Let `k` be the number of occupied `3`-cells in `V` incident to the tagged root
face `q`.

Because `q in dV`, the local incidence parity at `q` must be odd, so only

`k = 1` or `k = 3`

The exact rooted counts above decompose as:

- `n = 1`: `{1: 4}`
- `n = 2`: `{1: 60}`
- `n = 3`: `{1: 1160, 3: 4}`
- `n = 4`: `{1: 24852, 3: 148}`
- `n = 5`: `{1: 562352, 3: 4292}`

So the corrected rooted engine proves something sharper than the old
single-launch picture:

1. the `k = 1` sector is dominant but not complete
2. the `k = 3` rooted multi-launch sector is already present at `n = 3`
3. any honest closure has to retain that exact odd-parity root-face structure

## Corollary: pairwise shared-face grading is not the right exact invariant in `3+1`

An earlier exploratory writeup grouped rooted surfaces by a pairwise
shared-face excess.

That is not an exact invariant for the corrected `3+1` problem.

Reason: a plaquette face can be incident to `3` or `4` occupied `3`-cells, not
just `0`, `1`, or `2`. So boundary size alone does not encode the local
incidence structure by a simple pairwise shared-face count.

The corrected exact invariants recorded by this runner are:

1. total rooted count
2. exact boundary-size histogram `F = |dV|`
3. exact root-incidence sector `k`

Those are the load-bearing exact data for the next closure stage.

## Theorem 3: directed-cell face-factorization already fails at `n = 3`

The simplest rooted closure after the constant-lift no-go is:

> choose one root cell adjacent to `q`, then factorize its `15` outward child
> slots independently.

At `n = 3`, that factorized closure predicts:

- chain term: `4 * 15 * 15 = 900`
- double-child term: `4 * C(15, 2) = 420`

so

- predicted `F = 14` count: `1320`
- predicted `F = 12` count: `0`
- predicted `F = 16` count: `0`

But the exact rooted engine gives:

- exact `F = 14` count: `1036`
- exact `F = 12` count: `64`
- exact `F = 16` count: `64`

Therefore directed-cell face-slot factorization is false.

The first new obstruction after the constant-lift failure is now exact:

> local child branches on a directed cell are already coupled at `n = 3`.

So the next viable closure cannot factorize outward faces. It has to retain at
least the local edge-coupled child motifs on a directed cell boundary.

## Corollary: the first missed generator is local, not asymptotic

The `F = 12` sector at `n = 3` means the next missing ingredient is not a
far-infrared tail or a large-volume subtlety. It is a local rooted generator.

So the closure problem is now sharply posed:

1. corrected exact rooted `3`-chain coefficients are available through `n = 5`
2. the first false closure class is known exactly
3. the next closure must contain both a local directed-cell boundary-cluster
   theorem and a root-face odd-parity launch theorem

That is the correct theory stack after the earlier constant-lift no-go and the
first nonlocal connected coefficient.

## Exact partial locally-resummed plaquette dressing

Let `p = P_1plaq(beta)` denote the exact local one-plaquette block.

Then the corrected exact rooted engine through `n = 5` gives the partial
dressing polynomial

`H_partial(p) = 1`
`+ 4 p^4`
`+ 60 p^8`
`+ 160 p^10`
`+ 1204 p^12`
`+ 3312 p^14`
`+ 26484 p^16`
`+ 70500 p^18`
`+ 421432 p^20`
`+ 68832 p^22`
`+ 884 p^24`.

At the exact local `SU(3)` value

`p = P_1plaq(6) = 0.422531739649983`,

this gives

- `H_partial(P_1plaq(6)) = 1.330208557468936`
- `P_partial^(n<=5)(6) = 0.562055335884644`

This is not yet the full analytic plaquette. It is the exact rooted finite
engine that the real closure has to sum.

## Honest status

This note does **not** yet close full analytic `P(6)`.

What it closes is the next exact theorem gate:

1. the corrected rooted same-boundary gauge problem is now exact through five
   `3`-cells
2. boundary-shellable growth is now exactly dead
3. the first false rooted local closure class is now exactly dead
4. the root-face multi-launch sector is exact through five `3`-cells
5. the remaining closure problem is local and sharply identified

That is materially stronger than the earlier area-`5` coefficient alone, because
the program now knows exactly what kind of rooted operator is still missing.

The physical counting object beyond this raw rooted engine is now identified
exactly by:

- `docs/CUBICAL_QUOTIENT_THEOREM_NOTE.md`
- `docs/QUOTIENT_SURFACE_ENGINE_NOTE.md`

So these rooted counts should now be read as a filling-side precursor to the
quotient-distinct anchored surface gas, not as the final physical counting
engine.

## Commands run

```bash
python3 scripts/frontier_rooted_3chain_coefficient_engine.py
```

Output summary:

- corrected exact rooted counts through `n = 5`
- exact root-launch sector grading through `n = 5`
- exact partial locally-resummed dressing polynomial
- exact no-go against boundary-shellable rooted growth
- exact no-go against directed-cell face-slot factorization at `n = 3`
