---
name: review-loop
description: Use when an LLM agent needs to run `/review-loop`, review branch changes, run parallel physics-specific reviewers, identify overclaims/imported values/support-only material, apply narrow honest fixes, verify audit-system compatibility without applying audit verdicts, and re-review only files changed by those fixes.
---

# Review Loop

Run a local review/fix/re-review loop for this physics repo. This is not a
generic software review. Its job is to protect the live claim boundary:
retained/Nature-grade claims must have artifact support, imported values must
be explicit, and support-only results must not be promoted by prose.
It also protects the repo's authority language: reviewers must reject
unapproved axiom-set changes and noncanonical theory/status/claim vocabulary
instead of normalizing those changes during review.

This skill is **review only**. It may make branch/package hygiene changes that
allow the independent audit system to parse and queue claims, but it must not
apply audit verdicts, write `audited_clean`, or run the audit worker.

The bar is intentionally high: if review-loop is doing its job, the later
fresh-context audit should be mostly confirmatory. Do not pass branches that
leave the audit lane to discover basic claim-boundary, dependency-graph,
status-vocabulary, or runner-validity defects. Do not lose durable science
when a PR fails that bar: before closing or rejecting a branch, run the
salvage pass below and preserve any narrow, runner-backed lemma that can be
made canonical without changing the science.

## Arguments

Parse:

- focus text: optional free-text review focus;
- `--max-iterations N`: optional cap, default `5`;
- `--no-fix`: review only, do not edit;
- `--no-commit`: fix locally but do not create iteration commits.

## Setup

1. Read the local review/governance surfaces before judging status:
   - `docs/repo/REVIEW_FEEDBACK_WORKFLOW.md`
   - `docs/repo/ACTIVE_REVIEW_QUEUE.md`
   - `docs/repo/CONTROLLED_VOCABULARY.md`
   - `docs/CANONICAL_HARNESS_INDEX.md`
   - `docs/audit/README.md`
   - current `docs/MINIMAL_AXIOMS_*.md` surfaces when a branch touches
     axioms, foundations, primitive assumptions, minimal inputs, or framework
     authority wording
   - `docs/publication/ci3_z3/` when publication-facing files changed
   - `docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md` when
     quantitative or imported-value claims changed
2. Determine the base ref:
   - prefer `origin/main` if present;
   - otherwise use `main`;
   - if the current branch is the base branch, use `HEAD~1`.
3. Compute the review base with `git merge-base HEAD <base-ref>`.
4. Build the original changed-file set from committed, staged, unstaged, and
   untracked changes. Do not review outside this set except interacting files
   that are also in this original set.
5. Record whether the worktree was initially clean. If it was dirty, do not
   auto-commit without explicit user permission unless the slash-command
   invocation clearly requested commit-producing fixes.
6. If the task is to review open/non-landed PRs, include all non-merged PRs in
   the requested scope except PRs the user explicitly excluded. Closed-but-
   unmerged PR heads can be inspected with `gh pr view` and
   `git fetch origin pull/<N>/head:refs/tmp/pr-<N>`.

## Axiom And Vocabulary Gate

This gate applies before any reviewer can mark a branch PASS.

1. A branch must not add, remove, rename, split, merge, elevate, demote, or
   reinterpret axioms, primitive assumptions, postulates, minimal inputs, or
   foundational framework items unless the user explicitly approved that exact
   axiom-set change in the current task, or a landed governance document
   already authorizes the change.
2. If a branch touches axiom/foundation language, reviewers must identify the
   approved authority for the change. If no authority exists, classify it as
   `AXIOM_GOVERNANCE` and block landing. Do not repair an unapproved axiom
   change by inventing a softer label unless the user approved the new
   framing.
3. Review-loop fixes must not introduce new theory names, status labels, claim
   classes, lane labels, authority surfaces, review categories, or informal
   synonyms when existing repo language covers the case. Use
   `docs/repo/CONTROLLED_VOCABULARY.md`, `docs/audit/README.md`, and the
   canonical audit `claim_type` set:
   `positive_theorem`, `bounded_theorem`, `no_go`, `open_gate`,
   `decoration`, `meta`.
