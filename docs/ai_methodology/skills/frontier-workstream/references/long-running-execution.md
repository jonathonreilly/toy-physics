# Long-Running Execution

Use this reference when `frontier-workstream` is asked to run unattended.

## Runtime Prompt

If the user did not pass `--runtime`, ask before launch:

```text
How long should this workstream run unattended?
```

Accept compact durations such as `30m`, `2h`, or `6h`. Do not assume a default
runtime for execution. If the user asked only for a plan or status, do not ask.

## Preflight

Before modifying files or running long tasks:

1. Fetch current main: `git fetch origin`.
2. Check `git status --short --branch`.
3. Start from a clean branch off `origin/main`. If the current worktree is
   dirty or contains unrelated work, stop or create a separate clean worktree
   from `origin/main` before launching unattended science.
4. Use a dedicated science branch such as `frontier/<slug>-YYYYMMDD`.
5. Check the cooperative lock if available:
   `python3 scripts/automation_lock.py status`.
6. If the lock is free, acquire it with a TTL that covers the next checkpoint
   window:
   `python3 scripts/automation_lock.py acquire --owner frontier-workstream --purpose "<slug>" --ttl-hours N`.
7. Record start time, runtime, target stop time, branch, and checkpoint interval in
   `STATE.yaml`.

## Checkpoints

Checkpoint:

- after grounding;
- after route selection;
- before and after long scripts;
- after every artifact;
- after every review-loop pass;
- at least once per checkpoint interval;
- before stopping.

Each checkpoint updates `STATE.yaml` and `HANDOFF.md` with:

- current cycle and route;
- files changed;
- commands run and results;
- imports retired/exposed;
- review findings;
- next exact action;
- reason for continuing or stopping.

Refresh the lock before it expires. If the lock cannot be refreshed, stop
cleanly and write a handoff.

## Unattended Decision Policy

Avoid mid-run questions. When a decision is needed:

- choose the narrowest honest claim status;
- prefer no-go/archive/demotion over unsupported promotion;
- choose the highest-scoring route that passes the dramatic-step gate;
- skip ambiguous fixes that need human physics judgment;
- leave clear handoff notes for decisions that require the user.

## Commits And Pushes

Create incremental commits only for coherent science artifacts when the user
requested a run and did not pass `--no-commit`. Use one commit per major cycle.
Do not commit unrelated pre-existing changes.

Science workstream delivery requires pushing the dedicated science branch to
`origin`. Do not open a PR. Do not push to `main`. Do not merge or weave the
science through repo-wide authority surfaces during the workstream run.

If runtime is nearly exhausted and work is not coherent enough to commit, write
the workstream pack and handoff instead of forcing a commit.

## Stop Cleanly

At stop:

1. Run the smallest relevant checks that fit the remaining runtime.
2. Update `REVIEW_HISTORY.md` and `HANDOFF.md`.
3. Commit coherent work if allowed and appropriate.
4. Push the science branch to `origin` if it has commits.
5. Release the lock if held and no child process is running.
6. Report status, branch name, artifacts, remaining blockers, and exact resume
   command.
