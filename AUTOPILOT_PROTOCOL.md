# Physics Science Worker Protocol

This file is the stable operating protocol for the hourly science automation.

## Goal
- Make one bounded, genuine forward step each loop.
- Leave the repo, tracked work log, runtime handoff, and automation memory in a mutually consistent state.
- Prefer a pushed, synced checkpoint over a long chain of local-only metadata commits.

## Preflight
1. Read, in order:
   - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
   - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md` if it exists
   - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` if it exists
2. Reconcile git state before new work:
   - `git status --short --branch`
   - `git rev-list --left-right --count origin/main...main` if `origin/main` exists locally
   - `git log --oneline --decorate -n 8`
3. If the repo is already ahead of `origin/main`, attempt to push that work before doing new science. If push is unavailable, note it and avoid piling on extra metadata-only commits.
4. If tracked work log, runtime handoff, and memory disagree, reconcile them first from the real repo/log state before new work.

## Step Selection
1. Continue the highest-signal unfinished thread from the top work-log entry.
2. Prefer finishing the current thread over widening scope.
3. Do exactly one bounded science or integrity step by default.
4. A second step is allowed only if:
   - the first step finished cleanly,
   - it stays on the same thread,
   - and the second step is the obvious immediate continuation.

## Execution Rules
- Use canonical repo paths only.
- Update `README.md` when a conclusion changes.
- Run cheap audits only when code or benchmark semantics changed.
- Do not create metadata-only commits just to refresh status unless that status is the only unresolved item blocking the next run.

## State Update Rules
1. Prepend the newest entry to `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`.
   - Newest entry must be first.
   - Include:
     - current state
     - strongest confirmed conclusion
     - files/logs changed
     - exact next step
     - first concrete action
2. Refresh `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md` as a single latest-entry handoff.
3. Refresh `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` with:
   - run summary
   - strongest conclusion
   - commit state
   - remote sync status if known
   - new log paths

## Commit and Push Rules
1. Prefer one clean commit per loop that includes the real science/integrity change plus its README/work-log updates.
2. Push at the end of the loop.
3. If push fails:
   - record the failure once in the work log/handoff/memory,
   - do not keep emitting repeated “still ahead” commits on later loops,
   - next loop should try to reconcile/push before doing more work.
