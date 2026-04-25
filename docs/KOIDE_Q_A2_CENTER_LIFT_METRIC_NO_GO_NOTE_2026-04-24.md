# Koide Q A2-center lift metric no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_a2_center_lift_metric_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use the fact that the retained `Z_3` can be viewed as the center of `SU(3)` to
derive Koide from `A_2` weight geometry.

The exact support hit is:

```text
|omega_fund(A2)|^2 = 2/3.
```

## Executable theorem

The runner verifies the `A_2` Cartan arithmetic:

```text
C_A2 = [[2,-1],[-1,2]]
C_A2^-1 = (1/3)[[2,1],[1,2]]
|omega_1|^2 = 2/3
|rho_A2|^2 = 2
```

But a scaled root metric gives

```text
|omega_1|^2_scaled = lambda * 2/3.
```

Matching the Koide value fixes `lambda=1`; the retained `C_3` center does not
by itself supply that full `A_2` root metric.

The center characters

```text
0, 1, 2
```

also do not contain the `2x2` Cartan matrix or the map from an `A_2` weight
norm to the charged-lepton second-order source carrier.

## Residual

```text
RESIDUAL_SCALAR = A2_root_metric_and_source_map_not_retained
RESIDUAL_LIFT = A2_root_metric_and_source_map_not_retained
```

## Why this is not closure

The `A_2` number is exact support.  Closure would require:

- a retained lift from the `C_3` center to full `SU(3)/A_2` root data;
- a retained metric normalization;
- a physical map from `A_2` weight norm to the charged-lepton source scalar.

Those are not supplied by the center alone.

## Falsifiers

- A retained theorem that the charged-lepton `C_3` carrier is the `SU(3)`
  center with the standard `A_2` long-root normalization.
- A functor from `A_2` weight geometry to the normalized second-order source
  carrier that proves `K_TL=0`.
- A uniqueness theorem showing no scaled or alternative center lift is
  admissible.

## Boundaries

- The runner covers the `A_2` Cartan arithmetic and metric-scaling obstruction.
- It does not reject a future retained `SU(3)` family-lift theory; it isolates
  the exact lift/map such a theory must prove.

## Hostile reviewer objections answered

- **"The number is exactly right."**  Yes.  Exact arithmetic support is not a
  physical source law.
- **"But `Z_3` is the center of `SU(3)`."**  The center does not determine the
  full root datum or metric normalization.
- **"Could this become closure with a new family-lift theorem?"**  Yes, if the
  lift and source map are independently retained.  They are the residual.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_a2_center_lift_metric_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_A2_CENTER_LIFT_METRIC_NO_GO=TRUE
Q_A2_CENTER_LIFT_METRIC_CLOSES_Q=FALSE
RESIDUAL_SCALAR=A2_root_metric_and_source_map_not_retained
RESIDUAL_LIFT=A2_root_metric_and_source_map_not_retained
```
