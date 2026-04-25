# Claude Prompt Capture

**Capture date:** 2026-04-25

**Tool / model:** Claude Code CLI, model `claude-opus-4-7` (Opus 4.7, 1M
context). Earlier sessions also used Sonnet 4.5/4.6 and Opus 4.6.

**Machine:** macOS, user `jonreilly`. Capture from
`/Users/jonreilly/.claude/projects/`.

**Workspace / repo:** `/Users/jonreilly/Projects/Physics`

**Scope note:** This is a raw evidence pass — direct excerpts of user prompts
that drove the Cl(3)/Z³ work on this machine. No editing, no synthesis. Each
excerpt below is taken verbatim from the local jsonl session store. Prompts
are reproduced exactly as the human typed them, including informal tone,
typos, and shorthand. This complements the earlier
`prompts_session_*.md` extracts (which came from a different machine,
`/Users/jonBridger/Toy Physics/`).

---

## 1. Session jsonl record schema

Each user prompt in `~/.claude/projects/.../*.jsonl` is one line of JSON. The
relevant fields:

```json
{
  "parentUuid": "<parent message uuid>",
  "isSidechain": false,
  "promptId": "<uuid>",
  "type": "user",
  "message": {"role": "user", "content": "<verbatim prompt>"},
  "uuid": "<message uuid>",
  "timestamp": "2026-04-...T...Z",
  "permissionMode": "acceptEdits",
  "userType": "external",
  "entrypoint": "claude-desktop",
  "cwd": "/Users/jonreilly/Projects/Physics/.claude/worktrees/<name>",
  "sessionId": "<uuid>",
  "version": "2.1.X",
  "gitBranch": "claude/<branch>"
}
```

`isSidechain: true` marks a subagent prompt; `agentId` is also present in that
case. Tool-use results are also encoded as `type: "user"` records but with
`message.content` as a `tool_result` array rather than a string.

## 2. Raw prompt excerpts — current session (this capture)

Source:
`-Users-jonreilly-Projects-Physics--claude-worktrees-blissful-tu-ccc1e8/8c1087ee-70f9-443c-8759-108894e8f55e.jsonl`

Initial seed prompt for the current capture (verbatim, lightly truncated for
length):

