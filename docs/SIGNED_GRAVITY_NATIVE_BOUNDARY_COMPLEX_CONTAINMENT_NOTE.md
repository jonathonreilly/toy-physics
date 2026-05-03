# Signed Gravity Native Boundary-Complex Containment Note

**Date:** 2026-04-26
**Status:** decisive finite containment no-go for the raw retained boundary
complex; not a physical signed-gravity claim
**Script:** [`../scripts/signed_gravity_native_boundary_complex_containment.py`](../scripts/signed_gravity_native_boundary_complex_containment.py)

This note answers the decisive blocker left by
[`SIGNED_GRAVITY_REMAINING_CLOSURE_GATES_NOTE.md`](SIGNED_GRAVITY_REMAINING_CLOSURE_GATES_NOTE.md):

> Does the original retained boundary complex actually contain the
> orientation-line APS source character, or did we add it?

The finite answer is:

```text
FINAL_TAG: SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
```

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Containment Criterion

The test uses a strict no-extra-structure definition of "contained."

The original retained boundary complex may use:

```text
C^0(Y) -> C^1(Y) -> C^2(Y)
D_Y = d + d^*
```

with finite graph/lattice cells, orientations of cells, and the native
cochain/Hodge structure.

It may not use:

```text
extra rank-one orientation-line summand,
projection that removes harmonic Hodge zero modes,
inserted chi_eta rho Phi source term,
hard gap axiom added by hand.
```

A native APS source character would require:

```text
eta_delta(D_Y) != 0,
h_delta(D_Y) = 0,
chi_eta(Y) = sign eta_delta(D_Y),
orientation reversal flips chi_eta.
```

## Raw Boundary Complex Result

The raw Hodge boundary operator is odd with respect to cochain parity:

```text
Gamma D_Y + D_Y Gamma = 0.
```

Therefore its nonzero spectrum is paired:

```text
lambda <-> -lambda.
```

The finite graph-family readout is:

```text
cycle8:       eta=0, zero=2, chi=0
cycle12:      eta=0, zero=2, chi=0
ladder6:      eta=0, zero=2, chi=0
grid4x4_disk: eta=0, zero=1, chi=0
annulus7:     eta=0, zero=2, chi=0
```

So the raw retained cochain/Hodge boundary complex is eta-neutral.

## Orientation Reversal Control

Reversing edge or face orientations changes basis signs in the same complex.
It does not create an APS spectral asymmetry:

```text
eta=[0,0,0]
chi=[0,0,0]
edge_reversal_spectral_err=0.0e+00
face_reversal_spectral_err=0.0e+00
```

This is the central no-go. The raw complex contains orientation conventions,
but those conventions act as relabelings of the Hodge operator, not as an
active APS source character.

## What Was Added

The previous APS sign can be recovered only after two non-native operations:

1. add an oriented one-dimensional APS line;
2. quarantine or project away the native Hodge zero modes.

Harness readout:

```text
raw_zero_modes=2
kernel_projected=True
added_orientation_line_dim=1
extended=[(+1,+1,0,+1), (-1,-1,0,-1)]
```

The tuple is:

```text
(orientation, eta_ext, zero_ext, chi_ext).
```

So the orientation-line carrier works as a controlled extension, but it is not
contained in the raw retained boundary complex audited here.

## Source Character Consequence

The raw boundary eta contributes no orientation-odd source vector:

```text
positive retained source: [ +1, +1 ]
raw boundary eta:         [  0,  0 ]
desired signed source:    [ +1, -1 ]
```

The fitted residual is:

```text
native_basis_residual=1.414e+00
```

The determinant-orientation metadata can represent `[+1,-1]`, but that is
metadata until a retained boundary theorem turns it into an APS operator and a
variational source term. In current artifacts, that step was added as the
orientation-line source principle.

## Relation To The Source-Character Derivation

This note does not erase
[`SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md`](SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md).
It sharpens its scope.

What remains native at the finite determinant-line grammar level:

```text
Det(D_Omega) supplies magnitude and orientation functors.
The unique normalized local real source character is sign(eta).
```

What is not contained in the raw boundary complex:

```text
D_Y = d + d^* does not supply an unpaired gapped orientation-line APS mode.
```

So the current best classification is:

```text
native determinant-orientation grammar: yes, finite/conditional
native raw boundary-complex APS realization: no
orientation-line APS realization: added extension unless a new theorem derives it
```

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_native_boundary_complex_containment.py
```

Result:

```text
[PASS] raw retained cochain/Hodge boundary complex is eta-neutral
[PASS] orientation reversal is a relabeling/control for raw eta
[PASS] APS sign appears only after orientation-line extension and kernel quarantine
[PASS] native raw boundary source basis cannot contain the signed source character
[PASS] non-claim and added-structure classification is explicit
FINAL_TAG: SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
```

## Boundary Verdict

The decisive answer is:

```text
The original raw retained boundary complex does not currently contain the
orientation-line APS source character.
```

The sign carrier used by the APS signed-response harness is therefore an added
orientation-line realization unless future work proves that this line is a
retained boundary mode of the actual graph/refinement complex.

No physical signed-gravity claim follows from this note.

## Staggered-Dirac Boundary Follow-Up

The most natural escape hatch is now audited in
`SIGNED_GRAVITY_STAGGERED_DIRAC_APS_BOUNDARY_REALIZATION_NOTE.md` (sibling
artifact; cross-reference only — not a one-hop dep of this note)
with runner
[`../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py`](../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
```

Retained-compatible staggered-Dirac boundary operators on cycles, tori, and
even open faces are gapped but eta-neutral. Odd open faces can create an
unpaired eta, but that sign flips under a one-site staggering-origin shift and
vanishes under even refinement, so it is quarantined as a sublattice-imbalance
control. Pfaffian signs also remain determinant-line orientation metadata
unless an extra rule fixes the line as physical boundary data.

## Naturally Hosted Orientation-Line Follow-Up

The hosted-versus-selected distinction is now audited in
`SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md`
(downstream follow-up; cross-reference only — not a one-hop dep of this note)
with runner
[`../scripts/signed_gravity_naturally_hosted_orientation_line.py`](../scripts/signed_gravity_naturally_hosted_orientation_line.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

The determinant-line package naturally hosts a real orientation line / `Z2`
torsor and transports it as a flat local system under refinement. But the
determinant functor alone does not choose a canonical signed section, does not
place an unpaired APS mode inside the audited boundary operators, and does not
force the `chi_eta rho Phi` source term.
