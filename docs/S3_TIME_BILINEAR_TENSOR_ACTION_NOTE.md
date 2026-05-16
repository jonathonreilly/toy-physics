# Route 2 Tensorized Action from the Bilinear Carrier (definition-only)

**Date:** 2026-04-14 (originally); 2026-05-04 (first audited_renaming scope-narrow); 2026-05-16 (title/header honesty pass)
**Branch:** `codex/review-active`
**Status:** **definition-only** of `I_TB` and `Xi_TB` from named upstream inputs `(I_R, K_R, Lambda_R, u_*)`. The construction's identification with the **physical tensor dynamics law** (Einstein/Regge) is open and conditional on the upstream certificates listed below.
**Claim type:** open_gate
**Audit classification (matches load-bearing step class E, definition):** `audited_renaming` is the expected verdict for this note in its current scope; the next re-audit will land `audited_clean` only when items 2 and 5 below become retained-grade.
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

**Definition (scope-narrowed).** Given the following upstream inputs, the tensorized action `I_TB(f, a ; j)` and the spacetime carrier
`Xi_TB(t ; q)` defined below are well-defined and the algebraic identities
verified by the runner hold:

1. **`I_R` certificate** — the exact scalar Schur boundary action
   `I_R(f ; j) = (1/2) f^T Lambda_R f - j^T f`, associated with
   [`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](OH_SCHUR_BOUNDARY_ACTION_NOTE.md).
2. **`K_R` certificate** — the exact bilinear support carrier from
   [`S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md`](S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md),
   which is itself narrowed here to definition-only pending its own upstream
   certificates.
3. **`Lambda_R` certificate** — exact symmetric positive definite slice
   generator from the Schur boundary action, associated with
   [`S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md`](S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md).
4. **Canonical slice seed certificate** — exact normalized `u_*` on the
   slice carrier, associated with
   [`S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md`](S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md).
5. **Tensor-dynamics bridge theorem** — identification of the constructed
   `I_TB`/`Xi_TB` with the **physical** tensor dynamics law (Einstein/Regge
   on `PL S^3 x R`).

Items 1, 3, and 4 name existing current-main source surfaces but are not
treated here as retained-grade closure. Items 2 and 5 remain load-bearing
gaps for any future retained physical-dynamics claim.

## Audit-driven title and header honesty pass (2026-05-16)

The 2026-05-16 re-audit of this note carried verdict
`audited_renaming` (class E, definition). The note's body had already been
narrowed correctly on 2026-05-04 to a definition-only scope, but the
*title* still read "Route 2 **Exact** Tensorized Action from the Bilinear
Carrier" and the "Verdict" / "What this narrowed note closes" sections
re-used phrases like "exact tensorized construction" that an out-of-scope
reader could mis-read as a derivation claim. This pass:

- removes "Exact" from the title and replaces it with "(definition-only)";
- replaces remaining "exact" qualifiers inside the verdict / closure
  bullets with "definition-only" / "definitional";
- adds an explicit *Audit classification* line in the header so the next
  auditor and the publication control-plane both see the load-bearing
  step class (`E`, definition) and the matching verdict
  (`audited_renaming`) on first read.

No new theorem, new dependency edge, or new runner check is asserted by
this pass. It is a wording-only repair of the audit-honesty surface; the
underlying upstream-input and Einstein/Regge bridge gaps named below are
unchanged.

**Current upstream dep effective_status (per audit ledger as of the
2026-05-04 `audited_renaming` salvage):**

- `oh_schur_boundary_action_note` → `retained_bounded`
- `s3_time_bilinear_tensor_primitive_note` → `audited_renaming`
- `s3_time_transfer_matrix_bridge_note` → `audited_conditional`
- `s3_time_spacetime_tensor_primitive_note` → `audited_conditional`

That is, the four wired upstream deps are at definition-only, bounded, or
conditional grade — none is retained-clean — which is why this note's own
verdict remains `audited_renaming` (definition-only under named inputs)
rather than promoting toward a derived physical-dynamics claim. The
verdict will not move until at least items 2 and 5 are supplied as
retained certificates.

## Physical-dynamics identification (deferred to a separate bridge)

This note **does not derive**:

- The interpretation of `I_TB` as an exact tensor dynamics action (rather
  than a constructed quadratic functional)
- The interpretation of `Xi_TB(t; q) = vec K_R(q) ⊗ V_R(t)` as a physical
  spacetime tensor field (rather than a definitional outer product)
- The bridge from `I_TB`'s stationary points to the Einstein equations on
  `PL S^3 x R`

These three are the load-bearing bridge gaps flagged by the 2026-05-04
audit. Until those certificates are on the retained-grade surface, any
phrasing like "Route 2 has a tensorized action" is a **definitional
statement under upstream inputs**, not a derived physical-dynamics
theorem.

## Verdict (scope-narrowed)

Once the bilinear support carrier `K_R` is admitted (under its own
upstream-input conditional), Route 2 has a **definition-only**
tensorized construction. The Einstein/Regge identification — i.e., the
step that turns `I_TB` into a physical tensor dynamics law — remains the
open bridge.

The scalar Schur backbone and Route-2 kinematic scaffold named here are
algebraic objects with their own upstream-input conditionals, so they can
be combined with `K_R` into a definition-only tensorized action / coupling
candidate. The construction itself is algebraically clean; the
physical-meaning bridge is the gap.

## Named inputs for the definition

The definition names the following inputs. This note does not assert that
each input is retained-grade on current main:

- `S^3` spatial compactification
- anomaly-forced single-clock time
- background `PL S^3 x R`
- scalar Schur boundary action
  - `I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f`
- bilinear support carrier (named input under its own upstream conditional)
  - `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

## Algebraic tensorized construction

The minimal tensor extension is

`I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - vec K_R(q)||^2`.

The construction is algebraic under the named inputs:

- `I_R` is supplied as an input
- `vec K_R` is supplied as an input
- the quadratic penalty is purely definitional

## Algebraic spacetime carrier

Let

- `u_*` be the canonical normalized slice seed
- `V_R(t) = exp(-t Lambda_R) u_*`

Then the definition gives the Route-2 spacetime carrier

`Xi_TB(t ; q) = vec K_R(q) \otimes V_R(t)`.

This is the tensor analogue of the earlier bounded `Xi_R^(0)` construction,
but now built from the bilinear carrier rather than the bounded
`Theta_R^(0)` readout. Its physical tensor-dynamics interpretation remains
the open bridge named above.

## What this narrowed note closes

On the current Route-2 build program:

- tensorized action/coupling definition: supplied under named inputs
- endpoint carrier expression: supplied under named inputs
- physical tensor-dynamics identification: not supplied here

## What is still open

What is **not** yet closed is the last theorem:

> prove that the definition-only tensorized carrier / action `K_R`,
> `I_TB`, and `Xi_TB` are the Einstein/Regge tensor dynamics law on the
> current restricted class.

So the blocker has moved from:

- "there is no written tensor primitive"

to:

- "the named carrier has not yet been identified uniquely with the GR
  tensor law, and items 2 and 5 of the upstream-input list above are
  still required as retained-grade certificates before the construction
  can carry that identification."

## Bottom line

Route 2 now has a definition-only tensor carrier and tensorized
action/coupling construction on `PL S^3 x R`, under the named upstream
inputs.

The remaining GR gap is the final dynamics identification, not the absence of
a written carrier/action definition.
