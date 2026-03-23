## 2026-03-23 02:32 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read worklog, handoff, and autopilot memory in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - branch state before science: `main` ahead of `origin/main` by `9` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1040 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1040.txt`
- `1040` completed successfully (`total_elapsed=952.4s`) and introduced one new non-pocket row relative to `1024`/`1008`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the new frontier expansion at `1040`.
- Committed tracked science updates as `527e22b` (`Record nonpocket frontier expansion at variant limit 1040`).
- End-of-loop helper push retry failed again with transient DNS resolution (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), leaving `main` ahead of `origin/main` by `10`.

### Strongest confirmed conclusion
- `976..1024` was a short hold and growth resumes at `1040`:
  - non-pocket overlap-positive rows rise from `30` to `31`;
  - subtype count remains `4`;
  - the only new row is `local-morph-\u0461` (`add1-sensitive`, `neither/dpadj-only`, `cross=Y`);
  - both-sensitive exact-rule anchor is unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `976` was a two-row expansion, `976..1024` held, and `1040` starts the next add1-sensitive growth step.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1040.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1056`) and diff subtype context/rule sections versus `1040` and `1024`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1056 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1056.txt`

## 2026-03-23 01:32 America/New_York

### Current state
- Reconciled protocol preflight in canonical repo context:
  - read worklog, handoff, and autopilot memory in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - branch state before science: `main` ahead of `origin/main` by `8` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1024 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`
- `1024` completed successfully (`total_elapsed=937.1s`) and exactly matched `1008` and `992` subtype membership/exact-rule behavior.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `976..1024` short hold.

### Strongest confirmed conclusion
- `976` remains a two-row bump, not immediate further growth:
  - non-pocket overlap-positive rows remain `30` at `1024` (unchanged vs `1008` and `992`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u0428` and `local-morph-\u0430`;
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `944..960` was a short hold, `976` added two rows, and `976..1024` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1040`) and diff subtype context/rule sections versus `1024` and `1008`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1040 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1040.txt`

## 2026-03-23 00:32 America/New_York

### Current state
- Reconciled preflight first in canonical repo context:
  - read worklog, handoff, and autopilot memory in required order.
  - lock status was free, then acquired via `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-science --purpose "science step" --ttl-hours 6`.
  - branch state before science: `main` ahead of `origin/main` by `6` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1008 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`
- `1008` completed successfully (`total_elapsed=931.7s`) and exactly matched `992` and `976` subtype membership/exact-rule behavior.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `976..1008` short hold.
- Committed tracked science updates as `5b2730f` (`Confirm nonpocket hold through variant limit 1008`).
- End-of-loop helper push retry failed again with transient DNS resolution (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), leaving `main` ahead of `origin/main` by `7`.

### Strongest confirmed conclusion
- `976` remains a two-row bump, not immediate further growth:
  - non-pocket overlap-positive rows remain `30` at `1008` (unchanged vs `992` and `976`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u0428` and `local-morph-\u0430`;
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `944..960` was a short hold, `976` added two rows, and `976..1008` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1024`) and diff subtype context/rule sections versus `1008` and `992`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1024 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1024.txt`

## 2026-03-22 23:36 America/New_York

### Current state
- Ran janitor protocol preflight in canonical repo context (worklog, handoff, and autopilot memory reconciled first).
- Acquired cooperative lock with `python3 /Users/jonreilly/Projects/Physics/scripts/automation_lock.py acquire --owner physics-janitor --purpose "janitor pass" --ttl-hours 1`.
- Re-ran required helper push first:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
  - helper reported transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so janitor stopped science advancement and only repaired state drift.
- Reconciled tracked state mismatch:
  - prior top worklog entry still reported `ahead ... by 4`, while real git state was already one commit further ahead (`4d2d4bb`) from same-loop bookkeeping.
  - refreshed handoff + autopilot memory to match real HEAD/sync condition and preserve correct next action.
- No benchmark or semantics change was introduced in this janitor pass, so no confidence check was required.

### Strongest confirmed conclusion
- Science frontier conclusions are unchanged: `variant_limit=992` still matches `976` (30 non-pocket rows, 4 subtypes, unchanged both-sensitive exact-rule anchor at `deep_overlap_count >= 1.500`).

### Files and results changed in this run
- `/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md`
- `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
- `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`

### Exact next step
- Retry helper push first; if sync is available, continue with one bounded deeper rung at `variant_limit=1008` and compare against `992`/`976`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`

## 2026-03-22 23:31 America/New_York

### Current state
- Reconciled lock + git state first in canonical repo context:
  - lock was free, then acquired via `automation_lock.py acquire --owner physics-science`.
  - branch state before science: `main` ahead of `origin/main` by `2` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- Push helper again returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 992 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`
- `992` completed successfully (`total_elapsed=918.1s`) and exactly matched `976` subtype membership and exact-rule behavior.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `976..992` short hold.
- Committed tracked science updates as `7bc1725` (`Confirm nonpocket hold through variant limit 992`), then committed the final synced status note as `e348e79` (`Record push blockage after variant limit 992 update`).
- End-of-loop helper push retry failed again with transient DNS resolution (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), leaving `main` ahead of `origin/main` by `4`.

### Strongest confirmed conclusion
- `976` is currently a two-row bump, not immediate further growth:
  - non-pocket overlap-positive rows remain `30` at `992` (unchanged vs `976`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u0428` and `local-morph-\u0430`;
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `944..960` was a short hold, `976` added two rows, and `976..992` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 1008`) and diff subtype context/rule sections versus `992` and `976`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 1008 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1008.txt`
## 2026-03-22 22:32 America/New_York

### Current state
- Reconciled lock + git state first in canonical repo context:
  - lock was free, then acquired via `automation_lock.py acquire --owner physics-science`.
  - branch state before science: `main` ahead of `origin/main` by `1` commit (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- Push helper again returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 976 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`
- `976` completed successfully (`total_elapsed=907.6s`) and expanded non-pocket subtype membership relative to `960`/`944`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the new frontier expansion at `976`.

### Strongest confirmed conclusion
- `944..960` was a short hold, and growth resumes at `976` without a subtype-map change:
  - non-pocket overlap-positive rows increase from `28` to `30`;
  - subtype count remains `4`;
  - new rows are `local-morph-\u0428` (`add1-sensitive`, `ge6-only/dpadj-only`) and `local-morph-\u0430` (`add4-sensitive`, `dpadj-only/ge6-only`);
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 992`) and diff subtype context/rule sections versus `976` and `960`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 992 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-992.txt`
## 2026-03-22 21:32 America/New_York

### Current state
- Reconciled lock + git state first in canonical repo context:
  - lock was free, then acquired via `automation_lock.py acquire --owner physics-science`.
  - branch state before science: `main` ahead of `origin/main` by `4` commits (`behind=0`).
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- Push helper again returned transient DNS failure (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so continued with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 960 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`
- `960` completed successfully (`total_elapsed=895.3s`) and exactly matched the `944` subtype membership and exact-rule table.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the newly confirmed `944..960` short hold.

### Strongest confirmed conclusion
- `944` is currently a one-row bump, not immediate further growth:
  - non-pocket overlap-positive rows remain `28` at `960` (unchanged vs `944`);
  - subtype count remains `4`;
  - no new row appears beyond `local-morph-\u040f`;
  - both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- Strongest current frontier read: `896..928` was a `27`-row hold, `944` added one row, and `944..960` is now the next confirmed short hold.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`

### Exact next step
- Retry helper push first; if sync is available, run one deeper rung (`variant_limit = 976`) and diff subtype context/rule sections versus `960` and `944`.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- If push succeeds, then run:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 976 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-976.txt`
## 2026-03-22 20:31 America/New_York

