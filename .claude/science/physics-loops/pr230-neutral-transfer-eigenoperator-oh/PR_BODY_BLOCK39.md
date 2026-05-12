## PR230 Block39 Post-Block38 Queue-Admission Checkpoint

This update adds `YT_PR230_BLOCK39_POST_BLOCK38_QUEUE_ADMISSION_CHECKPOINT`.

It resumes after block38, consumes the lane-1 Block45 Euclidean row boundary,
the post-Block45 neutral off-diagonal applicability boundary, and the top
mass-scan subtraction-contract boundary plus the higher-shell source-Higgs
operator boundary.  It does not touch the live chunk worker and does not rerun
block38 as new evidence.  The checkpoint pivots through the ranked queue:

- source-Higgs remains first priority but is not admitted after Block45,
  because ordinary tau-keyed top/scalar-source correlators and reduced
  source-Higgs smoke are not physical Euclidean `C_ss/C_sH/C_HH(tau)` pole
  rows, and higher-shell cross rows remain taste-radial second-source rows
  rather than canonical `O_H` rows;
- W/Z accepted-action physical response is the selected fallback but is not
  admitted without accepted action, production W/Z rows, same-source top rows,
  matched covariance, strict non-observed `g2`, `delta_perp`, and final
  W-response rows; the top mass-scan boundary does not supply additive-top
  subtraction authority;
- neutral H3/H4 remains blocked without physical-transfer and
  source/canonical-Higgs coupling authority, and the post-Block45 neutral
  off-diagonal audit does not reopen that route.

## Claim Status

```yaml
actual_current_surface_status: open / block39 post-block38 queue-admission checkpoint
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

No retained or `proposed_retained` wording is authorized.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block39_post_block38_queue_admission_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_block39_post_block38_queue_admission_checkpoint.py
# SUMMARY: PASS=16 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=383 FAIL=0
```

Next exact action: supply accepted same-surface `O_H`/action plus physical
Euclidean `C_ss/C_sH/C_HH(tau)` rows with Gram/FV/IR authority, or a strict W/Z
physical-response packet with accepted action, production rows, matched
covariance, strict non-observed `g2`, `delta_perp`, and final W-response rows.
