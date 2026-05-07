# PR Backlog

Block01 review PR was created successfully:

https://github.com/jonathonreilly/cl3-lattice-framework/pull/639

Expected recovery command if GitHub PR creation fails:

```bash
git push -u origin physics-loop/pr230-neutral-transfer-eigenoperator-campaign-20260507
gh pr create \
  --base claude/yt-direct-lattice-correlator-2026-04-30 \
  --head physics-loop/pr230-neutral-transfer-eigenoperator-campaign-20260507 \
  --title "[physics-loop] pr230-neutral-transfer-eigenoperator-oh block01 exact negative boundary" \
  --body-file .claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/PR_BODY_BLOCK01.md
```
