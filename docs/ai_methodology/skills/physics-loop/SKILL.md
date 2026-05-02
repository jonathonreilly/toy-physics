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
time on named hard residuals before a route can be declared blocked or the
campaign can end, and it must leave reviewable PRs for the backlog.

When launched for a long unattended run, the default posture is a **campaign**:
keep working until the runtime or max-cycle budget is exhausted. If one route
or lane hits an honest stop, checkpoint it, select the next ranked science
opportunity from the repo, and continue. Do not stop the whole campaign merely
because the first target ends in a no-go, support-only boundary, or
human-judgment blocker.

For a request like "run for 12 hours unattended", treat the runtime as a work
budget, not a maximum that can be abandoned after the first clean stop. The
agent should spend the allotted time unless a global safety/tooling condition
makes safe continuation impossible. Per-route blockers, review demotions,
dirty PRs, missing retained proof, unavailable optional literature, or failed
PR creation are not global stop conditions; they trigger demotion/backlog,
checkpoint, and pivot.

## Arguments

Parse:

- goal/problem text: required unless running `status` or `resume`;
- `--mode plan|run|resume|status|campaign`: optional, infer from the user
  request;
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
- `--no-pr`: do not open review PRs;
- `--no-review-loop`: skip milestone `/review-loop` only if the user asked;
- `--no-commit`: do not create commits.

If `--runtime` is absent and the user wants execution, ask how long to run
before launching unattended work. Do not assume a fixed default. If the user
only asks for planning, produce the plan without asking for runtime.

Infer `--mode campaign` when the user asks for an overnight, unattended,
long-running, or 12-hour run, even if the user says only `run`. A campaign
keeps selecting science blocks until the runtime/max-cycle budget or global
queue exhaustion condition is reached.

## Science Delivery And PR Policy

For science loops, execute on clean remote branches and open review PRs for
each coherent block. Do not merge those PRs and do not push science work
directly to `main`.
No supervisor prompt may override this by telling the worker not to open PRs
unless the user explicitly supplied `--no-pr`.

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
- At each science-block closure, unless `--no-pr` was supplied, open one review
  PR for that block before pivoting to the next opportunity. Use
  `gh pr create` when authenticated; otherwise write `PR_BACKLOG.md` with
  exact commands and reasons PR creation failed.
- After opening a PR, verify it with `gh pr view` or `gh pr list`. If the PR is
  dirty against its intended base, update the branch or explicitly mark it as
  stacked in the PR body and `HANDOFF.md`.
- If PR creation or verification fails for network/auth reasons, write a
  complete `PR_BACKLOG.md` and continue the campaign if runtime remains.
  Missing GitHub access is a delivery degradation, not a science stop.
- PR titles must include `[physics-loop]`, the lane/block slug, and the honest
  status (`proposed_retained`, `proposed_promoted`, `exact-support`,
  `bounded-support`, `no-go`, `open`, or `demotion`).
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
  OPPORTUNITY_QUEUE.md
  NO_GO_LEDGER.md
  LITERATURE_BRIDGES.md
  ARTIFACT_PLAN.md
  CLAIM_STATUS_CERTIFICATE.md
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

Use `OPPORTUNITY_QUEUE.md` in campaign mode. It must rank candidate science
targets by:

- retained-positive probability;
- missing-import count;
- runner/test availability;
- review landability;
- blast radius and branch size;
- whether the target is independent of the just-blocked lane.

Use `CLAIM_STATUS_CERTIFICATE.md` for every science block. It must record the
actual current-surface status, any conditional/hypothetical status, dependency
classes, open imports, review-loop disposition, whether
`proposed_retained` / `proposed_promoted` wording is allowed in the PR
title/body/status lines, and whether independent audit remains required.

## Claim-Status Firewalls

The loop must separate actual current-surface status from conditional or
hypothetical status.

Every theorem/support/no-go note and every loop `STATE.yaml` checkpoint must
state the narrowest status using the controlled vocabulary. When a result
depends on a new axiom, same-surface family, observational admission, fitted
selector, admitted unit convention, or human judgment, the actual current
surface status is **not** `retained`.

Required status fields for major artifacts:

```yaml
actual_current_surface_status: open|no-go|exact-support|bounded-support|conditional-support|demotion|proposed_retained|proposed_promoted
conditional_surface_status: null|...
hypothetical_axiom_status: null|...
admitted_observation_status: null|...
proposal_allowed: true|false
proposal_allowed_reason: "..."
audit_required_before_effective_retained: true|false
bare_retained_allowed: false
```

Hard wording bans in branch-local physics-loop artifacts:

