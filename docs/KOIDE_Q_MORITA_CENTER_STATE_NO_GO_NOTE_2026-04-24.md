# Koide Q Morita-invariant center-state no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_morita_center_state_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use Morita invariance to justify the quotient-center source:

```text
Morita invariance removes rank amplification
  -> equal center-component weights
  -> K_TL = 0.
```

## Executable theorem

For a semisimple finite algebra:

```text
M_1 ⊕ M_2,
```

Morita invariance replaces raw matrix trace by normalized trace inside each
simple block:

```text
tr_n(I_n)/n = 1.
```

A Morita-invariant state still has component weights:

```text
phi = w_plus tau_plus + w_perp tau_perp
w_plus + w_perp = 1.
```

## Obstruction

The runner verifies:

```text
K_TL = 0 <=> w_plus = 1/2.
```

But Morita-invariant states include non-closing component weights:

```text
w_plus = 1/3 -> Q = 1,   K_TL = 3/8
w_plus = 1/2 -> Q = 2/3, K_TL = 0
w_plus = 2/3 -> Q = 1/2, K_TL = -3/8.
```

## What Morita invariance does prove

Morita invariance is useful: it rejects raw Hilbert-rank weighting as the only
possible finite-state principle.  It does not, however, choose a probability
measure across disconnected center components.

Uniform component counting:

```text
(w_plus,w_perp) = (1/2,1/2)
```

is a stronger source principle.

## Residual

```text
RESIDUAL_SCALAR = Morita_component_weight_w_plus_minus_one_half_equiv_K_TL
RESIDUAL_MEASURE = uniform_measure_over_Morita_components_not_derived
```

## Why this is not closure

The route sharpens the best quotient-center idea but does not derive the equal
component measure.  A Nature-grade closure would need a physical principle that
selects uniform weights over Morita components, not just normalized traces
inside each component.

## Falsifiers

- A retained theorem that Morita-invariant states on finite direct sums must
  use uniform component weights.
- A physical source law excluding nonuniform component measures.
- A component-exchange naturality theorem surviving the rank/isotype
  obstruction.

## Boundaries

- Covers matrix-rank Morita invariance and finite direct-sum component weights.
- Does not refute a stronger uniform-component physical principle.

## Hostile reviewer objections answered

- **"Morita invariance removes rank."**  Yes; it still leaves component
  weights.
- **"The quotient center has two points."**  A two-point space has a simplex of
  probability measures.
- **"Use uniform component counting."**  That is the residual measure principle.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_morita_center_state_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_MORITA_CENTER_STATE_NO_GO=TRUE
Q_MORITA_CENTER_STATE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=Morita_component_weight_w_plus_minus_one_half_equiv_K_TL
RESIDUAL_MEASURE=uniform_measure_over_Morita_components_not_derived
```
