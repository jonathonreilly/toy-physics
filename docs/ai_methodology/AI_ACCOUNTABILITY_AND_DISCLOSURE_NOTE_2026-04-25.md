# AI Accountability And Disclosure Note

---

**This is a methodology / disclosure / accountability-policy note.
It does not establish any retained scientific claim and does not
contain a first-principles physics derivation.**
For retained scientific claims, see the per-claim physics notes
referenced from the audit ledger; for the short manuscript framing
paragraph and broader process surface, see the cross-references at
the bottom of this file.

---

**Date:** 2026-04-25
**Status:** support / methodology disclosure record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / methodology disclosure record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no

This note is the longer repository-facing companion to the short framing
paragraph used in papers.

## Audit scope (operational narrowing 2026-05-10)

This file's load-bearing content is a **methodology / accountability-
policy disclosure**, not a first-principles physics derivation or an
algebraic closure over retained inputs. The audit ledger row for
`ai_methodology.ai_accountability_and_disclosure_note_2026-04-25`
carries verdict `audited_renaming`/meta with the auditor's reduced
result that:

> The load-bearing content is a disclosure/definition of process
> responsibility, not a first-principles computation or algebraic
> closure over retained inputs. There are no cited authorities or
> runner evidence, so the note cannot be audited as a positive
> theorem. The safe reduced result is only that this note records
> the repository's declared AI-use and human-responsibility policy.

The minimal-scope response in this PR is to **narrow** this document
operationally to its actual content — a methodology disclosure /
accountability-policy record — rather than to attach physics
authorities or runner evidence here. That would be a category error:
this note is not a physics claim. Until any future repositioning:

- This file makes **no** retained scientific-claim assertions.
- The disclosure of generative-AI use, the human-responsibility
  enumeration, the "Why This Matters" framing, the control-surface
  inventory, and the "Reading Rule" cross-references below are
  **methodology / accountability-policy content only**.
- This note records the repository's declared AI-use and
  human-responsibility policy. It does **not** assert that any
  physics result obtained with AI assistance is therefore correct
  or audit-clean; that surface is the per-claim audit ledger.
- The retained-status surface for any physics claim is the audit
  ledger (`docs/audit/AUDIT_LEDGER.md`) plus the per-claim physics
  notes, **not** this methodology disclosure.
- Retained-grade does **NOT** propagate from this methodology
  disclosure to any physics claim, AI-assisted derivation, or
  successor methodology revision.

For any retained scientific claim, audit the corresponding dedicated
physics note and its runner as a separate scoped claim — not this
methodology disclosure.

---

## Disclosure

This project has used generative-AI systems extensively, especially Claude and
OpenAI Codex.

These tools were used for:

- derivation drafting;
- candidate theorem construction;
- executable runner generation;
- no-go and obstruction search;
- branch review;
- claim-surface audit;
- selective landing and repo integration.

They were not treated as authors.

## Human Responsibility

The human author retained responsibility for:

- the foundational choice of framework surface;
- the selection of which scientific targets mattered;
- acceptance or rejection of proposed results;
- the final claim boundary on `main`;
- manuscript posture and interpretation.

AI systems were used as research and engineering instruments inside that
decision structure, not as the final authority on scientific truth.

## Why This Matters

The important point is not that AI was used. The important point is that a
sentence was not trusted just because an AI system wrote it. The repo was
organized so the claim could be checked against notes, runners, review, and
status labels.

That control surface includes:

- executable runner harnesses;
- explicit status labels (`retained`, `bounded`, `open`, `no-go`, `reject`);
- preserved no-go routes rather than positive-only storytelling;
- branch review and selective landing;
- explicit negative-boundary notes;
- active review and hygiene workflows.

The method is therefore plain: let the models generate and attack ideas, but
make the repo decide what is live.

## Reading Rule

- For the short manuscript paragraph, use
  `CANONICAL_FRAMING_PARAGRAPH_2026-04-25.md`.
- For the broader process description, use
  `../AI_METHODOLOGY_NOTE_2026-04-25.md` (sibling parent surface; backticked
  to avoid length-3 cycles through CANONICAL_FRAMING_PARAGRAPH and
  METHODOLOGY_PAPER_SOURCE_PACKET — citation graph direction is
  *ai_methodology_note → this_accountability* via the parent's downstream
  packet inventory).
