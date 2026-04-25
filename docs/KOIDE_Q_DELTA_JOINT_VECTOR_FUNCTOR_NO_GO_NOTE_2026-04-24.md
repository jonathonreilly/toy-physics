# Koide Q/delta joint vector-functor no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_delta_joint_vector_functor_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use one joint boundary/source functor to close both live primitives:

```text
joint retained functor
  -> u = 1/2
  -> theta_end - theta0 = eta_APS
  -> full Koide lane closure.
```

## Executable theorem

The live residual is a two-component vector:

```text
RESIDUAL_Q = u - 1/2
RESIDUAL_DELTA = delta - 2/9.
```

Full lane closure requires both components to vanish:

```text
(u, delta) = (1/2, 2/9).
```

## Obstruction

A scalar joint relation:

```text
a RESIDUAL_Q + b RESIDUAL_DELTA = 0
```

leaves a one-parameter curve.  For example with `a=b=1`:

```text
u = 3/5
delta = 11/90
```

satisfies the scalar relation while neither residual is closed.

## What would be enough

A vector-valued theorem with two independent equations would be algebraically
enough.  The runner verifies that the residual vector has full-rank Jacobian.

But current retained support does not provide that vector theorem:

```text
Q audits end at center-source preparation.
delta audits end at selected-line open endpoint selection.
```

## Residual

```text
RESIDUAL_Q = center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_DELTA = theta_end-theta0-eta_APS
RESIDUAL_VECTOR = two_independent_primitives_require_vector_theorem
```

## Why this is not closure

The joint route cannot close the lane with a single scalar bridge.  It either
needs two independent retained equations or a new theorem proving one residual
is a physical consequence of the other.

## Falsifiers

- A retained vector-valued boundary/source functor whose two components are
  exactly the Q source law and the delta endpoint law.
- A physical theorem deriving the delta endpoint from the Q source, or the Q
  source from the delta endpoint.
- A proof that admissible joint states are zero-dimensional rather than a
  scalar-relation curve.

## Boundaries

- Covers scalar joint relations between the two known residuals.
- Does not refute a future two-component physical theorem.

## Hostile reviewer objections answered

- **"One elegant principle can close both."**  It must be vector-valued or
  prove dependency; a scalar relation is underdetermined.
- **"Link Q and delta."**  Existing link identities are support; they do not
  remove either primitive.
- **"Choose the zero of both components."**  That is exactly the target import
  unless the vector law is derived.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_delta_joint_vector_functor_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_DELTA_JOINT_VECTOR_FUNCTOR_NO_GO=TRUE
Q_DELTA_JOINT_VECTOR_FUNCTOR_CLOSES_Q=FALSE
Q_DELTA_JOINT_VECTOR_FUNCTOR_CLOSES_DELTA=FALSE
RESIDUAL_Q=center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_DELTA=theta_end-theta0-eta_APS
RESIDUAL_VECTOR=two_independent_primitives_require_vector_theorem
```
