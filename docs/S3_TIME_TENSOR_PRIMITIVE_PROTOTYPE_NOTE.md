# Route 2 Tensor Primitive Prototype on `A1 x {E_x, T1x}`

**Status:** bounded - tensor primitive prototype
**Date:** 2026-04-14  
**Purpose:** define the current bounded prototype for the first missing Route-2
**Primary runner:** [`scripts/frontier_s3_time_tensor_primitive_prototype.py`](../scripts/frontier_s3_time_tensor_primitive_prototype.py) (PASS=4/0, slow ~120s)
primitive and extract its endpoint data cleanly from the existing tensor
frontier

## Verdict

The exact tensor-valued Route-2 support observable is still missing.

But the current frontier is now clean enough to define the right bounded
prototype:

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

on the microscopic support block

- `A1 x {E_x, T1x}`.

This is the correct first working object for the Route-2 tool-build program.

It is **bounded**, not exact, because it still comes from the current
tensor-boundary-drive pipeline rather than a theorem-grade tensor observable.

## Definition

Fix the exact seven-site star support and the adapted support basis

- `A1(center) ⊕ A1(shell) ⊕ E_x ⊕ E_perp ⊕ T1x ⊕ T1y ⊕ T1z`.

For a scalar `A1` background `q`, define the current bright-channel coefficient
pair by

- `Theta_R^(0)(q) := (gamma_E(q), gamma_T(q))`

where:

- `gamma_E(q)` is the aligned `E_x` response coefficient
- `gamma_T(q)` is the aligned `T1x` response coefficient

after normalizing by the exact reduced anisotropic shell amplitude.

This is the cleanest bounded tensor-valued object currently available on the
Route-2 support block.

## Why this is the right prototype

The existing frontier already proves:

1. the route-2 scalar machinery stays scalar-only
2. the tensor boundary drive is bright only on
   - `E_x`
   - `T1x`
3. the remaining `A1` dependence is controlled by the exact support-side scalar
   - `delta_A1`

So the first missing primitive should not be a large tensor algebra. It should
be the smallest support observable that records those two bright coefficients.

That is exactly what `Theta_R^(0)` does.

## Endpoint coefficients

On the two exact unit-charge `A1` endpoint backgrounds:

- center background `e0`
- shell background `s / sqrt(6)`

the prototype coefficients are:

- `Theta_R^(0)(e0) = (gamma_E, gamma_T)`
  - `(-3.772329e-04, +3.359952e-04)`
- `Theta_R^(0)(s / sqrt(6)) = (gamma_E, gamma_T)`
  - `(-2.010572e-04, +4.031968e-04)`

These are the first concrete endpoint data for the Route-2 primitive chain.

## Affine support law

The exact support-side scalar is

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

on the canonical `Q = 1` `A1` family.

Using the two endpoint values above, the current bounded prototype already
gives an affine support law

- `gamma_E(delta_A1)`
- `gamma_T(delta_A1)`

that reproduces:

- the canonical `A1` family at the `1e-8` level
- the exact local `O_h` and finite-rank `A1` baselines at the `few x 1e-6`
  level

So the bounded prototype already organizes the `A1` dependence correctly.

## What this closes

This closes the "what should we build first?" ambiguity for Route 2.

The first new object to build exactly is not abstract anymore. It has a clean
bounded prototype:

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

with known endpoint values and known dependence on the exact support scalar
`delta_A1`.

## What this does not close

This note still does **not** close:

1. an exact tensor-valued support observable
2. an exact endpoint coefficient theorem
3. an exact support-to-slice time-coupling law
4. full GR on Route 2

## Atlas-facing interpretation

This note should not enter the atlas as a retained tool yet.

It is the right **bounded staging tool** for a future atlas row:

- exact Route-2 tensor support observable

Once the exact tensor observable is derived, this bounded prototype and its
endpoint data become the obvious comparison surface.

## Bottom line

The Route-2 build program now has:

- the exact primitive chain
- the theorem that the first missing primitive is tensor-valued
- and a clean bounded prototype for that first primitive:
  - `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

That is enough to start building the exact version on purpose.
