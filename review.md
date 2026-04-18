# Review: `claude/yt-retention-landing-2026-04-18`

## Current Call

This branch is **clean as a reviewer handoff packet** and **not clean as a
`main` landing branch**.

That distinction matters.

- **Yes** as a science-only review branch carrying the YT UV-to-IR retention
  suite for reviewer inspection.
- **No** as a branch that should be merged directly into `main` right now.

The reason is not a package-weaving problem. On the contrary, the branch is
disciplined:

- it is only **1 commit ahead / 0 behind** `origin/main`;
- it touches **no live publication/control-plane surfaces**;
- the diff is science-only: notes, runners, logs, and reviewer-facing
  navigation/readiness artifacts;
- the aggregate readiness and manifest runners replay cleanly.

So as a reviewer packet, the branch is in good shape.

## What I Checked

- `git diff --name-status origin/main...origin/claude/yt-retention-landing-2026-04-18`
  shows a science-only branch with no publication-surface rewiring.
- `python3 scripts/frontier_yt_retention_manifest.py` ends with
  `Manifest-validator PASSED: 118`, `FAILED: 0`.
- `python3 scripts/frontier_yt_retention_landing_readiness.py` ends with
  `landing readiness runner complete`.
- The top-level notes are aligned that this branch is reviewer-facing and does
  **not** modify publication-surface files.

## Why This Is Not A `main` Landing Yet

The branch does **not** fail on hygiene. It fails on scope:

- it is a **large science bundle** (`121` files, `~59k` inserted lines),
  not a selective package promotion;
- the new notes repeatedly self-classify the new YT suite as retained and
  reviewer-ready, but that is exactly what a reviewer still has to assess;
- none of this science has yet been woven into the canonical publication
  surfaces, which is appropriate for review but means this is not yet a
  package-state merge.

So the right status is:

- **review-ready science packet**
- **not yet merge-ready package science**

## Practical Recommendation

Use this branch exactly as it is currently shaped:

1. hand it to the reviewer as the YT retention submission branch;
2. keep `main` unchanged until the reviewer accepts or narrows the claim set;
3. after review, do a separate selective landing branch that weaves only the
   accepted science into the repo surfaces in the standard way.

That is the clean process for this submission.

## Bottom Line

This branch is in the **right quarantine state**:

- good reviewer handoff
- good branch hygiene
- no live-surface contamination
- not a `main` merge candidate yet
