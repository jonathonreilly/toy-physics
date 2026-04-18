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
