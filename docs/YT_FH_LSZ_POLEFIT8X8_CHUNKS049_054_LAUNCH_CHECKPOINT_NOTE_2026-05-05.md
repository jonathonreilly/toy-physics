# PR #230 FH/LSZ Polefit8x8 Chunks049-054 Launch Checkpoint

Status: run-control support only.

After chunks043-048 were packaged, a fresh global FH/LSZ production collision
guard reported zero active workers and allowed another launch.  The polefit8x8
orchestrator then launched chunks049-054 from the repo cwd with fixed seeds
`2026051949` through `2026051954`, selected mass `0.75`, eight scalar
two-point modes, x8 noise, and isolated production output directories:

```text
python3 scripts/frontier_yt_fh_lsz_polefit8x8_wave_orchestrator.py --start-index 49 --end-index 54 --max-concurrent 6 --global-max-production-jobs 6 --runtime-minutes 1 --poll-seconds 60 --launch --run-gates --status-output outputs/yt_fh_lsz_polefit8x8_chunks049_054_launch_status_2026-05-05.json
# poll=2 completed=0 running=[49, 50, 51, 52, 53, 54] missing=0 all_jobs=6 launched_total=6
```

The launch record reports PIDs `79327` through `79332`, no missing chunks,
and root output paths for chunks049-054.  A post-launch collision guard refresh
records the intended global cap state:

```text
python3 scripts/frontier_yt_fh_lsz_global_production_collision_guard.py
# SUMMARY: PASS=8 FAIL=0
# active_workers=6 global_cap=6 launch_guard_allows_new_workers=false
```

This checkpoint is not evidence.  Running processes, scheduler return status,
logs, chunk-local output directories, launch status JSON, and post-launch
occupancy do not count toward PR #230.  Chunks049-054 can be counted only
after their root JSON artifacts land and pass the polefit8x8 combiner,
postprocessor, retained-route, campaign-status, and full assembly gates.  No
retained or proposed-retained top-Yukawa closure is authorized.

Next action: do not launch additional FH/LSZ workers while these six jobs are
active.  When root artifacts for chunks049-054 exist, package them through the
same polefit8x8 support-only gate chain.
