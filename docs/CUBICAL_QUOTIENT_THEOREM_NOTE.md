# Constructive Cubical Quotient Theorem for Rooted `3`-Chains on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact constructive quotient theorem  
**Script:** `scripts/frontier_cubical_quotient_theorem.py`

## Question

What is the correct physical quotient object after the rooted `3`-chain route
encounters same-boundary hidden fillings?

## Exact answer

The rooted filling is not physical data.

For finite rooted `3`-chains `V` and `W` on the `3 spatial + 1 time` cubic
lattice,

`dV = dW`

if and only if

`V + W`

is a finite closed `3`-chain, and that closed `3`-chain is the boundary of a
finite `4`-chain `X` over `F_2`:

`V + W = dX`.

So the canonical quotient object is the plaquette-boundary class itself,
equivalently the same-boundary surface key

`dV`.

## Theorem 1: same boundary implies a finite `4`-cube boundary witness

Fix two finite rooted `3`-chains with the same plaquette boundary.

Then their symmetric difference `V + W` has empty plaquette boundary, so it is
a finite closed `3`-chain.

The runner builds the exact finite `C_4 -> C_3` boundary matrix on a support
box and solves

`dX = V + W`

over `F_2` by deterministic lexicographic elimination.

That produces an explicit finite set of unit `4`-cubes whose boundary equals
the difference.

## Theorem 2: the hypercube-complement witness is exactly one `4`-cube boundary

The local same-boundary hidden-completion theorem already gave:

1. one rooted `3`-cell
2. the `7`-facet complement of that cell inside one incident unit `4`-cube

with the same plaquette boundary.

The constructive quotient runner shows that their difference is exactly the
boundary of that single unit `4`-cube.

So the local hidden-completion sector is not just qualitatively quotient-like.
It is literally one elementary `4`-cube boundary move.

## Theorem 3: the first rooted duplicate pair at `n = 4` is also one `4`-cube move

The first quotient collision in the rooted engine occurs at `n = 4`.

For the first exact duplicate pair found by the runner:

- both rooted fillings have the same plaquette-boundary key with `|dV| = 14`
- their symmetric difference has size `8`
- the exact filling witness is one unit `4`-cube

So the first rooted overcount is already an elementary cubical quotient move.

## Exhaustive finite-box checks

The runner also exhausts all closed `3`-chains in two small boxes:

1. one unit `4`-cube box
2. two adjacent unit `4`-cubes in a `2 x 1 x 1 x 1` box

In both cases, every closed `3`-chain is exactly fillable by the available
unit `4`-cubes:

- one-cube box: `2 / 2`
- two-cube box: `4 / 4`

That is not the general proof by itself, but it is a constructive audit of the
exact elimination machinery used for the rooted witnesses.

## Corollary: the canonical quotient key is `dV`

Because same-boundary rooted fillings differ exactly by finite `4`-cube
boundaries, the physical quotient key does not need an auxiliary rooted normal
form.

The exact canonical class representative is simply the sorted plaquette-boundary
key

`dV`.

That key is box-independent once the support contains the rooted filling.

## Why this matters

This is the step the earlier rooted program was missing.

Before this theorem, the branch knew that hidden same-boundary fillings existed.
After this theorem, the branch knows the correct physical object:

> anchored same-boundary plaquette surfaces modulo exact `4`-cube boundary
> moves.

So the next counting engine must count quotient-distinct surfaces, not raw
rooted fillings.

## Honest status

This note still does **not** derive analytic `P(6)`.

What it closes exactly is the quotient problem:

1. same-boundary rooted fillings are exactly equivalent under finite sums of
   unit `4`-cube boundaries
2. the local hypercube-complement sector is exactly one such move
3. the first rooted overcount at `n = 4` is also one such move

That is the exact bridge from the raw rooted engine to the physical
quotient-surface engine.

## Commands run

```bash
python3 scripts/frontier_cubical_quotient_theorem.py
```

Output summary:

- same-boundary root/complement witness: one unit `4`-cube
- first rooted `n = 4` duplicate witness: one unit `4`-cube
- exhaustive finite-box checks: `2/2` and `4/4` closed chains fillable
