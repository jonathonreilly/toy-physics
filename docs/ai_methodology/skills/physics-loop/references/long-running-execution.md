# Long-Running Execution

Use this reference when `physics-loop` is asked to run unattended.

## Runtime Prompt

If the user did not pass `--runtime`, ask before launch:

```text
How long should this physics loop run unattended?
```

Accept compact durations such as `30m`, `2h`, `6h`, or `12h`. Do not assume a
default runtime for execution. If the user asked only for a plan or status, do
not ask.

## Preflight

Before modifying files or running long tasks:

1. Fetch current main: `git fetch origin`.
2. Check `git status --short --branch`.
3. Start from a clean branch off `origin/main`. If the current worktree is
   dirty or contains unrelated work, stop or create a separate clean worktree
   from `origin/main` before launching unattended science.
4. Use dedicated science block branches such as
   `physics-loop/<slug>-blockNN-YYYYMMDD`.
5. Check the cooperative lock if available:
   `python3 scripts/automation_lock.py status`.
6. If the lock is free, acquire it with a TTL that covers the next checkpoint
   window:
   `python3 scripts/automation_lock.py acquire --owner physics-loop --purpose "<slug>" --ttl-hours N`.
7. Record start time, runtime, target stop time, branch, and checkpoint interval in
   `STATE.yaml`.

## Checkpoints

Checkpoint:

- after grounding;
- after route selection;
- before and after each deep stretch attempt;
- before and after stuck fan-out synthesis;
- before and after long scripts;
- after every artifact;
- after every review-loop pass;
- at least once per checkpoint interval;
- before stopping.

Each checkpoint updates `STATE.yaml` and `HANDOFF.md` with:

- current cycle and route;
- current science block and branch;
- current hard residual, `A_min`, and forbidden imports when in stretch mode;
- files changed;
- commands run and results;
- imports retired/exposed;
- review findings;
- PR status for the block;
- next exact action;
- reason for continuing or stopping.

Refresh the lock before it expires. If the lock cannot be refreshed, stop
cleanly and write a handoff.

## Unattended Decision Policy

Avoid mid-run questions. When a decision is needed:

- choose the narrowest honest claim status;
- prefer no-go/archive/demotion over unsupported promotion, but do not choose
  an easy no-go when a named hard residual has not yet received a stretch
  attempt;
- choose the highest-scoring route that passes the dramatic-step gate;
- after two audit/no-go/blocker cycles in a row, force a stretch attempt from
  minimal premises before more audit cycles;
- before stopping for "no route passes", run or emulate stuck fan-out across
  3-5 orthogonal premises and synthesize the result;
- skip ambiguous fixes that need human physics judgment;
- leave clear handoff notes for decisions that require the user.

## Commits And Pushes

Create incremental commits only for coherent science artifacts when the user
requested a run and did not pass `--no-commit`. Use one branch per science
block when practical, and one or more focused commits inside that branch. Do
not commit unrelated pre-existing changes.

Physics-loop delivery requires pushing each dedicated science block branch to
`origin`. Do not push science to `main`. Do not merge or weave the science
through repo-wide authority surfaces during the loop run.

## Review PR Backlog

At loop end, unless `--no-pr` was supplied:

1. For each coherent science block branch, run the smallest relevant checks
   that fit remaining runtime.
2. Push the branch to `origin`.
3. Open one PR per block with `gh pr create`.
4. Base independent block PRs on `main`; base dependent block PRs on the prior
   block branch and mark them as stacked.
5. Include links to `HANDOFF.md`, `REVIEW_HISTORY.md`, theorem notes, runners,
   logs, verification commands/results, imports retired/exposed, and remaining
   blockers.
6. Label or title the PR for review backlog, e.g.
   `[physics-loop][review-loop] <slug> block NN: <honest status>`.
7. Never merge the PR. The review-loop/backpressure process decides landing.

If `gh` is unavailable or not authenticated, write `PR_BACKLOG.md` with exact
`gh pr create` commands, branch names, bases, titles, and body-file paths. This
is a degraded delivery, not a reason to discard the block.

If runtime is nearly exhausted and work is not coherent enough to commit, write
the loop pack and handoff instead of forcing a commit.

## Stop Cleanly

At stop:

1. Run the smallest relevant checks that fit the remaining runtime.
2. Update `REVIEW_HISTORY.md` and `HANDOFF.md`.
3. Commit coherent work if allowed and appropriate.
4. Push science block branches to `origin` if they have commits.
5. Open or prepare the review PR backlog unless `--no-pr` was supplied.
6. Release the lock if held and no child process is running.
7. Report status, branch/PR names, artifacts, remaining blockers, and exact resume
   command.
