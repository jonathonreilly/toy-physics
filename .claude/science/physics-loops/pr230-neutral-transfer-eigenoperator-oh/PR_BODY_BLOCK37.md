## Physics-loop block37: post-block36 supervisor-yield checkpoint

This updates PR #230 with a branch-local supervisor-yield checkpoint for the
neutral transfer/eigenoperator campaign.

### Block37 result

- Consumes the post-block36 FH-LSZ full-set support commit plus native
  scalar/action/LSZ and W/Z absolute-authority route-exhaustion boundaries as
  support/no-go inputs only.
- Keeps the canonical `O_H` / source-Higgs route blocked until accepted
  same-surface `O_H`/action plus strict `C_ss/C_sH/C_HH` pole rows with
  Gram/FV/IR authority are supplied.
- Keeps W/Z selected as active fallback but blocked until accepted action,
  production W/Z mass-response rows, same-source top rows, matched covariance,
  strict non-observed `g2`, `delta_perp`, and final W-response rows are
  supplied.
- Keeps neutral H3/H4 blocked without physical transfer/off-diagonal dynamics
  plus source/canonical-Higgs coupling authority.
- Does not touch or inspect live chunk-worker output.
- Does not authorize retained or `proposed_retained` wording.

### Artifacts

- Runner: `scripts/frontier_yt_pr230_block37_post_block36_supervisor_yield_checkpoint.py`
- Note: `docs/YT_PR230_BLOCK37_POST_BLOCK36_SUPERVISOR_YIELD_CHECKPOINT_NOTE_2026-05-12.md`
- Certificate: `outputs/yt_pr230_block37_post_block36_supervisor_yield_checkpoint_2026-05-12.json`
- Campaign status: `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`
- Loop pack: `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/`

### Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block37_post_block36_supervisor_yield_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_block37_post_block36_supervisor_yield_checkpoint.py
# SUMMARY: PASS=13 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=375 FAIL=0
bash docs/audit/scripts/run_pipeline.sh
# OK, final rerun newly seeded=0, re-audit required=0, 5 known warnings
python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings
```

### Claim boundary

Actual current surface remains open.  This block is routing-only and should
yield until one explicit bridge input lands: accepted same-surface `O_H`/action
plus strict `C_ss/C_sH/C_HH` rows, strict W/Z accepted-action response packet,
or neutral H3/H4 physical-transfer authority.
