# Koide delta lattice-propagator radian-quantum no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_lattice_propagator_radian_quantum_no_go.py`  
**Status:** executable no-go; selected propagator phase unit remains open

## Theorem Attempt

Derive a retained lattice propagator identity

```text
G_C3(1) = exp(i * 2/d^2) G_0
```

on the selected endpoint, giving the Brannen phase `2/9`.

## Result

Negative.  On a one-dimensional selected endpoint, `C3` equivariance allows
any scalar propagator phase:

```text
G(1) = exp(i lambda) G_0.
```

Finite `C3` periodicity only gives root-of-unity phases.  It does not set
`lambda = 2/9`.

The closed finite-Dirac/APS support value remains exact:

```text
eta_APS = 2/9.
```

But the open selected propagator readout still has the form

```text
lambda_open = s eta_APS + c.
```

Basepoint preservation can remove `c`; it cannot force `s=1`.

## Residual

```text
RESIDUAL_PRIMITIVE = selected_open_propagator_phase_unit_lambda_equals_eta_APS
RESIDUAL_SCALAR = APS_to_open_propagator_scale_s_minus_one
COUNTERSTATE = equivariant_one_clock_phase_lambda_free
NEXT_ATTACK = hw1_baryon_Wilson_holonomy_or_new_endpoint_unit_law
```

## Hostile Review

This is not delta closure.  It prevents a support route from being promoted:
finite-lattice `eta_APS=2/9` is closed support, while the selected open
propagator phase unit is still a separate physical theorem.

## Verification

```bash
python3 scripts/frontier_koide_delta_lattice_propagator_radian_quantum_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_lattice_propagator_radian_quantum_no_go.py
```
