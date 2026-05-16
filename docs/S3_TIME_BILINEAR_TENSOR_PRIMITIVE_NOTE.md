# Route 2 Bilinear Tensor Carrier (Definition-Only)

**Date:** 2026-04-14 (originally); 2026-05-04 (first audit-narrowing as
`audited_renaming`); 2026-05-10 (audit-narrowing refresh: explicit
class-A definition framing under named admitted inputs); 2026-05-16
(science-fix renaming-repair: wire the missing retained-bounded
upstream `TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md` as the actual
`delta_A1` source, sharpen all load-bearing language to class-A
polynomial-identity substitution, and tag the finite-grid decoupling
check as class-D shadow rather than derivation).
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

- [`TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md`](TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: retained_bounded`,
  `audit_status: audited_clean`) — the actual retained-grade source of
  the scalar background datum `delta_A1(q) = phi_support(center)/Q -
  phi_support(arm_mean)/Q` used as a named admitted input here. The
  runner imports its `support_delta` helper directly. Cited as the
  authority closure for the `delta_A1` symbol only; it does **not**
  close the `delta_A1`-decoupling, aligned-bright coordinate, or
  physical-primitive-bridge gaps (those remain open and explicitly
  named below).
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

This note's load-bearing step is the class-A polynomial-identity
substitution

> `K_R(q) := [[u_E(q), u_T(q)], [delta_A1(q) u_E(q), delta_A1(q) u_T(q)]]`,

evaluated at the canonical `A1` background and at unit aligned
perturbations. Both substitution and evaluation are polynomial-identity
arithmetic in the named admitted inputs; no theorem of existence,
uniqueness, or physical interpretation is asserted by this step.

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
  - `delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`,
    supplied as a named admitted input by the retained-bounded note
    [`TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md`](TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md)
    (see the runner's `support_delta` import from the corresponding
    `frontier_tensor_support_center_excess_law.py`).
- the linear aligned bright coordinate symbols are
  - `u_E(q) := <E_x, q>`
  - `u_T(q) := <T1x, q>`

  Both are defined in this note as linear functionals of `q` against
  fixed basis vectors `E_x, T1x` from `build_adapted_basis()` in
  `frontier_same_source_metric_ansatz_scan.py`. Whether `(u_E, u_T)`
  coincide with the canonical aligned-bright coordinates of any bright/
  dark decomposition is **not** asserted by this note; that is the
  second upstream gap.

The key exact decoupling fact (assumed here; requires its own upstream
certificate):

> `delta_A1` is exactly blind to all non-`A1` perturbations, including
> `E_x`, `T1x`, `E_perp`, `T1y`, and `T1z`.

This is **not** derived in this note. The runner verifies a numerical
shadow of it (`blind_max < 1e-12` on a finite test set) but a numerical
check on a finite grid is class-D evidence, not a class-C derivation;
the upstream certificate remains the first open gap. So under the named
admitted inputs, the scalar background coordinate and the aligned
bright coordinates factor cleanly.

## Class-A definitional substitution (no primitive theorem asserted)

Under the named admitted inputs `(delta_A1, u_E, u_T)`, define the
bilinear carrier symbol

`K_R(q) := [[u_E(q), u_T(q)], [delta_A1(q) u_E(q), delta_A1(q) u_T(q)]]`.

Equivalently, as a 4-vector:

`vec K_R(q) := (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`.

The symbol `K_R` denotes nothing more than the right-hand-side polynomial
expression. Under the named admitted inputs, `K_R(q)`:

- is algebraically defined by polynomial-identity substitution
- inherits "microscopic, support-side" framing from the named inputs only
- has no asserted relation to any metric/curvature readout by this note

The section title says "no primitive theorem asserted" because this note
does **not** prove that this symbol is a physical tensor primitive on
the support block; that bridge is one of the three open gaps named in
the "Audit boundary" section above.

## Endpoint identity under the named inputs (class-A polynomial substitution)

For the canonical `A1` background family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

the background scalar formula is

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

as derived in the retained-bounded
[`TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md`](TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md)
and imported as a named admitted input here.

For unit aligned perturbations along the basis vectors `E_x, T1x`
(taken as named admitted inputs from the adapted basis, not derived as
canonical bright coordinates here), the polynomial-identity columns of
the symbol `K_R` are:

- `K_R(q_A1 + E_x) - K_R(q_A1) = [[1,0],[delta_A1(r),0]]`
- `K_R(q_A1 + T1x) - K_R(q_A1) = [[0,1],[0,delta_A1(r)]]`

These identities follow by polynomial substitution from the symbol's
definition; they do not assert that `(E_x, T1x)` are the physical
aligned-bright coordinates of any bright/dark decomposition. The
endpoint coefficient values, under the named admitted inputs, are:

- at `e0`: bright column = `(1, 1/6)`
- at `s / sqrt(6)`: bright column = `(1, 0)`

## Relation to the old bounded prototype (class-B bounded readout)

The prior bounded tensor pair

`Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))`

is treated by this note as a class-B bounded linear projection of the
class-A `K_R` symbol on the canonical `A1` family. The "exact primitive"
language used in earlier drafts of this note is **not** asserted here;
no positive theorem of primitive-ness for `K_R` is claimed.

On the canonical `A1` family, the bounded projection is

- `gamma_E = a_E u_E + b_E delta_A1 u_E`
- `gamma_T = a_T u_T + b_T delta_A1 u_T`

with the coefficients `a_E, b_E, a_T, b_T` fixed by the two endpoint
values measured from the old `eta_floor_tf` pipeline. This is a
class-B bounded readout (endpoint-fitted, not first-principles); the
identification of `K_R` with the underlying physical tensor primitive
is the third upstream gap and is **not** closed by the readout.

## What this changes (scope-restricted)

This note supplies a class-A definitional substitution for the symbol
`K_R` under the named admitted inputs. It does **not**:

- close any of the three upstream derivations named in the audit
  boundary section above,
- close the physical tensor-primitive bridge to GR readout,
- narrow the Route-2 blocker "Route 2 lacks any exact microscopic tensor
  primitive" — that blocker remains open at the physical-primitive
  level. Only the symbol-level substitution is supplied here.

What remains open is the same set of upstream theorem targets named in
the "Audit boundary" section; identification of `K_R` with any physical
tensor primitive in the GR-readout chain is outside this note's class-A
scope.

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
