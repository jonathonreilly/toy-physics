---
name: review-loop
description: Use when an LLM agent needs to run `/review-loop`, review branch changes, run parallel physics-specific reviewers, identify overclaims/imported values/support-only material, apply narrow honest fixes, verify audit-system compatibility without applying audit verdicts, and re-review only files changed by those fixes.
---

# Review Loop

Run a local review/fix/re-review loop for this physics repo. This is not a
generic software review. Its job is to protect the live claim boundary:
retained/Nature-grade claims must have artifact support, imported values must
be explicit, and support-only results must not be promoted by prose.

This skill is **review only**. It may make branch/package hygiene changes that
allow the independent audit system to parse and queue claims, but it must not
apply audit verdicts, write `audited_clean`, or run the audit worker.
It must not create or open pull requests. When reviewing an existing PR or
branch, review-loop either fixes/narrows that existing landing path and lands it
when requested, or rejects/closes it with a clear reason. Salvage, dependency
chain repair, audit queue regeneration, and parent re-audit gates are part of
that same landing path, not follow-up PRs.
It may correct status vocabulary and terminology so a PR follows repo
conventions, but it must not introduce new repo-wide axioms, new theory
language, new retained-surface claims, or new foundational premises without
explicit user approval. Imports are allowed for bounded theorem surfaces when
they are scoped, labelled, and dependency-checked; repo-wide axiom additions
are not review-loop fixes.

The framework baseline is physical `Cl(3)` on `Z^3`: call these the
`physical Cl(3) local algebra` and the `Z^3 spatial substrate` on live
science surfaces. Do not land new science under bare letter-number names
such as `A1`, `A2`, `G1`, or `R3`; those labels are overloaded with axioms,
assumptions, Lie types, lane stages, route codes, and branch blocks. If a
legacy shorthand is unavoidable, define it as an alias after the explicit
scientific name, for example `Koide Frobenius-equipartition condition
(legacy alias: A1)`. Review-loop must not treat the framework baseline as a
new axiom, new admitted premise, regulator interpretation, or optional
theory language. Correcting a PR back to this repo language is allowed. This
does not promote downstream science by itself: physical-species
identifications, `C_3`-breaking selectors, readout/scale/unit bridges, and
empirical matches remain separate bounded/open inputs unless they have their
own retained-grade derivation and independent audit closure.

The bar is intentionally high: if review-loop is doing its job, the later
fresh-context audit should be mostly confirmatory. Do not pass branches that
leave the audit lane to discover basic claim-boundary, dependency-graph,
status-vocabulary, or runner-validity defects. Do not lose durable science
when a PR fails that bar: before closing or rejecting a branch, run the
salvage pass below and preserve any narrow, runner-backed lemma that can be
made canonical without changing the science.
Non-science PRs require the same discipline: do not reject generated
audit/status or hygiene-only work just because it is not theorem science.
First decide whether it exposes a real audit-graph, cache, queue,
normalization, dependency-chain, or audit-readiness defect. If it does,
salvage the value into durable source, tooling, pipeline, or controlled-data
repairs and regenerate the generated surfaces from that repair.

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

## Stale PR Integration Guard

When landing one or more PRs, protect already-landed science before applying
any branch content. A PR branch may be based before another PR just landed, so
checking out whole files from that stale PR head can erase current-main source
science in shared files.

For every PR before integration:

```bash
git fetch origin main pull/<N>/head:refs/tmp/pr-<N>
pr_base=$(git merge-base origin/main refs/tmp/pr-<N>)
comm -12 \
  <(git diff --name-only "$pr_base"..origin/main | sort) \
  <(git diff --name-only "$pr_base"..refs/tmp/pr-<N> | sort)
```

If the overlap list is non-empty, or if earlier PRs have landed during the
same review-loop run, do **not** run `git checkout refs/tmp/pr-<N> -- <file>`
for those paths. Integrate the PR's delta against its merge base with a
three-way patch, rebase/merge, or cherry-pick source commits, then resolve any
conflicts by preserving both current-main science and the salvageable PR
science:

```bash
git diff --binary "$pr_base"..refs/tmp/pr-<N> -- <source paths> > /tmp/pr<N>.patch
git apply --3way /tmp/pr<N>.patch
```

Whole-file checkout from a PR head is allowed only when the file is new on the
PR or when `git diff --quiet "$pr_base"..origin/main -- <file>` proves current
`main` has not changed that path since the PR base. For every overlapped
source path, do a science-loss guard after integration: the current-main diff
from `pr_base` to `origin/main` must still be represented in the final file.
If that cannot be verified quickly, stop and treat it as a blocking integration
hazard rather than risking science loss.

