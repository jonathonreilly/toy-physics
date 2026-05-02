# Scope-Aware Classification Proposal — Reviewer Guide

**Date:** 2026-05-02
**Author:** Claude Opus 4.7 (1M context), via session led by jon@bridgerapps.com
**Branch:** `audit-lane/scope-aware-classification-proposal-20260502`
**Status:** proposal — not implemented; awaiting independent review.

This directory is a **proposal package**. It does not modify any live policy
doc, schema, or note in this PR. Each policy / skill doc that *would* change
is captured as a delta document. A reviewer can read the package end to end
without merging anything.

## Reading order

| # | Doc | Purpose | Length |
|---|---|---|---|
| 0 | [`00_PROPOSAL.md`](00_PROPOSAL.md) | What we are proposing and why | medium |
| 1 | [`01_SCHEMA_CHANGES.md`](01_SCHEMA_CHANGES.md) | Field-by-field before/after on the audit ledger | short |
| 2 | [`02_PROPAGATION_RULES.md`](02_PROPAGATION_RULES.md) | New `effective_status` computation rules | short |
| 3 | [`03_AUDITOR_PROTOCOL_CHANGES.md`](03_AUDITOR_PROTOCOL_CHANGES.md) | What changes for the audit agent (Codex) | short |
| 4 | [`04_POLICY_DOC_DELTAS.md`](04_POLICY_DOC_DELTAS.md) | Specific edits to `docs/audit/*` and `docs/repo/CONTROLLED_VOCABULARY.md` | medium |
| 5 | [`05_SKILL_DOC_DELTAS.md`](05_SKILL_DOC_DELTAS.md) | Specific edits to `physics-loop/SKILL.md` and `review-loop/SKILL.md` | short |
| 6 | [`06_MIGRATION_PLAN.md`](06_MIGRATION_PLAN.md) | Phased rollout with rollback per phase | medium |
| 7 | [`07_EXAMPLES.md`](07_EXAMPLES.md) | How recent campaign work maps under the new model | short |
| 8 | [`08_OPEN_QUESTIONS.md`](08_OPEN_QUESTIONS.md) | Items the reviewer should weigh in on | short |
| ★ | [`PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md`](PROPOSED_AUDIT_AGENT_PROMPT_TEMPLATE.md) | Full drop-in replacement for the audit prompt (anchor file) | medium |

## One-paragraph summary

The audit lane currently asks the *author* to declare the claim's tier
(`support`, `proposed_retained`, `bounded`, `open`, …) and the *auditor* to
verify the chain. The author tier was a defense-in-depth layer against four
CKM-style failure modes that the auditor's own verdict vocabulary
(`audited_renaming`, `audited_conditional`, `audited_decoration`,
`audited_failed`, `audited_numerical_match`) already catches independently.
Removing the author tier and letting the auditor classify both the *grade*
(does the chain close?) and the *scope* (positive theorem? bounded? no-go?
open gate? decoration?) gives a cleaner separation: the audit lane outputs a
high-bar retained library, papers are independent objects that consume the
library when they're written. Bounded and open work survive as first-class
auditor-set classifications, not as author-side hedges.

## What is *not* in this PR

- No source notes are modified (~1601 `Status:` lines stay as is until the
  migration plan is approved).
- No pipeline scripts are modified.
- No schema is migrated.
- The audit agent prompt template (`docs/audit/AUDIT_AGENT_PROMPT_TEMPLATE.md`)
  is left in place; the proposed replacement lives only in this proposal
  directory.

The migration plan in [`06_MIGRATION_PLAN.md`](06_MIGRATION_PLAN.md) describes
how each step would land in a follow-on PR after this design is approved.

## Reviewer asks

A careful reviewer should answer:

1. Are there CKM-style failure modes that the proposed audit verdict
   vocabulary fails to catch but that author tiers currently catch?
2. Is the proposed `claim_type` enum (positive_theorem, bounded_theorem,
   no_go, open_gate, decoration, meta) complete? Anything missing?
3. Does the migration plan have an honest rollback at each phase?
4. Are the proposed deltas to `physics-loop` and `review-loop` SKILLs
   internally consistent with the new model?
5. The eight open questions in [`08_OPEN_QUESTIONS.md`](08_OPEN_QUESTIONS.md).
