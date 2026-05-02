# Signed Gravity Staggered-Dirac APS Boundary Realization Note

**Date:** 2026-04-26
**Status:** support / retention-compatible staggered-Dirac boundary APS
realization no-go; not a physical signed-gravity claim
**Script:** [`../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py`](../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py)

This note follows
[`SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md`](SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md).
The raw cochain/Hodge boundary complex does not contain the orientation-line
APS source character. The natural remaining escape hatch was:

> Maybe the retained staggered-Dirac / Grassmann boundary operator, rather
> than the raw Hodge operator `D_Y=d+d^*`, contains a gapped unpaired
> eta/Pfaffian orientation mode.

The finite answer is:

```text
FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
```

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Strict Realization Gate

A native staggered-Dirac APS selector would need all of:

```text
eta_delta(D_stag,Y) != 0,
h_delta(D_stag,Y) = 0,
chi_eta = sign eta_delta(D_stag,Y),
orientation reversal flips chi_eta,
taste-compatible refinement preserves chi_eta,
no rank-one orientation line is added,
no Hodge/kernel projection is inserted.
```

The harness tests retained-compatible finite boundary operators built from the
same Kogut-Susskind staggered structure used elsewhere in the gravity lane:

```text
H_stag =
  sum_mu eta_mu(x) (-i/2) [shift_+mu - shift_-mu]
  + m epsilon(x).
```

## Retained-Compatible Boundary Readout

On taste-compatible cycles, tori, and even open faces, the staggered boundary
operator is gapped but eta-neutral:

```text
cycle8_apbc_m0:    eta=0, zero=0, chi=0
cycle10_apbc_m03:  eta=0, zero=0, chi=0
torus4x4_apbc_m0:  eta=0, zero=0, chi=0
torus4x6_apbc_m03: eta=0, zero=0, chi=0
open4x4_m03:       eta=0, zero=0, chi=0
open4x5_m03:       eta=0, zero=0, chi=0
```

The spectra are paired to numerical precision, even when the mass/staggering
gap removes zero modes.

Orientation and basis controls do not create a branch:

```text
eta=[0,0,0]
chi=[0,0,0]
orientation_reversal_err=0.0e+00
relabel_spectral_err=2.2e-15
```

So retained-compatible staggered boundaries do not repair the raw Hodge
eta-neutrality.

## Odd-Open-Face Trap

There is a tempting unpaired eta on an odd open face:

```text
open5x5_origin0_m03: eta=+1, chi=+1
open5x5_origin1_m03: eta=-1, chi=-1
open10x10_refined_m03: eta=0, chi=0
```

This is not a selector. It is a sublattice-imbalance artifact:

- the sign flips under a one-site staggering-origin shift;
- it disappears under even/taste-compatible refinement;
- it is tied to an odd open-face cell count, not a boundary orientation
  invariant.

The harness therefore quarantines it as:

```text
classification=odd_sublattice_imbalance_control
```

## Pfaffian Control

The real skew staggered kinetic kernel has a Pfaffian sign once a basis
orientation is chosen. But that sign is not an invariant branch label:

```text
cycle8_skew_apbc:  pf=+1.250e-01 -> -1.250e-01
torus3x4_skew_apbc: pf=+2.812e-01 -> -2.812e-01
```

In both cases the odd basis relabel preserves the spectrum and determinant:

```text
eig_err <= 1.1e-15
det_err = 0.0e+00
```

So the Pfaffian sign is determinant-line orientation metadata unless an
additional rule fixes the determinant-line orientation as physical boundary
data. It is not, by itself, a gauge-invariant `chi_eta`.

## Orientation-Line Insertion Control

The signed APS branch appears exactly when the previous extension is added:

```text
raw=(eta=0, zero=0, gap=1.000)
added_line=[(+1,+1,0,+1), (-1,-1,0,-1)]
```

The tuple is:

```text
(orientation, eta_ext, zero_ext, chi_ext).
```

This confirms the earlier classification: a rank-one orientation-line summand
is enough to produce the APS sign, but that is an extension/control unless a
retained theorem derives the line.

## Source Basis

The native staggered boundary eta contributes no orientation-odd source:

```text
positive retained source: [ +1, +1 ]
native staggered eta:     [  0,  0 ]
desired signed source:    [ +1, -1 ]
```

The residual remains:

```text
native_residual=1.414e+00
```

The odd-open-face control can mimic `[+1,-1]`, but it is not admissible as a
retained selector because it fails origin and refinement controls.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py
```

Result:

```text
[PASS] retained-compatible staggered boundary operators are eta-neutral
[PASS] staggered boundary orientation/relabel controls do not create eta sign
[PASS] odd-open-face unpaired eta is quarantined as sublattice imbalance
[PASS] Pfaffian sign is determinant-line orientation metadata, not invariant branch
[PASS] orientation-line insertion creates the APS sign only as a control
[PASS] native staggered boundary source basis cannot span signed source
[PASS] non-claim gate remains closed
FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
```

## Boundary Verdict

The natural staggered-Dirac escape hatch is closed at this finite level:

```text
The retained-compatible staggered-Dirac / Grassmann boundary operator does
not currently realize a native gapped unpaired APS eta/Pfaffian selector.
```

The determinant-orientation source-character grammar remains meaningful at
the finite functor level, but the actual boundary operator needed for signed
response still requires an added orientation-line realization unless a sharper
retained graph/refinement theorem derives it.

No physical signed-gravity claim follows from this note.

## Hosted-Versus-Selected Follow-Up

The determinant-line host question is now audited in
[`SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md`](SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md)
with runner
[`../scripts/signed_gravity_naturally_hosted_orientation_line.py`](../scripts/signed_gravity_naturally_hosted_orientation_line.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

This is the current sharp classification: the orientation line is naturally
hosted by the retained determinant-line package as a `Z2` torsor/local system,
but no canonical section or active source term is forced.
