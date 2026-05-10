# Bougerol-Lacroix / Oseledets MET - External Narrow Theorem

**Date:** 2026-05-10
**Claim type:** positive_theorem
**Scope:** external multiplicative-ergodic theorem for products of
random matrices under standard integrability hypotheses.
**Status authority:** source-note proposal only; independent audit
sets any audit result and pipeline-derived status.
**Runner:** [`scripts/frontier_bougerol_lacroix_oseledets_met_external_narrow.py`](../scripts/frontier_bougerol_lacroix_oseledets_met_external_narrow.py)
**Cache:** [`logs/runner-cache/frontier_bougerol_lacroix_oseledets_met_external_narrow.txt`](../logs/runner-cache/frontier_bougerol_lacroix_oseledets_met_external_narrow.txt)

## Claim

Let `(A_n)` be an i.i.d. sequence of invertible matrices on a
finite-dimensional real or complex vector space and assume

```text
E log^+ ||A_0|| < infinity,
E log^+ ||A_0^{-1}|| < infinity.
```

Oseledets' multiplicative ergodic theorem gives deterministic
Lyapunov exponents

```text
lambda_1 >= lambda_2 >= ... >= lambda_m
```

and an invariant filtration such that, for nonzero `v` in the
corresponding Oseledets subspace,

```text
lim_{N -> infinity} (1/N) log ||A_{N-1} ... A_0 v|| = lambda_i.
```

Bougerol-Lacroix is cited as a standard reference for products of
random matrices and related spectral-gap/projective-action refinements.
This note records the MET limit theorem only; it does not assert a
uniform exponential finite-N error term.

## Boundary

This note does not claim:

- that any framework blocking map satisfies the MET hypotheses;
- that any project-specific coupling equals `exp(lambda_1)`;
- verification of strong irreducibility, proximality, or a spectral
  gap for a framework process;
- closure of any framework substitution, hierarchy formula, or
  physical scale;
- any numerical prediction or comparison with observation.

Any later use must separately construct the random matrix process,
verify the theorem hypotheses, and bridge the resulting exponent to the
physical quantity of interest.

## External References

- V. I. Oseledets, "A multiplicative ergodic theorem", Transactions of
  the Moscow Mathematical Society 19 (1968), 197-231.
- P. Bougerol and J. Lacroix, Products of Random Matrices with
  Applications to Schrodinger Operators, Progress in Probability and
  Statistics 8, Birkhauser, 1985.
- E. Le Page, "Theoremes limites pour les produits de matrices
  aleatoires", Lecture Notes in Mathematics 928, Springer, 1982,
  258-303.

## Verification

The paired runner checks deterministic examples and policy boundaries:

1. diagonal products with known Lyapunov exponents;
2. the singular-value exponent definition on diagonal products;
3. equality of top-vector growth with the top exponent;
4. a degenerate no-gap example showing the theorem is not a spectral-gap
   rate claim;
5. submultiplicativity of operator products;
6. source-note boundary checks excluding framework bridge claims.

Expected runner result: `PASS=8`, `FAIL=0`.