4. If new vocabulary is genuinely needed, do not land it as an incidental
   review-loop fix. Require explicit user approval or record a
   `REPO_GOVERNANCE` item in `docs/repo/ACTIVE_REVIEW_QUEUE.md`.
5. PRs that introduce phrases like "new theory", "new axiom",
   "additional primitive", "framework postulate", "retained by construction",
   or new claim/status labels require explicit approval and repo-vocabulary
   placement before review-loop may land them.

Useful commands:

```bash
git diff --name-only <base>...HEAD
git diff --name-only --cached
git diff --name-only
git ls-files --others --exclude-standard
git diff <base>...HEAD -- <files>
git diff --cached -- <files>
git diff -- <files>
```

For untracked files, include their full content or a concise new-file summary
in reviewer prompts.

## Reviewer Fanout

On each iteration, set `files_to_review` to the files that changed since their
last clean review. On iteration 1, use all original changed files.

Run all applicable reviewers in parallel through the available agent/subagent
mechanism. If parallel agents are unavailable, run the same reviewer passes
locally and report that limitation.

### Required Reviewers

- `CodeRunnerReviewer`
  Review changed Python/scripts/log-producing code. Check syntax, decisive
  assertions, hard-coded targets, stale fixtures, literal `True` checks,
  hidden observations, reproducibility, paired runner/output agreement, and
  whether the runner actually tests the note's load-bearing bridge. If a
  runner checks audit-ledger dependency status, it must use the current
  retained-grade set (`retained`, `retained_bounded`, `retained_no_go`) rather
  than hard-coding stale expectations such as exactly `retained`.

- `PhysicsClaimReviewer`
  Attack theorem notes, claims tables, publication surfaces, and prose. Check
  semantic bridges, selector assumptions, status labels, exact/bounded/support
  boundaries, axiom/foundation wording, and code/prose drift. Block PASS when
  a branch changes the axiom set or minimal-input story without explicit user
  approval.

- `ImportSupportReviewer`
  Inventory every measured, fitted, literature, PDG, cosmological,
  normalization, boundary-condition, or convention input. Classify each as
  `zero-input structural`, `framework-derived`, `one computed lattice input`,
  `admitted normalization/boundary condition`, `standard/literature
  correction`, `observational comparator`, `support-only`, `insensitive
  nuisance`, or `unjustified import`. For a Nature-grade retention claim, every
  import must be derived, admitted with a narrow role, quantitatively
  insensitive, or the claim must be demoted.

- `NatureRetentionReviewer`
  Apply the hostile external-review bar. Ask whether the result can honestly
  be called retained/Nature-grade: no hidden unit identification, no structural
  redefinition, no imported selector, no unsupported first-principles claim,
  no unmatched observed target, and clear falsifiers/open gates. Output
  `RETAINED`, `RETAINED SUPPORT`, `BOUNDED`, `OPEN`, `NO-GO`, or `REJECT`.

- `RepoGovernanceReviewer`
  Check placement and authority surfaces. Ensure live findings route through
  `docs/repo/ACTIVE_REVIEW_QUEUE.md`, long packets go under
  `docs/work_history/repo/review_feedback/`, publication edits update the
  relevant `docs/publication/ci3_z3/` surfaces, status wording follows
  `docs/repo/CONTROLLED_VOCABULARY.md`, and changed claim notes are compatible
  with the audit lane's propose/ratify split. Also verify that load-bearing
  dependencies are real markdown links that seed the citation graph, not just
  code-formatted file names in prose. Check that no new theory/status/claim
  vocabulary or authority surface is introduced without explicit approval and
  a canonical repo placement.

### Optional Reviewer

Run `MethodologySkillReviewer` when files under `docs/ai_methodology/skills/`,
`docs/ai_methodology/`, or `.claude/commands/` changed. Check that the skill is
concise, triggerable from its frontmatter/command name, aligned with the AI
methodology lane, and not claiming physics authority.

## Reviewer Prompt

Use this prompt shape for each reviewer, filtered to only that reviewer's file
scope:

