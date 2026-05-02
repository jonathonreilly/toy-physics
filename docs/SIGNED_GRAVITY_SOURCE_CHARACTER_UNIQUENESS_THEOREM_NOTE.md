# Signed Gravity Source-Character Uniqueness Theorem Note

**Date:** 2026-04-26
**Status:** strongest current breakthrough target; uniqueness theorem inside
the determinant-orientation source-character grammar; invariant `A1` tensor
maximality; not a physical signed-gravity claim
**Script:** [`../scripts/signed_gravity_source_character_uniqueness_theorem.py`](../scripts/signed_gravity_source_character_uniqueness_theorem.py)

This note records the strongest result currently available in the signed
gravitational response lane.

The target was to remove the appearance of an inserted phenomenological sign.
The result is:

```text
Within the determinant-orientation source-character grammar,
chi_eta is the unique normalized local real source character.
```

Equivalently:

```text
c(Y) = sign eta_delta(D_Y) = chi_eta(Y).
```

This is still not an original-axiom-only theorem. The remaining premise is
that compact active gravitational sources are local sections of the real APS
determinant-orientation line. But once that source-character grammar is
admitted, the signed coefficient is no longer free.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Breakthrough Target

The maximal result worth aiming for in this lane was:

1. derive the signed scalar coefficient from determinant-line structure rather
   than placing `chi_eta` by hand;
2. keep positive inertial mass as the determinant-line norm;
3. preserve local sewing, so a remote spectator cannot flip a local source;
4. keep the real scalar action surface;
5. quarantine null and zero-mode sectors;
6. preserve source strength under orientation-preserving refinement;
7. identify how far the source line can lift tensorially.

The finite theorem audit lands that target in a conditional but nontrivial
form.

## Source-Character Grammar

Let `eta` denote the APS spectral asymmetry of a gapped compact boundary
sector. A source-character coefficient is a map:

```text
c: eta-sector -> {-1,0,+1}
```

with these constraints:

1. **Normalization:** `c(+1) = +1`.
2. **Null quarantine:** `c(0) = 0`.
3. **Active nonzero sectors:** `c(eta) != 0` for `eta != 0`.
4. **Orientation reversal:** `c(-eta) = -c(eta)`.
5. **Positive norm separation:** `|c(eta)| = 1` for `eta != 0`; the mass norm
   is positive and not multiplied by `eta`.
6. **Refinement invariance:** `c(k eta) = c(eta)` for every positive
   orientation-preserving refinement factor `k`.
7. **Local sewing:** disjoint components carry their own local source
   character. The global product orientation of the total determinant line
   cannot be used as every local source coefficient.

## Theorem 1: Source-Character Uniqueness

On every finite eta window, the normalized real source-character constraints
have exactly one solution:

```text
c(eta) = sign(eta).
```

Therefore:

```text
c(Y) = chi_eta(Y)
```

and the scalar source action is:

```text
S_src = - chi_eta(Y) M_phys <rho, Phi>.
```

This is not a fit. The audit enumerates all maps
`{-N,...,N} -> {-1,0,+1}` for `N = 8` satisfying the grammar and finds exactly
one normalized solution. The proof is also immediate algebraically:

- normalization gives `c(+1)=+1`;
- refinement gives `c(k)=c(1)=+1` for every positive `k`;
- orientation reversal gives `c(-k)=-1`;
- null quarantine gives `c(0)=0`.

## Theorem 2: Determinant Functor Split

The result is compatible with the retained scalar observable principle.

The determinant line carries two different pieces of structure:

```text
|Det|      -> log|det| magnitude generator
Or(Det)   -> local real orientation character
```

The retained scalar observable principle uses:

```text
W[J] = log|det(D+J)| - log|det D|.
```

That is the positive additive magnitude side. It does not see the orientation
character. The signed source line uses the orientation side:

```text
Or(Det_APS D_Y) -> {+1,-1}.
```

The two are not competing mechanisms; they are two functors of the same
determinant-line object.

## Why Global Product Sign Fails

For disjoint components:

```text
Det(Y_1 disjoint Y_2) = Det(Y_1) tensor Det(Y_2).
```

The total orientation is the product. But local source variation must remain
local. If a `+` source is later accompanied by a remote `-` spectator, the
source coefficient of the original `+` packet cannot flip.

Therefore the global product orientation is rejected as a local source law.
The local source law is componentwise:

```text
J_g(x in Omega_a) = chi_eta(Y_a) M_a rho_a(x).
```

## Control Failures

| rule | status | failure |
|---|---|---|
| `chi_eta` | pass | unique normalized source character |
| unsigned source | reject | violates orientation reversal |
| raw eta | reject | violates unit norm and refinement invariance |
| eta parity | reject | violates orientation/refinement constraints |
| complex eta phase | reject | leaves the real scalar action surface |
| global determinant product | reject | violates local sewing |

## Theorem 3: Tensor Maximality At `A1`

