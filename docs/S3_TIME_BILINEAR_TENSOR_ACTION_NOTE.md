# Route 2 Exact Tensorized Action from the Bilinear Carrier

**Date:** 2026-04-14 (originally); 2026-05-04 (audited_renaming scope-narrow)
**Branch:** `codex/review-active`
**Status:** **definition-only** of `I_TB` and `Xi_TB` from named upstream inputs `(I_R, K_R, Lambda_R, u_*)`. The construction's identification with the **physical tensor dynamics law** (Einstein/Regge) is open and conditional on the upstream certificates listed below.
**Primary runner:** [`scripts/frontier_s3_time_bilinear_tensor_action.py`](../scripts/frontier_s3_time_bilinear_tensor_action.py) (PASS=4/0)

## Audit-driven scope narrowing (2026-05-04)

The 2026-05-04 audit verdict was `audited_renaming`. The note's
load-bearing step is the **definition** of `I_TB` and `Xi_TB` as new
constructed symbols from the named inputs; it is not a derivation of
tensor dynamics from the axiom or from retained cited inputs. The note
itself acknowledges that the Einstein/Regge identification remains open.

The renaming criterion (from the audit, repair class
`missing_dependency_edge`): *"Provide retained upstream certificates for
I_R, K_R, Lambda_R, the canonical slice seed, and a bridge theorem
identifying the constructed action/carrier with the claimed tensor
dynamics."* This note now adopts the definition-only scope and records the
five upstream dependencies that closure would need.

## Statement (scope-narrowed)

**Definition (scope-narrowed).** Given the following upstream retained
inputs, the tensorized action `I_TB(f, a ; j)` and the spacetime carrier
`Xi_TB(t ; q)` defined below are well-defined and the algebraic identities
verified by the runner hold:

1. **`I_R` retained certificate** — the exact scalar Schur boundary
   action `I_R(f ; j) = (1/2) f^T Lambda_R f - j^T f`.
2. **`K_R` retained certificate** — the exact bilinear support carrier
   from `S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md` (which is itself
   currently under audited_renaming pending its own upstream certificates).
3. **`Lambda_R` retained certificate** — exact symmetric positive
   definite slice generator from the Schur boundary action.
4. **Canonical slice seed certificate** — exact normalized `u_*` on the
   slice carrier.
5. **Tensor-dynamics bridge theorem** — identification of the constructed
   `I_TB`/`Xi_TB` with the **physical** tensor dynamics law (Einstein/Regge
   on `PL S^3 x R`).

Items 1, 3, 4 are on the retained surface elsewhere; items 2 and 5 are the
load-bearing gaps.

## Physical-dynamics identification (deferred to a separate bridge)

This note **does not derive**:

- The interpretation of `I_TB` as an exact tensor dynamics action (rather
  than a constructed quadratic functional)
- The interpretation of `Xi_TB(t; q) = vec K_R(q) ⊗ V_R(t)` as a physical
  spacetime tensor field (rather than a definitional outer product)
- The bridge from `I_TB`'s stationary points to the Einstein equations on
  `PL S^3 x R`

These three are the load-bearing bridge gaps flagged by the 2026-05-04
audit. Until those certificates are on the retained surface, "Route 2 has
an exact tensorized action" is a **definitional statement under upstream
inputs**, not a derived physical-dynamics theorem.

## Verdict (scope-narrowed)

Once the exact bilinear support carrier `K_R` is admitted (under its own
upstream-input conditional), Route 2 has an exact **definitional**
tensorized construction. The Einstein/Regge identification — i.e., the
step that turns `I_TB` into a physical tensor dynamics law — remains the
open bridge.

The exact scalar Schur backbone and exact Route-2 kinematic scaffold are
already in hand, so they can be combined with `K_R` into a definitional
tensorized action/coupling candidate. The construction itself is
algebraically clean; the physical-meaning bridge is the gap.

## Exact inputs

Already exact on the current restricted class:

- `S^3` spatial compactification
- anomaly-forced single-clock time
- background `PL S^3 x R`
- scalar Schur boundary action
  - `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`
- exact bilinear support carrier
  - `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

## Exact tensorized construction

The minimal exact tensor extension is

`I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - vec K_R(q)||^2`.

This is exact because every input is exact:

- `I_R` is exact
- `vec K_R` is exact
- the quadratic penalty is purely algebraic

## Exact spacetime carrier

Let

- `u_*` be the canonical normalized slice seed
- `V_R(t) = exp(-t Lambda_R) u_*`

Then the exact Route-2 spacetime carrier is

`Xi_TB(t ; q) = vec K_R(q) \otimes V_R(t)`.

This is the tensor analogue of the earlier bounded `Xi_R^(0)` construction,
but now built from an exact microscopic carrier rather than the bounded
`Theta_R^(0)` readout.

## What is now closed

On the current Route-2 build program:

- exact tensor primitive: closed
- exact endpoint carrier law: closed
- exact tensorized action/coupling construction: closed as a construction

## What is still open

What is **not** yet closed is the last theorem:

> prove that the exact tensorized carrier/action `K_R`, `I_TB`, and `Xi_TB`
> are the Einstein/Regge tensor dynamics law on the current restricted class.

So the blocker has moved from:

- “there is no exact tensor primitive”

to:

- “the exact carrier has not yet been identified uniquely with the GR tensor
  law.”

## Bottom line

Route 2 now has an exact tensor carrier and an exact tensorized action/coupling
construction on `PL S^3 x R`.

The remaining GR gap is the final dynamics identification, not the absence of
an exact tensor primitive.
