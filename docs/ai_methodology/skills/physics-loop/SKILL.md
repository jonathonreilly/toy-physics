---
name: physics-loop
description: Use when an LLM agent needs to plan, launch, resume, or package a long-running theoretical-physics loop on a major hard open lane/problem, with repo grounding, assumption/import audits, no-go memory, deep first-principles stretch attempts, stuck fan-out, unattended checkpoints, review-loop backpressure, and one review PR per science block.
---

# Physics Loop

Run a stateful theoretical-physics loop that can make a major lane move:
retire a load-bearing import, close an exact support gate, prove a useful
no-go, add a decisive artifact, or isolate the remaining Nature-grade blocker.

This skill is not a bigger `/autopilot` and not a factory for easy audit
artifacts. It is a claim-state machine for hard physics. It must spend real
time on named hard residuals before stopping, and it must leave reviewable PRs
for the backlog.

## Arguments

Parse:

- goal/problem text: required unless running `status` or `resume`;
- `--mode plan|run|resume|status`: optional, infer from the user request;
- `--runtime DURATION`: optional unattended runtime such as `45m`, `2h`, or
  `6h`;
- `--target retained|exact-support|bounded-support|no-go|best-honest-status`:
  optional, default `best-honest-status`;
- `--loop SLUG`: optional existing or new loop slug;
- `--workstream SLUG`: legacy alias for `--loop`;
- `--literature`: allow targeted physics/math literature review;
- `--max-cycles N`: optional cap on major execution cycles;
- `--checkpoint-interval DURATION`: optional, default `30m`;
- `--deep-block DURATION`: optional sustained hard-problem block, default
  `90m`;
- `--no-pr`: do not open end-of-loop review PRs;
- `--no-review-loop`: skip milestone `/review-loop` only if the user asked;
- `--no-commit`: do not create commits.

If `--runtime` is absent and the user wants execution, ask how long to run
before launching unattended work. Do not assume a fixed default. If the user
only asks for planning, produce the plan without asking for runtime.

## Science Delivery And PR Policy

For science loops, execute on clean remote branches and open review PRs at the
end. Do not merge those PRs and do not push science work directly to `main`.

- Start science execution from current `origin/main` after `git fetch origin`.
- Use a dedicated branch namespace such as `physics-loop/<slug>-YYYYMMDD`.
- If the current worktree is dirty or not disposable, create a clean worktree
  from `origin/main` instead of mixing loop output with other changes.
- Treat each coherent major cycle as a **science block**. Prefer one branch per
  science block:
  `physics-loop/<slug>-blockNN-YYYYMMDD`.
- If a block depends on prior unmerged block output, create a stacked PR whose
  base is the prior block branch. If independent, base it on `main`.
- Commit coherent science artifacts to the block branch and push it to
  `origin`.
- At the end of the loop, unless `--no-pr` was supplied, open one review PR per
  science block. Use `gh pr create` when authenticated; otherwise write
  `PR_BACKLOG.md` with exact commands and reasons PR creation failed.
- PR titles must include `[physics-loop]`, the lane/block slug, and the honest
  status (`retained`, `exact-support`, `bounded-support`, `no-go`, `open`, or
  `demotion`).
- PR bodies must link the block's `HANDOFF.md`, notes, runners, verification
  commands/results, review findings, imports retired/exposed, and remaining
  blockers.
- Do not merge, push science to `main`, or update repo-wide authority surfaces
  as part of the science run.

Allowed science-branch output:

- theorem/support/no-go notes;
- scripts/runners and paired outputs needed to inspect the result;
- branch-local loop state under `.claude/science/physics-loops/`;
- review history and handoff notes for later integration.

Do not weave science results through `README`, `docs/repo/LANE_REGISTRY.yaml`,
`docs/work_history/repo/LANE_STATUS_BOARD.md`, publication matrices,
canonical-harness indexes, active review queues, or methodology docs during the
science run unless the user's task is explicitly a skill/governance update.
Record proposed weaving in `HANDOFF.md` for the later review process.

## Loop Pack

Create or update a durable pack under:

```text
.claude/science/physics-loops/<slug>/
  STATE.yaml
  GOAL.md
  ASSUMPTIONS_AND_IMPORTS.md
  ROUTE_PORTFOLIO.md
  NO_GO_LEDGER.md
  LITERATURE_BRIDGES.md
  ARTIFACT_PLAN.md
  REVIEW_HISTORY.md
  HANDOFF.md
  PR_BACKLOG.md
```

Legacy packs under `.claude/science/frontier-workstreams/<slug>/` may be read
for resume/migration, but new loop state should use `physics-loops`.

