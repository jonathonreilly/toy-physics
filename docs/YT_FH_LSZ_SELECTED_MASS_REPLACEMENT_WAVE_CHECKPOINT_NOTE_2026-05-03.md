# PR #230 FH/LSZ Selected-Mass Replacement Wave Checkpoint

**Status:** bounded-support / target-timeseries replacement wave complete  
**Runners:** `scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py`, `scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py`, `scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py`  
**Certificates:** `outputs/yt_fh_lsz_chunk004_target_timeseries_generic_checkpoint_2026-05-02.json` through `outputs/yt_fh_lsz_chunk010_target_timeseries_generic_checkpoint_2026-05-02.json`, `outputs/yt_fh_lsz_target_timeseries_replacement_queue_2026-05-02.json`, `outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json`

## Result

Chunk004 completed as a pre-optimization target-timeseries replacement that
was already running when the speedup patch landed. Chunks005-010 were then
rerun with the selected-mass FH/LSZ and normal-cache optimization, using fixed
seeds, chunk-isolated output directories, and no `--resume`.

Concurrency was capped at 3 workers to avoid colliding on chunk outputs while
still materially speeding the replacement campaign.

```text
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 4
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 5
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 6
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 7
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 8
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 9
python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 10
# each: SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py
# SUMMARY: PASS=9 FAIL=0
```

This checkpoint made the ready target-timeseries set chunks001-012 and emptied
the replacement queue.  The later chunk013-016 target-ESS wave supersedes this
as the current ready set, raising it to chunks001-016.

## Claim Boundary

This is production-processing support only. It does not certify target ESS,
response stability, combined L12/L16/L24 production, scalar-pole
derivative/model-class/FV/IR control, or canonical-Higgs identity. It does not
derive or set `kappa_s`, does not identify the source pole with the canonical
Higgs radial mode, and authorizes no retained or `proposed_retained` wording.

## Next Action

The target-observable ESS certificate has since passed for chunks001-016.
Continue response stability and scalar-pole postprocessing only as support. In
parallel, continue the higher-closure-probability identity routes:
same-surface `C_sH`/`C_HH`, a canonical-Higgs source identity theorem, or real
W/Z response rows with sector-overlap identity.
