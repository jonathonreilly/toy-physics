# Koide delta spectral-flow degree-normalization no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_spectral_flow_degree_normalization_no_go.py`  
**Status:** no-go; spectral-flow count does not force the selected endpoint degree

## Theorem Attempt

After endpoint-functor classification, the delta residual can be written as:

```text
delta_open = n eta_APS + c.
```

The attempted theorem is that spectral-flow quantization forces:

```text
n = 1
c = 0.
```

## Result

Negative.  Retained spectral-flow data can fix a crossing count on the closed
determinant/spectral line.  It has zero rank in the open selected-line endpoint
functor variables `n` and `c`.

The route closes only after adding the further identity:

```text
selected open Brannen endpoint = unit-degree spectral-flow generator.
```

That identity is the missing endpoint functor law.

## Countermodels

With the same ambient value `eta_APS = 2/9` and one protected crossing, the
following endpoint functors remain algebraically admissible:

```text
F(eta) = 0
F(eta) = -eta
F(eta) = 2 eta
F(eta) = eta + 1/9
```

They are excluded only by selecting the unit-degree endpoint functor and its
basepoint.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR_DEGREE = selected_line_spectral_flow_degree_not_forced_one
RESIDUAL_SCALAR = n_minus_one_plus_c_over_eta_APS
```

## Falsifiers

- A retained theorem that the selected Brannen open line is the fundamental
  spectral-flow generator, not a separate readout functor.
- A retained endpoint basepoint theorem deriving `c = 0`.
- A proof that all other integer-degree endpoint functors are unphysical from
  retained `Cl(3)/Z^3` structure alone.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_spectral_flow_degree_normalization_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_SPECTRAL_FLOW_DEGREE_NORMALIZATION_NO_GO=TRUE
DELTA_SPECTRAL_FLOW_DEGREE_NORMALIZATION_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR_DEGREE=selected_line_spectral_flow_degree_not_forced_one
RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS
```
