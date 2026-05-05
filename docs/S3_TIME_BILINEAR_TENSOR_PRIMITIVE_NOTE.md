# Route 2 Exact Bilinear Tensor Primitive

**Date:** 2026-04-14 (originally); 2026-05-04 (audited_renaming scope-narrow)
**Branch:** `codex/review-active`
**Status:** **definition-only** of a new bilinear microscopic carrier `K_R(q)` from named coordinates `(delta_A1, u_E, u_T)`. The decoupling fact, the exact aligned-bright property, and the tensor-primitive interpretation are **conditional on upstream retained derivations** that this note does not provide; see "Audit-driven scope narrowing" below.
**Primary runner:** [`scripts/frontier_s3_time_bilinear_tensor_primitive.py`](../scripts/frontier_s3_time_bilinear_tensor_primitive.py) (PASS=4/0)

## Audit-driven scope narrowing (2026-05-04)

The 2026-05-04 audit verdict was `audited_renaming`. The runner verifies
the algebraic shape of `K_R(q)` once the input coordinates
`(delta_A1, u_E, u_T)` and the decoupling fact are accepted; the verdict
narrows the load-bearing claim to the **definition** of the bilinear
carrier from those named inputs, not to a derivation of the inputs from
first principles.

The renaming criterion (from the audit): *"A second audit should re-check
whether an upstream retained derivation exists for the exact decoupling
fact and the tensor-primitive identification, since none is included in
this restricted packet."* This note now adopts the definition-only scope
and records the retained-elsewhere dependencies the closure would need.

## Statement (scope-narrowed)

**Definition (scope-narrowed).** Given input coordinates and the decoupling
fact below as upstream retained inputs, the bilinear microscopic tensor
carrier `K_R(q)` on the seven-site star support is well-defined and the
algebraic shape stated below holds.

This note **does not derive**:

- The decoupling fact `delta_A1 ⊥ {E_x, T1x, E_perp, T1y, T1z}`
- The exact aligned-bright coordinates `u_E(q) = <E_x, q>`, `u_T(q) = <T1x, q>`
- The interpretation of `K_R(q)` as a **physical** tensor primitive
  (rather than a definitional bilinear object)

These are the three load-bearing upstream dependencies flagged by the
2026-05-04 audit. To close this lane to retained-grade, a separate
retained theorem must supply:

1. A retained derivation of the `delta_A1`-decoupling property from the
   support-side Green / Schur machinery on the star support.
2. A retained derivation of the aligned-bright coordinate identification
   `u_E ↔ <E_x, ·>`, `u_T ↔ <T1x, ·>` from the canonical bright/dark
   decomposition of the support block.
3. A bridge theorem identifying the bilinear carrier `K_R(q)` with the
   physical tensor primitive used in the GR-readout chain (rather than as
   a constructed object whose physical meaning is asserted).

Until those three dependencies are on the retained surface, the corollary
"`K_R(q)` is the **physical** microscopic tensor primitive on the support
block" is **conditional on the bridges**, not a direct consequence of this
note.

## Exact ingredients (under upstream retained inputs)

On the seven-site star support, taking the decoupling fact as retained
upstream:

- the exact scalar background datum is
  - `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`
- the exact aligned bright coordinates are
  - `u_E(q) = <E_x, q>`
  - `u_T(q) = <T1x, q>`

The key exact decoupling fact (asserted, retained-elsewhere):

> `delta_A1` is exactly blind to all non-`A1` perturbations, including
> `E_x`, `T1x`, `E_perp`, `T1y`, and `T1z`.

So the scalar background coordinate and the aligned bright coordinates factor
cleanly.

## Exact primitive

Define the exact microscopic tensor carrier

`K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q) u_E(q), delta_A1(q) u_T(q)]]`.

Equivalently, as a 4-vector:

`vec K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`.

This carrier is:

- exact
- microscopic
- support-side
- prior to any metric/curvature readout

## Exact endpoint law

For the canonical `A1` background family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

the exact background scalar is

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

For unit aligned perturbations, the carrier columns are exact:

- `K_R(q_A1 + E_x) - K_R(q_A1) = [[1,0],[delta_A1(r),0]]`
- `K_R(q_A1 + T1x) - K_R(q_A1) = [[0,1],[0,delta_A1(r)]]`

So the endpoint coefficient theorem is now exact on the carrier itself:

- at `e0`: bright column = `(1, 1/6)`
- at `s / sqrt(6)`: bright column = `(1, 0)`

## Relation to the old bounded prototype

The prior bounded tensor pair

`Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

is not the exact primitive. It is a bounded linear readout of the exact
carrier.

On the canonical `A1` family, the current bounded projection is

- `gamma_E = a_E u_E + b_E delta_A1 u_E`
- `gamma_T = a_T u_T + b_T delta_A1 u_T`

with the coefficients `a_E, b_E, a_T, b_T` fixed by the two bounded endpoint
values already measured from the old `eta_floor_tf` pipeline.

So the exact carrier is now separated cleanly from the bounded numerical
readout.

## What this changes

This removes the earlier blocker:

> “Route 2 lacks any exact microscopic tensor primitive.”

That statement is no longer true.

What remains open is narrower:

> identify the exact bilinear carrier `K_R` with the final Einstein/Regge
> tensor dynamics law on the current restricted class.

## Bottom line

The exact new microscopic tensor primitive is:

`K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`.

The missing theorem is no longer the existence of an exact tensor carrier. It
is the final dynamics identification of that exact carrier.
