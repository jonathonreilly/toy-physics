# Koide delta determinant-line universal-endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_determinant_universal_endpoint_no_go.py`  
**Status:** no-go; determinant-line universality fixes the closed carrier, not the selected endpoint map

## Theorem Attempt

Use the determinant line as the universal carrier of APS/eta holonomy.  If the
selected Brannen endpoint line were forced to be that determinant line with its
based orientation, then:

```text
delta_open = eta_APS.
```

## Result

Negative from retained data alone.  The determinant line supplies the closed
holonomy carrier.  The selected open endpoint still needs a specified based,
orientation-preserving isomorphism from that carrier.

Without that isomorphism, tensor powers, duals, and flat twists give:

```text
F(eta) = n eta + c.
```

The universal property tells us where the closed eta lives.  It does not make
the selected open Brannen endpoint the unit determinant line.

## Countermaps

The runner checks determinant-compatible selected endpoint maps:

```text
F(eta) = 0
F(eta) = eta
F(eta) = -eta
F(eta) = 2 eta
F(eta) = eta + 1/9
```

Only the identity, untwisted map closes.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_ISOMORPHISM = based_orientation_preserving_selected_determinant_identity_not_retained
RESIDUAL_SCALAR = n_minus_one_plus_c_over_eta_APS
```

## Falsifiers

- A retained theorem that the selected Brannen endpoint is the based unit
  determinant line.
- A retained theorem excluding tensor powers, duals, and flat endpoint twists.
- A retained orientation/basepoint theorem deriving `n = 1` and `c = 0`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_determinant_universal_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_DETERMINANT_UNIVERSAL_ENDPOINT_NO_GO=TRUE
DELTA_DETERMINANT_UNIVERSAL_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_ISOMORPHISM=based_orientation_preserving_selected_determinant_identity_not_retained
RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS
```
