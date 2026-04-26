---
name: frontier-workstream
description: Use when an LLM agent needs to plan, launch, resume, or package a long-running theoretical-physics workstream on a major open lane/problem, with repo grounding, assumption/import audits, retained/no-go/literature review, dramatic-step route selection, unattended checkpoints, review-loop backpressure, and selective landing.
---

# Frontier Workstream

Run a stateful theoretical-physics workstream that can make a major lane move:
retire a load-bearing import, close an exact support gate, prove a useful
no-go, add a decisive artifact, or isolate the remaining Nature-grade blocker.

This skill is not a bigger `/autopilot`. It is a claim-state machine. Do not
run low-value iterations that only add prose, nearby runners, or another route
already killed by prior no-go work.

## Arguments

Parse:

- goal/problem text: required unless running `status` or `resume`;
- `--mode plan|run|resume|status`: optional, infer from the user request;
- `--runtime DURATION`: optional unattended runtime such as `45m`, `2h`, or
  `6h`;
- `--target retained|exact-support|bounded-support|no-go|best-honest-status`:
  optional, default `best-honest-status`;
- `--workstream SLUG`: optional existing or new workstream slug;
- `--literature`: allow targeted physics/math literature review;
- `--max-cycles N`: optional cap on major execution cycles;
- `--checkpoint-interval DURATION`: optional, default `30m`;
- `--no-review-loop`: skip milestone `/review-loop` only if the user asked;
- `--no-commit`: do not create commits.

If `--runtime` is absent and the user wants execution, ask how long to run
before launching unattended work. Do not assume a fixed default. If the user
only asks for planning, produce the plan without asking for runtime.

## Science Delivery Policy

For science workstreams, deliver work as a clean remote branch, not a PR and
not a direct weave into `main`.

- Start science execution from current `origin/main` after `git fetch origin`.
- Use a dedicated branch such as `frontier/<slug>-YYYYMMDD` or a user-provided
  branch name.
- If the current worktree is dirty or not disposable, create a clean worktree
  from `origin/main` instead of mixing workstream output with other changes.
- Commit coherent science artifacts to that branch and push the branch to
  `origin`.
- Do not open a PR.
- Do not merge, push to `main`, or update repo-wide authority surfaces as part
  of the science run.

Allowed science-branch output:

- theorem/support/no-go notes;
- scripts/runners and paired outputs needed to inspect the result;
- branch-local workstream state under `.claude/science/frontier-workstreams/`;
- review history and handoff notes for later integration.

Do not weave science results through `README`, `docs/repo/LANE_REGISTRY.yaml`,
`docs/work_history/repo/LANE_STATUS_BOARD.md`, publication matrices,
canonical-harness indexes, active review queues, or methodology docs during the
science run unless the user's task is explicitly a skill/governance update.
Record proposed weaving in `HANDOFF.md` for the later review process.

## Workstream Pack

Create or update a durable pack under:

```text
.claude/science/frontier-workstreams/<slug>/
  STATE.yaml
  GOAL.md
  ASSUMPTIONS_AND_IMPORTS.md
  ROUTE_PORTFOLIO.md
  NO_GO_LEDGER.md
  LITERATURE_BRIDGES.md
  ARTIFACT_PLAN.md
  REVIEW_HISTORY.md
  HANDOFF.md
```

Use `STATE.yaml` as the resume surface: current goal, target status, runtime,
cycle count, active route, files touched, open imports, no-go routes, review
findings, next exact action, and stop condition.

## Required Grounding

Before proposing or executing routes, read the relevant current repo surfaces:

- `docs/repo/REPO_ORGANIZATION.md`
- `docs/repo/CONTROLLED_VOCABULARY.md`
- `docs/repo/ACTIVE_REVIEW_QUEUE.md`
- `docs/repo/REVIEW_FEEDBACK_WORKFLOW.md`
- `docs/CANONICAL_HARNESS_INDEX.md`
- `docs/repo/LANE_REGISTRY.yaml`
- `docs/work_history/repo/LANE_STATUS_BOARD.md`
- relevant notes, runners, retained logs, publication tables, no-go notes, and
  atlas/tool surfaces for the requested lane.

