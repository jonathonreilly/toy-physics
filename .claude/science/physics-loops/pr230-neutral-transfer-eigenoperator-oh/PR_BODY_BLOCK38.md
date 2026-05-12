## PR230 Block38 Bridge Stuck-Fanout Checkpoint

This update adds `YT_PR230_BLOCK38_BRIDGE_STUCK_FANOUT_CHECKPOINT`.

It resumes after block37 on the current PR head after the block42/block43
timeseries boundaries and the block44 Euclidean source-Higgs row absence
boundary, and does not touch the live chunk worker.  The block does not rerun
the block37 absence checkpoint as new proof.  It consumes five
priority frames around the canonical `O_H` / source-Higgs bridge and W/Z
accepted-action fallback:

- degree-one `O_H` action premise;
- same-source EW action adoption;
- same-surface neutral multiplicity-one intake;
- taste-condensate `O_H` bridge;
- W/Z absolute-authority response.

All five frames remain support-only or exact current-surface boundaries.  The
current surface still lacks accepted same-surface `O_H`/action plus strict
`C_ss/C_sH/C_HH` rows, and also lacks a strict W/Z physical-response packet
with accepted action, production rows, same-source top rows, matched
covariance, strict non-observed `g2`, `delta_perp`, and final W-response rows.

## Claim Status

```yaml
actual_current_surface_status: open / block38 bridge stuck-fanout checkpoint
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

No retained or `proposed_retained` wording is authorized.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block38_bridge_stuck_fanout_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_block38_bridge_stuck_fanout_checkpoint.py
# SUMMARY: PASS=16 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=379 FAIL=0
```

Next exact action: supply one explicit missing artifact: accepted same-surface
`O_H`/action plus strict `C_ss/C_sH/C_HH` rows, or a strict W/Z
physical-response packet with accepted action, production rows, same-source top
rows, matched covariance, strict non-observed `g2`, `delta_perp`, and final
W-response rows.
