# PR Backlog

No PR was opened from this temporary science-fix worktree. The parent
science-fix loop owns delivery. If a standalone PR is needed, use:

```bash
git push origin claude/science-fix/restricted_strong_field_closure_note-f2ee33cc
gh pr create --base main --head claude/science-fix/restricted_strong_field_closure_note-f2ee33cc \
  --title "[physics-loop] restricted-strong-field-closure-note proposed_retained" \
  --body "See docs/RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md and .claude/science/physics-loops/restricted-strong-field-closure-note/HANDOFF.md"
```
