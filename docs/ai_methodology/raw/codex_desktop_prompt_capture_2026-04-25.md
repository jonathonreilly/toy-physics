# Codex Desktop Prompt Capture - 2026-04-25

**Capture date:** 2026-04-25

**Tool / model / machine context:** Codex desktop app; local session turn
context records `model: gpt-5.5`, host `Jonathons-Mac-mini.local`, user path
`/Users/jonBridger`.

**Workspace / repo:** `/Users/jonBridger/CI3Z2 Main`;
remote `https://github.com/jonathonreilly/cl3-lattice-framework.git`.

**Scope note:** raw prompt/instruction capture for the methodology archive.
This is not synthesis and not a polished methodology note.

---

## 1. Current User Prompt

Session file:

```text
/Users/jonBridger/.codex/sessions/2026/04/25/rollout-2026-04-25T10-06-36-019dc4f6-b743-76c3-a978-5eb5ed151fbf.jsonl
```

Raw environment context at the start of the task:

```text
<environment_context>
  <cwd>/Users/jonBridger/CI3Z2 Main</cwd>
  <shell>zsh</shell>
  <current_date>2026-04-25</current_date>
  <timezone>America/New_York</timezone>
</environment_context>
```

Raw user request:

```text
there is a new claude/raw-methodology-dump branch up on remote - can you find it, read the instruciton md in there, gather all the evidence appropiately and then land only the raw info dump on main appropiately (we are going to use it to build a methodology paper). you can inspect the work already on main to make sure you do this the right way
```

## 2. Remote Instruction Branch Evidence

Fetch discovered the requested branch under a dated name:

```text
* [new branch]        claude/raw-methodology-dump-2026-04-25 -> origin/claude/raw-methodology-dump-2026-04-25
```

Diff against current `origin/main`:

```text
git diff --name-status origin/main...origin/claude/raw-methodology-dump-2026-04-25
A       RAW_METHODOLOGY_DUMP_INSTRUCTION.md
```

Instruction file path read from the remote branch:

```text
origin/claude/raw-methodology-dump-2026-04-25:RAW_METHODOLOGY_DUMP_INSTRUCTION.md
```

Verbatim high-signal excerpt:

```text
Goal:
- Add YOUR raw methodology dump to the existing archive.
- This is evidence collection only, not synthesis, not cleanup, not a polished methodology note.

Current archive shape:
- top-level index: `docs/AI_METHODOLOGY_NOTE_2026-04-25.md`
- raw folder: `docs/ai_methodology/raw/`
- the archive already contains Claude raw captures and one Codex raw capture pass.
- Your job is to append your own raw files in the same spirit.

Minimum content to capture:
- where your local/session data lives
- representative raw prompt/session excerpts
- branch inventory relevant to your workflow
- worktree inventory relevant to your workflow
- review-note / `review.md` / review-packet evidence if present
- repo-hygiene evidence: selective landings, branch naming patterns, recent commit cadence, status-surface cleanup patterns
- exact paths, counts, and excerpts where possible
```

The instruction also said to work on
`claude/ai-methodology-capture-2026-04-25`. The user request for this pass was
different: read that instruction, gather the raw evidence, and land only the
raw information dump on `main`.

## 3. Existing Raw Archive Branch Evidence

The archive branch named by the instruction was already present and had raw
files under `docs/ai_methodology/raw/`:

```text
origin/claude/ai-methodology-capture-2026-04-25
```

Diff against current `origin/main` included:

```text
A       docs/ai_methodology/raw/ai_accountability_note.md
A       docs/ai_methodology/raw/canonical_framing_paragraph.md
A       docs/ai_methodology/raw/claude_machine_dump.md
A       docs/ai_methodology/raw/claude_prompt_capture.md
A       docs/ai_methodology/raw/claude_repo_hygiene.md
A       docs/ai_methodology/raw/claude_review_structure.md
A       docs/ai_methodology/raw/codex_machine_dump.md
A       docs/ai_methodology/raw/codex_prompt_capture.md
A       docs/ai_methodology/raw/codex_repo_hygiene.md
A       docs/ai_methodology/raw/codex_review_structure.md
A       docs/ai_methodology/raw/memory_files.md
A       docs/ai_methodology/raw/prompts_session_04c820e1.md
A       docs/ai_methodology/raw/prompts_session_67759a49.md
A       docs/ai_methodology/raw/prompts_session_855ddec4.md
A       docs/ai_methodology/raw/prompts_session_current.md
A       docs/ai_methodology/raw/prompts_session_small.md
A       docs/ai_methodology/raw/protocols.md
A       docs/ai_methodology/raw/repo_audit.md
A       docs/ai_methodology/raw/science_scaffolding.md
A       docs/ai_methodology/raw/workflow_tooling.md
```

The branch also had `review.md` and a raw front-door methodology note. Those
were intentionally not copied as branch-level surfaces in this landing. The
mainline landing restored only the raw annex files and then added this
current-machine raw Codex-desktop packet.
