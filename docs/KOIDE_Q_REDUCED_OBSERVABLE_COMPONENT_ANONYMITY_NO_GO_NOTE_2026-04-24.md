# Koide Q reduced-observable component-anonymity no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_reduced_observable_component_anonymity_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use the exact reduced observable theorem to derive quotient-center component
anonymity:

```text
W_red = log(1+k_plus) + log(1+k_perp)
  -> component anonymity
  -> K_TL = 0.
```

## What works

The reduced observable is symmetric on the abstract two-slot reduced carrier.
At the source-free point:

```text
k_plus = k_perp = 0
dW/dk = (1,1)
Q = 2/3
K_TL = 0.
```

This is exact support for the source-free conditional theorem.

## Obstruction

The same symmetric reduced observable admits a trace-normalized one-parameter
source family:

```text
Y = (y, 2-y)
K(y) = (1/y - 1, 1/(2-y) - 1).
```

For example:

```text
y = 2/3
K = (1/2, -1/4)
Q = 1
K_TL = 3/8.
```

So `W_red` symmetry does not force the source-free point.  It only says that
if the reduced source vanishes, Q closes.

## Residual

```text
RESIDUAL_SCALAR = reduced_source_K_zero_equiv_component_anonymity
RESIDUAL_SOURCE = source_free_reduced_point_not_derived_by_W_red_symmetry
```

## Why this is not closure

This route restates the already-reviewed source-free conditional closure.  A
Nature-grade proof still needs a physical law setting the reduced source to
zero or otherwise excluding the nonzero trace-normalized source family.

## Falsifiers

- A theorem deriving `K=0` from the reduced observable principle itself.
- A physical constraint excluding all nonzero reduced sources on the normalized
  positive carrier.
- A retained source-preparation law that selects `Y=(1,1)` before evaluating
  Q.

## Boundaries

- Covers the exact reduced observable generator and its normalized source
  family.
- Does not refute a future physical source-free theorem.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_reduced_observable_component_anonymity_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_REDUCED_OBSERVABLE_COMPONENT_ANONYMITY_NO_GO=TRUE
Q_REDUCED_OBSERVABLE_COMPONENT_ANONYMITY_CLOSES_Q=FALSE
RESIDUAL_SCALAR=reduced_source_K_zero_equiv_component_anonymity
RESIDUAL_SOURCE=source_free_reduced_point_not_derived_by_W_red_symmetry
```
