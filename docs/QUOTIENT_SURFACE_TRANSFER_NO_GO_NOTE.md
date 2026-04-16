# Exact No-Go Against Quotient-Surface-Only Rooted Transfer on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact obstruction theorem on the physical quotient object  
**Script:** `scripts/frontier_quotient_surface_transfer_no_go.py`

## Question

After quotienting rooted fillings by exact unit `4`-cube boundary moves, is the
physical same-boundary surface key `dV` enough to support an exact rooted
continuation law?

## Exact answer

No.

The quotient surface key is the correct physical **counting** object, but it is
not a sufficient rooted **transfer** state.

There are same-quotient rooted fillings whose next quotient continuations differ.

## Why this question matters

The cubical quotient theorem fixed the physical object:

`[V] = dV`.

That solved the raw overcount problem.

The next natural hope would be:

> once quotienting is done, perhaps the rooted continuation law closes on the
> quotient surface key alone.

This note proves that hope is false.

## Theorem 1: the first quotient collision is already not set-determined

At `n = 4` there are exactly `80` duplicate quotient classes.

For all `80` of them:

- the two raw representatives have the same quotient surface key
- the next quotient continuation **set** differs

So quotienting by itself does not produce a representative-independent rooted
continuation set.

There is a finer transitional fact:

- the scalar next quotient count is still the same on all `80` classes
- but the next `|dV|` histogram already differs on `32` of them

So by the first quotient collision, the set-level transfer is already dead and
the histogram-level transfer is partially dead.

### Exact `n = 4` witness

The runner exhibits a same-quotient pair:

`A = {((0,0,0,0),(0,1,2)), ((0,0,0,0),(0,2,3)), ((0,1,0,0),(0,2,3)), ((1,0,0,0),(1,2,3))}`

`B = {((0,0,0,0),(0,1,3)), ((0,0,0,0),(1,2,3)), ((0,0,0,1),(0,1,2)), ((0,0,1,0),(0,1,3))}`

with

- `N_next^quot(A) = 39`
- `N_next^quot(B) = 39`

but different next quotient `|dV|` histograms:

- `A`: `{18: 26, 20: 10, 14: 2, 12: 1}`
- `B`: `{18: 26, 20: 10, 12: 2, 14: 1}`

## Theorem 2: by `n = 5` even the scalar quotient continuation count fails

At `n = 5` there are exactly `2848` duplicate quotient classes.

For **every one** of those `2848` classes:

1. the scalar next quotient continuation count differs between the two raw
   representatives
2. the next `|dV|` histogram differs
3. the full next quotient continuation set differs

So by `n = 5` the quotient surface key is not even enough to determine the
coarsest one-step rooted count.

### Exact `n = 5` witness

The runner exhibits a same-quotient pair:

`A = {((0,0,0,0),(0,1,3)), ((0,0,0,0),(1,2,3)), ((0,0,0,1),(0,1,2)), ((0,1,0,0),(0,2,3)), ((1,1,0,0),(1,2,3))}`

`B = {((0,0,0,0),(0,1,2)), ((0,0,0,0),(0,2,3)), ((0,0,1,0),(0,1,3)), ((1,0,0,0),(1,2,3)), ((1,1,0,0),(1,2,3))}`

with:

- `N_next^quot(A) = 47`
- `N_next^quot(B) = 49`

and histograms:

- `A`: `{20: 31, 22: 11, 18: 3, 16: 2}`
- `B`: `{20: 31, 22: 13, 18: 3, 16: 2}`

## Corollary: quotient surface is the right polymer label, not the full rooted state

This sharpens the branch status.

The quotient surface key **is** still the correct physical same-boundary object
for the anchored surface gas.

But it is **not** enough to support a rooted local transfer or a rooted dynamic
program by itself.

So the quotient-surface gas and the rooted quotient transfer are different
problems:

1. the gas counts physical surfaces
2. the rooted transfer still carries hidden filling-sector information

## Why this matters for analytic `P(6)`

This kills another tempting closure class:

> derive `P(6)` by building an exact rooted transfer on quotient surface keys
> alone.

That route is now exactly dead.

The remaining missing object is therefore sharper:

> either a non-rooted finite-`beta` activity theorem directly on the
> quotient-surface gas, or an enriched rooted state that retains the hidden
> filling sector in addition to the quotient surface.

The first constructive version of that enriched-state route is now
`docs/HIDDEN_SHELL_CHANNEL_THEOREM_NOTE.md`, which proves that the `n = 5`
hidden quotient sector collapses to a finite local cube-shell alphabet. The
next exact propagation result is now `docs/HIDDEN_TWO_SHELL_PROPAGATION_THEOREM_NOTE.md`,
which proves that the first rooted image of that sector remains local but lifts
to an exact two-shell defect class rather than staying closed on the bare
one-shell alphabet.

## Honest status

This note still does **not** derive analytic `P(6)`.

It closes the next false closure class on the actual physical quotient object:

1. raw rooted filling transfer is not exact
2. quotient surface key alone is also not an exact rooted transfer state

That materially narrows what the remaining exact closure could even look like.

## Commands run

```bash
python3 scripts/frontier_quotient_surface_transfer_no_go.py
```

Output summary:

- `n = 4`: `80` duplicate quotient classes, all with different next quotient
  sets and `32` with different next `|dV|` histograms
- `n = 5`: `2848` duplicate quotient classes, all with different next scalar
  quotient continuation counts, histograms, and sets
