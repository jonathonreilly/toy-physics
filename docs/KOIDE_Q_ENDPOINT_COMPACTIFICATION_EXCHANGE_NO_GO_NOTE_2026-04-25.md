# Koide Q Endpoint-Compactification Exchange No-Go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_endpoint_compactification_exchange_no_go.py`  
**Status:** executable no-go; not Q closure

## Theorem Attempt

After the Hessian metric reduced the Q source cone to the flat log torsor
`x=log(1+rho)`, try adding the endpoint compactification.  The proposed
closure was that physical exchange of the two compactified endpoints fixes the
midpoint, giving `rho=0` and hence `K_TL=0`.

## Result

The route fails.  Endpoint exchange is not unique without a center.  On the
compactified log line, every reflection

```text
x -> C - x
```

exchanges the two endpoints and fixes `x=C/2`.  In source coordinate this is:

```text
I_A(rho) = A/(1+rho) - 1,  A=exp(C)>0.
```

Every `I_A` is:

- an involution;
- an orientation-reversing map of the source cone;
- an exchange of the two compactified endpoints;
- an exact Hessian isometry.

The fixed point is:

```text
rho = sqrt(A) - 1.
```

Thus endpoint exchange supplies a fixed point only after the exchange center
has been supplied.

## Counterexchange

The closing exchange is:

```text
A=1 -> fixed rho=0 -> Q=2/3, K_TL=0.
```

But the nonclosing exchange

```text
A=4 -> fixed rho=1 -> Q=1, K_TL=3/8
```

has the same endpoint-exchange and Hessian-isometry status.  Therefore the
compactification data do not distinguish the closing source.

## Relation To Self-Duality

The special `A=1` map is

```text
rho -> -rho/(1+rho),
```

equivalently `1+rho -> (1+rho)^-1`.  This is the normalized
Legendre/self-duality reflection already audited as a no-go: it closes Q only
after a fixed-point law is imposed.  Endpoint compactification does not derive
that law; it repackages the missing exchange center.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_endpoint_exchange_center_A_equals_one
RESIDUAL_SOURCE = endpoint_exchange_center_not_retained
COUNTEREXCHANGE = A_4_fixed_rho_1_Q_1_K_TL_3_over_8
```

The missing law is the retained physical center of endpoint exchange, not the
existence of endpoint exchange itself.

## Hostile Review

This no-go does **not** use:

- PDG masses;
- the observational `H_*` pin;
- assumed `K_TL=0`;
- assumed `Q=2/3`;
- assumed `delta=2/9`;
- a hidden selector primitive.

It uses `A=1` only as the conditional closing endpoint exchange and tests it
against the exact nonclosing `A=4` counterexchange.

## Verdict

```text
KOIDE_Q_ENDPOINT_COMPACTIFICATION_EXCHANGE_NO_GO=TRUE
Q_ENDPOINT_COMPACTIFICATION_EXCHANGE_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_ENDPOINT_EXCHANGE_CENTER_A_EQUALS_ONE=TRUE
```

Endpoint compactification sharpens the obstruction: Q closure requires a
retained source-origin/endpoint-center law.
