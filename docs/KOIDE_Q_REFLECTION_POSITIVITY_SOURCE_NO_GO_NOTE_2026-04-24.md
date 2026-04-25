# Koide Q reflection-positivity source no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_reflection_positivity_source_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use Euclidean reflection positivity to force the center-source law:

```text
Osterwalder-Schrader reflection positivity
  -> equal C3 center source
  -> K_TL = 0.
```

## Executable theorem

For a central two-label source covariance:

```text
C(u) = u P_plus + (1-u) P_perp
```

with the doublet block represented by two equal entries:

```text
C(u) = diag(u, (1-u)/2, (1-u)/2).
```

The runner verifies that reflection positivity reduces to nonnegative block
weights:

```text
0 <= u <= 1.
```

## Obstruction

Closing and non-closing sources are all reflection-positive:

```text
u = 1/3 -> Q = 1,   K_TL = 3/8
u = 1/2 -> Q = 2/3, K_TL = 0
u = 2/3 -> Q = 1/2, K_TL = -3/8.
```

Reflection positivity is positivity of the pairing.  It does not equalize the
two center coefficients.

## Exchange escape hatch

An artificial reflection that exchanges `P_plus` and `P_perp` would add a new
equation, but the retained C3 carrier has:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

OS reflection acts on Euclidean time/order, not on the inequivalent C3
real-isotype ranks.

## Residual

```text
RESIDUAL_SCALAR = center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_EQUALITY = reflection_positivity_does_not_equalize_center_coefficients
```

## Why this is not closure

Reflection positivity is necessary physical structure for Euclidean sources,
but it leaves a full positive interval of center states.  A Nature-grade proof
still needs an equality law or source preparation theorem.

## Falsifiers

- A retained reflection that genuinely exchanges the rank-1 and rank-2 center
  sectors.
- An OS reconstruction theorem whose positivity domain collapses to `u=1/2`.
- A physical reflection-charge law that equates the two center coefficients
  without importing the target source.

## Boundaries

- Covers positive central source covariances and artificial exchange checks.
- Does not refute a stronger reflection symmetry acting directly on retained
  C3 source labels.

## Hostile reviewer objections answered

- **"Reflection positivity is physical."**  Yes; it permits the target source
  but does not select it.
- **"The covariance should be symmetric."**  Symmetric and positive still
  allows unequal positive block weights.
- **"Add a reflection exchanging labels."**  That is the previously isolated
  non-retained rank-obstructed exchange.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_reflection_positivity_source_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_REFLECTION_POSITIVITY_SOURCE_NO_GO=TRUE
Q_REFLECTION_POSITIVITY_SOURCE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_EQUALITY=reflection_positivity_does_not_equalize_center_coefficients
```