Generated audit JSON/Markdown is a special case: do not hand-merge generated
files from stale PR heads. Resolve source files first, prefer the current
`origin/main` generated audit surface, then rerun the audit pipeline and strict
lint to regenerate it.

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

- `NoGoDisciplineReviewer`
  Scrutinize negative claims with the same rigor as positive ones. Trigger
  this reviewer whenever changed content includes a `no_go`, `stretch_attempt`,
  `bounded_with_named_walls`, or derived-no-go-boundary artifact, or when any
  other reviewer in this fanout outputs `NO-GO` / `BOUNDED` / `OVERCLAIM` on
  a negative claim. The reviewer must invoke the `no-go-discipline` skill
  and walk N1-N8 against the branch content (see
  [`docs/ai_methodology/skills/no-go-discipline/SKILL.md`](../no-go-discipline/SKILL.md)):
  N1 alternative-route enumeration (≥5 distinct routes), N2
  wall-independence audit, N3 hidden-wall scan, N4 residual matching,
  N5 rhetoric audit (per-element / per-mode / per-block / lattice-wide
  resolutions), N6 partial-closure path scan (convention-reframe vs new
  axiom), N7 steelman, N8 cross-cycle echo. Output `PASS` (negative claim
  honestly scoped) or `FAIL` with the failing checklist items named and the
  narrowest demoted claim proposed (`partial-attempt-with-named-untested-routes`,
  `partial-narrowing`, `bounded-with-corrected-wall-count`, or
  `stretch-attempt-with-honest-residual`). The reviewer must not approve a
  no-go that has not been stress-tested against the framework's full
  authority surface — under-tested negative claims are at least as harmful
  as overclaimed positive ones because they foreclose investigation paths
  permanently.

- `RepoGovernanceReviewer`
  Check placement and authority surfaces. Ensure live findings route through
  `docs/repo/ACTIVE_REVIEW_QUEUE.md`, long packets go under
  `docs/work_history/repo/review_feedback/`, publication edits update the
  relevant `docs/publication/ci3_z3/` surfaces, status wording follows
  `docs/repo/CONTROLLED_VOCABULARY.md`, and changed claim notes are compatible
  with the audit lane's propose/ratify split. Also verify that load-bearing
  dependencies are real markdown links that seed the citation graph, not just
  code-formatted file names in prose. Block ambiguous new science names such
  as bare `A1`, `A2`, `G1`, `R3`, `Route F`, or `Block 2` when they appear as
  titles, primary table labels, claim scopes, runner headlines, or review
  findings without an explicit scientific noun phrase. Block repo-wide axiom
  additions, nonstandard theory vocabulary, or new foundational claims unless
  the user explicitly approved that change; vocabulary corrections back to
  repo conventions are allowed.

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
- Do not approve new bare letter-number science names. Require explicit names
  from CONTROLLED_VOCABULARY, with shorthand only as a parenthetical alias.
- Do not approve a `NO-GO` or `BOUNDED with named walls` recommendation
  without running `no-go-discipline` N1-N8 against the branch content. An
  unscrutinized negative claim forecloses investigation paths permanently and
  is at least as harmful as an overclaimed positive.
````

## Consolidate Findings

Present one iteration summary:

```text
## Review Results (Iteration N)

### Code / Runner: PASS | RISK | FAIL
### Physics Claim Boundary: RETAINED | SUPPORT | BOUNDED | OPEN | REJECT
### Imports / Support: CLEAN | DISCLOSED | DEMOTE | FAIL
### Nature Retention: RETAINED | RETAINED SUPPORT | BOUNDED | OPEN | NO-GO | REJECT
### No-Go Discipline: PASS | FAIL | NOT APPLICABLE
### Repo Governance: PASS | FIX | QUEUE | ARCHIVE
### Audit Compatibility: PASS | FIX | BLOCKED | NOT APPLICABLE
### Methodology Skill: PASS | FIX | SKIPPED
```

Classify every finding:

- `BUG`
- `OVERCLAIM`
- `NO_GO_OVERCLAIM`
- `IMPORTED_VALUE`
- `SUPPORT_ONLY_DEMOTION`
- `MISSING_ARTIFACT`
- `SEMANTIC_BRIDGE`
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
   - audit/process hygiene: dependency-graph repairs, audit queue unlocks,
     stale runner-cache detection, generated-data normalization, cycle-break
     hygiene, and pipeline/tooling fixes that make audit results more reliable;
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
     derivation and reviewed in the same salvage branch.
