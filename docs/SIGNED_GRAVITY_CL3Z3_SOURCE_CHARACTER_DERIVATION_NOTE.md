# Signed Gravity Cl(3)/Z^3 Source-Character Derivation Note

**Date:** 2026-04-26
**Status:** finite determinant-line host/source-character grammar result;
canonical selector and source action remain unforced; not a physical
signed-gravity claim
**Script:** [`../scripts/signed_gravity_cl3z3_source_character_derivation.py`](../scripts/signed_gravity_cl3z3_source_character_derivation.py)

This note goes after the remaining premise left by
[`SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md`](SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md):

> Does the original `Cl(3)`/`Z^3` stack force the determinant-orientation
> source-character grammar, or is that grammar still an added extension?

The finite result is positive only at the host/source-character grammar level:

```text
FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
```

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim. It is a
finite determinant-line host/source-character result, not a theorem that the
raw retained boundary complex selects an active signed source.

## Original Stack Used

The derivation uses only structures already present in the accepted framework
surface:

1. local algebra `Cl(3)`;
2. physical spatial substrate `Z^3`;
3. finite local Grassmann / staggered-Dirac dynamics;
4. determinant-line functoriality of the finite Grassmann Gaussian;
5. the retained observable-principle split:

```text
Z[J] = det(D + J),
W[J] = log |det(D + J)| - log |det D|.
```

No free sign is introduced.

## Derived Object

For a compact source region `Omega` with boundary `Y = partial Omega`, the
finite Grassmann operator restricted to the region and its boundary carries a
determinant line:

```text
Det(D_Omega).
```

The retained scalar observable principle uses the magnitude functor:

```text
Det(D_Omega) -> |Det(D_Omega)| -> log |det|.
```

The signed source-character grammar uses the real orientation functor of the
gapped APS boundary determinant line:

```text
Det_APS(D_Y) -> Or(Det_APS D_Y) -> {+1,-1}.
```

On a gapped boundary sector this orientation is:

```text
chi_eta(Y) = sign eta_delta(D_Y).
```

So the determinant-line object supplies two distinct outputs:

```text
positive source norm:          M_phys rho
orientation-character host:    chi_eta(Y) after choosing a local section
```

The conditional source-character law studied by the later harnesses is:

```text
J_g = chi_eta(Y) M_phys rho.
```

The determinant-line object hosts the orientation side of that law. It does
not by itself choose the section or force the active source coupling.

## Finite Derivation Chain

### 1. `Cl(3)` Supplies Boundary Orientation Reversal

The finite audit builds Pauli representatives of `Cl(3)`:

```text
{e_i, e_j} = 2 delta_ij I.
```

The pseudoscalar orientation element is:

```text
omega = e_1 e_2 e_3 = i I.
```

Reflecting one normal generator sends:

```text
omega -> -omega.
```

So the local algebra contains the operation needed to reverse boundary
orientation.

### 2. `Z^3` Locality Supplies Compact Regions And Sewing

Compact regions in the physical `Z^3` substrate have boundaries, and disjoint
regions sew by direct sum at the finite operator level:

```text
D_(Omega_1 disjoint Omega_2) = D_Omega1 direct-sum D_Omega2.
```

The finite Grassmann Gaussian then gives:

```text
Det(D_1 direct-sum D_2) = Det(D_1) tensor Det(D_2).
```

The audit checks determinant multiplicativity and `log|det|` additivity to
machine precision.

### 3. Magnitude And Orientation Split

The retained observable principle already derives the positive scalar
magnitude side:

```text
W = log |det|.
```

That side is sign-blind and supplies the positive norm/source scale.

The orientation side is not the magnitude. It is the local real orientation
character of the APS boundary determinant line:

```text
Or(Det_APS D_Y).
```

For the finite APS boundary model:

```text
eta(+,-,0) = (+1,-1,0),
chi(+,-,0) = (+1,-1,0).
```

Orientation-preserving refinement multiplies raw `eta` but leaves the
orientation character fixed:

```text
eta = [1,2,3,5],
chi = [1,1,1,1].
```

So raw `eta` is rejected as source strength; `sign(eta)` survives.

### 4. Locality Rejects Global Product Signs

For disjoint components, the total determinant orientation is a product. That
cannot be used as every local source sign. If a `+` compact source is later
accompanied by a remote `-` source, the local sign of the original `+` source
cannot flip.

Therefore the local source character is componentwise:

```text
J_g(x in Omega_a) = chi_eta(Y_a) M_a rho_a(x).
```

The audit checks that the local derivative remains block-local, while a global
product sign would incorrectly flip the local `+` source.

### 5. The Character Is Unique

The source-character grammar inherited from the determinant line is then the
one already audited in
[`SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md`](SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md):

```text
c(0) = 0,
c(+1) = +1,
c(-eta) = -c(eta),
c(k eta) = c(eta), k > 0.
```

The unique normalized local real solution is:

```text
c(eta) = sign(eta).
```

Thus, after choosing the determinant-orientation source-character grammar, the
finite stack identifies the local character:

