# Koide Q Morita-Normalized Determinant No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_morita_normalized_determinant_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to derive the reduced quotient logdet from Morita-normalized determinant
theory.  On a matrix block, the source-response object is the normalized
log-determinant

```text
log det_r(I+kI_r) / r = log(1+k).
```

This deletes internal matrix rank and is invariant under matrix amplification.
If this is the physical charged-lepton source determinant, then

```text
dW_Morita|0 = (1,1)
K_TL = 0
Q = 2/3.
```

## Brainstormed Variants

1. Morita-normalized determinant: rank is dummy matrix amplification.
2. Full Hilbert determinant: rank is physical source multiplicity.
3. What if Morita normalization is forced by source-response?  Then Q closes.
4. What if full determinant remains physical?  It gives the exact rank
   counterstate.
5. Determinant-normalization exponent `alpha`: `alpha=0` is normalized,
   `alpha=1` is full rank determinant.

## Exact Audit

The runner verifies:

```text
logdet_full(M_2)=2 log(1+k)
normalized_logdet(M_2)=log(1+k).
```

Under amplification:

```text
logdet_full(M_2n)=2n log(1+k)
normalized_logdet(M_2n)=log(1+k).
```

So Morita normalization conditionally supplies the reduced generator:

```text
W_M = log(1+k_plus)+log(1+k_perp)
dW_M|0=(1,1)
Q=2/3.
```

The full determinant remains:

```text
W_full = log(1+k_plus)+2log(1+k_perp)
dW_full|0=(1,2)
Q=1
K_TL=3/8.
```

## Hostile Review

This route does not close Q from retained data.  It gives the cleanest
formulation of the missing law:

```text
derive_Morita_normalized_determinant_as_physical_source_generator.
```

Without that theorem, the full determinant is still an exact retained
countermodel.

## Verdict

```text
KOIDE_Q_MORITA_NORMALIZED_DETERMINANT_NO_GO=TRUE
Q_MORITA_NORMALIZED_DETERMINANT_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_MORITA_NORMALIZED_DETERMINANT_IS_PHYSICAL=TRUE
RESIDUAL_SCALAR=derive_Morita_normalized_determinant_as_physical_source_generator
RESIDUAL_Q=full_rank_determinant_source_response_not_excluded
COUNTERSTATE=full_determinant_w_plus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_morita_normalized_determinant_no_go.py
python3 -m py_compile scripts/frontier_koide_q_morita_normalized_determinant_no_go.py
```
