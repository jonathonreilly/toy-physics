# Claude Session — b6905fe0-246c-4ccd-a177-9b79c7bab138

**Source:** `/Users/jonreilly/.claude/projects/-Users-jonreilly-Projects-Physics--claude-worktrees-zen-turing-06eeca/b6905fe0-246c-4ccd-a177-9b79c7bab138.jsonl`

**Machine:** /Users/jonreilly/  (Claude Code, model claude-opus-4-X / sonnet-4-X)

**Working directory at session start:** `/Users/jonreilly/Projects/Physics/.claude/worktrees/zen-turing-06eeca`

**Git branch at session start:** `claude/zen-turing-06eeca`

**Claude Code version:** `2.1.119`

**Total user prompts captured:** 1

**Time range:** 2026-04-25T13:53:00.635Z → 2026-04-25T13:53:00.635Z

**Scope note:** Verbatim raw extraction of user-typed prompts from this
session jsonl. Subagent dispatches and tool-result records are excluded.
Each prompt below is reproduced exactly as the human typed it.

---

## Prompt 0001 — 2026-04-25T13:53:00.635Z

```
make a new "raw methodology dump" branch off main, put this instruction in it in a md: 
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

What to add:
- Add 2-4 new raw files under `docs/ai_methodology/raw/`, named with your tool/source prefix.
- Good examples:
  - `<tool>_machine_[dump.md](http://dump.md)`
  - `<tool>_prompt_[capture.md](http://capture.md)`
  - `<tool>_review_[structure.md](http://structure.md)`
  - `<tool>_repo_[hygiene.md](http://hygiene.md)`

Minimum content to capture:
- where your local/session data lives
- representative raw prompt/session excerpts
- branch inventory relevant to your workflow
- worktree inventory relevant to your workflow
- review-note / `[review.md](http://review.md)` / review-packet evidence if present
- repo-hygiene evidence: selective landings, branch naming patterns, recent commit cadence, status-surface cleanup patterns
- exact paths, counts, and excerpts where possible

Required header at top of each new raw file:
- capture date
- tool / model / machine context
- workspace/repo
- short scope note saying this is raw capture, not synthesis

Then update:
- `docs/AI_METHODOLOGY_NOTE_[2026-04-25.md](http://2026-04-25.md)`
so it no longer treats your tool as “to be added later”, and so it lists your new raw files in Section 5.

Desired output at the end:
- short summary of what raw files you added
- commit hash
- confirmation that only the methodology-capture branch was changed
```

