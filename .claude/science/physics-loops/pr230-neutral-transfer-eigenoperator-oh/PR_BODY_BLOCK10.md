# [physics-loop] PR230 neutral primitive H3/H4 aperture checkpoint - bounded-support/open

## Summary

Adds `YT_PR230_NEUTRAL_PRIMITIVE_H3H4_APERTURE_CHECKPOINT`.

After the source-Higgs bridge aperture stayed open at block09, this block
pivots to the next ranked neutral primitive route.  It verifies that H1/H2 Z3
support is loaded, then checks the current `44/63` two-source taste-radial
`C_sx/C_xx` row prefix against the missing H3/H4 obligations.

Result: bounded support / exact boundary.  The finite rows are useful staging
evidence, but they are not physical transfer/action matrices,
primitive-cone certificates, off-diagonal generators, canonical `O_H`, or
`C_sH/C_HH` pole rows.  `proposal_allowed=false`.

## Artifacts

- `scripts/frontier_yt_pr230_neutral_primitive_h3h4_aperture_checkpoint.py`
- `outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json`
- `docs/YT_PR230_NEUTRAL_PRIMITIVE_H3H4_APERTURE_CHECKPOINT_NOTE_2026-05-07.md`
- `scripts/frontier_yt_pr230_campaign_status_certificate.py`
- `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`
- `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/`

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_neutral_primitive_h3h4_aperture_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_neutral_primitive_h3h4_aperture_checkpoint.py
# SUMMARY: PASS=9 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=348 FAIL=0
bash docs/audit/scripts/run_pipeline.sh
# OK, 5 known warnings
python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings
git diff --check
# OK
```

## Next Action

Consume a real missing artifact: W/Z physical-response rows with accepted
action, sector-overlap, matched covariance, and strict non-observed `g2`; or a
fresh same-surface canonical `O_H` plus production `C_ss/C_sH/C_HH` Gram-flat
row packet.  Do not reopen the neutral primitive route without a same-surface
H3/H4 certificate.
