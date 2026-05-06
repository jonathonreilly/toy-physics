# PR Backlog

No PR has been opened from this sandboxed science-fix turn.

Recovery commands after verification:

```bash
git checkout -b physics-loop/dm-wilson-schur-feshbach-boundary-block01-20260506
git add docs/DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL_THEOREM_NOTE_2026-04-25.md scripts/frontier_dm_wilson_direct_descendant_schur_feshbach_boundary_variational.py .claude/science/physics-loops/dm-wilson-schur-feshbach-boundary-20260506
git commit -m "physics: close DM Wilson Schur-Feshbach boundary theorem scope"
git push origin physics-loop/dm-wilson-schur-feshbach-boundary-block01-20260506
gh pr create --base main --head physics-loop/dm-wilson-schur-feshbach-boundary-block01-20260506 --title "[physics-loop] dm-wilson-schur-feshbach-boundary proposed_retained" --body-file .claude/science/physics-loops/dm-wilson-schur-feshbach-boundary-20260506/HANDOFF.md
```