### Current state
- Reconciled git and lock state first in canonical repo context:
  - lock was free, then acquired via `automation_lock.py acquire --owner physics-science`.
  - branch state before science: `main` ahead of `origin/main` by `2` commits.
- Retried required pre-science sync with:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/automation_push.py push-if-ahead --workdir /Users/jonreilly/Projects/Physics`
- Push helper returned transient DNS failure again (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), so proceeded with one bounded same-thread science step.
- Executed one deeper non-pocket subtype rung:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 944 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
- `944` completed successfully (`total_elapsed=886.5s`) and introduced one new non-pocket row relative to `928/912`.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to record the new frontier behavior at `944`.
- Committed tracked science updates as `2a01cd5` (`Record nonpocket frontier expansion at variant limit 944`).
- End-of-loop helper push retry failed again with transient DNS resolution (`failure_kind=dns_failure`, `DNS lookup failed for github.com`, `attempts_used=4`), leaving `main` ahead of `origin/main` by `3`.

### Strongest confirmed conclusion
- `896..928` was a real short stable hold at `27` rows, but `944` starts the next growth phase:
  - non-pocket overlap-positive rows rise from `27` to `28`;
  - the only new row at this rung is `local-morph-\u040f`;
  - subtype count remains `4`;
  - `pair-only-sensitive` expands from `4` to `5` rows;
  - the both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 960`) to determine whether `944` is a one-row bump or the start of another accelerating band.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 960 > /Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-960.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`

## 2026-03-22 19:30 America/New_York

### Current state
- Reconciled the active branch before new work (`main` and `origin/main` were in sync at `47d1113`).
- Continued the active non-pocket subtype frontier thread with one bounded deeper rung in canonical repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 928 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
- Run completed successfully (`total_elapsed=867.8s`).
- `928` exactly matched `912` and `896` for non-pocket subtype membership and the exact-rule table.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to extend the confirmed `27`-row hold through `928`.
- End-of-loop push via `automation_push.py` failed with transient DNS resolution (`failure_kind=dns_failure`, `Could not resolve github.com`), so `main` remains ahead locally.

### Strongest confirmed conclusion
- `896..928` is now a confirmed stable hold at `27` non-pocket overlap-positive rows:
  - no new rows were added at `928` relative to `912/896`;
  - subtype count remains `4`;
  - `pair-only-sensitive` remains at `4` rows;
  - the both-sensitive exact-rule family remains unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-896.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 944`) to test whether the `896..928` stable band persists or the next growth phase resumes.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 944 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-944.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`

## 2026-03-22 19:01 America/New_York

### Current state
- Reconciled the synced `848` frontier first, then continued the active non-pocket subtype thread by executing four deeper rungs in canonical repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 864 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-864.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 880 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-880.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 896 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-896.txt`
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 912 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`
- `864` and `880` exactly matched the `832/848` frontier behavior.
- `896` introduced two new rows, and `912` exactly matched that expanded frontier.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to record the stable `832..880` band and the new `896/912` hold.

### Strongest confirmed conclusion
- `832..880` is now a real stable band:
  - non-pocket overlap-positive rows remain `25` across `832`, `848`, `864`, and `880`;
  - subtype count remains `4`;
  - the both-sensitive exact-rule family stays unchanged and still isolates `2` rows via `deep_overlap_count >= 1.500`.
- `896` and `912` then form the next confirmed hold:
  - non-pocket overlap-positive rows rise from `25` to `27` by adding `local-morph-\u03d4` and `local-morph-\u03d8`;
  - subtype count still remains `4`;
  - `pair-only-sensitive` expands to `4` rows;
  - the both-sensitive exact-rule family remains unchanged.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-864.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-880.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-896.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 928`) to test whether `896/912` is another short stable band or whether the next growth phase resumes immediately.

### First concrete action
- Execute:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 928 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-928.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-912.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-896.txt`

## 2026-03-22 17:30 America/New_York

### Current state
- Resumed the active non-pocket subtype frontier thread and executed one bounded deeper rung in canonical repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 848 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-848.txt`
- Run completed successfully (`total_elapsed=817.7s`).
- Reconciled git before new work and retried push first; push remains unavailable in this environment (`Could not resolve host: github.com`).
- Updated `/Users/jonreilly/Projects/Physics/README.md` to reflect the newly confirmed `832/848` hold.

### Strongest confirmed conclusion
- `848` is an exact replication of the `832` frontier behavior except for the header limit value:
  - non-pocket overlap-positive rows remain `25` (no new rows);
  - subtype count remains `4`;
  - both-sensitive exact-rule family is unchanged and still anchored by `deep_overlap_count >= 1.500` (`2` true positives).
- So `752..832` remains the accelerating growth phase, and `832/848` is now the first confirmed hold at that new `25`-row level.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-848.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`

### Exact next step
- Reconcile/push `main` first, then run one deeper rung (`variant_limit = 864`) to test whether `832/848` is a stable band or the next growth step resumes immediately.

### First concrete action
- Execute:
  - `git -C /Users/jonreilly/Projects/Physics push`
  - If push succeeds:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 864 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-864.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-848.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`

## 2026-03-22 16:30 America/New_York

### Current state
- Resumed the active non-pocket subtype frontier thread and executed one bounded deeper rung in canonical repo context:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 832 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
- Run completed successfully (`total_elapsed=814.3s`) and extended the active growth frontier.
- Updated `/Users/jonreilly/Projects/Physics/README.md` to reflect the new rung and unchanged exact-rule behavior.
- Committed the repo updates locally, but push failed due network/DNS (`Could not resolve host: github.com`), so `main` remains ahead of `origin/main`.

### Strongest confirmed conclusion
- The accelerating non-pocket growth phase continues at `832` rather than settling:
  - non-pocket overlap-positive rows increase from `23` to `25`;
  - two new rows appear: `local-morph-\u0399` (add1-sensitive, `neither/dpadj-only`) and `local-morph-\u03a0` (add4-sensitive, `dpadj-only/neither`);
  - subtype count remains `4`;
  - both-sensitive exact-rule family remains unchanged and still anchored by `deep_overlap_count >= 1.500` (`2` true positives).

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-800.txt`

### Exact next step
- Reconcile/push `main` first, then run one deeper rung (`variant_limit = 848`) to test whether this accelerating phase continues immediately or starts to plateau.

### First concrete action
- Execute:
  - `git -C /Users/jonreilly/Projects/Physics push`
  - If push succeeds:
  - `python3 /Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 848 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-848.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`

## 2026-03-22 15:45 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing three deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 784 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-784.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 800 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-800.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 816 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`
- All three runs completed successfully and each introduced additional non-pocket overlap-positive rows beyond the `752/768` frontier.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to record the accelerating `784..816` growth phase.

### Strongest confirmed conclusion
- The `752/768` expansion did not settle into a stable band. Instead, `784`, `800`, and `816` form a live accelerating growth phase:
  - `784` raises non-pocket overlap-positive rows from `18` to `20` by adding `local-morph-\u036c` and `local-morph-\u036f`;
  - `800` raises them again from `20` to `22` by adding `local-morph-\u0372` and `local-morph-\u037a`;
  - `816` raises them once more from `22` to `23` by adding `local-morph-\u0386`;
  - subtype count still remains `4` throughout.