3. Do not salvage by papering over missing science. If the durable part is
   only an obstruction or failed route, salvage it as a narrow `open_gate` or
   `no_go` only when the runner directly supports that negative boundary.
4. Strip all non-source material from salvage branches:
   claim-status certificates, handoffs, campaign state, expected audit
   verdicts, `target_effective_status_*`, `audit_status = ...`, generated audit
   verdict payloads, and branch-local logs.
5. Prefer small salvage slices grouped by coherent topic. Split unrelated
   lemmas rather than bundling them only because they came from the same failed
   PR, but do not open follow-up PRs for those slices. Land them through the
   current requested landing path or report that the work cannot be landed yet.
6. Run the normal audit-system compatibility gate on every salvage slice.
   The resulting rows must remain `unaudited`; the independent audit lane owns
   all verdicts.
7. For audit/process hygiene, preserve the durable repair rather than the
   generated symptom. Land source/tooling/pipeline/controlled-data changes when
   they strengthen the repo or unblock auditing without changing science.
   Regenerate audit JSON/Markdown from the pipeline afterward. Do not land
   hand-authored `effective_status`, `intrinsic_status`, `audit_status`, or
   expected-verdict edits as the authority for the change.
8. If no salvage is possible, leave a concise PR comment or review summary
   saying why, for example: "runner only rechecks assumed premise",
   "claim depends on closed sibling", "noncanonical stretch packet with no
   theorem-grade boundary", or "overbroad theorem not supported by runner".

Salvageable examples:

- a parity/counting/no-go lemma with a decisive finite algebra runner;
- a conditional textbook lemma that is useful only when explicitly marked as
  bounded support;
- a negative route that conclusively rules out one proposed mechanism and
  narrows the remaining open gate;
- an audit-hygiene PR whose generated status change reveals a real durable
  graph/tooling/pipeline defect, salvaged as the underlying repair plus
  regenerated audit outputs.

Not salvageable without a new research task:

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
6. Rename ambiguous science shorthand to explicit repo vocabulary without
   changing the claim boundary. Examples: write `physical Cl(3) local algebra`,
   `Z^3 spatial substrate`, `Koide Frobenius-equipartition condition`, or
   `Lie type A_1` instead of bare `A1` / `A2`.
7. Update `docs/repo/ACTIVE_REVIEW_QUEUE.md` for live unresolved findings.
8. Route detailed resolved packets to
   `docs/work_history/repo/review_feedback/` only when a long packet is needed.
9. When a PR is non-landable but salvageable, preserve only the durable
   note/runner content, make the claim boundary canonical, and land that source
   salvage through the current requested landing path. If the rejected branch
   contains substantial non-source packet material, use a clean temporary
   worktree for integration, but do not create or open a follow-up PR.

Skip:

- nits;
- suspected findings without evidence;
- ambiguous science gaps that need new derivation;
- attempts to paper over missing theorem steps with confident prose;
- repo-wide axiom additions, new theory terminology, or new foundational
  premises that lack explicit user approval;
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

7. **Pipeline-clean PASS gate (hard).** After running the pipeline, the
   following must hold for review-loop to issue PASS:

```bash
# Must produce no output. Any change here means the branch did not
# include the regenerated audit-data files; commit them before PASS.
git status --porcelain docs/audit/AUDIT_LEDGER.md \
                       docs/audit/AUDIT_QUEUE.md \
                       docs/audit/data \
                       docs/publication/ci3_z3/PUBLICATION_AUDIT_DIVERGENCE.md \
                       docs/publication/ci3_z3/CLAIMS_TABLE_EFFECTIVE_STATUS.md \
                       docs/publication/ci3_z3/DERIVATION_ATLAS_EFFECTIVE_STATUS.md \
                       docs/publication/ci3_z3/PUBLICATION_MATRIX_EFFECTIVE_STATUS.md \
                       docs/publication/ci3_z3/FULL_CLAIM_LEDGER_EFFECTIVE_STATUS.md \
                       docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX_EFFECTIVE_STATUS.md \
                       docs/publication/ci3_z3/RESULTS_INDEX_EFFECTIVE_STATUS.md \
                       docs/publication/ci3_z3/QUANTITATIVE_SUMMARY_TABLE_EFFECTIVE_STATUS.md \
                       docs/publication/ci3_z3/DERIVATION_VALIDATION_MAP_EFFECTIVE_STATUS.md
```

If this command prints any lines, BLOCK PASS and instruct the operator to
commit the regenerated files. When the audit workflow template is installed
as `.github/workflows/audit.yml`, PR runs enforce the same gate and the nightly
cron refreshes main; review-loop must not let a branch reach merge with
pipeline-derived files out of date with the source notes.

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
