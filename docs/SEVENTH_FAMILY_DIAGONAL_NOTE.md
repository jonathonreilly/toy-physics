# Seventh Family Diagonal Note

---

**This is a finite-sweep observation / boundary-cluster freeze note.
It does not establish any retained claim.**
For retained claims on seventh-family / diagonal-stripe content, see
the per-claim notes referenced from the `## Audit scope` block below.

---

**Status:** support / finite-sweep observation record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / finite-sweep observation record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no

This note freezes the seventh-family diagonal-stripe scout as a seed-selective
boundary on the no-restore grown slice.

## Audit scope (relabel 2026-05-10)

This file is a **finite-sweep observation / boundary-cluster freeze
note** for the seventh-family diagonal-stripe scout. It is **not** a
single retained theorem and **must not** be audited as one. The
audit ledger row for `seventh_family_diagonal_note` classified this
source as conditional/bounded_theorem with auditor's repair target:

> add enforced pass/fail checks plus routing/control comparators,
> or state the claim purely as a reproduced finite sweep table.

The minimal-scope response in this PR is to **relabel** this document
as a finite-sweep observation record rather than to add enforced
pass/fail checks or routing/control comparators here. Those steps
belong in dedicated review-loop or per-row audit passes. Until that
work is done:

- This file makes **no** retained-claim assertions of its own.
- The `7/18` passing-rows tally, per-drift/seed list, "selector is
  diagonal-stripe routing, not a control leak" framing, and
  seed-selective boundary narrative below are **historical
  finite-sweep observation memory only**.
- The note explicitly excludes any broad seventh-family theorem
  closure or family-wide claim.
- The retained-status surface for any seventh-family, diagonal-
  stripe-routing, or no-restore-grown-slice sub-claim is the audit
  ledger (`docs/audit/AUDIT_LEDGER.md`) plus the per-claim notes,
  **not** this finite-sweep observation record.
- Retained-grade does **NOT** propagate from this finite-sweep note
  to any sub-row, routing-vs-control verdict, or successor sweep.

For any retained claim about seventh-family diagonal-stripe content,
audit the corresponding dedicated note and its runner as a separate
scoped claim — not this finite-sweep observation record.

---

Runner: [`scripts/SEVENTH_FAMILY_DIAGONAL_SWEEP.py`](../scripts/SEVENTH_FAMILY_DIAGONAL_SWEEP.py)

Construction:
- non-shell diagonal stripes in the `y/z` plane
- layer-parity flips the stripe axis between `y+z` and `y-z`
- nearest-destination selection stays structured with a small fallback floor

Sweep result:
- exact zero-source baseline: `+0.000e+00` on all tested rows
- exact neutral cancellation: `+0.000e+00` on all tested rows
- sign orientation and weak-field response stay selective
- passing rows: `7/18`
- passing drifts / seeds: `0.0 / 0,1,2`; `0.2 / 2`; `0.3 / 1,2`; `0.5 / 1`
  (count corrected from a previous stale `6/18` line; the explicit per-row
  list was already correct and totals seven)

The narrow claim is:
- this is a seed-selective boundary pocket, not family-wide closure
- the selector is the diagonal-stripe routing, not a control leak
- do not promote this as a broad seventh-family theorem

This does not broaden the earlier retained families. It only says the
diagonal-stripe non-shell architecture can reproduce the signed-source package
on a narrow subset of rows.
