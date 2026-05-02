# Open Questions for the Reviewer

**Date:** 2026-05-02

These are decisions the proposal asks the reviewer to weigh in on
explicitly. Each has a default the proposal author would land on, but is
explicitly flagged so the reviewer doesn't have to read between lines.

## Q1 — Is `retained_bounded` worth a separate effective_status value?

**Alternatives:**

- (A, proposed) Add `retained_bounded` as a distinct value; downstream
  publication-table renderers can choose to render it next to `retained` or
  separately.
- (B) Collapse it into `retained` and represent the bound only via the
  `claim_scope` text field.

**Default:** (A). Rationale: a bounded theorem is *honestly retained for the
narrow scope*, but downstream consumers should know they're inheriting a
bounded statement. Renderers can group `retained` and `retained_bounded`
together if they want.

**Reviewer please confirm or flip.**

## Q2 — Should `open_gate` block downstream `proposed_retained` propagation?

**Alternatives:**

- (A, proposed) Yes, fully. Any chain that depends on an `open_gate` row is
  capped at `proposed_retained`, identical to depending on `unaudited`.
- (B) Allow downstream notes to be `audited_clean + claim_type=open_gate`
  if the downstream note explicitly cites the open_gate as a known
  conditional.

**Default:** (A). Rationale: open_gate means the upstream is *actively
incomplete*. Allowing chained propagation through an incomplete gate
defeats the purpose of having an open_gate type in the first place.

**Reviewer: any concrete case where (B) would be necessary?**

## Q3 — Multi-parent decorations — split or pick dominant?

**Alternatives:**

- (A, proposed) If the decoration's load-bearing step depends on multiple
  parents (rare but exists), the auditor returns `audited_conditional`
  instead, asking the author to clarify which parent is load-bearing.
- (B) Allow `decoration_parent_claim_id` to be a list; renderer chooses
  display.

**Default:** (A). Rationale: decoration is supposed to be a clean single-
parent reduction. Multi-parent decorations are usually a sign that the note
is actually doing more than one thing and should be split.

**Reviewer: are there real multi-parent decoration notes in the current
ledger that would suffer under (A)?**

## Q4 — `Type:` author hint as required vs optional

**Alternatives:**

- (A, proposed) Optional. Authors may include or omit. Auditor classifies
  regardless. Mismatch between hint and audit is logged for tracking but
  not blocked.
- (B) Required for new notes (warning at note-creation time if missing).
  Auditor still authoritative.

**Default:** (A). Rationale: making it optional minimizes friction during
migration and respects the principle that the auditor classifies. Hints
help the auditor get to the right answer faster but don't gate.

**Reviewer: would (B) significantly improve audit speed or accuracy?**

## Q5 — Backfill bias for critical rows

The migration backfills `claim_type` for ~1572 rows from a deterministic
inference rule. For 91 critical rows, the proposal flags them
`backfill_pending_critical` and queues for explicit re-audit instead of
silent backfill.

**Alternatives:**

- (A, proposed) Backfill all non-critical; queue critical for re-audit.
- (B) Backfill all rows uniformly; rely on cross-confirmation at next
  re-audit cycle to catch wrong classifications.
- (C) Re-audit all rows from scratch; no backfill anywhere.

**Default:** (A). Rationale: balances cost (no mass re-audit) against
risk (critical rows are highest-leverage and most likely to have
classification ambiguity).

**Reviewer: is (C) worth the cost? Is (B) too risky?**

## Q6 — Source-note `Status:` line: strip or auto-banner?

After phase 5 of the migration, source notes no longer need `Status:`
lines. But notes are still human-readable artifacts.

**Alternatives:**

- (A) Strip `Status:` lines entirely. Readers go to `AUDIT_LEDGER.md` for
  status.
- (B, proposed) Strip `Status:` lines, then auto-render an
  `<!-- AUDIT_BANNER_START -->` block at the top of each note from the
  current ledger row. Pipeline regenerates the banner on each run.
- (C) Replace `Status:` line with a single token (`audit-pending`,
  `retained`, `open_gate`, …) that the pipeline maintains.

**Default:** (B). Rationale: maintains note readability without re-
introducing author-side tier assignment. The banner is clearly machine-
generated and not author-authoritative.

**Reviewer: which option is least disruptive to current reading workflow?**

## Q7 — `proposed_retained` as a transient state — is the term confusing?

Under the new model, `proposed_retained` is *no longer author-set*. It is
a computed transient state meaning "audit is clean, dep chain isn't yet."
The word `proposed` may suggest authorial intent that no longer exists.

**Alternatives:**

- (A) Keep the name `proposed_retained` for continuity with old
  documentation.
- (B, proposed) Rename to `retained_pending_chain` or
  `awaiting_chain_clearance` to reflect the actual semantics.
- (C) Eliminate the value entirely; show such rows as `unaudited` until
  chain clears, with an `effective_status_blocked_by` field.

**Default:** (B). Rationale: name should describe what the state means.
`proposed_retained` is a misnomer once nothing is being proposed by an
author. (C) is too aggressive — losing the distinction between
"audit-pending entirely" and "audit-clean but chain-pending" is real
information.

**Reviewer: vote on naming.**

## Q8 — Author dispute path remains the same?

The current dispute path is: author disagrees with audit verdict →
third-auditor escalation. Under the new model, audit verdicts include
`claim_type`, so disputes can target the type assignment as well.

**Question:** Should `claim_type` disputes follow the exact same
escalation path as `verdict` disputes, or do they get a lighter-weight
process (e.g., author proposes a re-classification, single fresh auditor
confirms or denies)?

**Default:** Same path. Rationale: consistency. Differential paths add
complexity. If dispute volume is high, can be revisited as a follow-on.

**Reviewer: any concern about overload?**

## Summary of defaults

| Q | Default | One-line reason |
|---|---|---|
| Q1 | (A) Add `retained_bounded` as distinct value | bounded ≠ unconditional |
| Q2 | (A) `open_gate` blocks downstream propagation | gates exist to gate |
| Q3 | (A) Multi-parent → audited_conditional | clean reductions are single-parent |
| Q4 | (A) `Type:` hint optional | auditor classifies anyway |
| Q5 | (A) Backfill non-critical, re-audit critical | cost/risk balance |
| Q6 | (B) Auto-render banner | preserve readability |
| Q7 | (B) Rename `proposed_retained` → `retained_pending_chain` | name should match semantics |
| Q8 | Same dispute path | consistency |
