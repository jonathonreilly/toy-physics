# Route 2 Bilinear Tensor Carrier (Definition-Only)

**Date:** 2026-04-14 (originally); 2026-05-04 (first audit-narrowing as
`audited_renaming`); 2026-05-10 (audit-narrowing refresh: explicit
class-A definition framing under named admitted inputs).
**Branch:** `codex/review-active`
**Status:** class-A definition only — the bilinear microscopic carrier
`K_R(q)` is **defined** as a 2x2 matrix of polynomial expressions in the
named admitted-context inputs `(delta_A1, u_E, u_T)` and a runner-verified
algebraic identity follows mechanically. This note **does not** derive
the named inputs themselves, the `delta_A1`-decoupling fact, the aligned-
bright coordinate identification, or any "physical tensor primitive"
interpretation of `K_R`. The 2026-05-04 audit verdict was
`audited_renaming` and the 2026-05-10 audit-narrowing refresh below
keeps this scope.
**Claim type:** open_gate
**Status authority:** independent audit lane only.
**Authority role:** records a class-A bilinear definition under named
admitted inputs; explicitly **does not** propose retained, bounded, or
positive-theorem promotion. Names the three upstream gaps as the open
theorem targets.
**Primary runner:** [`scripts/frontier_s3_time_bilinear_tensor_primitive.py`](../scripts/frontier_s3_time_bilinear_tensor_primitive.py) (PASS=4/0)

## Audit boundary

The 2026-05-04 audit recorded the verdict `audited_renaming`, classifying
the load-bearing step as a definitional substitution under named inputs.
The 2026-05-10 audit-narrowing refresh confirms there is **no upstream
retained-grade derivation** of the named inputs on `main`, and adopts
the explicit class-A definition framing.

**Cited authorities (one-hop deps; cited, not closed in this note):**

- [`S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md`](S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md)
  (`claim_type: bounded_theorem`, `intrinsic_status: unaudited`) — the
  related Route-2 tensor-primitive surface this note identified as a
  conceptual sibling. Cited as related, not as authority closure.
- [`S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md`](S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md)
  (`claim_type: bounded_theorem`, `audit_status: audited_conditional`,
  `effective_status: audited_conditional`) — the Route-2 transfer-matrix
  bridge sibling row in this same cluster. Cited as related, not as
  authority closure.
- [`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: retained_bounded`) —
  the canonical Schur-boundary-action surface. Cited as the namesake of
  the support-side decomposition, not as the source of the
  `delta_A1`-decoupling derivation in this note.
- `S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md`
  (`claim_type: open_gate`, `intrinsic_status: unaudited`) — Wave-1
  sibling note treating a related discrete bilinear-tensor action.
  Cited as a sibling open-gate row, not as an authority closure;
  backticked to break length-2 citation cycle with the action note —
  citation graph direction is *action → this_primitive* (the action
  note imports `K_R` from this primitive; the reverse pointer is
  informational sibling, not load-bearing for this primitive's
  class-A definition).

**Admitted-context derivation gap (real, not import-redirect):**

This note explicitly admits the following three upstream gaps. None of
the four cited authorities, and no other current atlas surface, supplies
a retained-grade derivation of any of them; there is therefore **no**
upstream authority closure for the named inputs.

1. A retained-grade derivation of the `delta_A1`-decoupling property
   `delta_A1 ⊥ {E_x, T1x, E_perp, T1y, T1z}` from the support-side
   Green / Schur machinery on the seven-site star support.
2. A retained-grade derivation of the aligned-bright coordinate
   identification `u_E ↔ <E_x, ·>`, `u_T ↔ <T1x, ·>` from a canonical
   bright/dark decomposition.
3. A bridge theorem identifying the bilinear carrier `K_R(q)` with any
   physical tensor primitive in the GR-readout chain (rather than as a
   definitional bilinear object whose physical meaning is asserted).

These are **real derivation gaps**, not dependency-citation issues. The
note's name "tensor primitive" is a label only; the in-note content is
restricted to the class-A definition of `K_R` under the named admitted
inputs.

## Audit-driven scope narrowing (2026-05-04, refreshed 2026-05-10)

The 2026-05-04 audit verdict was `audited_renaming`. The runner verifies
the algebraic shape of `K_R(q)` once the input coordinates
`(delta_A1, u_E, u_T)` and the decoupling fact are accepted; the verdict
narrows the load-bearing claim to the **definition** of the bilinear
carrier from those named inputs, not to a derivation of the inputs from
first principles.

