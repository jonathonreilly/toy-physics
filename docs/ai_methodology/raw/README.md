# AI Methodology Raw Annex

**Capture date:** 2026-04-25

**Scope:** raw evidence annex for the Cl(3)/Z^3 AI-methodology paper lane.
This directory is intentionally machine-local and unsanitized. It is source
material for later grooming, not the methodology paper itself.

Content files in this raw annex, excluding this README:

```text
23 raw content files
42,275 lines
```

## Existing Archive Capture

Imported from `origin/claude/ai-methodology-capture-2026-04-25`:

```text
ai_accountability_note.md
canonical_framing_paragraph.md
claude_machine_dump.md
claude_prompt_capture.md
claude_repo_hygiene.md
claude_review_structure.md
codex_machine_dump.md
codex_prompt_capture.md
codex_repo_hygiene.md
codex_review_structure.md
memory_files.md
prompts_session_04c820e1.md
prompts_session_67759a49.md
prompts_session_855ddec4.md
prompts_session_current.md
prompts_session_small.md
protocols.md
repo_audit.md
science_scaffolding.md
workflow_tooling.md
```

Line count before the current Codex desktop packet:

```text
20 files
41,804 lines
```

## Current Codex Desktop Capture

Added from this Codex desktop session on `/Users/jonBridger`:

```text
codex_desktop_machine_dump_2026-04-25.md
codex_desktop_prompt_capture_2026-04-25.md
codex_desktop_review_hygiene_2026-04-25.md
```

Line count of the current Codex desktop packet:

```text
3 files
471 lines
```

These three files are the current agent's raw dump. They capture:

- local Codex session-store paths and counts;
- the current user prompt and remote instruction excerpt;
- branch and worktree inventories;
- review-packet search output;
- recent `origin/main` landing cadence;
- the selective-landing trace used to keep branch-local instruction/review
  files off the main surface while landing the raw annex.

## Use Boundary

This folder is allowed to contain:

- absolute machine paths;
- raw prompt excerpts;
- branch and worktree listings;
- direct command outputs;
- stale or machine-specific counts.

Later methodology-paper work should normalize, deduplicate, and cite from this
annex rather than treating it as polished prose.