For publication-facing or quantitative work, also inspect
`docs/publication/ci3_z3/` and
`docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md`.

## Workflow

1. **Preflight.** Check worktree state. If running unattended or modifying
   files, use the repo lock protocol and plan lock refreshes at checkpoints.
2. **Ground.** Build the current lane map from repo authority surfaces rather
   than memory.
3. **Audit assumptions/imports.** Create or refresh
   `ASSUMPTIONS_AND_IMPORTS.md`. See
   [`references/assumption-import-audit.md`](references/assumption-import-audit.md).
4. **Update no-go memory.** Extract prior no-go routes and reviewer objections
   into `NO_GO_LEDGER.md` so the workstream does not re-explore dead routes.
5. **Generate route portfolio.** Produce several independent routes and score
   them by likely claim-state movement. See
   [`references/route-patterns.md`](references/route-patterns.md).
6. **Apply the dramatic-step gate.** Execute only routes that can change the
   lane state: import retired, exact support added, no-go proven, major blocker
   isolated, or novel structure introduced with a falsifier.
7. **Execute one major cycle.** Produce a theorem note, runner/log pair,
   import-retirement audit, literature bridge, no-go packet, or demotion
   packet. Keep edits scoped to the chosen route.
8. **Checkpoint.** Update `STATE.yaml` and `HANDOFF.md` at least every
   checkpoint interval, before long scripts, after long scripts, and before
   stopping.
9. **Review at milestones.** After each major artifact, run the `review-loop`
   skill unless disabled. In science-run mode, record findings in branch-local
   `REVIEW_HISTORY.md` and `HANDOFF.md`; do not update the live active review
   queue or other repo-wide authority surfaces before the later review and
   integration process. Either fix locally, demote locally, archive locally, or
   select a new route.
10. **Close the cycle honestly.** Use the narrowest honest status inside the
    branch artifacts: retained, exact support, bounded support, open, no-go,
    reject, or historical. Do not patch a missing theorem step with prose. Put
    any proposed repo-wide weaving in `HANDOFF.md` for later review and
    backpressure integration.

## Literature

Use literature only when the user passes `--literature` or the route requires a
known theorem/experimental comparator. Prefer primary sources and stable math
references. Any literature value, theorem, or convention must be entered in the
assumption/import ledger with its role: bridge, comparator, admitted convention,
or non-derivation context. See
[`references/literature-bridge-protocol.md`](references/literature-bridge-protocol.md).

## Long-Running Execution

For unattended runs, follow
[`references/long-running-execution.md`](references/long-running-execution.md).
In short:

- ask for runtime if absent;
- avoid mid-run questions;
- checkpoint enough state that another agent can resume;
- refresh the lock before it expires;
- stop cleanly when runtime, max cycles, review blockers, or claim closure
  dictate;
- push only the dedicated science branch; never push to `main` from a science
  workstream.

## Stop Conditions

Stop and write a clear `HANDOFF.md` when:

- runtime or max cycles is reached;
- no route passes the dramatic-step gate;
- review-loop finds a blocker that requires human science judgment;
- the worktree changes externally in a way that affects the route;
- the target status is honestly achieved;
- required network/literature/tool access is unavailable.

## Final Report

Report:

- workstream slug and target;
- remote science branch;
- runtime used and cycles completed;
- claim-state movement achieved;
- imports retired or newly exposed;
- artifacts created and checks run;
- review-loop findings and disposition;
- commits created, if any;
- remaining Nature-grade blockers;
- exact next action from `HANDOFF.md`.

Do not claim Nature-grade closure unless the assumptions/import ledger,
decisive artifact, and review-loop disposition all support it.