- bare `retained` / `promoted` in source-note `Status:` lines;
- `retained branch-local`
- `would become retained`
- `promoted to retained`
- `retained on the actual surface` when a required premise is conditional,
  hypothetical, admitted, fitted, or human-judgment-only.

`proposed_retained` / `proposed_promoted` are allowed only when the certificate
supports a theorem-grade author proposal and marks the later independent audit
requirement. They must never be presented as audit-ratified retained status.

Allowed replacements include `exact negative boundary`, `exact support`,
`bounded support`, `conditional / support`, `open`, `demotion`, and
`hypothetical consequence map`. If the artifact maps what would follow from an
unadopted axiom, every table and runner summary must say "conditional on
accepted new axiom; not retained on the actual current surface."

## Retained-Proposal Certificate

Bare `retained` / `promoted` is an audit-ratified effective status, not a
branch-local author status. A physics-loop PR, note, runner, or status line may
use `proposed_retained` / `proposed_promoted` only after all of these are true:

1. `CLAIM_STATUS_CERTIFICATE.md` says `proposal_allowed: true`.
2. No open imports remain for the claimed target.
3. No observed target values, fitted selectors, admitted unit conventions, or
   literature values are load-bearing proof inputs.
4. Every dependency is retained, a retained corollary, or explicitly allowed
   exact support on the current authority surface.
5. A runner or proof artifact checks dependency classes, not only numerical
   output.
6. Review-loop disposition is `pass`; `pending`, `passed_with_notes`,
   `demote`, or `block` cannot certify a retained-grade proposal.
7. The PR body and handoff explicitly say independent audit is still required
   before the repo may treat the claim as effective retained/promoted.

If any item fails, use `open`, `exact-support`, `bounded-support`,
`conditional-support`, `no-go`, or `demotion` instead.

## Campaign Continuation Policy

Long unattended runs must continue through local stops.

In campaign or resume mode, a clean checkpoint is not a stop condition. Do not
send a final answer, release the repo lock, or stand down merely because a
route ends in no-go, exact support, bounded support, support-only status,
failed PR update, or missing retained closure. Treat each coherent block as a
checkpoint inside the larger run unless one of the explicit global stop
conditions below is met.

Nonfatal events that must **not** end a campaign while runtime remains:

- a route produces a no-go, exact negative boundary, demotion, or blocker;
- a route produces exact support, bounded support, or support-only evidence
  without the target retained/proposed-retained certificate;
- review-loop returns `demote` or `block` for the current artifact;
- retained-proposal certification fails;
- a PR is dirty, stacked, or cannot be opened because of GitHub/network auth;
- a lane reaches a human-judgment premise;
- optional literature access is unavailable for one route;
- the repo automation lock is unavailable but a branch-local supervisor lock
  can still prevent duplicate work.

Required response to a nonfatal event:

1. write the block's theorem/support/no-go note, runner, and output
   certificate;
2. demote or archive the current artifact honestly;
3. checkpoint `STATE.yaml`, `HANDOFF.md`, `REVIEW_HISTORY.md`, and
   `CLAIM_STATUS_CERTIFICATE.md`;
4. update the campaign status runner/certificate;
5. run the required checks for the block;
6. commit and push the coherent block;
7. open/update the PR, or write `PR_BACKLOG.md` when PR editing is
   unavailable;
8. refresh `OPPORTUNITY_QUEUE.md`;
9. immediately choose the next highest-ranked retained-positive opportunity
   and continue.

Global stop is allowed only when:

- runtime or max cycles is exhausted;
- the named target has a genuinely passing retained/proposed-retained
  certificate and the user did not request continued campaign work beyond that
  target;
- the worktree/repo changes externally in a way that makes safe continuation
  impossible;
- required core tooling for all viable routes is unavailable;
- a lock conflict means another active worker owns the same repo/task and no
  clean independent worktree can be created;
- the refreshed opportunity queue proves every viable target is blocked and no
  independent retained-positive candidate remains.

If context compacts, the session resumes, or a new worker takes over, read
`STATE.yaml` and `HANDOFF.md` first, reacquire or verify the repo lock, and
continue from the recorded next exact action before reopening broad planning.

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
6. **Build the opportunity queue.** In campaign mode or unattended runs longer
   than one major cycle, create `OPPORTUNITY_QUEUE.md` and keep at least three
   ranked science opportunities unless the repo has fewer viable open targets.
   Prefer retained-positive opportunities over more audit churn after one or
   two no-go/support-only cycles.
7. **Apply the dramatic-step gate.** Execute only routes that can change the
   lane state: import retired, exact support added, no-go proven, major blocker
   isolated, or novel structure introduced with a falsifier.
