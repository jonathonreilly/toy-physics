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
2. Before any new work, inspect the latest handoff for an already-launched science child.
   - If the latest handoff names an active log path or active child run, check that path first with `lsof`.
   - If the child is still running, do not start another science step.
   - If the child is still running and the current lock owner is `physics-science`, leave the lock held and exit after refreshing handoff/memory only.
   - If the child finished, treat parsing/finalizing that completed run as this loop's bounded step.
2. Check the cooperative worker lock:
   - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
   - if another live owner holds the lock, stop without doing new work
   - if a live `physics-science` lock already exists, do not treat that as free; reconcile the handoff/active-child state first
   - otherwise acquire it with:
     - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 2`
   - treat the lock as TTL-based shared state, not a process-liveness probe
3. Reconcile git state before new work:
   - `git status --short --branch`
   - `git rev-list --left-right --count origin/main...main` if `origin/main` exists locally
   - `git log --oneline --decorate -n 8`
4. If the repo is already ahead of `origin/main`, attempt to push that work before doing new science with:
   - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
   - if the helper reports a transient network or DNS failure, note it once and avoid piling on extra metadata-only commits
   - if the helper reports auth or non-fast-forward failure, stop and leave the repo for janitor/manual reconciliation
5. If tracked work log, runtime handoff, and memory disagree, reconcile them first from the real repo/log state before new work.

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
- Do not detach a long-running science child and then release the lock.
- If a science child is intentionally left running after the loop ends:
  - keep the `physics-science` lock held
  - do not create a tracked repo commit that treats the run as finished
  - record the in-progress state only in the runtime handoff and automation memory
  - let the next loop resume from that active child instead of starting new work

## State Update Rules
1. Prepend the newest entry to `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md` only for a finished, stable repo-facing result or a real repo-facing integrity fix.
   - Newest entry must be first.
   - Include:
     - current state
     - strongest confirmed conclusion
     - files/logs changed
     - exact next step
     - first concrete action
2. Refresh `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md` as a single latest-entry handoff every loop.
3. Refresh `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` every loop with:
   - run summary
   - strongest conclusion
   - commit state
   - remote sync status if known
   - new log paths
4. If the loop only started or monitored an in-progress child run, do not touch the tracked work log.

## Commit and Push Rules
1. Prefer one clean commit per loop that includes the real science/integrity change plus its README/work-log updates.
2. Do not create metadata-only commits for:
   - push failure status alone
   - lock release status alone
   - “run started” state while a child is still active
3. Push at the end of the loop with:
   - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
4. If push fails:
   - record the helper result once in the work log/handoff/memory,
   - if the only change is runtime handoff or memory, do not create another tracked commit,
   - do not keep emitting repeated “still ahead” commits on later loops,
   - next loop should try to reconcile/push before doing more work.
5. Release the worker lock before ending only if there is no active detached science child:
   - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-science`
