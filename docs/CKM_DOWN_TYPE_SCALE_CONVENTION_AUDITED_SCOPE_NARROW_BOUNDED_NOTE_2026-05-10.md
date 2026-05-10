# CKM Down-Type Scale-Convention Audited-Scope Narrowing Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_ckm_down_type_scale_convention_support.py`](../scripts/frontier_ckm_down_type_scale_convention_support.py)

## Why this note exists

The 2026-05-05 audit pass on the parent
[`CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md`](CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md)
returned `audited_numerical_match` with the explicit verdict:

> The runner mostly verifies arithmetic over imported constants and
> external PDG-style inputs, and it hard-codes the decisive full-loop
> transport factor as 1.14747 after noting its own one-loop computation
> gives a different value. The note is candid that the 5/6 bridge and
> the threshold-local scale choice are not theorem-grade closures. The
> load-bearing support is therefore a numerical match at a selected
> comparator scale, not a first-principles derivation or clean
> algebraic closure from retained inputs.

with re-audit guidance:

> missing_bridge_theorem: provide a retained derivation of the 5/6
> bridge and a retained argument selecting the threshold-local mass
> comparator, then rerun without hard-coding the contested transport
> factor.

This note narrows the parent's audited scope into the explicitly
algebraic and arithmetic content that the runner does close, separated
from the open-bridge dependencies that the parent itself flags.

This is a bounded scope-narrowing companion of an existing audited
note. It does not add a new axiom, does not add a new repo-wide theory
class, does not propose a status promotion, and does not modify the
parent note's audit ledger row.

## Audited verdict (verbatim, for clarity)

- `audit_status: audited_numerical_match`
- `audit_date: 2026-05-05`
- `chain_closes: false`
- `claim_scope` (audited): "Audited the support-level numerical
  scale-convention identity relating threshold-local and common-scale
  down-type mass-ratio comparisons, conditional on the imported
  alpha_s(v), 5/6 bridge, PDG mass inputs, and QCD transport factor."

The parent note's `Status` line and `Scope qualifiers` section already
record the same boundary in source form. This narrowing companion
isolates the **within-scope algebraic content** that the audit
verdict accepts as a numerical match.

## Narrow within-scope content (what the audited row does close)

Inside the audited support-level scope, the runner verifies the
following identities, each of which is independent of the open
bridge gaps and stands on imported authorities only:

| Identity | Class | Status |
|---|---|---|
| `C_F - T_F = 5/6` from SU(3) Casimir arithmetic | exact rational | audited PASS (sympy) |
| `|V_cb|_atlas = alpha_s(v) / sqrt(6)` | retained input arithmetic | audited PASS |
| 1-loop mass-anomalous-dimension exponent `gamma_m / (2 beta_0) = 12/25` for `n_f = 4` | exact rational from SU(3) Casimir bookkeeping | audited PASS |
| `R_thresh = R_common * transport_1loop` | exact QCD identity (1-loop transport) | audited PASS (10^-10) |
| `(R_pred / R_common) / (R_pred / R_thresh) = transport_1loop` | algebraic consequence of the previous identity | audited PASS (10^-10) |

These identities all close inside the audited scope. The numerical
match `R_pred / R_thresh - 1 = +0.20%` is also reproduced by the
runner; it is the **comparator-relative** numerical claim that the
audit verdict accepts as a class-G numerical match (not a first-
principles derivation).

## What the narrow scope does **not** close

The audit verdict and the parent's own scope qualifiers section
already flag these explicitly. This companion note records them in
one place for re-audit traceability:

- the theorem-grade derivation of the `5/6` bridge itself (the parent
  cites [`CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`](CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md)
  as bounded support);
- a retained theorem forcing the threshold-local comparator as the
  unique framework-natural mass-scale convention;
- elimination of the runner's hard-coded full-loop PDG transport
  factor `1.14747` in favour of a transport value computed from
  independent retained inputs;
- the down-type mass-ratio lane's bounded -> retained promotion;
- the canonical parent note
  [`QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md`](QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md)
  records the same scale-selection boundary as a separate bounded
  theorem.

## What would close the open dependencies (Path A future work)

Promoting the parent row from `audited_numerical_match` to a
retained theorem-grade derivation would require, per the audit
verdict's repair target:

1. a retained theorem deriving the `5/6` bridge `|V_cb| = (m_s/m_b)^{5/6}`
   from framework primitives at `g = 1` (non-perturbative
   exponentiation mechanism);
2. a retained theorem deriving the framework-natural mass-scale
   convention (threshold-local vs common-scale) from the framework
   action surface, **or** an RG-covariant transport theorem showing
   the bridge survives both conventions;
3. an updated runner that computes the transport factor from
   independent inputs (rather than hard-coding `1.14747`) and that
   constructs `R_common` independently of `R_thresh`.

Until at least one of (1) or (2) is supplied, the row remains a
bounded numerical-match support note at the audited scope.

## Dependencies

- [`CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md`](CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md)
  for the parent audited support note.
- [`CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`](CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md)
  for the open 5/6 bridge dependency.
- [`QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md`](QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md)
  for the canonical scale-selection boundary statement.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  for the retained `alpha_s(v)` anchor.
- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
  for the retained `|V_cb|_atlas = alpha_s(v) / sqrt(6)` anchor.

These are imported authorities for a bounded scope-narrowing companion
note. The row remains unaudited until the independent audit lane
reviews this companion, its dependencies, and the runner.

## Boundaries

This companion note does **not**:

- modify the parent note's audit-ledger row;
- promote the parent's `audit_status` from `audited_numerical_match`;
- re-derive the `5/6` bridge or the scale-selection theorem;
- eliminate the hard-coded transport factor in the parent runner;
- extend the audited scope beyond what the parent already declares.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_ckm_down_type_scale_convention_support.py
```

Expected (unchanged from parent):

```text
PASSED: 14/14
```

The runner is the same one cited by the parent note. This narrowing
companion does not introduce a new runner because the audited
within-scope algebraic content is already exercised. The new content
is the explicit scope-narrowing recording of which identities the
audit verdict accepts as a within-scope numerical match versus which
remain open as bridge dependencies.

```yaml
claim_id: ckm_down_type_scale_convention_audited_scope_narrow_bounded_note_2026-05-10
note_path: docs/CKM_DOWN_TYPE_SCALE_CONVENTION_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md
runner_path: scripts/frontier_ckm_down_type_scale_convention_support.py
proposed_claim_type: bounded_theorem
deps:
  - ckm_down_type_scale_convention_support_note_2026-04-22
  - ckm_five_sixths_bridge_support_note
  - quark_five_sixths_scale_selection_boundary_note_2026-04-28
  - alpha_s_derived_note
  - ckm_atlas_axiom_closure_note
audit_authority: independent audit lane only
```
