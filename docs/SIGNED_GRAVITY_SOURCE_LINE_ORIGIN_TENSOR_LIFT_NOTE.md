# Signed Gravity Source-Line Origin / Partial Tensor-Lift Note

**Date:** 2026-04-26
**Status:** conditional source-line origin theorem target; partial invariant
`A1` tensor lift; full tensor/Einstein lift still blocked
**Script:** [`../scripts/signed_gravity_source_line_origin_tensor_lift_audit.py`](../scripts/signed_gravity_source_line_origin_tensor_lift_audit.py)

This note develops the next nontrivial theory move after
[`SIGNED_GRAVITY_APS_LOCKED_AXIOM_EXTENSION_NOTE.md`](SIGNED_GRAVITY_APS_LOCKED_AXIOM_EXTENSION_NOTE.md).
The target is the origin of the eta-polarized source line:

```text
J_g = chi_eta(Y) M_phys rho.
```

The retained APS/Wald/Gauss route does not derive this term. The new move is
therefore not to hide the premise, but to make it sharper:

> Compact active gravitational sources are local sections of the real
> orientation line of the gapped APS boundary determinant line.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Source-Line Principle

For a compact source region `Omega` with boundary `Y = partial Omega`, let
`D_Y` be the APS boundary operator. On a gapped sector define:

```text
chi_eta(Y) = sign eta_delta(D_Y).
```

The candidate principle is:

```text
source packet = positive norm M_phys rho
              + local orientation in Or(Det_APS D_Y).
```

The inertial mass is the norm:

```text
M_inertial = M_phys > 0.
```

The active scalar source is the oriented section:

```text
J_g = chi_eta(Y) M_phys rho.
```

So the interaction is:

```text
S_src = - chi_eta(Y) M_phys <rho, Phi>.
```

This is a source-line origin target. It is still an added principle relative
to the old retained stack, but it is materially sharper than a free
phenomenological sign: the sign is the orientation of a named APS determinant
line, and the coefficient is fixed by the constraints below.

## Conditional Theorem

Assume a compact source satisfies:

1. **Local determinant-line orientation.** The source belongs to a local real
   orientation line `Or(Det_APS D_Y)` over its gapped boundary chamber.
2. **Positive norm separation.** The line norm gives positive inertial mass;
   orientation can affect active scalar charge but not the norm.
3. **Disjoint sewing locality.** Adding a remote source cannot flip the local
   active charge of an existing source.
4. **Orientation covariance.** Reversing the APS orientation reverses active
   scalar charge.
5. **Null quarantine.** `eta = 0` or zero-mode sectors are inactive controls
   or boundary defects.
6. **Real scalar action.** The weak scalar source action must be real.
7. **Refinement invariance.** Orientation-preserving refinement may multiply
   `eta`, but it cannot multiply the already normalized source mass.

Then the only coefficient over the three finite sectors is:

```text
c(Y) = sign eta_delta(D_Y) = chi_eta(Y).
```

Therefore:

```text
S_src = - chi_eta(Y) M_phys <rho, Phi>
```

is forced inside the source-line principle.

## Why The Controls Fail

The audit distinguishes the candidate from four tempting shortcuts.

| rule | result | failure mode |
|---|---|---|
| `eta_orientation_line` | pass | local, real, odd, null-quarantined, refinement-invariant |
| `unsigned_born_source` | control fail | ignores orientation; cannot produce `[+1,-1]` |
| `raw_eta_magnitude` | control fail | refinement multiplies `eta` and therefore source strength |
| `global determinant product` | control fail | adding a remote opposite sector flips a local source |
| `complex_eta_phase` | control fail | leaves the real scalar action surface |

The important distinction is local source-line orientation versus one global
determinant sign. A global product sign is not acceptable: two independent
sources with `+/-` orientations would give one product sign for both local
sources, so a remote spectator could flip the local active charge. That
violates source locality.

## Partial Tensor Lift

The existing universal-GR tensor notes already show that the exact scalar
observable generator has a tensor-valued Hessian candidate, but the full
Einstein/Regge identification is blocked by the missing curvature-localization
primitive.

The signed source line does not solve that full tensor problem.

What it can do cleanly is lift into the exact invariant `A1` lapse/trace
channel:

```text
Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0).
```

The audit checks:

