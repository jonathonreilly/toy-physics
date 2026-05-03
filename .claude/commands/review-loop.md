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
5. Enforce audit-system compatibility without running the independent audit:
   no bare `retained` / `promoted` status lines, seed changed claims through
   `docs/audit/scripts/run_pipeline.sh`, and require
   `python3 docs/audit/scripts/audit_lint.py --strict` to pass.
6. Treat review as the canonical science gate: the independent audit should be
   mostly confirmatory. Block PASS when a changed claim has missing graph
   dependencies, author-prewritten audit verdicts, stale retained-status
   assumptions, or a runner that does not test the load-bearing bridge.
7. Re-review only files changed by the fix pass, plus interacting files that
   were already in the original changed-file set.
8. Before closing or rejecting a non-landable PR, run the skill's salvage pass:
   preserve any durable, runner-backed lemma in the same requested landing path
   with a canonical claim type, and explicitly reject only the pieces that
   cannot be salvaged without new science.
9. End with a concise report covering imports/support status, retained/bounded
   disposition, salvage disposition, audit-readiness, commits, checks, and
   remaining manual science.

## Non-Negotiables

- Every imported or measured value must be identified.
- Support-only results must not be promoted to retained claims.
- Source-note `Status:` lines may not contain bare `retained` or `promoted`;
  use `proposed_retained`, `proposed_promoted`, `support`, `bounded`, or
  `open`. The audit lane alone grants effective retained status.
- Authors and review packets must not prefill audit verdicts such as
  `target_audit_status: audited_clean`, `audit_status = audited_clean`, or
  `effective_status = retained`; say that audit status is set only by the
  independent audit lane and effective status is pipeline-derived.
- Load-bearing dependencies in changed claim notes must be markdown links that
  seed the citation graph. After the audit pipeline, changed claim rows must
  show the intended deps in `docs/audit/data/audit_ledger.json`.
- `retained`, `retained_bounded`, and `retained_no_go` are the retained-grade
  dependency statuses. Reviewers must reject stale exact-status checks that
  require only `effective_status = retained` when bounded/no-go retained
  grades are valid.
- `/review-loop` must not apply audit verdicts. It prepares audit-clean review
  surfaces and reports which proposed claims require the independent
  audit worker.
- `/review-loop` must not create or open pull requests. If science is
  salvageable, land the source-only salvage and dependency-chain/audit-queue
  repairs as part of the current landing path; otherwise close or reject the
  existing PR with a clear reason.
- Nature-grade retention requires derived or explicitly admitted inputs,
  decisive artifact support, clear falsifiers, and no hidden semantic bridge.
- Closing a PR must not discard durable science. Salvage narrow
  theorem/no-go/open-gate lemmas into canonical source-only landing commits
  when the runner directly supports the narrowed claim and no audit
  verdict/status language is carried over.
- Live unresolved review findings belong in `docs/repo/ACTIVE_REVIEW_QUEUE.md`.
- Long historical packets belong in `docs/work_history/repo/review_feedback/`.
