# Constructed Route-2 Support Tensor Primitive: Response Jacobian of the Bounded Prototype

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** microscopic support block `A1 x {E_x, T1x}`  
**Status:** bounded constructed primitive candidate, not exact theorem

## Purpose

The current exact support-side machinery is scalar/rank-one on the `A1`
block, so it cannot produce an exact tensor observable on
`A1 x {E_x, T1x}`.

That no-go is already established. The remaining question is whether there is a
smaller tensor-valued object that survives where the scalar/rank-one machinery
fails, but still stays compatible with the current bounded tensor prototype
`Theta_R^(0)`.

The cleanest such object is the response Jacobian of the bounded prototype with
respect to the exact support scalar `delta_A1`.

## Constructed primitive candidate

Define the bounded support-response tensor primitive candidate

`Xi_R^(0) := d Theta_R^(0) / d delta_A1`

on the microscopic support block `A1 x {E_x, T1x}`.

Here:

- `Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))` is the current bounded
  two-channel prototype,
- `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q` is the exact
  surviving `A1` support scalar,
- and the derivative is taken along the exact projective `A1` support law.

This is the smallest new tensor-valued operator/object that survives the
current scalar/rank-one support no-go without reusing the blocked mixed support
block.

## Why this is the right new object

The exact support stack already proves:

1. the mixed `A1`-bright support block vanishes,
2. the support-to-active operator is rank one and charge-only,
3. the exact support scalar `delta_A1` is blind to `E_x` and `T1x`.

So the next thing that can possibly carry tensor information is not another
mixed support block. It is a response operator built from the bounded bright
channels themselves.

`Xi_R^(0)` does exactly that.

It is a `2`-component tensor response Jacobian with components:

- `Xi_E = d gamma_E / d delta_A1`
- `Xi_T = d gamma_T / d delta_A1`

## Compatibility with the bounded prototype

The bounded prototype obeys an affine law in the exact support scalar:

`Theta_R^(0)(q) = Theta_shell + Xi_R^(0) * delta_A1(q)`

where `Theta_shell = Theta_R^(0)(s / sqrt(6))`.

So `Xi_R^(0)` is compatible with `Theta_R^(0)` by construction:

- it is nonzero,
- it has the same two bright channels `E_x` and `T1x`,
- and it reconstructs the current bounded prototype from the exact support
  scalar `delta_A1`.

## Endpoint data

On the two exact unit-charge `A1` endpoint backgrounds:

- `e0`,
- `s / sqrt(6)`,

the bounded prototype endpoint values are:

- `Theta_R^(0)(e0) = (-3.772329e-04, +3.359952e-04)`
- `Theta_R^(0)(s / sqrt(6)) = (-2.010572e-04, +4.031968e-04)`

Therefore the response Jacobian is nonzero and points in a definite tensor
direction on the bright block.

## Structural status

`Xi_R^(0)` is structurally clean because:

- it lives on the exact microscopic support block,
- it uses the exact scalar support datum `delta_A1` as its single parameter,
- it has only the two bright tensor channels `E_x` and `T1x`,
- and it does not reintroduce the blocked mixed `A1`-bright support block.

It is therefore the smallest new tensor-valued support-side object that can be
reused as a Route-2 atlas tool while the exact tensor observable remains
absent.

## What this does not claim

This candidate is **not** yet:

1. an exact tensor-valued support observable,
2. an exact endpoint coefficient theorem,
3. an exact support-to-slice time-coupling law,
4. a full GR closure theorem.

It is a bounded constructed primitive candidate, not the final theorem.

## Practical conclusion

The current Route-2 build program now has one concrete new support-side tensor
object that survives the scalar/rank-one no-go:

`Xi_R^(0) = d Theta_R^(0) / d delta_A1`

This is the right comparison surface for any future exact tensor primitive on
`A1 x {E_x, T1x}`.
