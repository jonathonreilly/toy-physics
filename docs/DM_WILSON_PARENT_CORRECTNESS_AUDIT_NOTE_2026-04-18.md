# DM Wilson Parent Correctness Audit Note

**Date:** 2026-04-18
**Status:** exact repo audit of how far the current Wilson-parent story can be
trusted for the DM Wilson-to-`dW_e^H` route
**Script:** `scripts/frontier_dm_wilson_parent_correctness_audit_2026_04_18.py`

## Question

Can the current repo safely treat the Wilson parent as a fully validated,
fully specific parent for the DM route, so that deriving `I_e / P_e` is just
the next local theorem step?

## Bottom line

No.

What the current repo supports is weaker:

- there is an exact **gauge-side Wilson transfer parent** for the plaquette
  lane;
- there is an explicit **positive structured model class** realizing the
  desired `dW_e^H` responses;
- but there is still no theorem that the gauge-side parent is already the same
  object as the fermion-weighted retained parent used on the strong-CP side,
  no theorem-grade framework-point operator data fixing a unique parent
  descendant at `beta = 6`, and no Wilson-native map from that parent into
  `I_e / P_e` or `dW_e^H`.

So for the DM attack, the phrase "Wilson parent" should currently be read as:

- a partial gauge-side parent template and theorem-shape guide,

not as:

- a fully validated cross-sector parent already trustworthy enough to close the
  charged descendant problem by itself.

## Audit Finding 1: the current repo still carries two different parent-level formulas

From
[GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md):

- the plaquette lane parent is the gauge-side transfer object

  `Z_(L_s,L_t)(beta) = Tr[T_(L_s,beta)^(L_t)]`

  on the gauge-invariant spatial Hilbert space.

From [STRONG_CP_THETA_ZERO_NOTE.md](./STRONG_CP_THETA_ZERO_NOTE.md):

- the retained strong-CP partition is the fermion-weighted effective measure

  `Z = integral DU det(D[U] + m) e^(-S_Wilson[U])`.

Those are not the same formula.

The current repo does **not** yet contain an exact theorem saying:

- the fermion-weighted retained partition also factors through the same
  one-clock transfer object `T_(L_s,beta)`,
- or that the determinant-dressed effective action already yields one exact
  retained transfer operator canonically identified with the plaquette parent.

So the slogan "same Wilson parent object" is currently stronger than the
theorem bank if read across gauge and fermion sectors without qualification.

## Audit Finding 2: even the gauge-side framework-point operator data are still not fixed

From
[GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md):

- explicit transfer-state identification at `beta = 6` is still open.

From
[GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md):

- the exact factorized class

  `T_src(6) = exp(3 J) D_6 exp(3 J)`

  is known structurally,
- but the linked runner is only a generic positive-diagonal witness and is not
  an explicit Wilson `D_6` evaluation.

From
[GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md):

- even after the exact local marked-link factor is fixed, distinct admissible
  residual source-sector environment operators can still produce different
  Perron moments and different Jacobi data.

So the current repo does not yet fix a unique framework-point gauge-side
parent descendant even before PMNS/DM data are asked for.

## Audit Finding 3: the positive DM realization now on branch is model-level, not Wilson-native

From
[DM_WILSON_TO_DWEH_STRUCTURED_MODEL_REALIZATION_THEOREM_NOTE_2026-04-18.md](./DM_WILSON_TO_DWEH_STRUCTURED_MODEL_REALIZATION_THEOREM_NOTE_2026-04-18.md):

- the structured Wilson response class is explicitly realizable for arbitrary
  target `H_e`,
- but the note states explicitly that it does **not** derive that realization
  from the current-bank Wilson parent.

So the positive branch result is real, but it closes only:

- nonempty constructive realization of the structured response class.

It does **not** yet close:

- Wilson-native realization of that class from the retained stack.

This is exactly the distinction we need for the audit:

- positive existence has been shown,
- Wilson provenance has not.