````text
Review the following physics-repo changes.

Files to review:
<files>

Diff/content:
```diff
<diff for only those files; include untracked file content separately>
```

Focus:
<focus text or "None specified">

Context:
- Base ref: <base-ref>
- Iteration: <N> of <max>
- Already reviewed and unchanged: <reviewed_files>
- Repo review surfaces: REVIEW_FEEDBACK_WORKFLOW, ACTIVE_REVIEW_QUEUE,
  CONTROLLED_VOCABULARY, CANONICAL_HARNESS_INDEX, docs/audit/README.md

Rules:
- Findings must cite file/line when possible.
- Separate bugs, overclaims, support-only demotions, imported-value problems,
  repo-governance problems, and nits.
- Do not require new science for wording problems.
- Do not approve retained/Nature-grade language if an import or bridge remains
  hidden.
- Do not apply audit verdicts. Review only whether the branch is ready for the
  independent audit worker.
- Do not approve unapproved axiom-set changes or invented repo vocabulary.
  Use existing controlled vocabulary and audit claim types unless the user
  explicitly approved the new term/change.
````

## Consolidate Findings

Present one iteration summary:

```text
## Review Results (Iteration N)

### Code / Runner: PASS | RISK | FAIL
### Physics Claim Boundary: RETAINED | SUPPORT | BOUNDED | OPEN | REJECT
### Imports / Support: CLEAN | DISCLOSED | DEMOTE | FAIL
### Nature Retention: RETAINED | RETAINED SUPPORT | BOUNDED | OPEN | NO-GO | REJECT
### Repo Governance: PASS | FIX | QUEUE | ARCHIVE
### Audit Compatibility: PASS | FIX | BLOCKED | NOT APPLICABLE
### Methodology Skill: PASS | FIX | SKIPPED
```

Classify every finding:

- `BUG`
- `OVERCLAIM`
- `IMPORTED_VALUE`
- `SUPPORT_ONLY_DEMOTION`
- `MISSING_ARTIFACT`
- `SEMANTIC_BRIDGE`
- `AXIOM_GOVERNANCE`
- `VOCABULARY_GOVERNANCE`
- `REPO_GOVERNANCE`
- `AUDIT_COMPATIBILITY`
- `NIT`
- `SALVAGE_CANDIDATE`
- `SALVAGE_REJECT`

Stop immediately when all applicable reviewers are clean.

## Salvage Pass

Run this pass before closing a PR, marking it non-landable, or discarding a
stretch/campaign packet. The goal is to preserve meaningful science without
lowering the review bar.

1. Inventory the branch into these buckets:
   - canonical source candidates: theorem/no-go/open-gate notes and paired
     runners;
   - useful negative results: failed routes that name a durable obstruction and
     have a runner or exact calculation;
   - support-only calculations: exact algebra or bookkeeping that may be useful
     as bounded support but not as retained/Nature-grade science;
   - non-source material: claim-status certificates, handoffs, campaign state,
     generated audit files, expected audit verdicts, and branch-local logs.
2. For each source candidate, decide whether it can be salvaged with only
   review-level edits:
   - the claim can be narrowed to a canonical `claim_type`:
     `positive_theorem`, `bounded_theorem`, `no_go`, `open_gate`,
     `decoration`, or `meta`;
   - all imported physics, textbook machinery, observations, fitted values,
     and conventions are explicitly labelled;
   - the runner tests the actual load-bearing bridge, not just downstream
     arithmetic after the premise is assumed;
   - load-bearing dependencies can be represented as markdown links and
     non-load-bearing siblings can be kept out of the citation graph;
   - the salvage does not rely on a closed, unlanded, unaudited, or rejected
     sibling PR unless the dependency is copied in as a self-contained
     derivation and reviewed in the same salvage branch;
   - the salvage does not add or reframe axioms, primitive assumptions, theory
     names, claim classes, status labels, or authority surfaces without
     explicit user approval.
3. Do not salvage by papering over missing science. If the durable part is
   only an obstruction or failed route, salvage it as a narrow `open_gate` or
   `no_go` only when the runner directly supports that negative boundary.
