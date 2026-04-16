# Exact Root-Face Launch Theorem on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact local theorem  
**Script:** `scripts/frontier_root_face_launch_cluster.py`

## Question

Once the directed local theorem is known, what is the exact launch structure on
the plaquette face itself?

## Answer

The face launch is parity-constrained, and it already contains both one-cell and
three-cell sectors.

This matters because a single directed-cell launch only captures the one-cell
sector. It cannot close the full rooted same-boundary problem by itself.

## Theorem 1: exact root-face launch sectors

Fix the tagged plaquette face `q`.

On the exact `3+1` lattice, `q` is incident to exactly `4` different `3`-cells.

For a `3`-chain `V` to keep `q` in its boundary, the number of occupied
`3`-cells incident to `q` must be odd. So the allowed local launch sectors are:

- `1` incident cell
- `3` incident cells

The exact counts are:

- `4` one-cell launches with
  - `|dV| = 6`
  - `5` outgoing frontier faces
- `4` three-cell launches with
  - `|dV| = 16`
  - `15` outgoing frontier faces

So the exact structural root-face launch polynomial is

`H_root(z,p) = 1 + 4 p^4 z^5 + 4 p^14 z^15`.

## Theorem 2: exact generic frontier-face launch sectors

Now fix a frontier face whose parent cell is already occupied on one side.

There are only `3` exterior incident `3`-cells left.

Again odd exterior parity is required, so the allowed generic launch sectors are:

- `1` exterior cell
- `3` exterior cells

The exact counts are:

- `3` one-cell launches with
  - `|dV| = 6`
  - `5` outgoing frontier faces
- `1` three-cell launch with
  - `|dV| = 16`
  - `15` outgoing frontier faces

So the exact structural generic launch polynomial is

`H_gen(z,p) = 1 + 3 p^4 z^5 + p^14 z^15`.

## Corollary: single directed-cell launch is not the full local face theorem

The directed-cell theorem is still real and important, but it only sees the
sector where exactly one launch cell is chosen at a face.

This note closes the next exact obstruction:

> even locally, a frontier face already has a genuine three-cell launch sector.

Therefore the full local boundary problem is face-centered before it is
directed-cell centered.

## Why this matters for the transfer problem

The rooted-engine data already showed that the first `k = 3` root-incidence
sector appears at `n = 4`.

This note explains why that had to happen.

It is not a large-scale effect. It is already forced by the exact odd-parity
launch structure on a single plaquette face.

So any honest transfer has to contain:

1. the directed-cell local boundary theorem
2. the root-face / generic-face odd-parity launch theorem

If either piece is dropped, the full rooted gauge problem is not closed.

## Honest status

This note does **not** yet derive analytic `P(6)`.

It closes something narrower but decisive:

1. the exact local launch sectors on a plaquette face
2. the exact reason a single directed-cell launch is insufficient

The next exact consequence is recorded in
`docs/DIRECTED_CELL_BOUNDARY_STATE_TRANSFER_NOTE.md`.

## Commands run

```bash
python3 scripts/frontier_root_face_launch_cluster.py
```

Output summary:

- exact root-face incident count `4`
- exact generic exterior count `3`
- exact root-face launch sectors `4 @ (6,5)` and `4 @ (16,15)`
- exact generic-face launch sectors `3 @ (6,5)` and `1 @ (16,15)`