8. **Execute one major cycle.** Produce a theorem note, runner/log pair,
   import-retirement audit, literature bridge, no-go packet, or demotion
   packet. Keep edits scoped to the chosen route.
9. **Run deep-work pressure when stuck.** If the last two cycles were
   audit/no-go/blocker-isolation outputs, or if no easy route passes the gate,
   run a stretch-attempt cycle before declaring the active route blocked. See
   **Deep Work Rules** below.
10. **Certify status.** Before committing a block, write or update
    `CLAIM_STATUS_CERTIFICATE.md`. Demote any title, status line, table row,
    runner printout, or handoff sentence that fails the retained-proposal
    certificate.
11. **Checkpoint.** Update `STATE.yaml` and `HANDOFF.md` at least every
   checkpoint interval, before long scripts, after long scripts, and before
   any authorized campaign stop.
12. **Review at milestones.** After each major artifact, run the `review-loop`
   skill unless disabled. In science-run mode, record findings in branch-local
   `REVIEW_HISTORY.md` and `HANDOFF.md`; do not update the live active review
   queue or other repo-wide authority surfaces before the later review and
   integration process. The local disposition must be one of `pass`, `demote`,
   or `block`; `self-review pending` is not enough to push a PR. Either fix
   locally, demote locally, archive locally, or select a new route.
13. **Close the cycle honestly.** Use the narrowest honest status inside the
    branch artifacts: proposed_retained / proposed_promoted only when the
    certificate allows an audit-ready proposal; otherwise exact support,
    bounded support, open, no-go, reject, or historical. Do not patch a missing
    theorem step with prose. Put
    any proposed repo-wide weaving in `HANDOFF.md` for later review and
    backpressure integration.
14. **Open review PRs.** At each block closure, open or prepare one PR for the
    coherent science block unless `--no-pr` was supplied. In campaign mode,
    a missing PR must become `PR_BACKLOG.md` and the campaign must continue if
    runtime remains.
15. **Continue the campaign or stop.** After PR/backlog handling, if runtime
    remains and the current lane is blocked or closed, pick the next
    `OPPORTUNITY_QUEUE.md` item and continue without sending a final report or
    releasing the repo lock. Stop the whole campaign only when runtime/max
    cycles expires, the target status is genuinely achieved and no further
    campaign target was requested, or the queue has been freshly scanned and
    every viable opportunity is blocked by human judgment/tooling.
    In campaign mode, even successful retained-grade proposal of one target is
    a checkpoint, not a stop, unless no further target was requested or no
    viable next opportunity exists.

## Deep Work Rules

The loop must not stop merely because audit-grade routes are easy and hard
routes are risky.

- **Audit quota:** after two consecutive cycles whose main output is a no-go,
  demotion, dependency firewall, or blocker-isolation artifact, the next cycle
  must be a stretch attempt on a named hard residual.
- **Positive-retention pivot:** after a stretch attempt and one no-go/support
  cycle on the same lane, campaign mode must check the opportunity queue and
  prefer a different retained-positive candidate unless the current lane has a
  concrete next route with higher retained-positive probability.
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
  unless runtime is exhausted or required core tooling fails for every viable
  queued route.
- **No all-lane stop without queue evidence:** do not create a global stop
  marker such as `STOP_ALL_LANES_REQUESTED` unless `OPPORTUNITY_QUEUE.md` was
  refreshed in the same checkpoint and records why each viable next target is
  blocked.
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
- continue to the next ranked opportunity when one lane blocks and runtime
  remains;
- after every coherent block, write docs/runner/output, update the loop pack
  and campaign certificate, run checks, commit, push, record `PR_BACKLOG.md`
  when PR editing is unavailable, then immediately pivot to the next ranked
  route;
- stop cleanly only when runtime, max cycles, global queue exhaustion, or a
  global safety/tooling condition dictates;
- push only dedicated science block branches;
- open or prepare one review PR per science block at block closure;
- never push science work to `main`.

## Stop Conditions

Stop and write a clear `HANDOFF.md` when:

- runtime or max cycles is reached;
- no route in the refreshed opportunity queue passes the dramatic-step gate
  **after** the Deep Work Rules have been satisfied for the active target;
- the worktree changes externally in a way that affects the route;
- the requested target status is honestly achieved and the user did not ask for
  a continuing campaign;
- required core tooling for every viable queued route is unavailable.

Do not stop solely because review-loop finds a blocker, retained certification
fails, PR creation fails, a route ends in no-go/bounded support/support-only
status, a checkpoint is clean, or one lane needs human science judgment.
Demote or backlog that block and pivot.

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
