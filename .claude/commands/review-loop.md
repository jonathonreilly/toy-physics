# /review-loop — Physics Review Loop

Run the repo-native physics review loop from:

`docs/ai_methodology/skills/review-loop/SKILL.md`

## Invocation

`/review-loop [focus] [--max-iterations N] [--no-fix] [--no-commit]`

## Required Behavior

1. Read the skill file above before acting.
2. Review only branch/local changes against `origin/main` or `main`.
3. Fan out the physics reviewers in parallel when the agent environment allows:
   `CodeRunnerReviewer`, `PhysicsClaimReviewer`, `ImportSupportReviewer`,
   `NatureRetentionReviewer`, `RepoGovernanceReviewer`, and optionally
   `MethodologySkillReviewer`.
4. Fix only verified, narrow findings. Demote overclaims instead of patching
   missing science with prose.
5. Re-review only files changed by the fix pass, plus interacting files that
   were already in the original changed-file set.
6. End with a concise report covering imports/support status, retained/bounded
   disposition, commits, checks, and remaining manual science.

## Non-Negotiables

- Every imported or measured value must be identified.
- Support-only results must not be promoted to retained claims.
- Nature-grade retention requires derived or explicitly admitted inputs,
  decisive artifact support, clear falsifiers, and no hidden semantic bridge.
- Live unresolved review findings belong in `docs/repo/ACTIVE_REVIEW_QUEUE.md`.
- Long historical packets belong in `docs/work_history/repo/review_feedback/`.
