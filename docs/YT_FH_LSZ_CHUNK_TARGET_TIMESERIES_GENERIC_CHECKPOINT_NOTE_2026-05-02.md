# PR #230 FH/LSZ Generic Chunk Target-Timeseries Checkpoint

**Status:** bounded-support / reusable target-timeseries checkpoint
**Runner:** `scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py`
**Certificate:** `outputs/yt_fh_lsz_chunk011_target_timeseries_generic_checkpoint_2026-05-02.json`

## Purpose

Future FH/LSZ chunks should not need one-off checkpoint runners.  This block
adds a reusable runner that audits any completed `L12_T24_chunkNNN` output for
the production metadata, seed control, same-source FH/LSZ rows, and
per-configuration target time series required before the target ESS gate can
even be evaluated.

## Result

```text
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 11
# SUMMARY: PASS=14 FAIL=0
```

The generic runner reproduces the chunk011 target-timeseries support result:
chunk011 has production-phase metadata, `numba_gauge_seed_v1` seed control,
same-source `dE/ds`, same-source `C_ss(q)`, and target time series for source
response plus scalar LSZ modes.

## Claim Boundary

This is a processing harness, not retained or proposed-retained closure.  A
single L12 chunk remains partial support only.  Target ESS, response stability,
completed L12/L16/L24 production, scalar-pole derivative/model-class/FV/IR
gates, and canonical-Higgs identity remain required.

## Next Action

After chunk012 completes, rerun the combiner, ready-set, response-stability,
autocorrelation/ESS, and this generic checkpoint with `--chunk-index 12`.
