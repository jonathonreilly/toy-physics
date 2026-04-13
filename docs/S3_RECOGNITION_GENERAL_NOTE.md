# S^3 Recognition for General R

**Date:** 2026-04-13
**Status:** BOUNDED (strengthened computational evidence, not a general theorem)
**Script:** `scripts/frontier_s3_recognition_general.py`

## Theorem / Claim

For each R in {2, 3, 4, 5, 6}, the cone-capped cubical complex
M_R = B_R ∪ cone(∂B_R) is computationally verified to be PL homeomorphic
to S^3 via the Rubinstein-Thompson splitting-surface recognition algorithm.

## Assumptions

1. The cubical ball B_R is the union of all unit cubes in Z^3 whose 8
   corners lie within Euclidean distance R of the origin.
2. M_R = B_R ∪ cone(∂B_R) is the standard cone-cap closure.
3. Each unit cube is subdivided into 6 tetrahedra via the Freudenthal
   (staircase) triangulation.
4. Recognition uses only combinatorial/computational methods: vertex link
   enumeration, Euler characteristic, and free-face collapse.  No external
   theorems (Perelman, Moise, Schoenflies) are cited.

## What Is Actually Proved

For each R = 2, 3, 4, 5, 6, the script verifies all four conditions of
S^3 recognition:

| R | Vertices | Tetrahedra | Manifold | Surface S^2 | Ball collapse | Cone collapse | S^3 |
|---|----------|------------|----------|-------------|---------------|---------------|-----|
| 2 |       28 |         96 | YES      | YES         | 48/48         | 48/48         | PROVED |
| 3 |      118 |        528 | YES      | YES         | 336/336       | 192/192       | PROVED |
| 4 |      252 |      1,200 | YES      | YES         | 816/816       | 384/384       | PROVED |
| 5 |      486 |      2,448 | YES      | YES         | 1824/1824     | 624/624       | PROVED |
| 6 |      920 |      4,800 | YES      | YES         | 3744/3744     | 1056/1056     | PROVED |

The four conditions for each R:

1. **Closed PL 3-manifold:** Every vertex link is a PL 2-sphere
   (verified by checking connectivity, closure, and chi=2 for all
   vertex links in the full simplicial complex).

2. **Splitting surface is S^2:** The natural boundary ∂B_R, triangulated
   as a subcomplex of M_R, is a closed connected surface with chi=2.

3. **Ball side collapses:** B_R (the cubical ball, tetrahedralized)
   admits a complete free-face collapse to a point, proving it is a
   PL 3-ball.  All R values succeed with the deterministic greedy
   ordering (no randomization needed).

4. **Cone side collapses:** cone(∂B_R) admits a complete free-face
   collapse to a point, proving it is a PL 3-ball.  All R values
   succeed deterministically.

The conclusion for each R follows from the definition:
  S^3 = B^3 ∪_{S^2} B^3.

## What Remains Open

1. **Not a general theorem for all R.** The script verifies R = 2..6
   computationally.  It does not constitute a proof for arbitrary R.
   A general proof would require either:
   - A theorem that the Freudenthal triangulation of the cubical ball
     is always shellable (which would give collapse for all R), or
   - A general structural argument about the cone-cap construction.

2. **The lane remains bounded.** The S^3 compactification claim for
   the full Cl(3)-on-Z^3 framework is strengthened but not closed.
   The computational evidence covers R = 2..6, which is a
   significant extension beyond the original R = 2, but it is still
   finite verification, not a theorem.

3. **Collapse algorithm.** All tested R values succeed with
   deterministic greedy collapse.  For much larger R, the greedy
   ordering might get stuck (this would be an algorithmic limitation,
   not a topological obstruction, since the cone-cap construction
   always produces S^3).  The script includes randomized fallback
   for this case.

## Supporting Evidence from Other Scripts

- `frontier_s3_inductive_link.py`: All vertex links are S^2 for
  R = 2..10 (72/72 checks pass).  This covers the manifold condition
  well beyond R = 6.

- Homology H_*(M_R) = (Z, 0, 0, Z) verified for R = 2..6 in
  separate homology scripts.  This is consistent with S^3 but does
  not by itself prove S^3 (homology 3-spheres exist that are not S^3).

- The recognition algorithm (splitting + collapse) is strictly
  stronger than homology: it constitutes a full PL homeomorphism
  proof for each individual R.

## How This Changes The Paper

- The S^3 lane moves from "R=2 only" to "R=2..6 verified."
- This is a meaningful strengthening: the recognition algorithm works
  unchanged across a range of complex sizes (96 to 4,800 tetrahedra),
  with deterministic collapse succeeding in every case.
- The lane remains **bounded**, not closed.  Paper-safe wording:

  > S^3 recognition verified computationally for R = 2..6 via
  > splitting-surface collapse.  General R remains open.

- Do NOT claim "S^3 compactification proved" or "topology lane closed"
  based on this work alone.

## Commands Run

```
python3 scripts/frontier_s3_recognition_general.py
```

Total runtime: ~2.3s for all five R values.
