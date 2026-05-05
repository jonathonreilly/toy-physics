# PR #230 FH/LSZ Polefit8x8 Chunks043-048 Launch Checkpoint

Status: run-control support only.

After chunks037-042 were packaged, the global FH/LSZ production collision
guard reported zero active workers and allowed another launch.  The polefit8x8
orchestrator then launched chunks043-048 from the repo cwd with fixed seeds
`2026051943` through `2026051948`, selected mass `0.75`, eight scalar
two-point modes, x8 noise, and isolated production output directories:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_wave_orchestrator.py --start-index 43 --end-index 48 --max-concurrent 6 --global-max-production-jobs 6 --runtime-minutes 1 --poll-seconds 60 --launch --run-gates --status-output outputs/yt_fh_lsz_polefit8x8_chunks043_048_launch_status_2026-05-05.json
# poll=2 completed=0 running=[43, 44, 45, 46, 47, 48] missing=0 all_jobs=6 launched_total=6
```

The launch record reports PIDs `16475` through `16480`, no missing chunks,
and root output paths for chunks043-048.  A post-launch collision guard refresh
records the intended global cap state:

```text
python3 scripts/frontier_yt_fh_lsz_global_production_collision_guard.py
# SUMMARY: PASS=8 FAIL=0
# active_workers=6 global_cap=6 launch_guard_allows_new_workers=false
```

This checkpoint is not evidence.  Running processes, scheduler return status,
logs, chunk-local output directories, launch status JSON, and post-launch
occupancy do not count toward PR #230.  Chunks043-048 can be counted only
after their root JSON artifacts land and pass the polefit8x8 combiner,
postprocessor, retained-route, campaign-status, and full assembly gates.  No
retained or proposed-retained top-Yukawa closure is authorized.

Next action: do not launch additional FH/LSZ workers while these six jobs are
active.  When root artifacts for chunks043-048 exist, package them through the
same polefit8x8 support-only gate chain.
