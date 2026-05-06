# PR Backlog

No PR was opened in this local science-fix worktree.

If a review PR is required after verification:

```bash
git status --short
git checkout -b physics-loop/gauge-wilson-isotropy-boundary-block01-20260506
git add docs/GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md .claude/science/physics-loops/gauge-wilson-isotropy-boundary-20260506
git commit -m "Close Wilson isotropy boundary no-go derivation"
git push -u origin physics-loop/gauge-wilson-isotropy-boundary-block01-20260506
gh pr create --title "[physics-loop] gauge-wilson-isotropy-boundary no-go" --body "See .claude/science/physics-loops/gauge-wilson-isotropy-boundary-20260506/HANDOFF.md"
```