The renaming criterion (from the audit): *"A second audit should re-check
whether an upstream retained derivation exists for the exact decoupling
fact and the tensor-primitive identification, since none is included in
this restricted packet."* The 2026-05-10 refresh re-checks and confirms
**no such upstream retained-grade derivation exists on `main`**; the
class-A definition framing is therefore preserved.

## Statement (class-A definition only)

**Class-A definition (scope-bounded).** Given the named admitted-context
input symbols `delta_A1, u_E, u_T : R^k -> R` and the decoupling fact
of section "Named ingredients under upstream assumptions" as upstream
admitted inputs, the bilinear microscopic carrier `K_R(q)` on the
seven-site star support is **defined** as a 2x2 matrix of polynomial
expressions in `(delta_A1(q), u_E(q), u_T(q))` and the runner verifies
the corresponding endpoint-column identities to numerical zero.

This note's load-bearing step is the definitional substitution

> `K_R(q) := [[u_E(q), u_T(q)], [delta_A1(q) u_E(q), delta_A1(q) u_T(q)]]`,

evaluated at the canonical `A1` background and at unit aligned
perturbations. This is class-A polynomial algebra in the named admitted
inputs.

This note **does not derive** any of the following, which are the three
upstream gaps already named in the audit boundary above and re-listed
here for in-section visibility:

- The decoupling fact `delta_A1 ⊥ {E_x, T1x, E_perp, T1y, T1z}`.
- The exact aligned-bright coordinates `u_E(q) = <E_x, q>`,
  `u_T(q) = <T1x, q>`.
- The interpretation of `K_R(q)` as a **physical** tensor primitive
  (rather than a definitional bilinear object).

The note's name "tensor primitive" is a label for the definitional
bilinear carrier under named inputs; it is **not** a positive theorem
that `K_R` is a physical tensor primitive on the support block.

Related current surfaces include
[`S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md`](S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md),
[`S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md`](S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md),
[`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](OH_SCHUR_BOUNDARY_ACTION_NOTE.md),
and the action-side sibling `S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md`
(backticked to maintain the length-2-cycle break above).
This note does not treat those surfaces as retained-grade closure for the
three upstream dependencies above; see "Audit boundary".

## Named ingredients under upstream assumptions

On the seven-site star support, taking the decoupling fact as an assumed
upstream input:

- the exact scalar background datum is
  - `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`
- the exact aligned bright coordinates are
  - `u_E(q) = <E_x, q>`
  - `u_T(q) = <T1x, q>`

The key exact decoupling fact (assumed here; requires its own upstream
certificate):

> `delta_A1` is exactly blind to all non-`A1` perturbations, including
> `E_x`, `T1x`, `E_perp`, `T1y`, and `T1z`.

So the scalar background coordinate and the aligned bright coordinates factor
cleanly.

## Definition of the primitive

Define the exact microscopic tensor carrier

`K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q) u_E(q), delta_A1(q) u_T(q)]]`.

Equivalently, as a 4-vector:

`vec K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`.

This carrier is:

- algebraically defined under the named inputs
- microscopic
- support-side
- prior to any metric/curvature readout

## Endpoint identity under the named inputs

For the canonical `A1` background family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

the exact background scalar is

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

For unit aligned perturbations, the carrier columns are exact:

- `K_R(q_A1 + E_x) - K_R(q_A1) = [[1,0],[delta_A1(r),0]]`
- `K_R(q_A1 + T1x) - K_R(q_A1) = [[0,1],[0,delta_A1(r)]]`

So the endpoint coefficient identity holds on the carrier itself:

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

This narrows the earlier blocker:

> “Route 2 lacks any exact microscopic tensor primitive.”

The note supplies a definition-only bilinear carrier candidate. It does not
close the upstream derivations or the physical tensor-primitive bridge.

What remains open is narrower:

> identify the exact bilinear carrier `K_R` with the final Einstein/Regge
> tensor dynamics law on the current restricted class.

## Bottom line (scope-bounded)

The class-A definition under named admitted inputs is:

`K_R(q) := (u_E(q), u_T(q), delta_A1(q) u_E(q), delta_A1(q) u_T(q))`.

The runner verifies the endpoint-column identities follow from this
definition by polynomial-identity arithmetic, conditional on the named
admitted inputs.

The three open theorem targets are upstream of this note and are listed
explicitly in the "Audit boundary" section above:

1. retained-grade derivation of the `delta_A1`-decoupling fact;
2. retained-grade derivation of the aligned-bright coordinate
   identification;
3. retained-grade bridge theorem identifying `K_R` with a physical
   tensor primitive in the GR-readout chain.

None of these is closed in this note. The note's contribution is the
class-A definition only.
