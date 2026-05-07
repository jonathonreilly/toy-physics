# PR Backlog

Block01 PR was opened:

```text
https://github.com/jonathonreilly/cl3-lattice-framework/pull/639
```

Block02 is being integrated directly into draft PR #230 after user direction.
The science packet is already present on the PR #230 head as commit
`6308a320e` (`Add PR230 canonical O_H WZ common action cut`).  No standalone
block02 review PR should be opened unless PR #230 integration fails and the
packet needs separate review.

Block03 follows the same direct PR #230 landing path.  It adds a branch-local
stretch-attempt boundary for the canonical `O_H` / accepted-action root and
pivots the next exact action toward W/Z action-root work.  No standalone
block03 review PR should be opened unless PR #230 integration fails.

Recovery commands if direct PR #230 push or view fails:

```bash
git push origin HEAD:claude/yt-direct-lattice-correlator-2026-04-30
gh pr view 230 --json url,state,isDraft,headRefName
```
