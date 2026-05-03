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
6. Enforce the axiom and vocabulary governance gates: do not add, remove,
   rename, split, merge, or promote axioms / primitive assumptions unless the
   user explicitly approved that axiom-set change in the current task or a
   landed governance document already authorizes it. Do not introduce new
   theory names, claim classes, status labels, lane labels, or authority
   wording when existing repo vocabulary covers the case.
7. Treat review as the canonical science gate: the independent audit should be
   mostly confirmatory. Block PASS when a changed claim has missing graph
   dependencies, author-prewritten audit verdicts, stale retained-status
   assumptions, unapproved axiom-set changes, noncanonical vocabulary, or a
   runner that does not test the load-bearing bridge.
8. Re-review only files changed by the fix pass, plus interacting files that
   were already in the original changed-file set.
9. Before closing or rejecting a non-landable PR, run the skill's salvage pass:
   preserve any durable, runner-backed lemma as a source-only salvage PR with a
   canonical claim type, and explicitly reject only the pieces that cannot be
   salvaged without new science.
10. End with a concise report covering imports/support status, retained/bounded
   disposition, salvage disposition, audit-readiness, commits, checks, and
   remaining manual science.

## Non-Negotiables

- Every imported or measured value must be identified.
- No new axiom, primitive, postulate, foundational assumption, or minimal-input
  item may be added or elevated without explicit user approval for that exact
  change. A PR that changes the axiom set without that approval is not
  landable under `/review-loop`.
- No new theory name, status label, claim class, lane label, authority surface,
  or review category may be invented when existing repo conventions apply.
  Use `docs/repo/CONTROLLED_VOCABULARY.md`, `docs/audit/README.md`, and the
  current `claim_type` set; if new vocabulary is genuinely needed, require
  explicit user approval or queue it as governance work instead of landing it.
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
- Nature-grade retention requires derived or explicitly admitted inputs,
  decisive artifact support, clear falsifiers, and no hidden semantic bridge.
- Closing a PR must not discard durable science. Salvage narrow
  theorem/no-go/open-gate lemmas into canonical source-only follow-up PRs when
  the runner directly supports the narrowed claim and no audit verdict/status
  language is carried over.
- Live unresolved review findings belong in `docs/repo/ACTIVE_REVIEW_QUEUE.md`.
- Long historical packets belong in `docs/work_history/repo/review_feedback/`.