- The subtype mix also tightened:
  - `pair-only-sensitive` now has `3` rows after `784`;
  - the both-sensitive exact rule family broadens from `1` true positive to `2` at `800` and stays there at `816`, still anchored by `deep_overlap_count >= 1.500`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-784.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-800.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 832`) to test whether this accelerating growth phase continues immediately or finally settles.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 832 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-832.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-816.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-800.txt`

## 2026-03-22 14:14 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing five deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 720 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-720.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 736 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-736.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 752 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-752.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 768 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-768.txt`
- `720` and `736` exactly matched the `688/704` breakpoint band.
- `752` and `768` then each introduced one new row beyond that band.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to record the stable `688..736` band and the new `752/768` growth phase.

### Strongest confirmed conclusion
- The next stable band after `528..672` now runs through `688..736`:
  - non-pocket overlap-positive rows remain `16` across `688`, `704`, `720`, and `736`;
  - subtype count remains `4`;
  - new row `local-morph-\u0310` persists as an add1-sensitive case with response `neither/dpadj-only`;
  - the old exact add1-sensitive rule remains absent from the exact-rule table, while the both-sensitive rule `deep_overlap_count >= 1.500` still holds.
- `752` and `768` then mark the next live growth phase:
  - `752` adds `local-morph-\u034b`, raising non-pocket overlap-positive rows from `16` to `17`;
  - `768` adds `local-morph-\u035b`, raising them again from `17` to `18`;
  - subtype count still remains `4`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-720.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-736.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-752.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-768.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 784`) to test whether the new `752/768` growth phase persists immediately or settles into another stable band.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 784 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-784.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-768.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-752.txt`

## 2026-03-22 13:22 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing four deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 656 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-656.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 672 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-672.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 688 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-688.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 704 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-704.txt`
- The first two runs exactly matched the `528/544/560/576/592/608/624/640` band.
- The next two runs matched each other and introduced the same new row `local-morph-\u0310`.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to extend the stable four-subtype checkpoint through `672` and record the new `688/704` breakpoint.

### Strongest confirmed conclusion
- The four-subtype regime is now stable through `672`:
  - non-pocket overlap-positive rows remain `15` across `528`, `544`, `560`, `576`, `592`, `608`, `624`, `640`, `656`, and `672`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule remains the 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- `688` and `704` then mark the next confirmed breakpoint:
  - non-pocket overlap-positive rows rise from `15` to `16`;
  - new row `local-morph-\u0310` joins as an add1-sensitive case with response `neither/dpadj-only`;
  - subtype count stays `4`;
  - the old exact add1-sensitive rule drops out of the exact-rule table, while the both-sensitive rule `deep_overlap_count >= 1.500` still holds.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-656.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-672.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-688.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-704.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 720`) to test whether the new `688/704` breakpoint persists as a stable band or expands again immediately.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 720 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-720.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-704.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-688.txt`

## 2026-03-22 12:21 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing three deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 608 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-608.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 624 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-624.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 640 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-640.txt`
- All three runs completed successfully and exactly matched the `528/544/560/576/592` band.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to extend the stable four-subtype checkpoint through `640`.

### Strongest confirmed conclusion
- The four-subtype regime is now stable through `640`:
  - non-pocket overlap-positive rows remain `15` across `528`, `544`, `560`, `576`, `592`, `608`, `624`, and `640`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule remains the 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- So `528..640` is now the first stable checkpoint of the new four-subtype regime.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-608.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-624.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-640.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 656`) to test whether the stable four-subtype band persists beyond `640`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 656 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-656.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-640.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-624.txt`

## 2026-03-22 11:25 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 592 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-592.txt`
- The run completed successfully and exactly matched the `528/544/560/576` band.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to extend the stable four-subtype checkpoint through `592`.

### Strongest confirmed conclusion
- The four-subtype regime is now stable through `592`:
  - non-pocket overlap-positive rows remain `15` across `528`, `544`, `560`, `576`, and `592`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule remains the 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- So `528..592` is now the first stable checkpoint of the new four-subtype regime.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-592.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-560.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 608`) to test whether the stable four-subtype band persists beyond `592`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 608 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-608.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-592.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`

## 2026-03-22 11:12 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 576 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`
- The run completed successfully and exactly matched the `528/544/560` band.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to extend the stable four-subtype checkpoint through `576`.

### Strongest confirmed conclusion
- The four-subtype regime is now stable through `576`:
  - non-pocket overlap-positive rows remain `15` across `528`, `544`, `560`, and `576`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule remains the 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- So `528..576` is now the first stable checkpoint of the new four-subtype regime.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-560.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-544.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 592`) to test whether the stable four-subtype band persists beyond `576`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 592 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-592.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-576.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-560.txt`

## 2026-03-22 10:14 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 544 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-544.txt`
- The run completed successfully and exactly matched the `528` rung.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to capture the first stable checkpoint of the four-subtype regime.

### Strongest confirmed conclusion
- The new four-subtype regime is now stable through `544`:
  - non-pocket overlap-positive rows remain `15` across `528` and `544`;
  - subtype count remains `4`;
  - the `pair-only-sensitive` subtype persists with two rows (`local-morph-\u0236`, `local-morph-\u026e`);
  - the exact add1-sensitive rule is now the single 2-term low-degree cut `span_range >= 2.500 and core_low_degree_fraction >= 0.275`.
- So `528/544` is the first stable checkpoint of the new four-subtype regime, not just another moving expansion front.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-544.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-528.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 560`) to test whether the stable four-subtype band persists beyond `544`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 560 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-560.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-544.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-528.txt`

## 2026-03-22 09:53 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 512 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`
- The run completed successfully and extended the new four-subtype regime.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The new four-subtype regime persists and is still actively growing at `512`:
  - non-pocket overlap-positive rows rise from `13` to `14`;
  - subtype count remains `4`;
  - new row: `base:taper-wrap:local-morph-\u025d` (add1-sensitive);
  - the `pair-only-sensitive` fourth subtype persists.
- Exact add1-sensitive rules remain 2-term low-degree-gated cuts, but the strongest exact form has now shifted to rules like `core_low_degree_fraction >= 0.275 and mean_center >= -0.321`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-480.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 528`) to test whether the four-subtype regime continues expanding immediately beyond `512`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 528 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-528.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`

## 2026-03-22 09:43 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing two deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 480 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-480.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 496 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`
- Both runs completed successfully and matched each other exactly.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to capture the new subtype-count regime.

### Strongest confirmed conclusion
- `480/496` marks the start of a new four-subtype regime:
  - non-pocket overlap-positive rows rise from `11` to `13`;
  - subtype count rises from `3` to `4`;
  - new rows include `local-morph-\u0232` and `local-morph-\u0236`;
  - the new fourth subtype is `pair-only-sensitive`, represented by `local-morph-\u0236`.
- The old crossing-based one-term add1 separator is no longer sufficient in this regime. Exact add1-sensitive rules are now low-degree-gated 2-term cuts, such as `pocket_fraction <= 0.128 and core_low_degree_fraction >= 0.275`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-480.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-464.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-448.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 512`) to test whether the new four-subtype regime persists beyond `496`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 512 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-512.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-496.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-480.txt`

## 2026-03-22 08:48 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing three deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 400 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-400.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 416 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-416.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 432 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-432.txt`
- All three runs completed successfully and matched the new `368/384` breakpoint band exactly.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The new add1-sensitive branch growth is now stable through `432`:
  - non-pocket overlap-positive rows remain `9` across `368`, `384`, `400`, `416`, and `432`;
  - subtype count remains `3`;
  - the exact one-term add1-sensitive separator still holds via `crosses_midline = n`, now with `3` true positives and `0` errors.
