# PR Backlog

PR creation was not attempted because the local commit could not be created in
this sandbox. The worktree content is ready, but Git needs write access to the
worktree metadata under `/Users/jonBridger/Toy Physics/.git/worktrees/`.

Recovery commands from an environment with write access to that Git metadata:

```bash
git add docs/RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md \
  scripts/frontier_radial_scaling_protected_angle_narrow.py \
  logs/runner-cache/frontier_radial_scaling_protected_angle_narrow.txt \
  docs/audit/AUDIT_LEDGER.md docs/audit/AUDIT_QUEUE.md \
  docs/audit/data/audit_ledger.json docs/audit/data/audit_queue.json \
  docs/audit/data/auditor_reliability.json \
  docs/audit/data/citation_graph.json \
  docs/audit/data/effective_status_summary.json \
  docs/publication/ci3_z3/DERIVATION_ATLAS_EFFECTIVE_STATUS.md \
  docs/publication/ci3_z3/PUBLICATION_AUDIT_DIVERGENCE.md \
  .claude/science/physics-loops/radial-scaling-t4-domain-20260506
git commit -m "fix: close radial scaling T4 finite tangent domain"
git push origin HEAD
gh pr create --base main --head claude/science-fix/radial_scaling_protected_angle_narrow_theorem_note_2026-05-0-9e374e18 --title "[physics-loop] radial-scaling-t4-domain proposed_retained" --body-file .claude/science/physics-loops/radial-scaling-t4-domain-20260506/PR_BODY.md
```
