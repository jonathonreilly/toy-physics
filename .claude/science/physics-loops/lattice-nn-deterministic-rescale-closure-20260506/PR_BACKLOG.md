# PR Backlog

No PR was opened from this local science-fix worktree during the missing
derivation closure. If this block needs PR packaging, use:

```bash
git checkout claude/science-fix/lattice_nn_deterministic_rescale_note-9e374e18
git push -u origin claude/science-fix/lattice_nn_deterministic_rescale_note-9e374e18
gh pr create --title "[physics-loop] lattice-nn-deterministic-rescale proposed_retained" --body-file .claude/science/physics-loops/lattice-nn-deterministic-rescale-closure-20260506/HANDOFF.md
```
