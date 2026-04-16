# Exact Local Directed-Cell Boundary-Cluster Theorem on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact local theorem  
**Script:** `scripts/frontier_directed_cell_boundary_cluster.py`

## Question

What is the exact local boundary problem seen by a single directed `3`-cell
rooted at an incoming plaquette face `q`?

## Answer

It is finite, exact, and already locally coupled.

For one directed root cell with fixed incoming face `q`, the local outward
neighborhood contains:

- `5` outward root faces
- `15` outward child cells
- `2^15 = 32768` raw local child subsets

After quotienting by the full affine stabilizer of the directed root cell that
preserves `q`, the exact local state count is:

`32768 -> 2844`

So the directed local boundary problem really is a finite local theorem.

But it is not a product over the five outward faces.

## Theorem 1: exact directed local neighborhood

Fix

- the incoming plaquette face `q`
- one directed root `3`-cell incident to `q`

Then the root cell has exactly `5` outward boundary faces, and each outward face
admits exactly `3` external neighboring `3`-cells.

Therefore the total outward child-cell count is exactly

`5 * 3 = 15`.

## Theorem 2: exact stabilizer and orbit reduction

The full affine stabilizer of the directed root cell that preserves the incoming
face `q` exactly has size `16`.

Under that stabilizer, the `15` child slots decompose into exact orbit sizes

`4 + 8 + 1 + 2`.

So the raw local child-subset space reduces from

`2^15 = 32768`

to exactly

`2844`

stabilizer-reduced local orbit states.

This is the exact finite local state space for the directed-cell boundary
problem.

## Theorem 3: the local coupling obstruction is already exact at the pair level

Among the `C(15,2) = 105` unordered child pairs:

- `15` pairs lie on the same outward root face
- `16` pairs lie on distinct outward root faces but still share a plaquette
- `74` pairs lie on distinct outward faces and are disjoint

So even before any global transfer is attempted, the exact local boundary
problem is already coupled.

The naive product picture

> five outward faces with three independent child slots each

is false as an exact local theorem.

## Exact local orbit inventory

The exact orbit counts by child number are:

`{0:1, 1:4, 2:17, 3:52, 4:134, 5:266, 6:421, 7:527, 8:527, 9:421,`
`10:266, 11:134, 12:52, 13:17, 14:4, 15:1}`

The exact orbit counts by outgoing frontier-face number begin:

`{5:1, 9:5, 11:4, 13:14, 15:20, 17:46, 19:53, 21:108, 23:141, ...}`

So the local directed theorem does not just say “some couplings exist.” It gives
the exact finite local inventory that any honest transfer has to use.

## Why this matters

This theorem upgrades the previous rooted-engine statement.

Earlier, the branch only knew:

1. the first exact nonlocal connected coefficient
2. the rooted `3`-chain counts through five cells
3. the failure of face-slot factorization

Now the branch also knows the exact finite local directed boundary problem that
replaces that false factorization.

That is the right exact starting point for any real transfer or closure attempt.

## Honest status

This theorem does **not** yet derive full analytic `P(6)`.

What it does close exactly is the local directed-cell boundary theorem:

1. the local outward neighborhood is finite
2. the stabilizer reduction is exact
3. the first local coupling structure is exact

The next question is whether that exact local theorem is sufficient to close the
full rooted same-boundary gauge problem. The branch answer is now recorded in
`docs/DIRECTED_CELL_BOUNDARY_STATE_TRANSFER_NOTE.md`.

## Commands run

```bash
python3 scripts/frontier_directed_cell_boundary_cluster.py
```

Output summary:

- exact `5`-face / `15`-child directed geometry
- exact stabilizer size `16`
- exact orbit-state count `2844`
- exact pair-level local coupling counts `15 / 16 / 74`
