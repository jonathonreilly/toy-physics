# [physics-loop] PR230 W/Z physical-response packet intake - no-go/open

## Summary

Adds `YT_PR230_WZ_PHYSICAL_RESPONSE_PACKET_INTAKE_CHECKPOINT`.

After block10 left the neutral primitive aperture open, this block checks the
current branch for the strict W/Z physical-response packet.  The intake finds
only scout/schema rows and support contracts.  Accepted action, canonical
`O_H`/sector-overlap authority, production W/Z rows, same-source top rows,
matched covariance, strict non-observed `g2`, `delta_perp` authority, and final
W-response rows are absent.

## Artifacts

- `scripts/frontier_yt_pr230_wz_physical_response_packet_intake_checkpoint.py`
- `outputs/yt_pr230_wz_physical_response_packet_intake_checkpoint_2026-05-07.json`
- `docs/YT_PR230_WZ_PHYSICAL_RESPONSE_PACKET_INTAKE_CHECKPOINT_NOTE_2026-05-07.md`
- `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/`

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_wz_physical_response_packet_intake_checkpoint.py scripts/frontier_yt_pr230_campaign_status_certificate.py
python3 scripts/frontier_yt_pr230_wz_physical_response_packet_intake_checkpoint.py
# SUMMARY: PASS=10 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=350 FAIL=0
```

## Claim Boundary

Actual current-surface status is exact negative boundary / open.  No retained
or `proposed_retained` wording is authorized.

The block does not promote scout/smoke rows to production evidence, does not
use static EW algebra as response rows, does not assume `k_top = k_gauge` or
top/W covariance, does not use forbidden observed or normalization shortcuts,
does not relabel `C_sx/C_xx` as `C_sH/C_HH`, and does not touch the live chunk
worker.

## Next Action

Continue only with a fresh same-surface `O_H` certificate plus production
`C_ss/C_sH/C_HH` pole rows, or a strict W/Z physical-response packet with
accepted action, production rows, matched covariance, strict `g2`,
`delta_perp` authority, and final W-response rows.
