# Exact No-Go Against One-Shell Face-State Multiset Transfer on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact obstruction theorem  
**Script:** `scripts/frontier_one_shell_face_state_transfer_no_go.py`

## Question

After the exact directed-cell theorem, the exact root-face launch theorem, and
the rejection of the weakest scalar face closure, does a richer closure become
exact if it is allowed to use the **full multiset of exact one-shell local
boundary-face states**?

## Exact answer

No.

Even that still is not enough.

There are rooted connected `3`-chains `V` with:

1. the same exact multiset of one-shell local boundary-face states on `dV`
2. the same boundary-face count
3. different exact next rooted continuation counts

So any transfer law mediated only by the multiset of one-shell local face-star
states is not the exact rooted gauge-vacuum transfer.

## Definition: one-shell local face state

Fix a boundary plaquette face `f`.

Its exact one-shell local neighborhood is:

1. all `3`-cells incident to `f`
2. all `3`-cells incident to any plaquette face of those incident cells

Restrict the rooted cluster `V` to the occupied cells inside that neighborhood.
Then reduce by the full affine stabilizer of a plaquette face.

That stabilizer has exact size `64`, so the resulting one-shell state is a
canonical finite local invariant of the boundary face.

## Theorem 1: exact rooted witness pair at `n = 3`

Among the exact rooted connected `3`-chains with:

- `|V| = 3`
- `q in dV`

there is a witness pair:

`A = {((0,-1,0,0),(0,1,3)), ((0,0,-1,0),(0,2,3)), ((0,0,0,0),(0,1,3))}`

`B = {((0,0,-1,0),(0,1,2)), ((0,0,0,-1),(0,1,3)), ((0,0,0,0),(0,1,2))}`

such that:

1. `A` and `B` each have `16` boundary faces
2. the exact multiset of one-shell local boundary-face states is identical for
   `A` and `B`
3. the shared multiset contains exactly `5` local-state types, with
   multiplicities `8, 4, 2, 1, 1`
4. the exact next rooted continuation counts differ:
   - `N_next(A) = 35`
   - `N_next(B) = 37`

So the exact next step is not determined by the one-shell local boundary-face
multiset.

## Corollary: one-shell local face-state closure is exactly dead

This kills a much broader class of closures than the earlier scalar rejection.

The dead class is:

> any closure in which the rooted continuation law is mediated only by the
> multiset of exact one-shell local states attached to the current boundary
> faces.

That is stronger than ruling out:

- one generic frontier amplitude
- boundary-shellable transfer
- directed-cell face-slot factorization

because it still fails even after one keeps the full exact one-shell local
face-star data.

## Why this matters

This sharpens the remaining obstruction.

The missing object is no longer just “some richer local closure.” The branch
now knows exactly that the missing transfer information cannot be compressed
into one-shell boundary-face multisets.

So any honest next closure has to retain more than local face-star counts. It
has to carry at least some genuinely inter-face or larger-scale boundary
correlation data.

## Honest status

This note does **not** derive analytic `P(6)`.

What it closes exactly is the next false closure class:

1. scalar local face closure is dead
2. one-shell local face-state multiset closure is also dead

That is the cleanest exact statement of the remaining gauge-vacuum obstruction
currently on the branch.

## Commands run

```bash
python3 scripts/frontier_one_shell_face_state_transfer_no_go.py
```

Output summary:

- exact rooted `n = 3` count: `1164`
- exact face stabilizer size: `64`
- witness pair with identical one-shell local boundary-state multiset
- exact next rooted continuation counts: `35` vs `37`
