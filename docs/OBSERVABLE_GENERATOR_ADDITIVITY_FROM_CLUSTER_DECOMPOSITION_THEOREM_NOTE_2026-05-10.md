# Observable-Generator Additivity From Cluster Decomposition Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source note only. Audit verdicts and effective status
are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_observable_generator_additivity_from_cluster_decomposition.py`](../scripts/frontier_observable_generator_additivity_from_cluster_decomposition.py)

## Scope

This note records a finite-block support result for the observable-generator
choice in
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md).
It uses the finite Grassmann determinant surface described by
[`STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md):

```text
Z[J] = det(D + J).
```

When a block cut removes every hopping bond across the cut, the operator
has direct-sum form

```text
D = D_A (+) D_B,      J = J_A (+) J_B.
```

## Result

For any such no-cut block decomposition,

```text
Z[J_A (+) J_B]
  = det((D_A + J_A) (+) (D_B + J_B))
  = det(D_A + J_A) det(D_B + J_B).
```

Therefore the normalized log generator

```text
W[J] = log |det(D + J)| - log |det(D)|
```

is additive:

```text
W[J_A (+) J_B] = W_A[J_A] + W_B[J_B].
```

The same statement is the finite-dimensional cumulant statement: mixed
source derivatives of `W` vanish when the derivative support splits across
the no-cut block partition. Equivalently, connected truncated kernels do
not cross a block cut when the determinant factorizes.

## Boundary

This result narrows the parent observable-generator additivity condition,
but it does not retire the parent selection step. The choice to use the
normalized log determinant, rather than the raw determinant or another
non-additive functional of `Z[J]`, is still a definitional selection unless
closed by a separate retained-grade theorem.

Consequently this note does not change the status of
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
and does not add a new framework axiom.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_observable_generator_additivity_from_cluster_decomposition.py
```

Expected result: `PASS=7 FAIL=0`. A passing run supports only the bounded
finite-block additivity and cumulant-vanishing statement above.
