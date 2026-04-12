# Branch Scrub Protocol

**Date:** 2026-04-12  
**Purpose:** consolidate every non-`main` branch into one active review branch,
then archive or delete the source branch once its science is either retained,
held, or discarded explicitly

## Policy

This repo should have exactly two live working surfaces during consolidation:

- `main`: retained science only
- `codex/review-active`: active integration branch for uncaptured results

Everything else is a source branch to be scrubbed.

## Scrub Rule

For each non-`main` branch:

1. inspect the unique notes, scripts, and commits not already captured on
   `main` or `codex/review-active`
2. move any real uncaptured science into `codex/review-active`
3. write the result into one of three buckets:
   - bounded promotion candidate
   - explicit hold with blocker
   - discard / duplicate / superseded
4. only after that, archive or delete the source branch

No branch should be deleted before its unique payload is classified.

## Namespace Pass Order

Run the scrub in this order:

1. `codex/*`
   - highest chance of containing integration work that never made it to review
2. `claude/*`
   - highest chance of overnight science or branch-local notes that were never
     consolidated
3. `frontier/*`
   - mostly exploratory, but still needs a uniqueness pass before archive
4. legacy one-off refs
   - autopilot or historical utility refs can usually archive directly after
     confirming no unique docs/scripts

## Current Branch Surface

Remote `origin/*` counts at this checkpoint:

- `frontier/*`: 35
- `claude/*`: 32
- `codex/*`: 21
- `main`: 1
- legacy one-offs: 5

## Capture Standard

A branch is considered captured only when:

- its unique science artifacts are present on `codex/review-active`, or
- a review note on `codex/review-active` states that the branch was duplicate,
  superseded, or non-retainable

If neither is true, the branch is not yet safe to archive.

## Archive Standard

After capture, the source branch should move to one of:

- archive remote/repo
- git bundle
- deletion from the paper-facing remote after archive confirmation

The public submission surface should not carry historical branch clutter once
the contents are consolidated.

## Promotion Standard

Nothing moves from `codex/review-active` to `main` until it has:

- a bounded note
- a paired runner
- an explicit claim boundary
- no contradiction with existing retained notes

## End State

The consolidation is finished when:

1. every non-`main` branch has been scrubbed
2. every uncaptured result is either on `codex/review-active` or explicitly
   discarded
3. `main` contains only retained science
4. all other branches are archived or deleted

At that point the public repo should collapse to:

- `main`
- release tags

and no active review branch should remain.
