# Constructed Route-2 Support Tensor Primitive: Bounded Response Jacobian

**Date:** 2026-04-14; revised 2026-05-07
**Scope:** microscopic support block `A1 x {E_x, T1x}`
**Status:** bounded support-response theorem; not an exact tensor observable
**Claim type:** bounded_theorem
**Primary runner:** `scripts/frontier_s3_time_constructed_support_tensor_primitive.py` (PASS=7/0)

## Closed Bounded Statement

On the current bounded Route-2 staging surface, the support-response primitive
is the endpoint-fixed affine response of the bounded two-channel prototype

```text
Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))
```

with respect to the exact `A1` support scalar

```text
delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q.
```

The closed bounded object is

```text
Xi_R^(0)
  := (Theta_R^(0)(e0) - Theta_R^(0)(s/sqrt(6)))
     / (delta_A1(e0) - delta_A1(s/sqrt(6))).
```

Equivalently, it is the derivative of the endpoint-fixed affine bounded law

```text
Theta_aff(delta) = Theta_shell + Xi_R^(0) delta,
Theta_shell      = Theta_R^(0)(s/sqrt(6)).
```

This is the derivative statement used in this note. It is not a claim that the
raw tensor-frontier pipeline has been derived as an exact tensor observable.
The exact support scalar and the bounded affine tensor-law surface being
differentiated are the runner-backed surface of
[`TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md`](TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md).

## Runner Derivation

The primary runner recomputes the support basis, the exact support scalar, and
the bounded `Theta_R^(0)` endpoint values from the live Route-2 modules. Its
load-bearing endpoint data are:

```text
delta_A1(e0)        = 1.666666666667e-01
delta_A1(s/sqrt(6)) = -1.387778780781e-17

Theta_R^(0)(e0)        = (-3.772329167975e-04, +3.359952396063e-04)
Theta_R^(0)(s/sqrt(6)) = (-2.010572657265e-04, +4.031967723697e-04)
```

Therefore the endpoint denominator is `1/6` up to roundoff, and the response
Jacobian is computed rather than introduced by name:

```text
Xi_R^(0) = (-1.057053906426e-03, -4.032091965809e-04).
```

The vector is nonzero; the runner reports a norm of
`1.131344605899e-03`.

## Affine Compatibility

With

```text
Theta_shell = (-2.010572657265e-04, +4.031967723697e-04),
```

the bounded compatibility law is

```text
Theta_aff(q) = Theta_shell + Xi_R^(0) delta_A1(q).
```

The runner checks this law on the canonical `A1` family and on the two audited
baseline backgrounds:

```text
max canonical errors:     gamma_E=4.838e-09, gamma_T=1.067e-08
max audited-family errors: gamma_E=3.380e-06, gamma_T=4.190e-06
```

So the chain closed here is a bounded affine support-response closure: the
finite endpoint gap fixes a unique response vector, the vector is nonzero, and
the resulting affine law reconstructs the current bounded `Theta_R^(0)` staging
surface to the recorded tolerances.

## Structural Meaning

`Xi_R^(0)` lives on the `A1` support scalar and has image in the two bright
channels:

```text
Xi_R^(0) = (Xi_E, Xi_T)
        = (d gamma_E / d delta_A1, d gamma_T / d delta_A1)
```

for the endpoint-fixed affine bounded law above. It does not reintroduce a
mixed `A1`-bright support block: the runner's checked object has domain
`A1 x {E_x, T1x}` and image `(gamma_E, gamma_T)`.

This makes `Xi_R^(0)` a bounded comparison primitive for Route 2. It is useful
because it records the current two-channel tensor response to the exact scalar
support datum without claiming an exact support-side tensor observable.

## Boundaries

This note does not claim:

1. an exact tensor-valued support observable,
2. a first-principles derivation of the bounded endpoint coefficients,
3. an exact endpoint coefficient theorem,
4. an exact support-to-slice time-coupling law,
5. a full Einstein/Regge or GR closure theorem.

The exact bilinear carrier and readout-map questions remain separate Route-2
targets. This note closes only the bounded support-response Jacobian for the
current `Theta_R^(0)` staging surface.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_s3_time_constructed_support_tensor_primitive.py
```

Expected summary after the 2026-05-07 hardening:

```text
PASS=7 FAIL=0 TOTAL=7
```
