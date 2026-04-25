# Codex Desktop Machine Dump - 2026-04-25

**Capture date:** 2026-04-25

**Tool / model / machine context:** Codex desktop app; local session turn
context records `model: gpt-5.5`, `reasoning_effort: xhigh`, host
`Jonathons-Mac-mini.local`, user path `/Users/jonBridger`.

**Workspace / repo:** `/Users/jonBridger/CI3Z2 Main`;
remote `https://github.com/jonathonreilly/cl3-lattice-framework.git`.

**Scope note:** raw capture for the Codex-desktop side of the methodology
archive. This is machine-local evidence, not synthesis, cleanup, or a
publishable methodology claim.

---

## 1. Local Codex Store Inventory

Observed Codex home:

```text
/Users/jonBridger/.codex
```

Top-level store objects observed during capture:

```text
/Users/jonBridger/.codex/logs_2.sqlite
/Users/jonBridger/.codex/state_5.sqlite
/Users/jonBridger/.codex/session_index.jsonl
/Users/jonBridger/.codex/sessions
/Users/jonBridger/.codex/archived_sessions
/Users/jonBridger/.codex/shell_snapshots
/Users/jonBridger/.codex/rules/default.rules
/Users/jonBridger/.codex/config.toml
/Users/jonBridger/.codex/AGENTS.md
/Users/jonBridger/.codex/skills
/Users/jonBridger/.codex/plugins/cache
/Users/jonBridger/.codex/memories
```

File counts:

```text
find /Users/jonBridger/.codex/sessions -type f -name '*.jsonl' | wc -l
     467

find /Users/jonBridger/.codex/archived_sessions -type f -name '*.jsonl' | wc -l
     169
```

Store sizes:

```text
2.5G    /Users/jonBridger/.codex
532M    /Users/jonBridger/.codex/sessions
791M    /Users/jonBridger/.codex/archived_sessions
```

State/log file sizes:

```text
-rw-r--r--@ 1 jonBridger  staff  1117782016 Apr 25 10:12 /Users/jonBridger/.codex/logs_2.sqlite
-rw-r--r--@ 1 jonBridger  staff       34956 Apr 25 10:07 /Users/jonBridger/.codex/session_index.jsonl
-rw-r--r--@ 1 jonBridger  staff     4018176 Apr 25 10:11 /Users/jonBridger/.codex/state_5.sqlite
```

## 2. Current Session File

The current raw-methodology task was found by searching today's session store
for `raw-methodology-dump`:

```text
/Users/jonBridger/.codex/sessions/2026/04/25/rollout-2026-04-25T10-06-36-019dc4f6-b743-76c3-a978-5eb5ed151fbf.jsonl
```

That JSONL file includes the user prompt that initiated this capture and the
local turn context. The raw file also contains system/developer/tool context,
so this archive records the file path and selected user/task excerpts rather
than copying the full private control context into repo text.

## 3. Active Workspace Status Surface

The task started in a dirty non-main worktree:

```text
cwd: /Users/jonBridger/CI3Z2 Main
branch: claude/source-proximal-symmetric-endpoint-2026-04-24
upstream: origin/claude/source-proximal-symmetric-endpoint-2026-04-24
```

`git status --short --branch` showed one modified backlog file and a large
untracked science batch under `docs/` and `scripts/`. The raw methodology
landing therefore used a separate detached worktree at `origin/main`:

```text
/Users/jonBridger/CI3Z2-methodology-raw-main
detached HEAD: 4da26702 docs: land AI methodology lane
```

This is raw evidence of the repo-hygiene pattern used during the landing: do
not switch or clean a dirty science worktree in place; create an isolated
mainline worktree and land only the selected raw methodology surface.
