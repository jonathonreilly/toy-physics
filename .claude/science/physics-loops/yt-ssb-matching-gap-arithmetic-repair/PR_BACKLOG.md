# PR Backlog

No PR was opened from this local science-fix worktree.

Recovery commands for a normal GitHub-enabled environment:

```bash
git status --short
python3 scripts/frontier_yt_ssb_matching_gap.py
python3 -m py_compile scripts/frontier_yt_ssb_matching_gap.py
git add docs/YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md \
  docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md \
  docs/YT_RETENTION_LANDING_READINESS_2026-04-18.md \
  scripts/frontier_yt_ssb_matching_gap.py \
  scripts/frontier_yt_retention_landing_readiness.py \
  logs/retained/yt_ssb_matching_gap_2026-04-18.log \
  logs/retained/yt_retention_landing_readiness_2026-04-18.log \
  .claude/science/physics-loops/yt-ssb-matching-gap-arithmetic-repair
git commit -m "Repair YT SSB matching note as scoped H_unit arithmetic"
git push origin HEAD
gh pr create \
  --title "[physics-loop] yt-ssb-matching-gap-arithmetic-repair proposed_retained" \
  --body-file .claude/science/physics-loops/yt-ssb-matching-gap-arithmetic-repair/HANDOFF.md
```
