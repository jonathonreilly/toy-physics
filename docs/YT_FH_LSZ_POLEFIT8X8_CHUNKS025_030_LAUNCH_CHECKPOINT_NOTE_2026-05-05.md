# PR #230 FH/LSZ Polefit8x8 Chunks025-030 Launch Checkpoint

Status: run-control support only.

After chunks019-024 were packaged, the global FH/LSZ production collision
guard reported zero active production workers and allowed a new launch:

```text
python3 scripts/frontier_yt_fh_lsz_global_production_collision_guard.py
# SUMMARY: PASS=8 FAIL=0
```

The polefit8x8 orchestrator then launched chunks025-030 from the repo cwd with
fixed seeds `2026051925` through `2026051930`, selected mass `0.75`, eight
scalar two-point modes, x8 noise, and isolated production output directories:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_wave_orchestrator.py --start-index 25 --end-index 30 --max-concurrent 6 --global-max-production-jobs 6 --runtime-minutes 0 --poll-seconds 60 --launch --status-output outputs/yt_fh_lsz_polefit8x8_chunks025_030_launch_status_2026-05-05.json
```

Post-launch status:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_wave_orchestrator.py --start-index 25 --end-index 30 --max-concurrent 6 --global-max-production-jobs 6 --dry-run --status-output outputs/yt_fh_lsz_polefit8x8_chunks025_030_post_launch_status_2026-05-05.json
# running=[25, 26, 27, 28, 29, 30] missing=0 all_jobs=6
```

This checkpoint is not evidence.  Running processes, scheduler return status,
logs, and chunk-local output directories do not count toward PR #230.  Chunks
025-030 can be counted only after their root JSON artifacts land and pass the
polefit8x8 combiner, postprocessor, retained-route, campaign-status, and full
assembly gates.  No retained or proposed-retained top-Yukawa closure is
authorized.

Next action: do not launch additional FH/LSZ workers while these six jobs are
active.  When root artifacts for chunks025-030 exist, package them through the
same polefit8x8 support-only gate chain.
