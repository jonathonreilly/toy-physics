# [physics-loop] PR230 source-Higgs bridge aperture checkpoint - bounded-support/open

## Block

Adds `YT_PR230_SOURCE_HIGGS_BRIDGE_APERTURE_CHECKPOINT`.

Artifacts:

- `scripts/frontier_yt_pr230_source_higgs_bridge_aperture_checkpoint.py`
- `outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json`
- `docs/YT_PR230_SOURCE_HIGGS_BRIDGE_APERTURE_CHECKPOINT_NOTE_2026-05-07.md`
- updated `scripts/frontier_yt_pr230_campaign_status_certificate.py`
- updated loop pack under `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/`

## Result

The completed `001-044` two-source taste-radial chunks are bounded staging
support only.  They remain `C_sx/C_xx` rows, not canonical `C_sH/C_HH` pole
rows, and do not close canonical `O_H`, scalar-LSZ/FV authority, or Gram
flatness.

`proposal_allowed=false`; independent audit remains required before any
effective retained/proposed-retained status could be considered.

## Checks

```bash
python3 -m py_compile scripts/frontier_yt_pr230_source_higgs_bridge_aperture_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_source_higgs_bridge_aperture_checkpoint.py
# SUMMARY: PASS=18 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=347 FAIL=0
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings
```