- So the long `240..352` plateau has given way to a new stable band at `368..432`, and the change is still branch growth inside the existing add1-sensitive non-crossing family rather than a new subtype split.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-400.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-416.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-432.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-384.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 448`) to test whether the new `368..432` stable band still holds.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 448 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-448.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-432.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-416.txt`

## 2026-03-22 07:51 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing two deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 368 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 384 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-384.txt`
- Both runs completed successfully and matched each other exactly.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to capture the first post-`352` breakpoint.

### Strongest confirmed conclusion
- The long `240..352` plateau ends at `368/384` with the first new row after that band:
  - non-pocket overlap-positive rows rise from `8` to `9`;
  - subtype count remains `3`;
  - new row: `base:taper-wrap:local-morph-\u01cd` (add1-sensitive, non-crossing branch);
  - the exact one-term add1-sensitive separator still holds via `crosses_midline = n`, now with `3` true positives and `0` errors.
- So the new growth is inside the existing add1-sensitive non-crossing branch, not a new subtype family.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-384.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 400`) to test whether the new add1-sensitive branch growth persists beyond `384`.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 400 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-400.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-384.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`

## 2026-03-22 07:27 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing one deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 352 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`
- The `352` run completed successfully and exactly matched the existing `288`/`304`/`320`/`336` subtype membership and exact-rule table.
- Tightened hourly automation behavior:
  - added [AUTOPILOT_PROTOCOL.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md)
  - updated `/Users/jonreilly/.codex/automations/physics-autopilot/automation.toml` to require sync reconciliation first, newest-first worklog updates, and one bounded step by default.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The post-`208` add4-sensitive crossing expansion now remains plateaued through `352`:
  - non-pocket overlap-positive rows remain `8`;
  - subtype count remains `3`;
  - the add1-sensitive separator remains exact via `crosses_midline = n` (`2/2`, `0` FP, `0` FN).
- No subtype-membership or exact-rule-table changes appear across `288`, `304`, `320`, `336`, or `352`.
- The automation is now better aligned with this workflow because it will reconcile git/worklog/handoff state before new science work and will prepend the newest work-log entry instead of appending.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
  - [AUTOPILOT_PROTOCOL.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_PROTOCOL.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/automation.toml`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-320.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 368`) to test whether this stabilized `240..352` plateau still holds.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 368 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-368.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`

## 2026-03-22 07:18 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing two deeper rungs in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 320 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-320.txt`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 336 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`
- Both runs completed successfully and matched the existing `288`/`304` outputs exactly.
- Updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to fold the deeper plateau into the tracked science story.

### Strongest confirmed conclusion
- The post-`208` add4-sensitive crossing expansion now remains plateaued through `336`:
  - non-pocket overlap-positive rows remain `8`;
  - subtype count remains `3`;
  - the add1-sensitive separator remains exact via `crosses_midline = n` (`2/2`, `0` FP, `0` FN).
- There were no subtype-membership or exact-rule-table changes across `288`, `304`, `320`, or `336`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-304.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-320.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`

### Exact next step
- Run one deeper rung (`variant_limit = 352`) to test whether this stabilized `240..336` plateau still holds.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 352 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-352.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-336.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-320.txt`

## 2026-03-22 07:16 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by validating and diffing the completed deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 288 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
- Confirmed the `288` run is complete (`total_elapsed=279.9s`) and compared against `272` and `256`; no subtype-membership or exact-rule-table changes were found.
- Updated mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md` to carry conclusions through `288`.
- Ran cheap audit smoke check after updates:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8 > /tmp/2026-03-22-nonpocket-subtype-rules-8-post288-smoke.txt`
  - `real 27.110s`, `user 26.57s`, `sys 0.18s`.

### Strongest confirmed conclusion
- The post-`208` add4-sensitive crossing expansion is still plateaued through `288`:
  - non-pocket overlap-positive rows remain `8` (same as `240`/`256`/`272`);
  - subtype count remains `3`;
  - add1-sensitive separator remains exact via `crosses_midline = n` (`0` FP / `0` FN).
- Diffs versus `272` and `256` are metadata-only (start/end timestamps, elapsed runtime, and `variant_limit`).

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/tmp/2026-03-22-nonpocket-subtype-rules-8-post288-smoke.txt`
- Commit status:
  - Committed in this run: `1c2930c` (`Document nonpocket subtype plateau through variant limit 288`).
  - Push attempt failed in sandbox (`Could not resolve host: github.com`), so remote sync could not be refreshed from this run context.
  - Last known local/remote relation in git metadata: `origin/main...main = 0 behind / 1 ahead`.

### Exact next step
- Run one deeper rung (`variant_limit = 304`) to test whether the `240..288` plateau continues unchanged.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 304 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-304.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`

## 2026-03-22 06:19 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing the queued deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 272 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
- Run completed successfully:
  - `real 258.72s`, `user 258.34s`, `sys 0.27s`.
- Diffed `272` output against `256` and `240`, then updated mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The non-pocket subtype plateau persists through `272`:
  - non-pocket overlap-positive rows remain `8` (same as `240` and `256`);
  - subtype count remains `3`;
  - add1-sensitive separator remains exact via `crosses_midline = n` (`0` FP / `0` FN).
- No subtype-membership or exact-rule-table changes were observed vs `256`/`240` beyond timestamp/runtime lines.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
  - `/tmp/2026-03-22-nonpocket-subtype-rules-8-post272-smoke.txt`
- Commit status:
  - Committed and pushed: `e67a152` (`Document nonpocket subtype plateau through variant limit 272`), `e25c121` (`Sync worklog with pushed 272 plateau commit state`).
  - Repository sync is current at this checkpoint: `main` == `origin/main` at `e25c121`.

### Exact next step
- Run one deeper rung (`variant_limit = 288`) to test whether the `240..272` plateau continues unchanged.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 288 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-288.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`

## 2026-03-22 04:19 America/New_York

### Current state
- Continued the active non-pocket subtype stability thread by executing the queued deeper rung:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 240 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
- Run completed successfully in canonical repo context:
  - `real 234.85s`, `user 234.49s`, `sys 0.25s`.
- Compared `240` output against completed `224` and `208` logs and updated the mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.

### Strongest confirmed conclusion
- The `224` add4-sensitive expansion is persistent and continues at `240`:
  - non-pocket subtype rows increase from `6` to `8` (`224 -> 240`);
  - `local-morph-\u0133` persists;
  - two additional add4-sensitive crossing rows appear: `local-morph-\u014c` and `local-morph-\u014f`.
