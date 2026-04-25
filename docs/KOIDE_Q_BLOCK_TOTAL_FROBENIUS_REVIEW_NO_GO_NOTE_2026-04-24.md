# Koide Q block-total Frobenius closure review no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_block_total_frobenius_review_no_go.py`  
**Status:** Nature-grade review no-go; not closure

## Theorem under review

The historical block-total Frobenius route says:

```text
d=3 real-isotype multiplicities = (1,1)
equal block log-law -> E_plus = E_perp -> K_TL = 0.
```

## What survives

The arithmetic is exact.  For the Hermitian circulant carrier:

```text
E_plus = 3 a^2
E_perp = 6 |b|^2.
```

The equation

```text
E_plus = E_perp
```

is equivalent to:

```text
|b|^2 = a^2/2
kappa = 2
K_TL = 0.
```

## Review failure

The variational closure step chooses the equal block weights.

For a weighted block log-law:

```text
S = alpha log(E_plus) + beta log(E_perp)
```

at fixed total block energy, the runner verifies:

```text
E_perp / E_plus = beta / alpha.
```

Thus:

```text
alpha:beta = 1:1 -> Q = 2/3, K_TL = 0
alpha:beta = 1:2 -> Q = 1,   K_TL = 3/8.
```

Frobenius reciprocity gives the isotype multiplicity count `(1,1)`, but the
same retained carrier has dimension/rank count `(1,2)`.  Choosing multiplicity
weights rather than rank weights is the missing physical source functional.

## Residual

```text
RESIDUAL_SCALAR = equal_isotype_log_weight_minus_rank_weight_equiv_K_TL
RESIDUAL_WEIGHT = alpha_minus_beta_source_functional_weight
```

## Why this is not closure

The block-total Frobenius theorem is strong support for a candidate primitive:
equal real-isotype source weighting.  It does not derive that primitive from
the retained structure.  Promoting it as closure would import the equal-block
source law.

## Falsifiers

- A retained theorem proving the physical charged-lepton source functional uses
  isotype multiplicity weights `(1,1)`.
- A proof that the inherited rank/dimension weighting `(1,2)` is not an
  admissible source functional.
- A physical coarse-graining principle forcing `alpha=beta` without target
  import.

## Boundaries

- This review does not reject the block-total arithmetic.
- It rejects the historical promotion of equal block weights as a derived
  retained law.

## Hostile reviewer objections answered

- **"Frobenius reciprocity gives `(1,1)`."**  It gives a multiplicity count, not
  automatically a source weighting principle.
- **"The equal block law derives Koide."**  Yes, conditionally.  The equal block
  law is the missing primitive.
- **"Rank weights are less physical."**  That must be proved; the retained
  carrier supplies them naturally.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_block_total_frobenius_review_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_BLOCK_TOTAL_FROBENIUS_REVIEW_NO_GO=TRUE
Q_BLOCK_TOTAL_FROBENIUS_REVIEW_CLOSES_Q=FALSE
RESIDUAL_SCALAR=equal_isotype_log_weight_minus_rank_weight_equiv_K_TL
RESIDUAL_WEIGHT=alpha_minus_beta_source_functional_weight
```
