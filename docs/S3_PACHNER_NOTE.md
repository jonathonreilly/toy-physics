# S^3 Closure Path 1: Constructive PL Homeomorphism via Pachner Moves

**Status**: EXACT (all 10 checks pass)
**Script**: `scripts/frontier_s3_pachner.py`
**Runtime**: 0.1s

## Result

The cone-capped Freudenthal cubical ball M at R=2 is **PL S^3**, proved
by an explicit finite sequence of 59 Pachner moves (bistellar flips)
transforming M into the boundary of the 4-simplex (the standard minimal
S^3 triangulation with 5 vertices).

This is a **constructive proof**: no citation of Perelman, Moise, or the
Poincare conjecture is required.

## The complex M

- Freudenthal triangulation of all unit cubes whose 8 corners lie within
  Euclidean distance 2 of the origin in Z^3.
- Boundary triangles (faces of exactly one tetrahedron) are coned to a
  single apex vertex.
- Initial f-vector: **(28, 124, 192, 96)** (vertices, edges, triangles, tets).
- Euler characteristic: 0 (as required for S^3).
- All 28 vertex links are PL S^2 (verified computationally).

## The Pachner sequence

59 moves total: **23 vertex removals (4-1)**, **29 edge collapses (3-2)**,
**7 triangle splits (2-3)**.

| Phase | Vertices | Strategy |
|-------|----------|----------|
| Initial | 28 | No 4-1 candidates exist |
| Moves 1--24 | 28 -> 16 | Greedy 3-2 to unlock 4-1 on boundary vertices |
| Moves 25--44 | 16 -> 11 | 2-3 + 3-2 combos to "untangle" cone-apex edges |
| Moves 45--59 | 11 -> 5 | Final 3-2/4-1 cascade to minimal S^3 |

Final f-vector: **(5, 10, 10, 5)** = boundary of the 4-simplex.

## Why this works

1. **Pachner's theorem (1991)**: Any two PL-homeomorphic triangulations of
   a closed PL manifold are connected by a finite sequence of bistellar
   flips. We construct such a sequence explicitly.

2. **Each Pachner move preserves PL homeomorphism type** by definition. The
   moves are:
   - 4-1: Remove a vertex whose link is the boundary of a tetrahedron.
   - 3-2: Replace 3 tetrahedra sharing an edge with 2 sharing a triangle.
   - 2-3: Inverse of 3-2 (used sparingly to unlock 4-1/3-2 moves).

3. **The final complex is manifestly S^3**: every 4-element subset of 5
   vertices forms a tetrahedron, which is precisely the boundary of the
   4-simplex.

## Verification

- **E1**: f-vector (28, 124, 192, 96) and chi=0 confirmed.
- **E2**: 59-move Pachner sequence found deterministically (no randomization needed).
- **E3**: Euler characteristic = 0 maintained at every intermediate step.
- **E4**: Final complex = boundary of 4-simplex verified.
- **E5**: PL manifold condition (all vertex links = S^2) verified at
  every 10th step and final 5 steps during replay.
- **E6**: Every triangle in the final complex is shared by exactly 2
  tetrahedra (closed oriented manifold).

## Significance

This eliminates the dependence on Perelman/Moise for the S^3
identification. The previous approach (frontier_s3_direct_identification)
computed homology H_*(M; Z) = (Z, 0, 0, Z) exactly but still needed the
PL Poincare conjecture for the final identification step. The Pachner
sequence makes the identification purely constructive.

## Key technical insight

The initial Freudenthal triangulation has no vertices with tetrahedral
links (so no 4-1 moves are directly available). The strategy of using
3-2 moves on degree-3 edges to reduce local complexity, thereby creating
vertices with tetrahedral links, is what makes the simplification
possible. The 7 carefully placed 2-3 moves serve to "untangle" the
cone-apex connectivity in the middle phase.