- Subtype count remains `3` and the add1-sensitive separator remains exact (`crosses_midline = n`, `0` FP / `0` FN).
- Equivalent 2-term add1 rule variants shift at `240` (e.g., shell-deep predicates replace prior core-deep/core-low-degree alternates), but the core subtype split structure is unchanged.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-208.txt`
- Commit status:
  - Pending commit for README + tracking updates in this run.
  - Current local head before committing this run: `676c438`.

### Exact next step
- Run one deeper rung (`variant_limit = 256`) to test whether add4-sensitive crossing expansion continues linearly and whether the add1 exact-rule table remains structurally stable.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 256 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
- Then diff subtype context/rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
## 2026-03-22 03:20 America/New_York

### Current state
- Finished the previously blocked `variant_limit = 224` non-pocket subtype rung after adding per-call projection memoization in `/Users/jonreilly/Projects/Physics/toy_event_physics.py` (`project_metric_rows_and_anchor(...)`, cache keyed by `(metric_row, projection_matrix)`).
- Re-ran cheap audits and confirmed output stability:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8` (`real 25.16s`)
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 32` (`real 45.32s`)
  - diffs vs prior runs are timestamp/elapsed-only.
- Completed the canonical blocked run:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
  - runtime: `real 221.79s`.

### Strongest confirmed conclusion
- The `224` rung is now completed and introduces the first post-`208` non-pocket expansion:
  - non-pocket subtype rows increase from `5` to `6`;
  - new row: `base:taper-wrap:local-morph-\u0133` (add4-sensitive, crossing branch);
  - subtype count remains `3`.
- The add1-sensitive separator remains exact and unchanged (`crosses_midline = n` still isolates `local-morph-\xe7` and `local-morph-\xe9` with `0` FP / `0` FN).
- So the mechanism state updates from “stable through `208`” to “breakpoint at `224` via add4-sensitive branch growth, with core add1 rule intact.”

### Files and results changed in this run
- Code:
  - [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs touched/generated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` (completed run)
  - `/tmp/nonpocket8_after_projection_cache.txt`
  - `/tmp/nonpocket32_after_projection_cache.txt`
- Commit status:
  - Committed and pushed: `676c438` (`Unblock nonpocket 224 rung with projection caching`).
  - Repository sync is current at this checkpoint: `main` == `origin/main` at `676c438`.

### Exact next step
- Determine whether the new `224` add4-sensitive row (`local-morph-\u0133`) persists at the next rung or is transient by running and diffing one deeper rung (`variant_limit = 240`).

### First concrete action
- Run:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 240 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
- Then compare row membership/rule table against:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-208.txt`

## 2026-03-22 02:33 America/New_York

### Current state
- Resumed the same highest-signal blocked rung (`variant_limit = 224` non-pocket subtype-rule stability) and focused on `collect_self_maintenance_candidates(...)` / downstream derived-axis hotspots.
- Landed two runtime-oriented code changes in `/Users/jonreilly/Projects/Physics/toy_event_physics.py`:
  - added per-call seed/result dedup plumbing in `collect_self_maintenance_candidates(...)`:
    - `seen_seed_nodes` guard per interior seed node
    - `emergent_cache` memo keyed by `(seed_nodes, survive_counts, birth_counts)`
  - reduced object churn in `annotate_candidates_with_component_scores(...)` by replacing repeated multi-pass dataclass `replace(...)` calls with single-pass score assignment per candidate.
- Also switched `derive_emergent_persistent_nodes(...)` occupancy accumulation to sparse updates and `.get(..., 0.0)` downstream reads.
- Revalidated behavior with cheap audits (canonical repo):
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8` (`real 26.09s`)
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 32` (`real 47.02s`)
  - Output parity checks vs previous canonical runs were clean (timestamp/elapsed-only diffs).
- Re-ran `variant_limit = 224` multiple times with canonical log redirection; run still did not complete in this cycle.

### Strongest confirmed conclusion
- Mechanism conclusions remain unchanged: non-pocket subtype membership/exact-rule mapping is still fully confirmed only through `variant_limit = 208`.
- Runtime state did improve in where the interrupted `224` run reaches:
  - prior blocked interrupts were in self-maintenance collection / candidate scoring setup;
  - this run reached deeper derived-axis projection code (`project_metric_rows_and_anchor`) before interruption.
- The blocker has shifted downstream, but a fully completed `224` rung is still pending.

### Files and results changed in this run
- Code:
  - [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs touched/generated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` (start marker only; incomplete reruns)
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-nonpocket-subtype-224-interrupt-traces.txt`
  - `/tmp/nonpocket8_after_hotfix.txt`
  - `/tmp/nonpocket32_after_hotfix.txt`
- Commit status:
  - Pending commit in this run for runtime optimizations + tracking updates.
  - Last known relation before this run: `origin/main...main = 0 behind / 6 ahead`.

### Exact next step
- Target the now-dominant derived-axis projection overhead (`project_metric_rows_and_anchor` / projection matrix applications) so a single full `variant_limit = 224` rung can complete.

### First concrete action
- Add a small per-call cache in `project_metric_rows_and_anchor(...)` for repeated row projections keyed by the metric row tuple and projection basis, then rerun:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`

## 2026-03-22 01:26 America/New_York

### Current state
- Continued the same highest-signal blocked rung (`variant_limit = 224` non-pocket subtype-rule stability) and applied targeted runtime reductions in the specificity pipeline path.
- Patched `toy_event_physics.py` to reuse per-graph neighbor adjacency in the self-maintenance search stack:
  - added `build_graph_neighbor_lookup(...)`
  - threaded optional `neighbor_lookup` reuse through `evolve_self_maintaining_pattern`, `derive_emergent_persistent_nodes`, `connected_components`, and `derive_persistence_support`
  - precomputed one lookup per `collect_self_maintenance_candidates(...)` call and reused it across all seed/rule trials.
- Revalidated behavior with smoke runs:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 32`
- Retried `variant_limit = 224` with log redirection to `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`; run still did not complete in this cycle.

### Strongest confirmed conclusion
- Mechanism conclusions remain unchanged: non-pocket subtype membership/exact separators are still fully confirmed through `variant_limit = 208` only.
- The new optimization is materially effective at lower rungs (same outputs, faster runtime):
  - `8`: `35.8s -> 26.6s`
  - `32`: `69.2s -> 48.3s`
- The unresolved `224` blocker remains in the specificity/candidate-pool path; subtype rule search itself is no longer the dominant issue.

### Files and results changed in this run
- Code:
  - [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs touched/generated:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` (start marker only; incomplete rerun)
  - `/tmp/nonpocket8_after.txt` (smoke timing/output check)
  - `/tmp/nonpocket32_after.txt` (smoke timing/output check)
- Commit status:
  - Committed in this run: `d7e7606` (`Cache graph neighbors in self-maintenance candidate search`), `fab9f3f` (`Log neighbor-cache runtime progress for 224 subtype rung`), `766f207` (`Record push-blocked state for neighbor-cache run`), `7a7362e` (`Fix ahead count in latest autopilot worklog entry`), `3f5f31d` (`Sync latest worklog commit list and ahead count`), and `0b374ed` (`Align worklog commit metadata with final local state`).
  - Push attempt failed in sandbox (`Could not resolve host: github.com`), so remote sync could not be refreshed from this run context.
  - Last known local/remote relation in git metadata: `origin/main...main = 0 behind / 6 ahead`.

### Exact next step
- Reduce the remaining `variant_limit = 224` candidate search runtime by pruning repeated seed evaluations in `collect_self_maintenance_candidates(...)` (seed-builder de-dup and/or memoization of per-seed evolution outcomes), then rerun one full `224` rung.

### First concrete action
- Add a per-call memo in `collect_self_maintenance_candidates(...)` keyed by `(seed_nodes, survive_counts, birth_counts)` and skip duplicate seed-builder expansions before `derive_emergent_persistent_nodes(...)`, then run:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`

## 2026-03-22 00:27 America/New_York

### Current state
- Resumed the queued highest-signal mechanism step (`variant_limit = 224` non-pocket subtype-rule stability) and attempted controlled reruns:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
- The `224` rung still did not complete within this run window; interrupt traceback confirms the runtime hotspot is upstream in `pocket_wrap_suppressor_specificity_analysis` (deep candidate-pool/persistence search path), before subtype rule enumeration starts.
- Implemented and validated a rule-search efficiency patch in `scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py` (boundary-only thresholds + deduped bitmask predicate combinations), then smoke-checked at lower limits (`8` and `32`).

### Strongest confirmed conclusion
- Mechanism conclusions remain unchanged: non-pocket subtype membership and exact separators are still only fully confirmed through `variant_limit = 208`.
- The currently confirmed blocker for the `224` rung is not subtype rule combinatorics; it is the expensive overlap/specificity pipeline in `toy_event_physics.py` (`pocket_wrap_suppressor_specificity_analysis` stack).

### Files and results changed in this run
- Code:
  - [scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Attempted (incomplete) log target:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` (start marker only)
