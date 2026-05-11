# [physics-loop] PR230 block25 landed checkpoint - open

Block25 is a narrow post-block24 landed checkpoint for draft PR #230.

It verifies that the PR head moved from `82a01735f` to `a864e5fe5` only by the
block24 queue-pivot checkpoint commit.  No new source-Higgs, W/Z, or neutral
H3/H4 production/certificate packet landed, so no ranked route is currently
admitted.

Artifacts:

- `scripts/frontier_yt_pr230_block25_post_block24_landed_checkpoint.py`
- `docs/YT_PR230_BLOCK25_POST_BLOCK24_LANDED_CHECKPOINT_NOTE_2026-05-11.md`
- `outputs/yt_pr230_block25_post_block24_landed_checkpoint_2026-05-11.json`
- `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/HANDOFF.md`

Verification:

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block25_post_block24_landed_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_block25_post_block24_landed_checkpoint.py
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
git diff --check
```

Claim boundary: `proposal_allowed=false`.  This checkpoint does not claim
retained or `proposed_retained` status, does not use forbidden imports, does
not relabel `C_sx/C_xx` as `C_sH/C_HH`, and does not touch or inspect the live
chunk worker.
