# Wolfenstein Lambda-A Product Cancellation - Narrow Algebra Theorem

**Date:** 2026-05-10
**Claim type:** positive_theorem
**Status:** source-note proposal; independent audit owns audit verdict and
pipeline-derived effective status.
**Scope:** pure symbolic cancellation under explicitly supplied parametric
definitions.
**Primary runner:** [`scripts/frontier_wolfenstein_lambda_a_product_cancellation_narrow.py`](../scripts/frontier_wolfenstein_lambda_a_product_cancellation_narrow.py)
**Cache:** [`logs/runner-cache/frontier_wolfenstein_lambda_a_product_cancellation_narrow.txt`](../logs/runner-cache/frontier_wolfenstein_lambda_a_product_cancellation_narrow.txt)

## Claim

For positive symbols `alpha`, `n_pair`, and `n_color`, suppose the two
parametric identities

```
lambda^2 = alpha / n_pair
A^2 = n_pair / n_color
```

are supplied. Then

```
A^2 lambda^2 = alpha / n_color
```

because the `n_pair` factor cancels exactly. If one also defines
`n_quark = n_pair * n_color`, then the formal corollary

```
A^2 lambda^4 = alpha^2 / n_quark
```

follows by multiplying by `lambda^2` once more.

## Boundary

This note is not a derivation of the supplied identities, not a CKM closure,
not a numerical fit, and not a statement about external Wolfenstein
parameters. It preserves only the algebraic cancellation core. Any theorem
that uses this result with physical `alpha`, `lambda`, `A`, `n_pair`, or
`n_color` still has to derive or cite those input identities separately.

No imported values, external inputs, or literature constants are used. The
runner checks the cancellation on abstract symbols and on several rational
instances.

## Runner Checks

The paired runner verifies:

- exact symbolic cancellation of `A^2 lambda^2 - alpha/n_color`;
- exact symbolic cancellation of `A^2 lambda^4 - alpha^2/(n_pair*n_color)`;
- invariance over multiple positive rational count tuples;
- failure of the cancellation when one supplied hypothesis is perturbed;
- no empirical or retained-grade conclusion is emitted.