- Commit status:
  - Committed and pushed: `04a60a1` (`Speed up nonpocket subtype rule search`), `99f0c73` (`Log 224 subtype runtime blocker and next profiling step`), `8410de1` (`Correct commit sync state in latest worklog entry`).
  - Repository is synced: `main` == `origin/main` at `8410de1`.

### Exact next step
- Isolate and reduce `variant_limit = 224` specificity runtime in `toy_event_physics.py` enough to complete one full non-pocket subtype run, then compare subtype rows/rules against `192/208`.

### First concrete action
- Profile one controlled run with:
  - `python3 -m cProfile -o /Users/jonreilly/Projects/Physics/logs/2026-03-22-nonpocket-subtype-224.profile scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224`
- Then inspect top cumulative hotspots (`pstats`) and patch the highest-cost function in the `pocket_wrap_suppressor_specificity_analysis` path.

## 2026-03-21 23:26 America/New_York

### Current state
- Resumed the queued highest-signal mechanism step (`variant_limit = 224` for non-pocket subtype-rule stability) and launched:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224`
- In this sandbox, long-running non-TTY jobs could not be interrupted or introspected (`ps`/`pkill`/`killall` were blocked), so no completed `224` result was obtained within this run window.
- No code or README conclusions were changed because there is no finished new rung output to justify a mechanism update.

### Strongest confirmed conclusion
- The last fully confirmed mechanism state remains unchanged from the prior completed run: the non-pocket subtype rule map is stable and exact through `variant_limit = 208`.
- A definitive `224` breakpoint/no-breakpoint conclusion is still pending completion of a single successful `224` rung run.

### Files and results changed in this run
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Commit status:
  - Committed and pushed: `905375a` (`Log blocked variant-limit 224 subtype rung attempt`).
  - Repository is synced: `main` == `origin/main` at `905375a`.

### Exact next step
- Complete a single successful `variant_limit = 224` non-pocket subtype-rule rung and compare subtype membership plus exact-rule tables against the completed `192/208` baselines.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224 > /Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt` in a controllable execution mode (interactive/killable), then diff the new log against:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-192.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-208.txt`

# Physics Autopilot Worklog

This is the tracked loop-by-loop status ledger for the Physics autopilot.

Each autopilot run should:
- read this file first
- finish the highest-signal unfinished step before widening scope
- append a new timestamped entry at the top
- keep all paths canonical to this repository, not worktree-local paths

## 2026-03-21 22:56 America/New_York

### Current state
- Implemented and ran the queued non-pocket subtype exact-rule extraction step from the stabilized `176/192` overlap-context thread.
- Added helper:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit <N>`
- Executed and logged both planned rungs:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 192`
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 208`
- Updated README mechanism notes with the new rule-level result.

### Strongest confirmed conclusion
- Non-pocket overlap-positive membership and subtype behavior are unchanged between `192` and `208` (same `5` rows and same `3` suppressor-response subtypes).
- The add1-sensitive subtype (`local-morph-\\xe7`, `local-morph-\\xe9`) is exactly isolated by compact one-feature rules (`crosses_midline = n`, or equivalently `center_total_variation <= 2.500`).
- The crossing rows split exactly by overlap multiplicity: `deep_overlap_count = 2` isolates the single both-sensitive row (`local-morph-v`), while `crosses_midline = Y` with `deep_overlap_count = 1` isolates the add4-sensitive pair (`local-morph-\\x8e`, `local-morph-\\u0103`).
- So through `208`, the non-pocket branch is now rule-level explicit, not just qualitatively multi-subtype.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Added helper:
  - `/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-192.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-nonpocket-subtype-rules-208.txt`
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Commit status:
  - Committed and pushed: `a420284` (`Extract stable non-pocket subtype rules through variant limit 208`).

### Exact next step
- Stress-test whether the same non-pocket subtype rule map remains exact at the next ladder rung and detect the first rung where subtype membership or exact separators change.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 224` and compare subtype rows plus exact-rule table against the `192/208` logs.

## 2026-03-21 21:14 America/New_York

### Current state
- Resumed the pending non-pocket subtype step from the `176/192` overlap-context thread and ran the queued focused compare at `variant_limit = 192`:
  - `python3 scripts/pocket_wrap_suppressor_pair_kill_row_compare.py --variant-limit 192 --targets 'local-morph-v' 'local-morph-\\x8e' 'local-morph-\\xe7' 'local-morph-\\xe9' 'local-morph-\\u0103'`
- Updated README mechanism language with the new subtype split interpretation from that compare.

### Strongest confirmed conclusion
- The broadened non-pocket branch is not one coherent subtype.
- `local-morph-\\xe7` and `local-morph-\\xe9` form a matched non-crossing branch (`crosses_midline = n`) that flips only when `(1,0)` is added (`add1 -> ge6-only`, `add4 -> dpadj-only`).
- `local-morph-\\u0103` instead aligns with the crossing branch (`crosses_midline = Y`) and flips on `(4,0)` (`add4 -> ge6-only`, `add1 -> dpadj-only`).
- So within the same overlap-trigger family, the newly added rows already split into at least two suppressor-response subtypes.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-pair-kill-row-compare-192-nonpocket.txt`
- Commit status:
  - Committed and pushed: `b7c0ce2` (`Document non-pocket suppressor subtypes at variant limit 192`).
  - `main` now matches `origin/main` at `b7c0ce2`.

### Exact next step
- Convert the non-pocket subtype split from qualitative to exact-rule form on the stabilized `192` family, then check whether that rule remains exact at `variant_limit = 208`.

### First concrete action
- Add a small helper script that labels non-pocket overlap-positive rows by suppressor-response subtype at `variant_limit = 192` and performs a one/two-feature threshold search for `0` FP / `0` FN separators, then rerun at `208`.

## 2026-03-21 20:59 America/New_York

### Current state
- Continued the overlap-context ladder through the next two queued rungs:
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 176`
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 192`
- No new helper code was needed in this pass; this was a pure ladder-extension and interpretation step.

### Strongest confirmed conclusion
- `176` adds one more non-pocket overlap-positive row: `local-morph-\\u0103`.
- `192` is identical to `176`, so the broadened overlap-positive family appears stable at least through `192`.
- Current stabilized family through `192`:
  - pocket-signature rows: `local-morph-a`, `local-morph-\\xf6`
  - non-pocket rows: `local-morph-v`, `local-morph-\\x8e`, `local-morph-\\xe7`, `local-morph-\\xe9`, `local-morph-\\u0103`
- The robust exact one-feature separators in that stabilized band are still:
  - `boundary_roughness <= 0.288`
  - `pocket_fraction <= 0.081`
