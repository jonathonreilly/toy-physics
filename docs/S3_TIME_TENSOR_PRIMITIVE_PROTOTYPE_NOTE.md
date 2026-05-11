# Route 2 Tensor Primitive Prototype on `A1 x {E_x, T1x}`

**Status:** class-A definition only — the support-block prototype
`Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))` is **defined** as an ordered
pair of named admitted-input readouts on the seven-site star support, and
the runner verifies the affine `delta_A1` reproduction identities follow
mechanically once the named inputs are admitted. This note **does not**
derive the named inputs themselves, the bright-channel identification,
the asserted endpoint coefficient values, or any "physical tensor
primitive" interpretation of `Theta_R^(0)`.
**Date:** 2026-04-14 (originally); 2026-05-10 (audit-narrowing as
`audited_renaming`: explicit class-A definition framing under named
admitted inputs).
**Claim type:** open_gate
**Status authority:** independent audit lane only.
**Authority role:** records a class-A staging definition under named
admitted inputs; explicitly **does not** propose retained, bounded, or
positive-theorem promotion. Names the upstream gaps as the open theorem
targets.
**Primary runner:** [`scripts/frontier_s3_time_tensor_primitive_prototype.py`](../scripts/frontier_s3_time_tensor_primitive_prototype.py) (PASS=4/0)

## Audit boundary

The 2026-05-05 audit recorded the verdict `audited_renaming`, classifying
the load-bearing step as a definitional staging object whose asserted
endpoint coefficients, normalization, and affine reproduction values are
not derived from any cited authority or runner-internal first-principles
computation. The 2026-05-10 audit-narrowing refresh confirms there is
**no upstream retained-grade derivation** of the named inputs on `main`,
and adopts the explicit class-A definition framing.

**Cited authorities (one-hop deps; cited, not closed in this note):**

- [`S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md`](S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md)
  (`claim_type: open_gate`, `audit_status: audited_renaming`) — sibling
  Route-2 bilinear-carrier definition note. Cited as related, not as
  authority closure.
- [`S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md`](S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md)
  (`claim_type: bounded_theorem`, `audit_status: audited_conditional`)
  — sibling Route-2 spacetime-tensor candidate that consumes
  `Theta_R^(0)` as a bounded source-side input. Cited as related, not as
  authority closure.
