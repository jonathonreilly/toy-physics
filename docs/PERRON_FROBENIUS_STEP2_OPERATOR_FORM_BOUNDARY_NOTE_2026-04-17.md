# Perron-Frobenius Step-2 Operator-Form Boundary

**Date:** 2026-04-17  
**Status:** exact science-only proof-form boundary for future positive step-2A theorems  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_operator_form_boundary_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

Given the current PF lane, what mathematical **form** should a future positive
step-2A theorem have if it is going to survive hard review?

## Bottom line

It should be an operator-level descendant/intertwiner law, not a scalar
transplant.

The current branch already proves:

- the target codomain is charged-sector operator/Hermitian data
  `D_- / dW_e^H / H_e`;
- scalar-only and support-only candidate classes are already excluded;
- outside theory is admissible only as hypothesis template, not imported
  closure.

Therefore the only honest future theorem form is an operator statement of the
type:

- compression/intertwiner into `D_-`, or
- compression/intertwiner into `dW_e^H`,

for example in schematic form

- `I_e^* T_Wilson I_e -> D_-`,
- `P_e T_Wilson P_e -> dW_e^H`,

or an equivalent operator-descendant law with the same charged-sector content.

## Why this is now forced

### 1. The codomain is already operator/Hermitian

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md):

- the first honest step-2A target is

  `Wilson -> D_- -> dW_e^H -> H_e`.

So step 2A is not asking for another scalar observable. It is asking for an
operator descendant law into charged Hermitian data.

### 2. Scalar and support-only candidates are already excluded

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md):

- additive scalar-observable candidates are excluded;
- support-only intertwiner candidates are excluded;
- the admissible candidate shape is a genuinely new matrix-valued cross-sector
  descendant/intertwiner law.

### 3. External theory already fixes the right proof template

From
[PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md](./PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md)
and
[PERRON_FROBENIUS_EXTERNAL_THEORY_PROOF_STANDARD_NOTE_2026-04-17.md](./PERRON_FROBENIUS_EXTERNAL_THEORY_PROOF_STANDARD_NOTE_2026-04-17.md):

- Stinespring is the right **step-2 template**;
- but it is a template only, not imported proof.

So the admissible future theorem form is:

- operator-level descendant / compression / intertwiner.

Not admissible:

- scalar rhetoric about positivity,
- hand-waving analogy to positive maps,
- support transport alone,
- imported outside conclusions with unmatched hypotheses.

## Theorem 1: exact proof-form boundary for future positive step 2A

Assume the exact step-2A codomain reduction theorem, the exact step-2A
candidate-shape boundary theorem, and the exact PF external-theory proof
standard. Then any future positive step-2A theorem that would honestly connect
the Wilson parent object to the PMNS Hermitian codomain must be written as an
operator-level descendant/intertwiner law into charged-sector data, rather than
as a scalar-observable or support-only statement.

Therefore the right theorem search form is already fixed:

- compression/intertwiner into `D_-`,
- compression/intertwiner into `dW_e^H`,
- or an equivalent operator descendant carrying the same charged-sector
  Hermitian content.

## Corollary 1: Stinespring is useful only at the level of form

The branch may safely say:

- Stinespring indicates the right kind of theorem shape.

It may **not** safely say:

- Stinespring proves the Wilson-to-`dW_e^H` bridge already exists.

So the hard-review-safe usage is now explicit.

## Corollary 2: candidate search should be operator-first from here on

The branch should therefore spend effort on:

- explicit charged-sector compressions,
- explicit Schur-descendant constructions,
- explicit operator intertwiners.

Not on:

- more scalar observable repackaging,
- more support transport repackaging,
- more abstract PF rhetoric detached from operator realization.

## What this closes

- one exact proof-form boundary for future positive step-2A work;
- one exact clarification of how the outside Stinespring template may be used;
- one exact operator-first instruction for the next science move.

## What this does not close

- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a nonzero PMNS bridge amplitude;
- a positive global PF selector.

## Why this matters

This note makes the lane more review-proof.

It says not just what theorem is missing and what shape the bridge must have,
but also what form any future proof must take to count as real closure on this
branch.

## Atlas inputs used

- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md](./PERRON_FROBENIUS_ALL_PATHS_ATTACK_PROGRAM_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_EXTERNAL_THEORY_PROOF_STANDARD_NOTE_2026-04-17.md](./PERRON_FROBENIUS_EXTERNAL_THEORY_PROOF_STANDARD_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_operator_form_boundary_2026_04_17.py
```
