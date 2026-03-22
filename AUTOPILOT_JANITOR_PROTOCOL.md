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
   - otherwise acquire it with:
     - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-janitor --purpose "janitor pass" --ttl-hours 1`
3. Reconcile git state:
   - `git status --short --branch`
   - `git rev-list --left-right --count origin/main...main` if `origin/main` exists locally
   - `git log --oneline --decorate -n 8`

## Default Work
1. If the repo is ahead of `origin/main`, try to push before doing anything else with:
   - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
   - if the helper reports a transient network or DNS failure, record it once and stop
   - if the helper reports auth or non-fast-forward failure, stop for manual follow-up
2. If work log, handoff, and memory disagree, repair them from the real repo/log state.
3. If the latest science change touched benchmark code or scripts, run a cheap confidence pass:
   - `python3 scripts/base_confidence_check.py`
4. If the repo is already clean, synced, and state files agree, do not invent extra work. Record that the janitor loop found no cleanup needed.

## Boundaries
- Do not widen science scope.
- Do not start a new benchmark ladder by default.
- Only patch code if the janitor loop finds a real drift/integrity issue.

## State Update Rules
- Append nothing to README unless a correctness or sync conclusion changed.
- If janitor made a real fix, prepend a newest-first entry to `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`.
- Refresh `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md` only if the current top handoff is stale or wrong.
- Refresh `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` with janitor result and sync status.

## Commit and Push Rules
- Prefer one small janitor commit if a real repo-facing fix was needed.
- Push at the end if there was any new local commit or if the repo was ahead, using:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push fails, record the helper result once and stop.
- Release the worker lock before ending:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-janitor`
