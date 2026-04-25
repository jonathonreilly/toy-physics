# Koide Q renormalization/counterterm scale no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_renormalization_counterterm_scale_no_go.py`  
**Status:** no-go; Q not closed

## Theorem attempt

Try to derive the physical charged-lepton Q source law from retained
renormalization structure.  On the live normalized source fibre, write

```text
x = log(1 + rho).
```

If retained subtraction, normal-ordering, tadpole cancellation, or finite
counterterm normalization forces the subtraction point `mu = 0`, then the
renormalized zero-source condition `x - mu = 0` gives `rho = 0`, hence
`K_TL = 0` and the conditional support chain to `Q = 2/3`.

## Brainstormed routes

The runner tests six variants:

1. finite subtraction might force the physical log-source origin `mu = 0`;
2. normal-ordering might make zero background canonical;
3. tadpole cancellation might forbid a nonzero source background;
4. counterterm minimality might delete the affine source shift;
5. Callan-Symanzik stationarity might turn scheme covariance into a basepoint;
6. wrong-assumption inversion: `mu = log(2)` is an equally exact subtraction point.

The finite-counterterm route is the decisive test because it is the strongest
exact renormalization mechanism available in the retained packet.

## Result

The route fails as a closure theorem.  The zero-renormalized-source equation is

```text
x - mu = 0,
```

so it selects `x = mu`, not `x = 0`.  Therefore

```text
rho(mu) = exp(mu) - 1.
```

The closing case is only conditional:

```text
mu = 0 -> rho = 0 -> K_TL = 0 -> Q = 2/3.
```

But the same exact retained subtraction law also admits the nonclosing
countersection

```text
mu = log(2) -> rho = 1 -> K_TL = 3/8 -> Q = 1.
```

Finite counterterms make the obstruction explicit.  For

```text
S(x) = a0 + a1 x + a2 x^2
```

and affine counterterm `c0 + c1 x`, the conditions

```text
S_R(mu) = 0,
dS_R/dx |_{x=mu} = 0
```

solve as

```text
c0 = -a0 + a2 mu^2,
c1 = -a1 - 2 a2 mu.
```

The conditions determine counterterms for any supplied `mu`; they do not
derive `mu = 0`.

## Hostile review

- No Koide target is assumed.  The runner audits `mu=0` as conditional and
  `mu=log(2)` as an exact countersection.
- No PDG masses, observational `H_*` pin, `delta=2/9`, or Brannen-phase input
  appears.
- No new selector primitive is renamed as a theorem.  The missing theorem is
  named directly.
- Scheme covariance preserves only `x - mu`; it cannot choose the absolute
  source origin.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_renormalization_subtraction_mu_equals_zero
RESIDUAL_SOURCE = finite_counterterms_and_normal_ordering_leave_mu_free
COUNTERSECTION = mu_log2_rho_1_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 -m py_compile scripts/frontier_koide_q_renormalization_counterterm_scale_no_go.py
python3 scripts/frontier_koide_q_renormalization_counterterm_scale_no_go.py
```

Expected result:

```text
KOIDE_Q_RENORMALIZATION_COUNTERTERM_SCALE_NO_GO=TRUE
Q_RENORMALIZATION_COUNTERTERM_SCALE_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_SUBTRACTION_POINT_MU_EQUALS_ZERO=TRUE
RESIDUAL_SCALAR=derive_retained_renormalization_subtraction_mu_equals_zero
```
