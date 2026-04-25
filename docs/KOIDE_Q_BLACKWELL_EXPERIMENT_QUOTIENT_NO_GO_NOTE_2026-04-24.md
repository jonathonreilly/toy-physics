# Koide Q Blackwell experiment-quotient no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_blackwell_experiment_quotient_no_go.py`  
**Status:** no-go; Blackwell order does not retain the scalar-only source
quotient

## Theorem Attempt

Use Blackwell/decision-theoretic equivalence to justify quotienting the two
center labels.  The reduced scalar observable experiment cannot distinguish
`P_plus` from `P_perp`, so perhaps the physical experiment is forced to identify
them and prepare the anonymous quotient state.

## Result

Negative under current retained structure.

Use row-stochastic experiments on the hidden center label:

```text
E_full   = [[1,0],[0,1]]
E_scalar = [[1],[1]]
```

`E_full` is the retained label-resolving experiment, i.e. observing the central
label/eigenvalue of:

```text
Z = P_plus - P_perp.
```

The scalar-only experiment is a garbling of the full retained experiment:

```text
E_full * [[1],[1]] = E_scalar.
```

But there is no reverse garbling:

```text
E_scalar * [a,1-a] != E_full
```

for any `a`.  The exact equations require `a=1` and `a=0` simultaneously.

Therefore the full retained `Z` experiment is strictly more informative in
Blackwell order.  Choosing the scalar-only experiment is a physical quotient
law, not a consequence of decision theory.

## Decision-Risk Countermodel

For label-recovery loss:

```text
risk_full = 0
risk_scalar = min(w, 1-w).
```

The Blackwell comparison does not choose the source prior `w`.  In particular:

```text
w=1/3 -> Q=1, K_TL=3/8
w=1/2 -> Q=2/3, K_TL=0.
```

Only the second closes `Q`; decision theory alone does not select it.

## Residual

```text
RESIDUAL_SCALAR = source_prior_w_minus_one_half_after_blackwell_scalar_garbling
RESIDUAL_LABEL = retained_Z_experiment_strictly_blackwell_more_informative
RESIDUAL_PRIMITIVE =
  derive_physical_experiment_is_scalar_garbling_and_quotient_prepared
```

## Hostile Review

- **Target import:** none.  The Koide value appears only as the conditional
  consequence of the uniform quotient prior.
- **External empirical input:** none.
- **Hidden source-free law:** not promoted.
- **Missing axiom link:** exact.  Blackwell theory orders experiments; it does
  not say the physical experiment must be a garbling of a retained more
  informative experiment.
- **Closure claim:** rejected.  The runner prints
  `Q_BLACKWELL_EXPERIMENT_QUOTIENT_CLOSES_Q=FALSE`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_blackwell_experiment_quotient_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
PASSED: 13/13
KOIDE_Q_BLACKWELL_EXPERIMENT_QUOTIENT_NO_GO=TRUE
Q_BLACKWELL_EXPERIMENT_QUOTIENT_CLOSES_Q=FALSE
RESIDUAL_SCALAR=source_prior_w_minus_one_half_after_blackwell_scalar_garbling
RESIDUAL_LABEL=retained_Z_experiment_strictly_blackwell_more_informative
RESIDUAL_PRIMITIVE=derive_physical_experiment_is_scalar_garbling_and_quotient_prepared
```

## Consequence

This closes the decision-theoretic version of the source quotient route as a
no-go.  Scalar-only operational equivalence can support the quotient-center
law only after the retained `Z` experiment is physically discarded and the
quotient state is prepared uniformly.