```text
c(Y) = chi_eta(Y).
```

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_cl3z3_source_character_derivation.py
```

Result:

```text
[PASS] Cl(3) supplies an orientation-reversing normal operation
[PASS] finite Grassmann determinant line is functorial under disjoint sewing
[PASS] APS boundary determinant orientation gives sign(eta) with null/refinement controls
[PASS] local source derivative splits positive magnitude from local orientation character
[PASS] source-character grammar has unique chi_eta solution
[PASS] dependency audit uses original-stack structures and no free sign
FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
```

## What This Closes

This narrows the previous source-character grammar premise at the finite
determinant-line level:

- the determinant line is forced by the finite Grassmann Gaussian;
- `log|det|` supplies the positive scalar magnitude already retained;
- `Cl(3)` supplies boundary orientation reversal;
- the APS boundary determinant orientation supplies the local real character;
- `Z^3` locality and disjoint sewing force componentwise, not global-product,
  signs;
- refinement reduces raw `eta` to `sign(eta)`;
- the source-character uniqueness theorem then forces `chi_eta` inside a
  chosen local orientation/source section.

This is the cleanest current finite host for the conditional source-character
law:

```text
J_g = chi_eta(Y) M_phys rho
```

It is not, by itself, a derivation of the active `chi_eta rho Phi` source
term. The later naturally-hosted orientation-line audit shows that the same
determinant-line package supplies a `Z2` torsor/flat local system but does not
canonically select its section.

## What Remains Open

This is still not unconditional nature-grade closure.

Open items:

1. **Continuum determinant-line theorem.** The derivation is finite. It needs
   an inverse-limit or continuum version for arbitrary retained families.
2. **Actual-family APS construction.** The finite APS boundary model must be
   transported to the retained graph/lattice families used by the gravity
   lane.
3. **Tensor localization.** The scalar source character still lifts only to
   the invariant `A1` lapse/trace channel. The current finite route beyond
   `A1` is the oriented tensor-source lift
   `T_g = chi_eta T_plus`; the continuum graded pass now transports this lift
   over the chosen canonical continuum target and closes the nonlinear
   even-jet issue as an odd/even formal Einstein localization theorem.
4. **Dynamics and sector preparation.** The source-character derivation does
   not by itself prove physical preparation of opposite sectors.
5. **UV/core stability.** Same-sector attractive collapse remains the ordinary
   short-distance gravity problem.
6. **No phenomenology claim.** Nothing here licenses negative mass, shielding,
   propulsion, reactionless forces, or a physical signed-gravity prediction.

## Boundary Verdict

The new status is:

```text
CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
```

This is a materially stronger result than a free source-character axiom: the
orientation host is present on the finite original `Cl(3)`/`Z^3`
determinant-line surface. The remaining blockers are canonical section/source
selection, continuum transport, actual-family boundary realization, retained
tensor-source transport, and ordinary gravitational stability.

## Native Boundary-Complex Containment Follow-Up

The decisive containment audit is recorded in
[`SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md`](SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md)
with runner
[`../scripts/signed_gravity_native_boundary_complex_containment.py`](../scripts/signed_gravity_native_boundary_complex_containment.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
```

This sharpens the finite source-character result. The determinant-line grammar
is native at the functor/source-character level, but the raw retained
cochain/Hodge boundary operator

```text
D_Y = d + d^*
```

does not contain an unpaired gapped orientation-line APS mode. Its cochain
parity symmetry pairs the spectrum and gives `eta=0`; edge or face orientation
reversal is a relabeling control. The orientation-line APS realization used by
the signed-response harness is therefore an added extension unless a later
retained boundary theorem derives that line from the actual graph/refinement
complex.

The staggered-Dirac boundary realization audit now closes the most natural
escape hatch:

```text
FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
```

Retained-compatible staggered boundary operators are also eta-neutral. An odd
open face can create an unpaired eta, but it flips with the staggering-origin
choice and disappears under even refinement, so it is a quarantined imbalance
control, not a retained APS selector.

## Naturally Hosted Orientation-Line Follow-Up

The remaining host-versus-selector distinction is recorded in
[`SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md`](SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md)
with runner
[`../scripts/signed_gravity_naturally_hosted_orientation_line.py`](../scripts/signed_gravity_naturally_hosted_orientation_line.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

This keeps the finite determinant-line source-character grammar meaningful:
the retained Grassmann determinant functor naturally hosts a real orientation
line as a `Z2` torsor and flat local system. But it also sharpens the
limitation. A torsor is not a canonical signed section; raw Hodge and
retained-compatible staggered boundary operators remain eta-neutral, and the
hosted line does not by itself force the `chi_eta rho Phi` source term.

So the finite derivation should be read as a determinant-line host plus
conditional source-character grammar, not as a raw retained-boundary theorem
that already selects an active signed source.

## Nature-Grade Blocker Follow-Up

The five remaining blockers are audited in
[`SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md`](SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md)
with runner
[`../scripts/signed_gravity_nature_grade_closure_blockers.py`](../scripts/signed_gravity_nature_grade_closure_blockers.py).

Result:

```text
FINAL_TAG: SIGNED_GRAVITY_NATURE_GRADE_HARD_BLOCKERS_REDUCED_CONDITIONALS_REMAIN
```

That pass reduces the hard tensor obstruction through retained-carrier
transport, chosen-continuum transport, and a graded formal nonlinear Einstein
localization theorem: the scalar determinant source character is tensorially
maximal at invariant `A1`, while the derived orientation line can twist an
ordinary retained tensor source bundle. Nature-grade closure still requires
continuum determinant-line transport for the APS source character, actual
retained APS realization, sector preparation, any demanded global nonlinear
PDE dynamics, and UV/core stability.
