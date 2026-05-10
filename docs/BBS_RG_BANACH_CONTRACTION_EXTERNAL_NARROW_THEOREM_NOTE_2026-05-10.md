# BBS RG Banach Contraction — External Narrow Theorem

**Date:** 2026-05-10
**Claim type:** positive_theorem
**Scope:** external Banach-space contraction theorem, with
Bauerschmidt-Brydges-Slade/Brydges-Slade cited only as rigorous-RG
context where such contraction estimates are used.
**Status authority:** source-note proposal only; independent audit
sets any audit result and pipeline-derived status.
**Runner:** [`scripts/frontier_bbs_rg_banach_contraction_external_narrow.py`](../scripts/frontier_bbs_rg_banach_contraction_external_narrow.py)
**Cache:** [`logs/runner-cache/frontier_bbs_rg_banach_contraction_external_narrow.txt`](../logs/runner-cache/frontier_bbs_rg_banach_contraction_external_narrow.txt)

## Claim

Let `(B, ||.||)` be a Banach space. If `T: B -> B` is a bounded
linear operator with `||T||_op <= kappa` and `0 <= kappa < 1`, then
for every `x0 in B` and integer `N >= 0`,

```text
||T^N x0|| <= kappa^N ||x0||.
```

If `T_j` are bounded linear operators with `||T_j||_op <= kappa_j`,
then

```text
||(T_N ... T_1)x0|| <= (product_j kappa_j) ||x0||.
```

For a strict contraction on a complete metric space, Banach's
fixed-point theorem gives the standard error bound

```text
d(T^N x0, x_*) <= kappa^N d(x0, x_*),
```

and the geometric tail identity is

```text
sum_{k >= N} kappa^k = kappa^N / (1 - kappa).
```

## Boundary

This note records a functional-analysis theorem and an external
rigorous-RG context. It does not claim:

- that any framework blocking/coarse-graining map satisfies the BBS
  hypotheses;
- that any project-specific coupling is a BBS contraction constant;
- closure of any framework substitution, hierarchy formula, or
  physical scale;
- any numerical prediction or comparison with observation;
- any new framework axiom or repo-wide premise.

Any later framework use must separately construct the Banach space,
norm, map, contraction estimate, and physical bridge.

## External References

- S. Banach, "Sur les operations dans les ensembles abstraits et leur
  application aux equations integrales", Fundamenta Mathematicae 3
  (1922), 133-181.
- D. C. Brydges and G. Slade, "A renormalisation group method. V. A
  single renormalisation group step", Journal of Statistical Physics
  159 (2014), 589-667; arXiv:1403.7256.
- R. Bauerschmidt, D. C. Brydges, and G. Slade, Introduction to a
  Renormalisation Group Method, Lecture Notes in Mathematics 2242,
  Springer (2019); arXiv:1907.05474.

## Verification

The paired runner checks:

1. exact Fraction arithmetic for `||T^N x0|| = kappa^N ||x0||` on
   scalar contraction examples;
2. the geometric tail identity;
3. composition of distinct contractions;
4. the fixed-point error bound for an affine contraction;
5. sharpness at `kappa = 1` versus decay at `kappa < 1`;
6. substrate independence on scalar and finite-dimensional diagonal
   toy operators;
7. source-note boundary checks excluding framework bridge claims.

Expected runner result: `PASS=8`, `FAIL=0`.
