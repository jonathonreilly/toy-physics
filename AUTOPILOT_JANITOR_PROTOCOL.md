# Physics Janitor Worker Protocol

This file is the stable operating protocol for the background janitor automation.

## Goal
- Keep the science worker unblocked.
- Reconcile git state, work-log state, handoff state, and automation memory.
- Prefer fixing drift and pushing clean checkpoints over doing new science.

## Preflight
1. Read, in order:
   - `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
   - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md` if it exists
   - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` if it exists
2. Check the cooperative worker lock:
   - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
   - if a live lock is held by another owner, stop instead of mutating shared state
   - if the lock is held by `physics-science`, treat that as an active or recently active science loop and do not “clean up” around it
   - otherwise acquire it with:
     - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-janitor --purpose "janitor pass" --ttl-hours 1`
   - treat the lock as TTL-based shared state; always release it explicitly at the end of the loop
3. Reconcile git state:
   - `git status --short --branch`
   - `git rev-list --left-right --count origin/main...main` if `origin/main` exists locally
   - `git log --oneline --decorate -n 8`

## Default Work
1. If the repo is ahead of `origin/main`, try to push before doing anything else with:
   - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
   - if the helper reports a transient network or DNS failure, record it once and stop
   - if the helper reports auth or non-fast-forward failure, stop for manual follow-up
2. If the latest handoff shows an active science child, do not rewrite tracked state around it; only repair clearly stale lock/sync metadata if needed.
3. If work log, handoff, and memory disagree, repair them from the real repo/log state.
4. If the latest science change touched benchmark code or scripts, run a cheap confidence pass:
   - `python3 scripts/base_confidence_check.py`
5. If the repo is already clean, synced, and state files agree, do not invent extra work. Record that the janitor loop found no cleanup needed.

## Boundaries
- Do not widen science scope.
- Do not start a new benchmark ladder by default.
- Treat sparse sentinels as guardrails, not the main science thread, unless the work log explicitly says the latent/compression thread is closed and a new regime check is needed.
- Only patch code if the janitor loop finds a real drift/integrity issue.

## State Update Rules
- Append nothing to README unless a correctness or sync conclusion changed.
- If janitor made a real repo-facing fix, prepend a newest-first entry to `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`.
- Refresh `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md` only if the current top handoff is stale or wrong.
- Refresh `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` with janitor result and sync status.

## Commit and Push Rules
- Prefer one small janitor commit if a real repo-facing fix was needed.
- Do not create a tracked commit solely to record a push DNS failure or a lock-state correction.
- Push at the end if there was any new local commit or if the repo was ahead, using:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push fails, record the helper result once and stop.
- Release the worker lock before ending:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-janitor`
