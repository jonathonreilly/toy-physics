# Signed Gravity Nature-Grade Closure Blocker Audit Note

**Date:** 2026-04-26
**Status:** hard tensor blocker reduced by oriented tensor-source lift;
nature-grade closure not yet achieved
**Script:** [`../scripts/signed_gravity_nature_grade_closure_blockers.py`](../scripts/signed_gravity_nature_grade_closure_blockers.py)

This note goes after the five remaining blockers after the finite
`Cl(3)`/`Z^3` determinant-source-character derivation:

1. continuum determinant-line lift;
2. actual retained graph-family APS realization;
3. full tensor/Einstein localization beyond `A1`;
4. sector dynamics and preparation;
5. UV/core stability.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Result

Command:

```bash
python3 scripts/signed_gravity_nature_grade_closure_blockers.py
```

Result:

```text
FINAL_TAG: SIGNED_GRAVITY_NATURE_GRADE_HARD_BLOCKERS_REDUCED_CONDITIONALS_REMAIN
```

All executable checks passed, but the closure status is not all-green:

| gate | status | read |
|---|---|---|
| continuum determinant-line lift | conditional | finite projective/refinement consistency passes |
| actual retained graph-family APS realization | conditional | constructed carriers pass; raw graph Hodge and retained-compatible staggered-Dirac boundaries are eta-neutral; determinant-line hosting is real but does not canonically select `chi_eta` |
| full tensor/Einstein localization beyond `A1` | conditional | scalar determinant character is `A1`-maximal; continuum transport, graded formal localization, and finite Galerkin small-data contraction pass; global PDE existence is not claimed |
| sector dynamics and preparation | conditional | fixed sectors are superselected; opposite-sector preparation is boundary-data/defect preparation unless a physical channel is derived |
| UV/core stability | conditional | fixed-N softened core is bounded; pair softening alone fails thermodynamic/Ruelle stability |

So the current lane is materially stronger than before, but not nature-grade
closed.

## Gate 1: Continuum Determinant-Line Lift

Finite result:

```text
eta=[1,2,4,8],
chi=[1,1,1,1],
max_logdet_refinement_err=8.9e-16.
```

Interpretation:

- orientation-preserving refinement multiplies raw `eta`;
- the source character remains `sign(eta)`;
- determinant-line logs are projectively additive on the finite refinement
  sanity check.

Status:

```text
CONDITIONAL
```

What remains:

> replace the finite projective/refinement sanity check with an inverse-limit
> determinant-line theorem on the retained continuum/refinement family.

## Gate 2: Retained Graph-Family APS Realization

Finite constructed-family result:

```text
cubic_shell: eta=+1, chi=+1
subdivided_cubic_shell: eta=+3, chi=+1
rectangular_shell: eta=+2, chi=+1
orientation_reversed_shell: eta=-2, chi=-1
irregular_shell: eta=+5, chi=+1
```

Interpretation:

- the determinant-orientation construction is portable across a small
  graph-family proxy set;
- subdivision changes eta magnitude but not the source character;
- orientation reversal flips the source character.

Status:

```text
CONDITIONAL
```

What remains:

The remaining-gates follow-up is recorded in
[`SIGNED_GRAVITY_REMAINING_CLOSURE_GATES_NOTE.md`](SIGNED_GRAVITY_REMAINING_CLOSURE_GATES_NOTE.md)
with runner
[`../scripts/signed_gravity_remaining_closure_gates.py`](../scripts/signed_gravity_remaining_closure_gates.py).

It finds:

```text
raw_hodge_eta_neutral=True
orientation_extension_has_eta=True
zero_modes_quarantine=True
actual_extraction_closed=False
```

Updated remaining work:

> derive the retained orientation-line APS boundary mode on actual graph
> families; raw Hodge boundaries are eta-neutral and cannot supply the sign by
> themselves.