## Audit Finding 4: the missing load-bearing map is still the cross-sector Wilson-to-charged descendant

From [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- the exact observable engine is the scalar source generator

  `W[J] = log |det(D+J)| - log |det D|`,

  with first variations once microscopic `D` and source path `J` are supplied.

From [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md):

- the exact support intertwiner has a safe role only as support transport on
  the taste-cube / BZ-corner side.

From
[DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_CURRENT_BANK_BOUNDARY_NOTE_2026-04-18.md](./DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_CURRENT_BANK_BOUNDARY_NOTE_2026-04-18.md):

- current `main` still has no theorem-grade Wilson-to-`dW_e^H` descendant law,
- and no Wilson Hermitian source family realizing that codomain.

So the current load-bearing absence is still exactly:

- one theorem-grade Wilson-to-charged Hermitian descendant map.

That means the Wilson parent is not failing because it is false. It is failing
because the repo still has no exact theorem carrying it into the charged DM
codomain.

## Theorem 1: safe current-stack interpretation of the Wilson parent for the DM route

Assume:

1. the exact gauge-side transfer-operator realization on the plaquette lane;
2. the exact strong-CP retained partition formula;
3. the exact source-sector factorization and Perron/Jacobi underdetermination
   results;
4. the exact structured model realization note for the DM branch;
5. the exact current-bank boundary note excluding an existing
   Wilson-to-`dW_e^H` descendant theorem.

Then the strongest safe current-stack statement is:

- the repo has an exact **partial gauge-side Wilson parent template** with
  real operator-first value for theorem shape and positivity grammar,

but it does **not** yet have:

- a fully validated cross-sector Wilson parent already specific enough to be
  treated as the DM charged parent,
- a unique framework-point operator realization fixing the needed descendant
  data,
- or a theorem-grade Wilson-native derivation of `I_e / P_e / dW_e^H`.

Therefore any DM attack that assumes full Wilson-parent correctness beyond that
boundary is currently stronger than the exact theorem bank.

## Corollary 1: what is safe to use from the Wilson parent right now

It is safe to use the Wilson parent as:

- an operator-first template,
- a compression/intertwiner grammar guide,
- a source of gauge-side positivity and Perron structure,
- a reason to search for matrix-valued descendants rather than more scalar
  repackaging.

## Corollary 2: what is not safe to assume right now

It is not yet safe to assume:

- that the gauge transfer parent and the fermion-weighted retained parent are
  already theorem-grade identical,
- that a witness completion or hand-built structured realization is already a
  derived Wilson-native object,
- that the current parent data are explicit enough at `beta = 6` to force a
  unique charged descendant,
- or that `I_e / P_e` should already be extractable from the present parent
  stack without one new theorem.

## Positive consequence: the next honest positive fork

This audit does **not** kill the Wilson route. It sharpens it.

There are now two honest positive continuations:

1. **Effective-parent route.**
   Derive an exact retained parent operator for the determinant-dressed
   effective action

   `S_eff[U] = S_Wilson[U] - log det(D[U] + m)`,

   or an equivalent one-clock retained transfer law. That would remove the
   parent-identity mismatch directly.

2. **Direct-descendant route.**
   Bypass the global parent-identification issue and derive a Wilson Hermitian
   source family / `Psi` directly from the observable principle and the
   microscopic charged block, without assuming the stronger parent story
   upfront.

Those are the two routes that remain positive **and** audit-clean.

## What this closes

- one exact audit of why the current Wilson parent should not be treated as
  `100%` correct for the DM route yet
- one exact distinction between a partial gauge-side parent template and a
  fully validated DM charged parent
- one sharper positive fork for what the next theorem should actually try to
  prove

## What this does not close

- a retained effective-action transfer theorem
- a positive Wilson-native derivation of `I_e / P_e`
- a positive Wilson-to-`dW_e^H` descendant theorem
- the right-sensitive DM selector law
- the DM flagship lane