- So the current best read is that the broadened family is real, but the pocket-signature subset remains a compact low-roughness / low-pocket-fraction edge of the same overwrite-trigger family.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-176.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-192.txt`

### Exact next step
- Explain the new stabilized non-pocket branch internally: identify whether the added rows `\\xe7`, `\\xe9`, and `\\u0103` split into one coherent non-pocket subtype or multiple subtypes under the same overwrite trigger.

### First concrete action
- Run a focused row compare at `variant_limit = 192` for `local-morph-v`, `local-morph-\\x8e`, `local-morph-\\xe7`, `local-morph-\\xe9`, and `local-morph-\\u0103`, then search for small exact predicates that separate those non-pocket rows into stable subgroups.

## 2026-03-21 20:15 America/New_York

### Current state
- `main` started this run at `1572d7d` with a local uncommitted `AUTOPILOT_WORKLOG.md` status edit.
- Continued the same pocket-wrap suppressor overlap-context mechanism thread and executed the queued deeper rung:
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 128`
- The `128` rung completed successfully and produced the expected overlap-context/rule table log (`total_elapsed=421.9s`).
- Updated README mechanism language to include the `128` rung stability result.

### Strongest confirmed conclusion
- Overlap-positive membership still does not expand at `variant_limit = 128`; it remains exactly `local-morph-a`, `local-morph-v`, and `local-morph-\x8e`.
- The same shell/profile separators remain exact one rung deeper: `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` still isolate the canonical pocket-signature branch with `0` FP and `0` FN.
- The mechanism read is unchanged but now verified through `128`: `local-morph-a` remains the low-roughness, low-total-variation, shell-pocket-saturated tip of the same coordinate-exact overwrite-trigger family.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-128.txt`
- Commit status:
  - Committed and pushed: `5b8fb7c` (`Validate overlap-context separators through variant limit 128`).
  - `main` now matches `origin/main` at `5b8fb7c`.

### Exact next step
- Probe the next deeper ladder rung to find the first point where overlap-positive membership changes or exact one-feature separator behavior degrades.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 144`, then check whether overlap-positive rows remain `3` and whether `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` remain `0` FP / `0` FN.

## 2026-03-21 19:18 America/New_York

### Current state
- `main` started this run at `b914026` with local uncommitted `README.md` and `AUTOPILOT_WORKLOG.md` edits from the prior `96` rung documentation pass.
- Continued the same pocket-wrap suppressor overlap-context mechanism thread and executed the planned deeper rung:
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 112`
- The `112` rung completed successfully and produced the expected overlap-context/rule table log (`total_elapsed=371.6s`).
- Updated README mechanism language to include the `112` rung stability result.

### Strongest confirmed conclusion
- Overlap-positive membership still does not expand at `variant_limit = 112`; it remains exactly `local-morph-a`, `local-morph-v`, and `local-morph-\\x8e`.
- The shell/profile separators remain exact one rung deeper: `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` still isolate the canonical pocket-signature branch with `0` FP and `0` FN.
- The strongest mechanism read is unchanged but now verified through `112`: `local-morph-a` remains the low-roughness, low-total-variation, shell-pocket-saturated tip of the same coordinate-exact overwrite-trigger family.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-112.txt`
- Commit status:
  - Committed and pushed: `1572d7d` (`Validate overlap-context separators through variant limit 112`).
  - `main` now matches `origin/main` at `1572d7d`.

### Exact next step
- Probe the next deeper ladder rung to find the first point where overlap-positive membership changes or exact one-feature separator behavior degrades.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 128`, then check whether overlap-positive rows remain `3` and whether `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` remain `0` FP / `0` FN.

## 2026-03-21 20:33 America/New_York

### Current state
- Continued the same pocket-wrap suppressor overlap-context mechanism ladder and executed three deeper rungs:
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 128`
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 144`
  - `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 160`
- Added one focused follow-up compare at the first broadened pocket-signature rung:
  - `python3 scripts/pocket_wrap_suppressor_pair_kill_row_compare.py --variant-limit 160 --targets local-morph-a local-morph-v local-morph-\\x8e local-morph-\\xf6`

### Strongest confirmed conclusion
- `128` stays identical to the earlier ladder: still exactly `3` overlap-positive rows and the same exact one-feature separators.
- `144` is the first real breakpoint:
  - overlap-positive membership expands from `3` to `5`
  - two new non-pocket rows appear: `local-morph-\\xe7`, `local-morph-\\xe9`
  - the exact one-feature separator set shrinks from three older favorites to a different surviving pair/core, especially `boundary_roughness <= 0.288` and `pocket_fraction <= 0.081`
- `160` adds the first second pocket-signature row:
  - new row: `local-morph-\\xf6`
  - pocket-signature branch broadens from `1` to `2`
  - exact one-feature separators still exist, but the robust ones are now `boundary_roughness <= 0.288` and `pocket_fraction <= 0.081`
- The 160 row compare shows `local-morph-\\xf6` is not a different trigger. It is another anti-deep pocket branch of the same overwrite family, but even more compact than `local-morph-a`: lower roughness (`0.244`), lower total variation (`1.00`), no crossing, span `2`, and only one overlapping suppressor/deep coordinate `(4,0)`.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-128.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-144.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-160.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-row-compare-160.txt`

### Exact next step
- Determine whether the new `144/160` rows are the start of a stable broadened family or just a sparse transient band, and whether `boundary_roughness <= 0.288` plus `pocket_fraction <= 0.081` remains the right compact separator pair above `160`.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 176` and `--variant-limit 192`, then check:
  - whether overlap-positive membership expands again
  - whether pocket-signature membership stays at `2`
  - whether `boundary_roughness <= 0.288` and `pocket_fraction <= 0.081` remain exact one-feature separators.

## 2026-03-21 18:09 America/New_York

### Current state
- `main` started this run at `b914026` with a local uncommitted worklog edit.
- Continued the same pocket-wrap suppressor overlap-context mechanism thread and executed the planned deeper rung:
  - `scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 96`
- The `96` rung completed and produced the expected overlap-context/rule table log.
- Updated README mechanism language to include the `96` rung stability result.

### Strongest confirmed conclusion
- Overlap-positive membership did not expand at `variant_limit = 96`; it is still exactly the same three rows (`local-morph-a`, `local-morph-v`, `local-morph-\x8e`).
- The shell/profile separators remain exact at this deeper rung: `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` still isolate the canonical pocket-signature branch with `0` FP and `0` FN.
- So the strongest mechanism read is unchanged but now verified one rung deeper: `local-morph-a` remains the low-roughness, low-total-variation, shell-pocket-saturated tip of the same coordinate-exact overwrite-trigger family.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New log:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-96.txt`
- Commit status:
  - Pending in working tree (not committed yet in this run).

### Exact next step
- Probe the next deeper ladder rung to find the first point where overlap-positive membership or exact separator behavior changes.

### First concrete action
- Run `python3 scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 112` and check whether overlap-positive rows stay at `3` and whether the same one-feature exact separators remain `0` FP / `0` FN.

## 2026-03-21 17:12 America/New_York

### Current state
- `main` was synced to `origin/main` at run start; this loop continued the same pocket-wrap suppressor overlap-context mechanism thread.
- Executed the pending deeper overlap-context rule sweeps at:
  - `variant_limit = 72`
  - `variant_limit = 80`
- Both runs produced the same three overlap-positive rows and the same exact-rule counts as the `64` rung.
- Updated README mechanism language to mark those shell/profile separators as stable across `64/72/80`.

### Strongest confirmed conclusion
- The pocket-wrap suppressor split is still a single overwrite-trigger family, and the canonical pocket-signature branch remains exactly separable by shell/profile context alone.
- The one-feature separators `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, and `shell_pocket_fraction >= 0.812` now hold exactly (`0` FP, `0` FN) not only at `64` but also at `72` and `80`.

### Files and results changed in this run
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-72.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-80.txt`
- Commit status:
  - Committed and pushed: `b914026` (`Validate overlap-context separators through variant limit 80`).
  - `main` now matches `origin/main` at `b914026`.