- the `A1` projector commutes with sampled valid spatial rotations;
- the eta-polarized source vector stays in the `A1` channel;
- the complementary `E plus T1` channels remain rank-zero for this scalar
  source line.

So the status is:

```text
partial invariant A1 tensor lift: yes
full tensor / Einstein-Regge lift: no
```

This preserves the boundary from
[`UNIVERSAL_GR_POLARIZATION_FRAME_BUNDLE_BLOCKER_NOTE.md`](UNIVERSAL_GR_POLARIZATION_FRAME_BUNDLE_BLOCKER_NOTE.md):
the curvature-localization map is still missing.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_source_line_origin_tensor_lift_audit.py
```

Result:

```text
[PASS] origin constraints classify eta_orientation_line
[PASS] origin constraints classify unsigned_born_source
[PASS] origin constraints classify raw_eta_magnitude
[PASS] origin constraints classify complex_eta_phase
[PASS] local source-line sewing beats global determinant-product sign
[PASS] real source variation selects orientation sign over complex eta phase
[PASS] eta source line has invariant A1 tensor lift but not full tensor closure
FINAL_TAG: ETA_SOURCE_LINE_ORIGIN_CONDITIONAL_A1_TENSOR_LIFT
```

The first four rows are classification checks. Only `eta_orientation_line`
passes the origin constraints; the other rows pass because the audit correctly
rejects them as controls.

## What This Adds

This is a genuine theory improvement over the previous axiom note:

- the sign is no longer just a branch label placed into the source action;
- the host is the APS determinant-orientation line of each compact boundary;
- local sewing rules reject global determinant-product shortcuts;
- refinement invariance rejects raw `eta`;
- real-action discipline rejects complex eta phases;
- the tensor lift boundary is sharpened to "A1 yes, full tensor no."

## Remaining Review-Critical Gaps

This still does not close the lane unconditionally.

Open items:

1. **Axiom-to-source-line derivation.** The source-line principle itself still
   has to be derived from the original Cl(3)/`Z^3` axiom or admitted as a new
   extension.
2. **Full tensor lift.** The source line only populates the invariant scalar
   `A1` lapse/trace channel. It does not derive the complementary
   `E plus T1` curvature-localization bundle.
3. **Continuum determinant line.** The finite audit checks refinement
   invariance, but not a full continuum determinant-line theorem.
4. **Energy/UV closure.** Positive-inertial locked signs avoid the
   negative-mass runaway control, but ordinary same-sector short-distance
   gravity still needs the retained UV/core bound.
5. **Family portability.** Actual graph-family transport of the source-line
   orientation remains to be tested.

## Boundary Verdict

The new status is:

```text
ETA_SOURCE_LINE_ORIGIN_CONDITIONAL_A1_TENSOR_LIFT
```

This is the strongest current source-origin formulation for the signed
response lane. It should be treated as a conditional origin theorem inside a
new determinant-orientation source-line principle, not as a retained theorem
from APS/Wald/Gauss alone.

## Source-Character Uniqueness Follow-Up

The stronger source-character theorem is recorded in
[`SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md`](SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md)
with runner
[`../scripts/signed_gravity_source_character_uniqueness_theorem.py`](../scripts/signed_gravity_source_character_uniqueness_theorem.py).

Result:

```text
FINAL_TAG: ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL
```

That pass exhaustively enumerates the finite normalized real source
characters and proves that, within the determinant-orientation
source-character grammar, the only solution is `c(eta)=sign(eta)`. It also
shows that the tensor lift is maximal at the invariant `A1` channel: the
`E plus T1` complement has no nonzero canonical invariant vector.

The grammar premise is then attacked directly in
[`SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md`](SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md):

```text
FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
```

That result derives the determinant-orientation source-character grammar on
the finite accepted `Cl(3)`/`Z^3` Grassmann/staggered-Dirac surface.

## Hosted-Line Follow-Up

The later naturally-hosted orientation-line audit returns:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

It separates the host from the source principle. The determinant-line package
naturally hosts the real orientation line as a `Z2` torsor/local system, but
hosting alone does not choose the section and does not derive the
`chi_eta rho Phi` source term. Therefore the source-line principle in this
note is exactly the additional section/source principle that must either be
proved from retained structure or kept as a controlled extension.
