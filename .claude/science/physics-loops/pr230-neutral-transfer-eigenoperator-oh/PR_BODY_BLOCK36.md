## Physics-loop block36: source-Higgs / WZ dispatch checkpoint

This updates PR #230 with a branch-local dispatch checkpoint for the neutral
transfer/eigenoperator campaign.

### Block36 result

- Consumes the new lane-1 `O_H` root theorem attempt, top mass-scan response
  harness gate, lane-1 action-premise boundary, higher-shell preflight,
  neutral rank-one bypass boundary, and W/Z mass-response self-normalization
  no-go, plus the higher-shell Schur wave launch as run-control only and the
  HS/logdet scalar-action normalization no-go, then checkpoints the canonical
  `O_H` / source-Higgs route as blocked on the actual current surface.
- Selects strict W/Z accepted-action physical response as the active fallback.
- Keeps W/Z inadmissible until accepted action, production W/Z rows,
  same-source top rows, matched covariance, strict non-observed `g2`,
  `delta_perp`, and final W-response rows are supplied.
- Does not touch or inspect live chunk-worker output.
- Does not authorize retained or `proposed_retained` wording.

### Artifacts

- Runner: `scripts/frontier_yt_pr230_block36_source_higgs_wz_dispatch_checkpoint.py`
- Note: `docs/YT_PR230_BLOCK36_SOURCE_HIGGS_WZ_DISPATCH_CHECKPOINT_NOTE_2026-05-12.md`
- Certificate: `outputs/yt_pr230_block36_source_higgs_wz_dispatch_checkpoint_2026-05-12.json`
- Campaign status: `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`
- Loop pack: `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/`

### Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block36_source_higgs_wz_dispatch_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_block36_source_higgs_wz_dispatch_checkpoint.py
# SUMMARY: PASS=23 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=371 FAIL=0
bash docs/audit/scripts/run_pipeline.sh
# OK, final rerun newly seeded=0, re-audit required=0, 5 known warnings
python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings
```

### Claim boundary

Actual current surface remains open.  The next exact W/Z action is accepted
same-source EW/Higgs action plus production W/Z mass-response rows,
same-source top rows, matched covariance, strict non-observed `g2`,
`delta_perp` authority, and final W-response rows.  Reopen source-Higgs only
with accepted same-surface `O_H`/action plus strict `C_ss/C_sH/C_HH` pole rows.