- [`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
  (`claim_type: bounded_theorem`, `effective_status: retained_bounded`)
  — canonical Schur-boundary-action surface. Cited as the namesake of
  the support-side decomposition, not as the source of the
  `delta_A1`-decoupling derivation in this note.

**Admitted-context derivation gap (real, not import-redirect):**

This note explicitly admits the following upstream gaps. None of the
three cited authorities, and no other current atlas surface, supplies a
retained-grade derivation of any of them; there is therefore **no**
upstream authority closure for the named inputs.

1. A retained-grade derivation of the bright-channel identification
   `gamma_E(q) = <E_x, ·>` and `gamma_T(q) = <T1x, ·>` from a canonical
   bright/dark decomposition on the seven-site star support.
2. A retained-grade derivation of the exact reduced anisotropic shell
   amplitude that is used as the prototype's normalization.
3. A bridge theorem identifying the support-block pair `Theta_R^(0)`
   with any physical tensor primitive in the GR-readout chain (rather
   than as a definitional bounded readout asserted to be the right
   staging object).

These are **real derivation gaps**, not dependency-citation issues. The
note's name "tensor primitive prototype" is a label only; the in-note
content is restricted to the class-A definition of `Theta_R^(0)` under
the named admitted inputs and the runner-verified affine `delta_A1`
reproduction identity.

## Verdict (class-A definition only)

The exact tensor-valued Route-2 support observable is still missing.

The current frontier supplies a class-A staging definition:

- `Theta_R^(0)(q) := (gamma_E(q), gamma_T(q))`

on the microscopic support block

- `A1 x {E_x, T1x}`,

evaluated by reading off the aligned `E_x` and `T1x` response coefficients
after normalizing by the exact reduced anisotropic shell amplitude. This is
class-A polynomial algebra in the named admitted inputs (see "Audit
boundary" above).

It is the correct first working **definitional staging object** for the
Route-2 tool-build program. It is explicitly **not** a theorem-grade
tensor observable; the gap to such an observable is named as upstream
open derivation work above.

## Class-A definition under named admitted inputs

Fix the exact seven-site star support and the adapted support basis

- `A1(center) ⊕ A1(shell) ⊕ E_x ⊕ E_perp ⊕ T1x ⊕ T1y ⊕ T1z`.

For a scalar `A1` background `q`, **define** (under the three named
admitted inputs in "Audit boundary" above) the current bright-channel
coefficient pair by

- `Theta_R^(0)(q) := (gamma_E(q), gamma_T(q))`

where:

- `gamma_E(q)` is the aligned `E_x` response coefficient
- `gamma_T(q)` is the aligned `T1x` response coefficient

after normalizing by the exact reduced anisotropic shell amplitude.

This is the class-A definitional staging object currently available on
the Route-2 support block. The note **does not** derive the named
admitted inputs (bright-channel identification, exact reduced shell
amplitude, physical tensor-primitive bridge) — see "Audit boundary"
above for the explicit gap list.

## Why this is the staging definition

Under the named admitted inputs (see "Audit boundary"), the existing
runner already exhibits:

1. the route-2 scalar machinery stays scalar-only
2. the tensor boundary drive is bright only on
   - `E_x`
   - `T1x`
3. the remaining `A1` dependence is controlled by the exact support-side
   scalar
   - `delta_A1`

So the first staging object is not a large tensor algebra. It is the
smallest support observable that records those two bright coefficients.

That is exactly what the class-A definition of `Theta_R^(0)` does. This
is a definitional choice under named admitted inputs, not a theorem that
the staging object is the unique correct primitive.

## Endpoint coefficients (runner readouts under named inputs)

On the two unit-charge `A1` endpoint backgrounds:

- center background `e0`
- shell background `s / sqrt(6)`

the prototype coefficients **read off the runner under the named admitted
inputs** are:

- `Theta_R^(0)(e0) = (gamma_E, gamma_T)`
  - `(-3.772329e-04, +3.359952e-04)`
- `Theta_R^(0)(s / sqrt(6)) = (gamma_E, gamma_T)`
  - `(-2.010572e-04, +4.031968e-04)`

These are runner-internal readouts conditional on the named admitted
bright-channel identification and reduced-shell normalization (see
"Audit boundary"). They are **not** independently derived endpoint
coefficient theorems on this note's scope.

## Affine support law (runner-verified identity under named inputs)

The exact support-side scalar is

- `delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`

on the canonical `Q = 1` `A1` family.

Using the two endpoint values above, the class-A definition gives an
affine support-law identity

- `gamma_E(delta_A1)`
- `gamma_T(delta_A1)`

verified by the runner to reproduce:

- the canonical `A1` family at the `1e-8` level
- the exact local `O_h` and finite-rank `A1` baselines at the `few x 1e-6`
  level

The runner verifies the affine identity follows by polynomial-arithmetic
substitution from the class-A definition under the named admitted inputs.
This is class-A reproduction-identity arithmetic, not a derivation of the
named inputs themselves.

## What this changes

This note narrows the earlier blocker:

> "Route 2 lacks any concrete staging object for the first missing
> tensor-valued support observable."

The note supplies a class-A definitional staging object under named
admitted inputs. It does **not** close any of the upstream derivations,
the bright-channel identification, the reduced-shell normalization, or
the physical tensor-primitive bridge.

What remains open is narrower and is named explicitly above:

> close the three upstream gaps in "Audit boundary" and identify the
> staging object with a physical tensor primitive in the GR-readout
> chain.

## What this does not close

This note still does **not** close:

1. an exact tensor-valued support observable theorem
2. an exact endpoint coefficient theorem
3. an exact support-to-slice time-coupling law
4. full GR on Route 2

## Atlas-facing interpretation

This note **should not enter the atlas as a retained tool**.

It is a class-A definitional staging object under named admitted inputs.
Once the upstream open derivations close, this staging object and its
runner-verified affine identity become the obvious comparison surface
for a future retained-grade tensor support observable theorem.

## Bottom line (scope-bounded)

The class-A definition under named admitted inputs is:

- `Theta_R^(0)(q) := (gamma_E(q), gamma_T(q))`

with `gamma_E`, `gamma_T` the aligned `E_x` / `T1x` response coefficients
under the named bright-channel identification and reduced-shell
normalization. The runner verifies the affine `delta_A1` reproduction
identity follows from this definition by polynomial-arithmetic
substitution, conditional on the named admitted inputs.

The three open theorem targets are upstream of this note and are listed
explicitly in the "Audit boundary" section above:

1. retained-grade derivation of the bright-channel identification;
2. retained-grade derivation of the exact reduced anisotropic shell
   amplitude used as the prototype's normalization;
3. retained-grade bridge theorem identifying `Theta_R^(0)` with a
   physical tensor primitive in the GR-readout chain.

None of these is closed in this note. The note's contribution is the
class-A definition only.
