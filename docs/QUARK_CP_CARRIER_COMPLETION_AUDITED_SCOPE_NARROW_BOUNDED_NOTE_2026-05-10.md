# Quark CP-Carrier Completion Audited-Scope Narrowing Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_quark_cp_carrier_completion.py`](../scripts/frontier_quark_cp_carrier_completion.py)

## Why this note exists

The 2026-05-05 audit pass on the parent
[`QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md`](QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md)
returned `audited_numerical_match` with the explicit verdict:

> The load-bearing step is an optimized numerical completion using
> explicit solved carrier coefficients and imported comparator targets.
> The runner is not a trivial printout: it builds Hermitian mass
> matrices, diagonalizes them, computes CKM observables, and checks
> the determinant phase. However, the parameters xi_u and xi_d are
> tuned degrees of freedom rather than derived from the stated axiom,
> and the success criteria are external observation/atlas matches, so
> this is class G rather than first-principles class C.

with re-audit guidance:

> A second auditor should re-check the upstream imported constants and
> solve_magnitude_surface implementation if the audit scope is
> expanded beyond this restricted packet.

This note narrows the parent's audited scope into the explicit
existence-of-fit content that the runner does close, separated from
the absence of a retained derivation of the carrier coefficients.

This is a bounded scope-narrowing companion of an existing audited
note. It does not add a new axiom, does not add a new repo-wide theory
class, does not propose a status promotion, and does not modify the
parent note's audit ledger row.

## Audited verdict (verbatim, for clarity)

- `audit_status: audited_numerical_match`
- `audit_date: 2026-05-05`
- `chain_closes: true`
- `claim_scope` (audited): "Audited the bounded numerical existence
  claim that sector-specific complex 1-3 carriers can fit m_u/m_c,
  m_c/m_t, |V_us|, |V_cb|, |V_ub|, and J while keeping
  arg det(M_u M_d) numerically zero."

The parent note's `Safe statement`, `What closes`, and `What does not
close` sections already record the same boundary in source form.
This narrowing companion isolates the **within-scope existence
content** that the audit verdict accepts as a numerical match.

## Narrow within-scope content (what the audited row does close)

Inside the audited bounded-existence scope, the runner verifies the
following structural facts. Each is independent of any claim that the
solved carriers `xi_u`, `xi_d` are derived from framework primitives:

| Audited content | Status |
|---|---|
| The minimal Schur-NNI carrier closes the quark magnitudes while failing the CKM CP area on its own (no-go on minimal carrier) | audited PASS (parent runner) |
| Phase-only relaxation on the minimal Schur-NNI carrier does not repair J | audited PASS |
| Adding one determinant-neutral complex 1-3 carrier `xi_u`, `xi_d` per sector admits a numerical fit of `(m_u/m_c, m_c/m_t, \|V_us\|, \|V_cb\|, \|V_ub\|, J)` to ~1% or better at the comparator surface | audited PASS (G-class numerical match) |
| `arg det(M_u M_d) = 0 mod 2pi` is maintained numerically by the fit (1e-16) | audited PASS |
| The completed surface lifts `J` by more than a factor of 6 over the Schur-only anchor | audited PASS |
| The fitted carriers `xi_u`, `xi_d` are non-perturbatively large relative to the Schur 1-3 base term: `|xi_u|/c13_u^{base} ~ 102`, `|xi_d|/c13_d^{base} ~ 6.6` | audited PASS (recorded as caveat, not closure) |

The within-scope conclusion is an existence statement: the CKM atlas
and quark mass-ratio target surface admit a determinant-neutral
extended-carrier solution. This is a non-trivial computational
existence result, but it is **not** a derivation of the carriers from
framework primitives.

## What the narrow scope does **not** close

The audit verdict and the parent's own scope-qualifier sections
already flag these explicitly. This companion note records them in
one place for re-audit traceability:

- a retained derivation of `xi_u`, `xi_d` from framework primitives
  (the parent flags these as numerical bounded carrier coefficients);
- a perturbatively small correction interpretation: the fitted
  carriers dominate the Schur 1-3 base term, especially in the up
  sector, so this is not a small retained correction;
- a minimal-surface theorem upgrade: the Schur-NNI no-go on the
  minimal carrier remains intact;
- promotion of the row from `bounded` to `retained`.

A complementary stronger reduced-closure attempt is recorded in
[`QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md`](QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md);
that note continues to live as a separate bounded surface and is
**not** load-bearing for this narrowing companion.

## What would close the open dependency (Path A future work)

Promoting the parent row from `audited_numerical_match` to a retained
theorem-grade derivation would require, per the audit verdict's
repair target:

1. an independent retained theorem fixing `xi_u` and `xi_d` from
   framework primitives, including their carrier normalization,
   readout convention, and determinant-neutral constraint;
2. an updated runner that **tests** the derived carrier point
   (rejecting if it deviates from the derived value) rather than
   **fitting** to the comparator surface;
3. an explicit retained statement of why the determinant-neutral
   1-3 carrier is the minimal admissible CP-carrier slot beyond the
   Schur-NNI base.

Until at least (1) is supplied, the row remains a bounded numerical
existence-of-fit support note at the audited scope.

## Dependencies

- [`QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md`](QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md)
  for the parent audited support note.
- [`QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md`](QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md)
  for the complementary reduced-closure attempt (not load-bearing
  here).

These are imported authorities for a bounded scope-narrowing companion
note. The row remains unaudited until the independent audit lane
reviews this companion, its dependencies, and the runner.

## Boundaries

This companion note does **not**:

- modify the parent note's audit-ledger row;
- promote the parent's `audit_status` from `audited_numerical_match`;
- derive `xi_u` or `xi_d` from framework primitives;
- claim a small-correction interpretation of the fit;
- change the Schur-NNI minimal-surface CP no-go;
- extend the audited scope beyond what the parent already declares.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_cp_carrier_completion.py
```

Expected (unchanged from parent):

```text
TOTAL: PASS=11, FAIL=0
```

The runner is the same one cited by the parent note. This narrowing
companion does not introduce a new runner because the audited within-
scope existence content is already exercised. The new content is the
explicit scope-narrowing recording of what the audit verdict accepts
as a within-scope numerical existence match versus what remains open
as a derivation gap.

```yaml
claim_id: quark_cp_carrier_completion_audited_scope_narrow_bounded_note_2026-05-10
note_path: docs/QUARK_CP_CARRIER_COMPLETION_AUDITED_SCOPE_NARROW_BOUNDED_NOTE_2026-05-10.md
runner_path: scripts/frontier_quark_cp_carrier_completion.py
proposed_claim_type: bounded_theorem
deps:
  - quark_cp_carrier_completion_note_2026-04-18
audit_authority: independent audit lane only
```