### Exact next step
- Probe the first deeper rung where overlap-positive membership might change, then re-check whether the same exact shell/profile separators survive that membership expansion.

### First concrete action
- Run `scripts/pocket_wrap_suppressor_overlap_context_rules.py --variant-limit 96`, inspect whether any new overlap-positive row appears, and if yes, recompute which one-feature separators remain exact.

## 2026-03-21 16:53 America/New_York

### Current state
- `main` is now synced to `origin/main`.
- This loop reconciled and pushed the previously local suppressor-context commits:
  - `1efe351` `Compare suppressor pair-kill rows by context`
  - `4497b08` `Update autopilot worklog with commit status`
  - `b126b11` `Isolate pocket-wrap overlap-context separators`
- The active mechanism thread is still the pocket-wrap suppressor specificity line inside `base:taper-wrap` `local-morph`.
- Added a new overlap-context rule runner:
  - [scripts/pocket_wrap_suppressor_overlap_context_rules.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_overlap_context_rules.py)
- Logged the `variant_limit = 64` overlap-context sweep to:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-64.txt`

### Strongest confirmed conclusion
- Pair-kill is still the same coordinate-exact deep-support overwrite mechanism across all overlap-positive rows.
- The pocket-signature branch (`local-morph-a`) is not separated from the non-pocket overlap-positive rows by the overwrite trigger itself, but by broader shell/profile context.
- On the current `variant_limit = 64` overlap-positive set, exact one-feature separators already exist in shell/profile space alone:
  - `boundary_roughness <= 0.288`
  - `center_total_variation <= 2.500`
  - `shell_pocket_fraction >= 0.812`
- So the clean current read is: `local-morph-a` is the low-roughness, low-total-variation, shell-pocket-saturated tip of the same overwrite-trigger family, while `local-morph-v` and `local-morph-\x8e` are rougher or more internally varied contexts of that same mechanism.

### Files and results changed in this run
- Code:
  - [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
  - [scripts/pocket_wrap_suppressor_overlap_context_rules.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_overlap_context_rules.py)
- Updated narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Pushed commits:
  - `1efe351`
  - `4497b08`
  - `b126b11`
- New logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-row-compare-64.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-overlap-context-rules-64.txt`

### Exact next step
- Test whether those exact shell/profile separators survive a deeper local-morph ladder, rather than only the current `variant_limit = 64` overlap-positive set.

### First concrete action
- Sweep the overlap-context rule analysis at `variant_limit = 72` and `80`, then check whether `boundary_roughness <= 0.288`, `center_total_variation <= 2.500`, or `shell_pocket_fraction >= 0.812` remain exact separators of the pocket-signature branch.

## 2026-03-21 16:18 America/New_York

### Current state
- `main` is synced to `origin/main` at commit `57be550`.
- The active mechanism thread is the pocket-wrap suppressor specificity line inside `base:taper-wrap` `local-morph`.
- The repo now contains suppressor coverage, injection, and specificity helpers plus deeper ladder sweeps through `variant_limit = 64`, along with a focused pair-kill diagnostic runner.

### Strongest confirmed conclusion
- The paired suppressors `(1,0)` and `(4,0)` are not a generic kill switch. On the tested `40/48/56` local-morph ladders, pair-kill occurs exactly when the added suppressor nodes overwrite active deep support.
- Full two-cell overlap is sufficient but not necessary: one deeper partial-overlap row appears by `variant_limit = 48`, so the tighter current rule is `deep_overlap_count > 0 => pair_kill` on the tested ladder.
- The focused pair-kill diagnostic confirms that this is coordinate-exact rather than just count-based: at `variant_limit = 56` and `64`, the kill coordinates match the overlapping deep-support coordinates for all `3/3` pair-kill rows, including the partial-overlap row `local-morph-\x8e`.

### Files and results already documented
- Narrative conclusions: [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Model/helper implementation: [toy_event_physics.py](/Users/jonreilly/Projects/Physics/toy_event_physics.py)
- Current suppressor runners:
  - [scripts/pocket_wrap_suppressor_coverage.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_coverage.py)
  - [scripts/pocket_wrap_suppressor_coverage_sweep.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_coverage_sweep.py)
  - [scripts/pocket_wrap_suppressor_injection.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_injection.py)
  - [scripts/pocket_wrap_suppressor_specificity.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_specificity.py)
  - [scripts/pocket_wrap_suppressor_specificity_sweep.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_specificity_sweep.py)
  - [scripts/pocket_wrap_suppressor_pair_kill_diagnostic.py](/Users/jonreilly/Projects/Physics/scripts/pocket_wrap_suppressor_pair_kill_diagnostic.py)
- Latest logs:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-diagnostic-56.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-21-pocket-wrap-suppressor-pair-kill-diagnostic-64.txt`

### Exact next step
- Compare the non-pocket pair-kill rows (`local-morph-v` and `local-morph-\x8e`) against canonical `local-morph-a` to isolate what changes the route from pocket-signature to non-pocket while keeping the same deep-support overwrite mechanism.

### First concrete action
- Diff the baseline deep/pocket/low gaps and candidate-cell sets for `local-morph-a`, `local-morph-v`, and `local-morph-\x8e`, then check whether the non-pocket rows are missing only pocket signal or a larger shell/context property.

## 2026-03-22 05:19 America/New_York

### Current state
- Resumed the active non-pocket subtype stability thread and executed the queued deeper rung in canonical repo context:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 256 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
- Run completed successfully:
  - `real 246.81s`, `user 246.46s`, `sys 0.25s`.
- Compared `256` against `240`/`224` and updated mechanism narrative in `/Users/jonreilly/Projects/Physics/README.md`.
- Ran a cheap audit smoke check after updates:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 8 > /tmp/2026-03-22-nonpocket-subtype-rules-8-post256-smoke.txt`
  - `real 24.51s`, `user 24.40s`, `sys 0.03s`.

### Strongest confirmed conclusion
- The post-`208` add4-sensitive crossing expansion does not extend immediately at `256`:
  - non-pocket subtype rows are unchanged from `240` (`8` rows, subtype count `3`);
  - add1-sensitive separation remains exact via `crosses_midline = n` (`2/2`, `0` FP, `0` FN);
  - `256` and `240` differ only in run metadata (`variant_limit`/timestamps/elapsed).
- The strongest mechanism read is now: expansion occurred at `224/240`, then stabilized through at least `256`.

### Files and results changed in this run
- Narrative:
  - [README.md](/Users/jonreilly/Projects/Physics/README.md)
- Updated run tracking:
  - [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
  - `/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md`
  - `/Users/jonreilly/.codex/automations/physics-autopilot/memory.md`
- Logs generated/used:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-224.txt`
  - `/tmp/2026-03-22-nonpocket-subtype-rules-8-post256-smoke.txt`
- Commit status:
  - Committed and pushed: `5a29129` (`Document nonpocket subtype plateau through variant limit 256`).
  - Repository sync at end of run: `main` == `origin/main` at `5a29129`.

### Exact next step
- Run one deeper rung (`variant_limit = 272`) to test whether the add4-sensitive crossing branch remains plateaued after the `256` hold or resumes growth.

### First concrete action
- Execute:
  - `python3 scripts/pocket_wrap_suppressor_nonpocket_subtype_rules.py --variant-limit 272 > /Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-272.txt`
- Then diff subtype context/exact-rule sections versus:
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-256.txt`
  - `/Users/jonreilly/Projects/Physics/logs/2026-03-22-pocket-wrap-suppressor-nonpocket-subtype-rules-240.txt`
