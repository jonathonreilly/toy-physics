# Koide Q Reduced-Determinant Retention Next-Twenty No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_reduced_determinant_retention_next20_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to prove that the retained physical charged-lepton Q source generator is
the reduced determinant

```text
W_red = log(1+k_plus)+log(1+k_perp)
```

rather than the full retained rank determinant

```text
W_full = log(1+k_plus)+2 log(1+k_perp).
```

If `W_red` is the physical source generator, then

```text
dW_red|0 = (1,1)
K_TL = 0
Q = 2/3.
```

## Twenty Attacks Audited

The runner tests determinant multiplicativity, Morita amplification,
source-response derivatives, higher cumulants, heat/zeta regularization,
supertrace-like deletion, categorical trace naturality, determinant-line
constants, renormalized counterterms, Schur factorization, relative
determinants, Legendre/source duality, observable quotienting, minimum
description preference, stable `K0`, center trace states, Hilbert trace states,
determinant exponents, positivity, and the explicit reduced-retention residual.

## Exact Result

The reduced determinant is an exact sufficient law:

```text
W_red = log(1+k_plus)+log(1+k_perp)
dW_red|0=(1,1)
K_TL=0
Q=2/3
```

The full determinant remains a retained countergenerator:

```text
W_full = log(1+k_plus)+2log(1+k_perp)
dW_full|0=(1,2)
weights=(1/3,2/3)
K_TL=3/8
Q=1
```

The determinant exponent family makes the obstruction one-dimensional:

```text
W_alpha = log(1+k_plus)+2^alpha log(1+k_perp)
dW_alpha|0=(1,2^alpha)
closure requires alpha=0
full determinant is alpha=1
```

## Musk Simplification Pass

1. The necessary requirement is not a large determinant formalism; it is one
   physical source-generator law.
2. All audited determinant variants collapse to the scalar slope ratio
   `dW_perp/dW_plus`.
3. The proof target is therefore the identity `dW_perp/dW_plus = 1`, not another
   representation of `Q=2/3`.
4. The fastest decisive test for future routes is whether they exclude the full
   determinant slope ratio `2`.
5. The runner automates that test and records the full determinant counterstate.

## Hostile Review

This is not a Koide closure.  It does not derive the reduced determinant from
retained Cl(3)/`Z^3` charged-lepton structure.  It proves that the reduced
determinant would be sufficient, while preserving the exact retained
countergenerator that remains available without a new law.

The exact residual is:

```text
derive_reduced_determinant_as_retained_physical_source_generator
```

## Verdict

```text
KOIDE_Q_REDUCED_DETERMINANT_RETENTION_NEXT20_NO_GO=TRUE
Q_REDUCED_DETERMINANT_RETENTION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_REDUCED_DETERMINANT_IS_RETAINED_PHYSICAL_SOURCE=TRUE
RESIDUAL_SCALAR=derive_reduced_determinant_as_retained_physical_source_generator
RESIDUAL_SOURCE=full_rank_determinant_countergenerator_not_excluded
COUNTERSTATE=full_rank_determinant_w_plus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_reduced_determinant_retention_next20_no_go.py
python3 -m py_compile scripts/frontier_koide_q_reduced_determinant_retention_next20_no_go.py
```
