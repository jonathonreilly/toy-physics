# S_3 Taste-Cube Decomposition Note

**Date:** 2026-04-17
**Status:** exact support theorem on the full taste cube
**Script:** `scripts/frontier_s3_action_taste_cube_decomposition.py`
**Authority role:** canonical representation-theoretic support note for
axis-permutation symmetry on `C^8 = (C^2)^{\otimes 3}`

## Safe statement

Let `S_3` act on `C^8 = (C^2)^{\otimes 3}` by permuting tensor positions. Then:

- Hamming weight is preserved, so the computational basis splits as
  `1 + 3 + 3 + 1`
- the `hw = 0` and `hw = 3` sectors are trivial `A_1`
- each of the `hw = 1` and `hw = 2` sectors is the standard permutation
  representation `A_1 + E`
- therefore

```text
C^8 ~= 4 A_1 + 2 E
```

and the sign irrep `A_2` does not occur

This is a full-cube support theorem. It does not by itself prove any flavor
claim. Its safe role is to fix the exact `S_3` carrier content that later
generation and flavor tools are allowed to use.

## Classical results applied

- finite-group character theory for `S_3`
- the permutation-character formula `chi(pi) = |Fix(pi)|`
- standard decomposition of the three-point permutation representation as
  `A_1 + E`

## Framework-specific step

- identification of the `S_3` action as axis permutations on the taste cube
- exact computation of the character on the `8` computational basis states

## Why it matters on `main`

This theorem sharpens the repo's axis-symmetry language into an exact
representation statement. It supplies a clean canonical support tool for the
retained three-generation lane and for future bounded flavor work built on the
full taste cube rather than only on the retained `hw=1` triplet.

## Verification

Run:

```bash
python3 scripts/frontier_s3_action_taste_cube_decomposition.py
```

The runner checks the `S_3` representation law on `C^8`, Hamming-weight
preservation, the class characters, and the multiplicity calculation
`C^8 ~= 4 A_1 + 2 E`.