4. Strip all non-source material from salvage branches:
   claim-status certificates, handoffs, campaign state, expected audit
   verdicts, `target_effective_status_*`, `audit_status = ...`, generated audit
   verdict payloads, and branch-local logs.
5. Prefer small salvage PRs grouped by coherent topic. Split unrelated lemmas
   rather than bundling them only because they came from the same failed PR.
6. Run the normal audit-system compatibility gate on every salvage branch.
   The resulting rows must remain `unaudited`; the independent audit lane owns
   all verdicts.
7. If no salvage is possible, leave a concise PR comment or review summary
   saying why, for example: "runner only rechecks assumed premise",
   "claim depends on closed sibling", "noncanonical stretch packet with no
   theorem-grade boundary", or "overbroad theorem not supported by runner".

Salvageable examples:

- a parity/counting/no-go lemma with a decisive finite algebra runner;
- a conditional textbook lemma that is useful only when explicitly marked as
  bounded support;
- a negative route that conclusively rules out one proposed mechanism and
  narrows the remaining open gate.

Not salvageable without a new research task:

- audit-hygiene or graph-registration packages;
- branch-local certificates and handoffs with no source theorem;
- broad "closing derivations" whose runner assumes the missing bridge;
- expected audit verdicts or status-elevation packages;
- stretch-attempt notes that document research direction but do not define a
  canonical theorem/no-go/open-gate boundary.

## Fix Policy

If `--no-fix` was passed, do not edit.

Otherwise apply the narrowest honest fix:

1. Fix verified code bugs, broken reproduction commands, stale runner names,
   false PASS checks, and code/prose mismatches.
2. Demote overclaimed status when the artifact supports only support/bounded
   language.
3. Mark imported values explicitly; distinguish derived, admitted, fitted,
   measured, literature, boundary-condition, and insensitive nuisance inputs.
4. Add or repair paired runner/note references only when the artifact exists.
5. Make audit-system hygiene fixes only when they do not change the science:
   status-line tier labels, machine-local path removal, stale runner transcript
   refreshes, generated audit queue/ledger seeding, and discoverability wiring.
6. Update `docs/repo/ACTIVE_REVIEW_QUEUE.md` for live unresolved findings.
7. Route detailed resolved packets to
   `docs/work_history/repo/review_feedback/` only when a long packet is needed.
8. When a PR is non-landable but salvageable, create a new source-only salvage
   branch or PR rather than editing the rejected branch in place if the rejected
   branch contains substantial non-source packet material. Preserve only the
   durable note/runner content and make the claim boundary canonical.

Skip:

- nits;
- suspected findings without evidence;
- ambiguous science gaps that need new derivation;
- attempts to paper over missing theorem steps with confident prose;
- broad refactors unrelated to the finding.

## Audit-System Compatibility Gate

This gate is mandatory when a branch adds or edits source notes, runners,
claim tables, lane stubs, or publication/control-plane files.

The review loop must enforce the audit lane's propose/ratify split without
performing the independent audit:

1. Source-note `Status:` prose is not an audit authority. New or touched claim
   notes should use `Type:` / `Claim type:` metadata for intended audit
   classification.
2. If a no-go/firewall is intended to be theorem-grade, use
   `claim_type = no_go`; do not rely on support-style prose and expect audit
   ratification.
3. Keep disclaimers such as "This is not charged-lepton mass closure" outside
   audit metadata fields.
4. Do not prefill or recommend a verdict in author/review surfaces. Wording
   such as `target_audit_status: audited_clean`, `audit_status =
   audited_clean`, `effective_status = retained`, or "can land audited_clean"
   is not review-loop compatible. Use wording like `audit_status_authority:
   independent audit lane only` and "effective status is pipeline-derived
   after audit ratification and dependency closure."
