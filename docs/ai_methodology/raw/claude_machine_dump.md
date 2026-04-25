# Claude Machine Dump

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7` (Opus 4.7, 1M context)

**Machine context:** macOS Darwin 25.3.0, shell zsh, user `jonreilly`

**Workspace / repo:** `/Users/jonreilly/Projects/Physics` (git worktree
`/Users/jonreilly/Projects/Physics/.claude/worktrees/blissful-tu-ccc1e8` on
branch `claude/ai-methodology-capture-2026-04-25`)

**Claude home:** `/Users/jonreilly/.claude`

**Scope note:** This file is raw machine-side inventory for the Claude/Anthropic
half of the workflow on this specific machine. It is intentionally machine-local
and unsanitized. Not synthesis, not curated narrative — direct evidence only.
This is a separate capture from the earlier Claude session-prompt extracts
(those came from a different machine, `/Users/jonBridger/Toy Physics/`).

---

## 1. Top-level Claude state objects

```text
/Users/jonreilly/.claude/settings.json           1916 bytes  Feb 23 10:11
/Users/jonreilly/.claude/settings.local.json     1510 bytes  Feb 22 07:26
/Users/jonreilly/.claude/stats-cache.json        1736 bytes  Feb 19 14:55
/Users/jonreilly/.claude/history.jsonl         113834 bytes  Feb 23 10:06
```

Top-level subdirectories present (count by file/dir):

```text
/Users/jonreilly/.claude/backups
/Users/jonreilly/.claude/cache
/Users/jonreilly/.claude/commands         (6 user-global slash command files)
/Users/jonreilly/.claude/debug
/Users/jonreilly/.claude/downloads
/Users/jonreilly/.claude/paste-cache
/Users/jonreilly/.claude/plans            (3 plan files)
/Users/jonreilly/.claude/plugins          (3 enabled plugins)
/Users/jonreilly/.claude/projects         (46 project directories, 493 MB)
/Users/jonreilly/.claude/rules            (5 user-global rule files)
/Users/jonreilly/.claude/session-env      (35 session env directories)
/Users/jonreilly/.claude/sessions         (8 KB top-level sessions dir)
/Users/jonreilly/.claude/shell-snapshots
/Users/jonreilly/.claude/skills           (3 skill definitions)
/Users/jonreilly/.claude/statsig
/Users/jonreilly/.claude/telemetry
/Users/jonreilly/.claude/todos            (103 todo files)
```

## 2. Project store inventory

Total `~/.claude/projects/`: **493 MB**, **46 project directories**, **909
session jsonl files** (871 in `subagents/` subdirectories, 38 top-level), with
**37 distinct subagents directories** observed.

Physics-related project directories (count: **34**, first 10 shown):

```text
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-naughty-kowalevski-d14f8c
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-blissful-perlman
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-tender-mendeleev-a4ed81
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-romantic-chatterjee-331089
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-crazy-pascal-8623c8
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-angry-feynman-2df312
/Users/jonreilly/.claude/projects/-Users-jonreilly-projects-Physics--claude-worktrees-angry-chatelet-2dc78c
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-crazy-solomon
/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-intelligent-jepsen
```

Note the path-mangling convention: project directory names are the absolute
working directory with `/` replaced by `-`, including the `.claude/worktrees/`
subpath, so each git worktree gets its own session store.

## 3. Largest session jsonl files

Top 10 largest session files anywhere under `~/.claude/projects/`:

```text
30,728,741  ./-Users-jonreilly-Projects-Physics--claude-worktrees-intelligent-jepsen/1e4222c2-1bcc-46af-9536-a3b29430a56b.jsonl
30,084,407  ./-Users-jonreilly-Projects-Physics--claude-worktrees-youthful-neumann/4ffea772-7b7e-4df9-9f26-b4ca51147e5b.jsonl
28,119,068  ./-Users-jonreilly-Projects-Physics--claude-worktrees-angry-feynman-2df312/596e9a60-99e7-4724-8975-0c08ec8a4a4d.jsonl
25,166,740  ./-Users-jonreilly-Projects-Physics--claude-worktrees-distracted-napier/fe95a681-8d5d-4c1c-85ef-63c6026b68ce.jsonl
21,480,344  ./-Users-jonreilly-Projects-Physics--claude-worktrees-sleepy-cerf/049708ba-932d-481f-969a-04676d577e19.jsonl
20,870,931  ./-Users-jonreilly-Projects-Physics--claude-worktrees-youthful-neumann/4ffea772-7b7e-4df9-9f26-b4ca51147e5b/subagents/agent-acompact-9579826d5705ef24.jsonl
13,501,339  ./-Users-jonreilly-Projects-Physics--claude-worktrees-intelligent-jepsen/1e4222c2-1bcc-46af-9536-a3b29430a56b/subagents/agent-acompact-87cab1d5774665b0.jsonl
10,971,424  ./-Users-jonreilly-Projects-Physics--claude-worktrees-intelligent-jepsen/1e4222c2-1bcc-46af-9536-a3b29430a56b/subagents/agent-acompact-9c27fa20c0701b5d.jsonl
10,898,828  ./-Users-jonreilly-Projects-Physics--claude-worktrees-eloquent-bouman/6c2d4f26-0572-472d-b677-0d2009a9bd67.jsonl
 8,642,622  ./-Users-jonreilly-Projects-Physics--claude-worktrees-sleepy-cerf/049708ba-932d-481f-969a-04676d577e19/subagents/agent-acompact-a2a4dc8be59d7898.jsonl
