# Physics Summary Worker Protocol

This file is the stable operating protocol for the periodic summary automation.

## Goal
- Produce a concise progress digest every summary cycle.
- Summarize real progress since the last summary, not just restate the latest handoff.

## Inputs
Read, in order:
1. `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
2. `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md` if it exists
3. `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md` if it exists
4. `git log --oneline --decorate -n 20`
5. `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py status`
   - if another live owner holds the lock, skip this cycle rather than competing for shared state
   - otherwise acquire it with:
     - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-summary --purpose "summary pass" --ttl-hours 1`
   - treat the lock as TTL-based shared state; always release it explicitly at the end of the loop

## Output
- Append a timestamped section to:
  - `/Users/jonreilly/Projects/Physics/logs/physics_progress_summary.md`
- Each summary section should include:
  - repo sync status
  - commits since the last summary, grouped into science vs janitor/automation changes
  - strongest current confirmed conclusion
  - current active thread
  - exact next step

## Boundaries
- Do not do new science work.
- Do not change benchmark code unless the summary uncovers a clear reporting inconsistency that must be fixed immediately.
- Do not create a repo commit just to save the summary; keep it as operational output in `logs/`.

## Fallback
- If there were no new commits or no substantive changes since the last summary, write a short “no material change” summary entry instead of repeating the whole history.
- Release the worker lock before ending:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py release --owner physics-summary`