Use `STATE.yaml` as the resume surface: current goal, target status, runtime,
cycle/block count, active route, hard residual being attacked, files touched,
open imports, no-go routes, review findings, PR status, next exact action, and
stop condition.

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
   into `NO_GO_LEDGER.md` so the loop does not re-explore dead routes.
5. **Generate route portfolio.** Produce several independent routes and score
   them by likely claim-state movement. See
   [`references/route-patterns.md`](references/route-patterns.md).
6. **Apply the dramatic-step gate.** Execute only routes that can change the
   lane state: import retired, exact support added, no-go proven, major blocker
   isolated, or novel structure introduced with a falsifier.
7. **Execute one major cycle.** Produce a theorem note, runner/log pair,
   import-retirement audit, literature bridge, no-go packet, or demotion
   packet. Keep edits scoped to the chosen route.
8. **Run deep-work pressure when stuck.** If the last two cycles were
   audit/no-go/blocker-isolation outputs, or if no easy route passes the gate,
   run a stretch-attempt cycle before any stop. See **Deep Work Rules** below.
9. **Checkpoint.** Update `STATE.yaml` and `HANDOFF.md` at least every
   checkpoint interval, before long scripts, after long scripts, and before
   stopping.
10. **Review at milestones.** After each major artifact, run the `review-loop`
   skill unless disabled. In science-run mode, record findings in branch-local
   `REVIEW_HISTORY.md` and `HANDOFF.md`; do not update the live active review
   queue or other repo-wide authority surfaces before the later review and
   integration process. Either fix locally, demote locally, archive locally, or
   select a new route.
11. **Close the cycle honestly.** Use the narrowest honest status inside the
    branch artifacts: retained, exact support, bounded support, open, no-go,
    reject, or historical. Do not patch a missing theorem step with prose. Put
    any proposed repo-wide weaving in `HANDOFF.md` for later review and
    backpressure integration.
12. **Open review PRs.** At loop end, open or prepare one PR per science block
    unless `--no-pr` was supplied.

## Deep Work Rules

The loop must not stop merely because audit-grade routes are easy and hard
routes are risky.

- **Audit quota:** after two consecutive cycles whose main output is a no-go,
  demotion, dependency firewall, or blocker-isolation artifact, the next cycle
  must be a stretch attempt on a named hard residual.
- **Stretch attempt:** choose one blocker from `STATE.yaml` or `HANDOFF.md` and
  work it from minimal repo primitives for at least one `--deep-block`
  interval when runtime allows. A valid output may be partial structure,
  a sharper obstruction, a falsified premise, or a worked failed derivation
  with the exact load-bearing wall named.
- **First-principles reset:** before the stretch attempt, write the minimal
  allowed premise set (`A_min`) and forbidden imports. The attempt must not
  rely on observed target values, fitted selectors, or literature as hidden
  proof inputs.
- **Stuck fan-out:** before declaring "no route passes the gate", generate
  3-5 orthogonal premises/attack frames. If the active tool policy and user
  authorization allow parallel agents, run them in parallel; otherwise emulate
  the fan-out sequentially in separate notes/sections. Synthesize agreements,
  contradictions, and the best remaining attack.
- **Longer cadence:** checkpoint every `--checkpoint-interval`, but do not turn
  every checkpoint into a polished artifact. Sustained 90-120 minute hard
  attempts are preferred over several shallow audit cycles.
- **No shallow stop:** after the most recent blocker, do not stop until at
  least one stretch attempt and one stuck fan-out synthesis have been recorded,
  unless runtime is exhausted or tooling fails.
- **No-churn exception:** an honest first-principles attempt with named
  obstructions is valid progress even without closure. This exception does not
  allow vague prose, unverified algebra, or unsupported status promotion.

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
- push only dedicated science block branches;
- open or prepare one review PR per science block at the end;
- never push science work to `main`.

## Stop Conditions

Stop and write a clear `HANDOFF.md` when:

- runtime or max cycles is reached;
- no route passes the dramatic-step gate **after** the Deep Work Rules have
  been satisfied;
- review-loop finds a blocker that requires human science judgment;
- the worktree changes externally in a way that affects the route;
- the target status is honestly achieved;
- required network/literature/tool access is unavailable.

## Final Report

Report:

- loop slug and target;
- remote science branch;
- runtime used and cycles completed;
- claim-state movement achieved;
- imports retired or newly exposed;
- artifacts created and checks run;
- review-loop findings and disposition;
- commits and PRs created, if any;
- PRs that could not be opened, with exact recovery commands;
- remaining Nature-grade blockers;
- exact next action from `HANDOFF.md`.

Do not claim Nature-grade closure unless the assumptions/import ledger,
decisive artifact, and review-loop disposition all support it.
