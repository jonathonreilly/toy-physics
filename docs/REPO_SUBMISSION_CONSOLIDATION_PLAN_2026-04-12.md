# Repo Submission Consolidation Plan

**Date:** 2026-04-12  
**Goal:** reduce the repo from research-lab branch sprawl to a paper-submission surface that a reviewer can parse quickly

## Current Branch Surface

As of this snapshot, the repo has **105 refs** across local and remote branches.

Remote `origin/*` is dominated by exploratory namespaces:

- `frontier/*`: 35 branches
- `claude/*`: 32 branches
- `codex/*`: 21 branches
- `main`: 1 branch
- legacy/autopilot/sentinel refs: 5 branches

Local branches are also mostly workflow residue:

- `codex/*`: 10 branches
- `claude/*`: 2 branches

That is acceptable for active research. It is not acceptable for a paper-submission repo.

## Submission Policy

Yes: the repo should be submitted with the paper.

No: it should **not** be submitted in its current branch-heavy shape.

The submission repo should read like a release artifact, not a lab notebook.

## Target End State

Keep the public branch surface to:

- `main`
- optionally one temporary review branch during final cleanup

Everything else should move to an archive location:

- a separate archive remote/repo, or
- a git bundle stored outside the submission repo

The paper should then reference:

- one clean `main`
- one immutable release tag such as `paper1-submission-v1`

## What `main` Must Contain

`main` should hold only:

- retained note+runner pairs
- submission-facing documentation
- reproduction harnesses actually cited by the paper
- limitations and negatives that define the claim boundary

`main` should not hold:

- branch-specific synthesis notes
- Claude/Codex workflow debris
- contradictory frontier summaries
- abandoned exploratory runners with stronger claims than the retained notes
- `.claude/` or tool-worktree artifacts

## Required Submission Docs

Before submission, `main` should include:

- `README.md`
- `docs/PAPER1_SUBMISSION_MANIFEST.md`
- `docs/PAPER1_CLAIM_TO_ARTIFACT_MAP.md`
- `docs/PAPER1_REPRODUCTION_GUIDE.md`
- `docs/PAPER1_LIMITATIONS_AND_NEGATIVES.md`
- `docs/PAPER1_REVIEWER_FAQ.md`
- `docs/PAPER1_FIGURE_MAP.md`

Those files are the difference between a repository and a parsable research package.

## Branch Consolidation Sequence

### Phase 1: Freeze history

Before deleting any remote branches:

1. create an archive mirror or bare clone
2. push every current branch there
3. optionally create a `git bundle` backup of the full repo

Example:

```bash
git clone --mirror git@github.com:<org>/Physics.git Physics-archive.git
cd Physics-archive.git
git bundle create ../physics-full-history-2026-04-12.bundle --all
```

### Phase 2: Define the live surface

Keep live:

- `main`
- `codex/review-final-20260411` only until the final unresolved holds are decided

Archive or delete from the submission remote:

- all `frontier/*`
- all `claude/*`
- all stale `codex/*` integration branches
- legacy autopilot branches

### Phase 3: Move unresolved work behind one queue

Any non-retained artifact should live in exactly one place:

- `codex/review-final-20260411`

That branch should contain:

- unresolved holds
- promotion gates
- nothing already retained on `main`

### Phase 4: Tag the paper

Once `main` is clean:

1. tag the repo: `paper1-submission-v1`
2. freeze figure outputs and manifests
3. point the manuscript to that tag, not to a moving branch tip

## Immediate Reduction Rule

If the goal is a single parsable repo **now**, the branch policy should be:

- keep `main`
- keep `codex/review-final-20260411` temporarily
- archive everything else

Then, once the review queue is emptied:

- merge or close what survives
- archive `codex/review-final-20260411`
- leave only `main` plus release tags

## Why This Matters

A reviewer opening a repo with 90+ branches has no idea which branch represents the paper.

A reviewer opening a repo with:

- one `main`
- one manifest
- one reproduction guide
- one limitations file
- one release tag

can actually verify the work.

## Decision Rule

The repo is submission-ready when:

1. every paper claim maps to exactly one note+runner pair on `main`
2. every figure/table maps to one script and one expected output
3. `main` has no contradictory notes
4. the public branch surface is just `main` plus release tags
5. all unresolved work lives off `main` in a single explicit review queue or archive

## One-Sentence Policy

Use `main` for retained science, one review branch for unresolved work, and archive everything else so the submitted repo reads like a release, not a research process dump.
