# PR Backlog

No PR was opened from this temporary local science-fix worktree.

Recovery commands for a normal networked review lane:

```sh
git checkout -b physics-loop/dm-neutrino-weak-vector-closure-20260506
git add docs/DM_NEUTRINO_WEAK_VECTOR_THEOREM_NOTE_2026-04-15.md \
  scripts/frontier_dm_neutrino_weak_vector_theorem.py \
  outputs/frontier_dm_neutrino_weak_vector_theorem_2026-05-06.txt \
  .claude/science/physics-loops/dm-neutrino-weak-vector-closure-20260506
git commit -m "Close DM neutrino weak-vector derivation packet"
git push origin physics-loop/dm-neutrino-weak-vector-closure-20260506
gh pr create --title "[physics-loop] dm-neutrino-weak-vector exact-support" \
  --body-file .claude/science/physics-loops/dm-neutrino-weak-vector-closure-20260506/HANDOFF.md
```