```

Subagent invocations per worktree (top 10):

```text
217  -Users-jonreilly-Projects-Physics--claude-worktrees-sleepy-cerf
211  -Users-jonreilly-Projects-Physics--claude-worktrees-youthful-neumann
142  -Users-jonreilly-Projects-bridgerapps-AdPrax--claude-worktrees-upbeat-yalow
 68  -Users-jonreilly-Projects-bridgerapps-AdPrax
 45  -Users-jonreilly-Projects-Physics--claude-worktrees-vigilant-turing-e374dd
 38  -Users-jonreilly                                                 (top-level)
 30  -Users-jonreilly-Projects-Physics--claude-worktrees-angry-feynman-2df312
 18  -Users-jonreilly-Projects-bridgerapps-AdPrax--claude-worktrees-vigorous-poincare
 18  -Users-jonreilly-Projects-Physics--claude-worktrees-distracted-napier
 14  -Users-jonreilly-Projects-bridgerapps-AdPrax--claude-worktrees-great-poincare
```

## 4. Memory store on this machine

Path: `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics/memory/`

```text
MEMORY.md
feedback_hostile_review_semantics.md
project_axiom_chain_closure.md
project_brannen_ch_three_gap_closure.md
project_corrected_propagator.md
project_mirror_symmetry_breakthrough.md
```

`MEMORY.md` raw contents (5 entries, 2026-04-25):

```text
- [Corrected propagator](project_corrected_propagator.md) — 1/L^p attenuation enables gravitational attraction; gravity is pure phase effect
- [Mirror symmetry breakthrough](project_mirror_symmetry_breakthrough.md) — Z₂ DAGs break CLT ceiling: pur_cl=0.917 at N=100, decoherence grows
- [Axiom chain closure](project_axiom_chain_closure.md) — Full chain from local growth to physics on 4D grown graphs; gravity 2.0 SE + decoherence
- [Brannen CH three-gap closure](project_brannen_ch_three_gap_closure.md) — 2026-04-22: Gap 1 (Berry=CH), Gap 2 (Ω=1 derived), Gap 3 (operator map) all closed; runner 16/16
- [Hostile review must challenge semantics](feedback_hostile_review_semantics.md) — Trace-ratio derivations can be arithmetically perfect while comparing against convention-defined sources rather than physical couplings; hostile-review passes must stress-test the action-level identification of symbols, not just algebra
```

Note: this `jonreilly` machine's memory store is distinct from the
`jonBridger` memory store referenced in the earlier methodology note section
2.5. Both machines are part of the same author's parallel-investigation setup.

## 5. User-global rules

Path: `/Users/jonreilly/.claude/rules/` (5 files, all loaded as user
instructions on every session):

```text
autonomous-dev.md     7042 bytes  Feb 23 12:27
coding-style.md       7930 bytes  Jan 17 17:42
git-workflow.md       6296 bytes  Jan 17 17:42
performance.md        8014 bytes  Jan 17 17:42
security.md           6271 bytes  Jan 17 17:42
```

These rules govern every Claude session — they appear as
`/Users/jonreilly/.claude/rules/<name>.md` in the per-conversation system
prompt under "user's private global instructions for all projects."

## 6. User-global slash commands

Path: `/Users/jonreilly/.claude/commands/` (6 files):

```text
codemap.md         1063 bytes
rc.md               236 bytes
refactor-clean.md   875 bytes
review.md           887 bytes
tdd.md              759 bytes
verify.md           266 bytes
```

These are global; the **project-level** slash commands at
`/Users/jonreilly/Projects/Physics/.claude/commands/` are a distinct, larger
set (14 physics-specific commands — see `claude_repo_hygiene.md`).

## 7. User-global skills

Path: `/Users/jonreilly/.claude/skills/`:

```text
rigorous-coding/
understand-first/
verify-before-execute/
```

## 8. Active plugins

From `~/.claude/settings.json`:

```json
"enabledPlugins": {
  "sourcekit-lsp": true,
  "code-simplifier@claude-plugins-official": true,
  "ralph-loop@claude-plugins-official": true
}
```

`always thinking enabled: true`. Default permission mode: `acceptEdits`. Two
MCP servers configured (`github`, `memory`).

Plugin marketplaces present:

```text
/Users/jonreilly/.claude/plugins/marketplaces/claude-code-plugins
/Users/jonreilly/.claude/plugins/marketplaces/claude-plugins-official
```

`ralph-loop` plugin contributes the autonomous research loop machinery
referenced in `~/.claude/rules/autonomous-dev.md`.

## 9. Todos and session-env

```text
/Users/jonreilly/.claude/todos/         103 todo files
/Users/jonreilly/.claude/session-env/    35 session env directories
```

## 10. Current session evidence (this capture)

Session directory:
`/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-blissful-tu-ccc1e8/`

```text
8c1087ee-70f9-443c-8759-108894e8f55e.jsonl   241,035 bytes  (start of this raw-capture session)
```

Working directory at session start (raw from jsonl):

```text
"cwd":"/Users/jonreilly/Projects/Physics/.claude/worktrees/blissful-tu-ccc1e8"
"sessionId":"8c1087ee-70f9-443c-8759-108894e8f55e"
"version":"2.1.119"
"gitBranch":"claude/blissful-tu-ccc1e8"
"entrypoint":"claude-desktop"
"permissionMode":"acceptEdits"
```

The session id `8c1087ee-...` is deterministic and embedded in every event
record, so the full session trace is recoverable from the jsonl. Note the
`gitBranch` recorded at session start is `claude/blissful-tu-ccc1e8` — this
branch was checked out to `claude/ai-methodology-capture-2026-04-25` partway
through the session and the change is visible in subsequent events.
