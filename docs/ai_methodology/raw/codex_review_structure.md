# Codex Review Structure

**Capture date:** 2026-04-25

This file collects raw evidence for the Codex-side review loop, review packet
placement, and retainability discipline.

---

## 1. Canonical repo review workflow document

**Source file:**

```text
/Users/jonreilly/Projects/Physics/docs/repo/REVIEW_FEEDBACK_WORKFLOW.md
```

**Raw content:**

```text
# Review Feedback Workflow

**Purpose:** define the canonical process for landing, reviewing, triaging, and
closing repo feedback on `main`

## Canonical Files

- active queue:
  [`ACTIVE_REVIEW_QUEUE.md`](./ACTIVE_REVIEW_QUEUE.md)
- historical detailed packets:
  [`docs/work_history/repo/review_feedback/README.md`](../work_history/repo/review_feedback/README.md)
- historical planning backlogs:
  [`docs/work_history/repo/backlog/README.md`](../work_history/repo/backlog/README.md)

## Default Process

1. Land the candidate work on `main` if it is already honest enough to keep.
2. Have the reviewer check the landed surface or the clean science-only review
   branch.
3. Record any actionable finding in
   [`ACTIVE_REVIEW_QUEUE.md`](./ACTIVE_REVIEW_QUEUE.md).
4. If the review needs more than a short bullet list, add a detailed packet in
   [`docs/work_history/repo/review_feedback/`](../work_history/repo/review_feedback/README.md)
   and link it from the queue.
5. Triage each item into one of five buckets:
   - `fix on main`
   - `support-only demotion`
   - `science-needed`
   - `reject`
   - `historical only`
6. Resolve the item on `main` if it is wording, packaging, code, or honest
   demotion work.
7. Remove the item from the active queue once the repo-facing state is correct.

## Decision Rule

Use the narrowest honest fix:

- if the issue is wording, packaging, stale status language, or a reproducible
  code bug, fix it on `main`
- if the issue is a real missing theorem step or unjustified selector, do not
  fake closure; either demote the claim or keep the science off-main until the
  derivation exists
- if the issue concerns a historical lane that is no longer part of the live
  evidence chain, classify it as `historical only` rather than treating it as a
  live blocker

## Placement Rule

- do **not** put new review packets in the front-door `docs/` root unless they
  are themselves part of the live science package
- do **not** create new free-floating backlog files for current review work
- do **not** use branch-local notes as the long-term review source of truth

## What Belongs Where

- `docs/repo/ACTIVE_REVIEW_QUEUE.md`
  current actionable review state
- `docs/work_history/repo/review_feedback/`
  older audit notes, detailed review packets, and resolved review histories
- `docs/work_history/repo/backlog/`
  planning/backlog notes that are not current review truth surfaces
```

## 2. Related retainability / audit files

```text
/Users/jonreilly/Projects/Physics/docs/CLAUDE_BRANCH_RETAINABILITY_NOTE.md
LINES 213
/Users/jonreilly/Projects/Physics/docs/UNPROMOTED_BRANCH_RETAINABILITY_AUDIT_NOTE.md
LINES 103
```

Representative opening from `CLAUDE_BRANCH_RETAINABILITY_NOTE.md`:

```text
# Claude Branch Retainability Note

**Date:** 2026-04-05
**Scope:** branch-audit of `claude/distracted-napier` from a mainline-retainability perspective

This note is intentionally conservative. It does **not** merge branch claims
into `main`. It only asks which Claude-branch results look carryable onto
`main`, which ones are still interesting but branch-side, and which ones
currently fail our own bars.
```

This is direct evidence that the repo already had an explicit retainability
discipline before the later Codex review loop accelerated it.

## 3. `review.md` packet inventory found in active Codex temp/worktree space

Count found during this pass:

```text
3
```

Paths:

```text
/private/tmp/ai-method-review/review.md
/private/tmp/lorentz-boost-covariance-review/review.md
/private/tmp/three-sector-review/review.md
```

## 4. Current methodology-branch review note

**Source file:**

```text
/private/tmp/ai-method-review/review.md
```

**Opening excerpt:**

```text
# Review: `claude/ai-methodology-capture-2026-04-25`

## Verdict

Useful raw archive, but **not approved verbatim** for `main`.

The branch contains valuable source material for a methodology paper, but the
submitted surface is still a branch-local capture packet rather than a clean
public methodology lane.

I took a **selective landing** instead.
```

This is direct evidence of the Codex-side pattern:

- review raw branch honestly;
- land a narrower curated subset if appropriate;
- keep the review packet on the source branch.

## 5. Review-structure signals visible in current Codex branch inventory

Representative `origin/codex/*` review-oriented names observed on this pass:

```text
origin/codex/ckm-full-package-review
origin/codex/dm-science-reviewed-2026-04-17
origin/codex/leptogenesis-science-review-2026-04-16
origin/codex/p-derived-science-review
origin/codex/pf-science-review-2026-04-18
origin/codex/plaquette-env-review
origin/codex/review-active
```

These names are included here as raw evidence of branch naming conventions for
review, not yet as a cleaned taxonomy.
