# Branch / Worktree Cleanup Recommendation — 2026-05-03

**Type:** meta
**Status:** review inventory; cleanup actions NOT executed (require explicit
user confirmation to delete remote refs)

Inventory of remote branches on `origin` produced by
`docs/audit/scripts/inventory_remote_branches.py`. The repo had grown to 433
local branches and 172 remote-tracking refs over time; pruning of merged
upstream branches has reduced the remote count to 72.

## Inventory by category

| category | count | recommended action |
|---|---:|---|
| `protected` (main, audit-lane, etc.) | 1 | KEEP |
| `audit_lane` (audit infrastructure branch) | 1 | KEEP |
| `active_24h` (commits within last 24h) | 26 | KEEP |
| `worktree_or_special` (in active worktree) | 3 | KEEP for now |
| `fully_merged` (merge-base == HEAD on origin/main) | 21 | **safe to archive+delete** |
| `likely_squash_merged` (PR squashed into main) | 8 | **safe to archive+delete** |
| `has_novel_paths` (paths not yet in main) | 12 | per-branch review |

## Safe deletion candidates (29 branches)

These remote branches are either fully merged or likely squash-merged into
`origin/main`. The cleanup tool tags each with `archive/<branch>-<date>` BEFORE
deleting the remote ref, so recovery is one command:

```bash
git checkout -b <name> archive/<name>-2026-05-03
```

### `fully_merged`

- `claude/dm-neutrino-z3-bridge-honest-downgrade-2026-04-27`
- `claude/equivalence-principle-honest-downgrade-2026-04-27`
- `claude/main-20260428`
- `claude/native-gauge-runner-registration-2026-04-27`
- `claude/rconn-derivation-2026-04-27`
- `claude/yt-uv-to-ir-residual-assembly-2026-04-27`
- `cleanup-consolidation-2026-04-27`
- `codex/audit-chain-176-178-20260429`
- `codex/audit-charged-lepton-retirement`
- `codex/review-all-open-prs-20260428`
- `codex/review-charged-lepton-retirement`
- `codex/review-keeper-prs-20260428`
- `codex/review-lane4-neutrino-cascade-20260428`
- `codex/review-neutrino-quantitative-20260428`
- `codex/review-new-open-prs-20260429`
- `codex/review-pr173-20260429`
- `codex/review-pr181-20260429`
- `codex/review-pr182-20260430`
- `codex/review-pr189-20260430`
- `codex/review-pr193-20260430`
- `codex/update-review-loop-audit-compat`

### `likely_squash_merged`

- `claude/dm-neutrino-z3-bridge-character-derivation-2026-04-27`
- `claude/equivalence-principle-action-coupling-derivation-2026-04-27`
- `claude/yt-uv-to-ir-honest-downgrade-2026-04-27`
- `codex/audit-cross-confirm-stale-20260430`
- `codex/audit-re-audit-hubble-lane5-c1-corrected-cl4c`
- `codex/audit-site-phase-crossconfirm-20260430`
- `codex/third-auditor-disagreements-20260430`
- `physics-loop/lane2-atomic-scale-block01-20260428`

## Per-branch review needed (12 branches)

These branches contain commits whose touched paths are not yet in `origin/main`.
Each one is a per-branch decision: salvage the work into a fresh PR, or accept
that the work is abandoned and archive+delete.

- `audit-lane-proposal-scope-aware-classification-20260502`
- `audit/codex-backlog-sweep-2026-04-29`
- `claude/audit-phase4-real-physics-2026-05-01`
- `physics-loop/axiom-first-foundations-block01-20260429`
- `physics-loop/axiom-first-foundations-block02-20260429`
- `physics-loop/axiom-to-main-lane-cascade-20260429-block08-20260429`
- `physics-loop/axiom-to-main-lane-cascade-20260429-block10-20260429`
- `physics-loop/baryon-charge-integrality-block24-20260502`
- `physics-loop/hadron-sqrt-sigma-b2-block01-20260430`
- `physics-loop/hadronic-charges-block23-20260502`
- `physics-loop/lepton-universality-block26-20260502`
- `physics-loop/meson-charges-block25-20260502`

## Recently active (KEEP)

26 branches with commits in the last 24h. Listed
for completeness; cleanup tool already excludes these.

## Recommended execution

To execute the safe cleanup (archive + delete the 28 fully_merged +
likely_squash_merged remote branches):

```bash
# Always re-inventory first:
python3 docs/audit/scripts/inventory_remote_branches.py

# Then dry-run to confirm the plan:
python3 docs/audit/scripts/archive_and_delete_branches.py --dry-run

# Then execute (creates archive tags, then deletes remote branches):
python3 docs/audit/scripts/archive_and_delete_branches.py --execute
```

## Local branch cleanup (not in this inventory)

There are also ~450 LOCAL branches (branches that exist in `.git/refs/heads/`
but no longer track a remote). These accumulate from worktrees and old work.
After remote cleanup lands, they can be pruned with:

```bash
# Show local branches whose remote-tracking ref is gone:
git branch -vv | awk '/: gone]/{print $1}'

# Delete them (review first!):
git branch -vv | awk '/: gone]/{print $1}' | xargs git branch -D
```

## What this PR does

Documents the cleanup plan. **No remote branches deleted, no local branches
pruned.** The audit-data files include the freshly regenerated inventory so the
cleanup tool has accurate input when executed.