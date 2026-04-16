# Rank-1 + Rank-(n-1) Projector Algebra

**Status:** AIRTIGHT — pure linear algebra (weights only)
**Runner:** `scripts/frontier_projector_algebra.py` (25/25 PASS)
**Scope caveat:** the downstream identification with Unitarity Triangle
CP phase cos²(δ) is NOT claimed by this note (see caveat section).

## Theorem (algebra only)

For any n-dimensional Hilbert space C^n, the rank-1 projector onto a
specific unit vector v and the rank-(n-1) projector onto its orthogonal
complement satisfy:

```
P_1 + P_(n-1) = I_n       (completeness)
Tr(P_1) = 1
Tr(P_(n-1)) = n - 1
weight_1 = Tr(P_1)/n = 1/n
weight_(n-1) = Tr(P_(n-1))/n = (n-1)/n
```

For v = (1, 1, ..., 1)/√n (uniform superposition):
```
P_1 = (1/n) |1⟩⟨1|    where |1⟩ = (1,...,1)
P_(n-1) = I_n - P_1
```

## Specific cases

| n | weight_1 = 1/n | weight_(n-1) = (n-1)/n | Notable |
|---|---|---|---|
| 2 | 1/2 | 1/2 | trivial |
| 3 | 1/3 | 2/3 | color pair |
| 6 | 1/6 | 5/6 | quark block dim |
| 8 | 1/8 | 7/8 | lattice taste cube |

## Verification

The runner proves:
- Projector idempotency P² = P
- Hermiticity P = P†
- Rank (P_1) = 1, rank(P_(n-1)) = n-1
- Weights sum to 1
- For n=6: weight = 1/6 identified with cos²(δ) = 1/6 in the atlas
  (this is a structural IDENTIFICATION, not proved here)
- For n=3 with n_pair=2 pair subspace: overlap n_pair/n_color = 2/3

Additional verification: for a scalar Z_n action (e.g., Z_3 center
acting as ω·I), every rank-1+rank-(n-1) decomposition is Z_n-invariant.
So the uniform-superposition direction is not SINGLED OUT by Z_n; it
must be selected by a DIFFERENT physical argument.

## Scope caveat (important)

The projector algebra ABOVE is airtight. What is NOT airtight:

1. **The identification of this projector with CP phase cos²(δ).**
   The quark block Q_L = (2, 3) is irreducible under SU(2)×SU(3),
   so the "1+5" split of C^6 is NOT forced by gauge symmetry.
   Choosing the uniform superposition as the "aligned direction"
   requires a physical argument that is NOT contained in this note.

2. **Downstream CKM claims** (e.g., ρ² + η² = 1/6, δ = arctan(√5))
   depend on this structural identification. They are NOT in this
   derived branch.

## What this note IS

A clean theorem about projector weights in a d-dim Hilbert space.
Pure linear algebra. 25/25 PASS.

## What this note IS NOT

Not a derivation of the CP phase. Not a derivation of any CKM element.
Not a proof that the "aligned direction" in Q_L = (2, 3) is the uniform
superposition.
