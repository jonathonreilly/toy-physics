# Koide Q Named-Axiom Semialgebraic Admissibility No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_named_axiom_semialgebraic_admissibility_no_go.py`  
**Status:** no-go over retained inequality/admissibility constraints

## Theorem Attempt

Under the no-new-axioms rule, try to close `Q` by proving that retained
semialgebraic admissibility conditions isolate the hidden quotient-kernel
source charge:

```text
rho = 0.
```

The tested routes are source-response positivity, strict log-concavity, finite
analytic source-domain inequalities, boundary admissibility, and the inversion
where the full determinant `rho=1` branch remains physical.

## Result

For the source generator

```text
W_rho = log(1+k_plus) + (1+rho) log(1+k_perp),
```

the first derivative at the source origin is:

```text
dW_rho|0 = (1, 1+rho).
```

Source positivity requires:

```text
rho > -1.
```

The Hessian at the origin is:

```text
diag(-1, -1-rho),
```

so strict log-concavity gives the same condition:

```text
rho > -1.
```

Thus the current retained semialgebraic admissibility region is the connected
interval:

```text
(-1, infinity).
```

It contains both:

```text
rho = 0: reduced source response, Q = 2/3, K_TL = 0
rho = 1: full determinant response, Q = 1, K_TL = 3/8
```

## Boundary Obstruction

Selecting `rho=0` requires a boundary equation or an objective such as
least-source norm.  Those are not consequences of the current named retained
axioms.  An inequality that retains `rho=0` while excluding `rho=1` supplies a
new threshold/order source law unless it is independently retained.

## Hostile Review

This note does not claim closure and does not assume:

- `K_TL = 0`;
- `K = 0`;
- `P_Q = 1/2`;
- `Q = 2/3`;
- `delta = 2/9`;
- PDG mass matching;
- an observational `H_*` pin;
- a renamed selector primitive.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_semialgebraic_boundary_selecting_rho_zero
RESIDUAL_SOURCE = admissible_rho_interval_contains_rho_0_and_rho_1
COUNTERMODEL_PAIR = rho_0_reduced_response_and_rho_1_full_determinant_response
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_named_axiom_semialgebraic_admissibility_no_go.py
python3 -m py_compile scripts/frontier_koide_q_named_axiom_semialgebraic_admissibility_no_go.py
python3 scripts/frontier_koide_q_current_retained_source_class_exhaustion_no_go.py
python3 scripts/frontier_koide_q_residual_scalar_unification_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_NAMED_AXIOM_SEMIALGEBRAIC_ADMISSIBILITY_NO_GO=TRUE
Q_NAMED_AXIOM_SEMIALGEBRAIC_ADMISSIBILITY_CLOSES_Q_RETAINED_ONLY=FALSE
RESIDUAL_SCALAR=derive_retained_semialgebraic_boundary_selecting_rho_zero
COUNTERMODEL_PAIR=rho_0_reduced_response_and_rho_1_full_determinant_response
```
