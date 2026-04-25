# Koide Q data-processing label-resource no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_data_processing_label_resource_no_go.py`  
**Status:** no-go; data-processing monotonicity does not force label erasure

## Theorem Attempt

Use a resource-theoretic or data-processing principle to force the physical
source to discard the retained center-label observable:

```text
Z = P_plus - P_perp.
```

If the label resource is erased, then the quotient source is uniform and
`K_TL=0`.

## Result

Negative under current retained structure.

The retained label bias is:

```text
<Z> = p_plus - p_perp = 2w - 1.
```

The label resource:

```text
R_Z = (2w - 1)^2
```

vanishes exactly at:

```text
w = 1/2.
```

That is the Koide source-neutral condition, but a nonzero retained-label state
is still exact:

```text
w=1/3 -> R_Z=1/9, Q=1, K_TL=3/8.
```

## Data Processing

The scalar-only experiment is the label-erasing garbling of the retained
`Z` experiment:

```text
E_full * G_forget = E_scalar.
```

Data processing is satisfied for every prior:

```text
I(label; scalar) = 0 <= I(label; Z) = H(w).
```

It does not choose `w=1/2`.

## Channel Countermodel

For the symmetric Markov family:

```text
T_lambda =
  [[(1+lambda)/2, (1-lambda)/2],
   [(1-lambda)/2, (1+lambda)/2]]
```

the label bias transforms as:

```text
<Z>_after = lambda (2w - 1).
```

Thus:

```text
lambda=1 -> identity, preserves nonzero source
lambda=0 -> erasure, gives the uniform source
```

Both obey resource monotonicity.  Choosing `lambda=0` is the missing physical
erasure/quotient law.

## Residual

```text
RESIDUAL_SCALAR = label_resource_bias_2w_minus_1_equiv_K_TL
RESIDUAL_CHANNEL = choose_erasure_lambda_zero_over_retained_identity
RESIDUAL_PRIMITIVE = derive_physical_label_resource_erasure_channel
```

## Hostile Review

- **Target import:** none.  The Koide value appears only as the consequence of
  the zero-resource conditional.
- **External empirical input:** none.
- **Hidden source-free law:** not promoted.
- **Missing axiom link:** exact.  Data processing constrains allowed
  degradation; it does not say the physical channel must be degradation to the
  scalar-only quotient.
- **Closure claim:** rejected.  The runner prints
  `Q_DATA_PROCESSING_LABEL_RESOURCE_CLOSES_Q=FALSE`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_data_processing_label_resource_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
PASSED: 15/15
KOIDE_Q_DATA_PROCESSING_LABEL_RESOURCE_NO_GO=TRUE
Q_DATA_PROCESSING_LABEL_RESOURCE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=label_resource_bias_2w_minus_1_equiv_K_TL
RESIDUAL_CHANNEL=choose_erasure_lambda_zero_over_retained_identity
RESIDUAL_PRIMITIVE=derive_physical_label_resource_erasure_channel
```

## Consequence

The resource-theoretic route reduces to the same missing step as the
Blackwell/sufficient-statistic routes: derive why the physical experiment
erases the retained `Z` label and quotient-prepares the uniform source.
