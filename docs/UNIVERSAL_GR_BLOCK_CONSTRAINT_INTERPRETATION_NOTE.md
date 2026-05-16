# Universal GR Block-Constraint Interpretation on `PL S^3 x R`

**Status:** support - block-constraint interpretation
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / constraint interpretation test  
**Ownership:** universal constraint interpretation only

**Status authority and audit hygiene (2026-05-16):**
The audit lane has classified this row `audited_conditional`
(auditor codex-cli-gpt-5.5, auditor_confidence high, load-bearing
step class `F`). The verdict accepts the algebraic block split as
exact (see sibling row `universal_gr_casimir_block_localization_note`,
ledger status retained), but flags that the load-bearing
**identification step** — "the canonical block-localization theorem
is strong enough to give a canonical Hamiltonian/momentum-constraint
interpretation at the block level, with the A1 core as Hamiltonian
and the j=1 block as momentum" — is a renaming/interpretation step
rather than a first-principles derivation from retained authorities.
The note itself explicitly leaves the operator-level Einstein/Regge
identification and the normalization/sign convention on the
`E \oplus T1` complement open. Audit verdict and effective status
are set by the independent audit lane only; nothing in the present
edit promotes status.

The audit-stated cheapest re-audit path (verbatim from the ledger
`notes_for_re_audit_if_any`):

> missing_bridge_theorem: provide a retained theorem deriving the
> block-to-GR-constraint-sector identification, including the
> normalization/sign convention on the `E \oplus T1` complement.

Section "Audit-conditional perimeter" below makes the renaming
boundary explicit. Section "Candidate upstream supplier chain
(graph-bookkeeping only)" records the source-theorem-notes that
already supply the algebraic block-split half of the bridge (block
localization + invariant A1 section + quotient-kernel uniqueness +
scalar generator + `3+1` lift), with explicit disclaimer that this
does not supply the operator-level GR bridge and does not promote
`audit_status`. The remaining named bridge — the operator-level
Einstein/Regge identification on the block-localized universal
Hessian — stays open and is the same operator-identification gap
already recorded as the live blocker on
`universal_gr_canonical_projector_connection_note` and
`universal_gr_block_ident_note`.

## Verdict

The canonical block-localization theorem is strong enough to give a
canonical Hamiltonian/momentum-constraint interpretation at the block
level.

The exact universal block structure is:

- lapse block;
- shift block;
- spatial trace block;
- traceless shear block.

In the canonical symmetric `3+1` basis, the invariant core is the exact
rank-2 `A1` projector

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

The remaining complement then splits canonically by the universal `SO(3)`
Casimir into:

- shift (`j=1`, rank 3);
- traceless shear (`j=2`, rank 5).

So the lapse and shift blocks now admit a canonical constraint interpretation
on the direct universal route:

- the Hamiltonian-constraint sector is the exact `A1` core
  (`lapse + spatial trace`);
- the momentum-constraint sector is the exact `j=1` shift block.

This is the strongest exact statement currently supported by the universal
route.

## What is exact already

The universal stack already gives:

1. the scalar observable generator `W[J] = log|det(D+J)| - log|det D|`;
2. the exact `PL S^3 x R` lift;
3. the exact tensor-valued variational candidate
   `S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`;
4. the exact symmetric `3+1` quotient-kernel uniqueness;
5. the exact invariant section `Pi_A1`;
6. the exact canonical block-localization into lapse, shift, trace, and
   traceless shear.

That means the universal route no longer lacks a canonical block split.

## Constraint interpretation

The direct universal route now supports the following block-constraint
reading:

- the `A1` core is the Hamiltonian block;
- the `j=1` complement block is the momentum block;
- the trace/shear split is canonical and orthogonal inside the remaining
  spatial sector.

So, if the question is only whether lapse/shift blocks admit a canonical
Hamiltonian/momentum-constraint interpretation, the answer is yes.

## Exact remaining gap

The canonical block split is not yet the same thing as a full Einstein/Regge
derivation.

The remaining gap is:

> the atlas still does not canonically identify the block-localized
> universal Hessian with the Einstein/Regge constraint operator, including
> the exact normalization/sign convention on the `E \oplus T1` complement.

Equivalently:

- block localization is exact;
- constraint-sector interpretation is exact;
- operator-level Einstein/Regge identification is still open.

## Honest status

The direct universal route is now:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- exact at the canonical block-localization level;
- still missing the final operator-identification theorem for full GR.

## Audit-conditional perimeter

The internal content of this note — listed in "What is exact already"
and "Constraint interpretation" above — splits cleanly into an
**algebraic block-split half** that is already supported by retained
support theorems on the direct universal route, and a **GR-canonical
labeling half** that is the F-class renaming the audit verdict flags.

What the audit verdict accepts as exact on the algebraic side (each
sub-statement lives in its own audit ledger row, see the supplier
chain below):

1. the scalar observable generator `W[J] = log|det(D+J)| - log|det D|`
   (axiom-side observable principle);
2. the exact kinematic `PL S^3 x R` lift (Route 2);
3. the exact tensor-valued variational candidate
   `S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)` as a construction;
4. the exact unique symmetric `3+1` quotient kernel on the finite
   prototype;
5. the exact invariant rank-2 `A1` projector
   `Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)` on the canonical polarization
   basis;
6. the exact canonical Casimir block split of the 8D complement into
   the `j=1` shift triplet (rank 3) and the `j=2` traceless-shear
   block (rank 5), with explicit complement Casimir
   `diag(C) = (-2,-2,-2,-6,-6,-6,-6,-6)` and projector ranks
   `1, 3, 1, 5` that are orthogonal, complete, idempotent, and
   commute with the spatial rotation generators.