```text
Work on the raw methodology archive branch, not on main.

Target branch:
- `claude/ai-methodology-capture-2026-04-25`

Goal:
- Add YOUR raw methodology dump to the existing archive.
- This is evidence collection only, not synthesis, not cleanup, not a polished methodology note.

Current archive shape:
- top-level index: `docs/AI_METHODOLOGY_NOTE_[2026-04-25.md](http://2026-04-25.md)`
- raw folder: `docs/ai_methodology/raw/`
- the archive already contains Claude raw captures and one Codex raw capture pass.
- Your job is to append your own raw files in the same spirit.

Rules:
1. Do not touch `main`.
2. Do not curate or consolidate the archive.
3. Raw is good: machine-local paths, direct inventories, raw prompt excerpts, branch/worktree listings, counts, local session-store locations.
4. Keep the new material clearly labeled as your own capture.
5. Update the top-level raw note so it indexes your new files and updates the total file/line count if practical.
6. Use `apply_patch` for manual edits.
7. Commit and push back to `claude/ai-methodology-capture-2026-04-25`.
...
```

This single seed prompt is the entire user steering for this capture pass —
the rest of the session is autonomous execution.

## 3. Raw prompt excerpts — adjacent live worktrees

### 3.1 `claude/crazy-pascal-8623c8` (Planck-derivation worktree)

Source:
`-Users-jonreilly-Projects-Physics--claude-worktrees-crazy-pascal-8623c8/31d6e6cb-31ca-4f6e-9429-ca153d42900e.jsonl`

Verbatim user prompts (sequential, 2026-04-24):

```text
[2026-04-24T00:33:10.544Z]
"if we are able to derive plank natively from the axioms - how big of a deal would that be?"

[2026-04-24T01:10:15.775Z]
"what exactly is hbar?"
```

This is a representative scientific-direction prompt: short, exploratory,
asks the model to evaluate the significance of a derivation route. The full
session expanded from this seed into the Planck-scale program lane.

### 3.2 `claude/romantic-chatterjee-331089` (neutrino mass lane)

Source:
`-Users-jonreilly-Projects-Physics--claude-worktrees-romantic-chatterjee-331089/e9f79d2e-3335-4af6-9d0f-0ad8de9d9c74.jsonl`

Verbatim (2026-04-24):

```text
[2026-04-24T20:51:19.493Z]
"lets work in the absolute v mass delta m2 solar majorana lane - can you sync master and then go get some positive closures at nature grade native axiom level?"

[2026-04-24T21:04:26.007Z]
"put this on a clean branch off main for review"
```

This is a representative lane-direction prompt. It encodes a nontrivial number
of project-internal terms (`absolute v mass`, `delta m2 solar`, `majorana
lane`, `nature grade`, `native axiom`) that only make sense given the rest of
the repo.

### 3.3 `claude/zen-turing-06eeca` (the originating prompt for THIS branch)

Source:
`-Users-jonreilly-Projects-Physics--claude-worktrees-zen-turing-06eeca/*.jsonl`

Verbatim (this is the prompt that *created* the branch this capture lives in):

```text
"make a new \"raw methodology dump\" branch off main, put this instruction in it in a md:
Work on the raw methodology archive branch, not on main.

Target branch:
- `claude/ai-methodology-capture-2026-04-25`

Goal:
- Add YOUR raw methodology dump to the existing archive.
- This is evidence collection only, not synthesis, not cleanup, not a polished methodology note.
..."
```

So the `claude/ai-methodology-capture-2026-04-25` branch was itself
bootstrapped via a Claude session in another worktree, which wrote the
methodology-instruction file as a markdown handoff for the next worker
(this session). That is itself a methodology pattern — a prompt that
materializes the next prompt as a committed file.

### 3.4 Subagent invocation prompt (sample)

Source:
`-Users-jonreilly-Projects-Physics--claude-worktrees-eloquent-bouman/6c2d4f26-0572-472d-b677-0d2009a9bd67/subagents/agent-a8f29e69e17a40387.jsonl`

Verbatim opening of a subagent prompt (`isSidechain: true`):

```text
"I need you to search the framework's derivation atlas and retained docs for
ANY derivation paths or results that could help close this physics gap.
Report back in under 400 words what you find.

**The gap:** I need to derive `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6) =
1/sqrt(2*N_c)` as a purely retained framework result. The Clebsch-Gordan
factor `1/sqrt(6)` is clean from the (1,1)-singlet of the Q_L = (2,3) block.
What I can't derive purely algebraically is the `g_s^1` proportionality —
every path I've tried (HS bosonization, tree-level amplitude matching,
large-N_c meson saturation) introduces a dynamical assumption the reviewer..."
```

This shows the typical Claude-to-subagent dispatch pattern: the parent
session has narrowed the gap and hands the subagent a tightly scoped search
task with an explicit response budget ("under 400 words"). The full subagent
trace is recoverable from the file path above.

## 4. Prompt-volume signal across worktrees

Selected per-worktree session-file sizes (top-level only; subagent files
listed separately in `claude_machine_dump.md` §3):

| Worktree | jsonl size (bytes) | Indicative prompt count |
|---|---:|---:|
| intelligent-jepsen | 30,728,741 | ~1000+ |
| youthful-neumann | 30,084,407 | ~1000+ |
| angry-feynman | 28,119,068 | ~1000+ |
| distracted-napier | 25,166,740 | ~800+ |
| sleepy-cerf | 21,480,344 | ~700+ |
| eloquent-bouman | 10,898,828 | ~400+ |
| upbeat-williamson-a2ff73 | 7,871,636 | ~250+ |
| romantic-chatterjee-331089 | 6,800,253 | ~200+ |
| clever-lewin-1f8af5 | 6,277,924 | ~200+ |

(Indicative counts: the jsonl average per-message size in this codebase
runs roughly 25–40 KB once tool results are included; pure user prompts are
typically a few hundred bytes to a few KB. The "indicative count" column is
a rough rule-of-thumb based on the file size and is *not* a precise tally.)

## 5. Prompt style observations from raw evidence

These notes are descriptive, not prescriptive — they describe the actual prompt
style observed in the raw jsonl, not a recommended pattern.

- Prompts are **terse and shorthand-heavy**. Examples from §3 above:
  `"what exactly is hbar?"`, `"put this on a clean branch off main for
  review"`, `"lets work in the absolute v mass delta m2 solar majorana lane"`.
- Prompts assume **shared context that lives in the repo**, not in the
  prompt itself: phrases like `nature grade native axiom level` and
  `retained framework result` only resolve once the model has read the
  framework-internal `STATUS_VOCABULARY.md`-style notes.
- Prompts often **delegate research direction**, not just code edits:
  `"go get some positive closures"`, `"if we are able to derive plank
  natively"` — the human is steering by lane and grade, not by file.
- Prompts to subagents are **bounded explicitly** in scope and length:
  `"Report back in under 400 words"`, `"search ... for ANY derivation
  paths"`.
- The same human will **fork into a new worktree** to switch context; each
  worktree is a separate jsonl with its own session id, and steering
  prompts in different worktrees address different physics lanes
  concurrently.

## 6. Cross-reference

Earlier prompt-capture files in this archive (different machine, different
window) — not duplicated here:

- `prompts_session_04c820e1.md` — 589 prompts, jonBridger machine, 2026-04-12 → 04-14
- `prompts_session_855ddec4.md` — 220 prompts, jonBridger machine, 2026-04-14 → 04-15
- `prompts_session_67759a49.md` — 53 prompts, jonBridger machine, 2026-04-14 → 04-16
- `prompts_session_small.md` — 5 prompts combined
- `prompts_session_current.md` — 24 prompts, jonBridger machine, 2026-04-25

This file (`claude_prompt_capture.md`) adds raw prompt evidence from the
**`jonreilly` machine**, which runs in parallel to the `jonBridger` machine
and contributes its own Claude session corpus on the same project.
