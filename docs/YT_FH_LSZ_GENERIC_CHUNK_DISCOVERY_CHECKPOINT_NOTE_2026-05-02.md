# PR #230 FH/LSZ Generic Chunk Discovery Checkpoint

**Status:** bounded-support / closure-certificate discovery support
**Runners:** `scripts/frontier_yt_retained_closure_route_certificate.py`, `scripts/frontier_yt_pr230_campaign_status_certificate.py`
**Certificates:** `outputs/yt_retained_closure_route_certificate_2026-05-01.json`, `outputs/yt_pr230_campaign_status_certificate_2026-05-01.json`

## Purpose

The reusable FH/LSZ target-timeseries checkpoint emits one certificate per
chunk.  Retained-route and campaign-status runners should not require a static
edit every time a new `yt_fh_lsz_chunkNNN_target_timeseries_generic_checkpoint`
file is created.

This block updates both runners to discover those generic chunk certificates
by glob, load them into the campaign surface, and record an aggregate
discovery check.

## Result

```text
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=106 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=132 FAIL=0
```

The aggregate discovery row currently sees two generic target-timeseries chunk
certificates: chunk011 and chunk012.

## Claim Boundary

Automatic discovery is claim hygiene and processing support only.  It does not
promote generic chunk checkpoints, 12/63 L12 chunks, target-series presence,
or partial production rows to retained or `proposed_retained` evidence.  The
route still requires target-observable ESS, response stability, completed
L12/L16/L24 production, scalar-pole derivative/model-class/FV/IR gates, and
canonical-Higgs identity.

## Next Action

Continue target-timeseries chunks.  After each completed chunk, rerun the
combiner, ready-set, response-stability, autocorrelation/ESS, generic chunk
checkpoint, retained-route certificate, and campaign-status certificate.