5. Changed claim notes that cite load-bearing authorities must use markdown
   links, for example
   ``[`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)``.
   Code-formatted names such as `` `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` `` do
   not seed graph dependencies and are not enough.
6. Run the audit pipeline after review fixes:

```bash
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
git diff --check
```

The known graph-cycle warning is acceptable. Any strict-lint error blocks a
review-loop PASS.

The review loop must not run `docs/audit/scripts/apply_audit.py` and must not
write `audit_status`, `audited_clean`, or other audit verdicts. If the branch
introduces retained-grade `claim_type` rows, report those claim IDs in the
final report as requiring the independent audit worker.

After the pipeline, inspect the changed claim rows in
`docs/audit/data/audit_ledger.json`:

- `claim_type` must match the intended class (`positive_theorem`,
  `bounded_theorem`, `no_go`, `open_gate`, `decoration`, or `meta`).
- `audit_status` must remain `unaudited` unless the branch is only carrying
  already-audited history from `origin/main`.
- `effective_status` must be pipeline-derived, not hand-authored.
- New theorem/no-go/bounded rows with declared load-bearing authorities must
  have non-empty `deps` matching the markdown-linked authorities.
- Dependencies asserted as retained-grade must currently have
  `effective_status` in `{retained, retained_bounded, retained_no_go}`. Open
  gates, `unaudited`, `audit_in_progress`, `retained_pending_chain`, and
  terminal non-clean audit statuses are blockers for retained-grade claims.

Useful review-only inventory:

```bash
python3 - <<'PY'
import json, subprocess
changed = set()
for cmd in (
    ["git", "diff", "--name-only", "HEAD"],
    ["git", "diff", "--name-only", "--cached"],
):
    changed.update(subprocess.check_output(cmd, text=True).splitlines())
try:
    changed.update(subprocess.check_output(
        ["git", "diff", "--name-only", "origin/main...HEAD"], text=True
    ).splitlines())
except Exception:
    pass
rows=json.load(open("docs/audit/data/audit_ledger.json"))["rows"]
for cid,row in rows.items():
    if row.get("note_path") in changed:
        print(cid, row.get("claim_type"), row.get("audit_status"),
              row.get("effective_status"), row.get("deps"),
              row.get("note_path"))
PY
```

If generated audit files conflict while integrating current `origin/main`, do
not hand-merge generated JSON/Markdown. Resolve source files, prefer the
current remote generated audit files, then rerun `run_pipeline.sh` and strict
lint so the generated surface is rebuilt from source.

## Smoketest

After fixes, run the smallest relevant checks:

- `python3 -m py_compile <changed .py files>` for changed Python files;
- changed paired runners directly when they are expected to be short;
- if many changed runners are part of the branch, execute all practical
  changed runners with a bounded timeout, then rerun any timeout once with a
  longer timeout before classifying it as slow rather than broken;
- any reproduction commands named in changed notes when practical;
- publication/control-plane consistency checks by reading changed tables and
  nearby authority surfaces.
- `bash docs/audit/scripts/run_pipeline.sh` and
  `python3 docs/audit/scripts/audit_lint.py --strict` when claim notes or
  governance/publication surfaces changed.

If a runner is long, stochastic, or requires unavailable data, do not fake the
check. Report it as not run with the reason.

## Re-Review Tracking

Never re-review unchanged files.

After each fix pass:

1. Identify files modified by the fix pass.
2. If committing is allowed, create one iteration commit:
   `fix: address physics review findings (iteration N)`.
3. Set `files_to_review` to the files modified by the fix pass.
4. Add interacting files only if they are also in the original changed-file
   set. Find interactions through imports, runner/note pairs, canonical harness
   rows, publication tables, and explicit cross-links.
5. Loop until clean, no files changed, or max iterations reached.

## Final Report

Report:

- iterations run;
- files reviewed;
- total findings, fixed findings, skipped findings;
- import/support inventory summary;
- final claim-strength disposition;
- audit-compatibility status and proposed claim IDs needing independent audit;
- commits created;
- checks run and checks skipped;
- remaining issues with disposition;
- recommendation: `PASS`, `PASS WITH BOUNDED CLAIMS`, or `NEEDS MANUAL SCIENCE`.

Do not claim Nature readiness. Say whether the branch meets this repo's
Nature-grade retention bar or exactly what remains open.
