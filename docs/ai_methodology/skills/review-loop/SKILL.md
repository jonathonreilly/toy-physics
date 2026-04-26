---
name: review-loop
description: Use when an LLM agent needs to run `/review-loop`, review branch changes, run parallel physics-specific reviewers, identify overclaims/imported values/support-only material, apply narrow honest fixes, and re-review only files changed by those fixes.
---

# Review Loop

Run a local review/fix/re-review loop for this physics repo. This is not a
generic software review. Its job is to protect the live claim boundary:
retained/Nature-grade claims must have artifact support, imported values must
be explicit, and support-only results must not be promoted by prose.

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
  whether the runner actually tests the note's load-bearing bridge.

- `PhysicsClaimReviewer`
  Attack theorem notes, claims tables, publication surfaces, and prose. Check
  semantic bridges, selector assumptions, status labels, exact/bounded/support
  boundaries, and code/prose drift.

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
  relevant `docs/publication/ci3_z3/` surfaces, and status wording follows
  `docs/repo/CONTROLLED_VOCABULARY.md`.

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
  CONTROLLED_VOCABULARY, CANONICAL_HARNESS_INDEX

Rules:
- Findings must cite file/line when possible.
- Separate bugs, overclaims, support-only demotions, imported-value problems,
  repo-governance problems, and nits.
- Do not require new science for wording problems.
- Do not approve retained/Nature-grade language if an import or bridge remains
  hidden.
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
### Methodology Skill: PASS | FIX | SKIPPED
```

Classify every finding:

- `BUG`
- `OVERCLAIM`
- `IMPORTED_VALUE`
- `SUPPORT_ONLY_DEMOTION`
- `MISSING_ARTIFACT`
- `SEMANTIC_BRIDGE`
- `REPO_GOVERNANCE`
- `NIT`

Stop immediately when all applicable reviewers are clean.

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
5. Update `docs/repo/ACTIVE_REVIEW_QUEUE.md` for live unresolved findings.
6. Route detailed resolved packets to
   `docs/work_history/repo/review_feedback/` only when a long packet is needed.

Skip:

- nits;
- suspected findings without evidence;
- ambiguous science gaps that need new derivation;
- attempts to paper over missing theorem steps with confident prose;
- broad refactors unrelated to the finding.

## Smoketest

After fixes, run the smallest relevant checks:

- `python3 -m py_compile <changed .py files>` for changed Python files;
- changed paired runners directly when they are expected to be short;
- any reproduction commands named in changed notes when practical;
- publication/control-plane consistency checks by reading changed tables and
  nearby authority surfaces.

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
- commits created;
- checks run and checks skipped;
- remaining issues with disposition;
- recommendation: `PASS`, `PASS WITH BOUNDED CLAIMS`, or `NEEDS MANUAL SCIENCE`.

Do not claim Nature readiness. Say whether the branch meets this repo's
Nature-grade retention bar or exactly what remains open.
