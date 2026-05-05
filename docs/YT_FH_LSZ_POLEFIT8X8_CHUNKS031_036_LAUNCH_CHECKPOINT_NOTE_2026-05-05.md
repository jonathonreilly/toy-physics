# PR #230 FH/LSZ Polefit8x8 Chunks031-036 Launch Checkpoint

Status: run-control support only.

After chunks025-030 were packaged, the global FH/LSZ production collision
guard reported capacity for the next polefit8x8 wave.  The polefit8x8
orchestrator then launched chunks031-036 from the repo cwd with fixed seeds
`2026051931` through `2026051936`, selected mass `0.75`, eight scalar
two-point modes, x8 noise, and isolated production output directories:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_wave_orchestrator.py --start-index 31 --end-index 36 --max-concurrent 6 --global-max-production-jobs 6 --runtime-minutes 1 --poll-seconds 60 --launch --status-output outputs/yt_fh_lsz_polefit8x8_chunks031_036_launch_status_2026-05-05.json
# poll=2 completed=0 running=[31, 32, 33, 34, 35, 36] missing=0 all_jobs=6 launched_total=6
```

The launch record reports PIDs `4430` through `4435`, no missing chunks, and
root output paths for chunks031-036.  A post-launch collision guard refresh now
records the intended global cap state:

```text
python3 scripts/frontier_yt_fh_lsz_global_production_collision_guard.py
# SUMMARY: PASS=8 FAIL=0
# active_workers=6 global_cap=6 launch_guard_allows_new_workers=false
```

This checkpoint is not evidence.  Running processes, scheduler return status,
logs, chunk-local output directories, launch status JSON, and post-launch
occupancy do not count toward PR #230.  Chunks031-036 can be counted only after
their root JSON artifacts land and pass the polefit8x8 combiner,
postprocessor, retained-route, campaign-status, and full assembly gates.  No
retained or proposed-retained top-Yukawa closure is authorized.

Next action: do not launch additional FH/LSZ workers while these six jobs are
active.  When root artifacts for chunks031-036 exist, package them through the
same polefit8x8 support-only gate chain.