The decisive containment follow-up is recorded in
`SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md` (downstream
follow-up artifact; cross-reference only — that note cites this
nature-grade audit as predecessor, not vice versa)
with runner
[`../scripts/signed_gravity_native_boundary_complex_containment.py`](../scripts/signed_gravity_native_boundary_complex_containment.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
```

So the answer to the native-containment question is currently negative:
the original raw cochain/Hodge boundary complex has parity-paired spectrum
and `eta=0`; the orientation-line APS source character was added as an
extension unless a future retained boundary theorem derives that line.

The staggered-Dirac boundary follow-up is recorded in
`SIGNED_GRAVITY_STAGGERED_DIRAC_APS_BOUNDARY_REALIZATION_NOTE.md`
(downstream follow-up artifact; cross-reference only — that note cites
this nature-grade audit as predecessor, not vice versa)
with runner
[`../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py`](../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
```

Retained-compatible staggered-Dirac boundary operators are also eta-neutral.
The only unpaired finite eta found is an odd-open-face sublattice imbalance
that flips under staggering-origin shift and vanishes under even refinement.
Pfaffian signs are determinant-line orientation metadata, not invariant branch
labels.

The hosted-versus-selected follow-up is recorded in
[`SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md`](SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md)
with runner
[`../scripts/signed_gravity_naturally_hosted_orientation_line.py`](../scripts/signed_gravity_naturally_hosted_orientation_line.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
```

This is the sharpest current selector status: the determinant-line functor
naturally hosts a real orientation line / `Z2` torsor and transports it as a
flat local system, but it does not choose the canonical signed section and does
not force the `chi_eta rho Phi` source term.

## Gate 3: Tensor Localization Beyond `A1`

Original scalar-only covariance result:

```text
invariant_dim_full = 2,
invariant_dim_E_plus_T1 = 0.
```

Interpretation:

- the determinant source character has a canonical invariant lift into the
  `A1` lapse/trace sector;
- the `E plus T1` complement has no nonzero canonical invariant vector under
  the same symmetry constraints;
- therefore the signed scalar source line cannot by itself become a full tensor
  source.

The decisive follow-up is recorded in
`SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_NOTE.md` (sibling artifact;
cross-reference only — not a one-hop dep of this note) with runner
[`../scripts/signed_gravity_oriented_tensor_source_lift.py`](../scripts/signed_gravity_oriented_tensor_source_lift.py).

It uses the derived orientation line as a local system twisting the ordinary
tensor source bundle:

```text
T_g(Y) = chi_eta(Y) T_plus.
```

That finite lift passes:

```text
FINAL_TAG: SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_FINITE_CONDITIONAL
```

Corrected interpretation:

- scalar-only determinant character remains `A1`-maximal;
- non-`A1` signed tensor response is possible only when an ordinary tensor
  stress carrier `T_plus` already has non-`A1` content;
- the orientation-line twist preserves canonical block projectors, linear
  constraints, and locked response signs.

Status:

```text
CONDITIONAL
```

What remains:

The transport/retention follow-up is recorded in
[`SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_NOTE.md`](SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_NOTE.md)
with runner
[`../scripts/signed_gravity_tensor_source_transport_retention.py`](../scripts/signed_gravity_tensor_source_transport_retention.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FINITE_CONDITIONAL
```

Finite readout:

```text
retained_carrier=True
projective_transport=True
nonlinear_even_jet_gate=True
```

Continuum/graded follow-up:

The continuum/graded nonlinear follow-up is recorded in
[`SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md`](SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md)
with runner
[`../scripts/signed_gravity_continuum_graded_einstein_localization.py`](../scripts/signed_gravity_continuum_graded_einstein_localization.py).

It returns:

```text
FINAL_TAG: SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM
```

Updated remaining work:

> upgrade the formal graded local theorem to global nonlinear PDE
> existence/uniqueness only if the lane needs global dynamics. The scalar-only
> source remains `A1`-maximal.

The remaining-gates follow-up adds:

```text
finite_galerkin_small_data=True
global_pde_claim=False
```

So the tensor side now has finite Galerkin small-data existence/uniqueness, but
not a global continuum PDE theorem.

## Gate 4: Sector Dynamics And Preparation

Finite result:

```text
chi_path=[1,1,1,1,1,0,-1,-1,-1,-1,-1].
```

Interpretation:

- gapped histories preserve `chi_eta`;
- a sign change crosses a null/zero-mode boundary defect;
- both `+` and `-` components are definable as disconnected initial-data
  sectors;
- fixed-sector dynamics have zero leakage in the block-superselected harness;
- this does not yet prove a physical preparation channel for both sectors.

Status:

```text
CONDITIONAL
```

What remains:

> treat opposite-sector preparation as boundary-data/defect preparation unless
> a physical preparation channel is derived.

## Gate 5: UV/Core Stability

Finite result:

```text
E_same_core_min = 1.000,
E_opp_core_min = 2.326,
E_same_no_core_min = -62.700,
logZ = 8.866.
```

Interpretation:

- finite core / lattice UV structure bounds the two-body softened energy;
- opposite-sign positive-inertial channel remains bounded in the finite check;
- removing the core reproduces the ordinary same-sector fall-to-center trend;
- the finite Gaussian partition is UV finite;
- pair softening alone does not provide thermodynamic/Ruelle stability for
  arbitrary same-sector particle number.

Status:

```text
CONDITIONAL
```

What remains:

> add a genuine global stability mechanism; pair softening alone bounds fixed
> `N` but fails thermodynamic stability.

## Current Closure Stack

The current signed-response lane now has:

```text
CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE
ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL
SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_FINITE_CONDITIONAL
SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FINITE_CONDITIONAL
SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM
SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS
SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED
SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED
SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED
SIGNED_GRAVITY_NATURE_GRADE_HARD_BLOCKERS_REDUCED_CONDITIONALS_REMAIN
```

This is a serious finite theorem stack, not a free-sign model. But the last
tag is deliberately not a nature-grade closure tag.

## Nature-Grade Remaining Work

The highest-value next moves are:

1. **Actual-family APS extraction.** Build APS boundary operators from the
   retained gravity graph/lattice families by deriving a retained
   orientation-line boundary mode or a canonical section/source theorem for
   the naturally hosted determinant orientation line; raw Hodge and
   retained-compatible staggered-Dirac boundaries are eta-neutral.
2. **Continuum determinant line.** Lift the finite determinant-orientation
   character to the canonical refinement/inverse-limit family.
3. **Tensor-source theorem.** Decide whether the formal graded local theorem
   must be promoted to a global nonlinear PDE existence/uniqueness theorem, or
   whether the signed lane only needs the local formal continuum theorem plus
   separate sector-preparation/stability gates.
4. **Sector preparation.** Prove how both boundary sectors can be prepared, or
   demote the `-` sector to a formal boundary component.
5. **Global stability.** Add a real global stability mechanism; softened
   pair cores are fixed-`N` bounded but fail thermodynamic stability alone.

## Boundary Verdict

The new status is:

```text
SIGNED_GRAVITY_NATURE_GRADE_HARD_BLOCKERS_REDUCED_CONDITIONALS_REMAIN
```

The signed-response lane has a finite determinant-source-character derivation,
and the hard tensor blocker has been reduced through retained-carrier
transport, chosen-continuum transport, and a graded formal nonlinear Einstein
localization theorem. It is still not unconditionally closed at nature-grade
review: continuum determinant-line transport for the APS source character,
actual-family APS realization, sector preparation, global nonlinear dynamics
if demanded, and global UV/core stability remain conditional. The remaining
gates are now precise: raw graph Hodge APS extraction is eta-neutral,
native boundary-complex and staggered-Dirac boundary containment are negative
for the orientation-line APS mode, determinant-line hosting is real but not a
canonical selector, opposite-sector preparation is boundary-data/defect
preparation, and pair softening alone is not a thermodynamic stability
theorem.
