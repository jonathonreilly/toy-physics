# PR Backlog

PR creation status: blocked before commit.

Blocking command:

```bash
git add docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md scripts/higher_symmetry_gravity_probe.py logs/runner-cache/higher_symmetry_gravity_probe.txt docs/audit/AUDIT_LEDGER.md docs/audit/AUDIT_QUEUE.md docs/audit/data/audit_ledger.json docs/audit/data/audit_queue.json docs/audit/data/auditor_reliability.json docs/audit/data/citation_graph.json docs/audit/data/effective_status_summary.json .claude/science/physics-loops/higher-symmetry-gravity-probe-20260506
```

Observed failure:

```text
fatal: Unable to create '/Users/jonBridger/Toy Physics/.git/worktrees/higher_symmetry_gravity_probe_note-9e374e18/index.lock': Operation not permitted
```

Reason: this worktree's `.git` file points to a gitdir outside the writable
sandbox roots. The source edits remain in the worktree.

Recovery commands:

```bash
git add docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md \
  scripts/higher_symmetry_gravity_probe.py \
  logs/runner-cache/higher_symmetry_gravity_probe.txt \
  docs/audit/AUDIT_LEDGER.md \
  docs/audit/AUDIT_QUEUE.md \
  docs/audit/data/audit_ledger.json \
  docs/audit/data/audit_queue.json \
  docs/audit/data/auditor_reliability.json \
  docs/audit/data/citation_graph.json \
  docs/audit/data/effective_status_summary.json \
  .claude/science/physics-loops/higher-symmetry-gravity-probe-20260506
git commit -m "physics-loop: repair higher symmetry gravity cache"
git push origin claude/science-fix/higher_symmetry_gravity_probe_note-9e374e18
gh pr create \
  --title "[physics-loop] higher-symmetry-gravity-probe-20260506 bounded-support" \
  --body-file .claude/science/physics-loops/higher-symmetry-gravity-probe-20260506/PR_BACKLOG.md
```

Expected PR title:

```text
[physics-loop] higher-symmetry-gravity-probe-20260506 bounded-support
```

Expected head:

```text
claude/science-fix/higher_symmetry_gravity_probe_note-9e374e18
```