What the audit-conditional perimeter (i.e. what stays open and is
the F-class renaming flag) is exactly:

- (R1) deriving from retained universal-GR authorities that the
  `A1` core `(lapse + spatial trace)` is the **Hamiltonian-constraint
  sector** of GR rather than just the rank-2 invariant block of the
  canonical universal Casimir split. The current note imports the
  label "Hamiltonian" from GR canon and asserts the identification;
- (R2) deriving from retained universal-GR authorities that the
  `j=1` shift triplet is the **momentum-constraint sector** of GR
  rather than just the rank-3 vector irrep of the spatial-rotation
  Casimir on the complement. The current note imports the label
  "momentum" from GR canon and asserts the identification;
- (R3) the operator-level identification of the block-localized
  universal Hessian with the Einstein/Regge constraint operator,
  including the exact normalization/sign convention on the
  `E \oplus T1` complement (already named open in this note's
  "Exact remaining gap" section).

Items (R1) and (R2) are the F-class load-bearing renaming step the
audit flags. Item (R3) is the operator-identification theorem the
note itself names as still missing.

Until (R1), (R2), or a single bridge theorem subsuming both is
supplied by retained upstream notes, the present row stays a
**block-localization labeling note on the canonical universal
Casimir split** rather than a constraint-sector identification
result. The "Honest status" section above already says this; the
present section makes the audit-conditional perimeter explicit for
the citation graph.

## Candidate upstream supplier chain (graph-bookkeeping only)

The audit-stated repair target is a `missing_bridge_theorem`
(class F, identification of two symbols): a retained upstream
theorem deriving the block-to-GR-constraint-sector identification,
including the normalization/sign convention on the `E \oplus T1`
complement.

Six candidate supplier notes already exist on disk in this branch.
Their respective load-bearing inferences target the algebraic
block-split half of the audit-named bridge — they do **not** supply
the GR-canonical labeling half. Listing them is graph-bookkeeping
only and does not promote `audit_status`.

The notes and what each supplies:

- `observable_principle_from_axiom_note` — supplies the exact scalar
  observable generator `W[J]`.
- `s3_anomaly_spacetime_lift_note` — supplies the exact `PL S^3 x R`
  kinematic background.
- `universal_gr_tensor_variational_candidate_note` — supplies the
  exact tensor-valued variational candidate
  `S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)` as a construction.
- `universal_gr_tensor_quotient_uniqueness_note` — supplies the
  unique symmetric `3+1` quotient kernel on the finite prototype.
- `universal_gr_a1_invariant_section_note` — supplies the exact
  rank-2 invariant `Pi_A1` projector onto lapse and spatial trace
  and its frame-invariance numerics.
- `universal_gr_casimir_block_localization_note` — supplies the
  exact canonical Casimir block split of the 8D complement into the
  `j=1` shift triplet and the `j=2` traceless-shear block, with the
  projector commutation, orthogonality, completeness, and
  idempotence checks.

The exact remaining bridge — operator-level Einstein/Regge
identification on the block-localized universal Hessian with a
canonical normalization/sign convention on `E \oplus T1` — is the
same operator-identification frontier already named open in
`universal_gr_canonical_projector_connection_note`,
`universal_gr_block_ident_note`, and
`universal_gr_complement_canonical_note`. No retained note on the
current direct-universal stack supplies that operator-level
identification, which is why this row stays
`audited_conditional` after the graph-bookkeeping repair.

## Boundaries

This note does **not** claim:

- a first-principles derivation of the labels "Hamiltonian
  constraint" or "momentum constraint" from A1 + A2 + retained
  authorities — the labels are imported from GR canon and applied
  to the canonical universal Casimir blocks;
- an operator-level identification of the block-localized universal
  Hessian with the Einstein/Regge constraint operator;
- a canonical normalization or sign convention on the
  `E \oplus T1` complement;
- a canonical section or distinguished connection on the `SO(3)`
  orbit bundle over the complement (already named negatively in
  `universal_gr_constraint_action_stationarity_note` and
  `universal_gr_canonical_projector_connection_note`);
- a closure of the live direct-universal blocker at the
  curvature-localization level
  (`universal_gr_curvature_localization_blocker_note`).

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links
named in the audit-conditional perimeter and the candidate supplier
chain above so the audit citation graph can track them. It does
not promote this note or change the audited claim scope.

- [observable_principle_from_axiom_note](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [s3_anomaly_spacetime_lift_note](S3_ANOMALY_SPACETIME_LIFT_NOTE.md)
- [universal_gr_tensor_variational_candidate_note](UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md)
- [universal_gr_tensor_quotient_uniqueness_note](UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md)
- [universal_gr_a1_invariant_section_note](UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md)
- [universal_gr_casimir_block_localization_note](UNIVERSAL_GR_CASIMIR_BLOCK_LOCALIZATION_NOTE.md)
- [universal_gr_canonical_projector_connection_note](UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md)
- [universal_gr_block_ident_note](UNIVERSAL_GR_BLOCK_IDENT_NOTE.md)
- [universal_gr_complement_canonical_note](UNIVERSAL_GR_COMPLEMENT_CANONICAL_NOTE.md)
- [universal_gr_constraint_action_stationarity_note](UNIVERSAL_GR_CONSTRAINT_ACTION_STATIONARITY_NOTE.md)
- [universal_gr_curvature_localization_blocker_note](UNIVERSAL_GR_CURVATURE_LOCALIZATION_BLOCKER_NOTE.md)
