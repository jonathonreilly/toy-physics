# Koide Q noncommutative-geometry finite-state no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_ncg_finite_state_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use finite real spectral-triple structure to choose the center state:

```text
retained finite spectral triple
  -> quotient-center trace
  -> K_TL = 0.
```

## Executable theorem

The retained real C3 carrier has:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

A normalized positive central state is still:

```text
phi(P_plus) = u
phi(P_perp) = 1-u.
```

The source law is:

```text
K_TL = 0 <=> u = 1/2.
```

## Obstruction

Two natural finite states differ:

```text
inherited Hilbert trace: u = 1/3 -> Q = 1,   K_TL = 3/8
quotient-center trace:  u = 1/2 -> Q = 2/3, K_TL = 0.
```

The finite real structure preserves the singlet and conjugates inside the
two-dimensional real block; it does not exchange the rank-1 and rank-2 central
blocks.  Dirac/order-one constraints act on representation and operator
commutators, not on the choice of positive state `u`.

## Residual

```text
RESIDUAL_SCALAR = center_finite_state_u_minus_one_half_equiv_K_TL
RESIDUAL_STATE = quotient_center_trace_not_selected_by_retained_spectral_triple
```

## Why this is not closure

The quotient-center trace is exactly the state that would close Q, but the
retained finite spectral-triple data does not select it over the inherited
Hilbert trace.  A positive closure would need a new finite-action/state
principle deriving that choice.

## Falsifiers

- A retained finite spectral-triple axiom selecting the quotient-center trace
  rather than Hilbert trace.
- A real-structure theorem exchanging the rank-1 and rank-2 central blocks.
- A spectral action whose unique stationary positive center state is `u=1/2`
  without fitting the coefficient.

## Boundaries

- Covers the retained central state freedom, Hilbert trace, quotient-center
  trace, real-structure preservation, and model Dirac/order-one independence.
- Does not refute a new finite-action principle that physically selects the
  quotient-center trace.

## Hostile reviewer objections answered

- **"NCG has a canonical trace."**  The canonical Hilbert trace is rank
  weighted and does not close Q.
- **"Use the center trace."**  That is the residual state-selection primitive.
- **"Reality should pair sectors."**  It pairs the conjugate characters inside
  the real doublet, not the singlet with the doublet total.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_ncg_finite_state_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_NCG_FINITE_STATE_NO_GO=TRUE
Q_NCG_FINITE_STATE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_finite_state_u_minus_one_half_equiv_K_TL
RESIDUAL_STATE=quotient_center_trace_not_selected_by_retained_spectral_triple
```