On the symmetric `3+1` perturbation representation, the invariant subspace of
the spatial rotation generators is exactly two-dimensional:

```text
fixed(full symmetric 3+1) = A1 = span(lapse, spatial trace).
```

The complement has no nonzero invariant vector:

```text
fixed(E plus T1 complement) = 0.
```

So the determinant-orientation source line has a canonical tensor lift only to
the invariant `A1` lapse/trace channel. It cannot populate the complementary
tensor channels by itself. The later oriented tensor-source lift resolves the
larger tensor question only conditionally, by twisting an ordinary retained
tensor source bundle rather than deriving non-`A1` tensor components from this
scalar line.

This is an important maximality result:

```text
A1 lift: yes
full Einstein/Regge tensor lift: not from this source line alone
oriented tensor-source lift: conditional, if T_plus is retained
```

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_source_character_uniqueness_theorem.py
```

Result:

```text
[PASS] source-character axioms have a unique normalized solution
[PASS] candidate rule classification: chi_eta
[PASS] candidate rule classification: unsigned
[PASS] candidate rule classification: raw_eta
[PASS] candidate rule classification: parity_eta
[PASS] candidate rule classification: complex_phase
[PASS] determinant factorization splits magnitude additivity from local orientation source
[PASS] source character separates signed active charge from positive inertia
[PASS] 3+1 covariance allows exactly A1 invariant source lift and no complement vector
FINAL_TAG: ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL
```

The candidate-rule rows are classification checks: `chi_eta` is accepted and
the controls are correctly rejected.

## What This Achieves

This is the current strongest version of the lane:

- `chi_eta` is not a free coefficient inside the source-character grammar;
- the retained `log|det|` magnitude generator and the signed orientation line
  come from the same determinant-line structure;
- positive inertia remains the norm, not the oriented sign;
- locality rejects global product signs;
- refinement rejects raw eta;
- real-action discipline rejects complex phases;
- the tensor lift is pinned to `A1` and cannot be overclaimed.

## What Still Blocks Nature-Grade Closure

The result is strong but still conditional.

Remaining gaps:

1. **Original-axiom forcing.** The Cl(3)/`Z^3` axiom must still force compact
   active gravitational sources to be sections of `Or(Det_APS D_Y)`, rather
   than this being an admitted source-character grammar.
2. **Continuum determinant line.** The finite refinement theorem must be lifted
   to an inverse-limit or continuum determinant-line theorem.
3. **Tensor localization.** The `A1` maximality result says the scalar source
   line alone cannot close the full tensor sector. The current finite route is
   the oriented tensor-source lift `T_g = chi_eta T_plus`; the transport pass
   retains the ordinary tensor carrier on audited restricted classes, and the
   continuum graded pass closes chosen-continuum transport plus formal
   odd/even nonlinear Einstein localization.
4. **UV/core stability.** Same-sector attractive collapse remains an ordinary
   short-distance gravity issue.
5. **Family transport.** Actual retained graph-family source-line transport
   remains to be tested.

## Boundary Verdict

The new status is:

```text
ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL
```

This is the highest-value theory result currently achieved in the signed
response lane. It is the right candidate to defend as the nontrivial novel
element, while keeping the original-axiom and full tensor gaps explicit.

## Original-Stack Derivation Follow-Up

The finite original-stack derivation is recorded in
[`SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md`](SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md)
with runner
[`../scripts/signed_gravity_cl3z3_source_character_derivation.py`](../scripts/signed_gravity_cl3z3_source_character_derivation.py).

Result:

```text
FINAL_TAG: CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
```

That pass identifies the finite determinant-line host for the
source-character grammar in the accepted `Cl(3)`/`Z^3` stack: the finite
Grassmann Gaussian supplies the determinant line, `log|det|` supplies the
positive scalar magnitude, and the orientation side supplies the local real
character that the uniqueness theorem reduces to `chi_eta` once a local
orientation/source section is admitted.

The nature-grade blocker matrix is now recorded in
[`SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md`](SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md):

```text
FINAL_TAG: SIGNED_GRAVITY_NATURE_GRADE_HARD_BLOCKERS_REDUCED_CONDITIONALS_REMAIN
```

The finite source-character derivation survives, but unconditional closure
still remains conditional on continuum/family/dynamics/stability upgrades and
on deciding whether the formal graded local theorem must be promoted to global
nonlinear PDE existence/uniqueness.

## Hosted-Line Follow-Up

The host-versus-selector audit is recorded in
[`SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md`](SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md)
with runner
[`../scripts/signed_gravity_naturally_hosted_orientation_line.py`](../scripts/signed_gravity_naturally_hosted_orientation_line.py):

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

This does not weaken the uniqueness theorem inside its domain. It says the
domain is sharper than the raw retained boundary complex: once a local
orientation/source section is admitted, `chi_eta` is still the unique
normalized real source character. But the determinant-line host itself is a
`Z2` torsor and flat local system, not a canonical selected section, and it
does not force the `chi_eta rho Phi` source action without an additional
section/source theorem.
