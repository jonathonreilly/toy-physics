# Signed Gravity Oriented Tensor-Source Lift Note

**Date:** 2026-04-26
**Status:** finite conditional tensor-source lift; scalar-only no-overclaim
preserved; not a physical signed-gravity claim
**Script:** [`../scripts/signed_gravity_oriented_tensor_source_lift.py`](../scripts/signed_gravity_oriented_tensor_source_lift.py)

This note goes after the decisive blocker isolated in
[`SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md`](SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md):

> Can the signed determinant source character localize beyond invariant `A1`
> into the full tensor source bundle?

The answer is not the old scalar-only answer. The scalar determinant character
alone remains `A1`-maximal. But there is a stronger and cleaner construction:

```text
T_g(Y) = chi_eta(Y) T_plus.
```

That is, the determinant-orientation line twists the already-retained tensor
source bundle.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Key Distinction

The previous blocker was correct for scalar sources:

```text
chi_eta rho
```

is a scalar source character. It has a canonical lift only into the invariant
`A1` lapse/trace sector. It cannot manufacture shift or shear components.

The new construction does not ask it to manufacture those components. Instead
it uses `chi_eta` as a local orientation-line character that tensors with an
ordinary tensor stress source:

```text
ordinary tensor source:       T_plus in lapse plus shift plus trace plus shear
orientation-line character:   chi_eta in Or(Det_APS D_Y)
oriented tensor source:       T_g = chi_eta T_plus.
```

So:

- if `T_plus` has only scalar/lapse/trace content, the signed source remains
  `A1` only;
- if `T_plus` has ordinary tensor content, the same derived sign coherently
  orients every occupied canonical tensor block.

This avoids the false move of deriving tensor components from a scalar sign.

## Finite Theorem

Assume:

1. the determinant source character `chi_eta` is derived as in
   [`SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md`](SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md);
2. the universal GR route supplies canonical block projectors:

```text
lapse plus shift plus trace plus shear;
```

3. an ordinary positive-norm tensor source `T_plus` exists in that bundle;
4. `T_plus` satisfies any linear Ward/conservation constraints:

```text
C T_plus = 0.
```

Then:

```text
T_g(Y) = chi_eta(Y) T_plus
```

is a well-defined oriented tensor source. It:

- commutes with the canonical block projectors;
- flips every occupied tensor block coherently;
- preserves linear constraints because `C(chi_eta T_plus)=chi_eta C T_plus`;
- gives locked tensor response signs under the block-diagonal GR operator;
- leaves null sectors at zero;
- does not change the positive inertial/norm side.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_oriented_tensor_source_lift.py
```

Result:

```text
[PASS] canonical lapse/shift/trace/shear projectors are exact
[PASS] orientation-line twist flips every occupied tensor block coherently
[PASS] orientation-line twist preserves linear Ward/conservation constraints
[PASS] block-diagonal GR operator gives locked tensor response signs
[PASS] scalar-only determinant character remains A1-only
[PASS] non-A1 signed tensor response requires an ordinary tensor source carrier
[PASS] non-claim gate remains closed
FINAL_TAG: SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_FINITE_CONDITIONAL
```

Representative finite readout:

```text
block_norms={'lapse': 0.956, 'shift': 0.687, 'trace': 0.804, 'shear': 1.198}
pair_signs={(+,+): +, (+,-): -, (-,+): -, (-,-): +}
```

## What This Resolves

The old matrix row:

```text
full tensor/Einstein localization beyond A1: BLOCKED
```

was too strong if read as a statement about all signed tensor sources.

Corrected status:

```text
scalar-only determinant source: A1-maximal
oriented tensor source bundle: finite conditional lift
```

The signed lane can go beyond `A1` only through the tensor product:

```text
Or(Det_APS D_Y) tensor TensorSource.
```

It cannot go beyond `A1` through:

```text
Or(Det_APS D_Y) tensor ScalarDensity
```

alone.

## Remaining Gaps

This is still finite and conditional.

Open items:

1. **Ordinary tensor source carrier.** The lift requires retained ordinary
   tensor stress content. The sign line does not create it.
2. **Continuum/family transport.** The oriented tensor bundle must be carried
   through the retained continuum/refinement and actual graph-family APS
   constructions.
3. **Nonlinear tensor dynamics.** The audit checks a finite block-diagonal
   quadratic operator, not full nonlinear signed tensor dynamics.
4. **Sector preparation.** The existence of the oriented `-` tensor sector is
   still a boundary-sector/preparation question.
5. **No phenomenology claim.** The construction is a tensor-source grammar,
   not a physical prediction.

## Transport Follow-Up

The first transport/retention pass is now recorded in
[`SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_NOTE.md`](SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_NOTE.md)
with runner
[`../scripts/signed_gravity_tensor_source_transport_retention.py`](../scripts/signed_gravity_tensor_source_transport_retention.py).

Result:

```text
FINAL_TAG: SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FINITE_CONDITIONAL
```

That pass proves finite carrier retention on the audited restricted gravity
classes and finite projective/family transport of the orientation-line twist.
It also exposes the nonlinear even-jet obstruction to the naive `h -> -h`
promotion, so full nonlinear Einstein localization remains a separate graded
localization theorem target.

The graded target is now recorded in
[`SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md`](SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md)
with runner
[`../scripts/signed_gravity_continuum_graded_einstein_localization.py`](../scripts/signed_gravity_continuum_graded_einstein_localization.py).

Result:

```text
FINAL_TAG: SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM
```

That pass transports the signed tensor source over the chosen canonical
continuum family and replaces the naive sign flip by an odd/even formal
Einstein jet. Global nonlinear PDE existence remains outside the claim.

## Boundary Verdict

The new status is:

```text
SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_FINITE_CONDITIONAL
```

This reduces the decisive tensor blocker. The correct claim is not that the
scalar determinant source has hidden tensor content; it does not. The stronger
claim is that the derived orientation line can coherently twist the retained
tensor source bundle when such ordinary tensor stress content is present.
