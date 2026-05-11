## PR230 Block24 Queue-Pivot Admission Checkpoint

This update adds a branch-local physics-loop checkpoint for the neutral
transfer/eigenoperator campaign.

Block24 verifies the post-block23 PR #230 head:

```text
HEAD = 82a01735f6118dcea381c23c0bc2ff4230cc4e33
subject = Record PR230 block23 remote intake checkpoint
```

The only commit after the last scanned physics head
`0c266edf474e303e85defbd48a13913c910a08ba` is the block23 checkpoint commit.
No new physics packet landed after block23.

### Result

- Source-Higgs queue item is not admitted: accepted same-surface canonical
  `O_H`, production `C_ss/C_sH/C_HH` rows, source-Higgs production certificate,
  combined row packet, Gram/FV/IR authority, and scalar-LSZ authority remain
  absent.
- W/Z queue item is not admitted: accepted action, canonical
  `O_H`/sector-overlap authority, production W/Z rows, same-source top rows,
  matched covariance, strict non-observed `g2`, `delta_perp`, and final
  W-response rows remain absent.
- Neutral H3/H4 queue item is not admitted: physical neutral
  transfer/off-diagonal generator authority and source/canonical-Higgs coupling
  authority remain absent.
- The row stream remains `62/63` with `combined_rows_written=false`.
- Chunk063 completion alone is not closure.

### Files

- `scripts/frontier_yt_pr230_block24_queue_pivot_admission_checkpoint.py`
- `outputs/yt_pr230_block24_queue_pivot_admission_checkpoint_2026-05-11.json`
- `docs/YT_PR230_BLOCK24_QUEUE_PIVOT_ADMISSION_CHECKPOINT_NOTE_2026-05-11.md`
- refreshed campaign status certificate
- loop-pack updates under `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/`

### Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block24_queue_pivot_admission_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_block24_queue_pivot_admission_checkpoint.py
# SUMMARY: PASS=10 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=358 FAIL=0
bash docs/audit/scripts/run_pipeline.sh
# OK, newly seeded=1, re-audit required=0, 5 known warnings
python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings
git diff --check
# OK
```

No retained or `proposed_retained` wording is authorized.  The checkpoint does
not use Ward, `H_unit`, `y_t_bare`, observed targets, observed `g2`,
`alpha_LM`, plaquette, `u0`, unit conventions, W/Z scout promotion, or
`C_sx -> C_sH` aliasing, and it does not touch or inspect the live chunk
worker.
